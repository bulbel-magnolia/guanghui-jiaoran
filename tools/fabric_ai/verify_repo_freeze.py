"""Run original frozen verifiers in their expected layout, without editing them."""
from __future__ import annotations
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULT = ROOT / "results/fabric_ai/20260908"
HISTORY = ROOT / "results/history/fabric_ai/20260908/pre_numeric_correction"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--outdir', required=True)
    args = parser.parse_args()
    out = Path(args.outdir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    stage = out / 'frozen_verifier_layout'
    stage.mkdir(parents=True, exist_ok=True)
    def copy(source, dest):
        target=stage/dest
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source,target)
    for label in ['v1','v2a']:
        copy(RESULT/f'{label}_candidate_metrics.csv',f'results/fabric_ai_{label}_metrics/candidate_metrics.csv')
        copy(RESULT/f'{label}_summary.json',f'results/fabric_ai_{label}_metrics/summary.json')
    copy(RESULT/'candidate_space.json','results/fabric_ai_primary_prepare/candidate_space.json')
    copy(RESULT/'prepare_summary.json','results/fabric_ai_primary_prepare/summary.json')
    for name in ['design_mode_ranking.csv','design_mode_topk.csv','summary.json']:
        copy(RESULT/name,'results/fabric_ai_ranking_numeric_correction_20260908/'+name)
        copy(HISTORY/name,'results/fabric_ai_design_mode_final/'+name)
    copy(HISTORY/'freeze_inputs/common_candidate_space_237_HISTORICAL.json','freeze_inputs/common_candidate_space_237_HISTORICAL.json')
    copy(HISTORY/'logs/05_tests.log','logs/05_tests.log')
    for name in ['verify_design_mode.py','verify_ranking_numeric_correction.py']:
        copy(ROOT/'src/ai/fabric_ai_optimizer'/name,'tools/'+name)
    (stage/'audit').mkdir(exist_ok=True)
    test=subprocess.run([sys.executable,'-m','pytest','tests/fabric_ai/test_ranker.py','-q','-p','no:cacheprovider'],cwd=ROOT,capture_output=True,text=True,encoding='utf8',errors='replace')
    log=test.stdout+test.stderr+f'\nexit_code={test.returncode}\n'
    print(log,flush=True)
    (stage/'logs/07_tests_ranking_numeric_correction.log').write_text(log,encoding='utf8')
    (out/'ranking_tests.log').write_text(log,encoding='utf8')
    if test.returncode:return test.returncode
    for name in ['verify_design_mode.py','verify_ranking_numeric_correction.py']:
        result=subprocess.run([sys.executable,str(stage/'tools'/name)],cwd=stage,capture_output=True,text=True,encoding='utf8',errors='replace')
        print(result.stdout+result.stderr,flush=True)
        (out/(name+'.log')).write_text(result.stdout+result.stderr,encoding='utf8')
        if result.returncode:return result.returncode
    for name in ['final_verification.json','ranking_numeric_correction_verification.json']:
        shutil.copyfile(stage/'audit'/name,out/name)
    report=json.loads((out/'ranking_numeric_correction_verification.json').read_text())
    assert len(report['checks'])==15 and all(report['checks'].values())
    print('Current checkout: 9 ranking tests and 15/15 final correction checks passed.')
    return 0

if __name__=='__main__':raise SystemExit(main())
