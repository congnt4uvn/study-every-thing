# Bảo Mật AWS API Gateway

## Tổng Quan
Tài liệu này đề cập đến các tùy chọn bảo mật có sẵn cho AWS API Gateway, bao gồm các cơ chế xác thực và phân quyền.

## Các Tùy Chọn Bảo Mật Chính

### 1. Phân Quyền IAM
- **Vị trí**: Method Request → Phần Authorization
- **Mục đích**: Sử dụng IAM policies để kiểm soát quyền truy cập vào API của bạn
- **Trường hợp sử dụng**: Kiểm soát người dùng/vai trò IAM nào có thể gọi các phương thức API
- **Triển khai**: Bật phân quyền IAM ở cấp độ phương thức

### 2. Resource Policies (Chính Sách Tài Nguyên)
- **Mục đích**: Định nghĩa các chính sách để kiểm soát quyền truy cập vào toàn bộ API của bạn
- **Tính năng chính**:
  - Truy cập xuyên tài khoản
  - Kiểm soát truy cập dựa trên IP
  - Kiểm soát truy cập dựa trên VPC

#### Các Mẫu Resource Policy Phổ Biến

##### Danh Sách Cho Phép Tài Khoản AWS
- Cho phép các tài khoản, người dùng hoặc vai trò khác từ các tài khoản khác gọi API của bạn
- Kích hoạt truy cập xuyên tài khoản vào API Gateway

##### Danh Sách Từ Chối Theo Dải IP
- Cho phép hoặc từ chối các địa chỉ/dải IP cụ thể
- Hữu ích để hạn chế truy cập dựa trên vị trí mạng

##### Danh Sách Cho Phép Theo VPC Nguồn
- Tạo API Gateway riêng tư
- API chỉ có thể truy cập từ bên trong VPC cụ thể
- Tăng cường bảo mật cho các API nội bộ

### 3. Authorizers (Bộ Phân Quyền)
Thay thế cho phân quyền IAM với hai loại chính:

#### Lambda Authorizer
- **Kiểm soát tối đa**: Cung cấp tính linh hoạt cao nhất
- **Yêu cầu cấu hình**:
  - Triển khai hàm Lambda
  - IAM role (có thể cần)
  - Cấu hình event payload
  - Cài đặt caching cho kết quả phân quyền
- **Lợi ích**: Caching cải thiện hiệu suất bằng cách tránh gọi authorizer nhiều lần

#### Cognito User Pool Authorizer
- **Thiết lập đơn giản hơn**: Ít cấu hình hơn
- **Mục đích**: Xác thực yêu cầu bằng Amazon Cognito
- **Cấu hình**: Chỉ định Cognito User Pool nào sẽ sử dụng
- **Lợi ích**: Xác thực và quản lý người dùng tích hợp sẵn

## Thực Hành Tốt Nhất
1. Chọn phương pháp phân quyền phù hợp dựa trên trường hợp sử dụng của bạn
2. Bật caching cho Lambda authorizers để cải thiện hiệu suất
3. Sử dụng resource policies cho các kịch bản truy cập xuyên tài khoản
4. Triển khai hạn chế IP khi có thể áp dụng
5. Sử dụng danh sách cho phép VPC cho các API nội bộ/riêng tư

## Khi Nào Nên Sử Dụng Từng Phương Pháp

| Phương Pháp | Phù Hợp Nhất Cho |
|-------------|------------------|
| Phân Quyền IAM | Giao tiếp giữa các dịch vụ AWS |
| Lambda Authorizer | Logic phân quyền tùy chỉnh, token của bên thứ ba |
| Cognito User Pool | Ứng dụng người dùng với xác thực chuẩn |
| Resource Policies | Truy cập xuyên tài khoản, hạn chế IP, cô lập VPC |

## Tóm Tắt
AWS API Gateway cung cấp nhiều lớp bảo mật có thể kết hợp để tạo ra một chiến lược phân quyền mạnh mẽ. Hiểu rõ từng tùy chọn giúp bạn triển khai tư thế bảo mật phù hợp cho API của mình.
