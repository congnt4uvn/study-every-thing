# Lesson 10 — Compose patterns: dev/prod, env, healthchecks

## Goals
- Use environment variables safely and predictably
- Use healthchecks to detect readiness
- Structure Compose for dev vs prod without chaos

## Environment variables in Compose
You’ll see three common patterns:

1) Inline environment variables:
```yaml
services:
  app:
    image: myapp:1.0
    environment:
      LOG_LEVEL: "debug"
      PORT: "8080"
```

2) Load variables from an `.env` file (Compose automatically reads `.env` in the same directory):
```env
APP_PORT=8080
LOG_LEVEL=debug
```

```yaml
services:
  app:
    image: myapp:1.0
    ports:
      - "${APP_PORT}:8080"
    environment:
      LOG_LEVEL: "${LOG_LEVEL}"
```

3) `env_file:` to load a dedicated file:
```yaml
services:
  app:
    env_file:
      - ./app.env
```

### Guidance
- Don’t bake secrets into images.
- Prefer `.env` for non-secret local settings.
- For secrets, use your platform secret manager in production; for local dev, keep secrets out of git.

## Healthchecks
A healthcheck is a command Docker runs to decide whether a container is “healthy”.

Example:
```yaml
services:
  web:
    image: nginx:latest
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost/"]
      interval: 10s
      timeout: 3s
      retries: 5
```

Why it matters:
- Helps you see readiness problems quickly
- Helps Compose and your team diagnose “it started but it’s broken” scenarios

> Important: Even with healthchecks, your *application* should still do retries/backoff when calling dependencies.

## Dev vs prod patterns (simple and effective)
Keep it simple:
- One `compose.yaml` that defines services
- Optionally a `compose.override.yaml` for developer-only tweaks

Examples of dev-only tweaks:
- Bind mounts
- Live reload
- Exposing extra ports

Example override:
```yaml
services:
  app:
    volumes:
      - ./:/app
    environment:
      LOG_LEVEL: "debug"
```

## Compose profiles (optional)
Profiles let you enable optional services.

```yaml
services:
  jaeger:
    image: jaegertracing/all-in-one
    profiles: ["observability"]
```

Run with:
```powershell
docker compose --profile observability up -d
```

## Hands-on lab: add healthcheck + readiness thinking
1. Use a service that can respond to an HTTP check (nginx is fine).
2. Add a healthcheck.
3. Start stack and check health:
```powershell
docker compose up -d

docker compose ps
```

Look for a `healthy` status.

## Checklist
- I can use `.env` and variable substitution safely
- I can add healthchecks and read container health
- I have a strategy for dev vs prod Compose files

## Common pitfalls
- **Assuming `depends_on` means “ready”**: it mostly ensures start order, not readiness.
- **Committing secrets**: `.env` often accidentally gets committed; add it to `.gitignore`.
