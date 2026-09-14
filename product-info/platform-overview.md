---
title: BBVet Platform Overview
status: draft
updated: 2026-09-11
tags: [platform, structure, strategy]
---

# BBVet Platform Overview

## Product direction

The proposed BBVet experience is organised around three connected questions that a clinic owner or practice manager may ask:

1. **Industry Insight — "Where do I stand against my peers?"**
2. **Clinic Performance — "How has my clinic been performing?"**
3. **Clinic Health — "Am I moving toward the outcomes I care about?"**

The purpose of the restructuring is to reduce the feeling that BBVet is a collection of disconnected reports. The product should feel like one system in which benchmark data, clinic performance and goal progress reinforce each other.

## 1. Industry Insight

Industry Insight contains external benchmarking information. It is the evolution of the existing benchmark/reporting experience.

Primary user needs:

- compare the clinic with a relevant peer cohort;
- understand percentile positioning;
- review survey and industry report results;
- identify areas where the clinic differs materially from peers.

The product team currently expects Industry Insight to remain the broadest entry point for customers who want to understand their relative position.

## 2. Clinic Performance

Clinic Performance focuses on the clinic's own historical operating data.

Example views include:

- revenue health;
- transaction health;
- client activity;
- fee-type performance;
- selected operational KPIs;
- trends over time.

The important design distinction is that Clinic Performance is **internal benchmarking over time**, whereas Industry Insight is **external benchmarking against peers**.

## 3. Clinic Health

Clinic Health combines:

- the clinic's selected goals;
- current performance;
- historical performance;
- relevant industry benchmarks.

It should answer whether the clinic is progressing toward a chosen outcome and where management attention is most useful.

Current progress states are:

- **On Track**
- **Watch**
- **At Risk**

These state names are synthetic demo terminology for the CAB432 project.

## Design principles

- Start with a small number of clear insights.
- Avoid generic dashboard overload.
- Provide drill-down only when it helps a user make a decision.
- Explain why a metric matters, not only its value.
- Prefer connected navigation between insight, performance and health views.
