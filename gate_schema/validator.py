"""Validation functions for Gate artifacts.

Each function validates a dict against the corresponding schema
and raises ValidationError with a clear message on failure.
"""

from __future__ import annotations

from typing import Any

import jsonschema

from gate_schema.schemas import (
    TOOL_SCHEMA,
    POLICY_SCHEMA,
    ENVELOPE_SCHEMA,
    FILTER_RESULT_SCHEMA,
)


class ValidationError(Exception):
    """Raised when a Gate artifact fails schema validation."""
    def __init__(self, artifact_type: str, message: str, path: str = ""):
        self.artifact_type = artifact_type
        self.path = path
        super().__init__(f"Invalid {artifact_type}: {message}" + (f" (at {path})" if path else ""))


def _validate(data: dict[str, Any], schema: dict, artifact_type: str) -> None:
    """Validate data against a schema, raising ValidationError on failure."""
    try:
        jsonschema.validate(data, schema)
    except jsonschema.ValidationError as e:
        path = ".".join(str(p) for p in e.absolute_path) if e.absolute_path else ""
        raise ValidationError(artifact_type, e.message, path) from None


def validate_tool(data: dict[str, Any]) -> None:
    """Validate a tool manifest dict. Raises ValidationError."""
    _validate(data, TOOL_SCHEMA, "tool")


def validate_policy(data: dict[str, Any]) -> None:
    """Validate a policy document dict. Raises ValidationError."""
    _validate(data, POLICY_SCHEMA, "policy")


def validate_envelope(data: dict[str, Any]) -> None:
    """Validate an authorization envelope dict. Raises ValidationError."""
    _validate(data, ENVELOPE_SCHEMA, "envelope")


def validate_filter_result(data: dict[str, Any]) -> None:
    """Validate a filter result dict. Raises ValidationError."""
    _validate(data, FILTER_RESULT_SCHEMA, "filter_result")


def validate_tools_bulk(tools: list[dict[str, Any]]) -> list[tuple[int, ValidationError]]:
    """Validate a list of tools, returning (index, error) for failures."""
    errors = []
    for i, tool in enumerate(tools):
        try:
            validate_tool(tool)
        except ValidationError as e:
            errors.append((i, e))
    return errors
