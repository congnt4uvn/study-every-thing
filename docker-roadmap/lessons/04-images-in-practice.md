# Lesson 04 — Images in practice: pull, tag, inspect, push

## Goals
- Pull images, understand naming, and choose correct tags
- Tag images for your own repository
- Push to a registry (conceptually + practical steps)

## Image naming
A typical image reference looks like:

- `nginx:1.27` (defaults to Docker Hub)
- `docker.io/library/nginx:1.27` (explicit)
- `ghcr.io/myorg/myapp:1.0.0` (GitHub Container Registry)

Parts:
- **Registry host** (optional)
- **Namespace/repo**
- **Tag** (optional, defaults to `latest`)

## Pull and inspect
```powershell
docker pull nginx:1.27
docker image inspect nginx:1.27
```

## Tagging
Tags are just pointers to an image ID.

```powershell
# Example: give the same image a new tag
docker tag nginx:1.27 my-nginx:1.27

docker images my-nginx
```

## Pushing (overview)
To push, you need:
- A registry account
- A repository you can write to
- `docker login` to authenticate

Example flow:
```powershell
# Log in (prompts for credentials)
docker login

# Tag image with a registry/repo you own (example uses Docker Hub)
docker tag my-nginx:1.27 <your-dockerhub-username>/my-nginx:1.27

# Push
docker push <your-dockerhub-username>/my-nginx:1.27
```

## Digests for reproducibility
If you deploy `myapp:latest`, it can silently change. Prefer versioned tags.

For maximum reproducibility:
- Pin base images by digest in your Dockerfile (you’ll do this later)
- Pin deployment images by digest in your runtime environment

## Hands-on lab
1. Pull and compare sizes:
```powershell
docker pull alpine:3.19
docker pull ubuntu:24.04
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
```

2. Inspect entrypoint/cmd:
```powershell
docker image inspect ubuntu:24.04 | Select-String -Pattern 'Entrypoint|Cmd'
```

3. Cleanup unused tags (keep at least one):
```powershell
docker rmi my-nginx:1.27
```

## Checklist
- I understand what a tag is and why `latest` is risky
- I can tag images for a registry
- I know the basic push workflow
