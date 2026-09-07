# CCOC current theorem and proof spine — 2026-09-07

CCOC has one current publication spine. This document lists only the present CORE-1–CORE-5 proof dependencies. Historical non-nested replacement, mechanism-uncertainty, evidence-design, feedback, ecological special-case, and other removed branches are not part of the current CCOC theorem chain.

## 1. CORE-1 — canonical exact dynamic interface

For a declared finite deterministic controlled system and legal grammar, define two states as equivalent when every legal finite word gives the same output trace.

The canonical response quotient is the coarsest exact deterministic interface.

### Proof source

`docs/dynamic_boundary_blankets.md` proves:

1. finite counterfactual-horizon stabilization;
2. right-congruence / dynamic-interface completeness;
3. finite dynamic-blanket upper bounds; and
4. the uniform blanket obstruction when combined with addressability.

The executable implementations are `dynamic_boundary_blankets.py`, `grammar_aware_blankets.py`, and `shared_grammar.py`.

This is foundational substrate. The current novelty claim does not rest on generic fixed-grammar minimization.

---

## 2. CORE-2 — cross-grammar extension–compression lower bound

Let a declared comparison family contain a jointly realizable product

\[
I\times E_1\times\cdots\times E_q.
\]

If legal future words decode the inside coordinate and every exterior coordinate, then every two distinct product states are separated by a legal future trace. Therefore

\[
K_{\mathrm{open}}
\ge
\log_2|I|+\sum_j\log_2|E_j|.
\]

If closed context `j` admits a supplied exact factorization through `(I,E_j)`, then

\[
K_{\mathrm{closed},j}
\le
\log_2|I|+\log_2|E_j|,
\]

and hence

\[
\boxed{
K_{\mathrm{open}}-\max_jK_{\mathrm{closed},j}
\ge
\sum_j\log_2|E_j|-\max_j\log_2|E_j|.
}
\]

### Proof source

- `docs/extension_compression_noncommutation.md`
- `docs/portability_core_v1.md`
- executable injection certificate in `causal_model/extension_compression_noncommutation.py`.

The proof is an operational injection using declared decoder words, not an arithmetic assumption that independent memory contributions always add.

---

## 3. CORE-3 — bounded-local extremal sharpness

For every `m>=1`, the fixed-regular binary relay family has

\[
|P_C|=2,
\qquad
|P_O|=2^{m+1},
\qquad
K_O-K_C=m,
\]

under one fixed four-symbol primitive alphabet, with opening adding one primitive action, while the interaction graph remains a degree-at-most-three tree with one-edge focal/exterior cut and bounded local alphabets.

### Binary fixed-regular proof source

`docs/fixed_regular_extremal_theorem_2026-08-13.md` gives the all-`m` terminal-leaf proof:

1. fixed grammar and total local dynamics;
2. closed all-word invariant;
3. legal addressability of every exterior coordinate;
4. discreteness of the open quotient;
5. exact capacity sharpness;
6. bounded locality and one-edge cut; and
7. exact terminal-leaf binary query length
   \[
   2\lceil\log_2m\rceil+2.
   \]

Executable `certify_fixed_regular_extremal_theorem(m)` checks one finite supplied `m`; it is not the quantified proof itself.

### Strong bounded query arity theorem

The explicit `fire` action is an address delimiter, so a dormant coordinate need not sit at a terminal leaf. A relay-body node may both store one dormant bit and route later queries to descendants.

With at most `b` routing choices per selector step, the exact number of distinct memory-bearing selector positions through depth `h` is

\[
\boxed{
S_b(h)=\sum_{d=0}^{h}b^d
=
\begin{cases}
(b^{h+1}-1)/(b-1), & b\ge2,\\
h+1, & b=1.
\end{cases}}
\]

Therefore the exact minimum worst selector depth for `m` dormant one-bit coordinates is

\[
\boxed{
H_b^*(m)=\min\{h:S_b(h)\ge m\}.
}
\]

For `b>=2`,

\[
\boxed{
H_b^*(m)=
\left\lceil\log_b((b-1)m+1)\right\rceil-1,
}
\]

while

\[
\boxed{H_1^*(m)=m-1.}
\]

A query to depth `d` costs exactly `d` route actions, one `fire`, and `d+1` return ticks. Hence

\[
\boxed{L_b^*(m)=2H_b^*(m)+2.}
\]

Equivalently,

\[
\boxed{
L_b^*(m)=2\left\lceil\log_b((b-1)m+1)\right\rceil
\quad(b\ge2),
}
\]

and `L_1^*(m)=2m`.

In inverse form, a worst query budget `L>=2` permits exactly

\[
\boxed{
\iota_{\rm new}^{\max}(b,L)
=S_b\!\left(\left\lfloor\frac{L-2}{2}\right\rfloor\right)
}
\]

independently recoverable one-bit dormant coordinates in this selector-pulse class. With the focal bit included, the maximum open quotient size is `2^(1+iota_new^max)`.

A bound on `b` alone does **not** bound interface inflation: allowing query depth to grow makes `S_b(h)` unbounded for every fixed `b>=1`.

The matching trie has outdegree at most `b`, undirected degree at most `b+1`, one-edge focal/exterior cut, at most 12 selector-augmented local body states, and a three-symbol pulse alphabet. The action alphabet has size `b+2` for each fixed `b`.

Proof: `docs/bounded_query_arity_sharp_extremal_2026-09-07.md`.

Executable surface: `causal_model/bounded_query_arity.py`, with `certify_bounded_query_arity_extremal(m, b)` and `maximum_innovation_bits_for_query_budget(b, L)`.

### Terminal-leaf compatibility corollary

If dormant coordinates are additionally restricted to terminal leaves, Kraft/prefix-freeness gives instead

\[
H_{b,\mathrm{leaf}}^*(m)=\lceil\log_bm\rceil,
\qquad
L_{b,\mathrm{leaf}}^*(m)=2\lceil\log_bm\rceil+2
\]

for `b>=2`. This recovers the existing binary fixed-regular query theorem at `b=2`. For `b=1`, the terminal-leaf subclass can address only one leaf, whereas the stronger memory-bearing-node class supports an arbitrary unary chain.

The exact coefficients above are scoped to the declared selector + `fire` + radius-one-return architecture. They are not claimed for arbitrary bounded-local, adaptive, parallel, or richer-state query systems; the broader causal-cone theorem supplies only an architecture-agnostic order-level obstruction.

CORE-3 is sharpness support for CORE-2, not a second independent headline lower bound.

---

## 4. CORE-4 — positive conservative portability boundary

CCOC retains a positive boundary showing when a finite macro-law can remain exact across declared nested extension.

### Coherent portability

If every stage factors through one common finite macro dynamics and embeddings preserve macro labels, the stage laws are compatible restrictions of one portable law.

Proof: `docs/coherent_portable_macrolaw.md`.

### Conservative legal-action expansion

If legal action rows grow monotonically, old action meanings never change, and each newly legal action has one label-deterministic successor inside a macro fiber, the union grammar carries one finite conservative macro schema.

Proof: `docs/conservative_macro_schema.md`.

These are sufficient positive criteria. They are not the unique source-relative repair problem of MLTR.

---

## 5. CORE-5 — local future-word/new-action obstruction

If two states in one proposed macro fiber are separated by a later legal word or newly legal action, the proposed merge cannot be exact.

The proof is immediate from deterministic factorization: one quotient state cannot carry two distinct future traces or two different quotient successors under the same legal action.

Proof/witness sources are the CORE-4 documents and modules.

CORE-5 is a local warning. It does not by itself yield the global memory lower bound of CORE-2 or the unique coarsest inherited-law repair of MLTR.

---

## 6. Dependency graph

```text
CORE-1  canonical exact interface
   |
   +--> CORE-2  operational cross-grammar lower bound  [headline]
   |        |
   |        +--> CORE-3  bounded-local equality/sharpness witness
   |                  +--> exact node-addressed bounded-query-arity extremum
   |                  +--> terminal-leaf/Kraft compatibility corollary
   |
   +--> CORE-4  positive sufficient portability boundary
            |
            +--> CORE-5  concrete local obstruction when a proposed fiber is split
```

The first-paper story is therefore not a catalogue of quotient theorems. It is one structural contrast:

\[
\boxed{
\text{small exact interfaces in closed futures}
\not\Rightarrow
\text{one comparably small exact interface for an open future grammar},
}
\]

with a sharp bounded-local witness and a separate positive boundary showing when portability can hold.

---

## 7. Proof/replay rule

A quantified analytic theorem must have a written proof source. Finite certificates, tests, and replay artifacts are implementation guards and witnesses; they do not replace the quantified proof.

The executable registry `docs/theorem_registry.json` remains the current machine-readable inventory. `docs/claim_status_audit.md` records the current proof status and non-claims. Historical theorem truth remains available through Git history and the historical archive, not through this current proof spine.
