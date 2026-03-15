# Triển Khai Canary với AWS API Gateway

## Tổng Quan
Triển khai Canary là một chiến lược trong AWS API Gateway cho phép bạn kiểm tra các phiên bản API mới bằng cách dần dần triển khai chúng đến một tỷ lệ phần trăm nhỏ người dùng trước khi triển khai cho tất cả người dùng. Điều này giảm thiểu rủi ro khi giới thiệu các thay đổi có thể gây lỗi.

## Các Khái Niệm Chính

### Triển Khai Canary Là Gì?
- Một chiến lược triển khai định tuyến một phần trăm lưu lượng truy cập đến phiên bản mới trong khi giữ phần còn lại ở phiên bản ổn định
- Cho phép kiểm tra an toàn các thay đổi mới trong môi trường production
- Có thể được thăng cấp lên triển khai đầy đủ hoặc rollback nếu phát hiện vấn đề

### Các Phiên Bản Lambda Function
- Lambda function có thể có nhiều phiên bản (v1, v2, v.v.)
- Mỗi phiên bản có thể được gọi độc lập
- Các phiên bản được chỉ định bằng ký hiệu dấu hai chấm (ví dụ: `function-name:1`)

## Hướng Dẫn Từng Bước

### 1. Tạo API Gateway Resource
1. Tạo một resource mới có tên `canary-demo`
2. Thêm phương thức GET với tích hợp Lambda function
3. Bật tích hợp Lambda proxy
4. Liên kết với Lambda function `stage-variables-get`

### 2. Cấu Hình Phiên Bản Lambda
- Trỏ đến phiên bản 1 bằng cách thêm `:1` vào tên Lambda function
- Phiên bản 1 trả về: "Hello from Lambda v1"
- Phiên bản 2 trả về: "Hello from Lambda v2"

### 3. Kiểm Tra Thiết Lập Ban Đầu
```
GET /canary-demo
Response: "Hello from Lambda v1"
```

### 4. Triển Khai Đến Stage
1. Triển khai API đến một stage mới
2. Đặt tên stage là "canary"
3. Kiểm tra invoke URL: `/canary/canary-demo`
4. Xác nhận phản hồi: "Hello from Lambda v1"

### 5. Tạo Triển Khai Canary
1. Điều hướng đến tab Canary trong stage
2. Nhấp "Create Canary"
3. Đặt tỷ lệ phân phối:
   - **Cho demo**: 50% canary / 50% stage hiện tại
   - **Cho production**: Thường là 10-20% cho canary
4. Tạo canary

### 6. Cập Nhật Lên Phiên Bản 2
1. Quay lại Resources
2. Chọn phương thức GET trên `canary-demo`
3. Chỉnh sửa integration request
4. Thay đổi từ phiên bản 1 (`:1`) sang phiên bản 2 (`:2`)
5. Lưu thay đổi
6. Kiểm tra: Bây giờ sẽ trả về "Hello from Lambda v2"

### 7. Triển Khai Đến Canary
1. Triển khai API
2. Chọn stage "Canary"
3. Hoàn tất triển khai

### 8. Kiểm Tra Phân Phối Canary
- Điều hướng đến invoke URL và làm mới nhiều lần
- Quan sát các phản hồi xen kẽ:
  - "Hello from Lambda v1" (50% yêu cầu)
  - "Hello from Lambda v2" (50% yêu cầu)
- Điều này xác nhận canary đang định tuyến lưu lượng giữa các phiên bản

### 9. Thăng Cấp Canary
1. Sau khi kiểm tra hoàn tất và v2 được xác minh
2. Nhấp "Promote Canary"
3. Điều này cập nhật toàn bộ stage lên triển khai canary
4. Tất cả lưu lượng (100%) bây giờ đi đến phiên bản 2
5. Kiểm tra: Tất cả yêu cầu trả về "Hello from Lambda v2"

## Tóm Tắt

**Quy Trình Triển Khai Canary:**
1. Sửa đổi API resource/method của bạn
2. Tạo canary trong stage của bạn với tỷ lệ lưu lượng mong muốn
3. Triển khai các thay đổi đến canary
4. Kiểm tra với phân phối lưu lượng chia tách
5. Thăng cấp canary lên production (100% lưu lượng) khi sẵn sàng

**Lợi Ích:**
- Giảm thiểu rủi ro khi triển khai thay đổi
- Khả năng kiểm tra trong production với lưu lượng thực
- Dễ dàng rollback nếu phát hiện vấn đề
- Đường dẫn di chuyển dần dần cho các cập nhật API

**Thực Hành Tốt Nhất:**
- Bắt đầu với tỷ lệ phần trăm nhỏ (5-10%) cho các API quan trọng
- Giám sát các metrics trong quá trình triển khai canary
- Sử dụng CloudWatch để theo dõi lỗi và độ trễ
- Đặt giới hạn thời gian cho việc kiểm tra canary trước khi thăng cấp hoặc rollback
