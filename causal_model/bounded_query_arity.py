"""Sharp bounded-query-arity extremal layer for the CCOC relay family.

This module isolates the part of the relay theorem that depends on routing/query
arity. For a fixed integer ``b >= 2``, a prefix-selector pulse probe uses:

* at most ``b`` routing choices at each selector step;
* one terminal memory leaf per exterior bit;
* one ``fire`` action after the address; and
* radius-one return propagation, one edge per ``tick``.

If a leaf has selector depth ``d``, its canonical query length is ``2*d + 2``.
The exact minimax selector depth over ``m`` terminal leaves is
``ceil(log_b(m))`` by the prefix-code/Kraft bound, and a fixed-length ``b``-ary
code attains equality. Therefore the exact minimax worst query length in this
declared architecture class is

    2 * ceil(log_b(m)) + 2.

The unary boundary is explicit: with ``b == 1`` a prefix-free terminal selector
can address only one leaf. Thus ``m == 1`` has depth zero and query length two,
while ``m > 1`` is infeasible.

The finite certificate below checks one supplied ``(m, b)`` construction. The
quantified proof lives in
``docs/bounded_query_arity_sharp_extremal_2026-09-07.md``.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable

from .shared_grammar import FinitePrefixGrammar

FIRE = "fire"
TICK = "tick"

Address = tuple[int, ...]
ProbeWord = tuple[str, ...]


def _validate_positive_integer(value: int, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def _validate_nonnegative_integer(value: int, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{name} must be a non-negative integer")


def route_action(symbol: int) -> str:
    _validate_nonnegative_integer(symbol, "symbol")
    return f"route:{symbol}"


def routing_actions(query_arity: int) -> tuple[str, ...]:
    _validate_positive_integer(query_arity, "query_arity")
    return tuple(route_action(symbol) for symbol in range(query_arity))


def bounded_query_action_alphabet(query_arity: int) -> tuple[str, ...]:
    return routing_actions(query_arity) + (FIRE, TICK)


def bounded_query_closed_grammar(query_arity: int) -> FinitePrefixGrammar:
    actions = bounded_query_action_alphabet(query_arity)
    row = tuple(0 for _ in range(query_arity)) + (None, 0)
    return FinitePrefixGrammar(actions=actions, transition_table=(row,))


def bounded_query_open_grammar(query_arity: int) -> FinitePrefixGrammar:
    actions = bounded_query_action_alphabet(query_arity)
    return FinitePrefixGrammar(
        actions=actions,
        transition_table=(tuple(0 for _ in actions),),
    )


def ceil_log_base(module_count: int, query_arity: int) -> int:
    """Return exact integer ``ceil(log_b(m))`` without floating point.

    ``m == 1`` returns zero for every positive ``b``. The unary case with
    ``m > 1`` is infeasible and therefore raises ``ValueError``.
    """
    _validate_positive_integer(module_count, "module_count")
    _validate_positive_integer(query_arity, "query_arity")
    if module_count == 1:
        return 0
    if query_arity == 1:
        raise ValueError("query_arity=1 cannot prefix-address more than one terminal leaf")

    depth = 0
    capacity = 1
    while capacity < module_count:
        capacity *= query_arity
        depth += 1
    return depth


def _fixed_width_base_word(index: int, width: int, base: int) -> Address:
    _validate_nonnegative_integer(index, "index")
    _validate_nonnegative_integer(width, "width")
    _validate_positive_integer(base, "base")
    if index >= base**width:
        raise ValueError("index does not fit in requested base/width")
    digits = [0] * width
    remainder = index
    for position in range(width - 1, -1, -1):
        digits[position] = remainder % base
        remainder //= base
    return tuple(digits)


def sharp_prefix_addresses(module_count: int, query_arity: int) -> tuple[Address, ...]:
    """Return a prefix-free address family attaining the minimax depth."""
    depth = ceil_log_base(module_count, query_arity)
    if module_count == 1:
        return ((),)
    return tuple(
        _fixed_width_base_word(index, depth, query_arity)
        for index in range(module_count)
    )


def is_prefix_free(addresses: Iterable[Address]) -> bool:
    normalized = tuple(tuple(address) for address in addresses)
    if len(set(normalized)) != len(normalized):
        return False
    for left_index, left in enumerate(normalized):
        for right_index, right in enumerate(normalized):
            if left_index == right_index:
                continue
            if len(left) <= len(right) and right[: len(left)] == left:
                return False
    return True


def kraft_sum(addresses: Iterable[Address], query_arity: int) -> Fraction:
    """Return the exact Kraft sum for a candidate prefix code."""
    _validate_positive_integer(query_arity, "query_arity")
    normalized = tuple(tuple(address) for address in addresses)
    if query_arity == 1:
        return Fraction(len(normalized), 1)
    return sum(
        (Fraction(1, query_arity ** len(address)) for address in normalized),
        start=Fraction(0, 1),
    )


def canonical_probe_word(address: Address) -> ProbeWord:
    """Encode selector descent, one fire, and one-edge-per-tick return."""
    normalized = tuple(address)
    for symbol in normalized:
        _validate_nonnegative_integer(symbol, "address symbol")
    return (
        tuple(route_action(symbol) for symbol in normalized)
        + (FIRE,)
        + (TICK,) * (len(normalized) + 1)
    )


def maximum_addressable_leaves(query_arity: int, selector_depth: int) -> int:
    """Sharp number of terminal leaves addressable with max selector depth."""
    _validate_positive_integer(query_arity, "query_arity")
    _validate_nonnegative_integer(selector_depth, "selector_depth")
    if query_arity == 1:
        return 1
    return query_arity**selector_depth


def maximum_innovation_bits_for_query_budget(query_arity: int, query_budget: int) -> int:
    """Sharp innovation-bit capacity of this one-bit-per-leaf architecture.

    A canonical probe at selector depth ``d`` has length ``2*d+2``. Hence a
    budget below two cannot address a terminal memory leaf. For larger budgets
    the maximum feasible depth is ``floor((L-2)/2)``.
    """
    _validate_positive_integer(query_arity, "query_arity")
    _validate_nonnegative_integer(query_budget, "query_budget")
    if query_budget < 2:
        return 0
    selector_depth = (query_budget - 2) // 2
    return maximum_addressable_leaves(query_arity, selector_depth)


def _trie_child_counts(addresses: tuple[Address, ...]) -> tuple[int, ...]:
    children: dict[Address, set[int]] = {}
    for address in addresses:
        for depth, symbol in enumerate(address):
            prefix = address[:depth]
            children.setdefault(prefix, set()).add(symbol)
    return tuple(len(values) for values in children.values())


@dataclass(frozen=True)
class BoundedQueryArityExtremalCertificate:
    """Finite ``(m,b)`` certificate for the exact prefix-selector extremum."""

    module_count: int
    query_arity: int
    addresses: tuple[Address, ...]

    @property
    def selector_depth(self) -> int:
        return max(len(address) for address in self.addresses)

    @property
    def lower_bound_selector_depth(self) -> int:
        return ceil_log_base(self.module_count, self.query_arity)

    @property
    def worst_query_length(self) -> int:
        return max(len(canonical_probe_word(address)) for address in self.addresses)

    @property
    def exact_worst_query_formula(self) -> int:
        return 2 * self.lower_bound_selector_depth + 2

    @property
    def action_alphabet(self) -> tuple[str, ...]:
        return bounded_query_action_alphabet(self.query_arity)

    @property
    def closed_grammar(self) -> FinitePrefixGrammar:
        return bounded_query_closed_grammar(self.query_arity)

    @property
    def open_grammar(self) -> FinitePrefixGrammar:
        return bounded_query_open_grammar(self.query_arity)

    @property
    def newly_legal_action_count(self) -> int:
        return len(
            set(self.open_grammar.legal_actions(0))
            - set(self.closed_grammar.legal_actions(0))
        )

    @property
    def grammar_transition_difference_count(self) -> int:
        return sum(
            closed_target != open_target
            for closed_target, open_target in zip(
                self.closed_grammar.transition_table[0],
                self.open_grammar.transition_table[0],
                strict=True,
            )
        )

    @property
    def closed_interface_state_count(self) -> int:
        return 2

    @property
    def open_interface_state_count(self) -> int:
        return 2 ** (self.module_count + 1)

    @property
    def open_only_innovation_bits(self) -> int:
        return self.module_count

    @property
    def finite_domain_maximum_innovation_bits(self) -> int:
        return self.module_count

    @property
    def innovation_slack_bits(self) -> int:
        return self.finite_domain_maximum_innovation_bits - self.open_only_innovation_bits

    @property
    def maximum_trie_outdegree(self) -> int:
        counts = _trie_child_counts(self.addresses)
        return max(counts, default=0)

    @property
    def maximum_graph_degree_bound(self) -> int:
        # Every non-focal trie node has one parent plus at most b children.
        return max(1, self.maximum_trie_outdegree + 1)

    @property
    def focal_exterior_cut_width(self) -> int:
        return 1

    @property
    def kraft_sum(self) -> Fraction:
        return kraft_sum(self.addresses, self.query_arity)

    def verify(self) -> bool:
        try:
            _validate_positive_integer(self.module_count, "module_count")
            _validate_positive_integer(self.query_arity, "query_arity")
            if self.query_arity == 1 and self.module_count > 1:
                return False
            if len(self.addresses) != self.module_count:
                return False
            if not is_prefix_free(self.addresses):
                return False
            if any(
                symbol >= self.query_arity
                for address in self.addresses
                for symbol in address
            ):
                return False
            if self.kraft_sum > 1:
                return False
            if self.selector_depth != self.lower_bound_selector_depth:
                return False
            if self.worst_query_length != self.exact_worst_query_formula:
                return False
            if self.maximum_trie_outdegree > self.query_arity:
                return False
            if self.maximum_graph_degree_bound > self.query_arity + 1:
                return False
            if self.closed_grammar.state_count != 1 or self.open_grammar.state_count != 1:
                return False
            if self.closed_grammar.actions != self.action_alphabet:
                return False
            if self.open_grammar.actions != self.action_alphabet:
                return False
            if FIRE in self.closed_grammar.legal_actions(0):
                return False
            if FIRE not in self.open_grammar.legal_actions(0):
                return False
            if self.newly_legal_action_count != 1:
                return False
            if self.grammar_transition_difference_count != 1:
                return False
            if self.closed_interface_state_count != 2:
                return False
            if self.open_interface_state_count != 2 ** (self.module_count + 1):
                return False
            if self.open_only_innovation_bits != self.module_count:
                return False
            if self.innovation_slack_bits != 0:
                return False
            return True
        except (TypeError, ValueError):
            return False


def certify_bounded_query_arity_extremal(
    module_count: int,
    query_arity: int,
) -> BoundedQueryArityExtremalCertificate:
    """Construct and verify one sharp finite ``(m,b)`` witness."""
    addresses = sharp_prefix_addresses(module_count, query_arity)
    certificate = BoundedQueryArityExtremalCertificate(
        module_count=module_count,
        query_arity=query_arity,
        addresses=addresses,
    )
    if not certificate.verify():
        raise AssertionError("bounded-query-arity extremal certificate did not verify")
    return certificate


__all__ = [
    "FIRE",
    "TICK",
    "Address",
    "ProbeWord",
    "BoundedQueryArityExtremalCertificate",
    "bounded_query_action_alphabet",
    "bounded_query_closed_grammar",
    "bounded_query_open_grammar",
    "canonical_probe_word",
    "ceil_log_base",
    "certify_bounded_query_arity_extremal",
    "is_prefix_free",
    "kraft_sum",
    "maximum_addressable_leaves",
    "maximum_innovation_bits_for_query_budget",
    "route_action",
    "routing_actions",
    "sharp_prefix_addresses",
]
