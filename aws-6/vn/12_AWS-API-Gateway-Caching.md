# AWS API Gateway Caching

## Tổng Quan

Caching (bộ nhớ đệm) trong API Gateway giúp giảm số lượng lời gọi đến backend bằng cách lưu trữ các phản hồi và phục vụ chúng trực tiếp từ cache khi có sẵn.

## Cách Hoạt Động

1. **Luồng Yêu Cầu Từ Client:**
   - Client gửi yêu cầu đến API Gateway
   - API Gateway kiểm tra cache trước
   - Nếu **cache hit** (có dữ liệu): Trả về kết quả đã lưu ngay lập tức
   - Nếu **cache miss** (không có dữ liệu): Chuyển yêu cầu đến backend và lưu phản hồi vào cache

2. **Mục Đích:**
   - Giảm áp lực lên hệ thống backend
   - Cải thiện thời gian phản hồi
   - Giảm chi phí bằng cách giảm số lần gọi backend

## Cấu Hình Cache

### Thời Gian Tồn Tại (TTL - Time to Live)
- **Mặc định:** 300 giây (5 phút)
- **Tối thiểu:** 0 giây (không có caching)
- **Tối đa:** 3,600 giây (1 giờ)

### Kích Thước Cache
- **Phạm vi:** 0.5 GB đến 237 GB
- **Lưu ý:** Cache khá đắt - chỉ nên dùng cho môi trường production

### Cấu Hình Ở Cấp Độ Stage
- Cache được định nghĩa theo từng stage
- Mỗi stage có cài đặt cache riêng
- Cài đặt cache có thể được ghi đè ở cấp độ method

### Bảo Mật
- Cache có thể được mã hóa
- Có thể yêu cầu ủy quyền IAM để vô hiệu hóa cache

## Vô Hiệu Hóa Cache (Cache Invalidation)

### Vô Hiệu Hóa Thủ Công
- Có thể vô hiệu hóa toàn bộ cache ngay lập tức từ giao diện AWS Console

### Vô Hiệu Hóa Từ Phía Client
- Client có thể vô hiệu hóa cache bằng header: `Cache-Control: max-age=0`
- **Yêu cầu:** Ủy quyền IAM phù hợp
- **Không có IAM policy:** Bất kỳ client nào cũng có thể vô hiệu hóa cache (rủi ro bảo mật!)

### Vô Hiệu Hóa Theo Key
- Các mục cache cụ thể có thể được vô hiệu hóa dựa trên keys
- Tùy chọn ủy quyền:
  - **Yêu cầu ủy quyền:** Được khuyến nghị để bảo mật
  - **Bỏ qua yêu cầu không được ủy quyền:** Bỏ qua cache control headers
  - **Thất bại với lỗi 403:** Trả về lỗi forbidden
  - **Thêm cảnh báo:** Cho phép yêu cầu nhưng thêm cảnh báo vào phản hồi

## Ví Dụ IAM Policy

Để cho phép client vô hiệu hóa cache trên một resource cụ thể:

```json
{
  "Effect": "Allow",
  "Action": "execute-api:InvalidateCache",
  "Resource": "arn:aws:execute-api:region:account-id:api-id/stage-name/*/resource-path"
}
```

## Thực Hành Tốt Nhất

1. **Sử Dụng Ở Production:** Cache khá đắt, chỉ nên bật cho môi trường production hoặc pre-production
2. **Yêu Cầu Ủy Quyền:** Luôn yêu cầu ủy quyền IAM cho việc vô hiệu hóa cache để ngăn chặn lạm dụng
3. **Đặt TTL Phù Hợp:** Cân bằng giữa độ mới của dữ liệu và hiệu suất dựa trên tần suất cập nhật dữ liệu
4. **Tùy Chỉnh Theo Method:** Ghi đè cài đặt cache cho các method cụ thể cần hành vi khác nhau
5. **Giám Sát Hiệu Suất Cache:** Theo dõi tỷ lệ cache hit để đảm bảo chiến lược caching hiệu quả

## Điểm Chính Cần Nhớ

- Caching giảm đáng kể tải cho backend
- Cấu hình linh hoạt ở cả cấp độ stage và method
- Cân nhắc bảo mật rất quan trọng cho việc vô hiệu hóa cache
- Chỉ hiệu quả về chi phí trong môi trường production có lưu lượng cao
- IAM policies phù hợp ngăn chặn thao tác cache trái phép
