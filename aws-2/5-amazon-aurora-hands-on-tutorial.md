# Hướng Dẫn Thực Hành Amazon Aurora

## Tổng Quan

Hướng dẫn này sẽ giúp bạn tạo và cấu hình cơ sở dữ liệu Amazon Aurora trên AWS. Aurora là dịch vụ cơ sở dữ liệu quan hệ hiệu suất cao, có tính sẵn sàng cao, tương thích với MySQL và PostgreSQL.

> **Lưu ý:** Việc làm theo hướng dẫn thực hành này sẽ phát sinh chi phí AWS. Bạn có thể theo dõi mà không cần thực sự tạo cơ sở dữ liệu để hiểu các tùy chọn có sẵn.

## Tạo Cơ Sở Dữ Liệu Amazon Aurora

### Bước 1: Chọn Phương Thức Tạo Database

Chọn **Standard Create** (Tạo tiêu chuẩn) để có toàn quyền kiểm soát tất cả các tùy chọn cấu hình.

### Bước 2: Chọn Database Engine

Aurora cung cấp hai tùy chọn tương thích:
- **Tương thích MySQL**
- **Tương thích PostgreSQL**

Trong hướng dẫn này, chúng ta sẽ sử dụng Aurora **tương thích MySQL**.

### Bước 3: Chọn Phiên Bản Database

- Sử dụng **bộ chọn phiên bản** để chọn phiên bản Aurora của bạn
- Các bộ lọc có sẵn:
  - Hỗ trợ tính năng global database
  - Hỗ trợ tính năng parallel query
  - Hỗ trợ tính năng Serverless v2
- Phiên bản mặc định hiển thị: **3.04.1** (có thể khác tùy theo AWS cung cấp)

### Bước 4: Chọn Template

Chọn template **Production** để truy cập tất cả các tùy chọn cấu hình.

### Bước 5: Cài Đặt Database

**DB Cluster Identifier:** `database-two` (hoặc tên bạn ưa thích)

**Thông Tin Master:**
- Username: `admin`
- Password: [Nhập mật khẩu bảo mật của bạn]

### Bước 6: Cấu Hình Cluster Storage

Chọn giữa hai tùy chọn lưu trữ:

| Loại Storage | Phù Hợp Cho |
|-------------|-------------|
| **Aurora Standard** | Khối lượng công việc tiết kiệm chi phí với I/O vừa phải |
| **Aurora I/O Optimized** | Các hoạt động đầu vào/đầu ra cao (đọc/ghi chuyên sâu) |

Đối với hầu hết các trường hợp sử dụng, chọn **Aurora Standard**.

### Bước 7: Cấu Hình Instance

**Các Tùy Chọn Instance Class:**
- **Memory Optimized** - Cho khối lượng công việc hiệu suất cao
- **Burstable Classes** - Cho khối lượng công việc biến đổi
- Previous generation classes (tùy chọn)

Cho hướng dẫn này: **db.t3.medium**

**Tùy Chọn Serverless v2:**
Nếu phiên bản Aurora của bạn hỗ trợ Serverless:
- Thay vì chọn loại instance, cấu hình Aurora Capacity Units (ACU)
- Đặt ACU tối thiểu và tối đa cho tự động mở rộng
- Database tự động mở rộng giữa các đơn vị công suất này

### Bước 8: Tính Sẵn Sàng và Độ Bền

**Aurora Replicas:**
- Tạo Aurora replica trong Availability Zone (AZ) khác
- Lợi ích:
  - Tăng cường tính sẵn sàng
  - Cải thiện hiệu suất đọc trên các AZ
  - Chuyển đổi dự phòng tự động nhanh chóng
- Lưu ý: Tùy chọn này làm tăng chi phí nhưng cung cấp đầy đủ khả năng của Aurora

### Bước 9: Cấu Hình Kết Nối

**Compute Resource:** Không kết nối với EC2 instance

**Network Type:** IPv4 (hoặc dual-stack cho hỗ trợ IPv6)

**Cấu Hình VPC:**
- Sử dụng VPC mặc định
- Sử dụng subnet group mặc định

**Public Access:** Bật (cho phép kết nối từ địa chỉ IP công cộng)

**VPC Security Group:**
- Tạo security group mới
- Tên: `demo-database-aurora`
- Cho phép kết nối đến Aurora database

### Bước 10: Cấu Hình Bổ Sung

**Database Port:** 3306 (cổng mặc định của MySQL)

**Các Tính Năng Nâng Cao:**

1. **Local Write Forwarding**
   - Chuyển tiếp ghi từ read replica đến write instance tự động
   - Đơn giản hóa quản lý kết nối

2. **Tùy Chọn Xác Thực Database:**
   - **IAM-based authentication** - Sử dụng IAM roles để truy cập database
   - **Kerberos-based authentication** - Cơ chế xác thực bên ngoài

3. **Enhanced Monitoring:** Có thể tắt cho hướng dẫn này

4. **Tùy Chọn Database:**
   - Tên database ban đầu: `myDB`
   - Lưu giữ backup: 1 ngày
   - Mã hóa: Có sẵn
   - Backtracking: Khả năng tua lại database
   - Log exports: Các tùy chọn logging khác nhau

5. **Deletion Protection:** Bảo vệ database khỏi bị xóa nhầm

### Bước 11: Xem Xét và Tạo

- Xem xét ước tính chi phí hàng tháng
- Nhấp **Create Database**

## Hiểu Về Aurora Cluster Của Bạn

### Các Thành Phần Cluster

Sau khi tạo, Aurora cluster của bạn bao gồm:
- **Regional cluster** với:
  - Một **Writer instance**
  - Một **Reader instance**
- Các instance nằm ở **các Availability Zone khác nhau**

### Connection Endpoints

Aurora cung cấp nhiều loại endpoint:

| Loại Endpoint | Mục Đích | Trường Hợp Sử Dụng |
|--------------|----------|---------------------|
| **Writer Endpoint** | Luôn kết nối đến write instance | Ghi dữ liệu từ ứng dụng |
| **Reader Endpoint** | Luôn kết nối đến read replica | Đọc dữ liệu từ ứng dụng |
| **Instance-specific Endpoints** | Kết nối trực tiếp đến instance cụ thể | Trường hợp sử dụng nâng cao |

> **Thực Hành Tốt Nhất:** Ứng dụng nên sử dụng Writer và Reader endpoints thay vì các endpoint cụ thể của instance.

## Các Tính Năng Nâng Cao

### 1. Thêm Read Replica

- Thêm reader bổ sung vào reader cluster của bạn
- Tăng khả năng mở rộng đọc
- Có thể có tới 15 Aurora replicas

### 2. Cross-Region Read Replicas

- Tạo read replica ở các AWS region khác
- Cải thiện hiệu suất đọc cho các ứng dụng phân tán địa lý
- Cung cấp khả năng phục hồi thảm họa

### 3. Point-in-Time Restore

- Khôi phục database về bất kỳ thời điểm nào trong thời gian lưu giữ backup
- Hữu ích cho các tình huống khôi phục dữ liệu

### 4. Read Replica Auto-Scaling

Cấu hình chính sách tự động mở rộng:

```
Tên Policy: read-replica-scaling-policy
Target Metric: Average CPU Utilization hoặc Connection Count
Target Value: 60%
Min Capacity: 1 replica
Max Capacity: 15 replicas
```

**Cách hoạt động:**
- Giám sát mức sử dụng replica hoặc kết nối
- Tự động thêm replica khi vượt quá ngưỡng
- Thu nhỏ quy mô khi tải giảm
- Có thể xác định thời gian mở rộng cho policy

### 5. Global Database

**Yêu Cầu:**
- Phiên bản Aurora có tính năng global database được bật
- Loại instance đủ lớn cho replikasi toàn cầu

**Khả Năng:**
- Thêm các region database trên nhiều AWS region
- Tạo triển khai Aurora toàn cầu thực sự
- Đọc toàn cầu với độ trễ thấp

**Lưu ý:** Một số loại instance có thể cần được nâng cấp (ví dụ: lên loại instance large) trước khi thêm các region toàn cầu.

## Lợi Ích Chính Của Aurora

- **Hiệu suất tuyệt vời** - Nhanh hơn tới 5 lần so với MySQL tiêu chuẩn
- **Tính sẵn sàng cao** - Chuyển đổi dự phòng tự động trên các AZ
- **Khả năng mở rộng** - Tự động mở rộng với read replicas
- **Khả năng toàn cầu** - Tùy chọn triển khai đa vùng
- **Tùy chọn Serverless** - Tự động mở rộng công suất
- **Giải pháp hoàn chỉnh** - Dịch vụ database được quản lý toàn diện

## Xóa Aurora Database Của Bạn

Để tránh phí liên tục, làm theo các bước sau **theo thứ tự**:

### Bước 1: Xóa Reader Instance
1. Chọn reader instance
2. Chọn **Actions** → **Delete**
3. Gõ `delete me` để xác nhận

### Bước 2: Xóa Writer Instance
1. Chọn writer instance
2. Chọn **Actions** → **Delete**
3. Gõ `delete me` để xác nhận

### Bước 3: Xóa Database Cluster
1. Đợi cả hai instance bị xóa
2. Chọn database cluster
3. Chọn **Actions** → **Delete**
4. Xác nhận xóa

> **Quan Trọng:** Bạn không thể xóa cluster cho đến khi cả reader và writer instance được xóa trước.

## Tóm Tắt

Amazon Aurora là dịch vụ cơ sở dữ liệu quan hệ hàng đầu của AWS, cung cấp:
- Hiệu suất và khả năng mở rộng cao
- Tương thích với MySQL và PostgreSQL
- Replikasi và chuyển đổi dự phòng tự động
- Tự động mở rộng read replica
- Khả năng global database
- Tùy chọn serverless cho khối lượng công việc biến đổi

Điều này làm cho Aurora trở thành lựa chọn tuyệt vời cho các khối lượng công việc production yêu cầu độ tin cậy, hiệu suất và khả năng mở rộng.