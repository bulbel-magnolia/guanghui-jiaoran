"""Exercise the frozen CLI in separate output directories; never replace results."""
from __future__ import annotations
import argparse
import concurrent.futures
import hashlib
import importlib.metadata
import json
import subprocess
import sys
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]
R=ROOT/'results/fabric_ai/20260908'
CLI='src/ai/fabric_ai_optimizer/fabric_ai_benchmark.py'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--outdir',required=True)
    args=parser.parse_args()
    out=Path(args.outdir).resolve()
    out.mkdir(parents=True,exist_ok=True)
    frozen=[ROOT/'models/fabric_ai/common_model.json',*R.glob('*.csv'),*R.glob('*.json'),* (ROOT/'configs/fabric_ai').glob('*.json')]
    before={str(p.relative_to(ROOT)):sha(p) for p in frozen}
    common=['--model','models/fabric_ai/common_model.json']
    jobs={
        'prepare':[CLI,'prepare',*common,'--condition','configs/fabric_ai/v1_glucose_reference.json','--outdir',str(out/'prepare'),'--tol','1e-7'],
    }
    for label,condition in [('v1','v1_glucose_reference'),('v2a','v2a_historical_ethanol_stage')]:
        jobs['evaluate_'+label]=[CLI,'evaluate',*common,'--condition',f'configs/fabric_ai/{condition}.json','--pool','results/fabric_ai/20260908/candidate_space.json','--outdir',str(out/label),'--floors','0.1,0.5,0.9','--mutant-growth-fraction','0.95','--tol','1e-7']
    jobs['rank']=[CLI,'rank','--metrics','v1_glucose_reference=results/fabric_ai/20260908/v1_candidate_metrics.csv','v2a_historical_ethanol_stage=results/fabric_ai/20260908/v2a_candidate_metrics.csv','--summaries','v1_glucose_reference=results/fabric_ai/20260908/v1_summary.json','v2a_historical_ethanol_stage=results/fabric_ai/20260908/v2a_summary.json','--primary','v1_glucose_reference','--outdir',str(out/'rank'),'--top-k','6','--tol','1e-7']
    def run(item):
        name,command=item
        print('START '+name,flush=True)
        result=subprocess.run([sys.executable,*command],cwd=ROOT,capture_output=True,text=True,encoding='utf8',errors='replace')
        log='$ '+subprocess.list2cmdline([sys.executable,*command])+'\n'+result.stdout+result.stderr+f'\nexit_code={result.returncode}\n'
        (out/(name+'.log')).write_text(log,encoding='utf8')
        print('END '+name+' exit='+str(result.returncode),flush=True)
        return name,result.returncode
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        exits=dict(executor.map(run,jobs.items()))
    checks={'cli_exit_codes_zero':all(v==0 for v in exits.values()),'frozen_inputs_and_results_unchanged':before=={str(p.relative_to(ROOT)):sha(p) for p in frozen}}
    if checks['cli_exit_codes_zero']:
        expected=json.loads((R/'candidate_space.json').read_text())
        actual=json.loads((out/'prepare/candidate_space.json').read_text())
        checks['prepare_235_gene_set_exact']=set(actual['genes'])==set(expected['genes']) and len(actual['genes'])==235
        checks['prepare_gpr_footprints_exact']=actual['footprints']==expected['footprints']
        checks['prepare_blocked_reactions_exact']=set(actual['blocked_reaction_ids'])==set(expected['blocked_reaction_ids'])
        for label in ['v1','v2a']:
            a=pd.read_csv(out/label/'candidate_metrics.csv').sort_values('gene').reset_index(drop=True)
            b=pd.read_csv(R/f'{label}_candidate_metrics.csv').sort_values('gene').reset_index(drop=True)
            checks[label+'_235_gene_set_exact']=len(a)==235 and a['gene'].equals(b['gene'])
            summary=json.loads((out/label/'summary.json').read_text())
            checks[label+'_completed_without_solver_failures']=summary['status']=='COMPLETED' and summary['solver_failures']==0
            checks[label+'_residuals_within_1e_7']=max(summary['max_mass_balance_residual'],summary['max_bound_residual'])<=1e-7
            checks[label+'_metrics_byte_exact']=sha(out/label/'candidate_metrics.csv')==sha(R/f'{label}_candidate_metrics.csv')
        for name in ['design_mode_ranking.csv','design_mode_topk.csv']:
            checks['rank_'+name+'_byte_exact']=sha(out/'rank'/name)==sha(R/name)
    report={'status':'PASSED' if all(checks.values()) else 'REVIEW_REQUIRED','python':sys.version,'dependencies':{p:importlib.metadata.version(p) for p in ['cobra','scipy','swiglpk','pandas','pytest']},'tolerance':1e-7,'checks':checks,'exit_codes':exits,'frozen_hashes':before}
    (out/'smoke_report.json').write_text(json.dumps(report,indent=2),encoding='utf8')
    combined=json.dumps(report,indent=2)+'\n\n'+''.join((out/(name+'.log')).read_text(encoding='utf8')+'\n' for name in jobs)
    (out/'reproduction_smoke_test.log').write_text(combined,encoding='utf8')
    print(json.dumps(report,indent=2),flush=True)
    return 0 if all(checks.values()) else 1

if __name__=='__main__':raise SystemExit(main())
