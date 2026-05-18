from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

FEATURE_COLUMNS = [
    "cpu_percent",
    "memory_percent",
    "failed_ssh_logins",
    "successful_ssh_logins",
    "sudo_commands",
    "new_user_created",
    "process_count",
    "outbound_connections",
    "bytes_out_mb",
    "listening_ports",
    "package_install_count",
    "hour_of_day",
    "is_weekend",
]

TARGET_COLUMN = "is_security_anomaly"


def generate_server_events(rows: int = 6000, seed: int = 42, drift: bool = False) -> pd.DataFrame:
    """Generate safe synthetic server telemetry for defensive ML development."""

    rng = np.random.default_rng(seed)
    anomaly_rate = 0.08 if not drift else 0.14
    anomaly = rng.binomial(1, anomaly_rate, rows)

    cpu_percent = rng.normal(38 if not drift else 44, 14, rows) + anomaly * rng.normal(28, 9, rows)
    memory_percent = (
        rng.normal(54 if not drift else 58, 12, rows) + anomaly * rng.normal(18, 8, rows)
    )
    failed_ssh_logins = (
        rng.poisson(1.4 if not drift else 2.0, rows) + anomaly * rng.poisson(18, rows)
    )
    successful_ssh_logins = rng.poisson(2.5, rows) + anomaly * rng.poisson(1.5, rows)
    sudo_commands = rng.poisson(1.8, rows) + anomaly * rng.poisson(8, rows)
    new_user_created = rng.binomial(1, 0.015 + anomaly * 0.22, rows)
    process_count = rng.normal(145, 38, rows) + anomaly * rng.normal(120, 35, rows)
    outbound_connections = (
        rng.poisson(24 if not drift else 31, rows) + anomaly * rng.poisson(85, rows)
    )
    bytes_out_mb = rng.gamma(2.0, 28, rows) + anomaly * rng.gamma(4.0, 120, rows)
    listening_ports = rng.poisson(5, rows) + anomaly * rng.poisson(8, rows)
    package_install_count = rng.poisson(0.25, rows) + anomaly * rng.poisson(3, rows)
    hour_of_day = rng.integers(0, 24, rows)
    is_weekend = rng.binomial(1, 0.28, rows)

    off_hours = ((hour_of_day <= 5) | (hour_of_day >= 22)).astype(int)
    anomaly = np.maximum(
        anomaly,
        (
            (failed_ssh_logins > 12)
            & (sudo_commands > 5)
            & ((new_user_created == 1) | (off_hours == 1))
        ).astype(int),
    )

    return pd.DataFrame(
        {
            "host_id": [f"srv-{seed}-{index:05d}" for index in range(rows)],
            "cpu_percent": np.clip(cpu_percent, 0, 100).round(2),
            "memory_percent": np.clip(memory_percent, 0, 100).round(2),
            "failed_ssh_logins": failed_ssh_logins.astype(int),
            "successful_ssh_logins": successful_ssh_logins.astype(int),
            "sudo_commands": sudo_commands.astype(int),
            "new_user_created": new_user_created.astype(bool),
            "process_count": np.clip(process_count, 1, 5000).astype(int),
            "outbound_connections": outbound_connections.astype(int),
            "bytes_out_mb": bytes_out_mb.round(2),
            "listening_ports": listening_ports.astype(int),
            "package_install_count": package_install_count.astype(int),
            "hour_of_day": hour_of_day.astype(int),
            "is_weekend": is_weekend.astype(bool),
            TARGET_COLUMN: anomaly.astype(int),
        }
    )


def write_default_datasets(
    reference_path: Path,
    current_path: Path,
    rows: int = 6000,
    seed: int = 42,
) -> tuple[Path, Path]:
    reference_path.parent.mkdir(parents=True, exist_ok=True)
    current_path.parent.mkdir(parents=True, exist_ok=True)
    generate_server_events(rows=rows, seed=seed, drift=False).to_csv(reference_path, index=False)
    generate_server_events(rows=max(rows // 2, 200), seed=seed + 17, drift=True).to_csv(
        current_path,
        index=False,
    )
    return reference_path, current_path
