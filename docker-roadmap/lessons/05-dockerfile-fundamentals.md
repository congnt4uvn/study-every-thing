# Lesson 05 — Dockerfile fundamentals

## Goals
- Write a Dockerfile that builds a runnable image
- Understand key instructions: `FROM`, `WORKDIR`, `COPY`, `RUN`, `CMD`, `ENTRYPOINT`, `EXPOSE`
- Understand build context and why `.dockerignore` matters

## The build context
When you run `docker build .`, the `.` is the **build context**.
- Docker sends the context to the builder
- Large contexts make builds slow
- Sensitive files in context can accidentally end up inside images

## A minimal Dockerfile example
This example builds an image that runs a simple command.

```dockerfile
FROM alpine:3.19
CMD ["echo", "hello from a container"]
```

Build and run:
```powershell
docker build -t hello-alpine:1.0 .
docker run --rm hello-alpine:1.0
```

## Key instructions (practical meaning)
- `FROM` — base image
- `WORKDIR` — set working directory (creates it if needed)
- `COPY` — copy files into the image (from the build context)
- `RUN` — execute commands at build time (creates new layers)
- `ENV` — set environment variables
- `EXPOSE` — documentation of intended port (does not publish ports)
- `CMD` — default arguments (can be overridden at `docker run` time)
- `ENTRYPOINT` — the executable (often used for “always run this”)

### `CMD` vs `ENTRYPOINT`
- `CMD` is “default parameters.”
- `ENTRYPOINT` is “the program.”

Common pattern:
```dockerfile
ENTRYPOINT ["myapp"]
CMD ["--help"]
```

## Hands-on lab: containerize a tiny HTTP server (no code required)
We’ll use Python’s built-in web server.

Create a folder with a file `index.html`, then use:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY index.html /app/index.html
EXPOSE 8000
CMD ["python", "-m", "http.server", "8000"]
```

Build + run:
```powershell
docker build -t tiny-web:1.0 .
docker run --rm -p 8000:8000 tiny-web:1.0
```

Visit http://localhost:8000

## Checklist
- I can explain build context
- I can build an image with a Dockerfile and run it
- I understand `CMD` vs `ENTRYPOINT` at a high level

## Common pitfalls
- **Forgetting the build context**: `COPY` can only copy from the build context (not arbitrary system paths).
- **Copying too much**: you’ll fix this next lesson with `.dockerignore`.
- **Using `latest` everywhere**: prefer explicit base versions.
