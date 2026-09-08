from __future__ import annotations

import importlib.util
from pathlib import Path

import pandas as pd


MODULE_PATH = Path(__file__).resolve().parents[1] / "optimizer" / "fabric_ai_benchmark.py"
SPEC = importlib.util.spec_from_file_location("fabric_ai_benchmark", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def frame(rows):
    return pd.DataFrame(rows)


def row(
    gene,
    gcp=0.0,
    pmin95=0.0,
    gr=1.0,
    pcr=1.0,
    footprint=1,
    wt_growth=1.0,
    mutant_growth=None,
    pmax=1.0,
):
    if mutant_growth is None:
        mutant_growth = gr * wt_growth
    return {
        "gene": gene,
        "GCP": gcp,
        "Pmin95": pmin95,
        "GR": gr,
        "PCR_0.1": pcr,
        "mutant_mu_max": mutant_growth,
        "Pmax_0.1": pmax,
        "footprint_size": footprint,
    }


def summaries(wt_growth=1.0, wt_pmax=1.0):
    value = {"WT_mu_max": wt_growth, "WT_floor_metrics": {"0.1": {"Pmax": wt_pmax}}}
    return {"v1": value, "v2a": value}


def test_non_discriminating_scope_is_secondary_only():
    primary = frame([row("B"), row("A")])
    sensitivity = frame([row("B", gr=0.8), row("A", gr=0.9)])
    ranking, top, gate, scope, _ = MODULE.build_ranking(
        {"v1": primary, "v2a": sensitivity}, summaries(), "v1", 6, 1e-7
    )
    assert gate is True
    assert scope == "SECONDARY_FEASIBILITY_ORDER_ONLY"
    assert set(top["recommendation_scope"]) == {scope}


def test_fixed_lexicographic_order():
    primary = frame([
        row("A", gcp=0.2, pmin95=0.1, gr=0.7, pcr=0.9, footprint=2),
        row("B", gcp=0.2, pmin95=0.1, gr=0.8, pcr=0.8, footprint=1),
    ])
    sensitivity = frame([
        row("A", gcp=0.1, gr=0.9),
        row("B", gcp=0.1, gr=0.8),
    ])
    ranking, _, gate, _, _ = MODULE.build_ranking(
        {"v1": primary, "v2a": sensitivity}, summaries(), "v1", 6, 1e-7
    )
    assert gate is False
    assert list(ranking["gene"]) == ["B", "A"]


def test_numeric_noise_is_zeroed_before_ranking():
    primary = frame([row("B", gcp=1e-8, pmin95=1e-8), row("A")])
    sensitivity = frame([row("B"), row("A")])
    ranking, _, gate, _, _ = MODULE.build_ranking(
        {"v1": primary, "v2a": sensitivity}, summaries(), "v1", 6, 1e-7
    )
    assert gate is True
    assert list(ranking["gene"]) == ["A", "B"]


def test_condition_gene_sets_must_match():
    primary = frame([row("A"), row("B")])
    sensitivity = frame([row("A")])
    try:
        MODULE.build_ranking(
            {"v1": primary, "v2a": sensitivity}, summaries(), "v1", 6, 1e-7
        )
    except ValueError as error:
        assert "silent intersection" in str(error)
    else:
        raise AssertionError("different condition gene sets were accepted")


def test_top_k_is_not_expanded():
    primary = frame([row(str(index)) for index in range(10)])
    sensitivity = primary.copy()
    _, top, _, _, _ = MODULE.build_ranking(
        {"v1": primary, "v2a": sensitivity}, summaries(), "v1", 6, 1e-7
    )
    assert len(top) == 6


def test_native_pmax_equivalence_prevents_ratio_space_tie_break():
    wt_pmax = 0.06725532100612219
    delta = 2.629e-8
    primary = frame([
        row("A", pcr=1.0, pmax=wt_pmax),
        row("Z", pcr=(wt_pmax + delta) / wt_pmax, pmax=wt_pmax + delta),
    ])
    sensitivity = primary.copy()
    info = summaries(wt_pmax=wt_pmax)
    ranking, _, _, _, audit = MODULE.build_ranking(
        {"v1": primary, "v2a": sensitivity}, info, "v1", 6, 1e-7
    )
    assert list(ranking["gene"]) == ["A", "Z"]
    assert set(ranking["Primary_PCR_0.1"]) == {1.0}
    assert audit["primary_PCR_0.1_equivalent_to_WT_count"] == 2


def test_native_growth_equivalence_prevents_normalized_tie_break():
    wt_growth = 0.010416437798675585
    delta = 5e-8
    primary = frame([
        row("A", wt_growth=wt_growth, mutant_growth=wt_growth, gr=1.0),
        row("Z", wt_growth=wt_growth, mutant_growth=wt_growth + delta,
            gr=(wt_growth + delta) / wt_growth),
    ])
    sensitivity = primary.copy()
    ranking, _, _, _, audit = MODULE.build_ranking(
        {"v1": primary, "v2a": sensitivity}, summaries(wt_growth=wt_growth),
        "v1", 6, 1e-7
    )
    assert list(ranking["gene"]) == ["A", "Z"]
    assert set(ranking["Robust_GR"]) == {1.0}
    assert audit["growth_equivalent_to_WT_counts"] == {"v1": 2, "v2a": 2}


def test_native_objective_above_wt_beyond_tolerance_is_rejected():
    primary = frame([
        row("A", mutant_growth=1.0 + 2e-7, gr=1.0000002),
    ])
    try:
        MODULE.build_ranking(
            {"v1": primary, "v2a": primary.copy()}, summaries(), "v1", 6, 1e-7
        )
    except ValueError as error:
        assert "exceeds WT by more than tolerance" in str(error)
    else:
        raise AssertionError("native objective inconsistency was accepted")


def test_top_k_other_than_six_is_rejected():
    primary = frame([row("A")])
    try:
        MODULE.build_ranking(
            {"v1": primary, "v2a": primary.copy()}, summaries(), "v1", 5, 1e-7
        )
    except ValueError as error:
        assert "top_k is frozen at 6" in str(error)
    else:
        raise AssertionError("non-frozen top_k was accepted")
