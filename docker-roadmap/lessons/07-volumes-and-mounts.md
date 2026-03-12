# Lesson 07 — Data: volumes, bind mounts, permissions

## Goals
- Understand where container data lives
- Choose between bind mounts and volumes
- Avoid common Windows/WSL path pitfalls

## Why data handling matters
Containers are disposable. If your app stores important data *inside* the container filesystem and you delete the container, you lose that data.

You usually want one of:
- **Bind mount**: map a host path into the container (great for development)
- **Volume**: Docker-managed storage (great for databases and persistent state)

## Bind mounts
Bind mounts map a host directory/file into the container.

Example:
```powershell
# Mount current folder into /app
docker run --rm -it -v ${PWD}:/app alpine:3.19 sh
```

Use cases:
- Live-editing source code in an IDE while the container runs it
- Sharing config files with containers

## Volumes
Volumes are managed by Docker and live in Docker’s storage area.

Create and inspect:
```powershell
docker volume create mydata
docker volume ls
docker volume inspect mydata
```

Use in a container:
```powershell
docker run -d --name voltest -v mydata:/data alpine:3.19 sh -c "echo hi > /data/hello.txt; sleep 3600"
```

## Named volume vs anonymous volume
- Named volume: `mydata:/data` (easy to reuse)
- Anonymous volume: `-v /data` (harder to track; fine for some cases)

## Permissions (the usual pain point)
Containers often run as Linux users (even on Windows via WSL2).

Symptoms:
- “Permission denied” when writing to a mounted directory

Strategies:
- Prefer containers that run as non-root *but* support writable paths
- For dev bind mounts, align UID/GID or configure the app to use a writable directory
- For production, avoid bind mounts and use volumes + explicit ownership

## Windows + WSL2 notes
On Windows, Docker Desktop with WSL2 means:
- Linux containers run in a Linux VM/WSL environment
- File performance differs depending on whether you mount from:
  - A WSL filesystem path (usually faster), vs
  - A Windows filesystem path (can be slower)

If you use WSL2 heavily, consider keeping dev projects inside the WSL filesystem.

## Hands-on lab
1. Bind mount test:
```powershell
mkdir mount-demo
Set-Content -Path .\mount-demo\hello.txt -Value "hello"
docker run --rm -it -v ${PWD}\mount-demo:/data alpine:3.19 sh -c "ls -la /data; cat /data/hello.txt"
```

2. Volume persistence test:
```powershell
docker volume create persistdemo
docker run --rm -v persistdemo:/data alpine:3.19 sh -c "date > /data/created.txt"
docker run --rm -v persistdemo:/data alpine:3.19 sh -c "cat /data/created.txt"
```

3. Cleanup:
```powershell
docker volume rm persistdemo
```

## Checklist
- I can explain the difference between bind mounts and volumes
- I can create, inspect, and remove volumes
- I know how to approach permission issues instead of guessing
