# 05) Ngoại lệ & I/O (41–50)

## 41. Cây phân cấp exception trong Java?

**Đáp:** `Throwable` → (`Error`, `Exception`). `RuntimeException` là nhánh unchecked của `Exception`.

## 42. Khi nào nên tạo custom exception?

**Đáp:** Khi cần biểu diễn lỗi theo domain để caller xử lý rõ ràng (vd `InvalidOrderStateException`). Thường ưu tiên unchecked trừ khi caller thực sự có thể phục hồi.

## 43. Try-with-resources hoạt động thế nào?

**Đáp:** Tự động đóng resource implement `AutoCloseable`.

```java
try (BufferedReader br = Files.newBufferedReader(path)) {
    return br.readLine();
}
```

Nếu body và close đều ném lỗi, lỗi ở close sẽ bị **suppressed**.

## 44. `IOException` vs `FileNotFoundException`?

**Đáp:** `FileNotFoundException` là một `IOException` cụ thể, thường xảy ra khi mở file không tồn tại hoặc không có quyền.

## 45. NIO (`java.nio`) là gì, vì sao dùng?

**Đáp:** API hiện đại: `Path`, `Files`, channel/buffer; tiện và hiệu quả cho nhiều tác vụ (vd `Files.walk`, `Files.readString`).

## 46. `InputStream` vs `Reader`?

**Đáp:**
- `InputStream`: byte.
- `Reader`: char (giải mã theo charset).

Text dùng `Reader`, binary dùng `InputStream`.

## 47. Chọn charset an toàn thế nào?

**Đáp:** Luôn chỉ định rõ (vd `StandardCharsets.UTF_8`) thay vì phụ thuộc default của hệ thống.

## 48. Serialization là gì, rủi ro?

**Đáp:** Java serialization chuyển object ↔ bytes. Rủi ro: bảo mật (gadget chain), khó versioning, coupling ngầm. Với API, ưu tiên JSON/Protobuf + schema rõ.

## 49. Khác nhau giữa `throw new RuntimeException(e)` và `throw e`?

**Đáp:** Wrap đổi loại exception và “hình dạng” stacktrace; `throw e` giữ nguyên loại. Wrap có thể thêm ngữ cảnh nhưng có thể làm mất thông tin loại checked.

## 50. Exception chaining là gì?

**Đáp:** Giữ exception gốc làm cause.

```java
throw new IllegalStateException("Không tải được cấu hình", e);
```
