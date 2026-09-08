"""FABRIC-AI Production Optimizer benchmark v1.2.

Implements the frozen prepare, evaluate and rank contracts from
src/ai/fabric_ai_optimizer/FABRIC-AI_Production_Optimizer_SPEC_v1.2.md.
COBRA imports are delayed so the rank subcommand remains pandas-only.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import platform
import statistics
import sys
import time
from pathlib import Path
from typing import Any, Iterable

import pandas as pd


BIOMASS = "r_2111"
PRODUCT = "FABRIC_r_4799"
EPS = 1e-12


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def import_cobra_local(runtime_root: Path):
    import appdirs

    cache = runtime_root / ".runtime" / "cobrapy"
    cache.mkdir(parents=True, exist_ok=True)
    appdirs.user_cache_dir = lambda *args, **kwargs: str(cache)
    import cobra

    return cobra


def load_condition(path: Path) -> dict[str, Any]:
    condition = load_json(path)
    if "condition_id" not in condition or "bounds" not in condition:
        raise ValueError(f"invalid condition contract: {path}")
    condition["_path"] = str(path.resolve())
    return condition


def apply_condition(model, condition: dict[str, Any]) -> list[dict[str, Any]]:
    applied = []
    for row in condition["bounds"]:
        reaction = model.reactions.get_by_id(row["reaction"])
        before = [float(reaction.lower_bound), float(reaction.upper_bound)]
        if "lower_bound" in row:
            reaction.lower_bound = float(row["lower_bound"])
        if "upper_bound" in row:
            reaction.upper_bound = float(row["upper_bound"])
        applied.append(
            {
                "reaction": reaction.id,
                "before": before,
                "after": [float(reaction.lower_bound), float(reaction.upper_bound)],
            }
        )
    return applied


def load_model(model_path: Path, condition: dict[str, Any], tol: float):
    cobra = import_cobra_local(model_path.parent)
    model = cobra.io.load_json_model(str(model_path))
    model.solver = "glpk"
    tolerance_obj = model.solver.configuration.tolerances
    readback: dict[str, float | None] = {}
    for name in ("feasibility", "optimality", "integrality"):
        if not hasattr(tolerance_obj, name):
            readback[name] = None
            continue
        try:
            setattr(tolerance_obj, name, tol)
        except (AttributeError, ValueError):
            pass
        value = getattr(tolerance_obj, name, None)
        readback[name] = None if value is None else float(value)
    model.solver.configuration.presolve = True
    applied = apply_condition(model, condition)
    return cobra, model, readback, applied


def fresh_optimize(model, reaction_id: str, direction: str):
    import swiglpk

    model.objective = reaction_id
    model.objective_direction = direction
    model.solver.configuration.presolve = True
    model.solver.update()
    swiglpk.glp_std_basis(model.solver.problem)
    return model.optimize()


def reuse_objective_optimize(model, reaction_id: str, direction: str):
    """Reuse an LP basis only when constraints and bounds are unchanged."""
    model.objective = reaction_id
    model.objective_direction = direction
    model.solver.configuration.presolve = False
    return model.optimize()


def build_highs_growth_solver(model, tol: float):
    """Build a fresh/presolved HiGHS LP factory for gene-KO growth admission."""
    import numpy as np
    import scipy
    from scipy.optimize import linprog
    from cobra.util.array import create_stoichiometric_matrix

    reaction_ids = [reaction.id for reaction in model.reactions]
    reaction_index = {reaction_id: index for index, reaction_id in enumerate(reaction_ids)}
    stoichiometry = create_stoichiometric_matrix(model, array_type="lil").tocsr()
    rhs = np.zeros(stoichiometry.shape[0], dtype=float)
    base_bounds = [tuple(map(float, reaction.bounds)) for reaction in model.reactions]
    objective = np.zeros(len(reaction_ids), dtype=float)
    objective[reaction_index[BIOMASS]] = -1.0

    def solve(disabled_reactions: Iterable[str]):
        bounds = list(base_bounds)
        for reaction_id in disabled_reactions:
            bounds[reaction_index[reaction_id]] = (0.0, 0.0)
        result = linprog(
            objective,
            A_eq=stoichiometry,
            b_eq=rhs,
            bounds=bounds,
            method="highs",
            options={
                "presolve": True,
                "primal_feasibility_tolerance": tol,
                "dual_feasibility_tolerance": tol,
            },
        )
        status = (
            "optimal"
            if result.success
            else "infeasible"
            if result.status == 2
            else f"highs_status_{result.status}"
        )
        if not result.success:
            return status, math.nan, False, math.nan, math.nan, str(result.message)
        flux = result.x
        growth = clamp_zero(float(flux[reaction_index[BIOMASS]]), tol)
        finite = bool(np.isfinite(flux).all())
        mass = float(np.max(np.abs(stoichiometry.dot(flux))))
        lower = np.array([bound[0] for bound in bounds], dtype=float)
        upper = np.array([bound[1] for bound in bounds], dtype=float)
        bound = float(max(np.max(lower - flux), np.max(flux - upper), 0.0))
        return status, growth, finite, mass, bound, str(result.message)

    return solve, {
        "solver": "scipy.optimize.linprog(method=highs)",
        "scipy_version": scipy.__version__,
        "presolve": True,
        "primal_feasibility_tolerance": tol,
        "dual_feasibility_tolerance": tol,
    }


def build_highs_evaluation_solver(model, tol: float):
    """Return a fresh/presolved LP solve function for independent evaluation."""
    import numpy as np
    import scipy
    from scipy.optimize import linprog
    from cobra.util.array import create_stoichiometric_matrix

    reaction_ids = [reaction.id for reaction in model.reactions]
    reaction_index = {reaction_id: index for index, reaction_id in enumerate(reaction_ids)}
    stoichiometry = create_stoichiometric_matrix(model, array_type="lil").tocsr()
    rhs = np.zeros(stoichiometry.shape[0], dtype=float)
    base_bounds = [tuple(map(float, reaction.bounds)) for reaction in model.reactions]

    def solve(
        disabled_reactions: Iterable[str],
        objective_reaction: str,
        direction: str,
        biomass_floor: float | None = None,
    ):
        bounds = list(base_bounds)
        for reaction_id in disabled_reactions:
            bounds[reaction_index[reaction_id]] = (0.0, 0.0)
        if biomass_floor is not None:
            biomass_index = reaction_index[BIOMASS]
            lower, upper = bounds[biomass_index]
            bounds[biomass_index] = (max(lower, float(biomass_floor)), upper)
        objective = np.zeros(len(reaction_ids), dtype=float)
        sign = -1.0 if direction == "max" else 1.0
        objective[reaction_index[objective_reaction]] = sign
        result = linprog(
            objective,
            A_eq=stoichiometry,
            b_eq=rhs,
            bounds=bounds,
            method="highs",
            options={
                "presolve": True,
                "primal_feasibility_tolerance": tol,
                "dual_feasibility_tolerance": tol,
            },
        )
        status = (
            "optimal"
            if result.success
            else "infeasible"
            if result.status == 2
            else f"highs_status_{result.status}"
        )
        if not result.success:
            return status, math.nan, False, math.nan, math.nan, str(result.message)
        flux = result.x
        value = clamp_zero(float(flux[reaction_index[objective_reaction]]), tol)
        finite = bool(np.isfinite(flux).all())
        mass = float(np.max(np.abs(stoichiometry.dot(flux))))
        lower = np.array([bound[0] for bound in bounds], dtype=float)
        upper = np.array([bound[1] for bound in bounds], dtype=float)
        bound = float(max(np.max(lower - flux), np.max(flux - upper), 0.0))
        return status, value, finite, mass, bound, str(result.message)

    return solve, {
        "solver": "scipy.optimize.linprog(method=highs)",
        "scipy_version": scipy.__version__,
        "presolve": True,
        "primal_feasibility_tolerance": tol,
        "dual_feasibility_tolerance": tol,
    }


def clamp_zero(value: float, tol: float) -> float:
    if abs(value) <= tol:
        return 0.0
    return value


def metric_equivalent(value: float, tol: float) -> float:
    if abs(value) <= tol:
        return 0.0
    if abs(value - 1.0) <= tol:
        return 1.0
    return value


def native_objective_equivalent_ratio(
    mutant_value: float,
    wt_value: float,
    recorded_ratio: float,
    tol: float,
    *,
    metric: str,
    gene: str,
    condition: str,
) -> tuple[float, bool]:
    """Return a ranking ratio after comparing objectives in native solver units."""
    if not (math.isfinite(mutant_value) and math.isfinite(wt_value)):
        if math.isfinite(recorded_ratio):
            raise ValueError(
                f"{metric} native objective unavailable for finite recorded ratio: "
                f"gene={gene}, condition={condition}"
            )
        return math.nan, False
    delta = mutant_value - wt_value
    if delta > tol:
        raise ValueError(
            f"{metric} native objective exceeds WT by more than tolerance: "
            f"gene={gene}, condition={condition}, delta={delta:.17g}, tol={tol:.17g}"
        )
    if abs(delta) <= tol:
        return 1.0, True
    if not math.isfinite(recorded_ratio):
        raise ValueError(
            f"{metric} recorded ratio unavailable for non-equivalent native objectives: "
            f"gene={gene}, condition={condition}"
        )
    return recorded_ratio, False


def diagnostics(model, solution) -> tuple[bool, float, float]:
    if solution.status != "optimal":
        return False, math.nan, math.nan
    values = solution.fluxes
    finite = bool(all(math.isfinite(float(value)) for value in values.values))
    mass = 0.0
    for metabolite in model.metabolites:
        primal = metabolite.constraint.primal
        if primal is not None:
            mass = max(mass, abs(float(primal)))
    bound = 0.0
    for reaction in model.reactions:
        value = float(values[reaction.id])
        bound = max(
            bound,
            max(0.0, float(reaction.lower_bound) - value, value - float(reaction.upper_bound)),
        )
    return finite, mass, bound


def condition_protected_ids(condition: dict[str, Any]) -> list[str]:
    source = condition.get("protected_reaction_ids_file")
    if not source:
        raise ValueError("condition does not name the frozen protected-reaction file")
    path = (Path(condition["_path"]).parent / source).resolve()
    payload = load_json(path)
    return sorted(payload["reaction_ids"])


def command_prepare(args: argparse.Namespace) -> int:
    started = time.perf_counter()
    model_path = Path(args.model).resolve()
    condition_path = Path(args.condition).resolve()
    outdir = Path(args.outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    condition = load_condition(condition_path)
    cobra, model, tolerance_readback, applied = load_model(model_path, condition, args.tol)
    model_hash = sha256_file(model_path)
    protected = set(condition_protected_ids(condition))

    root = fresh_optimize(model, BIOMASS, "max")
    if root.status != "optimal":
        raise RuntimeError(f"WT growth solve failed: {root.status}")
    wt_growth = float(root.fluxes[BIOMASS])
    growth_floor = 0.1 * wt_growth

    gene_associated_internal = sorted(
        reaction.id for reaction in model.reactions if reaction.genes and reaction.id not in protected
    )
    fva_rows = []
    blocked: list[str] = []
    solver_failures = 0
    with model:
        biomass = model.reactions.get_by_id(BIOMASS)
        biomass.lower_bound = max(float(biomass.lower_bound), growth_floor)
        for index, reaction_id in enumerate(gene_associated_internal, start=1):
            minimum_solution = reuse_objective_optimize(model, reaction_id, "min")
            maximum_solution = reuse_objective_optimize(model, reaction_id, "max")
            min_status = minimum_solution.status
            max_status = maximum_solution.status
            minimum = float(minimum_solution.fluxes[reaction_id]) if min_status == "optimal" else math.nan
            maximum = float(maximum_solution.fluxes[reaction_id]) if max_status == "optimal" else math.nan
            if min_status != "optimal" or max_status != "optimal":
                solver_failures += 1
            is_blocked = bool(
                min_status == "optimal"
                and max_status == "optimal"
                and abs(minimum) <= args.tol
                and abs(maximum) <= args.tol
            )
            if is_blocked:
                blocked.append(reaction_id)
            fva_rows.append(
                {
                    "reaction": reaction_id,
                    "minimum": minimum,
                    "maximum": maximum,
                    "minimum_status": min_status,
                    "maximum_status": max_status,
                    "blocked_at_tol": is_blocked,
                }
            )
            if index % 250 == 0:
                print(f"prepare FVA {index}/{len(gene_associated_internal)}", flush=True)

    with (outdir / "reaction_fva.csv").open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fva_rows[0]) if fva_rows else ["reaction"])
        writer.writeheader()
        writer.writerows(fva_rows)

    blocked_set = set(blocked)
    highs_growth, highs_info = build_highs_growth_solver(model, args.tol)
    footprints: dict[str, list[str]] = {}
    admitted: list[str] = []
    audit_rows = []
    for index, gene in enumerate(sorted(model.genes, key=lambda item: item.id), start=1):
        with model:
            gene.knock_out()
            effective = sorted(
                reaction.id
                for reaction in gene.reactions
                if not reaction.functional
            )
        reason = ""
        mutant_growth = math.nan
        status = "not_solved"
        finite = False
        mass_residual = math.nan
        bound_residual = math.nan
        solver_message = "not_solved"
        if not effective:
            reason = "empty_effective_footprint"
        elif set(effective) & protected:
            reason = "protected_reaction_in_footprint"
        elif not (set(effective) - blocked_set):
            reason = "no_unblocked_internal_reaction"
        else:
            status, mutant_growth, finite, mass_residual, bound_residual, solver_message = highs_growth(effective)
            if status != "optimal" or not finite:
                reason = "mutant_growth_solver_failure"
            elif mass_residual > args.tol or bound_residual > args.tol:
                reason = "mutant_growth_residual_failure"
            elif mutant_growth + args.tol < growth_floor:
                reason = "mutant_growth_below_0.1_WT"
            else:
                reason = "eligible"
                admitted.append(gene.id)
                footprints[gene.id] = effective
        audit_rows.append(
            {
                "gene": gene.id,
                "footprint": ";".join(effective),
                "footprint_size": len(effective),
                "mutant_growth": mutant_growth,
                "solver_status": status,
                "finite": finite,
                "mass_balance_residual": mass_residual,
                "bound_residual": bound_residual,
                "solver_message": solver_message,
                "admission_reason": reason,
            }
        )
        if index % 250 == 0:
            print(f"prepare admission {index}/{len(model.genes)}", flush=True)

    with (outdir / "gene_admission_audit.csv").open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(audit_rows[0]))
        writer.writeheader()
        writer.writerows(audit_rows)

    elapsed = time.perf_counter() - started
    candidate_space = {
        "genes": admitted,
        "footprints": footprints,
        "model_sha256": model_hash,
        "condition_id": condition["condition_id"],
        "condition_sha256": sha256_file(condition_path),
        "excluded_reaction_ids": sorted(protected),
        "blocked_reaction_ids": blocked,
        "elapsed_seconds": elapsed,
        "native_genes_total": len(model.genes),
        "eligible_count": len(admitted),
        "rules": "FABRIC-AI Production Optimizer SPEC v1.2 sections 3, 4, 16, 17",
        "gene_growth_solver": "fresh SciPy/HiGHS LP with presolve enabled for every knockout",
    }
    write_json(outdir / "candidate_space.json", candidate_space)
    summary = {
        "status": "COMPLETED" if solver_failures == 0 else "COMPLETED_WITH_SOLVER_FAILURES",
        "command": "prepare",
        "condition_id": condition["condition_id"],
        "model_sha256": model_hash,
        "WT_mu_max": wt_growth,
        "growth_admission_floor": growth_floor,
        "gene_associated_internal_fva_count": len(gene_associated_internal),
        "blocked_count": len(blocked),
        "native_genes_total": len(model.genes),
        "eligible_count": len(admitted),
        "solver_failures": solver_failures,
        "wall_time_seconds": elapsed,
        "solver": model.solver.interface.__name__,
        "solver_tolerance_requested": args.tol,
        "solver_tolerance_readback": tolerance_readback,
        "FVA_solver_state": "GLPK basis reuse permitted only across objective switches at fixed bounds",
        "gene_growth_solver_details": highs_info,
        "applied_condition_bounds": applied,
        "cobra_version": cobra.__version__,
        "python": sys.version,
        "platform": platform.platform(),
    }
    write_json(outdir / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False), flush=True)
    return 0


def solve_product_at_floor(model, floor: float, direction: str, tol: float):
    with model:
        biomass = model.reactions.get_by_id(BIOMASS)
        biomass.lower_bound = max(float(biomass.lower_bound), float(floor))
        solution = fresh_optimize(model, PRODUCT, direction)
        if solution.status != "optimal":
            return solution.status, math.nan, False, math.nan, math.nan
        value = clamp_zero(float(solution.fluxes[PRODUCT]), tol)
        finite, mass, bound = diagnostics(model, solution)
        return solution.status, value, finite, mass, bound


def _command_evaluate_glpk_unselected(args: argparse.Namespace) -> int:
    """Retained diagnostic implementation; the v1.2 CLI uses HiGHS evaluation."""
    started = time.perf_counter()
    model_path = Path(args.model).resolve()
    condition_path = Path(args.condition).resolve()
    pool_path = Path(args.pool).resolve()
    outdir = Path(args.outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    floors = [float(value) for value in args.floors.split(",")]
    condition = load_condition(condition_path)
    pool = load_json(pool_path)
    cobra, model, tolerance_readback, applied = load_model(model_path, condition, args.tol)
    model_hash = sha256_file(model_path)
    if str(pool["model_sha256"]).lower() != model_hash.lower():
        raise RuntimeError("pool/model SHA mismatch")

    wt_solution = fresh_optimize(model, BIOMASS, "max")
    if wt_solution.status != "optimal":
        raise RuntimeError(f"WT growth solve failed: {wt_solution.status}")
    wt_growth = float(wt_solution.fluxes[BIOMASS])
    wt_floor_metrics: dict[str, dict[str, Any]] = {}
    for fraction in floors:
        floor = fraction * wt_growth
        min_status, minimum, min_finite, min_mass, min_bound = solve_product_at_floor(model, floor, "min", args.tol)
        max_status, maximum, max_finite, max_mass, max_bound = solve_product_at_floor(model, floor, "max", args.tol)
        wt_floor_metrics[str(fraction)] = {
            "absolute_growth_floor": floor,
            "Pmin": minimum,
            "Pmax": maximum,
            "minimum_status": min_status,
            "maximum_status": max_status,
            "finite": bool(min_finite and max_finite),
            "max_mass_balance_residual": max(min_mass, max_mass),
            "max_bound_residual": max(min_bound, max_bound),
        }

    rows = []
    solver_failures = 0
    infeasible_floors = 0
    max_mass_residual = 0.0
    max_bound_residual = 0.0
    pool_genes = list(pool["genes"])
    for index, gene_id in enumerate(pool_genes, start=1):
        gene = model.genes.get_by_id(gene_id)
        with model:
            gene.knock_out()
            actual_footprint = sorted(
                reaction.id
                for reaction in gene.reactions
                if not reaction.functional
            )
            expected_footprint = sorted(pool["footprints"][gene_id])
            footprint_match = actual_footprint == expected_footprint
            growth_solution = fresh_optimize(model, BIOMASS, "max")
            growth_status = growth_solution.status
            mutant_growth = (
                clamp_zero(float(growth_solution.fluxes[BIOMASS]), args.tol)
                if growth_status == "optimal"
                else math.nan
            )
            if growth_status != "optimal":
                solver_failures += 1
            gr = mutant_growth / wt_growth if math.isfinite(mutant_growth) and wt_growth > EPS else math.nan
            row: dict[str, Any] = {
                "gene": gene_id,
                "condition": condition["condition_id"],
                "footprint": ";".join(expected_footprint),
                "footprint_size": len(expected_footprint),
                "actual_footprint_match": footprint_match,
                "WT_mu_max": wt_growth,
                "mutant_mu_max": mutant_growth,
                "growth_status": growth_status,
                "GR": gr,
            }
            components = []
            for fraction in floors:
                label = f"{fraction:g}"
                absolute_floor = fraction * wt_growth
                if not math.isfinite(mutant_growth) or mutant_growth + args.tol < absolute_floor:
                    row[f"status_{label}"] = "growth_floor_infeasible"
                    row[f"Pmin_{label}"] = math.nan
                    row[f"Pmax_{label}"] = math.nan
                    row[f"PCR_{label}"] = math.nan
                    components.append(0.0)
                    infeasible_floors += 1
                    continue
                min_status, pmin, min_finite, min_mass, min_bound = solve_product_at_floor(
                    model, absolute_floor, "min", args.tol
                )
                max_status, pmax, max_finite, max_mass, max_bound = solve_product_at_floor(
                    model, absolute_floor, "max", args.tol
                )
                if min_status != "optimal" or max_status != "optimal" or not (min_finite and max_finite):
                    solver_failures += 1
                    row[f"status_{label}"] = f"solver_failure:{min_status}/{max_status}"
                    row[f"Pmin_{label}"] = math.nan
                    row[f"Pmax_{label}"] = math.nan
                    row[f"PCR_{label}"] = math.nan
                    components.append(0.0)
                    continue
                max_mass_residual = max(max_mass_residual, min_mass, max_mass)
                max_bound_residual = max(max_bound_residual, min_bound, max_bound)
                denominator = max(float(wt_floor_metrics[str(fraction)]["Pmax"]), EPS)
                row[f"status_{label}"] = "optimal"
                row[f"Pmin_{label}"] = pmin
                row[f"Pmax_{label}"] = pmax
                row[f"PCR_{label}"] = pmax / denominator
                components.append(pmin / denominator)
            row["GCP"] = statistics.mean(components)

            if math.isfinite(mutant_growth):
                near_floor = args.mutant_growth_fraction * mutant_growth
                min_status, pmin95, min_finite, min_mass, min_bound = solve_product_at_floor(
                    model, near_floor, "min", args.tol
                )
                max_status, pmax95, max_finite, max_mass, max_bound = solve_product_at_floor(
                    model, near_floor, "max", args.tol
                )
                if min_status == "optimal" and max_status == "optimal" and min_finite and max_finite:
                    row["Pmin95"] = pmin95
                    row["Pmax95"] = pmax95
                    row["status_95mut"] = "optimal"
                    max_mass_residual = max(max_mass_residual, min_mass, max_mass)
                    max_bound_residual = max(max_bound_residual, min_bound, max_bound)
                else:
                    row["Pmin95"] = math.nan
                    row["Pmax95"] = math.nan
                    row["status_95mut"] = f"solver_failure:{min_status}/{max_status}"
                    solver_failures += 1
            else:
                row["Pmin95"] = math.nan
                row["Pmax95"] = math.nan
                row["status_95mut"] = "mutant_growth_unavailable"
            rows.append(row)
        if index % 50 == 0:
            print(f"evaluate {condition['condition_id']} {index}/{len(pool_genes)}", flush=True)

    dataframe = pd.DataFrame(rows)
    dataframe.to_csv(outdir / "candidate_metrics.csv", index=False, encoding="utf-8-sig")
    elapsed = time.perf_counter() - started
    summary = {
        "status": "COMPLETED" if solver_failures == 0 else "COMPLETED_WITH_SOLVER_FAILURES",
        "command": "evaluate",
        "condition_id": condition["condition_id"],
        "model_sha256": model_hash,
        "pool_sha256": sha256_file(pool_path),
        "pool_count": len(pool_genes),
        "evaluated_count": len(rows),
        "WT_mu_max": wt_growth,
        "WT_floor_metrics": wt_floor_metrics,
        "floors": floors,
        "mutant_growth_fraction": args.mutant_growth_fraction,
        "solver_failures": solver_failures,
        "growth_floor_infeasible_count": infeasible_floors,
        "max_mass_balance_residual": max_mass_residual,
        "max_bound_residual": max_bound_residual,
        "wall_time_seconds": elapsed,
        "solver": model.solver.interface.__name__,
        "solver_tolerance_requested": args.tol,
        "solver_tolerance_readback": tolerance_readback,
        "presolve_readback": bool(model.solver.configuration.presolve),
        "applied_condition_bounds": applied,
        "cobra_version": cobra.__version__,
        "scipy_version": __import__("scipy").__version__,
    }
    write_json(outdir / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False), flush=True)
    return 0


def command_evaluate_highs(args: argparse.Namespace) -> int:
    """Independent evaluator using a fresh presolved HiGHS LP per phenotype."""
    started = time.perf_counter()
    model_path = Path(args.model).resolve()
    condition_path = Path(args.condition).resolve()
    pool_path = Path(args.pool).resolve()
    outdir = Path(args.outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    floors = [float(value) for value in args.floors.split(",")]
    condition = load_condition(condition_path)
    pool = load_json(pool_path)
    cobra, model, tolerance_readback, applied = load_model(model_path, condition, args.tol)
    model_hash = sha256_file(model_path)
    if str(pool["model_sha256"]).lower() != model_hash.lower():
        raise RuntimeError("pool/model SHA mismatch")

    solve, solver_info = build_highs_evaluation_solver(model, args.tol)
    wt_status, wt_growth, wt_finite, wt_mass, wt_bound, wt_message = solve(
        [], BIOMASS, "max"
    )
    if wt_status != "optimal" or not wt_finite or wt_mass > args.tol or wt_bound > args.tol:
        raise RuntimeError(
            f"WT growth solve failed: {wt_status}, finite={wt_finite}, mass={wt_mass}, bound={wt_bound}"
        )

    wt_floor_metrics: dict[str, dict[str, Any]] = {}
    for fraction in floors:
        floor = fraction * wt_growth
        min_status, pmin, min_finite, min_mass, min_bound, min_message = solve(
            [], PRODUCT, "min", floor
        )
        max_status, pmax, max_finite, max_mass, max_bound, max_message = solve(
            [], PRODUCT, "max", floor
        )
        wt_floor_metrics[str(fraction)] = {
            "absolute_growth_floor": floor,
            "Pmin": pmin,
            "Pmax": pmax,
            "minimum_status": min_status,
            "maximum_status": max_status,
            "finite": bool(min_finite and max_finite),
            "max_mass_balance_residual": max(min_mass, max_mass),
            "max_bound_residual": max(min_bound, max_bound),
            "minimum_message": min_message,
            "maximum_message": max_message,
        }

    rows: list[dict[str, Any]] = []
    solver_failures = 0
    infeasible_floors = 0
    max_mass_residual = wt_mass
    max_bound_residual = wt_bound
    pool_genes = list(pool["genes"])
    for index, gene_id in enumerate(pool_genes, start=1):
        gene = model.genes.get_by_id(gene_id)
        with model:
            gene.knock_out()
            actual_footprint = sorted(
                reaction.id for reaction in gene.reactions if not reaction.functional
            )
        expected_footprint = sorted(pool["footprints"][gene_id])
        footprint_match = actual_footprint == expected_footprint
        growth_status, mutant_growth, growth_finite, growth_mass, growth_bound, growth_message = solve(
            expected_footprint, BIOMASS, "max"
        )
        if growth_status == "infeasible":
            mutant_growth = 0.0
        growth_valid = bool(
            growth_status == "infeasible"
            or (
                growth_status == "optimal"
                and growth_finite
                and growth_mass <= args.tol
                and growth_bound <= args.tol
            )
        )
        if not growth_valid or not footprint_match:
            solver_failures += 1
        if math.isfinite(growth_mass):
            max_mass_residual = max(max_mass_residual, growth_mass)
        if math.isfinite(growth_bound):
            max_bound_residual = max(max_bound_residual, growth_bound)
        gr = mutant_growth / wt_growth if math.isfinite(mutant_growth) and wt_growth > EPS else math.nan
        row: dict[str, Any] = {
            "gene": gene_id,
            "condition": condition["condition_id"],
            "footprint": ";".join(expected_footprint),
            "footprint_size": len(expected_footprint),
            "actual_footprint_match": footprint_match,
            "WT_mu_max": wt_growth,
            "mutant_mu_max": mutant_growth,
            "growth_status": growth_status,
            "growth_finite": growth_finite,
            "growth_mass_balance_residual": growth_mass,
            "growth_bound_residual": growth_bound,
            "growth_solver_message": growth_message,
            "GR": gr,
        }
        components: list[float] = []
        for fraction in floors:
            label = f"{fraction:g}"
            absolute_floor = fraction * wt_growth
            if not math.isfinite(mutant_growth) or mutant_growth + args.tol < absolute_floor:
                row[f"status_{label}"] = "growth_floor_infeasible"
                row[f"Pmin_{label}"] = math.nan
                row[f"Pmax_{label}"] = math.nan
                row[f"PCR_{label}"] = math.nan
                components.append(0.0)
                infeasible_floors += 1
                continue
            min_status, pmin, min_finite, min_mass, min_bound, _ = solve(
                expected_footprint, PRODUCT, "min", absolute_floor
            )
            max_status, pmax, max_finite, max_mass, max_bound, _ = solve(
                expected_footprint, PRODUCT, "max", absolute_floor
            )
            valid = bool(
                min_status == "optimal"
                and max_status == "optimal"
                and min_finite
                and max_finite
                and min_mass <= args.tol
                and max_mass <= args.tol
                and min_bound <= args.tol
                and max_bound <= args.tol
            )
            if not valid:
                solver_failures += 1
                row[f"status_{label}"] = f"solver_failure:{min_status}/{max_status}"
                row[f"Pmin_{label}"] = math.nan
                row[f"Pmax_{label}"] = math.nan
                row[f"PCR_{label}"] = math.nan
                components.append(0.0)
                continue
            max_mass_residual = max(max_mass_residual, min_mass, max_mass)
            max_bound_residual = max(max_bound_residual, min_bound, max_bound)
            denominator = max(float(wt_floor_metrics[str(fraction)]["Pmax"]), EPS)
            row[f"status_{label}"] = "optimal"
            row[f"Pmin_{label}"] = pmin
            row[f"Pmax_{label}"] = pmax
            row[f"PCR_{label}"] = pmax / denominator
            components.append(pmin / denominator)
        row["GCP"] = statistics.mean(components)

        if growth_status == "infeasible":
            row["Pmin95"] = math.nan
            row["Pmax95"] = math.nan
            row["status_95mut"] = "mutant_infeasible"
        elif math.isfinite(mutant_growth):
            near_floor = args.mutant_growth_fraction * mutant_growth
            min_status, pmin95, min_finite, min_mass, min_bound, _ = solve(
                expected_footprint, PRODUCT, "min", near_floor
            )
            max_status, pmax95, max_finite, max_mass, max_bound, _ = solve(
                expected_footprint, PRODUCT, "max", near_floor
            )
            valid = bool(
                min_status == "optimal"
                and max_status == "optimal"
                and min_finite
                and max_finite
                and min_mass <= args.tol
                and max_mass <= args.tol
                and min_bound <= args.tol
                and max_bound <= args.tol
            )
            if valid:
                row["Pmin95"] = pmin95
                row["Pmax95"] = pmax95
                row["status_95mut"] = "optimal"
                max_mass_residual = max(max_mass_residual, min_mass, max_mass)
                max_bound_residual = max(max_bound_residual, min_bound, max_bound)
            else:
                row["Pmin95"] = math.nan
                row["Pmax95"] = math.nan
                row["status_95mut"] = f"solver_failure:{min_status}/{max_status}"
                solver_failures += 1
        else:
            row["Pmin95"] = math.nan
            row["Pmax95"] = math.nan
            row["status_95mut"] = "mutant_growth_unavailable"
        rows.append(row)
        if index % 25 == 0:
            print(f"evaluate {condition['condition_id']} {index}/{len(pool_genes)}", flush=True)

    pd.DataFrame(rows).to_csv(
        outdir / "candidate_metrics.csv", index=False, encoding="utf-8-sig"
    )
    elapsed = time.perf_counter() - started
    summary = {
        "status": "COMPLETED" if solver_failures == 0 else "COMPLETED_WITH_SOLVER_FAILURES",
        "command": "evaluate",
        "condition_id": condition["condition_id"],
        "model_sha256": model_hash,
        "pool_sha256": sha256_file(pool_path),
        "pool_count": len(pool_genes),
        "evaluated_count": len(rows),
        "WT_mu_max": wt_growth,
        "WT_floor_metrics": wt_floor_metrics,
        "floors": floors,
        "mutant_growth_fraction": args.mutant_growth_fraction,
        "solver_failures": solver_failures,
        "growth_floor_infeasible_count": infeasible_floors,
        "max_mass_balance_residual": max_mass_residual,
        "max_bound_residual": max_bound_residual,
        "wall_time_seconds": elapsed,
        "solver": solver_info["solver"],
        "solver_details": solver_info,
        "solver_tolerance_requested": args.tol,
        "COBRA_GLPK_loader_tolerance_readback": tolerance_readback,
        "applied_condition_bounds": applied,
        "cobra_version": cobra.__version__,
        "scipy_version": solver_info["scipy_version"],
        "WT_growth_solver_message": wt_message,
        "WT_growth_mass_balance_residual": wt_mass,
        "WT_growth_bound_residual": wt_bound,
    }
    write_json(outdir / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False), flush=True)
    return 0


def build_ranking(
    metrics: dict[str, pd.DataFrame],
    summaries: dict[str, dict[str, Any]],
    primary: str,
    top_k: int,
    tol: float,
):
    if primary not in metrics:
        raise ValueError("primary metrics label was not supplied")
    if set(summaries) != set(metrics):
        raise ValueError("metrics and summary labels must match exactly")
    if top_k != 6:
        raise ValueError("top_k is frozen at 6 for FABRIC-AI Design mode")
    gene_sets = {label: set(frame["gene"]) for label, frame in metrics.items()}
    if any(genes != gene_sets[primary] for genes in gene_sets.values()):
        raise ValueError("condition metrics gene sets differ; silent intersection is prohibited")
    indexed = {label: frame.set_index("gene", drop=False) for label, frame in metrics.items()}
    rows = []
    growth_equivalent_counts = {label: 0 for label in metrics}
    primary_pcr_equivalent_count = 0
    for gene in sorted(gene_sets[primary]):
        gcps = [metric_equivalent(float(indexed[label].loc[gene, "GCP"]), tol) for label in metrics]
        grs = []
        for label in metrics:
            condition_row = indexed[label].loc[gene]
            gr_equiv, equivalent = native_objective_equivalent_ratio(
                float(condition_row["mutant_mu_max"]),
                float(summaries[label]["WT_mu_max"]),
                float(condition_row["GR"]),
                tol,
                metric="GR",
                gene=gene,
                condition=label,
            )
            grs.append(gr_equiv)
            growth_equivalent_counts[label] += int(equivalent)
        primary_row = indexed[primary].loc[gene]
        pmin95 = metric_equivalent(float(primary_row["Pmin95"]), tol)
        primary_wt_pmax = float(summaries[primary]["WT_floor_metrics"]["0.1"]["Pmax"])
        pcr, pcr_equivalent = native_objective_equivalent_ratio(
            float(primary_row["Pmax_0.1"]),
            primary_wt_pmax,
            float(primary_row["PCR_0.1"]),
            tol,
            metric="PCR_0.1",
            gene=gene,
            condition=primary,
        )
        primary_pcr_equivalent_count += int(pcr_equivalent)
        rows.append(
            {
                "gene": gene,
                "Robust_GCP": min(gcps),
                "Median_GCP": statistics.median(gcps),
                "Primary_Pmin95": pmin95,
                "Robust_GR": min(grs),
                "Primary_PCR_0.1": pcr,
                "footprint_size": int(primary_row["footprint_size"]),
            }
        )
    ranking = pd.DataFrame(rows)
    non_discriminating = bool(
        all(abs(float(value)) <= tol for value in indexed[primary]["GCP"])
        and all(abs(float(value)) <= tol for value in indexed[primary]["Pmin95"])
    )
    ranking["_pcr_sort"] = ranking["Primary_PCR_0.1"].fillna(float("-inf"))
    ranking = ranking.sort_values(
        by=[
            "Robust_GCP", "Median_GCP", "Primary_Pmin95", "Robust_GR",
            "_pcr_sort", "footprint_size", "gene",
        ],
        ascending=[False, False, False, False, False, True, True],
        kind="mergesort",
    ).drop(columns=["_pcr_sort"])
    ranking.insert(0, "rank", range(1, len(ranking) + 1))
    scope = (
        "SECONDARY_FEASIBILITY_ORDER_ONLY"
        if non_discriminating
        else "DESIGN_MODE_PRODUCTION_RANKING"
    )
    ranking["recommendation_scope"] = scope
    top = ranking.head(top_k).copy()
    equivalence_audit = {
        "native_unit_tolerance": tol,
        "growth_equivalent_to_WT_counts": growth_equivalent_counts,
        "primary_PCR_0.1_equivalent_to_WT_count": primary_pcr_equivalent_count,
        "native_objective_inconsistency_count": 0,
    }
    return ranking, top, non_discriminating, scope, equivalence_audit


def command_rank(args: argparse.Namespace) -> int:
    started = time.perf_counter()
    metrics: dict[str, pd.DataFrame] = {}
    summaries: dict[str, dict[str, Any]] = {}
    source_hashes = {}
    for value in args.metrics:
        if "=" not in value:
            raise ValueError(f"invalid --metrics entry: {value}")
        label, filename = value.split("=", 1)
        path = Path(filename).resolve()
        metrics[label] = pd.read_csv(path)
        source_hashes[label] = {"path": str(path), "sha256": sha256_file(path), "rows": len(metrics[label])}
    for value in args.summaries:
        if "=" not in value:
            raise ValueError(f"invalid --summaries entry: {value}")
        label, filename = value.split("=", 1)
        path = Path(filename).resolve()
        summaries[label] = load_json(path)
        source_hashes.setdefault(label, {})["summary_path"] = str(path)
        source_hashes[label]["summary_sha256"] = sha256_file(path)
    ranking, top, non_discriminating, scope, equivalence_audit = build_ranking(
        metrics, summaries, args.primary, args.top_k, args.tol
    )
    outdir = Path(args.outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    ranking.to_csv(outdir / "design_mode_ranking.csv", index=False, encoding="utf-8-sig")
    top.to_csv(outdir / "design_mode_topk.csv", index=False, encoding="utf-8-sig")
    elapsed = time.perf_counter() - started
    status = (
        "NON_DISCRIMINATING_GUARANTEED_PRODUCTION"
        if non_discriminating
        else "COMPLETED_DISCRIMINATING_PRODUCTION_RANKING"
    )
    summary = {
        "status": status,
        "command": "rank",
        "primary_condition": args.primary,
        "reported_conditions": list(metrics),
        "candidate_count": len(ranking),
        "top_k": args.top_k,
        "topk_rows": len(top),
        "topk_interpretation": scope,
        "production_superiority_claim_allowed_from_topk": not non_discriminating,
        "ranking_order": [
            "Robust_GCP_desc", "Median_GCP_desc", "Primary_Pmin95_desc",
            "Robust_GR_desc", "Primary_PCR_at_0.1WT_desc", "footprint_size_asc", "gene_id_asc",
        ],
        "numeric_equivalence": {
            "native_unit_solver_tolerance": args.tol,
            "GR": "GR_equiv=1 iff abs(mutant_mu_max-WT_mu_max)<=tol; reject mutant>WT+tol",
            "Primary_PCR_0.1": "PCR_equiv=1 iff abs(Pmax_mutant-Pmax_WT)<=tol; reject mutant>WT+tol",
            "GCP_and_Pmin95": "existing absolute-zero handling preserved",
        },
        "equivalence_audit": equivalence_audit,
        "source_metrics": source_hashes,
        "wall_time_seconds": elapsed,
        "dependency_layer": "pandas only",
        "pandas_version": pd.__version__,
    }
    write_json(outdir / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False), flush=True)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    prepare = subparsers.add_parser("prepare")
    prepare.add_argument("--model", required=True)
    prepare.add_argument("--condition", required=True)
    prepare.add_argument("--outdir", required=True)
    prepare.add_argument("--tol", type=float, default=1e-7)
    prepare.set_defaults(func=command_prepare)

    evaluate = subparsers.add_parser("evaluate")
    evaluate.add_argument("--model", required=True)
    evaluate.add_argument("--condition", required=True)
    evaluate.add_argument("--pool", required=True)
    evaluate.add_argument("--outdir", required=True)
    evaluate.add_argument("--floors", default="0.1,0.5,0.9")
    evaluate.add_argument("--mutant-growth-fraction", type=float, default=0.95)
    evaluate.add_argument("--tol", type=float, default=1e-7)
    evaluate.set_defaults(func=command_evaluate_highs)

    rank = subparsers.add_parser("rank")
    rank.add_argument("--metrics", nargs="+", required=True)
    rank.add_argument("--summaries", nargs="+", required=True)
    rank.add_argument("--primary", required=True)
    rank.add_argument("--outdir", required=True)
    rank.add_argument("--top-k", type=int, default=6)
    rank.add_argument("--tol", type=float, default=1e-7)
    rank.set_defaults(func=command_rank)
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
