---
date: 2026-09-12
meeting: 1-on-1
participants: [Sam, Taylor]
synthetic: true
tags: [knowledge-custodian, weekly-summary, actions]
---

# 1-on-1 — Sam & Taylor — 2026-09-12

> Synthetic meeting transcript for CAB432 testing. Names and discussion are fictionalised/sanitised.

## Transcript

**Sam:** For the weekly Knowledge Custodian summary, I think it needs to distinguish decisions from discussion.

**Taylor:** Absolutely. Otherwise a half-formed idea from a transcript could get presented as settled.

**Sam:** We already have decisions, open questions and actions. Should we add "changed assumptions"?

**Taylor:** Yes. That's useful because the repo will contain older documents that are still semantically relevant even after a decision changes.

**Sam:** Good point. The retrieval layer might surface an older statement, so the agent needs to understand chronology.

**Taylor:** Which means the weekly summary should explicitly call out when something supersedes an earlier direction.

**Sam:** Another thought: repeated unresolved questions could eventually become GitHub issues automatically.

**Taylor:** Good future extension, but not for the assignment minimum.

## Notes

- Weekly summaries must distinguish settled decisions from discussion.
- Include a "changed assumptions" section.
- Chronology matters because vector retrieval may surface superseded information.
- Automatic issue creation from repeated unresolved questions is a future extension, not MVP.

## Follow-up

- Keep automatic issue promotion out of the CAB432 minimum scope.
