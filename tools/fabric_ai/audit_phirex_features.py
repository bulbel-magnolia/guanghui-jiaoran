"""Audit current part sequences/features; optionally regenerate the coordinate map."""
from __future__ import annotations
import argparse
import hashlib
import html
import json
from pathlib import Path
from Bio import SeqIO

ROOT=Path(__file__).resolve().parents[2]

def main():
    p=argparse.ArgumentParser();p.add_argument('--outdir',type=Path,required=True);p.add_argument('--write-map',action='store_true');a=p.parse_args()
    a.outdir.mkdir(parents=True,exist_ok=True)
    checks={};parts={}
    for ident, length in [('AISB26-045-001',12584),('AISB26-045-002',690)]:
        folder=ROOT/'parts'/ident
        old=ROOT/'results/evidence/20260909/phirex_annotation/original'/ident
        rec=SeqIO.read(folder/'registry_export.gb','genbank');fa=SeqIO.read(folder/'sequence.fasta','fasta')
        checks[ident+'_sequence_equal']=str(rec.seq).upper()==str(fa.seq).upper() and len(rec)==length
        checks[ident+'_DNA_bytes_unchanged']=(folder/'sequence.fasta').read_bytes()==(old/'sequence.fasta').read_bytes()
        checks[ident+'_five_files_exist']=all((folder/n).is_file() for n in ['sequence.fasta','registry_export.gb','map.svg','metadata.yaml','characterization.md'])
        features=[]
        for f in rec.features:
            row={'label':f.qualifiers.get('label',[f.type])[0],'type':f.type,'start_1based':int(f.location.start)+1,'end_1based':int(f.location.end),'strand':f.location.strand,'length':len(f)}
            if f.type=='CDS':
                seq=f.extract(rec.seq)
                if ident.endswith('002'):
                    aa=str(seq.translate());valid=len(seq)%3==0 and '*' not in aa
                    row['context']='vector-provided initiation/fusion context; no independent start/stop required'
                else:
                    try:aa=str(seq.translate(cds=True));valid=True
                    except Exception as e:aa='';valid=False;row['error']=str(e)
                row['reading_frame_check']=valid
                row['translation_sha256']=hashlib.sha256(aa.encode()).hexdigest()
                checks[ident+'_'+row['label']+'_frame']=valid
            features.append(row)
        parts[ident]={'features':features,'sequence_length':len(rec)}
    manifest=json.loads((ROOT/'results/evidence/20260909/phirex_annotation/change_manifest.json').read_text())
    checks['revised_genbank_matches_declared_hash']=hashlib.sha256((ROOT/'parts/AISB26-045-001/registry_export.gb').read_bytes()).hexdigest()==manifest['revised_genbank_sha256']
    feats=parts['AISB26-045-001']['features']
    checks['four_unresolved_regions_are_misc_feature']=all(next(f for f in feats if f['label']==name)['type']=='misc_feature' for name in manifest['unresolved_CDS_intervals'])
    if a.write_map:
        visible=[f for f in feats if f['type']!='source' and f['length']!=12584]
        height=135+len(visible)*34;left=470;scale=900/12584
        svg=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1450 {height}" role="img" aria-label="PhiReX annotated sequence intervals">',f'<rect width="1450" height="{height}" fill="white"/>','<style>text{font-family:Arial,sans-serif;fill:#202020} .muted{fill:#595959}</style>', '<text x="28" y="32" font-size="24">AISB26-045-001 | PhiReX | 12,584 bp</text>', '<text x="28" y="57" font-size="15">Coordinate-derived map. CDS: frame-consistent; region: coding boundaries unresolved. DNA unchanged.</text>']
        for i,f in enumerate(visible):
            y=85+i*34;label=html.escape(f['label']);x=left+(f['start_1based']-1)*scale;w=f['length']*scale
            cds=f['type']=='CDS';style='fill="#596877" stroke="#3b4752"' if cds else 'fill="#edf0f2" stroke="#7a8288"'
            if f['label'] in manifest['unresolved_CDS_intervals']:style+=' stroke-dasharray="5 3"'
            svg.extend([f'<text x="28" y="{y+15}" font-size="17">{label}</text>',f'<text x="236" y="{y+15}" font-size="14" class="muted">{f["start_1based"]}–{f["end_1based"]} | {f["type"]}</text>',f'<line x1="{left}" x2="1370" y1="{y+10}" y2="{y+10}" stroke="#e0e3e5"/>',f'<rect x="{x:.3f}" y="{y}" width="{w:.3f}" height="20" {style}/>'])
        y=91+len(visible)*34
        for n in [0,2000,4000,6000,8000,10000,12584]:
            x=left+n*scale;svg.append(f'<text x="{x:.3f}" y="{y}" text-anchor="middle" font-size="13">{n}</text>')
        svg.append('</svg>');(ROOT/'parts/AISB26-045-001/map.svg').write_text('\n'.join(svg)+'\n')
    report={'status':'PASSED' if all(checks.values()) else 'FAILED','checks':checks,'parts':parts,'unresolved_coding_regions':manifest['unresolved_CDS_intervals'],'interpretation':'Sequence/file consistency and feature integrity only; does not establish identities of assay samples or validate protein expression.'}
    (a.outdir/'feature_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'checks':checks,'unresolved':report['unresolved_coding_regions']},indent=2))
    return 0 if all(checks.values()) else 1
if __name__=='__main__':raise SystemExit(main())
