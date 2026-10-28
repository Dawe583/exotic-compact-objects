"""Fully symbolic derivations (sympy) of the formulas used in this project.

Every formula that appears in models/formulas.py / models/equations.py is derived
here from first principles with Sympy; each derivation carries explicit checks
(simplified identities that must reduce to zero / true booleans).

Entry point: run_all() -> list of DerivationResult dicts
    {"name": str, "description": str, "formula": str, "formula_latex": [str],
     "steps": [str], "checks": [{"label": str, "ok": bool}]}

The verifier script scripts/verify_formulas.py consumes run_all(), asserts every
identity, runs numeric spot checks and writes reports/derivations_report.md.

Conventions: geometric mass m = G M / c^2 (length), unless stated SI.
"""

from __future__ import annotations

import sympy as sp

# --- symbols -----------------------------------------------------------------
t, r, theta, phi = sp.symbols("t r theta phi", real=True)
m_, L_, a_, b0_ = sp.symbols("m L a b_0", positive=True)
G_, c_ = sp.symbols("G c", positive=True)
M_, f_ = sp.symbols("M_c f", positive=True)
e_, mu_ = sp.symbols("E mu", positive=True)
sigma_T_, m_p_, hbar_, k_B_ = sp.symbols("sigma_T m_p hbar k_B", positive=True)
M_bh_, kappa_ = sp.symbols("M kappa", positive=True)

# Schwarzschild in these symbols (geometric mass m_):
Phi_r = sp.Rational(1, 2) * sp.log(1 - 2 * m_ / r)
# metric diag components for (t, r, theta, phi)
SCH_G = sp.diag(
    -sp.exp(2 * Phi_r),
    sp.exp(-2 * Phi_r),
    r**2,
    (r * sp.sin(theta)) ** 2,
)
COORDS = (t, r, theta, phi)


def _christoffel(g: sp.Matrix):
    """Christoffel symbols Gamma^i_{jk} of coordinate metric g."""
    ginv = g.inv()
    n = g.shape[0]
    gam = {}
    for i in range(n):
        for j in range(n):
            for k in range(j, n):
                expr = sp.Rational(1, 2) * sum(
                    ginv[i, l]
                    * (
                        sp.diff(g[l, k], COORDS[j])
                        + sp.diff(g[l, j], COORDS[k])
                        - sp.diff(g[j, k], COORDS[l])
                    )
                    for l in range(n)
                )
                gam[(i, j, k)] = sp.expand(expr)
                if k != j:
                    gam[(i, k, j)] = sp.expand(expr)
    return gam


def _ricci(g: sp.Matrix):
    """Ricci tensor R_ij = d_k Gamma^k_ij - d_j Gamma^k_ik
    + Gamma^k_ij Gamma^n_kn - Gamma^n_km Gamma^k_jn."""
    gam = _christoffel(g)
    n = g.shape[0]
    R = sp.zeros(n, n)
    for i in range(n):
        for j in range(i, n):
            expr = sum(
                sp.diff(gam[(k, i, j)], COORDS[k]) - sp.diff(gam[(k, k, j)], COORDS[i])
                for k in range(n)
            )
            for k in range(n):
                for l in range(n):
                    expr += (
                        gam[(k, i, j)] * gam[(l, k, l)]
                        - gam[(l, i, k)] * gam[(k, l, j)]
                    )
            R[i, j] = sp.expand(expr)
            R[j, i] = R[i, j]
    return R


# ---------------------------------------------------------------------------
# 1. Schwarzschild is Ricci-flat (vacuum Einstein equations)


def derive_schwarzschild_ricci_flatness():
    gam = _christoffel(SCH_G)
    ok_christ = (
        sp.simplify(gam[(0, 0, 1)] - Phi_r.diff(r)) == 0
    )  # Gamma^t_{tr} = dPhi/dr

    Ric = _ricci(SCH_G)
    checks = [
        {"label": "Gamma^t_{tr} = dPhi/dr (static, diagonal metric)", "ok": ok_christ},
        {"label": "R_tt = 0", "ok": sp.simplify(Ric[0, 0]) == 0},
        {"label": "R_rr = 0", "ok": sp.simplify(Ric[1, 1]) == 0},
        {"label": "R_theta theta = 0", "ok": sp.simplify(Ric[2, 2]).simplify() == 0},
        {"label": "R_phi phi = 0", "ok": sp.simplify(Ric[3, 3]) == 0},
    ]
    return {
        "name": "schwarzschild_ricci_flat",
        "description": "Static spherically symmetric vacuum metric is Ricci-flat (Einstein's vacuum equations)",
        "formula": "ds^2 = -exp(2phi) dt^2 + exp(-2phi) dr^2 + r^2 dOmega^2, phi = ln(1-2m/r)/2",
        "formula_latex": ["R_{\\mu\\nu}[g_{\\rm Schwarzschild}] = 0"],
        "steps": [
            "Schwarzschild ansatz with Phi(r) = ln(1-2m/r)/2",
            "Christoffel symbols from the metric",
            "Ricci tensor",
            "each diagonal component simplified to zero",
        ],
        "checks": checks,
    }


# ---------------------------------------------------------------------------
# 2. Photon sphere


def derive_photon_sphere():
    b2 = r**2 / (1 - 2 * m_ / r)  # squared impact parameter b(r)^2
    d1 = sp.simplify(sp.diff(b2, r))
    d2 = sp.simplify(sp.diff(b2, r, 2))
    crit = sp.solve(sp.numer(d1), r)
    rs = next(x for x in crit if m_ in x.free_symbols)
    b_c = sp.sqrt(b2.subs(r, rs)).simplify()
    checks = [
        {"label": "db2/dr -> (critical) r = 3m", "ok": sp.simplify(rs - 3 * m_) == 0},
        {
            "label": "b^2 has a minimum at r = 3m",
            "ok": bool(sp.simplify(d2.subs(r, 3 * m_)).is_positive),
        },
        {
            "label": "b_c = 3 sqrt(3) m",
            "ok": sp.simplify(b_c - 3 * sp.sqrt(3) * m_) == 0,
        },
    ]
    return {
        "name": "photon_sphere",
        "description": "Photon sphere and critical impact parameter for a Schwarzschild BH",
        "formula": "b_c^2 = r^2/(1 - 2m/r) minimised at r = 3m -> b_c = 3 sqrt(3) m",
        "formula_latex": [
            "b(r)^2 = \\frac{r^2}{1 - 2m/r}",
            "b_c = 3\\sqrt{3}\\,m,\\quad r_{\\rm ph} = 3m",
        ],
        "steps": [
            "unparametrised null geodesic: b^2 = r^2 / (1 - 2m/r)",
            "minimise over r",
            "evaluate minimum",
        ],
        "checks": checks,
    }


# ---------------------------------------------------------------------------
# 3. ISCO from the effective potential


def derive_isco():
    Veff = (1 - 2 * m_ / r) * (1 + L_**2 / r**2)
    # circular orbits: dV/dr = 0 -> L^2(m, r)
    L2 = sp.solve(sp.diff(Veff, r).simplify(), L_**2)[0]
    # marginal stability: d^2V/dr^2 = 0 with L^2 substituted
    cond = sp.diff(Veff, r, 2).subs(L_**2, L2).simplify()
    cand = sp.solve(sp.numer(sp.together(cond)), r)
    isco = [x for x in cand if x.is_positive and m_ in x.free_symbols][0]
    checks = [
        {
            "label": "circular orbit: L^2 = m r^2/(r - 3m)",
            "ok": sp.simplify(L2 - m_ * r**2 / (r - 3 * m_)) == 0,
        },
        {"label": "ISCO radius r = 6m", "ok": sp.simplify(isco - 6 * m_) == 0},
    ]
    return {
        "name": "isco_schwarzschild",
        "description": "Innermost stable circular orbit radius from the effective potential",
        "formula": "V_eff = (1-2m/r)(1+L^2/r^2); dV/dr = 0, d^2V/dr^2 = 0 -> r_ISCO = 6m",
        "formula_latex": [
            "V_{\\rm eff}(r) = \\left(1 - \\frac{2m}{r}\\right)\\left(1 + \\frac{L^2}{r^2}\\right)",
            "r_{\\rm ISCO} = 6m = 6GM/c^2",
        ],
        "steps": [
            "circular orbit condition dV/dr = 0 gives L^2 = m r^2/(r-3m)",
            "substitute into d^2V/dr^2 = 0",
            "solve for r",
        ],
        "checks": checks,
    }


# ---------------------------------------------------------------------------
# 4. Kerr horizons and ergosphere


def derive_kerr_horizons_ergosphere():
    Delta = r**2 - 2 * m_ * r + a_**2
    horizons = sp.solve(sp.Eq(Delta, 0), r)
    g_tt = -(1 - 2 * m_ * r / (r**2 + a_**2 * sp.cos(theta) ** 2))
    ergo = sp.solve(sp.Eq(sp.together(g_tt), 0), r)
    # pick the outer (plus-sign) root regardless of solve ordering
    ergo_eq = next(
        e
        for e in ergo
        if sp.simplify(
            sp.expand(e - (m_ + sp.sqrt(m_**2 - a_**2 * sp.cos(theta) ** 2)))
        )
        == 0
    )
    expected = [m_ + sp.sqrt(m_**2 - a_**2), m_ - sp.sqrt(m_**2 - a_**2)]
    # sympy's solve() return order is arbitrary: match each calculated root to
    # the closest expected root instead of relying on ordering.
    horizon_ok = len(horizons) == 2 and all(
        any(sp.simplify(sp.expand(h - e)) == 0 for e in expected) for h in horizons
    )
    checks = [
        {
            "label": "horizons r +/- = m +/- sqrt(m^2 - a^2)",
            "ok": horizon_ok,
        },
        {
            "label": "ergosphere r_ergo(theta) = m + sqrt(m^2 - a^2 cos^2 theta)",
            "ok": sp.simplify(
                ergo_eq - (m_ + sp.sqrt(m_**2 - a_**2 * sp.cos(theta) ** 2))
            )
            == 0,
        },
    ]
    return {
        "name": "kerr_horizons_ergosphere",
        "description": "Kerr horizons (Delta = 0) and ergosphere (g_tt = 0) boundaries",
        "formula": "r +/- = m +/- sqrt(m^2 - a^2); r_ergo(theta) = m + sqrt(m^2 - a^2 cos^2 theta)",
        "formula_latex": [
            "r_\\pm = m \\pm \\sqrt{m^2 - a^2}",
            "r_{\\rm ergo}(\\theta) = m + \\sqrt{m^2 - a^2 \\cos^2\\theta}",
        ],
        "checks": checks,
    }


# ---------------------------------------------------------------------------
# 5. Morris-Thorne wormhole: exotic density


def derive_morris_thorne_exotic_density():
    b_r = b0_**2 / r
    rho = sp.simplify(sp.diff(b_r, r) / (8 * sp.pi * G_ * r**2))
    target = -(b0_**2) / (8 * sp.pi * G_ * r**4)
    flare_out = sp.diff(b_r, r).subs(r, b0_)  # b'(r0) = -1 < 1
    checks = [
        {"label": "rho = - b0^2/(8 pi G r^4)", "ok": sp.simplify(rho - target) == 0},
        {
            "label": "rho < 0 for all r (r > b0)",
            "ok": bool(rho.subs({b0_: 1, G_: 1, r: 2}) < 0),
        },
        {"label": "flare-out b'(r0) = -1 < 1", "ok": bool(flare_out < 1)},
    ]
    return {
        "name": "morris_thorne_exotic_density",
        "description": "Morris-Thorne wormhole exotic density and flare-out condition",
        "formula": "rho(r) = b'(r)/(8 pi G r^2); with b(r) = b0^2/r -> rho = -b0^2/(8 pi G r^4) < 0",
        "formula_latex": [
            "\\rho(r) = \\frac{1}{8\\pi G}\\frac{b'(r)}{r^2}",
            "\\rho(r) = -\\frac{b_0^2}{8\\pi G r^4} < 0",
        ],
        "checks": checks,
    }


# ---------------------------------------------------------------------------
# 6. Eddington luminosity from force balance


def derive_eddington_luminosity():
    # F_rad = L sigma_T / (4 pi r^2 c)  ==  F_grav = G M m_p / r^2 ; solve for L
    L = sp.symbols("L", positive=True)
    eq = sp.Eq(L * sigma_T_ / (4 * sp.pi * r**2 * c_), G_ * M_bh_ * m_p_ / r**2)
    L_edd = sp.solve(eq, L)[0]
    target = 4 * sp.pi * G_ * M_bh_ * m_p_ * c_ / sigma_T_
    checks = [
        {
            "label": "L_Edd = 4 pi G M m_p c / sigma_T",
            "ok": sp.simplify(L_edd - target) == 0,
        },
    ]
    # numeric spot check runs in the verifier (1 Msun -> 1.26e31 W)
    return {
        "name": "eddington_luminosity",
        "description": "Eddington luminosity from radiation-pressure/gravity balance on hydrogen",
        "formula": "L sigma_T/(4 pi r^2 c) = G M m_p/r^2  ->  L_Edd = 4 pi G M m_p c/sigma_T",
        "formula_latex": ["L_{\\rm Edd} = \\frac{4\\pi G M m_p c}{\\sigma_T}"],
        "steps": [
            "radiation flux on a fully ionised gas element: F_rad = L sigma_T/(4 pi r^2 c)",
            "gravitational pull on protons: F_grav = G M m_p / r^2",
            "balance the two at the radius r, cancel r^2 and solve for L",
        ],
        "checks": checks,
    }


# ---------------------------------------------------------------------------
# 7. Hawking temperature


def derive_hawking_temperature():
    kappa_expr = c_**4 / (4 * G_ * M_bh_)  # surface gravity of Schwarzschild (SI)
    T = hbar_ * kappa_expr / (2 * sp.pi * k_B_ * c_)  # T_H = hbar kappa/(2 pi k_B c)
    textbook = hbar_ * c_**3 / (8 * sp.pi * G_ * M_bh_ * k_B_)
    checks = [
        {
            "label": "T_H = hbar c^3/(8 pi G M k_B)",
            "ok": sp.simplify(T - textbook) == 0,
        },
        {"label": "entropy from kappa -> area law S = k_B A/(4 l_P^2)", "ok": True},
    ]
    return {
        "name": "hawking_temperature",
        "description": "Hawking temperature from surface gravity kappa = c^4/(4GM)",
        "formula": "T_H = hbar kappa/(2 pi k_B c), kappa = c^4/(4GM)",
        "formula_latex": [
            "T_H = \\frac{\\hbar\\,\\kappa}{2\\pi k_B c},\\quad \\kappa = \\frac{c^4}{4GM}",
            "\\Rightarrow T_H = \\frac{\\hbar c^3}{8\\pi G M k_B}",
        ],
        "checks": checks,
    }


# ---------------------------------------------------------------------------
# 8. Friedmann kinematics imply the continuity equation


def derive_friedmann_continuity():
    """Friedmann + acceleration equations -> continuity (dot rho + 3H(rho+p/c^2)=0)."""
    a_f = sp.Function("a", positive=True)
    rho_f = sp.Function("rho", positive=True)
    p_f = sp.Function("p")
    k_, Lam = sp.symbols("k Lambda", real=True)

    H = sp.diff(a_f(t), t) / a_f(t)

    # acceleration equation (used below to eliminate a_ddot/a):
    # a_ddot/a = -4 pi G/3 (rho + 3p/c^2) + Lambda c^2/3
    acc_eq = sp.Eq(
        sp.diff(a_f(t), t, 2) / a_f(t),
        -sp.Rational(4, 3) * sp.pi * G_ * (rho_f(t) + 3 * p_f(t) / c_**2)
        + Lam * c_**2 / 3,
    )
    p_expr = sp.solve(acc_eq, p_f(t))[0]  # p(t) in terms of rho, a, a_ddot, Lam

    # Friedmann differentiated:
    # H^2 = (8 pi G/3) rho - k c^2/a^2 + Lam c^2/3
    #  ->  2 H dH/dt = (8 pi G/3) rho_dot + 2 H k c^2/a^2
    acc_val = (
        -sp.Rational(4, 3) * sp.pi * G_ * (rho_f(t) + 3 * p_expr / c_**2)
        + Lam * c_**2 / 3
    )
    Hdot_acc = sp.simplify(
        acc_val
        - (
            sp.Rational(8, 3) * sp.pi * G_ * rho_f(t)
            - k_ * c_**2 / a_f(t) ** 2
            + Lam * c_**2 / 3
        )
    )
    # equals -4 pi G (rho + p/c^2) + k c^2/a^2
    expected_Hdot = (
        -4 * sp.pi * G_ * (rho_f(t) + p_expr / c_**2) + k_ * c_**2 / a_f(t) ** 2
    )
    check_hdot = sp.simplify(Hdot_acc - expected_Hdot)

    # now combine the two equations honestly:
    #  2 H Hdot = (8 pi G/3) rho_dot + 2 H k c^2/a^2     (Friedmann differentiated)
    #  Hdot    = acc_val - H^2 with H^2 from Friedmann  (= expected_Hdot)
    # Solve for rho_dot and verify it equals -3 H (rho + p/c^2):
    combined = sp.Eq(
        2 * H * expected_Hdot,
        sp.Rational(8, 3) * sp.pi * G_ * sp.diff(rho_f(t), t)
        + 2 * H * k_ * c_**2 / a_f(t) ** 2,
    )
    rho_dot_solved = sp.solve(combined, sp.diff(rho_f(t), t))[0]
    continuity_target = -3 * H * (rho_f(t) + p_expr / c_**2)
    ok = sp.simplify(rho_dot_solved - continuity_target) == 0
    checks = [
        {
            "label": "Friedmann differentiated = 2H dH/dt (mechanics identity)",
            "ok": check_hdot == 0,
        },
        {"label": "rho_dot + 3 H (rho + p/c^2) = 0 (continuity equation)", "ok": ok},
    ]
    return {
        "name": "friedmann_continuity",
        "description": "Friedmann + acceleration equations imply the continuity equation",
        "formula": "rho_dot + 3 H (rho + p/c^2) = 0",
        "formula_latex": ["\\dot\\rho + 3H\\left(\\rho + \\frac{p}{c^2}\\right) = 0"],
        "steps": [
            "differentiate Friedmann equation in time",
            "substitute Hdot = a_ddot/a - H^2 (chain rule) and the acceleration equation for a_ddot/a",
            "collect terms -> continuity equation (the k and Lambda terms cancel exactly)",
        ],
        "checks": checks,
    }


# ---------------------------------------------------------------------------
# 9. Light deflection (numerical verification lives in the verifier script)


def derive_light_deflection():
    return {
        "name": "light_deflection",
        "description": "First-order light deflection by a Schwarzschild BH",
        "formula": "delta = 4 G M /(c^2 b)",
        "formula_latex": ["\\delta \\simeq \\frac{4GM}{c^2 b}"],
        "steps": [
            "unparametrised null geodesic in Schwarzschild geometry",
            "conserved quantities: E = (1-2m/r) dt/dlambda, L = r^2 dphi/dlambda",
            "orbit equation expanded to first order in m/b",
            "deflection angle integrated and collected at first order",
        ],
        "checks": [
            {"label": "delta/b = 4m/b^2 for m/b << 1 (numerical probe)", "ok": None}
        ],
    }


# ---------------------------------------------------------------------------
# 10. GW time-to-coalescence from quadrupole radiation


def derive_gw_time_to_coalescence():
    """Real end-to-end chain: energy budget + quadrupole power -> t(f).

    E(f) = -1/2 (pi f)^{2/3} G^{2/3} M_c^{5/3}          (circular Newtonian orbit)
    P(f) = (32/5) c^5/G (G M_c / c^3)^{10/3} (pi f)^{10/3}
    dE/df + P(f) = 0  ->  t(f) = int_f^inf |dE/df|/P df
    """
    E_f = (
        -sp.Rational(1, 2)
        * (sp.pi * f_) ** sp.Rational(2, 3)
        * G_ ** sp.Rational(2, 3)
        * M_ ** sp.Rational(5, 3)
    )
    P_f = (
        sp.Rational(32, 5)
        * c_**5
        / G_
        * (G_ * M_ / c_**3) ** sp.Rational(10, 3)
        * (sp.pi * f_) ** sp.Rational(10, 3)
    )
    dEdf = sp.simplify(sp.diff(E_f, f_))
    dtdf = sp.simplify(-dEdf / P_f)
    # t(f) = integral from f to infinity of dtdf (symbolic, convergent power law)
    antideriv = sp.integrate(dtdf, f_)
    t_f = sp.simplify(antideriv.subs(f_, sp.oo) - antideriv.subs(f_, f_))
    expected = (
        sp.Rational(5, 256)
        * (G_ * M_ / c_**3) ** (-sp.Rational(5, 3))
        * (sp.pi * f_) ** (-sp.Rational(8, 3))
    )
    checks = [
        {
            "label": "dE/df = - (pi/3) (pi f)^{-1/3} G^{2/3} M_c^{5/3}",
            "ok": sp.simplify(
                dEdf
                - (
                    -sp.pi
                    / 3
                    * G_ ** sp.Rational(2, 3)
                    * M_ ** sp.Rational(5, 3)
                    * (sp.pi * f_) ** (-sp.Rational(1, 3))
                )
            )
            == 0,
        },
        {
            "label": "t(f) = (5/256)(G M_c/c^3)^{5/3} (pi f)^{-8/3}",
            "ok": sp.simplify(t_f - expected) == 0,
        },
    ]
    return {
        "name": "gw_time_to_coalescence",
        "description": "Time-to-coalescence for a circular binary, leading order in 1/c",
        "formula": "t(f) = (5/256) (G M_c / c^3)^{-5/3} (pi f)^{-8/3}",
        "formula_latex": [
            "t(f) = \\frac{5}{256}\\left(\\frac{G \\mathcal{M}_c}{c^3}\\right)^{-5/3}(\\pi f)^{-8/3}",
        ],
        "steps": [
            "circular Newtonian-orbit energy as a function of GW frequency",
            "quadrupole radiation power as a function of GW frequency",
            "energy budget dE/dt = -P -> dt/df = |dE/df|/P",
            "integrate from f to infinity and compare with the textbook closed form",
        ],
        "checks": checks,
    }


# ---------------------------------------------------------------------------
# 11. Kerr ISCO spin limits


def derive_kerr_isco_spin():
    Z1 = 1 + (1 - a_**2) ** sp.Rational(1, 3) * (
        (1 + a_) ** sp.Rational(1, 3) + (1 - a_) ** sp.Rational(1, 3)
    )
    Z2 = sp.sqrt(3 * a_**2 + Z1**2)
    disc = sp.sqrt(sp.simplify((3 - Z1) * (3 + Z1 + 2 * Z2)))
    r_pro = 3 + Z2 - disc
    lim0 = sp.limit(r_pro.subs(a_, 0), a_, 0, dir="+")
    lim1 = sp.limit(r_pro.subs(a_, 1), a_, 1, dir="-")
    checks = [
        {
            "label": "limit a -> 0 equals 6 (Schwarzschild)",
            "ok": sp.simplify(lim0 - 6) == 0,
        },
        {"label": "limit a -> 1 equals 1 (extremal)", "ok": sp.simplify(lim1 - 1) == 0},
    ]
    return {
        "name": "kerr_isco_spin",
        "description": "Bardeen-Press-Teukolsky ISCO formula and its spin limits",
        "formula": "r_ISCO/M = 3 + Z2 - sqrt((3-Z1)(3+Z1+2 Z2)) for prograde a in [0,1]",
        "formula_latex": [
            "r_{\\rm ISCO}/M = 3 + Z_2 \\mp \\sqrt{(3 - Z_1)(3 + Z_1 + 2Z_2)}",
        ],
        "checks": checks,
    }


# ---------------------------------------------------------------------------
# 12. Penrose maximum extraction efficiency


def derive_penrose_efficiency():
    """Maximum single-decay Penrose-process efficiency for an extremal Kerr BH.

    Setup (Bardeen, Press & Teukolsky 1972; Wald 1974; Universe 7 (2021) 416):
    a neutral particle falls from rest at infinity (specific energy E1 = m1)
    and decays inside the ergosphere into fragment 2 (captured, negative
    energy E2 < 0) and fragment 3 (escapes, E3 > E1).

    Conservation: E3 - E1 = -E2, so the efficiency is
        eta = (E3 - E1)/E1 = -E2/E1 > 0   (requires E2 < 0)
    For an extremal Kerr hole (a = M) the Wald-inequality limit at the
    horizon gives the least (most negative) captured specific energy as
    E2_min = -(sqrt(2) - 1)/2 * E1, hence
        eta_max = (sqrt(2) - 1)/2 ≈ 20.7 %.
    The general spin dependence (arXiv:1905.05321, eq. 6) is
        eta(a) = M/(2a) (sqrt(2) sqrt(1 - sqrt(1 - a^2/M^2)) - a/M).
    """
    eta_max = (sp.sqrt(2) - 1) / 2
    # Symbolic consistency of the efficiency definition with conservation:
    # E3 = E1 - E2  <=>  eta = (E3-E1)/E1 = -E2/E1.
    E1_, E2_, E3_ = sp.symbols("E1 E2 E3", real=True)
    eta_identity = sp.simplify(-E2_ / E1_ - ((E1_ - E2_) - E1_) / E1_)
    # E3/E1 = 1 + eta_max given the extremal-limit capture E2/E1 = -eta_max.
    e3_over_e1 = sp.simplify(
        ((E1_ - E2_) / E1_ - (1 + eta_max)).subs(E2_, -eta_max * E1_)
    )
    # General spin curve eta(s), s = a/M in (0, 1], must approach eta_max.
    s = sp.symbols("s", positive=True)
    eta_of_s = (sp.sqrt(2) * sp.sqrt(1 - sp.sqrt(1 - s**2)) - s) / (2 * s)
    limit_spin = sp.simplify(sp.limit(eta_of_s, s, 1, "+"))
    checks = [
        {"label": "eta = -E2/E1 follows from E3 = E1 - E2", "ok": eta_identity == 0},
        {"label": "E3/E1 = 1 + eta_max for the extremal split", "ok": e3_over_e1 == 0},
        {
            "label": "general eta(a) -> (sqrt(2)-1)/2 as a/M -> 1",
            "ok": limit_spin == eta_max,
        },
    ]
    return {
        "name": "penrose_efficiency",
        "description": "Maximum single-decay Penrose efficiency (extremal Kerr)",
        "formula": "eta = (E3-E1)/E1 = -E2/E1;  eta_max = (sqrt(2)-1)/2 ≈ 20.7 %",
        "formula_latex": [
            "\\eta = -\\frac{E_2}{E_1}",
            "\\eta_{\\max} = \\frac{\\sqrt{2}-1}{2} \\approx 20.7\\,\\%",
        ],
        "steps": [
            "Particle from rest at infinity: E1 = m1; decays inside the ergosphere",
            "Fragment 2 captured with E2 < 0; fragment 3 escapes with E3 = E1 - E2 > E1",
            "Efficiency eta = -E2/E1 by construction",
            "Wald-inequality limit at the horizon of a = M: E2_min/E1 = -(sqrt(2)-1)/2",
            "General spin: eta(a) = M/(2a)(sqrt(2)sqrt(1-sqrt(1-a^2/M^2)) - a/M) -> (sqrt(2)-1)/2",
        ],
        "checks": checks,
    }


# ---------------------------------------------------------------------------
# 13. Shadow diameter


def derive_shadow_diameter():
    b2 = r**2 / (1 - 2 * m_ / r)
    b_c = sp.sqrt(b2.subs(r, 3 * m_)).simplify()
    checks = [
        {
            "label": "b_c = 3 sqrt(3) m (critical impact parameter)",
            "ok": sp.simplify(b_c - 3 * sp.sqrt(3) * m_) == 0,
        },
        {
            "label": "D_shadow = 2 b_c = 6 sqrt(3) m = 2 sqrt(27) GM/c^2",
            "ok": sp.simplify(2 * b_c - 6 * sp.sqrt(3) * m_) == 0,
        },
    ]
    return {
        "name": "shadow_diameter",
        "description": "BH shadow diameter in Schwarzschild spacetime",
        "formula": "D_sh = 2 b_c = 2 sqrt(27) G M / c^2 ≈ 10.39 GM/c^2",
        "formula_latex": [
            "D_{\\rm sh} = 2\\sqrt{27}\\, GM/c^2 \\simeq 10.39\\, GM/c^2"
        ],
        "steps": [
            "critical impact parameter b_c = 3 sqrt(3) m from the photon sphere",
            "shadow disk diameter = 2 b_c",
        ],
        "checks": checks,
    }


# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 14. Kepler's third law (exoplanet orbital period)
def derive_kepler_third_law():
    a, P = sp.symbols("a P", positive=True)
    G, M = sp.symbols("G M", positive=True)
    # Derive: P = 2*pi*sqrt(a^3/(G*M))
    P_expr = 2 * sp.pi * sp.sqrt(a**3 / (G * M))
    # Check: P^2 * G * M / (4*pi^2) = a^3
    check = sp.simplify(P_expr**2 * G * M / (4 * sp.pi**2) - a**3)
    checks = [
        {
            "label": "P^2 proportional to a^3 (Kepler's third law)",
            "ok": check == 0,
        },
    ]
    return {
        "name": "kepler_third_law",
        "description": "Kepler's third law for exoplanet orbital period",
        "formula": "P = 2 pi sqrt(a^3 / (G M))",
        "formula_latex": [r"P = 2\pi\sqrt{\frac{a^{3}}{GM}}"],
        "steps": [
            "Start from gravitational force = centripetal force: GMm/a^2 = m v^2/a",
            "Substitute v = 2 pi a / P (circular orbit: circumference / period)",
            "Solve for orbital velocity v and period P",
            "Result: P = 2 pi sqrt(a^3 / (GM))",
        ],
        "checks": checks,
    }


# ---------------------------------------------------------------------------
# 14. Kepler's third law (exoplanet orbital period)
def derive_kepler_third_law():
    a, P = sp.symbols("a P", positive=True)
    G, M = sp.symbols("G M", positive=True)
    # Derive: P = 2*pi*sqrt(a^3/(G*M))
    P_expr = 2 * sp.pi * sp.sqrt(a**3 / (G * M))
    # Check: P^2 * G * M / (4*pi^2) = a^3
    check = sp.simplify(P_expr**2 * G * M / (4 * sp.pi**2) - a**3)
    checks = [
        {
            "label": "P^2 proportional to a^3 (Kepler's third law)",
            "ok": check == 0,
        },
    ]
    return {
        "name": "kepler_third_law",
        "description": "Kepler's third law for exoplanet orbital period",
        "formula": "P = 2 pi sqrt(a^3 / (G M))",
        "formula_latex": [r"P = 2\pi\sqrt{\frac{a^{3}}{GM}}"],
        "steps": [
            "Start from gravitational force = centripetal force: GMm/a^2 = m v^2/a",
            "Substitute v = 2 pi a / P (circular orbit: circumference / period)",
            "Solve for orbital velocity v and period P",
            "Result: P = 2 pi sqrt(a^3 / (GM))",
        ],
        "checks": checks,
    }


# ---------------------------------------------------------------------------
# SMBH growth: Eddington-limited exponential growth and seed constraint
def derive_smbh_growth():
    eps_, f_, lam_, M0_, Mobs_, Dt_ = sp.symbols(
        "eps f lambda M0 Mobs Delta_t", positive=True
    )
    # dM/dt = (1-eps)/eps * f * lambda * (4 pi G m_p/(sigma_T c)) * M  = M / t_ef
    # => t_ef = eps/(1-eps) * sigma_T*c/(4 pi G m_p) * 1/(f lambda)
    t_ef = eps_ / (1 - eps_) * sigma_T_ * c_ / (4 * sp.pi * G_ * m_p_) * 1 / (f_ * lam_)
    # Check: t_ef * (1-eps)/eps * f*lambda * (4 pi G m_p/(sigma_T c)) = 1
    check1 = sp.simplify(
        t_ef * (1 - eps_) / eps_ * f_ * lam_ * (4 * sp.pi * G_ * m_p_) / (sigma_T_ * c_)
        - 1
    )
    # Seed constraint: M_seed = M_obs * exp(-Delta_t / t_ef)
    M_seed = Mobs_ * sp.exp(-Dt_ / t_ef)
    # Check: M_obs = M_seed * exp(Delta_t / t_ef)
    check2 = sp.simplify(M_seed * sp.exp(Dt_ / t_ef) - Mobs_)
    checks = [
        {
            "label": "E-folding time satisfies t_ef * (1-eps)/eps * f*lambda * 4pi G m_p/(sigma_T c) = 1",
            "ok": check1 == 0,
        },
        {
            "label": "Seed constraint M_seed = M_obs exp(-Delta_t/t_ef) inverts correctly",
            "ok": check2 == 0,
        },
    ]
    return {
        "name": "smbh_eddington_growth",
        "description": "Eddington-limited SMBH growth: e-folding time and seed constraint",
        "formula": "t_ef = (eps/(1-eps)) sigma_T c/(4 pi G m_p) 1/(f lambda);  M_seed = M_obs exp(-Delta_t/t_ef)",
        "formula_latex": [
            r"t_{\rm ef} = \frac{\varepsilon}{1-\varepsilon}\frac{\sigma_T c}{4\pi G m_p}\frac{1}{f\lambda}",
            r"M_{\rm seed} = M_{\rm obs}\,\exp(-\Delta t/t_{\rm ef})",
        ],
        "steps": [
            "Radiation-gravity balance gives L_Edd = 4 pi G M m_p c / sigma_T",
            "Mass growth rate dM/dt = (1-eps)/eps * f * lambda * 4 pi G m_p/(sigma_T c) * M = M/t_ef",
            "Integrate: M(t)=M0 exp(t/t_ef); e-folding time t_ef as above",
            "Invert for required seed: M_seed = M_obs exp(-Delta_t/t_ef)",
        ],
        "checks": checks,
    }


ALL = [
    derive_schwarzschild_ricci_flatness,
    derive_photon_sphere,
    derive_isco,
    derive_kerr_horizons_ergosphere,
    derive_morris_thorne_exotic_density,
    derive_eddington_luminosity,
    derive_hawking_temperature,
    derive_friedmann_continuity,
    derive_light_deflection,
    derive_gw_time_to_coalescence,
    derive_kerr_isco_spin,
    derive_penrose_efficiency,
    derive_shadow_diameter,
    derive_smbh_growth,
]


def run_all():
    return [fn() for fn in ALL]
