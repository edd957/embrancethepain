from __future__ import annotations

from functools import lru_cache
from typing import Any

from fastapi import FastAPI, HTTPException

from infrasentinel_ai import __version__
from infrasentinel_ai.agents.workflow import analyze_event
from infrasentinel_ai.config import get_settings
from infrasentinel_ai.models.inference import score_event
from infrasentinel_ai.models.train import load_model
from infrasentinel_ai.rag.playbooks import PlaybookRetriever
from infrasentinel_ai.schemas import AnalysisResponse, HealthResponse, ScoreResponse, ServerEvent

app = FastAPI(
    title="InfraSentinel AI Security",
    version=__version__,
    description=(
        "Defensive ML/AI service for infrastructure anomaly detection, "
        "server risk scoring, and alert triage."
    ),
)


@lru_cache
def get_model() -> Any:
    return load_model(get_settings().model_path)


@lru_cache
def get_retriever() -> PlaybookRetriever:
    return PlaybookRetriever.from_markdown(get_settings().playbook_path)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="ok",
        model_loaded=settings.model_path.exists(),
        version=__version__,
    )


@app.post("/v1/score", response_model=ScoreResponse)
def score(event: ServerEvent) -> ScoreResponse:
    try:
        return score_event(get_model(), event)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=503,
            detail="Model artifact is missing. Run `infrasentinel train`.",
        ) from exc


@app.post("/v1/analyze", response_model=AnalysisResponse)
def analyze(event: ServerEvent) -> AnalysisResponse:
    try:
        return analyze_event(get_model(), get_retriever(), event)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
