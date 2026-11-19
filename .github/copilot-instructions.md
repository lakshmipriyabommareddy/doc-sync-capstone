# Copilot instructions

This repository syncs `sources/billing-api.json` into `docs/API.md` using the `docsync` Python package. Use only the Python standard library. The required documentation fields are `method`, `path`, `summary`, `auth`, and `owner`. Render missing, empty, null, or secret field values as `Not Found`; never invent or infer a value. A null owner must remain `Not Found`. Read local JSON only. If the source is missing, empty, invalid JSON, or otherwise invalid, leave the destination untouched. Keep source and destination paths within the repository root.

Run tests with `python -m unittest discover -s tests -v`.

Follow the workflow in order: requirements, architecture, design review, implementation plan, implementation, seven-area review, tests, and pull request. Design review and code review are read-only.