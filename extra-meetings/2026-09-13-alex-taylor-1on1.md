---
date: 2026-09-13
meeting: 1-on-1
participants: [Alex, Taylor]
synthetic: true
tags: [knowledge-custodian, retrieval, testing]
---

# 1-on-1 — Alex & Taylor — 2026-09-13

> Synthetic meeting transcript for CAB432 testing. Names and discussion are fictionalised/sanitised.

## Transcript

**Alex:** We need one or two facts that are deliberately weird enough that we can prove the agent retrieved them rather than guessed.

**Taylor:** Like the Project Lantern threshold?

**Alex:** Exactly. Seventy-two points is good because there's no reason the model would know that otherwise.

**Taylor:** Could we add another one in a meeting rather than a product document?

**Alex:** Yes. Let's say the internal prototype review cadence is every 11 days.

**Taylor:** That's odd enough to be useful.

**Alex:** Good. Then we can ask the agent, "How often is the internal prototype review cadence?" If it says 11 days, we know it found this transcript.

**Taylor:** Perfect. Just make sure it's clearly synthetic.

## Notes

- Project Lantern threshold remains 72 points.
- New deterministic retrieval fact: the synthetic internal prototype review cadence is **every 11 days**.
- These facts exist only to test retrieval behaviour.

## Follow-up

- Add a retrieval test question for the 11-day cadence.
