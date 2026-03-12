# Tổng Quan về AWS Auto Scaling Groups (ASG)

## Giới Thiệu

Khi triển khai một website hoặc ứng dụng, tải có thể thay đổi theo thời gian khi có nhiều người dùng truy cập website của bạn hơn. Trong AWS, chúng ta có thể tạo và xóa server rất nhanh chóng bằng cách sử dụng API call tạo EC2 instance. Để tự động hóa quy trình này, chúng ta có thể sử dụng Auto Scaling Groups (ASG).

## Auto Scaling Group là gì?

Auto Scaling Group là một dịch vụ AWS tự động điều chỉnh số lượng EC2 instances trong ứng dụng của bạn dựa trên nhu cầu.

### Mục Tiêu Chính của ASG

- **Scale Out (Mở rộng)**: Thêm EC2 instances để đáp ứng tải tăng cao
- **Scale In (Thu hẹp)**: Xóa bớt EC2 instances khi tải giảm
- Kích thước ASG của bạn thay đổi theo thời gian dựa trên nhu cầu

## Các Tính Năng Chính

### 1. Quản Lý Dung Lượng

Bạn có thể định nghĩa các tham số để đảm bảo có:
- Số lượng **tối thiểu** EC2 instances chạy mọi lúc
- Số lượng **tối đa** EC2 instances có thể chạy
- **Dung lượng mong muốn** để đạt hiệu suất tối ưu

### 2. Tích Hợp với Load Balancer

ASG có khả năng tích hợp mạnh mẽ với load balancer:
- Bất kỳ EC2 instances nào trong ASG đều tự động được liên kết với load balancer
- Traffic được phân phối đều trên tất cả các instances
- Cung cấp trải nghiệm người dùng liền mạch

### 3. Giám Sát Sức Khỏe và Tự Động Phục Hồi

- Nếu một instance được coi là không khỏe mạnh, nó sẽ tự động bị chấm dứt
- Một EC2 instance mới được tạo để thay thế instance không khỏe mạnh
- Đảm bảo tính sẵn sàng cao cho ứng dụng của bạn

### 4. Tiết Kiệm Chi Phí

- Bản thân Auto Scaling Groups là **miễn phí**
- Bạn chỉ trả tiền cho các tài nguyên được tạo bên dưới (EC2 instances)

## Cách Hoạt Động của ASG

### Cấu Hình Dung Lượng

1. **Dung Lượng Tối Thiểu**: Số lượng instances tối thiểu bạn muốn trong ASG (ví dụ: 2)
2. **Dung Lượng Mong Muốn**: Số lượng instances bạn muốn chạy (ví dụ: 4)
3. **Dung Lượng Tối Đa**: Số lượng instances tối đa được phép (ví dụ: 7)

Khi bạn điều chỉnh dung lượng mong muốn lên cao hơn (nhưng vẫn nhỏ hơn dung lượng tối đa), ASG của bạn có thể mở rộng bằng cách thêm nhiều EC2 instances hơn.

### Tích Hợp với Load Balancers

Khi bạn có các instances được đăng ký trong ASG:
- Elastic Load Balancer (ELB) phân phối traffic đến tất cả các instances
- Người dùng có thể truy cập website được cân bằng tải
- ELB thực hiện kiểm tra sức khỏe trên các EC2 instances
- Kết quả kiểm tra sức khỏe được chuyển đến ASG
- Các instances không khỏe mạnh tự động bị chấm dứt và thay thế

Sự kết hợp giữa load balancer và auto scaling group này cực kỳ mạnh mẽ để duy trì tính khả dụng và hiệu suất của ứng dụng.

## Tạo Auto Scaling Group

### Launch Template (Mẫu Khởi Chạy)

Để tạo một ASG, bạn cần một **launch template** (lưu ý: launch configurations đã lỗi thời nhưng hoạt động tương tự).

Launch template chứa thông tin về cách khởi chạy EC2 instances trong ASG của bạn:

- **AMI** (Amazon Machine Image)
- **Loại Instance**
- **EC2 User Data**
- **EBS Volumes**
- **Security Groups**
- **SSH Key Pair**
- **IAM Roles** cho EC2 instances
- **Thông Tin Network và Subnet**
- **Thông Tin Load Balancer**

Các tham số này tương tự như những tham số được chỉ định khi tạo một EC2 instance độc lập.

### Các Tham Số ASG Bổ Sung

- Kích thước tối thiểu
- Kích thước tối đa
- Dung lượng ban đầu
- Chính sách mở rộng (scaling policies)

## Auto Scaling với CloudWatch

### Tích Hợp CloudWatch Alarm

Auto Scaling Groups có thể thu hẹp và mở rộng dựa trên CloudWatch alarms. Điều này cho phép thực sự tự động hóa việc mở rộng cơ sở hạ tầng của bạn.

### Cách Hoạt Động

1. Bạn thiết lập CloudWatch alarms dựa trên các metrics (ví dụ: mức sử dụng CPU trung bình)
2. Khi ngưỡng metric bị vượt qua, alarm được kích hoạt
3. Alarm kích hoạt một hoạt động mở rộng trong ASG của bạn
4. Instances được thêm hoặc xóa tự động

### Ví Dụ Tình Huống

- ASG của bạn có 3 EC2 instances đang chạy
- Mức sử dụng CPU trung bình trên ASG tăng vượt ngưỡng
- CloudWatch alarm được kích hoạt
- Chính sách scale-out được kích hoạt
- Các EC2 instances bổ sung được khởi chạy tự động

### Chính Sách Mở Rộng

- **Chính Sách Scale Out**: Tăng số lượng instances khi nhu cầu cao
- **Chính Sách Scale In**: Giảm số lượng instances khi nhu cầu thấp

Việc tự động mở rộng kết hợp với alarms này chính là lý do tại sao nó được gọi là "Auto" Scaling Group.

## Tóm Tắt

Auto Scaling Groups cung cấp:
- Tự động điều chỉnh dung lượng dựa trên nhu cầu
- Tối ưu hóa chi phí bằng cách chỉ chạy các instances cần thiết
- Tính sẵn sàng cao thông qua giám sát sức khỏe và tự động phục hồi
- Tích hợp liền mạch với load balancers
- Tự động hóa thông qua CloudWatch alarms và chính sách mở rộng

Tất cả các tính năng này cùng nhau tạo thành một giải pháp mạnh mẽ để chạy các ứng dụng có khả năng mở rộng và sẵn sàng cao trong AWS.

---

*Hướng dẫn này cung cấp tổng quan về AWS Auto Scaling Groups và sự tích hợp của chúng với các dịch vụ AWS khác như EC2, ELB và CloudWatch.*