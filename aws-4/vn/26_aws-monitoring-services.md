# Các Dịch Vụ Giám Sát và Kiểm Toán AWS

## Tổng Quan
Tài liệu này so sánh ba dịch vụ AWS quan trọng: CloudTrail, CloudWatch và X-Ray. Hiểu rõ sự khác biệt giữa các dịch vụ này là điều cần thiết để giám sát và gỡ lỗi hiệu quả trên AWS.

---

## CloudTrail - Kiểm Toán API

### Mục Đích
CloudTrail được thiết kế để **kiểm toán các lệnh gọi API** được thực hiện trong tài khoản AWS của bạn.

### Tính Năng Chính
- Theo dõi các lệnh gọi API được thực hiện bởi:
  - Người dùng
  - Các dịch vụ
  - AWS Console
- Ghi lại toàn bộ hoạt động API để quản trị và tuân thủ

### Trường Hợp Sử Dụng
- Phát hiện các lệnh gọi API không được ủy quyền
- Tìm nguyên nhân gốc rễ của các thay đổi do lệnh gọi API
- Phân tích bảo mật và kiểm toán tuân thủ
- Theo dõi ai đã làm gì và khi nào

### Chức Năng Chính
**Kiểm toán và ghi lại hoạt động API**

---

## CloudWatch - Giám Sát

### Mục Đích
CloudWatch là dịch vụ **giám sát** toàn diện của AWS.

### Các Thành Phần

#### CloudWatch Metrics (Chỉ Số)
- Giám sát hiệu suất tài nguyên và ứng dụng
- Theo dõi các chỉ số cấp hệ thống (CPU, bộ nhớ, đĩa, mạng)
- Chỉ số tùy chỉnh cho ứng dụng

#### CloudWatch Logs (Nhật Ký)
- Lưu trữ và phân tích nhật ký ứng dụng
- Quản lý nhật ký tập trung
- Tìm kiếm và lọc dữ liệu nhật ký

#### CloudWatch Alarms (Cảnh Báo)
- Gửi thông báo dựa trên ngưỡng chỉ số
- Kích hoạt các hành động tự động
- Cảnh báo về các chỉ số bất thường

### Trường Hợp Sử Dụng
- Giám sát hiệu suất ứng dụng và hạ tầng
- Thiết lập cảnh báo cho các bất thường
- Theo dõi việc sử dụng tài nguyên
- Lưu trữ và phân tích nhật ký

### Chức Năng Chính
**Giám sát chỉ số và ghi nhật ký tổng thể**

---

## X-Ray - Truy Vết Phân Tán

### Mục Đích
X-Ray cung cấp **phân tích truy vết tự động** và **trực quan hóa sơ đồ dịch vụ** cho các hệ thống phân tán.

### Tính Năng Chính
- Truy vết các yêu cầu qua các dịch vụ phân tán
- Sơ đồ dịch vụ trực quan hiển thị các phụ thuộc
- Phân tích hiệu suất chi tiết
- Theo dõi yêu cầu từ đầu đến cuối

### Trường Hợp Sử Dụng
- Gỡ lỗi các ứng dụng phân tán
- Phân tích vấn đề về độ trễ
- Xác định lỗi và sự cố
- Hiểu luồng yêu cầu qua các microservices
- Tối ưu hóa hiệu suất

### Chức Năng Chính
**Gỡ lỗi và phân tích chi tiết theo hướng truy vết**

---

## So Sánh Nhanh

| Dịch Vụ | Mục Đích Chính | Lĩnh Vực Tập Trung |
|---------|----------------|-------------------|
| **CloudTrail** | Kiểm toán lệnh gọi API | Bảo mật & Tuân thủ |
| **CloudWatch** | Giám sát chỉ số & nhật ký | Hiệu suất & Sức khỏe |
| **X-Ray** | Truy vết yêu cầu phân tán | Gỡ lỗi & Độ trễ |

---

## Tóm Tắt

- **CloudTrail**: Sử dụng khi bạn cần biết "ai đã làm gì" - kiểm toán các lệnh gọi API
- **CloudWatch**: Sử dụng để giám sát tổng thể - các chỉ số, nhật ký và cảnh báo
- **X-Ray**: Sử dụng để gỡ lỗi chi tiết - truy vết yêu cầu và phân tích độ trễ

Mỗi dịch vụ phục vụ một mục đích riêng biệt trong hệ sinh thái AWS và chúng thường hoạt động cùng nhau để cung cấp khả năng quan sát toàn diện cho các ứng dụng của bạn.
