from pathlib import Path

DATA_ROOT = Path("/Users/wavefunction/ASU Dropbox/Tanmay Singh/TNG-MW").resolve()
CATALOG = DATA_ROOT / "catalog" / "mwm31s_hostcatalog.hdf5"
PROCESSED = DATA_ROOT / "processed"
FIGURES = DATA_ROOT / "figures"

PROCESSED.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)