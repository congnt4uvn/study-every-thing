# What’s New in Java 17 (LTS) (Lesson Notes)

Java 17 (2021) is a Long-Term Support release. In practice, adopting Java 17 usually means adopting a *set* of language and platform improvements that matured across Java 9–17.

This lesson focuses on the features you’ll most likely use when moving a codebase from Java 8 to Java 17.

## 1) The Java Platform Module System (JPMS) (Java 9)

**Goal:** Stronger encapsulation and reliable configuration.

- A *module* is a named set of packages with explicit dependencies.
- You declare a module in `module-info.java`.

Example (minimal):

```java
module com.example.app {
  requires java.sql;
  exports com.example.app.api;
}
```

Practical tips:
- Many applications run fine on 17 without modularizing your own code.
- You still benefit from JDK internal encapsulation (fewer “illegal access”).

## 2) `var` for Local Variables (Java 10)

**Goal:** Reduce boilerplate while keeping static typing.

```java
import java.util.ArrayList;

public class VarDemo {
  public static void main(String[] args) {
    var list = new ArrayList<String>();
    list.add("hello");
    System.out.println(list.get(0));
  }
}
```

Rules:
- `var` is only for **local variables** (not fields, not method params).
- The inferred type is fixed at compile time.

## 3) Standard HTTP Client (Java 11)

`java.net.http.HttpClient` replaces the old, awkward `HttpURLConnection`.

```java
import java.net.URI;
import java.net.http.*;

public class HttpClientDemo {
  public static void main(String[] args) throws Exception {
    HttpClient client = HttpClient.newHttpClient();
    HttpRequest request = HttpRequest.newBuilder(URI.create("https://example.com"))
        .GET()
        .build();

    HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
    System.out.println(response.statusCode());
  }
}
```

## 4) Text Blocks (Java 15)

**Goal:** Multi-line strings without ugly escaping.

```java
public class TextBlocks {
  public static void main(String[] args) {
    String json = """
      {
        "name": "Alice",
        "active": true
      }
      """;

    System.out.println(json);
  }
}
```

## 5) Switch Expressions (Java 14)

Switch can be an expression that returns a value.

```java
public class SwitchExpr {
  static int score(String grade) {
    return switch (grade) {
      case "A" -> 100;
      case "B" -> 80;
      case "C" -> 60;
      default -> 0;
    };
  }
}
```

Use `yield` for multi-statement arms.

## 6) Records (Java 16)

**Goal:** Concise, immutable data carriers.

```java
public class Records {
  public record Point(int x, int y) {}

  public static void main(String[] args) {
    Point p = new Point(1, 2);
    System.out.println(p.x() + "," + p.y());
  }
}
```

Records automatically generate:
- constructor
- accessors
- `equals`, `hashCode`, `toString`

## 7) Pattern Matching for `instanceof` (Java 16)

```java
public class InstanceofPattern {
  static int lengthIfString(Object o) {
    if (o instanceof String s) {
      return s.length();
    }
    return -1;
  }
}
```

## 8) Sealed Classes (Final in Java 17)

**Goal:** Restrict which classes can extend/implement a type.

```java
public class Sealed {
  public sealed interface Shape permits Circle, Rectangle {}

  public static final class Circle implements Shape {
    public final double r;
    public Circle(double r) { this.r = r; }
  }

  public static final class Rectangle implements Shape {
    public final double w, h;
    public Rectangle(double w, double h) { this.w = w; this.h = h; }
  }
}
```

This pairs well with exhaustive switches (especially in later Java versions).

## 9) Helpful NullPointerExceptions (Java 14)

When enabled by default (typical in Java 14+), the JVM points to the *exact* null dereference in chained calls, e.g. `a.b().c()`.

## 10) Garbage Collectors & Performance (9–17)

You don’t normally change code for these, but they matter:
- G1 GC became the default (Java 9+)
- Many JIT and runtime improvements
- Better container awareness (especially around memory limits)

## 11) Security & Packaging Changes You’ll Notice

- Strong encapsulation of JDK internals: old reflection hacks may break.
- Removed/deprecated components over time (e.g., applets are long gone; Nashorn removed in 15).

## Migration Checklist (Java 8 → 17)

- Update build tooling: Maven/Gradle plugins, CI images, and IDE settings.
- Replace removed APIs/flags (common pain: illegal reflective access, old `--add-opens` needs).
- Re-test TLS/crypto settings (older servers/ciphers can fail).
- Run with `--illegal-access=warn` on intermediate upgrades if needed.

## Practice Exercises

1. Convert a DTO class (fields + getters + `equals/hashCode`) into a `record`.
2. Use text blocks to embed JSON/SQL and write a small parser.
3. Model a closed hierarchy (e.g., `PaymentMethod`) using sealed types.
