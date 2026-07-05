# ADR-008 — RabbitMQ over Kafka

## Status
**Accepted** — In effect as of 2026-07-04

## Context
Our backend microservices require asynchronous background task routing (notification triggers, Razorpay fee validations, database indexing pipelines).

We evaluated:
1. **Apache Kafka**: High throughput, log-based partitioning, but complex cluster setup and management.
2. **RabbitMQ**: AMQP-compliant message queue broker. Light resource footprint, direct support for routing keys and exchange patterns.

## Decision
We chose **RabbitMQ** as our primary message queue broker. Given our current operational load, we do not require the petabyte-scale stream storage of Kafka. RabbitMQ's simple exchange-to-queue bindings are perfect for asynchronous dispatch routing.

## Consequences
- **Infrastructure**: Simple setup via docker-compose (`rabbitmq:3.13-management-alpine`).
- **Development**: Low development latency, simple async libraries (`aio-pika`).
- **Scale**: Easy upgrade to managed RabbitMQ services (CloudAMQP) when scaling.
