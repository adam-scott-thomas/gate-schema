"""Bundled schemas — loaded from gate-core or embedded fallbacks.

Tries to load from maelstrom-gate/schema/ first. If not installed,
uses embedded copies. This means gate-schema works standalone.
"""

from __future__ import annotations

import json
from pathlib import Path

# Try gate-core's schema directory first
_CORE_SCHEMA_DIR = Path(__file__).parent.parent.parent / "maelstrom-gate" / "schema"

TOOL_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Tool Manifest",
    "type": "object",
    "required": ["name", "execution_class"],
    "properties": {
        "name": {"type": "string", "minLength": 1},
        "execution_class": {
            "type": "string",
            "enum": ["read_only", "advisory", "external_action", "state_mutation", "high_impact"],
        },
        "description": {"type": "string"},
        "inputs": {"type": "object", "additionalProperties": {"type": "string"}},
        "metadata": {"type": "object", "additionalProperties": True},
    },
    "additionalProperties": False,
}

POLICY_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Gate Policy",
    "type": "object",
    "required": ["name", "rules"],
    "properties": {
        "name": {"type": "string", "minLength": 1},
        "description": {"type": "string"},
        "default_effect": {"type": "string", "enum": ["allow", "deny"]},
        "rules": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name", "effect"],
                "properties": {
                    "name": {"type": "string"},
                    "effect": {"type": "string", "enum": ["allow", "deny"]},
                    "execution_classes": {
                        "type": "array",
                        "items": {"type": "string", "enum": [
                            "read_only", "advisory", "external_action",
                            "state_mutation", "high_impact",
                        ]},
                    },
                    "tool_names": {"type": "array", "items": {"type": "string"}},
                    "conditions": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["field", "operator", "value"],
                            "properties": {
                                "field": {"type": "string"},
                                "operator": {
                                    "type": "string",
                                    "enum": ["eq", "neq", "gt", "gte", "lt", "lte", "in", "not_in"],
                                },
                                "value": {},
                            },
                        },
                    },
                    "priority": {"type": "integer"},
                },
            },
        },
    },
}

ENVELOPE_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Authorization Envelope",
    "type": "object",
    "required": ["envelope_id", "context_id", "tool_name", "signature"],
    "properties": {
        "envelope_id": {"type": "string"},
        "context_id": {"type": "string"},
        "tool_name": {"type": "string"},
        "allowed_tools": {"type": "array", "items": {"type": "string"}},
        "max_tool_calls": {"type": "integer", "minimum": 1},
        "max_retries": {"type": "integer", "minimum": 0},
        "budget_seconds": {"type": "integer", "minimum": 1},
        "execution_mode": {"type": "string", "enum": ["standard", "cautious", "minimal"]},
        "dry_run": {"type": "boolean"},
        "branching": {"type": "string", "enum": ["auto", "deny"]},
        "human_approved": {"type": "boolean"},
        "signature": {"type": "string", "minLength": 1},
    },
}

FILTER_RESULT_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Filter Result",
    "type": "object",
    "required": ["visible", "suppressed", "mode", "mode_zone"],
    "properties": {
        "visible": {"type": "array", "items": {"$ref": "#/$defs/tool"}},
        "suppressed": {"type": "array", "items": {"$ref": "#/$defs/tool"}},
        "mode": {"type": "number", "minimum": 0, "maximum": 1},
        "mode_zone": {"type": "string", "enum": ["normal", "elevated", "crisis"]},
        "thresholds": {"type": "object"},
    },
    "$defs": {
        "tool": {
            "type": "object",
            "required": ["name", "execution_class"],
            "properties": {
                "name": {"type": "string"},
                "execution_class": {"type": "string"},
            },
        },
    },
}


def _try_load_core_schema(name: str) -> dict | None:
    """Try to load a schema from gate-core's schema directory."""
    path = _CORE_SCHEMA_DIR / name
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return None
