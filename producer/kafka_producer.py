from kafka import KafkaProducer
from kafka.errors import KafkaError

import json
import time
import random
import logging

from tenacity import retry, stop_after_attempt, wait_fixed

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

TOPIC = "sensor_data"
BOOTSTRAP = "127.0.0.1:9092"   # force IPv4 on Windows

import random, time

def generate_sensor_data():
 
    is_anomaly = (random.randint(1, 25) == 1)

    if is_anomaly:
        return {
            "timestamp": int(time.time()),
            "temperature": random.choice([-10.0, 60.0]),
            "humidity": random.choice([0.0, 100.0]),
            "pressure": random.choice([890.0, 1100.0]),
            
            "is_anomaly_source": 1
        }
    else:
        return {
            "timestamp": int(time.time()),
            "temperature": round(random.uniform(20.0, 30.0), 2),
            "humidity": round(random.uniform(30.0, 60.0), 2),
            "pressure": round(random.uniform(990.0, 1010.0), 2),
            "is_anomaly_source": 0
        }


def json_serializer(data):
    return json.dumps(data).encode("utf-8")

@retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
def create_producer():
    return KafkaProducer(
        bootstrap_servers=[BOOTSTRAP],
        value_serializer=json_serializer,
        acks="all",
        retries=5,
        linger_ms=50
    )

producer = create_producer()

@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def send_data(data):
    future = producer.send(TOPIC, data)
    md = future.get(timeout=10)
    logging.info(f"Sent -> topic={md.topic}, partition={md.partition}, offset={md.offset}")

if __name__ == "__main__":
    try:
        while True:
            data = generate_sensor_data()
            logging.info(f"Generated: {data}")
            send_data(data)
            time.sleep(1)
    except KafkaError as e:
        logging.error(f"KafkaError: {e}")
    except KeyboardInterrupt:
        logging.info("Stopped by user.")
    finally:
        producer.flush()
        producer.close()
