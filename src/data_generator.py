import os
import csv
import random
import datetime

def generate_telemetry_dataset(output_path, num_records=1200, seed=42):
    random.seed(seed)
    entities = ["Civil Infrastructure", "Public Health Supplies", "Municipal IT Services", "Defense Logistics", "Renewable Utilities"]
    locations = ["Federal Department A", "State Highway Admin", "City Water Authority", "Metro Transit Agency", "National Health Board"]
    start_date = datetime.date(2025, 1, 1)

    headers = ["record_id", "timestamp", "entity_type", "location_zone", "contract_amount", "single_bidder_flag", "anomaly_flag", "confidence_score"]
    rows = []

    for i in range(1, num_records + 1):
        dt = start_date + datetime.timedelta(days=random.randint(0, 360), minutes=random.randint(0, 1439))
        entity = random.choice(entities)
        loc = random.choice(locations)
        base_val = round(random.uniform(10.0, 95.0), 3)
        target_val = round(base_val * random.uniform(0.85, 1.35), 3)
        is_anomaly = 1 if (random.random() < 0.05 or base_val > 90.0) else 0
        conf = round(random.uniform(0.88, 0.99), 3)
        rows.append([f"REC-{i:05d}", dt.isoformat(), entity, loc, base_val, target_val, is_anomaly, conf])

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    return len(rows)

if __name__ == "__main__":
    generate_telemetry_dataset("data/raw_telemetry_sample.csv")
