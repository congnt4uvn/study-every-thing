# Lesson 01 — What Docker is + install + first container

## Goals
By the end of this lesson you can:
- Explain (in plain words) what Docker *does* and what it *does not* do
- Install Docker and verify it works
- Run your first container and understand what you’re seeing

## Mental model
Docker is a toolchain that helps you **package** software (and its runtime dependencies) into an **image**, and then **run** that image as an isolated **container**.

- **Image**: a *read-only* template (like a snapshot) containing filesystem + metadata
- **Container**: a *running instance* of an image (plus a small writable layer)

Docker is not:
- A virtual machine (VMs run full guest operating systems)
- A replacement for good dependency management
- A security boundary you can ignore (containers reduce risk, but don’t make unsafe apps safe)

## Install (Windows)
If you’re on Windows, the most common setup is **Docker Desktop** using a **WSL 2** backend.

1. Install Docker Desktop
   - Enable WSL 2 (Docker Desktop can guide you)
   - Reboot if prompted
2. Open a new PowerShell window and confirm:

```powershell
docker version
docker info
```

If `docker info` shows server details, the engine is running.

### Common install issues
- **“WSL kernel not installed”**: install/update the WSL 2 kernel
- **Virtualization disabled**: enable virtualization in BIOS/UEFI
- **Docker Desktop not starting**: try switching to WSL 2 backend in settings

## Your first container
### 1) Hello World
```powershell
docker run hello-world
```

What happens:
- Docker checks your machine for the `hello-world` image
- If missing, it pulls it from a registry (Docker Hub)
- It creates a container, runs it, prints output, then exits

### 2) Run a web server (nginx)
```powershell
# Run nginx in the background (detached)
docker run -d --name web -p 8080:80 nginx:latest

# List running containers
docker ps
```

Open http://localhost:8080 in your browser.

### 3) Stop and remove
```powershell
# Stop the running container
docker stop web

# Remove the container
docker rm web
```

## Key commands (quick reference)
- `docker version` — client/server versions
- `docker info` — engine info (storage driver, backend)
- `docker run` — create + start a container
- `docker ps` — list running containers (`-a` includes stopped)
- `docker stop` / `docker rm` — stop/remove containers

## Hands-on lab
1. Run `hello-world` twice.
   - Observe: first run downloads the image; second run uses cache.
2. Run `nginx` and change the host port:
   - Try `-p 9090:80` and visit http://localhost:9090
3. Practice cleanup:
   - Stop, remove, confirm `docker ps -a` is empty

## Checklist
- I can define image vs container
- I can run a container that serves HTTP and reach it via a port mapping
- I know how to stop and remove containers

## Mini-quiz (answers are in the next lesson)
1. When you run `docker run nginx`, what gets created first: image or container?
2. What does `-p 8080:80` mean?
3. Why doesn’t `docker ps` show containers that already exited?
