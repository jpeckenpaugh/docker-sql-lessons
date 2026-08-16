# Docker Lessons

A hands-on series for support engineers moving into DevOps. Each numbered
folder is a self-contained lesson that builds a small Dockerized Python app.
Each lesson has its own `README.md` with the goal, files, and exercises.

| Lesson | Folder | Builds |
| --- | --- | --- |
| 1 | [`01-monitor/`](01-monitor/README.md) | A long-lived daemon that samples CPU/RAM/Disk into SQLite |
| 2 | [`02-lesson-catalogue/`](02-lesson-catalogue/README.md) | A FastAPI JSON API that tracks lessons and notes |

## Prerequisites

- **Docker Desktop** (free), started and running.
- Basic familiarity with the command line.

## How to use

Each lesson is independent — `cd` into a folder and follow its README:

```bash
cd 01-monitor
docker compose up -d --build
```

The top-level `docker-compose.yml` (still available for Lesson 1) just runs
the `01-monitor/` service; you can also run it from here with:

```bash
docker compose up -d --build
```

## Lesson map

### Lesson 1 — `01-monitor/`: system stats sampler

Run a long-lived container that samples real CPU / RAM / Disk every N seconds,
stores each snapshot in a SQLite database, and lets you query the history with
SQL. Covers images vs containers, a daemon that stays running, Dockerfile
basics, bind mounts vs named volumes, env-var config, and the `sqlite3` CLI.

### Lesson 2 — `02-lesson-catalogue/`: FastAPI catalogue API

Containerize a FastAPI app that serves a lesson catalogue over JSON with a
SQLite backend. Covers exposing ports, hot-reload with a bind mount, CRUD
endpoints, Pydantic schemas, and persisting data in a named volume.