# AWS Lambda - Synchronous Invocations (Gọi Đồng Bộ)

## Tổng Quan
Synchronous invocations (gọi đồng bộ) trong AWS Lambda xảy ra khi người gọi chờ đợi hàm hoàn thành và nhận kết quả ngay lập tức.

## Khái Niệm Chính

### Synchronous Invocation Là Gì?
- Người gọi chờ đợi Lambda function hoàn thành việc thực thi
- Kết quả được trả về trực tiếp cho người gọi
- Nếu thực thi mất 2 phút, bạn sẽ đợi 2 phút để nhận kết quả
- Phổ biến khi kiểm tra hàm thông qua giao diện AWS Console

## Phương Pháp Kiểm Tra

### 1. Giao Diện AWS Console
- Điều hướng đến Lambda function của bạn
- Sử dụng nút "Test"
- Thao tác này thực hiện synchronous invocation
- Kết quả hiển thị trực tiếp trên cửa sổ console

### 2. AWS CLI (Command Line Interface - Giao Diện Dòng Lệnh)

#### Thiết Lập
Bạn có thể sử dụng:
- **AWS CloudShell** (có sẵn ở các vùng được hỗ trợ)
- **Terminal Cục Bộ** với AWS CLI đã cài đặt

#### Kiểm Tra Phiên Bản CLI
```bash
aws --version
```
Mong đợi: AWS CLI phiên bản 2.x

#### Liệt Kê Các Lambda Functions
```bash
aws lambda list-functions
```

**Lưu ý:** Nếu sử dụng CLI trong terminal cục bộ (không phải CloudShell), thêm cờ region:
```bash
aws lambda list-functions --region eu-west-1
```

#### Gọi Lambda Function Đồng Bộ
```bash
aws lambda invoke \
  --function-name hello-world \
  --payload '{"key": "value"}' \
  --cli-binary-format raw-in-base64-out \
  response.json
```

**Lưu Ý Quan Trọng:**
- Xóa tham số `--region` nếu sử dụng CloudShell (region được tự động phát hiện)
- Đối với CLI v1, cú pháp lệnh có thể khác một chút
- Kết quả được ghi vào tệp được chỉ định (`response.json`)

## Các Lỗi Thường Gặp

### Lỗi Function Not Found (Không Tìm Thấy Hàm)
- Xác minh tên hàm chính xác
- Đảm bảo bạn đang ở đúng region
- Kiểm tra xem hàm có tồn tại trong tài khoản AWS của bạn không

## Sự Khác Biệt Giữa Các Phiên Bản CLI
- **CLI v2** (được khuyến nghị): Cú pháp lệnh hiện tại như hiển thị ở trên
- **CLI v1** (cũ hơn): Có thể có cấu trúc lệnh hơi khác
- Luôn sử dụng CLI v2 khi có thể

## Thực Hành Tốt Nhất
1. Sử dụng CloudShell để kiểm tra nhanh mà không cần thiết lập cục bộ
2. Luôn xác minh region của bạn khi sử dụng CLI cục bộ
3. Kiểm tra phiên bản CLI để đảm bảo tương thích với các lệnh
4. Sử dụng synchronous invocations để nhận phản hồi và kiểm tra ngay lập tức
5. Cân nhắc asynchronous invocations cho các tác vụ chạy lâu

## Trường Hợp Sử Dụng Cho Synchronous Invocations
- Ứng dụng tương tác yêu cầu phản hồi ngay lập tức
- Tích hợp API Gateway
- Kiểm tra và gỡ lỗi Lambda functions
- Quy trình làm việc request-response (yêu cầu-phản hồi)

---
*Tài Liệu Học Tập: AWS Lambda Synchronous Invocations*
