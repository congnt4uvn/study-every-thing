# 10) Test, Build & Best practice (91–100)

## 91. JUnit 5 khác JUnit 4 ở điểm chính nào?

**Đáp:** JUnit 5 modular (`junit-jupiter`), extension model mạnh hơn, hỗ trợ tốt hơn cho parameterized test; package annotation `@Test` khác.

## 92. Unit test vs integration test?

**Đáp:**
- Unit: test nhỏ, cô lập (thường dùng fake/mock).
- Integration: test tương tác thật giữa thành phần (DB/FS/HTTP), chậm hơn nhưng tăng độ tin cậy.

## 93. Mocking là gì, khi nào nên tránh?

**Đáp:** Mock thay dependency bằng test double. Tránh mock quá sâu vào chi tiết nội bộ; ưu tiên mock boundary bên ngoài và test behavior.

## 94. Maven vs Gradle?

**Đáp:**
- Maven: declarative XML, convention rõ, ổn định.
- Gradle: DSL linh hoạt, incremental build tốt hơn trong nhiều case.

## 95. Semantic versioning là gì, vì sao quan trọng?

**Đáp:** `MAJOR.MINOR.PATCH`. MAJOR = breaking; MINOR = thêm tính năng tương thích; PATCH = sửa lỗi. Giúp quản lý dependency và nâng cấp an toàn.

## 96. Vì sao `null` dễ gây vấn đề, thay thế bằng gì?

**Đáp:** `null` dẫn tới NPE và hợp đồng mơ hồ. Thay thế: `Optional` (return), empty collection, Null Object, validation.

## 97. SOLID là gì (ngắn gọn)?

**Đáp:** 5 nguyên lý thiết kế: SRP, OCP, LSP, ISP, DIP.

## 98. Thiết kế code dễ test trong Java như thế nào?

**Đáp:** Constructor injection, tránh global `static` state, phụ thuộc interface, gom side-effect ở rìa (I/O), tách logic thuần khỏi hạ tầng.

## 99. `System.currentTimeMillis()` vs `System.nanoTime()`?

**Đáp:**
- `currentTimeMillis`: wall-clock (có thể nhảy).
- `nanoTime`: monotonic, phù hợp đo duration.

## 100. Các “pitfall” hiệu năng phổ biến trong Java service?

**Đáp:** Tạo quá nhiều object (GC pressure), I/O blocking trên request thread, lock contention, cache/queue không giới hạn, log chatty, thiếu timeout/retry.
