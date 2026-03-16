# AWS SAM (Serverless Application Model) - Tài Liệu Học Tập

## Tổng Quan
AWS SAM là một framework để phát triển và triển khai các ứng dụng serverless. Nó đơn giản hóa quá trình xây dựng ứng dụng serverless bằng cách cung cấp:
- Cấu hình dưới định dạng YAML
- Tự động tạo các file CloudFormation phức tạp
- Khả năng debug ở local

## Tính Năng Chính

### 1. Framework SAM
- Viết code với cấu hình SAM YAML đơn giản
- SAM tự động tạo các file CloudFormation phức tạp
- Hỗ trợ tất cả tính năng CloudFormation: outputs, mappings, parameters, resources, v.v.

### 2. Tích Hợp Với Các Dịch Vụ AWS
- **CodeDeploy**: Triển khai Lambda functions ở hậu trường
- **Lambda**: Serverless compute
- **API Gateway**: RESTful APIs
- **DynamoDB**: Cơ sở dữ liệu NoSQL

### 3. Phát Triển Local
SAM cho phép chạy các dịch vụ sau ở local:
- Lambda functions
- API Gateway
- DynamoDB

## Cấu Trúc SAM Template

### Transform Header
```yaml
Transform: AWS::Serverless-2016-10-31
```
Header này cho biết đây là SAM template và yêu cầu CloudFormation chuyển đổi nó.

### SAM Constructs So Với CloudFormation
Thay vì dùng CloudFormation constructs, sử dụng các construct đặc biệt của SAM:

| SAM Construct | Dịch Vụ AWS | Mô Tả |
|--------------|-------------|-------|
| `AWS::Serverless::Function` | Lambda | Serverless function |
| `AWS::Serverless::Api` | API Gateway | RESTful API |
| `AWS::Serverless::SimpleTable` | DynamoDB | Bảng NoSQL |

## Quy Trình Triển Khai

### Triển Khai SAM Truyền Thống

1. **Build** - `sam build`
   - Chuyển đổi SAM template thành CloudFormation template
   - Chuẩn bị application code

2. **Deploy** - `sam deploy`
   - Nén và upload code lên S3 bucket
   - Thực thi CloudFormation ChangeSet
   - Tạo serverless stack (Lambda, API Gateway, DynamoDB)

**Lưu ý**: Trước đây cần hai lệnh (`sam package` và `sam deploy`), giờ chỉ cần `sam deploy`.

## SAM Accelerate

### Mục Đích
SAM Accelerate giảm độ trễ triển khai bằng cách cung cấp các tùy chọn triển khai nhanh hơn.

### Lệnh Chính
```bash
sam sync --watch
```

### Cách Hoạt Động
- Bỏ qua CloudFormation khi chỉ thay đổi code
- Sử dụng service APIs trực tiếp để cập nhật nhanh
- Theo dõi thay đổi file và tự động đồng bộ
- Lý tưởng để test Lambda functions trên cloud

### Các Tùy Chọn Triển Khai

| Lệnh | Mô Tả |
|------|-------|
| `sam sync` | Đồng bộ cả code và infrastructure |
| `sam sync --code` | Chỉ đồng bộ code (trong vài giây, không qua CloudFormation) |
| `sam sync --resource <ResourceID>` | Cập nhật Lambda function cụ thể |
| `sam sync --watch` | Theo dõi thay đổi file và tự động đồng bộ |

### Các Trường Hợp Sử Dụng
- **Test Code Nhanh**: Cập nhật Lambda code mà không cần triển khai CloudFormation đầy đủ
- **Quy Trình Phát Triển**: Watch mode để đồng bộ liên tục
- **Cập Nhật Có Chọn Lọc**: Chỉ cập nhật các function hoặc dependencies cụ thể

## Lợi Ích Của SAM

1. **Cấu Hình Đơn Giản**: Cú pháp YAML dễ dàng hơn so với CloudFormation thuần
2. **Phát Triển Nhanh Hơn**: Test và debug ở local
3. **Triển Khai Nhanh**: SAM Accelerate cho các vòng lặp phát triển nhanh
4. **Tương Thích CloudFormation**: Hỗ trợ đầy đủ các tính năng CloudFormation
5. **Tập Trung Serverless**: Được xây dựng chuyên biệt cho ứng dụng serverless

## Thực Hành Tốt Nhất

- Sử dụng `sam sync --watch` trong quá trình phát triển tích cực
- Sử dụng `sam deploy` cho triển khai production
- Test ở local trước khi triển khai lên AWS
- Tận dụng SAM constructs để có template sạch hơn
- Dùng option `--code` khi chỉ cập nhật Lambda code

## Tóm Tắt
AWS SAM là một framework mạnh mẽ giúp đơn giản hóa việc phát triển ứng dụng serverless bằng cách cung cấp các template đơn giản hơn, khả năng test local, và các tùy chọn triển khai nhanh thông qua SAM Accelerate. Nó lý tưởng cho việc xây dựng các ứng dụng dựa trên Lambda với API Gateway và DynamoDB.
