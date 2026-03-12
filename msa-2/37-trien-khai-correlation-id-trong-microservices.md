# Triển Khai Correlation ID trong Microservices

## Tổng Quan

Hướng dẫn này trình bày cách triển khai xử lý correlation ID trong các microservices riêng lẻ (Accounts, Loans, Cards) để nhận và xử lý correlation ID được gửi bởi Spring Cloud Gateway server.

## Luồng Kiến Trúc

```
Gateway Server (Port 8072)
    ↓ (chuyển tiếp correlation ID)
Accounts Microservice
    ↓ (chuyển tiếp correlation ID qua Feign)
Loans & Cards Microservices
```

## Triển Khai trong Accounts Microservice

### 1. Cập Nhật CustomerController

`CustomerController` chứa API `fetchCustomerDetails` giao tiếp với nhiều microservices.

**Thêm Tham Số Request Header:**

```java
@GetMapping("/fetchCustomerDetails")
public ResponseEntity<CustomerDetailsDto> fetchCustomerDetails(
    @RequestHeader("eazybank-correlation-id") String correlationId,
    @RequestParam String mobileNumber) {
    
    // Business logic
}
```

### 2. Thêm Logger vào CustomerController

**Tạo Biến Logger:**

```java
public class CustomerController {
    
    private static final Logger logger = LoggerFactory.getLogger(CustomerController.class);
    
    // ... existing code ...
}
```

**Thêm Câu Lệnh Logger:**

```java
logger.debug("eazybank-correlation-id found: {}", correlationId);
```

### 3. Cập Nhật Service Layer

**Chỉnh Sửa Interface ICustomerService:**

```java
public interface ICustomerService {
    CustomerDetailsDto fetchCustomerDetails(String correlationId, String mobileNumber);
}
```

**Cập Nhật CustomerServiceImpl:**

```java
@Override
public CustomerDetailsDto fetchCustomerDetails(String correlationId, String mobileNumber) {
    // Truyền correlationId cho Feign clients
    LoansDto loansDto = loansFeignClient.fetchLoanDetails(correlationId, mobileNumber);
    CardsDto cardsDto = cardsFeignClient.fetchCardDetails(correlationId, mobileNumber);
    
    // ... existing code ...
}
```

### 4. Cập Nhật Feign Clients

**Interface LoansFeignClient:**

```java
@FeignClient(name = "loans")
public interface LoansFeignClient {
    
    @GetMapping("/api/fetch")
    public ResponseEntity<LoansDto> fetchLoanDetails(
        @RequestHeader("eazybank-correlation-id") String correlationId,
        @RequestParam String mobileNumber);
}
```

**Interface CardsFeignClient:**

```java
@FeignClient(name = "cards")
public interface CardsFeignClient {
    
    @GetMapping("/api/fetch")
    public ResponseEntity<CardsDto> fetchCardDetails(
        @RequestHeader("eazybank-correlation-id") String correlationId,
        @RequestParam String mobileNumber);
}
```

## Triển Khai trong Loans Microservice

### 1. Cập Nhật LoansController

**Thêm Tham Số Request Header:**

```java
@GetMapping("/fetch")
public ResponseEntity<LoansDto> fetchLoanDetails(
    @RequestHeader("eazybank-correlation-id") String correlationId,
    @RequestParam String mobileNumber) {
    
    logger.debug("eazybank-correlation-id found: {}", correlationId);
    
    // ... existing code ...
}
```

### 2. Thêm Biến Logger

```java
public class LoansController {
    
    private static final Logger logger = LoggerFactory.getLogger(LoansController.class);
    
    // ... existing code ...
}
```

## Triển Khai trong Cards Microservice

### 1. Cập Nhật CardsController

**Thêm Tham Số Request Header:**

```java
@GetMapping("/fetch")
public ResponseEntity<CardsDto> fetchCardDetails(
    @RequestHeader("eazybank-correlation-id") String correlationId,
    @RequestParam String mobileNumber) {
    
    logger.debug("eazybank-correlation-id found: {}", correlationId);
    
    // ... existing code ...
}
```

### 2. Thêm Biến Logger

```java
public class CardsController {
    
    private static final Logger logger = LoggerFactory.getLogger(CardsController.class);
    
    // ... existing code ...
}
```

## Kích Hoạt Debug Logging

Thêm cấu hình sau vào `application.yml` cho mỗi microservice:

### Accounts Microservice

```yaml
logging:
  level:
    com.eazybytes.accounts: DEBUG
```

### Loans Microservice

```yaml
logging:
  level:
    com.eazybytes.loans: DEBUG
```

### Cards Microservice

```yaml
logging:
  level:
    com.eazybytes.cards: DEBUG
```

## Kiểm Thử Triển Khai

### 1. Khởi Động Lại Tất Cả Services

Khởi động lại các services theo thứ tự:
1. **Accounts Application**
2. **Loans Application**
3. **Cards Application**
4. Xác minh tất cả services đã đăng ký với **Eureka Server**
5. **Gateway Server Application**

### 2. Tạo Dữ Liệu Test

Vì sử dụng H2 database, tạo dữ liệu test trước thông qua Gateway Server (Port 8072):

**Tạo Account:**
```http
POST http://localhost:8072/eazybank/accounts/api/create
Content-Type: application/json

{
  "mobileNumber": "1234567890",
  "name": "John Doe",
  "email": "john@example.com"
}
```

**Tạo Card:**
```http
POST http://localhost:8072/eazybank/cards/api/create
Content-Type: application/json

{
  "mobileNumber": "1234567890"
}
```

**Tạo Loan:**
```http
POST http://localhost:8072/eazybank/loans/api/create
Content-Type: application/json

{
  "mobileNumber": "1234567890"
}
```

### 3. Kiểm Tra Luồng Correlation ID

**Lấy Thông Tin Chi Tiết Customer:**
```http
GET http://localhost:8072/eazybank/accounts/api/fetchCustomerDetails?mobileNumber=1234567890
```

**Response Mong Đợi:**
- Status: 200 OK
- Body: Chứa chi tiết account, loan, và card
- **Headers: Chứa `eazybank-correlation-id`**

### 4. Xác Minh Logs

**Gateway Server Logs:**
```
eazybank-correlation-id generated in RequestTraceFilter: <UUID>
Updated the correlation id to the outbound headers
```

**Accounts Microservice Logs:**
```
eazybank-correlation-id found: <UUID>
```

**Loans Microservice Logs:**
```
eazybank-correlation-id found: <UUID>
```

**Cards Microservice Logs:**
```
eazybank-correlation-id found: <UUID>
```

## Các Tình Huống Sử Dụng Correlation ID

### Luồng Request Thành Công

1. Client gửi request đến Gateway Server
2. Gateway tạo correlation ID: `a1b2c3d4-e5f6-7890-abcd-ef1234567890`
3. Gateway chuyển tiếp đến Accounts với correlation ID trong header
4. Accounts ghi log: "correlation-id found: a1b2c3d4..."
5. Accounts chuyển tiếp đến Loans với cùng correlation ID
6. Loans ghi log: "correlation-id found: a1b2c3d4..."
7. Accounts chuyển tiếp đến Cards với cùng correlation ID
8. Cards ghi log: "correlation-id found: a1b2c3d4..."
9. Gateway trả về response với correlation ID trong header

### Gỡ Lỗi Request Thất Bại

**Tình Huống:** Client báo lỗi với correlation ID cụ thể

1. Tìm kiếm Gateway logs theo correlation ID → Request đã đến Gateway ✓
2. Tìm kiếm Accounts logs theo correlation ID → Request đã đến Accounts ✓
3. Tìm kiếm Loans logs theo correlation ID → Request KHÔNG tìm thấy ✗
4. **Kết Luận:** Vấn đề xảy ra trong giao tiếp Accounts → Loans

## Các Điểm Triển Khai Chính

### Sử Dụng @RequestHeader

```java
@RequestHeader("eazybank-correlation-id") String correlationId
```

- Trích xuất giá trị header từ HTTP request
- Tương tự `@RequestParam` nhưng dành cho headers
- Tự động ánh xạ giá trị header sang tham số method

### Truyền Headers qua Feign Client

```java
@FeignClient(name = "loans")
public interface LoansFeignClient {
    @GetMapping("/api/fetch")
    ResponseEntity<LoansDto> fetchLoanDetails(
        @RequestHeader("eazybank-correlation-id") String correlationId,
        @RequestParam String mobileNumber
    );
}
```

- Feign tự động thêm header vào request gửi đi
- Duy trì correlation ID qua các ranh giới microservice

### Thực Hành Tốt Với Logger

```java
private static final Logger logger = LoggerFactory.getLogger(ClassName.class);
```

- Sử dụng SLF4J Logger
- Đặt `static final` để tối ưu hiệu suất
- Sử dụng tên class đúng để nhận diện log

## Lợi Ích Của Triển Khai Này

1. **Truy Vết End-to-End** - Theo dõi requests qua tất cả microservices
2. **Gỡ Lỗi Dễ Dàng** - Nhanh chóng xác định nơi xảy ra lỗi
3. **Hỗ Trợ Client** - Clients có thể cung cấp correlation ID trong support tickets
4. **Tập Hợp Log** - Tìm kiếm tất cả logs sử dụng một correlation ID duy nhất
5. **Phân Tích Hiệu Suất** - Đo độ trễ qua các microservices

## Gateway Server như Edge Server

Gateway Server hoạt động như một **Edge Server** cung cấp:

- **Điểm Vào Duy Nhất** - Tất cả traffic bên ngoài đi qua port 8072
- **Cross-Cutting Concerns** - Logging, auditing, security
- **Request Routing** - Định tuyến đến microservices thích hợp
- **Custom Filters** - Tiền xử lý và hậu xử lý requests/responses
- **Security Layer** - Xác thực và phân quyền (được đề cập trong phần security)

## Tóm Tắt Các Bước Triển Khai

1. ✅ Tạo Gateway Server với Spring Cloud Gateway
2. ✅ Thêm dependencies vào project
3. ✅ Cấu hình properties trong `application.yml`
4. ✅ Cấu hình routing
5. ✅ Tạo custom filters cho correlation ID
6. ✅ Cập nhật microservices để chấp nhận correlation ID
7. ✅ Kích hoạt debug logging
8. ✅ Kiểm thử qua Gateway Server trên port 8072

## Chuẩn Bị Phỏng Vấn

Các khái niệm chính cần nhớ:
- **Edge Server Pattern** - Điểm vào duy nhất cho tất cả client requests
- **Correlation ID** - Mã định danh duy nhất để truy vết request
- **Spring Cloud Gateway** - Được xây dựng trên Spring Reactive (không phải Servlet API)
- **Custom Filters** - Triển khai cross-cutting concerns
- **Feign Client** - HTTP client khai báo cho giao tiếp giữa các services
- **Service Discovery** - Tất cả services đăng ký với Eureka

## Các Bước Tiếp Theo

Trong phần bảo mật microservices, Gateway Server sẽ được tận dụng để:
- Triển khai xác thực và phân quyền
- Đảm bảo chỉ người dùng được xác thực mới có thể truy cập microservices
- Tập trung hóa các vấn đề bảo mật tại edge

## Tài Nguyên

- Tham khảo slides để ôn tập nhanh các khái niệm
- Sử dụng trong chuẩn bị phỏng vấn
- Tham chiếu cho việc triển khai Gateway patterns trong dự án thực tế