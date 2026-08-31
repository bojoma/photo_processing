#!/usr/bin/env python3
"""Export TagLab project annotations.

Usage:
  python3 scripts/export_project.py --project PATH_OR_NAME
  python3 scripts/export_project.py --project nb_black_2-5-26
  python3 scripts/export_project.py --all

If --all is used, a master CSV will be written to `data/master_taglab_data.csv`.
When exporting a single project, this script now defaults to writing only the
per-project CSV in the project folder (named `<projectname>_taglab_data.csv`).
Use `--skip-master` and `--no-project-csv` to control outputs.
"""
import argparse
import json
import csv
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
PROJECTS_ROOT = REPO_ROOT / 'taglab_projects'
MASTER_CSV = REPO_ROOT / 'data' / 'master_taglab_data.csv'


def process_project_dir(dirpath, write_project_csv=True):
    dirp = Path(dirpath)
    # find a project JSON inside dir
    jsons = [p for p in dirp.glob('*.json') if p.name != 'coral_dictionary.json' and 'backup' not in p.name.lower()]
    if not jsons:
        return 0, []
    proj_file = jsons[0]
    try:
        project = json.load(open(proj_file, 'r', encoding='utf-8'))
    except Exception as e:
        print(f"Failed to load {proj_file}: {e}")
        return 0, []

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
                'project_folder': dirp.name,
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
                'project_folder': dirp.name,
                'photo_filename': photo_name,
                'colony_id': pt.get('Id',''),
                'class': pt.get('Class',''),
                'substrate': str(pt.get('Note','')).strip(),
                'area_cm2': 0.0,
                'perimeter_cm': 0.0,
                'length_cm': 0.0,
                'width_cm': 0.0
            })

    if write_project_csv and rows:
        # write per-project CSV named <project_json_basename>_export.csv (previous format)
        out = dirp / (proj_file.stem + '_export.csv')
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['project_folder','photo_filename','colony_id','class','substrate','area_cm2','perimeter_cm','length_cm','width_cm']
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader(); w.writerows(rows)
        print(f'Wrote {len(rows)} rows to {out}')

    return len(rows), rows


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--project', '-p', help='Project folder name or path')
    group.add_argument('--all', action='store_true', help='Process all project folders')
    parser.add_argument('--no-project-csv', dest='project_csv', action='store_false', help='Do not write per-project CSV (only master)')
    parser.add_argument('--skip-master', dest='skip_master', action='store_true', help='Do not write the master CSV (useful when exporting single projects)')
    args = parser.parse_args()

    # default behavior: when running a single project, do not write the master CSV
    if not args.all:
        args.skip_master = True

    master_rows = []
    if args.all:
        for d in sorted(PROJECTS_ROOT.iterdir()):
            if not d.is_dir():
                continue
            if d.name.lower().startswith('backups'):
                continue
            n, rows = process_project_dir(d, write_project_csv=args.project_csv)
            if rows:
                master_rows.extend(rows)
    else:
        proj = args.project
        p = Path(proj)
        if not p.exists():
            # allow folder name
            p = PROJECTS_ROOT / proj
        if not p.exists() or not p.is_dir():
            print('Project folder not found:', proj)
            sys.exit(2)
        n, rows = process_project_dir(p, write_project_csv=args.project_csv)
        if rows:
            master_rows.extend(rows)

    # write master CSV unless the user requested skipping it
    if master_rows and not args.skip_master:
        MASTER_CSV.parent.mkdir(parents=True, exist_ok=True)
        with open(MASTER_CSV, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['project_folder','photo_filename','colony_id','class','substrate','area_cm2','perimeter_cm','length_cm','width_cm']
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader(); w.writerows(master_rows)
        print(f'Wrote master CSV with {len(master_rows)} rows to {MASTER_CSV}')


if __name__ == '__main__':
    main()
