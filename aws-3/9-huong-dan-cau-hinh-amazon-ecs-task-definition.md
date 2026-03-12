# Hướng Dẫn Cấu Hình Amazon ECS Task Definition

## Tổng Quan

Hướng dẫn này cung cấp cái nhìn toàn diện về việc cấu hình task definition của Amazon ECS (Elastic Container Service) thông qua AWS console. Task definition là bản thiết kế mô tả cách các container nên được khởi chạy và cấu hình trong ECS cluster của bạn.

## Cấu Hình Cơ Bản

### Tên Family

Bước đầu tiên là định nghĩa tên family cho task definition của bạn. Ví dụ, bạn có thể đặt tên là `wordpress`.

### Yêu Cầu Hạ Tầng

Bạn có sự linh hoạt trong việc chọn nơi các container của mình sẽ chạy:

- **AWS Fargate** - Công cụ tính toán serverless
- **Amazon EC2 instances** - Triển khai truyền thống dựa trên EC2
- **Cả hai** - Phương pháp kết hợp

#### Sự Khác Biệt Chính

**Fargate:**
- Phải chọn từ các mức CPU và memory được định nghĩa trước tương thích với Fargate
- Network mode phải là AWS VPC

**EC2 Instances:**
- Có thể nhập bất kỳ giá trị tùy chỉnh nào cho memory và CPU
- Có tùy chọn cho các network mode nâng cao hơn

## IAM Roles

### Task Role

Task role rất quan trọng và thường xuyên xuất hiện trong các kỳ thi AWS. Chúng:
- Cho phép container của bạn thực hiện API calls đến các dịch vụ AWS
- Cung cấp IAM role tự động cho containers
- Được thiết kế đặc biệt cho các ECS task của bạn

### Task Execution Role

IAM role này:
- Dành riêng cho container agent
- Được sử dụng để thực hiện AWS API requests thay mặt bạn
- Là role tiêu chuẩn cần thiết cho các hoạt động ECS

## Cấu Hình Container

### Essential Containers

Mỗi task definition phải có ít nhất một essential container:

- **Hành vi Essential Container**: Nếu một essential container bị lỗi hoặc bị kill, toàn bộ task sẽ dừng lại
- **Hành vi Non-Essential Container**: Có thể dừng mà không ảnh hưởng đến task

**Ví dụ Cấu Hình:**
- Tên: `wordpress`
- Image URI: `WordPress`
- Essential: Có

Bạn có thể thêm nhiều container (Container 2, Container 3, v.v.) theo nhu cầu.

### Cấu Hình Image

#### Public Registry
Pull images trực tiếp từ các repository công khai như Docker Hub.

#### Private Registry
Đối với private repository, bạn cần:
- Thông tin xác thực
- Secrets Manager ARN chứa secret
- Điều này cho phép pull images từ private repository một cách an toàn

### Port Mapping

Định nghĩa tất cả các port mà container của bạn sẽ expose:

- **Container Port**: Số port
- **Các loại Protocol**: HTTP, HTTP2, gRPC, hoặc none
- **Port Name**: Định danh tùy chỉnh cho port
- **Multiple Mappings**: Thêm nhiều port mapping nếu cần cho các ứng dụng multi-port

### Giới Hạn Tài Nguyên

Kiểm soát phân bổ tài nguyên cho containers:

- **vCPUs**: Đơn vị CPU ảo
- **Memory**: Giới hạn cứng và mềm
- **Use Case**: Quan trọng khi chạy nhiều container cùng nhau

## Biến Môi Trường

### Cấu Hình Trực Tiếp

Thêm biến môi trường riêng lẻ:

```
Name: FOO
Value: BAR
```

### Tích Hợp Secrets Manager

Đối với dữ liệu nhạy cảm:

```
Name: SECRET_DB_PASSWORD
Value From: ARN của Secrets Manager secret
```

### SSM Parameter Store

Tương tự Secrets Manager, bạn có thể tham chiếu parameters từ AWS Systems Manager Parameter Store.

### Environment File

Hoặc, load biến môi trường từ file:
- File phải được lưu trên Amazon S3
- Cung cấp quản lý cấu hình tập trung

## Cấu Hình Logging

### Điểm Đến Log

ECS hỗ trợ nhiều điểm đến logging:

- **Amazon CloudWatch Logs** (tích hợp native)
- **Splunk**
- **Amazon Data Firehose**
- **Amazon Kinesis Data Streams**
- **Amazon OpenSearch Service**
- **Amazon S3**

### AWS FireLens

Sử dụng AWS FireLens để định tuyến log nâng cao đến nhiều điểm đến khác nhau.

### Cấu Hình CloudWatch

Khi sử dụng CloudWatch, chỉ định:
- Tên log group
- AWS region
- Stream prefix
- Tùy chọn tự động tạo group
- Các giá trị cấu hình bổ sung (tùy chọn)

## Cấu Hình Health và Timeout

### Health Checks

Đảm bảo containers vẫn khỏe mạnh trong suốt vòng đời của chúng.

### Timeouts

**Start Timeout:**
- Kill container nếu nó không khởi động trong thời gian chỉ định
- Ngăn chặn các tiến trình khởi động bị treo

**Stop Timeout:**
- Đảm bảo shutdown một cách graceful
- Kill container nếu nó không dừng đúng cách trong khoảng thời gian timeout

## Cấu Hình Docker

Các cài đặt cụ thể cho Docker:
- Docker labels
- Cấu hình tài nguyên cụ thể
- Nhìn chung ít quan trọng hơn cho các triển khai cơ bản

## Cấu Hình Storage

### Các Loại Volume

**Bind Mount:**
- Định nghĩa tên volume
- Mount các đường dẫn file system cục bộ

**Amazon EFS (Elastic File System):**
- Mount network file systems
- Chia sẻ dữ liệu giữa nhiều container
- Giải pháp lưu trữ bền vững

### Container Mount Points

Cấu hình nơi và cách volume được mount:
- Định nghĩa đường dẫn mount trong container
- Mount volumes từ các container khác
- Mount từ EFS hoặc bind mounts

**Khái Niệm Chính**: Bạn có thể mount dữ liệu từ EFS, từ file system cục bộ, hoặc thậm chí giữa các container.

## Giám Sát và Observability

### Tích Hợp AWS X-Ray

Bật trace collection để gửi dữ liệu đến AWS X-Ray:
- Sử dụng sidecar container (AWS Distro for OpenTelemetry)
- CPU và memory tự động được điều chỉnh cho sidecar

### Thu Thập Metrics

Gửi metrics đến các dịch vụ giám sát tập trung:
- **Amazon CloudWatch**
- **Amazon Managed Service for Prometheus**

Sử dụng nhiều thư viện khác nhau để thu thập và chuyển tiếp metrics cho việc giám sát toàn diện.

## Review Task Definition

### Tạo Task Definition

Sau khi cấu hình tất cả các cài đặt:
1. Click "Create"
2. Review tất cả cài đặt ở định dạng JSON (tùy chọn)
3. Tạo revision mới cho các cập nhật
4. Sửa đổi cài đặt riêng lẻ theo nhu cầu

### Review JSON

Bạn có thể review toàn bộ task definition ở định dạng JSON trước khi tạo, cho phép:
- Xác minh tất cả các cài đặt
- Export cho version control
- Tạo template cho tự động hóa

## Tóm Tắt

Task definition trong Amazon ECS cung cấp:
- Tùy chọn hạ tầng linh hoạt (Fargate và EC2)
- Quản lý IAM role toàn diện
- Hỗ trợ nhiều container với phân loại essential/non-essential
- Cấu hình mở rộng cho networking, storage và monitoring
- Tích hợp với các dịch vụ AWS (Secrets Manager, CloudWatch, X-Ray, EFS)
- Orchestration container có khả năng mở rộng và bảo mật

Hiểu về cấu hình task definition là điều cần thiết để triển khai và quản lý hiệu quả các ứng dụng được đóng gói trong container trên AWS ECS.