# gate-schema — Integration Map

## What It Validates

| Artifact | Schema | Used By |
|----------|--------|---------|
| Tool manifest | tool.schema.json | gate-server (request validation), gate-sdk (registration) |
| Policy document | policy.schema.json | gate-policy (YAML loading), gate-server (policy endpoints) |
| Authorization envelope | envelope.schema.json | gate-server (envelope endpoints), gate-guard (enforcement) |
| Filter result | filter-result.schema.json | gate-dashboard (API response), gate-compliance (audit records) |

## Integration Points

| Component | How gate-schema connects |
|-----------|------------------------|
| gate-core | Schemas derived from SPEC.md, aligned with schema/ directory |
| gate-server | Request validation middleware (stub placed) |
| gate-policy | YAML policy validation before loading |
| gate-compliance | Audit record schema validation |
| gate-sdk | Tool registration validation |
| CI/CD | Conformance test suite for any Gate implementation |
