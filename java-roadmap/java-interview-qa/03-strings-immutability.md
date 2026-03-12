# 03) Strings & Immutability (21–30)

## 21. Why is `String` immutable?

**A:** Enables safe sharing, string interning, caching of hash code, and security (e.g., classloading, file paths) because values can’t be changed behind your back.

## 22. What is the String pool (interning)?

**A:** The JVM keeps a pool of canonical `String` instances. String literals are interned by default.

```java
String a = "hi";
String b = "hi";
System.out.println(a == b); // true (same interned object)
```

## 23. `new String("x")` vs `"x"`?

**A:** `"x"` uses the interned literal; `new String("x")` creates a new object (usually unnecessary).

## 24. `StringBuilder` vs `StringBuffer`?

**A:**
- `StringBuilder`: mutable, **not synchronized**, faster in single-thread contexts.
- `StringBuffer`: synchronized (legacy); usually avoid unless you truly need it.

## 25. Why is string concatenation in loops slow?

**A:** `String` is immutable; `s += x` creates new objects repeatedly. Use `StringBuilder`.

```java
StringBuilder sb = new StringBuilder();
for (String part : parts) sb.append(part);
String result = sb.toString();
```

## 26. What does `String#equalsIgnoreCase` do (and not do)?

**A:** It compares characters case-insensitively in a locale-independent way (but still not a full Unicode locale-aware collation). For sorting/human text, use `Collator`.

## 27. What is a “defensive copy”?

**A:** When exposing mutable state, copy it to keep immutability.

```java
public Date getCreatedAt() { return new Date(createdAt.getTime()); }
```

Prefer modern immutable types like `Instant`.

## 28. How do you build an immutable class in Java?

**A:**
- Make class `final` (or ensure no mutating overrides).
- Make fields `private final`.
- No setters.
- Validate in constructor.
- Defensive copies for mutable inputs/outputs.

## 29. What is `record` in Java, and when would you use it?

**A:** A `record` is a concise immutable data carrier.

```java
public record Point(int x, int y) {}
```

Use for DTOs/value objects where identity is the state.

## 30. How do `String#format` and `System.out.printf` differ?

**A:** Both use format specifiers; `String.format` returns a string, `printf` writes to an output stream. `String.format` can be slower than simple concatenation for trivial cases.
