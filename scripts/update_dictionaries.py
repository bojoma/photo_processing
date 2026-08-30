#!/usr/bin/env python3
import json
from pathlib import Path
import shutil
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1] / 'taglab_projects'
CORAL = ROOT / 'coral_dictionary.json'
BACKUPS = ROOT / 'backups' / datetime.now().strftime('%Y%m%d_%H%M%S')
BACKUPS.mkdir(parents=True, exist_ok=True)

with CORAL.open('r', encoding='utf-8') as f:
    coral = json.load(f)

modified = []
for p in sorted(ROOT.rglob('*.json')):
    if p.name == 'coral_dictionary.json':
        continue
    try:
        data = json.loads(p.read_text(encoding='utf-8'))
    except Exception as e:
        print(f"SKIP (invalid json): {p} -> {e}")
        continue
    old = data.get('dictionary')
    if old != coral:
        # backup
        shutil.copy2(p, BACKUPS / p.name)
        data['dictionary'] = coral
        p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        modified.append(str(p.relative_to(ROOT)))

print(f"Modified {len(modified)} files")
for m in modified:
    print(m)
print(f"Backups saved to: {BACKUPS}")
