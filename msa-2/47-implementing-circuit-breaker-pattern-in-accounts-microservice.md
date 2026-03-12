# Triển Khai Circuit Breaker Pattern trong Accounts Microservice

## Tổng Quan

Hướng dẫn này trình bày cách triển khai circuit breaker pattern trong accounts microservice sử dụng Spring Cloud Circuit Breaker với tích hợp Resilience4j và OpenFeign.

## Vấn Đề

Accounts microservice có một REST API tên là `fetchCustomerDetails` gọi đến cả cards và loans microservices. Khi một trong các dịch vụ phụ thuộc này:
- Phản hồi rất chậm
- Hoàn toàn ngừng hoạt động
- Có vấn đề về mạng

Điều này tạo ra hiệu ứng domino ảnh hưởng đến accounts microservice và sau đó là Gateway server, có thể gây ra các lỗi liên hoàn.

## Giải Pháp: Circuit Breaker Pattern với Feign Client

Spring Cloud OpenFeign cung cấp tích hợp sẵn với circuit breaker pattern, cho phép chúng ta triển khai khả năng phục hồi với cấu hình tối thiểu.

### Bước 1: Thêm Circuit Breaker Dependency

Thêm dependency Spring Cloud Circuit Breaker Resilience4j vào file `pom.xml`:

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-circuitbreaker-resilience4j</artifactId>
</dependency>
```

**Lưu ý:** Sử dụng `spring-cloud-starter-circuitbreaker-resilience4j` (không phải phiên bản reactive) vì accounts microservice không được xây dựng trên Spring Reactor.

### Bước 2: Kích Hoạt Circuit Breaker trong Cấu Hình

Thêm thuộc tính sau vào file `application.yml`:

```yaml
spring:
  cloud:
    openfeign:
      circuitbreaker:
        enabled: true
```

Cấu hình này kích hoạt circuit breaker cho tất cả OpenFeign clients trong accounts microservice.

### Bước 3: Thêm Các Thuộc Tính Resilience4j Bổ Sung

Bao gồm các thuộc tính cấu hình Resilience4j giống như đã sử dụng trong gateway server (kích thước cửa sổ trượt, ngưỡng tỷ lệ lỗi, thời gian chờ, v.v.).

### Bước 4: Tạo Các Fallback Classes

#### LoansFallback Class

Tạo một fallback class triển khai interface `LoansFeignClient`:

```java
@Component
public class LoansFallback implements LoansFeignClient {
    
    @Override
    public ResponseEntity<LoansDto> fetchLoanDetails(String correlationId) {
        return null;
    }
}
```

#### CardsFallback Class

Tương tự, tạo fallback class cho cards microservice:

```java
@Component
public class CardsFallback implements CardsFeignClient {
    
    @Override
    public ResponseEntity<CardsDto> fetchCardDetails(String correlationId) {
        return null;
    }
}
```

**Logic Nghiệp Vụ:** Các phương thức fallback trả về `null` thay vì ném RuntimeException. Trong môi trường production, bạn có thể:
- Trả về giá trị được lưu trong cache
- Lấy dữ liệu từ cơ sở dữ liệu thay thế
- Trả về giá trị mặc định
- Triển khai bất kỳ logic nghiệp vụ tùy chỉnh nào

### Bước 5: Cấu Hình Fallback trong Feign Clients

#### LoansFeignClient Interface

```java
@FeignClient(name = "loans", fallback = LoansFallback.class)
public interface LoansFeignClient {
    // định nghĩa các phương thức
}
```

#### CardsFeignClient Interface

```java
@FeignClient(name = "cards", fallback = CardsFallback.class)
public interface CardsFeignClient {
    // định nghĩa các phương thức
}
```

### Bước 6: Thêm Kiểm Tra Null trong Service Layer

Cập nhật `CustomerServiceImpl` để xử lý các phản hồi null tiềm năng từ các phương thức fallback:

```java
// Đối với Loans
ResponseEntity<LoansDto> loansResponseEntity = loansFeignClient.fetchLoanDetails(correlationId);
if (loansResponseEntity != null) {
    customerDetailsDto.setLoansDto(loansResponseEntity.getBody());
}

// Đối với Cards
ResponseEntity<CardsDto> cardsResponseEntity = cardsFeignClient.fetchCardDetails(correlationId);
if (cardsResponseEntity != null) {
    customerDetailsDto.setCardsDto(cardsResponseEntity.getBody());
}
```

## Lợi Ích

1. **Giảm Tải Nhẹ Nhàng:** Khi một microservice ngừng hoạt động, ứng dụng tiếp tục cung cấp dữ liệu một phần thay vì lỗi hoàn toàn
2. **Cải Thiện Trải Nghiệm Người Dùng:** Clients nhận được dữ liệu accounts và các microservice khả dụng ngay cả khi một dịch vụ bị lỗi
3. **Ngăn Chặn Lỗi Liên Hoàn:** Circuit breaker ngăn chặn hiệu ứng domino từ các lỗi dịch vụ phụ thuộc
4. **Cấu Hình Tối Thiểu:** Tận dụng tích hợp sẵn giữa Feign và Circuit Breaker

## Những Điểm Chính

- Spring Cloud OpenFeign tự động bao bọc tất cả các phương thức với circuit breaker khi được cấu hình đúng cách
- Fallback classes phải triển khai cùng interface với Feign client
- Luôn thêm kiểm tra null khi làm việc với cơ chế fallback
- Circuit breaker pattern là thiết yếu để xây dựng microservices có khả năng phục hồi
- Logic fallback cung cấp sự linh hoạt để triển khai các yêu cầu nghiệp vụ tùy chỉnh

## Tài Liệu Tham Khảo

- Tài liệu Spring Cloud OpenFeign
- Hỗ trợ Spring Cloud Circuit Breaker
- Hướng dẫn tích hợp Resilience4j