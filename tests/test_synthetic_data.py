from infrasentinel_ai.data.synthetic import FEATURE_COLUMNS, TARGET_COLUMN, generate_server_events


def test_generate_server_events_shape() -> None:
    data = generate_server_events(rows=300, seed=7)

    assert list(data.columns) == ["host_id", *FEATURE_COLUMNS, TARGET_COLUMN]
    assert len(data) == 300
    assert data[TARGET_COLUMN].isin([0, 1]).all()


def test_drifted_server_events_change_distribution() -> None:
    reference = generate_server_events(rows=500, seed=7, drift=False)
    current = generate_server_events(rows=500, seed=7, drift=True)

    assert current["failed_ssh_logins"].mean() > reference["failed_ssh_logins"].mean()
