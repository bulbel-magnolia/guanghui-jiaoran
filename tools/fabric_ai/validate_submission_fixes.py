"""Run narrow submission-hardening checks without re-solving the frozen model."""
from __future__ import annotations
import argparse
import ast
import hashlib
import importlib.metadata
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote,urlsplit
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]
E=ROOT/'results/evidence/20260909'
F=ROOT/'results/fabric_ai/20260908'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def dump(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8')

def scan_links():
    paths=[* (ROOT/'wiki').glob('*.md'),ROOT/'README.md',ROOT/'attributions.md',ROOT/'AI-USE-DISCLOSURE.md',* (ROOT/'parts').rglob('*.md')]
    paths += [p for p in E.rglob('*.md') if 'recovered_v08' not in p.parts and 'validation' not in p.parts]
    paths += list((ROOT/'results/fabric_ai/20260909').rglob('README.md'))
    missing=[];count=0
    for p in paths:
        s=p.read_text(encoding='utf-8')
        # Code fences contain command examples, not links.
        s=re.sub(r'```.*?```','',s,flags=re.S)
        urls=re.findall(r'!?\[[^\]\n]*\]\(([^)\n]+)\)',s)
        urls += re.findall(r'(?:src|href)=["\']([^"\']+)["\']',s)
        for u in urls:
            u=u.strip().strip('<>')
            if re.match(r'^[a-z][a-z0-9+.-]*:',u,re.I) or u.startswith(('#','//')):continue
            pathname=unquote(u.split('#',1)[0].split('?',1)[0])
            if not pathname:continue
            count+=1
            if not (p.parent/pathname).resolve().exists():missing.append({'file':str(p.relative_to(ROOT)),'target':u})
    return {'scope':'Relative file targets in all Wiki pages, current root/parts docs, new evidence narrative. Immutable recovered archive prose and historical audit copies excluded; no external/browser or fragment rendering claim.','files_scanned':len(paths),'references_checked':count,'missing':missing}

def main():
    p=argparse.ArgumentParser();p.add_argument('--outdir',required=True,type=Path);a=p.parse_args();out=a.outdir.resolve()
    if out.exists() and any(out.iterdir()):raise ValueError('Use a new empty validation output directory')
    out.mkdir(parents=True,exist_ok=True);dump(out/'verification.json',{'status':'RUNNING'})
    checks={};commands={}
    def execute(name,args):
        r=subprocess.run([sys.executable,*args],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
        text='$ python '+' '.join(args)+'\n'+r.stdout+r.stderr+f'\nexit_code={r.returncode}\n'
        (out/(name+'.log')).write_text(text,encoding='utf-8');commands[name]={'args':args,'exit_code':r.returncode};checks[name+'_exit_zero']=r.returncode==0
        print(name,r.returncode,flush=True);return r,text
    tests={}
    for name,path,count in [('frozen9','tests/fabric_ai/test_ranker.py',9),('hardening','tests/fabric_ai/test_ranker_input_validation.py',40),('learn_tests','tests/fabric_ai/test_learn_mode.py',19)]:
        r,text=execute(name,['-m','pytest',path,'-q','-p','no:cacheprovider']);m=re.search(r'(\d+) passed',text);tests[name]=int(m.group(1)) if m else 0;checks[name+'_expected_count']=tests[name]==count
    execute('frozen_verifiers',['tools/fabric_ai/verify_repo_freeze.py','--outdir',str(out/'frozen_verifiers')])
    v=out/'frozen_verifiers/ranking_numeric_correction_verification.json'
    checks['original_final_verification_15_of_15']=v.exists() and len(load(v)['checks'])==15 and all(load(v)['checks'].values())
    execute('parts_integrity',['tools/fabric_ai/check_parts_integrity.py','--out',str(out/'parts_integrity.csv')])
    execute('feature_audit',['tools/fabric_ai/audit_phirex_features.py','--outdir',str(out/'feature_audit')])
    execute('learn_reproduction',['src/ai/fabric_ai_optimizer/learn_mode.py','--outdir',str(out/'learn')])
    learned=ROOT/'results/fabric_ai/20260909/learn_mode_iteration'
    same={n:(out/'learn'/n).exists() and (out/'learn'/n).read_bytes()==(learned/n).read_bytes() for n in ['before.json','experimental_feedback.json','after.json','comparison.csv','recomputed_feedback.csv','quantitative_delta.csv','verification.json']}
    checks['learn_reproduction_byte_exact']=all(same.values());dump(out/'learn_reproduction_comparison.json',same)
    labels=['v1_glucose_reference','v2a_historical_ethanol_stage']
    args=['src/ai/fabric_ai_optimizer/fabric_ai_benchmark.py','rank','--metrics',*[f'{label}=results/fabric_ai/20260908/{short}_candidate_metrics.csv' for short,label in zip(['v1','v2a'],labels)],'--summaries',*[f'{label}=results/fabric_ai/20260908/{short}_summary.json' for short,label in zip(['v1','v2a'],labels)],'--primary',labels[0],'--outdir',str(out/'rank'),'--top-k','6','--tol','1e-7']
    execute('strict_rank_reproduction',args)
    rank_comparison={}
    for n in ['design_mode_ranking.csv','design_mode_topk.csv']:
        try:
            pd.testing.assert_frame_equal(pd.read_csv(out/'rank'/n),pd.read_csv(F/n),check_dtype=False,check_exact=True)
            rank_comparison[n]={'all_cells_exact':True,'bytes_exact':sha(out/'rank'/n)==sha(F/n)}
        except Exception as exc:rank_comparison[n]={'all_cells_exact':False,'error':str(exc)}
    checks['strict_rank_all_frozen_cells_exact']=all(v['all_cells_exact'] for v in rank_comparison.values())
    dump(out/'rank_output_comparison.json',{'tables':rank_comparison,'scope':load(out/'rank/summary.json')['topk_interpretation']})
    checks['scope_unchanged']=load(out/'rank/summary.json')['topk_interpretation']=='SECONDARY_FEASIBILITY_ORDER_ONLY'
    protected=load(E/'pre_repair_protected_hashes.json');changes=[n for n,h in protected.items() if sha(ROOT/n)!=h]
    checks['frozen_inputs_results_configs_baselines_unchanged']=not changes
    dump(out/'protected_files_comparison.json',{'checked_count':len(protected),'changed':changes})
    original=load(E/'original_sorting_kernel_hash.json')
    checks['historical9_test_source_bytes_unchanged']=sha(ROOT/'tests/fabric_ai/test_ranker.py')==original['original_test_file_sha256']
    source=ast.parse((ROOT/'src/ai/fabric_ai_optimizer/fabric_ai_benchmark.py').read_text())
    node=next(n for n in source.body if isinstance(n,ast.FunctionDef) and n.name=='_rank_validated_frames');node.name='build_ranking'
    checks['sorting_kernel_ast_unchanged']=hashlib.sha256(ast.dump(node,include_attributes=False).encode()).hexdigest()==original['original_function_ast_sha256']
    wiki='\n'.join(p.read_text() for p in (ROOT/'wiki').glob('*.md'))
    stale={'A480_false_raw_pointer_absent':'A480 原始值与平均值见元件表征' not in wiki,
           'old_Top6_not_in_current_Wiki':'YOR311C' not in wiki,
           'obsolete_pool_not_current_claim':not bool(re.search(r'237\s*(?:genes|个基因)',wiki)),
           'C3_5_not_claimed_from_handbook': '当前证据不足' in (ROOT/'wiki/Collaboration.md').read_text() and load(E/'medal_evidence_status.json')['C3_5']['status']=='C3_5_CURRENT_EVIDENCE_NOT_SUFFICIENT',
           'C3_2_no_superiority_claim':not load(E/'medal_evidence_status.json')['C3_2']['production_superiority_claim']}
    dump(out/'stale_claim_scan.json',{'scope':'Targeted requested claims, not a generic literature audit','checks':stale});checks['targeted_stale_claims_corrected']=all(stale.values())
    # The report itself is linked from the summary; materialize it before scanning.
    dump(out/'relative_links.json',{'status':'RUNNING'})
    links=scan_links();dump(out/'relative_links.json',links);checks['relative_file_links_exist']=not links['missing']
    from PIL import Image
    import numpy as np
    P=E/'phirex_annotation';record=load(P/'figure_edit_record.json');before=np.array(Image.open(P/'original/phirex-expression.webp').convert('RGB'));after=np.array(Image.open(ROOT/'wiki/assets/figures/phirex-expression.webp').convert('RGB'));mask=np.zeros(before.shape[:2],dtype=bool)
    for x1,y1,x2,y2 in record['edited_rectangles_xyxy']:mask[y1:y2,x1:x2]=True
    checks['figure_outside_edit_mask_unchanged']=np.array_equal(before[~mask],after[~mask])
    checks['figure_matches_declared_edit_hash']=sha(ROOT/'wiki/assets/figures/phirex-expression.webp')==record['output_sha256']
    import cairosvg
    cairosvg.svg2png(url=str(ROOT/'parts/AISB26-045-001/map.svg'),write_to=str(out/'phirex_map_render.png'),output_width=1450)
    checks['SVG_render_created']=(out/'phirex_map_render.png').stat().st_size>0
    report={'status':'PASSED' if all(checks.values()) else 'FAILED','checks':checks,'tests':tests,'original_final_verification':'15/15' if checks['original_final_verification_15_of_15'] else 'FAILED','environment':{'python':sys.version,'dependencies':{p:importlib.metadata.version(p) for p in ['pandas','pytest','biopython','PyYAML','CairoSVG','Pillow','numpy']}},'commands':commands,'scope':'Submission hardening + recovered Learn replay. No 235x2 metabolic re-evaluation; no new wet-lab data; no remote submission.', 'relative_links':{'references_checked':links['references_checked'],'missing_count':len(links['missing'])}}
    dump(out/'verification.json',report)
    dump(out/'validation_files_sha256.json',{str(p.relative_to(out)):sha(p) for p in sorted(out.rglob('*')) if p.is_file() and p.name!='validation_files_sha256.json' and '__pycache__' not in p.parts})
    print(json.dumps(report,ensure_ascii=False,indent=2));return 0 if all(checks.values()) else 1
if __name__=='__main__':raise SystemExit(main())
