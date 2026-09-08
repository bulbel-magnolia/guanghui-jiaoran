"""Check existing AISB26 files; an optional signed ZIP is used only for comparison."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def fasta(raw):
    lines=raw.decode('utf-8-sig').splitlines()
    assert sum(line.startswith('>') for line in lines)==1,'Expected one FASTA record'
    sequence=''.join(line.strip() for line in lines if not line.startswith('>')).upper()
    assert re.fullmatch('[ACGTRYSWKMBDHVN]+',sequence),'Invalid FASTA alphabet'
    return sequence

def genbank(raw):
    text=raw.decode('utf-8-sig')
    origins=re.findall(r'^ORIGIN\s*\n(.*?)^//',text,re.M|re.S)
    assert len(origins)==1,'Expected one GenBank record'
    sequence=re.sub(r'[\s0-9]','',origins[0]).upper()
    assert re.fullmatch('[ACGTRYSWKMBDHVN]+',sequence),'Invalid GenBank alphabet'
    length=int(re.search(r'^LOCUS\s+\S+\s+(\d+)\s+bp',text,re.M).group(1))
    assert len(sequence)==length,'GenBank LOCUS length mismatch'
    cds=[location.strip() for location in re.findall(r'^     CDS\s+([^\n]+)',text,re.M)]
    return sequence,cds

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',required=True)
    parser.add_argument('--source-zip',help='Exact FABRIC-AI_v0.8_phase2_baseline_signed_20260905.zip')
    args=parser.parse_args()
    archive=zipfile.ZipFile(args.source_zip) if args.source_zip else None
    rows=[]
    def add(part,check,status,detail):rows.append(dict(part_id=part,check=check,status=status,detail=detail))
    for part,length in [('AISB26-045-001',12584),('AISB26-045-002',690)]:
        folder=ROOT/'parts'/part
        for name in ['sequence.fasta','registry_export.gb','map.svg','metadata.yaml','characterization.md']:
            p=folder/name
            add(part,'file_exists:'+name,'PASS' if p.is_file() else 'MISSING',str(p.relative_to(ROOT)))
            if p.is_file():add(part,'sha256:'+name,'RECORDED',hashlib.sha256(p.read_bytes()).hexdigest())
            if archive and name in (['sequence.fasta','registry_export.gb','map.svg'] if part.endswith('001') else ['registry_export.gb','map.svg']):
                matches=[n for n in archive.namelist() if n.endswith(f'parts/{part}/{name}') and not n.startswith('__MACOSX/')]
                if len(matches)!=1:add(part,'signed_source:'+name,'FAIL','Missing/ambiguous archive member')
                else:add(part,'signed_source:'+name,'PASS' if p.is_file() and p.read_bytes()==archive.read(matches[0]) else 'FAIL',matches[0])
        f=folder/'sequence.fasta';g=folder/'registry_export.gb'
        if f.exists():
            sequence=fasta(f.read_bytes());add(part,'fasta_length','PASS' if len(sequence)==length else 'FAIL',str(len(sequence)))
        if f.exists() and g.exists():
            gb,cds=genbank(g.read_bytes())
            add(part,'fasta_genbank_sequence','PASS' if sequence==gb else 'FAIL',f'FASTA {len(sequence)} bp; GenBank {len(gb)} bp')
            if part.endswith('002'):
                add(part,'full_length_CDS_1_690','PASS' if cds==['1..690'] and sequence==gb else 'FAIL',json.dumps(cds))
        else:add(part,'fasta_genbank_sequence','BLOCKED','Required FASTA and/or GenBank missing')
        svg=folder/'map.svg'
        if svg.exists():
            tree=ET.parse(svg)
            add(part,'svg_document','PASS' if tree.getroot().tag.endswith('svg') else 'FAIL','XML parsed')
            references=[value for node in tree.iter() for key,value in node.attrib.items() if key.rsplit('}',1)[-1] in ['href','src']]
            relative=[v for v in references if not v.startswith(('#','//')) and not re.match(r'^[a-z][a-z0-9+.-]*:',v,re.I)]
            missing=[v for v in relative if not (folder/v.split('#')[0]).exists()]
            add(part,'svg_relative_paths','PASS' if not missing else 'FAIL',json.dumps({'relative_references':relative,'missing':missing}))
        if not archive:add(part,'signed_source_provenance','BLOCKED','Specified signed ZIP not available; no alternate source substituted')
    output=Path(args.out);output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('w',newline='',encoding='utf-8-sig') as fp:
        w=csv.DictWriter(fp,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    passed=all(r['status'] not in ['FAIL','MISSING','BLOCKED'] for r in rows)
    print(json.dumps({'status':'PASSED' if passed else 'BLOCKED','rows':len(rows)},ensure_ascii=False))
    return 0 if passed else 1

if __name__=='__main__':raise SystemExit(main())
