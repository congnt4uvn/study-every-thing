# AWS Auto Scaling Groups - Hướng Dẫn Thực Hành

## Giới Thiệu

Hướng dẫn thực hành này sẽ giúp bạn tạo và quản lý AWS Auto Scaling Groups (ASG). Bạn sẽ học cách tạo launch templates, cấu hình các thiết lập ASG, tích hợp với Application Load Balancers, và trải nghiệm tính năng auto scaling trong thực tế.

## Yêu Cầu Trước Khi Bắt Đầu

Trước khi bắt đầu hướng dẫn này:
- Terminate (chấm dứt) tất cả EC2 instances đang chạy để bắt đầu từ đầu
- Đảm bảo bạn có không có instance nào đang chạy trong EC2

## Bước 1: Tạo Auto Scaling Group

1. Điều hướng đến **Auto Scaling Groups** ở menu bên trái
2. Nhấp **Create Auto Scaling Group**
3. Đặt tên cho ASG của bạn: `Demo ASG`

## Bước 2: Tạo Launch Template

Vì chúng ta cần tham chiếu đến một launch template, hãy tạo một cái:

### Cấu Hình Cơ Bản

1. Nhấp **Create a launch template**
2. **Tên template**: `my demo template`
3. **Mô tả**: `templates`

### Cấu Hình Instance

1. **Amazon Machine Image (AMI)**:
   - Vào Quick Start
   - Chọn **Amazon Linux**
   - Chọn **Amazon Linux 2** (phiên bản X86)
   - Sử dụng AMI đủ điều kiện free tier

2. **Instance Type**:
   - Chọn **t2.micro** (đủ điều kiện free tier)

3. **Key Pair**:
   - Bao gồm key pair **EC2 tutorial**

4. **Security Group**:
   - Chọn một security group đã tồn tại (ví dụ: `launch-wizard-1`)
   - Lưu ý: Subnets không được bao gồm trong launch templates

5. **Storage (Lưu trữ)**:
   - Mặc định: 8 GB gp2 volume

### Chi Tiết Nâng Cao - User Data

1. Cuộn xuống **Advanced Details**
2. Tìm phần **User Data**
3. Nhập script user data của bạn (script này sẽ tạo web server trên mỗi EC2 instance)

```bash
#!/bin/bash
# Script user data của bạn ở đây
# Script này sẽ bootstrap một web server trên mỗi instance
```

4. Nhấp **Create launch template**

## Bước 3: Cấu Hình Auto Scaling Group

### Chọn Launch Template

1. Làm mới danh sách template
2. Chọn `my demo template` (version 1)
3. Xem lại tóm tắt
4. Nhấp **Next**

### Tùy Chọn Khởi Chạy Instance

1. **Instance Type Requirements**:
   - Giữ nguyên t2.micro mặc định từ launch template
   - Reset về launch template nếu cần

2. **Cấu Hình Network**:
   - Chọn VPC của bạn
   - Chọn nhiều Availability Zones
   - **AZ Distribution**: Balanced best effort (đảm bảo instances được phân bổ đều trên 3 AZs)

### Tích Hợp Load Balancer

1. **Gắn vào Load Balancer**:
   - Chọn "Attach to an existing load balancer target group"
   - Chọn `demo tg alb` (target group đã tạo trước đó)
   - Điều này gắn tất cả instances của ASG vào load balancer

2. Bỏ qua VPC Lattice integration và zonal shift settings

### Health Checks (Kiểm Tra Sức Khỏe)

Bật cả hai:
- **EC2 health checks**
- **Load balancer health checks**

Điều này cho phép ALB kiểm tra sức khỏe của instance, và ASG có thể tự động terminate các instances không khỏe mạnh.

## Bước 4: Cấu Hình Kích Thước Group và Scaling

1. **Desired capacity** (Dung lượng mong muốn): 1
2. **Minimum capacity** (Dung lượng tối thiểu): 1
3. **Maximum capacity** (Dung lượng tối đa): 1

Tạm thời, chúng ta sẽ để automatic scaling ở chế độ tắt để khám phá nó sau.

## Bước 5: Cài Đặt Bổ Sung

1. **Instance maintenance policy**: No policy
2. **Additional capacity settings**: Sử dụng mặc định
3. Bỏ qua notifications và tags
4. Xem lại tất cả các tùy chọn
5. Nhấp **Create Auto Scaling Group**

## Bước 6: Giám Sát Hoạt Động ASG

### Lịch Sử Hoạt Động (Activity History)

1. Nhấp vào Auto Scaling Group của bạn
2. Vào tab **Activity**
3. Làm mới để xem lịch sử hoạt động
4. Bạn sẽ thấy: "Launching a new instance" vì dung lượng là 0 và desired là 1

### Quản Lý Instance

1. Vào tab **Instance Management**
2. Xác minh rằng một EC2 instance đã được tạo bởi ASG
3. Điều hướng đến **EC2 Instances** để xem instance đang chạy

### Đăng Ký Target Group

1. Vào **Target Groups** (menu bên trái)
2. Tìm target group của bạn
3. Vào tab **Targets**
4. Ban đầu hiển thị **unhealthy** (instance vẫn đang bootstrapping)
5. Sau khi bootstrapping hoàn tất, trạng thái chuyển sang **healthy**

### Kiểm Tra Load Balancer

1. Điều hướng đến Application Load Balancer của bạn
2. Sao chép DNS name và mở trong trình duyệt
3. Bạn nên thấy phản hồi "Hello World"
4. Điều này xác nhận toàn bộ cài đặt đang hoạt động:
   - Instance được tạo bởi ASG ✓
   - Đã đăng ký trong target group ✓
   - Load balancer đang định tuyến traffic ✓

## Khắc Phục Sự Cố Instance Không Khỏe Mạnh

Nếu instance của bạn không bao giờ trở nên healthy:

**Vấn Đề Thường Gặp**:
1. **Security Group cấu hình sai**: Kiểm tra inbound/outbound rules
2. **Vấn đề EC2 User Data script**: Xác minh cú pháp và logic của script

ASG sẽ tự động terminate các instances không khỏe mạnh và tạo instances mới. Kiểm tra Activity History để xem các sự kiện này.

## Bước 7: Trải Nghiệm Scale Out (Mở Rộng)

### Tăng Dung Lượng

1. **Edit Auto Scaling Group size**
2. Đặt **Desired capacity**: 2
3. Đặt **Maximum capacity**: 2
4. Nhấp **Update**

### Giám Sát Hoạt Động Scaling

1. Vào **Activity History**
2. Làm mới để xem hoạt động mới
3. Bạn sẽ thấy: "Launching a new EC2 instance" vì desired capacity thay đổi từ 1 lên 2
4. Instance thứ hai sẽ được tạo và đăng ký vào target group

### Xác Minh Phân Phối Tải

1. Đợi instance mới trở nên healthy
2. Điều hướng đến DNS name của ALB
3. Làm mới nhiều lần
4. Bạn sẽ thấy hai địa chỉ IP khác nhau luân phiên
5. Điều này xác nhận load balancing trên cả hai instances

## Bước 8: Trải Nghiệm Scale In (Thu Hẹp)

### Giảm Dung Lượng

1. **Edit Auto Scaling Group size**
2. Đặt **Desired capacity**: 1
3. Nhấp **Update**

### Giám Sát Việc Terminate

1. Vào **Activity History**
2. Bạn sẽ thấy thông báo: "Terminating instance"
3. ASG sẽ:
   - Chọn một trong hai instances
   - Terminate nó
   - Hủy đăng ký khỏi target group
4. Bạn quay lại với một EC2 instance

## Tóm Tắt

Trong hướng dẫn thực hành này, bạn đã học:

- ✓ Cách tạo và cấu hình Launch Templates
- ✓ Cách tạo Auto Scaling Groups
- ✓ Cách tích hợp ASG với Application Load Balancers
- ✓ Cách cấu hình health checks
- ✓ Cách scale out thủ công (tăng dung lượng)
- ✓ Cách scale in thủ công (giảm dung lượng)
- ✓ Cách ASG tự động quản lý vòng đời của instance

## Các Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ khám phá **automatic scaling** - nơi ASG tự động điều chỉnh dung lượng dựa trên nhu cầu mà không cần can thiệp thủ công.

---

**Những Điểm Chính Cần Nhớ**:
- Auto Scaling Groups cung cấp tính khả dụng cao và khả năng chịu lỗi
- Launch Templates định nghĩa cách instances nên được cấu hình
- Tích hợp với ALB cho phép phân phối traffic một cách liền mạch
- ASG tự động thay thế các instances không khỏe mạnh
- Manual scaling thể hiện sức mạnh của ASG trước khi tự động hóa nó