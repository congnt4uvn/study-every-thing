# Ghi chú học AWS: Giám sát (Logs, Metrics, Tracing, Auditing)

Tài liệu này dựa trên ý trong `file.txt`: ứng dụng “chạy trên cloud” vẫn **có thể bị sập**, và nếu không bật giám sát thì lúc 2:00 sáng bạn khó trả lời câu hỏi **“đã xảy ra chuyện gì?”**.

## Vì sao giám sát quan trọng
- Giúp phát hiện sự cố sớm, giảm thời gian khôi phục.
- Cho bạn quan sát được **hệ thống đang làm gì** và **ai thay đổi gì** trong AWS.
- Biến thông báo “service down” thành tín hiệu + bằng chứng để xử lý.

## 4 trụ cột được nhắc trong nguồn
### 1) Logs (Nhật ký)
**Là gì:** Các bản ghi theo thời gian (log ứng dụng, log hệ thống, access log).

**Dùng để:**
- Debug lỗi, phân tích hành vi bất thường
- Tìm nguyên nhân gốc sau sự cố
- Điều tra bảo mật (kết hợp với audit)

**Dịch vụ AWS thường dùng:** Amazon **CloudWatch Logs**

### 2) Metrics (Chỉ số)
**Là gì:** Chuỗi số theo thời gian (CPU, latency, error rate, queue depth, …).

**Dùng để:**
- Theo dõi sức khỏe hệ thống và cảnh báo
- Lập kế hoạch năng lực
- Phát hiện suy giảm hiệu năng

**Dịch vụ AWS thường dùng:** Amazon **CloudWatch Metrics** (+ **Alarms**)

### 3) Tracing (Theo vết)
**Là gì:** Theo dõi luồng xử lý request xuyên qua nhiều dịch vụ (tốn thời gian ở đâu, call nào lỗi).

**Dùng để:**
- Debug hệ thống phân tán / microservices
- Tìm nút thắt cổ chai hoặc dependency chậm

**Dịch vụ AWS thường dùng:** AWS **X-Ray**

### 4) Auditing (Ghi vết/Audit)
**Là gì:** Ghi lại hành động trong tài khoản AWS (API call, thao tác console), trả lời “ai làm gì, khi nào, từ đâu.”

**Dùng để:**
- Tuân thủ (compliance) và quản trị
- Ứng cứu sự cố bảo mật
- Truy vết thay đổi gây outage (deploy/config/IAM)

**Dịch vụ AWS thường dùng:** AWS **CloudTrail**

## Checklist thực tế (tối giản nhưng hiệu quả)
- Gom log tập trung (đẩy log ứng dụng vào CloudWatch Logs).
- Xác định metric cốt lõi (latency, tỉ lệ 4xx/5xx, mức bão hòa tài nguyên).
- Tạo CloudWatch alarm cho các metric này và gửi thông báo (thường qua Amazon SNS).
- Bật tracing cho các luồng quan trọng (X-Ray) và truyền trace ID.
- Bật CloudTrail (tốt nhất là toàn tổ chức) để ghi nhận hoạt động API.

## Những câu hỏi “2:00 a.m.” cần trả lời được
- Error rate/latency có tăng đột biến không? (metrics)
- Có log lỗi gì quanh thời điểm sự cố? (logs)
- Call xuống dịch vụ nào bị chậm/bị lỗi? (tracing)
- Có ai thay đổi cấu hình/deploy/IAM ngay trước đó không? (auditing)

## Tự kiểm tra nhanh
1) Trụ cột nào trả lời “ai thay đổi gì trong AWS?”
2) Trụ cột nào tốt nhất để tìm dependency chậm trong microservices?
3) Hãy nêu 3 ví dụ metric bạn sẽ đặt alarm cho một web API.
