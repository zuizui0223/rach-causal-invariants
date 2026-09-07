# Sharp bounded-query-arity extremum — 2026-09-07

> **Status:** exact analytic strengthening of the query-latency layer of CORE-3. The theorem is sharp inside the declared prefix-selector + fire + radius-one return-pulse architecture class. It is not a claim that the exact coefficient below holds for every bounded-local controlled system.

## 1. Architecture class

Fix integers

\[
m\ge 1,
\qquad
b\ge 1.
\]

There are \(m\) terminal exterior memory leaves, one permanent bit \(b_j\) per leaf, and one focal output bit \(y\). A query begins with the selector at the relay-body root.

A legal selector step has at most \(b\) routing choices. Every memory leaf \(j\) therefore has an address

\[
a_j\in\Sigma_b^*,
\qquad
|\Sigma_b|=b,
\]

and the terminal addresses are prefix-free. After the address, one `fire` action emits the selected permanent bit as a pulse. Radius-one return propagation then moves that pulse one parent edge per `tick` until it reaches the focal root. The focal node is separated from the entire relay body by one extra edge.

For a leaf of selector depth \(d_j=|a_j|\), the canonical probe is

\[
w_j=a_j\,\mathsf{fire}\,\mathsf{tick}^{d_j+1},
\]

so its exact length is

\[
|w_j|=2d_j+2.
\]

For fixed \(b\), the common primitive action alphabet has size \(b+2\): \(b\) route symbols, `fire`, and `tick`. The closed grammar loops on the route symbols and `tick`; the open grammar adds the single missing `fire` loop. Thus opening still changes exactly one one-state-DFA transition.

---

## 2. Theorem — exact minimax selector depth

For \(b\ge2\), among all prefix-free terminal address families for \(m\) leaves with routing arity at most \(b\), the minimum possible maximum selector depth is

\[
\boxed{
H_b^*(m)=\left\lceil\log_b m\right\rceil.
}
\]

### Lower bound

Let

\[
h=\max_j |a_j|.
\]

Because the addresses are prefix-free, Kraft's inequality gives

\[
\sum_{j=1}^m b^{-|a_j|}\le1.
\]

Since every \(|a_j|\le h\),

\[
b^{-|a_j|}\ge b^{-h},
\]

and therefore

\[
m b^{-h}\le1.
\]

Hence

\[
m\le b^h,
\qquad
h\ge\log_bm,
\]

so integer depth forces

\[
h\ge\lceil\log_bm\rceil.
\]

The same inequality can be read directly as the leaf-capacity bound for a rooted tree of outdegree at most \(b\).

### Matching construction

Set

\[
h=\lceil\log_bm\rceil.
\]

There are \(b^h\ge m\) words of length exactly \(h\) over \(\Sigma_b\). Choose any \(m\) of them and use their prefix trie as the relay body. All selected terminal addresses have length \(h\), are prefix-free, and every trie node has at most \(b\) children. Thus

\[
\max_j|a_j|=h.
\]

The lower and upper bounds coincide. \(\square\)

---

## 3. Corollary — exact sharp worst query length

For \(b\ge2\), every prefix-selector pulse realization in this class obeys

\[
L_{\rm query}^{\rm worst}
\ge
2\lceil\log_bm\rceil+2.
\]

The fixed-length \(b\)-ary construction above attains equality because every deepest query uses exactly

\[
h\text{ route steps}
+1\text{ fire}
+(h+1)\text{ return ticks}.
\]

Therefore

\[
\boxed{
L_{b}^{*}(m)
=
2\left\lceil\log_bm\right\rceil+2.
}
\]

This is an exact minimax equality, not merely \(\Theta(\log m)\).

For \(b=2\), it recovers the existing fixed-regular binary result

\[
L_2^*(m)=2\lceil\log_2m\rceil+2.
\]

---

## 4. Unary boundary \(b=1\)

A unary alphabet contains only the words

\[
\epsilon,0,00,000,\ldots,
\]

which are totally ordered by the prefix relation. Hence a prefix-free set can contain at most one terminal address.

Therefore:

- if \(m=1\), the unique leaf may sit at selector depth zero and
  \[
  L_1^*(1)=2;
  \]
- if \(m>1\), no terminal prefix-selector realization with query arity one exists.

So the \(b=1\) case is not obtained by substituting into \(\log_bm\); it is a separate feasibility boundary.

---

## 5. Sharp inverse form — maximum innovation under a query budget

The equality can be inverted. Let every exterior leaf store one binary response coordinate and let the worst allowed canonical query length be \(L\).

A leaf at selector depth \(h\) requires

\[
2h+2\le L,
\]

so

\[
h\le\left\lfloor\frac{L-2}{2}\right\rfloor.
\]

For \(L\ge2\) and \(b\ge2\), at most

\[
b^{\left\lfloor(L-2)/2\right\rfloor}
\]

terminal coordinates can be addressed. A full \(b\)-ary depth-\(h\) tree attains this count exactly. Since each leaf contributes one independently recoverable dormant bit, the maximum open-only innovation in this architecture is therefore

\[
\boxed{
\iota_{\rm new}^{\max}(b,L)
=
b^{\left\lfloor(L-2)/2\right\rfloor}
\quad(L\ge2,b\ge2).
}
\]

For \(L<2\), no terminal bit can be queried by this protocol, so the maximum is zero. For \(b=1\), the maximum is one bit for every \(L\ge2\).

This inverse statement is the sharp bounded-query-arity extremum: a fixed query-depth budget gives an exact cap on how many independently recoverable one-bit exterior coordinates the selector-pulse architecture can expose.

---

## 6. Interface-memory sharpness is unchanged

Use the comparison domain

\[
D_m=\{0,1\}^{m+1}
=\{(y,b_1,\ldots,b_m)\}.
\]

Exactly as in the binary fixed-regular proof, the closed grammar cannot create a pulse because `fire` is illegal. Thus every closed trace depends only on \(y\), giving

\[
|P_C|=2,
\qquad
K_C=1.
\]

After opening, each exterior coordinate \(b_j\) has its legal decoder word \(w_j\). Distinct states with equal \(y\) differ in some \(b_j\) and are separated by the corresponding query, while unequal \(y\) are separated by the current output. Hence

\[
|P_O|=2^{m+1},
\qquad
K_O=m+1.
\]

Therefore

\[
\boxed{
K_O-K_C=m,
}
\]

which still attains the absolute finite-domain memory upper bound. Query arity changes the minimum access latency, not the attainable exact memory inflation.

---

## 7. Locality resources

The matching construction is a trie whose relay-body outdegree is at most \(b\). Adding the unique parent edge gives undirected graph degree at most

\[
\boxed{b+1}.
\]

The focal/exterior cut remains one edge. For fixed \(b\), all structural resource bounds are independent of \(m\). The pulse/message alphabet can remain \(\{\varnothing,0,1\}\), and the selector augmentation needs only a selected/unselected flag on the same finite relay and leaf states; the dynamic state alphabet therefore need not grow with \(m\).

The action alphabet does contain the \(b\) routing symbols, so it has size \(b+2\). Thus the theorem should be read as a family indexed by a fixed query-arity bound \(b\), not as one action alphabet simultaneously independent of both \(m\) and \(b\).

---

## 8. Exact scope and non-claim

The exact coefficient

\[
2\lceil\log_bm\rceil+2
\]

is proved for the declared prefix-selector + one-fire + radius-one-return architecture. It should **not** be promoted to a universal exact latency theorem for every deterministic bounded-local network of degree \(b+1\) or every conceivable adaptive query protocol.

The broader CCOC causal-cone result supports only an order lower bound under bounded degree and bounded local state. The present result closes the sharper minimax problem after the query architecture itself is fixed.

Accordingly, the safe claim is:

\[
\boxed{
\text{exact bounded-arity extremum within the canonical selector-pulse realization class.}
}
\]

A genuinely universal exact coefficient would require a separate lower bound covering arbitrary encodings, adaptive routing, internal aggregation, and non-prefix query semantics.

---

## 9. Executable certificate

The finite replay/consistency surface is

```python
from causal_model.bounded_query_arity import (
    certify_bounded_query_arity_extremal,
    maximum_innovation_bits_for_query_budget,
)

cert = certify_bounded_query_arity_extremal(module_count=m, query_arity=b)
assert cert.verify()
assert cert.selector_depth == cert.lower_bound_selector_depth
assert cert.worst_query_length == 2 * cert.selector_depth + 2
assert cert.open_only_innovation_bits == m
assert cert.innovation_slack_bits == 0
```

The certificate checks the finite prefix code, exact Kraft sum, grammar edit, trie arity, graph-degree bound, sharp selector depth, sharp query length, and finite-domain memory equality for one supplied \((m,b)\). It does not replace the quantified proof above.
