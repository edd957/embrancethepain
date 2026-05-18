from __future__ import annotations

from infrasentinel_ai.schemas import RuleFinding, ServerEvent


def evaluate_rules(event: ServerEvent) -> list[RuleFinding]:
    findings: list[RuleFinding] = []
    off_hours = event.hour_of_day <= 5 or event.hour_of_day >= 22

    if event.failed_ssh_logins >= 15 and event.successful_ssh_logins >= 1:
        findings.append(
            RuleFinding(
                rule_id="AUTH-001",
                severity="high",
                message="Successful login after elevated failed SSH attempts.",
            )
        )
    if event.new_user_created and event.sudo_commands >= 5:
        findings.append(
            RuleFinding(
                rule_id="PRIV-001",
                severity="critical",
                message="New user creation combined with elevated sudo activity.",
            )
        )
    if event.bytes_out_mb >= 750 and event.outbound_connections >= 80:
        findings.append(
            RuleFinding(
                rule_id="NET-001",
                severity="high",
                message="Large outbound transfer with high connection fan-out.",
            )
        )
    if event.package_install_count >= 3 and off_hours:
        findings.append(
            RuleFinding(
                rule_id="OPS-001",
                severity="medium",
                message="Package installation activity during off-hours.",
            )
        )
    if event.listening_ports >= 15:
        findings.append(
            RuleFinding(
                rule_id="SURFACE-001",
                severity="medium",
                message="Unusually large number of listening ports.",
            )
        )

    return findings
