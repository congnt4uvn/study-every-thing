# Lesson 04 — Collections + equals/hashCode

## Goal

Learn core collections (`List`, `Set`, `Map`) and the rules for `equals()`/`hashCode()` that make them work correctly.

## Key concepts

- `List`: ordered, duplicates allowed.
- `Set`: no duplicates.
- `Map`: key → value.
- Big-O intuition matters (e.g., `HashMap` average $O(1)$ lookup).
- `equals()` and `hashCode()` must be consistent, especially for `HashSet` and `HashMap` keys.

## Hands-on

### 1) Lists and iteration

```java
var names = new java.util.ArrayList<String>();
names.add("Ada");
names.add("Linus");

for (String name : names) {
  System.out.println(name);
}
```

### 2) Maps

```java
var ages = new java.util.HashMap<String, Integer>();
ages.put("Ada", 20);

System.out.println(ages.get("Ada"));
System.out.println(ages.getOrDefault("Bob", -1));
```

### 3) equals/hashCode with a value object

```java
import java.util.Objects;

public final class UserId {
  private final String value;

  public UserId(String value) {
    if (value == null || value.isBlank()) {
      throw new IllegalArgumentException("value required");
    }
    this.value = value;
  }

  public String value() {
    return value;
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) return true;
    if (!(o instanceof UserId other)) return false;
    return value.equals(other.value);
  }

  @Override
  public int hashCode() {
    return Objects.hash(value);
  }

  @Override
  public String toString() {
    return value;
  }
}
```

Try it:

```java
var set = new java.util.HashSet<UserId>();
set.add(new UserId("u1"));
System.out.println(set.contains(new UserId("u1"))); // should be true
```

### 4) When to use which

- Need ordering? `ArrayList`.
- Need uniqueness? `HashSet`.
- Need key-based lookup? `HashMap`.
- Need sorted keys? `TreeMap` / `TreeSet`.

## Checklist

- You can choose `List` vs `Set` vs `Map` for a use case.
- You can implement `equals()`/`hashCode()` correctly for value objects.
- You understand why mutating keys in a `HashMap` is dangerous.

## Common pitfalls

- Using mutable objects as map keys.
- Forgetting to override `hashCode()` when overriding `equals()`.
- Prematurely optimizing with exotic collections.

## Next

Functional Java: lambdas, streams, and Optional.
