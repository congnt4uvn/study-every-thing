# Thiết Lập EC2 Đa Vùng và ALB cho Route 53

## Tổng Quan

Hướng dẫn này sẽ giúp bạn thiết lập ba EC2 instance trên các vùng AWS khác nhau và cấu hình Application Load Balancer (ALB) để chuẩn bị cho việc cấu hình Route 53.

## Tổng Quan Kiến Trúc

Chúng ta sẽ tạo:
- 3 EC2 instance ở các vùng khác nhau (Frankfurt, Northern Virginia, Singapore)
- 1 Application Load Balancer tại Frankfurt
- Target group để định tuyến lưu lượng

## Bước 1: Khởi Động EC2 Instance Đầu Tiên (Frankfurt - EU Central 1)

### Cấu Hình Instance

1. Truy cập dịch vụ EC2 và click **Launch Instance**
2. Chọn **Amazon Linux 2** AMI
3. Chọn instance type **t2.micro**
4. **Key Pair**: Chọn "Proceed without a key pair" (chúng ta sẽ dùng EC2 Instance Connect)

### Cài Đặt Security Group

Tạo security group mới với các rule sau:
- **SSH**: Port 22, Source: Anywhere
- **HTTP**: Port 80, Source: Anywhere

### Script User Data

Trong phần Advanced Details, thêm bootstrap script sau:

```bash
#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd
EC2_AVAIL_ZONE=$(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone)
echo "<h1>Hello World from $(hostname -f) in AZ $EC2_AVAIL_ZONE</h1>" > /var/www/html/index.html
```

Script này sẽ:
- Cài đặt Apache HTTP server
- Hiển thị hostname của instance và availability zone
- Sử dụng EC2 metadata để lấy thông tin AZ

4. Click **Launch Instance**

## Bước 2: Khởi Động EC2 Instance Thứ Hai (Northern Virginia - US East 1)

1. Chuyển sang vùng **US East 1** (Northern Virginia)
2. Khởi động instance với cùng cấu hình:
   - Amazon Linux 2
   - t2.micro
   - Không cần key pair
   - Security group: Cho phép SSH và HTTP
   - Cùng user data script từ Bước 1
3. Khởi động instance

## Bước 3: Khởi Động EC2 Instance Thứ Ba (Singapore - AP Southeast 1)

1. Chuyển sang vùng **AP Southeast 1** (Singapore)
2. Khởi động instance với cài đặt tương tự:
   - Amazon Linux 2
   - t2.micro
   - Không cần key pair
   - Security group: Cho phép SSH và HTTP
   - Cùng user data script
3. Khởi động instance

## Bước 4: Tạo Application Load Balancer (Frankfurt)

### Cấu Hình ALB

1. Quay lại vùng **Frankfurt (EU Central 1)**
2. Truy cập **Load Balancers** và click **Create Load Balancer**
3. Chọn **Application Load Balancer**

### Cấu Hình Cơ Bản

- **Name**: `DemoRoute53ALB`
- **Scheme**: Internet-facing
- **IP address type**: IPv4

### Network Mapping

- Chọn **3 availability zones** (tất cả subnet có sẵn)

### Security Groups

- Chọn security group đã tạo trước đó (có HTTP và SSH được bật)

### Listeners và Routing

- **Protocol**: HTTP
- **Port**: 80
- Tạo target group mới

## Bước 5: Tạo Target Group

1. **Target type**: Instances
2. **Name**: `demo-tg-route53`
3. **Protocol**: HTTP
4. **Port**: 80
5. Click **Next**

### Đăng Ký Target

1. Chọn EC2 instance tại Frankfurt
2. Click **Include as pending below**
3. Xem lại và click **Create target group**

## Bước 6: Hoàn Tất Tạo ALB

1. Quay lại trang tạo Load Balancer
2. Refresh và chọn target group vừa tạo: `demo-tg-route53`
3. Xem lại cài đặt và click **Create Load Balancer**
4. Click **View Load Balancer**

## Bước 7: Kiểm Tra

### Test EC2 Instances

Kiểm tra từng instance bằng cách truy cập địa chỉ IP công khai qua HTTP:

**Instance Frankfurt (EU Central 1)**
- Copy địa chỉ IPv4 công khai
- Truy cập qua trình duyệt: `http://<public-ip>`
- Kết quả mong đợi: `Hello World from <hostname> in AZ eu-central-1b`

**Instance Northern Virginia (US East 1)**
- Copy địa chỉ IPv4 công khai
- Truy cập qua trình duyệt: `http://<public-ip>`
- Kết quả mong đợi: `Hello World from <hostname> in AZ us-east-1a`

**Instance Singapore (AP Southeast 1)**
- Copy địa chỉ IPv4 công khai
- Truy cập qua trình duyệt: `http://<public-ip>`
- Kết quả mong đợi: `Hello World from <hostname> in AZ ap-southeast-1b`

### Test Application Load Balancer

1. Copy tên DNS của ALB từ chi tiết Load Balancer
2. Truy cập qua trình duyệt: `http://<alb-dns-name>`
3. ALB có thể mất vài phút để provisioning
4. Khi đã hoạt động, bạn sẽ thấy: `Hello World from <hostname> in AZ eu-central-1b`

## Tóm Tắt

Bạn đã tạo thành công:
- ✅ 3 EC2 instance trên 3 vùng AWS khác nhau
- ✅ 1 Application Load Balancer tại Frankfurt
- ✅ 1 Target group với instance đã đăng ký
- ✅ Tất cả instance đang phục vụ HTTP traffic với thông tin vùng

## Tham Chiếu Chi Tiết Instance

Lưu giữ thông tin tài nguyên của bạn:

| Vùng | Mã Vùng | IP Công Khai | Availability Zone |
|------|---------|--------------|-------------------|
| Frankfurt | eu-central-1 | `<ip-của-bạn>` | eu-central-1b |
| Northern Virginia | us-east-1 | `<ip-của-bạn>` | us-east-1a |
| Singapore | ap-southeast-1 | `<ip-của-bạn>` | ap-southeast-1b |

**Tên DNS ALB**: `<tên-dns-alb-của-bạn>`

## Các Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ cấu hình Route 53 để triển khai:
- Chính sách định tuyến theo địa lý (Geographic routing)
- Định tuyến dựa trên độ trễ (Latency-based routing)
- Cấu hình failover
- Health checks

Hãy lưu giữ thông tin này để cấu hình Route 53!