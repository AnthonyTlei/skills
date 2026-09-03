---
{
  "schema_version": 1,
  "id": "PAY-001",
  "title": "Submit a payment",
  "domain": "payments",
  "capability": "Payment collection",
  "summary": "A signed-in customer can submit a payment to the configured provider.",
  "actors": ["customer", "payment-provider"],
  "surfaces": ["web", "api", "integration"],
  "lifecycle": "active",
  "implementation": "complete",
  "verification": "test-verified",
  "entry_points": ["/checkout", "POST /api/payments"],
  "depends_on": ["ACC-001"],
  "code_refs": ["src/payments.py#submit_payment"],
  "test_refs": ["tests/test_payments.py#test_submit_payment"],
  "spec_refs": ["docs/product.md#payments"],
  "decision_refs": [],
  "last_verified": {
    "date": "2026-09-03",
    "methods": ["python3 -m unittest tests/test_payments.py"]
  }
}
---

## Behavior

Submission records the provider result without treating a timeout as success.
