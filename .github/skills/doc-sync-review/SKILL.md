# Documentation sync review skill

Use this checklist when reviewing the billing API JSON-to-Markdown sync.

## Correctness
- Confirm the documented values come only from the source and required fields are `method`, `path`, `summary`, `auth`, and `owner`.
- Missing, empty, null, or secret values are rendered exactly as `Not Found`; never infer values. A null owner remains `Not Found`.
- Empty endpoint arrays are valid and produce a useful document.

## Security
- Read local JSON only; do not fetch URLs or execute source content.
- Detect and suppress secret values rather than exposing them in Markdown or error messages.
- Resolve and constrain source and destination paths to the repository root, including symlink-aware resolution.

## Error handling
- Missing, empty, malformed, or structurally invalid input must fail safely and leave the destination unchanged.
- Errors should be actionable without leaking source secrets. Avoid partial destination writes.

## Test coverage
- Verify happy path, Not Found, secrets, missing file, empty file, bad JSON, empty endpoints, and path escape.
- Assert invalid source cases preserve pre-existing output.

## Code clarity
- Keep validation, redaction, rendering, and file operations understandable and focused.
- Make failure behavior and path assumptions explicit.

## DRY
- Centralize required fields, missing-value handling, and secret detection; avoid duplicated transformations.

## Dependency safety
- Use Python standard library only. Do not add runtime or test dependencies.