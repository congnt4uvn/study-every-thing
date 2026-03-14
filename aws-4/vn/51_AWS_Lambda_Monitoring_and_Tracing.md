# AWS Lambda: Giám Sát và Theo Dõi

## Tổng Quan
Tài liệu này bao gồm các khả năng giám sát và theo dõi cho các hàm AWS Lambda, bao gồm CloudWatch Metrics, CloudWatch Logs, và AWS X-Ray.

## CloudWatch Metrics cho Lambda

### Truy Cập Metrics
1. Mở hàm Lambda của bạn trong AWS Console
2. Điều hướng đến tab **Monitor** (Giám sát)
3. Xem phần **Metrics** (Chỉ số)

### Các Chỉ Số Quan Trọng

#### Chỉ Số Về Lời Gọi
- **Invocations**: Số lần hàm Lambda được gọi
- **Duration**: Thời gian thực thi của mỗi lời gọi
- **Error Count**: Số lượng lời gọi thất bại
- **Success Rate**: Tỷ lệ phần trăm thực thi thành công

#### Chỉ Số Hiệu Suất
- **Throttles**: Xảy ra khi bạn vượt quá giới hạn Lambda
- **Async Delivery Failures**: Các sự kiện mà hàm không có cơ hội xử lý
- **Iterator Age**: Liên quan khi đọc từ một luồng dữ liệu (stream)
- **Concurrent Executions**: Hiển thị mức độ đồng thời của hàm Lambda
  - Các hàm ít lượt truy cập thường hiển thị 1 thực thi đồng thời
  - Các hàm có lượng truy cập cao có thể có mức đồng thời cao hơn nhiều

### Giám Sát Trực Quan
- Chỉ báo màu xanh: Thực thi thành công
- Chỉ báo màu đỏ: Đã xảy ra lỗi
- Các biểu đồ này rất quan trọng để giám sát các hàm Lambda trong môi trường production theo thời gian

## CloudWatch Logs

### Log Streams (Luồng Nhật Ký)
- Mỗi lời gọi hàm Lambda tạo ra một log stream
- Mỗi log stream chứa thông tin thực thi chi tiết

### Thông Tin Trong Log Bao Gồm:
- **Request ID**: Mã định danh duy nhất cho mỗi lời gọi
- **Console Logs**: Bất kỳ log nào được ghi vào console bởi hàm của bạn
- **Execution Reports**: Thông tin chi tiết về quá trình thực thi
  - Thời gian thực thi của hàm
  - Thông tin tính phí
  - Kích thước bộ nhớ được cấu hình
  - Bộ nhớ tối đa đã sử dụng
  - Thời gian khởi tạo (cold start time)

### Điểm Quan Trọng
- CloudWatch Logs rất cần thiết cho việc gỡ lỗi các hàm Lambda
- Log streams cung cấp chi tiết thực thi toàn diện
- Reports giúp tối ưu hóa hiệu suất và chi phí của hàm

## AWS X-Ray

### Cấu Hình
1. Vào phần **Configuration** (Cấu hình) của hàm Lambda
2. Điều hướng đến **Monitoring and Operation Tools** (Công cụ giám sát và vận hành)
3. Nhấp **Edit** (Chỉnh sửa)
4. Bật tính năng X-Ray tracing

### Tính Năng
- CloudWatch Logs được bật mặc định
- X-Ray cung cấp khả năng theo dõi phân tán
- Giúp xác định các điểm nghẽn về hiệu suất
- Hữu ích cho việc gỡ lỗi các ứng dụng serverless phức tạp

## Thực Hành Tốt Nhất

1. **Giám Sát Các Hàm Production**: Thường xuyên xem xét CloudWatch metrics cho các hàm Lambda đang chạy production
2. **Thiết Lập Cảnh Báo**: Cấu hình CloudWatch alarms cho tỷ lệ lỗi và throttles
3. **Tối Ưu Bộ Nhớ**: Sử dụng báo cáo sử dụng bộ nhớ để điều chỉnh kích thước hàm phù hợp
4. **Theo Dõi Concurrency**: Giám sát concurrent executions để hiểu các mẫu mở rộng
5. **Bật X-Ray**: Sử dụng X-Ray cho các ứng dụng phức tạp với nhiều dịch vụ

## Các Trường Hợp Sử Dụng Giám Sát

- **Kiểm Thử Destinations**: Giám sát cả success và error destinations
- **Tối Ưu Hiệu Suất**: Sử dụng các chỉ số duration và memory
- **Quản Lý Chi Phí**: Theo dõi invocations và duration để ước tính hóa đơn
- **Khắc Phục Sự Cố**: Sử dụng logs và traces để gỡ lỗi
- **Lập Kế Hoạch Năng Lực**: Giám sát throttles và concurrent executions

## Tóm Tắt

AWS Lambda cung cấp giám sát toàn diện thông qua:
- **CloudWatch Metrics**: Bảng điều khiển trực quan cho các chỉ số hiệu suất chính
- **CloudWatch Logs**: Nhật ký thực thi chi tiết cho mỗi lời gọi
- **AWS X-Ray**: Theo dõi phân tán cho các ứng dụng phức tạp

Các công cụ này kết hợp với nhau cung cấp khả năng hiển thị hoàn chỉnh về hiệu suất, lỗi và sử dụng tài nguyên của hàm Lambda.
