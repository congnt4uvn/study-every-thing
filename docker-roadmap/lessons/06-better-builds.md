# Lesson 06 — Better builds: caching, .dockerignore, multi-stage

## Goals
- Make builds faster and images smaller
- Understand cache invalidation (why small Dockerfile changes can cause big rebuilds)
- Use `.dockerignore` to keep secrets/junk out of images
- Use multi-stage builds for production images

## Caching fundamentals
Docker caches build steps (layers). A step is reusable when:
- The instruction text is identical, and
- All inputs to that instruction are unchanged (for `COPY`, file contents matter)

**Rule:** Put the most frequently changing steps *later* in the Dockerfile.

### Example: Node app (cache-friendly ordering)
Bad (rebuilds dependencies every time you change source):
```dockerfile
COPY . .
RUN npm ci
```

Better:
```dockerfile
COPY package*.json ./
RUN npm ci
COPY . .
```

## `.dockerignore`
Create `.dockerignore` to avoid copying unnecessary files into the build context.

Typical entries:
```gitignore
.git
node_modules
bin
obj
*.log
.env
.env.*
Dockerfile
compose*.yaml
```

Why it matters:
- Speed: smaller build context
- Security: prevents accidental inclusion of secrets
- Correctness: avoids “works on my machine” artifacts

## Multi-stage builds
Multi-stage builds let you:
- Build with heavyweight tools (SDKs, compilers)
- Ship only the runtime output (small image)

Example (conceptual):
```dockerfile
# Build stage
FROM node:20 AS build
WORKDIR /src
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Runtime stage
FROM nginx:1.27
COPY --from=build /src/dist /usr/share/nginx/html
```

## Build arguments and environment variables
- `ARG` exists only at build time
- `ENV` exists at runtime (inside the running container)

Common use:
- `ARG` for choosing a build mode
- `ENV` for configuring the application

## Hands-on lab
1. Create a folder with:
   - `Dockerfile`
   - `.dockerignore`
   - a few dummy files (`notes.txt`, `.env`, `node_modules/` folder)

2. Build twice and compare speed:
```powershell
docker build -t demo-cache:1.0 .
docker build -t demo-cache:1.0 .
```

3. Change a file that is copied *late* in the Dockerfile and rebuild.
   - Observe: earlier layers remain cached.

4. Confirm `.dockerignore` works:
   - Add a huge dummy file and ignore it; rebuild context should stay small.

## Checklist
- I can explain why Dockerfile ordering affects build speed
- I understand `.dockerignore` and use it by default
- I can describe multi-stage builds and why they produce smaller images

## Common pitfalls
- **Copying the whole repo too early**: destroys cache efficiency.
- **Forgetting `.dockerignore`**: leaks secrets and slows builds.
- **Shipping build tools**: huge images and larger attack surface.
