# Threat Model

## Protected Assets

- Linux servers and workloads
- Authentication systems
- Privileged accounts
- Operational logs and telemetry
- Incident response workflows

## Defensive Goals

- Detect unusual infrastructure activity early.
- Explain why a server event was considered risky.
- Help analysts triage alerts consistently.
- Avoid storing or publishing sensitive telemetry.

## Out of Scope

- Exploitation
- Credential harvesting
- Malware execution
- Persistence tooling
- Evasion logic
- Unauthorized scanning or access

## Assumptions

- Events are collected from approved telemetry sources.
- Analysts review high-impact actions before enforcement.
- Production deployments enforce authentication, authorization, and audit logging around the API.
