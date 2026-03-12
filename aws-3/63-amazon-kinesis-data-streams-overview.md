# Tổng Quan về Amazon Kinesis Data Streams

## Giới Thiệu

Amazon Kinesis Data Streams là dịch vụ được sử dụng để thu thập và lưu trữ dữ liệu streaming theo thời gian thực. Khái niệm chính cần nhớ là dịch vụ này được thiết kế để xử lý dữ liệu **theo thời gian thực** (real-time).

## Dữ Liệu Thời Gian Thực Là Gì?

Dữ liệu thời gian thực là dữ liệu được tạo ra và sử dụng ngay lập tức. Các ví dụ phổ biến bao gồm:

- **Click streams**: Tương tác của người dùng trên website
- **Thiết bị IoT**: Các thiết bị kết nối internet như xe đạp thông minh
- **Metrics và logs**: Dữ liệu giám sát máy chủ cần xử lý ngay lập tức

## Tổng Quan Kiến Trúc

### Producers (Nhà Sản Xuất)

Producers chịu trách nhiệm gửi dữ liệu vào Kinesis Data Streams:

- **Ứng dụng tùy chỉnh**: Code bạn viết để thu thập dữ liệu từ website hoặc thiết bị
- **Kinesis Agent**: Agent có thể cài đặt trên server để thu thập metrics và logs

### Kinesis Data Streams

Thành phần trung tâm nhận và lưu trữ dữ liệu streaming theo thời gian thực.

### Consumers (Người Tiêu Thụ)

Các ứng dụng consumer xử lý dữ liệu từ Kinesis Data Streams:

- **Ứng dụng tùy chỉnh**: Code bạn viết để đọc và xử lý dữ liệu stream
- **AWS Lambda functions**: Các hàm serverless có thể đọc từ streams
- **Amazon Data Firehose**: Để phân phối dữ liệu đến nhiều đích khác nhau
- **Managed Service for Apache Flink**: Để phân tích thời gian thực

## Tính Năng Chính

### Lưu Trữ Dữ Liệu
- Dữ liệu có thể được lưu trữ trên stream **tối đa 365 ngày**
- Dữ liệu được lưu trữ cho phép xử lý lại và phát lại
- Dữ liệu không thể xóa thủ công; nó tự hết hạn dựa trên thời gian lưu trữ

### Thông Số Kỹ Thuật
- Kích thước dữ liệu tối đa: **10 MB mỗi bản ghi**
- Use case điển hình: Khối lượng lớn các điểm dữ liệu thời gian thực nhỏ
- **Thứ tự dữ liệu**: Được đảm bảo khi sử dụng cùng partition ID
- Partition ID cho phép bạn chỉ định các điểm dữ liệu liên quan theo thời gian

### Bảo Mật
- **Mã hóa at-rest**: Mã hóa KMS
- **Mã hóa in-flight**: Mã hóa HTTPS

## Thư Viện Tối Ưu

### Cho Producers
- **Kinesis Producer Library (KPL)**: Được thiết kế cho các thao tác ghi có throughput cao

### Cho Consumers
- **Kinesis Client Library (KCL)**: Được tối ưu hóa cho việc tiêu thụ dữ liệu hiệu quả

## Các Chế Độ Công Suất

### Chế Độ Provisioned (Được Cung Cấp Trước)

**Cấu hình:**
- Tự chọn số lượng shards cho stream của bạn
- Mỗi shard cung cấp:
  - **Công suất ghi**: 1 MB/giây hoặc 1,000 bản ghi/giây
  - **Công suất đọc**: 2 MB/giây

**Ví dụ về Scale:**
- Để xử lý 10,000 bản ghi/giây hoặc 10 MB/giây, bạn cần 10 shards

**Quản lý:**
- Scale thủ công để điều chỉnh số lượng shards
- Yêu cầu giám sát các chỉ số throughput
- **Giá**: Trả phí theo mỗi shard được cung cấp mỗi giờ

### Chế Độ On-Demand (Theo Yêu Cầu)

**Cấu hình:**
- Không cần cung cấp hoặc quản lý công suất
- **Công suất mặc định**: 4,000 bản ghi/giây hoặc 4 MB/giây đầu vào
- Tự động scale dựa trên throughput quan sát được trong 30 ngày qua

**Giá:**
- Trả phí theo stream mỗi giờ
- Tính phí dựa trên khối lượng dữ liệu thực tế vào và ra

## Các Trường Hợp Sử Dụng

Kinesis Data Streams lý tưởng cho:
- Phân tích thời gian thực
- Thu thập dữ liệu log và sự kiện
- Nhập dữ liệu IoT
- Phân tích click stream
- Giám sát và cảnh báo thời gian thực

## Tóm Tắt

Amazon Kinesis Data Streams cung cấp giải pháp streaming dữ liệu thời gian thực mạnh mẽ và có khả năng mở rộng. Với các tính năng như lưu trữ dữ liệu, đảm bảo thứ tự, và các chế độ công suất linh hoạt, nó đóng vai trò là thành phần quan trọng trong kiến trúc dữ liệu thời gian thực hiện đại. Chọn chế độ provisioned cho khối lượng công việc có thể dự đoán hoặc chế độ on-demand cho các mẫu traffic thay đổi.