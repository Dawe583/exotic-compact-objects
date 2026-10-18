# Reissner-Nordström Black Hole: Complete Theoretical Derivation

## 1. Einstein-Maxwell Action and Field Equations

The Reissner-Nordström solution describes a static, spherically symmetric black hole with mass $M$ and electric charge $Q$. We begin with the Einstein-Maxwell action:

\begin{equation}
S = \int d^4x \sqrt{-g} \left[ \frac{1}{16\pi G} R - \frac{1}{4} F_{\mu\nu} F^{\mu\nu} \right]
\end{equation}

where $F_{\mu\nu} = \partial_\mu A_\nu - \partial_\nu A_\mu$ is the electromagnetic field tensor. Varying with respect to $g^{\mu\nu}$ and $A_\mu$ yields the coupled field equations:

\begin{align}
G_{\mu\nu} &= 8\pi G T_{\mu\nu}^{\text{(EM)}} \\
\nabla_\mu F^{\mu\nu} &= 0
\end{align}

with the electromagnetic stress-energy tensor:

\begin{equation}
T_{\mu\nu}^{\text{(EM)}} = \frac{1}{4\pi} \left( F_{\mu\alpha} F_\nu^{\;\alpha} - \frac{1}{4} g_{\mu\nu} F_{\alpha\beta} F^{\alpha\beta} \right)
\end{equation}

---

## 2. Spherically Symmetric Ansatz

For a static, spherically symmetric spacetime, the metric takes the form:

\begin{equation}
ds^2 = -f(r) dt^2 + \frac{dr^2}{f(r)} + r^2 d\Omega^2
\end{equation}

where $d\Omega^2 = d\theta^2 + \sin^2\theta d\phi^2$. The electromagnetic potential for a purely electric charge is:

\begin{equation}
A_\mu dx^\mu = -\Phi(r) dt, \quad \Phi(r) = \frac{Q}{r}
\end{equation}

The non-zero components of $F_{\mu\nu}$ are:

\begin{equation}
F_{tr} = -F_{rt} = \partial_r \Phi = -\frac{Q}{r^2}
\end{equation}

The invariant $F_{\mu\nu}F^{\mu\nu}$ evaluates to:

\begin{equation}
F_{\mu\nu}F^{\mu\nu} = 2 F_{tr}F^{tr} = -\frac{2Q^2}{r^4}
\end{equation}

---

## 3. Einstein Equations for the Metric Function

The non-zero components of the Einstein tensor for the ansatz (4) are:

\begin{align}
G_{tt} &= \frac{f}{r^2} \frac{d}{dr}\left[ r(1-f) \right] \\
G_{rr} &= -\frac{1}{r^2 f} \frac{d}{dr}\left[ r(1-f) \right] \\
G_{\theta\theta} &= \frac{r^2}{2} f'' + r f' \\
G_{\phi\phi} &= \sin^2\theta \, G_{\theta\theta}
\end{align}

The electromagnetic stress-energy components are:

\begin{align}
T_{tt}^{\text{(EM)}} &= \frac{Q^2}{8\pi r^4} f \\
T_{rr}^{\text{(EM)}} &= -\frac{Q^2}{8\pi r^4 f} \\
T_{\theta\theta}^{\text{(EM)}} &= -\frac{Q^2}{8\pi r^2} \\
T_{\phi\phi}^{\text{(EM)}} &= \sin^2\theta \, T_{\theta\theta}^{\text{(EM)}}
\end{align}

The $tt$ (or $rr$) Einstein equation gives:

\begin{equation}
\frac{1}{r^2} \frac{d}{dr}\left[ r(1-f) \right] = \frac{G Q^2}{r^4}
\end{equation}

Integrating once:

\begin{equation}
r(1-f) = 2GM - \frac{G Q^2}{r}
\end{equation}

Solving for $f(r)$:

\begin{equation}
\boxed{f(r) = 1 - \frac{2GM}{r} + \frac{G Q^2}{r^2}}
\end{equation}

This is the **Reissner-Nordström metric function**.

---

## 4. Horizon Structure

Horizons occur where $f(r) = 0$:

\begin{equation}
r^2 - 2GM r + G Q^2 = 0
\end{equation}

The roots are:

\begin{equation}
r_\pm = GM \pm \sqrt{G^2 M^2 - G Q^2}
\end{equation}

\begin{itemize}
\item $r_+$: **Event horizon** (outer horizon)
\item $r_-$: **Cauchy horizon** (inner horizon)
\end{itemize}

---

### 4.1 Three Regimes

\begin{align}
\textbf{Subextremal:} &\quad G M^2 > Q^2 \quad (r_+ > r_-) \\
\textbf{Extremal:} &\quad G M^2 = Q^2 \quad (r_+ = r_- = GM) \\
\textbf{Superextremal:} &\quad G M^2 < Q^2 \quad (\text{naked singularity, no horizon})
\end{align}

The **cosmic censorship conjecture** forbids the superextremal case.

---

## 5. Extremal Limit and Near-Horizon Geometry

In the extremal limit $Q^2 = G M^2$, the two horizons coincide:

\begin{equation}
r_+ = r_- = r_e = GM
\end{equation}

Define near-horizon coordinates:

\begin{equation}
r = r_e + \lambda \rho, \quad t = \frac{\tau}{\lambda}, \quad \lambda \to 0
\end{equation}

The metric becomes:

\begin{equation}
ds^2 = \frac{\rho^2}{r_e^2} d\tau^2 - \frac{r_e^2}{\rho^2} d\rho^2 - r_e^2 d\Omega^2
\end{equation}

This is $\text{AdS}_2 \times S^2$ with radii $r_e$ for both factors.

---

## 6. Surface Gravity and Hawking Temperature

The surface gravity is defined by:

\begin{equation}
\kappa = \frac{1}{2} \left. \frac{df}{dr} \right|_{r=r_+}
\end{equation}

Computing:

\begin{equation}
\frac{df}{dr} = \frac{2GM}{r^2} - \frac{2GQ^2}{r^3}
\end{equation}

Evaluating at $r_+$:

\begin{equation}
\kappa = \frac{GM}{r_+^2} - \frac{GQ^2}{r_+^3} = \frac{r_+ - r_-}{2r_+^2}
\end{equation}

Using $r_+ r_- = G Q^2$ and $r_+ + r_- = 2GM$:

\begin{equation}
\boxed{\kappa = \frac{\sqrt{G^2 M^2 - G Q^2}}{r_+^2} = \frac{r_+ - r_-}{2r_+^2}}
\end{equation}

The Hawking temperature is:

\begin{equation}
\boxed{T_H = \frac{\kappa}{2\pi} = \frac{r_+ - r_-}{4\pi r_+^2} = \frac{\sqrt{G^2 M^2 - G Q^2}}{2\pi r_+^2}}
\end{equation}

---

## 7. Black Hole Entropy

The Bekenstein-Hawking entropy is one-quarter the horizon area in Planck units:

\begin{equation}
S = \frac{A_+}{4G} = \frac{4\pi r_+^2}{4G} = \frac{\pi r_+^2}{G}
\end{equation}

In terms of $M$ and $Q$:

\begin{equation}
\boxed{S = \pi \left( GM + \sqrt{G^2 M^2 - G Q^2} \right)^2 / G}
\end{equation}

---

## 8. Thermodynamics: First Law and Smarr Formula

The first law of black hole mechanics for RN black holes:

\begin{equation}
\boxed{dM = \frac{\kappa}{8\pi G} dA + \Phi_+ dQ}
\end{equation}

where $\Phi_+ = Q/r_+$ is the electric potential at the horizon.

\begin{proof}
Vary $M = \frac{r_+}{2G} + \frac{Q^2}{2r_+}$ (from $f(r_+)=0$):

\begin{align}
dM &= \frac{dr_+}{2G} + \frac{Q}{r_+} dQ - \frac{Q^2}{2r_+^2} dr_+ \\
&= \left( \frac{1}{2G} - \frac{Q^2}{2r_+^2} \right) dr_+ + \frac{Q}{r_+} dQ \\
&= \frac{r_+^2 - G Q^2}{2G r_+^2} dr_+ + \Phi_+ dQ \\
&= \frac{r_+ - r_-}{4G r_+^2} (8\pi r_+ dr_+) + \Phi_+ dQ \\
&= \frac{\kappa}{2\pi} \frac{dA}{8\pi G} + \Phi_+ dQ \quad \text{(using } dA = 8\pi r_+ dr_+) \\
&= T_H dS + \Phi_+ dQ
\end{align}
\end{proof}

The **Smarr formula** (from scaling arguments):

\begin{equation}
\boxed{M = \frac{\kappa A}{4\pi G} + \Phi_+ Q = 2 T_H S + \Phi_+ Q}
\end{equation}

---

## 9. Thermodynamic Potentials

### 9.1 Helmholtz Free Energy (Canonical Ensemble, Fixed $Q$)

\begin{equation}
F(T, Q) = M - T_H S
\end{equation}

Using $M = \frac{r_+}{2G} + \frac{Q^2}{2r_+}$ and $T_H = \frac{r_+ - r_-}{4\pi r_+^2}$, $S = \frac{\pi r_+^2}{G}$:

\begin{align}
F &= \frac{r_+}{2G} + \frac{Q^2}{2r_+} - \frac{r_+ - r_-}{4\pi r_+^2} \cdot \frac{\pi r_+^2}{G} \\
&= \frac{r_+}{2G} + \frac{Q^2}{2r_+} - \frac{r_+ - r_-}{4G} \\
&= \frac{r_+ + r_-}{4G} + \frac{Q^2}{2r_+} \\
&= \frac{GM}{2G} + \frac{Q^2}{2r_+} = \frac{M}{2} + \frac{Q^2}{2r_+}
\end{align}

### 9.2 Gibbs Free Energy (Grand Canonical Ensemble, Fixed $\Phi$)

\begin{equation}
G(T, \Phi) = M - T_H S - \Phi Q
\end{equation}

Using $\Phi = Q/r_+$ and the Smarr formula:

\begin{equation}
G = M - \left( \frac{M}{2} - \frac{\Phi Q}{2} \right) - \Phi Q = \frac{M}{2} - \frac{\Phi Q}{2}
\end{equation}

---

## 10. Heat Capacity and Phase Transitions

The heat capacity at constant charge:

\begin{equation}
C_Q = T_H \left( \frac{\partial S}{\partial T_H} \right)_Q
\end{equation}

Compute $\partial S / \partial r_+ = 2\pi r_+/G$ and $\partial T_H / \partial r_+$:

\begin{equation}
T_H = \frac{1}{4\pi} \left( \frac{1}{r_+} - \frac{G Q^2}{r_+^3} \right)
\end{equation}

\begin{equation}
\frac{\partial T_H}{\partial r_+} = \frac{1}{4\pi} \left( -\frac{1}{r_+^2} + \frac{3G Q^2}{r_+^4} \right) = \frac{3G Q^2 - r_+^2}{4\pi r_+^4}
\end{equation}

Thus:

\begin{equation}
C_Q = T_H \frac{2\pi r_+/G}{(3G Q^2 - r_+^2)/(4\pi r_+^4)} = \frac{2\pi r_+^2}{G} \frac{r_+^2 - G Q^2}{3G Q^2 - r_+^2}
\end{equation}

Using $r_+^2 - G Q^2 = r_+(r_+ - r_-)$:

\begin{equation}
\boxed{C_Q = \frac{2\pi r_+^2}{G} \frac{r_+(r_+ - r_-)}{3G Q^2 - r_+^2}}
\end{equation}

$C_Q$ diverges at $r_+^2 = 3G Q^2$, signaling a **Davies phase transition**. For $r_+^2 < 3G Q^2$, $C_Q < 0$ (thermodynamically unstable); for $r_+^2 > 3G Q^2$, $C_Q > 0$ (stable).

---

## 11. Schwinger Pair Production and Black Hole Discharge

A charged black hole can discharge via Schwinger pair production in its electric field. The electric field near the horizon:

\begin{equation}
E = \frac{Q}{r_+^2}
\end{equation}

The Schwinger pair production rate per unit volume for electrons/positrons:

\begin{equation}
\Gamma = \frac{(eE)^2}{4\pi^3} \sum_{n=1}^\infty \frac{1}{n^2} \exp\left( -\frac{n\pi m_e^2}{eE} \right)
\end{equation}

For $eE \ll m_e^2$, the leading term dominates:

\begin{equation}
\Gamma \approx \frac{e^2 E^2}{4\pi^3} \exp\left( -\frac{\pi m_e^2}{eE} \right)
\end{equation}

The discharge rate:

\begin{equation}
\frac{dQ}{dt} = -e \int \Gamma \, dV
\end{equation}

Near the horizon, integrate over a shell of thickness $\sim 1/E$:

\begin{equation}
\frac{dQ}{dt} \sim -e \cdot \frac{e^2 E^2}{4\pi^3} \cdot 4\pi r_+^2 \cdot \frac{1}{E} \exp\left( -\frac{\pi m_e^2}{eE} \right)
\end{equation}

\begin{equation}
\frac{dQ}{dt} \sim -\frac{e^3 E r_+^2}{\pi^2} \exp\left( -\frac{\pi m_e^2 r_+^2}{e Q} \right)
\end{equation}

Substituting $E = Q/r_+^2$:

\begin{equation}
\boxed{\frac{dQ}{dt} \sim -\frac{e^3 Q}{\pi^2 r_+^2} \exp\left( -\frac{\pi m_e^2 r_+^2}{e Q} \right)}
\end{equation}

---

## 12. Discharge Timescale

For a near-extremal black hole, $r_+ \approx GM \approx Q/\sqrt{G}$. The exponent becomes:

\begin{equation}
\frac{\pi m_e^2 r_+^2}{e Q} \approx \frac{\pi m_e^2 Q}{e \sqrt{G}} = \pi \frac{m_e^2}{e} \frac{Q}{\sqrt{G}}
\end{equation}

In Planck units ($G = 1$), for a solar mass black hole $M \sim 10^{38}$, $Q \sim 10^{38}$:

\begin{equation}
\frac{\pi m_e^2 Q}{e} \sim \pi \times (10^{-22})^2 \times 10^{38} / 10^{-1} \sim 10^{-6} \ll 1
\end{equation}

The exponential suppression is negligible; discharge is rapid. For smaller $Q$, the exponent grows and discharge slows.

---

## 13. Euclidean Action and Partition Function

The Euclidean RN metric (with $t \to -i\tau$):

\begin{equation}
ds_E^2 = f(r) d\tau^2 + \frac{dr^2}{f(r)} + r^2 d\Omega^2
\end{equation}

Regularity at $r_+$ requires $\tau \sim \tau + \beta$ with $\beta = 2\pi/\kappa = 1/T_H$.

The Euclidean action:

\begin{equation}
I_E = -\frac{1}{16\pi G} \int d^4x \sqrt{g} R + \frac{1}{4} \int d^4x \sqrt{g} F_{\mu\nu}F^{\mu\nu} + \text{boundary terms}
\end{equation}

For RN, the bulk action vanishes on-shell ($R = 0$ for Einstein-Maxwell). The boundary term at infinity gives:

\begin{equation}
I_E = \beta M - \frac{A_+}{4G} - \beta \Phi_+ Q
\end{equation}

The partition function $Z = e^{-I_E}$ yields the thermodynamic potentials.

---

## 14. Dual CFT Description (Kerr/CFT Analogue)

For near-extremal RN, the near-horizon $\text{AdS}_2 \times S^2$ suggests a dual 1D CFT. The central charge:

\begin{equation}
c = \frac{3 r_e^2}{G} = 12 \pi G M^2
\end{equation}

The Frolov-Thorne temperature:

\begin{equation}
T_L = \frac{r_+^2}{2\pi (r_+ - r_-)}
\end{equation}

Cardy formula reproduces the entropy:

\begin{equation}
S = \frac{\pi^2}{3} c T_L = \frac{\pi^2}{3} \cdot \frac{3 r_+^2}{G} \cdot \frac{r_+^2}{2\pi (r_+ - r_-)} \cdot \frac{r_+ - r_-}{r_+^2} = \frac{\pi r_+^2}{G}
\end{equation}

---

## 15. Perturbative Stability

### 15.1 Gravitational Perturbations

The Regge-Wheeler equation for axial perturbations:

\begin{equation}
\frac{d^2 \Psi}{dr_*^2} + \left[ \omega^2 - V_{\text{RW}}(r) \right] \Psi = 0
\end{equation}

where $dr_* = dr/f(r)$ and

\begin{equation}
V_{\text{RW}}(r) = f(r) \left[ \frac{\ell(\ell+1)}{r^2} - \frac{6GM}{r^3} + \frac{4GQ^2}{r^4} \right]
\end{equation}

### 15.2 Electromagnetic Perturbations

Coupled to gravitational perturbations via the Zerilli equation. The system is stable for $Q^2 < G M^2$.

---

## 16. Geodesics and Particle Motion

### 16.1 Effective Potential for Timelike Geodesics

For a particle of mass $\mu$ and charge $q$:

\begin{equation}
\frac{1}{2} \dot{r}^2 + V_{\text{eff}}(r) = \frac{E^2}{2}
\end{equation}

\begin{equation}
V_{\text{eff}}(r) = \frac{f(r)}{2} \left( 1 + \frac{L^2}{r^2} \right) - \frac{qQ}{r}
\end{equation}

### 16.2 Innermost Stable Circular Orbit (ISCO)

Solve $V_{\text{eff}}' = V_{\text{eff}}'' = 0$. For neutral particles ($q=0$):

\begin{equation}
r_{\text{ISCO}} = \frac{GM}{2} \left[ 3 + \sqrt{9 - 8\frac{Q^2}{GM^2}} \right]
\end{equation}

---

## 17. Summary of Key Formulas

\begin{center}
\begin{tabular}{|l|l|}
\hline
\textbf{Quantity} & \textbf{Expression} \\
\hline
Metric function $f(r)$ & $1 - \frac{2GM}{r} + \frac{GQ^2}{r^2}$ \\
Horizons $r_\pm$ & $GM \pm \sqrt{G^2M^2 - GQ^2}$ \\
Surface gravity $\kappa$ & $\frac{r_+ - r_-}{2r_+^2}$ \\
Temperature $T_H$ & $\frac{r_+ - r_-}{4\pi r_+^2}$ \\
Entropy $S$ & $\pi r_+^2/G$ \\
Electric potential $\Phi_+$ & $Q/r_+$ \\
First law & $dM = T_H dS + \Phi_+ dQ$ \\
Smarr formula & $M = 2T_H S + \Phi_+ Q$ \\
Heat capacity $C_Q$ & $\frac{2\pi r_+^2}{G} \frac{r_+(r_+-r_-)}{3GQ^2 - r_+^2}$ \\
Extremal limit & $Q^2 = GM^2$, $r_+ = r_- = GM$ \\
\hline
\end{tabular}
\end{center}

---

## 18. Appendix: Derivation of Smarr Formula from Scaling

The RN solution is characterized by two parameters $(M, Q)$. Under scaling $r \to \lambda r$, $t \to \lambda t$:

\begin{itemize}
\item $M \to \lambda M$
\item $Q \to \lambda Q$
\item $A \to \lambda^2 A$
\item $\kappa \to \lambda^{-1} \kappa$
\item $\Phi \to \lambda^{-1} \Phi$
\end{itemize}

Euler's theorem for homogeneous functions: $M(\lambda A, \lambda Q) = \lambda M(A, Q)$. Differentiate w.r.t. $\lambda$ at $\lambda=1$:

\begin{equation}
M = \left( \frac{\partial M}{\partial A} \right)_Q A + \left( \frac{\partial M}{\partial Q} \right)_A Q
\end{equation}

From the first law $dM = \frac{\kappa}{8\pi G} dA + \Phi dQ$, we identify:

\begin{equation}
\frac{\partial M}{\partial A} = \frac{\kappa}{8\pi G}, \quad \frac{\partial M}{\partial Q} = \Phi
\end{equation}

Thus:

\begin{equation}
M = \frac{\kappa A}{8\pi G} + \Phi Q = 2 T_H S + \Phi Q
\end{equation}

---

## 19. References

\begin{enumerate}
\item Reissner, H. (1916). \"Über die Eigengravitation des elektrischen Feldes nach der Einsteinschen Theorie.\" \textit{Annalen der Physik}, 355(9), 106–120.
\item Nordström, G. (1918). \"On the Energy of the Gravitational Field in Einstein's Theory.\" \textit{Proceedings of the Royal Dutch Academy of Sciences}, 20, 1238–1245.
\item Hawking, S. W. (1975). \"Particle Creation by Black Holes.\" \textit{Communications in Mathematical Physics}, 43(3), 199–220.
\item Davies, P. C. W. (1978). \"Thermodynamic Phase Transitions of Kerr-Newman Black Holes.\" \textit{Proceedings of the Royal Society A}, 358(1695), 441–454.
\item Schwinger, J. (1951). \"On Gauge Invariance and Vacuum Polarization.\" \textit{Physical Review}, 82(5), 664–679.
\end{enumerate}