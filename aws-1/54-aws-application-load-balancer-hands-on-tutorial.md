# AWS Application Load Balancer - Hướng Dẫn Thực Hành

## Tổng Quan

Hướng dẫn thực hành này trình bày cách tạo và cấu hình AWS Application Load Balancer (ALB) để phân phối lưu lượng truy cập giữa nhiều EC2 instance. Bạn sẽ học cách thiết lập target group, cấu hình security group và kiểm tra chức năng cân bằng tải.

## Điều Kiện Tiên Quyết

- Tài khoản AWS với quyền phù hợp
- Hiểu biết cơ bản về EC2 instance
- Quen thuộc với security group

## Phần 1: Khởi Chạy EC2 Instance

### Bước 1: Tạo Hai EC2 Instance

1. Truy cập bảng điều khiển EC2 và nhấp **Launch Instances**
2. Cấu hình các thiết lập sau:
   - **Số lượng instance**: 2
   - **Tên**: My First Instance (đổi tên instance thứ hai thành "My Second Instance")
   - **AMI**: Amazon Linux 2
   - **Loại instance**: t2.micro
   - **Key pair**: Tiếp tục mà không cần key pair (chúng ta sẽ dùng EC2 Instance Connect nếu cần)

### Bước 2: Cấu Hình Network Settings

1. Chọn **existing security group**
2. Chọn security group **Launch Wizard 1**
   - Cho phép lưu lượng HTTP và SSH đến EC2 instance

### Bước 3: Thêm User Data Script

1. Cuộn xuống **Advanced details**
2. Thêm EC2 user data script để tự động cấu hình các instance
3. Khởi chạy cả hai instance

### Bước 4: Xác Minh Thiết Lập Instance

1. Đợi cả hai instance đạt trạng thái "running"
2. Sao chép địa chỉ IPv4 của instance đầu tiên và truy cập trong trình duyệt
3. Bạn sẽ thấy "Hello World" từ instance đầu tiên
4. Lặp lại với instance thứ hai
5. Cả hai instance đều hiển thị "Hello World" với các mã định danh khác nhau

## Phần 2: Hiểu Về Các Loại Load Balancer

### Application Load Balancer (ALB)
- **Giao thức**: HTTP và HTTPS
- **Trường hợp sử dụng**: Ứng dụng web và microservices
- **Tầng**: Tầng 7 (Tầng ứng dụng)

### Network Load Balancer (NLB)
- **Giao thức**: TCP, UDP, hoặc TLS qua TCP
- **Trường hợp sử dụng**: Ứng dụng hiệu suất cực cao
- **Hiệu suất**: Hàng triệu yêu cầu mỗi giây với độ trễ cực thấp

### Gateway Load Balancer (GLB)
- **Trường hợp sử dụng**: Bảo mật, phát hiện xâm nhập, tường lửa
- **Mục đích**: Phân tích lưu lượng mạng

### Classic Load Balancer
- **Trạng thái**: Đang bị ngừng hỗ trợ (có thể không còn khả dụng)
- **Lưu ý**: Không khuyến nghị cho các triển khai mới

## Phần 3: Tạo Application Load Balancer

### Bước 1: Cấu Hình Cài Đặt Cơ Bản

1. Điều hướng đến **Load Balancers** trong bảng điều khiển EC2
2. Nhấp **Create Load Balancer**
3. Chọn **Application Load Balancer**
4. Cấu hình:
   - **Tên**: DemoALB
   - **Scheme**: Internet-facing
   - **Loại địa chỉ IP**: IPv4

### Bước 2: Network Mapping

1. Chọn tất cả các availability zone để đảm bảo tính khả dụng cao
2. Điều này đảm bảo load balancer được triển khai trên nhiều AZ

### Bước 3: Cấu Hình Security Group

1. Tạo security group mới:
   - **Tên**: demo-sg-load-balancer
   - **Mô tả**: Allow HTTP into load balancer, into ALB
   - **Inbound rules**: Cho phép HTTP từ mọi nơi (0.0.0.0/0)
   - **Outbound rules**: Giữ cài đặt mặc định

2. Sau khi tạo, làm mới và chọn security group mới
3. Xóa security group mặc định

## Phần 4: Tạo Target Group

### Bước 1: Cấu Hình Cơ Bản

1. Nhấp **Create target group**
2. Cấu hình:
   - **Loại target**: Instances
   - **Tên**: demo-tg-alb
   - **Giao thức**: HTTP
   - **Cổng**: 80
   - **Phiên bản HTTP**: HTTP/1

### Bước 2: Health Check

- Giữ cài đặt health check mặc định
- Điều này cho phép ALB giám sát tình trạng sức khỏe của instance

### Bước 3: Đăng Ký Target

1. Nhấp **Next**
2. Chọn cả hai EC2 instance
3. Chỉ định **cổng 80** cho cả hai instance
4. Nhấp **Include as pending below**
5. Tạo target group

## Phần 5: Hoàn Thành Thiết Lập Load Balancer

### Bước 1: Liên Kết Target Group Với Listener

1. Quay lại trang tạo load balancer
2. Làm mới danh sách target group
3. Chọn **demo-tg-alb** làm target group
4. Listener sẽ định tuyến lưu lượng HTTP trên cổng 80 đến target group này

### Bước 2: Tạo Load Balancer

1. Nhấp **Create load balancer**
2. Đợi load balancer được cung cấp (trạng thái: Active)

## Phần 6: Kiểm Tra Load Balancer

### Kiểm Tra 1: Xác Minh Load Balancing

1. Sao chép DNS name của load balancer
2. Dán vào trình duyệt
3. Bạn sẽ thấy "Hello World" từ một trong các instance
4. Làm mới trang nhiều lần
5. **Kết quả**: Instance đích thay đổi mỗi lần làm mới, chứng minh load balancing đang hoạt động

### Kiểm Tra 2: Kiểm Tra Target Health

1. Điều hướng đến phần **Target Groups**
2. Chọn **demo-tg-alb**
3. Xem tab **Targets**
4. Cả hai instance đều hiển thị trạng thái **healthy**

### Kiểm Tra 3: Tình Huống Instance Lỗi

1. Dừng một trong các EC2 instance
2. Đợi khoảng 30 giây
3. Làm mới chế độ xem target group
4. **Kết quả**: Instance đã dừng hiển thị "unused" hoặc "unhealthy"
5. Truy cập URL load balancer lần nữa
6. **Kết quả**: Lưu lượng chỉ được chuyển đến instance còn healthy

### Kiểm Tra 4: Khôi Phục Instance

1. Khởi động lại instance đã dừng
2. Đợi nó khởi động
3. Instance sẽ hiển thị trạng thái "initial health"
4. Sau khi vượt qua health check, nó trở thành "healthy"
5. Làm mới URL load balancer
6. **Kết quả**: Lưu lượng giờ được cân bằng giữa cả hai instance

## Những Điều Quan Trọng Cần Nhớ

### Lợi Ích Của Load Balancer

1. **Điểm truy cập duy nhất**: Một URL để truy cập nhiều instance
2. **Chuyển đổi dự phòng tự động**: Instance không healthy tự động bị loại khỏi rotation
3. **Tính khả dụng cao**: Lưu lượng tiếp tục chảy ngay cả khi instance lỗi
4. **Giám sát sức khỏe**: Target group liên tục giám sát tình trạng instance
5. **Khôi phục tự động**: Instance tự động được thêm lại khi healthy

### Các Thực Hành Tốt Nhất

- Triển khai load balancer trên nhiều availability zone
- Cấu hình health check phù hợp
- Sử dụng security group riêng cho load balancer
- Giám sát target health thường xuyên
- Lập kế hoạch bảo trì và khôi phục instance

## Kết Luận

Bạn đã thành công:
- Tạo và cấu hình Application Load Balancer
- Thiết lập target group với hai EC2 instance
- Kiểm tra chức năng load balancing
- Xác minh cơ chế chuyển đổi dự phòng và khôi phục tự động

Application Load Balancer cung cấp một giải pháp mạnh mẽ để phân phối lưu lượng giữa nhiều target trong khi đảm bảo tính khả dụng cao và quản lý sức khỏe tự động.