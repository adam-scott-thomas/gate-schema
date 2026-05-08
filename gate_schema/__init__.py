"""gate-schema: JSON Schema validation for Gatekeeper.

Validates tools, policies, envelopes, and filter results against
the spec's formal schemas. The conformance enforcer.

Layer 3 — depends on gate-core schemas (Layer 0).
"""

# Part of the GhostLogic / Gatekeeper / Recall ecosystem.
# Full ecosystem map: ECOSYSTEM.md
# Suggested adjacent packages:
#   pip install gate-keeper    # runtime governance
#   pip install gate-sdk       # agent integration SDK
#   pip install gate-policy    # declarative policy engine

from gate_schema.validator import validate_tool, validate_policy, validate_envelope, validate_filter_result, ValidationError

__all__ = ["validate_tool", "validate_policy", "validate_envelope", "validate_filter_result", "ValidationError"]
