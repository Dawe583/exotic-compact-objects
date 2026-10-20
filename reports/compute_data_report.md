# Compute with downloaded data

Generated (UTC): 2026-10-19T20:15:25.774159+00:00

## 1. GWTC catalogue (391 events, refreshed from GWOSC today)

- Catalogue rows: **391** (GWTC-1..GWTC-5, source scripts/update_gwosc_gwtc5.py)
- Chirp mass recomputed from (m1, m2): median relative deviation **9.04e-03** over 282 events with catalogue values
- Redshift from luminosity distance (Planck18 interpolation): median rel. deviation **6.99e-03**, p90 2.31e-02 over 282 events
- Lower mass-gap candidates (2.5 < m2 < 5 Msun): **2** (results/gwtc_mass_gap_candidates.csv)
- Remnant radiation physics: 279 events with final mass; ISCO radius range 25-2.0e+03 km; Hawking temperature range 2.20e-08-2.78e-10 K (results/gwtc_remnant_isco_hawking.csv)

Figures: figures/gwtc_mass_plane.png

## 2. Strain quicklook (GWOSC 4 kHz R1 HDF5, downloaded today)

- **GW170817** (GPS 1187008882.4): chirp-like band-power excess seen: True
  detectors: H1: peak@-0.18s (P/M=1.5x), L1: peak@-1.01s (P/M=859.6x), V1: peak@+0.05s (P/M=2.3x)
- **GW190814** (GPS 1249852257.0): chirp-like band-power excess seen: False
  detectors: H1: peak@-0.14s (P/M=2.0x), L1: peak@-0.03s (P/M=2.4x), V1: peak@-3.19s (P/M=1.4x)
- **GW190521** (GPS 1242442967.4): chirp-like band-power excess seen: False
  detectors: H1: peak@+0.04s (P/M=1.8x), L1: peak@+0.04s (P/M=2.6x), V1: peak@-2.60s (P/M=1.6x)

Notes: excess = max band power (30-450 Hz) within +-4 s of the catalogue event time
divided by the whole-segment median; high ratios can also be driven by instrument
glitches (e.g. the known transients in the GW190521 H1/L1 segments and the well
documented L1 glitch about 1 s before the GW170817 merger - the L1 peak at
-1.01 s here is consistent with that glitch, not a merger detection).

Figures: figures/strain_GW170817.png, figures/strain_GW190814.png, figures/strain_GW190521.png

## 3. Project-synthetic BBH waveform set (245 npz)

- Waveforms characterised: **245**
- config/label consistency: 245/245
- q range: 1 - 10
- Spearman rho(q, f_peak_inst) = **0.126**; rho(chi_eff, f_peak_inst) = **0.939**; rho(q, amp_peak) = **-0.827** (negative: equal-mass binaries radiate the strongest h22 peak - the expected sense)
- non-spinning configs in the set: only 4 -> too few for a separate q-trend; spin coverage dominates
- median f_peak (inst, at amplitude max) M = 0.105
- median f_peak (fft) M = 0.009
- median f_peak / f_ring = 12.031
- NR reference (not these files): f_peak M approx 0.057 for q=1 non-spinning numerical relativity; this synthetic set does NOT reproduce NR peak relations - it characterises the project-generated surrogate data only.
- These are project-synthetic surrogate-style waveforms (config q/chi), not numerical-relativity catalogues; trends characterise the dataset.

Figures: figures/sxs_trends.png - Results: results/sxs_characterization.csv
