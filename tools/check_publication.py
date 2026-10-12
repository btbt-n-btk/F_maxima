"""Check static links, numerical geometry, CSV agreement and distribution hashes."""
import argparse
import csv
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from verify_packing import verify_packing


class Links(HTMLParser):
    def __init__(self):
        super().__init__();self.values=[]
    def handle_starttag(self,tag,attrs):
        self.values.extend(value for key,value in attrs if key in ('href','src') and value)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--refresh-manifest',action='store_true')
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[1];docs=root/'docs'
    errors=[];links=0
    for path in docs.rglob('*.html'):
        parsed=Links();parsed.feed(path.read_text(encoding='utf-8'))
        for value in parsed.values:
            url=urlsplit(value)
            if url.scheme or url.netloc or not url.path:continue
            target=(path.parent/unquote(url.path)).resolve()
            try: target.relative_to(docs.resolve())
            except ValueError: errors.append(f'Link outside site: {path.name}: {value}');continue
            if not target.is_file():errors.append(f'Missing link: {path.name}: {value}')
            links+=1
    records=json.loads((docs/'data/comparison.json').read_text(encoding='utf-8'))
    if [row['n'] for row in records]!=list(range(3,13)):errors.append('Expected N=3..12.')
    with (docs/'data/comparison.csv').open(encoding='utf-8',newline='') as handle:
        csv_rows=list(csv.DictReader(handle))
    if len(csv_rows)!=len(records):errors.append('CSV row count differs.')
    for row in records:
        n=row['n'];data=json.loads((docs/f'data/best_{n}.json').read_text(encoding='utf-8'))
        result=verify_packing(data,7.65e-7)
        if not result['valid_within_tolerance']:errors.append(f'Invalid geometry N={n}')
        if data['n_spheres']!=n or abs(data['height_cm']-row['height_cm'])>1e-10:errors.append(f'JSON height/count differs N={n}')
        match=[value for value in csv_rows if int(value['n'])==n]
        if len(match)!=1 or abs(float(match[0]['height_cm'])-row['height_cm'])>1e-10:errors.append(f'CSV height differs N={n}')
        if not row['numerically_converged'] or not all(row['criteria'].values()):errors.append(f'Convergence criteria fail N={n}')
        if row['optimality_proven'] or data.get('optimality_proven'):errors.append(f'Unexpected optimality claim N={n}')
    hashes={str(path.relative_to(root)).replace('\\','/'):hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(root.rglob('*')) if path.is_file() and path.name!='manifest.json' and not any(part in ('.git','__pycache__') for part in path.parts)}
    manifest=docs/'manifest.json'
    if args.refresh_manifest and not errors:
        manifest.write_text(json.dumps({'schema_version':1,'sha256':hashes},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    expected=json.loads(manifest.read_text(encoding='utf-8'))['sha256']
    if expected!=hashes:errors.append('Manifest differs; after deliberate edits, use --refresh-manifest.')
    for error in errors:print('FAIL:',error)
    if not errors:print(f'PASS: {len(records)} geometries, {links} local links, CSV/JSON and {len(hashes)} file hashes.')
    return 1 if errors else 0


if __name__=='__main__':raise SystemExit(main())
