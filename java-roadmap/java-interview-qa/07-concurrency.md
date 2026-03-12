# 07) Concurrency (61–70)

## 61. What is the difference between a process and a thread?

**A:** A process has its own address space; threads share the process memory but have separate stacks and scheduling.

## 62. What does `synchronized` do?

**A:** It provides mutual exclusion and establishes a happens-before relationship: entering a monitor acquires a lock; exiting releases it, ensuring visibility of writes.

## 63. What is `volatile` used for?

**A:** `volatile` ensures **visibility** of reads/writes and prevents certain reordering; it does not provide atomicity for compound actions.

```java
private volatile boolean running = true;
```

## 64. Why is `i++` not thread-safe?

**A:** It’s a read-modify-write sequence (three steps). Without atomicity, updates can be lost. Use `AtomicInteger.incrementAndGet()` or locking.

## 65. What is deadlock? Give a typical cause.

**A:** Two+ threads each hold a lock and wait for the other, forming a cycle. A common cause is inconsistent lock ordering.

## 66. `wait()` vs `sleep()`?

**A:**
- `wait()`: releases the monitor and waits for notify; must be called while holding the monitor.
- `sleep()`: pauses a thread but **does not** release locks.

## 67. `notify()` vs `notifyAll()`?

**A:** `notify()` wakes one waiting thread; `notifyAll()` wakes all. In many designs, `notifyAll()` is safer to avoid missed conditions, but can cause thundering herd.

## 68. What is an `ExecutorService` and why use it?

**A:** It manages thread pools and task execution, separating submission from execution policy.

```java
ExecutorService pool = Executors.newFixedThreadPool(8);
Future<Integer> f = pool.submit(() -> 42);
```

## 69. What is the difference between `Runnable` and `Callable`?

**A:** `Runnable` returns no value and can’t throw checked exceptions; `Callable<V>` returns a value and can throw checked exceptions.

## 70. What are `CompletableFuture` and common use cases?

**A:** A promise-like API for async composition: chaining, combining, handling errors.

```java
CompletableFuture.supplyAsync(this::load)
    .thenApply(this::transform)
    .exceptionally(ex -> fallback());
```
