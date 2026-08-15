"""Time-series stats sampler.

Every STAT_FREQ seconds, captures CPU / RAM / Disk and inserts a snapshot
into the SQLite database at DB_PATH. Runs forever, keeping the container alive.

Environment:
    STAT_FREQ  seconds between samples (default 10)
    DB_PATH    path to the SQLite database (default /data/system_stats.db)
"""
import os
import sqlite3
import time
from datetime import datetime, timezone

import psutil

DB_PATH = os.environ.get("DB_PATH", "/data/system_stats.db")
STAT_FREQ = int(os.environ.get("STAT_FREQ", "10"))

SCHEMA = """
CREATE TABLE IF NOT EXISTS system_stats (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    captured_at   TEXT    NOT NULL,
    cpu_percent   REAL    NOT NULL,
    ram_total     INTEGER NOT NULL,
    ram_available INTEGER NOT NULL,
    ram_used      INTEGER NOT NULL,
    disk_total    INTEGER NOT NULL,
    disk_free     INTEGER NOT NULL,
    disk_used     INTEGER NOT NULL
)
"""


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(SCHEMA)
    conn.commit()
    return conn


def sample():
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    return (
        datetime.now(timezone.utc).isoformat(timespec="seconds"),
        cpu,
        mem.total,
        mem.available,
        mem.used,
        disk.total,
        disk.free,
        disk.used,
    )


def main():
    conn = connect()
    print(f"Stats sampler started: every {STAT_FREQ}s -> {DB_PATH}", flush=True)
    while True:
        row = sample()
        conn.execute(
            """
            INSERT INTO system_stats
                (captured_at, cpu_percent, ram_total, ram_available, ram_used,
                 disk_total, disk_free, disk_used)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            row,
        )
        conn.commit()
        print(
            f"{row[0]}  cpu={row[1]:5.1f}%  "
            f"ram_used={row[4] / 1024**3:5.2f} GiB  "
            f"disk_used={row[7] / 1024**3:6.2f} GiB",
            flush=True,
        )
        time.sleep(STAT_FREQ)


if __name__ == "__main__":
    main()
