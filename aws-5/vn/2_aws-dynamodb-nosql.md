# AWS DynamoDB - Tài Liệu Học Tập Cơ Sở Dữ Liệu NoSQL

## Tổng Quan
DynamoDB là **cơ sở dữ liệu NoSQL serverless** được cung cấp bởi AWS.

## Kiến Trúc Truyền Thống vs NoSQL

### Kiến Trúc RDBMS Truyền Thống
```
Clients → ELB → EC2 Instances (Auto Scaling Group) → RDS Database
```

**Các Thành Phần:**
- **Elastic Load Balancer (ELB)**: Phân phối traffic
- **EC2 Instances**: Tầng ứng dụng với Auto Scaling Group
- **Amazon RDS**: Cơ sở dữ liệu quan hệ (MySQL, PostgreSQL, v.v.)

### Đặc Điểm của RDBMS Truyền Thống
✅ **Ưu Điểm:**
- Hỗ trợ ngôn ngữ truy vấn SQL
- Yêu cầu mô hình hóa dữ liệu chặt chẽ
- Có định nghĩa bảng và schema rõ ràng
- Hỗ trợ joins, aggregations và các phép tính phức tạp

⚠️ **Hạn Chế Về Mở Rộng:**
- **Mở rộng dọc (Vertical Scaling)**: Cần nâng cấp phần cứng mạnh hơn (CPU, RAM, I/O tốt hơn)
- **Mở rộng ngang (Horizontal Scaling)**: Chỉ giới hạn ở thao tác đọc
  - Thêm EC2 instances ở tầng ứng dụng
  - Thêm RDS Read Replicas (bị giới hạn bởi số lượng replica tối đa)
- **Không có khả năng mở rộng ngang cho ghi** với RDS

## Cơ Sở Dữ Liệu NoSQL

### Định Nghĩa
- **NoSQL** = "Not Only SQL" hoặc "Non SQL"
- Cơ sở dữ liệu phi quan hệ
- Kiến trúc phân tán
- Cung cấp khả năng mở rộng ngang

### Các Công Nghệ NoSQL Phổ Biến
- **MongoDB**
- **AWS DynamoDB** ⭐

### Lợi Ích Chính
- ✅ Khả năng mở rộng theo chiều ngang
- ✅ Kiến trúc phân tán
- ✅ Phù hợp hơn cho ứng dụng quy mô lớn
- ✅ Tùy chọn serverless (DynamoDB)

## Ghi Chú Học Tập
- DynamoDB là dịch vụ cơ sở dữ liệu NoSQL được quản lý bởi AWS
- Khắc phục các hạn chế về mở rộng ngang của RDS truyền thống
- Lý tưởng cho các ứng dụng yêu cầu throughput đọc/ghi cao
- Serverless có nghĩa là không cần quản lý cơ sở hạ tầng
