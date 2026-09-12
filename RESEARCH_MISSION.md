/goal

# Tight Knots Lab

## AI-Assisted Research on Ropelength, Geometric Knot Optimization and Physical Filaments

# Mission

Construire un laboratoire de recherche reproductible consacré au problème de **ropelength** des nœuds et entrelacs.

Pour une courbe fermée \(K\subset\mathbb R^3\), définir :

$$
\operatorname{Rop}(K)
=
\frac{\operatorname{Length}(K)}
{\operatorname{Thickness}(K)}.
$$

Pour une classe d'isotopie \(\mathcal K\),

$$
\operatorname{Rop}(\mathcal K)
=
\inf_{K\in\mathcal K}\operatorname{Rop}(K).
$$

Le but n'est PAS simplement de lancer un optimiseur numérique pour produire des nœuds visuellement serrés.

Le but est de découvrir des résultats mathématiques rigoureux tels que :

* nouvelle borne inférieure ;
* nouvelle borne supérieure constructive ;
* constante asymptotique améliorée ;
* famille de nœuds/liens possédant une construction quasi-optimale ;
* nouvelle relation ropelength ↔ crossing number ;
* nouvelle structure du graphe de contacts ;
* nouvelle condition de criticité ;
* configuration explicitement certifiable ;
* preuve qu'une famille géométrique atteint ou approche une limite optimale ;
* nouvelle obstruction géométrique ;
* nouvelle connexion avec la mécanique des filaments épais.

Prioriser les **objets mathématiques explicables et certifiables** plutôt que la seule optimisation numérique.

---

# 0. PHILOSOPHIE

Le Quantum Max-Cut Lab et le Self-Avoiding Walk Lab ont montré que le meilleur résultat peut apparaître à côté de la cible initiale.

Ici également :

```text
tight knot
↓
numerical optimization
↓
contact structure
↓
geometric pattern
↓
conjecture
↓
lower/upper bound
↓
theorem
```

ou :

```text
torus knot family
↓
helical packing
↓
convex geometry
↓
asymptotic constant
↓
sharp inequality
```

Suivre les mathématiques lorsqu'elles indiquent une direction plus intéressante.

---

# 1. ORCHESTRATION ASTRA / LUNA

Suivre :

`donvito/codex-astra-luna-orchestrator`

Utiliser la meilleure configuration réellement disponible.

Topologie préférée :

```text
ASTRA ROOT
    |
    +-- Luna researcher
    +-- Luna explorer
    +-- Luna geometer/worker
    +-- Luna tester
    |
    +-- Astra reviewer
    |
    v
ASTRA ROOT
integration scientifique
```

Ne jamais prétendre utiliser Astra ou un niveau de reasoning non réellement disponible.

Documenter les modèles effectifs.

---

## Astra root

Responsable de :

* stratégie scientifique ;
* formulation des conjectures ;
* choix des familles de nœuds ;
* décomposition des preuves ;
* architecture des expériences ;
* synthèse des résultats ;
* choix des claims ;
* interprétation géométrique ;
* décision de poursuivre ou abandonner une piste.

---

## Luna researcher

Recherche :

* ropelength ;
* ideal knots ;
* thickness/reach ;
* knot energies ;
* quadrisecants ;
* ropelength criticality ;
* strut sets ;
* kink measures ;
* torus knots/links ;
* crossing-number bounds ;
* lattice knots ;
* physical polymer knots ;
* littérature 2025–2026.

Toujours privilégier les sources primaires.

---

## Luna explorer

Inspecte :

* Ridgerunner ;
* plCurve ;
* bases de configurations minimisées ;
* KnotInfo ;
* SnapPy si pertinent ;
* logiciels de knot invariants ;
* fichiers VECT ;
* méthodes de collision/self-distance ;
* codes récents.

Lecture seule par défaut.

---

## Luna worker

Implémente :

* générateurs géométriques ;
* courbes paramétriques ;
* helices ;
* torus embeddings ;
* optimisations ;
* contact detection ;
* thickness estimators ;
* convex-hull bounds ;
* interval certification ;
* visualization ;
* search engine.

---

## Luna tester

Doit essayer de casser :

* knot type ;
* thickness claim ;
* absence d'auto-intersection ;
* contact set ;
* curvature constraints ;
* lower bound ;
* asymptotic claim ;
* numerical minimum ;
* global-optimum assertion.

---

## Astra reviewer

Pour chaque résultat important :

> Assume that the theorem is false.

Chercher :

* mauvaise classe isotopique ;
* self-intersection cachée ;
* thickness surestimée ;
* local minimum pris pour global minimum ;
* contact oublié ;
* curvature violation ;
* asymptotic extrapolation abusive ;
* scaling mistake ;
* mauvaise normalisation du diamètre/rayon ;
* résultat déjà connu.

---

# 2. WORKSPACE

Créer :

```text
tight-knots-lab/
```

avec :

```text
README.md
ENVIRONMENT_AUDIT.md
STATE_OF_THE_ART.md
NORMALIZATION.md
RESEARCH_LOG.md
ORCHESTRATION_LOG.md
NOVELTY_LOG.md
NEXT.md

papers/
references/
src/
tests/
geometry/
data/
benchmarks/
experiments/
results/
proofs/
claims/
publication/
```

Initialiser Git immédiatement.

---

# 3. ENVIRONMENT AUDIT

Vérifier :

* Python ;
* C/C++ ;
* Rust si utile ;
* scipy ;
* sympy ;
* numpy ;
* scipy.optimize ;
* trimesh ;
* shapely uniquement si réellement pertinent ;
* interval arithmetic ;
* CGAL éventuel ;
* knot libraries ;
* SnapPy ;
* SageMath ;
* Ridgerunner ;
* plCurve ;
* OpenBLAS ;
* visualization 3D ;
* GPU.

Le GPU n'est pas prioritaire.

Ce problème sera probablement dominé par :

```text
geometry
+
nonlinear constrained optimization
+
contact search
+
exact/interval certification
```

Ne pas payer de licence ou compute externe sans autorisation.

---

# 4. NORMALISATION

Créer :

`NORMALIZATION.md`

Fixer définitivement :

* rope radius ;
* rope diameter ;
* thickness ;
* reach ;
* contour length ;
* polygonal thickness ;
* smooth thickness ;
* crossing number ;
* link vs knot conventions.

Pour une courbe \(C^{1,1}\), utiliser comme référence :

$$
\operatorname{Thi}(K)
=
\min
\left\{
\frac{1}{\kappa_{\max}},
\frac12\operatorname{DCSD}(K)
\right\},
$$

avec DCSD = doubly critical self-distance.

Vérifier précisément les hypothèses et conventions dans les sources.

Toute comparaison de ropelength doit utiliser la même convention de thickness.

---

# 5. ÉTAT DE L'ART 2026

Faire une recherche bibliographique fraîche.

Ne pas graver les chiffres ci-dessous sans vérification.

Inclure au minimum :

* Gonzalez–Maddocks ;
* Cantarella ;
* Kusner ;
* Sullivan ;
* Rawdon ;
* Denne ;
* Diao ;
* quadrisecant bounds ;
* ropelength criticality ;
* Ridgerunner ;
* numerical ideal knots ;
* torus-knot/link constructions ;
* travaux Klotz 2025–2026 ;
* physical tight-knot/polymer literature récente.

Créer :

`STATE_OF_THE_ART.md`

Pour chaque résultat :

```text
object
knot/link family
rigorous?
numerical?
lower bound
upper bound
claimed optimum?
proof method
source
code/data
remaining gap
```

---

# 6. CONTRÔLES POSITIFS

Avant toute nouveauté, reproduire plusieurs résultats connus.

## Unknot

Configuration circulaire.

Vérifier exactement sa ropelength sous notre convention.

## Trefoil

Reproduire une configuration tight numérique connue.

Ne PAS prétendre connaître exactement son minimum si la littérature ne le prouve pas.

Comparer :

* Ridgerunner ;
* notre optimisation ;
* coordonnées de référence.

## Simple links

Reproduire :

* Hopf link ;
* petits torus links ;
* quelques knots ≤ 8–10 crossings.

---

# 7. TOPOLOGY VALIDATION

Toute géométrie candidate doit être accompagnée d'une preuve ou certification de sa classe topologique.

Utiliser plusieurs invariants lorsque possible :

* Alexander polynomial ;
* Jones polynomial ;
* HOMFLY-PT ;
* linking number ;
* Dowker code ;
* braid representation ;
* SnapPy/KnotInfo identification.

Pour les familles paramétriques :

préférer une **preuve constructive d'isotopie** plutôt qu'une simple identification numérique.

---

# 8. THICKNESS ENGINE

Construire une implémentation indépendante capable d'estimer :

$$
\operatorname{Thi}(K)
=
\min
\left(
\operatorname{MinRad},
\frac12\operatorname{DCSD}
\right).
$$

Pour les courbes polygonales :

* vertex curvature constraints ;
* edge-edge distances ;
* struts ;
* polygonal thickness.

Pour les courbes analytiques :

* curvature ;
* pairwise critical distance ;
* certified root isolation lorsque possible.

Comparer systématiquement à Ridgerunner/octrope lorsque disponible.

---

# 9. CONTACT GRAPH

Pour une configuration tight ou presque tight, construire :

$$
\mathcal C(K)
$$

où les sommets/paramètres représentent des portions de la courbe et les arêtes représentent les contacts actifs.

Enregistrer :

* struts ;
* kink locations ;
* multiplicities ;
* symmetries ;
* contact-distance distribution.

Question :

> Le graphe de contacts révèle-t-il une structure combinatoire répétitive ?

C'est potentiellement l'équivalent du `k-Edge Separator` trouvé dans Quantum Max-Cut.

---

# 10. AXE A — STRUCTURED TORUS LINKS

Priorité initiale.

Étudier :

$$
T(p,q)
$$

et particulièrement les grandes familles :

$$
T(Q,Q),
\quad
T(mQ,Q),
\quad
T(Q+r,Q).
$$

Le travail récent de 2025–2026 montre que les constructions en hélices concentriques et close-packed structures donnent des bornes nettement améliorées.

Ne pas simplement reproduire ces constructions.

Chercher :

* nouveaux packings ;
* plusieurs shells ;
* shell populations optimales ;
* helices non uniformes ;
* pitch variable ;
* radial compression variable ;
* boundary-layer corrections ;
* end-closing geometry ;
* non-circular cross-sections only if mathematically justified.

---

# 11. OBJECTIF ASYMPTOTIQUE

Pour une famille \(\mathcal K_Q\) avec crossing number \(C_Q\), étudier :

$$
\frac{\operatorname{Rop}(\mathcal K_Q)}
{C_Q^{3/4}}.
$$

Chercher :

$$
\liminf_{Q\to\infty}
\frac{\operatorname{Rop}(\mathcal K_Q)}
{C_Q^{3/4}}
$$

et

$$
\limsup_{Q\to\infty}
\frac{\operatorname{Rop}(\mathcal K_Q)}
{C_Q^{3/4}}.
$$

Le jackpot serait :

$$
\boxed{
\operatorname{Rop}(\mathcal K_Q)
\sim
\alpha C_Q^{3/4}
}
$$

avec \(\alpha\) exact ou encadré très étroitement.

---

# 12. AXE B — IMPROVE LOWER BOUNDS

Ne pas faire uniquement des constructions supérieures.

Chercher des bornes inférieures via :

* convex hull ;
* packing arguments ;
* quadrisecants ;
* projection geometry ;
* area/volume exclusion ;
* slicing planes ;
* tube packing ;
* contact graph ;
* bridge number ;
* braid index ;
* crossing number.

Pour chaque lower bound :

```text
assumptions
↓
geometric invariant
↓
inequality
↓
asymptotic coefficient
```

Priorité aux arguments qui s'appliquent à une famille complète.

---

# 13. AXE C — PACKING CROSS-SECTIONS

Pour les familles comportant de nombreux segments/helices parallèles, considérer leurs intersections avec une coupe transverse.

On obtient souvent un packing de disques.

Chercher :

* hexagonal packing ;
* boundary deficit ;
* discrete isoperimetry ;
* convex hull perimeter ;
* shell effects.

Question :

> Peut-on transformer un problème 3D de ropelength en un problème 2D de packing suffisamment précis pour obtenir une constante asymptotique sharp ?

---

# 14. AXE D — HELICAL GEOMETRY

Pour une hélice :

$$
r(\theta)
=
(R\cos\theta,
R\sin\theta,
a\theta).
$$

Calculer exactement :

* length per turn ;
* curvature ;
* torsion ;
* self-distance ;
* distance between neighboring helices.

Résoudre les contraintes de non-overlap :

$$
d_{\min}\ge2r_{\text{rope}}.
$$

Chercher les paramètres optimaux :

$$
R,\quad a,\quad \Delta\theta,\quad\text{shell radii}.
$$

Puis tenter de transformer les optimums numériques en solutions d'équations analytiques.

---

# 15. AXE E — SYMBOLIC REGRESSION

Lorsqu'un paramètre optimal semble converger :

$$
R_Q\to R_*,
\qquad
a_Q\to a_*,
$$

calculer haute précision et tester :

* rational reconstruction ;
* algebraic recognition ;
* PSLQ.

Mais :

```text
PSLQ ≠ proof
```

Toute formule candidate doit être dérivée géométriquement.

---

# 16. AXE F — BOUNDARY CORRECTIONS

Les grandes constructions asymptotiques possèdent souvent :

$$
L(Q)
=
AQ^{3/2}
+
BQ
+
CQ^{1/2}
+
O(1).
$$

Ne pas regarder uniquement \(A\).

Chercher :

$$
B,C,\ldots
$$

Ils peuvent révéler la vraie géométrie optimale des frontières.

Une amélioration de correction sous-dominante peut également permettre de distinguer deux constructions ayant le même leading coefficient.

---

# 17. AXE G — GLOBAL VS LOCAL MINIMA

Ridgerunner et gradient descent peuvent produire :

$$
K_{\text{local}}.
$$

Ne jamais appeler cela automatiquement :

$$
K_{\text{global}}.
$$

Utiliser :

* many-start optimization ;
* symmetry-breaking perturbations ;
* random initial configurations ;
* simulated annealing ;
* differential evolution ;
* basin hopping ;
* continuation between families.

Si plusieurs minima apparaissent :

les conserver tous.

Ils peuvent représenter des phases géométriques différentes.

---

# 18. AXE H — CONTACT TOPOLOGY PHASES

Lorsqu'un paramètre varie, surveiller les changements du graphe de contacts.

Exemple :

$$
\lambda<\lambda_c
\Rightarrow
\mathcal C_1
$$

$$
\lambda>\lambda_c
\Rightarrow
\mathcal C_2.
$$

Une transition de contact peut produire une formule piecewise exacte pour l'optimum.

Chercher :

* bifurcations ;
* contact creation ;
* contact loss ;
* curvature-active transitions.

---

# 19. AXE I — CRITICALITY

Étudier les conditions de criticité de ropelength :

* strut forces ;
* kink measures ;
* balance equations.

Pour une configuration candidate, chercher un certificat du type :

$$
\text{length gradient}
=
\text{contact forces}
+
\text{curvature forces}.
$$

Une configuration satisfaisant une condition critique certifiée est bien plus intéressante qu'une simple sortie d'optimiseur.

---

# 20. AXE J — CERTIFIED UPPER BOUNDS

Une configuration explicite donne une upper bound si l'on certifie :

1. knot/link type ;
2. absence d'auto-intersection ;
3. thickness \(\ge1\) après scaling ;
4. length \(\le L\).

Utiliser interval arithmetic.

Objectif :

$$
\operatorname{Rop}(\mathcal K)
\le L_{\rm certified}.
$$

Ne pas reposer uniquement sur floating point.

---

# 21. AXE K — CERTIFIED LOWER BOUNDS

Chercher des résultats de la forme :

$$
\operatorname{Rop}(\mathcal K)
\ge L_{\rm lower}.
$$

Si :

$$
L_{\rm upper}-L_{\rm lower}
$$

devient petit, chercher à identifier les conditions d'égalité.

Le scénario idéal :

$$
L_{\rm lower}=L_{\rm upper}.
$$

Ce serait une ropelength exacte.

---

# 22. AXE L — SMALL KNOT ATLAS

Créer un atlas reproductible pour des knots à faible crossing number.

Pour chaque type :

```text
knot
crossing number
best known upper
our upper
known lower
contact graph
symmetry
local minima
source
```

Ne pas essayer immédiatement de battre tous les records.

Chercher plutôt des motifs communs.

---

# 23. AUTOMATED GEOMETRY DISCOVERY

Construire un moteur :

```text
knot/link family
+
parameterization
+
symmetry
+
packing pattern
+
contact constraints
↓
optimization
↓
candidate configuration
↓
contact extraction
↓
symbolic simplification
↓
certificate
```

Le but n'est pas seulement de trouver une valeur plus petite.

Le but est de trouver **une géométrie explicable**.

---

# 24. GEOMETRIC GRAMMAR

Chercher si les tight knots peuvent être décrits avec quelques primitives :

* circle arcs ;
* helices ;
* straight segments ;
* clasp arcs ;
* constant curvature pieces ;
* symmetric junctions.

Si une famille optimisée converge vers un assemblage fini de primitives :

extraire cette grammaire.

Cela pourrait transformer une optimisation infinie-dimensionnelle en un problème à quelques paramètres.

---

# 25. AXE M — PHYSICAL FILAMENT MODEL

Après avoir résolu une question géométrique, traduire vers un filament physique.

Comparer ropelength pure avec une énergie de filament :

$$
E
=
\frac{A}{2}\int\kappa^2 ds
+
\text{tension}
+
\text{self-contact}
+
\text{hydrodynamics/thermal terms}.
$$

Ne pas mélanger :

$$
\text{ropelength optimum}
$$

et

$$
\text{physical free-energy optimum}.
$$

Mais étudier comment l'un contraint l'autre.

Applications possibles :

* DNA ;
* proteins ;
* semiflexible polymers ;
* active polymers ;
* filament materials.

---

# 26. PHYSICAL QUESTION

Pour un filament de rayon \(r\), une ropelength minimale \(L_*\) implique une longueur de contour minimale :

$$
\ell_{\min}
=
rL_*
$$

si la convention utilise thickness = radius.

Vérifier systématiquement la convention.

Une amélioration rigoureuse sur \(L_*\) donne donc immédiatement une contrainte géométrique sur la longueur nécessaire pour réaliser un nœud physique d'épaisseur donnée.

---

# 27. KNOTTING UNDER CONFINEMENT

Extension secondaire :

* tubes ;
* nanopores ;
* slabs ;
* spheres ;
* cylinders.

Définir :

$$
\operatorname{Rop}_{\Omega}(\mathcal K).
$$

Étudier comment le confinement change :

* optimum ;
* contact graph ;
* knot localization.

À lancer seulement après un résultat utile sur le problème libre.

---

# 28. RANDOM/ACTIVE POLYMERS

Ne pas confondre probabilité de formation d'un knot avec ropelength minimal.

Cependant, si une géométrie tight particulière apparaît fréquemment dans des simulations hydrodynamiques ou active-polymer :

la comparer quantitativement aux minimizers géométriques.

Cela peut produire une question physique intéressante :

> La dynamique sélectionne-t-elle les mêmes configurations que le problème purement géométrique ?

---

# 29. NOVELTY PROTOCOL

Pour chaque résultat :

```text
claims/CLAIM-XXXX.md
```

contenant :

```text
Exact statement
Knot/link family
Ropelength convention
Proof level
Numerical evidence
Topology verification
Thickness verification
Counterexample search
Closest literature
Independent derivation
Novelty status
Open objections
```

Labels :

```text
KNOWN
REDISCOVERED
POSSIBLY NOVEL
STRONG NOVELTY EVIDENCE
VERIFIED RESULT
```

Toujours distinguer :

$$
\text{mathematically verified}
\neq
\text{publication novelty}.
$$

---

# 30. PROOF LEVELS

## Level 0

visual/numerical observation.

## Level 1

reproducible optimization.

## Level 2

independent topology + thickness check.

## Level 3

certified numerical/geometric bound.

## Level 4

analytic proof candidate.

## Level 5

independent implementation + adversarial Astra review.

---

# 31. REPRODUCIBILITY

Chaque expérience :

```text
experiment_id
UTC
commit
knot/link
parameterization
initial state
optimizer
tolerances
seed
length
thickness
ropelength
knot invariants
contact count
hardware
runtime
input hashes
output hashes
```

Ne jamais écraser les meilleurs résultats précédents.

---

# 32. CURRENT 2026 TARGET

La littérature 2025–2026 récente sur torus links fournit un terrain de départ particulièrement pertinent.

Auditer notamment :

* concentric-helical constructions ;
* \(T(Q,Q)\) bounds ;
* large-Q asymptotics ;
* close-packed disk lower bounds ;
* optimized helices ;
* gradient-descent configurations.

Ne pas supposer que leurs paramètres ou constants sont optimaux.

Chercher précisément :

> Quels degrés de liberté géométriques ont été fixés par les constructions existantes et pourraient être libérés ?

Exemples :

* nonuniform pitch ;
* shell-dependent pitch ;
* shell-dependent radii ;
* phase offsets ;
* elliptic deformation ;
* boundary shell optimization ;
* nonuniform closure.

Chaque généralisation doit rester topologiquement contrôlée.

---

# 33. PREMIER GRAND OBJECTIF

Pour une famille structurée telle que \(T(Q,Q)\), obtenir une amélioration de l'un des types suivants :

### A

meilleure upper bound asymptotique.

### B

meilleure lower bound asymptotique.

### C

réduction significative du gap entre les deux.

### D

nouvelle géométrie explicite avec coefficient analytiquement calculable.

### E

preuve d'optimalité dans une classe géométrique clairement définie.

### F

preuve que certaines constructions existantes ne peuvent pas être asymptotiquement optimales.

---

# 34. DEUXIÈME OBJECTIF : UNIVERSAL ROPENGTH BOUNDS

Étudier ensuite les inégalités générales :

$$
\operatorname{Rop}(K)
\ge
\alpha\,c(K)^{3/4}
$$

et variantes.

Faire une carte précise de :

* meilleur \(\alpha\) universel prouvé ;
* meilleures familles donnant des contraintes supérieures sur le meilleur \(\alpha\) possible ;
* gaps connus ;
* hypothèses exactes.

Chercher si les nouvelles familles structurées permettent d'améliorer :

* le universal lower coefficient ;
* les obstruction families ;
* ou seulement les family-specific bounds.

Ne jamais confondre ces trois résultats.

---

# 35. DISCOVERY ENGINE

Moteur cible :

```text
family
↓
parameterization generator
↓
constraint builder
↓
optimizer
↓
topology check
↓
thickness/contact engine
↓
pattern mining
↓
symbolic recognition
↓
candidate theorem
```

Utiliser Astra pour interpréter les configurations, pas simplement choisir le plus petit nombre.

---

# 36. FIRST EXPERIMENTS

Après M1, comparer au moins :

### Experiment A

reproduction d'une torus-link construction 2026.

### Experiment B

libération de pitch/radius par shell.

### Experiment C

new boundary-layer packing.

### Experiment D

multi-start unconstrained refinement avec topology preservation.

### Experiment E

contact-graph clustering entre les solutions.

La priorité n'est pas le meilleur résultat numérique brut mais la découverte d'une structure répétitive.

---

# 37. MILESTONE M1 — REPRODUCIBLE GEOMETRY LAB

Exiger :

* environment audit ;
* normalization ;
* current bibliography ;
* Ridgerunner reproduction ;
* independent thickness checker ;
* topology checker ;
* unknot positive control ;
* trefoil control ;
* simple torus-link control ;
* interval/certified upper-bound demo ;
* contact graph extraction ;
* independent reviewer.

---

# 38. MILESTONE M2 — AUTOMATED DISCOVERY

Construire le moteur permettant de varier :

```text
family
Q
number of shells
shell populations
pitch
radii
phase
closure geometry
symmetry
```

Le système doit produire au moins une observation structurelle non injectée manuellement.

Exemple acceptable :

> toutes les meilleures configurations convergent vers un ratio précis entre pitch et shell radius.

---

# 39. MILESTONE M3 — CANDIDATE RESULT

Choisir selon :

$$
\frac{
\text{importance}
\times
\text{proofability}
\times
\text{generality}
}{
\text{certification cost}
}.
$$

Puis :

```text
candidate geometry
↓
independent optimization
↓
topology attack
↓
thickness attack
↓
symbolic reconstruction
↓
analytic bound
↓
counterexample search
↓
Astra review
↓
novelty audit
```

---

# 40. MILESTONE M4 — PUBLICATION CANDIDATE

Si un résultat survit :

```text
publication/
  main.tex
  figures/
  geometry/
  checkers/
  reproduce.py
  requirements-lock.txt
  CONTRIBUTION_REVIEW.md
  VALIDATION.md
```

Ne pas écrire un papier avant d'avoir un vrai résultat.

---

# 41. FIRST MULTI-AGENT RUN

Lancer en parallèle :

## researcher-1 — Mathematical frontier

Trouver les meilleures bornes rigoureuses actuelles :

* general ropelength ;
* crossing-number relationships ;
* torus knot/link families ;
* small knots.

---

## researcher-2 — 2025–2026 frontier

Auditer en profondeur les travaux récents sur :

* concentric helices ;
* \(T(Q,Q)\) ;
* close packing ;
* physical tight filaments.

Identifier précisément les degrés de liberté qui n'ont pas été explorés.

---

## explorer — Software/data

Installer/auditer :

* Ridgerunner ;
* plCurve ;
* known tight-knot datasets ;
* topology packages.

---

## worker — Minimal geometry engine

Construire :

```text
src/curves/
src/thickness/
src/topology/
src/contacts/
```

avec unknot/Hopf/trefoil tests.

---

## tester — Independent validator

Créer une deuxième voie pour :

* length ;
* curvature ;
* self-distance ;
* knot invariant.

Ne pas réutiliser les routines du worker dans les tests critiques.

---

# 42. PREMIÈRE QUESTION APRÈS M1

Astra doit répondre :

> Quel est actuellement le plus gros gap attaquable entre une lower bound rigoureuse et une construction supérieure pour une famille structurée de knots/links ?

Comparer au minimum :

* \(T(Q,Q)\) ;
* autres torus families ;
* alternating vs non-alternating torus knots ;
* selected small knots.

Choisir la cible selon :

```text
gap size
structure
proofability
available data
physical meaning
novelty opportunity
```

---

# 43. LEÇON DES PROJETS PRÉCÉDENTS

QMC :

```text
approximation
→ entanglement depth
→ graph partitions
```

SAW :

```text
connective constant
→ prudent walks
→ non-D-finiteness
```

Tight Knots pourrait faire :

```text
ropelength optimization
→ contact graph
→ packing theorem
```

ou :

```text
torus knot
→ concentric helices
→ exact asymptotic coefficient
```

ou :

```text
numerical minimizer
→ finite geometric grammar
→ analytic tight configuration
```

Ne pas résister à un détour mathématique prometteur.

---

# 44. DIRECTIVE FINALE

Ne PAS fonctionner comme :

```text
optimizer
→ lower number
→ "new tight knot"
```

Fonctionner comme :

```text
ASTRA
↓
question géométrique

LUNA RESEARCHER
→ littérature

LUNA EXPLORER
→ logiciels / data

LUNA WORKER
→ nouvelles géométries

LUNA TESTER
→ topology / thickness falsification

ASTRA REVIEWER
→ attaque du théorème

ASTRA
→ extrait la structure
↓
analytic bound
↓
certificate
↓
novelty audit
```

Règle d'or :

**Une belle configuration numérique n'est pas un théorème.**

Et :

**Chercher la géométrie qui explique l'optimum, pas seulement l'optimum.**

---

# ACTION IMMÉDIATE

1. créer `tight-knots-lab`;
2. installer l'orchestration project-scoped ;
3. initialiser Git ;
4. auditer hardware/software ;
5. produire `NORMALIZATION.md` ;
6. produire `STATE_OF_THE_ART.md` à jour au 12 septembre 2026 ;
7. installer ou compiler Ridgerunner/plCurve si possible ;
8. reproduire unknot, Hopf, trefoil ;
9. implémenter un thickness checker indépendant ;
10. implémenter topology verification ;
11. auditer en détail les torus-link papers 2025–2026 ;
12. identifier le gap mathématique le plus attaquable ;
13. reproduire une construction récente ;
14. extraire son contact graph ;
15. lister tous les paramètres artificiellement fixés dans cette construction ;
16. proposer trois généralisations minimales ;
17. lancer les premières optimisations ;
18. chercher une structure, pas seulement une amélioration décimale ;
19. faire M1_REVIEW ;
20. seulement ensuite lancer M2.

Ne me demander une intervention que pour :

* paiement ;
* credentials ;
* compute externe payant ;
* publication/contact externe ;
* décision scientifique majeure incompatible.

Pour les décisions techniques ordinaires :

**décider, documenter, tester, continuer.**
