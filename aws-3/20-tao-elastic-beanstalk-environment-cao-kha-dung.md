# Tạo Môi Trường Elastic Beanstalk Có Tính Khả Dụng Cao

## Tổng Quan

Hướng dẫn này sẽ trình bày quy trình tạo môi trường AWS Elastic Beanstalk sẵn sàng cho production với cấu hình có tính khả dụng cao. Bạn sẽ học cách thiết lập môi trường cân bằng tải với khả năng tự động mở rộng.

## Yêu Cầu Trước Khi Bắt Đầu

- Tài khoản AWS với quyền IAM phù hợp
- Ứng dụng Elastic Beanstalk đã tồn tại
- Hiểu biết cơ bản về các dịch vụ AWS (EC2, ALB, Auto Scaling)

## Tạo Môi Trường Production

### Bước 1: Khởi Tạo Môi Trường Mới

1. Truy cập console Elastic Beanstalk
2. Tạo môi trường mới
3. Chọn loại **Web server environment**
4. Đặt tên môi trường là `prod` (cho production)
5. Chọn nền tảng được quản lý: **Node.js**
6. Chọn ứng dụng mẫu (tạm thời)
7. Chọn preset **High Availability** (không phải Single Instance)

Cấu hình này cho phép chúng ta khám phá các tính năng nâng cao của Beanstalk và hiểu cách hoạt động của tính khả dụng cao.

### Bước 2: Cấu Hình Service Roles

1. Nhấp **Next**
2. Sử dụng service role đã tồn tại
3. Chọn các service role đã được tạo trước đó
4. Nhấp **Next**

### Bước 3: Cấu Hình Tùy Chọn

#### Cài Đặt Networking và VPC

- **Chọn VPC**: Chọn VPC cụ thể hoặc sử dụng mặc định (tùy chọn)
- **Instance Settings**: Chọn các subnet để khởi chạy instances
  - Chọn tất cả các subnet có sẵn để đảm bảo tính khả dụng cao
  - **Public IP**: Không cần thiết khi sử dụng load balancer (tắt tùy chọn này)

#### Cấu Hình Database

**Lưu Ý Quan Trọng**: Nếu bạn thêm database vào môi trường Beanstalk:
- Vòng đời của database được liên kết với môi trường
- Xóa môi trường sẽ xóa luôn database
- **Giải pháp**: Tạo snapshot của database trước khi xóa để khôi phục sau này

Trong hướng dẫn này, chúng ta sẽ không thêm database.

### Bước 4: Cấu Hình Instance

#### Root Volume và Security Groups

- Sử dụng cài đặt root volume mặc định
- Cho phép tự động cấu hình security group

#### Cài Đặt Auto Scaling Group (ASG)

Cấu hình ASG với các tham số sau:

- **Loại Môi Trường**: Load Balanced
- **Dung Lượng**: Tối thiểu 1, tối đa 4 instances
- **Fleet Composition**: Chọn giữa On-Demand hoặc Spot instances
- **Instance Type**: t3.micro (được khuyến nghị để tiết kiệm chi phí)
- **AMI ID**: Sử dụng mặc định hoặc chỉ định AMI tùy chỉnh

#### Chính Sách Scaling

Cấu hình cách ASG của bạn mở rộng:
- Đặt ngưỡng network trung bình
- Xác định dung lượng tối thiểu và tối đa
- Cấu hình các triggers và ngưỡng scaling

### Bước 5: Cấu Hình Load Balancer

#### Cài Đặt Load Balancer

- **Visibility**: Public load balancer
- **Subnets**: Chọn ba subnet để đảm bảo tính khả dụng cao
- **Type**: Chọn giữa:
  - **Application Load Balancer (ALB)** - Được khuyến nghị cho HTTP/HTTPS
  - **Network Load Balancer (NLB)** - Cho traffic TCP

#### Tùy Chọn ALB

- **Dedicated**: Một ALB cho mỗi môi trường
- **Shared**: Chia sẻ ALB giữa nhiều môi trường (tiết kiệm chi phí)

Cấu hình các cài đặt bổ sung:
- Listeners
- Processes
- Rules

Tất cả cấu hình load balancer có thể được quản lý trực tiếp trong Beanstalk.

### Bước 6: Health Reporting và Monitoring

#### Cấu Hình Health Check

- Bật **CloudWatch custom metrics**
- Chọn **Enhanced health reporting** (được khuyến nghị)
- Cấu hình các tham số health check

#### Các Tính Năng Bổ Sung

- **Managed Updates**: Beanstalk tự động quản lý các bản cập nhật nền tảng
- **Email Notifications**: Thiết lập cảnh báo cho các sự kiện quan trọng của môi trường
- **Rolling Updates**: Cấu hình chiến lược cập nhật (quan trọng cho việc chuẩn bị thi)

### Bước 7: Cấu Hình Platform Software

Các tích hợp tùy chọn:
- **Amazon X-Ray**: Bật distributed tracing
- **CloudWatch Logs**: Stream log ứng dụng
- Các cài đặt cụ thể cho nền tảng khác

## Phương Pháp Triển Khai: Skip to Review

Do các vấn đề tiềm ẩn với console mới, cách tiếp cận an toàn hơn:

1. Hủy quy trình cấu hình chi tiết
2. Tạo lại môi trường với:
   - Application: `MyApplication`
   - Environment name: `MyApplication-prod`
   - Platform: Node.js 12
   - Preset: High Availability
3. Nhấp **Next**
4. Nhấp **Skip to Review**
5. Xem lại tất cả các tham số
6. Nhấp **Submit**

**Thời Gian Triển Khai**: Khoảng 10 phút

## Xác Minh Triển Khai

### Xác Minh Môi Trường

1. Chờ trạng thái môi trường trở thành sẵn sàng
2. Nhấp vào URL môi trường
3. Xác minh trang "Congratulations" tải thành công

### Xác Minh Load Balancer

Điều hướng đến **EC2 > Load Balancers**:
- Xác minh việc tạo load balancer
- Kiểm tra các availability zones (nên trải rộng 3 AZs)
- Kiểm tra target groups
- Xác nhận một instance healthy đã được đăng ký

### Xác Minh EC2 Instance

Kiểm tra EC2 instance đã tạo:
- Tương ứng với `MyApplication-prod`
- Xem lại cài đặt security group:
  - Cho phép port 80 từ security group của load balancer
  - Security group của load balancer cho phép port 80 từ bất kỳ đâu
  - Quy tắc outbound cho phép port 80 đến bất kỳ đâu

### Xác Minh Auto Scaling Group

Điều hướng đến **EC2 > Auto Scaling Groups**:
- Nên có hai ASG (môi trường dev và prod)
- Cấu hình ASG production:
  - Tối thiểu: 1 instance
  - Tối đa: 4 instances
- Kiểm tra **Instance Management**: Một instance đang in service
- Xác minh **Automatic Scaling**: Các chính sách dynamic scaling được cấu hình bởi Elastic Beanstalk

## Những Điểm Chính Cần Ghi Nhớ

### Lợi Ích Của Elastic Beanstalk

1. **Cấu Hình Tự Động**: Beanstalk tự động cấu hình tất cả các thành phần hạ tầng
2. **Triển Khai Đơn Giản**: Upload code và chỉ định yêu cầu về tính khả dụng cao
3. **Quản Lý Toàn Diện**: Xử lý load balancers, auto scaling, health checks và monitoring
4. **Cách Ly Môi Trường**: Môi trường dev và prod riêng biệt với các cấu hình khác nhau

### Các Thành Phần Kiến Trúc

- **Load Balancer**: Phân phối traffic qua nhiều instances
- **Auto Scaling Group**: Tự động mở rộng dựa trên nhu cầu
- **Security Groups**: Được cấu hình đúng cách cho giao tiếp an toàn
- **Health Monitoring**: Health checks tích hợp sẵn và tích hợp CloudWatch

## Kết Luận

Bây giờ bạn đã có hai môi trường Beanstalk hoạt động đầy đủ:
- **Môi trường Development**: Cấu hình single instance
- **Môi trường Production**: Tính khả dụng cao với load balancing và auto scaling

Điều này chứng minh sức mạnh và sự đơn giản của AWS Elastic Beanstalk trong việc triển khai các ứng dụng có khả năng mở rộng mà không cần quản lý độ phức tạp của hạ tầng.

## Các Bước Tiếp Theo

- Khám phá cấu hình rolling updates
- Triển khai các chính sách auto-scaling tùy chỉnh
- Cấu hình tên miền tùy chỉnh
- Thiết lập CI/CD pipelines cho triển khai tự động