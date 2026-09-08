import csv,json,pathlib,re,urllib.parse
ROOT=pathlib.Path(__file__).resolve().parents[2]
OUT=ROOT/'results/evidence/20260908/code_parts_sync'
OUT.mkdir(parents=True,exist_ok=True)
rows=[]
def add(path,line,kind,status,detail,target=''):
    rows.append(dict(path=path,line=line,category=kind,status=status,target=target,detail=detail[:500]))
patterns={
 'template':r'YYYY-MM-DD|<例|<姓名|BBa_XXXX|<your-repo-url>|<repo-url>|<repo-dir>|<hash>',
 'old_candidate_pool':r'237[ -]gene(?:s)?|237\s*个?基因',
 'old_top6':r'YOR311C',
 'optenvelope_zero_claim':r'true zero candidate|真实零候选',
 'production_superiority':r'production[-_ ]superiority|生产性能优于公开基线',
}
def context(relative):
    if relative.startswith('results/history/'):return 'HISTORICAL_AUDIT'
    if relative.endswith(('DESIGN_MODE_V1_2_AUDIT.md','DESIGN_MODE_PRIMARY_RESULT.json')):return 'HISTORICAL_AUDIT'
    if relative.endswith('RANKING_NUMERIC_EQUIVALENCE_CORRECTION.md') and not relative.endswith('README_RANKING_NUMERIC_EQUIVALENCE_CORRECTION.md'):return 'TASK_INSTRUCTION'
    if relative.endswith('_TASK.md') or relative.endswith('_TASK_V1.md'):return 'TASK_INSTRUCTION'
    if relative.startswith('results/baseline/20260907/'):return 'HISTORICAL_BASELINE'
    if relative.startswith('src/') or relative.startswith('tests/') or relative.startswith('tools/'):return 'CODE_OR_CONTRACT'
    return 'REVIEW_CONTEXT'
for p in sorted(ROOT.rglob('*')):
    if not p.is_file():continue
    rel=p.relative_to(ROOT).as_posix()
    if any(x in p.relative_to(ROOT).parts for x in ['.git','.reproduction','__pycache__','.runtime']) or rel.startswith('results/evidence/20260908/code_parts_sync/'):continue
    if p.suffix.lower() not in ['.md','.json','.yaml','.yml','.txt','.py','.csv','.html']:continue
    if p.stat().st_size>2_000_000:continue
    text=p.read_text(encoding='utf8',errors='replace')
    for n,line in enumerate(text.splitlines(),1):
        for kind,pat in patterns.items():
            if re.search(pat,line,re.I):
                status=context(rel)
                if kind=='production_superiority' and re.search(r'false|prohibited.*true|no production|cannot support|do not support|not support',line,re.I):status='PROHIBITION_NOT_CONFLICT'
                if p.suffix=='.csv' and kind=='old_top6':status='GENE_DATA_NOT_TOP6_CLAIM'
                if p.suffix=='.json' and kind=='old_top6' and not any(x in rel for x in ['summary','FINAL','verification']):status='GENE_DATA_NOT_TOP6_CLAIM'
                add(rel,n,kind,status,line.strip())
        if rel=='README.md' and re.search(r'45%|零化学废水|零毒排放|8 条通路|48 项',line):
            add(rel,n,'science_claim','SCIENCE_REVIEW_REQUIRED',line.strip())
        if rel=='wiki/Verifiability.md' and re.search(r'27%|0\.27|0\.61|生物学重复',line):
            add(rel,n,'science_claim','SCIENCE_REVIEW_REQUIRED',line.strip())
    if p.suffix.lower() not in ['.md','.html']:continue
    # Inline Markdown links, reference definitions and HTML href/src references.
    links=list(re.finditer(r'(?<!!)\[[^\]\n]*\]\((<[^>]+>|[^\s)]+)(?:\s+"[^"]*")?\)',text))
    links+=list(re.finditer(r'!\[[^\]\n]*\]\((<[^>]+>|[^\s)]+)(?:\s+"[^"]*")?\)',text))
    links+=list(re.finditer(r'^\s*\[[^\]]+\]:\s*(\S+)',text,re.M))
    links+=list(re.finditer(r'(?:href|src)=["\']([^"\']+)["\']',text))
    for m in links:
        target=m.group(1).strip('<>')
        if target.startswith(('#','//')) or re.match(r'^[a-z][a-z0-9+.-]*:',target,re.I):continue
        path=urllib.parse.unquote(target.split('#',1)[0].split('?',1)[0])
        if not path:continue
        resolved=(ROOT/path.lstrip('/')) if path.startswith('/') else p.parent/path
        exists=resolved.exists()
        add(rel,text.count('\n',0,m.start())+1,'relative_link','EXISTS' if exists else 'BROKEN',target,target)
required=['Home','Project-Description','Design','AI-Computational-Methods','Wet-Lab-Experiments','Integrated-Validation','Verifiability','Engineering-Cycle','Parts','Human-Practices','AI-Ethics-Safety','Education','Collaboration','Attributions']
for page in required:
    path='wiki/'+page+'.md';add(path,0,'wiki_page','EXISTS' if (ROOT/path).is_file() else 'MISSING','Required/recommended page inventory from repository README')
for part in ['AISB26-045-001','AISB26-045-002']:
    for name in ['sequence.fasta','metadata.yaml','characterization.md','registry_export.gb','map.svg']:
        path=f'parts/{part}/{name}';add(path,0,'part_file','EXISTS' if (ROOT/path).is_file() else 'MISSING','Required five-file inventory')
for name in ['v1_glucose_reference.json','v2a_historical_ethanol_stage.json']:
    p=ROOT/'configs/fabric_ai'/name
    target=json.loads(p.read_text())['protected_reaction_ids_file']
    add(p.relative_to(ROOT).as_posix(),0,'frozen_condition_relative_path','EXISTS' if (p.parent/target).exists() else 'BROKEN',target,target)
with (OUT/'consistency_scan.csv').open('w',newline='',encoding='utf-8-sig') as fp:
    w=csv.DictWriter(fp,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
from collections import Counter
print(json.dumps(dict(Counter(r['status'] for r in rows)),indent=2))
for r in rows:
    if r['status'] in ['BROKEN','MISSING'] or (r['status']=='REVIEW_CONTEXT' and r['category']!='relative_link'):
        print(r['path'],r['line'],r['category'],r['status'],r['detail'][:180])
