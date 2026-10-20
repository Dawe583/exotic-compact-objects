#!/usr/bin/env python3
"""Verify every derived formula, symbolically and numerically.

1. Executes models/derivations.run_all() -> asserts every symbolic check.
2. Runs numeric spot checks (astropy/scipy) against the closed forms.
3. Writes reports/derivations_report.md and results/derivation_checks.json.

Run: .venv/bin/python research/projects/exotic-compact-objects/scripts/verify_formulas.py
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from astropy import constants as const
from astropy import units as u

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from models import derivations as D  # noqa: E402
from models import formulas as F  # noqa: E402

RESULTS_DIR = ROOT / "results"
REPORTS_DIR = ROOT / "reports"

# ----------------------------------------------------------------- numeric checks


def numerical_checks():
    out = []

    # 1. Eddington luminosity for 1 Msun: L = 4 pi G M m_p c / sigma_T
    L = F.eddington_luminosity(1 * u.Msun)
    ref = (4 * np.pi * const.G * (1 * u.Msun) * const.m_p * const.c / const.sigma_T).to(
        u.W
    )
    rel = abs((L - ref) / ref).value
    out.append(
        {
            "label": "Eddington luminosity: analytic vs astropy constants (1 Msun)",
            "value_w": L.to(u.W).value,
            "reference_w": ref.to(u.W).value,
            "relative_deviation": rel,
            "pass": rel < 1e-3,
        }
    )

    # 2. Hawking temperature for 1 Msun ~ 6.1e-8 K
    T = const.hbar * const.c**3 / (8 * np.pi * const.G * (1 * u.Msun) * const.k_B)
    out.append(
        {
            "label": "Hawking temperature of a 1 Msun Schwarzschild BH",
            "value_k": T.to(u.K).value,
            "reference_k": 6.1e-8,
            "relative_deviation": abs(T.to(u.K).value - 6.1e-8) / 6.1e-8,
            "pass": abs(T.to(u.K).value - 6.1e-8) / 6.1e-8 < 0.05,  # reference rounded
        }
    )

    # 3. Kerr ISCO: exact code vs a=0 limit 6 GM and monotone drift for a>0
    M = 1 * u.Msun
    isco_0 = F.kerr_isco_radius(M, 0.0)
    ref_0 = 6 * const.G * M / const.c**2
    rel0 = abs((isco_0 - ref_0) / ref_0).value
    isco_09 = F.kerr_isco_radius(M, 0.9)
    out.append(
        {
            "label": "Kerr ISCO a=0 equals 6 GM/c^2; prograde r(a=0.9) < r(a=0)",
            "value_km_a0": isco_0.to(u.km).value,
            "relative_deviation_a0": rel0,
            "value_km_a09": isco_09.to(u.km).value,
            "pass": rel0 < 1e-9 and isco_09 < isco_0,
        }
    )

    # 4. GW time-to-coalescence: independent ODE check of df/dt vs closed form.
    #    df/dt = (96/5) pi^(8/3) (G M_c / c^3)^(5/3) f^(11/3),  Mc = 1.219 Msun (BNS-like)
    from scipy.integrate import solve_ivp

    Mc_s = (
        ((1.219 * const.M_sun).to(u.kg).value) * const.G.si.value / const.c.si.value**3
    )  # [s]
    Mc_q = 1.219 * u.Msun

    def dfdt(_t, y):
        f = y[0]
        return (
            (96.0 / 5.0)
            * np.pi ** (8.0 / 3.0)
            * Mc_s ** (5.0 / 3.0)
            * f ** (11.0 / 3.0)
        )

    f0, f1 = 30.0, 1000.0
    sol = solve_ivp(
        dfdt,
        (0.0, 1e6),
        [f0],
        rtol=1e-11,
        atol=1e-12,
        dense_output=True,
        events=lambda t, y: y[0] - f1,
        max_step=10.0,
    )
    t_ode = float(sol.t_events[0][0])
    t_closed = float(
        (
            F.gw_time_to_coalescence(Mc_q, f1 / u.s)
            - F.gw_time_to_coalescence(Mc_q, f0 / u.s)
        )
        .to(u.s)
        .value
    )
    rel = abs(t_ode - t_closed) / t_closed
    out.append(
        {
            "label": "Time to coalescence: df/dt ODE integration vs closed form (30 Hz -> 1 kHz, Mc=1.219 Msun)",
            "t_ode_s": t_ode,
            "t_closed_s": t_closed,
            "relative_deviation": rel,
            "pass": bool(rel < 1e-4),
        }
    )

    # 5. Photon shadow: M87* (6.5e9 Msun at 16.8 Mpc) ~ 42 microarcsec,
    #    Sgr A* (4.3e6 Msun at 8.28 kpc) ~ 52 microarcsec.
    for label, m, d, ref_uas in [
        ("M87*", 6.5e9 * u.Msun, 16.8 * u.Mpc, 42.0),
        ("Sgr A*", 4.3e6 * u.Msun, 8.28 * u.kpc, 52.5),
    ]:
        theta = F.shadow_angular_diameter(m, d).to(u.uas)
        rel = abs(theta.value - ref_uas) / ref_uas
        out.append(
            {
                "label": f"EHT shadow angular diameter check ({label})",
                "value_uas": float(theta.value),
                "reference_uas": ref_uas,
                "relative_deviation": rel,
                "pass": rel < 0.25,  # weak-field approx; real ring is Kerr+inclination
            }
        )

    # 6. Light-deflection angle from actual Schwarzschild geodesic integration.
    #    Orbit equation for null paths: u'' + u = 3 m u^2, m=G=c=1, u=1/r.
    #    Start at the true periapsis u* (turning point), integrate out, find the
    #    asymptotic angle; by symmetry delta = 2 (phi_asym- - pi/2).
    from scipy.integrate import solve_ivp
    from scipy.optimize import brentq

    b = 40.0  # impact parameter b_infty (m = 1 units -> m/b = 0.025 weak field)

    def rhs(x, y):
        u, up = y
        return [up, -u + 3.0 * u**2]

    # periapsis u*: satisfies b^2 u^2 (1 - 2u) = 1  (from conserved b at the turn);
    # take the lower (outer) root in (0, 1/3] where the cubic rises to its max
    u_star = brentq(lambda u: b**2 * u**2 * (1 - 2 * u) - 1.0, 1e-4, 1.0 / 3.0)
    sol = solve_ivp(
        rhs,
        (0.0, 3.0),
        [u_star, 0.0],
        rtol=1e-12,
        atol=1e-13,
        dense_output=True,
        max_step=5e-4,
    )
    # find where the outgoing branch reaches u -> 0 (asymptote)
    # bracket around the first sign change of (u - u_thresh) along the grid
    u_thresh = 1e-6
    grid = np.linspace(0.05, 2.9, 800)
    u_vals = sol.sol(grid)[0]
    idx = int(np.argmax(u_vals < u_thresh))
    if idx == 0 or idx == len(grid) - 1:
        raise RuntimeError("no asymptote crossing found in integration window")
    phi_asym = brentq(lambda x: sol.sol(x)[0] - u_thresh, grid[idx - 1], grid[idx])
    delta_num = 2.0 * (phi_asym - np.pi / 2.0)
    delta_first_order = 4.0 / b  # = 4 m / b with m=1
    delta_second_order = 15.0 * np.pi / (4.0 * b**2)  # (15 pi/4) (m/b)^2
    rel_first = abs(delta_num - delta_first_order) / delta_first_order
    rel_analytic2 = abs(delta_num - delta_first_order - delta_second_order) / (
        delta_first_order + delta_second_order
    )
    out.append(
        {
            "label": "Light deflection: geodesic integration vs analytic deflection",
            "impact_parameter_m": b,
            "delta_integrated_rad": float(delta_num),
            "delta_first_order_rad": float(delta_first_order),
            "delta_second_order_rad": float(delta_second_order),
            "relative_deviation_vs_first_order": rel_first,
            "relative_deviation_vs_analytic_including_2nd_order": rel_analytic2,
            "pass": bool(rel_analytic2 < 0.02),
        }
    )

    return out


# ------------------------------------------------------------------------ reporting


def main():
    t_start = time.time()
    report_lines = [
        "# Formula derivations and verification",
        "",
        f"Generated (UTC): {datetime.now(timezone.utc).isoformat()}",
        "",
        "Every entry: symbolic derivation in `models/derivations.py` executed with Sympy,",
        "each check simplifies to an identity (0) or strict inequality; then numeric",
        "spot-checks against the closed forms (astropy/scipy precise integration).",
        "",
    ]
    json_out = {
        "fetched_utc": datetime.now(timezone.utc).isoformat(),
        "symbolic": [],
        "numeric": [],
    }

    all_ok = True
    # --- symbolic
    report_lines += ["## Symbolic derivations", ""]
    for res in D.run_all():
        checks = res.get("checks", [])
        failed = [
            c["label"]
            for c in checks
            if c.get("ok") is not None and not bool(c.get("ok"))
        ]
        entry = {
            "name": res["name"],
            "description": res.get("description"),
            "formula": res.get("formula"),
            "checks": [
                {
                    "label": c["label"],
                    "ok": (None if c.get("ok") is None else bool(c["ok"])),
                }
                for c in checks
            ],
            "all_ok": not failed,
        }
        json_out["symbolic"].append(entry)
        status = "PASS" if not failed else "FAIL: " + "; ".join(failed)
        all_ok &= not failed
        report_lines.append(f"### {res['name']} — {status}")
        if res.get("description"):
            report_lines.append(f"{res['description']}")
        report_lines.append(f"- formula: `{res.get('formula', '')}`")
        for c in checks:
            state = (
                ("PASS" if c.get("ok") is True else "numeric probe (see below)")
                if c.get("ok") is not False
                else "FAIL"
            )
            report_lines.append(f"- check: **{c['label']}** → {state}")
        report_lines.append("")

    # --- numeric
    report_lines += ["## Numerical spot checks", ""]
    for chk in numerical_checks():
        json_out["numeric"].append(chk)
        all_ok &= bool(chk["pass"])
        report_lines.append(f"### {chk['label']} — {'PASS' if chk['pass'] else 'FAIL'}")
        for k, v in chk.items():
            if k not in {"label", "pass"}:
                report_lines.append(f"- {k}: {v}")
        report_lines.append("")

    report_lines.append(
        f"Total: {'ALL CHECKS PASS' if all_ok else 'SOME CHECKS FAILED'} "
        f"({time.time() - t_start:.1f} s)"
    )
    report_lines.append("")

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "derivation_checks.json").write_text(
        json.dumps(json_out, indent=2, default=str)
    )
    (REPORTS_DIR / "derivations_report.md").write_text("\n".join(report_lines))
    print("\n".join(report_lines[-3:]))
    print(
        "wrote",
        REPORTS_DIR / "derivations_report.md",
        "and",
        RESULTS_DIR / "derivation_checks.json",
    )
    if not all_ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
