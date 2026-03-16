# AWS Step Functions: Các loại workflow (Tài liệu học)

## 1) Tổng quan
AWS Step Functions có **3 lựa chọn workflow**:

1. **Standard Workflow** (mặc định)
2. **Express Workflow - Asynchronous**
3. **Express Workflow - Synchronous**

---

## 2) Standard Workflow

### Đặc điểm chính
- Thời gian chạy tối đa: **tối đa 1 năm**
- Mô hình thực thi: **exactly-once**
- Thông lượng: khoảng **2.000 executions/giây**
- Lịch sử execution trên console: tối đa **90 ngày**
- Lưu log dài hạn: dùng **CloudWatch Logs** và cấu hình retention

### Cách tính phí
- Tính theo **số lần chuyển trạng thái (state transitions)**
  - State transition là khi workflow chuyển từ state này sang state khác.

### Trường hợp sử dụng điển hình
- Phù hợp với tác vụ **không idempotent**, ví dụ:
  - Xử lý thanh toán

---

## 3) Express Workflow (Tổng quát)

### Đặc điểm chính
- Thời gian chạy tối đa: **tối đa 5 phút**
- Khả năng mở rộng rất cao: **hơn 100.000 executions/giây**
- Không theo dõi chi tiết execution trên console như Standard
- Quan sát kết quả chủ yếu qua **CloudWatch Logs**

### Cách tính phí
- Tính theo:
  - Số lần execution
  - Thời lượng execution
  - Mức dùng bộ nhớ

### Trường hợp sử dụng điển hình
- Nạp dữ liệu IoT
- Xử lý dữ liệu streaming
- Backend/mobile API lưu lượng lớn

---

## 4) Express Asynchronous và Synchronous

## 4.1 Express Asynchronous
- Gọi workflow xong trả về nhanh; bên gọi **không chờ** kết quả cuối
- Cam kết thực thi: **at least once**
- Nếu lỗi, Step Functions có thể tự retry
- Vì retry, có thể xảy ra xử lý trùng lặp
- Cần thiết kế action theo hướng **idempotent**

### Khi nào nên dùng
- Khi không cần phản hồi ngay lập tức
- Ví dụ: gửi message/event kiểu fire-and-forget

## 4.2 Express Synchronous
- Bên gọi chờ workflow chạy xong rồi nhận kết quả
- Cam kết thực thi: **at most once**
- Nếu lỗi, Step Functions **không tự khởi động lại** workflow
- Logic retry do ứng dụng của bạn tự xử lý

### Khi nào nên dùng
- Khi cần kết quả ngay để phản hồi cho client
- Ví dụ: điều phối microservices sau API Gateway hoặc Lambda

---

## 5) Bảng so sánh nhanh

| Tiêu chí | Standard | Express Async | Express Sync |
|---|---|---|---|
| Thời gian tối đa | Tối đa 1 năm | Tối đa 5 phút | Tối đa 5 phút |
| Cam kết thực thi | Exactly-once | At least once | At most once |
| Thông lượng | ~2.000/giây | 100.000+/giây | 100.000+/giây |
| Có chờ kết quả không | Có (luồng thông thường) | Không | Có |
| Phù hợp nhất | Luồng dài, độ tin cậy cao, tác vụ không idempotent | Sự kiện lưu lượng lớn, fire-and-forget | Request/response thời gian thực |
| Cách tính phí | Theo state transitions | Theo số lần chạy + thời lượng + bộ nhớ | Theo số lần chạy + thời lượng + bộ nhớ |

---

## 6) Điểm cần nhớ cho ôn thi
- **Standard = exactly-once, chạy dài (tối đa 1 năm)**
- **Express = chạy ngắn (tối đa 5 phút), scale rất lớn**
- **Async Express = at least once**
- **Sync Express = at most once**
- Với Async có retry, luôn kiểm tra tính **idempotent**

---

## 7) Câu hỏi tự kiểm tra
1. Vì sao xử lý thanh toán thường phù hợp với Standard workflow?
2. Tại sao Async Express có thể gây tác dụng lặp nếu action không idempotent?
3. Nếu API caller cần nhận kết quả ngay, nên dùng loại nào?
4. Khác biệt về cách tính phí giữa Standard và Express là gì?
