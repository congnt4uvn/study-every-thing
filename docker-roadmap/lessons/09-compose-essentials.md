# Lesson 09 — Docker Compose essentials

## Goals
- Understand what Compose is (and what it isn’t)
- Run multi-container apps with `compose.yaml`
- Use `up`, `down`, `logs`, and `exec` effectively

## What Compose does
Docker Compose lets you define a set of services (containers), networks, and volumes in a YAML file and run them together.

It’s ideal for:
- Local development stacks (app + database + cache)
- Demo environments
- Small single-host deployments

It is not:
- A multi-node orchestrator (that’s Kubernetes, Swarm, Nomad, etc.)

## Minimal example: nginx
Create `compose.yaml`:

```yaml
services:
  web:
    image: nginx:latest
    ports:
      - "8080:80"
```

Run it:
```powershell
docker compose up -d

docker compose ps
docker compose logs
```

Stop it:
```powershell
docker compose down
```

## Useful Compose commands
- `docker compose up` — create/start services
- `docker compose down` — stop/remove services (add `-v` to remove volumes)
- `docker compose logs -f` — follow logs
- `docker compose exec <service> <cmd>` — run a command in a running service
- `docker compose config` — view merged/validated config

## Hands-on lab: app + redis (no code)
Create `compose.yaml`:

```yaml
services:
  redis:
    image: redis:7
    ports:
      - "6379:6379"

  client:
    image: alpine:3.19
    depends_on:
      - redis
    command: ["sh", "-c", "apk add --no-cache redis; redis-cli -h redis ping"]
```

Run:
```powershell
docker compose up --build
```

Expected output includes `PONG`.

Cleanup:
```powershell
docker compose down
```

## Checklist
- I can explain Compose at a high level
- I can run a multi-service stack
- I can inspect logs and exec into a service

## Common pitfalls
- **YAML indentation**: a single space mistake can break configuration.
- **`depends_on` isn’t readiness**: it controls start order, not “service is ready.” (You’ll handle readiness later with healthchecks.)
