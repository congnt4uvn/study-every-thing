# AWS CloudFront Real-Time Logs (Nhật Ký Thời Gian Thực)

## Tổng Quan

CloudFront Real-Time Logs cho phép bạn nhận tất cả các yêu cầu (requests) được gửi đến CloudFront theo thời gian thực bằng cách chuyển chúng đến Kinesis Data Stream. Tính năng này giúp bạn giám sát, phân tích và thực hiện các hành động dựa trên hiệu suất phân phối nội dung.

## Kiến Trúc

### Luồng Xử Lý Thời Gian Thực

1. **Người dùng** gửi yêu cầu đến **CloudFront**
2. Khi bật real-time logs, tất cả các yêu cầu sẽ được ghi lại vào **Kinesis Data Stream**
3. **Lambda function** có thể xử lý các bản ghi này từ Kinesis Data Stream để xử lý ngay lập tức

### Luồng Xử Lý Gần Thời Gian Thực

Đối với xử lý theo lô gần thời gian thực:

1. **Người dùng** gửi yêu cầu đến **CloudFront**
2. CloudFront gửi logs đến **Kinesis Data Stream** (CloudFront chỉ có thể gửi đến Kinesis Data Stream)
3. **Kinesis Data Firehose** xử lý các bản ghi theo lô (batches)
4. Dữ liệu được chuyển đến các đích như **Amazon S3**, **OpenSearch**, hoặc các đích được hỗ trợ khác

## Tính Năng Chính

### Tỷ Lệ Lấy Mẫu (Sampling Rate)

Bạn có thể cấu hình tỷ lệ lấy mẫu, giúp xác định tỷ lệ phần trăm các yêu cầu được gửi đến Kinesis Data Stream. Điều này đặc biệt hữu ích cho các API hoặc endpoint có lưu lượng truy cập cao, nơi việc ghi lại mọi yêu cầu có thể không cần thiết.

### Tùy Chỉnh Trường và Cache Behaviors

Real-time logs cho phép bạn chỉ định:

- **Những trường nào** sẽ được bao gồm trong logs
- **Cache behaviors hoặc path patterns nào** cần được giám sát

**Ví dụ**: Bạn có thể cấu hình logging chỉ ghi lại các yêu cầu khớp với path pattern `/images/*`, cho phép bạn tập trung vào các loại traffic cụ thể.

## Các Trường Hợp Sử Dụng

- **Giám sát hiệu suất**: Theo dõi các chỉ số phân phối nội dung theo thời gian thực
- **Phân tích bảo mật**: Phát hiện và phản ứng với các mẫu đáng ngờ
- **Phân tích lưu lượng truy cập**: Hiểu hành vi người dùng và các mẫu truy cập
- **Thông tin vận hành**: Đưa ra quyết định dựa trên dữ liệu yêu cầu thực tế

## Lợi Ích

- Khả năng hiển thị dữ liệu yêu cầu CloudFront theo thời gian thực
- Lấy mẫu linh hoạt để kiểm soát khối lượng dữ liệu
- Ghi log có chọn lọc dựa trên cache behaviors
- Tích hợp với các dịch vụ phân tích và xử lý của AWS