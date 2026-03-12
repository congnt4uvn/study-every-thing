# Guide: Push a Docker image to Docker Hub

This guide shows how to push a local Docker image to Docker Hub.

## Prerequisites

- Docker Desktop installed and running
- A Docker Hub account: https://hub.docker.com/
- (Recommended) A repository created on Docker Hub (e.g., `my-app`)

Verify Docker works:

```sh
docker version
```

## 1) Sign in to Docker Hub

In a terminal:

```sh
docker login
```

- Enter your Docker Hub username and password (or an access token).
- If your org requires SSO, use an access token.

## 2) Build (or identify) the local image

If you need to build from a `Dockerfile` in the current folder:

```sh
docker build -t my-app:1.0.0 .
```

Or list images you already have:

```sh
docker images
```

## 3) Tag the image with your Docker Hub namespace

Docker Hub image names must include your Docker Hub username (or org) and repository name:

Format:

- `docker.io/<USERNAME>/<REPO>:<TAG>`
- Most of the time you can omit `docker.io/`.

Example (replace `YOUR_USERNAME`):

```sh
docker tag my-app:1.0.0 YOUR_USERNAME/my-app:1.0.0
```

If you want `latest` too:

```sh
docker tag my-app:1.0.0 YOUR_USERNAME/my-app:latest
```

Tip: confirm tags:

```sh
docker images YOUR_USERNAME/my-app
```

## 4) Push to Docker Hub

Push the versioned tag:

```sh
docker push YOUR_USERNAME/my-app:1.0.0
```

Optionally push `latest`:

```sh
docker push YOUR_USERNAME/my-app:latest
```

## 5) Verify on Docker Hub

- Open your Docker Hub repository in the browser and check the “Tags” list.

You can also test pulling from another machine:

```sh
docker pull YOUR_USERNAME/my-app:1.0.0
```

## Common issues

### "denied: requested access to the resource is denied"

Usually one of:

- Not logged in: run `docker login`
- Wrong repository name (typo) or wrong namespace (username/org)
- Repo doesn’t exist (create it on Docker Hub, or ensure auto-create is allowed)
- Pushing to an org repo without permission

### "unauthorized: incorrect username or password"

- Use a Docker Hub access token instead of your password (recommended)
- Re-run `docker login` and try again

### Pushing large images is slow

- Ensure you’re on a stable connection
- Consider reducing image size (multi-stage builds, smaller base images)

## Quick reference

```sh
# login
docker login

# build
docker build -t my-app:1.0.0 .

# tag
docker tag my-app:1.0.0 YOUR_USERNAME/my-app:1.0.0

# push
docker push YOUR_USERNAME/my-app:1.0.0
```
