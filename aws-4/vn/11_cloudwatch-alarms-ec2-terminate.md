# Ghi chú học AWS — CloudWatch Alarm (CPU EC2 → Terminate)

## Lab này minh hoạ điều gì
Bạn có thể dùng **Amazon CloudWatch Alarms** để theo dõi một metric (ví dụ **EC2 CPUUtilization**) và kích hoạt **hành động** (ví dụ **terminate EC2 instance**) khi metric vượt ngưỡng trong một khoảng thời gian được cấu hình.

Mẫu tư duy phổ biến:
- Quan sát: CloudWatch **Metrics**
- Ra quyết định: quy tắc đánh giá của **Alarm**
- Hành động: **Alarm actions** (SNS, Auto Scaling, EC2 actions, Systems Manager, ...)

## Khái niệm cần nắm
### Metric & dimensions
- **Namespace**: nơi metric thuộc về (với EC2 thường là `AWS/EC2`).
- **Metric name**: ví dụ `CPUUtilization`.
- **Dimensions**: cặp key/value để lọc đúng đối tượng, ví dụ `InstanceId=i-...`.

### Statistic & period
- **Statistic**: cách tổng hợp datapoint (Average/Sum/Maximum/Minimum, ...).
- **Period**: độ dài mỗi datapoint dùng để đánh giá alarm (thường 1 phút, 5 phút).
  - Nếu EC2 **không bật detailed monitoring**, nhiều metric sẽ có chu kỳ **5 phút**.

### Logic đánh giá
Alarm được đánh giá dựa trên:
- **Loại ngưỡng**: Static threshold hoặc Anomaly Detection.
- **Toán tử so sánh**: `GreaterThanThreshold`, ...
- **Datapoints to alarm** và **evaluation periods**.
  - Ví dụ: “**3/3** period > 95%” với period 5 phút tương đương khoảng **15 phút** CPU cao liên tục.

### Trạng thái alarm
- **OK**: trong ngưỡng.
- **ALARM**: thoả điều kiện vượt ngưỡng.
- **INSUFFICIENT_DATA**: chưa đủ datapoint (hay gặp với instance/metric mới).

## Các bước thực hiện (Console)
1. Tạo một EC2 instance nhỏ (ví dụ `t2.micro`) để test.
2. Vào **CloudWatch → Alarms → Create alarm**.
3. **Select metric**:
   - Chọn **EC2 metrics**.
   - Vào **Per-Instance Metrics**.
   - Tìm theo `InstanceId`.
   - Chọn **CPUUtilization**.
4. Cấu hình metric:
   - Statistic: thường dùng **Average**.
   - Period: **5 minutes** (phù hợp basic monitoring).
5. Cấu hình điều kiện:
   - Static threshold.
   - Ví dụ: `CPUUtilization > 95`.
   - Ví dụ đánh giá: **3 out of 3** datapoints.
6. Cấu hình hành động:
   - Khi trạng thái **ALARM**, chọn **EC2 action → Terminate instance**.
7. Đặt tên alarm (ví dụ): `EC2 on high CPU`.
8. Tạo alarm.

Lưu ý:
- Sau khi tạo, alarm có thể ở **INSUFFICIENT_DATA** cho tới khi đủ datapoint.

## Test nhanh không cần “đốt CPU” (CLI)
Thay vì tạo tải CPU cao 95%+ trong ~15 phút, bạn có thể set trạng thái alarm để test.

Ví dụ lệnh:
```bash
aws cloudwatch set-alarm-state \
  --alarm-name "EC2 on high CPU" \
  --state-value ALARM \
  --state-reason "testing"
```

Kỳ vọng:
- Alarm chuyển sang **ALARM**.
- Action được chạy (trong lab này: terminate EC2 instance).
- Kiểm tra tại:
  - **Alarm History** trong CloudWatch
  - Trạng thái EC2: shutting-down → terminated

## Lưu ý an toàn (quan trọng)
- **Terminate là huỷ tài nguyên** (mất dữ liệu trên instance store / EBS tuỳ cấu hình). Chỉ làm với instance dùng để test.
- Áp dụng IAM least privilege; terminate cần quyền như `ec2:TerminateInstances`.
- Trong production, cân nhắc hành động an toàn hơn (notify, restart/recover, scale out) trước khi terminate.

## Checklist / xử lý sự cố nhanh
- Không thấy metric?
  - Chờ vài phút sau khi launch; metric có thể lên chậm.
- Alarm cứ `INSUFFICIENT_DATA`?
  - Chờ đủ số datapoint (tuỳ period và evaluation periods).
- Chọn period không đúng?
  - Basic monitoring thường 5 phút; detailed monitoring hỗ trợ 1 phút.
- Action không chạy?
  - Xem **Alarm History**, đảm bảo alarm thực sự vào trạng thái **ALARM** và đã gắn action.

## Câu hỏi luyện tập
1. Nếu period 1 phút và bạn cấu hình “5 out of 5”, cần CPU vượt ngưỡng bao lâu?
2. Khi nào nên dùng `Maximum` thay vì `Average` cho CPU?
3. Khi nào nên chọn Anomaly Detection thay vì static threshold?

## Gợi ý mở rộng (tuỳ chọn)
- Thay terminate bằng:
  - SNS notification
  - Auto Scaling policy
  - SSM Automation action
- Tạo thêm alarm cho `StatusCheckFailed` và so sánh.
