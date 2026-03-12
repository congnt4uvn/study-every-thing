# Docker Zero → Hero Roadmap

A practical, hands-on study plan to learn Docker from fundamentals to real-world workflows.

## Who this is for
- Developers who want consistent local dev environments
- DevOps/SRE beginners who need container basics for deployment pipelines
- Anyone who wants to *understand* what Docker is doing (not just copy/paste commands)

## How to use this roadmap
- Go lesson-by-lesson in order.
- Every lesson has:
  - **Goals** (what you should be able to do)
  - **Concepts** (what you should understand)
  - **Hands-on lab** (commands + expected outcomes)
  - **Checklist** (quick self-test)
- Keep a notes file of mistakes and fixes; Docker skill improves fastest by debugging.

## Prerequisites
- Basic terminal comfort (PowerShell or Bash)
- Basic app knowledge (any one: Node/Python/.NET/Java)

## Study schedule (suggested)
- **Fast track (1 week):** 1–2 lessons/day + capstone on the weekend
- **Steady (2–3 weeks):** 3–5 lessons/week + repeat labs until fluent

## Lessons
1. [Lesson 01 — What Docker is + install + first container](lessons/01-what-is-docker.md)
2. [Lesson 02 — Core concepts: images, containers, layers, registries](lessons/02-core-concepts.md)
3. [Lesson 03 — Container lifecycle + essential CLI](lessons/03-cli-and-lifecycle.md)
4. [Lesson 04 — Images in practice: pull, tag, inspect, push](lessons/04-images-in-practice.md)
5. [Lesson 05 — Dockerfile fundamentals](lessons/05-dockerfile-fundamentals.md)
6. [Lesson 06 — Better builds: caching, .dockerignore, multi-stage](lessons/06-better-builds.md)
7. [Lesson 07 — Data: volumes, bind mounts, permissions](lessons/07-volumes-and-mounts.md)
8. [Lesson 08 — Networking: ports, DNS, bridge networks](lessons/08-networking-basics.md)
9. [Lesson 09 — Docker Compose essentials](lessons/09-compose-essentials.md)
10. [Lesson 10 — Compose patterns: dev/prod, env, healthchecks](lessons/10-compose-patterns.md)
11. [Lesson 11 — Debugging & troubleshooting](lessons/11-debugging.md)
12. [Lesson 12 — Security basics: least privilege, secrets, scanning](lessons/12-security-basics.md)
13. [Lesson 13 — Capstone: containerize an app + publish an image](lessons/13-capstone.md)

## What “hero” looks like
You’re effectively “Docker-proficient” when you can:
- Write Dockerfiles that build fast and ship small images
- Use Compose to run multi-service systems locally
- Debug common issues (ports, mounts, DNS, permissions)
- Push versioned images to a registry and explain what’s inside

## Optional next steps
- Learn OCI concepts and how Docker relates to containerd
- Learn Kubernetes basics (deployments, services, ingress)
- Learn supply-chain security deeper (SBOMs, signing, SLSA)
