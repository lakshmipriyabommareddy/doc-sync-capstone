---
applyTo: "docsync/**/*.py,tests/**/*.py"
---

Use Python standard library only. Keep functions focused and type-hinted where useful. Validate all source data before writing output; do not leak secrets in rendered documentation or error messages. Confine filesystem paths to the repository root and preserve the destination on missing or invalid input. Run tests with `python -m unittest discover -s tests -v`.