# AWS API Gateway - Tích hợp OpenAPI

## Tổng quan
Tài liệu này hướng dẫn cách làm việc với định nghĩa OpenAPI trong AWS API Gateway, bao gồm import và export cấu hình API.

## Import một định nghĩa OpenAPI

### Các bước để Import:
1. **Tạo một API mới**
   - Chọn loại REST API
   - Click vào tùy chọn "Import"

2. **Cung cấp file định nghĩa API**
   - Bạn cần một file định nghĩa API theo định dạng OpenAPI
   - Ví dụ: Click vào "Example API" để xem một mẫu định nghĩa OpenAPI
   - File này định nghĩa cách một API nên được xây dựng trên API Gateway

3. **Import và Tạo**
   - Import file example API
   - Click "Create API"
   - Kết quả: Một API mới (ví dụ: "Pet Store") được tạo với các resources phù hợp

### Lợi ích:
- Tất cả resources được tự động tạo từ file định nghĩa OpenAPI
- Rất tiện lợi cho việc thiết lập API nhanh chống
- Đảm bảo tính nhất quán trong việc triển khai API

## Export một API dưới dạng OpenAPI

### Các bước để Export:
1. **Điều hướng đến API**
   - Vào API của bạn trong API Gateway
   - Chọn một stage (ví dụ: stage "prod")

2. **Tùy chọn Export**
   - Click vào "Stage Actions"
   - Chọn "Export"
   
3. **Cấu hình thiết lập Export**
   - **Format**: Chọn giữa Swagger hoặc OpenAPI 3
   - **Loại File**: JSON hoặc YAML
   - **Extensions**: Bao gồm extensions của API Gateway và Postman (tùy chọn)

4. **Tạo File**
   - Export sẽ tạo ra file
   - File này có thể được import ở nơi khác nếu cần

## Tạo SDK tự động

### Tạo SDK tự động:
Khi bạn sử dụng định dạng OpenAPI, bạn có thể tự động tạo SDK cho nhiều ngôn ngữ lập trình:

- **Android**
- **JavaScript**
- **iOS**
- **Java**
- **Ruby**

### Lợi ích:
- Ứng dụng có thể dễ dàng tương tác với API thông qua SDK được tạo
- Giảm thời gian phát triển
- Đảm bảo type safety và sử dụng API đúng cách

## Những điểm quan trọng

Sức mạnh của định nghĩa OpenAPI trong API Gateway bao gồm:
- Dễ dàng import/export cấu hình API
- Tự động tạo SDK cho nhiều nền tảng
- Tài liệu API được chuẩn hóa
- Quản lý và triển khai API đơn giản hóa

---

**Dịch vụ AWS**: API Gateway  
**Chủ đề**: Tích hợp OpenAPI  
**Ngày**: 2026
