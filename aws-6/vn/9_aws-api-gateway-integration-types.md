# Các Kiểu Tích Hợp AWS API Gateway

## Tổng Quan
Tài liệu này trình bày các cách khác nhau để tích hợp API Gateway với các dịch vụ backend. Hiểu rõ các kiểu tích hợp này là rất quan trọng để thiết kế và triển khai các giải pháp API trên AWS.

## 1. Tích Hợp MOCK

**Mục đích:** Trả về phản hồi mà không cần gửi yêu cầu đến backend.

**Trường Hợp Sử Dụng:**
- Phát triển và kiểm thử
- Cấu hình API Gateway mà không cần thiết lập backend
- Không phù hợp cho môi trường production

**Tính Năng Chính:**
- Không cần backend
- Hữu ích cho việc tạo prototype và phát triển
- Trả về các phản hồi được định nghĩa trước

---

## 2. Tích Hợp HTTP/AWS Lambda (Không Proxy)

**Mục đích:** Chuyển tiếp yêu cầu đến Lambda hoặc các dịch vụ AWS khác với khả năng sửa đổi yêu cầu và phản hồi.

**Yêu Cầu Cấu Hình:**
- Thiết lập integration request (yêu cầu tích hợp)
- Thiết lập integration response (phản hồi tích hợp)
- Ánh xạ dữ liệu sử dụng mapping templates

**Khả Năng:**
- Sửa đổi yêu cầu trước khi gửi đến backend
- Chuyển đổi phản hồi trước khi trả về client
- Sử dụng mapping templates để chuyển đổi dữ liệu

**Ví Dụ Trường Hợp Sử Dụng:**
Tạo REST API ánh xạ đến SQS Queue bằng cách:
- Thay đổi định dạng yêu cầu
- Đổi tên các tham số
- Sắp xếp lại cấu trúc dữ liệu
- Đảm bảo SQS có thể hiểu lời gọi API

**Điểm Quan Trọng:** API Gateway có toàn quyền kiểm soát để sửa đổi cả yêu cầu và phản hồi.

---

## 3. AWS Proxy (Lambda Proxy)

**Mục đích:** Tích hợp trực tiếp nơi các yêu cầu được chuyển đến Lambda mà không có sửa đổi.

**Đặc Điểm:**
- Yêu cầu từ client trở thành đầu vào trực tiếp cho Lambda
- Không thể sửa đổi yêu cầu/phản hồi
- Không cho phép mapping templates
- Không thể sửa đổi headers hoặc query string parameters
- Function xử lý toàn bộ logic cho yêu cầu và phản hồi

**Cấu Trúc Yêu Cầu:**
Lambda nhận một tài liệu JSON chứa:
- Thông tin resource
- Path (đường dẫn)
- HTTP method
- Headers
- Query string parameters (tham số chuỗi truy vấn)
- Stage variables (biến giai đoạn)
- Body (nội dung)
- Metadata khác

**Cấu Trúc Phản Hồi:**
Lambda phải trả về:
```json
{
  "statusCode": 200,
  "headers": {...},
  "body": "..."
}
```

**Điểm Quan Trọng:** Toàn bộ công việc nằm ở backend; API Gateway chỉ chuyển tiếp các yêu cầu.

---

## 4. HTTP Proxy

**Mục đích:** Chuyển tiếp yêu cầu trực tiếp đến các HTTP endpoints mà không có sửa đổi.

**Đặc Điểm:**
- Không có mapping templates
- Yêu cầu được chuyển trực tiếp đến backend
- Phản hồi được chuyển trực tiếp trả lại client
- Có thể thêm HTTP headers (ví dụ: API keys)

**Ví Dụ Kịch Bản:**
1. Client tạo HTTP request đến API Gateway
2. API Gateway chuyển tiếp request đến backend (ví dụ: Application Load Balancer)
3. Tùy chọn: Thêm HTTP headers như API key
4. Backend nhận yêu cầu với headers được thêm vào
5. Phản hồi được chuyển tiếp trở lại client

**Lợi Ích Bảo Mật:** Có thể thêm authentication headers mà client không cần biết.

---

## Mapping Templates (Mẫu Ánh Xạ)

**Khả Dụng:** Chỉ cho tích hợp HTTP/AWS Lambda (phương thức không proxy)

**Chức Năng:**
- Đổi tên hoặc sửa đổi query string parameters
- Sửa đổi nội dung body
- Thêm hoặc sửa đổi headers
- Chuyển đổi dữ liệu yêu cầu và phản hồi

**Công Nghệ:** Sử dụng Velocity Template Language (VTL)

---

## Bảng So Sánh Tổng Hợp

| Kiểu Tích Hợp | Sửa Đổi Yêu Cầu | Sửa Đổi Phản Hồi | Mapping Templates | Trường Hợp Sử Dụng |
|---------------|-----------------|------------------|-------------------|-------------------|
| MOCK | N/A | ✓ | ✓ | Phát triển/Kiểm thử |
| HTTP/AWS Lambda | ✓ | ✓ | ✓ | Kiểm soát toàn diện việc chuyển đổi |
| AWS Proxy | ✗ | ✗ | ✗ | Chuyển tiếp đơn giản đến Lambda |
| HTTP Proxy | ✗ | ✗ | ✗ | Tích hợp HTTP backend trực tiếp |

---

## Mẹo Học Tập

1. **MOCK** chỉ dành cho kiểm thử
2. **Tích hợp Proxy** (AWS Proxy & HTTP Proxy) không cho phép chuyển đổi
3. **Tích hợp không proxy** (HTTP/AWS Lambda) cho phép kiểm soát toàn diện thông qua mapping templates
4. **VTL** là ngôn ngữ được sử dụng cho mapping templates
5. Chọn kiểu tích hợp dựa trên việc bạn có cần chuyển đổi yêu cầu/phản hồi hay không

---

## Điểm Chính Cần Nhớ

- Phương thức proxy cung cấp sự đơn giản và chuyển tiếp trực tiếp
- Phương thức không proxy cung cấp tính linh hoạt với các chuyển đổi
- Mapping templates cho phép chuyển đổi dữ liệu mạnh mẽ
- Các tính năng bảo mật như API keys có thể được thêm một cách minh bạch
- Lambda Proxy đặt toàn bộ logic trong hàm Lambda
