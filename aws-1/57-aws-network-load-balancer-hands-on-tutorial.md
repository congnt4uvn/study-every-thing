# AWS Network Load Balancer (NLB) - Hướng Dẫn Thực Hành

## Tổng Quan

Hướng dẫn thực hành này sẽ giúp bạn tạo và cấu hình AWS Network Load Balancer (NLB), bao gồm thiết lập security groups, target groups và khắc phục các sự cố thường gặp.

## Tạo Network Load Balancer

### Bước 1: Cấu Hình Cơ Bản

1. Điều hướng đến trang tạo Load Balancer
2. Chọn **Network Load Balancer**
3. Cấu hình các thiết lập sau:
   - **Tên**: `DemoNLB`
   - **Scheme**: Internet-facing (Hướng ra Internet)
   - **Loại địa chỉ IP**: IPv4

### Bước 2: Ánh Xạ Mạng (Network Mapping)

1. Chọn VPC của bạn
2. Kích hoạt tất cả các availability zone (trong ví dụ này là ba AZ)
3. Với mỗi availability zone:
   - Một subnet sẽ được tự động liên kết
   - Một địa chỉ IPv4 sẽ được AWS gán
   - **Lưu ý**: Bạn sẽ nhận được một địa chỉ IPv4 cố định cho mỗi AZ được kích hoạt
   - **Tùy chọn**: Bạn có thể sử dụng Elastic IP thay vì địa chỉ IP do AWS gán

### Bước 3: Security Groups

Việc gắn security group vào Network Load Balancer được khuyến nghị và là một tính năng mới hơn.

1. Nhấp **Create security group** (Tạo nhóm bảo mật)
2. Cấu hình security group:
   - **Tên**: `demo-sg-nlb`
   - **Inbound rules**: Cho phép HTTP (cổng 80) từ bất kỳ đâu (0.0.0.0/0)
   - **Outbound rules**: Mặc định (cho phép tất cả)
3. Tạo security group
4. Làm mới và chọn `demo-sg-nlb`
5. Xóa security group mặc định

**Điểm Quan Trọng**: Tương tự như Application Load Balancers (ALB), Network Load Balancers cũng sử dụng security groups để kiểm soát lưu lượng truy cập.

### Bước 4: Listeners và Routing

1. Cấu hình giao thức listener:
   - **Các tùy chọn có sẵn**: TCP, TCP_UDP, TLS, hoặc UDP
   - **Đã chọn**: TCP trên cổng 80
2. Tạo target group (xem phần tiếp theo)

## Tạo Target Group

### Cấu Hình Target Group

1. Nhấp **Create target group** (Tạo nhóm mục tiêu)
2. Chọn **Instances** làm loại target
3. Cấu hình các thiết lập:
   - **Tên**: `demo-tg-nlb`
   - **Giao thức**: TCP
   - **Cổng**: 80
   - **VPC**: Chọn VPC của bạn

### Cài Đặt Health Check (Kiểm Tra Sức Khỏe)

1. **Giao thức**: HTTP (vì chúng ta có ứng dụng HTTP trên các EC2 instances)
   - Các tùy chọn khác bao gồm: TCP, HTTPS
2. **Cài đặt nâng cao**:
   - **Ngưỡng khỏe mạnh (Healthy threshold)**: 2
   - **Thời gian chờ (Timeout)**: 2 giây
   - **Khoảng thời gian (Interval)**: 5 giây

### Đăng Ký Targets

1. Nhấp **Next** (Tiếp theo)
2. Chọn hai EC2 instances có sẵn của bạn
3. Nhấp **Include as pending below** (Bao gồm dưới dạng đang chờ)
4. Tạo target group

### Hoàn Tất Tạo Load Balancer

1. Quay lại cấu hình Network Load Balancer
2. Làm mới danh sách target group
3. Chọn `demo-tg-nlb`
4. Xem lại cấu hình
5. Tạo Network Load Balancer

## Khắc Phục Sự Cố

### Vấn Đề: Instances Không Khỏe Mạnh (Unhealthy)

Khi lần đầu truy cập URL của NLB, ứng dụng có thể không hoạt động.

**Nguyên Nhân Gốc Rễ**: Các target instances không khỏe mạnh vì health checks đang thất bại.

**Giải Pháp**: Cập nhật security groups của EC2 instances

1. Điều hướng đến các EC2 instances trong target group
2. Nhấp vào **Security** → **Security groups**
3. Kiểm tra các inbound rules hiện tại:
   - SSH từ bất kỳ đâu ✓
   - HTTP từ ALB security group ✓
   - HTTP từ NLB security group ✗ (thiếu)

4. Thêm một inbound rule mới:
   - **Loại**: HTTP
   - **Nguồn**: `demo-sg-nlb` (NLB security group)
   - **Mô tả**: "Allow traffic from NLB" (Cho phép lưu lượng từ NLB)

**Kết Quả**: Sau khi thêm quy tắc này, NLB có thể giao tiếp với các EC2 instances trong target group, và health checks sẽ vượt qua.

## Xác Minh

1. Đợi các instances trở nên khỏe mạnh trong target group
2. Truy cập URL của Network Load Balancer trong trình duyệt
3. Bạn sẽ thấy: "Hello World from [IP của instance]"
4. Làm mới nhiều lần để thấy IP thay đổi, xác nhận việc cân bằng tải giữa các instances

## Những Điểm Chính

- Network Load Balancers hoạt động tương tự như Application Load Balancers về mặt security groups
- Security groups của EC2 instances phải cho phép lưu lượng từ **cả** ALB và NLB security groups
- Cấu hình security group là rất quan trọng để NLB hoạt động đúng cách

## Dọn Dẹp (Phòng Tránh Chi Phí)

Để tránh phát sinh chi phí:

1. **Xóa Network Load Balancer**:
   - Chọn `DemoNLB`
   - Xóa

2. **Tùy chọn**: Xóa target group:
   - Chọn `demo-tg-nlb`
   - Xóa

3. **Tùy chọn**: Xóa security group:
   - Chọn `demo-sg-nlb`
   - Xóa
   - Lưu ý: Điều này không thực sự cần thiết nhưng là thực hành tốt

## Kết Luận

Bạn đã thành công tạo và cấu hình AWS Network Load Balancer, thiết lập security groups, khắc phục các vấn đề về health check, và học được các phương pháp tốt nhất để quản lý tài nguyên NLB.