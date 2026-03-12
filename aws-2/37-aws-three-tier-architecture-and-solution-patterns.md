# Kiến Trúc Ba Tầng AWS và Các Mẫu Giải Pháp

## Tổng Quan

Tài liệu này đề cập đến các kiến trúc giải pháp AWS điển hình, tập trung vào mẫu kiến trúc ba tầng, triển khai LAMP stack và lưu trữ WordPress trên AWS.

## Kiến Trúc Giải Pháp Ba Tầng

### Các Thành Phần Kiến Trúc

Kiến trúc ba tầng là một mẫu phổ biến được sử dụng trong AWS, cung cấp bảo mật, khả năng mở rộng và tách biệt các mối quan tâm.

#### Tầng 1: Cân Bằng Tải (Public Subnet)

- **Elastic Load Balancer (ELB)** được triển khai trên nhiều Vùng Khả Dụng (Availability Zones)
- Phải nằm trong **public subnets** để có thể truy cập từ internet
- Người dùng truy cập ứng dụng thông qua truy vấn DNS của **Route 53**
- Phân phối lưu lượng đến tầng ứng dụng

#### Tầng 2: Tầng Ứng Dụng (Private Subnet)

- **EC2 instances** trong một **Auto Scaling Group**
- Được triển khai trong **private subnets** để tăng cường bảo mật
- Chỉ có thể truy cập từ ELB, không trực tiếp từ internet
- Phân bổ trên ba Vùng Khả Dụng để đảm bảo tính sẵn sàng cao
- Lưu lượng được định tuyến từ public subnets đến private subnets sử dụng **route tables**

#### Tầng 3: Tầng Dữ Liệu (Data Subnet)

- Nằm trong private subnet thứ hai (mức sâu hơn)
- Còn được gọi là **data subnet**
- Bao gồm:
  - **Amazon RDS**: Cơ sở dữ liệu chính cho các thao tác đọc/ghi
  - **ElastiCache**: Tầng cache để:
    - Lưu cache dữ liệu từ RDS
    - Lưu trữ dữ liệu phiên (session) trong bộ nhớ
    - Cải thiện hiệu suất ứng dụng

### Lợi Ích Bảo Mật

- Tài nguyên tính toán được cô lập trong private subnets
- Tăng cường bảo mật thông qua phân đoạn mạng
- Kiến trúc phòng thủ nhiều lớp

## LAMP Stack trên EC2

### Các Thành Phần

**LAMP** là một stack ứng dụng web phổ biến bao gồm:

- **L**inux: Hệ điều hành cho EC2 instances
- **A**pache: Web server chạy trên Linux
- **M**ySQL: Cơ sở dữ liệu (có thể sử dụng RDS MySQL)
- **P**HP: Logic ứng dụng để render các trang web

### Các Thành Phần Bổ Sung

- **Redis hoặc Memcached** (ElastiCache): Cho công nghệ caching
- **EBS (Elastic Block Store)**: Để lưu trữ dữ liệu cục bộ, bao gồm:
  - Cache cục bộ
  - Dữ liệu ứng dụng
  - Lưu trữ phần mềm

## WordPress trên AWS

### Tổng Quan Kiến Trúc

Triển khai WordPress trên AWS sử dụng kiến trúc nhiều tầng với khả năng lưu trữ chia sẻ.

### Các Thành Phần Chính

#### Cân Bằng Tải và Tính Toán
- **Elastic Load Balancer**: Phân phối lưu lượng người dùng
- **EC2 Instances**: Lưu trữ ứng dụng WordPress
- **Auto Scaling Group**: Quản lý việc mở rộng EC2 instances

#### Giải Pháp Lưu Trữ Chia Sẻ

**Vấn Đề**: Nhiều EC2 instances cần chia sẻ hình ảnh do người dùng tải lên

**Giải Pháp**: **Amazon EFS (Elastic File System)**
- Hệ thống file mạng có thể truy cập trên tất cả EC2 instances
- Tạo Elastic Network Interfaces trong mỗi Vùng Khả Dụng
- Cho phép chia sẻ file trên tất cả các máy chủ ứng dụng
- Hoàn hảo cho việc lưu trữ và truy cập hình ảnh chia sẻ

### Kiến Trúc WordPress Quy Mô Đầy Đủ

AWS cung cấp một kiến trúc tham chiếu WordPress toàn diện bao gồm:

- NAT Gateways và Internet Gateways
- Auto Scaling Groups
- Nhiều subnets (public và private)
- Cơ sở dữ liệu Amazon Aurora
- Amazon EFS cho lưu trữ chia sẻ
- Công nghệ cân bằng tải
- CloudFront và S3 (để phân phối nội dung)

## Những Điểm Chính Cần Nhớ

1. **Kiến trúc ba tầng** là một mẫu cơ bản trong thiết kế giải pháp AWS
2. **Phân đoạn mạng** thông qua subnets cung cấp các lớp bảo mật
3. **Các khái niệm VPC** là thiết yếu để hiểu kiến trúc AWS
4. Các tầng khác nhau phục vụ các mục đích khác nhau:
   - Public subnets cho các thành phần hướng internet
   - Private subnets cho logic ứng dụng
   - Data subnets cho cơ sở dữ liệu và caching
5. **EFS** là lý tưởng cho lưu trữ file chia sẻ trên nhiều instances
6. Các mẫu này thường xuyên xuất hiện trong các kỳ thi chứng chỉ AWS

## Kết Luận

Hiểu các mẫu kiến trúc này là rất quan trọng cho:
- Thiết kế các giải pháp AWS an toàn và có khả năng mở rộng
- Vượt qua các kỳ thi chứng chỉ AWS
- Làm việc hiệu quả với vai trò nhà phát triển AWS

Hãy dành thời gian nghiên cứu các sơ đồ kiến trúc này và hiểu cách các dịch vụ AWS khác nhau hoạt động cùng nhau để tạo ra các ứng dụng mạnh mẽ, sẵn sàng cho sản xuất.