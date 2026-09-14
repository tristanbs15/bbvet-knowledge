---
date: 2026-08-28
meeting: Product Weekly
participants: [Alex, Sam, Jordan, Taylor]
synthetic: true
tags: [subscriptions, clinic-performance, prototypes]
---

# Product Weekly — 2026-08-28

> Synthetic meeting transcript for CAB432 testing. Names, numbers and discussion are fictionalised/sanitised.


## Transcript

**Alex:** I looked at the Essential proposal again. Removing internal performance completely makes the product harder to explain.

**Jordan:** I agree. If a clinic sees that it is below a peer benchmark but can't see whether its own trend is improving, we're creating an artificial break in the experience.

**Sam:** What if Essential gets just the headline metrics? Revenue, transactions and maybe one client activity measure.

**Taylor:** That feels better. Premium can still own the complete KPI library, drill-downs and longer history.

**Alex:** Let's prototype that split. We'll use the internal codename Northstar for the demo so we don't confuse it with production work.

**Jordan:** What should Clinic Health actually show first?

**Sam:** Maybe three statuses: On Track, Watch and At Risk. No red/yellow/green traffic-light language for now.

**Taylor:** I like that. We also need to avoid suggesting that benchmark median equals the "correct" goal.

## Decisions

- Move away from the idea that Essential contains no internal performance data.
- Prototype a reduced set of Clinic Performance metrics in Essential.
- Use On Track, Watch and At Risk as the synthetic Clinic Health progress states.

## Open questions

- Which exact KPIs belong in Essential?
- Should goal suggestions use cohort median, upper quartile or a range?
- How should target difficulty be communicated?

## Actions

- Build the Northstar prototype with a reduced Essential view.
- Draft goal-setting examples for Clinic Health.
