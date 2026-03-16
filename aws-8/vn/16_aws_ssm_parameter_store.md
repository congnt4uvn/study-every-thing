# AWS SSM Parameter Store - Hướng Dẫn Học Tập

## Tổng Quan

AWS Systems Manager (SSM) Parameter Store là một giải pháp lưu trữ an toàn để quản lý cấu hình và bí mật trên các ứng dụng và hạ tầng AWS của bạn.

## Các Tính Năng Chính

### 1. **Lưu Trữ An Toàn**
- Lưu trữ cấu hình và bí mật một cách an toàn
- Mã hóa tùy chọn bằng AWS KMS (Key Management Service)
- Dữ liệu được mã hóa cả khi đang lưu trữ lẫn khi truyền tải

### 2. **Không Máy Chủ & Có Thể Mở Rộng**
- Dịch vụ được quản lý hoàn toàn (không cần quản lý hạ tầng)
- Tự động mở rộng theo nhu cầu của bạn
- Lưu trữ bền vững với tính mô dự dự được tích hợp sẵn

### 3. **Tích Hợp Dễ Dàng**
- SDK đơn giản cho nhà phát triển sử dụng
- Tích hợp đầy đủ với AWS CloudFormation
- CloudFormation có thể sử dụng các tham số làm đầu vào cho các stack

### 4. **Theo Dõi Phiên Bản**
- Tự động ghi phiên bản khi cập nhật tham số
- Dễ dàng quay lại các phiên bản trước đó
- Theo dõi lịch sử thay đổi tham số

### 5. **Bảo Mật & Giám Sát**
- Kiểm soát truy cập thông qua IAM (Identity and Access Management)
- Thông báo qua Amazon EventBridge
- Dấu vết kiểm toán của tất cả quyền truy cập và sửa đổi tham số

## Phân Cấp & Tổ Chức Tham Số

Các tham số có thể được tổ chức theo cấu trúc phân cấp bằng cách sử dụng các đường dẫn:

```
/my-department/
  ├── my-app/
  │   ├── /dev/
  │   │   ├── DB-URL
  │   │   └── DB-password
  │   └── /prod/
  │       ├── DB-URL
  │       └── DB-password
  └── another-app/
      ...
```

Phương pháp có cấu trúc này:
- Tổ chức tham số một cách hợp lý
- Đơn giản hóa quản lý chính sách IAM
- Cho phép ứng dụng truy cập toàn bộ phòng ban hoặc các đường dẫn cụ thể

## Loại Tham Số

### 1. **Cấu Hình Văn Bản Thường**
- Tham số không được mã hóa
- Phù hợp cho cấu hình không nhạy cảm
- Truy xuất nhanh hơn

### 2. **Cấu Hình Được Mã Hóa (Bí Mật)**
- Được mã hóa bằng KMS
- Yêu cầu quyền khóa KMS cho ứng dụng
- Phù hợp cho dữ liệu nhạy cảm như mật khẩu, khóa API

## Cách Thức Hoạt Động

1. **Ứng dụng yêu cầu tham số** từ Parameter Store
2. **Kiểm tra quyền IAM** để xác minh quyền truy cập
3. **Nếu được mã hóa:** Dịch vụ KMS xử lý giải mã
4. **Tham số được truy xuất** và trả về cho ứng dụng

### Yêu Cầu Truy Cập
- Ứng dụng phải có quyền IAM để truy cập Parameter Store
- Đối với các tham số được mã hóa, ứng dụng cần quyền truy cập khóa KMS
- Các trường hợp phổ biến: vai trò EC2 instance, vai trò thực thi Lambda, vai trò tác vụ ECS

## Các Trường Hợp Sử Dụng

- Thông tin xác thực cơ sở dữ liệu
- Khóa API và token
- Cấu hình ứng dụng
- Cờ tính năng (Feature flags)
- Khóa cấp phép
- Cài đặt theo từng môi trường

## Các Thực Hành Tốt Nhất

1. Sử dụng đặt tên phân cấp cho tổ chức
2. Mã hóa dữ liệu nhạy cảm bằng KMS
3. Sử dụng chính sách IAM để hạn chế quyền truy cập theo đường dẫn
4. Bật theo dõi phiên bản cho mục đích kiểm toán
5. Sử dụng EventBridge để nhận thông báo về thay đổi tham số
6. Định kỳ kiểm tra quyền truy cập tham số
7. Thực hiện nguyên tắc đặc quyền tối thiểu trong chính sách IAM

## Truy Xuất Với IAM

Bằng cách tổ chức các tham số theo cấu trúc phân cấp, bạn có thể cấp quyền ở các cấp độ khác nhau:
- Cấp quyền truy cập toàn bộ đường dẫn `/my-department/`
- Hoặc hạn chế quyền truy cập đường dẫn cụ thể `/my-department/my-app/dev/`
- Điều này giúp đơn giản hóa đáng kể quản lý quyền
