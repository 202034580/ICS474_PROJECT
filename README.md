# ICS 474 Real-Time Sensor Data Streaming Project

This project implements an **end-to-end real-time big data pipeline** for streaming,
processing, storing, and visualizing IoT sensor data using Apache Kafka, Apache Spark,
PostgreSQL, and Grafana.

The system simulates sensor readings (temperature, humidity, and pressure), performs
real-time anomaly detection, and visualizes results through interactive dashboards.

---

## 🚀 Overview

The goal of this project is to demonstrate a complete real-time data analytics pipeline.
Sensor data is generated continuously, processed using stream processing techniques,
stored persistently, and visualized for monitoring and analysis.  
The project highlights how modern big data tools can be integrated to build scalable
and real-time monitoring systems.

---

## 🏗️ Architecture & Data Pipeline

The system follows a real-time streaming architecture as shown below:

Python Kafka Producer  
↓  
Apache Kafka (Message Broker)  
↓  
Spark Structured Streaming (Processing & Anomaly Detection)  
↓  
PostgreSQL (Persistent Storage)  
↓  
Grafana (Visualization & Monitoring)

---

## 🧰 Technologies Used

| Component | Version |
|---------|--------|
| Java JDK | 17.0.17 |
| Python | 3.12.2 |
| Apache Kafka | 3.9.1 |
| Apache Spark | 3.5.1 |
| PostgreSQL | 16.11 |
| pgAdmin 4 | 9.10 |
| Grafana | 12.2.2 |

---

## 📁 Project Structure

```text
ICS474_PROJECT/
├── producer/        # Kafka producer (Python)
├── spark/           # Spark streaming job
├── sql/             # SQL scripts
├── grafana/         # Grafana dashboards
├── screenshots/     # Execution screenshots
└── README.md
```
---

## ⚙️ Setup & Execution
1. Start Zookeeper
```powershell
.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
```
--- 


## 2. Start Kafka Broker
```powershell
.\bin\windows\kafka-server-start.bat .\config\server.properties
```
---

## 3. Run Kafka Producer
```powershell

python producer/kafka_producer.py
```
---
## 4. Run Spark Streaming Job
```powershell

spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 `
--jars C:\jdbc\postgresql-42.7.7.jar `
spark/pyspark_stream_to_postgres.py
```
---
## 📊 Results & Visualization
Processed sensor data is stored in PostgreSQL and visualized using Grafana dashboards.
The dashboards display real-time temperature, humidity, and pressure values, and clearly
highlight anomalous readings detected during stream processing.

---

## 🔮 Main differences
This project extends the original prototype:
https://github.com/Apostu0Alexandru/kafka-streaming-dashboard

Key differences include:

Added Spark Structured Streaming for real-time processing

Implemented anomaly detection logic inside Spark

Integrated PostgreSQL for persistent storage

Used pgAdmin 4 for data verification

Built Grafana dashboards based on PostgreSQL

---

## 📚 References
Apache Kafka Documentation: https://kafka.apache.org/documentation/

Apache Spark Documentation: https://spark.apache.org/docs/latest/

Grafana Documentation: https://grafana.com/docs/

Original Project Repository: https://github.com/Apostu0Alexandru/kafka-streaming-dashboard
