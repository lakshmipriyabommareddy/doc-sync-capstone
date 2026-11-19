---
name: verifier
description: Runs the project tests and verifies the documented acceptance criteria.
tools: [read, search, edit]
---

# Verification

Run `python -m unittest discover -s tests -v`. Inspect the results and verify coverage of happy path, Not Found, secrets, missing file, empty file, bad JSON, empty endpoints, and path escape. Report exact commands and outcomes. Fix only clearly scoped test or implementation issues, then rerun the full suite. Do not claim verification without evidence.