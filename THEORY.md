# Complete Theory – Black Holes, Wormholes, White Holes

All equations are written in LaTeX.

## 1. General Relativity Basics

Metric:
$$ds^2 = g_{\mu\nu}\,dx^\mu dx^\nu$$

Christoffel:
$$\Gamma^\lambda_{\mu\nu} = \frac{1}{2} g^{\lambda\sigma}(\partial_\mu g_{\nu\sigma} + \partial_\nu g_{\mu\sigma} - \partial_\sigma g_{\mu\nu})$$

Riemann:
$$R^\rho_{\ \sigma\mu\nu} = \partial_\mu \Gamma^\rho_{\nu\sigma} - \partial_\nu \Gamma^\rho_{\mu\sigma} + \Gamma^\rho_{\mu\lambda}\Gamma^\lambda_{\nu\sigma} - \Gamma^\rho_{\nu\lambda}\Gamma^\lambda_{\mu\sigma}$$

Ricci:
$$R_{\mu\nu} = R^\lambda_{\ \mu\lambda\nu}, \quad R = g^{\mu\nu}R_{\mu\nu}$$

Einstein:
$$G_{\mu\nu} + \Lambda g_{\mu\nu} = \frac{8\pi G}{c^4} T_{\mu\nu}, \quad G_{\mu\nu}=R_{\mu\nu}-\frac12 R g_{\mu\nu}$$

## 2. Schwarzschild Black Hole

Metric:
$$ds^2 = -(1-\frac{2GM}{rc^2})c^2 dt^2 + (1-\frac{2GM}{rc^2})^{-1} dr^2 + r^2 d\Omega^2$$

Event horizon:
$$R_s = \frac{2GM}{c^2}$$

Hawking temperature:
$$T_H = \frac{\hbar c^3}{8\pi G M k_B}$$

ISCO:
$$R_{\rm ISCO} = 6 R_s \quad (\text{Schwarzschild})$$

Photon sphere:
$$R_{\rm ph} = \frac{3GM}{c^2}$$

## 3. Kerr Black Hole

Outer horizon:
$$r_+ = \frac{GM}{c^2}\left(1 + \sqrt{1 - a^2}\right)$$

Ergosphere (equator):
$$r_{\rm ergo} = \frac{2GM}{c^2}$$

## 4. White Holes

Time reversal of Schwarzschild: same metric, $t \to -t$.

Instability:
$$\delta(t) = \delta_0 e^{t/\tau}, \quad \tau \sim \frac{GM}{c^3}$$

## 5. Wormholes (Morris–Thorne)

Metric:
$$ds^2 = -e^{2\Phi(r)}dt^2 + \left(1-\frac{b(r)}{r}\right)^{-1}dr^2 + r^2 d\Omega^2$$

Throat:
$$b(r_0)=r_0$$

Flare-out:
$$b'(r_0) < 1$$

Embedding:
$$\frac{dz}{dr} = \pm \sqrt{\frac{b(r)}{r-b(r)}}$$

## 6. Hawking Radiation & Thermodynamics

Power:
$$P \sim \frac{\hbar c^6}{15360\pi G^2 M^2}$$

Lifetime:
$$\tau \sim \frac{5120\pi G^2 M^3}{\hbar c^4}$$

Bekenstein–Hawking entropy:
$$S = \frac{k_B c^3 A}{4 G \hbar}$$

## 7. Advanced

Penrose process: energy extraction from ergosphere.

Superradiance condition:
$$\omega < m\,\Omega_H$$

Kerr ISCO decreases with spin.

## 8. White Hole Deep Dive

Maximal extension (Kruskal–Szekeres) has four regions; white hole is region IV.

Instability timescale:
$$\tau \sim GM/c^3$$

Observational candidates: GRBs, FRBs (speculative).
EOF
echo written