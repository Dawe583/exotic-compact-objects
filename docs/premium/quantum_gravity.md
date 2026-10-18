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

Use SI dimensions $[G]=mathrm{L^3M^{-1}T^{-2}}$, $[hbar]=mathrm{ML^2T^{-1}}$, and $[c]=mathrm{LT^{-1}}$. Seek a length $G^ahbar^b c^d$. Equating exponents to length gives

$$
3a+2b+d=1,qquad -a+b=0,qquad -2a-b-d=0.
$$

From the mass equation $b=a$. The time equation gives $d=-3a$, and the length equation becomes $2a=1$, hence $a=b=1/2$ and $d=-3/2$:

$$
ell_P=sqrt{rac{hbar G}{c^3}}.
$$

The associated time, mass, energy, and temperature are defined by

$$
t_P=rac{ell_P}{c}=sqrt{rac{hbar G}{c^5}},quad m_P=sqrt{rac{hbar c}{G}},quad E_P=m_Pc^2=sqrt{rac{hbar c^5}{G}},quad T_P=rac{E_P}{k_B}.
$$

These are combinations of constants, not measured particle properties. The conventions use the unreduced Planck mass; factors such as $8pi$ enter reduced-Planck conventions in field theory.

## Schwarzschild–Compton crossover (heuristic)

For a mass $m$, the Schwarzschild radius of a nonrotating classical black hole is $r_s=2Gm/c^2$. The reduced Compton wavelength is $arlambda_C=hbar/(mc)$. Equating the two,

$$
rac{2Gm}{c^2}=rac{hbar}{mc}
quadLongrightarrowquad
2Gm^2=hbar c
quadLongrightarrowquad
m=rac{m_P}{sqrt{2}},qquad r_s=arlambda_C=sqrt{2},ell_P.
$$

The conventional Planck scale is therefore the order-of-magnitude crossover, with order-unity differences depending on radius/wavelength conventions. This is a heuristic comparison of classical and quantum localization scales, not a derivation of a black-hole production threshold or evidence that a quantum black hole has been observed.

## Bekenstein–Hawking entropy and its dimensions

For a Schwarzschild horizon, $A=4pi r_s^2$. Substituting $r_s=2GM/c^2$ gives

$$
A=4pileft(rac{2GM}{c^2}ight)^2=rac{16pi G^2M^2}{c^4}.
$$

The semiclassical Bekenstein–Hawking entropy is

$$
S_{BH}=rac{k_B A}{4ell_P^2}.
$$

Since $ell_P^2=hbar G/c^3$, this is equivalently

$$
S_{BH}=rac{k_B A c^3}{4hbar G}
=rac{4pi k_B GM^2}{hbar c}.
$$

Dimensional interpretation: $[A]=mathrm{L^2}$ and $[ell_P^2]=mathrm{L^2}$, so $A/(4ell_P^2)$ is dimensionless and counts entropy in units of $k_B$; $S_{BH}$ has thermodynamic entropy units. The area law is a semiclassical result (with important quantum-gravity implications), not a direct count of experimentally resolved horizon microstates. Its microscopic interpretation depends on a candidate theory.

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

At characteristic energy $E$, a higher-derivative correction is generically suppressed by powers of $E/E_P$ (or an appropriate EFT cutoff), with coefficients set by Wilson coefficients and operator structure. The plot uses $epsilon^2=(E/E_P)^2$ as a **dimensional suppression illustration** with unit coefficient, not a prediction for a specific observable. Small $epsilon$ supports an expansion; near unity it signals breakdown of that expansion, not a numerical prediction for UV physics.

## Conditional phenomenology: Lorentz-violating photon dispersion

A frequently discussed model-dependent example modifies photon dispersion as $E^2simeq p^2c^2[1+eta(E/E_{QG})^n]$, with $|eta|(E/E_{QG})^nll1$. To leading order the fractional group-velocity shift is approximately $delta v/csimeq (n+1)eta(E/E_{QG})^n/2$ for this convention. A propagation-time difference over distance $L$ is then $Delta tsimeq -(n+1)eta L(E/E_{QG})^n/(2c)$ (sign depends on convention). The notebook plots this formula for explicitly chosen $eta,n,E_{QG},L$ and does **not** use an observed lag or claim a bound.

Actual constraints require a specified operator/model, source-intrinsic emission-lag treatment, redshift integration, instrumental response, and selection/systematic analysis. Liberati & Maccione review such model-dependent phenomenology ([arXiv:0906.0681](https://arxiv.org/abs/0906.0681)); this reference is not a blanket bound on quantum gravity. No direct detection of Lorentz-violating quantum-gravity dispersion is claimed here.

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
