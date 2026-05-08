"""gate-schema demo — run with: python -m gate_schema

Validates good and bad Gate artifacts to show schema enforcement.
"""

from gate_schema.validator import (
    validate_tool, validate_policy, validate_envelope,
    validate_filter_result, validate_tools_bulk, ValidationError,
)

print("=" * 65)
print("  gate-schema -- JSON Schema Validation for Gatekeeper")
print("=" * 65)

# --- Valid artifacts ---
print("\n[1] Valid artifacts\n")

valid_cases = [
    ("tool", {"name": "read_file", "execution_class": "read_only", "description": "Read a file"}),
    ("policy", {"name": "enterprise", "rules": [{"name": "deny-deploy", "effect": "deny"}], "default_effect": "allow"}),
    ("envelope", {"envelope_id": "env_1", "context_id": "sess_1", "tool_name": "read_file", "signature": "abc123def456", "max_tool_calls": 20, "execution_mode": "standard"}),
    ("filter_result", {"visible": [{"name": "read", "execution_class": "read_only"}], "suppressed": [], "mode": 0.3, "mode_zone": "normal"}),
]

validators = {"tool": validate_tool, "policy": validate_policy, "envelope": validate_envelope, "filter_result": validate_filter_result}

for artifact_type, data in valid_cases:
    try:
        validators[artifact_type](data)
        print(f"    + {artifact_type:<15} VALID")
    except ValidationError as e:
        print(f"    x {artifact_type:<15} {e}")

# --- Invalid artifacts ---
print("\n[2] Invalid artifacts (caught by schema)\n")

bad_cases = [
    ("tool (no name)", validate_tool, {"execution_class": "read_only"}),
    ("tool (bad class)", validate_tool, {"name": "x", "execution_class": "mega_impact"}),
    ("tool (extra field)", validate_tool, {"name": "x", "execution_class": "read_only", "danger": True}),
    ("policy (bad effect)", validate_policy, {"name": "p", "rules": [{"name": "r", "effect": "maybe"}]}),
    ("envelope (no sig)", validate_envelope, {"envelope_id": "e", "context_id": "c", "tool_name": "t"}),
    ("filter (mode>1)", validate_filter_result, {"visible": [], "suppressed": [], "mode": 1.5, "mode_zone": "normal"}),
]

for label, fn, data in bad_cases:
    try:
        fn(data)
        print(f"    ? {label:<25} MISSED (should have failed)")
    except ValidationError as e:
        print(f"    x {label:<25} CAUGHT: {e}")

# --- Bulk validation ---
print("\n[3] Bulk tool validation\n")

tools = [
    {"name": "read_file", "execution_class": "read_only"},
    {"name": "deploy", "execution_class": "high_impact"},
    {"execution_class": "advisory"},  # missing name
    {"name": "bad", "execution_class": "ultra_impact"},  # invalid class
    {"name": "write_db", "execution_class": "state_mutation"},
]

errors = validate_tools_bulk(tools)
print(f"    {len(tools)} tools checked, {len(errors)} invalid:")
for idx, err in errors:
    print(f"      [{idx}] {err}")

print(f"\n{'=' * 65}")
print(f"  Schemas cover: tools, policies, envelopes, filter results")
print(f"  {len(valid_cases)} artifact types validated. {len(bad_cases)} bad inputs caught.")
print(f"{'=' * 65}")
