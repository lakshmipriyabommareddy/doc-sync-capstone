# 07 — Tests

After review findings are resolved, use the `verifier` agent. Run `python -m unittest discover -s tests -v`; check happy path, Not Found, secrets, missing file, empty file, bad JSON, empty endpoints, and path escape. Report exact outcomes and fix failures before rerunning.