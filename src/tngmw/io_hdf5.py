from __future__ import annotations
from pathlib import Path
import h5py
import pandas as pd
from typing import Dict, Any, List

def list_hdf5(file: Path) -> Dict[str, List[str]]:
    out = {}
    with h5py.File(file, "r") as f:
        def visit(name, node):
            if isinstance(node, h5py.Dataset):
                grp = "/".join(name.split("/")[:-1]) or "/"
                out.setdefault(grp, []).append(name.split("/")[-1])
        f.visititems(visit)
    return out

def load_hdf5_to_dataframe(file: Path, prefer_groups: List[str] | None = None) -> pd.DataFrame:
    """
    Strategy:
      1) If prefer_groups provided, try concatenating datasets within those groups on matching lengths.
      2) Else, search for the largest-length aligned set of 1D datasets and assemble columns.
    """
    with h5py.File(file, "r") as f:
        # Discover candidates
        candidates: Dict[str, Any] = {}
        def collect(name, node):
            if isinstance(node, h5py.Dataset) and len(node.shape) == 1:
                candidates[name] = len(node)
        f.visititems(collect)

        if not candidates:
            raise RuntimeError("No 1D datasets found to form a table.")

        # choose the modal length
        from collections import Counter
        lengths = Counter(candidates.values())
        target_len, _ = lengths.most_common(1)[0]

        cols = {}
        for name, n in candidates.items():
            if n == target_len:
                key = name.replace("/", "__")
                cols[key] = f[name][...]

    df = pd.DataFrame(cols)
    return df