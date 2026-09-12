# ropelength-minimizing-knots

Numerically-computed **ropelength-minimizing configurations** of knots and links — the shapes that
minimize *ropelength* (the ratio of length to thickness for a tube of fixed radius
around the curve). In many cases these configurations are the witnesses behind the
**ropelength upper bounds tabulated on [KnotInfo](https://knotinfo.math.indiana.edu/)**:
the number in the table is the ropelength of the shape in this repository.

These shapes were computed with [ridgerunner](https://github.com/designbynumbers/ridgerunner) (constrained gradient descent for
ropelength). This repository exists to give the configurations a specific, discoverable
home; contributions of configurations with lower ropelength and/or higher resolution are very welcome!

## File format (`.tsv`)

Each file is a plain **tab-separated** list of vertex coordinates:

```
x <TAB> y <TAB> z      # one vertex per line
...
                       # a BLANK LINE separates the components of a link
...
```

- Each **component is a closed loop**: the last vertex joins back to the first (there is
  no repeated closing vertex).
- A **knot** is a single component (no blank lines); a **link** has one blank line between
  each pair of components.
- Coordinates are full-precision output from the optimizer.

This is exactly the geometry format ingested by the [Knoodle](https://github.com/HenrikSchumacher/Knoodle) tools (`knoodletools`), so
you can load these files directly in `knoodleidentify` to check knot types, or `knoodledraw` to create knot diagrams for them.

## Directory layout

```
knots/
  prime/3-10/        # 249 files:  3_1.tsv ... 10_165.tsv
  composite/3-10/    # 550 files:  3_1+3_1.tsv, 2_2_1... (see naming)
links/
  prime/2-9/         # 130 files:  2_2_1.tsv (Hopf), 6_3_3.tsv, ...
  composite/2-9/     #  14 files
```

- **knots vs links** is determined by the number of components (1 vs. more).
- **prime vs composite** distinguishes connect sums.
- The `3-10` / `2-9` level is the **crossing-number range of the underlying prime table**
  this batch was built from (prime knots 3–10 crossings; prime links 2–9). If higher-crossing
  data is added later, it will go in new, parallel subdirectories (e.g. `knots/prime/11/`, `knots/prime/12/`), leaving the
  existing files untouched.

## Naming

- **Prime knots** — `C_N`: crossing number `C`, table index `N`. e.g. `3_1` (trefoil),
  `10_165`.
- **Prime links** — `C_K_N`: crossing number `C`, number of components `K`, index `N`.
  e.g. `2_2_1` (Hopf link), `6_3_3`.
- **Composites** — summands joined by `+` (connect sum). e.g. `3_1+3_1` (granny/square knot),
  `2_2_1+3_1` (Hopf link connect-sum trefoil). A `_m` on a summand denotes its **mirror**;
  `_TreeA` / `_TreeB` distinguish inequivalent association trees of a multi-summand sum.

## Converting back to Geomview VECT

The original data was in Geomview `VECT` format. If you need it back (e.g. for
`ridgerunner`), a small script is included:

```bash
./tsv2vect.sh knots/prime/3-10/3_1.tsv            # writes VECT to stdout
./tsv2vect.sh knots/prime/3-10/3_1.tsv 3_1.vect   # writes VECT to a file
```

It rebuilds a minimal, colorless VECT of closed polylines. The forward converter used to
build this repository, `vect2kndl.py`, is also included for reproducibility.

## Counts

943 configurations total: knots (prime **249**, composite **550**), links (prime **130**,
composite **14**).

## References

- **Ropelength values** for these knots and links are tabulated on
  [KnotInfo](https://knotinfo.math.indiana.edu/).
- Ashton, T., Cantarella, J., Piatek, M., & Rawdon, E. J. (2011).
  Knot Tightening by Constrained Gradient Descent. Experimental Mathematics, 20(1), 57–90.
  https://doi.org/10.1080/10586458.2011.544581
- Ashton, T., Cantarella  J., Piatek, M., & Rawdon, E. J. (2005).
  Self-contact Sets for 50 Tightly Knotted and Linked Tubes
  https://arxiv.org/abs/math/0508248 

## License

Released into the public domain under **[CC0 1.0](LICENSE)**. These are mathematical
objects inherent in the knot and link types, not creative works — no rights are reserved.
A citation to the papers above is appreciated but not required.
