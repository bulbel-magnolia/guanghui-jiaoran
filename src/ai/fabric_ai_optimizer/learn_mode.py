"""Replay recovered v0.8 feedback as an explicit, auditable state transition.

The six historical targets are independent of the frozen 235-gene Design task.
This module updates evidence and next actions; it does not retrain the GSMM.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import importlib.util
import json
import math
from pathlib import Path
from typing import Any
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, allow_nan=False).encode()
    return hashlib.sha256(raw).hexdigest()


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n', encoding='utf-8')


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8-sig'))


def load_engine(config: dict[str, Any]):
    source = ROOT / config['source_root'] / config['engine_path']
    if sha(source) != config['engine_sha256']:
        raise ValueError('Recovered feedback engine hash mismatch')
    spec = importlib.util.spec_from_file_location('recovered_feedback_v08', source)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def initialize_state(selected: pd.DataFrame, source_hash: str) -> dict[str, Any]:
    """The before state accepts selection records only, never outcome data."""
    needed = {'record_id', 'gene', 'orf', 'reaction_id', 'plan_id', 'feedback_label'}
    if not needed <= set(selected.columns) or selected.empty:
        raise ValueError('Invalid selected-target table')
    for key in ['record_id', 'gene', 'orf', 'reaction_id']:
        if selected[key].isna().any() or selected[key].astype(str).str.strip().eq('').any() or selected[key].duplicated().any():
            raise ValueError(f'Missing/duplicate selected key: {key}')
    forbidden = {'outcome_status', 'updated_evidence_tier', 'post_feedback_rank', 'terminal_yield_mg_L'}
    if forbidden & set(selected.columns) or not selected['feedback_label'].fillna('').eq('').all():
        raise ValueError('Post-experiment evidence leaked into before state')
    rows = [{'gene': str(r.gene), 'orf': str(r.orf), 'reaction_id': str(r.reaction_id),
             'plan_id': int(r.plan_id), 'selection_record_id': str(r.record_id),
             'evidence_tier': None, 'evidence_status': 'NOT_YET_ASSESSED',
             'next_cycle_action': 'selected_for_round1'}
            for r in selected.itertuples(index=False)]
    state = {'schema_version': '1.0', 'phase': 'before_feedback',
             'scope': 'historical_six_target_evidence_state',
             'origin': '2026 explicit representation of recovered pre-validation selection; not a fabricated historical executable model',
             'selection_sha256': source_hash, 'targets': rows,
             'metrics': {'target_count': len(rows), 'classified_target_count': 0,
                         'unassessed_target_count': len(rows), 'quantified_target_count': 0,
                         'next_action_class_count': 1}}
    state['state_id'] = 'before:' + digest(state)
    return state


def validate_feedback(validation: pd.DataFrame, outcomes: pd.DataFrame,
                      selected: pd.DataFrame, rules: dict[str, Any]) -> None:
    for frame in [outcomes, selected]:
        if frame['reaction_id'].duplicated().any():
            raise ValueError('Duplicate target outcome/selection')
    if set(outcomes['reaction_id']) != set(selected['reaction_id']):
        raise ValueError('Outcome coverage differs from selected targets')
    keys = ['strain_or_target', 'condition', 'time_h']
    if validation.duplicated(keys).any():
        raise ValueError('Duplicate measurement key; do not synthesize replicates')
    numbers = pd.to_numeric(validation['value'], errors='coerce')
    if not numbers.map(lambda x: math.isfinite(float(x)) and x >= 0).all():
        raise ValueError('Non-finite or negative measurement')
    mapping = {'astaxanthin concentration': 'mg/L', 'biomass OD600': 'OD600'}
    for condition, unit in mapping.items():
        if not validation.loc[validation['condition'].eq(condition), 'unit'].eq(unit).all():
            raise ValueError('Unexpected measurement units')
    by_reaction = selected.set_index('reaction_id')
    for r in outcomes.itertuples(index=False):
        if r.gene != by_reaction.loc[r.reaction_id, 'gene'] or r.orf != by_reaction.loc[r.reaction_id, 'orf']:
            raise ValueError('Target identity mismatch')
    # The inherited engine requires positive denominators for the control and
    # for the 96 h persistence baseline; zero is not a missing-value surrogate.
    relevant = validation[validation['strain_or_target'].eq('AST') |
                          (pd.to_numeric(validation['time_h']).eq(rules['persistence_start_h']) &
                           validation['condition'].eq('astaxanthin concentration'))]
    if (pd.to_numeric(relevant['value']) <= 0).any():
        raise ValueError('Feedback ratio has a nonpositive denominator')


def apply_feedback(before: dict[str, Any], computed: pd.DataFrame,
                   rules_hash: str) -> dict[str, Any]:
    before = copy.deepcopy(before)
    expected_id = before.pop('state_id')
    if expected_id != 'before:' + digest(before):
        raise ValueError('Before-state identity mismatch')
    if before['phase'] != 'before_feedback':
        raise ValueError('Expected a pre-feedback state')
    genes = [r['gene'] for r in before['targets']]
    if computed['gene'].duplicated().any() or set(computed['gene']) != set(genes):
        raise ValueError('Computed update must cover the same targets')
    indexed = computed.set_index('gene')
    rows = []
    number_fields = ['terminal_yield_mg_L', 'fold_vs_ast', 'improvement_percent',
                     'persistence_change_percent', 'biomass_120h_od600', 'biomass_fold_vs_ast']
    for old in before['targets']:
        r = indexed.loc[old['gene']]
        row = {**old, 'evidence_tier': int(r['updated_evidence_tier']),
               'evidence_status': r['feedback_label'], 'outcome_status': r['outcome_status'],
               'next_cycle_action': r['next_cycle_action'], 'rule_trace': r['rule_trace']}
        for field in number_fields:
            value = r[field]
            row[field] = None if value == '' or pd.isna(value) else float(value)
        rows.append(row)
    state = {'schema_version': '1.0', 'phase': 'after_feedback', 'scope': before['scope'],
             'previous_state_id': expected_id, 'rules_sha256': rules_hash,
             'changed_model_element': 'Per-target evidence state and next-cycle action table; original v0.8 thresholds and metabolic Design model unchanged',
             'targets': rows,
             'metrics': {'target_count': len(rows), 'classified_target_count': len(rows),
                         'unassessed_target_count': 0,
                         'quantified_target_count': sum(r['outcome_status'] == 'quantified' for r in rows),
                         'next_action_class_count': len({r['next_cycle_action'] for r in rows}),
                         'tier1_count': sum(r['evidence_tier'] == 1 for r in rows),
                         'tier2_count': sum(r['evidence_tier'] == 2 for r in rows),
                         'tier3_count': sum(r['evidence_tier'] == 3 for r in rows)}}
    state['state_id'] = 'after:' + digest(state)
    return state


def run(config_path: Path, outdir: Path) -> dict[str, Any]:
    config = read_json(config_path)
    source = ROOT / config['source_root']
    data = source / 'data/processed/gsmm_evidence_v0_2'
    manifest = read_json(source / 'SOURCE_MANIFEST.json')
    for member, expected in manifest['members'].items():
        if sha(source / member) != expected:
            raise ValueError(f'Archive member changed: {member}')
    rule_path = source / config['rules_path']
    if sha(rule_path) != config['rules_sha256']:
        raise ValueError('Frozen feedback rules changed')
    freeze_path = ROOT / config['design_freeze_path']
    if sha(freeze_path) != config['design_freeze_sha256'] or read_json(freeze_path)['freeze_status'] != 'FABRIC_AI_V1_2_DESIGN_MODE_FINAL_FROZEN':
        raise ValueError('Learn requires the declared completed Design freeze')
    protected = config['frozen_design_guard']
    if any(sha(ROOT / name) != expected for name, expected in protected.items()):
        raise ValueError('Frozen Design inputs/results changed')
    outdir = outdir.resolve()
    if outdir.exists() and any(outdir.iterdir()):
        raise ValueError('Use an empty output directory; existing evidence is not overwritten')
    if outdir == source or source in outdir.parents:
        raise ValueError('Cannot write into recovered sources')
    outdir.mkdir(parents=True, exist_ok=True)
    selected = pd.read_csv(data / 'selected_targets_pre_validation.csv', keep_default_na=False)
    before = initialize_state(selected, sha(data / 'selected_targets_pre_validation.csv'))
    dump(outdir / 'before.json', before)
    # Outcome files are first loaded only after before.json has been materialized.
    validation = pd.read_csv(data / 'wetlab_validation.csv', keep_default_na=False)
    outcomes = pd.read_csv(data / 'round1_outcomes.csv', keep_default_na=False)
    rules = read_json(rule_path)
    validate_feedback(validation, outcomes, selected, rules)
    dump(outdir / 'experimental_feedback.json', {
        'measurements': validation.to_dict('records'), 'outcomes': outcomes.to_dict('records'),
        'source_hashes': {n: sha(data / n) for n in ['wetlab_validation.csv', 'round1_outcomes.csv']},
        'data_scope': 'Historical approximate figure digitization and categorical feasibility records; no replicate/statistical inference added'})
    computed = load_engine(config).compute_feedback_from_frames(validation, outcomes, selected, rules)
    stored = pd.read_csv(data / 'post_feedback_evidence.csv', keep_default_na=False)
    numeric_columns = ['value', 'time_h', 'plan_id', 'terminal_yield_mg_L', 'fold_vs_ast',
                       'improvement_percent', 'late_window_start_h', 'late_window_end_h',
                       'persistence_change_percent', 'biomass_120h_od600', 'biomass_fold_vs_ast',
                       'updated_evidence_tier', 'display_order']
    normalized_computed, normalized_stored = computed.copy(), stored.copy()
    for column in numeric_columns:
        normalized_computed[column] = pd.to_numeric(computed[column], errors='raise')
        normalized_stored[column] = pd.to_numeric(stored[column], errors='raise')
    pd.testing.assert_frame_equal(normalized_computed, normalized_stored,
                                  check_dtype=False, check_exact=False, rtol=1e-12, atol=1e-12)
    after = apply_feedback(before, computed, sha(rule_path))
    dump(outdir / 'after.json', after)
    computed.to_csv(outdir / 'recomputed_feedback.csv', index=False)
    comparisons = []
    by_gene = {r['gene']: r for r in after['targets']}
    for row in before['targets']:
        new = by_gene[row['gene']]
        comparisons.append({'gene': row['gene'], 'orf': row['orf'],
                            'before_evidence_tier': None, 'after_evidence_tier': new['evidence_tier'],
                            'before_action': row['next_cycle_action'], 'after_action': new['next_cycle_action'],
                            'action_changed': row['next_cycle_action'] != new['next_cycle_action'],
                            **{k: new[k] for k in ['fold_vs_ast', 'persistence_change_percent', 'biomass_fold_vs_ast']}})
    pd.DataFrame(comparisons).to_csv(outdir / 'comparison.csv', index=False)
    deltas = [{'metric': k, 'before': before['metrics'][k], 'after': after['metrics'][k],
               'delta': after['metrics'][k] - before['metrics'][k]} for k in before['metrics']]
    pd.DataFrame(deltas).to_csv(outdir / 'quantitative_delta.csv', index=False)
    checks = {'source_members_byte_exact': True, 'rules_unchanged': True,
              'before_uses_selection_only': all(r['evidence_tier'] is None for r in before['targets']),
              'same_six_targets': set(by_gene) == set(selected['gene']) and len(by_gene) == 6,
              'original_v08_full_output_reproduced': True,
              'all_six_actions_updated': all(r['action_changed'] for r in comparisons),
              'tier_counts_1_1_4': [after['metrics'][f'tier{i}_count'] for i in [1, 2, 3]] == [1, 1, 4],
              'design_guard_unchanged': all(sha(ROOT / n) == expected for n, expected in protected.items()),
              'no_invented_prior_numeric_tiers': all(r['evidence_tier'] is None for r in before['targets'])}
    report = {'status': 'PASSED' if all(checks.values()) else 'FAILED',
              'checks': checks, 'config_sha256': sha(config_path), 'engine_sha256': config['engine_sha256'],
              'before_state_id': before['state_id'], 'after_state_id': after['state_id'],
              'metric_interpretation': 'Evidence-state update counts; not predictive accuracy or production improvement',
              'quantitative_delta': deltas}
    dump(outdir / 'verification.json', report)
    dump(outdir / 'output_hashes.json', {p.name: sha(p) for p in sorted(outdir.iterdir()) if p.is_file()})
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=ROOT / 'configs/fabric_ai/learn_mode_v08_replay.json')
    parser.add_argument('--outdir', type=Path, required=True)
    args = parser.parse_args()
    return 0 if run(args.config.resolve(), args.outdir)['status'] == 'PASSED' else 1


if __name__ == '__main__':
    raise SystemExit(main())
