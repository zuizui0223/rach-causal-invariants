import pytest

import causal_model.portability_core as core
from causal_model.bounded_query_arity import (
    BoundedQueryArityExtremalCertificate,
    TerminalLeafBoundedQueryArityExtremalCertificate,
    canonical_probe_word,
    ceil_log_base,
    certify_bounded_query_arity_extremal,
    certify_terminal_leaf_bounded_query_arity_extremal,
    is_prefix_closed,
    is_prefix_free,
    maximum_addressable_leaves,
    maximum_addressable_nodes,
    maximum_innovation_bits_for_query_budget,
    maximum_open_interface_state_count_for_query_budget,
    maximum_terminal_leaf_innovation_bits_for_query_budget,
    minimum_node_selector_depth,
    sharp_node_addresses,
    sharp_prefix_addresses,
)
from causal_model.extremal_open_composition import certify_fixed_regular_extremal_theorem


@pytest.mark.parametrize(
    ("module_count", "query_arity", "expected_depth"),
    (
        (1, 1, 0),
        (2, 1, 1),
        (5, 1, 4),
        (1, 2, 0),
        (2, 2, 1),
        (3, 2, 1),
        (4, 2, 2),
        (7, 2, 2),
        (8, 2, 3),
        (4, 3, 1),
        (5, 3, 2),
        (13, 3, 2),
        (14, 3, 3),
    ),
)
def test_exact_node_selector_depth(module_count: int, query_arity: int, expected_depth: int) -> None:
    assert minimum_node_selector_depth(module_count, query_arity) == expected_depth


@pytest.mark.parametrize(
    ("query_arity", "selector_depth", "expected_nodes"),
    (
        (1, 0, 1),
        (1, 4, 5),
        (2, 0, 1),
        (2, 1, 3),
        (2, 2, 7),
        (3, 1, 4),
        (3, 2, 13),
        (4, 2, 21),
    ),
)
def test_exact_route_word_capacity(query_arity: int, selector_depth: int, expected_nodes: int) -> None:
    assert maximum_addressable_nodes(query_arity, selector_depth) == expected_nodes


@pytest.mark.parametrize(
    ("module_count", "query_arity"),
    ((1, 1), (5, 1), (1, 2), (3, 2), (7, 2), (8, 2), (13, 3), (17, 4)),
)
def test_node_certificate_attains_counting_and_latency_lower_bound(module_count: int, query_arity: int) -> None:
    certificate = certify_bounded_query_arity_extremal(module_count, query_arity)

    assert isinstance(certificate, BoundedQueryArityExtremalCertificate)
    assert certificate.verify()
    assert len(certificate.addresses) == module_count
    assert len(set(certificate.addresses)) == module_count
    assert is_prefix_closed(certificate.addresses)
    assert certificate.selector_depth == minimum_node_selector_depth(module_count, query_arity)
    assert certificate.selector_capacity_at_depth >= module_count
    if certificate.selector_depth > 0:
        assert maximum_addressable_nodes(query_arity, certificate.selector_depth - 1) < module_count
    assert certificate.worst_query_length == 2 * certificate.selector_depth + 2
    assert certificate.open_only_innovation_bits == module_count
    assert certificate.innovation_slack_bits == 0
    assert certificate.newly_legal_action_count == 1
    assert certificate.grammar_transition_difference_count == 1
    assert certificate.maximum_trie_outdegree <= query_arity
    assert certificate.maximum_graph_degree_bound <= query_arity + 1
    assert certificate.focal_exterior_cut_width == 1
    assert certificate.selector_augmented_body_state_count_bound == 12
    assert certificate.pulse_message_alphabet_size == 3

    for address in certificate.addresses:
        probe = canonical_probe_word(address)
        assert len(probe) == 2 * len(address) + 2
        assert probe[len(address)] == "fire"


def test_fire_delimiter_makes_prefix_free_addresses_unnecessary() -> None:
    certificate = certify_bounded_query_arity_extremal(3, 2)
    assert certificate.addresses == ((), (0,), (1,))
    assert is_prefix_closed(certificate.addresses)
    assert not is_prefix_free(certificate.addresses)
    assert certificate.selector_depth == 1
    assert certificate.worst_query_length == 4

    terminal = certify_terminal_leaf_bounded_query_arity_extremal(3, 2)
    assert terminal.selector_depth == 2
    assert terminal.worst_query_length == 6


@pytest.mark.parametrize(
    ("query_arity", "query_budget", "expected_bits"),
    (
        (1, 0, 0),
        (1, 1, 0),
        (1, 2, 1),
        (1, 4, 2),
        (1, 6, 3),
        (2, 0, 0),
        (2, 1, 0),
        (2, 2, 1),
        (2, 3, 1),
        (2, 4, 3),
        (2, 5, 3),
        (2, 6, 7),
        (3, 4, 4),
        (3, 6, 13),
        (4, 6, 21),
    ),
)
def test_inverse_node_query_budget_extremum(query_arity: int, query_budget: int, expected_bits: int) -> None:
    assert maximum_innovation_bits_for_query_budget(query_arity, query_budget) == expected_bits
    assert maximum_open_interface_state_count_for_query_budget(query_arity, query_budget) == 2 ** (expected_bits + 1)


@pytest.mark.parametrize("query_arity", (1, 2, 3, 4))
def test_inverse_extremum_has_matching_finite_witnesses(query_arity: int) -> None:
    for selector_depth in range(4):
        query_budget = 2 * selector_depth + 2
        module_count = maximum_addressable_nodes(query_arity, selector_depth)
        certificate = certify_bounded_query_arity_extremal(module_count, query_arity)
        assert certificate.selector_depth == selector_depth
        assert certificate.worst_query_length == query_budget
        assert certificate.open_only_innovation_bits == module_count
        assert maximum_innovation_bits_for_query_budget(query_arity, query_budget) == module_count


@pytest.mark.parametrize(
    ("module_count", "query_arity", "expected_depth"),
    (
        (1, 1, 0),
        (1, 2, 0),
        (2, 2, 1),
        (3, 2, 2),
        (4, 2, 2),
        (5, 2, 3),
        (8, 3, 2),
        (9, 3, 2),
        (10, 3, 3),
        (16, 4, 2),
    ),
)
def test_terminal_leaf_subclass_retains_kraft_extremum(
    module_count: int,
    query_arity: int,
    expected_depth: int,
) -> None:
    assert ceil_log_base(module_count, query_arity) == expected_depth
    certificate = certify_terminal_leaf_bounded_query_arity_extremal(module_count, query_arity)
    assert isinstance(certificate, TerminalLeafBoundedQueryArityExtremalCertificate)
    assert certificate.verify()
    assert is_prefix_free(certificate.addresses)
    assert certificate.selector_depth == expected_depth
    assert certificate.worst_query_length == 2 * expected_depth + 2


def test_terminal_leaf_unary_boundary_is_explicit() -> None:
    terminal = certify_terminal_leaf_bounded_query_arity_extremal(1, 1)
    assert terminal.verify()
    assert terminal.selector_depth == 0
    assert terminal.worst_query_length == 2
    assert maximum_addressable_leaves(1, 100) == 1
    assert maximum_terminal_leaf_innovation_bits_for_query_budget(1, 100) == 1

    with pytest.raises(ValueError):
        ceil_log_base(2, 1)
    with pytest.raises(ValueError):
        sharp_prefix_addresses(2, 1)
    with pytest.raises(ValueError):
        certify_terminal_leaf_bounded_query_arity_extremal(2, 1)


def test_terminal_binary_case_recovers_existing_fixed_regular_query_length() -> None:
    for module_count in range(1, 9):
        terminal = certify_terminal_leaf_bounded_query_arity_extremal(module_count, 2)
        existing = certify_fixed_regular_extremal_theorem(module_count)
        assert terminal.worst_query_length == existing.worst_canonical_query_length


def test_node_addressed_binary_never_worse_than_terminal_existing_relay() -> None:
    strict_improvements = 0
    for module_count in range(1, 17):
        node_addressed = certify_bounded_query_arity_extremal(module_count, 2)
        existing = certify_fixed_regular_extremal_theorem(module_count)
        assert node_addressed.worst_query_length <= existing.worst_canonical_query_length
        strict_improvements += int(
            node_addressed.worst_query_length < existing.worst_canonical_query_length
        )
    assert strict_improvements > 0


def test_public_surface_exports_both_sharp_and_terminal_variants() -> None:
    assert core.BoundedQueryArityExtremalCertificate is BoundedQueryArityExtremalCertificate
    assert core.TerminalLeafBoundedQueryArityExtremalCertificate is TerminalLeafBoundedQueryArityExtremalCertificate
    assert core.certify_bounded_query_arity_extremal is certify_bounded_query_arity_extremal
    assert core.certify_terminal_leaf_bounded_query_arity_extremal is certify_terminal_leaf_bounded_query_arity_extremal
    assert core.maximum_innovation_bits_for_query_budget is maximum_innovation_bits_for_query_budget
    assert core.minimum_node_selector_depth is minimum_node_selector_depth


def test_invalid_parameters_fail_closed() -> None:
    with pytest.raises(ValueError):
        certify_bounded_query_arity_extremal(0, 2)
    with pytest.raises(ValueError):
        certify_bounded_query_arity_extremal(1, 0)
    with pytest.raises(ValueError):
        maximum_innovation_bits_for_query_budget(2, -1)
