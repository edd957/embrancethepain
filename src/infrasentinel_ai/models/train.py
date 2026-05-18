from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import average_precision_score, roc_auc_score

from infrasentinel_ai.data.synthetic import FEATURE_COLUMNS, TARGET_COLUMN
from infrasentinel_ai.features.preprocess import build_pipeline


def train_model(
    data_path: Path,
    model_path: Path,
    metrics_path: Path,
    seed: int = 42,
) -> dict[str, float]:
    data = pd.read_csv(data_path)
    features = data[FEATURE_COLUMNS]
    labels = data[TARGET_COLUMN]
    model = IsolationForest(
        n_estimators=250,
        contamination=0.1,
        max_samples="auto",
        random_state=seed,
        n_jobs=-1,
    )
    pipeline = build_pipeline(model)
    pipeline.fit(features)

    anomaly_score = -pipeline.decision_function(features)
    metrics = {
        "roc_auc": round(float(roc_auc_score(labels, anomaly_score)), 4),
        "average_precision": round(float(average_precision_score(labels, anomaly_score)), 4),
        "rows": float(len(data)),
        "anomaly_rate": round(float(labels.mean()), 4),
    }

    model_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, model_path)
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics


def load_model(model_path: Path) -> Any:
    if not model_path.exists():
        raise FileNotFoundError(f"Model artifact not found: {model_path}")
    return joblib.load(model_path)
