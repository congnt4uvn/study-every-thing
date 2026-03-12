# 08) Streams & Functional Style (71–80)

## 71. What is a Stream in Java?

**A:** A Stream is a declarative pipeline over data supporting transformations and terminal operations; it’s not a data structure and can be consumed once.

## 72. Intermediate vs terminal operations?

**A:**
- Intermediate: lazy transformations (`map`, `filter`, `sorted`).
- Terminal: triggers execution (`collect`, `forEach`, `reduce`, `count`).

## 73. `map` vs `flatMap`?

**A:**
- `map`: 1-to-1 transform.
- `flatMap`: 1-to-many, then flattens.

```java
Stream<String> words = lines.flatMap(line -> Arrays.stream(line.split("\\s+")));
```

## 74. `Optional` — what is it for, and what is it not for?

**A:** It models an optional return value to reduce `null` handling. It’s not intended for fields in most designs and shouldn’t replace every null check.

## 75. `orElse` vs `orElseGet`?

**A:** `orElse(x)` eagerly evaluates `x`; `orElseGet(supplier)` is lazy.

```java
value.orElseGet(this::expensiveDefault);
```

## 76. What is method reference syntax?

**A:** A shorthand for lambdas.

```java
list.forEach(System.out::println);
```

## 77. `Collectors.toList()` vs `Stream.toList()`?

**A:** `Stream.toList()` returns an unmodifiable list (implementation-defined). `Collectors.toList()` usually returns a mutable list but doesn’t guarantee mutability.

## 78. When are parallel streams a bad idea?

**A:** For small workloads, heavy contention, blocking I/O, or when order/side-effects matter. Measure; don’t assume faster.

## 79. What is `reduce` and a common pitfall?

**A:** `reduce` combines elements into one. Pitfall: using a non-associative accumulator or mutating shared state breaks parallel behavior.

## 80. Give an example of grouping with streams.

**A:**

```java
Map<String, Long> counts = words.stream()
    .collect(Collectors.groupingBy(w -> w, Collectors.counting()));
```
