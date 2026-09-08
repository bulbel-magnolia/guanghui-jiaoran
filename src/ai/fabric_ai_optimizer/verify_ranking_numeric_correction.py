"""Independent checks for the ranking-only native-unit equivalence correction."""

from __future__ import annotations

import hashlib
import json
import math
import statistics
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
TOL = 1e-7
PRIMARY = "v1_glucose_reference"
LABELS = [PRIMARY, "v2a_historical_ethanol_stage"]
METRICS = {
    PRIMARY: ROOT / "results/fabric_ai_v1_metrics/candidate_metrics.csv",
    "v2a_historical_ethanol_stage": ROOT / "results/fabric_ai_v2a_metrics/candidate_metrics.csv",
}
SUMMARIES = {
    PRIMARY: ROOT / "results/fabric_ai_v1_metrics/summary.json",
    "v2a_historical_ethanol_stage": ROOT / "results/fabric_ai_v2a_metrics/summary.json",
}
EXPECTED_INPUT_HASHES = {
    str(METRICS[PRIMARY].relative_to(ROOT)).replace("\\", "/"): "2176df82d1f75ee7c38990836c3e185c658b2c615635664e800c68063332300d",
    str(METRICS[LABELS[1]].relative_to(ROOT)).replace("\\", "/"): "e270f2636e8fb0e52702f43e35fc6a7e8aea5acdffa344fb7b09c45d0839e150",
    str(SUMMARIES[PRIMARY].relative_to(ROOT)).replace("\\", "/"): "a2592d738b36ad299d7ba64d7084284d00d60cad707c8cb9ead2663976f30c22",
    str(SUMMARIES[LABELS[1]].relative_to(ROOT)).replace("\\", "/"): "8d21cfa35bc4757e5317e0c397347cb8f938ebb38e4aac7bd934f9c30ed8677e",
}
RESULT = ROOT / "results/fabric_ai_ranking_numeric_correction_20260908"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def zero_equiv(value: float) -> float:
    return 0.0 if abs(value) <= TOL else value


def native_ratio(mutant: float, wt: float, recorded: float) -> float:
    if not (math.isfinite(mutant) and math.isfinite(wt)):
        return math.nan
    if mutant > wt + TOL:
        raise AssertionError(f"KO objective exceeds WT+tolerance: {mutant} > {wt}+{TOL}")
    return 1.0 if abs(mutant - wt) <= TOL else recorded


def independently_rank(frames, summaries):
    indexed = {label: frame.set_index("gene", drop=False) for label, frame in frames.items()}
    rows = []
    for gene in sorted(indexed[PRIMARY].index):
        gcps = [zero_equiv(float(indexed[label].loc[gene, "GCP"])) for label in LABELS]
        grs = [
            native_ratio(
                float(indexed[label].loc[gene, "mutant_mu_max"]),
                float(summaries[label]["WT_mu_max"]),
                float(indexed[label].loc[gene, "GR"]),
            )
            for label in LABELS
        ]
        primary_row = indexed[PRIMARY].loc[gene]
        wt_pmax = float(summaries[PRIMARY]["WT_floor_metrics"]["0.1"]["Pmax"])
        pcr = native_ratio(
            float(primary_row["Pmax_0.1"]), wt_pmax, float(primary_row["PCR_0.1"])
        )
        rows.append(
            {
                "gene": gene,
                "Robust_GCP": min(gcps),
                "Median_GCP": statistics.median(gcps),
                "Primary_Pmin95": zero_equiv(float(primary_row["Pmin95"])),
                "Robust_GR": min(grs),
                "Primary_PCR_0.1": pcr,
                "footprint_size": int(primary_row["footprint_size"]),
            }
        )
    expected = pd.DataFrame(rows)
    expected["_pcr_sort"] = expected["Primary_PCR_0.1"].fillna(float("-inf"))
    expected = expected.sort_values(
        by=[
            "Robust_GCP",
            "Median_GCP",
            "Primary_Pmin95",
            "Robust_GR",
            "_pcr_sort",
            "footprint_size",
            "gene",
        ],
        ascending=[False, False, False, False, False, True, True],
        kind="mergesort",
    ).drop(columns="_pcr_sort")
    expected.insert(0, "rank", range(1, len(expected) + 1))
    expected["recommendation_scope"] = "SECONDARY_FEASIBILITY_ORDER_ONLY"
    return expected.reset_index(drop=True)


def main() -> int:
    actual_hashes = {}
    for relative, expected in EXPECTED_INPUT_HASHES.items():
        actual_hashes[relative] = sha256(ROOT / relative)
    frames = {label: pd.read_csv(METRICS[label]) for label in LABELS}
    summaries = {label: read_json(SUMMARIES[label]) for label in LABELS}
    ranking = pd.read_csv(RESULT / "design_mode_ranking.csv")
    top = pd.read_csv(RESULT / "design_mode_topk.csv")
    historical_ranking = pd.read_csv(
        ROOT / "results/fabric_ai_design_mode_final/design_mode_ranking.csv"
    )
    rank_summary = read_json(RESULT / "summary.json")
    expected_ranking = independently_rank(frames, summaries)
    expected_gene_sets = [set(frames[label]["gene"]) for label in LABELS]
    ranking_match = ranking.equals(expected_ranking)
    old_ranks = historical_ranking.set_index("gene")["rank"].astype(int)
    new_ranks = ranking.set_index("gene")["rank"].astype(int)
    changed_rank_count = int((old_ranks.sort_index() != new_ranks.sort_index()).sum())
    checks = {
        "frozen_metric_and_summary_hashes_exact": actual_hashes == EXPECTED_INPUT_HASHES,
        "frozen_candidate_metrics_235_each": all(len(frames[label]) == 235 for label in LABELS),
        "condition_gene_sets_exactly_match": expected_gene_sets[0] == expected_gene_sets[1],
        "no_native_growth_above_WT_plus_tolerance": all(
            not ((frames[label]["mutant_mu_max"] - summaries[label]["WT_mu_max"]) > TOL).any()
            for label in LABELS
        ),
        "no_primary_Pmax_above_WT_plus_tolerance": not (
            frames[PRIMARY]["Pmax_0.1"]
            - summaries[PRIMARY]["WT_floor_metrics"]["0.1"]["Pmax"]
            > TOL
        ).any(),
        "ranking_matches_independent_native_unit_recompute": ranking_match,
        "ranking_priority_exact": rank_summary["ranking_order"] == [
            "Robust_GCP_desc",
            "Median_GCP_desc",
            "Primary_Pmin95_desc",
            "Robust_GR_desc",
            "Primary_PCR_at_0.1WT_desc",
            "footprint_size_asc",
            "gene_id_asc",
        ],
        "non_discrimination_gate_unchanged": rank_summary["status"]
        == "NON_DISCRIMINATING_GUARANTEED_PRODUCTION",
        "secondary_scope_only": set(top["recommendation_scope"])
        == {"SECONDARY_FEASIBILITY_ORDER_ONLY"},
        "top_k_fixed_at_6": len(top) == 6 and rank_summary["top_k"] == 6,
        "top6_is_ranking_head": top.equals(ranking.head(6)),
        "historical_ranking_retained_for_audit": len(historical_ranking) == 235,
        "production_superiority_claim_prohibited": rank_summary[
            "production_superiority_claim_allowed_from_topk"
        ]
        is False,
        "native_objective_inconsistency_count_zero": rank_summary[
            "equivalence_audit"
        ]["native_objective_inconsistency_count"]
        == 0,
        "nine_ranking_tests_passed": "9 passed" in (
            ROOT / "logs/07_tests_ranking_numeric_correction.log"
        ).read_text(encoding="utf-8"),
    }
    passed = all(checks.values())
    report = {
        "status": "PASSED" if passed else "FAILED",
        "scope": "ranking/tests/verification correction only",
        "native_unit_solver_tolerance": TOL,
        "source_commit_with_correction_instruction": "36ebd194b9f9cd94b6ab685bfe0057d752204cc1",
        "checks": checks,
        "source_hashes": actual_hashes,
        "ranking_sha256": sha256(RESULT / "design_mode_ranking.csv"),
        "topk_sha256": sha256(RESULT / "design_mode_topk.csv"),
        "secondary_top6": top["gene"].tolist(),
        "candidate_rank_changes_vs_historical_numeric_handling": changed_rank_count,
    }
    output = ROOT / "audit/ranking_numeric_correction_verification.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
