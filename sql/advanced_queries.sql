-- ==========================================================
-- Advanced Analytical Window Functions & Statistical CTEs
-- Repository: GovSpend-Public-Procurement-Integrity-Analytics
-- Author: Abdussatar (@abdussatarkhan)
-- ==========================================================

WITH daily_aggregates AS (
    SELECT
        d.full_date,
        e.entity_name,
        COUNT(f.event_id) AS event_count,
        AVG(f.contract_amount) AS avg_metric_val,
        AVG(f.single_bidder_flag) AS avg_target_val,
        SUM(f.anomaly_flag) AS total_anomalies
    FROM fact_contract_award f
    JOIN dim_date d ON f.date_key = d.date_key
    JOIN dim_entity e ON f.entity_key = e.entity_key
    GROUP BY d.full_date, e.entity_name
),
rolling_window_metrics AS (
    SELECT
        full_date,
        entity_name,
        avg_metric_val,
        -- 7-Day Rolling Moving Average
        AVG(avg_metric_val) OVER(
            PARTITION BY entity_name
            ORDER BY full_date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS rolling_7d_avg,
        -- 30-Day Rolling Population Standard Deviation
        STDDEV_POP(avg_metric_val) OVER(
            PARTITION BY entity_name
            ORDER BY full_date
            ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
        ) AS rolling_30d_stddev,
        -- Window Rank by Volume
        DENSE_RANK() OVER(
            PARTITION BY full_date
            ORDER BY event_count DESC
        ) AS daily_volume_rank
    FROM daily_aggregates
)
SELECT
    full_date,
    entity_name,
    ROUND(avg_metric_val, 4) AS observed_value,
    ROUND(rolling_7d_avg, 4) AS rolling_7d_baseline,
    -- Standardized Statistical Z-Score
    CASE 
        WHEN rolling_30d_stddev > 0.0001 THEN 
            ROUND((avg_metric_val - rolling_7d_avg) / rolling_30d_stddev, 3)
        ELSE 0.000
    END AS statistical_z_score,
    daily_volume_rank
FROM rolling_window_metrics
ORDER BY full_date DESC, statistical_z_score DESC;
