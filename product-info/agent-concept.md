---
title: BBVet Knowledge Custodian Concept
status: assignment-demo
updated: 2026-09-14
tags: [cab432, agent, rag, knowledge]
---

# BBVet Knowledge Custodian

## Problem

Product knowledge can become fragmented across:

- meeting transcripts;
- product documentation;
- decision logs;
- issues;
- mockups.

Finding the reasoning behind a decision can be slower than finding the current decision itself.

## Assignment demo goal

Build a small cloud-native AI agent that can:

1. answer questions using retrieved repository context;
2. expose selected repository actions through MCP tools;
3. asynchronously index newly added documents;
4. generate an autonomous weekly product summary.

## Example user questions

- What decisions were made about Clinic Health this month?
- What changed in the subscription model?
- Which open questions have appeared repeatedly?
- What did the latest meeting decide about unrealistic goals?
- Create a follow-up issue for unresolved confidence-band work.

## Weekly summary format

The autonomous weekly summary should contain:

### Key decisions
A short list of decisions made during the period.

### Open questions
Issues that have not yet been resolved.

### Actions
Clear follow-up items.

### Changed assumptions
Any decision that supersedes or materially changes an earlier direction.

## Test-only fact

The synthetic pilot cohort contains **18 clinics**.

The internal retrieval test known as **Project Lantern** uses a threshold of **72 points** to confirm that the agent has retrieved the expected document rather than answering from general knowledge.

These numbers are fictional and exist only to support CAB432 testing.
