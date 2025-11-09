import numpy as np
import pandas as pd

# map common column aliases to canonical names
ALIASES = {
    "stellar_mass": ["Mstar", "StellarMass", "SubhaloMassInRadType__4", "SubhaloMassType__4"],
    "sfr": ["SFR", "SFR_total", "SFRinRad", "SubhaloSFR", "SFR__total"],
    "subhalo_id": ["SubhaloID", "ID", "id", "SUBFINDID", "subfind_id"],
    "group_id": ["GroupID", "FOFGroupID", "hostID", "HostID"],
}

def coalesce(df: pd.DataFrame, keys: list[str]) -> pd.Series | None:
    for k in keys:
        if k in df.columns:
            return df[k]
    return None

def add_ssfr(df: pd.DataFrame) -> pd.DataFrame:
    m = coalesce(df, ALIASES["stellar_mass"])
    sfr = coalesce(df, ALIASES["sfr"])
    out = df.copy()
    if m is not None and sfr is not None:
        # masses in 1e10 Msun or Msun? Handle scale heuristically.
        m_val = m.astype(float)
        sfr_val = sfr.astype(float)
        # If typical stellar masses are < 1e3, assume 1e10 Msun units and rescale
        scale = 1e10 if np.nanmedian(m_val) < 1e3 else 1.0
        m_msun = m_val * scale
        with np.errstate(divide="ignore", invalid="ignore"):
            out["sSFR"] = sfr_val / m_msun
            out["log10_sSFR"] = np.log10(out["sSFR"].replace(0, np.nan))
    return out

def starforming_mask(df: pd.DataFrame,
                     sfr_min: float = 0.01,
                     log10_ssfr_min: float = -11.5) -> pd.Series:
    out = pd.Series(False, index=df.index)
    sfr = coalesce(df, ALIASES["sfr"])
    if sfr is not None:
        out |= (sfr.astype(float) >= sfr_min)
    if "log10_sSFR" in df.columns:
        out |= (df["log10_sSFR"] >= log10_ssfr_min)
    return out