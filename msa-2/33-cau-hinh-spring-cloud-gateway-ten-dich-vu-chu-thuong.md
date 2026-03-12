# Cấu Hình Spring Cloud Gateway Cho Tên Dịch Vụ Chữ Thường

## Tổng Quan

Theo mặc định, Spring Cloud Gateway yêu cầu tên các microservice phải được chỉ định bằng chữ in hoa khi định tuyến các yêu cầu. Tài liệu này giải thích cách cấu hình Gateway server để chấp nhận tên dịch vụ viết thường, giúp cung cấp cấu trúc API chuyên nghiệp và thân thiện với người dùng hơn.

## Thách Thức Với Hành Vi Mặc Định

Khi sử dụng Spring Cloud Gateway với service discovery, cấu hình mặc định yêu cầu tên dịch vụ phải viết hoàn toàn bằng chữ in hoa:

```
http://gateway-server/ACCOUNTS/api/...
http://gateway-server/LOANS/api/...
http://gateway-server/CARDS/api/...
```

Nếu bạn cố gắng sử dụng tên dịch vụ viết thường mà không có cấu hình phù hợp, Gateway server sẽ trả về lỗi **404 Not Found**:

```
http://gateway-server/accounts/api/...  ❌ Trả về lỗi 404
```

Hành vi này không lý tưởng vì:
- Sử dụng chữ in hoa hoàn toàn trong đường dẫn URL là không phổ biến
- Tạo trải nghiệm kém cho người tiêu dùng API
- Không tuân theo các thực hành tốt nhất của REST API

## Giải Pháp: Kích Hoạt Lowercase Service ID

Để cho phép tên dịch vụ viết thường trong định tuyến Gateway, thêm cấu hình sau vào file `application.yml` của Gateway server:

```yaml
spring:
  cloud:
    gateway:
      discovery:
        locator:
          enabled: true
          lowercase-service-id: true
```

### Giải Thích Cấu Hình

- **`spring.cloud.gateway.discovery.locator.enabled`**: Kích hoạt tự động tạo route dựa trên các dịch vụ đã đăng ký với discovery server
- **`spring.cloud.gateway.discovery.locator.lowercase-service-id`**: Cấu hình Gateway để chấp nhận tên dịch vụ ở định dạng chữ thường

## Các Bước Triển Khai

1. **Mở Cấu Hình Gateway Server**
   - Điều hướng đến dự án Spring Cloud Gateway của bạn trong IntelliJ IDEA
   - Mở file `application.yml`

2. **Thêm Thuộc Tính Cấu Hình**
   - Tìm section `spring.cloud.gateway.discovery.locator`
   - Thêm thuộc tính `lowercase-service-id: true` cùng cấp với `enabled`

3. **Build Lại Ứng Dụng**
   - Thực hiện clean build Gateway server
   - Đợi quá trình build hoàn tất thành công

4. **Khởi Động Lại Gateway Server**
   - Dừng instance Gateway server đang chạy
   - Khởi động Gateway server với cấu hình mới

## Kiểm Tra Cấu Hình

### Trước Khi Cấu Hình
```
GET http://gateway-server/ACCOUNTS/api/fetch?mobileNumber=1234567890
✅ Thành công (200 OK)

GET http://gateway-server/accounts/api/fetch?mobileNumber=1234567890
❌ Lỗi (404 Not Found)
```

### Sau Khi Cấu Hình
```
GET http://gateway-server/accounts/api/fetch?mobileNumber=1234567890
✅ Thành công (200 OK)

GET http://gateway-server/loans/api/fetch?mobileNumber=1234567890
✅ Thành công (200 OK)

GET http://gateway-server/cards/api/fetch?mobileNumber=1234567890
✅ Thành công (200 OK)
```

## Lợi Ích

1. **Thiết Kế API Chuyên Nghiệp**: URL viết thường tuân theo tiêu chuẩn ngành và quy ước REST API
2. **Trải Nghiệm Lập Trình Viên Tốt Hơn**: Người tiêu dùng API không cần phải nhớ quy ước viết hoa
3. **Tính Nhất Quán**: Phù hợp với các mẫu URL phổ biến được sử dụng trong các ứng dụng web hiện đại
4. **Tính Linh Hoạt**: Hỗ trợ cả tên dịch vụ viết hoa và viết thường (mặc dù khuyến nghị viết thường)

## Thực Hành Tốt Nhất

- Luôn sử dụng tên dịch vụ viết thường trong môi trường production
- Tài liệu hóa các mẫu URL một cách rõ ràng cho người tiêu dùng API
- Kiểm tra cả các thao tác fetch và create/update sau khi triển khai thay đổi này
- Đảm bảo tất cả các ứng dụng client được cập nhật để sử dụng tên dịch vụ viết thường

## Kết Luận

Việc kích hoạt lowercase service ID trong Spring Cloud Gateway là một thay đổi cấu hình đơn giản nhưng cải thiện đáng kể khả năng sử dụng và tính chuyên nghiệp của kiến trúc microservices của bạn. Thay đổi cấu hình một dòng này đảm bảo các API endpoint của bạn tuân theo các thực hành tốt nhất của ngành và cung cấp trải nghiệm tốt hơn cho các developer sử dụng dịch vụ của bạn.