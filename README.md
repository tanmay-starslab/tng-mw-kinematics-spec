# TNG-MW: Kinematic and Spectral Analysis Toolkit

A minimal workflow for analyzing Milky-Way–type galaxies in the IllustrisTNG simulation.  
Includes utilities for catalog inspection, filtering star-forming systems, and preparing data for synthetic spectra generation using `yt` and `trident`.

## Quick Start
```bash
git clone https://github.com/<username>/tng-mw-kinematics-spec.git
cd tng-mw-kinematics-spec
uv venv --python 3.12
source .venv/bin/activate
uv pip install -e .
```

### Run
```bash
python scripts/quick_look.py
python scripts/export_starforming_csv.py

```

## Dependencies
numpy, pandas, h5py, matplotlib, yt, trident, illustris_python, scida

## Data Source
IllustrisTNG Milky Way / Andromeda dataset: https://www.tng-project.org/data/milkyway+andromeda/

## License
MIT License © 2025 Tanmay Singh
