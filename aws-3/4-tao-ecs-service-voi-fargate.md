# Tạo ECS Service với AWS Fargate

## Tổng Quan

Bài hướng dẫn này trình bày cách tạo một Amazon ECS (Elastic Container Service) service sử dụng AWS Fargate, một công cụ tính toán serverless cho container. Chúng ta sẽ đi qua từng bước tạo task definition, cấu hình service, và triển khai container với Application Load Balancer.

## Yêu Cầu Trước Khi Bắt Đầu

- Tài khoản AWS với quyền truy cập phù hợp
- Hiểu biết cơ bản về container và Docker
- Quen thuộc với AWS Console

## Bước 1: Tạo Task Definition

Trước khi tạo ECS service, bạn cần định nghĩa task definition để chỉ định cách container của bạn sẽ chạy.

### Cấu Hình Task Definition

1. Điều hướng đến panel **Task Definition** trong ECS console
2. Nhấp **Create new task definition** (Tạo task definition mới)
3. Cấu hình các thiết lập sau:

**Thông Tin Cơ Bản:**
- **Task Definition Name** (Tên Task Definition): `nginxdemos-hello`
  - Tên này tham chiếu đến Docker image `nginxdemos/hello` từ Docker Hub

**Yêu Cầu Hạ Tầng:**
- **Launch Type** (Loại khởi chạy): AWS Fargate (serverless compute)
  - Lựa chọn khác: Amazon EC2 instances (không đề cập trong demo này)
- **Operating System** (Hệ điều hành): Linux
- **Architecture** (Kiến trúc): Mặc định

**Task Size (Cấu hình Fargate):**
- **vCPU**: 0.5 (Lựa chọn từ 0.5 đến 16 vCPU)
- **Memory** (Bộ nhớ): 1 GB (Lựa chọn lên đến 120 GB)
  - Các tài nguyên này được cung cấp bởi Fargate theo kiểu serverless

**IAM Roles (Vai trò IAM):**
- **Task Role** (Vai trò task): Không có (không cần thiết cho demo này)
  - Sử dụng khi container của bạn cần gọi API đến các dịch vụ AWS
- **Task Execution Role** (Vai trò thực thi task): Để mặc định
  - `ECS task execution role` sẽ được tạo tự động nếu chưa tồn tại

### Cấu Hình Container

**Chi Tiết Container:**
- **Name** (Tên): `nginxdemos-hello`
- **Image URI**: `nginxdemos/hello`
  - Tự động pull image từ Docker Hub
- **Essential Container** (Container thiết yếu): Có

**Port Mappings (Ánh xạ cổng):**
- **Container Port** (Cổng container): 80
- **Host Port** (Cổng host): 80
- **Protocol** (Giao thức): TCP

**Cài Đặt Bổ Sung (Để mặc định):**
- Giới hạn phân bổ tài nguyên
- Biến môi trường
- Cấu hình logging

**Storage (Lưu trữ):**
- **Ephemeral Storage** (Lưu trữ tạm thời): 21 GB (mặc định cho Fargate)

4. Nhấp **Create** để hoàn tất việc tạo task definition

> **Lưu ý**: Bạn sẽ thấy "Version 1" cho task definition đầu tiên. Số phiên bản sẽ tăng lên với mỗi lần cập nhật.

## Bước 2: Tạo ECS Service

Bây giờ task definition đã sẵn sàng, hãy triển khai nó dưới dạng một service.

### Cấu Hình Service

1. Điều hướng đến **Clusters** trong ECS console
2. Chọn cluster của bạn (ví dụ: `demo-cluster`)
3. Đi đến tab **Services**
4. Nhấp **Create Service** (Tạo Service)

**Chi Tiết Service:**
- **Task Definition Family**: `nginxdemos-hello`
- **Revision** (Phiên bản): Latest (mới nhất hoặc phiên bản cụ thể)
- **Service Name** (Tên service): Giữ mặc định hoặc tùy chỉnh

**Cấu Hình Compute:**
- **Capacity Provider Strategy**: Sử dụng mặc định
- **Launch Type**: AWS Fargate
- **Platform Version** (Phiên bản nền tảng): Latest

**Cấu Hình Deployment:**
- **Application Type** (Loại ứng dụng): Service
- **Deployment Type** (Loại triển khai): Replica
- **Desired Tasks** (Số task mong muốn): 1 (bắt đầu với một task)
  - Bạn có thể scale lên nhiều task sau
- **AZ Rebalancing** (Cân bằng lại AZ): Để cài đặt mặc định
- **Deployment Options** (Tùy chọn triển khai): Để mặc định

### Cấu Hình Networking

**Cài Đặt Network:**
- **Subnets**: Giữ các lựa chọn mặc định
- **Security Group** (Nhóm bảo mật): Tạo mới
  - **Name** (Tên): Giữ tên tự động tạo
  - **Inbound Rules** (Quy tắc vào): Cho phép HTTP traffic từ mọi nơi (port 80)
- **Public IP** (IP công khai): Bật (Yes)

### Cấu Hình Load Balancer

**Thiết Lập Load Balancer:**
- **Load Balancer Type** (Loại Load Balancer): Application Load Balancer
- **Load Balancer Name** (Tên Load Balancer): `DemoALBForECS`
- **Listener**: Port 80
- **Target Group** (Nhóm đích):
  - **Name** (Tên): `nginxdemosTG`
  - **Port** (Cổng): 80
  - **Health Check** (Kiểm tra sức khỏe): Cài đặt mặc định

**Cài Đặt Bổ Sung (Bỏ qua cho demo này):**
- VPC Lattice: Không cấu hình
- Service Auto Scaling: Không cấu hình (không có CloudWatch alarm)
- Volumes: Không cấu hình

5. Nhấp **Create** để triển khai service

## Bước 3: Xác Minh Triển Khai

### Kiểm Tra Trạng Thái Service

1. Nhấp vào service vừa tạo
2. Xác minh các thông tin sau:
   - **Desired Tasks** (Task mong muốn): 1
   - **Running Tasks** (Task đang chạy): 1
   - **Status** (Trạng thái): Active

### Kiểm Tra Target Group và Load Balancer

1. Nhấp vào **Target Group** được liên kết
2. Xác minh:
   - Một địa chỉ IP đã được đăng ký làm target (IP private của container)
   - Trạng thái health check nên là "healthy"

3. Điều hướng đến tab **Load Balancer**
4. Tìm load balancer của bạn (`DemoALBForECS`)
5. Sao chép **DNS name**

### Kiểm Tra Ứng Dụng

1. Mở tab trình duyệt mới
2. Dán DNS name của Load Balancer
3. Bạn sẽ thấy **nginx welcome page**
4. Địa chỉ server hiển thị phải khớp với IP private đã đăng ký trong target group

### Xem Chi Tiết Task

1. Vào service và nhấp vào tab **Tasks**
2. Nhấp vào task đang chạy để xem:
   - Task revision
   - Launch type (Fargate)
   - Địa chỉ IP private
   - Chi tiết container
   - **Logs**: Xem logs của nginx container

### Giám Sát Service Events

1. Trong service, điều hướng đến tab **Events**
2. Xem lại timeline triển khai:
   - Task đã bắt đầu
   - Đăng ký trong target group
   - Hoàn thành triển khai
   - Đạt trạng thái ổn định

## Bước 4: Scale ECS Service

Một trong những lợi ích chính của ECS với Fargate là khả năng scale ngang dễ dàng.

### Scale Up (Tăng quy mô)

1. Chọn service của bạn
2. Nhấp **Update Service** (Cập nhật Service)
3. Thay đổi **Desired Number of Tasks** từ 1 lên 3
4. Giữ nguyên tất cả các cài đặt khác
5. Nhấp **Update**

**Điều Gì Xảy Ra:**
- ECS provision hai task bổ sung
- Fargate tự động phân bổ tài nguyên compute cần thiết
- Các task được phân phối qua các Availability Zone
- Tất cả task đăng ký với Application Load Balancer

### Xác Minh Scaling

1. Làm mới tab **Tasks**
   - Tiến trình trạng thái: Pending → Activating → Running
2. Điều hướng đến Target Group
   - Xác minh ba địa chỉ IP đã được đăng ký
3. Kiểm tra phân phối tải:
   - Làm mới trình duyệt nhiều lần
   - IP server sẽ thay đổi với mỗi lần refresh
   - Điều này xác nhận ALB đang phân phối traffic qua tất cả container

## Bước 5: Scale Down và Dọn Dẹp

Để tránh chi phí không cần thiết, bạn có thể scale down hoặc dừng service.

### Scale Down về Không

1. Chọn service của bạn
2. Nhấp **Update Service**
3. Đặt **Desired Number of Tasks** về 0
4. Nhấp **Update**
5. Xác minh trong tab **Tasks** rằng tất cả task đã dừng

### Dọn Dẹp Bổ Sung (nếu có)

Nếu bạn có ECS cluster dựa trên EC2:
1. Điều hướng đến Auto Scaling Group
2. Đặt **Desired Capacity** về 0
3. Điều này đảm bảo không có EC2 instance nào đang chạy

### Xác Minh Dọn Dẹp

1. Kiểm tra tab **Tasks** - không nên có task nào đang chạy
2. Xem tab **Events** để thấy lịch sử cập nhật service

## Tóm Tắt

Trong hướng dẫn này, bạn đã học cách:

1. ✅ Tạo ECS Task Definition với đặc tả container
2. ✅ Triển khai ECS Service trên AWS Fargate (serverless)
3. ✅ Cấu hình networking với security group và public IP
4. ✅ Thiết lập Application Load Balancer với target group
5. ✅ Xác minh và kiểm tra service đã triển khai
6. ✅ Scale service lên xuống một cách linh hoạt
7. ✅ Giám sát service event và task log
8. ✅ Dọn dẹp tài nguyên để giảm thiểu chi phí

## Điểm Chính

- **AWS Fargate** cung cấp khả năng thực thi container serverless mà không cần quản lý server
- **Task Definition** là bản thiết kế cho container của bạn
- **Service** duy trì số lượng task mong muốn đang chạy
- **Application Load Balancer** phân phối traffic qua nhiều container instance
- **Scaling** rất đơn giản và diễn ra trong vài phút
- Nền tảng tự động xử lý việc provision hạ tầng

## Bước Tiếp Theo

- Khám phá ECS Service Auto Scaling với CloudWatch alarm
- Triển khai CI/CD pipeline cho deployment tự động
- Cấu hình custom task role để tích hợp với các dịch vụ AWS
- Thiết lập CloudWatch Logs để log tập trung
- Triển khai load balancing nâng cao với path-based routing

---

**Ngữ Cảnh Khóa Học**: Bài giảng này là một phần của chuỗi đào tạo AWS về Amazon ECS và các dịch vụ container hóa.