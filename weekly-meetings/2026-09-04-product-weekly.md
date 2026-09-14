---
date: 2026-09-04
meeting: Product Weekly
participants: [Alex, Sam, Jordan, Taylor]
synthetic: true
tags: [goals, benchmarks, subscriptions]
---

# Product Weekly — 2026-09-04

> Synthetic meeting transcript for CAB432 testing. Names, numbers and discussion are fictionalised/sanitised.


## Transcript

**Sam:** I tested the goal-setting idea with synthetic clinic data. A fixed benchmark target feels too prescriptive.

**Taylor:** Then benchmark data should probably be context, not the goal itself.

**Alex:** So if the cohort range is 3.3 to 3.7 transactions per active client, we might suggest 3.3, but the clinic could still choose 3.2 or 3.5.

**Jordan:** Yes, and the timeframe matters just as much. Moving from 2.9 to 3.5 in one month is different from doing it over twelve months.

**Sam:** We could calculate a difficulty indicator from current value, target gap, recent rate of change and timeframe.

**Taylor:** Important point: do not prevent users from choosing something difficult. Warn them, explain it, but don't block them.

**Alex:** On subscriptions, I think we're ready to lock the headline direction. Essential gets selected internal metrics. Premium keeps the full internal benchmarking suite.

**Jordan:** That also makes the transition into Clinic Health make more sense.

## Decisions

- Essential will include selected internal performance metrics.
- Premium retains the full internal benchmarking capability.
- Benchmarks may suggest Clinic Health targets, but the clinic chooses its final target and timeframe.
- Ambitious targets should be explained rather than blocked.

## Open questions

- Numeric difficulty score versus labels.
- How much historical data should feed the difficulty calculation?
- Should Premium expose What-If modelling immediately or in a later release?

## Actions

- Update the subscription-model document.
- Draft a simple difficulty calculation for prototype use.
