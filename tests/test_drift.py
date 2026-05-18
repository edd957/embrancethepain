from infrasentinel_ai.data.synthetic import generate_server_events
from infrasentinel_ai.evaluation.drift import drift_report, population_stability_index


def test_population_stability_index_zero_for_same_series() -> None:
    data = generate_server_events(rows=500, seed=11)

    assert population_stability_index(data["cpu_percent"], data["cpu_percent"]) == 0.0


def test_drift_report_contains_summary() -> None:
    reference = generate_server_events(rows=800, seed=11, drift=False)
    current = generate_server_events(rows=800, seed=12, drift=True)
    report = drift_report(reference, current)

    assert "summary" in report
    assert "features" in report
    assert report["summary"]["max_psi"] >= 0
