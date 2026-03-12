# AWS IAM Roles

## Giới Thiệu

IAM Roles là thành phần chính cuối cùng của AWS Identity and Access Management (IAM). Chúng cung cấp một cách an toàn để cấp quyền cho các dịch vụ AWS thực hiện các hành động thay mặt bạn trong tài khoản AWS của bạn.

## IAM Roles Là Gì?

IAM Roles tương tự như IAM Users ở chỗ cả hai đều có các chính sách quyền (permissions policies) được gán cho chúng. Tuy nhiên, có một sự khác biệt cơ bản:

- **IAM Users:** Dành cho con người thực tế cần truy cập tài nguyên AWS
- **IAM Roles:** Dành cho các dịch vụ AWS cần thực hiện các hành động thay mặt bạn

## Tại Sao Chúng Ta Cần IAM Roles?

Các dịch vụ AWS mà bạn khởi chạy trong hành trình điện toán đám mây của mình sẽ cần thực hiện nhiều hành động khác nhau trên tài khoản của bạn. Giống như người dùng, các dịch vụ này cần quyền để thực thi các hành động này. IAM Roles cung cấp một cơ chế an toàn để gán các quyền này cho dịch vụ AWS mà không cần nhúng thông tin xác thực.

## Cách Hoạt Động Của IAM Roles

Khi một dịch vụ AWS cần truy cập tài nguyên AWS:

1. Bạn tạo một IAM Role với các quyền cụ thể
2. Bạn gán role này cho dịch vụ AWS
3. Dịch vụ và role cùng nhau tạo thành một thực thể
4. Khi dịch vụ cố gắng truy cập tài nguyên AWS, nó sử dụng IAM Role
5. Nếu role có quyền chính xác, API call sẽ thành công

### Quy Trình Ví Dụ

Hãy xem xét một EC2 Instance (máy chủ ảo trong AWS):

```
EC2 Instance + IAM Role → Truy cập Tài nguyên AWS
```

1. Bạn tạo một EC2 Instance
2. Bạn gán một IAM Role với các quyền cụ thể cho instance
3. EC2 Instance giờ có thể thực hiện các hành động trên AWS dựa trên quyền của role
4. Nếu chính sách quyền đúng, instance sẽ truy cập thành công các tài nguyên AWS cần thiết

## Các Trường Hợp Sử Dụng Phổ Biến Cho IAM Roles

Trong hành trình AWS của bạn, bạn sẽ gặp một số kịch bản phổ biến mà IAM Roles là thiết yếu:

### 1. EC2 Instance Roles
- Cho phép các máy chủ ảo EC2 truy cập các dịch vụ AWS khác
- Trường hợp sử dụng phổ biến nhất cho IAM Roles
- Ví dụ: EC2 instance truy cập S3 buckets hoặc DynamoDB tables

### 2. Lambda Function Roles
- Cho phép các hàm AWS Lambda tương tác với các dịch vụ AWS khác
- Bắt buộc cho các ứng dụng serverless

### 3. CloudFormation Roles
- Cho phép CloudFormation tạo và quản lý tài nguyên AWS thay mặt bạn
- Thiết yếu cho infrastructure as code

## Các Khái Niệm Chính

### Lợi Ích Về Bảo Mật
- **Không có thông tin xác thực hardcoded:** Dịch vụ không cần access keys nhúng trong code
- **Thông tin xác thực tạm thời:** Roles cung cấp security credentials tạm thời
- **Đặc quyền tối thiểu:** Chỉ gán quyền cần thiết cho nhiệm vụ

### Thực Hành Tốt Nhất
1. Tạo các role cụ thể cho các mục đích cụ thể
2. Tuân theo nguyên tắc đặc quyền tối thiểu (least privilege)
3. Thường xuyên xem xét và kiểm toán quyền của role
4. Sử dụng roles thay vì chia sẻ thông tin xác thực người dùng

## Bắt Đầu

Trong bài giảng tiếp theo, chúng ta sẽ thực hành các bước tạo IAM Role trong AWS Console. Mặc dù chúng ta sẽ tạo role, nhưng chúng ta sẽ chưa sử dụng nó ngay lập tức—nó sẽ trở nên hữu ích khi chúng ta bắt đầu làm việc với EC2 Instances trong phần tiếp theo.

## Tóm Tắt

- **IAM Roles** cấp quyền cho các dịch vụ AWS, không phải người dùng thực tế
- Các dịch vụ sử dụng roles để thực hiện các hành động trên tài khoản AWS của bạn
- Các ví dụ phổ biến bao gồm EC2 Instance Roles, Lambda Function Roles và CloudFormation Roles
- Roles cung cấp một cách an toàn để quản lý quyền dịch vụ mà không cần thông tin xác thực hardcoded
- Hiểu về roles là thiết yếu để xây dựng kiến trúc AWS an toàn

## Các Bước Tiếp Theo

Trong bài giảng sau, bạn sẽ học cách tạo IAM Role thông qua thực hành. Kiến thức nền tảng này sẽ rất quan trọng khi chúng ta tiến xa hơn trong khóa học và bắt đầu khởi chạy các dịch vụ AWS yêu cầu quyền dựa trên role.