# Lesson 08 — JVM basics + performance

## Goal

Understand how Java runs on the JVM, learn memory/GC basics, and build a habit of measuring performance before optimizing.

## Key concepts

- Java code compiles to bytecode; the JVM interprets and JIT-compiles hot code.
- Memory is managed by GC; object allocation is cheap, but allocation *rate* matters.
- Common tools: `jcmd`, `jstack`, `jmap` (advanced), profilers (VisualVM, YourKit, async-profiler).
- Benchmarking: microbenchmarks are tricky; use JMH when you need real numbers.

## Hands-on

### 1) Observe memory settings

Run:

```bash
java -XshowSettings:vm -version
```

Look for heap settings.

### 2) Simple timing (good for sanity checks, not true benchmarking)

```java
long start = System.nanoTime();

long sum = 0;
for (int i = 0; i < 10_000_000; i++) {
  sum += i;
}

long elapsedMs = (System.nanoTime() - start) / 1_000_000;
System.out.println("sum=" + sum + " elapsedMs=" + elapsedMs);
```

### 3) Basic profiling mindset

Before optimizing, ask:

- What is slow? (measure)
- Where is time spent? (profile)
- What changed? (repeat)

## Checklist

- You can explain what the JVM does at a high level (bytecode, JIT, GC).
- You know why “benchmarks” with a single `System.nanoTime()` can mislead.
- You know at least one profiler you can use.

## Common pitfalls

- Optimizing without measuring.
- Prematurely tuning GC for beginner projects.
- Confusing throughput vs latency.

## Next

Testing and quality: build confidence and avoid regressions.
