# Experimental comparison of knot-invariant discrimination

This repository measures collision rates for three computed quantities on a
fixed registry of knots with at most 11 crossings:

- Khovanov homology, computed with JavaKhV2;
- the HOMFLY-PT polynomial, computed with SageMath; and
- numerical values returned by SnapPy for knot complements.

The results are engineering measurements on the committed data, not claims
that any listed invariant is complete. A singleton collision class means only
that no *other registry entry* has the same stored value.

## Mathematical scope and corrections

A Wirtinger presentation presents the fundamental group of a knot complement,
but the ordinary knot group is not a complete knot invariant. The square and
granny knots are distinct and have isomorphic fundamental groups, as discussed
in [Tuffley's paper on generalized knot groups](https://arxiv.org/abs/0706.1807).
The stronger statement that knots in the 3-sphere are determined by their
complements is the [Gordon-Luecke theorem](https://doi.org/10.2307/1990979).
This project does not implement complement homeomorphism recognition or a
peripheral-system comparison.

The composite-knot registry assumes additivity of minimal crossing number:

\[
c(K \mathbin{\#} L) = c(K) + c(L).
\]

This remains a conjecture, not a theorem in general. The easy upper bound is
obtained by joining minimal diagrams. Published work supplies lower bounds;
for example, [Qiu and Wang](https://arxiv.org/abs/2407.10467) prove a factor-16
bound. Consequently, the claim that this repository enumerates *every* knot
through 11 crossings is conditional on crossing-number additivity. The
committed collection is still a useful explicitly defined sample even if that
conjecture is not assumed.

## Input data

The analysis joins these three name-to-value registries and now verifies that
their knot-name sets agree exactly:

- [`HOMFLY-PT-reg.txt`](HOMFLY-PT-reg.txt)
- [`khovanov-reg.txt`](khovanov-reg.txt)
- [`volume_info_list-reg.txt`](volume_info_list-reg.txt)

There are 1,783 entries:

| Category | Count |
| --- | ---: |
| Prime knots, with mirror images represented separately | 1,582 |
| Composite knots | 200 |
| Unknot | 1 |

After mirror pairs are identified, the prime-knot volume analysis uses 801
base names: 781 chiral pairs and 20 amphichiral knots.

The registry names and invariant values are treated as source data. The script
checks format, duplicate names, record counts, and cross-file name agreement;
it does not independently recompute the three invariants.

## Exact-invariant collision results

For an invariant or tuple of invariants, entries are grouped by exact equality
of their stored strings. These are **collision classes**, not isotopy classes.

| Features used | Classes | Singletons | Pairs | Triples | Classes of four |
| --- | ---: | ---: | ---: | ---: | ---: |
| Khovanov homology | 1,549 | 1,349 | 167 | 32 | 1 |
| HOMFLY-PT polynomial | 1,669 | 1,559 | 106 | 4 | 0 |
| Khovanov + HOMFLY-PT | 1,677 | 1,575 | 98 | 4 | 0 |

The detailed groups are committed as:

- [`json/get_kho_stat.json`](json/get_kho_stat.json)
- [`json/get_hom_stat.json`](json/get_hom_stat.json)
- [`json/get_kho_hom_stat.json`](json/get_kho_hom_stat.json)

On this dataset, the HOMFLY-PT strings create more classes than the Khovanov
strings, and combining both creates eight additional classes beyond HOMFLY-PT
alone. This finite comparison does not establish a general ordering between
the invariants.

In the intended indexing workflow, Khovanov homology is tried first because
the JavaKhV2 runs used by this project were more predictable in time and
memory. HOMFLY-PT is evaluated only when the first lookup collides; some large,
unreduced input diagrams took longer than the project's 20-minute operational
limit.

For the 200 committed composite-knot entries, the joint Khovanov/HOMFLY-PT
strings happen to be unique within the sample. See
[`json/get_kho_hom_non_prime_stat.json`](json/get_kho_hom_non_prime_stat.json).
This is a registry observation, not proof that the pair is complete for
composite knots.

## Numerical volume analysis

The volume registry was produced with SnapPy 3.1.1. SnapPy's documentation
states that [`Manifold.volume()`](https://snappy.computop.org/manifold.html#snappy.Manifold.volume)
returns the volume of the *current solution to the hyperbolic gluing
equations*. A certified result requires hyperbolicity verification; SnapPy
documents that workflow under
[`verify_hyperbolicity()` and verified computations](https://snappy.computop.org/verify.html).
The committed registry does not contain verification certificates.

This distinction is essential:

- Hyperbolic volume is a genuine invariant for a verified hyperbolic knot
  complement.
- A knot and its mirror have the same (unsigned) hyperbolic volume, so volume
  cannot detect chirality.
- Torus, satellite, and composite knot complements are not hyperbolic. A zero
  or near-zero numerical value returned from a degenerate solution must not be
  promoted to a certified hyperbolic volume or a general knot invariant.

For that reason, all results that combine the recorded volume with composite
knots are retained only as deprecated historical output:

- [`json/get_deprecated_kho_hom_vol_stat.json`](json/get_deprecated_kho_hom_vol_stat.json)
- [`json/get_deprecated_kho_hom_vol_non_prime_stat.json`](json/get_deprecated_kho_hom_vol_non_prime_stat.json)

They must not be used as evidence of topological discrimination.

### Pairwise tolerance experiment

The script compares all

\[
\binom{801}{2} = 320{,}400
\]

unordered pairs of distinct prime-knot base names. With the historical
tolerance `abs(v1 - v2) < 1e-4`, 45 pairs collide. These are numerical
collisions, not cases where the knots were “incorrectly proved equal.” The
experiment shows that the stored values separate most pairs in this finite
sample, but it does not make volume a complete knot invariant.

Tolerance closeness is reflexive and symmetric but not transitive, so it does
not define equivalence classes. The code therefore also records a separate
descriptive binning experiment by formatting values to three decimal places.
That produces 749 bins:

| Bin size | Number of bins |
| ---: | ---: |
| 1 | 703 |
| 2 | 44 |
| 3 | 1 |
| 7 | 1 |

The seven-entry bin is the near-zero/non-hyperbolic group. Decimal binning is
transitive because equal formatted strings form classes, but results near a
rounding boundary are sensitive to numerical error. Details are in
[`json/get_col_stat2.json`](json/get_col_stat2.json).

## Chirality experiment

Among the 781 committed chiral prime-knot pairs:

- Khovanov homology differs for 777 pairs and collides for 4:
  `K10a104`, `K10a48`, `K10a71`, and `K10a91`.
- The HOMFLY-PT polynomial differs for 773 pairs and collides for 8:
  `K10a104`, `K10a48`, `K10a71`, `K10a91`, `K10n2`, `K11n24`, `K11n82`, and
  `K9n1`.
- Every mirror pair has equal recorded volume within `1e-4`, as expected.

Thus every mirror pair separated by HOMFLY-PT in this dataset is also
separated by the stored Khovanov homology. The statement is deliberately
limited to these 781 pairs and these encodings.

## Reproduce the analysis

Python 3.10 or newer is sufficient; no third-party package is needed.

```bash
python reader.py
python -m unittest discover -s tests -v
```

The 12 summary lines should match [`reader_log.txt`](reader_log.txt), and the
JSON outputs should remain unchanged. Paths are resolved relative to this
repository without changing the caller's working directory.

No PyPI publishing step is part of this project.

## Citation

If you use this repository in academic work, please cite it as:

```bibtex
@software{topologicalknotindexer_conflict_lab,
  author = {{GGN\_2015}},
  title = {{conflict\_lab}},
  year = {2026},
  url = {https://github.com/TopologicalKnotIndexer/conflict_lab}
}
```
