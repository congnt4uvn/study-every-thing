# Lesson 03 — Container lifecycle + essential CLI

## Goals
- Get fluent with the day-to-day commands
- Understand container states (created, running, exited)
- Know when to use `run` vs `start` vs `exec`

## Lifecycle and “what command does what”
### `docker run`
Creates *and* starts a new container.

```powershell
# New container every time you run this
docker run --rm alpine:3.19 echo "hi"
```

- `--rm` removes the container after it exits (great for one-off tasks).

### `docker start`
Starts an *existing* stopped container.

```powershell
docker create --name myalpine alpine:3.19
docker start myalpine
```

### `docker exec`
Runs a command inside a *running* container.

```powershell
docker run -d --name web -p 8080:80 nginx:latest
docker exec -it web sh
```

## Essential commands
### Listing
```powershell
docker ps           # running
docker ps -a        # all
```

### Logs
```powershell
docker logs web
docker logs -f web  # follow
```

### Inspect
```powershell
docker inspect web
```

### Resource usage
```powershell
docker stats
```

### Cleanup
```powershell
# Stop/remove specific container
docker stop web
docker rm web

# Remove unused data (be careful)
docker system df
```

> Tip: Avoid `docker system prune -a` until you truly understand what it deletes.

## Hands-on lab: “break the fear barrier”
1. Run a container that stays alive:
```powershell
docker run -d --name sleeper alpine:3.19 sh -c "while true; do date; sleep 2; done"
```

2. Watch logs:
```powershell
docker logs -f sleeper
```

3. Exec into it (in another terminal):
```powershell
docker exec -it sleeper sh
ps
exit
```

4. Inspect it:
```powershell
docker inspect sleeper | Select-String -Pattern '"IPAddress"|"Image"|"Mounts"'
```

5. Cleanup:
```powershell
docker rm -f sleeper
```

## Checklist
- I can attach to logs and exec into a running container
- I know how to inspect a container to understand how it’s configured
- I can clean up containers safely

## Common pitfalls
- **Trying `exec` on a stopped container**: start it first.
- **Confusing `run` with `start`**: `run` creates a new container each time unless you reuse a name and manage collisions.
- **Forgetting port mappings**: `EXPOSE` in an image is documentation, not a host-port publish.
