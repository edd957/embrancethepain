from infrasentinel_ai.rules.engine import evaluate_rules
from infrasentinel_ai.schemas import ServerEvent


def test_rules_detect_privilege_escalation_pattern() -> None:
    event = ServerEvent(
        host_id="srv-test-001",
        cpu_percent=80,
        memory_percent=70,
        failed_ssh_logins=20,
        successful_ssh_logins=1,
        sudo_commands=8,
        new_user_created=True,
        process_count=300,
        outbound_connections=120,
        bytes_out_mb=900,
        listening_ports=20,
        package_install_count=4,
        hour_of_day=2,
        is_weekend=False,
    )

    findings = evaluate_rules(event)
    rule_ids = {finding.rule_id for finding in findings}

    assert "AUTH-001" in rule_ids
    assert "PRIV-001" in rule_ids
    assert "NET-001" in rule_ids
