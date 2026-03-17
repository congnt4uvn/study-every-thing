# AWS Athena – Truy Vấn Dữ Liệu Từ S3

## Tổng Quan

**Amazon Athena** là dịch vụ truy vấn tương tác **serverless** (không cần máy chủ), cho phép bạn phân tích dữ liệu lưu trữ trong **Amazon S3** bằng ngôn ngữ **SQL** tiêu chuẩn — mà không cần cấu hình hay quản lý bất kỳ hạ tầng máy chủ nào.

---

## Các Khái Niệm Quan Trọng

| Thuật ngữ | Mô tả |
|-----------|-------|
| **Athena** | Công cụ truy vấn SQL serverless cho dữ liệu trên S3 |
| **S3 Bucket** | Kho lưu trữ đối tượng chứa dữ liệu thô |
| **Query Result Location** | S3 bucket riêng dùng để lưu kết quả truy vấn |
| **Database** | Vùng chứa logic cho các bảng trong Athena |
| **Table** | Định nghĩa schema ánh xạ tới các file trong S3 |

---

## Hướng Dẫn Từng Bước: Sử Dụng Athena Để Truy Vấn S3

### Bước 1 – Cấu Hình Vị Trí Lưu Kết Quả Truy Vấn

Trước khi chạy bất kỳ truy vấn nào, Athena yêu cầu một S3 bucket để lưu kết quả.

1. Mở **Athena Query Editor**.
2. Vào **Settings** → nhập đường dẫn S3 bucket làm vị trí kết quả.
3. Mẹo: Dùng trình duyệt S3 ngay trong phần cài đặt Athena để tránh gõ nhầm đường dẫn.

```
s3://ten-bucket-ket-qua-cua-ban/
```

> Luôn thêm **dấu gạch chéo `/` ở cuối** đường dẫn S3.

---

### Bước 2 – Tạo Database

Chạy câu lệnh SQL sau trong Athena editor để tạo database mới:

```sql
CREATE DATABASE s3_access_logs_db;
```

Sau khi tạo, database mới sẽ xuất hiện ở bảng bên trái của Query Editor.

---

### Bước 3 – Tạo Bảng (Table)

Tạo bảng ánh xạ tới các file access log của S3 đang lưu trong bucket:

```sql
CREATE EXTERNAL TABLE s3_access_logs (
  bucket_owner STRING,
  bucket       STRING,
  request_datetime STRING,
  remote_ip    STRING,
  requester    STRING,
  request_id   STRING,
  operation    STRING,
  key          STRING,
  request_uri  STRING,
  http_status  INT,
  error_code   STRING,
  bytes_sent   BIGINT,
  object_size  BIGINT,
  ...
)
ROW FORMAT ...
LOCATION 's3://ten-bucket-nguon-cua-ban/';
```

> Định nghĩa bảng đầy đủ (bao gồm `ROW FORMAT` và danh sách cột) lấy từ tài liệu chính thức **Amazon S3 + Athena**. Bạn chỉ cần thay đổi giá trị `LOCATION`.

- Đặt `LOCATION` trỏ đến S3 bucket chứa dữ liệu nguồn.
- Nếu dữ liệu nằm trong thư mục con (prefix), thêm prefix vào cuối:
  ```
  LOCATION 's3://ten-bucket/ten-prefix/'
  ```

---

### Bước 4 – Xem Trước Bảng (Preview Table)

Sau khi tạo bảng, bạn có thể xem nhanh 10 hàng dữ liệu:

- Nhấp vào **menu ba chấm** bên cạnh tên bảng ở bảng trái.
- Chọn **Preview Table**.

Thao tác này tự động tạo và chạy:

```sql
SELECT * FROM s3_access_logs LIMIT 10;
```

---

### Bước 5 – Chạy Các Truy Vấn Phân Tích

#### Đếm Số Yêu Cầu Theo HTTP Status và Thao Tác

```sql
SELECT http_status, operation, request_uri, COUNT(*) AS so_luong
FROM s3_access_logs
GROUP BY http_status, operation, request_uri
ORDER BY so_luong DESC;
```

Kết quả phân tích:
- `404` — Lỗi Not Found (bất thường? cần điều tra!)
- `200` — Yêu cầu thành công
- `403` — **Truy cập trái phép** (vấn đề bảo mật)

#### Phát Hiện Truy Cập Trái Phép (Lỗi 403)

```sql
SELECT *
FROM s3_access_logs
WHERE http_status = 403;
```

Dùng truy vấn này để xác định ai đang cố truy cập bucket mà không có quyền.

---

## Tại Sao Nên Dùng Athena?

- **Serverless** — không cần cài đặt hay quản lý hạ tầng.
- **Trả tiền theo truy vấn** — tính phí dựa trên lượng dữ liệu được quét.
- **SQL tiêu chuẩn** — dễ học với ai đã biết SQL.
- **Làm việc trực tiếp trên S3** — không cần pipeline ETL hay nạp dữ liệu trước.
- **Có thể mở rộng** — xử lý petabyte dữ liệu tự động.

---

## Các Trường Hợp Sử Dụng Phổ Biến

- Phân tích **S3 access logs** để kiểm tra bảo mật.
- Chạy **phân tích ad-hoc** trên dữ liệu log hoặc sự kiện thô.
- Truy vấn **CloudTrail**, **ELB**, hoặc **VPC Flow Logs** lưu trên S3.
- Phân tích chi phí và báo cáo từ dữ liệu trên S3.

---

## Tóm Tắt Quy Trình

```
S3 Bucket (dữ liệu thô)
       ↓
  Tạo Database    →  CREATE DATABASE ...
       ↓
  Tạo Bảng       →  CREATE EXTERNAL TABLE ... LOCATION 's3://...'
       ↓
  Chạy Truy Vấn  →  SELECT, GROUP BY, WHERE ...
       ↓
  Kết quả lưu về →  S3 Result Bucket
```

Athena giúp bạn khai thác thông tin từ dữ liệu trên S3 cực kỳ dễ dàng chỉ bằng SQL — không cần máy chủ, không cần nạp dữ liệu, không phức tạp.

---

## Câu Hỏi Ôn Tập

1. Bạn phải cấu hình điều gì trước khi chạy truy vấn Athena đầu tiên?
2. Câu lệnh SQL nào được dùng để tạo database mới trong Athena?
3. Làm thế nào để chỉ định vị trí dữ liệu nguồn khi tạo bảng?
4. Mã HTTP nào cho thấy có truy cập trái phép vào S3?
5. Tại sao Athena được gọi là "serverless"? Điều này có ý nghĩa gì với người dùng?

---

*Nguồn: AWS Athena – Truy Vấn Dữ Liệu S3 (Ghi Chú Bài Giảng)*
