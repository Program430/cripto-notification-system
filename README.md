# Price Change Notification System

## Short Description

**PriceChangeNotificationSystem** is a system for collecting price data from different sources and notifying users when the price changes.

The tracked object for the MVP is **cryptocurrency**, but the project architecture should allow the system to be adapted for almost any object that has an up-to-date price value.

## Project Goal

Build a **prod-like MVP** that satisfies functional, non-functional, technical, and code quality requirements.

## Requirements

### Functional Requirements

* Return information about currencies available in the system and the current price of each currency.
* Register users.
* Authorize and authenticate users.
* Allow users to subscribe to a selected currency.
* Notify users via **Telegram** when the subscription price threshold is crossed.

### Non-Functional Requirements

* High fault tolerance.
* Logging.
* Basic metrics and dashboards.
* Use optimization techniques:

  * indexes;
  * caching.

### Technical Requirements

* Use **Kafka** as the message broker.
* Unit testing for the application functionality.
* Integration testing for the API.

### Code Requirements

* Low coupling between modules.
* Clean architecture.
* Dependencies should point to abstractions, not implementations.
* Use **ruff** and **mypy**.
* Database models may be used as domain models.

## Quick Start

Create a local `.env` file:

```bash
cp .env.example .env
```

Start the prod-like stack:

```bash
docker compose up -d --build
```

## Local Development

Local development uses a compose override:

```bash
docker compose -f docker-compose.yml -f docker-compose.local.yml up --build
```

Or with Makefile:

```bash
make dev-up
```

Dev mode includes:

- `uvicorn --reload`;
- `debugpy` on `localhost:5678`;
- bind mount `./src:/app/src`;
- the same observability stack as the prod-like setup.

## Quality Checks

Full check:

```bash
make check
```

Tests only:

```bash
make test
make test-unit
make test-integration
```

## Status And Releases

- [docs/releases.md](docs/releases.md)
