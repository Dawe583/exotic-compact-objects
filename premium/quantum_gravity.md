# Quantum gravity: why it is needed, what is known, and what remains open

## Scope and evidence labels

This module distinguishes three levels that are often conflated:

- **Established empirical frameworks:** general relativity (GR) describes gravity macroscopically; quantum field theory (QFT) describes the other known interactions and quantum matter. Their tested domains overlap in situations such as quantum fields on curved backgrounds, but a complete quantum theory of spacetime has not been empirically confirmed.
- **Controlled low-energy theory:** quantizing perturbations of the metric gives a gravitational effective field theory (EFT). It is predictive order by order below its cutoff and is not a claim to solve the ultraviolet (UV) completion. This distinction is emphasized by Wallace (2022, [arXiv:2112.12235](https://arxiv.org/abs/2112.12235)).
- **Candidate UV approaches:** string theory, loop/canonical quantum gravity, asymptotic safety, and causal approaches each use different mathematical assumptions and have unresolved questions. None is an experimentally established complete theory.

Throughout, **measured input** means an experimentally determined constant or observational fact; **derived** means algebra from stated definitions; **illustration** means a model calculation with chosen parameters, not data. No plotted point in this module is a direct observation of quantum gravity.

## Why combine GR and QFT?

GR makes geometry dynamical: its metric responds to stress-energy. QFT normally assumes fields and causal structure on a spacetime background. At low curvature and low energy, matter QFT on a classical curved background is useful and has important consequences (including Hawking radiation as a robust semiclassical prediction), but quantized matter generically contributes quantum corrections to gravitational dynamics. Conversely, if gravity is to interact consistently with quantum matter, gravitational degrees of freedom must participate in a quantum description. The conflict is most acute when curvature/energy reaches the Planck scale or when semiclassical backreaction is essential, such as the early universe and black-hole evaporation. These motivations do not themselves establish that spacetime is discrete or select a unique theory.

## Planck scales: dimensional derivation

Use SI dimensions $[G]=\mathrm{L^3M^{-1}T^{-2}}$, $[\hbar]=\mathrm{ML^2T^{-1}}$, and $[c]=\mathrm{LT^{-1}}$. Seek a length $G^a\hbar^b c^d$. Equating exponents to length gives

$$
3a+2b+d=1,\qquad -a+b=0,\qquad -2a-b-d=0.
$$

From the mass equation $b=a$. The time equation gives $d=-3a$, and the length equation becomes $2a=1$, hence $a=b=1/2$ and $d=-3/2$:

$$
\ell_P=\sqrt{\frac{\hbar G}{c^3}}.
$$

The associated time, mass, energy, and temperature are defined by

$$
t_P=\frac{\ell_P}{c}=\sqrt{\frac{\hbar G}{c^5}},\quad m_P=\sqrt{\frac{\hbar c}{G}},\quad E_P=m_Pc^2=\sqrt{\frac{\hbar c^5}{G}},\quad T_P=\frac{E_P}{k_B}.
$$

These are combinations of constants, not measured particle properties. The conventions use the unreduced Planck mass; factors such as $8\pi$ enter reduced-Planck conventions in field theory.

## Schwarzschild–Compton crossover (heuristic)

For a mass $m$, the Schwarzschild radius of a nonrotating classical black hole is $r_s=2Gm/c^2$. The reduced Compton wavelength is $\bar{\lambda}_C=\hbar/(mc)$. Equating the two,

$$
\frac{2Gm}{c^2}=\frac{\hbar}{mc}
\quad\Longrightarrow\quad
2Gm^2=\hbar c
\quad\Longrightarrow\quad
m=\frac{m_P}{\sqrt{2}},\qquad r_s=\bar{\lambda}_C=\sqrt{2}\,\ell_P.
$$

The conventional Planck scale is therefore the order-of-magnitude crossover, with order-unity differences depending on radius/wavelength conventions. This is a heuristic comparison of classical and quantum localization scales, not a derivation of a black-hole production threshold or evidence that a quantum black hole has been observed.

## Bekenstein–Hawking entropy and its dimensions

For a Schwarzschild horizon, $A=4\pi r_s^2$. Substituting $r_s=2GM/c^2$ gives

$$
A=4\pi\left(\frac{2GM}{c^2}\right)^2=\frac{16\pi G^2M^2}{c^4}.
$$

The semiclassical Bekenstein–Hawking entropy is

$$
S_{BH}=\frac{k_B A}{4\ell_P^2}.
$$

Since $\ell_P^2=\hbar G/c^3$, this is equivalently

$$
S_{BH}=\frac{k_B A c^3}{4\hbar G}=\frac{4\pi k_B GM^2}{\hbar c}.
$$

Dimensional interpretation: $[A]=\mathrm{L^2}$ and $[\ell_P^2]=\mathrm{L^2}$, so $A/(4\ell_P^2)$ is dimensionless and counts entropy in units of $k_B$; $S_{BH}$ has thermodynamic entropy units. The area law is a semiclassical result (with important quantum-gravity implications), not a direct count of experimentally resolved horizon microstates. Its microscopic interpretation depends on a candidate theory.

## Approaches and what each does not establish

| Approach | Core framework / assumption | What is controlled or notable | Open questions; evidence status |
|---|---|---|---|
| Gravitational EFT | Expand about a low-energy background; include every local operator allowed by symmetries, ordered in derivatives/energy. | Low-energy quantum corrections can be calculated perturbatively; nonrenormalizability of Einstein gravity does not prevent EFT predictivity at fixed order. | EFT alone does not specify a UV completion; no direct measurement of its tiny quantum-gravity corrections is established. See Donoghue ([arXiv:gr-qc/9512024](https://arxiv.org/abs/gr-qc/9512024)); Wallace ([arXiv:2112.12235](https://arxiv.org/abs/2112.12235)). |
| Canonical / loop quantum gravity | Canonical quantization of GR variables; loop formulation uses holonomies/fluxes and background-independent kinematics. | Defines mathematically rich quantum-geometric states and discrete spectra for particular operators in standard constructions. | Recovering semiclassical spacetime and GR universally, dynamics, matter coupling, and unique observational signatures remain open; kinematical discreteness is not itself an observation. See Ashtekar & Bianchi ([arXiv:2104.04394](https://arxiv.org/abs/2104.04394)). |
| String theory | Extended strings and consistency conditions; perturbative formulations require specified backgrounds, with dualities and branes broadening the framework. | Provides UV-finite perturbative constructions in appropriate settings and black-hole microstate counting for selected systems. | No experimentally selected vacuum/low-energy spectrum; cosmological realization, nonperturbative formulation, and distinctive falsifiable signatures remain unresolved. Success in selected models is not empirical confirmation of our universe. See Polchinski, *String Theory*; overview [arXiv:hep-th/0002230](https://arxiv.org/abs/hep-th/0002230). |
| Asymptotic safety | Hypothesis that gravity's renormalization-group flow approaches a non-Gaussian UV fixed point with finitely many relevant directions. | Functional RG truncations provide evidence within approximations and motivate testable low-energy consequences. | Truncation/systematic-control issues, existence and universality of the full fixed point, and empirical discrimination remain open; it is a research program, not established UV completion. See Eichhorn ([arXiv:1810.07615](https://arxiv.org/abs/1810.07615)). |
| Causal dynamical triangulations (causal approach) | Define a path integral using causally restricted triangulated geometries and study continuum limits numerically. | Nonperturbative numerical evidence for extended four-dimensional geometry in studied regimes. | Continuum-limit control, matter/cosmology, relation to observed low-energy physics, and signatures remain active issues; numerical phase structure is not direct evidence of quantum spacetime. See Ambjørn, Görlich, Jurkiewicz & Loll ([arXiv:1203.3591](https://arxiv.org/abs/1203.3591)). |

These programs are not interchangeable versions of one agreed theory. EFT is a shared low-energy framework, while the remaining rows make distinct commitments and have differing degrees of mathematical development.

## EFT power counting: a controlled illustration

At characteristic energy $E$, a higher-derivative correction is generically suppressed by powers of $E/E_P$ (or an appropriate EFT cutoff), with coefficients set by Wilson coefficients and operator structure. The plot uses $\epsilon^2=(E/E_P)^2$ as a **dimensional suppression illustration** with unit coefficient, not a prediction for a specific observable. Small $\epsilon$ supports an expansion; near unity it signals breakdown of that expansion, not a numerical prediction for UV physics.

## Conditional phenomenology: Lorentz-violating photon dispersion

A frequently discussed model-dependent example modifies photon dispersion as

$$
E^2\simeq p^2c^2\left[1+\eta\left(\frac{E}{E_{QG}}\right)^n\right],\qquad |\eta|\left(\frac{E}{E_{QG}}\right)^n\ll1.
$$

Here $\eta$ is a dimensionless model parameter, $n$ is a positive integer, and $E_{QG}$ is a model scale; none is a measured parameter in the illustration. Different dispersion operators need not give the same coefficient or energy dependence.

For the stated convention, set $x=E/E_{QG}$ and rewrite the dispersion relation to first order as

$$
p(E)=\frac{E}{c}\left(1+\eta x^n\right)^{-1/2}\simeq\frac{E}{c}\left(1-\frac{\eta}{2}x^n\right).
$$

Differentiate this approximate momentum with respect to energy:

$$
\frac{dp}{dE}\simeq\frac{1}{c}\left[1-\frac{n+1}{2}\eta x^n\right].
$$

The group velocity is $v_g=dE/dp=(dp/dE)^{-1}$, so expanding the reciprocal to first order gives

$$
\frac{v_g}{c}\simeq 1+\frac{n+1}{2}\eta\left(\frac{E}{E_{QG}}\right)^n,
\qquad \frac{\delta v}{c}\simeq\frac{n+1}{2}\eta\left(\frac{E}{E_{QG}}\right)^n.
$$

For a constant energy along a flat-space path of length $L$, the first-order travel-time difference is

$$
\Delta t\simeq\frac{L}{v_g}-\frac{L}{c}\simeq-\frac{n+1}{2}\eta\frac{L}{c}\left(\frac{E}{E_{QG}}\right)^n.
$$

The sign depends on the convention and sign of $\eta$. This is the leading-order result; it assumes small $|\eta|x^n$, a specified dispersion relation, and neglects expansion/redshift evolution. The notebook plots this formula for explicitly chosen $\eta,n,E_{QG},L$ and does **not** use an observed lag or claim a bound.

Actual constraints require a specified operator/model, source-intrinsic emission-lag treatment, redshift integration, instrumental response, and selection/systematic analysis. Liberati & Maccione review such model-dependent phenomenology ([arXiv:0906.0681](https://arxiv.org/abs/0906.0681)); this reference is not a blanket bound on quantum gravity. No direct detection of Lorentz-violating quantum-gravity dispersion is claimed here.

## Quantitative observational constraints

These are constraints on specific phenomenological signatures, not detections of quantum gravity:

- **GRB 090510:** Fermi detected a $31\,\mathrm{GeV}$ photon during the first second from a burst at $z=0.903\pm0.003$. Using the one-sigma conservative photon-energy and redshift values ($28.0\,\mathrm{GeV}$ and $z=0.900$), the authors' most conservative emission-start choice gives $E_{QG,1}/E_P>1.19$ for a **linear** energy-dependent photon-propagation model. Less conservative emission-time choices give stronger limits, but depend more heavily on associating the high-energy photon with lower-energy emission. This does not constrain all quantum-gravity models; the source's intrinsic emission time is a central assumption ([Fermi LAT/GBM Collaboration, *Nature* 462, 331 (2009)](https://arxiv.org/abs/0908.1832)).
- **GW170817 / GRB 170817A:** the measured gamma-ray delay was $(1.74\pm0.05)\,\mathrm{s}$. The published interval for the relative gravitational-wave and light propagation speeds is $-3\times10^{-15}<(v_g-v_\gamma)/c<7\times10^{-16}$. This tests relative propagation in that event, with interpretation conditional on the source-emission timing; it is not a direct measurement of Planck-scale spacetime structure ([LIGO Scientific Collaboration et al., *Phys. Rev. Lett.* 119, 161101 (2017)](https://arxiv.org/abs/1710.05834)).

The notebook now reconstructs the conservative GRB bound from the paper's event inputs, numerically integrates the cosmological propagation kernel, checks the quadrature with an independent trapezoidal calculation, and compares the result with the authors' value. It also recomputes the same event under Planck18 parameters; that value is a cosmology-sensitivity check, not a replacement for the published result.
 
For linear energy-dependent propagation in a flat expanding cosmology, with the source-frame photon energy redshifting along the path,

$$
\Delta t_{\rm LIV}\simeq\frac{\Delta E_{\rm obs}}{E_{QG,1}H_0}\mathbin{\cdot}
\int_0^z\frac{1+z'}{\sqrt{\Omega_m(1+z')^3+\Omega_\Lambda}}\,dz',
\qquad
E_{QG,1}\geq\frac{\Delta E_{\rm obs}}{\Delta t_{\max}H_0}\mathbin{\cdot}
\int_0^z\frac{1+z'}{\sqrt{\Omega_m(1+z')^3+\Omega_\Lambda}}\,dz'.
$$

Using the source paper's flat cosmology ($H_0=71\,\mathrm{km\,s^{-1}\,Mpc^{-1}}$, $\Omega_m=0.27$, $\Omega_\Lambda=0.73$), conservative energy/redshift inputs ($28.0\,\mathrm{GeV}$, $z=0.900$), $\Delta t_{\max}=0.859\,\mathrm{s}$, and a $0.1\,\mathrm{MeV}$ reference photon, the notebook recovers $E_{QG,1}/E_P\simeq1.190$, consistent with the published $>1.19$. Replacing only the cosmology with Astropy Planck18 gives approximately $1.217$; the difference illustrates model/cosmology dependence rather than a more precise measurement. The detected $31\,\mathrm{GeV}$ photon itself has $E/E_P\simeq2.54\times10^{-18}$; a quadratic EFT-size estimate would be $\sim6.45\times10^{-36}$ only for a unit Wilson coefficient and should not be mistaken for a universal correction.

| Fermi Table 2 case | Timing assumption or method | Published timing input | Conditional linear bound |
|---|---|---:|---:|
| (a) | Any onset of emission below $1\,\mathrm{MeV}$ | $\Delta t<859\,\mathrm{ms}$ | $E_{QG,1}/E_P>1.19$ |
| (b) | Main emission below $1\,\mathrm{MeV}$ | $\Delta t<299\,\mathrm{ms}$ | $E_{QG,1}/E_P>3.42$ |
| (c) | Main emission above $0.1\,\mathrm{GeV}$ | $\Delta t<181\,\mathrm{ms}$ | $E_{QG,1}/E_P>5.63$ |
| (d) | Onset above $1\,\mathrm{GeV}$ | $\Delta t<99\,\mathrm{ms}$ | $E_{QG,1}/E_P>10.0$ |
| (e) | Associate the high-energy photon with a contemporaneous low-energy spike | $\Delta t<10\,\mathrm{ms}$ | $E_{QG,1}/E_P>102$ |
| (f) | Associate a $0.75\,\mathrm{GeV}$ photon with the first spike; opposite-sign delay | $\Delta t<19\,\mathrm{ms}$ | $E_{QG,1}/E_P>1.33$ |
| (g) | Dispersion of high-energy spikes, not one assigned lag | $|\Delta t/\Delta E|<30\,\mathrm{ms\,GeV^{-1}}$ at $99\%$ | $E_{QG,1}/E_P>1.22$ |

Cases (a)–(g) are alternative analyses of one burst and are correlated, not seven independent constraints. The strongest limits depend most on the assignment of intrinsic emission times. The sensitivity plot retains those assumptions separately instead of pooling them.

## Observational status and unsolved questions

Gravitational waves, black-hole shadow images, precision tests of GR, and cosmological observations test classical/semiclassical gravitational models in their regimes. They do not resolve Planck-scale spacetime structure. No complete quantum theory of gravity has a uniquely confirmed empirical prediction. Potential tests are difficult because the natural suppression scale is extreme and proposed signatures are often model-dependent and degenerate with source physics or conventional astrophysics. Central unsolved problems include a controlled UV completion (or proof one is unnecessary), recovery of classical spacetime, quantum black-hole information and microstates, singularity resolution, and distinctive, robust, falsifiable observables.

## References

1. J. F. Donoghue, “General relativity as an effective field theory: The leading quantum corrections,” *Phys. Rev. D* **50**, 3874 (1994), [arXiv:gr-qc/9512024](https://arxiv.org/abs/gr-qc/9512024).
2. D. Wallace, “Quantum Gravity at Low Energies,” *Stud. Hist. Philos. Sci. B* **89**, 1 (2022), [arXiv:2112.12235](https://arxiv.org/abs/2112.12235).
3. A. Ashtekar and E. Bianchi, “A short review of loop quantum gravity,” *Rep. Prog. Phys.* **84**, 042001 (2021), [arXiv:2104.04394](https://arxiv.org/abs/2104.04394).
4. J. Polchinski, “String theory,” [arXiv:hep-th/0002230](https://arxiv.org/abs/hep-th/0002230).
5. A. Eichhorn, “Status of the asymptotic safety paradigm for quantum gravity,” [arXiv:1810.07615](https://arxiv.org/abs/1810.07615).
6. J. Ambjørn et al., “Quantum gravity as the sum over spacetimes,” [arXiv:1203.3591](https://arxiv.org/abs/1203.3591).
7. S. Liberati and L. Maccione, “Quantum gravity phenomenology: achievements and challenges,” *J. Phys. Conf. Ser.* **314**, 012007 (2011), [arXiv:0906.0681](https://arxiv.org/abs/0906.0681).
8. CODATA/NIST constants via Astropy's constants package, [Astropy constants documentation](https://docs.astropy.org/en/stable/constants/index.html); fundamental SI constants are defined exactly where applicable, while $G$ has measurement uncertainty.
