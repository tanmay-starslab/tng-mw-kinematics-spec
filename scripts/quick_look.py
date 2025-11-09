#!/usr/bin/env python
from pathlib import Path
import pandas as pd
from tngmw.paths import CATALOG, PROCESSED
from tngmw.io_hdf5 import list_hdf5, load_hdf5_to_dataframe

def main():
    print(f"[info] catalog: {CATALOG}")
    layout = list_hdf5(CATALOG)
    print("[info] HDF5 groups -> datasets:")
    for g, ds in sorted(layout.items()):
        print(f"  {g}: {len(ds)} datasets")

    df = load_hdf5_to_dataframe(CATALOG)
    print(f"[info] table shape: {df.shape}")
    out = PROCESSED / "catalog_raw_sample.parquet"
    df.to_parquet(out, index=False)
    print(f"[ok] wrote {out}")

if __name__ == "__main__":
    main()