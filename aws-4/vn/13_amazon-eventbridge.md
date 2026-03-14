# Amazon EventBridge (trước đây là CloudWatch Events) — Ghi chú học

## EventBridge là gì?
Amazon EventBridge là dịch vụ định tuyến sự kiện (event routing) nằm ở giữa **nguồn sự kiện (sources)** và **đích nhận (targets/destinations)**.

## Khả năng chính
- **Lập lịch / cron**: chạy tác vụ theo thời gian (ví dụ mỗi giờ, mỗi 4 giờ, mỗi Thứ Hai 8:00, Thứ Hai đầu tiên của tháng).
- **Khớp mẫu sự kiện (event pattern)**: phản ứng khi một dịch vụ AWS phát sinh sự kiện.

## Luồng hoạt động (mô hình tư duy)
1. **Nguồn** tạo sự kiện (hoặc lịch/schedule tạo sự kiện).
2. **Rule của EventBridge** lọc/chọn sự kiện (ví dụ chỉ lấy sự kiện của một S3 bucket cụ thể).
3. EventBridge tạo/đẩy **tài liệu JSON sự kiện** (payload chứa chi tiết như resource ID, thời gian, IP, …).
4. Sự kiện được gửi tới một hoặc nhiều **target**.

## Nguồn sự kiện (ví dụ)
- **EC2**: thay đổi trạng thái instance (start/stop/terminate)
- **CodeBuild**: build thất bại
- **S3**: sự kiện khi object được upload
- **Trusted Advisor**: phát hiện (finding) mới, ví dụ liên quan bảo mật
- **CloudTrail + EventBridge**: chặn/bắt *mọi API call* trong AWS account (mẫu rất mạnh cho audit/automation)

## Target / điểm đến (ví dụ)
EventBridge có thể đẩy sự kiện tới nhiều dịch vụ, gồm:
- **AWS Lambda**
- **SNS / SQS**
- **Kinesis Data Streams**
- **Step Functions**
- **CodePipeline / CodeBuild** (tự động hoá CI/CD)
- **ECS task / AWS Batch job**
- **SSM Automation**
- **EC2 actions** (start/stop/restart)

## Event bus
- **Default event bus**: các dịch vụ AWS thường publish event vào đây.
- **Partner event bus**: đối tác SaaS có thể gửi event thẳng vào account của bạn (ví dụ trong bài: Zendesk, Datadog, Auth0; tuỳ danh sách partner).
- **Custom event bus**: ứng dụng của bạn tự phát event vào bus do bạn tạo.

## Cross-account
Có thể truy cập event bus **cross-account** thông qua **resource-based policies**.

## Ví dụ thực tế dễ nhớ
- **Cảnh báo bảo mật**: khi **IAM root user đăng nhập**, gửi vào **SNS** để nhận email thông báo.
- **Tự động hoá theo giờ**: mỗi giờ trigger **Lambda** chạy script.
- **Tự động hoá theo S3**: khi upload object lên bucket, trigger xử lý tiếp theo.

## Từ khoá dễ gặp trong exam
Nếu thấy:
- “**cron**”, “scheduled rule”, “run every X” → nghĩ đến **EventBridge schedule**
- “react to service events”, “event pattern” → nghĩ đến **EventBridge rule**
- “route to Lambda/SNS/SQS/Step Functions/CodePipeline” → nghĩ đến **EventBridge targets**
- “SaaS partner events” → nghĩ đến **Partner event bus**
- “app tự phát event” → nghĩ đến **Custom event bus**
