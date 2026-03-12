# Chuỗi Cung Cấp Thông Tin Xác Thực AWS

## Tổng Quan

Chuỗi Cung Cấp Thông Tin Xác Thực AWS (AWS Credentials Provider Chain) là một khái niệm quan trọng xác định thứ tự mà AWS CLI và SDK tìm kiếm thông tin xác thực. Hiểu rõ chuỗi này rất quan trọng cho việc cấu hình bảo mật AWS đúng cách và khắc phục sự cố.

## Thứ Tự Chuỗi Thông Tin Xác Thực CLI

Khi bạn sử dụng AWS CLI, nó sẽ tìm kiếm thông tin xác thực theo thứ tự ưu tiên sau:

1. **Tùy Chọn Dòng Lệnh** (Ưu tiên cao nhất)
   - Region (vùng)
   - Output format (định dạng đầu ra)
   - Profile (hồ sơ)
   - Access Key ID
   - Secret Access Key
   - Session Token

2. **Biến Môi Trường**
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_SESSION_TOKEN`

3. **File Thông Tin Xác Thực CLI**
   - Được cấu hình qua `aws configure`
   - Nằm tại `~/.aws/credentials`

4. **File Cấu Hình CLI**
   - Nằm tại `~/.aws/config`

5. **Thông Tin Xác Thực Container**
   - Được sử dụng cho ECS tasks

6. **Thông Tin Xác Thực EC2 Instance Profile** (Ưu tiên thấp nhất)
   - IAM role được gán cho EC2 instances

## Thứ Tự Chuỗi Thông Tin Xác Thực SDK

Đối với AWS SDK (ví dụ: Java SDK), thứ tự ưu tiên tương tự:

1. **System Properties** (ví dụ: Java system properties)
2. **Biến Môi Trường**
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
3. **File Profile Thông Tin Xác Thực Mặc Định**
4. **Thông Tin Xác Thực Amazon ECS Container**
5. **Thông Tin Xác Thực EC2 Instance Profile**

## Kịch Bản Phổ Biến: Vấn Đề Ưu Tiên Chuỗi Thông Tin Xác Thực

### Vấn Đề

Xem xét kịch bản này:

1. Bạn triển khai một ứng dụng trên EC2 instance
2. Ứng dụng sử dụng **biến môi trường** với thông tin xác thực IAM user để gọi Amazon S3 API
3. Thông tin xác thực IAM user này có quyền **S3 FullAccess** (truy cập tất cả S3 buckets)
4. Tuân theo best practices, bạn tạo một IAM role với **quyền tối thiểu** (chỉ truy cập một S3 bucket cụ thể)
5. Bạn gán IAM role này cho EC2 instance thông qua instance profile
6. **Vấn đề**: Ứng dụng vẫn có quyền truy cập tất cả S3 buckets!

### Tại Sao Điều Này Xảy Ra?

Chuỗi thông tin xác thực ưu tiên **biến môi trường cao hơn** so với thông tin xác thực EC2 instance profile. Mặc dù bạn đã gán instance profile với quyền hạn chế, nhưng biến môi trường vẫn đang được sử dụng.

### Giải Pháp

**Xóa bỏ (unset) các biến môi trường** trên EC2 instance. Sau khi xóa, chuỗi thông tin xác thực sẽ chuyển sang sử dụng thông tin xác thực EC2 instance profile, có quyền hạn chế đúng cách.

## Best Practices Về Thông Tin Xác Thực

### ❌ Không Bao Giờ Làm Điều Này

- **KHÔNG BAO GIỜ lưu thông tin xác thực trong code**
- Đây là thực hành cực kỳ tệ và là rủi ro bảo mật lớn

### ✅ Best Practices

1. **Kế thừa thông tin xác thực từ chuỗi thông tin xác thực**
2. **Trong AWS**: Sử dụng IAM roles càng nhiều càng tốt
   - EC2 Instance Roles cho EC2 instances
   - ECS Task Roles cho ECS tasks
   - Lambda Execution Roles cho Lambda functions
3. **Bên ngoài AWS**: Sử dụng biến môi trường hoặc named profiles
   - Cấu hình qua AWS CLI: `aws configure`
   - Sử dụng named profiles cho nhiều tài khoản

## Điểm Chính Cần Nhớ

- Chuỗi cung cấp thông tin xác thực tuân theo thứ tự ưu tiên cụ thể
- Biến môi trường có ưu tiên cao hơn instance profiles
- Luôn sử dụng IAM roles khi làm việc trong AWS
- Không bao giờ hardcode thông tin xác thực trong code ứng dụng
- Hiểu rõ chuỗi thông tin xác thực là cần thiết để khắc phục sự cố xác thực

## Mẹo Thi Cử

- Nắm vững thứ tự ưu tiên của chuỗi thông tin xác thực
- Hiểu các câu hỏi kịch bản phổ biến về xung đột thông tin xác thực
- Nhớ rằng biến môi trường ghi đè thông tin xác thực instance profile
- Biết các best practices về quản lý thông tin xác thực trong AWS