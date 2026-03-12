# Những điểm mới trong Java 21 (LTS) (Bài học)

Java 21 (2023) là bản LTS và mang lại nâng cấp rất lớn về concurrency, đặc biệt là **virtual threads**. Ngoài ra, pattern matching cho `switch` đã hoàn thiện và collections có thêm API mới.

Bài này tập trung vào các tính năng Java 21 quan trọng nhất trong thực tế.

## 1) Virtual Threads (JEP 444) — Chính thức

**Vấn đề:** Platform thread tốn tài nguyên; server nhiều kết nối thường phải dùng async.

**Giải pháp:** Virtual thread là thread “nhẹ”, do JVM quản lý.

```java
import java.util.concurrent.*;

public class VirtualThreadsDemo {
  public static void main(String[] args) throws Exception {
    try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
      Future<String> f = executor.submit(() -> {
        Thread.sleep(100);
        return "done";
      });
      System.out.println(f.get());
    }
  }
}
```

Gợi ý:
- Phù hợp với code theo kiểu **blocking I/O** (HTTP, JDBC, v.v.).
- Vẫn cần chú ý các chỗ block không “park” tốt (một số native call).

## 2) Structured Concurrency (JEP 453) — Preview

**Mục tiêu:** Gom nhiều tác vụ chạy song song thành một “đơn vị công việc”: chạy cùng nhau, huỷ cùng nhau, fail cùng nhau.

Tính năng **preview** trong Java 21; cần `--enable-preview`.

## 3) Scoped Values (JEP 446) — Preview

Scoped values là lựa chọn an toàn hơn cho một số trường hợp dùng `ThreadLocal`, đặc biệt khi có virtual threads.

Cũng là **preview** trong Java 21.

## 4) Pattern Matching cho `switch` (JEP 441) — Chính thức

Switch hỗ trợ type pattern và guard (`when`).

```java
public class SwitchPatterns {
  static String describe(Object o) {
    return switch (o) {
      case null -> "null";
      case Integer i -> "int " + i;
      case String s when s.isBlank() -> "chuỗi rỗng/blank";
      case String s -> "chuỗi '" + s + "'";
      default -> "loại khác";
    };
  }
}
```

## 5) Record Patterns (JEP 440) — Chính thức

Cho phép “bóc tách” record ngay trong pattern.

```java
public class RecordPatterns {
  record Point(int x, int y) {}

  static String quadrant(Point p) {
    return switch (p) {
      case Point(int x, int y) when x >= 0 && y >= 0 -> "Q1";
      case Point(int x, int y) when x < 0 && y >= 0 -> "Q2";
      case Point(int x, int y) when x < 0 && y < 0 -> "Q3";
      case Point(int x, int y) -> "Q4";
    };
  }
}
```

## 6) Sequenced Collections (JEP 431) — Chính thức

Thêm API thống nhất cho collections có thứ tự (encounter order).

Interface mới:
- `SequencedCollection<E>`
- `SequencedSet<E>`
- `SequencedMap<K, V>`

Method tiêu biểu:
- `getFirst()`, `getLast()`
- `addFirst(E)`, `addLast(E)`
- `removeFirst()`, `removeLast()`
- `reversed()`

## 7) Unnamed Patterns & Variables (JEP 443) — Preview

Cho phép bỏ qua giá trị không cần dùng bằng `_`.

**Preview** trong Java 21.

## 8) String Templates (JEP 430) — Preview

String templates là tính năng **preview** trong Java 21 (có thể thay đổi ở phiên bản sau).

## 9) Foreign Function & Memory (FFM) API (JEP 442) — Preview

API hiện đại để gọi native code và thao tác off-heap, thay thế dần cho JNI.

**Preview** trong Java 21.

## 10) Hiệu năng & runtime

- Generational ZGC (JEP 439)
- Nhiều cải tiến JIT/runtime

## Cách compile/run preview

- Compile: `javac --release 21 --enable-preview YourFile.java`
- Run: `java --enable-preview YourMainClass`

## Checklist nâng cấp (Java 17 → 21)

- Kiểm tra lại framework/library có hỗ trợ bytecode level 21.
- Cân nhắc có dùng preview trong production hay không.
- Benchmark nếu muốn áp dụng virtual threads cho service I/O-heavy.

## Bài tập

1. Chuyển code dùng executor sang `newVirtualThreadPerTaskExecutor()`.
2. Thay chuỗi `instanceof` phức tạp bằng `switch` pattern matching.
3. Dùng `getFirst()`/`getLast()` cho code rõ nghĩa hơn.
