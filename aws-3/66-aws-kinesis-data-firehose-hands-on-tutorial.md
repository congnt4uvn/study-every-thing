# AWS Kinesis Data Firehose - Hướng Dẫn Thực Hành

## Tổng Quan

Hướng dẫn thực hành này trình bày cách sử dụng Amazon Kinesis Data Firehose với delivery streams để nhập, chuyển đổi và phân phối dữ liệu streaming đến các đích khác nhau.

## Tổng Quan Kiến Trúc

Kinesis Data Firehose hoạt động với kiến trúc như sau:

### Nguồn Dữ Liệu (Producers)
- **Kinesis Data Streams** (trường hợp sử dụng của chúng ta)
- **Direct PUTs** thông qua:
  - Kinesis Data Agents
  - Các dịch vụ AWS (CloudWatch, IoT Core, EventBridge, v.v.)
  - Ứng dụng tùy chỉnh sử dụng AWS SDK

### Chuyển Đổi Dữ Liệu
- Lambda functions để chuyển đổi dữ liệu
- Chuyển đổi định dạng bản ghi (Parquet, ORC)
- Lọc, nén và xử lý

### Đích Đến
**Các đích chính cần nhớ:**
- Amazon S3
- Amazon OpenSearch Service (trước đây là ElasticSearch)
- Amazon Redshift

**Các tùy chọn bổ sung:**
- Dịch vụ bên thứ ba
- HTTP endpoints tùy chỉnh

## Hướng Dẫn Từng Bước

### Bước 1: Tạo Delivery Stream

1. Truy cập console **Kinesis Data Firehose**
2. Nhấp vào **Delivery Streams**
3. Nhấp **Create delivery stream**

### Bước 2: Cấu Hình Nguồn

1. Chọn loại nguồn: **Kinesis Data Stream**
2. Duyệt và chọn stream của bạn (ví dụ: `DemoStream`)
3. Tên delivery stream được tự động tạo

### Bước 3: Chuyển Đổi và Convert Bản Ghi (Tùy Chọn)

#### Chuyển Đổi Bản Ghi Nguồn với Lambda
- Bật chuyển đổi để:
  - Lọc dữ liệu
  - Giải nén bản ghi
  - Chuyển đổi định dạng
  - Xử lý bản ghi nguồn

#### Chuyển Đổi Định Dạng Bản Ghi
- Chuyển đổi sang định dạng **Parquet** hoặc **ORC**
- Hữu ích cho các đích cụ thể
- Lưu ý: Điều này được đề cập chi tiết trong chứng chỉ AWS Data & Analytics

### Bước 4: Chọn Đích Đến

1. Chọn **Amazon S3** làm đích đến
2. Chọn S3 bucket hiện có hoặc tạo mới
   - Ví dụ: `demo-firehose-stephane-V3`
3. Cấu hình các tùy chọn bổ sung:
   - Dynamic partitioning: Không (cho demo này)
   - S3 bucket prefix: Để trống
   - Bucket error output prefix: Để trống

### Bước 5: Cấu Hình Buffer Settings

#### Kích Thước Buffer
- **Mặc định**: 5 MB
- **Các tùy chọn**: 
  - Lớn hơn (128+ MB) để tăng hiệu quả
  - Nhỏ hơn (1 MB) để tăng tốc độ
- **Cài đặt demo**: 1 MB (để phân phối nhanh hơn)

#### Khoảng Thời Gian Buffer
- **Mục đích**: Tần suất flush buffer nếu chưa đầy
- **Các tùy chọn**:
  - 300 giây (5 phút)
  - 60 giây (1 phút) - tối thiểu
  - 900 giây (15 phút)
- **Cài đặt demo**: 60 giây (tối thiểu để tăng tốc độ)

**Điểm Quan Trọng**: Dữ liệu được phân phối khi kích thước buffer đạt ngưỡng HOẶC khoảng thời gian buffer hết hạn (điều nào xảy ra trước).

### Bước 6: Nén và Mã Hóa

#### Các Tùy Chọn Nén
- GZIP
- Snappy
- Zip
- Hadoop-Compatible Snappy

**Lợi ích**: Giảm chi phí lưu trữ trên S3

#### Mã Hóa
- Bật/tắt theo nhu cầu
- Cấu hình cài đặt mã hóa cho dữ liệu khi lưu trữ

### Bước 7: Quyền Truy Cập

Console tự động tạo IAM role với các quyền cần thiết để:
- Ghi vào S3 bucket đích
- Đọc từ Kinesis Data Stream nguồn

### Bước 8: Tạo Delivery Stream

Nhấp **Create delivery stream** và đợi cho đến khi trạng thái là **Active**.

## Kiểm Tra Cấu Hình

### Gửi Dữ Liệu Thử Nghiệm

1. Mở **AWS CloudShell**
2. Chạy lệnh để gửi dữ liệu đến Kinesis Data Stream của bạn:
   - Đảm bảo sử dụng đúng tên stream (ví dụ: `DemoStream`)
   - Gửi các bản ghi mẫu:
     - `user signup`
     - `user login`
     - `user logout`

### Xác Minh Phân Phối Dữ Liệu

1. Truy cập **S3 console**
2. Tìm bucket đích của bạn
3. **Đợi 60 giây** (khoảng thời gian buffer) để dữ liệu xuất hiện
4. Làm mới giao diện bucket
5. Điều hướng qua các thư mục phân vùng (được tổ chức theo ngày)
6. Tải xuống và mở file bản ghi
7. Xác minh dữ liệu chứa các bản ghi thử nghiệm của bạn

## Giám Sát

Sau khi delivery stream hoạt động, bạn có thể giám sát:
- **Metrics**: Xem thông lượng dữ liệu và thống kê phân phối
- **Configuration**: Xem lại chi tiết cấu hình
- **Error Logs**: Kiểm tra CloudWatch Logs để tìm lỗi

## Dọn Dẹp

**Quan Trọng**: Để tránh chi phí phát sinh, xóa tài nguyên theo thứ tự sau:

1. **Xóa Delivery Stream**:
   - Điều hướng đến delivery stream
   - Nhập tên để xác nhận xóa
   - Xóa

2. **Xóa Kinesis Data Stream**:
   - Điều hướng đến DemoStream
   - Xóa stream
   - **Quan Trọng**: Kinesis Data Streams tính phí theo giờ nếu để chạy

## Những Điểm Chính Cần Nhớ

- Kinesis Data Firehose đơn giản hóa việc phân phối dữ liệu streaming
- Cài đặt buffer kiểm soát tần suất và hiệu quả phân phối
- Nhiều tùy chọn chuyển đổi có sẵn thông qua Lambda
- Tự động tạo IAM role để xử lý quyền truy cập
- Nhớ dọn dẹp tài nguyên để tránh chi phí không cần thiết
- Các đích đến chính cần nhớ: **S3, OpenSearch, Redshift**

## Bước Tiếp Theo

Tiếp tục khám phá các dịch vụ streaming AWS và các mẫu tích hợp dữ liệu trong các bài giảng tiếp theo.