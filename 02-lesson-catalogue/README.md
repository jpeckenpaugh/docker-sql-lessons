# Lesson 2 — FastAPI Lesson Catalogue

Builds an HTTP API that serves a **lesson catalogue** over JSON. Lessons have
titles and can collect notes; everything persists in a SQLite database.

## Learning goals

- Containerizing an HTTP API (FastAPI + uvicorn) instead of a CLI daemon
- Exposing container ports to the host (`8000:8000`)
- Hot-reload for development via a bind mount (`--reload`)
- REST endpoints: `GET`/`POST` on `/lessons` and `/notes`
- Pydantic schemas for request/response validation
- Persisting data in a named volume so it survives restarts

## Files

| File | Purpose |
| --- | --- |
| `Dockerfile` | Builds the image, installs deps, runs uvicorn |
| `docker-compose.yml` | Defines the `api` service, port, volumes, env vars |
| `requirements.txt` | FastAPI, uvicorn, SQLAlchemy |
| `app/main.py` | The FastAPI app with the `/lessons` and `/notes` routes |
| `app/models.py` | SQLAlchemy models (`Lesson`, `Note`) |
| `app/schemas.py` | Pydantic schemas for request/response bodies |
| `app/database.py` | Engine/session setup; reads `DATABASE_URL` |

## Getting started

```bash
cd 02-lesson-catalogue
docker compose up -d --build
```

Once up, the API is at:

- Interactive docs (Swagger UI): http://localhost:8000/docs
- All lessons: `GET http://localhost:8000/lessons`

## Trying it out

```bash
# create a lesson
curl -X POST http://localhost:8000/lessons \
  -H "Content-Type: application/json" \
  -d '{"title": "Understanding images vs containers"}'

# list lessons
curl http://localhost:8000/lessons

# get one lesson
curl http://localhost:8000/lessons/1

# add a note to a lesson
curl -X POST http://localhost:8000/notes \
  -H "Content-Type: application/json" \
  -d '{"lesson_id": 1, "body": "An image is a template; a container is a running instance."}'

# list notes
curl http://localhost:8000/notes
```

## Editing code without rebuilding

The `docker-compose.yml` bind-mounts `./app` into the container and uvicorn
runs with `--reload`, so changes to `app/*.py` are picked up immediately.

## Controlling the stack

```bash
docker compose logs -f        # follow the uvicorn access logs
docker compose down           # stop the API, KEEP the database volume
docker compose down -v        # stop AND delete the SQLite database
docker compose up -d          # start again (data is still there)
```

## Suggested exercises

1. Add a `DELETE /lessons/{id}` endpoint (the model's `cascade` already
   removes its notes).
2. Add a field to the `Lesson` model and Pydantic schema, e.g. `difficulty`.
3. Query the SQLite DB directly from inside the container:
   `docker exec -it lessons-api python -c "..."`.
4. Bump to a second service (e.g. a DB container) and connect the two via the
   compose network instead of using bind-mounted SQLite.