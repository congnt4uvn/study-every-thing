# AWS X-Ray với Elastic Beanstalk (EB) — Ghi chú học

## Mục tiêu
Bật tracing AWS X-Ray cho môi trường Elastic Beanstalk, đảm bảo:
- X-Ray daemon chạy trên các EC2 instance của EB.
- EC2 instance profile (IAM role) có quyền để gửi trace lên dịch vụ X-Ray.
- Code ứng dụng được instrument (gắn SDK/cấu hình) để phát sinh và gửi trace.

## Ý chính
Các nền tảng Elastic Beanstalk thường **đã có sẵn X-Ray daemon**, nên bạn thường **không cần đóng gói daemon**. Việc cần làm chủ yếu là **bật daemon**, kiểm tra **IAM role**, và **instrument ứng dụng**.

## Điều kiện cần
- Một Elastic Beanstalk environment.
- IAM role gắn với EC2 instance (instance profile).
- Ứng dụng đã tích hợp AWS X-Ray SDK (hoặc cơ chế auto-instrumentation phù hợp).

## Cách A — Bật X-Ray trong Elastic Beanstalk Console
1. Tạo hoặc mở một EB environment.
2. Vào **Configuration**.
3. Tìm phần **Monitoring** (tên mục có thể thay đổi theo platform/version).
4. Bật **Amazon X-Ray** / **X-Ray daemon**.
5. Apply thay đổi.

Kết quả: X-Ray daemon sẽ chạy trên các EC2 instance của EB.

## Cách B — Bật bằng file `.ebextensions`
Nếu bạn muốn bật bằng cấu hình trong source bundle:

- Tạo thư mục: `.ebextensions/`
- Thêm file, ví dụ: `.ebextensions/xray-daemon.config`

Ví dụ cấu hình tối giản (mang tính minh hoạ để “enable daemon”):

```yaml
option_settings:
  aws:elasticbeanstalk:xray:
    XRayEnabled: true
```

Lưu ý:
- Namespace/key có thể khác nhau tuỳ platform, nhưng ý của bài là: **chỉ cần một cấu hình rất nhỏ là có thể bật daemon**.
- File phải có đuôi `.config`.

## IAM — Quyền của instance profile (rất quan trọng)
X-Ray daemon cần quyền để ghi dữ liệu trace lên AWS X-Ray.

Thông thường, role mặc định của EB (hay gặp tên kiểu **aws-elasticbeanstalk-ec2-role**) có sẵn policy (ví dụ “Web Tier policy”) bao gồm quyền cho X-Ray.

Nếu bạn dùng **custom role**, hãy đảm bảo role đó có đủ quyền liên quan đến X-Ray (gửi trace segments/telemetry, đọc sampling rules, v.v.).

Checklist:
- EB environment đang dùng đúng **EC2 instance profile**.
- Role đó có các quyền X-Ray cần thiết.

## Instrument ứng dụng (cũng bắt buộc)
Bật daemon chưa đủ—ứng dụng phải tạo và gửi trace.

Checklist:
- Thêm AWS X-Ray SDK (hoặc tương đương) vào ứng dụng.
- Instrument request vào và các call ra (HTTP client, DB, AWS SDK…) theo hướng dẫn của ngôn ngữ/framework.
- Đảm bảo app gửi segments/subsegments tới daemon (thường chạy local trên instance).

## Lưu ý với Multi-container / Docker
Nếu bạn chạy **multi-container Docker** trên Elastic Beanstalk, bạn có thể phải tự quản lý X-Ray daemon (ví dụ chạy dạng sidecar container), tương tự cách làm trong ECS.

## Kiểm tra
- Tạo traffic vào ứng dụng.
- Vào **AWS X-Ray console** để xem:
  - Service map
  - Traces của service EB

Nếu app chỉ là trang “Congratulations” và chưa instrument, bạn có thể không thấy trace hữu ích.

## Dọn dẹp
- Nhớ terminate EB environment sau khi học/xong demo để tránh tốn chi phí.

## Tự kiểm tra nhanh
- 3 điều kiện để tracing chạy end-to-end là gì? (Daemon bật, IAM đúng, app instrument)
- Với multi-container Docker khác gì? (Có thể phải tự chạy/quản lý daemon)
