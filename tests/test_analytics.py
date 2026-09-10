import os
import pytest
from src.analytics_engine import AnalyticsEngine
from src.data_generator import generate_telemetry_dataset

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "raw_telemetry_sample.csv")

@pytest.fixture(scope="module")
def engine():
    if not os.path.isfile(DATA_PATH):
        generate_telemetry_dataset(DATA_PATH, num_records=200)
    return AnalyticsEngine(DATA_PATH)

def test_data_load_integrity(engine):
    assert len(engine.records) > 0
    first = engine.records[0]
    assert "record_id" in first
    assert "contract_amount" in first
    assert "single_bidder_flag" in first

def test_summary_statistics(engine):
    stats = engine.compute_summary_statistics()
    assert stats["record_count"] >= 100
    assert stats["mean"] > 0
    assert stats["stddev"] > 0
    assert stats["min"] <= stats["median"] <= stats["max"]
    assert stats["p95"] <= stats["p99"]

def test_anomaly_detection_threshold(engine):
    anomalies = engine.detect_statistical_anomalies(z_threshold=2.0)
    assert isinstance(anomalies, list)
    for a in anomalies:
        assert abs(a["z_score"]) >= 2.0

def test_group_by_entity(engine):
    grouped = engine.group_by_entity()
    assert len(grouped) > 0
    for ent, metrics in grouped.items():
        assert metrics["count"] > 0
        assert metrics["avg_value"] > 0
