# AWS Elastic Load Balancer - Giới Thiệu

## Load Balancing Là Gì?

Load balancer (bộ cân bằng tải) là một máy chủ hoặc một tập hợp các máy chủ có nhiệm vụ chuyển tiếp lưu lượng truy cập đến nhiều EC2 instance hoặc máy chủ backend/downstream.

### Cách Hoạt Động Của Load Balancing

Xét một kịch bản với ba EC2 instance được đặt phía sau một Elastic Load Balancer (ELB):

- Khi người dùng đầu tiên kết nối đến ELB, lưu lượng của họ được gửi đến một EC2 instance
- Khi người dùng thứ hai kết nối, họ được định tuyến đến một EC2 instance khác
- Người dùng thứ ba được cân bằng đến EC2 instance thứ ba

Nguyên tắc chính là khi có nhiều người dùng kết nối, tải sẽ được phân phối đều trên nhiều EC2 instance. Người dùng không biết họ đang kết nối đến instance backend nào - họ chỉ kết nối đến load balancer, cung cấp một điểm kết nối duy nhất.

## Tại Sao Nên Sử Dụng Load Balancer?

### Lợi Ích Chính

1. **Phân Tán Tải**: Phân phối lưu lượng truy cập trên nhiều instance downstream
2. **Điểm Truy Cập Duy Nhất**: Cung cấp một endpoint duy nhất cho ứng dụng của bạn
3. **Xử Lý Lỗi**: Xử lý liền mạch các lỗi của instance downstream thông qua cơ chế health check
4. **Kiểm Tra Sức Khỏe**: Giám sát tình trạng instance liên tục
5. **SSL Termination**: Xử lý lưu lượng HTTPS được mã hóa cho website của bạn
6. **Stickiness**: Duy trì phiên làm việc với cookies
7. **High Availability**: Duy trì tính khả dụng cao trên nhiều zone
8. **Phân Tách Lưu Lượng**: Tách biệt lưu lượng công khai khỏi lưu lượng riêng tư trong cloud

## Elastic Load Balancer (ELB)

### Managed Load Balancer (Dịch Vụ Được Quản Lý)

Elastic Load Balancer là một dịch vụ được quản lý, nghĩa là:

- **Quản Lý Bởi AWS**: AWS quản lý load balancer và đảm bảo nó sẽ hoạt động
- **Bảo Trì**: AWS xử lý việc nâng cấp, bảo trì và high availability
- **Cấu Hình**: Cung cấp các tùy chọn cấu hình để điều chỉnh hành vi của load balancer
- **Tiết Kiệm Chi Phí**: Rẻ hơn so với việc tự thiết lập load balancer của riêng bạn
- **Khả Năng Mở Rộng**: Loại bỏ khó khăn trong việc quản lý load balancer riêng từ góc độ khả năng mở rộng

### Tích Hợp Với AWS

Load balancer tích hợp liền mạch với nhiều dịch vụ AWS:

- EC2 instances
- Auto Scaling Groups
- Amazon ECS
- AWS Certificate Manager
- Amazon CloudWatch
- Amazon Route 53
- AWS WAF
- AWS Global Accelerator
- Và nhiều dịch vụ khác theo thời gian

## Health Checks (Kiểm Tra Sức Khỏe)

Health check là cơ chế quan trọng để load balancer xác minh xem EC2 instance có hoạt động đúng hay không. Nếu một instance không hoạt động, lưu lượng sẽ không được gửi đến instance đó.

### Cấu Hình Health Check

Health check được thực hiện bằng cách sử dụng:
- **Port**: Cổng để kiểm tra (ví dụ: 4567)
- **Route**: Endpoint để xác minh (ví dụ: `/health`)
- **Protocol**: Thường là HTTP

**Ví Dụ Cấu Hình:**
- Protocol: HTTP
- Port: 4567
- Endpoint: `/health`

Nếu EC2 instance không phản hồi với response OK (thường là mã trạng thái HTTP 200), instance sẽ được đánh dấu là không khỏe mạnh (unhealthy), và load balancer sẽ ngừng gửi lưu lượng đến instance đó.

## Các Loại AWS Load Balancer

### 1. Classic Load Balancer (CLB)
- **Thế Hệ**: V1 (thế hệ cũ)
- **Năm**: 2009
- **Giao Thức**: HTTP, HTTPS, TCP, SSL (Secure TCP)
- **Trạng Thái**: Đã lỗi thời - AWS không khuyến nghị sử dụng nữa
- **Khả Dụng**: Vẫn có sẵn nhưng hiển thị là deprecated trong console

### 2. Application Load Balancer (ALB)
- **Thế Hệ**: V2 (thế hệ mới)
- **Năm**: 2016
- **Giao Thức**: HTTP, HTTPS, WebSocket
- **Khuyến Nghị**: Được khuyến nghị cho các ứng dụng hiện đại

### 3. Network Load Balancer (NLB)
- **Thế Hệ**: V2 (thế hệ mới)
- **Năm**: 2017
- **Giao Thức**: TCP, TLS (Secure TCP), UDP
- **Trường Hợp Sử Dụng**: Ứng dụng hiệu suất cao, độ trễ thấp

### 4. Gateway Load Balancer (GWLB)
- **Thế Hệ**: Mới nhất
- **Năm**: 2020
- **Lớp**: Network Layer (Layer 3)
- **Giao Thức**: IP Protocol
- **Trường Hợp Sử Dụng**: Triển khai, mở rộng và quản lý các thiết bị ảo của bên thứ ba

### Khuyến Nghị

Rất khuyến nghị sử dụng các load balancer thế hệ mới (ALB, NLB, GWLB) vì chúng cung cấp nhiều tính năng hơn.

### Các Loại Load Balancer Theo Quyền Truy Cập

- **Internal (Private)**: Truy cập mạng riêng tư
- **External (Public)**: Load balancer công khai cho website và ứng dụng

## Cấu Hình Bảo Mật

### Security Group Của Load Balancer

Người dùng có thể truy cập load balancer từ bất kỳ đâu bằng HTTP hoặc HTTPS.

**Quy Tắc Security Group:**
- **Port Range**: 80 (HTTP) hoặc 443 (HTTPS)
- **Source**: `0.0.0.0/0` (bất kỳ đâu)

Điều này cho phép tất cả người dùng kết nối đến load balancer.

### Security Group Của EC2 Instance

EC2 instance chỉ nên cho phép lưu lượng đến trực tiếp từ load balancer.

**Quy Tắc Security Group:**
- **Protocol**: HTTP
- **Port**: 80
- **Source**: Security Group của Load Balancer (không phải IP range)

Bằng cách liên kết security group của EC2 instance với security group của load balancer, bạn đảm bảo rằng EC2 instance chỉ chấp nhận lưu lượng có nguồn gốc từ load balancer. Đây là một cơ chế bảo mật nâng cao.

## Tóm Tắt

Load balancer là một lựa chọn hiển nhiên khi nói đến cân bằng tải trên AWS. Chúng cung cấp:
- Phân phối lưu lượng tự động
- High availability và khả năng chịu lỗi
- Tích hợp liền mạch với các dịch vụ AWS
- Cơ chế bảo mật nâng cao
- Giải pháp tiết kiệm chi phí và có khả năng mở rộng

Trong các phần tiếp theo, chúng ta sẽ thảo luận chi tiết hơn về Classic Load Balancer, Application Load Balancer và Network Load Balancer.