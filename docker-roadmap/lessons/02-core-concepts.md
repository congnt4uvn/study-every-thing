# Lesson 02 — Core concepts: images, containers, layers, registries

## Goals
- Understand images/layers and why builds are cacheable
- Understand container filesystem behavior (read-only layers + writable layer)
- Understand registries, repositories, tags, and digests

## Concepts
### Images and layers
A Docker image is typically built from a **Dockerfile**. Each instruction (like `RUN`, `COPY`) creates a new **layer**.

Why layers matter:
- Layers are content-addressed and reused across images
- Reusing layers makes builds and pulls faster
- A tiny change can invalidate a layer and all layers after it

### Container filesystem
When you run an image, Docker adds a thin writable layer on top:
- Image layers (read-only)
- Container layer (writable)

If you delete the container, its writable layer is deleted too.

### Registries, repos, tags, digests
- **Registry**: a server that stores images (e.g., Docker Hub, GHCR, ECR)
- **Repository**: a namespace for related images (e.g., `library/nginx`)
- **Tag**: a mutable label (e.g., `nginx:1.27`, `nginx:latest`)
- **Digest**: an immutable content hash (e.g., `nginx@sha256:...`)

Rule of thumb:
- Use **tags** for humans
- Use **digests** for reproducible deployments

## Explore images locally
```powershell
# List images
docker images

# Inspect metadata (env vars, entrypoint, ports, etc.)
docker image inspect nginx:latest

# See layer history
docker history nginx:latest
```

## Hands-on lab
1. Pull two tags and compare:
```powershell
docker pull alpine:3.19
docker pull alpine:latest
docker images alpine
```

2. See how tags point to different content:
```powershell
docker image inspect alpine:3.19 | Select-String -Pattern 'Id|RepoTags|RepoDigests'
```

3. Run a container and write a file:
```powershell
docker run --name tmp -it alpine:3.19 sh
# inside container:
echo "hello" > /hello.txt
cat /hello.txt
exit
```

Now start it again and confirm the file still exists (same container):
```powershell
docker start -ai tmp
cat /hello.txt
exit
```

Remove it and confirm the data disappears:
```powershell
docker rm -f tmp
```

## Checklist
- I can explain layers and caching
- I know tags are mutable and digests are immutable
- I understand why container-local writes disappear with container deletion

## Answers to Lesson 01 mini-quiz
1. The image must exist (or be pulled) before a container can be created.
2. Map host port 8080 → container port 80.
3. `docker ps` only shows running containers by default; use `docker ps -a`.
