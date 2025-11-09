# TNG MW Kinematics + Na I D / Ca II H&K

Two-panel diagnostic: left—TNG gas kinematics; right—synthetic absorption for Na I D and Ca II H&K along selected impact parameters.

## Layout
- Data root: `/Users/wavefunction/ASU Dropbox/Tanmay Singh/TNG-MW/`
- Repo: `/Users/wavefunction/github_repos/tng-mw-kinematics-spec/`

## Steps
1. Create uv env; install deps.
2. Run `scripts/quicklook_catalog.py` to inspect columns/metadata.
3. Run `scripts/export_starforming_csv.py` for SFR/sSFR filters.
4. Run `scripts/select_subhalo_432106.py` to extract MW-like target.

## Next
- Download minimal TNG subhalo/cutout for the selected system.
- Build kinematic maps and synthetic spectra (yt+trident).