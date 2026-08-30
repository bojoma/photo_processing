# Photo Processing

## Overview

This repository contains utilities and data for processing TagLab photo exports and cleaning imagery-related survey data for the Hurricane Hole surveys project.

## Key contents

- `data/` : raw and derived CSV exports (including `master_taglab_data.csv`).
- `scripts/` : processing scripts (Python and R). Notable files:
  - `scripts/batch_export_taglab.py` — batch processes TagLab exports.
  - `scripts/cleaning_garmin.R` — R script for cleaning Garmin/track metadata.
- `taglab_projects/` : TagLab project JSONs, dictionaries, and per-project exports.
- `photo_processing.Rproj` : RStudio project file for R-based workflows.
- `index.html` and `Classifier_Instructions.md` : documentation and instructions for classification workflows.

## Getting started

1. Inspect the data directory:

```bash
ls -la data
```

2. Run the Python batch export script to regenerate project exports (requires Python 3):

```bash
python3 scripts/batch_export_taglab.py
```

3. Use the R project for cleaning or analysis in RStudio by opening `photo_processing.Rproj`.

## Data notes

- `master_taglab_data.csv` is the consolidated TagLab export used for downstream analysis.
- Per-project TagLab JSONs and CSVs are stored under `taglab_projects/` grouped by project folder.

## Contributing

If you add scripts or change data processing steps, please:

- Keep data exports in `taglab_projects/` named consistently (project-specific folder).

## Contact

For questions about the processing pipeline, contact the repository owner.
