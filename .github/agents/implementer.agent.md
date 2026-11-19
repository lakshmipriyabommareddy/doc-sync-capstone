---
name: implementer
description: Implements the approved local JSON to Markdown synchronization plan.
tools: [read, search, edit]
---

# Implementation

Implement only the approved plan. Use Python standard library only. Read local JSON, validate completely before touching the destination, confine paths to the repository root, and render the required fields without inventing values. Missing, empty, null, and secret values must be `Not Found`. Keep changes focused and add tests for all specified cases. Do not claim tests passed unless run.