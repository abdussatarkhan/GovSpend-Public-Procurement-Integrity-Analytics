import csv
import math
from collections import defaultdict

class AnalyticsEngine:
    """High-performance statistical modeling & analytics engine for GovSpend: Public Sector Procurement & Collusion Risk Intelligence."""

    def __init__(self, data_file_path):
        self.data_file_path = data_file_path
        self.records = []
        self.load_data()

    def load_data(self):
        with open(self.data_file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.records.append({
                    "record_id": row["record_id"],
                    "timestamp": row["timestamp"],
                    "entity_type": row["entity_type"],
                    "location_zone": row["location_zone"],
                    "contract_amount": float(row["contract_amount"]),
                    "single_bidder_flag": float(row["single_bidder_flag"]),
                    "anomaly_flag": int(row["anomaly_flag"]),
                    "confidence_score": float(row["confidence_score"])
                })

    def compute_summary_statistics(self):
        vals = [r["contract_amount"] for r in self.records]
        if not vals:
            return {}
        n = len(vals)
        mean_val = sum(vals) / n
        variance = sum((x - mean_val) ** 2 for x in vals) / (n - 1 if n > 1 else 1)
        stddev = math.sqrt(variance)
        sorted_vals = sorted(vals)
        p50 = sorted_vals[int(n * 0.50)]
        p95 = sorted_vals[int(n * 0.95)]
        p99 = sorted_vals[int(n * 0.99)]

        return {
            "record_count": n,
            "mean": round(mean_val, 4),
            "stddev": round(stddev, 4),
            "median": round(p50, 4),
            "p95": round(p95, 4),
            "p99": round(p99, 4),
            "min": round(sorted_vals[0], 4),
            "max": round(sorted_vals[-1], 4)
        }

    def detect_statistical_anomalies(self, z_threshold=2.5):
        stats = self.compute_summary_statistics()
        mean = stats["mean"]
        std = stats["stddev"]
        anomalies = []
        for r in self.records:
            if std > 0:
                z = (r["contract_amount"] - mean) / std
                if abs(z) >= z_threshold:
                    anomalies.append({
                        "record_id": r["record_id"],
                        "entity_type": r["entity_type"],
                        "value": r["contract_amount"],
                        "z_score": round(z, 3)
                    })
        return anomalies

    def group_by_entity(self):
        grouped = defaultdict(list)
        for r in self.records:
            grouped[r["entity_type"]].append(r["contract_amount"])
        result = {}
        for ent, vals in grouped.items():
            result[ent] = {
                "count": len(vals),
                "avg_value": round(sum(vals) / len(vals), 3),
                "max_value": round(max(vals), 3)
            }
        return result
