# AWS Copilot - Hướng Dẫn Bắt Đầu

## Tổng Quan

Hướng dẫn này sẽ giúp bạn thiết lập và triển khai ứng dụng đầu tiên bằng AWS Copilot CLI. AWS Copilot là giao diện dòng lệnh giúp đơn giản hóa việc xây dựng, phát hành và vận hành các ứng dụng container sẵn sàng cho production trên Amazon ECS và AWS Fargate.

## Yêu Cầu Trước Khi Bắt Đầu

Trước khi bắt đầu, hãy đảm bảo bạn đã cài đặt các công cụ sau:

- **AWS CLI** - Giao diện dòng lệnh cho các dịch vụ AWS
- **Docker Desktop** - Nền tảng container để xây dựng và chạy ứng dụng
- **AWS Copilot CLI** - Công cụ chúng ta sẽ sử dụng trong hướng dẫn này

## Cài Đặt AWS Copilot

1. Truy cập trang tài liệu AWS Copilot
2. Chọn phương thức cài đặt phù hợp với nền tảng của bạn:
   - macOS
   - Linux
   - Windows

3. Sau khi cài đặt, kiểm tra xem công cụ đã hoạt động chưa:
   ```bash
   copilot --help
   ```

## Hướng Dẫn Từng Bước

### 1. Clone Repository Mẫu

Clone repository mẫu từ AWS chứa ứng dụng tương thích với Copilot:

```bash
git clone [URL repository AWS samples]
cd example
```

Repository này bao gồm Dockerfile và các cấu hình cần thiết để triển khai ứng dụng container.

### 2. Khởi Tạo Copilot

Bắt đầu quá trình khởi tạo Copilot:

```bash
copilot init
```

Bạn sẽ được yêu cầu cung cấp một số thông tin cấu hình:

#### Tên Ứng Dụng
Nhập tên cho ứng dụng của bạn:
```
example-app
```

#### Loại Service
Chọn loại triển khai từ các tùy chọn có sẵn:

- **Request-driven web service** - Sử dụng AWS App Runner
- **Load balanced web service** - Sử dụng Application Load Balancer (ALB) công khai với ECS trên Fargate
- **Backend service** - Service riêng tư với load balancer tùy chọn
- **Worker service** - Kiến trúc SQS tới ECS trên Fargate
- **Static site** - Để lưu trữ nội dung tĩnh
- **Scheduled job** - Cho các tác vụ định kỳ giống cron

Trong hướng dẫn này, chọn: **Load balanced web service**

#### Tên Service
Đặt tên cho service của bạn:
```
front-end
```

#### Chọn Dockerfile
Copilot sẽ phát hiện Dockerfile trong thư mục của bạn. Xác nhận để sử dụng nó.

### 3. Cấu Hình Môi Trường

Khi được hỏi về môi trường:

1. Nhập tên môi trường: `test`
2. Copilot sẽ tạo môi trường test nếu nó chưa tồn tại
3. Xác nhận triển khai bằng cách nhấn `y`

### 4. Quá Trình Triển Khai

Copilot bây giờ sẽ:

1. Tạo AWS CloudFormation stack sets
2. Triển khai các tài nguyên hạ tầng bao gồm:
   - KMS key để mã hóa
   - S3 bucket cho artifacts
   - ECR repository cho container images
   - ECS cluster
   - Application Load Balancer
   - Security groups
   - IAM roles
   - Cấu hình VPC
   - Target groups và listeners
   - Lambda functions
   - CloudWatch log groups

Việc triển khai tuân theo các best practices của AWS cho ứng dụng container.

### 5. Xem Ứng Dụng Của Bạn

Sau khi triển khai hoàn tất, Copilot sẽ cung cấp một URL công khai. Mở URL này trong trình duyệt để xem ứng dụng của bạn đang chạy.

### 6. Xem Xét Các Tài Nguyên AWS

#### CloudFormation Console
Truy cập AWS CloudFormation để xem:
- Stack set administration role
- Application stack với tất cả tài nguyên
- Các sự kiện tạo tài nguyên và trạng thái

#### ECS Console
Kiểm tra các tài nguyên ECS của bạn:
1. Truy cập ECS service console
2. Tìm cluster của bạn: `example-app-test-Cluster`
3. Xem xét các services và task definitions
4. Kiểm tra cách các tài nguyên được cấu hình theo best practices

#### Load Balancer
Xem xét cấu hình và thiết lập của Application Load Balancer.

### 7. Hiểu Về Cấu Hình Copilot

Copilot tạo một thư mục `copilot/` trong dự án của bạn với các file cấu hình:

```
copilot/
├── environments/
│   └── test/
│       └── manifest.yml
└── front-end/
    └── manifest.yml
```

#### Environment Manifest (`copilot/environments/test/manifest.yml`)
Chứa cấu hình đặc thù cho môi trường:
- Tên môi trường
- Loại môi trường
- Các thiết lập môi trường bổ sung

#### Service Manifest (`copilot/front-end/manifest.yml`)
Chứa cấu hình đặc thù cho service:
- Tên service
- Loại service
- Thiết lập container
- Cấu hình load balancer
- Chính sách auto-scaling
- Các thiết lập tùy chỉnh khác

Bạn có thể chỉnh sửa các file manifest này để tùy chỉnh hạ tầng dưới dạng code, sau đó triển khai lại bằng Copilot.

### 8. Dọn Dẹp

Để xóa tất cả tài nguyên và tránh chi phí phát sinh:

```bash
copilot app delete
```

Xác nhận việc xóa bằng cách nhấn `y`. Lệnh này sẽ xóa tất cả các CloudFormation stacks và các tài nguyên liên quan.

## Lợi Ích Chính Của AWS Copilot

- **Triển khai đơn giản** - Triển khai ứng dụng container với cấu hình tối thiểu
- **Best practices** - Tự động tuân theo các best practices của AWS cho kiến trúc
- **Infrastructure as Code** - Các file manifest cung cấp quản lý cấu hình
- **Khả năng quan sát đầy đủ** - Tích hợp dễ dàng với CloudFormation, ECS và các dịch vụ AWS khác
- **Nhiều loại workload** - Hỗ trợ các kiến trúc ứng dụng khác nhau
- **Dọn dẹp dễ dàng** - Các lệnh đơn giản để xóa tất cả tài nguyên

## Kết Luận

AWS Copilot đơn giản hóa đáng kể quá trình triển khai các ứng dụng container trên AWS. Bằng cách trừu tượng hóa phần lớn sự phức tạp, nó cho phép các nhà phát triển tập trung vào code ứng dụng trong khi đảm bảo hạ tầng tuân theo các best practices.

## Tài Nguyên Bổ Sung

- [Tài liệu AWS Copilot](https://aws.github.io/copilot-cli/)
- [Tài liệu AWS ECS](https://docs.aws.amazon.com/ecs/)
- [Tài liệu AWS Fargate](https://docs.aws.amazon.com/fargate/)