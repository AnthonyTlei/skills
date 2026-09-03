---
{
  "schema_version": 1,
  "id": "PAY-002",
  "title": "Retry an unsettled payment",
  "domain": "payments",
  "capability": "Payment recovery",
  "summary": "A background worker can retry an unsettled provider request.",
  "actors": ["retry-worker", "payment-provider"],
  "surfaces": ["worker", "integration"],
  "lifecycle": "proposed",
  "implementation": "absent",
  "verification": "unverified",
  "entry_points": ["payment-retry job"],
  "depends_on": ["PAY-001"],
  "code_refs": [],
  "test_refs": [],
  "spec_refs": ["docs/product.md#payment-retries"],
  "decision_refs": []
}
---

## Behavior

Retry policy remains proposed and is not represented as implemented behavior.
