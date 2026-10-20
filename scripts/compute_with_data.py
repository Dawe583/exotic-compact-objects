#!/usr/bin/env python3
"""Compute physics with the downloaded (and project-synthetic) data.

Three real-data blocks plus one synthetic-characterisation block:

1. GWTC catalogue reconciliation (391 events, refreshed by
   scripts/update_gwosc_gwtc5.py):
     - chirp mass recomputed from m1,m2 vs catalogue chirp_mass_source
     - redshift from luminosity distance (Planck18 interpolation) vs catalogue z
     - lower-mass-gap candidates (2.5 < m2 < 5 Msun)
     - ISCO radius + Hawking temperature of every remnant with a final mass
2. Strain quicklook analysis for GW170817 / GW190814 / GW190521
   (H1+L1+V1 4 kHz HDF5 downloaded by scripts/download_strain_marquee.py):
     - whitened bandpassed time series around each event
     - time-frequency map; peak-time vs catalogue GPS
3. Project-synthetic BBH waveforms (data/raw/sxs_waveforms/*.npz:
   NOT numerical relativity - surrogate-style project data):
     - config vs label consistency
     - peak strain amplitude, peak frequency f_peak (fft of h22)
     - post-merger ringdown frequency proxy (Hilbert phase) and ratio f_peak/f_ring

Outputs: results/compute_with_data.json, reports/compute_data_report.md,
results/sxs_characterization.csv and figures/gwtc_mass_plane.png,
figures/strain_<event>.png, figures/sxs_trends.png.

Run: .venv/bin/python research/projects/exotic-compact-objects/scripts/compute_with_data.py
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from astropy import constants as const  # noqa: E402
from astropy import units as u  # noqa: E402
from astropy.cosmology import Planck18  # noqa: E402
from scipy import signal, stats  # noqa: E402

from models import formulas as F  # noqa: E402

RESULTS = ROOT / "results"
REPORTS = ROOT / "reports"
FIGURES = ROOT / "figures"
EXTERNAL = ROOT / "data" / "external"
STRAIN_DIR = ROOT / "data" / "raw" / "strain"
SXS_DIR = ROOT / "data" / "raw" / "sxs_waveforms"

OUT_JSON = {"fetched_utc": datetime.now(timezone.utc).isoformat()}


# --------------------------------------------------------------------------- 1
def gwtc_analysis() -> dict:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    csv = EXTERNAL / "gwosc_gwtc_all.csv"
    df = pd.read_csv(csv)
    n_total = len(df)

    # ---- chirp-mass reconciliation -----------------------------------------
    sub = df.dropna(subset=["mass_1_source", "mass_2_source"]).copy()
    m1 = sub["mass_1_source"].to_numpy(float)
    m2 = sub["mass_2_source"].to_numpy(float)
    mc = (m1 * m2) ** (3 / 5) / (m1 + m2) ** (1 / 5)
    sub["chirp_mass_recomputed"] = mc
    sub["eta_recomputed"] = m1 * m2 / (m1 + m2) ** 2
    both = sub.dropna(subset=["chirp_mass_source"])
    rel_dev = (
        np.abs(both["chirp_mass_recomputed"] - both["chirp_mass_source"])
        / both["chirp_mass_source"]
    )
    chirp_stats = {
        "n_with_masses": len(sub),
        "n_catalog_chirp_too": len(both),
        "median_rel_dev": float(np.median(rel_dev)),
        "max_rel_dev": float(rel_dev.max()),
    }

    # ---- cosmology: z from DL via Planck18 ----------------------------------
    cosm = df.dropna(subset=["luminosity_distance", "redshift"]).copy()
    dl = cosm["luminosity_distance"].to_numpy(float)
    z_cat = cosm["redshift"].to_numpy(float)
    z_grid = np.linspace(1e-4, 2.0, 4000)
    dl_grid = Planck18.luminosity_distance(z_grid).to_value(u.Mpc)
    z_comp = np.interp(dl, dl_grid, z_grid)
    frac = np.abs(z_comp - z_cat) / np.clip(z_cat, 1e-9, None)
    cosm_stats = {
        "n_events": len(cosm),
        "median_rel_dev_z": float(np.median(frac)),
        "p90_rel_dev_z": float(np.quantile(frac, 0.9)),
        "max_z_catalog": float(z_cat.max()),
    }

    # ---- lower mass gap candidates -----------------------------------------
    gap = sub[(sub["mass_2_source"] > 2.5) & (sub["mass_2_source"] < 5.0)]
    gap_list = gap[["event_id", "mass_1_source", "mass_2_source", "chi_eff"]]
    gap_list.to_csv(RESULTS / "gwtc_mass_gap_candidates.csv", index=False)

    # ---- remnant ISCO + Hawking temperature ---------------------------------
    rem = df.dropna(subset=["final_mass_source"]).copy()
    isco_km = []
    hawking_k = []
    for m in rem["final_mass_source"]:
        isco_km.append(float(F.kerr_isco_radius(m * u.Msun, 0.0).to(u.km).value))
        hawking_k.append(
            float(
                (
                    const.hbar
                    * const.c**3
                    / (8 * np.pi * const.G * m * u.Msun * const.k_B)
                )
                .to(u.K)
                .value
            )
        )
    rem["isco_radius_km"] = isco_km
    rem["hawking_temperature_k"] = hawking_k
    rem_stats = {
        "n_with_final_mass": len(rem),
        "final_mass_range_msun": [
            float(rem["final_mass_source"].min()),
            float(rem["final_mass_source"].max()),
        ],
        "isco_range_km": [
            float(rem["isco_radius_km"].min()),
            float(rem["isco_radius_km"].max()),
        ],
        "hawking_T_min_max_k": [
            float(rem["hawking_temperature_k"].max()),
            float(rem["hawking_temperature_k"].min()),
        ],
    }
    rem[
        ["event_id", "final_mass_source", "isco_radius_km", "hawking_temperature_k"]
    ].to_csv(RESULTS / "gwtc_remnant_isco_hawking.csv", index=False)

    # ---- figure: source masses m1 vs m2 with the gap band -------------------
    fig, ax = plt.subplots(figsize=(7, 6))
    by_cat = df.groupby("catalog.shortName")
    for cat, g in by_cat:
        gg = g.dropna(subset=["mass_1_source", "mass_2_source"])
        ax.scatter(
            gg["mass_2_source"],
            gg["mass_1_source"],
            s=9,
            alpha=0.55,
            label=f"{cat} ({len(gg)})",
        )
    ax.axhspan(2.5, 5.0, color="crimson", alpha=0.10, lw=0)
    ax.text(
        0.04,
        3.6,
        "lower mass gap band (2.5-5 Msun, m2)",
        fontsize=8,
        color="crimson",
        transform=ax.get_yaxis_transform(),
    )
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"$m_2$ source frame [Msun]")
    ax.set_ylabel(r"$m_1$ source frame [Msun]")
    ax.set_title(
        f"GWTC mass plane: {n_total} catalogue events ({len(sub)} with both masses)"
    )
    ax.legend(fontsize=7, loc="lower right")
    ax.grid(alpha=0.25, which="both")
    fig.tight_layout()
    FIGURES.mkdir(exist_ok=True)
    fig.savefig(FIGURES / "gwtc_mass_plane.png", dpi=150)
    plt.close(fig)

    return {
        "n_total": n_total,
        "chirp_mass_reconciliation": chirp_stats,
        "cosmology_check": cosm_stats,
        "mass_gap_candidates": {
            "n": len(gap),
            "events": gap_list.head(20).to_dict("records"),
        },
        "remnant_radiation_physics": rem_stats,
    }


# --------------------------------------------------------------------------- 2
def strain_quicklook(event: str) -> dict:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import h5py

    manifest = json.loads((STRAIN_DIR / "manifest.json").read_text())
    meta = manifest["events"][event]
    gps = float(meta["gps"])
    out = {"event": event, "gps": gps, "detectors": {}}

    fig, axes = plt.subplots(3, 1, figsize=(9, 10), sharex=False)
    found_any = False

    for det_prefix, det_name in (("H-H1", "H1"), ("L-L1", "L1"), ("V-V1", "V1")):
        seg = [f for f in meta["files"] if f.startswith(det_prefix) and "32.hdf5" in f]
        if not seg:
            out["detectors"][det_name] = {"status": "no 32 s segment"}
            continue
        path = STRAIN_DIR / event / seg[0]
        with h5py.File(path, "r") as h5:
            ts = h5["strain/Strain"][:]
            attrs = dict(h5["strain/Strain"].attrs)
        x0, dx = float(attrs["Xstart"]), float(attrs["Xspacing"])
        fs = 1.0 / dx
        t_gps = x0 + np.arange(len(ts)) * dx

        # whitening PSD from the whole segment
        f_psd, pxx = signal.welch(ts, fs=fs, nperseg=4096)
        asd = np.sqrt(np.interp(np.fft.rfftfreq(len(ts), d=dx), f_psd, pxx))
        spec = np.fft.rfft(ts) / asd
        white = np.fft.irfft(spec, n=len(ts))
        sos = signal.butter(4, [20, 500], btype="band", fs=fs, output="sos")
        white_bp = signal.sosfiltfilt(sos, white)

        # band-power trace over the FULL segment; search the excess within the
        # +-4 s analysis window around the catalogue event time only (the raw
        # segment edges carry the whitening/filter transient artefact)
        f_s, t_s, Sxx = signal.spectrogram(white_bp, fs=fs, nperseg=512, noverlap=448)
        band = (f_s > 30) & (f_s < 450)
        bp_full = Sxx[band].sum(axis=0)
        t_gwcache = x0 + t_s  # absolute GPS of each spectrogram frame
        in_win = (t_gwcache > gps - 4) & (t_gwcache < gps + 4)
        if in_win.sum() == 0:
            out["detectors"][det_name] = {"status": "event not inside segment"}
            continue
        i_peak = int(np.argmax(np.where(in_win, bp_full, -np.inf)))
        metric = float(bp_full[i_peak] / np.median(bp_full))
        t_peak_offset = float(t_gwcache[i_peak] - gps)

        # window around the event (for the figure)
        w = (t_gps > gps - 4) & (t_gps < gps + 4)
        wt = t_gps[w] - gps
        wy = white_bp[w]

        out["detectors"][det_name] = {
            "status": "ok",
            "file": seg[0],
            "tf_peak_time_offset_s": t_peak_offset,
            "tf_power_max_over_median": metric,
        }
        found_any = found_any or metric > 5

        ax0 = (
            axes[0] if det_name == "H1" else (axes[1] if det_name == "L1" else axes[2])
        )
        ax0.plot(wt, wy / max(1e-23, np.std(wy)), lw=0.6)
        ax0.set_ylabel(f"{det_name} whitened (sigma)")
        ax0.grid(alpha=0.3)
        # windowed spectrogram for the figure only
        _fs, _ts, _Sxx = signal.spectrogram(wy, fs=fs, nperseg=512, noverlap=448)
        ax2 = ax0.twinx()
        ax2.pcolormesh(
            _ts - 4.0,
            _fs,
            _Sxx / np.median(_Sxx),
            shading="auto",
            cmap="viridis",
            alpha=0.55,
        )
        ax2.set_yscale("log")
        ax2.set_ylim(20, 800)
        ax2.set_ylabel("f [Hz]")

    axes[-1].set_xlabel("time from catalogue GPS [s]")
    fig.suptitle(f"{event}: whitened strain + time-frequency map (GWOSC 4 kHz, R1)")
    fig.tight_layout()
    fig.savefig(FIGURES / f"strain_{event}.png", dpi=150)
    plt.close(fig)

    out["chirp_like_signal_seen"] = bool(found_any)
    return out


# --------------------------------------------------------------------------- 3
def sxs_characterisation() -> dict:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from scipy.signal import hilbert

    rows = []
    files = sorted(SXS_DIR.glob("*.npz"))
    label_ok = 0
    for p in files:
        cfg = np.load(p, allow_pickle=True)["config"].item()
        arr = np.load(p)
        t, h22r, h22i = arr["t"], arr["h22_real"], arr["h22_imag"]
        label = cfg.get("label", "")
        if f"q{label.split('q')[-1]}" in p.name or p.name.endswith(f"{label}.npz"):
            label_ok += 1
        dt = float(t[1] - t[0])
        h22 = h22r + 1j * h22i

        # peak GW frequency (a) from a Hann-windowed FFT of h22 and
        # (b) instantaneous at the amplitude peak (robust to inspiral dwell)
        amp_peak = float(np.abs(h22).max())

        win = np.hanning(len(t))
        H = np.abs(np.fft.fft((h22 - h22.mean()) * win))
        freq = np.fft.fftfreq(len(t), d=dt)  # cycles per M (G=c=M=1)
        pos = freq > 0
        f_peak = float(freq[pos][np.argmax(H[pos])])

        i_peak = int(np.argmax(np.abs(h22)))
        t_peak = float(t[i_peak])
        if 1 <= i_peak < len(t) - 100:
            dphi = np.unwrap(np.angle(h22[i_peak + 1 : i_peak + 101]))
            f_peak_inst = float(np.median(np.diff(dphi) / (2 * np.pi) / dt))
        else:
            f_peak_inst = np.nan

        # post-merger ringdown frequency proxy (h22 is analytic: phase derivative)
        tail = t > t_peak + 1.0
        if tail.sum() > 100:
            phi = np.unwrap(np.angle(h22[tail]))
            f_ring = float(np.median(np.diff(phi) / (2 * np.pi) / dt))
        else:
            f_ring = np.nan

        rows.append(
            {
                "file": p.name,
                "q": float(cfg.get("q", np.nan)),
                "chi1z": float(cfg.get("chi1z", np.nan)),
                "chi2z": float(cfg.get("chi2z", np.nan)),
                "amp_peak": amp_peak,
                "f_peak_M_fft": f_peak,
                "f_peak_M_inst": f_peak_inst,
                "f_ring_M": f_ring,
            }
        )

    df = pd.DataFrame(rows)
    # effective spin proxy for the observed peak-frequency trend
    df["chi_eff"] = (df["q"] * df["chi1z"] + df["chi2z"]) / (1.0 + df["q"])
    df.to_csv(RESULTS / "sxs_characterization.csv", index=False)

    nn = df.dropna(subset=["q", "f_peak_M_inst", "chi_eff"])
    rho_q_fpeak = stats.spearmanr(nn["q"], nn["f_peak_M_inst"]).statistic
    rho_chieff_fpeak = stats.spearmanr(nn["chi_eff"], nn["f_peak_M_inst"]).statistic
    rho_q_amp = stats.spearmanr(nn["q"], nn["amp_peak"]).statistic
    nonspin = int(((df["chi1z"] == 0) & (df["chi2z"] == 0)).sum())
    nn2 = df.dropna(subset=["f_ring_M"])
    ratio = (
        (nn2["f_peak_M_inst"] / nn2["f_ring_M"])
        .replace([np.inf, -np.inf], np.nan)
        .dropna()
    )

    summary = {
        "n_waveforms": len(df),
        "config_label_consistent": label_ok,
        "q_range": [float(nn["q"].min()), float(nn["q"].max())],
        "spearman_q_vs_f_peak_inst": float(rho_q_fpeak),
        "spearman_chieff_vs_f_peak_inst": float(rho_chieff_fpeak),
        "spearman_q_vs_amp_peak": float(rho_q_amp),
        "n_nonspinning_waveforms": nonspin,
        "median_f_peak_M_inst": float(np.median(nn["f_peak_M_inst"])),
        "median_f_peak_M_fft": float(np.median(df["f_peak_M_fft"].dropna())),
        "median_f_peak_over_f_ring": float(np.median(ratio)),
        "note": (
            "These are project-synthetic surrogate-style waveforms (config q/chi), "
            "not numerical-relativity catalogues; trends characterise the dataset."
        ),
    }

    # figure: f_peak and amplitude vs q
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))
    sc = ax[0].scatter(
        nn["q"], nn["f_peak_M_inst"], c=nn["chi_eff"], cmap="coolwarm", s=14, alpha=0.7
    )
    fig.colorbar(sc, ax=ax[0], label="chi_eff proxy")
    ax[0].set_xlabel("mass ratio q")
    ax[0].set_ylabel(r"$f_{\rm peak,inst}\,M$")
    ax[0].set_title("Peak frequency (at amplitude max) vs mass ratio")
    ax[0].set_xscale("log")
    ax[1].scatter(
        nn["q"], nn["amp_peak"], c=nn["chi1z"], cmap="coolwarm", s=14, alpha=0.7
    )
    ax[1].set_xlabel("mass ratio q")
    ax[1].set_ylabel(r"$|h_{22}|_{\rm peak}\, (M/r)$")
    ax[1].set_xscale("log")
    ax[1].set_title(f"Peak amplitude vs mass ratio (Spearman {rho_q_amp:.2f})")
    fig.tight_layout()
    fig.savefig(FIGURES / "sxs_trends.png", dpi=150)
    plt.close(fig)

    return summary


# --------------------------------------------------------------------------- main
def main() -> None:
    RESULTS.mkdir(exist_ok=True)
    REPORTS.mkdir(exist_ok=True)
    FIGURES.mkdir(exist_ok=True)

    print("== 1/3 GWTC catalogue physics ...")
    OUT_JSON["gwtc"] = gwtc_analysis()

    print("== 2/3 strain quicklooks ...")
    OUT_JSON["strain"] = {
        ev: strain_quicklook(ev) for ev in ("GW170817", "GW190814", "GW190521")
    }

    print("== 3/3 synthetic waveform characterisation ...")
    OUT_JSON["sxs_synthetic"] = sxs_characterisation()

    (RESULTS / "compute_with_data.json").write_text(json.dumps(OUT_JSON, indent=2))

    # ---- markdown report -----------------------------------------------------
    g = OUT_JSON["gwtc"]
    s = OUT_JSON["strain"]
    x = OUT_JSON["sxs_synthetic"]
    lines = [
        "# Compute with downloaded data",
        "",
        f"Generated (UTC): {OUT_JSON['fetched_utc']}",
        "",
        "## 1. GWTC catalogue (391 events, refreshed from GWOSC today)",
        "",
        f"- Catalogue rows: **{g['n_total']}** (GWTC-1..GWTC-5, source scripts/update_gwosc_gwtc5.py)",
        "- Chirp mass recomputed from (m1, m2): "
        f"median relative deviation **{g['chirp_mass_reconciliation']['median_rel_dev']:.2e}** "
        f"over {g['chirp_mass_reconciliation']['n_catalog_chirp_too']} events with catalogue values",
        "- Redshift from luminosity distance (Planck18 interpolation): "
        f"median rel. deviation **{g['cosmology_check']['median_rel_dev_z']:.2e}**, "
        f"p90 {g['cosmology_check']['p90_rel_dev_z']:.2e} over {g['cosmology_check']['n_events']} events",
        f"- Lower mass-gap candidates (2.5 < m2 < 5 Msun): **{g['mass_gap_candidates']['n']}** "
        "(results/gwtc_mass_gap_candidates.csv)",
        "- Remnant radiation physics: "
        f"{g['remnant_radiation_physics']['n_with_final_mass']} events with final mass; "
        f"ISCO radius range {g['remnant_radiation_physics']['isco_range_km'][0]:.0f}-"
        f"{g['remnant_radiation_physics']['isco_range_km'][1]:.1e} km; "
        f"Hawking temperature range "
        f"{g['remnant_radiation_physics']['hawking_T_min_max_k'][0]:.2e}-"
        f"{g['remnant_radiation_physics']['hawking_T_min_max_k'][1]:.2e} K "
        "(results/gwtc_remnant_isco_hawking.csv)",
        "",
        "Figures: figures/gwtc_mass_plane.png",
        "",
        "## 2. Strain quicklook (GWOSC 4 kHz R1 HDF5, downloaded today)",
        "",
    ]
    for ev, info in s.items():
        dets = ", ".join(
            f"{k}: peak@{v.get('tf_peak_time_offset_s', '+'):+.2f}s (P/M={v.get('tf_power_max_over_median', 0):.1f}x)"
            for k, v in info["detectors"].items()
            if v.get("status") == "ok"
        )
        lines += [
            f"- **{ev}** (GPS {info['gps']:.1f}): chirp-like band-power excess seen: {info['chirp_like_signal_seen']}",
            f"  detectors: {dets}",
        ]
    lines += [
        "",
        "Notes: excess = max band power (30-450 Hz) within +-4 s of the catalogue event time",
        "divided by the whole-segment median; high ratios can also be driven by instrument",
        "glitches (e.g. the known transients in the GW190521 H1/L1 segments and the well",
        "documented L1 glitch about 1 s before the GW170817 merger - the L1 peak at",
        "-1.01 s here is consistent with that glitch, not a merger detection).",
        "",
        "Figures: figures/strain_GW170817.png, figures/strain_GW190814.png, figures/strain_GW190521.png",
        "",
        "## 3. Project-synthetic BBH waveform set (245 npz)",
        "",
        f"- Waveforms characterised: **{x['n_waveforms']}**",
        f"- config/label consistency: {x['config_label_consistent']}/{x['n_waveforms']}",
        f"- q range: {x['q_range'][0]:g} - {x['q_range'][1]:g}",
        f"- Spearman rho(q, f_peak_inst) = **{x['spearman_q_vs_f_peak_inst']:.3f}**; "
        f"rho(chi_eff, f_peak_inst) = **{x['spearman_chieff_vs_f_peak_inst']:.3f}**; "
        f"rho(q, amp_peak) = **{x['spearman_q_vs_amp_peak']:.3f}** "
        f"(negative: equal-mass binaries radiate the strongest h22 peak - the expected sense)",
        f"- non-spinning configs in the set: only {x['n_nonspinning_waveforms']} -> too few "
        "for a separate q-trend; spin coverage dominates",
        f"- median f_peak (inst, at amplitude max) M = {x['median_f_peak_M_inst']:.3f}",
        f"- median f_peak (fft) M = {x['median_f_peak_M_fft']:.3f}",
        f"- median f_peak / f_ring = {x['median_f_peak_over_f_ring']:.3f}",
        f"- NR reference (not these files): f_peak M approx 0.057 for q=1 non-spinning "
        "numerical relativity; this synthetic set does NOT reproduce NR peak relations - "
        "it characterises the project-generated surrogate data only.",
        f"- {x['note']}",
        "",
        "Figures: figures/sxs_trends.png - Results: results/sxs_characterization.csv",
        "",
    ]
    (REPORTS / "compute_data_report.md").write_text("\n".join(lines))
    print("\n".join(lines))
    print("wrote results/compute_with_data.json, reports/compute_data_report.md")


if __name__ == "__main__":
    main()
