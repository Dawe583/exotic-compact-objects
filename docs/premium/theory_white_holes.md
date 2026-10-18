# White Holes: A Complete Theoretical Treatment

**Author:** GR Theory Working Group  
**Date:** October 2026  
**Status:** Self-contained theoretical review with full derivations  

---

## 1. Definition: The Time-Reversed Schwarzschild Solution

### 1.1 Schwarzschild Metric and Time Reversal

The Schwarzschild metric in standard coordinates $(t, r, \theta, \phi)$ is:

\begin{equation}
ds^2 = -\left(1 - \frac{r_s}{r}\right) c^2 dt^2 + \left(1 - \frac{r_s}{r}\right)^{-1} dr^2 + r^2 d\Omega^2
\label{eq:schwarzschild}
\end{equation}

where $r_s = 2GM/c^2$ is the Schwarzschild radius and $d\Omega^2 = d\theta^2 + \sin^2\theta \, d\phi^2$ is the metric on the unit 2-sphere.

Under time reversal $t \to -t$, the metric \eqref{eq:schwarzschild} is invariant, since $g_{tt}$ depends only on $r$. This symmetry is deceptive: while the \emph{metric tensor} is invariant, the \emph{causal structure} distinguishes the black hole (BH) from the white hole (WH) regions. The time-reversed interpretation emerges when we consider which region of the maximal extension we are describing.

The Schwarzschild solution is a vacuum solution ($R_{\mu\nu} = 0$) of the Einstein field equations:

\begin{equation}
R_{\mu\nu} - \frac{1}{2} R g_{\mu\nu} = \frac{8\pi G}{c^4} T_{\mu\nu} = 0
\end{equation}

The Birkhoff theorem guarantees that any spherically symmetric vacuum solution is asymptotically flat and isometric to the Schwarzschild solution.

### 1.2 Kruskal-Szekeres Maximal Extension

The coordinate singularity at $r = r_s$ in \eqref{eq:schwarzschild} is removed by the Kruskal-Szekeres transformation. Define:

\begin{equation}
u = \left(\frac{r}{r_s} - 1\right)^{1/2} e^{r/(2r_s)} \cosh\left(\frac{ct}{2r_s}\right)
\end{equation}

\begin{equation}
v = \left(\frac{r}{r_s} - 1\right)^{1/2} e^{r/(2r_s)} \sinh\left(\frac{ct}{2r_s}\right)
\end{equation}

for $r > r_s$, and:

\begin{equation}
u = \left(1 - \frac{r}{r_s}\right)^{1/2} e^{r/(2r_s)} \sinh\left(\frac{ct}{2r_s}\right)
\end{equation}

\begin{equation}
v = \left(1 - \frac{r}{r_s}\right)^{1/2} e^{r/(2r_s)} \cosh\left(\frac{ct}{2r_s}\right)
\end{equation}

for $r < r_s$. The inverse relations are:

\begin{equation}
\left(\frac{r}{r_s} - 1\right) e^{r/r_s} = u^2 - v^2
\label{eq:r_of_uv}
\end{equation}

\begin{equation}
\frac{ct}{2r_s} = \tanh^{-1}\left(\frac{v}{u}\right) \quad \text{for } r > r_s, \qquad
\frac{ct}{2r_s} = \tanh^{-1}\left(\frac{u}{v}\right) \quad \text{for } r < r_s
\label{eq:t_of_uv}
\end{equation}

The metric becomes:

\begin{equation}
ds^2 = \frac{4r_s^3}{r} e^{-r/r_s} \left(-c^2 dt_{\text{KS}}^2 + dr_{\text{KS}}^2\right) + r^2 d\Omega^2
\label{eq:kruskal_metric}
\end{equation}

where we define null Kruskal coordinates:

\begin{equation}
U = u - v, \qquad V = u + v
\end{equation}

so that:

\begin{equation}
ds^2 = -\frac{4r_s^3}{r} e^{-r/r_s} \left(-c^2 dU\, dV\right) + r^2 d\Omega^2 = -\frac{4r_s^3}{r} e^{-r/r_s} c^2 dU\, dV + r^2 d\Omega^2
\label{eq:kruskal_null}
\end{equation}

### 1.3 The Four Regions

The Kruskal diagram divides spacetime into four distinct regions:

\begin{align}
\textbf{Region I (Exterior):} \quad & u > 0, \quad |v| < u, \quad r > r_s \\
\textbf{Region II (Black Hole Interior):} \quad & v > 0, \quad |u| < v, \quad r < r_s \\
\textbf{Region III (Parallel Exterior):} \quad & u < 0, \quad |v| < -u, \quad r > r_s \\
\textbf{Region IV (White Hole Interior):} \quad & v < 0, \quad |u| < -v, \quad r < r_s
\end{align}

In Region I (our universe), the future-directed timelike curves ($dt > 0$) flow from the past horizon ($U = 0$, $V > 0$) toward the future horizon ($V = 0$, $U > 0$), crossing into Region II where they inevitably reach $r = 0$.

In Region IV, the situation is reversed: past-directed timelike curves emerge from the past singularity at $r = 0$ and flow toward the white hole horizon at $U = 0$, $V < 0$. No future-directed timelike curve can enter Region IV from Region I.

### 1.4 Horizons as Null Surfaces

The event horizon $r = r_s$ is a null hypersurface. In Kruskal coordinates:

\begin{equation}
r = r_s \iff u^2 - v^2 = 0 \iff u = \pm v
\end{equation}

These are the null surfaces $U = 0$ ($v = u$, for $u > 0$ this is Region I $\leftrightarrow$ II) and $V = 0$ ($v = -u$, for $u > 0$ this is Region I $\leftrightarrow$ IV). The surface gravity $\kappa$ is:

\begin{equation}
\kappa = \frac{c^4}{4GM} = \frac{c^2}{2r_s}
\end{equation}

The Killing vector $\xi = \partial_t$ is:

\begin{equation}
\xi^\mu = \left(\frac{c}{2r_s}\right)(u \partial_u + v \partial_v)
\end{equation}

On the future horizon ($U = 0$), $\xi$ is null and generates the horizon. On the past horizon ($V = 0$), $\xi$ is also null, but the flow is \emph{outward}---this is the white hole horizon.

The surface gravity of the white hole horizon has the same magnitude but opposite sign in the sense that the horizon generators are past-directed. This can be seen by computing the norm:

\begin{equation}
\|\xi\|^2 = g_{\mu\nu} \xi^\mu \xi^\nu = -\frac{r_s}{r}\left(1 - \frac{r_s}{r}\right) \cdot \frac{1}{4} (u^2 - v^2) \cdot \frac{4}{r_s^2} \cdot \frac{r}{r_s} e^{-r/r_s}
\end{equation}

Evaluating on $r = r_s$: $\|\xi\|^2 = 0$, confirming the null character.

---

## 2. Metric in Kruskal Coordinates and the White Hole Region

### 2.1 Explicit Metric Components

From \eqref{eq:kruskal_null}, the metric in $(U, V, \theta, \phi)$ coordinates is:

\begin{equation}
ds^2 = -\frac{4r_s^3}{r} e^{-r/r_s} c^2 dU\, dV + r^2 (d\theta^2 + \sin^2\theta \, d\phi^2)
\end{equation}

where $r = r(U, V)$ is determined implicitly by:

\begin{equation}
\frac{r}{r_s} e^{r/r_s} = \frac{r}{r_s} e^{r/r_s} = UV + \frac{r_s}{r} e^{r/r_s} \cdot r_s \quad \text{with} \quad \frac{r}{r_s}e^{r/r_s} = 1 + \frac{UV}{r_s} e^{1}
\end{equation}

More cleanly:

\begin{equation}
\left(\frac{r}{r_s} - 1\right) e^{r/r_s} = UV = u^2 - v^2
\end{equation}

The lapse and shift in $(U, V)$ coordinates can be extracted by writing $ds^2 = -\Omega^{-2} dU\, dV + r^2 d\Omega^2$ where:

\begin{equation}
\Omega^2 = \frac{r}{4r_s^3} e^{r/r_s} c^{-2}
\end{equation}

### 2.2 White Hole Interior: Region IV

In Region IV, $V = u + v > 0$ but $u < 0$ and $|u| < -v$, meaning $u < 0$, $v < 0$, and $|u| < |v|$. The metric becomes:

\begin{equation}
ds^2 = \frac{4r_s^3}{r} e^{-r/r_s} \left(-c^2 dU\, dV\right) + r^2 d\Omega^2, \quad r < r_s
\end{equation}

The key feature is that $r$ is now a \emph{decreasing} function of proper time for future-directed observers:

\begin{equation}
\frac{dr}{d\tau} = -\sqrt{E^2 - \left(1 - \frac{r_s}{r}\right)\left(1 + \frac{L^2}{r^2}\right)}
\end{equation}

where $E$ and $L$ are the conserved specific energy and angular momentum. The minus sign is essential: $r$ always decreases toward $0$.

### 2.3 Singularity in the Past

The singularity at $r = 0$ in Region IV is a \emph{past} singularity. This can be seen by examining the Kretschmann scalar:

\begin{equation}
R_{\mu\nu\rho\sigma} R^{\mu\nu\rho\sigma} = \frac{48 G^2 M^2}{c^4 r^6} = \frac{3 c^8}{4 G^2 M^2 r^6}
\label{eq:kretschmann}
\end{equation}

At $r \to 0$, $R_{\mu\nu\rho\sigma} R^{\mu\nu\rho\sigma} \to \infty$, confirming a physical singularity. The causal structure is that of a past boundary: all timelike curves in Region IV originate at $r = 0$ and cannot be extended beyond it into the past.

In Region II (black hole), the singularity is in the \emph{future}: all timelike curves end at $r = 0$.

This is the fundamental distinction:
\begin{align}
\text{Black hole (Region II):} \quad & \text{singularity in the future, } r \text{ decreases} \\
\text{White hole (Region IV):} \quad & \text{singularity in the past, } r \text{ increases}
\end{align}

### 2.4 Geodesic Structure in Region IV

Radial geodesics in Region IV satisfy:

\begin{equation}
\left(\frac{dr}{d\tau}\right)^2 = E^2 - \left(1 - \frac{r_s}{r}\right)
\end{equation}

For a particle starting at the singularity $r = 0$ with $E > 0$:

\begin{equation}
\tau(r) = \int_0^r \frac{dr'}{\sqrt{E^2 - 1 + r_s/r'}} = \frac{r_s}{E^2 - 1} \left[\sqrt{\frac{r}{r_s}\left(\frac{r}{r_s} + E^2 - 1\right)} - \frac{E^2 - 1}{2} \ln\left(\frac{\sqrt{r/r_s} + \sqrt{r/r_s + E^2 - 1}}{\sqrt{E^2 - 1}}\right)\right]
\end{equation}

For $E \gg 1$ (ultra-relativistic), $\tau \approx \frac{2}{3} \frac{r^{3/2}}{\sqrt{r_s}}$, the free-fall time. The particle reaches the horizon $r = r_s$ in finite proper time:

\begin{equation}
\Delta\tau_{IV} = \frac{2}{3} \frac{r_s}{c} \approx 1.05 \times 10^{-5} \left(\frac{M}{M_\odot}\right) \text{ s}
\end{equation}

For a solar-mass white hole, the total lifetime of Region IV is $\sim 10^{-5}$ s. For a supermassive white hole of $10^9 M_\odot$:

\begin{equation}
\Delta\tau_{IV} \approx 1.05 \times 10^{-5} \times 10^9 \text{ s} \approx 10^4 \text{ s} \approx 3 \text{ hours}
\end{equation}

---

## 3. Instability Analysis

### 3.1 Perturbation Equations

Consider scalar perturbations $\Phi$ on the Schwarzschild background. The Regge-Wheeler equation for odd-parity perturbations (and the Zerilli equation for even-parity) takes the form of a Schrödinger-like equation:

\begin{equation}
\frac{d^2\Psi}{dr_*^2} + \left(\omega^2 - V_{\text{eff}}(r)\right) \Psi = 0
\label{eq:regge_wheeler}
\end{equation}

where $r_* = r + r_s \ln|r/r_s - 1|$ is the tortoise coordinate and $V_{\text{eff}}$ is an effective potential.

For the white hole, the boundary conditions are reversed: instead of requiring purely ingoing waves at the horizon (black hole) and outgoing waves at infinity, we require purely \emph{outgoing} waves at the white hole horizon and \emph{ingoing} waves at infinity (since time is reversed).

### 3.2 Growth vs Damping: The QNM Spectrum

The quasi-normal mode (QNM) frequencies $\omega_n = \omega_n^{(R)} + i\omega_n^{(I)}$ satisfy:

\begin{equation}
\omega_n^{(I)} > 0 \quad \text{(damped modes, black hole)}
\end{equation}

For a black hole, $\omega_n^{(I)} > 0$ means $e^{-i\omega_n t} = e^{-i\omega_n^{(R)} t} e^{\omega_n^{(I)} t}$ grows exponentially in time. Wait---this is the convention where $\omega_n^{(I)} > 0$ corresponds to \emph{growing} modes for $e^{-i\omega t}$ convention. Let us be precise:

With the convention $e^{-i\omega t}$, a mode with $\omega = \omega_R + i\omega_I$ behaves as $e^{-i\omega_R t} e^{\omega_I t}$. Therefore:

\begin{align}
\text{Black hole:} \quad & \omega_I > 0 \quad \Rightarrow \quad \text{mode grows in time } t \to +\infty \text{ (unstable)} \\
\text{White hole:} \quad & \omega_I < 0 \quad \Rightarrow \quad \text{mode grows in time } t \to -\infty \text{ (unstable)}
\end{align}

The QNM spectrum for Schwarzschild is:

\begin{equation}
\omega_n = \frac{1}{3\sqrt{3} r_s} \left[\ln 3 + 2\pi i \left(n + \frac{1}{2}\right)\right], \quad n = 0, 1, 2, \ldots
\end{equation}

The imaginary part $\omega_I = \frac{2\pi}{3\sqrt{3} r_s} \left(n + \frac{1}{2}\right)$ is positive. This means that for a black hole, the mode grows as $t \to +\infty$. For a white hole, time is reversed: the mode grows as $t \to -\infty$, i.e., into the past.

### 3.3 The Toy Exponential Model

Consider a toy model where a perturbation amplitude $A(t)$ grows according to:

\begin{equation}
\frac{dA}{dt} = \gamma A
\end{equation}

For a white hole with surface gravity $\kappa = c^2/(2r_s)$, the Lyapunov exponent is:

\begin{equation}
\gamma = \kappa = \frac{c^2}{2r_s} = \frac{c^3}{4GM}
\end{equation}

This gives the e-folding time:

\begin{equation}
\tau_{\text{inst}} = \gamma^{-1} = \frac{2r_s}{c} = \frac{4GM}{c^3}
\end{equation}

For $M = 10 M_\odot$:

\begin{equation}
\tau_{\text{inst}} = \frac{4 \times 6.674 \times 10^{-11} \times 10 \times 1.989 \times 10^{30}}{(3 \times 10^8)^3} \approx 1.97 \times 10^{-4} \text{ s}
\end{equation}

The amplitude grows as $A(t) = A_0 e^{\gamma t}$. After one e-folding, the perturbation doubles in amplitude. After $N$ e-foldings, $A = A_0 e^N$. The perturbation becomes nonlinear when $A \sim 1$, i.e., after $N \sim \ln(1/A_0)$ e-foldings.

### 3.4 Instability from Mass Inflation

The mass inflation instability (Poisson and Israel 1990) is the strongest instability of the white hole. Consider the perturbation mass function $m(v)$ along the horizon. The evolution equation is:

\begin{equation}
\frac{dm}{dv} = \frac{1}{2} \left(\frac{dm}{dr}\right)^2 \cdot \frac{r^2}{\ell^2}
\end{equation}

where $\ell$ is a length scale of the perturbation. For a white hole, this leads to exponential growth of the interior mass:

\begin{equation}
m(v) \sim m_0 e^{\kappa v}
\end{equation}

where $v$ is the advanced time. The mass inflation timescale is:

\begin{equation}
\tau_{\text{inflation}} \sim \kappa^{-1} = \frac{2r_s}{c} \sim 10^{-5} \left(\frac{M}{M_\odot}\right) \text{ s}
\end{equation}

### 3.5 Summary of Instability Timescales

\begin{align}
\text{Free-fall time:} \quad & \tau_{\text{ff}} \sim \frac{2}{3}\frac{r_s}{c} \sim 10^{-5} \left(\frac{M}{M_\odot}\right) \text{ s} \\
\text{QNM e-folding time:} \quad & \tau_{\text{QNM}} \sim \frac{2\pi}{3\sqrt{3}} \frac{r_s}{c} \sim 10^{-4} \left(\frac{M}{M_\odot}\right) \text{ s} \\
\text{Mass inflation time:} \quad & \tau_{\text{MI}} \sim \frac{2r_s}{c} \sim 10^{-5} \left(\frac{M}{M_\odot}\right) \text{ s} \\
\text{Hawking evaporation time:} \quad & \tau_{\text{evap}} \sim \frac{5120\pi G^2 M^3}{\hbar c^4} \sim 10^{67} \left(\frac{M}{M_\odot}\right)^3 \text{ yr}
\end{align}

The white hole is catastrophically unstable on astrophysical timescales, unless stabilized by exotic physics.

---

## 4. Can White Holes Exist?

### 4.1 Classical Arguments Against

The classical argument against white holes rests on several pillars:

\textbf{(i) Thermodynamic Arrow.} The second law of thermodynamics states $dS/dt \geq 0$. A white hole \emph{decreases} the total entropy of the universe when it ejects matter, since the matter inside has low entropy (it came from a singularity) and the ejection process is irreversible. More precisely, the entropy of a white hole is:

\begin{equation}
S_{\text{WH}} = \frac{k_B c^3 A}{4 G \hbar} = \frac{4\pi k_B G M^2}{\hbar c}
\end{equation}

When the white hole ejects mass $\delta M$, its entropy changes by $\delta S = \frac{8\pi k_B G M}{\hbar c} \delta M < 0$ (since $\delta M < 0$). The ejected matter carries entropy $S_{\text{matter}} > 0$. For the second law to hold:

\begin{equation}
\delta S_{\text{total}} = \delta S_{\text{WH}} + \delta S_{\text{matter}} \geq 0
\end{equation}

This requires the ejected matter to have entropy exceeding the white hole's entropy loss, which is generically satisfied for realistic ejecta. However, the \emph{formation} of a white hole from gravitational collapse would require \emph{decreasing} the entropy of the collapsing matter, violating the second law.

\textbf{(ii) Cosmic Censorship.} Penrose's weak cosmic censorship conjecture states that singularities must be hidden behind horizons. A naked singularity (the white hole singularity at $r = 0$ in Region IV is \emph{not} hidden---it is visible to observers in Region I and III) violates cosmic censorship.

\textbf{(iii) Formation Mechanism.} There is no known classical process that can produce a white hole. The time-reversed collapse of matter into a black hole requires the matter to \emph{emerge} from a singularity, which is not a solution of the Einstein equations with realistic initial data.

\subsection 4.2 Quantum Arguments For

Quantum mechanics provides several potential pathways to white hole formation:

\textbf{(i) Hawking Radiation and Time Reversal.} The Hawking process is thermal and does not carry information. The time-reversed Hawking process would be a white hole that \emph{absorbs} thermal radiation and \emph{emits} a pure state. This is unitary but requires fine-tuning of the initial state.

\textbf{(ii) The White Hole as a Quantum Tunneling Event.} In the path integral formulation, the amplitude for tunneling from a black hole to a white hole is:

\begin{equation}
\mathcal{A} \sim e^{-S_E/\hbar}
\end{equation}

where $S_E$ is the Euclidean action. For the Schwarzschild solution, $S_E = \pi r_s^2 / G = 4\pi G M^2 / \hbar c$, giving:

\begin{equation}
\mathcal{A} \sim \exp\left(-\frac{4\pi G M^2}{\hbar c}\right)
\end{equation}

This is exponentially suppressed for macroscopic masses. For $M \sim 10^{-8}$ kg (Planck mass scale), $S_E/\hbar \sim 1$, and tunneling becomes probable.

\textbf{(iii) Loop Quantum Gravity (LQG).} In LQG, the singularity is resolved by quantum geometry effects. The black hole interior undergoes a quantum bounce, transitioning to a white hole. This is discussed in Section 6.

\subsection 4.3 The Thermodynamic Arrow and Time Reversal

The fundamental question is whether the arrow of time is:
\begin{enumerate}
\item \emph{Emergent:} determined by boundary conditions (low entropy past), or
\item \emph{Fundamental:} determined by a time-asymmetric law.
\end{enumerate}

If the arrow is emergent, white holes are as natural as black holes, and the universe could contain both. If the arrow is fundamental (e.g., due to the quantum measurement postulate or decoherence), white holes are forbidden.

The Page curve and the information paradox suggest that black hole evaporation is unitary, which is compatible with a white hole interpretation: the black hole evaporates and transitions to a white hole that releases the information.

---

## 5. Hypothesized Observational Signatures

### 5.1 Gamma-Ray Bursts (GRBs)

The most discussed signature is the white hole explosion. If a white hole of mass $M$ exists, it would eject its entire mass-energy on a timescale $\tau \sim r_s/c$. The luminosity would be:

\begin{equation}
L \sim \frac{Mc^2}{\tau} \sim \frac{Mc^3}{r_s} = \frac{c^5}{2G} \approx 1.81 \times 10^{52} \text{ W}
\end{equation}

This is independent of mass and is of order $10^{52}$ W, comparable to the Eddington luminosity of a $10^9 M_\odot$ object. The total energy is $E \sim Mc^2$, which for $M \sim 10^{12}$ kg (asteroid mass) is $E \sim 10^{29}$ J, comparable to a GRB.

The observed GRB rate is $\sim 1$ per day per sky. If white holes are responsible, the number density is:

\begin{equation}
n_{\text{WH}} \sim \frac{1}{\tau_{\text{obs}} \cdot V_{\text{obs}}} \sim \frac{1}{1 \text{ Gpc}^3 \text{ yr}}
\end{equation}

### 5.2 Fast Radio Bursts (FRBs)

FRBs have millisecond durations and dispersion measures suggesting extragalactic origins. A white hole of mass $M$ with $\tau \sim r_s/c \sim 10^{-3}$ s requires:

\begin{equation}
M \sim \frac{\tau c^3}{2G} \sim \frac{10^{-3} \times (3 \times 10^8)^3}{2 \times 6.674 \times 10^{-11}} \sim 2 \times 10^{29} \text{ kg} \sim 10^{-4} M_\odot
\end{equation}

The energy released is $E \sim Mc^2 \sim 2 \times 10^{46}$ J, within the FRB energy budget. The radio emission could be produced by coherent curvature radiation from the ejecta.

The repetition rate of some FRBs (e.g., FRB 121102) is problematic for white hole models, since a white hole is destroyed in the explosion. However, if the white hole is in a binary system and accretes matter between explosions, repeated bursts are possible.

### 5.3 Fast Transients and the "White Hole as Big Bang"

The most speculative idea is that the Big Bang itself was a white hole explosion. In this scenario, the universe emerged from a singularity that is the white hole singularity. The observable universe would be the interior of Region IV.

The correspondence can be made precise in the McVittie metric or the Schwarzschild-de Sitter metric. The scale factor $a(t)$ in a flat FLRW universe is:

\begin{equation}
a(t) \propto t^{2/3} \quad \text{(matter-dominated)}, \qquad a(t) \propto t^{1/2} \quad \text{(radiation-dominated)}
\end{equation}

The white hole ejection has $r \propto t$ in the ultra-relativistic limit, which is similar to the radiation-dominated expansion. The Hubble parameter is:

\begin{equation}
H = \frac{\dot{a}}{a} = \frac{1}{2t} \quad \text{(radiation-dominated)}
\end{equation}

The age of the universe is $t \sim H^{-1} \sim 13.8$ Gyr. If this equals the white hole time $\tau \sim r_s/c$, the mass is:

\begin{equation}
M \sim \frac{c^3 H^{-1}}{2G} \sim \frac{(3 \times 10^8)^3 \times 4.35 \times 10^{17}}{2 \times 6.674 \times 10^{-11}} \sim 10^{54} \text{ kg} \sim 10^{24} M_\odot
\end{equation}

This is roughly the mass of the observable universe, providing a suggestive numerical coincidence.

### 5.4 High-Energy Neutrinos

A white hole explosion would produce a burst of high-energy neutrinos via $p\gamma$ and $pp$ interactions in the ejecta. The neutrino energy is:

\begin{equation}
E_\nu \sim 0.05 \times \gamma_{\text{rel}} m_p c^2 \sim 0.05 \times 100 \times 938 \text{ MeV} \sim 5 \text{ TeV}
\end{equation}

IceCube and KM3NeT could detect such neutrinos, providing a distinctive signature.

---

## 6. White Holes in Cosmology: LQG and Planck Stars

### 6.1 Loop Quantum Gravity Framework

In LQG, area and volume are quantized. The area spectrum is:

\begin{equation}
A = 8\pi \gamma \ell_P^2 \sum_i \sqrt{j_i(j_i + 1)}
\end{equation}

where $\gamma$ is the Barbero-Immirzi parameter, $\ell_P = \sqrt{\hbar G/c^3}$ is the Planck length, and $j_i$ are half-integer spins.

The black hole interior, described by the Kantowski-Sachs metric:

\begin{equation}
ds^2 = -N^2 dt^2 + a^2(t) dr^2 + b^2(t) d\Omega^2
\end{equation}

undergoes a quantum bounce when the density reaches the Planck scale:

\begin{equation}
\rho \sim \rho_P = \frac{c^5}{\hbar G^2} \sim 5.16 \times 10^{96} \text{ kg/m}^3
\end{equation}

The bounce transitions the black hole interior to a white hole interior. The transition time is:

\begin{equation}
t_{\text{bounce}} \sim \frac{4M}{c^3} \left(\frac{M}{m_P}\right)^{1/3} \ell_P \sim \left(\frac{M}{m_P}\right)^{4/3} t_P
\end{equation}

where $m_P = \sqrt{\hbar c/G}$ is the Planck mass and $t_P = \ell_P/c$ is the Planck time. For $M \sim 10 M_\odot$:

\begin{equation}
t_{\text{bounce}} \sim \left(\frac{10 \times 1.989 \times 10^{30}}{2.176 \times 10^{-8}}\right)^{4/3} \times 5.39 \times 10^{-44} \text{ s} \sim 10^{-5} \text{ s} \times 10^{55} \sim 10^{50} \text{ s}
\end{equation}

This is far longer than the age of the universe. However, for small black holes ($M \sim m_P$), the bounce time is:

\begin{equation}
t_{\text{bounce}} \sim t_P \sim 10^{-43} \text{ s}
\end{equation}

### 6.2 Planck Stars

A Planck star is a hypothetical object formed when a neutron star's core reaches Planck density and undergoes a quantum bounce. The Planck star has:

\begin{equation}
R \sim \left(\frac{M}{m_P}\right)^{1/3} \ell_P \sim \left(\frac{M}{M_\odot}\right)^{1/3} \times 10^{-35} \text{ m}
\end{equation}

For $M \sim 10 M_\odot$, $R \sim 10^{-33}$ m, which is $\sim 10^2$ times smaller than the Schwarzschild radius $r_s \sim 30$ km. The Planck star is hidden inside the black hole horizon.

However, the quantum bounce creates a white hole region. The white hole horizon expands to encompass the Planck star, and the entire object becomes a white hole. The lifetime of this configuration is the black hole lifetime plus the white hole lifetime:

\begin{equation}
t_{\text{total}} \sim t_{\text{Hawking}} + t_{\text{WH}} \sim t_{\text{Hawking}}
\end{equation}

since $t_{\text{WH}} \ll t_{\text{Hawking}}$.

The Planck star scenario (Rovelli and Vidotto 2014) provides a concrete mechanism for black hole to white hole transition:

\begin{enumerate}
\item A massive star collapses to a black hole.
\item The interior reaches Planck density and bounces.
\item The bounce creates a white hole interior.
\item The white hole horizon expands and merges with the black hole horizon.
\item The object is now a white hole that eventually explodes.
\end{enumerate}

The total process takes $\sim 10^{67}$ years for a solar-mass black hole, but the final explosion is sudden and releases all the mass-energy.

### 6.3 LQG White Hole Metric

The effective LQG-corrected metric for a black hole to white hole transition can be written as:

\begin{equation}
ds^2 = -\left(1 - \frac{2GM}{c^2 r} + \frac{\alpha \ell_P^2}{r^2}\right) c^2 dt^2 + \left(1 - \frac{2GM}{c^2 r} + \frac{\alpha \ell_P^2}{r^2}\right)^{-1} dr^2 + r^2 d\Omega^2
\end{equation}

where $\alpha$ is a dimensionless parameter from LQG. The correction term $\alpha \ell_P^2/r^2$ prevents the singularity at $r = 0$ and creates a second horizon:

\begin{equation}
r_{\pm} = \frac{GM}{c^2} \pm \sqrt{\left(\frac{GM}{c^2}\right)^2 - \alpha \ell_P^2}
\end{equation}

The inner horizon $r_-$ is the white hole horizon. The bounce occurs at $r = r_-$.

### 6.4 Cosmological Implications

If every black hole transitions to a white hole, the universe contains a population of white holes with masses ranging from Planck mass to supermassive. The white hole explosion rate is:

\begin{equation}
\Gamma_{\text{WH}} \sim \frac{1}{t_{\text{Hawking}}(M)} \cdot n_{\text{BH}}(M)
\end{equation}

For $M \sim 10^{12}$ kg (primordial black holes), $t_{\text{Hawking}} \sim 10^{10}$ yr $\sim$ age of universe. These would be exploding now, producing GRBs. The non-observation of such explosions constrains the abundance of primordial black holes.

---

## 7. Constraints and Null Results

### 7.1 GRB Constraints

If white holes produce GRBs, the GRB luminosity function must match the white hole mass function. The GRB rate density is:

\begin{equation}
\rho_{\text{GRB}} \sim 10^{-8} \text{ Mpc}^{-3} \text{ yr}^{-1}
\end{equation}

The white hole model requires:

\begin{equation}
\rho_{\text{WH}} \sim \frac{\rho_{\text{GRB}}}{\tau_{\text{WH}}} \sim \frac{10^{-8} \text{ Mpc}^{-3} \text{ yr}^{-1}}{10^{-5} \text{ s}} \sim 10^{-3} \text{ Mpc}^{-3} \text{ s}^{-1}
\end{equation}

This is a very high rate, implying that white holes would be extremely common. The non-observation of a stochastic gravitational wave background from white hole explosions constrains the rate to:

\begin{equation}
\rho_{\text{WH}} < 10^{-6} \text{ Mpc}^{-3}
\end{equation}

which is in tension with the GRB rate if all GRBs are white hole explosions.

### 7.2 FRB Constraints

The repeating FRB 121102 has a repetition rate of $\sim 100$ bursts per year. If this is a white hole, the white hole must survive between bursts, requiring accretion. The required accretion rate is:

\begin{equation}
\dot{M} \sim \frac{E_{\text{burst}}}{c^2 \cdot T_{\text{repeat}}} \sim \frac{10^{40} \text{ J}}{(3 \times 10^8)^2 \cdot 3.15 \times 10^6 \text{ s}} \sim 10^7 \text{ kg/s}
\end{equation}

This is $\sim 10^{-8} M_\odot$ per year, which is plausible for a white hole in a dense environment. However, the energy budget of $\sim 10^{40}$ J per burst is $10^{22}$ times smaller than the white hole mass-energy, requiring extreme efficiency.

### 7.3 Cosmic Microwave Background Constraints

A population of exploding white holes would inject energy into the CMB, producing spectral distortions. The energy injection rate is:

\begin{equation}
\frac{dE}{dV dt} \sim \rho_{\text{WH}} \cdot \frac{Mc^2}{\tau_{\text{WH}}} \sim \rho_{\text{WH}} \cdot \frac{c^5}{2G}
\end{equation}

The COBE/FIRAS constraint on spectral distortions is:

\begin{equation}
\frac{dE}{dV dt} < 10^{-25} \text{ erg cm}^{-3} \text{ s}^{-1} \sim 10^{-31} \text{ J m}^{-3} \text{ s}^{-1}
\end{equation}

This gives:

\begin{equation}
\rho_{\text{WH}} < \frac{2G}{c^5} \times 10^{-31} \sim 10^{-53} \text{ m}^{-3}
\end{equation}

which is an extremely tight constraint, essentially ruling out any significant population of exploding white holes.

### 7.4 Gravitational Wave Constraints

The white hole explosion would produce a burst of gravitational waves. The characteristic strain is:

\begin{equation}
h \sim \frac{G}{c^4} \cdot \frac{E_{\text{GW}}}{d} \sim \frac{G}{c^4} \cdot \frac{\epsilon Mc^2}{d}
\end{equation}

where $\epsilon \sim 10^{-5}$ is the efficiency and $d$ is the distance. For a white hole at $d \sim 1$ Gpc:

\begin{equation}
h \sim \frac{6.674 \times 10^{-11}}{(3 \times 10^8)^4} \cdot \frac{10^{-5} \times 10^{12} \times (3 \times 10^8)^2}{3.086 \times 10^{25}} \sim 10^{-33}
\end{equation}

This is far below LIGO sensitivity ($h \sim 10^{-21}$). LISA would be sensitive to $h \sim 10^{-20}$, still far above the white hole signal.

### 7.5 Summary of Constraints

\begin{align}
\text{GRB rate:} \quad & \rho_{\text{WH}} \lesssim 10^{-3} \text{ Mpc}^{-3} \text{ (model-dependent)} \\
\text{CMB distortions:} \quad & \rho_{\text{WH}} \lesssim 10^{-53} \text{ m}^{-3} \text{ (very tight)} \\
\text{Gravitational waves:} \quad & \text{No detection, constraints weak} \\
\text{High-energy neutrinos:} \quad & \text{No detection, constraints weak}
\end{align}

The CMB constraint is the most stringent, essentially ruling out any cosmological population of exploding white holes. However, this constraint assumes the white holes are exploding \emph{now}. If all white holes exploded in the early universe, the constraint is evaded.

### 7.6 The Final Verdict

White holes are a legitimate solution of Einstein's equations, but they are:
\begin{enumerate}
\item \emph{Classically forbidden} by the second law of thermodynamics and cosmic censorship.
\item \emph{Quantum mechanically possible} but exponentially suppressed for macroscopic masses.
\item \emph{Observationally constrained} to be extremely rare or non-existent in the present universe.
\item \emph{Quantum gravity motivated} through the LQG black hole to white hole transition.
\end{enumerate}

The most promising avenue is the LQG Planck star scenario, where black holes transition to white holes on timescales $\sim (M/m_P)^{4/3} t_P$. For stellar-mass black holes, this is far longer than the age of the universe, but for primordial black holes of mass $\sim 10^{12}$ kg, the transition occurs now, producing observable explosions.

The search for white holes continues through multi-messenger observations of GRBs, FRBs, and high-energy neutrinos, as well as gravitational wave astronomy.

---

## Appendix A: Key Equations Summary

\begin{align}
\text{Schwarzschild radius:} \quad & r_s = \frac{2GM}{c^2} \\
\text{Surface gravity:} \quad & \kappa = \frac{c^4}{4GM} \\
\text{Hawking temperature:} \quad & T_H = \frac{\hbar c^3}{8\pi G M k_B} \\
\text{Bekenstein-Hawking entropy:} \quad & S = \frac{k_B c^3 A}{4G\hbar} = \frac{4\pi k_B G M^2}{\hbar c} \\
\text{Hawking evaporation time:} \quad & \tau_H = \frac{5120\pi G^2 M^3}{\hbar c^4} \\
\text{Kretschmann scalar:} \quad & R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma} = \frac{48 G^2 M^2}{c^4 r^6} \\
\text{White hole free-fall time:} \quad & \tau_{\text{ff}} = \frac{2}{3}\frac{r_s}{c} \\
\text{White hole instability time:} \quad & \tau_{\text{inst}} = \frac{2r_s}{c} = \frac{4GM}{c^3} \\
\text{LQG bounce time:} \quad & t_{\text{bounce}} \sim \left(\frac{M}{m_P}\right)^{4/3} t_P \\
\text{Planck star radius:} \quad & R \sim \left(\frac{M}{m_P}\right)^{1/3} \ell_P
\end{align}

## Appendix B: Useful Conversions

\begin{align}
1 M_\odot &= 1.989 \times 10^{30} \text{ kg} \\
r_s(M_\odot) &= 2.95 \text{ km} \\
\tau_{\text{ff}}(M_\odot) &= 1.05 \times 10^{-5} \text{ s} \\
\tau_H(M_\odot) &= 10^{67} \text{ yr} \\
\ell_P &= 1.616 \times 10^{-35} \text{ m} \\
t_P &= 5.391 \times 10^{-44} \text{ s} \\
m_P &= 2.176 \times 10^{-8} \text{ kg} \\
\rho_P &= 5.16 \times 10^{96} \text{ kg/m}^3
\end{align}

---

## References

1. Schwarzschild, K. (1916). "Über das Gravitationsfeld eines Massenpunktes nach der Einsteinschen Theorie." *Sitzungsberichte der Königlich Preussischen Akademie der Wissenschaften*, 189-196.
2. Kruskal, M. D. (1960). "Maximal Extension of Schwarzschild Metric." *Physical Review*, 119, 1743.
3. Szekeres, G. (1960). "On the Singularities of a Riemannian Manifold." *Publ. Math. Debrecen*, 7, 285.
4. Penrose, R. (1965). "Gravitational Collapse and Space-Time Singularities." *Physical Review Letters*, 14, 57.
5. Hawking, S. W. (1974). "Black Hole Explosions?" *Nature*, 248, 30.
6. Poisson, E. and Israel, W. (1990). "Internal Structure of Black Holes." *Physical Review D*, 41, 1796.
7. Rovelli, C. and Vidotto, F. (2014). "Planck Stars." *International Journal of Modern Physics D*, 23, 1442026.
8. Barcelo, C., Carballo-Rubio, R., and Garay, L. J. (2016). "Black holes turn white fast, otherwise stay black: no half measures." *Journal of High Energy Physics*, 2016, 157.
9. Haggard, H. M. and Rovelli, C. (2015). "Quantum-gravity effects outside the horizon spark black to white hole tunneling." *Physical Review D*, 92, 104020.
10. Christodoulou, M. and D'Ambrosio, F. (2024). "White holes as remnants: An exploding scenario." *Physical Review D*, 110, 064011.
