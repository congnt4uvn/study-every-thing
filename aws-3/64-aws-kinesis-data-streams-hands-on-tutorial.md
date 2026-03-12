# AWS Kinesis Data Streams - Hướng Dẫn Thực Hành

## Tổng Quan

Hướng dẫn thực hành này sẽ giúp bạn tạo và làm việc với Amazon Kinesis Data Streams, bao gồm việc tạo dữ liệu (producing) và tiêu thụ dữ liệu (consuming) bằng AWS CLI và CloudShell.

## Mục Lục

1. [Tạo Kinesis Data Stream](#tạo-kinesis-data-stream)
2. [Hiểu Về Các Chế Độ Dung Lượng](#hiểu-về-các-chế-độ-dung-lượng)
3. [Tùy Chọn Producer và Consumer](#tùy-chọn-producer-và-consumer)
4. [Sử Dụng AWS CloudShell](#sử-dụng-aws-cloudshell)
5. [Gửi Dữ Liệu Đến Kinesis](#gửi-dữ-liệu-đến-kinesis)
6. [Tiêu Thụ Dữ Liệu Từ Kinesis](#tiêu-thụ-dữ-liệu-từ-kinesis)

## Tạo Kinesis Data Stream

### Các Tùy Chọn Có Sẵn

Khi bạn mở dịch vụ Kinesis, bạn sẽ thấy ba tùy chọn:
- **Data Streams** - Để truyền dữ liệu theo thời gian thực
- **Data Firehose** - Để chuyển dữ liệu đến các đích trong AWS
- **Data Analytics** - Để phân tích thời gian thực

### Thông Tin Về Giá

Giá của Kinesis Data Streams dựa trên:
- **$0.05 cho mỗi shard mỗi giờ**
- **Chi phí cho các thao tác PUT** khi gửi dữ liệu vào stream

### Tạo Stream Đầu Tiên

1. Điều hướng đến dịch vụ Kinesis trong AWS Console
2. Nhấp "Create Data Stream"
3. Đặt tên cho stream của bạn (ví dụ: `DemoStream`)
4. Xác định dung lượng của data stream

## Hiểu Về Các Chế Độ Dung Lượng

### Chế Độ On-Demand (Theo Yêu Cầu)

**Tính Năng:**
- Không cần lập kế hoạch dung lượng
- Tự động mở rộng quy mô
- Thông lượng ghi tối đa: **200 MB/giây**
- Dung lượng ghi tối đa: **200,000 bản ghi/giây**
- Dung lượng đọc tối đa: **400 MB/giây** cho mỗi consumer (với enhanced Fan-Out)

**Giá:**
- Mô hình thanh toán theo thông lượng
- **Không có gói miễn phí**

### Chế Độ Provisioned (Cung Cấp Trước)

**Tính Năng:**
- Cần cung cấp shard thủ công
- Công cụ Shard Estimator có sẵn để tính toán dung lượng cần thiết
- Dung lượng dựa trên:
  - Số bản ghi mỗi giây
  - Kích thước bản ghi
  - Số lượng consumer

**Dung Lượng Shard:**
- **1 shard = 1 MB/giây dung lượng ghi**
- **1 shard = 2 MB/giây dung lượng đọc**
- Nhân dung lượng với số lượng shard (ví dụ: 10 shard = dung lượng x10)

**Giá:**
- Giá theo từng shard
- **Không có gói miễn phí**

### Cân Nhắc Về Chi Phí

⚠️ **Quan Trọng:** Hướng dẫn thực hành này sẽ phát sinh chi phí. Nếu bạn muốn tránh chi phí, hãy bỏ qua hướng dẫn này. Tuy nhiên, chi phí sẽ là tối thiểu nếu bạn xóa tài nguyên ngay sau khi hoàn thành.

## Tùy Chọn Producer và Consumer

### Producer (Ghi Dữ Liệu)

Ba tùy chọn được khuyến nghị để truyền dữ liệu đến Kinesis:

1. **Kinesis Agent** - Để truyền từ các máy chủ ứng dụng
2. **AWS SDK** - Để phát triển producer ở mức thấp
3. **Kinesis Producer Library (KPL)** - Để phát triển producer ở mức cao với API tốt hơn

Tất cả các tùy chọn đều có sẵn trên GitHub.

### Consumer (Đọc Dữ Liệu)

Các tùy chọn để tiêu thụ dữ liệu từ Kinesis:

- Kinesis Data Analytics
- Kinesis Data Firehose
- Kinesis Client Library (KCL)
- AWS Lambda

### Quản Lý Stream

**Giám Sát:**
- Xem các bản ghi được gửi đến stream
- Giám sát các chỉ số stream trong CloudWatch

**Cấu Hình:**
- Mở rộng stream bằng cách điều chỉnh số lượng shard (ví dụ: từ 1 đến 5 shard)
- Thêm tag để tổ chức
- Cấu hình enhanced Fan-Out cho các ứng dụng consumer

## Sử Dụng AWS CloudShell

### Tại Sao Dùng CloudShell?

CloudShell cung cấp giao diện dòng lệnh được cấu hình sẵn trong AWS với:
- Miễn phí sử dụng
- Không cần cấu hình
- Tự động kế thừa thông tin xác thực
- AWS CLI phiên bản 2 được cài đặt sẵn

### Truy Cập CloudShell

1. Nhấp vào biểu tượng CloudShell (bên cạnh biểu tượng chuông) trong AWS Console
2. Đợi môi trường khởi tạo (thiết lập lần đầu có thể mất một chút thời gian)
3. Terminal mở sẵn sàng sử dụng

### Kiểm Tra Phiên Bản AWS CLI

```bash
aws --version
```

Kết quả mong đợi: `aws-cli/2.1.16` hoặc tương tự (phiên bản 2.x)

## Gửi Dữ Liệu Đến Kinesis

### Sử Dụng API put-record

API `put-record` gửi từng bản ghi đến Kinesis stream của bạn.

**Cấu Trúc Lệnh:**

```bash
aws kinesis put-record \
  --stream-name DemoStream \
  --partition-key user1 \
  --data "user signup" \
  --cli-binary-format raw-in-base64-out
```

**Tham Số:**
- `--stream-name`: Tên của Kinesis stream
- `--partition-key`: Khóa xác định shard nào sẽ nhận dữ liệu (các bản ghi có cùng partition key sẽ đi đến cùng một shard)
- `--data`: Dữ liệu thực tế
- `--cli-binary-format raw-in-base64-out`: Bắt buộc đối với dữ liệu văn bản

### Các Lệnh Ví Dụ

```bash
# Gửi bản ghi đầu tiên
aws kinesis put-record \
  --stream-name DemoStream \
  --partition-key user1 \
  --data "user signup" \
  --cli-binary-format raw-in-base64-out

# Gửi bản ghi thứ hai
aws kinesis put-record \
  --stream-name DemoStream \
  --partition-key user1 \
  --data "user login" \
  --cli-binary-format raw-in-base64-out

# Gửi bản ghi thứ ba
aws kinesis put-record \
  --stream-name DemoStream \
  --partition-key user1 \
  --data "user logout" \
  --cli-binary-format raw-in-base64-out
```

### Phản Hồi Thành Công

```json
{
  "ShardId": "shardId-0000000000000",
  "SequenceNumber": "49590338752..."
}
```

### Xem Các Chỉ Số

Sau khi gửi bản ghi:
1. Vào tab Monitoring
2. Đặt khoảng thời gian là 1 giờ
3. Xem các chỉ số PUT record (có thể mất vài phút để xuất hiện trong CloudWatch)

## Tiêu Thụ Dữ Liệu Từ Kinesis

### Bước 1: Mô Tả Stream

Đầu tiên, lấy thông tin về cấu trúc stream của bạn:

```bash
aws kinesis describe-stream --stream-name DemoStream
```

**Phản hồi bao gồm:**
- StreamDescription
- Thông tin Shard (ví dụ: `shardId-0000000000000`)

Shard ID này cần thiết để tiêu thụ dữ liệu.

### Bước 2: Lấy Shard Iterator

```bash
aws kinesis get-shard-iterator \
  --stream-name DemoStream \
  --shard-id shardId-0000000000000 \
  --shard-iterator-type TRIM_HORIZON
```

**Các Loại Shard Iterator:**
- `TRIM_HORIZON` - Đọc từ đầu stream (tất cả bản ghi)
- `LATEST` - Chỉ đọc các bản ghi mới từ thời điểm này trở đi

**Phản Hồi:**
Trả về token `ShardIterator` được sử dụng để tiêu thụ các bản ghi.

### Bước 3: Lấy Các Bản Ghi

```bash
aws kinesis get-records --shard-iterator <ShardIterator-từ-lệnh-trước>
```

### Hiểu Phản Hồi

**Cấu Trúc Bản Ghi:**
```json
{
  "Records": [
    {
      "SequenceNumber": "...",
      "Data": "dXNlciBzaWdudXA=",
      "PartitionKey": "user1",
      "ApproximateArrivalTimestamp": "..."
    }
  ],
  "NextShardIterator": "..."
}
```

### Giải Mã Dữ Liệu Base64

Trường data được mã hóa base64. Để giải mã:

**Tùy Chọn 1: Công Cụ Trực Tuyến**
- Truy cập trang web giải mã base64
- Dán dữ liệu đã mã hóa (ví dụ: `dXNlciBzaWdudXA=`)
- Nhấp "DECODE" để xem văn bản gốc (ví dụ: "user signup")

**Tùy Chọn 2: Dòng Lệnh**
```bash
echo "dXNlciBzaWdudXA=" | base64 --decode
```

### Lặp Qua Các Bản Ghi

Phản hồi bao gồm trường `NextShardIterator`. Sử dụng giá trị này trong các lệnh gọi `get-records` tiếp theo để tiếp tục đọc từ vị trí bạn đã dừng lại.

```bash
aws kinesis get-records --shard-iterator <NextShardIterator>
```

## Các Chế Độ Tiêu Thụ

### Chế Độ Shared Consumption (Tiêu Thụ Chia Sẻ)

Phương pháp API mức thấp được trình bày trong hướng dẫn này sử dụng **chế độ shared consumption**:
- Mô tả stream thủ công
- Lấy shard iterator
- Truy xuất bản ghi với get-records

### Chế Độ Enhanced Fan-Out

Để có hiệu suất tốt hơn với nhiều consumer:
- Sử dụng **Kinesis Client Library (KCL)**
- Cung cấp API mức cao hơn
- Quản lý shard tự động
- Thông lượng dành riêng cho mỗi consumer

## Tóm Tắt

Trong hướng dẫn thực hành này, bạn đã học cách:

✅ Tạo Kinesis Data Stream  
✅ Hiểu các chế độ dung lượng On-Demand và Provisioned  
✅ Sử dụng AWS CloudShell cho các thao tác CLI  
✅ Gửi dữ liệu đến Kinesis bằng API `put-record`  
✅ Tiêu thụ dữ liệu từ Kinesis bằng API mức thấp  
✅ Giải mã dữ liệu được mã hóa base64  
✅ Lặp qua các bản ghi bằng shard iterator  

### Các Bước Tiếp Theo

Giữ stream của bạn chạy cho hướng dẫn tiếp theo về **Kinesis Data Firehose**, nơi bạn sẽ học cách chuyển dữ liệu streaming đến nhiều đích khác nhau trong AWS.

## Ghi Chú Quan Trọng

- **API Mức Thấp vs Mức Cao**: Hướng dẫn này sử dụng lệnh CLI mức thấp. Đối với các ứng dụng production, hãy xem xét sử dụng KPL (Kinesis Producer Library) và KCL (Kinesis Client Library) để có abstraction tốt hơn
- **Dọn Dẹp Tài Nguyên**: Nhớ xóa Kinesis stream của bạn sau khi hoàn thành hướng dẫn để tránh phát sinh chi phí liên tục
- **Partition Key**: Các bản ghi có cùng partition key luôn đi đến cùng một shard, đảm bảo thứ tự cho các sự kiện liên quan

---

**Hoàn thành hướng dẫn!** Bây giờ bạn đã có kinh nghiệm thực hành với Amazon Kinesis Data Streams.