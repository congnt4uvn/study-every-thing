# Lesson 09 — Testing + quality toolbox

## Goal

Write unit tests with JUnit 5, understand mocking, and learn a minimal quality toolbox (formatting, static analysis, logging).

## Key concepts

- Unit tests should be fast, deterministic, and focused.
- Prefer testing behavior via public APIs.
- Mocking is a tool, not a default.
- Logging: use SLF4J + Logback (common in server apps).

## Hands-on

### 1) JUnit 5 test structure (conceptual)

```java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class MathTest {
  @Test
  void add_twoNumbers() {
    assertEquals(4, 2 + 2);
  }
}
```

### 2) Test your own code

Pick a small class from earlier lessons (e.g., `BankAccount`) and test:

- deposit increases balance
- withdraw throws on insufficient funds

### 3) What to mock

Mock external boundaries:

- current time (`Clock`)
- random values
- network calls
- filesystem

But prefer real objects for pure domain logic.

## Checklist

- You can write JUnit tests and run them.
- You can explain when mocking is helpful.
- You know why tests should not depend on ordering or time.

## Common pitfalls

- Writing tests that mirror implementation (too brittle).
- Over-mocking and testing mocks.
- Mixing unit tests with integration tests without clear separation.

## Next

Build tools: make your project repeatable (dependencies, packaging, running tests).
