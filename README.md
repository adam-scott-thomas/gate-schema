# gate-schema

[![status](https://img.shields.io/badge/status-v0.1.0-blue)]()
[![tests](https://img.shields.io/badge/tests-31_passing-brightgreen)]()
[![license](https://img.shields.io/badge/license-Apache_2.0-green)]()

> JSON Schema validator for Gatekeeper artifacts.

Conformance enforcement for tools, policies, envelopes, and filter results.
Ships the canonical schemas derived from SPEC.md and a handful of `validate_*`
functions that raise a typed error if an artifact drifts from the contract.

## Install

```bash
pip install gate-schema  # once published
# or from source:
pip install -e .[dev]
```

## Quick example

```python
from gate_schema import validate_tool, validate_policy, validate_envelope, ValidationError

validate_tool({
    "name": "deploy",
    "execution_class": "high_impact",
    "description": "Deploy to production",
})  # returns silently on valid

try:
    validate_tool({"name": "deploy"})  # missing execution_class
except ValidationError as e:
    print(e)  # "required field 'execution_class' missing"
```

## What it validates

| Function | Schema |
|----------|--------|
| `validate_tool` | tool manifest entry |
| `validate_policy` | full policy document |
| `validate_envelope` | HMAC authorization envelope |
| `validate_filter_result` | server filter response |

Every schema maps to a SPEC.md section so drift is caught at the boundary —
before it reaches the store, the wire, or the signing key.

## Tests

```bash
pytest tests/
```

31 tests across each validator and edge cases (extreme values, unknown fields,
malformed envelopes).

## How it fits

Layer 3 (observability) in [Gatekeeper](https://github.com/adam-scott-thomas/gate-keeper).
Used by `gate-compliance`'s `ValidatedCollector` and optionally by `gate-server`
request middleware.

## License

Apache-2.0.
