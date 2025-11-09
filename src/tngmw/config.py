
# src/tngmw/config.py
import os
from pathlib import Path

# --- Core paths ---
DATA_ROOT = Path("/Users/wavefunction/ASU Dropbox/Tanmay Singh/TNG-MW").resolve()
RAW        = DATA_ROOT / "raw"
PROCESSED  = DATA_ROOT / "processed"
NOTEBOOKS  = DATA_ROOT / "notebooks"
for p in (RAW, PROCESSED, NOTEBOOKS):
    p.mkdir(parents=True, exist_ok=True)

# --- API key loader ---
def load_tng_api_key() -> str:
    key = os.getenv("TNG_API_KEY")
    if key:
        return key
    env = Path(__file__).resolve().parents[2] / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if line.strip().startswith("TNG_API_KEY="):
                return line.split("=", 1)[1].strip()
    raise RuntimeError("TNG_API_KEY not set. Add it to your shell env or .env file (gitignored).")

TNG_API_KEY = load_tng_api_key()
HEADERS     = {"api-key": TNG_API_KEY}

# --- Simulation constants ---
SIMULATION  = "TNG50-1"
SNAPNUM     = 99
SUBID       = 432106


PLOTS = DATA_ROOT / "plots"

for d in [RAW, PROCESSED, PLOTS]:
    d.mkdir(parents=True, exist_ok=True)
# --- End of config.py ---