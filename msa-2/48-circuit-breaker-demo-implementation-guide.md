# Hướng Dẫn Triển Khai Circuit Breaker Pattern với Spring Boot

## Tổng Quan

Hướng dẫn này trình bày cách triển khai và kiểm tra Circuit Breaker pattern trong kiến trúc microservices sử dụng Spring Boot, Resilience4j, và OpenFeign. Circuit Breaker pattern giúp xây dựng các microservices có khả năng phục hồi bằng cách ngăn chặn lỗi lan truyền và cung cấp cơ chế giảm tải nhẹ nhàng.

## Thiết Lập Kiến Trúc

Môi trường demo bao gồm các microservices sau:

1. **Config Server** - Quản lý cấu hình tập trung
2. **Eureka Server** - Khám phá và đăng ký dịch vụ
3. **Gateway Server** - API Gateway để định tuyến yêu cầu
4. **Accounts Microservice** (Port 8080) - Dịch vụ chính có triển khai circuit breaker
5. **Cards Microservice** - Dịch vụ phụ thuộc cho thông tin thẻ
6. **Loans Microservice** - Dịch vụ phụ thuộc cho thông tin khoản vay

Tất cả microservices được đăng ký với Eureka server và có thể xác minh qua Eureka dashboard.

## Giám Sát Trạng Thái Circuit Breaker

### Các Endpoint Actuator

Spring Boot Actuator cung cấp giám sát thời gian thực của circuit breakers:

- **Trạng thái Circuit Breakers**: `/actuator/circuitbreakers`
- **Sự kiện Circuit Breaker**: `/actuator/circuitbreakerevents`

### Trạng Thái Ban Đầu

Trước khi gửi request đầu tiên, không có circuit breakers nào hiển thị trong các endpoint actuator. Circuit breakers chỉ được tạo và kích hoạt khi request đầu tiên đi qua hệ thống.

### Quy Ước Đặt Tên Circuit Breaker

Circuit breakers tuân theo mẫu đặt tên này:
```
<TênInterface>.<TênMethod>(<KiểuThamSố1>, <KiểuThamSố2>, ...)
```

**Ví dụ:**
- `cardFeignClient.fetchCardDetails(String, String)`
- `loansFeignClient.fetchLoanDetails(String, String)`

## Hướng Dẫn Demo

### Kịch Bản Thành Công

1. **Tạo Dữ Liệu Test**
   - Tạo dữ liệu accounts qua POST request
   - Tạo dữ liệu cards với cùng số điện thoại
   - Tạo dữ liệu loans với cùng số điện thoại

2. **Lấy Thông Tin Chi Tiết Khách Hàng**
   - Request: `GET /fetchCustomerDetails`
   - Response: Trả về dữ liệu khách hàng đầy đủ bao gồm accounts, cards và loans
   - Trạng thái Circuit Breaker: `CLOSED` cho cả cardFeignClient và loansFeignClient

3. **Xác Minh Qua Actuator**
   - Hai circuit breakers được tạo tự động
   - Cả hai hiển thị trạng thái: `CLOSED`
   - Events hiển thị: Request đơn lẻ với loại `SUCCESS`

### Kịch Bản Lỗi - Loans Microservice Ngừng Hoạt Động

1. **Dừng Loans Microservice**
   - Mô phỏng lỗi dịch vụ bằng cách dừng ứng dụng loans

2. **Hành Vi Request**
   - Request: `GET /fetchCustomerDetails`
   - Response: 
     - ✅ Dữ liệu Accounts: Thành công
     - ✅ Dữ liệu Cards: Thành công
     - ❌ Dữ liệu Loans: `null` (fallback được kích hoạt)

3. **Chuyển Đổi Trạng Thái Circuit Breaker**
   - Sau nhiều request thất bại, loans circuit breaker chuyển từ `CLOSED` sang `OPEN`
   - Actuator events hiển thị: `FAILURE_RATE_EXCEEDED`
   - Chuyển đổi trạng thái: `CLOSED → OPEN`

### Kịch Bản Lỗi - Nhiều Dịch Vụ Ngừng Hoạt Động

1. **Dừng Cả Cards và Loans Microservices**
   - Mô phỏng nhiều dịch vụ phụ thuộc bị lỗi

2. **Hành Vi Request**
   - Request: `GET /fetchCustomerDetails`
   - Response:
     - ✅ Dữ liệu Accounts: Thành công
     - ❌ Dữ liệu Cards: `null` (fallback được kích hoạt)
     - ❌ Dữ liệu Loans: `null` (fallback được kích hoạt)

3. **Trạng Thái Circuit Breakers**
   - Cả hai circuit breakers chuyển sang trạng thái `OPEN`
   - Events hiển thị: Trạng thái `NOT_PERMITTED` cho cả hai dịch vụ
   - Gateway và Accounts microservice tiếp tục hoạt động mà không bị ảnh hưởng lan truyền

## Ví Dụ Thực Tế: Trang Web Amazon

Xem xét kịch bản trang chủ Amazon:

- **Nhiều microservices** làm việc cùng nhau để hiển thị thông tin:
  - Danh sách sản phẩm
  - Giảm giá và banner
  - Gợi ý dựa trên lịch sử đơn hàng

- **Giảm Tải Nhẹ Nhàng**: Nếu microservice gợi ý bị lỗi:
  - ✅ Trang chủ vẫn hoạt động bình thường
  - ✅ Sản phẩm, banner và giảm giá vẫn hiển thị
  - ❌ Chỉ phần gợi ý bị ẩn
  - ✅ Người dùng có thể tiếp tục duyệt web một cách liền mạch

Cách tiếp cận này đảm bảo **trải nghiệm khả thi tối thiểu** thay vì lỗi hoàn toàn.

## Các Bước Triển Khai

### Bước 1: Thêm Dependency

Thêm dependency Resilience4j vào `pom.xml`:

```xml
<dependency>
    <groupId>io.github.resilience4j</groupId>
    <artifactId>resilience4j-spring-boot2</artifactId>
</dependency>
```

### Bước 2: Cấu Hình Feign Client Interface

Thêm cấu hình fallback vào các Feign client interfaces:

```java
@FeignClient(name = "cards-service", fallback = CardsFallback.class)
public interface CardFeignClient {
    @GetMapping("/api/cards")
    CardsDto fetchCardDetails(@RequestParam String mobileNumber);
}
```

### Bước 3: Triển Khai Fallback Bean

Tạo fallback implementation cho mỗi Feign client:

```java
@Component
public class CardsFallback implements CardFeignClient {
    @Override
    public CardsDto fetchCardDetails(String mobileNumber) {
        // Trả về null hoặc response mặc định
        return null;
    }
}
```

### Bước 4: Cấu Hình Properties

Định nghĩa các thuộc tính circuit breaker trong `application.yml`:

```yaml
resilience4j:
  circuitbreaker:
    instances:
      cardsService:
        registerHealthIndicator: true
        slidingWindowSize: 10
        minimumNumberOfCalls: 5
        permittedNumberOfCallsInHalfOpenState: 3
        waitDurationInOpenState: 10s
        failureRateThreshold: 50
```

## Các Trạng Thái Circuit Breaker

1. **CLOSED**: Hoạt động bình thường, requests được xử lý
2. **OPEN**: Dịch vụ đang lỗi, requests bị chặn và fallback được gọi
3. **HALF_OPEN**: Kiểm tra xem dịch vụ đã phục hồi chưa

## Quy Trình Phục Hồi

Khi các microservices phụ thuộc (cards và loans) được khởi động lại và bắt đầu phản hồi thành công:
- Circuit breakers tự động phát hiện các phản hồi thành công
- Trạng thái chuyển từ `OPEN` về `CLOSED`
- Hoạt động bình thường được tiếp tục

## Lợi Ích Chính

✅ **Ngăn Chặn Lỗi Lan Truyền**: Cô lập các dịch vụ bị lỗi
✅ **Giảm Tải Nhẹ Nhàng**: Cung cấp chức năng một phần thay vì lỗi hoàn toàn
✅ **Cải Thiện Trải Nghiệm Người Dùng**: Người dùng nhận được một số dữ liệu thay vì lỗi
✅ **Khả Năng Phục Hồi Hệ Thống**: Gateway và các dịch vụ khác không bị ảnh hưởng
✅ **Tự Động Phục Hồi**: Circuit breakers tự chữa lành khi dịch vụ phục hồi

## Kết Luận

Circuit Breaker pattern là yếu tố thiết yếu để xây dựng kiến trúc microservices có khả năng phục hồi. Bằng cách triển khai nó với Resilience4j và OpenFeign, bạn có thể đảm bảo hệ thống của mình xử lý lỗi một cách nhẹ nhàng và cung cấp trải nghiệm tốt nhất có thể cho người dùng cuối.

## Bước Tiếp Theo

Khám phá các resilience patterns khác được cung cấp bởi Resilience4j:
- Retry Pattern (Mẫu Thử Lại)
- Rate Limiter (Giới Hạn Tốc Độ)
- Bulkhead Pattern (Mẫu Ngăn Khoang)
- Time Limiter (Giới Hạn Thời Gian)

---

*Hướng dẫn này dựa trên demo thực tế về triển khai Circuit Breaker pattern trong Spring Boot microservices.*