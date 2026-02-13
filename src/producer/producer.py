import json
import os
import random
import time
import uuid
import signal
import sys
from datetime import datetime
from kafka import KafkaProducer

KAFKA_BROKER = os.getenv("KAFKA_BROKER_URL", "kafka:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "application-logs")
MESSAGE_RATE = float(os.getenv("MESSAGE_RATE", "1"))

running = True

def shutdown_handler(signum, frame):
    global running
    print("Shutting down producer gracefully...")
    running = False

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

services = ["auth-service", "user-api", "payment-service"]
levels = ["INFO", "WARN", "ERROR"]

print("Producer started...")

while running:
    log_event = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "service_name": random.choice(services),
        "level": random.choice(levels),
        "message": "Synthetic log message",
        "trace_id": str(uuid.uuid4())
    }

    producer.send(TOPIC, log_event)
    producer.flush()

    print(f"Sent: {log_event}")

    time.sleep(1 / MESSAGE_RATE)

producer.close()
print("Producer stopped.")
sys.exit(0)
