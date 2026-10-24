# Early supermassive black-hole growth: observations, timescales, and seed constraints

**Scope.** This section accompanies [`notebooks/23_early_smbh_growth.ipynb`](../notebooks/23_early_smbh_growth.ipynb), a reproducible analysis of a deliberately selected—not complete or statistically representative—set of high-redshift black-hole observations. It includes luminous quasars, JWST spectroscopic AGN, the Chandra/JWST X-ray source UHZ1, and resolved gas-dynamical modelling of Abell 2744-QSO1. The notebook calculates Planck-2018 cosmic ages, checks the growth algebra symbolically and numerically, samples explicit conditional growth scenarios, and generates cosmic-time, growth-track, seed-feasibility, Eddington-ratio, seed-sensitivity, and nearby reverberation-mass context plots.

## Uncertainty propagation and local method-comparison data

Quoted mass measurement summaries and assumed astrophysical growth scenarios are propagated as distinct quantities. For J0313$-$1806, the notebook samples a positive-truncated normal mass distribution centered on the reported $1.6\times10^9\,M_\odot$ with standard deviation $0.4\times10^9\,M_\odot$. For CEERS_1019 it samples $\log_{10}(M_{\rm BH}/M_\odot)\sim\mathcal{N}(6.95,0.37^2)$, matching the quoted log-mass uncertainty. These are transparent approximations to quoted summaries, not source-published posterior samples. They omit method-calibration, luminosity, and other correlated systematics; GN-z11's quoted $\pm0.3$ dex and UHZ1's luminosity/Eddington-dependent estimate are retained in the ledger but not given invented statistical distributions.

For each target, the seeded generator uses $30{,}000$ independent scenario draws at fixed $z_f=20$ with $\epsilon\sim U(0.057,0.2)$, $f_{\rm duty}\sim U(0.3,1)$, and $\lambda\sim U(0.3,3)$. The numerical generator seed is $20261019$. Uniform ranges and independence are design choices for a sensitivity exercise—not observational priors, measured distributions, or posterior probabilities. The plotted empirical cumulative distribution and fractions below reference seed masses are conditional only on these ranges, fixed formation redshift, constant-average exponential-growth model, and adopted measurement-summary approximations. They do not establish a probability for any seed channel.

The notebook independently compares inverse growth with a direct exponential calculation, forwards the required seed back to the target mass, and checks an analytic boundary identity: for a specified seed $M_s$, the equality boundary obeys

$$f_{\rm duty}\lambda=\frac{t_0\,\epsilon}{(1-\epsilon)\Delta t}\ln\!\left(\frac{M_{\rm obs}}{M_s}\right),\qquad t_0=\frac{\sigma_Tc}{4\pi Gm_p}.$$

The additional local-data plot reads `data/processed/agn_reverberation_masses.csv`, retaining the distinct `logmass_lower_error_dex` and `logmass_upper_error_dex` columns. The file is a literature compilation of 86 nearby/low-redshift AGN from `agn_bh_mass.csv`, as recorded in [`data/DATA_INVENTORY.md`](../data/DATA_INVENTORY.md); it is not an early-universe sample. Reverberation mapping estimates masses using broad-line response delays and line velocities. It is method-comparison/context data only, and should not be equated with high-redshift single-epoch virial scaling, luminosity/Eddington-inferred mass, or resolved gas kinematics. The selected $z<1$ plotting subset does not correct for compilation selection or missing masses and has no early-universe inference.

The uncertainty CDF and local reverberation plot complement the original scenario heat maps, but neither resolves selection effects or method-dependent systematics. The inventory explicitly identifies several other generated/synthetic catalogs; none is treated as observational evidence here.

## Evidence ledger and interpretation

These measurements do not all have the same meaning or evidential strength. J0313−1806 at spectroscopic redshift $z=7.6423\pm0.0013$ is a luminous quasar with a published Mg II virial estimate $M_{\rm BH}=(1.6\pm0.4)\times10^9\,M_\odot$ and $L_{\rm bol}/L_{\rm Edd}=0.67\pm0.14$. CEERS_1019 at $z=8.679$ has a broad-H$\beta$ AGN signature and single-epoch virial estimate $\log_{10}(M_{\rm BH}/M_\odot)=6.95\pm0.37$, with reported Eddington ratio $1.2\pm0.5$. GN-z11 at $z=10.603$ shows JWST/NIRSpec high-ionization lines and very dense gas consistent with an AGN; the reported local-virial mass is $\log_{10}(M_{\rm BH}/M_\odot)=6.2\pm0.3$, with approximately five-times-Eddington accretion (uncertainty about a factor of two). Its authors note that if local virial relations fail, an Eddington-luminosity estimate instead gives roughly $10^7\,M_\odot$.

UHZ1 at $z\approx10.1$ is a Chandra X-ray/JWST AGN candidate with inferred bolometric luminosity around $5\times10^{45}\,\mathrm{erg\,s^{-1}}$. The often cited black-hole mass near $4\times10^7\,M_\odot$ assumes Eddington luminosity; it is not a dynamical mass, and X-ray obscuration/column-density uncertainty leaves a broad interpretation. Abell 2744-QSO1 at spectroscopic $z=7.04$ is an important methodological advance: resolved gas kinematics have been used for direct dynamical modelling. The paper reports a simple, inclination-unconstrained rotation fit of $\log_{10}(M_{\rm BH}/M_\odot)=6.75\pm0.15$ as a lower bound and an inclination-corrected MOKA3D fit of $7.7\pm0.3$, together with Eddington ratio around $0.02$. The latter depends strongly on inclination/deprojection and the adopted model; this should not be silently equated with a virial mass or treated as assumption-free. The authors discuss nuclear-cluster and primordial-black-hole alternatives as well as a black-hole interpretation.

The notebook preserves quoted uncertainties and methods in a pandas observation table, rather than pooling incomparable masses. It deliberately does not populate a long catalog with uncertain values. Luminosity-selected quasars, JWST survey sources, lensed sources, and X-ray-selected systems have distinct selection functions; obscuration, magnification, transient activity, line detectability, and virial calibration all affect the observed sample. No population abundance inference is attempted.

## Derivation and model readout

For fully ionized hydrogen, Thomson scattering transfers outward force $F_{\rm rad}=\sigma_T L/(4\pi r^2c)$ to an electron–proton pair, while gravity exerts $F_g=GMm_p/r^2$. At balance, $F_{\rm rad}=F_g$; cancelling the common inverse-square factor gives $L_{\rm Edd}=4\pi GMm_pc/\sigma_T$, approximately $1.26\times10^{38}(M/M_\odot)\,\mathrm{erg\,s^{-1}}$. This idealized spherical limit depends on opacity and composition.

Define radiative efficiency $\epsilon=L/(\dot M_{\rm in}c^2)$, Eddington ratio $\lambda=L/L_{\rm Edd}$, and duty fraction $f_{\rm duty}$. The retained black-hole mass rate is $\dot M=(1-\epsilon)\dot M_{\rm in}$. Substitution of $\dot M_{\rm in}=L/(\epsilon c^2)$ and the Eddington luminosity gives

$$\frac{dM}{dt}=\frac{1-\epsilon}{\epsilon}f_{\rm duty}\lambda\frac{4\pi Gm_p}{\sigma_Tc}M.$$

For constant parameters this is $dM/M=dt/t_{\rm ef}$. Integrating between $M_0,t_0$ and $M,t$ gives $\ln(M/M_0)=(t-t_0)/t_{\rm ef}$, hence $M=M_0\exp[(t-t_0)/t_{\rm ef}]$. The e-folding time used here explicitly includes the retained-mass factor:

$$t_{\rm ef}=\frac{\epsilon}{1-\epsilon}\frac{\sigma_Tc}{4\pi Gm_p}\frac{1}{f_{\rm duty}\lambda}.$$

With pure-hydrogen Thomson opacity and $\epsilon=0.1$, continuous Eddington-limited accretion yields approximately $50\,\mathrm{Myr}$ per e-fold. Definitions that omit the $(1-\epsilon)$ correction quote a slightly different “Salpeter time”; the notebook makes this convention explicit and checks the expression using Astropy constants and SymPy.

For seed formation redshift $z_f$ and observation redshift $z_o$, the available time is $\Delta t=t(z_o)-t(z_f)$, where ages are computed with Astropy's `Planck18` flat $\Lambda$CDM realization ($H_0=67.66\,\mathrm{km\,s^{-1}\,Mpc^{-1}}$, $\Omega_m=0.30966$, $\Omega_\Lambda=0.68885$, $T_{\rm CMB}=2.7255\,\mathrm{K}$, and $N_{\rm eff}=3.046$). Radiation and neutrinos mean $\Omega_\Lambda\ne1-\Omega_m$ exactly. Inverting the exponential solution yields $M_{\rm seed,req}=M_{\rm obs}\exp[-\Delta t/t_{\rm ef}]$. The scenario grid explicitly varies seed mass ($10$–$10^6\,M_\odot$), formation redshift ($15$–$30$), efficiency ($0.057$–$0.3$), duty cycle ($0.1$–$1$), and Eddington ratio ($0.3$–$5$). These are exploratory parameter values, not observational priors or claims that a source sustained a specific history.

The notebook’s visualizations show how distinct seed masses and effective accretion histories can arrive at similar endpoints, and how an inferred required seed changes over the duty-cycle/Eddington-ratio plane. Each feasibility boundary is conditional on the chosen target mass, formation time, efficiency, and constant-average growth prescription. Crossing a reference seed scale does not demonstrate a particular formation mechanism or viable gas supply. Mergers, episodic super-Eddington phases, changing spin and efficiency, feedback, and duty-cycle variation are not explicitly modelled.

## Why no unique seed channel follows

A final mass and observation epoch constrain the integrated growth budget, not the seed alone. Earlier formation, a more massive seed, higher time-averaged Eddington ratio, higher duty cycle, lower radiative efficiency, and merger growth can compensate one another. The observations also retain large method-dependent uncertainties: local virial calibrations may not apply at very high redshift; broad lines can have host/outflow contributions; UHZ1’s X-ray mass interpretation depends on uncertain obscuration and bolometric correction; lensing and inclination matter for relevant targets; and AGN luminosity is variable. Consequently neither the luminous-quasar masses nor the JWST/X-ray AGN detections establish one unique origin. Population III remnants with rapid growth, direct-collapse heavy seeds, nuclear-cluster pathways, primordial black holes, and combinations remain possibilities to be tested against larger, better characterized samples and more robust dynamical constraints.

## Sources

- Planck Collaboration (2020), *Planck 2018 results VI: Cosmological parameters*, A&A 641, A6. [https://doi.org/10.1051/0004-6361/201833910](https://doi.org/10.1051/0004-6361/201833910).
- Astropy `Planck18` realization and parameter values: [Astropy cosmology documentation](https://docs.astropy.org/en/stable/api/astropy.cosmology.realizations.Planck18.html).
- Larson et al. (2023), *A CEERS Discovery of an Accreting Supermassive Black Hole 570 Myr after the Big Bang*, ApJL 953, L29. [arXiv:2303.08918](https://arxiv.org/abs/2303.08918); [DOI](https://doi.org/10.3847/2041-8213/ace619).
- Maiolino et al. (2024), *A small and vigorous black hole in the early Universe*, Nature 627, 59–63. [https://doi.org/10.1038/s41586-024-07052-5](https://doi.org/10.1038/s41586-024-07052-5).
- Natarajan et al. (2023), *First Detection of an Over-Massive Black Hole Galaxy UHZ1*, ApJL 958, L20. [arXiv:2308.02654](https://arxiv.org/abs/2308.02654).
- Wang et al. (2021), *A Luminous Quasar at Redshift 7.642*, ApJL 907, L1. [https://doi.org/10.3847/2041-8213/abd8c6](https://doi.org/10.3847/2041-8213/abd8c6); [arXiv:2101.03179](https://arxiv.org/abs/2101.03179).
- Juodžbalis et al. (2026), resolved dynamical black-hole mass in Abell 2744-QSO1, Nature 653, 1017–1021. [https://doi.org/10.1038/s41586-026-10579-4](https://doi.org/10.1038/s41586-026-10579-4).

## Data provenance

See `docs/DATA_PROVENANCE.md` (workspace root) for the real/derived/synthetic classification of every dataset used here.
