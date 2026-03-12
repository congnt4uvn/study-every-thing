# Các Loại EC2 Instance

## Tổng Quan

EC2 instances có nhiều loại khác nhau được tối ưu hóa cho các trường hợp sử dụng khác nhau. AWS hiện tại cung cấp bảy danh mục khác nhau của EC2 instances, mỗi loại được thiết kế để đáp ứng các yêu cầu workload cụ thể.

## Quy Ước Đặt Tên Instance

AWS tuân theo quy ước đặt tên chuẩn hóa cho EC2 instances. Ví dụ: **m5.2xlarge**

- **m** = Lớp instance (ví dụ: general purpose - đa năng)
- **5** = Thế hệ của instance (cải tiến theo thời gian: m5 → m6 → m7...)
- **2xlarge** = Kích thước trong lớp instance (small → large → 2xlarge → 4xlarge...)

Kích thước càng lớn, instance càng có nhiều bộ nhớ và tài nguyên CPU.

## Các Loại EC2 Instance

### 1. General Purpose (Đa Năng)

**Đặc điểm:**
- Cân bằng giữa tài nguyên compute, memory và networking
- Phù hợp cho các workload đa dạng

**Trường hợp sử dụng:**
- Web servers
- Code repositories
- Hosting ứng dụng tổng quát

**Họ Instance:** T-series, M-series

**Ví dụ:** t2.micro (đủ điều kiện Free Tier)

### 2. Compute Optimized (Tối Ưu Hóa Tính Toán)

**Đặc điểm:**
- Được tối ưu hóa cho các tác vụ đòi hỏi tính toán cao
- Bộ xử lý hiệu năng cao

**Trường hợp sử dụng:**
- Xử lý hàng loạt (batch processing)
- Chuyển mã media (media transcoding)
- Web servers hiệu năng cao
- High-performance computing (HPC)
- Machine learning
- Game servers chuyên dụng

**Họ Instance:** C-series (C5, C6, v.v.)

### 3. Memory Optimized (Tối Ưu Hóa Bộ Nhớ)

**Đặc điểm:**
- Hiệu năng nhanh cho các workload xử lý tập dữ liệu lớn trong bộ nhớ
- Dung lượng RAM cao

**Trường hợp sử dụng:**
- Cơ sở dữ liệu quan hệ/phi quan hệ hiệu năng cao
- Cache store quy mô web phân tán (ví dụ: ElastiCache)
- Cơ sở dữ liệu trong bộ nhớ cho business intelligence (BI)
- Xử lý real-time dữ liệu lớn không có cấu trúc

**Họ Instance:** R-series (R viết tắt của RAM), X1, High Memory, Z1

### 4. Storage Optimized (Tối Ưu Hóa Lưu Trữ)

**Đặc điểm:**
- Được tối ưu hóa cho việc truy cập tần suất cao vào tập dữ liệu lớn trên bộ nhớ local
- Hiệu năng I/O cao

**Trường hợp sử dụng:**
- Hệ thống xử lý giao dịch trực tuyến tần suất cao (OLTP)
- Cơ sở dữ liệu quan hệ và NoSQL
- Cache cho cơ sở dữ liệu trong bộ nhớ (ví dụ: Redis)
- Ứng dụng kho dữ liệu (data warehousing)
- Hệ thống file phân tán

**Họ Instance:** I-series, D-series, H1

## Ví Dụ So Sánh Instance

| Loại Instance | vCPUs | Bộ nhớ | Tối ưu hóa |
|--------------|-------|---------|------------|
| t2.micro | 1 | 1 GB | Đa năng |
| r5.16xlarge | 16 | 512 GB | Bộ nhớ |
| c5d.4xlarge | 16 | 32 GB | Tính toán |

## Tài Nguyên Hữu Ích

**EC2Instances.info** - Website so sánh toàn diện cung cấp:
- Danh sách đầy đủ tất cả các loại instance AWS
- Thông tin giá cả (Linux On-Demand, chi phí Reserved)
- Thông số kỹ thuật Memory và vCPU
- Khả năng tìm kiếm và lọc
- Công cụ phân tích so sánh

## Điểm Chính Cần Nhớ

- Chọn loại instance dựa trên yêu cầu workload cụ thể của bạn
- Các họ instance phát triển với các thế hệ phần cứng mới
- Tham khảo tài liệu AWS và công cụ so sánh để có thông tin cập nhật
- Các loại instance khác nhau có mô hình giá khác nhau
- Free Tier bao gồm t2.micro instances cho workload đa năng