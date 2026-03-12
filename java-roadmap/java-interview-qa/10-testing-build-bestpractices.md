# 10) Testing, Build & Best Practices (91–100)

## 91. JUnit 5 vs JUnit 4 — big differences?

**A:** JUnit 5 is modular (`junit-jupiter`), supports richer extensions, parameterized tests improvements, and modern annotations (`@Test` lives in a different package).

## 92. What is a unit test vs an integration test?

**A:**
- Unit: tests a small unit in isolation (often with fakes/mocks).
- Integration: tests interactions between components (DB, filesystem, HTTP), slower but higher confidence.

## 93. What is mocking and when should you avoid it?

**A:** Mocking replaces dependencies with test doubles. Avoid over-mocking internal details; prefer mocking external boundaries and testing behavior.

## 94. Maven vs Gradle?

**A:**
- Maven: declarative XML, convention-heavy, stable.
- Gradle: programmable DSL, faster incremental builds, flexible.

Teams often choose based on ecosystem and build complexity.

## 95. What is semantic versioning and why care?

**A:** `MAJOR.MINOR.PATCH`. Breaking changes increment MAJOR; new backward-compatible features increment MINOR; fixes increment PATCH. Helps dependency management and upgrade safety.

## 96. Why is `null` considered problematic, and what are alternatives?

**A:** `null` causes NPEs and unclear contracts. Alternatives: `Optional` for returns, empty collections, Null Object pattern, validation.

## 97. What is SOLID (briefly)?

**A:** Five design principles: Single responsibility, Open/closed, Liskov substitution, Interface segregation, Dependency inversion.

## 98. How would you design for testability in Java?

**A:** Prefer constructor injection, avoid global state (`static`), depend on interfaces, keep side effects at boundaries, and separate pure logic from I/O.

## 99. What is the difference between `System.currentTimeMillis()` and `System.nanoTime()`?

**A:**
- `currentTimeMillis`: wall-clock time (can jump).
- `nanoTime`: monotonic for measuring elapsed time (best for durations).

## 100. What are common performance pitfalls in Java services?

**A:** Excess allocations (GC pressure), blocking I/O on request threads, contention on locks, unbounded caches/queues, chatty logging, and missing timeouts/retries.
