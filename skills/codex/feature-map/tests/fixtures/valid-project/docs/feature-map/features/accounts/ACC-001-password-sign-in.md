---
{
  "schema_version": 1,
  "id": "ACC-001",
  "title": "Password sign-in",
  "domain": "accounts",
  "capability": "Session access",
  "summary": "A registered customer can establish an authenticated session.",
  "actors": ["customer"],
  "surfaces": ["web", "api"],
  "lifecycle": "active",
  "implementation": "complete",
  "verification": "test-verified",
  "entry_points": ["/sign-in", "POST /api/sessions"],
  "depends_on": [],
  "code_refs": ["src/accounts.py#sign_in"],
  "test_refs": ["tests/test_accounts.py#test_sign_in"],
  "spec_refs": ["docs/product.md#sign-in"],
  "decision_refs": [],
  "last_verified": {
    "date": "2026-09-03",
    "methods": ["python3 -m unittest tests/test_accounts.py"]
  }
}
---

## Behavior

Valid credentials establish a session; invalid credentials do not.
