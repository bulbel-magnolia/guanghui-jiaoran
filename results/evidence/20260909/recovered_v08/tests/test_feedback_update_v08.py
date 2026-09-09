from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
AI_ROOT = REPO_ROOT / "src" / "ai"
if str(AI_ROOT) not in sys.path:
    sys.path.insert(0, str(AI_ROOT))

from fabric_ai.metabolic import (
    build_feedback_sensitivity_summary,
    compute_feedback_from_frames,
    compute_feedback_update,
)


EVIDENCE_DIR = REPO_ROOT / "data" / "processed" / "gsmm_evidence_v0_2"


class FeedbackUpdateV08Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validation = pd.read_csv(
            EVIDENCE_DIR / "wetlab_validation.csv", keep_default_na=False
        )
        cls.outcomes = pd.read_csv(
            EVIDENCE_DIR / "round1_outcomes.csv", keep_default_na=False
        )
        cls.selected = pd.read_csv(
            EVIDENCE_DIR / "selected_targets_pre_validation.csv",
            keep_default_na=False,
        )
        cls.rules = json.loads(
            (EVIDENCE_DIR / "feedback_rules.json").read_text(encoding="utf-8")
        )

    def test_expected_feedback_is_computed_for_all_six_targets(self) -> None:
        frame = compute_feedback_update(EVIDENCE_DIR).set_index("gene")
        self.assertEqual(frame.loc["PAN5", "feedback_label"], "batch_supported_positive_effect")
        self.assertEqual(int(frame.loc["PAN5", "updated_evidence_tier"]), 1)
        self.assertEqual(frame.loc["MDE1", "feedback_label"], "yield_or_persistence_negative")
        self.assertEqual(int(frame.loc["MDE1", "updated_evidence_tier"]), 2)
        unavailable = frame[frame["updated_evidence_tier"].eq(3)]
        self.assertEqual(set(unavailable.index), {"RIB2", "MRI1", "SPE2", "FUM1"})
        self.assertEqual(
            set(unavailable["next_cycle_action"]),
            {"record_construction_or_cultivation_redesign_direction"},
        )

    def test_evidence_tier_is_not_a_rank(self) -> None:
        frame = compute_feedback_update(EVIDENCE_DIR)
        self.assertNotIn("post_feedback_rank", frame.columns)
        self.assertEqual(frame["display_order"].tolist(), [1, 2, 3, 4, 5, 6])
        tier_three = frame[frame["updated_evidence_tier"].eq(3)]
        self.assertEqual(tier_three["display_order"].nunique(), 4)

    def test_project_threshold_rationale_and_sensitivity_are_explicit(self) -> None:
        self.assertEqual(self.rules["threshold_role"], "project_level_decision_thresholds")
        rationale = self.rules["threshold_rationale"]
        self.assertIn("small-sample evidence", rationale)
        self.assertIn("not statistical-significance criteria", rationale)
        summary = build_feedback_sensitivity_summary(
            self.validation, self.outcomes, self.selected, self.rules
        ).set_index("gene")
        self.assertEqual(set(summary.index), {"RIB2", "PAN5", "MDE1", "MRI1", "SPE2", "FUM1"})
        self.assertTrue(summary["classification_stable"].all())
        self.assertEqual(set(summary["scenarios_evaluated"]), {144})
        self.assertEqual(summary.loc["PAN5", "observed_evidence_tiers"], "1")
        self.assertEqual(summary.loc["MDE1", "observed_evidence_tiers"], "2")

    def test_pan5_label_changes_when_endpoint_is_perturbed(self) -> None:
        changed = self.validation.copy()
        mask = (
            changed["strain_or_target"].eq("delta_PAN5")
            & changed["condition"].eq("astaxanthin concentration")
            & pd.to_numeric(changed["time_h"], errors="coerce").eq(120)
        )
        changed.loc[mask, "value"] = 0.40
        frame = compute_feedback_from_frames(
            changed, self.outcomes, self.selected, self.rules
        ).set_index("gene")
        self.assertEqual(frame.loc["PAN5", "terminal_yield_score"], "below_control")
        self.assertEqual(frame.loc["PAN5", "feedback_label"], "yield_or_persistence_negative")
        self.assertEqual(int(frame.loc["PAN5", "updated_evidence_tier"]), 2)

    def test_mde1_label_changes_when_endpoint_is_perturbed(self) -> None:
        changed = self.validation.copy()
        mask = (
            changed["strain_or_target"].eq("delta_MDE1")
            & changed["condition"].eq("astaxanthin concentration")
            & pd.to_numeric(changed["time_h"], errors="coerce").eq(120)
        )
        changed.loc[mask, "value"] = 0.50
        frame = compute_feedback_from_frames(
            changed, self.outcomes, self.selected, self.rules
        ).set_index("gene")
        self.assertEqual(frame.loc["MDE1", "terminal_yield_score"], "positive")
        self.assertEqual(frame.loc["MDE1", "persistence_score"], "maintained")
        self.assertEqual(frame.loc["MDE1", "feedback_label"], "batch_supported_positive_effect")
        self.assertEqual(int(frame.loc["MDE1", "updated_evidence_tier"]), 1)

    def test_feedback_rules_do_not_branch_on_gene_name(self) -> None:
        source = (AI_ROOT / "fabric_ai" / "metabolic.py").read_text(encoding="utf-8")
        body = source.split("def compute_feedback_from_frames", 1)[1].split(
            "def build_feedback_sensitivity_summary", 1
        )[0]
        self.assertNotIn("if gene", body)
        self.assertNotIn("elif gene", body)

    def test_pre_validation_tables_do_not_leak_round1_labels(self) -> None:
        for filename in (
            "optknock_plans_pre_validation.csv",
            "selected_targets_pre_validation.csv",
        ):
            frame = pd.read_csv(EVIDENCE_DIR / filename, keep_default_na=False)
            self.assertTrue(frame["feedback_label"].astype(str).str.strip().eq("").all())
            self.assertFalse(
                {"outcome_status", "updated_evidence_tier", "post_feedback_rank"}
                & set(frame.columns)
            )

    def test_plan_objective_values_are_transcribed_without_ranking_claim(self) -> None:
        frame = pd.read_csv(
            EVIDENCE_DIR / "optknock_plans_pre_validation.csv",
            keep_default_na=False,
        )
        expected = [
            0.0067, 0.0067, 0.0067, 0.0067, 0.0067, 0.0025, 0.0025,
            0.0025, 0.0025, 0.0067, 0.0060, 0.0025, 0.0067, 0.0067,
        ]
        self.assertEqual(frame["objective_value_transcribed"].tolist(), expected)
        self.assertEqual(set(frame["objective_definition_status"]), {"unrecovered"})
        self.assertEqual(set(frame["comparability_status"]), {"not_established"})

    def test_target_selection_basis_is_page_level_only(self) -> None:
        frame = pd.read_csv(
            EVIDENCE_DIR / "target_selection_evidence.csv",
            keep_default_na=False,
        )
        self.assertEqual(len(frame), 6)
        self.assertEqual(set(frame["target_specific_evidence_status"]), {"page_level_only"})
        self.assertEqual(set(frame["pathway_position"]), {"not_recovered"})
        self.assertEqual(set(frame["expected_carbon_flow_effect"]), {"not_recovered"})

    def test_stored_post_feedback_matches_recomputation(self) -> None:
        computed = compute_feedback_update(EVIDENCE_DIR)
        stored = pd.read_csv(
            EVIDENCE_DIR / "post_feedback_evidence.csv", keep_default_na=False
        )
        keys = [
            "reaction_id",
            "feedback_label",
            "updated_evidence_tier",
            "display_order",
            "rule_trace",
        ]
        pd.testing.assert_frame_equal(
            computed[keys].sort_values("reaction_id").reset_index(drop=True),
            stored[keys].sort_values("reaction_id").reset_index(drop=True),
            check_dtype=False,
        )


if __name__ == "__main__":
    unittest.main()