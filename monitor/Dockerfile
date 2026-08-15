FROM python:3.12-slim

# sqlite3 CLI so students can query the database from inside the container
RUN apt-get update && apt-get install -y --no-install-recommends sqlite3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first so pip layer only rebuilds when requirements change
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app
COPY app.py entrypoint.sh ./
RUN chmod +x entrypoint.sh

# Mount point for the stats database (named volume in docker-compose.yml)
RUN mkdir -p /data

CMD ["bash", "entrypoint.sh"]
