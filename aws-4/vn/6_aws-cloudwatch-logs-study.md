# AWS CloudWatch Logs — Ghi chú học tập (Dựa trên `file.txt`)

## 1) CloudWatch Logs là gì?
CloudWatch Logs là dịch vụ AWS dùng để **thu thập, lưu trữ, tìm kiếm và phân tích log** từ các dịch vụ AWS và từ ứng dụng của bạn.

Trong console, bạn sẽ làm việc chủ yếu với:
- **Log group**: “thùng chứa” cấp cao (thường theo ứng dụng/dịch vụ).
- **Log stream**: chuỗi log events phát sinh từ một nguồn cụ thể (ví dụ: một Lambda, một EC2 instance, một container task, …).

## 2) Log group & log stream (mô hình tư duy quan trọng)
- Một **log group** có thể chứa nhiều **log streams**.
- Một **log stream** thường tương ứng với một nguồn tạo log.
- Khi dùng **SSM Run Command**, bạn có thể thấy các stream đại diện cho:
  - Các **instance ID** khác nhau
  - Hai kênh output tách riêng như **stdout** và **stderr**

Mẫu thường gặp trong phần minh hoạ:
- Cùng một Run Command ID chạy trên nhiều instance
- Mỗi instance có stream cho `stdout` và `stderr`

## 3) Đọc log và tìm kiếm nhanh
Trong một log stream, bạn có thể:
- Xem từng dòng log/event
- Tìm theo từ khoá (ví dụ: `http`, `installing`) để lọc nhanh các dòng liên quan

Gợi ý: tìm từ khoá trong stream là bước “nhanh-gọn” trước khi chuyển sang Logs Insights.

## 4) Metric filters (biến mẫu log thành metric)
**Metric filter** sẽ quét log events mới trong log group và khi match mẫu, nó sẽ **đẩy dữ liệu metric** sang CloudWatch Metrics.

Quy trình điển hình (trên console):
1. Mở một log group
2. Tạo **metric filter**
3. Nhập **filter pattern** (ví dụ: `installing`)
4. Test pattern trên log mẫu để xem số lượng matches
5. Cấu hình metric:
   - **Filter name** (ví dụ: `DemoMetricFilter`)
   - **Metric namespace** (custom, ví dụ: `DemoFilter`)
   - **Metric name** (ví dụ: `DemoMetric`)
   - **Metric value** (thường dùng `1` để đếm số lần xuất hiện)

Lưu ý:
- Metric có thể chưa thấy ngay nếu hiện tại không có log mới match pattern được gửi vào.
- Metric filters rất hay dùng để đo lỗi/cảnh báo/sự kiện quan trọng chỉ xuất hiện trong log.

## 5) Tạo Alarm dựa trên metric filter
Khi metric đã có, bạn có thể tạo **CloudWatch Alarm**:
- Kích hoạt khi metric vượt/ngang ngưỡng
- Dùng để cảnh báo (hoặc tự động hoá) khi một mẫu log xảy ra quá nhiều

## 6) Subscription filters (đẩy log ra ngoài)
**Subscription filter** dùng để forward log events (theo điều kiện match) tới các đích như:
- Amazon OpenSearch/Elasticsearch
- Amazon Kinesis Data Streams
- Amazon Kinesis Data Firehose
- AWS Lambda (tự xử lý/biến đổi log)

Giới hạn quan trọng (được nhắc trong walkthrough):
- Mỗi log group tối đa **2 subscription filters**

## 7) Retention (thời gian lưu log)
Bạn có thể cấu hình thời gian giữ log:
- Từ **never expire** đến các mốc retention cố định (trong console minh hoạ có tới 120 tháng / 10 năm)

Retention là “đòn bẩy” quan trọng để tối ưu chi phí.

## 8) Export log sang Amazon S3
Trong log group, bạn có thể **export data** sang S3:
- Chọn khoảng thời gian cần export
- Có thể lọc theo **log stream prefix** nếu chỉ muốn một số streams
- Chọn S3 bucket và bucket prefix

Hữu ích cho lưu trữ lâu dài hoặc phân tích downstream.

## 9) Mã hoá log group bằng KMS
Khi tạo log group, bạn có thể chọn **KMS key**.
- Nếu cấu hình, log group sẽ hiển thị thông tin mã hoá/KMS Key ID.

## 10) CloudWatch Logs Insights (ngôn ngữ query cho log)
Logs Insights cho phép dùng query language để phân tích log trên một hoặc nhiều log groups.

Mẹo sử dụng:
- Nếu query không ra dữ liệu, kiểm tra **time range** (ví dụ: 1 giờ gần nhất vs 60 ngày).
- Có thể **export kết quả** query.
- Có thể **lưu query** để dùng lại.
- Console có sẵn các query mẫu/use case (ví dụ: thống kê latency theo 5 phút cho Lambda, top nguồn/đích trong VPC Flow Logs).

## 11) Checklist luyện tập nhanh
- Nhận diện log groups do service tạo (Lambda, Glue, DataSync, SSM Run Command).
- Mở một log group và hiểu cấu trúc log streams (instance ID, stdout/stderr).
- Tìm từ khoá trong stream (ví dụ: `installing`).
- Tạo metric filter để đếm số lần xuất hiện của từ khoá.
- Tạo alarm dựa trên metric đó.
- Xem các đích subscription filter và nhớ giới hạn “2 per log group”.
- Thử set retention cho một log group test.
- Export một khoảng thời gian nhỏ sang S3.
- Chạy một query Logs Insights, sau đó mở rộng time range nếu cần.
