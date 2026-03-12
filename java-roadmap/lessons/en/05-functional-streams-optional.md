# Lesson 05 — Lambdas, Streams, Optional

## Goal

Write cleaner data-processing code using lambdas and streams, and handle absence safely with `Optional`.

## Key concepts

- Lambda: function value (behavior passed as data).
- Stream: a pipeline for processing collections.
- Prefer **pure functions** in stream operations (avoid side effects).
- `Optional<T>` expresses “may be missing” explicitly.

## Hands-on

### 1) Lambdas and functional interfaces

```java
java.util.function.Predicate<String> nonBlank = s -> s != null && !s.isBlank();
System.out.println(nonBlank.test("hi"));
```

### 2) Stream pipeline

```java
var names = java.util.List.of(" Ada ", "", "Bob", "alice");

var cleaned = names.stream()
  .map(String::trim)
  .filter(s -> !s.isBlank())
  .map(String::toLowerCase)
  .sorted()
  .toList();

System.out.println(cleaned);
```

### 3) Grouping and counting

```java
var words = java.util.List.of("a", "bb", "c", "dd", "eee");

var countsByLength = words.stream()
  .collect(java.util.stream.Collectors.groupingBy(
    String::length,
    java.util.stream.Collectors.counting()
  ));

System.out.println(countsByLength);
```

### 4) Optional: avoid null checks everywhere

```java
static java.util.Optional<String> findUserEmail(java.util.Map<String, String> emails, String userId) {
  return java.util.Optional.ofNullable(emails.get(userId));
}

var emails = java.util.Map.of("u1", "u1@example.com");

String email = findUserEmail(emails, "u2")
  .orElse("unknown@example.com");
```

## Checklist

- You can write stream pipelines with `map/filter/sorted/collect`.
- You can explain when streams are appropriate (and when a loop is clearer).
- You can use `Optional` intentionally.

## Common pitfalls

- Overusing streams for simple code (readability matters).
- Using `Optional` as a field type everywhere (use sparingly; great for return values).
- Side effects in `map()` (keep transformations pure).

## Next

I/O and integration basics: files, JSON, and HTTP calls.
