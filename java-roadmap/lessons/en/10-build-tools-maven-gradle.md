# Lesson 10 — Build tools: Maven / Gradle

## Goal

Learn the standard Java project structure and how Maven/Gradle manage dependencies, compilation, and tests.

## Key concepts

- A build tool makes your project reproducible.
- Dependencies have versions; you must manage upgrades intentionally.
- Standard layout (Maven/Gradle):
  - `src/main/java` (production code)
  - `src/test/java` (tests)

## Hands-on (Maven path)

### 1) Create a Maven project

If you have Maven installed:

```bash
mvn -v
```

Generate a project (example):

```bash
mvn archetype:generate -DgroupId=com.example -DartifactId=demo -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false
```

### 2) Add dependencies

Common starter deps:

- JUnit 5 for tests
- Jackson for JSON

You’ll edit `pom.xml` to add them.

### 3) Build and test

```bash
mvn test
mvn package
```

## Hands-on (Gradle path)

If you use Gradle, learn the equivalent:

- `build.gradle` / `build.gradle.kts`
- `gradle test`
- dependency blocks

## Checklist

- You can explain why a build tool matters.
- You can add a dependency and use it in code.
- You can run tests via the build tool.

## Common pitfalls

- Copy/pasting random versions without understanding.
- Not pinning tool versions in teams.
- Mixing Gradle and Maven concepts.

## Next

Spring Boot: build a real HTTP API the way Java teams commonly do.
