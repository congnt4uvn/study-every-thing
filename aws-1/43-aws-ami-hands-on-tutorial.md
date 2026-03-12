# AWS AMI - Hướng Dẫn Thực Hành

## Tổng Quan

Hướng dẫn này trình bày cách tạo và sử dụng Amazon Machine Images (AMIs) để lưu và tái sử dụng cấu hình EC2 instance, giảm thời gian khởi động và chuẩn hóa việc triển khai.

## Yêu Cầu Trước Khi Bắt Đầu

- Tài khoản AWS có quyền truy cập EC2
- Security group đã tồn tại (ví dụ: launch-wizard-1)
- Hiểu biết cơ bản về EC2 instances

## Phần 1: Tạo EC2 Instance với User Data

### Bước 1: Khởi Chạy EC2 Instance

1. Truy cập vào EC2 console và khởi chạy instance mới
2. Chọn **Amazon Linux 2** làm AMI
3. Chọn loại instance **t2.micro**
4. Chọn key pair của bạn (hoặc bỏ qua nếu không cần cho demo này)

### Bước 2: Cấu Hình Network Settings

1. Cuộn xuống phần network settings
2. Nhấp **Edit**
3. Chọn security group đã tồn tại (ví dụ: launch-wizard-1)

### Bước 3: Thêm User Data Script

1. Cuộn đến **Advanced Details**
2. Trong phần **User Data**, thêm script sau (không bao gồm dòng cuối):

```bash
#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd
# Lưu ý: Chúng ta KHÔNG tạo file index.html ở đây
```

**Quan trọng:** Sao chép mọi thứ ngoại trừ dòng cuối cùng. Chúng ta đang cài đặt Apache web server (HTTPD) nhưng chưa tạo file index. Điều này cho phép chúng ta tạo một AMI sạch với web server đã được cài đặt sẵn.

### Bước 4: Khởi Chạy và Chờ Đợi

1. Nhấp **Launch Instance**
2. Đợi instance đạt trạng thái "running"
3. **Hãy kiên nhẫn** - ngay cả khi trạng thái hiển thị "running", user data script cần 1-2 phút để hoàn thành

### Bước 5: Xác Minh Cài Đặt

1. Sao chép địa chỉ **Public IPv4**
2. Mở trình duyệt và truy cập `http://[địa-chỉ-ip-công-khai-của-bạn]`
3. Bạn sẽ thấy trang test Apache sau 2 phút
4. Nếu bạn thấy lỗi kết nối, hãy đợi thêm một chút để user data script hoàn tất

## Phần 2: Tạo AMI

### Bước 1: Tạo AMI

1. Nhấp chuột phải vào instance đang chạy
2. Chọn **Image and templates** > **Create image**
3. Đặt tên là `demo-image`
4. Giữ nguyên các thiết lập mặc định
5. Nhấp **Create image**

### Bước 2: Theo Dõi Quá Trình Tạo AMI

1. Điều hướng đến **AMIs** trong menu bên trái
2. Bạn sẽ thấy AMI của mình với trạng thái "pending"
3. Đợi trạng thái chuyển sang "available"

## Phần 3: Khởi Chạy Instance từ AMI Của Bạn

### Bước 1: Khởi Chạy từ AMI

1. Nhấp vào AMI của bạn và chọn **Launch instance from AMI**
2. Hoặc vào **Launch Instance** và chọn tab **My AMIs**
3. Chọn AMI `demo-image` của bạn

### Bước 2: Cấu Hình Instance Mới

1. Chọn key pair của bạn (tùy chọn)
2. Chỉnh sửa network settings và chọn security group đã có
3. Cuộn đến **Advanced Details** > **User Data**

### Bước 3: Thêm User Data Tối Thiểu

Vì HTTPD đã được cài đặt trong AMI, chúng ta chỉ cần tạo file index:

```bash
#!/bin/bash
echo "<h1>Hello World from $(hostname -f)</h1>" > /var/www/html/index.html
```

**Điểm Quan Trọng:** Chúng ta không cần cài đặt lại HTTPD vì nó đã có sẵn trong AMI. Điều này giảm đáng kể thời gian khởi động.

### Bước 4: Khởi Chạy và Xác Minh

1. Khởi chạy instance
2. Đợi nó đạt trạng thái "running"
3. Sao chép địa chỉ IP công khai
4. Truy cập `http://[địa-chỉ-ip-công-khai-của-bạn]`
5. Bạn sẽ thấy "Hello World" nhanh hơn nhiều so với trước

## Lợi Ích Của Việc Sử Dụng AMIs

### Tốc Độ
- **Thời gian khởi động nhanh hơn** - Phần mềm đã cài đặt sẵn không cần cài lại
- Trong demo này, instance thứ hai nhanh hơn nhiều vì HTTPD đã được cài đặt sẵn

### Chuẩn Hóa
- Đóng gói phần mềm bảo mật, dependencies và cấu hình
- Tạo golden image cho việc triển khai nhất quán
- Giảm sự khác biệt cấu hình giữa các instances

### Trường Hợp Sử Dụng
- Cài đặt phần mềm tiên quyết mất 2-3 phút
- Đóng gói thành AMI
- Khởi chạy instances mới từ AMI
- Thêm tùy chỉnh tối thiểu ở cuối
- Đạt được thời gian triển khai nhanh hơn nhiều

## Dọn Dẹp

1. Điều hướng đến EC2 instances của bạn
2. Chọn cả hai instances (instance gốc và instance từ AMI)
3. Nhấp **Instance State** > **Terminate**
4. Xác nhận terminate

## Những Điểm Chính Cần Nhớ

- AMIs lưu trạng thái hoàn chỉnh của một EC2 instance
- User data scripts chạy khi khởi động lần đầu để tùy chỉnh instances
- AMIs giảm đáng kể thời gian khởi động bằng cách cài đặt sẵn phần mềm
- AMIs lý tưởng để tạo các triển khai chuẩn hóa, có thể lặp lại
- Luôn đợi user data scripts hoàn thành trước khi kiểm tra

## Các Bước Tiếp Theo

- Khám phá việc tạo AMIs với các software stacks phức tạp hơn
- Tìm hiểu về chia sẻ AMI và quyền hạn
- Nghiên cứu tự động tạo AMI với AWS Systems Manager
- Thực hành với các bản phân phối Linux và cấu hình khác nhau