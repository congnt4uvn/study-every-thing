# What’s New in Java 21 (LTS) (Lesson Notes)

Java 21 (2023) is an LTS release and one of the biggest concurrency upgrades in Java’s history. It also completes a multi-release effort around pattern matching and adds new collection APIs.

This lesson highlights the most important Java 21 features you’ll actually use.

## 1) Virtual Threads (JEP 444) — Final

**Problem:** Traditional platform threads are expensive; high-concurrency servers often need async code.

**Solution:** Virtual threads are lightweight threads managed by the JVM.

```java
import java.util.concurrent.*;

public class VirtualThreadsDemo {
  public static void main(String[] args) throws Exception {
    try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
      Future<String> f = executor.submit(() -> {
        Thread.sleep(100);
        return "done";
      });
      System.out.println(f.get());
    }
  }
}
```

Guidelines:
- Great for **blocking I/O** style code (HTTP calls, JDBC, etc.).
- You still must avoid blocking on things that don’t “park” well (some native calls).
- Keep using structured APIs (executors/scopes) rather than ad-hoc thread creation.

## 2) Structured Concurrency (JEP 453) — Preview

**Goal:** Treat multiple concurrent tasks as a single unit of work (start together, cancel together, fail together).

This is **preview** in Java 21; it requires `--enable-preview`.

Conceptually:
- Fork tasks in a scope.
- Join.
- Handle failures/cancellation deterministically.

## 3) Scoped Values (JEP 446) — Preview

Scoped values are a safer alternative to some uses of `ThreadLocal`, especially with virtual threads.

Also **preview** in 21 and requires `--enable-preview`.

Use cases:
- request IDs
- security context
- per-request configuration without global mutable state

## 4) Pattern Matching for `switch` (JEP 441) — Final

Switch now supports type patterns and guards.

```java
public class SwitchPatterns {
  static String describe(Object o) {
    return switch (o) {
      case null -> "null";
      case Integer i -> "int " + i;
      case String s when s.isBlank() -> "blank string";
      case String s -> "string '" + s + "'";
      default -> "something else";
    };
  }
}
```

Why it matters:
- Less `if/else` + casts.
- Pairs well with sealed types for exhaustiveness.

## 5) Record Patterns (JEP 440) — Final

Deconstruct records directly in patterns.

```java
public class RecordPatterns {
  record Point(int x, int y) {}

  static String quadrant(Point p) {
    return switch (p) {
      case Point(int x, int y) when x >= 0 && y >= 0 -> "Q1";
      case Point(int x, int y) when x < 0 && y >= 0 -> "Q2";
      case Point(int x, int y) when x < 0 && y < 0 -> "Q3";
      case Point(int x, int y) -> "Q4";
    };
  }
}
```

## 6) Sequenced Collections (JEP 431) — Final

Adds uniform APIs for collections with a defined encounter order.

New interfaces:
- `SequencedCollection<E>`
- `SequencedSet<E>`
- `SequencedMap<K, V>`

Key methods:
- `getFirst()`, `getLast()`
- `addFirst(E)`, `addLast(E)`
- `removeFirst()`, `removeLast()`
- `reversed()`

Example idea:
- Use `list.getFirst()` instead of `list.get(0)` for readability.

## 7) Unnamed Patterns & Variables (JEP 443) — Preview

Lets you ignore values you don’t care about using `_`.

This is **preview** in Java 21.

## 8) String Templates (JEP 430) — Preview (Java 21)

Java 21 introduces string templates as a **preview** feature (syntax and APIs may change).

It provides a structured way to combine literals and expressions (and potentially validate/escape them).

## 9) Foreign Function & Memory (FFM) API (JEP 442) — Preview

A modern alternative to JNI for calling native code and working with off-heap memory.

**Preview** in Java 21.

## 10) Performance & Runtime Highlights

- Generational ZGC (JEP 439)
- Many JIT/runtime improvements

## How to Compile/Run Preview Features

For preview features in Java 21:

- Compile: `javac --release 21 --enable-preview YourFile.java`
- Run: `java --enable-preview YourMainClass`

(Exact commands may vary if you use Maven/Gradle; set compiler args accordingly.)

## Migration Checklist (Java 17 → 21)

- Re-check frameworks: some require specific bytecode levels.
- Decide whether to use preview features; production teams often wait for final.
- Consider virtual threads for I/O-heavy services, but benchmark.

## Practice Exercises

1. Convert an executor-based server simulation to `newVirtualThreadPerTaskExecutor()`.
2. Replace a complex `instanceof` chain with a `switch` pattern match.
3. Update code that uses `list.get(0)` to `getFirst()` where it improves clarity.
