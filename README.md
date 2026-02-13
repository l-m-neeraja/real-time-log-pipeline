# Real-Time Log Processing Pipeline (Kafka + Docker)

## Overview

This project builds a simple real-time log processing pipeline using:

- Apache Kafka  
- Docker & Docker Compose  
- Python  

The system generates synthetic application logs, streams them through Kafka, filters only ERROR and WARN logs, and writes them to a file in JSON Lines format.

The goal of this project is to understand:

- Event-driven architecture  
- Kafka producer & consumer  
- Containerized services  
- Service dependencies and health checks  
- Configuration using environment variables  

---

## Architecture

```
Producer (Python)
      |
      v
Kafka Topic (application-logs)
      |
      v
Consumer (Python)
      |
      v
processed_errors_warnings.jsonl
```

- The Producer generates random log messages.
- Kafka acts as the message broker.
- The Consumer reads logs and filters only ERROR and WARN.
- Filtered logs are written to a file.

---

## Log Format

Each log message follows this JSON schema:

```json
{
  "timestamp": "ISO 8601 format",
  "service_name": "auth-service | user-api | payment-service",
  "level": "INFO | WARN | ERROR",
  "message": "Synthetic log message",
  "trace_id": "UUID"
}
```

---

## Project Structure

```
real-time-log-pipeline/
│
├── docker-compose.yml
├── README.md
├── .env.example
│
├── src/
│   ├── producer/
│   └── consumer/
│
├── tests/
└── data/
```

---

## Prerequisites

Make sure you have:

```
docker --version
docker compose version
git --version
```

---

## How to Run

From the root directory:

```
docker compose up --build -d
```

This will:

- Start Zookeeper  
- Start Kafka  
- Create the application-logs topic automatically  
- Start Producer  
- Start Consumer  

---

## Check Running Services

```
docker compose ps
```

Kafka should show `(healthy)`.

---

## View Logs

Producer logs:

```
docker compose logs -f producer
```

Consumer logs:

```
docker compose logs -f consumer
```

---

## Verify Output File

```
cat data/processed_errors_warnings.jsonl
```

The file will contain only ERROR and WARN logs in JSON Lines format.

---

## Environment Variables

All configuration is handled using environment variables.

See `.env.example`:

```
KAFKA_BROKER_URL=kafka:9092
KAFKA_TOPIC=application-logs
MESSAGE_RATE=2
LOG_LEVEL_FILTER=ERROR,WARN
OUTPUT_FILE_PATH=/data/processed_errors_warnings.jsonl
```

This makes the system flexible without modifying code.

---

## Running Unit Tests

Install pytest:

```
pip install pytest
```

Run:

```
pytest
```

Tests verify the filtering logic used in the consumer.

---

## Graceful Shutdown

Both producer and consumer handle:

- SIGINT  
- SIGTERM  

This ensures proper shutdown without crashing or corrupting data.

Stop services:

```
docker compose down
```

---

## What This Project Demonstrates

- Real-time data streaming using Kafka  
- Producer and consumer implementation in Python  
- Docker-based service orchestration  
- Health checks for service readiness  
- Config-driven architecture  
- Basic error handling and log filtering  
