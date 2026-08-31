#!/usr/bin/env python3
"""
Generate a small `export_taglab.py` script inside each TagLab project folder.
Each generated script can be run inside its folder to export that project's
annotations to a CSV named `<project_json_basename>_export.csv`.
"""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1] / 'taglab_projects'

template = r'''#!/usr/bin/env python3
import json, csv, sys
from pathlib import Path

P = Path(__file__).resolve().parent
proj_files = [f for f in P.glob('*.json') if f.name != 'coral_dictionary.json' and 'backup' not in f.name.lower()]
if not proj_files:
    print('No project JSON found in', P)
    sys.exit(1)
proj_file = proj_files[0]
try:
    project = json.load(open(proj_file, 'r', encoding='utf-8'))
except Exception as e:
    print('Failed to load', proj_file, '->', e)
    sys.exit(1)

rows = []
for img in project.get('images', []):
    photo_name = img.get('name', proj_file.name)
    px_to_mm = float(img.get('map_px_to_mm_factor', 1.0) or 1.0)
    ann = img.get('annotations', {})
    regions = ann.get('regions', [])
    points = ann.get('points', [])
    for r in regions:
        if not isinstance(r, dict):
            continue
        area_px = r.get('area', 0)
        perim_px = r.get('perimeter', 0)
        area_cm2 = (float(area_px) * (px_to_mm ** 2)) / 100.0 if area_px else 0.0
        perim_cm = (float(perim_px) * px_to_mm) / 10.0 if perim_px else 0.0
        bbox = r.get('bbox', [])
        length_cm = width_cm = 0.0
        if isinstance(bbox, (list, tuple)) and len(bbox) == 4:
            w_px = bbox[2]; h_px = bbox[3]
            length_cm = (max(w_px, h_px) * px_to_mm) / 10.0
            width_cm = (min(w_px, h_px) * px_to_mm) / 10.0
        rows.append({
            'project_folder': P.name,
            'photo_filename': photo_name,
            'colony_id': r.get('id',''),
            'class': r.get('class name',''),
            'substrate': str(r.get('note','')).strip(),
            'area_cm2': round(area_cm2,3),
            'perimeter_cm': round(perim_cm,3),
            'length_cm': round(length_cm,3),
            'width_cm': round(width_cm,3)
        })
    for pt in points:
        if not isinstance(pt, dict):
            continue
        rows.append({
            'project_folder': P.name,
            'photo_filename': photo_name,
            'colony_id': pt.get('Id',''),
            'class': pt.get('Class',''),
            'substrate': str(pt.get('Note','')).strip(),
            'area_cm2': 0.0,
            'perimeter_cm': 0.0,
            'length_cm': 0.0,
            'width_cm': 0.0
        })

out = P / (proj_file.stem + '_export.csv')
if not rows:
    print('No annotations to export for', P.name)
    sys.exit(0)
with open(out, 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['project_folder','photo_filename','colony_id','class','substrate','area_cm2','perimeter_cm','length_cm','width_cm']
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader(); w.writerows(rows)
print('Wrote', len(rows), 'rows to', out)
'''

created = 0
for d in sorted([p for p in ROOT.iterdir() if p.is_dir()]):
    # skip backups and directories that look like exports
    if d.name.lower().startswith('backups'):
        continue
    # check for presence of a project json
    jsons = [f for f in d.glob('*.json') if f.name != 'coral_dictionary.json' and 'backup' not in f.name.lower()]
    if not jsons:
        continue
    target = d / 'export_taglab.py'
    target.write_text(template)
    created += 1

print(f'Created {created} exporter scripts inside project folders')
