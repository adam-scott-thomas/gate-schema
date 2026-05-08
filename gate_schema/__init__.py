"""gate-schema: JSON Schema validation for Gatekeeper.

Validates tools, policies, envelopes, and filter results against
the spec's formal schemas. The conformance enforcer.

Layer 3 — depends on gate-core schemas (Layer 0).
"""

from gate_schema.validator import validate_tool, validate_policy, validate_envelope, validate_filter_result, ValidationError

__all__ = ["validate_tool", "validate_policy", "validate_envelope", "validate_filter_result", "ValidationError"]
