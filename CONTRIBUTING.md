# Contributing

Thank you for reviewing InfraSentinel AI Security.

## Development Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
make bootstrap
make test
```

## Pull Request Checklist

- Add or update tests for changed behavior.
- Run `ruff check .`, `mypy src`, and `pytest`.
- Update documentation when API behavior, model behavior, or security assumptions change.
- Keep examples defensive and safe for public review.

## Security Boundaries

This project is for defensive monitoring and alert triage. Do not contribute exploit code, credential theft logic, evasion tooling, persistence mechanisms, destructive automation, or instructions that would enable unauthorized access.
