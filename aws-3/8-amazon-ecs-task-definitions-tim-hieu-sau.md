# Amazon ECS Task Definitions - Tìm Hiểu Sâu

## Giới Thiệu

Amazon ECS Task Definitions được định nghĩa dưới dạng JSON, mặc dù console cung cấp giao diện UI để giúp bạn tạo JSON. Task definition cho biết ECS service cách chạy một hoặc nhiều Docker container trên ECS.

## Thông Tin Quan Trọng Trong Task Definitions

Một task definition chứa các thông tin quan trọng bao gồm:

- **Image Name**: Docker image sử dụng
- **Port Binding**: Cho cả container và host (khi sử dụng EC2)
- **Memory và CPU**: Yêu cầu tài nguyên cho container
- **Environment Variables**: Các giá trị cấu hình
- **Networking Information**: Cấu hình mạng
- **IAM Role**: Quyền hạn gắn với task definition
- **Logging Configuration**: Như CloudWatch logs

Đây là những thành phần quan trọng nhất, và các kỳ thi AWS sẽ kiểm tra bạn về một số thành phần này.

## Ví Dụ Về Port Mapping

### EC2 Launch Type

Khi chạy trên EC2 instance:

1. EC2 instance phải được đăng ký với ECS cluster
2. Phải chạy ECS agent
3. Bạn chạy Docker container thông qua ECS task definition (ví dụ: Apache HTTP server)

**Cấu Hình Port:**
- **Container Port**: Port 80 (expose HTTP server trên container)
- **Host Port**: Có thể là 80 hoặc 8080 (map với port của EC2 instance)
- Container port và host port không nhất thiết phải giống nhau

Internet hoặc mạng bên ngoài có thể truy cập EC2 instance trên host port (ví dụ: 8080), port này được chuyển đến container port 80, cung cấp quyền truy cập vào HTTP server.

**Quan trọng**: Bạn có thể định nghĩa tối đa **10 container cho mỗi task definition**.

## Dynamic Host Port Mapping

### Với Load Balancing (EC2 Launch Type)

Khi sử dụng load balancing với EC2 launch type, bạn sẽ có **Dynamic Host Port Mapping** nếu chỉ định nghĩa container port trong task definition.

**Cách hoạt động:**
- Mỗi ECS task có container port được đặt là 80
- Host port được đặt là 0 (không được thiết lập)
- Host port trở nên ngẫu nhiên/động
- Mỗi ECS task trong EC2 instance có thể truy cập từ một port khác nhau trên host

**Tích Hợp Application Load Balancer (ALB):**
- ALB tự động biết cách tìm đúng port thông qua tính năng Dynamic Host Port Mapping
- ALB, khi liên kết với ECS service, tự động kết nối đến các port khác nhau trên các instance khác nhau
- **Lưu ý**: Tính năng này KHÔNG hoạt động với Classic Load Balancer (thế hệ cũ)
- Chỉ hoạt động với ALB

**Cấu Hình Security Group:**
- EC2 instance security group phải cho phép bất kỳ port nào từ ALB security group
- Điều này cần thiết vì host port mapping không được biết trước

### Fargate Launch Type

Với Fargate, cấu hình khác:

- Mỗi ECS task nhận **private IP duy nhất**
- Không có host (vì là Fargate)
- Bạn chỉ cần định nghĩa **container ports**
- Mỗi task nhận private IP riêng thông qua Elastic Network Interface (ENI)
- Tất cả các task sử dụng cùng container ports

**ALB với Fargate:**
- ALB kết nối đến tất cả Fargate tasks trên cùng port (ví dụ: port 80)

**Cấu Hình Security Group:**
- ECS ENI Security Group: Phải cho phép port 80 từ ALB security group
- ALB Security Group: Phải cho phép port 80 hoặc 443 (nếu bật SSL) từ web

## IAM Roles Trong ECS

IAM roles được gán **cho mỗi task definition** (không phải ở service level).

**Cách hoạt động:**
1. Tạo task definition và gán ECS task role
2. Điều này cho phép ECS tasks của bạn truy cập các dịch vụ AWS (ví dụ: Amazon S3)
3. Khi bạn tạo ECS service từ task definition này, mỗi ECS task tự động assume và kế thừa ECS task role này
4. Tất cả các task trong service của bạn nhận cùng quyền hạn

**Ví dụ:**
- Task Definition 1 → Role có quyền truy cập S3 → Service 1 → Tất cả task có thể truy cập S3
- Task Definition 2 → Role có quyền truy cập DynamoDB → Service 2 → Tất cả task có thể truy cập DynamoDB

**Mẹo thi**: IAM roles cho ECS tasks được định nghĩa ở **task definition level**.

## Environment Variables

Task definitions có thể có environment variables từ nhiều nguồn:

### 1. Giá Trị Hard-coded
- Đặt trực tiếp trong task definition
- Sử dụng cho các giá trị cố định, không bí mật như URL

### 2. AWS Systems Manager Parameter Store hoặc Secrets Manager
- Cho các biến nhạy cảm như:
  - API keys
  - Cấu hình chung
  - Mật khẩu database
- Tham chiếu chúng trong ECS task definition
- Các giá trị được fetch và resolve tại runtime
- Được inject như environment variables trong ECS task của bạn

### 3. Amazon S3 Bucket
- Load environment variables trực tiếp từ S3 bucket
- Được gọi là **bulk environment variables loading** thông qua file

## Chia Sẻ Dữ Liệu Giữa Các Container

Một ECS task có thể chứa một hoặc nhiều container trong cùng task definition.

**Tại sao nhiều container?**
- Side containers (sidecars) có thể giúp với logging, tracing, v.v.
- Các container có thể cần chia sẻ file cho metrics, logs, v.v.

### Giải Pháp Bind Mount

Để chia sẻ dữ liệu, mount một **data volume** (bind mount) lên cả hai container. Điều này hoạt động cho cả **EC2 và Fargate tasks**.

**Kiến trúc:**
1. **Application Containers**: Một hoặc nhiều container chạy ứng dụng của bạn
2. **Sidecar Containers**: Cho metrics và logs
3. **Bind Mount**: Tạo shared storage (ví dụ: `/var/logs`)
   - Application containers ghi vào shared storage
   - Metrics và log containers đọc từ shared storage

### Triển Khai Storage

**EC2 Tasks:**
- Bind mount sử dụng EC2 instance storage
- Dữ liệu gắn với lifecycle của EC2 instance

**Fargate Tasks:**
- Sử dụng ephemeral storage
- Dữ liệu gắn với container lifecycle
- Khi Fargate task biến mất, storage cũng biến mất
- Dung lượng storage: **20 GB đến 200 GB** shared storage

### Các Use Case Phổ Biến

- Chia sẻ dữ liệu giữa nhiều container
- Sidecar containers gửi metrics hoặc logs đến các đích khác
- Sidecar cần đọc từ shared storage

## Tóm Tắt

Amazon ECS Task Definitions cung cấp cách toàn diện để cấu hình cách container của bạn chạy trên ECS. Những điểm chính:

- Định nghĩa container, ports, tài nguyên và quyền hạn trong định dạng JSON
- Port mapping khác nhau giữa EC2 và Fargate launch types
- Dynamic Host Port Mapping cho phép tích hợp ALB với EC2 tasks
- IAM roles được định nghĩa ở task definition level
- Environment variables có thể đến từ nhiều nguồn bảo mật
- Bind mounts cho phép chia sẻ dữ liệu giữa các container trong cùng task

Hiểu rõ các khái niệm này rất quan trọng cho kỳ thi chứng chỉ AWS và để triển khai hiệu quả các ứng dụng container hóa trên ECS.