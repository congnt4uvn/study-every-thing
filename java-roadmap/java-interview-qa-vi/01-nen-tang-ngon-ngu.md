# 01) Nền tảng ngôn ngữ (1–10)

## 1. Java là gì, và vì sao gọi là “đa nền tảng”?

**Đáp:** Mã Java biên dịch ra **bytecode** (`.class`). Bytecode chạy trên **JVM** của từng hệ điều hành/CPU. Do đó cùng một bytecode có thể chạy ở nhiều nơi miễn có JVM phù hợp.

## 2. JDK vs JRE vs JVM khác nhau thế nào?

**Đáp:**
- **JVM**: chạy bytecode (GC, JIT, runtime).
- **JRE**: JVM + thư viện chuẩn để chạy ứng dụng.
- **JDK**: JRE + công cụ phát triển (ví dụ `javac`, `jar`, `javadoc`, `jcmd`).

## 3. Kiểu nguyên thủy (primitive) trong Java là gì? Kể tên.

**Đáp:** 8 kiểu: `byte`, `short`, `int`, `long`, `float`, `double`, `char`, `boolean`. Đây là kiểu giá trị, không phải object.

## 4. Autoboxing/unboxing là gì?

**Đáp:** Tự động chuyển đổi giữa primitive và wrapper.

```java
Integer x = 10; // boxing (int -> Integer)
int y = x;     // unboxing (Integer -> int)
```

Cẩn thận `NullPointerException` khi unbox `null`.

## 5. `==` và `.equals()` khác gì?

**Đáp:**
- `==`: so sánh **giá trị** (primitive) hoặc **tham chiếu** (object có cùng instance không).
- `.equals()`: so sánh **bằng nhau về mặt logic** (có thể override).

## 6. `static` dùng để làm gì?

**Đáp:** `static` thuộc về **class**, không thuộc về từng object.
- Field `static`: trạng thái dùng chung (cẩn thận concurrency/test).
- Method `static`: hàm tiện ích không cần state instance.
- Static block: khởi tạo một lần khi class được load.

## 7. Phân biệt `final`, `finally`, `finalize()`.

**Đáp:**
- `final`: không gán lại (biến), không override (method), không kế thừa (class).
- `finally`: khối chạy sau `try` (kể cả có exception).
- `finalize()`: cơ chế cũ liên quan GC; đã deprecated, nên tránh.

## 8. Java truyền tham số theo kiểu gì (pass-by-value)?

**Đáp:** Java **luôn** pass-by-value.
- Primitive: copy giá trị.
- Object: copy **giá trị tham chiếu** (hai biến trỏ cùng object).

## 9. Các access modifier và phạm vi của chúng?

**Đáp:**
- `private`: trong class.
- (package-private): không ghi gì; trong package.
- `protected`: trong package + subclass (có quy tắc).
- `public`: mọi nơi.

## 10. Interface và abstract class khác nhau thế nào?

**Đáp:**
- **Interface**: hợp đồng; có thể có `default`/`static`; hỗ trợ đa kế thừa kiểu.
- **Abstract class**: dùng cho chia sẻ implement/state; chỉ đơn kế thừa.
