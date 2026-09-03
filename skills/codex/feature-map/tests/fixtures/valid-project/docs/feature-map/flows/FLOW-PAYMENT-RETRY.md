---
{
  "schema_version": 1,
  "id": "FLOW-PAYMENT-RETRY",
  "title": "Worker retries an unsettled payment",
  "type": "system",
  "summary": "A scheduled worker submits a bounded retry.",
  "primary_actor": "retry-worker",
  "supporting_actors": ["payment-provider"],
  "lifecycle": "proposed",
  "entry_points": ["payment-retry job"],
  "steps": [
    {
      "feature": "PAY-002",
      "outcome": "One retry is attempted under the configured policy."
    }
  ],
  "external_systems": ["Payment provider"]
}
---

## Narrative

This flow remains proposed.
