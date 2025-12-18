CREATE TABLE IF NOT EXISTS sensor_readings (
    ts TIMESTAMP,
    sensor_id TEXT,
    temperature DOUBLE PRECISION,
    humidity DOUBLE PRECISION,
    pressure DOUBLE PRECISION,
    anomaly_flag INTEGER,
    is_anomaly_source INTEGER
);
