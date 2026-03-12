# 05) Exceptions & I/O (41–50)

## 41. What is the exception hierarchy in Java?

**A:** `Throwable` → (`Error`, `Exception`). `RuntimeException` is the unchecked subset of `Exception`.

## 42. When would you create a custom exception?

**A:** When you need a domain-specific failure type that callers can handle meaningfully (e.g., `InvalidOrderStateException`). Prefer unchecked unless callers can realistically recover.

## 43. How does try-with-resources work?

**A:** It automatically closes resources implementing `AutoCloseable`.

```java
try (BufferedReader br = Files.newBufferedReader(path)) {
    return br.readLine();
}
```

If both body and close throw, the close exception is **suppressed**.

## 44. Difference between `IOException` and `FileNotFoundException`?

**A:** `FileNotFoundException` is a specific `IOException` typically thrown when opening a file path that doesn’t exist or can’t be opened.

## 45. What is NIO (`java.nio`) and why use it?

**A:** NIO provides `Path`, `Files`, buffers/channels, better scalability for certain I/O patterns, and modern APIs (e.g., `Files.walk`, `Files.readString`).

## 46. `InputStream` vs `Reader`?

**A:**
- `InputStream`: byte-oriented.
- `Reader`: character-oriented (decodes bytes using charset).

Use `Reader` for text, `InputStream` for binary.

## 47. How do you choose a charset safely?

**A:** Always specify it explicitly (e.g., `StandardCharsets.UTF_8`) instead of relying on the platform default.

## 48. What is serialization, and what are the risks?

**A:** Java serialization turns objects into bytes and back. Risks: security (gadget chains), versioning fragility, hidden coupling. Prefer JSON/Protobuf and explicit schemas for APIs.

## 49. What is the difference between `throw new RuntimeException(e)` and `throw e`?

**A:** Wrapping changes the exception type and stack trace “shape”. `throw e` preserves the original type; wrapping can add context but may hide checked types.

## 50. What is exception chaining?

**A:** Storing the original exception as the cause.

```java
throw new IllegalStateException("Failed to load config", e);
```
