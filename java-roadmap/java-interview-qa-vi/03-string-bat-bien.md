# 03) String & Bất biến (21–30)

## 21. Vì sao `String` là immutable?

**Đáp:** Để chia sẻ an toàn, hỗ trợ string pool/intern, cache hashCode, và tăng an toàn bảo mật (giá trị không thể bị thay đổi ngầm).

## 22. String pool (interning) là gì?

**Đáp:** JVM giữ một pool các `String` chuẩn hóa. Literal string được intern sẵn.

```java
String a = "hi";
String b = "hi";
System.out.println(a == b); // true
```

## 23. `new String("x")` khác gì `"x"`?

**Đáp:** `"x"` dùng instance interned; `new String("x")` tạo object mới (thường không cần thiết).

## 24. `StringBuilder` vs `StringBuffer`?

**Đáp:**
- `StringBuilder`: nhanh, không synchronized (phổ biến).
- `StringBuffer`: synchronized (legacy), hiếm khi cần.

## 25. Vì sao nối chuỗi trong vòng lặp thường chậm?

**Đáp:** Vì `String` immutable; mỗi lần `+=` tạo object mới. Dùng `StringBuilder`.

```java
StringBuilder sb = new StringBuilder();
for (String p : parts) sb.append(p);
String s = sb.toString();
```

## 26. `equalsIgnoreCase` làm gì và không làm gì?

**Đáp:** So sánh không phân biệt hoa/thường theo quy tắc chuẩn (không phải sắp xếp/so khớp theo locale phức tạp). Với sorting theo ngôn ngữ, dùng `Collator`.

## 27. Defensive copy là gì?

**Đáp:** Copy dữ liệu mutable khi nhận/ trả ra để bảo vệ bất biến.

```java
public Date getCreatedAt() { return new Date(createdAt.getTime()); }
```

Ưu tiên `Instant`/`LocalDateTime` thay vì `Date`.

## 28. Làm sao thiết kế một class immutable?

**Đáp:**
- Class `final` (hoặc kiểm soát override).
- Field `private final`.
- Không có setter.
- Validate trong constructor.
- Defensive copy với input/output mutable.

## 29. `record` là gì, dùng khi nào?

**Đáp:** `record` là data carrier bất biến, cú pháp ngắn.

```java
public record Point(int x, int y) {}
```

Dùng cho DTO/value object khi “identity” chính là state.

## 30. `String.format` và `printf` khác nhau?

**Đáp:** `String.format` trả về chuỗi; `printf` in ra stream. `format` thường tốn chi phí hơn nối chuỗi đơn giản với trường hợp nhỏ.
