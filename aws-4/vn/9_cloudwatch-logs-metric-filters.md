# Metric Filter cho CloudWatch Logs (Ghi chú học AWS)

## Mục đích
**CloudWatch Logs metric filter** dùng để quét các log event trong một **log group**. Khi log khớp **filter pattern**, CloudWatch sẽ **publish** một điểm dữ liệu vào **CloudWatch Metrics** (thường là custom metric trong custom namespace). Sau đó bạn có thể tạo **CloudWatch Alarm** để cảnh báo/automation.

Use case phổ biến: phát hiện lỗi **HTTP 4xx/5xx** trong access log và cảnh báo khi lỗi tăng.

## Tình huống (từ `file.txt`)
- Nguồn log: NGINX access logs đẩy vào **CloudWatch Logs**.
- Mục tiêu: phát hiện các response **HTTP 400**.
- Cách làm:
  1) Tạo metric filter match `400`
  2) Mỗi lần match publish giá trị `1`
  3) Tạo alarm dựa trên metric đó

## Khái niệm cần nhớ
- **Log group / log stream**: nơi log của app được ghi vào.
- **Filter pattern**: biểu thức để match log event.
- **Metric namespace**: “thư mục” chứa custom metrics (ví dụ: `MetricFilters`).
- **Metric name**: tên metric được phát ra (ví dụ: `MyDemoFilter`).
- **Metric value**: giá trị publish mỗi lần match (hay dùng `1`).
- **Default value**: giá trị khi không có match (hay dùng `0`).

## Các bước tạo metric filter (Console)
1. Mở **CloudWatch** → **Logs** → chọn **log group**.
2. Chọn **Actions** → **Create metric filter** (hoặc vào mục **Metric filters** để tạo).
3. Nhập **Filter pattern**.
   - Demo đơn giản: `400`
4. Test pattern:
   - Dùng chức năng **Test pattern** với sample events.
   - Kiểm tra số lượng match có hợp lý (ví dụ “14 match trên 50 events”).
5. Cấu hình metric:
   - **Filter name**: ví dụ `MetricFilter400Code`
   - **Metric namespace**: ví dụ `MetricFilters`
   - **Metric name**: ví dụ `MyDemoFilter`
   - **Metric value**: `1`
   - **Default value**: `0`
6. Tạo filter.

## Hành vi quan trọng
- **Metric filter không chạy hồi tố (không retroactive)**.
  - Không “đổ lại” dữ liệu metric cho log cũ.
  - Metric chỉ bắt đầu có data từ lúc filter được tạo và có **log mới** phù hợp.

## Tạo log mới để thấy metric
Nếu metric đang 0 hoặc chưa thấy:
- Restart app servers / redeploy / tạo traffic test (ví dụ gọi `/test`).
- Chờ vài phút rồi vào **CloudWatch → Metrics**.
- Tìm custom namespace (ví dụ `MetricFilters`).

## Tạo CloudWatch Alarm dựa trên metric
1. CloudWatch → **Metrics** → tìm metric trong namespace.
2. Chọn metric → **Create alarm**.
3. Chọn điều kiện:
   - Demo: **Static threshold** “Greater than 50”.
   - Thực tế: chọn threshold theo traffic và kỳ vọng hệ thống; cân nhắc period/statistic.
4. Chọn notification/action:
   - SNS topic (Email/SMS) hoặc action khác.
5. Đặt tên alarm (ví dụ `DemoMetricFilterAlarm`).

## Mẹo về pattern (thực tế)
- Bắt đầu đơn giản rồi refine để giảm false positive.
- Nếu log dạng JSON/structured, nên match theo field thay vì tìm substring.
- Với access log, nên match đúng field status code để chính xác hơn.

## Checklist xử lý sự cố
- Không thấy metric sau khi tạo:
  - Kiểm tra có log mới đổ vào không.
  - Kiểm tra pattern có match log mới không.
  - Chờ độ trễ publish metric (vài phút).
- Match quá nhiều:
  - Pattern quá rộng → cần siết lại.
- Alarm không chạy:
  - Kiểm tra period/statistic/evaluation.
  - Kiểm tra metric có vượt threshold thật không.

## Ý chính để nhớ (thi/phỏng vấn)
- Metric filter → tạo **custom metric** từ log.
- Alarm → cảnh báo/automation dựa trên metric.
- Không có backfill: **không retroactive**.
