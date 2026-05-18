from pathlib import Path

from infrasentinel_ai.data.synthetic import generate_server_events
from infrasentinel_ai.models.inference import score_event
from infrasentinel_ai.models.train import load_model, train_model
from infrasentinel_ai.schemas import ServerEvent


def test_train_and_score_event(tmp_path: Path) -> None:
    data_path = tmp_path / "server_events.csv"
    model_path = tmp_path / "model.joblib"
    metrics_path = tmp_path / "metrics.json"
    generate_server_events(rows=800, seed=21).to_csv(data_path, index=False)

    metrics = train_model(data_path, model_path, metrics_path, seed=21)
    model = load_model(model_path)
    response = score_event(
        model,
        ServerEvent(
            host_id="srv-prod-042",
            cpu_percent=88,
            memory_percent=80,
            failed_ssh_logins=18,
            successful_ssh_logins=1,
            sudo_commands=9,
            new_user_created=True,
            process_count=340,
            outbound_connections=125,
            bytes_out_mb=920,
            listening_ports=18,
            package_install_count=4,
            hour_of_day=3,
            is_weekend=False,
        ),
    )

    assert metrics["roc_auc"] > 0.7
    assert 0 <= response.anomaly_score <= 1
    assert response.risk_level in {"low", "medium", "high", "critical"}
