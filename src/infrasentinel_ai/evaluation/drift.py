from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from infrasentinel_ai.data.synthetic import FEATURE_COLUMNS


def population_stability_index(
    reference: pd.Series,
    current: pd.Series,
    buckets: int = 10,
) -> float:
    edges = np.unique(reference.quantile(np.linspace(0, 1, buckets + 1)).to_numpy())
    if len(edges) <= 2:
        return 0.0
    ref_counts = pd.cut(reference, bins=edges, include_lowest=True).value_counts(normalize=True)
    cur_counts = pd.cut(current, bins=edges, include_lowest=True).value_counts(normalize=True)
    aligned = pd.concat([ref_counts, cur_counts], axis=1).fillna(0.0001)
    aligned.columns = ["reference", "current"]
    aligned = aligned.clip(lower=0.0001)
    ratio = np.log(aligned["current"] / aligned["reference"])
    psi = ((aligned["current"] - aligned["reference"]) * ratio).sum()
    return round(float(psi), 5)


def drift_report(reference: pd.DataFrame, current: pd.DataFrame) -> dict[str, object]:
    feature_scores: dict[str, float] = {}
    for column in FEATURE_COLUMNS:
        feature_scores[column] = population_stability_index(
            reference[column].astype(float),
            current[column].astype(float),
        )
    max_feature = max(feature_scores, key=lambda feature: feature_scores[feature])
    return {
        "summary": {
            "max_drift_feature": max_feature,
            "max_psi": feature_scores[max_feature],
            "status": "attention_required" if feature_scores[max_feature] >= 0.2 else "stable",
        },
        "features": feature_scores,
    }


def write_drift_report(
    reference_path: Path,
    current_path: Path,
    report_path: Path,
) -> dict[str, object]:
    report = drift_report(pd.read_csv(reference_path), pd.read_csv(current_path))
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report
