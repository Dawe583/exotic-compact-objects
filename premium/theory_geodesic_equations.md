# Geodesic Equations for Schwarzschild and Kerr Spacetimes

## Hamilton-Jacobi Separability, Carter Constant, Effective Potentials, Orbit Classification, and Pericenter Advance

---

## 1. Introduction

The motion of test particles and light rays in black hole spacetimes is governed by the geodesic equation:

$$
\frac{d^2 x^\mu}{d\lambda^2} + \Gamma^\mu_{\nu\rho} \frac{dx^\nu}{d\lambda} \frac{dx^\rho}{d\lambda} = 0
$$

where $\lambda$ is an affine parameter (proper time $\tau$ for timelike geodesics, arbitrary affine parameter for null geodesics). For the Schwarzschild and Kerr metrics, the geodesic equations exhibit remarkable integrability properties due to the existence of sufficient conserved quantities.

This document provides a complete derivation of the geodesic equations, their first integrals, the Hamilton-Jacobi formulation, the Carter constant for Kerr, effective potentials, orbit classification, and the pericenter advance formula.

---

## 2. Geodesic Equations from the Lagrangian

### 2.1 Lagrangian Formulation

The geodesic equations can be derived from the Lagrangian:

$$
\mathcal{L} = \frac{1}{2} g_{\mu\nu} \dot{x}^\mu \dot{x}^\nu
$$

where $\dot{x}^\mu = dx^\mu/d\lambda$. The Euler-Lagrange equations:

$$
\frac{d}{d\lambda} \left( \frac{\partial \mathcal{L}}{\partial \dot{x}^\mu} \right) - \frac{\partial \mathcal{L}}{\partial x^\mu} = 0
$$

are equivalent to the geodesic equations. The canonical momenta are:

$$
p_\mu = \frac{\partial \mathcal{L}}{\partial \dot{x}^\mu} = g_{\mu\nu} \dot{x}^\nu
$$

The Hamiltonian is:

$$
\mathcal{H} = p_\mu \dot{x}^\mu - \mathcal{L} = \frac{1}{2} g^{\mu\nu} p_\mu p_\nu
$$

For affinely parameterized geodesics, $\mathcal{H} = \frac{1}{2} \epsilon$ where $\epsilon = -1$ (timelike), $0$ (null), $+1$ (spacelike).

---

## 3. Schwarzschild Geodesics

### 3.1 Metric and Lagrangian

The Schwarzschild metric in standard coordinates $(t, r, \theta, \phi)$:

$$
ds^2 = -f(r) dt^2 + f(r)^{-1} dr^2 + r^2 (d\theta^2 + \sin^2\theta d\phi^2), \quad f(r) = 1 - \frac{2M}{r}
$$

The Lagrangian:

$$
2\mathcal{L} = -f(r) \dot{t}^2 + f(r)^{-1} \dot{r}^2 + r^2 \dot{\theta}^2 + r^2 \sin^2\theta \dot{\phi}^2
$$

### 3.2 Conserved Quantities

Due to stationarity and spherical symmetry:

$$
\begin{aligned}
E &= -\frac{\partial \mathcal{L}}{\partial \dot{t}} = f(r) \dot{t} \quad \text{(energy per unit mass)} \\
L_z &= \frac{\partial \mathcal{L}}{\partial \dot{\phi}} = r^2 \sin^2\theta \dot{\phi} \quad \text{(axial angular momentum)}
\end{aligned}
$$

Spherical symmetry implies total angular momentum $L$ is conserved. By rotational symmetry, we can set $\theta = \pi/2$ (equatorial plane) without loss of generality, giving $L = L_z$.

### 3.3 Radial Equation and Effective Potential

The normalization condition $g_{\mu\nu} \dot{x}^\mu \dot{x}^\nu = \epsilon$ ($\epsilon = -1$ for timelike, $0$ for null) gives:

$$
-f(r) \dot{t}^2 + f(r)^{-1} \dot{r}^2 + r^2 \dot{\phi}^2 = \epsilon
$$

Substituting $\dot{t} = E/f(r)$ and $\dot{\phi} = L/r^2$:

$$
-\frac{E^2}{f(r)} + \frac{\dot{r}^2}{f(r)} + \frac{L^2}{r^2} = \epsilon
$$

Multiply by $f(r)$:

$$
\dot{r}^2 = E^2 - f(r)\left(\epsilon + \frac{L^2}{r^2}\right)
$$

Define the **effective potential**:

$$
\boxed{V_{\text{eff}}(r) = f(r)\left(\epsilon + \frac{L^2}{r^2}\right) = \left(1 - \frac{2M}{r}\right)\left(\epsilon + \frac{L^2}{r^2}\right)}
$$

Then:

$$
\boxed{\frac{1}{2}\dot{r}^2 + \frac{1}{2}V_{\text{eff}}(r) = \frac{1}{2}E^2}
$$

This is a 1D energy conservation equation.

### 3.4 Explicit Effective Potentials

#### Timelike Geodesics ($\epsilon = -1$):

$$
V_{\text{eff}}^{\text{(timelike)}}(r) = \left(1 - \frac{2M}{r}\right)\left(-1 + \frac{L^2}{r^2}\right) = -1 + \frac{L^2}{r^2} + \frac{2M}{r} - \frac{2ML^2}{r^3}
$$

#### Null Geodesics ($\epsilon = 0$):

$$
V_{\text{eff}}^{\text{(null)}}(r) = \left(1 - \frac{2M}{r}\right)\frac{L^2}{r^2} = \frac{L^2}{r^2} - \frac{2ML^2}{r^3}
$$

### 3.5 Orbit Classification (Timelike)

Circular orbits occur at extrema of $V_{\text{eff}}$: $dV_{\text{eff}}/dr = 0$.

$$
\frac{dV_{\text{eff}}}{dr} = -\frac{2L^2}{r^3} - \frac{2M}{r^2} + \frac{6ML^2}{r^4} = 0
$$

Multiply by $r^4/2$:

$$
-L^2 r - M r^2 + 3M L^2 = 0 \quad \Rightarrow \quad M r^2 - 3M L^2 + L^2 r = 0
$$

Solve for $L^2$:

$$
L^2 = \frac{M r^2}{r - 3M}
$$

For circular orbits to exist, need $r > 3M$.

**Innermost Stable Circular Orbit (ISCO)**: Determined by $d^2V_{\text{eff}}/dr^2 = 0$:

$$
\frac{d^2V_{\text{eff}}}{dr^2} = \frac{6L^2}{r^4} + \frac{4M}{r^3} - \frac{24ML^2}{r^5} = 0
$$

Substitute $L^2 = M r^2/(r-3M)$:

$$
\frac{6M}{r^2(r-3M)} + \frac{4M}{r^3} - \frac{24M^2}{r^3(r-3M)} = 0
$$

Multiply by $r^3(r-3M)/M$:

$$
6r + 4(r-3M) - 24M = 0 \quad \Rightarrow \quad 10r - 12M - 24M = 0 \quad \Rightarrow \quad r = \frac{36M}{10} = 6M
$$

**Result**: ISCO at $r = 6M$ for Schwarzschild.

Orbit types for timelike geodesics:
- **Bound orbits**: $E^2 < 1$, two turning points (pericenter and apocenter)
- **Unbound orbits**: $E^2 \ge 1$, one turning point (pericenter only)
- **Plunging orbits**: No turning points, fall directly into horizon
- **Circular orbits**: $E^2 = V_{\text{eff}}(r_c)$, $\dot{r} = 0$

### 3.6 Pericenter Advance (Schwarzschild)

For nearly circular bound orbits, the radial oscillation frequency $\omega_r$ differs from the angular frequency $\omega_\phi$, causing precession.

The orbital equation from $dr/d\phi = \dot{r}/\dot{\phi}$:

$$
\left(\frac{dr}{d\phi}\right)^2 = \frac{r^4}{L^2}\left[E^2 - \left(1 - \frac{2M}{r}\right)\left(1 + \frac{L^2}{r^2}\right)\right]
$$

Let $u = 1/r$, then $dr/d\phi = -(1/u^2) du/d\phi$:

$$
\left(\frac{du}{d\phi}\right)^2 = \frac{E^2 - 1}{L^2} + \frac{2M}{L^2}u - u^2 + 2M u^3
$$

Differentiate w.r.t. $\phi$:

$$
\frac{d^2u}{d\phi^2} + u = \frac{M}{L^2} + 3M u^2
$$

For nearly circular orbit $u = u_0 + \delta u$ with $u_0 = 1/r_0$:

$$
u_0 = \frac{M}{L^2} + 3M u_0^2
$$

The perturbation satisfies:

$$
\frac{d^2(\delta u)}{d\phi^2} + \delta u = 6M u_0 \delta u
$$

So:

$$
\frac{d^2(\delta u)}{d\phi^2} + (1 - 6M u_0)\delta u = 0
$$

The radial oscillation frequency in $\phi$ is:

$$
\omega_r = \sqrt{1 - \frac{6M}{r_0}}
$$

The angular period is $2\pi$, so the advance per orbit is:

$$
\Delta\phi = 2\pi\left(\frac{1}{\omega_r} - 1\right) \approx 2\pi\left(\frac{1}{\sqrt{1 - 6M/r_0}} - 1\right) \approx \frac{6\pi M}{r_0}
$$

More precisely, using $r_0 = a(1-e^2)$ for elliptical orbits:

$$
\boxed{\Delta\phi = \frac{6\pi M}{a(1-e^2)}}
$$

This is the famous **pericenter advance** (e.g., Mercury's 43''/century).

---

## 4. Kerr Geodesics

### 4.1 Metric and Lagrangian

Kerr metric in Boyer-Lindquist coordinates:

$$
\begin{aligned}
ds^2 &= -\left(1 - \frac{2Mr}{\rho^2}\right) dt^2 - \frac{4Mra\sin^2\theta}{\rho^2} dt d\phi + \frac{\rho^2}{\Delta} dr^2 + \rho^2 d\theta^2 \\
&\quad + \left(r^2 + a^2 + \frac{2Mra^2\sin^2\theta}{\rho^2}\right)\sin^2\theta d\phi^2
\end{aligned}
$$

where $\rho^2 = r^2 + a^2\cos^2\theta$, $\Delta = r^2 - 2Mr + a^2$.

The Lagrangian:

$$
2\mathcal{L} = g_{tt}\dot{t}^2 + 2g_{t\phi}\dot{t}\dot{\phi} + g_{rr}\dot{r}^2 + g_{\theta\theta}\dot{\theta}^2 + g_{\phi\phi}\dot{\phi}^2
$$

### 4.2 Conserved Quantities

From stationarity ($\partial_t$) and axisymmetry ($\partial_\phi$):

$$
\begin{aligned}
E &= -p_t = -g_{tt}\dot{t} - g_{t\phi}\dot{\phi} \quad \text{(energy)} \\
L_z &= p_\phi = g_{t\phi}\dot{t} + g_{\phi\phi}\dot{\phi} \quad \text{(axial angular momentum)}
\end{aligned}
$$

Solving for $\dot{t}$ and $\dot{\phi}$:

$$
\begin{pmatrix} \dot{t} \\ \dot{\phi} \end{pmatrix} = \frac{1}{g_{tt}g_{\phi\phi} - g_{t\phi}^2} \begin{pmatrix} g_{\phi\phi} & -g_{t\phi} \\ -g_{t\phi} & g_{tt} \end{pmatrix} \begin{pmatrix} -E \\ L_z \end{pmatrix}
$$

Using $g_{tt}g_{\phi\phi} - g_{t\phi}^2 = -\Delta\sin^2\theta/\rho^2$:

$$
\begin{aligned}
\dot{t} &= \frac{1}{\Delta}\left[(r^2+a^2)\frac{(r^2+a^2)E - a L_z}{\rho^2} + a(L_z - a E\sin^2\theta)\right] \\
\dot{\phi} &= \frac{1}{\Delta}\left[a\frac{(r^2+a^2)E - a L_z}{\rho^2} + \frac{L_z}{\sin^2\theta} - a E\right]
\end{aligned}
$$

### 4.3 Hamilton-Jacobi Separability

The Hamilton-Jacobi equation for geodesics:

$$
\frac{\partial S}{\partial \lambda} + \frac{1}{2}g^{\mu\nu}\frac{\partial S}{\partial x^\mu}\frac{\partial S}{\partial x^\nu} = 0
$$

For stationary, axisymmetric spacetimes, seek solution:

$$
S = \frac{1}{2}\epsilon\lambda - E t + L_z \phi + S_r(r) + S_\theta(\theta)
$$

Substitute into HJ equation. The inverse metric components:

$$
\begin{aligned}
g^{tt} &= -\frac{(r^2+a^2)^2 - a^2\Delta\sin^2\theta}{\rho^2\Delta} \\
g^{t\phi} &= -\frac{2Mra}{\rho^2\Delta} \\
g^{\phi\phi} &= \frac{\Delta - a^2\sin^2\theta}{\rho^2\Delta\sin^2\theta} \\
g^{rr} &= \frac{\Delta}{\rho^2} \\
g^{\theta\theta} &= \frac{1}{\rho^2}
\end{aligned}
$$

The HJ equation becomes:

$$
\frac{\Delta}{\rho^2}\left(\frac{dS_r}{dr}\right)^2 + \frac{1}{\rho^2}\left(\frac{dS_\theta}{d\theta}\right)^2 + \frac{1}{\rho^2\Delta}\left[((r^2+a^2)E - a L_z)^2 - \Delta(L_z\csc\theta - a E\sin\theta)^2\right] = \epsilon
$$

Multiply by $\rho^2$:

$$
\Delta\left(\frac{dS_r}{dr}\right)^2 + \left(\frac{dS_\theta}{d\theta}\right)^2 + \frac{1}{\Delta}\left[((r^2+a^2)E - a L_z)^2 - \Delta(L_z\csc\theta - a E\sin\theta)^2\right] = \epsilon\rho^2
$$

**Key observation**: The $r$ and $\theta$ dependence separates! Rearrange:

$$
\Delta\left(\frac{dS_r}{dr}\right)^2 - \frac{((r^2+a^2)E - a L_z)^2}{\Delta} - \epsilon r^2 = -\left(\frac{dS_\theta}{d\theta}\right)^2 - (L_z\csc\theta - a E\sin\theta)^2 - \epsilon a^2\cos^2\theta
$$

Left side depends only on $r$, right side only on $\theta$. Both equal a separation constant $\mathcal{Q}$ (the **Carter constant**).

### 4.4 Carter Constant

Define:

$$
\boxed{\mathcal{Q} = \left(\frac{dS_\theta}{d\theta}\right)^2 + (L_z\csc\theta - a E\sin\theta)^2 + \epsilon a^2\cos^2\theta}
$$

Equivalently, in terms of momenta:

$$
\boxed{\mathcal{Q} = p_\theta^2 + (L_z\csc\theta - a E\sin\theta)^2 + \epsilon a^2\cos^2\theta}
$$

For timelike geodesics ($\epsilon = -1$), Carter's original definition is often:

$$
\mathcal{K} = \mathcal{Q} + (L_z - a E)^2
$$

where $\mathcal{K}$ is the Carter constant as originally defined.

### 4.5 First-Order Geodesic Equations

From the separation:

#### Radial Equation:

$$
\rho^4 \dot{r}^2 = \Delta^2 \left(\frac{dS_r}{dr}\right)^2 = \left[(r^2+a^2)E - a L_z\right]^2 - \Delta\left[\mathcal{Q} + (L_z - a E)^2 + \epsilon r^2\right]
$$

Define the **radial potential**:

$$
\boxed{R(r) = \left[(r^2+a^2)E - a L_z\right]^2 - \Delta\left[\mathcal{Q} + (L_z - a E)^2 + \epsilon r^2\right]}
$$

Then:

$$
\boxed{\rho^4 \dot{r}^2 = R(r)}
$$

#### Polar Equation:

$$
\rho^4 \dot{\theta}^2 = \left(\frac{dS_\theta}{d\theta}\right)^2 = \mathcal{Q} - (L_z\csc\theta - a E\sin\theta)^2 - \epsilon a^2\cos^2\theta
$$

Define the **polar potential**:

$$
\boxed{\Theta(\theta) = \mathcal{Q} - (L_z\csc\theta - a E\sin\theta)^2 - \epsilon a^2\cos^2\theta}
$$

Then:

$$
\boxed{\rho^4 \dot{\theta}^2 = \Theta(\theta)}
$$

#### Time and Azimuthal Equations:

$$
\boxed{
\begin{aligned}
\rho^2 \dot{t} &= \frac{(r^2+a^2)}{\Delta}\left[(r^2+a^2)E - a L_z\right] - a(a E\sin^2\theta - L_z) \\
\rho^2 \dot{\phi} &= \frac{a}{\Delta}\left[(r^2+a^2)E - a L_z\right] + \frac{L_z}{\sin^2\theta} - a E
\end{aligned}
}
$$

### 4.6 Effective Potentials

#### Radial Effective Potential

For given $E, L_z, \mathcal{Q}$, the radial motion is governed by:

$$
\frac{1}{2}\dot{r}^2 + V_{\text{eff}}(r) = \frac{1}{2}E^2
$$

where $V_{\text{eff}}$ is defined implicitly by $R(r) = \rho^4(E^2 - 2V_{\text{eff}})$ for timelike ($\epsilon=-1$). Explicitly:

$$
R(r) = \left[(r^2+a^2)E - a L_z\right]^2 - \Delta\left[\mathcal{Q} + (L_z - a E)^2 - r^2\right]
$$

Expand:

$$
\begin{aligned}
R(r) &= E^2(r^2+a^2)^2 - 2aE L_z(r^2+a^2) + a^2 L_z^2 \\
&\quad - (r^2 - 2Mr + a^2)\left[\mathcal{Q} + L_z^2 - 2a E L_z + a^2 E^2 - r^2\right]
\end{aligned}
$$

This is a quartic polynomial in $r$. The roots determine turning points.

#### Polar Effective Potential

The $\theta$ motion is bounded by $\Theta(\theta) \ge 0$. For equatorial orbits ($\theta = \pi/2$, $\dot{\theta} = 0$):

$$
\mathcal{Q} = 0 \quad \text{(equatorial)}
$$

For inclined orbits, $\mathcal{Q} > 0$ (prograde) or $\mathcal{Q} < 0$ (retrograde relative to frame-dragging).

The polar motion oscillates between $\theta_{\text{min}}$ and $\theta_{\text{max}}$ where $\Theta(\theta) = 0$.

### 4.7 Orbit Classification (Kerr)

The radial potential $R(r)$ is a quartic polynomial. Its roots classify orbits:

$$
R(r) = E^2 r^4 + 2M E^2 r^3 + \cdots
$$

Actually, expand properly:

$$
\begin{aligned}
R(r) &= \left[E r^2 + E a^2 - a L_z\right]^2 - (r^2 - 2Mr + a^2)\left[\mathcal{Q} + L_z^2 - 2a E L_z + a^2 E^2 - r^2\right] \\
&= E^2 r^4 + 2E(E a^2 - a L_z) r^2 + (E a^2 - a L_z)^2 \\
&\quad - \left[(r^2 - 2Mr + a^2)(\mathcal{Q} + L_z^2 - 2a E L_z + a^2 E^2) - (r^2 - 2Mr + a^2)r^2\right] \\
&= E^2 r^4 + \cdots + r^4 - 2M r^3 + a^2 r^2 - \cdots
\end{aligned}
$$

Leading order: $R(r) \sim (E^2 - 1)r^4 + 2M r^3 + \cdots$

**Classification by roots of $R(r) = 0$**:

For timelike geodesics ($E^2 < 1$ for bound):
- **4 real roots**: Bound orbit (libration between two roots)
- **2 real roots, 2 complex**: Unbound orbit (scattering)
- **1 real root (triple)**: Critical plunging orbit
- **0 real roots**: Plunging orbit

**Special orbits**:
- **Spherical orbits**: $R(r) = R'(r) = 0$ (constant $r$)
- **Homoclinic orbits**: Asymptotic to unstable spherical orbit
- **ISCO**: Innermost stable circular orbit (marginally stable spherical orbit)

#### Equatorial Orbits ($\mathcal{Q} = 0$)

For prograde/retrograde equatorial orbits, the ISCO radii are:

$$
r_{\text{ISCO}} = M\left[3 + Z_2 \mp \sqrt{(3-Z_1)(3+Z_1+2Z_2)}\right]
$$

where

$$
Z_1 = 1 + \sqrt[3]{1-\chi^2}\left(\sqrt[3]{1+\chi} + \sqrt[3]{1-\chi}\right), \quad Z_2 = \sqrt{3\chi^2 + Z_1^2}
$$

and $\chi = a/M$. The upper sign is prograde, lower is retrograde.

For $\chi = 0$: $r_{\text{ISCO}} = 6M$ (Schwarzschild).
For $\chi = 1$ (extremal): $r_{\text{ISCO}}^{\text{pro}} = M$, $r_{\text{ISCO}}^{\text{retro}} = 9M$.

---

## 5. Hamilton-Jacobi Theory and Action-Angle Variables

### 5.1 Action Variables

The action variables for Kerr geodesics:

$$
\begin{aligned}
J_r &= \frac{1}{2\pi}\oint p_r dr = \frac{1}{\pi}\int_{r_{\text{min}}}^{r_{\text{max}}} \frac{\sqrt{R(r)}}{\Delta} dr \\
J_\theta &= \frac{1}{2\pi}\oint p_\theta d\theta = \frac{1}{\pi}\int_{\theta_{\text{min}}}^{\theta_{\text{max}}} \sqrt{\Theta(\theta)} d\theta \\
J_\phi &= L_z \\
J_t &= -E
\end{aligned}
$$

These are adiabatic invariants for slowly evolving systems.

### 5.2 Fundamental Frequencies

The fundamental frequencies are:

$$
\Omega_i = \frac{\partial H}{\partial J_i}, \quad i \in \{r, \theta, \phi\}
$$

where $H = \frac{1}{2}g^{\mu\nu}p_\mu p_\nu = \frac{1}{2}\epsilon$.

For bound orbits, the motion is quasi-periodic with three frequencies:
- $\Omega_r$: radial frequency
- $\Omega_\theta$: polar frequency
- $\Omega_\phi$: azimuthal frequency

The orbit is periodic iff $\Omega_r/\Omega_\theta$ and $\Omega_\phi/\Omega_\theta$ are rational.

### 5.3 Mino Time Parametrization

For elliptic integrals, introduce **Mino time** $\lambda$ (not to be confused with affine parameter):

$$
d\lambda = \frac{d\tau}{\rho^2}
$$

Then:

$$
\begin{aligned}
\left(\frac{dr}{d\lambda}\right)^2 &= R(r) \\
\left(\frac{d\theta}{d\lambda}\right)^2 &= \Theta(\theta) \\
\frac{dt}{d\lambda} &= \frac{(r^2+a^2)^2 E - 2Mra L_z}{\Delta} + a^2 E\sin^2\theta - a L_z \\
\frac{d\phi}{d\lambda} &= \frac{2Mra E + (\Delta - a^2\sin^2\theta)L_z/\sin^2\theta}{\Delta}
\end{aligned}
$$

The $r$ and $\theta$ equations decouple completely in Mino time.

---

## 6. Pericenter Advance in Kerr

### 6.1 General Formula

For nearly circular, nearly equatorial orbits in Kerr, the pericenter advance per radial period is:

$$
\Delta\phi = 2\pi\left(\frac{\Omega_\phi}{\Omega_r} - 1\right)
$$

The frequencies can be computed from the effective potential or via Mino time integrals.

### 6.2 Weak-Field Expansion

For large $r$ (post-Newtonian expansion), the advance per orbit is:

$$
\Delta\phi = \frac{6\pi M}{a(1-e^2)} \mp \frac{8\pi a M^{3/2}}{a^{3/2}(1-e^2)^{3/2}} + \mathcal{O}(M^2/a^2)
$$

where the upper sign is prograde, lower is retrograde. The second term is the **Lense-Thirring precession** due to frame-dragging.

### 6.3 Exact Strong-Field Expression

For exact strong-field orbits, the advance is computed from:

$$
\Delta\phi = \oint \frac{d\phi}{dr} dr = 2\int_{r_{\text{min}}}^{r_{\text{max}}} \frac{\dot{\phi}}{\dot{r}} dr
$$

Using the first-order equations:

$$
\frac{d\phi}{dr} = \frac{\rho^2 \dot{\phi}}{\rho^2 \dot{r}} = \frac{\frac{a}{\Delta}[(r^2+a^2)E - a L_z] + \frac{L_z}{\sin^2\theta} - a E}{\pm\sqrt{R(r)}/\rho^2}
$$

For equatorial orbits ($\theta = \pi/2$, $\mathcal{Q} = 0$):

$$
\Delta\phi = 2\int_{r_p}^{r_a} \frac{\frac{a}{\Delta}[(r^2+a^2)E - a L_z] + L_z - a E}{\sqrt{R(r)}} \rho^2 dr
$$

This integral can be expressed in terms of elliptic integrals.

### 6.4 Pericenter Advance for Circular Orbits

For circular orbits at radius $r_0$, the radial epicyclic frequency $\kappa$ is:

$$
\kappa^2 = \frac{1}{2g_{rr}}\frac{d^2V_{\text{eff}}}{dr^2}\bigg|_{r_0}
$$

The azimuthal frequency is $\Omega = d\phi/dt$. The advance per orbit:

$$
\Delta\phi = 2\pi\left(\frac{\Omega}{\kappa} - 1\right)
$$

For Kerr equatorial circular orbits:

$$
\Omega = \frac{M^{1/2}}{r_0^{3/2} \pm a M^{1/2}}
$$

$$
\kappa^2 = \Omega^2\left(1 - \frac{6M}{r_0} \pm \frac{8a M^{1/2}}{r_0^{3/2}} - \frac{3a^2}{r_0^2}\right)
$$

Then:

$$
\boxed{\Delta\phi = 2\pi\left[\left(1 - \frac{6M}{r_0} \pm \frac{8a M^{1/2}}{r_0^{3/2}} - \frac{3a^2}{r_0^2}\right)^{-1/2} - 1\right]}
$$

---

## 7. Null Geodesics and Gravitational Lensing

### 7.1 Null Geodesic Equations

For photons ($\epsilon = 0$), the equations simplify. The impact parameters:

$$
\xi = \frac{L_z}{E}, \quad \eta = \frac{\mathcal{Q}}{E^2}
$$

The radial and polar potentials become:

$$
\begin{aligned}
R(r) &= \left[(r^2+a^2) - a\xi\right]^2 - \Delta\left[\eta + (\xi - a)^2\right] \\
\Theta(\theta) &= \eta + a^2\cos^2\theta - \xi^2\cot^2\theta
\end{aligned}
$$

### 7.2 Spherical Photon Orbits

Spherical orbits ($r = \text{const}$) satisfy $R(r) = R'(r) = 0$. The critical impact parameters:

$$
\begin{aligned}
\xi &= \frac{r^2(r-3M) + a^2(r+M)}{a(r-M)} \\
\eta &= \frac{r^3(4a^2M - r(r-3M)^2)}{a^2(r-M)^2}
\end{aligned}
$$

The photon sphere in Schwarzschild is at $r = 3M$.

### 7.3 Shadow of Kerr Black Hole

The boundary of the black hole shadow is given by the critical impact parameters $(\xi, \eta)$ for spherical photon orbits. The shadow shape is:

$$
\alpha = -\xi\csc\theta_o, \quad \beta = \pm\sqrt{\eta + a^2\cos^2\theta_o - \xi^2\cot^2\theta_o}
$$

where $\theta_o$ is the observer's inclination.

---

## 8. Summary of Key Formulas

### 8.1 Schwarzschild

| Quantity | Expression |
|----------|------------|
| Effective potential (timelike) | $V_{\text{eff}} = (1-2M/r)(-1 + L^2/r^2)$ |
| Effective potential (null) | $V_{\text{eff}} = (1-2M/r)L^2/r^2$ |
| ISCO | $r = 6M$ |
| Photon sphere | $r = 3M$ |
| Pericenter advance | $\Delta\phi = 6\pi M / [a(1-e^2)]$ |

### 8.2 Kerr

| Quantity | Expression |
|----------|------------|
| Radial potential | $R(r) = [(r^2+a^2)E - a L_z]^2 - \Delta[\mathcal{Q} + (L_z - a E)^2 + \epsilon r^2]$ |
| Polar potential | $\Theta(\theta) = \mathcal{Q} - (L_z\csc\theta - a E\sin\theta)^2 - \epsilon a^2\cos^2\theta$ |
| Carter constant | $\mathcal{Q} = p_\theta^2 + (L_z\csc\theta - a E\sin\theta)^2 + \epsilon a^2\cos^2\theta$ |
| Prograde ISCO ($a=M$) | $r = M$ |
| Retrograde ISCO ($a=M$) | $r = 9M$ |
| Pericenter advance (circular) | $\Delta\phi = 2\pi[(1 - 6M/r_0 \pm 8a\sqrt{M/r_0^3} - 3a^2/r_0^2)^{-1/2} - 1]$ |

---

## 9. Conclusion

The geodesic equations in Schwarzschild and Kerr spacetimes are completely integrable. The Schwarzschild case has 4 conserved quantities ($E, L_x, L_y, L_z$ with one constraint), while Kerr has 4 independent conserved quantities ($E, L_z, \mathcal{Q}, \epsilon$) due to the hidden symmetry represented by the Killing-Yano tensor. This allows reduction to quadratures and analytic solutions in terms of elliptic functions. The pericenter advance formula generalizes the classic Schwarzschild result to include frame-dragging effects in Kerr.

---

*End of document. All derivations are self-contained and step-by-step.*