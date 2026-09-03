---
{
  "schema_version": 1,
  "id": "FLOW-CHECKOUT",
  "title": "Customer completes checkout",
  "type": "user",
  "summary": "A customer signs in and submits a payment.",
  "primary_actor": "customer",
  "supporting_actors": ["payment-provider"],
  "lifecycle": "active",
  "entry_points": ["/checkout"],
  "steps": [
    {
      "feature": "ACC-001",
      "outcome": "The customer establishes a session."
    },
    {
      "feature": "PAY-001",
      "outcome": "The payment result is recorded."
    }
  ],
  "external_systems": ["Payment provider"]
}
---

## Narrative

The provider boundary remains explicit in the payment feature.
