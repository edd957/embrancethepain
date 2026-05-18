# InfraSentinel Security Playbooks

## SSH Brute Force Investigation

Review authentication logs for repeated failed SSH attempts, source address concentration, and successful access after failures. Validate whether the access pattern matches an approved administrator workflow.

## Privilege Escalation Review

Investigate new user creation, sudo command volume, group membership changes, and changes to authorized keys. Preserve relevant logs before remediation.

## Data Exfiltration Triage

Inspect outbound data volume, destination reputation, connection fan-out, and process ownership. If activity is unexplained, isolate non-essential network paths and preserve evidence.

## Unexpected Package Installation

Review package manager logs, installation time, initiating user, and associated process tree. Validate against approved maintenance windows and change records.

## Attack Surface Expansion

Review newly listening ports, bound interfaces, firewall changes, and service owners. Close unnecessary exposure and confirm the service is documented.

## Drift Response

When telemetry drift exceeds the attention threshold, compare recent host behavior against the reference period, review infrastructure changes, and decide whether thresholds or model retraining are required.
