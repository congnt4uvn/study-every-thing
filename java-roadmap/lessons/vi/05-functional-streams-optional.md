# Bài 05 — Lambda, Streams, Optional

## Mục tiêu

Viết code xử lý dữ liệu gọn hơn bằng lambda và stream, và xử lý “có thể thiếu” bằng `Optional`.

## Khái niệm chính

- Lambda: coi hàm như một giá trị.
- Stream: pipeline xử lý collection.
- Ưu tiên hàm “thuần” trong stream (tránh side effect).
- `Optional<T>` thể hiện “có thể không có” rõ ràng.

## Thực hành

### 1) Lambda và functional interface

```java
java.util.function.Predicate<String> nonBlank = s -> s != null && !s.isBlank();
System.out.println(nonBlank.test("hi"));
```

### 2) Pipeline với stream

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

### 3) Grouping và counting

```java
var words = java.util.List.of("a", "bb", "c", "dd", "eee");

var countsByLength = words.stream()
  .collect(java.util.stream.Collectors.groupingBy(
    String::length,
    java.util.stream.Collectors.counting()
  ));

System.out.println(countsByLength);
```

### 4) Optional: giảm null check

```java
static java.util.Optional<String> findUserEmail(java.util.Map<String, String> emails, String userId) {
  return java.util.Optional.ofNullable(emails.get(userId));
}

var emails = java.util.Map.of("u1", "u1@example.com");

String email = findUserEmail(emails, "u2")
  .orElse("unknown@example.com");
```

## Checklist

- Viết được stream pipeline với `map/filter/sorted/collect`.
- Giải thích được khi nào nên dùng stream (và khi nào loop rõ hơn).
- Dùng `Optional` có chủ đích.

## Lỗi thường gặp

- Lạm dụng stream cho bài toán đơn giản (đọc khó hơn).
- Dùng `Optional` làm field khắp nơi (thường hợp lý nhất là return value).
- Side effect trong `map()`.

## Tiếp theo

I/O và tích hợp: file, JSON, và gọi HTTP.
