from __future__ import annotations

from typing import Any

from infrasentinel_ai.models.inference import score_event
from infrasentinel_ai.rag.playbooks import PlaybookRetriever
from infrasentinel_ai.schemas import AnalysisResponse, ServerEvent


def analyze_event(model: Any, retriever: PlaybookRetriever, event: ServerEvent) -> AnalysisResponse:
    score = score_event(model, event)
    query = " ".join(
        [
            score.risk_level,
            *score.top_signals,
            *[finding.message for finding in score.findings],
        ]
    )
    playbooks = retriever.search(query, top_k=3)
    return AnalysisResponse(
        score=score,
        retrieved_playbooks=playbooks,
        analyst_summary=_summary(score.risk_level, score.risk_score, score.top_signals),
        recommended_actions=_actions(score.risk_level),
    )


def _summary(level: str, score: int, signals: list[str]) -> str:
    return (
        f"Infrastructure event is classified as {level} risk with score {score}. "
        f"Primary signals: {', '.join(signals)}."
    )


def _actions(level: str) -> list[str]:
    if level == "critical":
        return [
            "Isolate host from non-essential network paths.",
            "Preserve volatile evidence and relevant logs.",
            "Rotate credentials associated with recent access.",
            "Escalate to incident response lead immediately.",
        ]
    if level == "high":
        return [
            "Open a security investigation case.",
            "Review authentication, sudo, process, and outbound network logs.",
            "Apply temporary access restrictions while validating activity.",
        ]
    if level == "medium":
        return [
            "Queue for analyst review.",
            "Increase monitoring sensitivity for the host for 24 hours.",
        ]
    return ["Log the event and continue normal monitoring."]
