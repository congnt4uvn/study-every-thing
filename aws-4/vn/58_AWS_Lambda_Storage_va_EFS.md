# AWS Lambda Storage và Tích hợp EFS

## Gắn kết File System với Lambda

### Tổng quan
Các hàm Lambda có thể truy cập hệ thống file EFS (Elastic File System) khi chạy trong VPC. Điều này cung cấp bộ nhớ lưu trữ liên tục và chia sẻ cho các ứng dụng serverless.

### Yêu cầu Cấu hình
Để gắn kết hệ thống file EFS vào hàm Lambda:
- Cấu hình Lambda để gắn kết hệ thống file EFS vào thư mục local trong quá trình khởi tạo
- Sử dụng tính năng **EFS Access Points**
- Triển khai các hàm Lambda trong **Private Subnet** có kết nối đến VPC

### Kiến trúc
```
EFS File System
    ↓
EFS Access Point
    ↓
Lambda Function (Private Subnet) → VPC
```

### Hạn chế
- **Giới hạn Kết nối**: Mỗi instance Lambda tạo một kết nối đến hệ thống file EFS
  - Cần giám sát để tránh đạt đến giới hạn kết nối EFS
- **Giới hạn Burst**: Nhiều hàm Lambda khởi động đồng thời có thể đạt đến giới hạn connection burst

---

## So sánh các Tùy chọn Lưu trữ Lambda

### 1. Ephemeral Storage (/tmp)

| Thuộc tính | Chi tiết |
|------------|----------|
| **Kích thước Tối đa** | 10 GB |
| **Tính Liên tục** | Ephemeral (tạm thời - mất khi function instance bị hủy) |
| **Nội dung** | Dynamic (có thể chỉnh sửa) |
| **Loại** | File system với đầy đủ các thao tác file system |
| **Chi phí** | Miễn phí đến 512 MB, trả thêm cho dung lượng vượt quá |
| **Truy cập** | Chỉ một function (không chia sẻ) |
| **Hiệu suất** | Mức độ truy xuất dữ liệu nhanh nhất |
| **Chia sẻ** | Không chia sẻ giữa các lần gọi function |

**Trường hợp Sử dụng**: Lưu trữ tạm thời cho việc thực thi function, tải xuống hoặc xử lý các file tạm thời.

### 2. Lambda Layers

| Thuộc tính | Chi tiết |
|------------|----------|
| **Kích thước Tối đa** | 5 layers mỗi function, tổng cộng 250 MB (trong giới hạn kích thước package) |
| **Tính Liên tục** | Bền vững (không thể thay đổi - immutable) |

**Trường hợp Sử dụng**: Chia sẻ code chung, thư viện hoặc dependencies cho nhiều hàm Lambda.

---

## Điểm Chính Cần Nhớ

1. **Tích hợp EFS** cung cấp lưu trữ liên tục và chia sẻ cho các hàm Lambda
2. **Access Points** là bắt buộc cho tích hợp Lambda-EFS
3. **Cấu hình VPC** là bắt buộc để truy cập EFS
4. **Quản lý Kết nối** rất quan trọng để tránh đạt giới hạn
5. **Lưu trữ /tmp** nhanh nhưng tạm thời
6. **Lambda Layers** không thể thay đổi và có thể tái sử dụng cho nhiều functions

---

## Best Practices (Thực hành Tốt nhất)

- Sử dụng EFS cho dữ liệu liên tục, chia sẻ giữa nhiều lần gọi Lambda
- Sử dụng /tmp cho xử lý tạm thời trong một lần gọi duy nhất
- Sử dụng Lambda Layers cho code và dependencies được chia sẻ
- Giám sát số lượng kết nối EFS khi mở rộng quy mô
- Cân nhắc các mẫu burst khi thiết kế kiến trúc
