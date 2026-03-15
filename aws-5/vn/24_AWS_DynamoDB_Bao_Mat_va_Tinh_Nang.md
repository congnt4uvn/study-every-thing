# AWS DynamoDB - Hướng Dẫn Học Về Bảo Mật và Tính Năng

## Tổng Quan
Tài liệu này bao gồm các tính năng bảo mật và khả năng thiết yếu của Amazon DynamoDB, một dịch vụ cơ sở dữ liệu NoSQL được quản lý hoàn toàn trong AWS.

## Tính Năng Bảo Mật

### 1. VPC Endpoints (Điểm Cuối VPC)
- **Mục đích**: Truy cập DynamoDB mà không cần sử dụng internet công cộng
- **Lợi ích**: Toàn bộ lưu lượng truy cập được giữ trong VPC để tăng cường bảo mật
- **Trường hợp sử dụng**: Kết nối riêng tư, an toàn đến DynamoDB từ VPC của bạn

### 2. Kiểm Soát Truy Cập qua IAM
- **Tích hợp IAM đầy đủ**: Truy cập DynamoDB được kiểm soát hoàn toàn bởi IAM
- **Quyền chi tiết**: Định nghĩa các quyền cụ thể cho người dùng và vai trò
- **Thực hành tốt nhất**: Làm cho nó trở thành lựa chọn cơ sở dữ liệu tuyệt vời trong môi trường AWS

### 3. Mã Hóa
- **Khi lưu trữ**: Sử dụng AWS KMS (Key Management Service)
- **Khi truyền tải**: Được bảo mật bằng giao thức SSL/TLS
- **Tuân thủ**: Đáp ứng các yêu cầu bảo mật và tuân thủ

## Sao Lưu và Khôi Phục

### Point-in-Time Recovery (PITR - Khôi Phục Tại Thời Điểm)
- Tương tự như chức năng PITR của RDS
- **Không ảnh hưởng đến hiệu suất** trong quá trình sao lưu
- Bật sao lưu liên tục cho khôi phục thảm họa

### Sao Lưu và Khôi Phục Tiêu Chuẩn
- Tạo các bản sao lưu theo yêu cầu
- Khôi phục bảng về bất kỳ thời điểm nào

## Global Tables (Bảng Toàn Cầu)

### Sao Chép Đa Vùng
- **Đa vùng**: Triển khai trên nhiều vùng AWS
- **Đa hoạt động**: Sao chép hoạt động-hoạt động (active-active)
- **Sao chép hoàn toàn**: Dữ liệu được đồng bộ hóa trên tất cả các vùng
- **Hiệu suất cao**: Truy cập độ trễ thấp trên toàn cầu

### Điều Kiện Tiên Quyết
- Phải bật **DynamoDB Streams** trước
- Streams ghi lại các thay đổi cấp độ mục để sao chép

## DynamoDB Local (DynamoDB Cục Bộ)

### Công Cụ Phát Triển
- **Mục đích**: Mô phỏng DynamoDB cục bộ
- **Lợi ích**:
  - Phát triển và kiểm tra ứng dụng cục bộ
  - Không cần kết nối đến dịch vụ AWS
  - Tiết kiệm chi phí cho phát triển
  - Khả năng phát triển ngoại tuyến

## Di Chuyển Dữ Liệu

### AWS Database Migration Service (DMS)
- Di chuyển dữ liệu **đến** và **từ** DynamoDB
- **Nguồn/Đích được hỗ trợ**:
  - MongoDB ↔ DynamoDB
  - DynamoDB ↔ Oracle
  - DynamoDB ↔ MySQL
  - DynamoDB ↔ S3
  - Và nhiều hơn nữa...

## Kiểm Soát Truy Cập Chi Tiết (Fine-Grained Access Control)

### Trường Hợp Sử Dụng
- Ứng dụng web và di động cần truy cập trực tiếp vào DynamoDB
- **Vấn đề**: Không muốn tạo người dùng IAM riêng cho từng khách hàng
- **Giải pháp**: Sử dụng định danh liên kết với thông tin xác thực tạm thời

### Nhà Cung Cấp Định Danh
- Amazon Cognito User Pools
- Google Login
- Facebook Login
- OpenID Connect
- SAML
- Các nhà cung cấp định danh khác

### Luồng Xác Thực
1. Người dùng đăng nhập thông qua nhà cung cấp định danh
2. Trao đổi thông tin xác thực để nhận **thông tin xác thực AWS tạm thời**
3. Thông tin xác thực tạm thời an toàn hơn
4. Thông tin xác thực được liên kết với vai trò IAM bị hạn chế

### Kiểm Soát Truy Cập Cấp Độ Hàng

#### Sử Dụng Điều Kiện LeadingKeys
```json
{
  "Effect": "Allow",
  "Action": [
    "dynamodb:GetItem",
    "dynamodb:BatchGetItem",
    "dynamodb:Query",
    "dynamodb:PutItem",
    "dynamodb:UpdateItem",
    "dynamodb:DeleteItem",
    "dynamodb:BatchWriteItem"
  ],
  "Resource": "arn:aws:dynamodb:region:account:table/TableName",
  "Condition": {
    "ForAllValues:StringEquals": {
      "dynamodb:LeadingKeys": [
        "${cognito-identity.amazonaws.com:sub}"
      ]
    }
  }
}
```

**Điểm Chính**:
- LeadingKeys hạn chế quyền truy cập ở **cấp độ hàng**
- Người dùng chỉ có thể truy cập/sửa đổi dữ liệu khi khóa chính khớp với định danh của họ
- `${cognito-identity.amazonaws.com:sub}` được thay thế khi chạy bằng ID người dùng thực tế

### Kiểm Soát Truy Cập Cấp Độ Cột

#### Sử Dụng Điều Kiện Thuộc Tính
- Chỉ định điều kiện trên **thuộc tính**
- Giới hạn cột (thuộc tính) nào người dùng có thể xem
- Cung cấp bảo mật cấp độ thuộc tính

## Tóm Tắt

### Triển Khai Kiểm Soát Truy Cập Chi Tiết
1. **Đăng nhập Liên kết**: Sử dụng nhà cung cấp định danh để xác thực
2. **Thông tin xác thực tạm thời**: Trao đổi để nhận thông tin xác thực AWS tạm thời
3. **Vai trò IAM bị hạn chế**: Áp dụng điều kiện để giới hạn quyền truy cập
4. **Điều kiện LeadingKeys**: Để kiểm soát truy cập cấp độ hàng
5. **Điều kiện Thuộc tính**: Để kiểm soát truy cập cấp độ cột

### Thực Hành Tốt Nhất về Bảo Mật
- ✅ Sử dụng VPC endpoints cho kết nối riêng tư
- ✅ Triển khai chính sách IAM với đặc quyền tối thiểu
- ✅ Bật mã hóa khi lưu trữ và truyền tải
- ✅ Sử dụng kiểm soát truy cập chi tiết cho ứng dụng khách
- ✅ Bật PITR cho khôi phục thảm họa
- ✅ Sử dụng DynamoDB Local cho phát triển/kiểm tra

## Điểm Chính Cần Nhớ
- DynamoDB cung cấp các tính năng bảo mật cấp doanh nghiệp
- Kiểm soát truy cập chi tiết cho phép truy cập trực tiếp an toàn của khách hàng
- Global tables cung cấp khả năng sẵn sàng cao đa vùng
- Nhiều tùy chọn sao lưu đảm bảo độ bền của dữ liệu
- DMS tạo điều kiện thuận lợi cho việc di chuyển dữ liệu dễ dàng

---
*Cập nhật lần cuối: 15 Tháng 3, 2026*
