# Sharp bounded-query-arity extremum — 2026-09-07

> **Status:** exact analytic strengthening of the query-latency layer of CORE-3. The strongest theorem below is sharp inside the declared selector + explicit `fire` delimiter + radius-one return-pulse architecture with one dormant binary response coordinate per memory-bearing selector node. A stricter terminal-leaf/Kraft theorem is retained as a compatibility corollary. Neither exact coefficient is claimed for arbitrary bounded-local or adaptive controlled systems.

## 1. Why terminal prefix-freeness is not fundamental

The binary fixed-regular relay placed dormant bits only at terminal leaves. That makes its selector addresses prefix-free and leads naturally to Kraft's inequality.

But the open grammar contains an explicit action

\[
\mathsf{fire}
\]

that terminates routing and requests the currently selected memory. Hence an address may be a prefix of another address without ambiguity. For example, with binary routing,

\[
\epsilon,\quad 0,\quad 00
\]

can identify three different memory-bearing body nodes: fire immediately at the body root, route once then fire, or route twice then fire.

Therefore the true selector-pulse extremum counts **all selectable body nodes through a depth**, not only terminal leaves at that depth.

---

## 2. Architecture class

Fix integers

\[
m\ge1,
\qquad
b\ge1.
\]

The network contains one focal output node `ROOT` and an exterior rooted relay body attached to it by one edge. The relay body has outdegree at most \(b\). Each of \(m\) declared memory-bearing body nodes stores one permanent binary coordinate. A body node may simultaneously be a relay and a memory site.

A query begins with the selector at the relay-body root. At each selector step there are at most \(b\) routing choices, represented by an alphabet

\[
\Sigma_b=\{0,1,\ldots,b-1\}.
\]

A memory site \(j\) has a distinct route address

\[
a_j\in\Sigma_b^*.
\]

The physical selected-node set is prefix-closed: whenever a non-root node occurs, its parent route prefix occurs as a body node. Memory addresses themselves need not be prefix-free.

After the route address, one `fire` action emits the permanent bit at the selected node as a pulse. Starting from a quiescent comparison state, the canonical query has no competing pulse. Radius-one return propagation moves the emitted bit one parent edge per `tick` until it reaches the focal node.

If a selected body node has selector depth

\[
d=|a_j|,
\]

its graph distance to the focal `ROOT` is \(d+1\), and the canonical probe is

\[
w_j
=
a_j\,\mathsf{fire}\,\mathsf{tick}^{d+1}.
\]

Hence

\[
\boxed{|w_j|=2d+2.}
\]

For fixed \(b\), the common primitive action alphabet has size \(b+2\): the \(b\) routing symbols, `fire`, and `tick`. The one-state closed grammar loops on routing and `tick`; the one-state open grammar adds exactly the single missing `fire` loop. Thus opening changes one grammar transition while the plant rule remains fixed.

---

## 3. Selector-word capacity

Let \(h\) be the maximum allowed selector depth. There are at most \(b^d\) route words of length exactly \(d\). Therefore the number of distinct selectable positions representable by route words of length at most \(h\) is at most

\[
S_b(h)
=
\sum_{d=0}^{h} b^d.
\]

Thus

\[
\boxed{
S_b(h)=
\begin{cases}
\dfrac{b^{h+1}-1}{b-1}, & b\ge2,\\[6pt]
h+1, & b=1.
\end{cases}}
\]

This is a pure counting upper bound: even if an implementation uses merging paths or cycles, it cannot associate more than one independently selected target with each distinct route word unless extra addressing information beyond the declared \(b\)-ary route sequence is introduced.

The bound is attained by the full rooted \(b\)-ary trie through depth \(h\), with one dormant bit at every body node. For \(b=1\), the matching object is a chain of \(h+1\) memory-bearing nodes.

Therefore \(S_b(h)\) is the exact selector-position capacity.

---

## 4. Theorem — exact minimax depth for \(m\) dormant bits

Let

\[
H_b^*(m)
\]

denote the minimum possible maximum selector depth among the declared one-bit-per-selected-node realizations.

The capacity bound implies that every realization of depth \(h\) must satisfy

\[
m\le S_b(h).
\]

Conversely, choose body nodes in breadth-first order from the full \(b\)-ary trie until \(m\) memory sites have been assigned. This set is prefix-closed, has outdegree at most \(b\), and reaches exactly the least depth for which \(S_b(h)\ge m\).

Hence

\[
\boxed{
H_b^*(m)
=
\min\{h\ge0:S_b(h)\ge m\}.
}
\]

For \(b\ge2\), solving the geometric-sum inequality gives

\[
\boxed{
H_b^*(m)
=
\left\lceil
\log_b\bigl((b-1)m+1\bigr)
\right\rceil-1.
}
\]

For unary routing,

\[
\boxed{H_1^*(m)=m-1.}
\]

The lower bound and construction coincide, so this is an exact minimax theorem. \(\square\)

---

## 5. Corollary — exact worst query length

A deepest selected node at depth \(H_b^*(m)\) needs exactly

\[
H_b^*(m)
+1
+(H_b^*(m)+1)
=
2H_b^*(m)+2
\]

actions: route, fire, and return.

Therefore

\[
\boxed{
L_b^*(m)=2H_b^*(m)+2.
}
\]

Equivalently, for \(b\ge2\),

\[
\boxed{
L_b^*(m)
=
2\left\lceil
\log_b\bigl((b-1)m+1\bigr)
\right\rceil,
}
\]

and for \(b=1\),

\[
\boxed{L_1^*(m)=2m.}
\]

This is exact, including the coefficient and additive term, inside the declared selector-pulse architecture.

### Binary examples

For \(b=2\), selector capacities by depth are

\[
1,3,7,15,\ldots
\]

and

\[
L_2^*(m)=2\lceil\log_2(m+1)\rceil.
\]

Thus \(m=3\) dormant bits need worst query length only \(4\), whereas the terminal-leaf binary relay needs \(6\). The improvement comes entirely from allowing the body root and internal relays to carry the same one-bit dormant memory.

---

## 6. Sharp inverse extremum under a query budget

Now fix a worst canonical query budget \(L\).

For \(L<2\), no dormant exterior bit can emit a pulse and return to the focal node, so

\[
\iota_{\rm new}^{\max}(b,L)=0.
\]

For \(L\ge2\), the deepest selectable memory site can have depth at most

\[
h_L
=
\left\lfloor\frac{L-2}{2}\right\rfloor.
\]

The exact selector-position capacity is therefore \(S_b(h_L)\). Because the full/truncated trie construction assigns one independently recoverable dormant bit to every selected body node, this upper bound is attained.

Hence

\[
\boxed{
\iota_{\rm new}^{\max}(b,L)
=
S_b\!\left(\left\lfloor\frac{L-2}{2}\right\rfloor\right)
\qquad(L\ge2).
}
\]

For \(b\ge2\),

\[
\boxed{
\iota_{\rm new}^{\max}(b,L)
=
\frac{
 b^{\left\lfloor(L-2)/2\right\rfloor+1}-1
}{b-1}.
}
\]

For \(b=1\),

\[
\boxed{
\iota_{\rm new}^{\max}(1,L)
=
\left\lfloor\frac{L}{2}\right\rfloor.
}
\]

If the focal bit is also allowed to vary, the corresponding maximum exact open quotient size is

\[
\boxed{
|P_O|_{\max}
=
2^{1+\iota_{\rm new}^{\max}(b,L)}.
}
\]

This is the sharp finite extremum requested by a simultaneous **routing-arity bound \(b\)** and **worst query-length budget \(L\)** in the declared architecture.

---

## 7. Bounded arity alone does not bound interface inflation

For every fixed \(b\ge1\), the depth \(h\) may grow. Consequently

\[
S_b(h)\to\infty
\]

and the construction exposes arbitrarily many dormant bits while keeping routing arity fixed.

Thus

\[
\boxed{
\sup (K_O-K_C)=\infty
\quad\text{under a bound on }b\text{ alone}.
}
\]

A finite sharp maximum appears only after a finite access/query budget (or another size/horizon resource) is imposed.

---

## 8. Exact interface-memory equality for every \(m\)

Use comparison domain

\[
D_m
=
\{0,1\}^{m+1}
=
\{(y,b_1,\ldots,b_m)\}.
\]

In a quiescent comparison state, routing actions move only the selector and `tick` propagates only existing pulses. Since `fire` is illegal in the closed grammar, no pulse can be created by any closed word. Therefore every closed output trace depends only on the initial focal bit \(y\):

\[
|P_C|=2,
\qquad
K_C=1.
\]

After opening, every memory-bearing body node \(j\) has its legal word

\[
w_j=a_j\,\mathsf{fire}\,\mathsf{tick}^{|a_j|+1}
\]

whose final focal output is \(b_j\). If two states have different focal bits, current output separates them. If their focal bits agree but the states differ, some dormant coordinate \(b_j\) differs and \(w_j\) separates them. Thus the open quotient is discrete:

\[
|P_O|=2^{m+1},
\qquad
K_O=m+1.
\]

Hence

\[
\boxed{K_O-K_C=m.}
\]

This reaches the absolute finite-domain upper bound. Changing query arity changes how quickly the dormant coordinates can be reached; it does not reduce the attainable exact memory inflation when query length is allowed to grow.

---

## 9. Locality/resource accounting

The matching body is a rooted trie of outdegree at most \(b\). Every body node has one parent edge, including the body root's edge to focal `ROOT`, so the undirected degree is at most

\[
\boxed{b+1.}
\]

Removing the one `ROOT`--body-root edge disconnects the focal node from every dormant coordinate, so the focal/exterior cut stays

\[
\boxed{1.}
\]

A memory-bearing relay can use the fixed product state

\[
\text{permanent bit}
\times
\text{pulse }\{\varnothing,0,1\}
\times
\text{selector flag},
\]

which has at most

\[
2\cdot3\cdot2=12
\]

local states. The pulse/message alphabet has three symbols. These state and message bounds are independent of both \(m\) and \(b\); the graph degree and routing-action count depend on the fixed arity parameter \(b\).

For fixed \(b\), the action alphabet has size \(b+2\). Thus this is a uniform-in-\(m\) family for each fixed arity bound \(b\), not one primitive alphabet simultaneously independent of \(b\).

---

## 10. Terminal-leaf compatibility theorem

If one adds the extra restriction that **only terminal leaves may store dormant coordinates**, then the selected addresses must be prefix-free. Kraft's inequality applies:

\[
\sum_{j=1}^{m} b^{-|a_j|}\le1.
\]

For \(b\ge2\), if \(h=\max_j|a_j|\), then

\[
m b^{-h}\le1,
\]

so

\[
\boxed{
H_{b,\mathrm{leaf}}^*(m)
=
\lceil\log_bm\rceil.
}
\]

Choosing \(m\) fixed-length words at that depth attains equality, and therefore

\[
\boxed{
L_{b,\mathrm{leaf}}^*(m)
=
2\lceil\log_bm\rceil+2.
}
\]

For \(b=2\), this exactly recovers the existing fixed-regular relay theorem.

For \(b=1\), unary words are totally ordered by prefix, so a prefix-free terminal set can contain at most one address: \(m=1\) has query length 2 and \(m>1\) is infeasible in the terminal-leaf subclass. This does **not** contradict the stronger node-addressed theorem, where a unary chain can carry one dormant bit at every node and achieves \(L_1^*(m)=2m\).

The terminal-leaf theorem is therefore a correct sharp result for the old architecture, but not the sharp result for the larger selector-pulse class.

---

## 11. Exact scope and non-claims

The strong counting theorem assumes:

1. route selection is encoded by a word with at most \(b\) choices per selector step;
2. one independently variable dormant binary coordinate is attached to each selected body node;
3. `fire` explicitly terminates the address and emits only the selected coordinate;
4. return propagation is radius one, costing one action per parent edge; and
5. the query begins from the declared root-selector/quiescent macro state.

Under these contracts, the node count, depth, latency, and budget extremum are exact.

It should **not** be promoted to a universal exact latency theorem for every bounded-degree network or every adaptive query protocol. Arbitrary encodings could use richer local states, parallelism, non-tree addressing, variable-output symbols, or different query/reset semantics. The broader CCOC causal-cone theorem remains the appropriate architecture-agnostic order-level obstruction.

The safe claim is

\[
\boxed{
\text{exact bounded-routing-arity extremum within the canonical selector-pulse class.}
}
\]

No historical firstness claim is made for rooted-tree counting, Kraft coding, or selector routing.

---

## 12. Executable certificates

The strongest finite certificate is

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

The terminal-leaf compatibility surface is

```python
from causal_model.bounded_query_arity import (
    certify_terminal_leaf_bounded_query_arity_extremal,
)

leaf_cert = certify_terminal_leaf_bounded_query_arity_extremal(m, b)
assert leaf_cert.verify()
```

The finite certificates check address construction, selector capacity, grammar edit, trie arity, graph-degree/cut bounds, exact depth/query formulas, and finite-domain memory equality at supplied parameters. They are replay/consistency objects; the quantified proofs are the analytic arguments above.
