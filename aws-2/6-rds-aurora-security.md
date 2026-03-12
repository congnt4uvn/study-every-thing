# Bảo Mật RDS và Aurora

## Tổng Quan

Hướng dẫn này bao gồm các tính năng bảo mật và các phương pháp tốt nhất cho cơ sở dữ liệu AWS RDS (Relational Database Service) và Amazon Aurora.

## Mã Hóa Dữ Liệu Lưu Trữ (Encryption at Rest)

Bạn có thể mã hóa dữ liệu lưu trữ trên cơ sở dữ liệu RDS và Aurora, có nghĩa là dữ liệu được mã hóa trên các ổ đĩa.

### Các Điểm Chính:

- **Master và Replicas**: Cả cơ sở dữ liệu master và bất kỳ read replica nào đều được mã hóa bằng AWS KMS (Key Management Service)
- **Cấu Hình Khi Khởi Tạo**: Mã hóa phải được xác định tại thời điểm khởi chạy trong lần khởi chạy đầu tiên của cơ sở dữ liệu
- **Hạn Chế Quan Trọng**: Nếu cơ sở dữ liệu master không được mã hóa, các read replica cũng không thể được mã hóa

### Mã Hóa Cơ Sở Dữ Liệu Chưa Được Mã Hóa

Để mã hóa một cơ sở dữ liệu chưa được mã hóa hiện có:

1. Tạo một snapshot từ cơ sở dữ liệu chưa được mã hóa
2. Khôi phục snapshot đó thành một cơ sở dữ liệu đã được mã hóa

Lưu ý: Bạn phải thực hiện qua quá trình snapshot và restore để kích hoạt mã hóa cho cơ sở dữ liệu hiện có.

## Mã Hóa Trong Quá Trình Truyền Tải (In-Flight Encryption)

Cơ sở dữ liệu RDS và Aurora hỗ trợ mã hóa trong quá trình truyền tải giữa client và cơ sở dữ liệu.

### Cấu Hình:

- Mỗi cơ sở dữ liệu trên RDS và Aurora đều sẵn sàng có mã hóa trong quá trình truyền tải **theo mặc định**
- Client phải sử dụng chứng chỉ gốc TLS từ AWS (được cung cấp trên trang web AWS)

## Xác Thực Cơ Sở Dữ Liệu

RDS và Aurora hỗ trợ nhiều phương thức xác thực:

### 1. Username và Password
Phương pháp xác thực cổ điển sử dụng thông tin đăng nhập username và password.

### 2. Xác Thực IAM Roles
- Bạn có thể sử dụng IAM roles để kết nối đến cơ sở dữ liệu
- Ví dụ: Các EC2 instance có IAM roles có thể xác thực trực tiếp đến cơ sở dữ liệu
- Lợi ích: Loại bỏ nhu cầu quản lý username và password
- Giúp quản lý tất cả bảo mật trong AWS và IAM

## Kiểm Soát Truy Cập Mạng

### Security Groups

Bạn có thể kiểm soát quyền truy cập mạng vào cơ sở dữ liệu bằng security groups:

- Cho phép hoặc chặn các cổng cụ thể
- Cho phép hoặc chặn các địa chỉ IP cụ thể
- Cho phép hoặc chặn các security group cụ thể

### Truy Cập SSH

- RDS và Aurora **không có quyền truy cập SSH** vì chúng là các dịch vụ được quản lý
- Ngoại lệ: Dịch vụ RDS Custom từ AWS có cung cấp quyền truy cập SSH

## Nhật Ký Kiểm Toán (Audit Logs)

### Mục Đích
Audit Logs giúp bạn theo dõi các truy vấn đang được thực hiện trên RDS và Aurora theo thời gian và giám sát các hoạt động cơ sở dữ liệu.

### Cấu Hình:

1. Kích hoạt Audit Logs trên cơ sở dữ liệu RDS hoặc Aurora
2. Lưu ý: Audit logs sẽ bị mất sau một khoảng thời gian

### Lưu Trữ Dài Hạn

Để giữ audit logs trong thời gian dài:

- Gửi chúng đến dịch vụ **CloudWatch Logs** trên AWS
- Điều này đảm bảo logs được lưu giữ và có thể phân tích theo thời gian

## Tóm Tắt

RDS và Aurora cung cấp các tùy chọn bảo mật toàn diện bao gồm:

- ✅ Mã hóa dữ liệu lưu trữ sử dụng KMS
- ✅ Mã hóa trong quá trình truyền tải sử dụng TLS
- ✅ Nhiều phương thức xác thực (username/password và IAM roles)
- ✅ Kiểm soát truy cập mạng qua security groups
- ✅ Ghi nhật ký kiểm toán với tích hợp CloudWatch Logs
- ❌ Không có quyền truy cập SSH (dịch vụ được quản lý)

Các tính năng bảo mật này giúp bạn bảo vệ cơ sở dữ liệu và duy trì tuân thủ các phương pháp tốt nhất về bảo mật.