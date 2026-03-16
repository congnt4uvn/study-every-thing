# AWS: So sánh SSM Parameter Store với Secrets Manager

## Tổng quan
Hướng dẫn này đề cập đến những khác biệt giữa AWS Systems Manager (SSM) Parameter Store và Secrets Manager, bao gồm các tính năng, trường hợp sử dụng và khả năng xoay vòng bí mật.

## Những khác biệt chính

### Secrets Manager
**Chi phí:** Đắt hơn so với Parameter Store

**Tính năng:**
- Xoay vòng bí mật tự động sử dụng Lambda Functions
- Nhiều Lambda Functions được cung cấp sẵn cho các dịch vụ
- Tích hợp mạnh mẽ với các dịch vụ AWS:
  - Amazon RDS
  - Amazon Redshift
  - Document DB
- Mã hóa KMS bắt buộc cho tất cả bí mật
- Tích hợp CloudFormation có sẵn

**Trường hợp sử dụng:** Tốt nhất để quản lý thông tin xác thực nhạy cảm cần xoay vòng tự động

---

### SSM Parameter Store
**Chi phí:** Rẻ hơn so với Secrets Manager

**Tính năng:**
- Phạm vi sử dụng rộng (tham số và bí mật)
- API đơn giản
- Không có xoay vòng bí mật gốc (nhưng có thể triển khai thủ công)
- Mã hóa KMS tùy chọn
- Tích hợp CloudFormation có sẵn
- Có thể tham chiếu Bí mật từ Secrets Manager bằng API Parameter Store

**Trường hợp sử dụng:** Tốt nhất để lưu trữ tham số cấu hình và bí mật đơn giản với yêu cầu chi phí thấp

---

## Xoay vòng Bí mật

### Xoay vòng Secrets Manager
Khi xoay vòng một bí mật (ví dụ: mật khẩu cơ sở dữ liệu Amazon RDS):

1. Thiết lập Secrets Manager để tự động gọi Lambda Function
2. Khoảng thời gian xoay vòng mặc định: Mỗi 30 ngày
3. AWS cung cấp các Lambda Functions được xây dựng sẵn cho các dịch vụ phổ biến (RDS, Redshift, v.v.)
4. Những Lambda Functions này tự động thay đổi mật khẩu trong các dịch vụ tích hợp
5. Không cần mã tùy chỉnh cho các tích hợp gốc

---

### Xoay vòng Parameter Store
Không giống như Secrets Manager, Parameter Store không có tính năng xoay vòng gốc.

**Triển khai thủ công:**
1. Tạo quy tắc Amazon EventBridge
2. Kích hoạt theo lịch trình đã định (tương tự khoảng thời gian 30 ngày)
3. Sử dụng Lambda Function tùy chỉnh để xoay vòng bí mật thủ công
4. Tài liệu AWS được cung cấp cho triển khai tùy chỉnh

**Lưu ý:** Nếu sử dụng mật khẩu RDS trong Parameter Store, cần sử dụng phương pháp EventBridge + Lambda

---

## Tóm tắt

| Tính năng | Secrets Manager | Parameter Store |
|-----------|-----------------|-----------------|
| Chi phí | Cao hơn | Thấp hơn |
| Xoay vòng gốc | Có (30 ngày) | Không |
| Mã hóa KMS | Bắt buộc | Tùy chọn |
| Trường hợp sử dụng | Thông tin xác thực nhạy cảm | Phạm vi rộng |
| Tích hợp sẵn | Có | Không |
| Xoay vòng tùy chỉnh | Lambda thủ công | Lambda tùy chỉnh + EventBridge |

Chọn **Secrets Manager** để quản lý bí mật tự động với tích hợp AWS mạnh mẽ.
Chọn **Parameter Store** cho cấu hình chung và các kịch bản tối ưu chi phí.
