"""Evidence-backed helpers for the FABRIC-AI metabolic optimization loop.

The repository does not contain the original Yeast9 model or the complete list
of 307 screened reactions. This module validates the recovered decision chain
and computes post-validation feedback from the recorded measurements and the
versioned rule file. It does not pretend to rerun FBA or OptKnock.
"""

from __future__ import annotations

import itertools
import json
import shutil
from pathlib import Path
from typing import Any

import pandas as pd


REQUIRED_EVIDENCE_COLUMNS = {
    "record_id",
    "round_label",
    "decision_stage",
    "strain_or_target",
    "condition",
    "value",
    "unit",
    "time_h",
    "data_status",
    "source_figure",
    "source_file_internal",
    "feedback_label",
    "notes",
}

EVIDENCE_FILES = (
    "round0_fermentation.csv",
    "model_inputs.csv",
    "candidate_reactions.csv",
    "optknock_plans_pre_validation.csv",
    "selected_targets_pre_validation.csv",
    "round1_outcomes.csv",
    "wetlab_validation.csv",
    "target_selection_evidence.csv",
    "evidence_conflicts.csv",
)
COMPUTED_FEEDBACK_FILE = "post_feedback_evidence.csv"
SENSITIVITY_FILE = "feedback_threshold_sensitivity.csv"

EXPECTED_SELECTED_TARGETS = {
    "r_0014": ("RIB2", "YOL066C"),
    "r_0019": ("PAN5", "YHR063C"),
    "r_0086": ("MDE1", "YJR024C"),
    "r_0087": ("MRI1", "YPR118W"),
    "r_0145": ("SPE2", "YOL052C"),
    "r_0452": ("FUM1", "YPL262W"),
}


def load_evidence(evidence_dir: str | Path, filename: str) -> pd.DataFrame:
    """Load one evidence table and validate the shared provenance columns."""

    if filename not in (*EVIDENCE_FILES, COMPUTED_FEEDBACK_FILE):
        raise ValueError(f"Unknown GSMM evidence file: {filename}")
    path = Path(evidence_dir) / filename
    if not path.is_file():
        raise FileNotFoundError(f"GSMM evidence file not found: {path}")
    frame = pd.read_csv(path, keep_default_na=False)
    missing = REQUIRED_EVIDENCE_COLUMNS.difference(frame.columns)
    if missing:
        raise ValueError(f"{filename} is missing columns: {sorted(missing)}")
    return frame


def _measurement(
    validation: pd.DataFrame,
    strain: str,
    condition: str,
    time_h: float,
) -> float | None:
    numeric_value = pd.to_numeric(validation["value"], errors="coerce")
    numeric_time = pd.to_numeric(validation["time_h"], errors="coerce")
    mask = (
        validation["strain_or_target"].eq(strain)
        & validation["condition"].eq(condition)
        & numeric_time.eq(time_h)
    )
    values = numeric_value[mask].dropna()
    if len(values) > 1:
        raise ValueError(f"Expected at most one {strain} {condition} value at {time_h} h")
    return float(values.iloc[0]) if len(values) == 1 else None


def compute_feedback_from_frames(
    validation: pd.DataFrame,
    outcomes: pd.DataFrame,
    selected: pd.DataFrame,
    rules: dict[str, Any],
) -> pd.DataFrame:
    """Compute Round 1 labels from measurements, outcomes, and versioned rules.

    The function deliberately has no gene-specific branches. A changed endpoint
    or persistence value changes the resulting score and tier through the same
    rules for every quantified target.
    """

    terminal_h = float(rules["terminal_time_h"])
    persistence_h = float(rules["persistence_start_h"])
    control_terminal = _measurement(
        validation, "AST", "astaxanthin concentration", terminal_h
    )
    control_biomass = _measurement(validation, "AST", "biomass OD600", terminal_h)
    if control_terminal is None or control_biomass is None:
        raise ValueError("AST control requires terminal yield and biomass values")

    outcomes_by_reaction = {
        str(row.reaction_id): row for row in outcomes.itertuples(index=False)
    }
    if set(outcomes_by_reaction) != set(selected["reaction_id"].astype(str)):
        raise ValueError("Round 1 outcomes must cover exactly the selected targets")

    rows: list[dict[str, Any]] = []
    for display_order, target in enumerate(selected.itertuples(index=False), start=1):
        reaction = str(target.reaction_id)
        gene = str(target.gene)
        outcome = outcomes_by_reaction[reaction]
        outcome_status = str(outcome.outcome_status)
        strain = str(outcome.strain_or_target)
        quantified = outcome_status == "quantified"

        terminal: float | None = None
        start: float | None = None
        biomass: float | None = None
        fold: float | None = None
        improvement: float | None = None
        persistence: float | None = None
        biomass_fold: float | None = None

        if quantified:
            terminal = _measurement(
                validation, strain, "astaxanthin concentration", terminal_h
            )
            start = _measurement(
                validation, strain, "astaxanthin concentration", persistence_h
            )
            biomass = _measurement(validation, strain, "biomass OD600", terminal_h)
            if terminal is None or start is None or biomass is None:
                raise ValueError(
                    f"Quantified target {reaction} requires yield at both rule times "
                    "and terminal biomass"
                )
            fold = terminal / control_terminal
            improvement = (fold - 1.0) * 100.0
            persistence = (terminal / start - 1.0) * 100.0
            biomass_fold = biomass / control_biomass

            if fold >= float(rules["positive_terminal_fold_min"]):
                terminal_score = "positive"
            elif fold <= float(rules["negative_terminal_fold_max"]):
                terminal_score = "below_control"
            else:
                terminal_score = "comparable_to_control"
            persistence_score = (
                "maintained"
                if persistence >= float(rules["persistence_change_percent_min"])
                else "negative"
            )
            biomass_score = (
                "maintained"
                if biomass_fold >= float(rules["biomass_fold_min"])
                else "reduced"
            )
            feasibility_score = "quantified"

            if (
                terminal_score == "positive"
                and persistence_score == "maintained"
                and biomass_score == "maintained"
            ):
                tier = 1
                label = "batch_supported_positive_effect"
                action = "prioritize_for_next_cycle"
            else:
                tier = 2
                label = (
                    "yield_or_persistence_negative"
                    if terminal_score == "below_control"
                    or persistence_score == "negative"
                    else "quantified_mixed_or_neutral_evidence"
                )
                action = "deprioritize_and_review_mechanism"
            trace = (
                f"terminal={terminal_score};persistence={persistence_score};"
                f"biomass={biomass_score}->tier{tier}"
            )
        elif outcome_status == "feasibility_not_passed_in_current_round":
            terminal_score = "not_available"
            persistence_score = "not_available"
            biomass_score = "not_available"
            feasibility_score = "not_passed_in_current_round"
            tier = 3
            label = "feasibility_not_passed_in_current_round"
            action = "record_construction_or_cultivation_redesign_direction"
            trace = "feasibility=not_passed_in_current_round->tier3"
        else:
            raise ValueError(f"Unsupported outcome_status for {reaction}: {outcome_status}")

        rows.append(
            {
                "record_id": f"FB-{gene}",
                "round_label": "Feedback",
                "decision_stage": "post_validation_feedback",
                "strain_or_target": strain,
                "condition": "rule-computed Round 1 feedback",
                "value": tier,
                "unit": "evidence_tier",
                "time_h": terminal_h if quantified else "",
                "data_status": "computed_rule_output",
                "source_figure": "Round 1 validation records and feedback_rules.json",
                "source_file_internal": (
                    "data/processed/gsmm_evidence_v0_2/wetlab_validation.csv; "
                    "data/processed/gsmm_evidence_v0_2/round1_outcomes.csv"
                ),
                "feedback_label": label,
                "notes": "Generated from recorded inputs; not a manually assigned label",
                "plan_id": target.plan_id,
                "reaction_id": reaction,
                "gene": gene,
                "orf": str(target.orf),
                "outcome_status": outcome_status,
                "terminal_yield_mg_L": terminal if terminal is not None else "",
                "fold_vs_ast": fold if fold is not None else "",
                "improvement_percent": improvement if improvement is not None else "",
                "late_window_start_h": persistence_h if quantified else "",
                "late_window_end_h": terminal_h if quantified else "",
                "persistence_change_percent": (
                    persistence if persistence is not None else ""
                ),
                "biomass_120h_od600": biomass if biomass is not None else "",
                "biomass_fold_vs_ast": biomass_fold if biomass_fold is not None else "",
                "terminal_yield_score": terminal_score,
                "persistence_score": persistence_score,
                "biomass_score": biomass_score,
                "feasibility_score": feasibility_score,
                "updated_evidence_tier": tier,
                "display_order": display_order,
                "rule_trace": trace,
                "next_cycle_action": action,
                "rules_version": str(rules["rules_version"]),
            }
        )

    frame = pd.DataFrame(rows)
    return frame.sort_values("display_order", kind="stable").reset_index(drop=True)


def build_feedback_sensitivity_summary(
    validation: pd.DataFrame,
    outcomes: pd.DataFrame,
    selected: pd.DataFrame,
    rules: dict[str, Any],
) -> pd.DataFrame:
    """Summarize tier stability across the versioned project-threshold grid."""

    grid = rules["sensitivity_grid"]
    keys = (
        "positive_terminal_fold_min",
        "negative_terminal_fold_max",
        "persistence_change_percent_min",
        "biomass_fold_min",
    )
    scenarios = list(itertools.product(*(grid[key] for key in keys)))
    observed: dict[str, set[int]] = {
        str(gene): set() for gene in selected["gene"].astype(str)
    }
    for values in scenarios:
        varied = dict(rules)
        varied.update(dict(zip(keys, values)))
        frame = compute_feedback_from_frames(validation, outcomes, selected, varied)
        for row in frame.itertuples(index=False):
            observed[str(row.gene)].add(int(row.updated_evidence_tier))

    baseline = compute_feedback_from_frames(validation, outcomes, selected, rules)
    rows = []
    for row in baseline.itertuples(index=False):
        tiers = sorted(observed[str(row.gene)])
        rows.append(
            {
                "gene": str(row.gene),
                "reaction_id": str(row.reaction_id),
                "baseline_evidence_tier": int(row.updated_evidence_tier),
                "scenarios_evaluated": len(scenarios),
                "observed_evidence_tiers": "|".join(str(value) for value in tiers),
                "classification_stable": len(tiers) == 1,
                "positive_terminal_fold_min_range": (
                    f"{min(grid['positive_terminal_fold_min']):g}–"
                    f"{max(grid['positive_terminal_fold_min']):g}"
                ),
                "negative_terminal_fold_max_range": (
                    f"{min(grid['negative_terminal_fold_max']):g}–"
                    f"{max(grid['negative_terminal_fold_max']):g}"
                ),
                "persistence_change_percent_min_range": (
                    f"{min(grid['persistence_change_percent_min']):g}–"
                    f"{max(grid['persistence_change_percent_min']):g}"
                ),
                "biomass_fold_min_range": (
                    f"{min(grid['biomass_fold_min']):g}–"
                    f"{max(grid['biomass_fold_min']):g}"
                ),
                "interpretation": (
                    "stable across the project-level sensitivity grid"
                    if len(tiers) == 1
                    else "changes within the project-level sensitivity grid"
                ),
            }
        )
    return pd.DataFrame(rows).sort_values("gene", kind="stable").reset_index(drop=True)


def compute_feedback_update(
    evidence_dir: str | Path,
    rules_path: str | Path | None = None,
) -> pd.DataFrame:
    """Load pre-validation inputs and calculate post-validation feedback."""

    evidence = Path(evidence_dir)
    selected = load_evidence(evidence, "selected_targets_pre_validation.csv")
    outcomes = load_evidence(evidence, "round1_outcomes.csv")
    validation = load_evidence(evidence, "wetlab_validation.csv")
    path = Path(rules_path) if rules_path else evidence / "feedback_rules.json"
    rules = json.loads(path.read_text(encoding="utf-8"))
    return compute_feedback_from_frames(validation, outcomes, selected, rules)


def validate_closed_loop(evidence_dir: str | Path) -> dict[str, Any]:
    """Validate the recorded 307 -> 14 -> 6 -> Round 1 evidence chain."""

    evidence = Path(evidence_dir)
    candidates = load_evidence(evidence, "candidate_reactions.csv")
    plans = load_evidence(evidence, "optknock_plans_pre_validation.csv")
    targets = load_evidence(evidence, "selected_targets_pre_validation.csv")
    outcomes = load_evidence(evidence, "round1_outcomes.csv")

    candidate_counts = pd.to_numeric(candidates["candidate_count"], errors="coerce")
    if candidate_counts.dropna().tolist() != [307]:
        raise ValueError("Candidate summary must record exactly 307 reactions")
    if candidates["reaction_id"].astype(str).str.strip().ne("").any():
        raise ValueError("Do not fabricate reaction IDs when the 307-item list is absent")
    if len(plans) != 14 or plans["reaction_id"].nunique() != 14:
        raise ValueError("OptKnock evidence must contain 14 distinct recorded plans")
    if plans["feedback_label"].astype(str).str.strip().ne("").any():
        raise ValueError("Pre-validation plans must not contain feedback labels")
    if len(targets) != 6 or targets["reaction_id"].nunique() != 6:
        raise ValueError("Experimental selection must contain six distinct targets")
    if targets["feedback_label"].astype(str).str.strip().ne("").any():
        raise ValueError("Pre-validation target selection must not contain feedback labels")
    if outcomes["feedback_label"].astype(str).str.strip().ne("").any():
        raise ValueError("Round 1 outcomes are rule inputs and must not contain labels")

    observed = {
        str(row.reaction_id): (str(row.gene), str(row.orf))
        for row in targets.itertuples(index=False)
    }
    if observed != EXPECTED_SELECTED_TARGETS:
        raise ValueError(f"Selected target mapping mismatch: {observed}")

    feedback = compute_feedback_update(evidence)
    if set(feedback["reaction_id"]) != set(EXPECTED_SELECTED_TARGETS):
        raise ValueError("Every selected target must receive computed feedback")

    stored_path = evidence / COMPUTED_FEEDBACK_FILE
    if stored_path.is_file():
        stored = load_evidence(evidence, COMPUTED_FEEDBACK_FILE)
        keys = [
            "reaction_id",
            "feedback_label",
            "updated_evidence_tier",
            "display_order",
            "rule_trace",
        ]
        left = feedback[keys].sort_values("reaction_id").reset_index(drop=True)
        right = stored[keys].sort_values("reaction_id").reset_index(drop=True)
        if not left.astype(str).equals(right.astype(str)):
            raise ValueError("Stored post-feedback evidence is stale; regenerate it")

    metrics = endpoint_metrics(evidence)
    return {
        "candidate_reaction_count": 307,
        "recorded_optknock_plan_count": 14,
        "selected_target_count": 6,
        "round1_quantified_mutants": ["PAN5", "MDE1"],
        "round1_current_feasibility_not_passed": ["RIB2", "MRI1", "SPE2", "FUM1"],
        "feedback_rules_version": feedback["rules_version"].iloc[0],
        "computed_feedback_count": len(feedback),
        **metrics,
    }


def endpoint_metrics(evidence_dir: str | Path) -> dict[str, float]:
    """Calculate same-batch Round 1 endpoint and time-course metrics."""

    validation = load_evidence(evidence_dir, "wetlab_validation.csv")

    def required(target: str, time_h: float) -> float:
        value = _measurement(
            validation, target, "astaxanthin concentration", time_h
        )
        if value is None:
            raise ValueError(f"Expected one {target} astaxanthin value at {time_h} h")
        return value

    control_120 = required("AST", 120)
    pan5_120 = required("delta_PAN5", 120)
    mde1_96 = required("delta_MDE1", 96)
    mde1_120 = required("delta_MDE1", 120)
    return {
        "control_astaxanthin_120h_mg_L": control_120,
        "pan5_astaxanthin_120h_mg_L": pan5_120,
        "pan5_fold_vs_control": pan5_120 / control_120,
        "pan5_improvement_percent": (pan5_120 / control_120 - 1.0) * 100.0,
        "mde1_astaxanthin_96h_mg_L": mde1_96,
        "mde1_astaxanthin_120h_mg_L": mde1_120,
        "mde1_late_change_percent": (mde1_120 / mde1_96 - 1.0) * 100.0,
    }


def build_validation_summary(evidence_dir: str | Path) -> pd.DataFrame:
    """Build a seven-row control/target summary from computed feedback."""

    evidence = Path(evidence_dir)
    validation = load_evidence(evidence, "wetlab_validation.csv")
    feedback = compute_feedback_update(evidence)
    terminal_h = float(feedback["late_window_end_h"].replace("", pd.NA).dropna().iloc[0])
    persistence_h = float(
        feedback["late_window_start_h"].replace("", pd.NA).dropna().iloc[0]
    )
    control_yield = _measurement(
        validation, "AST", "astaxanthin concentration", terminal_h
    )
    control_start = _measurement(
        validation, "AST", "astaxanthin concentration", persistence_h
    )
    control_biomass = _measurement(validation, "AST", "biomass OD600", terminal_h)
    if control_yield is None or control_start is None or control_biomass is None:
        raise ValueError("AST control requires both rule-time yields and terminal biomass")

    control = {
        "record_id": "VAL-SUM-AST",
        "round_label": "Round1",
        "decision_stage": "integrated_validation",
        "strain_or_target": "AST",
        "condition": "control reference",
        "value": control_yield,
        "unit": "mg/L",
        "time_h": terminal_h,
        "data_status": "derived_calculation",
        "source_figure": "Same-batch astaxanthin and biomass curves",
        "source_file_internal": "docs/evidence/gsmm-model-evidence.md",
        "feedback_label": "control_reference",
        "notes": "Same-batch reference for rule-computed comparisons",
        "reaction_id": "",
        "gene": "AST",
        "orf": "",
        "terminal_yield_mg_L": control_yield,
        "fold_vs_ast": 1.0,
        "improvement_percent": 0.0,
        "late_window_start_h": persistence_h,
        "late_window_end_h": terminal_h,
        "persistence_change_percent": (control_yield / control_start - 1.0) * 100.0,
        "biomass_120h_od600": control_biomass,
        "biomass_fold_vs_ast": 1.0,
        "terminal_yield_score": "control",
        "persistence_score": "control",
        "biomass_score": "control",
        "feasibility_score": "control",
        "feedback_tier": 0,
        "rule_trace": "control_reference",
        "next_cycle_action": "reference_only",
    }

    target_rows = feedback.rename(columns={"updated_evidence_tier": "feedback_tier"}).copy()
    columns = list(control)
    for column in columns:
        if column not in target_rows:
            target_rows[column] = ""
    return pd.concat(
        [pd.DataFrame([control]), target_rows[columns]], ignore_index=True
    )


def materialize_results(evidence_dir: str | Path, output_dir: str | Path) -> dict[str, Any]:
    """Copy traceable inputs and write computed, machine-readable results."""

    source = Path(evidence_dir)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    for filename in EVIDENCE_FILES:
        shutil.copyfile(source / filename, output / filename)
    for filename in ("feedback_rules.json", "data_status_mapping.csv"):
        shutil.copyfile(source / filename, output / filename)

    computed = compute_feedback_update(source)
    computed.to_csv(output / COMPUTED_FEEDBACK_FILE, index=False)
    build_validation_summary(source).to_csv(output / "validation_summary.csv", index=False)
    rules = json.loads((source / "feedback_rules.json").read_text(encoding="utf-8"))
    build_feedback_sensitivity_summary(
        load_evidence(source, "wetlab_validation.csv"),
        load_evidence(source, "round1_outcomes.csv"),
        load_evidence(source, "selected_targets_pre_validation.csv"),
        rules,
    ).to_csv(output / SENSITIVITY_FILE, index=False)

    summary = validate_closed_loop(source)
    summary.update(
        {
            "pipeline_status": "evidence_chain_verified",
            "solver_environment_status": "solver_environment_not_in_release",
            "original_yeast9_model_recovered": False,
            "original_optimization_code_recovered": False,
            "fba_optknock_rerun_claim_allowed": False,
            "feedback_generation": "computed_from_round1_inputs_and_versioned_rules",
            "interpretation": (
                "The recorded decision chain and feedback update are reproducible as an "
                "evidence summary. FBA and OptKnock require the original model and "
                "constraint files before rerunning."
            ),
        }
    )
    (output / "closed_loop_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return summary