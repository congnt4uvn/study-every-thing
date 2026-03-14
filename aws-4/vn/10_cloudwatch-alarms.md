# AWS CloudWatch Alarms — Ghi chú học (VI)

## CloudWatch Alarm là gì?
- CloudWatch Alarm dùng để **theo dõi một metric** và **kích hoạt thông báo/hành động** khi metric vượt ngưỡng.
- Có thể cấu hình nhiều tuỳ chọn khi đánh giá metric (ví dụ chọn thống kê như maximum, và các lựa chọn khác tuỳ loại metric).

## Trạng thái của Alarm
CloudWatch Alarm có 3 trạng thái:
- **OK**: Alarm không bị kích hoạt.
- **INSUFFICIENT_DATA**: Không đủ dữ liệu để xác định trạng thái.
- **ALARM**: Vượt ngưỡng; sẽ kích hoạt thông báo/hành động.

## Period (cửa sổ đánh giá)
- **Period** là khoảng thời gian mà alarm dùng để đánh giá metric.
- Có thể rất ngắn hoặc rất dài tuỳ nhu cầu.
- Áp dụng được cho **custom metric độ phân giải cao**, ví dụ **10 giây**, **30 giây**, hoặc bội số của **60 giây**.

## Mục tiêu của Alarm (Alarm có thể làm gì)
CloudWatch Alarm thường có 3 nhóm mục tiêu:
1) **Hành động lên EC2 instance**
   - Stop, terminate, reboot, hoặc **recover** instance.
2) **Hành động Auto Scaling**
   - Scale out / scale in.
3) **Gửi thông báo qua SNS**
   - Gửi sang **Amazon SNS**; từ SNS có thể “móc nối” sang **AWS Lambda** để chạy logic tuỳ ý.

## Composite Alarms
### Khi nào cần Composite Alarm
- CloudWatch Alarm thông thường thường gắn với **một metric**.
- Nếu cần điều kiện dựa trên **nhiều metric**, dùng **Composite Alarm**.

### Cách hoạt động
- **Composite Alarm** theo dõi **trạng thái của nhiều alarm khác**.
- Có thể kết hợp bằng điều kiện **AND / OR**.

### Lợi ích: giảm “nhiễu” cảnh báo
- Giúp giảm số lượng cảnh báo không cần thiết bằng cách đặt điều kiện tổng hợp.

### Ví dụ mô hình
- Alarm A: theo dõi **CPU** của EC2.
- Alarm B: theo dõi **IOPS** của EC2.
- Composite Alarm: `AlarmA AND AlarmB` (hoặc `AlarmA OR AlarmB`) tuỳ mục tiêu.
- Khi điều kiện composite thoả, composite alarm có thể kích hoạt hành động (ví dụ gửi SNS).

## EC2 instance recovery bằng alarm
### Status checks
- **Instance status check**: kiểm tra bản thân máy ảo EC2.
- **System status check**: kiểm tra lớp phần cứng/host bên dưới.
- **Attached EBS status check**: kiểm tra sức khoẻ các EBS volume gắn kèm.

### Hành vi khi recover
- Có thể tạo CloudWatch Alarm trên các status check này.
- Khi bị breach, có thể kích hoạt **EC2 instance recovery** (chuyển instance sang host khác).
- Sau khi recover, instance giữ nguyên:
  - **private IP**, **public IP**, và **Elastic IP**
  - **metadata**
  - **placement group**
- Có thể gửi thông báo sang **SNS topic** để biết instance đã được recover.

## Alarm từ CloudWatch Logs metric filter
- Có thể tạo alarm dựa trên **CloudWatch Logs metric filter**.
- Mẫu phổ biến: đếm số lần xuất hiện từ khoá như **"error"** trong log.
- Khi số lần vượt ngưỡng, alarm kích hoạt và gửi SNS.

## Kiểm thử alarm & thông báo
- Có thể dùng lệnh CLI **SetAlarmState** (thường gọi là “set alarm state”) để ép trạng thái alarm khi kiểm thử, kể cả khi metric chưa thật sự vượt ngưỡng.

## Câu hỏi tự ôn
- 3 trạng thái của CloudWatch Alarm là gì?
- **Period** điều khiển điều gì?
- Kể 3 loại mục tiêu/hành động mà alarm có thể kích hoạt.
- Khi nào nên dùng **Composite Alarm**?
- Instance/System/EBS status check tương ứng kiểm tra phần nào?
