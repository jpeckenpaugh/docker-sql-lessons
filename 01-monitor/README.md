# Lesson 1 — System Stats Sampler

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
| `Dockerfile` | Builds the image (installs Python deps + `sqlite3`) |
| `entrypoint.sh` | Prints a banner, then starts `app.py` |
| `app.py` | Samples CPU/RAM/Disk every `STAT_FREQ`s, writes to SQLite |
| `requirements.txt` | Python dependencies (`psutil`) |

The service is defined by the `docker-compose.yml` at the repo root (the
`monitor` service), which sets the volumes and env vars. You can run it from
either this folder's parent or the repo root.

## Getting started

```bash
# from the repo root:
docker compose up -d --build

# watch it capture a snapshot every 10 seconds
docker compose logs -f

# verify it is still running
docker ps
```

## Querying the stats

```bash
docker exec -it system-monitor bash
sqlite3 /data/system_stats.db
```

Inside the `sqlite3` prompt:

```sql
.tables

SELECT * FROM system_stats ORDER BY id DESC LIMIT 5;

-- summaries
SELECT COUNT(*) AS samples,
       ROUND(AVG(cpu_percent), 1)            AS avg_cpu_pct,
       ROUND(AVG(ram_used) / 1024 / 1024, 1) AS avg_ram_used_mib,
       ROUND(AVG(disk_used) / 1024 / 1024, 1) AS avg_disk_used_mib
FROM system_stats;
```

Exit the container with `exit` or `Ctrl-D`.

## Changing the sampling interval

```bash
STAT_FREQ=2 docker compose up -d      # sample every 2 seconds (one-off)
```

To change it permanently, edit `STAT_FREQ` in the root `docker-compose.yml`.

## Controlling the stack

```bash
docker compose logs -f        # follow live captures
docker compose down           # stop container, KEEP the stats volume
docker compose down -v        # stop AND delete the stats database
docker compose up -d          # start again (history is still there)
```

## Suggested exercises

1. Sample every 2 seconds, generate load (`yes > /dev/null &`), then SQL-query
   the CPU column to see the spike captured in real time.
2. Compute a moving average:
   `SELECT AVG(cpu_percent) FROM system_stats WHERE id > (SELECT MAX(id) - 10 FROM system_stats);`
3. Add a new stat (e.g. network bytes via `psutil.net_io_counters()`) — the
   schema in `app.py` is the only place to touch.
4. Try to read the DB after `docker compose down -v` — it's gone. Then discuss
   why named volumes matter in production.