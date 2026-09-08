"""Regression test for the single-command manuscript-core replay."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify_paper_core.py"
REPORT = ROOT / "artifacts" / "paper_core_reproducibility_report.json"


def test_paper_core_replay_writes_a_scope_limited_deterministic_report():
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), "--write-report"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    report = json.loads(completed.stdout)

    assert REPORT.is_file()
    assert report["schema_version"] == 1
    assert report["scope"]["product_object"].startswith("declared product-indexed subset")
    assert "selector" in report["scope"]["bounded_query_contract"]
    assert report["core_1_exact_interface"]["refinement_verified"]
    assert report["core_2_operational_addressability"]["product_state_count"] == 12
    assert report["core_2_operational_addressability"]["gap_lower_bound"] == 1.0
    assert report["core_3_binary_sharpness"][-1] == {
        "module_count": 6,
        "closed_bits": 2,
        "open_bits": 7,
        "gap_bits": 5,
        "maximum_degree": 3,
    }
    assert report["core_3_bounded_query_arity"] == [
        {
            "module_count": 4,
            "query_arity": 1,
            "selector_depth": 3,
            "worst_query_length": 8,
            "innovation_bits": 4,
            "maximum_degree_bound": 2,
            "local_body_state_count_bound": 12,
        },
        {
            "module_count": 7,
            "query_arity": 2,
            "selector_depth": 2,
            "worst_query_length": 6,
            "innovation_bits": 7,
            "maximum_degree_bound": 3,
            "local_body_state_count_bound": 12,
        },
        {
            "module_count": 13,
            "query_arity": 3,
            "selector_depth": 2,
            "worst_query_length": 6,
            "innovation_bits": 13,
            "maximum_degree_bound": 4,
            "local_body_state_count_bound": 12,
        },
        {
            "module_count": 21,
            "query_arity": 4,
            "selector_depth": 2,
            "worst_query_length": 6,
            "innovation_bits": 21,
            "maximum_degree_bound": 5,
            "local_body_state_count_bound": 12,
        },
    ]
    assert report["core_4_5_portability_boundary"]["future_word_obstruction_verified"]
    assert report["core_4_5_portability_boundary"]["new_action_obstruction_verified"]
