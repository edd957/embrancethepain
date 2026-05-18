from __future__ import annotations

import json
from typing import Annotated

import pandas as pd
import typer
from rich.console import Console

from infrasentinel_ai.config import get_settings
from infrasentinel_ai.data.synthetic import write_default_datasets
from infrasentinel_ai.evaluation.drift import write_drift_report
from infrasentinel_ai.models.train import train_model

app = typer.Typer(help="InfraSentinel AI Security command line tools.")
console = Console()
RowsOption = Annotated[int, typer.Option(min=200)]


@app.command("generate-data")
def generate_data(rows: RowsOption = 6000) -> None:
    settings = get_settings()
    reference_path, current_path = write_default_datasets(
        settings.reference_data_path,
        settings.current_data_path,
        rows=rows,
        seed=settings.random_seed,
    )
    console.print(f"Wrote reference data to [bold]{reference_path}[/bold]")
    console.print(f"Wrote current data to [bold]{current_path}[/bold]")


@app.command("train")
def train() -> None:
    settings = get_settings()
    if not settings.reference_data_path.exists():
        write_default_datasets(settings.reference_data_path, settings.current_data_path)
    metrics = train_model(
        settings.reference_data_path,
        settings.model_path,
        settings.metrics_path,
        seed=settings.random_seed,
    )
    console.print_json(json.dumps(metrics))


@app.command("evaluate")
def evaluate() -> None:
    settings = get_settings()
    if not settings.metrics_path.exists():
        train()
    console.print(settings.metrics_path.read_text(encoding="utf-8"))


@app.command("drift-report")
def drift_report() -> None:
    settings = get_settings()
    if not settings.reference_data_path.exists() or not settings.current_data_path.exists():
        write_default_datasets(settings.reference_data_path, settings.current_data_path)
    report = write_drift_report(
        settings.reference_data_path,
        settings.current_data_path,
        settings.drift_report_path,
    )
    console.print_json(json.dumps(report))


@app.command("sample-event")
def sample_event() -> None:
    settings = get_settings()
    if not settings.current_data_path.exists():
        write_default_datasets(settings.reference_data_path, settings.current_data_path)
    row = pd.read_csv(settings.current_data_path).drop(columns=["is_security_anomaly"]).iloc[0]
    console.print_json(json.dumps(row.to_dict()))


@app.command("serve")
def serve() -> None:
    import uvicorn

    uvicorn.run("infrasentinel_ai.api.main:app", host="0.0.0.0", port=8000, reload=True)
