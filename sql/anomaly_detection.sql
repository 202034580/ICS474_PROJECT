SELECT *
FROM public.sensor_readings
WHERE anomaly_flag = 1
   OR is_anomaly_source = 1
ORDER BY ts DESC;
