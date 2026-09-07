import pytest

from causal_model.bounded_query_arity import (
    BoundedQueryArityExtremalCertificate,
    canonical_probe_word,
    ceil_log_base,
    certify_bounded_query_arity_extremal,
    is_prefix_free,
    maximum_addressable_leaves,
    maximum_innovation_bits_for_query_budget,
    sharp_prefix_addresses,
)
from causal_model.extremal_open_composition import certify_fixed_regular_extremal_theorem


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
def test_exact_integer_selector_depth(module_count: int, query_arity: int, expected_depth: int) -> None:
    assert ceil_log_base(module_count, query_arity) == expected_depth


def test_unary_boundary_is_explicit() -> None:
    certificate = certify_bounded_query_arity_extremal(1, 1)
    assert certificate.verify()
    assert certificate.selector_depth == 0
    assert certificate.worst_query_length == 2
    assert maximum_addressable_leaves(1, 100) == 1
    assert maximum_innovation_bits_for_query_budget(1, 100) == 1

    with pytest.raises(ValueError):
        ceil_log_base(2, 1)
    with pytest.raises(ValueError):
        sharp_prefix_addresses(2, 1)
    with pytest.raises(ValueError):
        certify_bounded_query_arity_extremal(2, 1)


@pytest.mark.parametrize(
    ("module_count", "query_arity"),
    ((1, 2), (2, 2), (3, 2), (5, 2), (8, 3), (10, 3), (17, 4)),
)
def test_certificate_attains_kraft_and_latency_lower_bound(module_count: int, query_arity: int) -> None:
    certificate = certify_bounded_query_arity_extremal(module_count, query_arity)

    assert isinstance(certificate, BoundedQueryArityExtremalCertificate)
    assert certificate.verify()
    assert len(certificate.addresses) == module_count
    assert is_prefix_free(certificate.addresses)
    assert certificate.kraft_sum <= 1
    assert certificate.selector_depth == ceil_log_base(module_count, query_arity)
    assert certificate.worst_query_length == 2 * ceil_log_base(module_count, query_arity) + 2
    assert certificate.open_only_innovation_bits == module_count
    assert certificate.innovation_slack_bits == 0
    assert certificate.newly_legal_action_count == 1
    assert certificate.grammar_transition_difference_count == 1
    assert certificate.maximum_trie_outdegree <= query_arity
    assert certificate.maximum_graph_degree_bound <= query_arity + 1
    assert certificate.focal_exterior_cut_width == 1

    for address in certificate.addresses:
        probe = canonical_probe_word(address)
        assert len(probe) == 2 * len(address) + 2
        assert probe[len(address)] == "fire"


def test_binary_case_recovers_existing_fixed_regular_query_length() -> None:
    for module_count in range(1, 9):
        bounded = certify_bounded_query_arity_extremal(module_count, 2)
        existing = certify_fixed_regular_extremal_theorem(module_count)
        assert bounded.worst_query_length == existing.worst_canonical_query_length


@pytest.mark.parametrize(
    ("query_arity", "query_budget", "expected_bits"),
    (
        (2, 0, 0),
        (2, 1, 0),
        (2, 2, 1),
        (2, 3, 1),
        (2, 4, 2),
        (2, 5, 2),
        (2, 6, 4),
        (3, 4, 3),
        (3, 6, 9),
        (4, 6, 16),
    ),
)
def test_inverse_query_budget_extremum(query_arity: int, query_budget: int, expected_bits: int) -> None:
    assert maximum_innovation_bits_for_query_budget(query_arity, query_budget) == expected_bits


def test_invalid_parameters_fail_closed() -> None:
    with pytest.raises(ValueError):
        certify_bounded_query_arity_extremal(0, 2)
    with pytest.raises(ValueError):
        certify_bounded_query_arity_extremal(1, 0)
    with pytest.raises(ValueError):
        maximum_innovation_bits_for_query_budget(2, -1)
