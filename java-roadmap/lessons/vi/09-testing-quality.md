# Bài 09 — Testing + bộ công cụ chất lượng

## Mục tiêu

Viết unit test với JUnit 5, hiểu mocking, và nắm toolbox tối thiểu (formatting, static analysis, logging).

## Khái niệm chính

- Unit test phải nhanh, ổn định, tập trung.
- Ưu tiên test hành vi thông qua public API.
- Mocking là công cụ, không phải mặc định.
- Logging: trong server app thường dùng SLF4J + Logback.

## Thực hành

### 1) Cấu trúc JUnit 5 (mô hình)

```java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class MathTest {
  @Test
  void add_twoNumbers() {
    assertEquals(4, 2 + 2);
  }
}
```

### 2) Test code của bạn

Chọn một class nhỏ (ví dụ `BankAccount`) và test:

- deposit tăng balance
- withdraw throw khi không đủ tiền

### 3) Khi nào cần mock

Mock “biên” ngoài:

- thời gian (`Clock`)
- random
- network call
- filesystem

Với domain logic thuần, ưu tiên object thật.

## Checklist

- Viết và chạy được JUnit test.
- Giải thích được khi nào mock hữu ích.
- Biết vì sao test không nên phụ thuộc thứ tự/thời gian.

## Lỗi thường gặp

- Test phản chiếu implementation (dễ vỡ khi refactor).
- Over-mock và “test mock”.
- Trộn unit test với integration test mà không tách bạch.

## Tiếp theo

Build tool: làm project chạy lặp lại được (dependency, build, test).
