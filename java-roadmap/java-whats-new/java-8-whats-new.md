# What’s New in Java 8 (Lesson Notes)

Java 8 (2014) was a major shift toward **functional-style programming** in Java. If you learn only one release deeply, Java 8 is still foundational because many modern APIs and coding styles assume these concepts.

## 1) Lambda Expressions

**Goal:** Pass behavior (code) as data.

### Before Java 8
You had to write anonymous inner classes.

### Java 8
You can write lambdas for **functional interfaces** (interfaces with exactly one abstract method).

```java
import java.util.Arrays;
import java.util.List;

public class Lambdas {
  public static void main(String[] args) {
    List<String> names = Arrays.asList("Bob", "Alice", "Charlie");
    names.sort((a, b) -> a.compareToIgnoreCase(b));
    System.out.println(names);
  }
}
```

**Key ideas**
- Lambdas capture “effectively final” variables.
- They don’t create a new scope for `this` (unlike anonymous classes).

## 2) Method References

Method references are shorthand for simple lambdas.

```java
import java.util.Arrays;
import java.util.List;

public class MethodRefs {
  public static void main(String[] args) {
    List<String> names = Arrays.asList("A", "B", "C");
    names.forEach(System.out::println);
  }
}
```

Forms:
- `ClassName::staticMethod`
- `instance::instanceMethod`
- `ClassName::instanceMethod` (receiver becomes first argument)
- `ClassName::new` (constructor reference)

## 3) Streams API

**Goal:** Declarative data pipelines with transformations and terminal operations.

```java
import java.util.List;
import java.util.Arrays;
import java.util.stream.Collectors;

public class Streams {
  public static void main(String[] args) {
    List<String> words = Arrays.asList("java", "stream", "API", "rocks");

    String result = words.stream()
        .filter(w -> w.length() >= 4)
        .map(String::toUpperCase)
        .sorted()
        .collect(Collectors.joining(", "));

    System.out.println(result);
  }
}
```

**Important stream concepts**
- Streams are **lazy**: intermediate ops don’t run until a terminal op executes.
- Prefer stateless, non-interfering functions.
- Parallel streams exist (`parallelStream()`), but they’re not a free speedup.

## 4) Default & Static Methods in Interfaces

Java 8 allows interfaces to evolve without breaking all implementers.

```java
interface Greeter {
  default String hello(String name) {
    return "Hello, " + name;
  }

  static Greeter english() {
    return new Greeter() {};
  }
}
```

Rules to remember:
- If a class provides an implementation, it wins over interface defaults.
- If two interfaces provide the same default, you must disambiguate.

## 5) Functional Interfaces (`java.util.function`)

Common functional interfaces:
- `Predicate<T>`: `T -> boolean`
- `Function<T, R>`: `T -> R`
- `Supplier<T>`: `() -> T`
- `Consumer<T>`: `T -> void`
- `UnaryOperator<T>` / `BinaryOperator<T>`

Example:

```java
import java.util.function.Predicate;

public class Predicates {
  public static void main(String[] args) {
    Predicate<String> longWord = s -> s.length() >= 10;
    System.out.println(longWord.test("encyclopedia"));
  }
}
```

## 6) `Optional<T>`

**Goal:** Represent “maybe present” values explicitly.

```java
import java.util.Optional;

public class Optionals {
  static Optional<String> findUserEmail(String userId) {
    if (userId == null) return Optional.empty();
    return Optional.of(userId + "@example.com");
  }

  public static void main(String[] args) {
    String email = findUserEmail("u1")
        .map(String::toLowerCase)
        .orElse("unknown@example.com");

    System.out.println(email);
  }
}
```

Guidelines:
- Don’t use `Optional` for fields in domain models unless your team standardizes it.
- Don’t call `get()` without `isPresent()`.

## 7) New Date/Time API (`java.time`)

Java 8 introduced a modern, immutable date/time API inspired by Joda-Time.

```java
import java.time.*;

public class TimeApi {
  public static void main(String[] args) {
    LocalDate today = LocalDate.now();
    LocalDate payday = LocalDate.of(2026, 3, 31);

    Period until = Period.between(today, payday);
    System.out.println("Days until payday: " + until.getDays());

    Instant now = Instant.now();
    System.out.println("Epoch millis: " + now.toEpochMilli());
  }
}
```

Use cases:
- `LocalDate`, `LocalTime`, `LocalDateTime` for local concepts
- `ZonedDateTime` for time zones
- `Instant` for timestamps

## 8) `CompletableFuture`

**Goal:** Compose async tasks without “callback hell”.

```java
import java.util.concurrent.CompletableFuture;

public class Futures {
  public static void main(String[] args) {
    CompletableFuture<Integer> f = CompletableFuture
        .supplyAsync(() -> 40)
        .thenApply(x -> x + 2)
        .thenApply(x -> x * 10);

    System.out.println(f.join());
  }
}
```

Notes:
- `join()` throws unchecked exceptions; `get()` throws checked ones.
- For production, consider providing a custom `Executor`.

## 9) Small-but-Useful Additions

- Base64: `java.util.Base64`
- Collections improvements: `forEach`, `removeIf`, `replaceAll`, `computeIfAbsent`
- Parallel array ops: `Arrays.parallelSort` and friends
- Repeating/type annotations (advanced; mostly tooling/frameworks)

## Migration Tips (Pre-8 → 8)

- Introduce streams gradually; don’t force streams everywhere.
- Prefer `java.time` over `java.util.Date`/`Calendar`.
- Learn the difference between `map` vs `flatMap` for `Optional`/streams.

## Practice Exercises

1. Convert a loop that filters and transforms a list into a stream pipeline.
2. Write a `CompletableFuture` chain with error handling (`exceptionally`).
3. Refactor a `Date`-based utility to `java.time`.
