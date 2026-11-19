# User story: Automated billing API documentation sync

As a maintainer of the billing API, I want to generate `docs/API.md` from `sources/billing-api.json` so the published API reference reflects the local source consistently without exposing secrets or inventing missing details.

## Acceptance criteria

- The sync reads a local JSON source and writes a Markdown API reference.
- Each endpoint documents `method`, `path`, `summary`, `auth`, and `owner`.
- Missing, empty, null, or secret field values appear as `Not Found`; values are never inferred.
- Empty endpoint collections are valid.
- Missing, empty, malformed, or structurally invalid sources leave the destination untouched.
- Source and destination paths cannot escape the repository root.
- The implementation and tests use only the Python standard library.

## Decisions

- A null `owner` stays as `Not Found`.
- Read local JSON only; do not retrieve remote sources.
- Write nothing when the source is missing or invalid (including empty or malformed JSON).

## Verification

Run `python -m unittest discover -s tests -v`.