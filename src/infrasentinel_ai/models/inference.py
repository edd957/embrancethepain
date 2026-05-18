from __future__ import annotations

from typing import Any

import pandas as pd

from infrasentinel_ai.data.synthetic import FEATURE_COLUMNS
from infrasentinel_ai.rules.engine import evaluate_rules
from infrasentinel_ai.schemas import ScoreResponse, ServerEvent


def score_event(model: Any, event: ServerEvent) -> ScoreResponse:
    frame = pd.DataFrame([event.model_dump()])[FEATURE_COLUMNS]
    raw_score = float(-model.decision_function(frame)[0])
    normalized_score = _normalize_anomaly_score(raw_score)
    findings = evaluate_rules(event)
    rule_boost = sum(_severity_weight(finding.severity) for finding in findings)
    risk_score = min(100, round(normalized_score * 70 + rule_boost))
    return ScoreResponse(
        host_id=event.host_id,
        anomaly_score=round(normalized_score, 4),
        risk_score=risk_score,
        risk_level=risk_level(risk_score),
        top_signals=top_signals(event, normalized_score),
        findings=findings,
    )


def _normalize_anomaly_score(raw_score: float) -> float:
    return max(0.0, min(1.0, 1 / (1 + pow(2.718281828, -8 * raw_score))))


def _severity_weight(severity: str) -> int:
    return {"critical": 28, "high": 18, "medium": 10, "low": 4}[severity]


def risk_level(score: int) -> str:
    if score >= 85:
        return "critical"
    if score >= 65:
        return "high"
    if score >= 40:
        return "medium"
    return "low"


def top_signals(event: ServerEvent, anomaly_score: float) -> list[str]:
    signals: list[str] = []
    if anomaly_score >= 0.7:
        signals.append("High model anomaly score")
    if event.failed_ssh_logins >= 10:
        signals.append("Elevated failed SSH logins")
    if event.sudo_commands >= 8:
        signals.append("Unusual sudo command volume")
    if event.new_user_created:
        signals.append("New local user creation")
    if event.bytes_out_mb >= 500:
        signals.append("Large outbound data transfer")
    if event.outbound_connections >= 100:
        signals.append("High outbound connection count")
    if event.hour_of_day <= 5 or event.hour_of_day >= 22:
        signals.append("Off-hours activity")
    return signals or ["No dominant suspicious signal"]
