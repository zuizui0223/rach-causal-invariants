# CCOC current executable theorem registry

Machine-readable current registry: [`theorem_registry.json`](theorem_registry.json).  
Historical theorem archive: [`historical_theorem_archive.md`](historical_theorem_archive.md) / [`historical_theorem_archive.json`](historical_theorem_archive.json).

CCOC is a **mathematical ecology** repository, not an empirical data repository. Read [the non-empirical scope policy](nonempirical_scope.md) before connecting a finite theorem to an ecological application.

A current registry entry means its source, tests, documentation, and replay route must exist **now**. Historical validity/provenance is tracked separately and does not force old source bundles to remain in the current tree.

## Current executable CCOC surface

| ID | CCOC role | Status | Primary source |
|---|---|---|---|
| `CORE-1` | foundation: exact grammar-aware dynamic interface | exact finite theorem | `causal_model/grammar_aware_blankets.py` |
| `CORE-2` | **headline: cross-grammar addressability / extension--compression lower bound** | lower-bound obstruction | `causal_model/extension_compression_noncommutation.py` |
| `CORE-3` | headline support: bounded-local extremal realization + sharp bounded-query-arity access | sharpness witness | `causal_model/extremal_open_composition.py` + `causal_model/bounded_query_arity.py` |
| `CORE-4` | supporting positive boundary only | sufficient criterion | `causal_model/coherent_portable_macrolaw.py`, `causal_model/conservative_macro_schema.py` |
| `CORE-5` | supporting local obstruction only | local obstruction | `causal_model/conservative_macro_schema.py` |

### `CORE-1`

For a supplied finite controlled system and action grammar, an exact interface preserves output, legal-action rows, and successor labels. Fixed-grammar minimization itself is classical substrate.

### `CORE-2`

Under declared joint realization and operational future separation, the open grammar may force a much finer **minimum exact response interface** than every supplied closed grammar. The closed optimum is allowed to depend on the closed grammar. This quantifier gap is the live CCOC structural/quantitative manuscript candidate.

### `CORE-3`

The explicit relay realizes the separation with bounded-local structure. The query-arity layer is now exact inside the canonical selector + explicit `fire` delimiter + radius-one return-pulse architecture with one dormant binary coordinate per selected body node.

With routing arity `b` and selector depth `h`, the exact number of selectable memory-bearing body positions is

\[
S_b(h)=\sum_{d=0}^{h}b^d.
\]

Hence the sharp depth is the least `h` with `S_b(h)>=m`. For `b>=2`,

\[
H_b^*(m)=\left\lceil\log_b((b-1)m+1)\right\rceil-1,
\]

and for `b=1`, `H_1^*(m)=m-1`. The exact worst canonical query length is

\[
L_b^*(m)=2H_b^*(m)+2.
\]

Thus for `b>=2`,

\[
L_b^*(m)=2\left\lceil\log_b((b-1)m+1)\right\rceil,
\]

while `L_1^*(m)=2m`.

With a worst query budget `L>=2`, the exact maximum number of independently recoverable dormant one-bit coordinates is

\[
\iota_{\rm new}^{\max}(b,L)
=S_b\!\left(\left\lfloor\frac{L-2}{2}\right\rfloor\right).
\]

A fixed arity bound alone does not cap the interface gap, because increasing query depth makes `S_b(h)` unbounded.

The stronger construction retains one-edge focal/exterior cut, degree at most `b+1`, at most 12 selector-augmented body states, a three-symbol pulse alphabet, and one newly legal `fire` grammar transition. The exact coefficient is architecture-specific and is not promoted to arbitrary bounded-local or adaptive query systems.

The old terminal-leaf relay remains as a stricter compatibility theorem: prefix-freeness/Kraft gives

\[
L_{b,\mathrm{leaf}}^*(m)=2\lceil\log_bm\rceil+2
\]

for `b>=2`, exactly recovering the existing binary fixed-regular theorem at `b=2`. Historical realization firstness remains separately controlled.

### `CORE-4`

A proposed finite macro law remains exact across the declared expansion when old meanings are coherent and newly available actions descend uniformly on each macro fiber. This is a supporting sufficient boundary for `CORE-2`, not a source-relative repair theorem.

### `CORE-5`

A future word or newly legal action that separates two states in one proposed macro fiber refutes that merge. It supports the obstruction picture but does not construct the unique coarsest repair of an inherited partition and does not rule out every alternative macro-law.

## Claim firewall against MLTR

CCOC owns the optimization gap

\[
\max_i\min_{q\text{ exact under }\Gamma_i}\log_2|q|
\quad\text{versus}\quad
\min_{q\text{ exact under }\Gamma_O}\log_2|q|,
\]

including lower bounds and bounded-local sharpness.

MLTR owns the different source-relative problem in which one accepted source law is fixed and the target solution must refine its carried labels. Unique coarsest repair, transport defect, route coherence, and minimum history completion are therefore **not CCOC headline claims**.

See [`ccoc_mltr_claim_firewall_2026-08-16.md`](ccoc_mltr_claim_firewall_2026-08-16.md).

## Historical results

`CORE-0`, `EXT-1`–`EXT-4`, `ID-1`–`ID-3`, and `LEGACY-1` no longer belong to the executable registry. Their theorem statements, former source paths, and immutable recovery pin are in the historical archive.

Moving an ID out of this file changes **repository maintenance status**, not theorem truth.