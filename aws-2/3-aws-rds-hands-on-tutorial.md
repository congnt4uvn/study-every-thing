# Hướng Dẫn Thực Hành AWS RDS

## Giới Thiệu

Hướng dẫn này sẽ giúp bạn tạo và quản lý một instance cơ sở dữ liệu Amazon RDS (Relational Database Service), bao gồm kết nối và thực hiện các thao tác cơ bản.

## Tạo Cơ Sở Dữ Liệu RDS

### Bước 1: Truy Cập RDS Console

1. Điều hướng đến Aurora và RDS console
2. Nhấp vào **Databases** ở thanh bên trái
3. Nhấp vào **Create database**

### Bước 2: Cấu Hình Cơ Sở Dữ Liệu

#### Chọn Engine
- Chọn giữa **Standard Create** hoặc **Easy Create**
- Cho hướng dẫn này, chọn **Standard Create** để xem tất cả các tùy chọn
- Chọn **MySQL** làm loại engine
- Giữ phiên bản engine mặc định

#### Templates (Mẫu)
Chọn từ ba tùy chọn mẫu:
- **Production**: Nhiều cài đặt hơn, triển khai multi-AZ
- **Dev/Test**: Cài đặt môi trường phát triển
- **Free Tier**: Giới hạn triển khai single AZ (khuyến nghị cho hướng dẫn này)

> **Lưu ý**: Mẫu Production cung cấp triển khai multi-AZ DB instance (2 instances) hoặc triển khai multi-AZ DB cluster (3 instances) để có tính sẵn sàng cao.

### Bước 3: Cài Đặt Cơ Sở Dữ Liệu

#### Định Danh Cơ Sở Dữ Liệu
- Giữ database identifier mặc định
- Master username: `admin`

#### Quản Lý Thông Tin Xác Thực
Bạn có hai tùy chọn:
1. **Self-managed**: Tự tạo và quản lý mật khẩu
2. **AWS Secrets Manager**: An toàn hơn nhưng có chi phí thêm

Cho hướng dẫn này:
- Chọn **Self-managed**
- Master password: Nhập mật khẩu của bạn (ví dụ: `password`)
- Xác nhận master password
- Bật **Password authentication only**

> **Lưu ý**: Xác thực IAM cũng có sẵn như một tùy chọn.

### Bước 4: Cấu Hình Instance

- **Instance type**: Chọn `db.t4g.micro` (hoặc tùy chọn free tier có sẵn)
- **Storage type**: 20 GB dung lượng được phân bổ
- **Storage autoscaling**: Tùy chọn - có thể mở rộng lên đến 1000 GB nếu cần

### Bước 5: Cài Đặt Kết Nối

- **EC2 connection**: Chọn "Don't connect to an EC2 compute resource"
- **VPC**: Sử dụng VPC mặc định
- **Subnet group**: Giữ mặc định
- **Public access**: Chọn **Yes** (để truy cập cơ sở dữ liệu với IP công khai)
- **VPC security group**: Chọn **Create new**
  - Name: `demo-rds`
- **Availability Zone**: Không ưu tiên
- **RDS Proxy**: Không yêu cầu
- **Port**: 3306 (cổng MySQL mặc định)

### Bước 6: Cấu Hình Bổ Sung

- **Monitoring**: Standard insights (Enhanced monitoring có sẵn nếu cần)
- **Log exports**: Tùy chọn
- **Estimated cost**: Xem xét thông tin RDS free tier (có sẵn trong 12 tháng)

### Bước 7: Tạo Cơ Sở Dữ Liệu

Nhấp vào **Create database** và chờ instance được tạo.

## Cài Đặt SQL Client

Trong khi cơ sở dữ liệu đang được tạo, tải xuống và cài đặt **SQLectron**:

1. Truy cập trang web SQLectron
2. Nhấp vào **Download GUI**
3. Chọn phiên bản phù hợp cho nền tảng của bạn:
   - Windows: Tải xuống trình cài đặt Windows mới nhất
   - Mac: Tải xuống file DMG
4. Cài đặt ứng dụng

## Kết Nối Đến Cơ Sở Dữ Liệu RDS

### Bước 1: Xác Minh Việc Tạo Cơ Sở Dữ Liệu

Khi cơ sở dữ liệu được tạo và hiển thị là **Available**:
1. Ghi chú địa chỉ **endpoint**
2. Xác minh **port** (3306)
3. Kiểm tra cài đặt **security group**

### Bước 2: Cấu Hình Security Group

1. Nhấp vào security group
2. Xem xét **inbound rules**
3. Đảm bảo cổng TCP 3306 được mở cho địa chỉ IP của bạn
4. Nếu cần, sửa đổi để cho phép truy cập từ mọi nơi (0.0.0.0/0 cho IPv4)

> **Cảnh Báo Bảo Mật**: Đối với môi trường production, hạn chế quyền truy cập chỉ cho các địa chỉ IP cụ thể.

### Bước 3: Kết Nối Sử Dụng SQLectron

1. Mở SQLectron
2. Nhấp **Add** để thêm kết nối cơ sở dữ liệu mới
3. Cấu hình kết nối:
   - **Name**: RDS demo
   - **Database Type**: MySQL
   - **Server Address**: Dán endpoint RDS của bạn
   - **Port**: 3306
   - **User**: admin
   - **Password**: Mật khẩu của bạn
   - **Initial Database**: mydb

4. Nhấp **Test** để xác minh kết nối
5. Nếu thành công, nhấp **Save** và **Connect**

### Khắc Phục Sự Cố Kết Nối

Nếu kết nối thất bại, kiểm tra:
- Cơ sở dữ liệu được đặt thành **public access**
- Security group cho phép IP của bạn trên cổng 3306
- Endpoint và thông tin xác thực chính xác được sử dụng

## Làm Việc Với Cơ Sở Dữ Liệu

### Tạo Bảng

Sau khi kết nối, bạn có thể thực thi các câu lệnh SQL:

```sql
CREATE TABLE mytable (
    name VARCHAR(20),
    firstname VARCHAR(20)
);
```

Thực thi câu lệnh này để tạo một bảng mới.

### Chèn Dữ Liệu

```sql
INSERT INTO mytable VALUES ('Maarek', 'Stephane');
```

### Truy Vấn Dữ Liệu

Nhấp **Select Rows** hoặc thực thi:

```sql
SELECT * FROM mytable;
```

Bạn sẽ thấy dữ liệu đã chèn được hiển thị.

## Tính Năng Quản Lý RDS

### Tạo Read Replicas

1. Chọn cơ sở dữ liệu của bạn
2. Nhấp **Actions** → **Create read replica**
3. Cấu hình cài đặt read replica
4. Chọn có bật multi-AZ cho replica hay không
5. Tạo replica để tăng khả năng đọc

### Giám Sát

Điều hướng đến tab **Monitoring** để xem:
- **CPU utilization**: Theo dõi việc sử dụng tài nguyên
- **Database connections**: Giám sát các kết nối đang hoạt động
- Nhiều metric khác để điều chỉnh hiệu suất

Sử dụng các metric này để xác định khi nào cần mở rộng instance cơ sở dữ liệu.

### Snapshots và Backups

**Tạo Snapshots**:
1. Chọn cơ sở dữ liệu của bạn
2. Nhấp **Actions** → **Take snapshot**
3. Snapshot có thể được khôi phục bất kỳ lúc nào

**Tùy Chọn Khôi Phục**:
- Khôi phục đến một thời điểm
- Khôi phục từ snapshot
- Di chuyển snapshot sang region khác

## Lợi Ích Của Amazon RDS

- **Fully managed**: AWS xử lý bảo trì, backups và cập nhật
- **Read replicas**: Mở rộng khả năng đọc
- **Multi-AZ deployment**: Tính sẵn sàng cao và khắc phục thảm họa
- **Easy scaling**: Tăng loại instance khi cần
- **Automated backups**: Khôi phục point-in-time
- **Monitoring**: Metric CloudWatch tích hợp

## Dọn Dẹp

### Xóa Cơ Sở Dữ Liệu

Để tránh các khoản phí đang diễn ra:

1. Chọn cơ sở dữ liệu của bạn
2. Nhấp **Modify**
3. Cuộn xuống cuối
4. **Tắt deletion protection**
5. Nhấp **Continue** → **Apply immediately**
6. Chờ việc sửa đổi hoàn tất
7. Chọn lại cơ sở dữ liệu
8. Nhấp **Actions** → **Delete**
9. Chọn các tùy chọn:
   - Bỏ chọn **Create final snapshot** (tùy chọn)
   - Gõ `delete me` để xác nhận
   - Xác nhận rằng tất cả dữ liệu sẽ bị mất
10. Nhấp **Delete**

## Kết Luận

Bạn đã tạo, cấu hình, kết nối và quản lý thành công cơ sở dữ liệu Amazon RDS MySQL. RDS cung cấp giải pháp cơ sở dữ liệu được quản lý mạnh mẽ với các tính năng như read replicas, triển khai multi-AZ, backup tự động và khả năng mở rộng dễ dàng - tất cả đều cần thiết cho các ứng dụng production.

## Lưu Ý Quan Trọng

- Hướng dẫn này sử dụng các tùy chọn free tier khi có sẵn
- Free tier có sẵn trong 12 tháng
- Luôn bảo mật cơ sở dữ liệu của bạn đúng cách trong production
- Giám sát chi phí bằng AWS Budgets
- Cân nhắc sử dụng AWS Secrets Manager để quản lý mật khẩu trong môi trường production