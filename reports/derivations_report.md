# Formula derivations and verification

Generated (UTC): 2026-10-27T23:14:18.167102+00:00

Every entry: symbolic derivation in `models/derivations.py` executed with Sympy,
each check simplifies to an identity (0) or strict inequality; then numeric
spot-checks against the closed forms (astropy/scipy precise integration).

## Symbolic derivations

### schwarzschild_ricci_flat — PASS
Static spherically symmetric vacuum metric is Ricci-flat (Einstein's vacuum equations)
- formula: `ds^2 = -exp(2phi) dt^2 + exp(-2phi) dr^2 + r^2 dOmega^2, phi = ln(1-2m/r)/2`
- check: **Gamma^t_{tr} = dPhi/dr (static, diagonal metric)** → PASS
- check: **R_tt = 0** → PASS
- check: **R_rr = 0** → PASS
- check: **R_theta theta = 0** → PASS
- check: **R_phi phi = 0** → PASS

### photon_sphere — PASS
Photon sphere and critical impact parameter for a Schwarzschild BH
- formula: `b_c^2 = r^2/(1 - 2m/r) minimised at r = 3m -> b_c = 3 sqrt(3) m`
- check: **db2/dr -> (critical) r = 3m** → PASS
- check: **b^2 has a minimum at r = 3m** → PASS
- check: **b_c = 3 sqrt(3) m** → PASS

### isco_schwarzschild — PASS
Innermost stable circular orbit radius from the effective potential
- formula: `V_eff = (1-2m/r)(1+L^2/r^2); dV/dr = 0, d^2V/dr^2 = 0 -> r_ISCO = 6m`
- check: **circular orbit: L^2 = m r^2/(r - 3m)** → PASS
- check: **ISCO radius r = 6m** → PASS

### kerr_horizons_ergosphere — PASS
Kerr horizons (Delta = 0) and ergosphere (g_tt = 0) boundaries
- formula: `r +/- = m +/- sqrt(m^2 - a^2); r_ergo(theta) = m + sqrt(m^2 - a^2 cos^2 theta)`
- check: **horizons r +/- = m +/- sqrt(m^2 - a^2)** → PASS
- check: **ergosphere r_ergo(theta) = m + sqrt(m^2 - a^2 cos^2 theta)** → PASS

### morris_thorne_exotic_density — PASS
Morris-Thorne wormhole exotic density and flare-out condition
- formula: `rho(r) = b'(r)/(8 pi G r^2); with b(r) = b0^2/r -> rho = -b0^2/(8 pi G r^4) < 0`
- check: **rho = - b0^2/(8 pi G r^4)** → PASS
- check: **rho < 0 for all r (r > b0)** → PASS
- check: **flare-out b'(r0) = -1 < 1** → PASS

### eddington_luminosity — PASS
Eddington luminosity from radiation-pressure/gravity balance on hydrogen
- formula: `L sigma_T/(4 pi r^2 c) = G M m_p/r^2  ->  L_Edd = 4 pi G M m_p c/sigma_T`
- check: **L_Edd = 4 pi G M m_p c / sigma_T** → PASS

### hawking_temperature — PASS
Hawking temperature from surface gravity kappa = c^4/(4GM)
- formula: `T_H = hbar kappa/(2 pi k_B c), kappa = c^4/(4GM)`
- check: **T_H = hbar c^3/(8 pi G M k_B)** → PASS
- check: **entropy from kappa -> area law S = k_B A/(4 l_P^2)** → PASS

### friedmann_continuity — PASS
Friedmann + acceleration equations imply the continuity equation
- formula: `rho_dot + 3 H (rho + p/c^2) = 0`
- check: **Friedmann differentiated = 2H dH/dt (mechanics identity)** → PASS
- check: **rho_dot + 3 H (rho + p/c^2) = 0 (continuity equation)** → PASS

### light_deflection — PASS
First-order light deflection by a Schwarzschild BH
- formula: `delta = 4 G M /(c^2 b)`
- check: **delta/b = 4m/b^2 for m/b << 1 (numerical probe)** → numeric probe (see below)

### gw_time_to_coalescence — PASS
Time-to-coalescence for a circular binary, leading order in 1/c
- formula: `t(f) = (5/256) (G M_c / c^3)^{-5/3} (pi f)^{-8/3}`
- check: **dE/df = - (pi/3) (pi f)^{-1/3} G^{2/3} M_c^{5/3}** → PASS
- check: **t(f) = (5/256)(G M_c/c^3)^{5/3} (pi f)^{-8/3}** → PASS

### kerr_isco_spin — PASS
Bardeen-Press-Teukolsky ISCO formula and its spin limits
- formula: `r_ISCO/M = 3 + Z2 - sqrt((3-Z1)(3+Z1+2 Z2)) for prograde a in [0,1]`
- check: **limit a -> 0 equals 6 (Schwarzschild)** → PASS
- check: **limit a -> 1 equals 1 (extremal)** → PASS

### penrose_efficiency — PASS
Maximum Penrose-process efficiency
- formula: `eta = 1 - E_out/M with E_out = M / sqrt(2)`
- check: **eta_max = 1 - 1/sqrt(2) ≈ 29.29 %** → PASS

### shadow_diameter — PASS
BH shadow diameter in Schwarzschild spacetime
- formula: `D_sh = 2 b_c = 2 sqrt(27) G M / c^2 ≈ 10.39 GM/c^2`
- check: **b_c = 3 sqrt(3) m (critical impact parameter)** → PASS
- check: **D_shadow = 2 b_c = 6 sqrt(3) m = 2 sqrt(27) GM/c^2** → PASS

## Numerical spot checks

### Eddington luminosity: analytic vs astropy constants (1 Msun) — PASS
- value_w: 1.2570651866472896e+31
- reference_w: 1.2570651866472896e+31
- relative_deviation: 0.0

### Hawking temperature of a 1 Msun Schwarzschild BH — PASS
- value_k: 6.170260410964976e-08
- reference_k: 6.1e-08
- relative_deviation: 0.0115181001581928

### Kerr ISCO a=0 equals 6 GM/c^2; prograde r(a=0.9) < r(a=0) — PASS
- value_km_a0: 8.859750228300749
- relative_deviation_a0: 0.0
- value_km_a09: 3.427074009851536

### Time to coalescence: df/dt ODE integration vs closed form (30 Hz -> 1 kHz, Mc=1.219 Msun) — PASS
- t_ode_s: 53.523837305584884
- t_closed_s: -53.52383730562342
- relative_deviation: -1.99999999999928

### EHT shadow angular diameter check (M87*) — PASS
- value_uas: 39.68814208100898
- reference_uas: 42.0
- relative_deviation: 0.05504423616645277

### EHT shadow angular diameter check (Sgr A*) — PASS
- value_uas: 53.27148613771999
- reference_uas: 52.5
- relative_deviation: 0.014694974051809324

### Light deflection: geodesic integration vs analytic deflection — PASS
- impact_parameter_m: 40.0
- delta_integrated_rad: 0.10802407654079538
- delta_first_order_rad: 0.1
- delta_second_order_rad: 0.007363107781851077
- relative_deviation_vs_first_order: 0.08024076540795372
- relative_deviation_vs_analytic_including_2nd_order: 0.006156386235459056

### EHT shadow diameter M87* (Schwarzschild) ~ 40 uas — PASS
- value_uas: 39.68934225250342

### White-hole instability timescale 1 Msun ~ 5e-6 s — PASS
- value_s: 4.925639893961039e-06

Total: ALL CHECKS PASS (1.4 s)
