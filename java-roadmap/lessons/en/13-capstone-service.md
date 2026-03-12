# Lesson 13 — Capstone: production-style Java service

## Goal

Build a small service end-to-end with good engineering habits: clean APIs, tests, persistence, configuration, and basic operational readiness.

## Project: “Task Tracker API”

Build a REST API that manages tasks.

### Requirements (MVP)

- Create task
- Get task by id
- List tasks (simple pagination: `limit` + `offset`)
- Update task status
- Delete task

Task fields:

- `id` (string)
- `title` (non-blank)
- `status` (`OPEN`, `DONE`)
- `createdAt` (timestamp)

### Non-functional requirements

- Validation errors return 400.
- Not found returns 404.
- Unit tests for core service logic.
- Integration test for repository (optional but recommended).

## Suggested architecture

- Controller layer: request/response mapping only
- Service layer: business rules + transactions
- Repository layer: DB access
- DTOs: public API shapes
- Entities: DB shapes

## Step-by-step checklist

1) Scaffold Spring Boot project (Web, Validation, Data JPA).

2) Add DB + migrations

- Use H2 first if you want speed.
- Move to PostgreSQL when ready.
- Add Flyway migration for `tasks` table.

3) Implement domain logic

- Define allowed status transitions (if any).
- Enforce title constraints.

4) Implement endpoints

- `POST /api/tasks`
- `GET /api/tasks/{id}`
- `GET /api/tasks?limit=..&offset=..`
- `PATCH /api/tasks/{id}` (status update)
- `DELETE /api/tasks/{id}`

5) Add tests

- Unit tests for `TaskService`.
- Test validation and not-found behavior (controller tests or integration).

6) Add operational basics

- Use structured logging (at least consistent log messages).
- Add config via `application.yml` + environment variables.
- Add a `/actuator/health` endpoint if you include Spring Actuator.

## What “done” looks like

- You can run the service locally and call it with curl/Postman.
- Tests run in CI-style via `mvn test` or `gradle test`.
- You can explain where business logic lives and why.

## Next (optional directions)

- Add authentication/authorization.
- Add caching (Redis) for read-heavy endpoints.
- Containerize with Docker and add a simple CI pipeline.
