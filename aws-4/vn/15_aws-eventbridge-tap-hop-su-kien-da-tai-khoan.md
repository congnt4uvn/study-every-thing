# Ghi chú học AWS: Tập hợp sự kiện đa tài khoản với Amazon EventBridge

## Mục tiêu
Tập hợp (aggregate) các sự kiện từ nhiều tài khoản AWS (ví dụ: thay đổi trạng thái EC2) về **một tài khoản trung tâm** để quản lý rule/định tuyến/notify ở một nơi.

## Ý chính (theo nội dung file.txt)
- Mỗi **tài khoản nguồn** (Account A/B/C/…) tạo **EventBridge rule** với **event pattern** để bắt sự kiện (ví dụ: EC2 state change).
- **Target** của rule trong một tài khoản có thể là **event bus ở tài khoản khác** (tài khoản trung tâm).
- Để hoạt động được, **event bus của tài khoản trung tâm** cần **resource policy** cho phép các tài khoản khác gửi sự kiện vào (quyền `events:PutEvents`).
- Ở tài khoản trung tâm, bạn tạo các rule trên event bus để kích hoạt **SNS**, **Lambda**,… tuỳ nhu cầu.

## Kiến trúc tổng quan
1. **Tài khoản trung tâm**
   - Tạo hoặc dùng một event bus (thường dùng **custom event bus**, ví dụ `central-bus`).
   - Gắn **policy** cho event bus để cho phép tài khoản nguồn `PutEvents`.
   - Tạo rule tập trung và định tuyến tới SNS/Lambda/…

2. **Mỗi tài khoản nguồn**
   - Tạo rule lọc sự kiện bằng event pattern.
   - Cấu hình target trỏ tới **event bus ARN** của tài khoản trung tâm.

## Các bước triển khai (mức khái quát)
### 1) Tài khoản trung tâm: tạo/chọn event bus
- Dùng **custom event bus** giúp tách luồng sự kiện và dễ quản trị.

### 2) Tài khoản trung tâm: thêm quyền nhận sự kiện từ tài khoản khác
Bạn cần resource-based policy trên event bus trung tâm để cho phép:
- **Action**: `events:PutEvents`
- **Principal**: danh sách account ID nguồn (hoặc role cụ thể tuỳ thiết kế)
- **Resource**: ARN của event bus trung tâm

Ví dụ policy (minh hoạ):
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowPutEventsFromOtherAccounts",
      "Effect": "Allow",
      "Principal": { "AWS": ["111111111111", "222222222222"] },
      "Action": "events:PutEvents",
      "Resource": "arn:aws:events:REGION:CENTRAL_ACCOUNT_ID:event-bus/central-bus"
    }
  ]
}
```

### 3) Tài khoản nguồn: tạo rule bắt sự kiện (ví dụ EC2)
Ví dụ event pattern cho sự kiện đổi trạng thái EC2:
```json
{
  "source": ["aws.ec2"],
  "detail-type": ["EC2 Instance State-change Notification"]
}
```

### 4) Tài khoản nguồn: đặt target là event bus ở tài khoản trung tâm
- Target: event bus (khác account)
- ARN: `arn:aws:events:REGION:CENTRAL_ACCOUNT_ID:event-bus/central-bus`

### 5) Tài khoản trung tâm: tạo rule để xử lý/định tuyến
Ví dụ:
- Nếu instance chuyển sang `stopped` → gửi SNS thông báo
- Nếu `terminated` → gọi Lambda để cleanup

## Checklist nhanh để kiểm tra
- Policy của event bus trung tâm đã cho phép đúng các account nguồn.
- Rule ở account nguồn match đúng sự kiện bạn muốn (test bằng cách đổi state của EC2).
- Target ARN đúng **region** + **account ID** + **tên bus**.
- Rule ở account trung tâm được tạo trên **đúng event bus** (custom bus hay default bus).

## Lỗi hay gặp
- **Nhầm event bus**: events đổ vào custom bus nhưng rule lại tạo trên default bus.
- **Sai region**: EventBridge là theo region; cần thống nhất theo thiết kế.
- **Thiếu quyền**: không có policy thì cross-account `PutEvents` sẽ không chạy.

## Câu hỏi tự ôn
- Nên lọc sự kiện ở account nguồn, ở account trung tâm, hay cả hai?
- Khi nào dùng SNS, khi nào dùng Lambda (alert vs automation)?
- Bạn sẽ đặt naming convention cho event bus/rule như thế nào để dễ quản trị?
