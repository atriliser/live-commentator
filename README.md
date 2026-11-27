# Live Match AI Commentator

A multi-agent system for live football commentary.

Historical matches from [StatsBomb Open Data](https://github.com/statsbomb/open-data) are replayed into Kafka as a live feed. The goal (v1.0) is real-time LLM commentary in several languages with triage, critique and translation agents, plus pre-match analysis.

## Status: v0.1

The event pipeline works end to end, no LLM yet:

- a replayer publishes match events to Kafka at configurable speed;
- a FastAPI service consumes them and streams to the browser via Server-Sent Events;
- the whole stack starts with one `docker compose up`.

## Architecture

```
replay ──► Kafka (match-events) ──► api: consumer ──► Broadcaster ──► SSE ──► browser
```

- `replay` reads a StatsBomb events file and publishes events with the original timing (sped up).
- `api` runs one Kafka consumer in the FastAPI lifespan and fans events out to every connected client; each client has a bounded queue, and a slow client loses events instead of slowing down everyone.
- Kafka message key is `match_id`, so all events of a match stay ordered in one partition.

## Quick start

Requirements: Docker with Compose (on macOS, for example, Colima).

1. Download the match events (World Cup 2018 final, France – Croatia):

   ```bash
   mkdir -p data/raw
   curl -o data/raw/8658.json https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/8658.json
   ```

2. Start everything:

   ```bash
   docker compose up --build
   ```

3. Open http://127.0.0.1:8000/ within 15 seconds — the replay starts after a short delay, and the page shows events from the moment it connects.

Stop: `Ctrl+C`, then `docker compose down`.

## Configuration

| Variable | Default | Used by |
| --- | --- | --- |
| `KAFKA_BOOTSTRAP_SERVERS` | `localhost:9092` | api, replay |
| `KAFKA_TOPIC` | `match-events` | api, replay |
| `MATCH_ID` | `8658` | replay |
| `REPLAY_SPEEDUP` | `60.0` | replay |
| `REPLAY_START_DELAY_SECONDS` | `0` (`15` in compose) | replay |

Kafka has two listeners: `localhost:9092` for clients on the host and `kafka:19092` for containers in the compose network.

## Development

Requirements: Python 3.13, [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run ruff format && uv run ruff check && uv run mypy src tests && uv run pytest
```

Run the services on the host (Kafka from compose):

```bash
docker compose up -d kafka kafka-init
uv run uvicorn live_commentator.api_app:app --reload
uv run python -m live_commentator.replay_app
```

## Data

Match data: [StatsBomb Open Data](https://github.com/statsbomb/open-data). Data source: StatsBomb.

The data is not committed to this repository; see Quick start for how to download it.