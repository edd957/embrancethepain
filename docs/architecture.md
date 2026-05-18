# Architecture

InfraSentinel AI Security is a defensive infrastructure security platform built around a simple production-ready pattern:

1. Normalize server telemetry.
2. Score behavior with an anomaly detection model.
3. Enrich the score with deterministic security rules.
4. Retrieve relevant response playbooks.
5. Return an analyst-ready summary and recommended actions.

## Components

## Synthetic Telemetry

The data generator creates safe synthetic Linux server telemetry. It includes authentication activity, privilege activity, process volume, network egress, exposed ports, package installation activity, and time context.

## ML Model

The default model is `IsolationForest`, chosen because it is lightweight, auditable, CPU-friendly, and appropriate for anomaly detection demos without external services.

## Rule Engine

The rule engine detects high-signal defensive patterns:

- Successful SSH login after many failures.
- New user creation combined with sudo activity.
- Large outbound transfer with high connection fan-out.
- Package installation during off-hours.
- Unusually large listening-port surface.

## Analyst Workflow

The analyst workflow combines model score, rule findings, and retrieved playbooks into a response object suitable for SOC tools, dashboards, or ticket enrichment.

## API

- `GET /health`
- `POST /v1/score`
- `POST /v1/analyze`

## Production Extension Points

- Replace synthetic telemetry with logs from EDR, SIEM, cloud audit logs, or OpenTelemetry.
- Add authentication and tenant isolation to the API.
- Persist scores to a security data lake.
- Replace local TF-IDF retrieval with an enterprise knowledge base.
- Add model registry tracking and scheduled retraining.
