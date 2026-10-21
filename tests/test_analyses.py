"""Smoke tests for the research analysis scripts."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def test_remnant_energetics_output():
    p = ROOT / "results" / "remnant_energetics.csv"
    assert p.exists()
    df = pd.read_csv(p)
    assert len(df) >= 200
    for col in ("event_id", "a_fit", "eta_radiative", "e_rot_msun", "margin_to_bound" if False else "e_rot_msun"):
        assert col in df.columns
    assert (df.eta_radiative >= 0).all() and (df.eta_radiative <= 0.5).all()


def test_exotic_discrimination_output():
    p = ROOT / "results" / "exotic_discrimination.csv"
    assert p.exists()
    df = pd.read_csv(p)
    assert "margin_to_bound" in df.columns
    assert (df.margin_to_bound >= 0).all()


def test_agn_demographics_output():
    p = ROOT / "results" / "agn_demographics.csv"
    assert p.exists()
    df = pd.read_csv(p)
    assert "log10_mass" in df.columns
    assert len(df) >= 50


def test_figures_exist():
    for name in ("remnant_energetics", "exotic_discrimination", "agn_demographics", "sxs_waveform_analysis"):
        assert (ROOT / "premium" / "figures" / f"{name}.html").exists()


def test_site_pages_exist():
    for name in ("index.html", "data.html", "gallery.html", "models.html"):
        assert (ROOT / "premium" / name).exists()
        assert (ROOT / "docs" / "premium" / name).exists()
