# Fisher Information Matrix for Gravitational Wave Parameter Estimation

## Derivatives of Waveform w.r.t. Masses/Spins, SNR Integrals, Covariance Matrix, Degeneracy Analysis for BH Binary Parameters

---

## 1. Introduction

The Fisher information matrix (FIM) provides a powerful analytical framework for estimating parameter uncertainties in gravitational wave (GW) observations. In the high signal-to-noise ratio (SNR) limit, the posterior distribution for signal parameters $\theta^i$ is well-approximated by a multivariate Gaussian with covariance matrix given by the inverse Fisher matrix. This document provides a complete derivation of the FIM for compact binary coalescence signals, including waveform derivatives, inner products, SNR integrals, and degeneracy analysis for black hole binary parameters.

---

## 2. GW Data Analysis Framework

### 2.1 Signal Model

The GW strain from a compact binary inspiral-merger-ringdown is:

$$
h(t; \theta) = h_+(t; \theta) F_+(\alpha, \delta, \psi) + h_\times(t; \theta) F_\times(\alpha, \delta, \psi)
$$

where $\theta = \{M_c, \eta, \chi_1, \chi_2, t_c, \phi_c, D_L, \alpha, \delta, \psi, \iota\}$ are the parameters, and $F_{+,\times}$ are antenna pattern functions.

In frequency domain (stationary phase approximation for inspiral):

$$
\tilde{h}(f; \theta) = \mathcal{A}(f; \theta) e^{i\Psi(f; \theta)}
$$

### 2.2 Noise Model

Detector noise is characterized by the one-sided power spectral density (PSD) $S_n(f)$:

$$
\langle \tilde{n}(f) \tilde{n}^*(f') \rangle = \frac{1}{2} \delta(f-f') S_n(f)
$$

### 2.3 Inner Product

The noise-weighted inner product between two signals $a, b$:

$$
\boxed{(a|b) = 4 \Re \int_{f_{\text{min}}}^{f_{\text{max}}} \frac{\tilde{a}(f) \tilde{b}^*(f)}{S_n(f)} df}
$$

Properties:
- Real and symmetric: $(a|b) = (b|a)$
- Positive definite: $(h|h) > 0$ for $h \ne 0$
- SNR: $\rho = \sqrt{(h|h)}$

---

## 3. Fisher Information Matrix

### 3.1 Definition

For a signal $h(\theta)$ with parameters $\theta^i$, the Fisher matrix is:

$$
\boxed{\Gamma_{ij} = \left( \frac{\partial h}{\partial \theta^i} \middle| \frac{\partial h}{\partial \theta^j} \right)}
$$

### 3.2 Gaussian Approximation

In the high-SNR limit, the likelihood is:

$$
\mathcal{L}(\theta) \propto \exp\left[-\frac{1}{2}(\Delta h | \Delta h)\right] \approx \exp\left[-\frac{1}{2}\Gamma_{ij} \Delta\theta^i \Delta\theta^j\right]
$$

where $\Delta h = h(\theta) - h(\hat{\theta})$ and $\Delta\theta^i = \theta^i - \hat{\theta}^i$.

### 3.3 Covariance Matrix

The parameter covariance matrix is the inverse Fisher matrix:

$$
\boxed{\Sigma^{ij} = (\Gamma^{-1})^{ij}}
$$

The 1-$\sigma$ uncertainty on parameter $\theta^i$:

$$
\sigma_{\theta^i} = \sqrt{\Sigma^{ii}}
$$

Correlation coefficient:

$$
\rho_{ij} = \frac{\Sigma^{ij}}{\sqrt{\Sigma^{ii}\Sigma^{jj}}}
$$

---

## 4. Waveform Derivatives

### 4.1 Frequency-Domain Waveform (SPA)

For non-precessing binaries in the inspiral regime (post-Newtonian):

$$
\tilde{h}(f) = \mathcal{A} f^{-7/6} e^{i\Psi(f)}
$$

Amplitude:

$$
\mathcal{A} = \frac{1}{D_L} \sqrt{\frac{5}{24}} \pi^{-2/3} \mathcal{M}_c^{5/6} \mathcal{F}(\iota, \psi)
$$

where $\mathcal{F}$ encodes antenna patterns and inclination.

Phase:

$$
\Psi(f) = 2\pi f t_c - \phi_c - \frac{\pi}{4} + \frac{3}{128}(\pi \mathcal{M}_c f)^{-5/3} \sum_{k=0}^N \psi_k (\pi \mathcal{M}_c f)^{k/3}
$$

### 4.2 Key Parameters

| Parameter | Symbol | Description |
|-----------|--------|-------------|
| Chirp mass | $\mathcal{M}_c = (m_1 m_2)^{3/5}/(m_1+m_2)^{1/5}$ | Dominant phase evolution |
| Symmetric mass ratio | $\eta = m_1 m_2/(m_1+m_2)^2$ | Sub-dominant phase |
| Effective spin | $\chi_{\text{eff}} = (m_1\chi_1 + m_2\chi_2)/M$ | Leading spin-orbit |
| Precessing spin | $\chi_p$ | Precession effects |
| Coalescence time | $t_c$ | Time of merger |
| Coalescence phase | $\phi_c$ | Phase at merger |
| Luminosity distance | $D_L$ | Amplitude scaling |
| Inclination | $\iota$ | Amplitude modulation |

### 4.3 Derivatives of the Waveform

Write $\tilde{h} = A e^{i\Psi}$ with $A = |\tilde{h}|$. Then:

$$
\frac{\partial \tilde{h}}{\partial \theta^i} = \left( \frac{\partial \ln A}{\partial \theta^i} + i \frac{\partial \Psi}{\partial \theta^i} \right) \tilde{h}
$$

The Fisher matrix becomes:

$$
\Gamma_{ij} = 4 \int \frac{|\tilde{h}|^2}{S_n} \left[ \frac{\partial \ln A}{\partial \theta^i} \frac{\partial \ln A}{\partial \theta^j} + \frac{\partial \Psi}{\partial \theta^i} \frac{\partial \Psi}{\partial \theta^j} \right] df
$$

The cross-term vanishes because it's purely imaginary and the integral takes the real part.

### 4.4 Explicit Phase Derivatives (Inspiral)

For the chirp mass $\mathcal{M}_c$:

$$
\frac{\partial \Psi}{\partial \mathcal{M}_c} = -\frac{5}{128} (\pi \mathcal{M}_c f)^{-8/3} \frac{1}{\mathcal{M}_c} \sum_k \psi_k \left(1 - \frac{5k}{3}\right) (\pi \mathcal{M}_c f)^{k/3}
$$

Leading order ($k=0$):

$$
\frac{\partial \Psi}{\partial \mathcal{M}_c} \approx -\frac{5}{128} (\pi \mathcal{M}_c f)^{-8/3} \frac{1}{\mathcal{M}_c}
$$

For symmetric mass ratio $\eta$:

$$
\frac{\partial \Psi}{\partial \eta} = \frac{3}{128} (\pi \mathcal{M}_c f)^{-5/3} \sum_k \frac{\partial \psi_k}{\partial \eta} (\pi \mathcal{M}_c f)^{k/3}
$$

For effective spin $\chi_{\text{eff}}$:

$$
\frac{\partial \Psi}{\partial \chi_{\text{eff}}} = \frac{3}{128} (\pi \mathcal{M}_c f)^{-5/3} \sum_k \frac{\partial \psi_k}{\partial \chi_{\text{eff}}} (\pi \mathcal{M}_c f)^{k/3}
$$

For $t_c$:

$$
\frac{\partial \Psi}{\partial t_c} = 2\pi f
$$

For $\phi_c$:

$$
\frac{\partial \Psi}{\partial \phi_c} = -1
$$

For $D_L$:

$$
\frac{\partial \ln A}{\partial D_L} = -\frac{1}{D_L}, \quad \frac{\partial \Psi}{\partial D_L} = 0
$$

For inclination $\iota$:

$$
\frac{\partial \ln A}{\partial \iota} = \frac{\partial \ln \mathcal{F}}{\partial \iota}
$$

---

## 5. SNR Integrals and Analytical Approximations

### 5.1 Power-Law Noise Approximation

For analytical insight, approximate $S_n(f) \propto f^\alpha$ over the sensitive band. For LIGO, $\alpha \approx -4$ at low frequencies, $\alpha \approx 0$ at mid-frequencies, $\alpha \approx 4$ at high frequencies.

Define the **moment integrals**:

$$
I_q = \int_{f_{\text{min}}}^{f_{\text{max}}} \frac{|\tilde{h}(f)|^2}{S_n(f)} f^q df
$$

For inspiral $|\tilde{h}|^2 \propto f^{-7/3}$:

$$
I_q \propto \int f^{-7/3 + q - \alpha} df
$$

### 5.2 Analytical Fisher Matrix (Restricted PN, Single Detector)

At leading PN order, the waveform depends on $\mathcal{M}_c, \eta, t_c, \phi_c, D_L$ (and angles). The Fisher matrix has block structure:

$$
\Gamma = \begin{pmatrix}
\Gamma_{\text{phase}} & 0 \\
0 & \Gamma_{\text{amp}}
\end{pmatrix}
$$

where $\Gamma_{\text{phase}}$ involves $\mathcal{M}_c, \eta, t_c, \phi_c$ and $\Gamma_{\text{amp}}$ involves $D_L, \iota, \psi, \alpha, \delta$.

#### Phase Parameter Submatrix

Using $\partial \Psi/\partial \mathcal{M}_c \propto f^{-8/3}$, $\partial \Psi/\partial \eta \propto f^{-2/3}$, $\partial \Psi/\partial t_c \propto f$, $\partial \Psi/\partial \phi_c = 1$:

$$
\Gamma_{ij}^{\text{phase}} = 4 \int \frac{|\tilde{h}|^2}{S_n} \frac{\partial \Psi}{\partial \theta^i} \frac{\partial \Psi}{\partial \theta^j} df
$$

With $|\tilde{h}|^2/S_n \propto f^{-7/3}$ (assuming flat noise for simplicity):

$$
\Gamma_{\mathcal{M}_c\mathcal{M}_c} \propto \int f^{-7/3} f^{-16/3} df = \int f^{-23/3} df \propto f_{\text{low}}^{-20/3}
$$

$$
\Gamma_{\eta\eta} \propto \int f^{-7/3} f^{-4/3} df = \int f^{-11/3} df \propto f_{\text{low}}^{-8/3}
$$

$$
\Gamma_{t_c t_c} \propto \int f^{-7/3} f^2 df = \int f^{-1/3} df \propto f_{\text{high}}^{2/3}
$$

$$
\Gamma_{\mathcal{M}_c \eta} \propto \int f^{-7/3} f^{-10/3} df = \int f^{-17/3} df \propto f_{\text{low}}^{-14/3}
$$

This shows:
- $\mathcal{M}_c$ is best measured (most negative power $\to$ dominated by low frequencies)
- $\eta$ is less well measured
- $t_c$ is measured from high frequencies

### 5.3 Mass Parameter Correlations

The chirp mass $\mathcal{M}_c$ and mass ratio $\eta$ are highly correlated. The correlation coefficient:

$$
\rho_{\mathcal{M}_c \eta} \approx 0.9 - 0.99
$$

This degeneracy arises because both parameters affect the phase evolution at similar PN orders.

**Reparameterization**: Use $\mathcal{M}_c$ and $\delta = \mathcal{M}_c \eta^{3/5}$ (or total mass $M$) to reduce correlations.

### 5.4 Spin Degeneracies

The effective spin $\chi_{\text{eff}}$ enters at 1.5PN order:

$$
\psi_3 \propto \chi_{\text{eff}}
$$

So $\partial \Psi/\partial \chi_{\text{eff}} \propto f^{-2/3}$, same frequency dependence as $\partial \Psi/\partial \eta$.

**Strong degeneracy**: $\chi_{\text{eff}}$ and $\eta$ are highly correlated ($\rho \sim 0.8-0.9$).

The precessing spin $\chi_p$ enters at higher PN orders and through amplitude modulation, breaking some degeneracies.

---

## 6. Complete Fisher Matrix for BH Binaries

### 6.1 Parameter Set

For a non-precessing binary, the intrinsic parameters are:

$$
\theta_{\text{int}} = \{\mathcal{M}_c, \eta, \chi_1, \chi_2\}
$$

or equivalently $\{\mathcal{M}_c, \eta, \chi_{\text{eff}}, \chi_p\}$.

Extrinsic parameters:

$$
\theta_{\text{ext}} = \{t_c, \phi_c, D_L, \iota, \psi, \alpha, \delta\}
$$

### 6.2 Full Fisher Matrix Expression

$$
\Gamma_{ij} = 4 \Re \int_{f_{\text{low}}}^{f_{\text{high}}} \frac{1}{S_n(f)} \frac{\partial \tilde{h}^*}{\partial \theta^i} \frac{\partial \tilde{h}}{\partial \theta^j} df
$$

For $\tilde{h} = A e^{i\Psi}$:

$$
\Gamma_{ij} = 4 \int \frac{A^2}{S_n} \left( \frac{\partial \ln A}{\partial \theta^i} \frac{\partial \ln A}{\partial \theta^j} + \frac{\partial \Psi}{\partial \theta^i} \frac{\partial \Psi}{\partial \theta^j} \right) df
$$

### 6.3 Amplitude Derivatives

The amplitude $A \propto D_L^{-1} \mathcal{M}_c^{5/6} f^{-7/6} \mathcal{F}(\iota, \psi, \alpha, \delta)$:

$$
\begin{aligned}
\frac{\partial \ln A}{\partial D_L} &= -\frac{1}{D_L} \\
\frac{\partial \ln A}{\partial \mathcal{M}_c} &= \frac{5}{6\mathcal{M}_c} \\
\frac{\partial \ln A}{\partial \iota} &= \frac{\mathcal{F}'(\iota)}{\mathcal{F}(\iota)} \\
\frac{\partial \ln A}{\partial \psi} &= \frac{\mathcal{F}'(\psi)}{\mathcal{F}(\psi)} \\
\frac{\partial \ln A}{\partial \alpha} &= \frac{\mathcal{F}'(\alpha)}{\mathcal{F}(\alpha)} \\
\frac{\partial \ln A}{\partial \delta} &= \frac{\mathcal{F}'(\delta)}{\mathcal{F}(\delta)}
\end{aligned}
$$

### 6.4 Phase Derivatives (Up to 3.5PN)

The phase $\Psi(f)$ in the SPA is:

$$
\Psi(f) = 2\pi f t_c - \phi_c - \frac{\pi}{4} + \frac{3}{128\eta}(\pi M f)^{-5/3} \sum_{k=0}^7 \psi_k (\pi M f)^{k/3}
$$

where $M = m_1 + m_2$ and $\mathcal{M}_c = \eta^{3/5}M$.

The PN coefficients $\psi_k$ depend on $\eta$, $\chi_{\text{eff}}$, $\chi_p$, and higher spin combinations.

Key derivatives:

$$
\begin{aligned}
\frac{\partial \Psi}{\partial t_c} &= 2\pi f \\
\frac{\partial \Psi}{\partial \phi_c} &= -1 \\
\frac{\partial \Psi}{\partial \mathcal{M}_c} &= -\frac{5}{128} \frac{1}{\mathcal{M}_c} (\pi \mathcal{M}_c f)^{-8/3} \left[1 + \sum_{k=2}^7 \left(1 - \frac{5k}{3}\right) \psi_k (\pi \mathcal{M}_c f)^{k/3} \right] \\
\frac{\partial \Psi}{\partial \eta} &= \frac{3}{128} (\pi M f)^{-5/3} \left[ -\frac{1}{\eta^2} \sum \psi_k (\pi M f)^{k/3} + \frac{1}{\eta} \sum \frac{\partial \psi_k}{\partial \eta} (\pi M f)^{k/3} + \frac{5}{3} \frac{M}{\mathcal{M}_c} \sum \psi_k (\pi M f)^{k/3} \right] \\
\frac{\partial \Psi}{\partial \chi_{\text{eff}}} &= \frac{3}{128} (\pi M f)^{-5/3} \frac{1}{\eta} \sum \frac{\partial \psi_k}{\partial \chi_{\text{eff}}} (\pi M f)^{k/3}
\end{aligned}
$$

---

## 7. Covariance Matrix and Error Estimation

### 7.1 Inversion and Parameter Errors

The covariance matrix:

$$
\Sigma = \Gamma^{-1}
$$

Marginalized error on parameter $\theta^i$:

$$
\sigma_i = \sqrt{\Sigma_{ii}}
$$

### 7.2 Sky Localization

Sky position $(\alpha, \delta)$ enters through:
- Time delays between detectors: $\Delta t \approx \frac{R_\oplus}{c} \sin\theta \cos(\phi - \phi_0)$
- Antenna pattern modulation

For a network of $N$ detectors, the timing information dominates:

$$
\Gamma_{\alpha\alpha} \approx \sum_{I<J} \frac{(2\pi f_0)^2 \rho_I^2 \rho_J^2}{\rho^2} \left(\frac{\partial \Delta t_{IJ}}{\partial \alpha}\right)^2
$$

where $f_0$ is the effective frequency. Sky area:

$$
\Delta \Omega \approx 2\pi \sqrt{\Sigma_{\alpha\alpha}\Sigma_{\delta\delta} - \Sigma_{\alpha\delta}^2}
$$

### 7.3 Distance-Inclination Degeneracy

The amplitude depends on $D_L$ and $\iota$ as:

$$
A \propto \frac{1}{D_L} \sqrt{F_+^2(1+\cos^2\iota)^2 + 4F_\times^2\cos^2\iota}
$$

For a single detector, $D_L$ and $\iota$ are perfectly degenerate (only the combination $D_L/\mathcal{F}(\iota)$ is measured). With multiple detectors, the degeneracy is broken by different antenna patterns.

---

## 8. Degeneracy Analysis for BH Binary Parameters

### 8.1 Mass-Spin Degeneracy

The phase evolution depends on combinations:

$$
\Psi \sim \frac{1}{\eta} \left[ \psi_0 + \psi_2 \eta + \psi_3 \chi_{\text{eff}} + \psi_4 \eta^2 + \cdots \right]
$$

At leading orders:
- $\psi_0 \propto 1$ (Newtonian)
- $\psi_2 \propto \eta$ (1PN)
- $\psi_3 \propto \chi_{\text{eff}}$ (1.5PN spin-orbit)
- $\psi_4 \propto \eta^2$ (2PN)

The **chirp mass** $\mathcal{M}_c$ determines the overall frequency scaling.
The **mass ratio** $\eta$ enters at 1PN and higher.
The **effective spin** $\chi_{\text{eff}}$ enters at 1.5PN.

**Degeneracy direction**: Increasing $\eta$ speeds up inspiral; increasing $\chi_{\text{eff}}$ (aligned) also speeds up inspiral. They are partially degenerate.

### 8.2 Quantitative Degeneracy Analysis

Define the **degeneracy matrix** $D_{ij} = \rho_{ij}$ (correlation matrix). Eigenvalues of $D$ show the number of well-constrained combinations.

For a typical BBH at SNR=20:
- 1 combination: $\mathcal{M}_c$ (measured to $\sim 0.1\%$)
- 1 combination: $t_c$ (measured to $\sim 10^{-4}$ s)
- 1 combination: $\mathcal{M}_c \eta^{3/5}$ (total mass)
- 1 combination: $\chi_{\text{eff}}$ (measured to $\sim 0.1$)
- Remaining combinations poorly constrained

### 8.3 Precession Breaks Degeneracies

For precessing binaries ($\chi_p \ne 0$), the amplitude and phase modulate at the precession frequency. This introduces new frequency dependencies that break the $\eta$-$\chi_{\text{eff}}$ degeneracy.

The precession frequency:

$$
\Omega_p \sim \frac{\chi_p}{M} \left(\frac{M}{r}\right)^{5/2}
$$

Modulation signatures in $h(t)$ provide independent information about $\chi_p$ and $\iota$.

### 8.4 Higher Modes

Higher harmonics ($\ell>2$ modes) break degeneracies because:
- Different mass/spin dependence
- Different angular dependence
- Different frequency scaling

For example, the $(3,3)$ mode scales as $\mathcal{M}_c^{5/6} f^{-7/6}$ but with different $\eta$ dependence.

---

## 9. Multi-Detector Fisher Matrix

### 9.1 Network Fisher Matrix

For $N$ detectors with uncorrelated noise:

$$
\Gamma_{ij}^{\text{net}} = \sum_{I=1}^N \Gamma_{ij}^{(I)}
$$

Each detector has its own antenna pattern $F_{+,\times}^{(I)}$ and PSD $S_n^{(I)}$.

### 9.2 Time Delay Information

The time delay between detectors $I$ and $J$:

$$
\Delta t_{IJ} = \frac{\mathbf{x}_I - \mathbf{x}_J}{c} \cdot \hat{\mathbf{n}}
$$

where $\hat{\mathbf{n}}$ is the sky direction. The phase shift:

$$
\Psi_I(f) = \Psi(f) + 2\pi f \Delta t_I
$$

This adds a term $\partial \Psi/\partial \alpha \propto f$ which significantly improves sky localization.

### 9.3 Network SNR

The network SNR:

$$
\rho_{\text{net}}^2 = \sum_I \rho_I^2
$$

Parameter errors scale as $1/\rho_{\text{net}}$.

---

## 10. Beyond Fisher: Limitations and Extensions

### 10.1 Fisher Matrix Limitations

1. **High-SNR approximation**: Breaks down at low SNR
2. **Gaussian posterior assumption**: Non-linearities cause non-Gaussianities
3. **Prior independence**: Fisher matrix assumes flat priors
4. **Single-mode assumption**: Ignores multi-modal posteriors

### 10.2 Higher-Order Corrections

The **Edgeworth expansion** includes skewness and kurtosis:

$$
p(\theta) \approx \mathcal{N}(\hat{\theta}, \Gamma^{-1}) \left[1 + \frac{1}{6} \kappa_{ijk} H^{ijk} + \cdots \right]
$$

where $\kappa_{ijk}$ are third cumulants and $H^{ijk}$ are Hermite polynomials.

### 10.3 Bayesian vs Fisher

The Fisher matrix is the expectation of the Hessian of the log-likelihood:

$$
\Gamma_{ij} = -\left\langle \frac{\partial^2 \ln \mathcal{L}}{\partial \theta^i \partial \theta^j} \right\rangle
$$

In the Bayesian framework with prior $\pi(\theta)$, the posterior covariance is:

$$
\Sigma_{\text{Bayes}}^{-1} = \Gamma + \Pi
$$

where $\Pi_{ij} = -\partial^2 \ln \pi / \partial \theta^i \partial \theta^j$ is the prior precision.

---

## 11. Practical Computation

### 11.1 Numerical Derivatives

For complex waveforms (IMRPhenom, SEOBNR), derivatives are computed numerically:

$$
\frac{\partial \tilde{h}}{\partial \theta^i} \approx \frac{\tilde{h}(\theta + \Delta\theta^i \hat{e}_i) - \tilde{h}(\theta - \Delta\theta^i \hat{e}_i)}{2\Delta\theta^i}
$$

Step size $\Delta\theta^i$ must be chosen carefully (too small: numerical noise; too large: truncation error).

### 11.2 Frequency Integration

The integral:

$$
\Gamma_{ij} = 4 \Re \int \frac{\partial \tilde{h}^*}{\partial \theta^i} \frac{\partial \tilde{h}}{\partial \theta^j} \frac{df}{S_n(f)}
$$

is computed using quadrature (e.g., Simpson's rule) on a logarithmic frequency grid.

### 11.3 Regularization

The Fisher matrix can be ill-conditioned. Regularization techniques:
- Eigenvalue truncation: discard modes with $\lambda < \epsilon \lambda_{\text{max}}$
- Tikhonov regularization: $\Gamma \to \Gamma + \epsilon I$
- SVD inversion

---

## 12. Example: GW150914-like Binary

### 12.1 Parameters

$m_1 = 36 M_\odot$, $m_2 = 29 M_\odot$, $\mathcal{M}_c = 28 M_\odot$, $\eta = 0.24$, $D_L = 400$ Mpc, SNR = 24.

### 12.2 Fisher Matrix Predictions (Order of Magnitude)

| Parameter | Fisher $\sigma$ | Notes |
|-----------|-----------------|-------|
| $\mathcal{M}_c$ | $\sim 0.1 M_\odot$ | Best measured |
| $M$ | $\sim 1 M_\odot$ | |
| $\eta$ | $\sim 0.02$ | Correlated with $\chi_{\text{eff}}$ |
| $\chi_{\text{eff}}$ | $\sim 0.1$ | Prior-dependent |
| $t_c$ | $\sim 10^{-4}$ s | |
| $D_L$ | $\sim 50$ Mpc | Degenerate with $\iota$ |
| $\iota$ | $\sim 0.3$ rad | |
| $\Delta \Omega$ | $\sim 100$ deg$^2$ | 2-detector network |

### 12.3 Comparison with Bayesian Inference

For GW150914, Bayesian PE gives:
- $\mathcal{M}_c = 28.1^{+0.5}_{-0.5} M_\odot$
- $\eta = 0.24^{+0.03}_{-0.02}$
- $\chi_{\text{eff}} = -0.07^{+0.17}_{-0.16}$

Fisher matrix underestimates uncertainties at low SNR and misses prior effects.

---

## 13. Advanced Topics

### 13.1 Fisher Matrix for Eccentric Binaries

Eccentricity $e_0$ enters at high PN orders and through harmonic structure. The Fisher matrix includes derivatives w.r.t. $e_0$ and mean anomaly $l_0$.

### 13.2 Fisher Matrix for Tidal Deformability

For neutron stars, the tidal deformability $\Lambda$ enters at 5PN order:

$$
\psi_{10} \propto -\frac{39}{2} \tilde{\Lambda}
$$

where $\tilde{\Lambda}$ is the mass-weighted tidal parameter.

The derivative $\partial \Psi/\partial \Lambda \propto f^{5/3}$ (high frequency).

### 13.3 Fisher Matrix for Modified Gravity

Parametrized post-Einsteinian (ppE) framework:

$$
\Psi(f) = \Psi_{\text{GR}}(f) + \beta u^b
$$

where $u = (\pi M f)^{1/3}$. Fisher matrix extended to $\{\beta, b\}$.

### 13.4 Fisher Matrix for Ringdown

For the ringdown signal (quasinormal modes):

$$
h(t) \propto e^{-t/\tau} \cos(2\pi f_0 t + \phi)
$$

Parameters: $\{f_0, \tau, A, \phi\}$. Fisher matrix computable analytically.

---

## 14. Summary of Key Formulas

### 14.1 Fisher Matrix Definition

$$
\boxed{\Gamma_{ij} = 4 \Re \int_{f_{\text{low}}}^{f_{\text{high}}} \frac{\partial \tilde{h}^*(f)}{\partial \theta^i} \frac{\partial \tilde{h}(f)}{\partial \theta^j} \frac{df}{S_n(f)}}
$$

### 14.2 Waveform Derivative

$$
\boxed{\frac{\partial \tilde{h}}{\partial \theta^i} = \left( \frac{\partial \ln A}{\partial \theta^i} + i \frac{\partial \Psi}{\partial \theta^i} \right) \tilde{h}}
$$

### 14.3 Covariance Matrix

$$
\boxed{\Sigma^{ij} = (\Gamma^{-1})^{ij}, \quad \sigma_i = \sqrt{\Sigma^{ii}}}
$$

### 14.4 SNR

$$
\boxed{\rho = \sqrt{(h|h)} = \sqrt{4 \int \frac{|\tilde{h}(f)|^2}{S_n(f)} df}}
$$

### 14.5 Degeneracy Directions (Leading Order)

$$
\boxed{
\begin{aligned}
\mathcal{M}_c &\text{: best constrained (low-freq dominated)} \\
t_c &\text{: best constrained (high-freq dominated)} \\
\eta, \chi_{\text{eff}} &\text{: strongly degenerate (same freq scaling)} \\
D_L, \iota &\text{: degenerate for single detector}
\end{aligned}
}
$$

---

## 15. Conclusion

The Fisher information matrix provides a fast, analytical tool for forecasting parameter estimation capabilities of GW detectors. While it has limitations (high-SNR, Gaussian approximation), it correctly captures the scaling of uncertainties with SNR, the parameter degeneracies inherent in the waveform structure, and the improvement from detector networks. For precision cosmology and tests of GR, the Fisher matrix remains the workhorse for detector design and data analysis planning.

---

*End of document. All derivations from first principles to final expressions.*