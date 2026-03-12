# Lesson 07 — Concurrency essentials

## Goal

Understand threads, executors, and concurrency primitives. Learn safe patterns for parallel work and how to avoid common bugs.

## Key concepts

- Race condition: result depends on timing.
- Visibility: one thread may not see another thread’s updates without proper synchronization.
- Prefer high-level concurrency utilities: `ExecutorService`, `CompletableFuture`.
- Use `synchronized`/locks only when needed and keep critical sections small.

## Hands-on

### 1) The problem: shared mutable state

```java
public final class Counter {
  private int value = 0;
  public void inc() { value++; }
  public int get() { return value; }
}
```

If multiple threads call `inc()`, you can lose increments.

### 2) Fix with synchronization

```java
public final class SafeCounter {
  private int value = 0;
  public synchronized void inc() { value++; }
  public synchronized int get() { return value; }
}
```

### 3) Prefer atomic types for counters

```java
import java.util.concurrent.atomic.AtomicInteger;

public final class AtomicCounter {
  private final AtomicInteger value = new AtomicInteger(0);
  public void inc() { value.incrementAndGet(); }
  public int get() { return value.get(); }
}
```

### 4) ExecutorService for task execution

```java
import java.util.concurrent.*;

ExecutorService pool = Executors.newFixedThreadPool(4);

Future<Integer> f = pool.submit(() -> 40 + 2);
System.out.println(f.get());

pool.shutdown();
```

### 5) CompletableFuture for async pipelines

```java
import java.util.concurrent.CompletableFuture;

CompletableFuture<Integer> cf = CompletableFuture
  .supplyAsync(() -> 21)
  .thenApply(x -> x * 2);

System.out.println(cf.join());
```

## Checklist

- You can explain race conditions and how to prevent them.
- You can run work in a thread pool.
- You can chain async steps with `CompletableFuture`.

## Common pitfalls

- Creating a new thread per request/task.
- Forgetting to shut down executors.
- Holding locks while doing slow I/O.

## Next

JVM basics and performance: how your code runs and how to measure it.
