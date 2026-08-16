#!/bin/bash
set -e
echo "Starting stats sampler: every ${STAT_FREQ}s -> ${DB_PATH}"
python app.py
