"""Independent structural checks for the selected Design-mode freeze outputs."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
TOL = 1e-7


def read_json(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def main() -> int:
    historical = read_json("freeze_inputs/common_candidate_space_237_HISTORICAL.json")
    fresh = read_json("results/fabric_ai_primary_prepare/candidate_space.json")
    prepare = read_json("results/fabric_ai_primary_prepare/summary.json")
    v1_summary = read_json("results/fabric_ai_v1_metrics/summary.json")
    v2a_summary = read_json("results/fabric_ai_v2a_metrics/summary.json")
    rank_summary = read_json("results/fabric_ai_design_mode_final/summary.json")
    v1 = pd.read_csv(ROOT / "results/fabric_ai_v1_metrics/candidate_metrics.csv")
    v2a = pd.read_csv(ROOT / "results/fabric_ai_v2a_metrics/candidate_metrics.csv")
    ranking = pd.read_csv(ROOT / "results/fabric_ai_design_mode_final/design_mode_ranking.csv")
    top = pd.read_csv(ROOT / "results/fabric_ai_design_mode_final/design_mode_topk.csv")

    expected_genes = [
        gene for gene in historical["genes"] if gene not in {"YER014W", "YOR176W"}
    ]
    footprint_mismatches = [
        gene
        for gene in expected_genes
        if sorted(historical["footprints"][gene]) != sorted(fresh["footprints"][gene])
    ]
    checks = {
        "prepare_completed": prepare["status"] == "COMPLETED",
        "fresh_eligible_235": fresh["eligible_count"] == 235 == len(fresh["genes"]),
        "corrected_gene_set_exact": set(fresh["genes"]) == set(expected_genes),
        "blocked_set_exact": set(fresh["blocked_reaction_ids"]) == set(historical["blocked_reaction_ids"]),
        "full_gpr_footprints_exact": not footprint_mismatches,
        "v1_completed_235": v1_summary["status"] == "COMPLETED" and len(v1) == 235,
        "v2a_completed_235": v2a_summary["status"] == "COMPLETED" and len(v2a) == 235,
        "sensitivity_pool_not_intersected": set(v1["gene"]) == set(v2a["gene"]) == set(fresh["genes"]),
        "all_footprints_match": bool(v1["actual_footprint_match"].all() and v2a["actual_footprint_match"].all()),
        "no_solver_failures": v1_summary["solver_failures"] == 0 and v2a_summary["solver_failures"] == 0,
        "residuals_within_tolerance": max(
            v1_summary["max_mass_balance_residual"],
            v1_summary["max_bound_residual"],
            v2a_summary["max_mass_balance_residual"],
            v2a_summary["max_bound_residual"],
        ) <= TOL,
        "primary_non_discriminating_actual": bool(
            (v1["GCP"].abs() <= TOL).all() and (v1["Pmin95"].abs() <= TOL).all()
        ),
        "rank_gate_exact": rank_summary["status"] == "NON_DISCRIMINATING_GUARANTEED_PRODUCTION",
        "ranking_235": len(ranking) == 235,
        "topk_fixed_6": len(top) == 6 and rank_summary["top_k"] == 6,
        "topk_secondary_only": set(top["recommendation_scope"]) == {"SECONDARY_FEASIBILITY_ORDER_ONLY"},
        "no_production_superiority_permission": rank_summary["production_superiority_claim_allowed_from_topk"] is False,
        "tests_passed": "5 passed" in (ROOT / "logs/05_tests.log").read_text(encoding="utf-8"),
    }
    passed = all(checks.values())
    report = {
        "status": "PASSED" if passed else "FAILED",
        "tolerance": TOL,
        "checks": checks,
        "footprint_mismatches": footprint_mismatches,
        "v2a_infeasible_mutants": sorted(v2a.loc[v2a["growth_status"] == "infeasible", "gene"].tolist()),
        "v2a_growth_floor_infeasible_cells": v2a_summary["growth_floor_infeasible_count"],
        "secondary_top6": top["gene"].tolist(),
    }
    (ROOT / "audit/final_verification.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
