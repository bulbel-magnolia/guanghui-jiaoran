"""Recovered feedback replay and new state-transition checks.

Perturbed values below are test-only fixtures and never replace observations.
"""
from pathlib import Path
import copy
import runpy
import pandas as pd
import pytest

ROOT=Path(__file__).resolve().parents[2]
M=runpy.run_path(str(ROOT/'src/ai/fabric_ai_optimizer/learn_mode.py'))
CONFIG=ROOT/'configs/fabric_ai/learn_mode_v08_replay.json'
C=M['read_json'](CONFIG)
D=ROOT/C['source_root']/'data/processed/gsmm_evidence_v0_2'
ENGINE=M['load_engine'](C)

@pytest.fixture
def data():
    return [pd.read_csv(D/n,keep_default_na=False) for n in ['wetlab_validation.csv','round1_outcomes.csv','selected_targets_pre_validation.csv']]+[M['read_json'](D/'feedback_rules.json')]

def state(selected):return M['initialize_state'](selected,M['sha'](D/'selected_targets_pre_validation.csv'))

def test_before_has_no_fabricated_tiers_or_ranks(data):
    b=state(data[2]);assert len(b['targets'])==6
    assert all(r['evidence_tier'] is None and 'rank' not in r for r in b['targets'])
    assert b['metrics']['classified_target_count']==0

def test_before_is_deterministic(data):assert state(data[2])==state(data[2])

def test_selection_label_leak_rejected(data):
    data[2].loc[0,'feedback_label']='positive'
    with pytest.raises(ValueError,match='leaked'):state(data[2])

def test_selection_column_leak_rejected(data):
    data[2]['updated_evidence_tier']=1
    with pytest.raises(ValueError,match='leaked'):state(data[2])

def test_duplicate_selection_rejected(data):
    data[2].loc[1,'gene']=data[2].loc[0,'gene']
    with pytest.raises(ValueError):state(data[2])

def test_original_thresholds_unchanged(data):
    rules=data[3]
    assert [rules[k] for k in ['positive_terminal_fold_min','negative_terminal_fold_max','persistence_change_percent_min','biomass_fold_min']]==[1.05,0.95,0.0,0.9]
    assert M['sha'](D/'feedback_rules.json')==C['rules_sha256']

def test_computed_metrics_and_actions(data):
    M['validate_feedback'](*data)
    a=M['apply_feedback'](state(data[2]),ENGINE.compute_feedback_from_frames(*data),C['rules_sha256'])
    rows={r['gene']:r for r in a['targets']}
    assert rows['PAN5']['fold_vs_ast']==pytest.approx(0.67/0.47)
    assert rows['PAN5']['persistence_change_percent']==pytest.approx((0.67/0.61-1)*100)
    assert rows['MDE1']['persistence_change_percent']==pytest.approx((0.36/0.42-1)*100)
    assert [a['metrics'][f'tier{i}_count'] for i in [1,2,3]]==[1,1,4]
    assert a['metrics']['classified_target_count']==6

def test_missing_measurement_rejected(data):
    data[0]=data[0][~(data[0]['strain_or_target'].eq('delta_PAN5') & pd.to_numeric(data[0]['time_h']).eq(120))]
    with pytest.raises(ValueError):ENGINE.compute_feedback_from_frames(*data)

def test_missing_outcome_rejected(data):
    data[1]=data[1].iloc[:-1]
    with pytest.raises(ValueError):M['validate_feedback'](*data)

def test_duplicate_measurement_rejected(data):
    data[0]=pd.concat([data[0],data[0].iloc[:1]])
    with pytest.raises(ValueError):M['validate_feedback'](*data)

@pytest.mark.parametrize('bad',[float('nan'),float('inf'),-1.0])
def test_invalid_measurement_rejected(data,bad):
    data[0].loc[0,'value']=bad
    with pytest.raises(ValueError):M['validate_feedback'](*data)

def test_wrong_unit_rejected(data):
    data[0].loc[0,'unit']='g/L'
    with pytest.raises(ValueError):M['validate_feedback'](*data)

def test_tampered_before_rejected(data):
    b=state(data[2]);b['targets'][0]['evidence_tier']=1
    with pytest.raises(ValueError,match='identity'):M['apply_feedback'](b,ENGINE.compute_feedback_from_frames(*data),C['rules_sha256'])

def test_gene_agnostic_rule_responds_to_test_only_perturbation(data):
    mask=data[0]['strain_or_target'].eq('delta_PAN5') & data[0]['condition'].eq('astaxanthin concentration') & pd.to_numeric(data[0]['time_h']).eq(120)
    data[0].loc[mask,'value']=0.4
    f=ENGINE.compute_feedback_from_frames(*data).set_index('gene')
    assert f.loc['PAN5','updated_evidence_tier']==2

def test_full_reproduction_and_immutable_design(tmp_path):
    report=M['run'](CONFIG,tmp_path/'run1')
    second=M['run'](CONFIG,tmp_path/'run2')
    assert report==second and all(report['checks'].values())
    for name in ['before.json','after.json','comparison.csv','experimental_feedback.json','recomputed_feedback.csv','quantitative_delta.csv','verification.json']:
        assert (tmp_path/'run1'/name).read_bytes()==(tmp_path/'run2'/name).read_bytes()

def test_existing_evidence_not_overwritten(tmp_path):
    p=tmp_path/'out';p.mkdir();(p/'existing').write_text('keep')
    with pytest.raises(ValueError,match='empty output'):M['run'](CONFIG,p)

def test_bad_freeze_hash_rejected(tmp_path):
    config=copy.deepcopy(C);config['design_freeze_sha256']='0'*64
    p=tmp_path/'config.json';M['dump'](p,config)
    with pytest.raises(ValueError,match='Design freeze'):M['run'](p,tmp_path/'out')
