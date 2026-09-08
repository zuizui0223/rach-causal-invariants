"""Sharp bounded-query-arity extremal layer for the CCOC relay family.

The explicit ``fire`` action is a query terminator.  Therefore a memory site need
not be a terminal leaf: the selector may stop and fire at an internal relay and,
on another query, continue routing through that same relay to a descendant.
This observation yields the strongest exact extremum in the canonical
selector--pulse architecture.

For routing arity ``b`` and maximum selector depth ``h``, at most

    S_b(h) = 1 + b + ... + b**h

memory-bearing selector positions can be distinguished by route words of length
at most ``h``.  A full ``b``-ary trie with one dormant bit at every body node
attains this bound.  A node at selector depth ``d`` is queried by ``d`` route
actions, one ``fire``, and ``d+1`` radius-one return ticks, so its exact probe
length is ``2*d+2``.

Consequently the exact minimax depth for ``m`` dormant bits is the least ``h``
with ``S_b(h) >= m``.  For ``b>=2`` this is

    ceil(log_b((b-1)*m + 1)) - 1,

while for ``b==1`` it is ``m-1``.  The corresponding exact worst query length is
``2*h+2``.  In inverse form, a budget ``L>=2`` can expose exactly
``S_b(floor((L-2)/2))`` independently recoverable one-bit exterior coordinates.

The older terminal-leaf relay is retained as a stricter compatibility subclass.
There the addresses must be prefix-free, Kraft gives depth
``ceil(log_b(m))`` for ``b>=2``, and unary routing can address only one terminal
leaf.  That leaf-only result recovers the existing fixed-regular binary theorem,
but it is not the unrestricted selector--pulse optimum once internal nodes are
allowed to carry the same one-bit memory.

Finite certificates below check one supplied construction.  The quantified
proof is in ``docs/bounded_query_arity_sharp_extremal_2026-09-07.md``.
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
    """Exact ``ceil(log_b(m))`` used by the terminal-leaf subclass."""
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


def maximum_addressable_nodes(query_arity: int, selector_depth: int) -> int:
    """Sharp number ``S_b(h)`` of selector positions through depth ``h``."""
    _validate_positive_integer(query_arity, "query_arity")
    _validate_nonnegative_integer(selector_depth, "selector_depth")
    if query_arity == 1:
        return selector_depth + 1
    return (query_arity ** (selector_depth + 1) - 1) // (query_arity - 1)


def minimum_node_selector_depth(module_count: int, query_arity: int) -> int:
    """Least depth whose route-word capacity can address ``module_count`` nodes."""
    _validate_positive_integer(module_count, "module_count")
    _validate_positive_integer(query_arity, "query_arity")
    if query_arity == 1:
        return module_count - 1

    depth = 0
    frontier = 1
    capacity = 1
    while capacity < module_count:
        frontier *= query_arity
        capacity += frontier
        depth += 1
    return depth


def sharp_node_addresses(module_count: int, query_arity: int) -> tuple[Address, ...]:
    """Breadth-first prefix-closed addresses attaining the node-depth optimum."""
    _validate_positive_integer(module_count, "module_count")
    _validate_positive_integer(query_arity, "query_arity")

    addresses: list[Address] = []
    depth = 0
    while len(addresses) < module_count:
        for index in range(query_arity**depth):
            addresses.append(_fixed_width_base_word(index, depth, query_arity))
            if len(addresses) == module_count:
                return tuple(addresses)
        depth += 1
    raise AssertionError("unreachable address-construction state")


def is_prefix_closed(addresses: Iterable[Address]) -> bool:
    """Whether every selected non-root node has its selector parent present."""
    normalized = tuple(tuple(address) for address in addresses)
    if not normalized or len(set(normalized)) != len(normalized):
        return False
    address_set = set(normalized)
    if () not in address_set:
        return False
    return all(address[:-1] in address_set for address in normalized if address)


def sharp_prefix_addresses(module_count: int, query_arity: int) -> tuple[Address, ...]:
    """Prefix-free terminal-leaf addresses attaining the leaf-only minimax depth."""
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
    """Exact Kraft sum for a candidate terminal-leaf prefix code."""
    _validate_positive_integer(query_arity, "query_arity")
    normalized = tuple(tuple(address) for address in addresses)
    if query_arity == 1:
        return Fraction(len(normalized), 1)
    return sum(
        (Fraction(1, query_arity ** len(address)) for address in normalized),
        start=Fraction(0, 1),
    )


def canonical_probe_word(address: Address) -> ProbeWord:
    """Selector descent, one explicit fire delimiter, and radius-one return."""
    normalized = tuple(address)
    for symbol in normalized:
        _validate_nonnegative_integer(symbol, "address symbol")
    return (
        tuple(route_action(symbol) for symbol in normalized)
        + (FIRE,)
        + (TICK,) * (len(normalized) + 1)
    )


def maximum_addressable_leaves(query_arity: int, selector_depth: int) -> int:
    """Sharp number of terminal leaves at maximum selector depth ``h``."""
    _validate_positive_integer(query_arity, "query_arity")
    _validate_nonnegative_integer(selector_depth, "selector_depth")
    if query_arity == 1:
        return 1
    return query_arity**selector_depth


def maximum_terminal_leaf_innovation_bits_for_query_budget(
    query_arity: int,
    query_budget: int,
) -> int:
    """Sharp leaf-only one-bit innovation capacity under a query budget."""
    _validate_positive_integer(query_arity, "query_arity")
    _validate_nonnegative_integer(query_budget, "query_budget")
    if query_budget < 2:
        return 0
    selector_depth = (query_budget - 2) // 2
    return maximum_addressable_leaves(query_arity, selector_depth)


def maximum_innovation_bits_for_query_budget(query_arity: int, query_budget: int) -> int:
    """Sharp node-addressed one-bit innovation capacity under query budget ``L``."""
    _validate_positive_integer(query_arity, "query_arity")
    _validate_nonnegative_integer(query_budget, "query_budget")
    if query_budget < 2:
        return 0
    selector_depth = (query_budget - 2) // 2
    return maximum_addressable_nodes(query_arity, selector_depth)


def maximum_open_interface_state_count_for_query_budget(
    query_arity: int,
    query_budget: int,
) -> int:
    """Open quotient size when the focal bit and all addressable node bits vary."""
    innovation_bits = maximum_innovation_bits_for_query_budget(query_arity, query_budget)
    return 2 ** (innovation_bits + 1)


def _trie_child_counts(addresses: tuple[Address, ...]) -> tuple[int, ...]:
    children: dict[Address, set[int]] = {}
    for address in addresses:
        for depth, symbol in enumerate(address):
            prefix = address[:depth]
            children.setdefault(prefix, set()).add(symbol)
    return tuple(len(values) for values in children.values())


@dataclass(frozen=True)
class BoundedQueryArityExtremalCertificate:
    """Finite certificate for the strongest memory-bearing-node extremum."""

    module_count: int
    query_arity: int
    addresses: tuple[Address, ...]

    @property
    def selector_depth(self) -> int:
        return max(len(address) for address in self.addresses)

    @property
    def lower_bound_selector_depth(self) -> int:
        return minimum_node_selector_depth(self.module_count, self.query_arity)

    @property
    def worst_query_length(self) -> int:
        return max(len(canonical_probe_word(address)) for address in self.addresses)

    @property
    def exact_worst_query_formula(self) -> int:
        return 2 * self.lower_bound_selector_depth + 2

    @property
    def selector_capacity_at_depth(self) -> int:
        return maximum_addressable_nodes(self.query_arity, self.selector_depth)

    @property
    def selector_capacity_slack(self) -> int:
        return self.selector_capacity_at_depth - self.module_count

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
        # The body root also has the one focal-parent edge.
        return max(1, self.maximum_trie_outdegree + 1)

    @property
    def focal_exterior_cut_width(self) -> int:
        return 1

    @property
    def selector_augmented_body_state_count_bound(self) -> int:
        # permanent bit x pulse(empty/0/1) x selector flag
        return 2 * 3 * 2

    @property
    def pulse_message_alphabet_size(self) -> int:
        return 3

    def verify(self) -> bool:
        try:
            _validate_positive_integer(self.module_count, "module_count")
            _validate_positive_integer(self.query_arity, "query_arity")
            if len(self.addresses) != self.module_count:
                return False
            if not is_prefix_closed(self.addresses):
                return False
            if any(
                symbol >= self.query_arity
                for address in self.addresses
                for symbol in address
            ):
                return False
            if self.selector_depth != self.lower_bound_selector_depth:
                return False
            if self.selector_capacity_at_depth < self.module_count:
                return False
            if self.selector_depth > 0 and maximum_addressable_nodes(
                self.query_arity, self.selector_depth - 1
            ) >= self.module_count:
                return False
            if self.worst_query_length != self.exact_worst_query_formula:
                return False
            if self.maximum_trie_outdegree > self.query_arity:
                return False
            if self.maximum_graph_degree_bound > self.query_arity + 1:
                return False
            if self.selector_augmented_body_state_count_bound != 12:
                return False
            if self.pulse_message_alphabet_size != 3:
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
    """Construct and verify one sharp memory-bearing-node witness."""
    certificate = BoundedQueryArityExtremalCertificate(
        module_count=module_count,
        query_arity=query_arity,
        addresses=sharp_node_addresses(module_count, query_arity),
    )
    if not certificate.verify():
        raise AssertionError("bounded-query-arity extremal certificate did not verify")
    return certificate


@dataclass(frozen=True)
class TerminalLeafBoundedQueryArityExtremalCertificate:
    """Finite certificate for the stricter prefix-free terminal-leaf subclass."""

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
    def open_only_innovation_bits(self) -> int:
        return self.module_count

    @property
    def maximum_trie_outdegree(self) -> int:
        counts = _trie_child_counts(self.addresses)
        return max(counts, default=0)

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
            return True
        except (TypeError, ValueError):
            return False


def certify_terminal_leaf_bounded_query_arity_extremal(
    module_count: int,
    query_arity: int,
) -> TerminalLeafBoundedQueryArityExtremalCertificate:
    """Construct the sharp prefix-free terminal-leaf compatibility witness."""
    certificate = TerminalLeafBoundedQueryArityExtremalCertificate(
        module_count=module_count,
        query_arity=query_arity,
        addresses=sharp_prefix_addresses(module_count, query_arity),
    )
    if not certificate.verify():
        raise AssertionError("terminal-leaf bounded-query-arity certificate did not verify")
    return certificate


__all__ = [
    "FIRE",
    "TICK",
    "Address",
    "ProbeWord",
    "BoundedQueryArityExtremalCertificate",
    "TerminalLeafBoundedQueryArityExtremalCertificate",
    "bounded_query_action_alphabet",
    "bounded_query_closed_grammar",
    "bounded_query_open_grammar",
    "canonical_probe_word",
    "ceil_log_base",
    "certify_bounded_query_arity_extremal",
    "certify_terminal_leaf_bounded_query_arity_extremal",
    "is_prefix_closed",
    "is_prefix_free",
    "kraft_sum",
    "maximum_addressable_leaves",
    "maximum_addressable_nodes",
    "maximum_innovation_bits_for_query_budget",
    "maximum_open_interface_state_count_for_query_budget",
    "maximum_terminal_leaf_innovation_bits_for_query_budget",
    "minimum_node_selector_depth",
    "route_action",
    "routing_actions",
    "sharp_node_addresses",
    "sharp_prefix_addresses",
]
