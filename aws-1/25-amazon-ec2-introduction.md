# Giới Thiệu Amazon EC2

## Tổng Quan

Amazon EC2 (Elastic Compute Cloud) là một trong những dịch vụ phổ biến nhất của AWS và được sử dụng rộng rãi trong ngành công nghiệp. Nó đại diện cho phương pháp **Infrastructure as a Service (IaaS)** của AWS, cho phép bạn tạo trang web và ứng dụng đầu tiên trên AWS.

## Amazon EC2 Là Gì?

EC2 không chỉ là một dịch vụ đơn lẻ - nó được cấu thành từ nhiều thành phần hoạt động cùng nhau:

- **Máy Ảo**: Thuê các máy ảo được gọi là EC2 instances
- **Lưu Trữ**: Lưu trữ dữ liệu trên ổ đĩa ảo (EBS volumes)
- **Cân Bằng Tải**: Phân phối tải giữa các máy sử dụng Elastic Load Balancer (ELB)
- **Tự Động Mở Rộng**: Mở rộng dịch vụ sử dụng Auto Scaling Groups (ASG)

Hiểu về EC2 là nền tảng để nắm bắt cách thức hoạt động của cloud. Nguyên tắc cốt lõi của cloud là khả năng thuê tài nguyên tính toán bất cứ khi nào bạn cần, theo yêu cầu - và EC2 thể hiện hoàn hảo khái niệm này.

## Các Tùy Chọn Cấu Hình EC2 Instance

Khi tạo một EC2 instance, bạn có thể tùy chỉnh nhiều khía cạnh khác nhau:

### 1. Hệ Điều Hành
Chọn từ ba tùy chọn chính:
- **Linux** (lựa chọn phổ biến nhất)
- **Windows**
- **macOS**

### 2. Tài Nguyên Tính Toán
- **CPU**: Chọn lượng sức mạnh tính toán và số lượng lõi
- **RAM**: Chọn lượng bộ nhớ truy cập ngẫu nhiên cần thiết

### 3. Tùy Chọn Lưu Trữ
Bạn có sự linh hoạt trong việc chọn loại lưu trữ:
- **Lưu trữ gắn qua mạng**: EBS (Elastic Block Store) hoặc EFS (Elastic File System)
- **Lưu trữ gắn phần cứng**: EC2 Instance Store

### 4. Cấu Hình Mạng
- Tốc độ card mạng
- Loại địa chỉ IP công khai
- **Security Groups**: Quy tắc tường lửa cho EC2 instance của bạn

### 5. Bootstrap Script
- **EC2 User Data**: Script để cấu hình instance khi khởi động lần đầu

Sức mạnh của cloud nằm ở khả năng chọn chính xác cách bạn muốn cấu hình máy ảo và thuê nó từ AWS trong chớp mắt.

## EC2 User Data & Bootstrapping

### Bootstrapping Là Gì?

Bootstrapping đề cập đến việc thực thi các lệnh khi máy khởi động. Script EC2 User Data cho phép bạn tự động bootstrap các instances của mình.

### Đặc Điểm Chính:
- **Chỉ chạy một lần**: Thực thi khi instance khởi động lần đầu, không bao giờ chạy lại
- **Mục đích**: Tự động hóa các tác vụ khởi động
- **Quyền root**: Chạy với quyền người dùng root (quyền sudo)

### Các Tác Vụ Bootstrap Phổ Biến:
- Cài đặt các bản cập nhật hệ thống
- Cài đặt các gói phần mềm
- Tải xuống các tệp phổ biến từ internet
- Bất kỳ tác vụ cấu hình tùy chỉnh nào bạn cần

### Lưu Ý Quan Trọng:
Càng thêm nhiều tác vụ vào User Data script, instance của bạn sẽ càng mất nhiều thời gian để khởi động.

## Tóm Tắt

Amazon EC2 cung cấp một cách linh hoạt và mạnh mẽ để chạy các máy chủ ảo trên cloud. Với nhiều tùy chọn cấu hình đa dạng, từ hệ điều hành đến lưu trữ và mạng, bạn có thể điều chỉnh các instances để đáp ứng nhu cầu cụ thể của mình. Khả năng bootstrapping thông qua EC2 User Data càng tăng cường tự động hóa, giúp triển khai các instances đã được cấu hình một cách nhanh chóng hơn.

Trong các buổi thực hành sắp tới, chúng ta sẽ khám phá các khái niệm này một cách chi tiết và thực tế, xem cách làm việc trực tiếp với EC2 instances.