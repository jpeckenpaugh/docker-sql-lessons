# Docker + Python System Stats Sampler — Lesson 1

An intro lesson for support engineers moving into DevOps. We run a long-lived
container that **samples real CPU / RAM / Disk stats every N seconds**, stores
each snapshot in a SQLite database, and lets you query the history with SQL.

## Learning goals

- What an **image** vs a **container** is
- A container that **stays running** (a daemon) vs one that exits
- `Dockerfile` basics: base image, install packages, copy, command
- Using `docker compose` with a bind mount (code) + named volume (data)
- Configuration via environment variables (`STAT_FREQ`)
- Querying a time-series history with the `sqlite3` CLI

## Files

| File | Purpose |
| --- | --- |
| `docker-compose.yml` | Defines the `monitor` service, volumes, env vars |
| `monitor/Dockerfile` | Builds the image (installs Python deps + `sqlite3`) |
| `monitor/entrypoint.sh` | Prints a banner, then starts `app.py` |
| `monitor/app.py` | Samples CPU/RAM/Disk every `STAT_FREQ`s, writes to SQLite |

## Getting started

Prerequisite: install **Docker Desktop** (free) and start it.

```bash
# 1. Build and start detached (container keeps running in the background)
docker compose up -d --build

# 2. Watch it capture a snapshot every 10 seconds
docker compose logs -f

# 3. Verify it is still running
docker ps

# 4. Connect to the container and query the stats
docker exec -it system-monitor bash
```

## Querying the stats

Once inside the container (`docker exec -it system-monitor bash`):

```bash
sqlite3 /data/system_stats.db

# inside the sqlite3 prompt:
.tables
SELECT * FROM system_stats ORDER BY id DESC LIMIT 5;

# summaries
SELECT
    COUNT(*)                                AS samples,
    ROUND(AVG(cpu_percent), 1)              AS avg_cpu_pct,
    ROUND(AVG(ram_used) / 1024 / 1024, 1)   AS avg_ram_used_mib,
    ROUND(AVG(disk_used) / 1024 / 1024, 1)  AS avg_disk_used_mib
FROM system_stats;

# latest snapshot
SELECT * FROM system_stats ORDER BY id DESC LIMIT 1;
```

Exit the container with `exit` or `Ctrl-D`.

## Changing the sampling interval

```bash
STAT_FREQ=2 docker compose up -d      # sample every 2 seconds (one-off)
```

To change it permanently, edit `STAT_FREQ` in `docker-compose.yml` and run
`docker compose up -d`.

## Controlling the stack

```bash
docker compose logs -f        # follow live captures
docker compose down           # stop container, KEEP the stats volume
docker compose down -v        # stop AND delete the stats database
docker compose up -d          # start again (history is still there)
```

## Suggested in-lesson exercises

1. Sample every 2 seconds, generate load (`yes > /dev/null &`), then SQL-query
   the CPU column to see the spike captured in real time.
2. Compute a moving average: `SELECT AVG(cpu_percent) FROM system_stats WHERE id > (SELECT MAX(id) - 10 FROM system_stats);`
3. Add a new stat (e.g. network bytes via `psutil.net_io_counters()`) — the
   schema in `app.py` is the only place to touch.
4. Try to read the DB after `docker compose down -v` — it's gone. Then discuss
   why named volumes matter in production.

## Wanted for next lesson

- Containerize an HTTP API (Flask/FastAPI) that serves the stats over JSON
- Graph the history (e.g. feed it to Grafana or a simple chart)
- Deploy the same container to Azure with GitHub Actions
