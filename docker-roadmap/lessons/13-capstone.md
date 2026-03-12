# Lesson 13 — Capstone: containerize an app + publish an image

## Goal
Demonstrate end-to-end Docker proficiency by:
- Creating a production-minded Dockerfile
- Running the app locally with Compose (app + dependency)
- Tagging and publishing an image (to a registry you control)

## Suggested capstone project
Choose one simple web app you can run locally (any language). Examples:
- Python Flask/FastAPI
- Node Express
- .NET minimal API

Add one dependency service:
- Postgres or Redis

## Deliverables (what to build)
1) `.dockerignore`
2) `Dockerfile` (multi-stage if your language benefits)
3) `compose.yaml` with at least two services
4) A short README describing how to run it

## Reference templates (adapt to your stack)
### `.dockerignore` (starter)
```gitignore
.git
.env
.env.*
**/*.log
node_modules
bin
obj
__pycache__
.venv
```

### `compose.yaml` (app + postgres example)
```yaml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: example
      POSTGRES_USER: app
      POSTGRES_DB: app
    volumes:
      - dbdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  app:
    build:
      context: .
    environment:
      DATABASE_URL: "postgres://app:example@db:5432/app"
    ports:
      - "8080:8080"
    depends_on:
      - db

volumes:
  dbdata:
```

### Dockerfile patterns
#### Pattern A: simple runtime (no build step)
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080
CMD ["python", "app.py"]
```

#### Pattern B: multi-stage build (when you compile/build assets)
Multi-stage is most useful when you have a build output you can copy into a smaller runtime image.

## Run and validate
```powershell
# Build and start everything
docker compose up --build

# In another terminal, watch status
docker compose ps

# View logs
docker compose logs -f
```

Validation checklist:
- App starts without manual container steps
- Restarting containers doesn’t lose database data (volume works)
- No secrets are baked into the image
- Image builds repeatably

## Publish the image
1. Choose a versioning scheme (e.g., `1.0.0`, `1.0.1`)
2. Tag and push:
```powershell
# Example with Docker Hub
docker tag <your-local-image>:latest <your-username>/<repo>:1.0.0
docker push <your-username>/<repo>:1.0.0
```

## Stretch goals (optional)
- Add a healthcheck to the app
- Run the app as a non-root user
- Reduce image size with multi-stage build and smaller base
- Add a CI workflow that builds and pushes on tags

## Checklist
- I can build, run, debug, and publish a real Docker image
- I can explain my Dockerfile and Compose decisions
- I can reproduce the environment on another machine
