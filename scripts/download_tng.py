# --- config & helpers ---
import os, json, pathlib, requests

# Paths
DATA_ROOT = pathlib.Path("/Users/wavefunction/ASU Dropbox/Tanmay Singh/TNG-MW").resolve()
RAW      = (DATA_ROOT / "raw");      RAW.mkdir(parents=True, exist_ok=True)
PROCESSED= (DATA_ROOT / "processed"); PROCESSED.mkdir(parents=True, exist_ok=True)

# Load API key from environment or .env
def load_tng_api_key():
    key = os.getenv("TNG_API_KEY")
    if key: return key
    env = pathlib.Path.cwd().parent / ".env"  # adjust if notebook is inside notebooks/
    if env.exists():
        for line in env.read_text().splitlines():
            if line.strip().startswith("TNG_API_KEY="):
                return line.split("=",1)[1].strip()
    raise RuntimeError("TNG_API_KEY not set (env or .env).")

API_KEY = load_tng_api_key()

# Base URL for this subhalo
BASE = "https://www.tng-project.org/api/TNG50-1/snapshots/99/subhalos/432106/"

# Session with auth header
S = requests.Session()
S.headers.update({"api-key": API_KEY})

def get_json(url: str):
    r = S.get(url); r.raise_for_status()
    return r.json()

def download_binary(url: str, outpath: pathlib.Path, params: dict | None = None):
    with S.get(url, params=params, stream=True) as r:
        r.raise_for_status()
        with open(outpath, "wb") as f:
            for chunk in r.iter_content(chunk_size=1<<20):
                if chunk: f.write(chunk)
    return outpath


# ---------------- CLI ----------------
import argparse

def cmd_detail(args):
    detail = get_json(BASE)
    out = PROCESSED / f"subhalo_{args.id}_detail.json"
    out.write_text(json.dumps(detail, indent=2))
    print(f"[ok] wrote {out}")

def default_cutout_params(size="min"):
    if size == "min":
        return {
            "gas": ",".join([
                "Coordinates","Velocities","Masses","Density","InternalEnergy",
                "SFR","GFM_Metallicity","ElectronAbundance","NeutralHydrogenAbundance"
            ]),
            "stars": "Coordinates,Velocities,Masses,GFM_Metallicity",
            "bh": "Coordinates,Velocities,Masses",
            # omit DM to keep files smaller; add `"dm":"Coordinates,Velocities"` if needed
        }
    elif size == "kin":
        return {
                "gas": "Coordinates,Velocities,Masses,Density,InternalEnergy,SFR",
                "stars": "Coordinates,Velocities,Masses",
        }
    elif size == "full-small":
        return {
            "gas": "Coordinates,Velocities,Masses,Density,InternalEnergy,SFR,GFM_Metallicity,ElectronAbundance,NeutralHydrogenAbundance",
            "stars": "Coordinates,Velocities,Masses,GFM_StellarPhotometrics,GFM_Metallicity",
            "dm": "Coordinates,Velocities",
            "bh": "Coordinates,Velocities,Masses",
        }
    else:
        raise ValueError("size must be one of: min, kin, full-small")

def cmd_cutout(args):
    params = default_cutout_params(args.size)
    url = BASE + "cutout.hdf5"
    out = RAW / f"subhalo_{args.id}_cutout_{args.size}.hdf5"
    print(f"[info] downloading cutout → {out.name}")
    download_binary(url, out, params=params)
    print(f"[ok] wrote {out}")

def cmd_vis(args):
    detail = get_json(BASE)
    vis = detail.get("vis", {})
    wanted = {
        "halo_gas_dens": vis.get("halo_gas_dens"),
        "halo_gas_temp": vis.get("halo_gas_temp"),
        "halo_stellar_dens": vis.get("halo_stellar_dens"),
        "galaxy_gas_dens_faceon": vis.get("galaxy_gas_dens_faceon"),
        "galaxy_stellar_light_faceon": vis.get("galaxy_stellar_light_faceon"),
    }
    for name, url in wanted.items():
        if not url: 
            continue
        out = RAW / f"{name}_{args.id}.png"
        print(f"[info] {name} → {out.name}")
        download_binary(url, out)
    print("[ok] visualizations saved")

def cmd_tree_png(args):
    detail = get_json(BASE)
    url = detail["vis"]["mergertree_sublink"]
    out = RAW / f"mergertree_{args.id}.png"
    download_binary(url, out)
    print(f"[ok] wrote {out}")

def cmd_mwm31s(args):
    detail = get_json(BASE)
    urls = detail.get("supplementary_data", {}).get("MWM31s_cutouts", [])
    if not urls:
        print("[warn] no MWM31s_cutouts list")
        return
    for u in urls:
        name = u.rstrip("/").split("/")[-1]
        out = RAW / f"mwm31s_{args.id}_{name}"
        print(f"[info] {name}")
        download_binary(u, out)
    print("[ok] MWM31s cutouts saved")

def main():
    p = argparse.ArgumentParser(description="Download TNG subhalo detail, cutouts, and visuals")
    p.add_argument("--id", type=int, default=432106, help="Subhalo ID (default: 432106)")
    sub = p.add_subparsers(dest="cmd", required=True)

    s1 = sub.add_parser("detail", help="download subhalo JSON detail")
    s1.set_defaults(func=cmd_detail)

    s2 = sub.add_parser("cutout", help="download constrained cutout HDF5")
    s2.add_argument("--size", choices=["min","kin","full-small"], default="min")
    s2.set_defaults(func=cmd_cutout)

    s3 = sub.add_parser("vis", help="download PNG visualizations")
    s3.set_defaults(func=cmd_vis)

    s4 = sub.add_parser("tree-png", help="download merger tree PNG")
    s4.set_defaults(func=cmd_tree_png)

    s5 = sub.add_parser("mwm31s", help="download all MWM31s supplementary cutouts (multiple HDF5)")
    s5.set_defaults(func=cmd_mwm31s)

    args = p.parse_args()
    # rebase BASE if a different id is passed (URL path stays same except id)
    global BASE
    BASE = f"https://www.tng-project.org/api/TNG50-1/snapshots/99/subhalos/{args.id}/"
    args.func(args)

if __name__ == "__main__":
    main()