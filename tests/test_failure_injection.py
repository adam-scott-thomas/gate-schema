"""Failure injection + cross-layer validation for gate-schema.

Tests for:
- Edge cases: empty strings, null values, boundary numbers
- Real gate-core output validated against schemas
- Real gate-policy output validated against schemas
- Real envelope output validated against schemas
- ValidationError attributes
"""
import json
from dataclasses import asdict

import pytest

from gate_schema.validator import (
    validate_tool, validate_policy, validate_envelope,
    validate_filter_result, validate_tools_bulk, ValidationError,
)


# --- Edge cases ---


def test_tool_empty_name_rejected():
    """Tool name must have minLength 1."""
    with pytest.raises(ValidationError):
        validate_tool({"name": "", "execution_class": "read_only"})


def test_tool_empty_description_ok():
    validate_tool({"name": "x", "execution_class": "read_only", "description": ""})


def test_envelope_empty_signature_rejected():
    """Signature must have minLength 1."""
    with pytest.raises(ValidationError):
        validate_envelope({
            "envelope_id": "e1", "context_id": "c1",
            "tool_name": "r", "signature": "",
        })


def test_envelope_budget_zero_rejected():
    """budget_seconds minimum is 1."""
    with pytest.raises(ValidationError):
        validate_envelope({
            "envelope_id": "e1", "context_id": "c1",
            "tool_name": "r", "signature": "abc",
            "budget_seconds": 0,
        })


def test_envelope_max_calls_zero_rejected():
    """max_tool_calls minimum is 1."""
    with pytest.raises(ValidationError):
        validate_envelope({
            "envelope_id": "e1", "context_id": "c1",
            "tool_name": "r", "signature": "abc",
            "max_tool_calls": 0,
        })


def test_filter_result_mode_negative_rejected():
    with pytest.raises(ValidationError):
        validate_filter_result({
            "visible": [], "suppressed": [],
            "mode": -0.1, "mode_zone": "normal",
        })


def test_filter_result_invalid_zone():
    with pytest.raises(ValidationError):
        validate_filter_result({
            "visible": [], "suppressed": [],
            "mode": 0.5, "mode_zone": "panic",
        })


def test_policy_with_conditions():
    """Policy with full conditions should validate."""
    validate_policy({
        "name": "test",
        "default_effect": "allow",
        "rules": [{
            "name": "after-hours",
            "effect": "deny",
            "execution_classes": ["high_impact"],
            "conditions": [
                {"field": "hour", "operator": "gte", "value": 22},
                {"field": "role", "operator": "neq", "value": "admin"},
            ],
            "priority": 10,
        }],
    })


def test_policy_invalid_operator():
    with pytest.raises(ValidationError):
        validate_policy({
            "name": "test",
            "rules": [{
                "name": "r1", "effect": "deny",
                "conditions": [{"field": "x", "operator": "LIKE", "value": "%"}],
            }],
        })


def test_bulk_empty_list():
    assert validate_tools_bulk([]) == []


def test_bulk_all_invalid():
    tools = [{"bad": True}, {"also_bad": True}]
    errors = validate_tools_bulk(tools)
    assert len(errors) == 2


# --- ValidationError attributes ---


def test_validation_error_has_artifact_type():
    try:
        validate_tool({"execution_class": "read_only"})
        assert False, "Should have raised"
    except ValidationError as e:
        assert e.artifact_type == "tool"
        assert "Invalid tool" in str(e)


def test_validation_error_has_path():
    try:
        validate_tool({"name": "x", "execution_class": "bad_class"})
        assert False, "Should have raised"
    except ValidationError as e:
        assert "execution_class" in e.path or "execution_class" in str(e)


# --- Cross-layer: validate real gate-core output ---


def test_validate_real_gate_core_tools():
    """gate-core Tool objects should validate as tools when converted to dict."""
    from maelstrom_gate import Gate, Tool
    gate = Gate()
    gate.add_tools([
        Tool("read", execution_class="read_only", description="Read files"),
        Tool("deploy", execution_class="high_impact"),
    ])
    for t in gate.tools:
        validate_tool({
            "name": t.name,
            "execution_class": t.execution_class,
            "description": t.description,
            "inputs": dict(t.inputs),
        })


def test_validate_real_filter_result():
    """gate-core filter result should validate against filter_result schema."""
    from maelstrom_gate import Gate, Tool
    gate = Gate()
    gate.add_tools([
        Tool("read", execution_class="read_only"),
        Tool("deploy", execution_class="high_impact"),
    ])
    result = gate.filter(0.5)
    validate_filter_result({
        "visible": [{"name": t.name, "execution_class": t.execution_class} for t in result.visible],
        "suppressed": [{"name": t.name, "execution_class": t.execution_class} for t in result.suppressed],
        "mode": result.mode,
        "mode_zone": result.mode_status,
        "thresholds": {k: v for k, v in result.thresholds.items() if v is not None},
    })


def test_validate_real_envelope():
    """gate-core envelope should validate against envelope schema."""
    from maelstrom_gate import Tool, build_envelope
    e = build_envelope(Tool("r", execution_class="read_only"), 0.1, "ctx", "key")
    data = asdict(e)
    data["allowed_tools"] = list(data["allowed_tools"])  # tuple -> list for JSON
    validate_envelope(data)


def test_validate_real_policy():
    """gate-policy policy should validate against policy schema."""
    from gate_policy.loader import load_policy
    policy_dict = {
        "name": "test-policy",
        "default_effect": "allow",
        "rules": [
            {"name": "deny-deploys", "effect": "deny",
             "execution_classes": ["high_impact"], "priority": 10},
        ],
    }
    # Validate the raw dict
    validate_policy(policy_dict)
    # Also verify it loads correctly in gate-policy
    loaded = load_policy(policy_dict)
    assert loaded.name == "test-policy"
