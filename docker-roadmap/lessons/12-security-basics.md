# Lesson 12 — Security basics: least privilege, secrets, scanning

## Goals
- Reduce container attack surface with simple practices
- Understand “don’t run as root” and when it matters
- Understand secrets handling and supply-chain basics

## Baseline: what Docker security is and isn’t
Docker helps you:
- Isolate processes
- Limit filesystem and network exposure
- Make deployments reproducible

Docker does not automatically:
- Fix vulnerabilities in your dependencies
- Prevent credential leaks
- Make an insecure app secure

## Practical security practices (high leverage)
### 1) Choose sane base images
- Prefer small, maintained images (e.g., `*-slim`, Alpine where appropriate)
- Prefer explicit versions over `latest`
- Keep base images updated

### 2) Don’t run as root (when possible)
In Dockerfile:
```dockerfile
# Example (conceptual)
RUN addgroup --system app && adduser --system --ingroup app app
USER app
```

If your app needs to bind to low ports (<1024) or write to specific directories, configure those paths explicitly.

### 3) Keep secrets out of images
Never do:
- `COPY .env ...` into the image
- Hard-code API keys in the Dockerfile

Do:
- Provide secrets at runtime (env vars, secret managers)
- For local dev, keep secrets in ignored files

### 4) Reduce what the container can do
At runtime (advanced but useful):
- Drop Linux capabilities
- Use read-only filesystem where possible
- Don’t mount the Docker socket into app containers unless you truly intend “containers controlling Docker”

Example flags (conceptual):
```bash
--read-only
--cap-drop=ALL
```

### 5) Scan images (conceptual)
Image scanning detects known vulnerabilities in OS packages and sometimes language deps.

Options depend on your environment:
- Docker Scout (Docker Desktop)
- Trivy (popular open-source)
- Registry scanning (GHCR, ECR, etc.)

## Supply-chain basics
Threats include:
- Compromised base image
- Typosquatting (pulling `nignx` instead of `nginx`)
- Injected dependencies in build steps

Mitigations:
- Pin versions
- Use trusted registries
- Review Dockerfile build steps
- Consider SBOM generation later

## Hands-on lab (safe basics)
1. Inspect what user an image runs as:
```powershell
docker image inspect nginx:latest | Select-String -Pattern 'User'
```

2. Run a container with a read-only rootfs (may not work for all images):
```powershell
docker run --rm --read-only nginx:latest
```

If it fails, that’s a useful lesson: many apps need a writable temp directory; you’d provide one explicitly.

## Checklist
- I avoid `latest` and choose maintained bases
- I understand why secrets must not be baked into images
- I can describe simple runtime hardening options
