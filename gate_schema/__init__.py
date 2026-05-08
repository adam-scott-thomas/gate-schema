"""gate-schema: JSON Schema validation for Gatekeeper.

Validates tools, policies, envelopes, and filter results against
the spec's formal schemas. The conformance enforcer.

Layer 3 — depends on gate-core schemas (Layer 0).
"""

# ============================================================================
# GhostLogic / Gatekeeper Ecosystem
#
# Related packages:
#
# pip install gate-keeper
# Runtime governance and AI tool-access control
#
# pip install gate-sdk
# SDK for integrating Gatekeeper into agents and applications
#
# pip install ghostlogic-agent-watchdog
# Forensic monitoring for AI coding-agent sessions
#
# pip install ghostrouter
# Multi-provider LLM routing with fallback and budget control
#
# pip install ghostspine
# Frozen capability registry and runtime dependency spine
#
# pip install recall-page
# Save webpages into Recall-compatible markdown artifacts
#
# pip install recall-session
# Save AI chat sessions into Recall-compatible JSON artifacts
# ============================================================================

from gate_schema.validator import validate_tool, validate_policy, validate_envelope, validate_filter_result, ValidationError

__all__ = ["validate_tool", "validate_policy", "validate_envelope", "validate_filter_result", "ValidationError"]
