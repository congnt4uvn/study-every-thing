# Lesson 03 — Exceptions, packages, and generics

## Goal

Learn how Java organizes code with packages, how exceptions work, and how generics provide type safety.

## Key concepts

- Packages map to folders; they prevent naming collisions.
- Exceptions are for **exceptional** situations (not normal control flow).
- Checked vs unchecked exceptions (practically: most modern application code uses unchecked, but you must understand both).
- Generics: `List<String>` means a list that only contains strings.

## Hands-on

### 1) Create a package

File path example:

- `src/main/java/com/example/app/Main.java`

```java
package com.example.app;

public class Main {
  public static void main(String[] args) {
    System.out.println("packaged!");
  }
}
```

### 2) Exceptions: throw, try/catch/finally

```java
static int parsePositiveInt(String s) {
  try {
    int n = Integer.parseInt(s);
    if (n <= 0) {
      throw new IllegalArgumentException("must be > 0");
    }
    return n;
  } catch (NumberFormatException e) {
    throw new IllegalArgumentException("not an integer: " + s, e);
  }
}
```

Rules of thumb:

- Include context in exception messages.
- Wrap lower-level exceptions when it helps preserve cause + add meaning.

### 3) Generics: write a typed wrapper

```java
public final class Box<T> {
  private final T value;

  public Box(T value) {
    this.value = value;
  }

  public T get() {
    return value;
  }
}

Box<String> b = new Box<>("hello");
String v = b.get();
```

### 4) Wildcards (read-only vs write)

```java
static int totalLength(java.util.List<? extends CharSequence> items) {
  int total = 0;
  for (CharSequence cs : items) {
    total += cs.length();
  }
  return total;
}
```

## Checklist

- You can structure code using packages.
- You can throw and handle exceptions intentionally.
- You can use generics (`List<T>`, `Map<K,V>`) without raw types.

## Common pitfalls

- Catching `Exception` everywhere (too broad; hides bugs).
- Swallowing exceptions (catching and doing nothing).
- Using raw types like `List` instead of `List<String>`.

## Next

Collections: the standard data structures you’ll use constantly.
