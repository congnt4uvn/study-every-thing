# Những điểm mới trong Java 8 (Bài học)

Java 8 (2014) là một bước ngoặt lớn khi Java chuyển mạnh sang phong cách **lập trình hàm**. Rất nhiều dự án hiện đại vẫn dựa trên các khái niệm của Java 8, nên đây là nền tảng quan trọng.

## 1) Biểu thức Lambda

**Mục tiêu:** Truyền “hành vi” (đoạn code) như một giá trị.

Trong Java 8, bạn có thể dùng lambda với **functional interface** (interface chỉ có đúng 1 phương thức trừu tượng).

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

Ghi nhớ:
- Lambda chỉ capture biến “effectively final”.
- Lambda không tạo scope `this` mới như anonymous class.

## 2) Method Reference

Method reference là cú pháp rút gọn cho các lambda đơn giản.

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

Các dạng phổ biến:
- `ClassName::staticMethod`
- `instance::instanceMethod`
- `ClassName::instanceMethod` (đối tượng nhận trở thành tham số đầu)
- `ClassName::new`

## 3) Streams API

**Mục tiêu:** Viết pipeline xử lý dữ liệu theo kiểu khai báo (declarative).

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

Khái niệm quan trọng:
- Stream **lazy**: intermediate operation chỉ chạy khi có terminal operation.
- Ưu tiên hàm stateless và không can thiệp vào nguồn dữ liệu.
- `parallelStream()` có thể giúp tăng tốc nhưng không phải lúc nào cũng hiệu quả.

## 4) Default/Static Method trong Interface

Java 8 cho phép interface “tiến hoá” mà không làm vỡ các class implement.

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

Quy tắc:
- Method của class luôn ưu tiên hơn default method của interface.
- Nếu hai interface có cùng default method, bạn phải tự resolve.

## 5) Functional Interfaces (`java.util.function`)

Các interface hay dùng:
- `Predicate<T>`: `T -> boolean`
- `Function<T, R>`: `T -> R`
- `Supplier<T>`: `() -> T`
- `Consumer<T>`: `T -> void`

Ví dụ:

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

**Mục tiêu:** Biểu diễn rõ ràng giá trị “có thể không tồn tại”.

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

Khuyến nghị:
- Không nên lạm dụng `Optional` cho field trong model nếu team chưa thống nhất.
- Tránh `get()` trực tiếp nếu chưa chắc chắn có giá trị.

## 7) API Ngày/Giờ mới (`java.time`)

API mới immutable, rõ ràng hơn `Date/Calendar`.

```java
import java.time.*;

public class TimeApi {
  public static void main(String[] args) {
    LocalDate today = LocalDate.now();
    LocalDate payday = LocalDate.of(2026, 3, 31);

    Period until = Period.between(today, payday);
    System.out.println("Số ngày đến payday: " + until.getDays());

    Instant now = Instant.now();
    System.out.println("Epoch millis: " + now.toEpochMilli());
  }
}
```

## 8) `CompletableFuture`

**Mục tiêu:** Kết hợp các tác vụ async theo chuỗi.

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

## 9) Một số bổ sung hữu ích

- Base64: `java.util.Base64`
- Cải tiến collections: `forEach`, `removeIf`, `replaceAll`, `computeIfAbsent`
- `Arrays.parallelSort` (và các hàm parallel khác)

## Gợi ý nâng cấp (Pre-8 → 8)

- Áp dụng stream dần dần, đừng “stream hoá” mọi thứ.
- Dùng `java.time` thay cho `Date/Calendar`.
- Hiểu rõ `map` vs `flatMap` trong stream/Optional.

## Bài tập

1. Chuyển một đoạn `for` filter + map sang stream.
2. Viết chuỗi `CompletableFuture` có xử lý lỗi (`exceptionally`).
3. Refactor utility dùng `Date` sang `java.time`.
