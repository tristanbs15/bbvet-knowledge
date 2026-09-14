# BBVet Knowledge Repository — Assignment 2 Demo

> **Important:** This repository contains synthetic/sanitised demo content created for a CAB432 cloud-computing assessment. It is not a source of truth for BBVet and should not contain confidential business, customer, employee, financial, or personal information.

## Purpose

This repository acts as the knowledge source for the **BBVet Knowledge Custodian** agent.

The agent is intended to:

- answer natural-language questions about product documentation and meeting history;
- retrieve relevant context semantically rather than relying on keyword search;
- identify recent product decisions and unresolved questions;
- process newly added knowledge asynchronously;
- generate an autonomous weekly product summary.

## Repository structure

- `meetings/` — synthetic weekly product meeting transcripts.
- `product/` — current product concept documentation.
- `decisions/` — concise decision log used as a canonical reference.
- `summaries/` — output location for generated weekly summaries.
- `images/` — optional product screenshots/mockups for multimodal testing.

## Suggested demo questions

Try asking the future agent questions such as:

1. What are the three main areas of the proposed BBVet platform?
2. Why does Clinic Health exist?
3. What changed in the proposed Essential tier between August and September?
4. Which meeting introduced the "confidence band" idea?
5. What unresolved questions remain around clinic-set goals?
6. What was Project Lantern's test threshold?
7. What decisions from the most recent meeting superseded earlier thinking?
8. Summarise all discussion relating to AI-generated interpretation.

## Synthetic test facts

Several deliberately distinctive facts are included so retrieval can be verified during the assessment. For example:

- **Project Lantern test threshold:** 72 points.
- **Pilot cohort size:** 18 synthetic clinics.
- **Clinic Health progress state names:** On Track, Watch, At Risk.
- **Internal prototype codename:** Northstar.

These facts are intentionally fictional.
