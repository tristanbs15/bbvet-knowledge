---
date: 2026-09-11
meeting: Product Weekly
participants: [Alex, Sam, Jordan, Taylor]
synthetic: true
tags: [clinic-health, confidence, agent, weekly-summary]
---

# Product Weekly — 2026-09-11

> Synthetic meeting transcript for CAB432 testing. Names, numbers and discussion are fictionalised/sanitised.


## Transcript

**Alex:** One issue with the current Clinic Health prototype is that the projection looks too certain. It draws a single future line even when the history is noisy.

**Jordan:** Could we show a range instead?

**Sam:** Maybe a confidence band around projected performance. We shouldn't overstate the statistical sophistication, but it would communicate uncertainty better than one line.

**Taylor:** I like the idea as exploration. Don't mark it as a final requirement yet.

**Alex:** Agreed.

**Jordan:** For the CAB432 Knowledge Custodian demo, what should the weekly autonomous run actually do?

**Sam:** Keep it simple. Look at knowledge added during the week and produce four sections: decisions, open questions, actions and changed assumptions.

**Taylor:** Store a run record with the timestamp as proof that it happened autonomously.

**Alex:** Good. Let's use 18 synthetic clinics as the pilot cohort in the demo documents so we have a distinctive retrieval fact.

**Jordan:** We also need a deterministic retrieval test.

**Sam:** Let's use Project Lantern. If the agent can retrieve the 72-point threshold from the documentation, we know it isn't guessing from general knowledge.

## Decisions

- Investigate a confidence band for Clinic Health projections; this is exploratory, not final.
- The autonomous weekly summary will contain decisions, open questions, actions and changed assumptions.
- Store a persistent run record for each scheduled execution.
- Use 18 synthetic clinics as the demo pilot cohort.
- Project Lantern retrieval threshold is 72 points.

## Open questions

- What confidence method would be appropriate in a production implementation?
- Should the weekly summary be committed to Git, stored in DynamoDB, or both?
- Should repeated unresolved questions be automatically promoted into GitHub issues?

## Actions

- Implement the scheduled EventBridge workflow.
- Add persistent agent-run storage.
- Add Project Lantern as a deterministic retrieval test.
