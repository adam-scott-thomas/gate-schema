"""Tests for schema validation."""

import pytest
from gate_schema.validator import (
    validate_tool, validate_policy, validate_envelope,
    validate_filter_result, validate_tools_bulk, ValidationError,
)


# --- Tool validation ---

def test_valid_tool():
    validate_tool({"name": "read_file", "execution_class": "read_only"})


def test_valid_tool_full():
    validate_tool({
        "name": "deploy",
        "execution_class": "high_impact",
        "description": "Deploy to production",
        "inputs": {"version": "string"},
        "metadata": {"team": "platform"},
    })


def test_tool_missing_name():
    with pytest.raises(ValidationError) as exc:
        validate_tool({"execution_class": "read_only"})
    assert "tool" in str(exc.value)


def test_tool_invalid_class():
    with pytest.raises(ValidationError):
        validate_tool({"name": "x", "execution_class": "mega_impact"})


def test_tool_extra_field():
    with pytest.raises(ValidationError):
        validate_tool({"name": "x", "execution_class": "read_only", "danger": True})


# --- Policy validation ---

def test_valid_policy():
    validate_policy({
        "name": "test",
        "rules": [{"name": "r1", "effect": "deny"}],
    })


def test_policy_invalid_effect():
    with pytest.raises(ValidationError):
        validate_policy({
            "name": "test",
            "rules": [{"name": "r1", "effect": "maybe"}],
        })


def test_policy_missing_rules():
    with pytest.raises(ValidationError):
        validate_policy({"name": "test"})


# --- Envelope validation ---

def test_valid_envelope():
    validate_envelope({
        "envelope_id": "env_1",
        "context_id": "ctx_1",
        "tool_name": "read_file",
        "signature": "abc123",
    })


def test_envelope_missing_sig():
    with pytest.raises(ValidationError):
        validate_envelope({
            "envelope_id": "env_1",
            "context_id": "ctx_1",
            "tool_name": "read_file",
        })


# --- Filter result validation ---

def test_valid_filter_result():
    validate_filter_result({
        "visible": [{"name": "read", "execution_class": "read_only"}],
        "suppressed": [],
        "mode": 0.5,
        "mode_zone": "elevated",
    })


def test_filter_result_invalid_mode():
    with pytest.raises(ValidationError):
        validate_filter_result({
            "visible": [], "suppressed": [],
            "mode": 1.5, "mode_zone": "normal",
        })


# --- Bulk validation ---

def test_bulk_valid():
    tools = [
        {"name": "a", "execution_class": "read_only"},
        {"name": "b", "execution_class": "advisory"},
    ]
    assert validate_tools_bulk(tools) == []


def test_bulk_mixed():
    tools = [
        {"name": "a", "execution_class": "read_only"},
        {"execution_class": "read_only"},  # missing name
        {"name": "c", "execution_class": "bad_class"},
    ]
    errors = validate_tools_bulk(tools)
    assert len(errors) == 2
    assert errors[0][0] == 1
    assert errors[1][0] == 2
