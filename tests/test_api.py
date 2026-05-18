from pathlib import Path

from fastapi.testclient import TestClient

from infrasentinel_ai.api.main import app
from infrasentinel_ai.config import get_settings
from infrasentinel_ai.data.synthetic import generate_server_events
from infrasentinel_ai.models.train import train_model


def test_health_endpoint() -> None:
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_score_endpoint(tmp_path: Path, monkeypatch) -> None:
    model_path = tmp_path / "model.joblib"
    metrics_path = tmp_path / "metrics.json"
    data_path = tmp_path / "server_events.csv"
    generate_server_events(rows=800, seed=31).to_csv(data_path, index=False)
    train_model(data_path, model_path, metrics_path, seed=31)

    settings = get_settings()
    monkeypatch.setattr(settings, "model_path", model_path)
    from infrasentinel_ai.api import main

    main.get_model.cache_clear()
    client = TestClient(app)
    response = client.post(
        "/v1/score",
        json={
            "host_id": "srv-test-001",
            "cpu_percent": 55,
            "memory_percent": 62,
            "failed_ssh_logins": 2,
            "successful_ssh_logins": 1,
            "sudo_commands": 1,
            "new_user_created": False,
            "process_count": 140,
            "outbound_connections": 20,
            "bytes_out_mb": 50,
            "listening_ports": 5,
            "package_install_count": 0,
            "hour_of_day": 13,
            "is_weekend": False,
        },
    )

    assert response.status_code == 200
    assert "risk_score" in response.json()
