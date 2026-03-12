# Cấu Hình Timeout trong Spring Cloud Gateway

## Tổng Quan

Hướng dẫn này trình bày cách cấu hình timeout trong Spring Cloud Gateway để ngăn chặn các microservice chờ đợi phản hồi vô thời hạn, điều này có thể dẫn đến cạn kiệt tài nguyên và các vấn đề về hiệu suất.

## Vấn Đề

Khi các microservice phản hồi chậm hoặc bị treo, các ứng dụng client và gateway server có thể lãng phí tài nguyên quý giá (thread, bộ nhớ) để chờ đợi các phản hồi có thể không bao giờ đến. Nếu không có cấu hình timeout phù hợp:

- Các thread bị chặn vô thời hạn
- Tài nguyên server bị tiêu thụ không cần thiết
- Ứng dụng client có trải nghiệm người dùng kém
- Hiệu suất hệ thống giảm sút theo thời gian

### Kịch Bản Minh Họa

Khi gọi endpoint `contact-info` trong `LoansController`:
- Không có timeout: Ứng dụng chờ đợi vô thời hạn (có thể hàng phút)
- Với circuit breaker (AccountsController): Tự động timeout sau 1 giây và chuyển sang fallback
- Hành vi khác nhau tùy thuộc vào việc có triển khai Circuit Breaker pattern hay không

## Giải Pháp: Cấu Hình HTTP Timeout

Spring Cloud Gateway cung cấp hai loại cấu hình timeout:

### 1. Connection Timeout
Thời gian tối đa mà gateway server chờ để thiết lập kết nối với microservice đích.

**Trường hợp sử dụng**: Xử lý vấn đề mạng hoặc khi microservice không thể truy cập được.

### 2. Response Timeout
Thời gian tối đa mà gateway server chờ để nhận phản hồi hoàn chỉnh từ microservice.

**Trường hợp sử dụng**: Xử lý các service phản hồi chậm hoặc bị treo trong quá trình xử lý.

## Triển Khai

### Cấu Hình Timeout Toàn Cục

Thêm các thuộc tính sau vào file `application.yml` của Gateway server:

```yaml
spring:
  cloud:
    gateway:
      httpclient:
        connect-timeout: 1000        # 1 giây (đơn vị milliseconds)
        response-timeout: 2s         # 2 giây
```

**Chi Tiết Cấu Hình:**
- `connect-timeout`: 1000ms (1 giây) - Thời gian để thiết lập kết nối
- `response-timeout`: 2s - Thời gian chờ tối đa cho phản hồi

Các cài đặt toàn cục này áp dụng cho tất cả các microservice được định tuyến qua Gateway server.

### Cấu Hình Timeout Theo Từng Route

Để cấu hình timeout riêng cho từng route:

#### Sử Dụng Java DSL

```java
.route(r -> r.path("/api/loans/**")
    .metadata("response-timeout", 5000)
    .metadata("connect-timeout", 2000)
    .uri("lb://LOANS"))
```

#### Sử Dụng application.yml

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: loans-service
          uri: lb://LOANS
          metadata:
            response-timeout: 5000
            connect-timeout: 2000
```

### Vô Hiệu Hóa Timeout Cho Route Cụ Thể

Để vô hiệu hóa cấu hình timeout toàn cục cho một route cụ thể, đặt response timeout thành giá trị âm:

```yaml
metadata:
  response-timeout: -1  # Vô hiệu hóa timeout - chờ đợi vô thời hạn
```

**Cảnh báo**: Sử dụng cẩn thận vì có thể dẫn đến cạn kiệt tài nguyên.

## Hành Vi Với Circuit Breaker

Khi Circuit Breaker pattern được cấu hình (ví dụ: cho Accounts microservice):
- Timeout nội bộ của Circuit Breaker (mặc định: 1 giây) được ưu tiên
- Cấu hình timeout toàn cục của gateway bị bỏ qua
- Cơ chế fallback được kích hoạt khi xảy ra timeout
- Cấu hình timeout của Circuit Breaker có thể được ghi đè riêng biệt

## Kiểm Tra Cấu Hình

### Trước Khi Cấu Hình Timeout
1. Đặt breakpoint trong endpoint của microservice
2. Gửi request qua Postman
3. Kết quả: Client chờ đợi vô thời hạn (ví dụ: hơn 2 phút)

### Sau Khi Cấu Hình Timeout
1. Đặt breakpoint trong endpoint của microservice
2. Gửi request qua Postman
3. Kết quả: Lỗi "Gateway Timeout" sau 2 giây

## Thực Hành Tốt Nhất

1. **Luôn Cấu Hình Timeout**: Không bao giờ để microservice không có cấu hình timeout
2. **Điều Chỉnh Theo Yêu Cầu Nghiệp Vụ**: Đặt giá trị timeout phù hợp với trường hợp sử dụng của bạn
3. **Xem Xét Đặc Điểm Service**: Các service khác nhau có thể yêu cầu giá trị timeout khác nhau
4. **Giám Sát và Tinh Chỉnh**: Thường xuyên xem xét và điều chỉnh giá trị timeout dựa trên các chỉ số hiệu suất
5. **Sử Dụng Circuit Breaker**: Kết hợp timeout với Circuit Breaker pattern để có khả năng phục hồi tốt hơn

## Điểm Chính Cần Nhớ

- Cấu hình timeout ngăn ngừa cạn kiệt tài nguyên trong kiến trúc microservices
- Spring Cloud Gateway hỗ trợ cả cấu hình timeout toàn cục và theo từng route
- Connection timeout xử lý vấn đề thiết lập kết nối
- Response timeout xử lý phản hồi chậm hoặc bị treo
- Cấu hình timeout của Circuit Breaker ghi đè timeout toàn cục của gateway
- Cấu hình timeout phù hợp là thiết yếu cho microservices sẵn sàng triển khai production

## Các Pattern Liên Quan

- Circuit Breaker Pattern
- Fallback Mechanism
- Service Discovery
- API Gateway Design Patterns

## Tài Liệu Tham Khảo Thêm

Tham khảo tài liệu chính thức của Spring Cloud Gateway để biết:
- Các tùy chọn cấu hình timeout bổ sung
- Cấu hình định tuyến nâng cao
- Triển khai custom filter
- Tích hợp circuit breaker

---

*Hướng dẫn này minh họa tầm quan trọng của cấu hình timeout trong việc xây dựng microservices có khả năng phục hồi và hiệu suất cao với Spring Cloud Gateway.*