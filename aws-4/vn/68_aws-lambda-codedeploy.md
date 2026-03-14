# Triển khai AWS Lambda với CodeDeploy

## Tổng quan
CodeDeploy tích hợp với AWS Lambda để tự động hóa việc chuyển đổi lưu lượng (traffic shifting) cho các Lambda aliases, dựa trên tính năng versions và aliases của Lambda. Điều này đặc biệt hữu ích khi triển khai Serverless Application Model (SAM) framework.

## Khái niệm Traffic Shifting
Khi nâng cấp một PROD alias từ Lambda function Version 1 (V1) lên Version 2 (V2), CodeDeploy dần dần chuyển lưu lượng từ 100% V1 sang 100% V2 theo thời gian.

**Ví dụ quy trình:**
- Bắt đầu: 100% V1, 0% V2
- Bước 1: 90% V1, 10% V2
- Bước 2: 50% V1, 50% V2
- Kết thúc: 0% V1, 100% V2

## Các chiến lược triển khai

### 1. Linear Deployment (Triển khai tuyến tính)
Tăng lưu lượng dần đều theo phần trăm cố định mỗi N phút cho đến khi đạt 100%.

**Các tùy chọn có sẵn:**
- `Linear10PercentEvery3Minutes` - Tăng 10% lưu lượng mỗi 3 phút
- `Linear10PercentEvery10Minutes` - Tăng 10% lưu lượng mỗi 10 phút

### 2. Canary Deployment (Triển khai thử nghiệm)
Thử nghiệm với X% lưu lượng, sau đó chuyển ngay sang 100%.

**Các tùy chọn có sẵn:**
- `Canary10Percent5Minutes` - Chuyển 10% lưu lượng sang V2 trong 5 phút, sau đó chuyển sang 100%
- `Canary10Percent30Minutes` - Chuyển 10% lưu lượng sang V2 trong 30 phút, sau đó chuyển sang 100%

### 3. AllAtOnce Deployment (Triển khai tức thì)
Chuyển đổi lưu lượng ngay lập tức từ V1 sang V2.

**Đặc điểm:**
- ✅ Phương pháp triển khai nhanh nhất
- ⚠️ Nguy hiểm nhất - không có giai đoạn thử nghiệm dần dần
- ❌ Rủi ro cao nếu V2 chưa được kiểm tra kỹ lưỡng

## Cơ chế Rollback (Khôi phục)

### Kiểm tra sức khỏe
CodeDeploy hỗ trợ các traffic hooks trước và sau để giám sát tình trạng Lambda function trong quá trình triển khai.

### Phát hiện lỗi
- **Traffic Hooks** - Có thể phát hiện và báo cáo lỗi trong quá trình triển khai
- **CloudWatch Alarms** - Có thể kích hoạt khi các metrics cho thấy có vấn đề

### Tự động Rollback
Khi phát hiện lỗi thông qua traffic hooks hoặc CloudWatch alarms, CodeDeploy tự động thực hiện rollback về phiên bản ổn định trước đó.

## Tích hợp với SAM
Tính năng CodeDeploy được tích hợp đầy đủ trong SAM (Serverless Application Model) framework, cho phép thực hành và triển khai các Lambda function deployments.

---

**Điểm cần nhớ:**
- Luôn kiểm tra các Lambda version mới trước khi triển khai production
- Sử dụng chiến lược Canary hoặc Linear để triển khai an toàn hơn
- Thiết lập giám sát và CloudWatch alarms phù hợp
- Cấu hình traffic hooks để kiểm tra sức khỏe tự động
- AllAtOnce chỉ nên dùng khi hoàn toàn tin tưởng vào phiên bản mới
