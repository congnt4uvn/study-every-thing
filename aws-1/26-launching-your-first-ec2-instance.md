# Khởi Chạy EC2 Instance Đầu Tiên Của Bạn

## Giới Thiệu

Trong hướng dẫn này, chúng ta sẽ khởi chạy EC2 instance đầu tiên chạy Amazon Linux. Bạn sẽ được tìm hiểu tổng quan về các tham số khác nhau khi khởi chạy một EC2 instance, và chúng ta sẽ triển khai một web server trực tiếp trên instance bằng cách sử dụng user data.

## Yêu Cầu Trước

- Tài khoản AWS có quyền truy cập vào EC2 Console
- Hiểu biết cơ bản về điện toán đám mây

## Hướng Dẫn Từng Bước

### 1. Truy Cập EC2 Console

1. Điều hướng đến **EC2 Console**
2. Nhấp vào **Instances**
3. Nhấp vào **Launch Instances**

### 2. Cấu Hình Tên và Tags cho Instance

- Nhập tên cho instance của bạn: `My First Instance`
- Điều này tạo ra một name tag cho instance
- Bạn có thể thêm các tag bổ sung nếu cần, nhưng name tag là đủ cho hiện tại

### 3. Chọn Amazon Machine Image (AMI)

1. Chọn **Amazon Linux 2 AMI** từ các tùy chọn Quick Start
2. AMI này được **free tier eligible** (đủ điều kiện miễn phí)
3. Chọn kiến trúc: **64-bit x86**
4. AWS cung cấp các image này làm quick starts để dễ dàng triển khai

### 4. Chọn Instance Type

- Chọn **t2.micro** (đủ điều kiện miễn phí)
- Instance type này cung cấp:
  - Công suất CPU đủ cho các workload cơ bản
  - Bộ nhớ đủ để test và phát triển
  - 750 giờ miễn phí mỗi tháng trong năm đầu tiên (tương đương chạy 24/7 trong một tháng)
- Nếu t2.micro không có sẵn ở region của bạn, t3.micro sẽ được đề xuất thay thế

**Lưu ý:** Bạn có thể so sánh các instance type khác nhau bằng cách nhấp vào link so sánh, hiển thị các cấu hình khác nhau với CPU, memory và giá cả khác nhau.

### 5. Tạo Key Pair để Truy Cập SSH

Key pair cần thiết để truy cập an toàn vào instance của bạn qua SSH.

1. Nhấp **Create a new key pair**
2. Đặt tên: `EC2 Tutorial`
3. Key pair type: **RSA**
4. Key pair format:
   - **PEM format**: Cho Mac, Linux, hoặc Windows 10+
   - **PPK format**: Cho Windows 7 hoặc Windows 8 (sử dụng với PuTTY)
5. Nhấp **Create** - key pair sẽ được tải xuống tự động

### 6. Cấu Hình Network Settings

#### Cấu Hình Security Group

Security group hoạt động như một tường lửa ảo kiểm soát lưu lượng đến và đi từ instance của bạn.

1. Console sẽ tạo một security group có tên `launch-wizard-1`
2. Cấu hình các inbound rule sau:
   - **Allow SSH traffic from anywhere** (Port 22) - để truy cập từ xa
   - **Allow HTTP traffic from the internet** (Port 80) - để truy cập web server
3. HTTPS không cần thiết cho hướng dẫn này
4. Instance của bạn sẽ nhận được public IP address tự động

### 7. Cấu Hình Storage

- Mặc định: **8 GB gp2 root volume**
- Free tier bao gồm tới **30 GB EBS general purpose SSD storage**
- **Delete on termination**: Được bật theo mặc định (volume sẽ bị xóa khi instance bị terminate)

### 8. Thêm User Data Script

User data cho phép bạn chạy các lệnh khi khởi chạy lần đầu tiên EC2 instance.

1. Cuộn xuống **Advanced details**
2. Tìm phần **User data** ở cuối
3. Dán script sau:

```bash
#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd
echo "<h1>Hello World from $(hostname -f)</h1>" > /var/www/html/index.html
```

**Script này làm gì:**
- Cập nhật các gói hệ thống
- Cài đặt Apache HTTP web server
- Khởi động và kích hoạt web server
- Tạo một file HTML đơn giản hiển thị "Hello World"

**Quan trọng:** Script này chỉ thực thi một lần trong lần khởi chạy đầu tiên của instance.

### 9. Review và Launch

1. Xem xét instance summary:
   - 1 instance loại t2.micro
   - Đủ điều kiện free tier (750 giờ mỗi tháng)
   - 30 GB EBS storage được bao gồm
2. Nhấp **Launch Instance**
3. Nhấp **View all Instances**

## Hiểu Về Instance Của Bạn

### Các Trạng Thái Instance

Instance của bạn sẽ trải qua nhiều trạng thái:

1. **Pending**: Instance đang được khởi chạy (mất 10-15 giây)
2. **Running**: Instance đang hoạt động và có thể truy cập
3. **Stopping**: Instance đang tắt
4. **Stopped**: Instance đã dừng (không tính phí compute, nhưng storage vẫn tính phí)
5. **Terminated**: Instance bị xóa vĩnh viễn

### Chi Tiết Instance

Khi instance đang chạy, bạn sẽ thấy:

- **Instance Name**: My First Instance
- **Instance ID**: Định danh duy nhất cho instance của bạn
- **Public IPv4 Address**: Được sử dụng để truy cập instance từ internet
- **Private IPv4 Address**: Được sử dụng cho giao tiếp mạng nội bộ AWS
- **Instance Type**: t2.micro
- **AMI**: Amazon Linux 2
- **Key Pair**: EC2 Tutorial

### Thông Tin Security Group

- **Name**: launch-wizard-1
- **Inbound Rules**:
  - Port 22 (SSH): Có thể truy cập từ mọi nơi
  - Port 80 (HTTP): Có thể truy cập từ mọi nơi
- **Outbound Rules**: Tất cả giao tiếp được cho phép (cho phép truy cập internet)

### Thông Tin Storage

- **Một volume**: 8 GB được gắn vào instance

## Truy Cập Web Server Của Bạn

### Phương Pháp 1: Sử Dụng Console

1. Tìm **Public IPv4 Address** trong chi tiết instance
2. Nhấp **Open Address** hoặc sao chép IP

### Phương Pháp 2: Nhập Thủ Công

1. Sao chép public IPv4 address
2. Mở trình duyệt web
3. Nhập: `http://[YOUR-PUBLIC-IP]`

**Quan trọng:** Đảm bảo sử dụng `http://` và KHÔNG dùng `https://`. Sử dụng HTTPS sẽ dẫn đến màn hình loading vô tận vì chúng ta chưa cấu hình SSL.

### Kết Quả Mong Đợi

Bạn sẽ thấy một trang hiển thị:
```
Hello World from [PRIVATE-IP-ADDRESS]
```

**Lưu ý:** IP được hiển thị là private IPv4 address, không phải public IP được sử dụng để truy cập trang.

### Xử Lý Sự Cố

Nếu trang không tải ngay lập tức:
- Đợi 5 phút để user data script hoàn thành
- Làm mới trang
- Xác minh bạn đang sử dụng `http://` không phải `https://`
- Kiểm tra trạng thái instance là "Running"

## Quản Lý Instance Của Bạn

### Dừng Instance

**Khi nào nên dừng:** Để tránh phí khi bạn không cần instance chạy.

1. Chọn instance của bạn
2. Đi tới **Instance State** → **Stop Instance**
3. Instance chuyển sang trạng thái "Stopping"
4. Khi đã dừng, bạn sẽ không bị tính phí cho thời gian compute (phí storage vẫn áp dụng)

**Quan trọng:** Khi bạn dừng rồi khởi động lại instance, public IPv4 address có thể thay đổi. Private IPv4 address vẫn giữ nguyên.

### Khởi Động Instance Đã Dừng

1. Chọn instance đã dừng của bạn
2. Đi tới **Instance State** → **Start Instance**
3. Đợi instance chuyển sang trạng thái "Running"
4. Ghi chú public IPv4 address mới
5. Truy cập web server của bạn bằng IP mới

### Terminate Instance

**Cảnh báo:** Terminate sẽ xóa vĩnh viễn instance và root volume của nó.

1. Chọn instance của bạn
2. Đi tới **Instance State** → **Terminate Instance**
3. Xác nhận hành động trong hộp thoại cảnh báo

**Hành động này không thể hoàn tác.**

## Những Điểm Chính Cần Nhớ

1. **Sức Mạnh Đám Mây**: Bạn có thể tạo instance trong vài giây mà không cần sở hữu server vật lý
2. **Khả Năng Mở Rộng**: Bạn có thể khởi chạy 1 hoặc 100 instance dễ dàng như nhau
3. **Linh Hoạt**: Start, stop và terminate instance theo nhu cầu
4. **Kiểm Soát Chi Phí**: Chỉ trả tiền cho các instance đang chạy (dừng khi không sử dụng)
5. **User Data**: Tự động hóa thiết lập ban đầu bằng script
6. **IP Động**: Public IPv4 address có thể thay đổi sau khi stop/start (private IP giữ nguyên)
7. **Free Tier**: 750 giờ t2.micro mỗi tháng trong năm đầu tiên

## Best Practices (Thực Hành Tốt Nhất)

- **Sử Dụng Tags**: Tag các instance để tổ chức và theo dõi chi phí tốt hơn
- **Bảo Mật**: Hạn chế truy cập SSH cho các IP range cụ thể trong môi trường production
- **Dừng Khi Không Dùng**: Dừng instance khi không sử dụng để giảm chi phí
- **Quản Lý Key**: Giữ các file private key của bạn an toàn
- **Cập Nhật Thường Xuyên**: Giữ instance của bạn được cập nhật với các bản vá bảo mật mới nhất

## Cân Nhắc Chi Phí

- **Free Tier**: 750 giờ t2.micro hàng tháng (12 tháng đầu)
- **Storage**: 30 GB EBS storage được bao gồm trong free tier
- **Stopped Instance**: Không có phí compute, nhưng phí storage vẫn áp dụng
- **Truyền Dữ Liệu**: Theo dõi truyền dữ liệu outbound để quản lý chi phí

## Bước Tiếp Theo

- Tìm hiểu về Elastic IP (địa chỉ public IP tĩnh)
- Khám phá các instance type khác nhau cho các workload khác nhau
- Hiểu về các mô hình định giá EC2 instance
- Thiết lập truy cập SSH vào instance của bạn
- Cấu hình các security group rule nâng cao

## Kết Luận

Bạn đã khởi chạy thành công EC2 instance đầu tiên và triển khai một web server! Điều này chứng minh sức mạnh cơ bản của điện toán đám mây: cung cấp nhanh chóng, linh hoạt và định giá theo mức sử dụng. Bây giờ bạn có thể start, stop và terminate instance bằng các API call đơn giản, cho bạn quyền kiểm soát hoàn toàn hạ tầng đám mây của mình.

---

*Hướng dẫn này là một phần của loạt bài AWS EC2 fundamentals.*