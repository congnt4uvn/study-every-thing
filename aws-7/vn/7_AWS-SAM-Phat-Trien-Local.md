# Khả Năng Phát Triển Local với AWS SAM

## Tổng Quan
AWS SAM (Serverless Application Model) là một framework cung cấp khả năng phát triển local mạnh mẽ để kiểm thử và debug các hàm Lambda mà không cần deploy lên cloud.

## Các Tính Năng Chính

### 1. Endpoint Lambda Local
**Lệnh:** `sam local start-lambda`

- Khởi động các hàm AWS Lambda như các endpoint local trên máy tính của bạn
- Mô phỏng môi trường Lambda framework
- Cho phép chạy automated tests đối với các endpoint local
- Cung cấp phản hồi phát triển nhanh chóng mà không tốn chi phí cloud deployment

### 2. Gọi Lambda Function Local
**Lệnh:** `sam local invoke`

- Gọi một hàm Lambda một lần với payload được chỉ định
- Hữu ích cho việc tạo và kiểm thử các test cases cụ thể
- Tự động thoát sau khi hoàn thành việc gọi hàm

**Quan trọng:** Khi hàm Lambda của bạn tương tác với các dịch vụ AWS (ví dụ: gọi API DynamoDB), hãy sử dụng tùy chọn `--profile` để chỉ định môi trường AWS nào sẽ chạy.

```bash
sam local invoke --profile <your-profile>
```

### 3. Endpoint API Gateway Local
**Lệnh:** `sam local start-api`

- Khởi động một HTTP server local để host tất cả APIs và functions của bạn
- Cung cấp tính năng tự động reload code theo thời gian thực
- Tự động cập nhật APIs khi code của Lambda function thay đổi
- Lý tưởng cho việc kiểm thử API integrations ở local

### 4. Tạo Events cho Lambda Functions
**Lệnh:** `sam local generate-event`

Tạo sample payloads cho các nguồn sự kiện AWS khác nhau và chuyển chúng vào các lệnh gọi Lambda.

**Ví dụ:**
```bash
sam local generate-event s3 put --bucket mybucket --key mykey | sam local invoke
```

**Các Nguồn Event Được Hỗ Trợ:**
- Amazon S3
- API Gateway
- SNS (Simple Notification Service)
- Kinesis
- DynamoDB
- Và nhiều nguồn event Lambda của AWS khác

## Lợi Ích
- ✅ Chu kỳ phát triển nhanh hơn
- ✅ Giảm chi phí AWS trong quá trình phát triển
- ✅ Debug và testing dễ dàng hơn
- ✅ Không cần deploy lên cloud liên tục
- ✅ Khả năng automated testing

## Best Practices (Thực Hành Tốt Nhất)
1. Luôn sử dụng AWS profiles phù hợp khi testing các functions tương tác với các dịch vụ AWS
2. Tạo các event payloads thực tế để testing kỹ lưỡng
3. Tận dụng tính năng automatic reloading trong quá trình phát triển API
4. Tạo các test suites toàn diện sử dụng local endpoints

---

*Ghi Chú Học Tập: Hiểu rõ khả năng local của SAM là điều cần thiết cho việc phát triển ứng dụng serverless hiệu quả trên AWS.*
