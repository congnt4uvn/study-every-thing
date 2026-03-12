# 09) Module, Reflection & Java hiện đại (81–90)

## 81. Java module system (JPMS) là gì?

**Đáp:** Từ Java 9, JPMS tổ chức code thành module với dependency rõ ràng và encapsulation mạnh qua `module-info.java`.

## 82. `requires` và `exports` trong `module-info.java` nghĩa là gì?

**Đáp:**
- `requires`: module này phụ thuộc module khác.
- `exports`: công khai package cho module khác dùng.

## 83. Vì sao reflection có thể “hỏng” ở Java mới?

**Đáp:** Encapsulation mạnh có thể chặn “illegal reflective access”. Thư viện cần khai báo module đúng hoặc cấu hình hợp lệ; tránh lạm dụng JVM flag.

## 84. Reflection là gì, dùng khi nào hợp lý?

**Đáp:** Reflection cho phép inspect/invoke class/method lúc runtime. Hợp lý cho framework (DI, serialization), nhưng đổi lại: chậm hơn, kém type-safety, khó refactor.

## 85. Annotation là gì, dùng ra sao?

**Đáp:** Metadata gắn vào code. Nếu retention là `RUNTIME`, framework có thể đọc qua reflection.

## 86. `@Retention(SOURCE|CLASS|RUNTIME)` khác nhau?

**Đáp:**
- `SOURCE`: bỏ sau compile.
- `CLASS`: có trong bytecode nhưng không nhất thiết có ở runtime.
- `RUNTIME`: có thể đọc ở runtime.

## 87. Sealed class/interface là gì?

**Đáp:** Giới hạn những type nào được phép extend/implement.

```java
public sealed interface Shape permits Circle, Rectangle {}
```

## 88. Pattern matching cho `instanceof` giải quyết gì?

**Đáp:** Giảm boilerplate cast.

```java
if (obj instanceof String s) {
    System.out.println(s.length());
}
```

## 89. Text block (`"""`) là gì?

**Đáp:** Literal chuỗi nhiều dòng, giảm escape, hữu ích cho JSON/SQL.

## 90. Virtual thread (Project Loom) là gì (khái niệm)?

**Đáp:** Thread nhẹ do JVM quản lý, giúp xử lý rất nhiều tác vụ đồng thời theo kiểu “thread-per-task” nhưng ít tốn OS thread hơn.
