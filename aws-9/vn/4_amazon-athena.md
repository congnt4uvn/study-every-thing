# Amazon Athena — Tài Liệu Học Tập

---

## Amazon Athena là gì?

**Amazon Athena** là một **dịch vụ truy vấn serverless** (không máy chủ) cho phép bạn phân tích dữ liệu lưu trữ trong **Amazon S3** bằng ngôn ngữ **SQL** tiêu chuẩn.

- Được xây dựng trên nền tảng **Presto engine**
- Không cần cung cấp hoặc quản lý hạ tầng
- Phân tích trực tiếp dữ liệu trong S3 — không cần di chuyển dữ liệu

---

## Các Định Dạng File Hỗ Trợ

| Định dạng | Ghi chú                           |
|-----------|-----------------------------------|
| CSV       | Định dạng flat-file phổ biến      |
| JSON      | Dữ liệu bán cấu trúc              |
| ORC       | Dạng cột — khuyến nghị            |
| Avro      | Định dạng nhị phân theo hàng      |
| Parquet   | Dạng cột — khuyến nghị ★          |

> **Lưu ý:** Apache **Parquet** và **ORC** là các định dạng được khuyến nghị để tối ưu hiệu suất và tiết kiệm chi phí.

---

## Giá Cả

- **Trả tiền theo truy vấn** — giá cố định theo **terabyte dữ liệu được quét**
- Giảm lượng dữ liệu quét = giảm chi phí

---

## Các Trường Hợp Sử Dụng Phổ Biến

- Truy vấn tức thời (ad hoc queries)
- Trí tuệ kinh doanh (BI), phân tích, và báo cáo
- Phân tích log từ các dịch vụ AWS:
  - VPC Flow Logs
  - Load Balancer Logs
  - AWS CloudTrail Trails

> **Mẹo thi:** Khi thấy *"phân tích dữ liệu trong S3 bằng SQL engine serverless"* → nghĩ đến **Athena**.

---

## Tích Hợp — Amazon QuickSight

```
Amazon QuickSight  ──►  Amazon Athena  ──►  Amazon S3
```

Athena thường được kết hợp cùng **Amazon QuickSight** để xây dựng báo cáo và dashboard.

---

## Cải Thiện Hiệu Suất

### 1. Sử Dụng Định Dạng Dữ Liệu Dạng Cột
- Sử dụng **Apache Parquet** hoặc **ORC**
- Chỉ các cột bạn truy vấn mới được quét → **cải thiện hiệu suất và chi phí đáng kể**
- Dùng **AWS Glue** (ETL) để chuyển đổi CSV → Parquet

### 2. Nén Dữ Liệu
- Nén file để giảm lượng dữ liệu cần quét
- Các codec nén hỗ trợ: GZIP, SNAPPY, ZSTD, v.v.

### 3. Phân Vùng (Partition) Dữ Liệu Trong S3
Tổ chức dữ liệu trong S3 theo cấu trúc đường dẫn tương ứng với các cột:

```
s3://my-bucket/flight-data/year=1991/month=01/day=01/
```

- Athena dùng đường dẫn phân vùng để **bỏ qua các thư mục không liên quan**
- Lọc theo năm/tháng/ngày → chỉ quét đúng phân vùng cần thiết
- Giảm đáng kể lượng dữ liệu được quét

### 4. Sử Dụng File Lớn Hơn
- Ưu tiên các file có kích thước **≥ 128 MB**
- Nhiều file nhỏ → overhead cao cho Athena
- File lớn hơn → dễ dàng và nhanh hơn khi quét

---

## Federated Query (Truy Vấn Liên Hợp)

Athena có thể truy vấn dữ liệu **ngoài S3** — bất kỳ nguồn dữ liệu quan hệ, phi quan hệ, hoặc tùy chỉnh nào.

### Cách hoạt động

```
Amazon Athena
    │
    ▼
Lambda Function (Data Source Connector)  ──►  Nguồn dữ liệu bên ngoài
```

Mỗi **Data Source Connector** là một **Lambda function** thực thi federated query đến các dịch vụ khác.

### Các Nguồn Dữ Liệu Được Hỗ Trợ (ví dụ)

| Dịch vụ AWS           | On-Premises / Khác  |
|-----------------------|---------------------|
| ElastiCache           | HBase trên EMR      |
| Amazon DynamoDB       | Cơ sở dữ liệu nội bộ|
| Amazon RDS / Aurora   | SQL Server / MySQL  |
| Amazon Redshift       |                     |
| DocumentDB            |                     |
| CloudWatch Logs       |                     |

- Kết quả truy vấn có thể được **lưu lại vào Amazon S3** để phân tích sau.

---

## Bảng Tổng Hợp

| Tính năng             | Chi tiết                                                |
|-----------------------|---------------------------------------------------------|
| Loại dịch vụ         | Serverless query service                                |
| Ngôn ngữ             | SQL tiêu chuẩn                                          |
| Engine               | Presto                                                  |
| Nguồn dữ liệu        | Amazon S3 (chính) + federated sources                   |
| Định dạng tốt nhất   | Apache Parquet, ORC                                     |
| Mô hình giá          | Theo TB dữ liệu quét                                    |
| Công cụ ETL          | AWS Glue                                                |
| Công cụ BI           | Amazon QuickSight                                       |
| Kết nối liên hợp     | AWS Lambda (Data Source Connector)                      |

---

## Các Điểm Quan Trọng Cho Kỳ Thi

1. **Serverless** — không cần cung cấp cơ sở dữ liệu
2. Dùng **Parquet/ORC** để tối ưu chi phí và hiệu suất
3. Dùng **Glue** để chuyển đổi định dạng dữ liệu (VD: CSV → Parquet)
4. **Phân vùng** dữ liệu S3 để giảm thiểu việc quét dữ liệu
5. Dùng **file lớn hơn** (≥ 128 MB) để tăng hiệu quả
6. **Federated Query** qua Lambda connector có thể truy cập bất kỳ nguồn dữ liệu nào
7. Kết quả federated query được lưu vào **S3**
