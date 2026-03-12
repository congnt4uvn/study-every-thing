# Amazon EFS - Hệ Thống Tệp Đàn Hồi

## Tổng Quan

Amazon EFS (Elastic File System) là một hệ thống NFS (Network File System) được quản lý, cung cấp lưu trữ tệp có khả năng mở rộng và tính sẵn sàng cao cho các EC2 instance trên nhiều vùng sẵn sàng.

### Đặc Điểm Chính

- **Tính Sẵn Sàng Cao**: Có thể truy cập qua nhiều vùng sẵn sàng
- **Khả Năng Mở Rộng**: Tự động mở rộng mà không cần lập kế hoạch dung lượng
- **Chi Phí Cao**: Khoảng gấp 3 lần chi phí của EBS volume GP2
- **Trả Theo Sử Dụng**: Không cần cấp phát dung lượng trước

## Kiến Trúc

Hệ thống tệp EFS được bảo vệ bởi security groups và có thể được mount đồng thời bởi nhiều EC2 instance trên các vùng sẵn sàng khác nhau:

- EC2 instances trong US-EAST-1A
- EC2 instances trong US-EAST-1B
- EC2 instances trong US-EAST-1C

Tất cả các instance có thể kết nối đồng thời với cùng một hệ thống tệp mạng thông qua EFS.

## Trường Hợp Sử Dụng

- Quản lý nội dung
- Web serving
- Chia sẻ dữ liệu
- Hosting WordPress

## Yêu Cầu Kỹ Thuật

### Giao Thức và Tương Thích

- **Giao Thức**: NFS (Network File System)
- **Kiểm Soát Truy Cập**: Security groups
- **Tương Thích HĐH**: Chỉ hỗ trợ Linux-based AMI (không tương thích với Windows)
- **Mã Hóa**: Hỗ trợ mã hóa dữ liệu nghỉ bằng KMS
- **Hệ Thống Tệp**: Tuân thủ POSIX với API tệp chuẩn

### Tự Động Mở Rộng

- Không cần lập kế hoạch dung lượng
- Hệ thống tệp tự động mở rộng
- Thanh toán theo mức sử dụng mỗi gigabyte

## Hiệu Năng và Quy Mô

### Khả Năng Mở Rộng

- **Client Đồng Thời**: Hàng nghìn NFS client
- **Throughput**: 10+ GB/s
- **Kích Thước Tối Đa**: Quy mô petabyte (tăng trưởng tự động)

### Chế Độ Hiệu Năng

Được thiết lập khi tạo EFS:

#### 1. General Purpose (Mặc Định)
- Tối ưu cho các trường hợp nhạy cảm về độ trễ
- Lý tưởng cho: Web server, ứng dụng CMS

#### 2. Max I/O
- Độ trễ cao nhưng throughput cao hơn
- Xử lý song song cao
- Lý tưởng cho: Ứng dụng big data, xử lý media

### Chế Độ Throughput

#### 1. Bursting (Bùng Nổ)
- Baseline: 50 MB/s cho mỗi TB lưu trữ
- Burst: Lên đến 100 MB/s
- Throughput tăng theo dung lượng lưu trữ

#### 2. Provisioned (Cấp Phát)
- Thiết lập throughput độc lập với dung lượng lưu trữ
- Ví dụ: 1 GB/s cho 1 TB lưu trữ
- Tách biệt throughput khỏi dung lượng lưu trữ

#### 3. Elastic (Khuyến nghị cho workload không dự đoán được)
- Tự động điều chỉnh throughput dựa trên workload
- Lên đến 3 GB/s cho đọc
- Lên đến 1 GB/s cho ghi
- Hoàn hảo cho workload không dự đoán được

## Lớp Lưu Trữ

### Các Tầng Lưu Trữ

EFS cung cấp quản lý vòng đời để tự động di chuyển tệp giữa các tầng lưu trữ:

#### 1. Standard Tier (Tầng Chuẩn)
- Dành cho các tệp được truy cập thường xuyên
- Chi phí cao hơn nhưng truy cập ngay lập tức

#### 2. EFS-IA (Infrequent Access - Truy Cập Không Thường Xuyên)
- Chi phí lưu trữ thấp hơn
- Chi phí theo lượt truy xuất
- Dành cho tệp được truy cập ít thường xuyên

#### 3. Archive Storage Tier (Tầng Lưu Trữ)
- Dành cho dữ liệu hiếm khi truy cập (vài lần mỗi năm)
- Chi phí lưu trữ thấp nhất
- Lý tưởng cho lưu trữ dài hạn

### Chính Sách Vòng Đời

Tự động di chuyển tệp giữa các tầng lưu trữ dựa trên mẫu truy cập:

**Ví dụ**: Các tệp trong EFS Standard không được truy cập trong 60 ngày có thể tự động chuyển sang tầng EFS-IA.

## Tính Sẵn Sàng và Độ Bền

### Standard (Multi-AZ - Đa Vùng)
- EFS trên nhiều vùng sẵn sàng
- Khuyến nghị cho workload production
- Kiến trúc chống thảm họa

### One Zone (Một Vùng)
- Chỉ một vùng sẵn sàng
- Tùy chọn chi phí thấp hơn
- Phù hợp cho môi trường phát triển
- Vẫn bao gồm chức năng backup
- Tương thích với tầng lưu trữ IA (EFS One Zone-IA)

## Tiết Kiệm Chi Phí

Bằng cách triển khai đúng sự kết hợp giữa các lớp lưu trữ và chính sách vòng đời, bạn có thể đạt được:

**Tiết kiệm lên đến 90% chi phí**

## Tóm Tắt

Amazon EFS cung cấp một hệ thống tệp mạng được quản lý, có khả năng mở rộng cao và có thể được chia sẻ trên nhiều EC2 instance trong các vùng sẵn sàng khác nhau. Mặc dù đắt hơn EBS, khả năng tự động mở rộng, mô hình trả theo sử dụng và các tùy chọn hiệu năng linh hoạt khiến nó trở nên lý tưởng cho các ứng dụng yêu cầu lưu trữ tệp được chia sẻ với tính sẵn sàng cao và độ bền tốt.