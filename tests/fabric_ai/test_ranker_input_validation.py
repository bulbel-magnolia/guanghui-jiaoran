"""Submission hardening uses real frozen evaluation rows, not synthetic keys."""
from pathlib import Path
import copy
import runpy
import pandas as pd
import pytest

ROOT=Path(__file__).resolve().parents[2]
M=runpy.run_path(str(ROOT/'src/ai/fabric_ai_optimizer/fabric_ai_benchmark.py'))
R=ROOT/'results/fabric_ai/20260908'
LABELS={'v1':'v1_glucose_reference','v2a':'v2a_historical_ethanol_stage'}

@pytest.fixture
def inputs():
    return ({label:pd.read_csv(R/f'{short}_candidate_metrics.csv') for short,label in LABELS.items()},
            {label:M['load_json'](R/f'{short}_summary.json') for short,label in LABELS.items()})

def run(data):
    return M['build_ranking'](*data,LABELS['v1'],6,1e-7)

def test_exact_frozen_output_and_infeasible_sensitivity_preserved(inputs):
    ranking,top,gate,scope,_=run(inputs)
    pd.testing.assert_frame_equal(ranking.reset_index(drop=True),pd.read_csv(R/'design_mode_ranking.csv'),check_dtype=False,check_exact=True)
    pd.testing.assert_frame_equal(top.reset_index(drop=True),pd.read_csv(R/'design_mode_topk.csv'),check_dtype=False,check_exact=True)
    assert gate and scope=='SECONDARY_FEASIBILITY_ORDER_ONLY'
    infeasible=inputs[0][LABELS['v2a']].query("growth_status == 'infeasible'")
    assert infeasible['gene'].tolist()==['YMR303C']

@pytest.mark.parametrize('column',['GCP','Pmin95','GR','mutant_mu_max','Pmax_0.1','PCR_0.1','footprint_size'])
@pytest.mark.parametrize('value',[float('nan'),float('inf')])
def test_corrupt_critical_metric_rejected(inputs,column,value):
    inputs[0][LABELS['v1']][column]=inputs[0][LABELS['v1']][column].astype(float)
    inputs[0][LABELS['v1']].loc[0,column]=value
    with pytest.raises(ValueError):run(inputs)

def test_all_nan_cannot_receive_production_scope(inputs):
    inputs[0][LABELS['v1']][['GCP','Pmin95']]=float('nan')
    with pytest.raises(ValueError):run(inputs)

@pytest.mark.parametrize('field,value',[('status','COMPLETED_WITH_SOLVER_FAILURES'),('solver_failures',1),
 ('evaluated_count',234),('pool_count',236),('solver_tolerance_requested',1e-5),
 ('model_sha256','a'*64),('pool_sha256','b'*64),('mutant_growth_fraction',0.90),
 ('max_mass_balance_residual',1e-4),('condition_id','wrong')])
def test_invalid_summary_rejected(inputs,field,value):
    inputs[1][LABELS['v2a']][field]=value
    with pytest.raises(ValueError):run(inputs)

@pytest.mark.parametrize('field',['model_sha256','pool_sha256','status','solver_failures'])
def test_missing_summary_provenance_rejected(inputs,field):
    del inputs[1][LABELS['v1']][field]
    with pytest.raises(ValueError):run(inputs)

@pytest.mark.parametrize('field',['GR','PCR_0.1'])
def test_inconsistent_derived_metric_rejected(inputs,field):
    inputs[0][LABELS['v1']].loc[0,field]=0.123456
    with pytest.raises(ValueError,match='Derived'):run(inputs)

def test_native_unit_ratio_noise_allowed(inputs):
    f=inputs[0][LABELS['v1']];wt=inputs[1][LABELS['v1']]['WT_mu_max']
    f.loc[0,'GR']+=1e-9/wt
    run(inputs)

def test_missing_condition_genes_rejected(inputs):
    inputs[0][LABELS['v2a']]=inputs[0][LABELS['v2a']].iloc[:-1]
    with pytest.raises(ValueError):run(inputs)

def test_duplicate_genes_rejected(inputs):
    f=inputs[0][LABELS['v1']];f.loc[1,'gene']=f.loc[0,'gene']
    with pytest.raises(ValueError,match='Duplicate'):run(inputs)

def test_footprint_mismatch_rejected(inputs):
    inputs[0][LABELS['v2a']].loc[0,'actual_footprint_match']=False
    with pytest.raises(ValueError,match='Footprint'):run(inputs)

def test_invalid_fractional_footprint_rejected(inputs):
    inputs[0][LABELS['v1']]['footprint_size']=inputs[0][LABELS['v1']]['footprint_size'].astype(float)
    inputs[0][LABELS['v1']].loc[0,'footprint_size']=1.5
    with pytest.raises(ValueError):run(inputs)

def test_solver_failure_row_rejected(inputs):
    inputs[0][LABELS['v1']].loc[0,'status_95mut']='solver_failure:infeasible/optimal'
    with pytest.raises(ValueError):run(inputs)

def test_primary_cannot_claim_infeasible_to_hide_nan(inputs):
    f=inputs[0][LABELS['v1']]
    f.loc[0,['growth_status','status_95mut','Pmin95']]=['infeasible','mutant_infeasible',float('nan')]
    with pytest.raises(ValueError):run(inputs)

def test_infeasible_sensitivity_cannot_carry_positive_output(inputs):
    f=inputs[0][LABELS['v2a']];f.loc[f['gene'].eq('YMR303C'),'GCP']=0.5
    with pytest.raises(ValueError):run(inputs)
