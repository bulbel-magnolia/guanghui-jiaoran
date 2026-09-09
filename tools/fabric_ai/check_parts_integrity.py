"""Check current submitted parts against archived source and declared revision.

An optional original ZIP verifies the archived provenance, not byte equality of
an intentionally revised annotation/map with its predecessor.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile
from Bio import SeqIO

ROOT=Path(__file__).resolve().parents[2]
AUDIT=ROOT/'results/evidence/20260909/phirex_annotation'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',required=True,type=Path);parser.add_argument('--source-zip',type=Path);a=parser.parse_args()
    revision=json.loads((AUDIT/'change_manifest.json').read_text())
    source=json.loads((AUDIT/'original_file_hashes.json').read_text())
    rows=[]
    def add(part,check,ok,detail):rows.append({'part_id':part,'check':check,'status':'PASS' if ok else 'FAIL','detail':detail})
    for part,length in [('AISB26-045-001',12584),('AISB26-045-002',690)]:
        folder=ROOT/'parts'/part;old=AUDIT/'original'/part
        for name in ['sequence.fasta','registry_export.gb','metadata.yaml','characterization.md','map.svg']:
            add(part,'exists:'+name,(folder/name).is_file(),str((folder/name).relative_to(ROOT)))
        for name in ['sequence.fasta','registry_export.gb','map.svg']:
            add(part,'source_archive_hash:'+name,sha(old/name)==source[part+'/'+name],source[part+'/'+name])
        fa=SeqIO.read(folder/'sequence.fasta','fasta');gb=SeqIO.read(folder/'registry_export.gb','genbank');og=SeqIO.read(old/'registry_export.gb','genbank')
        add(part,'sequence_length',len(fa)==len(gb)==length,str(length))
        add(part,'FASTA_equals_GenBank',str(fa.seq).upper()==str(gb.seq).upper(),'Per-base comparison')
        add(part,'DNA_equals_original',str(gb.seq).upper()==str(og.seq).upper() and (folder/'sequence.fasta').read_bytes()==(old/'sequence.fasta').read_bytes(),'No nucleotide edits')
        if part.endswith('001'):
            add(part,'declared_annotation_hash',sha(folder/'registry_export.gb')==revision['revised_genbank_sha256'],revision['revision_id'])
            add(part,'declared_coordinate_map_hash',sha(folder/'map.svg')==revision['revised_map_sha256'],'Regenerated from revised feature types; coordinates unchanged')
        else:
            add(part,'unchanged_GenBank',sha(folder/'registry_export.gb')==sha(old/'registry_export.gb'),'BmCBP GenBank not edited')
            cds=[f for f in gb.features if f.type=='CDS']
            add(part,'CDS_1_690',len(cds)==1 and int(cds[0].location.start)==0 and int(cds[0].location.end)==690,'Vector fusion context retained')
        tree=ET.parse(folder/'map.svg');add(part,'SVG_parses',tree.getroot().tag.endswith('svg'),'XML parse')
        if a.source_zip:
            with zipfile.ZipFile(a.source_zip) as z:
                # DNA is invariant; annotation corrections are assessed above.
                raw=z.read('parts/'+part+'/sequence.fasta')
                seq=''.join(l.strip() for l in raw.decode('utf-8-sig').splitlines() if not l.startswith('>')).upper()
                add(part,'original_zip_sequence',seq==str(fa.seq).upper(),a.source_zip.name)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    with a.out.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=['part_id','check','status','detail']);w.writeheader();w.writerows(rows)
    ok=all(r['status']=='PASS' for r in rows);print(json.dumps({'status':'PASSED' if ok else 'FAILED','checks':len(rows)}));return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
