# AWS Elastic Beanstalk - Hướng Dẫn Thực Hành

## Giới Thiệu

Hướng dẫn này sẽ giúp bạn tạo và triển khai ứng dụng đầu tiên sử dụng dịch vụ AWS Elastic Beanstalk. Bạn sẽ học cách thiết lập môi trường web server, cấu hình các IAM roles cần thiết, và hiểu được những tài nguyên mà Beanstalk tự động tạo ra.

## Tạo Ứng Dụng Elastic Beanstalk Đầu Tiên

### Bước 1: Chọn Loại Môi Trường

1. Truy cập vào **Elastic Beanstalk console**
2. Nhấn vào **Create application**
3. Chọn giữa:
   - **Web server environment** - Để chạy website
   - **Worker environment** - Để xử lý các tác vụ từ hàng đợi (queue)

Trong hướng dẫn này, chúng ta sẽ chọn **Web server environment**.

### Bước 2: Cấu Hình Thông Tin Ứng Dụng

1. **Application name**: Nhập `My Application`
2. **Environment information**:
   - Tên môi trường: `My Application Dev` (đại diện cho môi trường phát triển của bạn)
   - Tên miền: Sẽ được tự động tạo và dùng để truy cập web servers của bạn

### Bước 3: Chọn Nền Tảng (Platform)

1. Chọn **Managed platform**
2. Chọn **Node.js** (hoặc nền tảng bạn muốn)
3. Sử dụng các tùy chọn mặc định mới nhất

> **Lưu ý**: Bạn có thể thấy các phiên bản khác so với hướng dẫn này, nhưng việc sử dụng các giá trị mặc định mới nhất sẽ đảm bảo tính tương thích.

### Bước 4: Mã Nguồn Ứng Dụng

Trong hướng dẫn này, chọn **Sample application**. Ứng dụng mẫu này sẽ phù hợp với cấu hình môi trường bạn đã chọn.

> Trong các tình huống thực tế, bạn có thể tải lên mã nguồn của riêng mình tại đây.

### Bước 5: Cấu Hình Presets

Elastic Beanstalk cung cấp ba cấu hình preset:

- **Single instance** - Đủ điều kiện cho free tier (chúng ta sẽ sử dụng cái này)
- **High availability** - Bao gồm load balancer
- **Custom configuration** - Cho tùy chỉnh nâng cao

Chọn **Single instance** để giữ mọi thứ đơn giản và nhấn **Next**.

## Cấu Hình Quyền Truy Cập Dịch Vụ

### Tạo IAM Roles

Bạn cần tạo hai IAM roles cho Elastic Beanstalk:

#### 1. Service Role

1. Nhấn vào **Create role** cho service role
2. Chọn **Elastic Beanstalk environment**
3. Nhấn **Next** qua các permission policies
4. Tên role: `AWS Elastic Beanstalk service role` (đã được điền sẵn)
5. Nhấn **Create role**
6. Quay lại Beanstalk console, làm mới và chọn role vừa tạo

#### 2. EC2 Instance Profile

1. Nhấn vào **Create role** cho EC2 instance profile
2. Chọn **Beanstalk Compute**
3. Nhấn **Next** qua các permissions (đã được thêm sẵn)
4. Nhấn **Create Role**
5. Quay lại Beanstalk console, làm mới và chọn role

### Hoàn Tất Cấu Hình

1. Để trống các trường tùy chọn
2. Bỏ qua cấu hình networking (bước 3, 4, 5) - chúng ta sẽ dùng giá trị mặc định
3. Nhấn **Skip to review** để đi thẳng đến trang xem lại
4. Xác nhận rằng cả service role và EC2 instance profile đều được chọn trong phần service access
5. Nhấn **Submit**

## Hiểu Những Gì Beanstalk Tạo Ra

### Tích Hợp CloudFormation

Khi bạn submit ứng dụng Beanstalk, các sự kiện bắt đầu xuất hiện trong phần **Events**. Các sự kiện này đến từ **AWS CloudFormation**, một dịch vụ mà Beanstalk sử dụng để cung cấp hạ tầng.

Để xem CloudFormation stack:

1. Truy cập vào **CloudFormation console**
2. Tìm Elastic Beanstalk stack của bạn
3. Nhấn vào **Events** để xem các tài nguyên đang được tạo
4. Trong **Resources**, bạn sẽ thấy:
   - Auto Scaling Group
   - Launch Configuration
   - Elastic IP
   - Security Groups
   - Và nhiều hơn nữa...

### Trực Quan Hóa Stack

1. Vào **Templates** trong CloudFormation
2. Nhấn **View in Application Composer**
3. Xem biểu diễn trực quan của tất cả các tài nguyên đang được tạo, bao gồm:
   - Launch configuration
   - Security groups
   - Elastic IP
   - Wait conditions
   - Condition handles

Trực quan hóa này giúp bạn hiểu những gì Elastic Beanstalk tạo ra đằng sau hậu trường.

## Giám Sát Quá Trình Triển Khai

### Các Tài Nguyên Được Tạo

Khi quá trình triển khai tiến triển, bạn có thể xác minh các tài nguyên trong các AWS console khác nhau:

#### EC2 Console

- Truy cập **EC2** > **Instances**
- Bạn sẽ thấy một instance **T3.micro** đang chạy
- Instance có địa chỉ IP công khai được gán

#### Elastic IPs

- Vào **EC2** > **Elastic IPs**
- Một Elastic IP đã được tạo và phân bổ cho EC2 instance của bạn

#### Auto Scaling Groups

- Truy cập **Auto Scaling Groups**
- Xem auto scaling group đang quản lý EC2 instance duy nhất của bạn
- Trong **Instance Management**, bạn sẽ thấy EC2 instance của mình

### Triển Khai Thành Công

Khi triển khai hoàn tất:
- Trạng thái hiển thị "Successfully launched"
- Trạng thái sức khỏe hiển thị "OK"
- Một tên miền được cung cấp

Nhấn vào tên miền để truy cập ứng dụng của bạn. Bạn sẽ thấy:
> "Congratulations, you are now running Elastic Beanstalk on this EC2 instance"

## Các Tính Năng Của Elastic Beanstalk

### Tùy Chọn Quản Lý Ứng Dụng

#### Tải Lên Phiên Bản Mới
- Nhấn vào **Upload and Deploy**
- Tải lên phiên bản ứng dụng mới của bạn
- Beanstalk tự động triển khai nó lên các EC2 instances

#### Giám Sát Sức Khỏe
- Xem thông tin health check cho tất cả instances
- Giám sát trạng thái và chẩn đoán instance

#### Logs
- Truy cập application logs
- Debug vấn đề và giám sát hành vi ứng dụng

#### Monitoring
- Xem các metrics cho ứng dụng của bạn
- Giám sát hiệu suất và sử dụng tài nguyên

#### Alarms
- Thiết lập CloudWatch alarms
- Nhận thông báo về các vấn đề

#### Managed Updates
- Cấu hình cập nhật platform tự động
- Giữ môi trường của bạn luôn cập nhật

#### Configuration
- Sửa đổi cấu hình môi trường
- Áp dụng thay đổi cho môi trường Beanstalk của bạn

### Nhiều Môi Trường

Trong **My Application**, bạn có thể tạo nhiều môi trường:
- **My Application Dev** - Môi trường phát triển
- **My Application Prod** - Môi trường production (tạo khi cần)

Điều này cho phép bạn quản lý các giai đoạn khác nhau trong vòng đời ứng dụng.

## Elastic Beanstalk vs CloudFormation

### Elastic Beanstalk
- Tập trung vào **mã nguồn ứng dụng** và **môi trường**
- Được thiết kế để triển khai và quản lý ứng dụng
- Trừu tượng hóa việc quản lý hạ tầng

### CloudFormation
- Được sử dụng để triển khai **infrastructure stacks**
- Làm việc với bất kỳ loại hạ tầng AWS nào
- Kiểm soát chi tiết hơn đối với tài nguyên
- Beanstalk sử dụng CloudFormation bên dưới

## Dọn Dẹp

### Khi Nào Nên Xóa Ứng Dụng

- **Giữ lại** nếu bạn đang tham gia thêm các khóa học tập trung vào Beanstalk (ví dụ: AWS Certified Developer)
- **Xóa** nếu bạn đã hoàn thành các bài giảng Beanstalk cần thiết cho kỳ thi

### Cách Xóa

1. Truy cập vào ứng dụng của bạn
2. Nhấn **Actions**
3. Chọn **Delete application**
4. Xác nhận xóa

Điều này sẽ dọn dẹp tất cả các tài nguyên được tạo bởi Beanstalk, bao gồm:
- EC2 instances
- Auto Scaling groups
- Elastic IPs
- Security groups
- CloudFormation stacks

## Tổng Kết

Trong hướng dẫn thực hành này, bạn đã học được cách:
- Tạo một ứng dụng Elastic Beanstalk
- Cấu hình web server environments
- Thiết lập IAM roles cho Beanstalk
- Hiểu các tài nguyên mà Beanstalk tự động tạo
- Giám sát triển khai thông qua CloudFormation
- Quản lý và cấu hình môi trường Beanstalk của bạn
- Dọn dẹp tài nguyên khi hoàn thành

Elastic Beanstalk đơn giản hóa việc triển khai ứng dụng bằng cách tự động xử lý việc cung cấp hạ tầng, load balancing, auto-scaling, và giám sát sức khỏe ứng dụng, cho phép bạn tập trung vào mã nguồn của mình.

---

**Bước Tiếp Theo**: Thực hành triển khai ứng dụng của riêng bạn và khám phá các tùy chọn cấu hình nâng cao khi bạn trở nên quen thuộc hơn với Elastic Beanstalk.