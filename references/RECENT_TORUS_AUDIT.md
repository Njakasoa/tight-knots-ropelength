# Recent torus-link and filament audit

**Scope.** Primary-source audit completed 12 September 2026 (papers available by that cutoff). The central papers are Klotz–Thompson (2025) on concentric helical units and Klotz (2026) on \(T(Q,Q)\). “Ropelength” below means centerline length for a tube of radius \(a=1\); consequently every no-overlap distance is \(d\ge2\), and every length, radius, and height scales linearly with \(a\). Thus a result \(L\) in the papers becomes \(aL\) for thickness/radius \(a\), with \(R\mapsto aR\), \(H\mapsto aH\), and the constraint \(d\ge2a\). This removes the common diameter/radius ambiguity.

## 1. Primary papers and status

| Source | What it actually establishes | Status |
|---|---|---|
| Alexander R. Klotz and Finn Thompson, “Ropelength-minimizing concentric helices and non-alternating torus knots,” *Proceedings of the Royal Society A* **481** (2321), article 20250319 (2025), [publisher DOI](https://doi.org/10.1098/rspa.2025.0319), [arXiv full text](https://arxiv.org/html/2504.00861) | Exact cylindrical-helix constraint and optimum for one shell; finite-(Q) shell searches; asymptotic (7.82869Q^{3/2}) multihelix construction; closure estimates for (T(3Q,Q)). | Peer-reviewed article. The arXiv HTML is useful for equations and appendix; use the published DOI as the bibliographic record. |
| Alexander R. Klotz, “Tight Bounds for Tight Links: Ropelength of \(T(Q,Q)\) torus links,” *Journal of Physics A: Mathematical and Theoretical* **59** (2026), 285201, [published DOI](https://doi.org/10.1088/1751-8121/ae862e), [arXiv record](https://arxiv.org/abs/2603.02416), [v2 full text](https://arxiv.org/html/2603.02416v2), [PDF](https://arxiv.org/pdf/2603.02416) | Wegner/Groemer convex-hull lower bound; zero-parameter toroidal constructions (13.38, \(C^{3/4}\)); conditional maximum-occupancy construction (11.68, \(C^{3/4}\)); low-\(Q\) planar/toroidal numerical constructions. | Peer-reviewed publication (2026); v2 is the inspected arXiv version. The 11.68 asymptotic remains explicitly conditional on an unproved full transcendental no-overlap claim. |
| Amit Dawadi, Animesh Biswas, Julien Chopin, and Arshad Kudrolli, “Bundling architecture in elastic filaments with applied twist,” *Physical Review E* **112**, 015416 (2025), [DOI](https://doi.org/10.1103/d782-cbmc), [arXiv record/full-text links](https://arxiv.org/abs/2501.04650) | X-ray/optical observations and neo-Hookean model for real silicone multifilament bundles: contact, radial instability, migration, and torque. | Peer-reviewed physical-filament study; not a ropelength minimization theorem. |
| Shiheng Yan *et al.*, “Rigidity Criteria for Chainmail Consisting of Tessellations of Torus Knots,” *Physical Review Letters* **135**, 088201 (2025), [author PDF](https://www.daraio.caltech.edu/publications/202508_Yan.pdf), [DOI](https://doi.org/10.1103/8w3q-4x8m) | 3-D printed torus-knot particles and tessellated chainmail; modified Maxwell and crease-line criteria. | Peer-reviewed physical realization of torus-knot particles, but it studies rigid-body fabrics rather than thick-link ropelength. |

Shell downloads were attempted with `curl` into `tight-knots-lab/papers/`; this environment could not resolve `arxiv.org` (DNS failure), so no local PDF was obtained. The linked primary HTML/PDF/DOI records are the reproducible source locations.

## 2. Klotz–Thompson 2025: exact construction data

### One cylindrical (N)-helix

For (N) equally spaced helices, indexed (i=0,ldots,N-1), one pitch is

\[
x_i(\theta)=R\cos\left(\theta+\frac{2\pi i}{N}\right),\quad
y_i(\theta)=R\sin\left(\theta+\frac{2\pi i}{N}\right),\quad
z_i(\theta)=\frac{H\theta}{2\pi},\qquad 0\le\theta\le2\pi.
\]

The length of one helix is

\[
L_h=\sqrt{H^2+(2\pi R)^2}.
\]

The paper uses a unit-radius tube, hence the centerline no-overlap threshold (d\ge2). For the closest pair of adjacent helices, the phase offset (phi_N) is the negative real solution of

\[
2-2\cos\left(\phi_N+\frac{2\pi}{N}\right)=\phi_N^2,
\qquad -\frac{2\pi}{N}\le \phi_N\le0.
\]

The corresponding single-shell optimum is

\[
R_o=2\sqrt{\frac{1}{\phi_N^2-\phi_N\sin(\phi_N+2\pi/N)}},
\]
\[
H_o=4\pi\sqrt{\frac{\sin(\phi_N+2\pi/N)}{\phi_N^2\sin(\phi_N+2\pi/N)-\phi_N^3}}.
\]

For large \(N\), the Taylor reduction \(\phi_N\simeq\pi/N\) gives

\[
R_o\simeq\frac{\sqrt2}{\pi}N,\qquad H_o\simeq\sqrt{8}\,N,
\qquad L_o\simeq4N^2.
\]

The circumference (2\pi R_o) and height (H_o) are equal asymptotically, and the pitch angle is (45^\circ). The approximation is already within about 1% for (N\ge4), but the authors say to use the exact (phi_N)-based values for specific coordinates.

### Concentric shells and finite optimization

With a central straight rod and shell occupancies (M_1,ldots,M_T), (Q=1+\sum_iM_i), the model places shell (i) at

\[
R_i=R+2(i-1),
\]

and uses a common height (H), because all top and bottom endpoints are level. The length is

\[
L=H+\sum_{i=1}^T M_i\sqrt{H^2+\left(2\pi[R+2(i-1)]\right)^2}.
\]

The central rod contributes (H). The paper’s finite-(Q) searches impose (2\le R\le4), (H\ge2\max_iM_i), and a numerical adjacent-helix distance check (500 vertices per sampled helix). They enumerate all (2^{N-1}) compositions only up to (N=20), then restrict the shell count heuristically. For (N=12), the best reported arrangement is (1!-!4!-!5!-!2), with (L=292.92); the best arrangement notation includes the central rod.

The authors report optimized finite cases through 39 total components. Selected ideal arrangements are (1!-!4!-!5!-!2) for (Q=12), (1!-!5!-!7!-!8!-!5) for (Q=26), and (1!-!5!-!8!-!9!-!9!-!7) for (Q=39). These are numerical upper-bound constructions, not proofs of global ropelength optimality.

### Asymptotic multihelix formulas

The paper considers three increasingly efficient constructions. A constant increment (k\ge5) puts (k,2k,\ldots,kT) helices on shells at their ideal radii, with the outer shell setting (H). Its large-(T) length and crossing scaling are

\[
L_\alpha\simeq1.72,k^2T^3,qquad Q\simeq\frac{k}{2}T^2,qquad
\frac{L_\alpha}{C}\ge\frac{10.89}{\sqrt Q}
\]

where (C\simeq Q^2) per repeated pitch. The inequality is minimized at (k=5), since a radial shell gap of at least 2 is required.

For (T) equal shells of (N_s) helices each, separated radially by 2, the authors derive

\[
\frac{L_\beta}{C}<\frac{2\pi T}{Q}+\frac4T,
\]

optimized at (T=\sqrt{2Q/\pi}), hence (L_\beta/C<4\sqrt{2\pi/Q}\simeq10.03/\sqrt Q). Using ideal inner-shell radius/height gives (L_\gamma\simeq9.34Q^{3/2}). “Infilling” the empty inner region by shells with (4i) helices at radius (2i) moves approximately

\[
N_{int}\simeq\frac{Q}{2\pi}
\]

helices inward, changing the length by (Delta L\simeq-1.5Q^{3/2}). The resulting asymptotic length is

\[
L_\delta=7.82869\,Q^{3/2}=\frac{7.82869}{\sqrt Q}C.
\]

The reported exact prefactor is the integral expression in [Eq. (24 of the full text](https://arxiv.org/html/2504.00861v1#S9.E24)); the decimal is (7.82869), not an independently proved global optimum. Reverse-Jenga (remove an outer helix and insert it into the first inner shell that remains non-overlapping) lowers numerical examples further, but it is an algorithmic heuristic with discrete distance checks.

### Closure into torus links

Repeating the unit (p) times and bending its axis into a circle gives a (T(pQ,Q)) link with (Q) components. The torus parameterization used in the later paper is equivalent to the 2025 construction. Before the safety offset, the major radius is

\[
R_M=\frac{pH}{2\pi}.
\]

The inner extrema approach after bending. The 2025 paper’s sufficient repair is to increase the major radius by the outer minor radius (r_o); for an ideal outer shell (r_o=H/(2\pi)), this changes (R_M) by a factor ((p+1)/p). The crossing number is

\[
C=pQ(Q-1).
\]

Applying the conservative (k=5) incremental length gives

\[
\frac{L}{C^{3/4}}\simeq10.89,p^{1/4}\frac{p+1}{p},
\]

whose minimum is at (p=3), approximately 19.11. This estimate overstates the cost because outer shells are underconstrained and do not all scale linearly with the major radius. The optimized finite example (1!-!5!-!7!-!6) closes as (T(57,19)) with reported ratio 11.54; the (T(2163,721)) construction has 1,557,360 crossings and ratio 12.06. Ridgerunner rescaled a (T(48,16)) discretization by only 0.09–0.30% depending on vertex count, which is numerical evidence of clearance, not a continuous proof.

## 3. Klotz 2026: (T(Q,Q)), close packing, and toroidal formulas

### Lower bound and its hypotheses

In (T(pQ,Q)), each component has total linking number (p(Q-1)). The elementary isoperimetric bound is

\[
L_{T(pQ,Q)}>2\pi Q\left(1+\sqrt{p(Q-1)}\right)
\simeq2\pi\sqrt p\,Q^{3/2}.
\]

For a convex hull (W(N)) around (N) unit disks, the paper uses the Wegner/Groemer inequality

\[
W(N)\ge\sqrt{4\pi\left(\sqrt{12}(N-1)+(2-\sqrt3)\left\lceil\sqrt{12N-3}-3\right\rceil+\pi\right)}.
\]

After the (2\pi) push-off and multiplication by (Q), the bound is

\[
L_{T(pQ,Q)}\ge Q\left[2\pi+\sqrt{4\pi\left(\sqrt{12}(p(Q-1)-1)+(2-\sqrt3)\left\lceil\sqrt{12p(Q-1)-3}-3\right\rceil+\pi\right)}\right].
\]

For (p=1), its large-(Q) coefficient is

\[
\alpha_w>\sqrt{8\pi\sqrt3}+\frac{2\pi+\sqrt{2\pi(7\sqrt3-12)}}{\sqrt Q}
\simeq6.60+\frac{7.17}{\sqrt Q}.
\]

The symbolic correction above is the expansion of the exact bound in Eq. (6) after dropping the ceiling term as in the paper’s Eq. (8). The paper prints the decimal \(7.61\) beside that expression; direct evaluation of the printed symbolic expression gives \(2\pi+\sqrt{2\pi(7\sqrt3-12)}=7.1671\ldots\), so the decimal is a source inconsistency and should not be reproduced as an independently derived constant.

This uses close-packed disks with packing fraction (sigma=\pi/\sqrt{12}). The author warns that the Wegner bound may not be attained for finite (N), that numerical hull values are often about 5% larger, and—crucially—that the cone-puncture hypothesis in the Cantarella et al. theorem is not guaranteed for (p>1). Treat the Wegner expression as a rigorously stated disk-packing inequality, but the resulting (T(pQ,Q)) lower-bound interpretation as conditional when that topological/geometric hypothesis is absent. All constants above are for radius (a=1); multiply by (a) for physical tube radius (a).

### Toroidal helix parameterization and exact same-shell constraint

For (N) helices of cylindrical radius (r), height (H), repeat number (p), and torus major radius (R_0=pH/(2\pi)), the centerline is

\[
\begin{aligned}
x_i(\theta)&=[R_0+r\cos(p\theta)]\cos\left(\theta+\frac{2\pi i}{N}\right),\\
y_i(\theta)&=[R_0+r\cos(p\theta)]\sin\left(\theta+\frac{2\pi i}{N}\right),\\
z_i(\theta)&=r\sin(p\theta).
\end{aligned}
\]

For same-cylinder neighbors, the exact distance test is

\[
d(\theta_\Delta)=\sqrt{2r^2\left[1-\cos\left(\theta_\Delta+\frac{2\pi}{N}\right)\right]+\left(\frac{H\theta_\Delta}{2\pi}\right)^2}\ge2,
\quad -\pi\le\theta_\Delta\le\pi.
\]

The minimizing phase is a small negative number with no closed form. Large-(N) single-shell values are (r=\sqrt2N/\pi), (H=\sqrt8N). For concentric shells, neighboring minor radii must differ by at least 2. A torus with outer minor radius (r_o) has effective hole height (H_c=2\pi(R_0-r_o)), which is smaller than the straight height and controls the inner-side overlap.

### Guaranteed-parameter (k=4) construction

The zero-parameter construction uses shell radii (r_i=2i), occupancies (4i), outer (r_o=2T), (N_o=4T), and the rectangular unwrapping approximation. Its effective height is

\[
H_c\ge\frac{2\pi}{\sqrt{\pi^2-4}}N_o\simeq2.59N_o.
\]

Choosing

\[
R_0=\frac{H_c}{2\pi}+r_o
=\left(\frac1{\sqrt{\pi^2-4}}+\frac12\right)N_o
\simeq0.913N_o
\]

and (Q\simeq2T^2), the closed height is

\[
H_0=2\pi R_0=\kappa\sqrt Q,
\qquad
\kappa=2\pi\left(\frac1{\sqrt{\pi^2-4}}+\frac12\right)\sqrt8\simeq16.22.
\]

The straight-helix sum and integral are

\[
L_4=\sum_{i=1}^{\sqrt{Q/2}}4i\sqrt{\kappa^2Q+(4\pi i)^2},
\]
\[
L_4\simeq\frac{Q^{3/2}}{12\pi^2}
\left[(\kappa^2+8\pi^2)^{3/2}-\left(\kappa^2+\frac{16\pi^2}{Q}\right)^{3/2}\right].
\]

Thus (alpha_4\to17.36). Hopf-linking two copies through their holes doubles length and gives four times the asymptotic crossing count for (p=1). The double-torus coefficient before toroidal length correction is

\[
\alpha_{4D}=\frac{4\pi}{3}(5\sqrt5-8)\simeq13.32.
\]

The numerical toroidal correction is the limit reported as 1.0042, producing (13.38); the paper says it is below 1.005 for (T\ge10). This is a numerical correction, not a closed-form theorem.

### Maximum-occupancy construction and the 11.68 claim

For shell radius (r) and effective hole radius (h), the rectangular/small-angle estimate is

\[
N_a=\frac{\pi h r}{\sqrt{h^2+r^2}}.
\]

The authors propose (N_{\max}=\lfloor N_a-\epsilon\rfloor), with the cubic-approximation range

\[
\pi\left(r-\left(\arcsin\frac1r\right)^{-1}\right)\le\epsilon\le2\pi-6.
\]

Their v2 length and count formulas are

\[
L_{opt}=\sum_{i=1}^{T}
\frac{4\pi iT}{\sqrt{4T^2+4i^2}}
\sqrt{(8\pi T)^2+(4\pi i)^2}
\]

and

\[
Q=\sum_{i=1}^{T}\frac{2\pi iT}{\sqrt{i^2+T^2}}
\simeq2\pi(\sqrt2-1)T^2\simeq2.6T^2.
\]

After the double-torus factor (1/\sqrt2), the asymptotic coefficient is

\[
\alpha_{opt}
=\sqrt{(7+5\sqrt2)\pi}
\left[\sqrt{10}-2+3\left(\operatorname{atanh}\sqrt{\frac25}-\operatorname{atanh}\frac12\right)\right]
\simeq11.64.
\]

The measured/integrated toroidal correction 1.00385 gives 11.68. This is not presently a certified upper bound: the appendix proves only properties of a cubic truncation of the exact distance equation. It explicitly says the full transcendental constraint has not been proved for the proposed integer occupancy. Numerical tests reached (T=100), (Q=52{,}203), (C\approx2.7\times10^9), with 1000 samples per helix. The claim applies first to (Q\simeq5.2T^2); outer helices can be removed to hit a desired (Q), but a complete no-overlap proof after arbitrary removal is also absent.

### v1 versus v2 transcription corrections

The arXiv record identifies v2 as revised 13 March 2026. The v1 HTML printed Eq. (19) as (N_a=\pi h r/(h^2+r^2)), omitting the square root. V2 correctly prints (N_a=\pi h r/\sqrt{h^2+r^2}). V1 Eq. (21) used the integrand \(\sqrt{1+3/(i^2+T^2)}\); v2 uses the dimensionally consistent \(\sqrt{(4T^2+i^2)/(T^2+i^2)}\). Reproductions should use v2 and retain a version note in code or notebooks.

## 4. Recent physical filament evidence

### Elastic multifilament bundles (Dawadi *et al.*, PRE 2025)

The experiments use silicone filaments of diameter (d_0=2.60\,\mathrm{mm}), Poisson ratio about 0.5, and shear modulus (1.43\pm0.1\,\mathrm{MPa}). They vary (n=2)–16 filaments, initially parallel on circular clamps of radius (R_0=25\,\mathrm{mm}), relaxed length (L_f=162\,\mathrm{mm}), with force (F=nF_1), (F_1=0.735\,\mathrm N). A scaled X-ray setup uses (R_0=20\,\mathrm{mm}), (L_f=110\,\mathrm{mm}).

The observed sequence is: a hyperboloid-like fan-out, first contact in a ring near \(\theta_c\), then a tight central bundle. For (n=16), radial instability occurs around (200^\circ) after contact around (140^\circ); (n=8) and 16 show disorder and filament migration, while (n=2) and 4 remain ordered over the reported range. The bundle radius is nearly constant after formation, and filament inclination is modeled by

\[
\phi_i=\tan^{-1}(\Omega_Br_i).
\]

The elastogeometric model writes (E_{el}=E_s+E_t+E_b+E_c) and obtains (F=\partial E_{el}/\partial L|_\theta), (M=\partial E_{el}/\partial\theta|_L), using a representative helical bundle plus a straight fan-out region and a neo-Hookean law. This is useful physical evidence that perfect concentric, constant-radius, equal-pitch bundles are fragile under elasticity and preparation history. It does not validate Klotz’s unit-radius ropelength assumptions or supply a torus-link closure.

### Printed torus-knot particles (Yan *et al.*, PRL 2025)

Their particle centerline is

\[
x=[R+r\cos(qt)]\cos(pt),\quad y=[R+r\cos(qt)]\sin(pt),\quad z=r\sin(qt),
\]

with (p=1) fixed and (q) controlling petals. They require clearance below 5% of wire thickness and assume smooth surfaces, then model interlocking contacts as point-bar constraints. Their modified Maxwell count is (M=2j+g-2b-3), and for periodic cells (M_{cell}=2j_{cell}+g_{cell}-2b_{cell}+1). These fixed choices (planarity, (p=1), small clearance, ideal smooth contact) are explicit degrees-of-freedom controls. The work demonstrates physical manufacturability and topology-controlled connectivity, but it does not measure ropelength or prove tube thickness.

For a direct recent knotting-dynamics reference, Cunha, Tubiana, Biswal, and MacKintosh, “Hierarchical Knot Formation of Semiflexible Filaments Driven by Hydrodynamics,” *PRL* **135**, 248201 (12 Dec 2025), [APS record](https://journals.aps.org/prl/abstract/10.1103/z7jb-fvjl), reports Brownian-dynamics sedimentation under strong fields, hydrodynamically induced knotting, and stabilization into tight knots. The accessible source is the abstract; no formula-level claims from that paper are used here.

## 5. Three minimal topology-controlled generalizations

These are bounded extensions of the published parameterizations, not claims that a new optimum has been found.

1. **Repeat-number family (T(pQ,Q)).** Keep the concentric unit and replace the single torus wrap by integer (p\ge1) in the toroidal parameterization. Enforce (C=pQ(Q-1)), (R_M=pH/(2\pi)), and a sufficient inner-extrema offset (+r_o) (or a direct exact distance check). This changes topology through the known torus-link family while preserving the shell geometry. The lower-bound caveat for (p>1) must be carried with the experiment.

2. **Integer shell-occupancy family.** Keep shell radii (R_i=R+2(i-1)), common (H), and a fixed repeat (p), while varying integer occupancies (M_i) with (sum_iM_i=Q-1). Every candidate must satisfy the exact same-shell transcendental distance and all cross-shell/toroidal distances. This isolates combinatorial packing from topology: (p,Q) fix the torus-link type, while (M_i,R,H) are geometric variables.

3. **Low-mode radial deformation family.** Replace the sinusoidal minor-radius term by a topology-preserving Fourier perturbation, for example (r\cos(p\theta)\mapsto r[\cos(p\theta)+\eta\cos(2p\theta+\delta)]), and reject any parameter for which the curve self-intersects, changes the intended closure, or violates (d\ge2a). Klotz–Thompson and Klotz explicitly identify higher Fourier modes/cycloidal radial profiles as a future direction; Dawadi *et al.* supply a physical warning that elasticity can induce radius migration. This family has a small, attackable parameter set ((\eta,\delta)) and keeps the toroidal winding numbers fixed.

## 6. Strongest attackable gap

The cleanest rigorous target is the missing full no-overlap theorem behind Klotz 2026 Eq. (20), followed by the toroidal and cross-shell checks. The exact same-shell problem reduces to minimizing

\[
d^2(\theta;N,r,h)=2r^2\left[1-\cos\left(\theta+\frac{2\pi}{N}\right)\right]+h^2\theta^2
\]

over the relevant phase interval. The paper’s appendix shows that (N_a-\epsilon) is safe for the *cubic truncation* in several limits, but explicitly does not show that the full transcendental minimum is at least 4 for all (r,h,T). It also relies on sampled numerical tests. A rigorous, reproducible attack would:

* prove where the exact minimizer lies (the relevant interval is near (-2\pi/N<\theta<0));
* bound the cosine remainder with interval arithmetic or alternating Taylor bounds over that interval;
* propagate the bound uniformly over shell radii (r=2i), hole radius (h=2T), and the integer floor/epsilon rule;
* separately verify all toroidal same-shell, cross-shell, and double-torus distances; and
* only then claim an (11.68,a) asymptotic upper bound for every sufficiently large admissible (Q).

This gap is stronger than searching for a lower ropelength: closing it would convert the headline (11.68) construction from “numerically supported conditional construction” into a reproducible certified family. The next mathematical target is a sharpened lower bound: the Wegner expression is a disk-packing inequality, but finite-(N) hull optimality and the cone-puncture condition for (p>1) remain separate hypotheses. The physical filament papers suggest a second, experimentally meaningful stress test: quantify how radial instability, migration, and elastic strain alter the exact-clearance model before interpreting a geometric optimum as a realizable filament.

## Sources

1. [Klotz and Thompson, “Ropelength-minimizing concentric helices and non-alternating torus knots,” arXiv:2504.00861v1](https://arxiv.org/abs/2504.00861); published as [Proc. R. Soc. A 481, 20250319 (2025)](https://doi.org/10.1098/rspa.2025.0319).
2. [Klotz, “Tight Bounds for Tight Links: Ropelength of \(T(Q,Q)\) torus links,” *J. Phys. A* **59** (2026), 285201](https://doi.org/10.1088/1751-8121/ae862e); inspected [arXiv:2603.02416v2](https://arxiv.org/html/2603.02416v2) and version history at [arXiv:2603.02416](https://arxiv.org/abs/2603.02416).
3. [Dawadi, Biswas, Chopin, and Kudrolli, “Bundling architecture in elastic filaments with applied twist,” PRE 112, 015416 (2025)](https://doi.org/10.1103/d782-cbmc); [arXiv:2501.04650](https://arxiv.org/abs/2501.04650).
4. [Yan *et al.*, “Rigidity Criteria for Chainmail Consisting of Tessellations of Torus Knots,” PRL 135, 088201 (2025)](https://www.daraio.caltech.edu/publications/202508_Yan.pdf).
5. [Cunha, Tubiana, Biswal, and MacKintosh, “Hierarchical Knot Formation of Semiflexible Filaments Driven by Hydrodynamics,” PRL 135, 248201 (2025)](https://doi.org/10.1103/z7jb-fvjl).

## Integration note — local primary-source acquisition

After the researcher's sandbox DNS failure, root used reviewed network access to
retrieve the primary PDFs. See `papers/DOWNLOAD_MANIFEST.json` for versions,
URLs and hashes. The 2026 file is arXiv v2, not the later published PDF; the
publisher-version access limitation remains relevant.
