# Lesson 11 — Debugging & troubleshooting

## Goals
- Debug containers systematically (without random guessing)
- Use `logs`, `exec`, `inspect`, and `stats`
- Recognize the most common Docker failure modes

## The debugging loop
When something isn’t working, answer these in order:
1. Is the container running?
2. If it exited, *why*?
3. If it’s running, is the app listening on the expected port/interface?
4. Is the port published correctly?
5. Is networking correct between services?
6. Are mounts/permissions correct?

## Core commands
### Is it running?
```powershell
docker ps
docker ps -a
```

### What did it log?
```powershell
docker logs <container>
docker logs -f <container>
```

### What is it actually configured to do?
```powershell
docker inspect <container>
```

Look at:
- `Config.Env`
- `Config.Cmd`, `Config.Entrypoint`
- `NetworkSettings.Ports`
- `Mounts`

### What’s happening inside the container?
```powershell
docker exec -it <container> sh
```

Inside, check:
- Processes: `ps`
- Listening ports: `ss -lntp` (may require installing `iproute2`)
- DNS: `cat /etc/resolv.conf`, `nslookup <service>`

### Resource constraints
```powershell
docker stats
```

If memory is pegged, the kernel may kill your process (OOM kill).

## Common issues and fixes
### “It works in the container but not from my browser”
Typical causes:
- App is listening only on `127.0.0.1` inside the container
- Port mapping is missing or wrong

Fix:
- Make the app listen on `0.0.0.0` inside the container
- Publish the port with `-p host:container` or Compose `ports:`

### “Connection refused” between services
Typical causes:
- Using `localhost` to reach another container
- Services not on the same network
- Wrong port

Fix:
- Use the Compose service name (e.g., `http://db:5432`)

### Permission denied with mounts
Typical causes:
- Container user can’t write to mounted directory

Fix:
- Use a writable path
- Adjust ownership/permissions
- Use volumes for stateful services

## Hands-on lab: debug a broken container (intentionally)
1. Run nginx but map the wrong port:
```powershell
docker run -d --name broken -p 8080:81 nginx:latest
```

2. Visit http://localhost:8080 (it should fail).

3. Diagnose:
```powershell
docker ps
docker port broken
docker logs broken
docker inspect broken | Select-String -Pattern 'Ports'
```

4. Fix by recreating with correct mapping:
```powershell
docker rm -f broken
docker run -d --name fixed -p 8080:80 nginx:latest
```

Cleanup:
```powershell
docker rm -f fixed
```

## Checklist
- I can debug port mapping problems quickly
- I know when to use `inspect` vs `exec`
- I can explain why `localhost` is often wrong in multi-container setups
