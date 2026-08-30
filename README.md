# Photo Processing

## Overview

This repository contains utilities and data for processing TagLab photo exports and cleaning imagery-related survey data for the Hurricane Hole surveys project.

## Key contents

- `data/` : raw and derived CSV exports (including `master_taglab_data.csv`).
- `scripts/` : processing scripts (Python and R). Notable files:
  - `scripts/batch_export_taglab.py` — batch processes TagLab exports.
    - `scripts/export_project.py` — master exporter CLI; preferred way to export a single project or all projects. See usage below.
  - `scripts/cleaning_garmin.R` — R script for cleaning Garmin/track metadata.
- `taglab_projects/` : TagLab project JSONs, dictionaries, and per-project exports.
- `photo_processing.Rproj` : RStudio project file for R-based workflows.
- `index.html` and `Classifier_Instructions.md` : documentation and instructions for classification workflows.

## Getting started

1. Inspect the data directory:

```bash
ls -la data
```

2. Export TagLab annotations (recommended):

- Run the master exporter for a single project (by folder name or path):

```bash
# by project folder name (runs exporter and writes a per-project CSV next to the project JSON)
python3 scripts/export_project.py --project nb_black_2-5-26

# or by explicit path
python3 scripts/export_project.py --project taglab_projects/nb_black_2-5-26
```

- Export all projects and create/update the master CSV:

```bash
python3 scripts/export_project.py --all
```

Notes:
- Per-project wrapper scripts (`export_taglab.py`) were removed in favor of the single canonical script above. If you prefer lightweight wrappers, run `scripts/generate_project_exporters.py` to recreate them.

3. Use the R project for cleaning or analysis in RStudio by opening `photo_processing.Rproj`.

## Data notes

- `master_taglab_data.csv` is the consolidated TagLab export used for downstream analysis.
- Per-project TagLab JSONs and CSVs are stored under `taglab_projects/` grouped by project folder.

## Contributing

If you add scripts or change data processing steps, please:

- Keep data exports in `taglab_projects/` named consistently (project-specific folder).

## Contact

For questions about the processing pipeline, contact the repository owner.
