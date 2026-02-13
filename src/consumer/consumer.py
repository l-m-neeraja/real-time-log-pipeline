import json
import os
import signal
import sys
from kafka import KafkaConsumer

KAFKA_BROKER = os.getenv("KAFKA_BROKER_URL", "kafka:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "application-logs")
LOG_LEVEL_FILTER = os.getenv("LOG_LEVEL_FILTER", "ERROR,WARN").split(",")
OUTPUT_FILE = os.getenv("OUTPUT_FILE_PATH", "/data/processed_errors_warnings.jsonl")

running = True

def shutdown_handler(signum, frame):
    global running
    print("Shutting down consumer gracefully...")
    running = False

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("Consumer started...")

with open(OUTPUT_FILE, "a") as file:
    while running:
        try:
            for message in consumer:
                log_event = message.value

                if log_event.get("level") in LOG_LEVEL_FILTER:
                    file.write(json.dumps(log_event) + "\n")
                    file.flush()
                    print(f"Written: {log_event}")

        except json.JSONDecodeError as e:
            print(f"Malformed JSON: {e}", file=sys.stderr)
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)

consumer.close()
print("Consumer stopped.")
sys.exit(0)
