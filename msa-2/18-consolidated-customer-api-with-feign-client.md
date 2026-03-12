# Xây Dựng API Tổng Hợp Thông Tin Khách Hàng Với Feign Client và Eureka

## Tổng Quan

Hướng dẫn toàn diện này trình bày cách xây dựng một API tổng hợp thông tin chi tiết khách hàng, tập hợp dữ liệu từ nhiều microservice sử dụng OpenFeign client và Eureka service discovery. Triển khai này thể hiện các pattern giao tiếp giữa các microservice trong kiến trúc Spring Boot microservices.

## Yêu Cầu Nghiệp Vụ

Tạo một endpoint API duy nhất trả về thông tin đầy đủ của khách hàng bao gồm:
- Thông tin cá nhân (tên, email, số điện thoại)
- Thông tin tài khoản
- Chi tiết khoản vay
- Thông tin thẻ

Dữ liệu được phân tán trên ba microservice:
- **Accounts Microservice**: Lưu trữ dữ liệu khách hàng và tài khoản
- **Loans Microservice**: Quản lý thông tin khoản vay
- **Cards Microservice**: Xử lý chi tiết thẻ

## Yêu Cầu Tiên Quyết

- Spring Cloud OpenFeign
- Spring Cloud Netflix Eureka Client
- Spring Boot Web
- Lombok
- H2 Database (cho môi trường phát triển)
- Config Server đang chạy
- Eureka Server đang chạy

## Triển Khai Từng Bước

### Bước 1: Tạo CustomerDetailsDto

Tạo một DTO toàn diện để lưu trữ dữ liệu tổng hợp từ cả ba microservice.

**File**: `src/main/java/com/easybank/accounts/dto/CustomerDetailsDto.java`

```java
package com.easybank.accounts.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

@Data
@Schema(
    name = "CustomerDetails",
    description = "Schema để lưu thông tin khách hàng, tài khoản, thẻ và khoản vay"
)
public class CustomerDetailsDto {
    
    @Schema(description = "Tên của khách hàng", example = "Nguyễn Văn A")
    private String name;
    
    @Schema(description = "Địa chỉ email của khách hàng", example = "nguyenvana@example.com")
    private String email;
    
    @Schema(description = "Số điện thoại của khách hàng", example = "0123456789")
    private String mobileNumber;
    
    @Schema(description = "Thông tin tài khoản của khách hàng")
    private AccountsDto accountsDto;
    
    @Schema(description = "Thông tin khoản vay của khách hàng")
    private LoansDto loansDto;
    
    @Schema(description = "Thông tin thẻ của khách hàng")
    private CardsDto cardsDto;
}
```

**Điểm Chính**:
- Sử dụng annotation `@Data` của Lombok cho getter/setter
- Bao gồm annotation OpenAPI schema cho tài liệu API
- Kết hợp DTO từ cả ba microservice

### Bước 2: Tạo CustomerController

Xây dựng một REST controller mới dành riêng cho các thao tác khách hàng.

**File**: `src/main/java/com/easybank/accounts/controller/CustomerController.java`

```java
package com.easybank.accounts.controller;

import com.easybank.accounts.dto.CustomerDetailsDto;
import com.easybank.accounts.service.ICustomerService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.constraints.Pattern;
import lombok.AllArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@Tag(
    name = "REST API cho Khách hàng trong EasyBank",
    description = "REST APIs trong EasyBank để lấy thông tin chi tiết khách hàng"
)
@RestController
@RequestMapping(path = "/api", produces = {MediaType.APPLICATION_JSON_VALUE})
@Validated
public class CustomerController {
    
    private final ICustomerService iCustomerService;
    
    public CustomerController(ICustomerService iCustomerService) {
        this.iCustomerService = iCustomerService;
    }
    
    @Operation(
        summary = "API REST Lấy Thông Tin Chi Tiết Khách Hàng",
        description = "REST API để lấy thông tin chi tiết khách hàng dựa trên số điện thoại"
    )
    @ApiResponses({
        @ApiResponse(
            responseCode = "200",
            description = "HTTP Status OK"
        ),
        @ApiResponse(
            responseCode = "500",
            description = "HTTP Status Internal Server Error"
        )
    })
    @GetMapping("/fetchCustomerDetails")
    public ResponseEntity<CustomerDetailsDto> fetchCustomerDetails(
            @RequestParam
            @Pattern(regexp = "(^$|[0-9]{10})", message = "Số điện thoại phải có 10 chữ số")
            String mobileNumber) {
        
        CustomerDetailsDto customerDetailsDto = 
            iCustomerService.fetchCustomerDetails(mobileNumber);
        return ResponseEntity
                .status(HttpStatus.OK)
                .body(customerDetailsDto);
    }
}
```

**Tính Năng Chính**:
- Constructor injection đơn (không cần `@Autowired`)
- Validation sử dụng `@Pattern` cho định dạng số điện thoại
- Annotation OpenAPI cho tài liệu Swagger
- RESTful endpoint tại `/api/fetchCustomerDetails`

### Bước 3: Định Nghĩa Interface ICustomerService

Tạo interface cho tầng service.

**File**: `src/main/java/com/easybank/accounts/service/ICustomerService.java`

```java
package com.easybank.accounts.service;

import com.easybank.accounts.dto.CustomerDetailsDto;

public interface ICustomerService {
    
    /**
     * Lấy thông tin chi tiết khách hàng bao gồm tài khoản, khoản vay và thẻ
     * @param mobileNumber - Số điện thoại đầu vào
     * @return CustomerDetailsDto - Thông tin khách hàng tổng hợp
     */
    CustomerDetailsDto fetchCustomerDetails(String mobileNumber);
}
```

### Bước 4: Triển Khai CustomerServiceImpl

Đây là nơi diễn ra điều kỳ diệu - điều phối các cuộc gọi đến nhiều microservice.

**File**: `src/main/java/com/easybank/accounts/service/impl/CustomerServiceImpl.java`

```java
package com.easybank.accounts.service.impl;

import com.easybank.accounts.dto.AccountsDto;
import com.easybank.accounts.dto.CardsDto;
import com.easybank.accounts.dto.CustomerDetailsDto;
import com.easybank.accounts.dto.LoansDto;
import com.easybank.accounts.entity.Accounts;
import com.easybank.accounts.entity.Customer;
import com.easybank.accounts.exception.ResourceNotFoundException;
import com.easybank.accounts.mapper.AccountsMapper;
import com.easybank.accounts.mapper.CustomerMapper;
import com.easybank.accounts.repository.AccountsRepository;
import com.easybank.accounts.repository.CustomerRepository;
import com.easybank.accounts.service.ICustomerService;
import com.easybank.accounts.service.client.CardsFeignClient;
import com.easybank.accounts.service.client.LoansFeignClient;
import lombok.AllArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class CustomerServiceImpl implements ICustomerService {
    
    private AccountsRepository accountsRepository;
    private CustomerRepository customerRepository;
    private CardsFeignClient cardsFeignClient;
    private LoansFeignClient loansFeignClient;
    
    @Override
    public CustomerDetailsDto fetchCustomerDetails(String mobileNumber) {
        // Bước 1: Lấy khách hàng từ database local
        Customer customer = customerRepository.findByMobileNumber(mobileNumber)
            .orElseThrow(() -> new ResourceNotFoundException(
                "Customer", "mobileNumber", mobileNumber));
        
        // Bước 2: Lấy tài khoản từ database local
        Accounts accounts = accountsRepository.findByCustomerId(customer.getCustomerId())
            .orElseThrow(() -> new ResourceNotFoundException(
                "Account", "customerId", customer.getCustomerId().toString()));
        
        // Bước 3: Ánh xạ customer và accounts sang DTO
        CustomerDetailsDto customerDetailsDto = CustomerMapper.mapToCustomerDetailsDto(
            customer, new CustomerDetailsDto());
        customerDetailsDto.setAccountsDto(
            AccountsMapper.mapToAccountsDto(accounts, new AccountsDto()));
        
        // Bước 4: Lấy khoản vay từ Loans microservice qua Feign Client
        ResponseEntity<LoansDto> loansDtoResponseEntity = 
            loansFeignClient.fetchLoanDetails(mobileNumber);
        customerDetailsDto.setLoansDto(loansDtoResponseEntity.getBody());
        
        // Bước 5: Lấy thẻ từ Cards microservice qua Feign Client
        ResponseEntity<CardsDto> cardsDtoResponseEntity = 
            cardsFeignClient.fetchCardDetails(mobileNumber);
        customerDetailsDto.setCardsDto(cardsDtoResponseEntity.getBody());
        
        return customerDetailsDto;
    }
}
```

**Điểm Nổi Bật Của Triển Khai**:
1. **Truy Cập Database Local**: Lấy dữ liệu khách hàng và tài khoản từ repository local
2. **Gọi Service Từ Xa**: Sử dụng Feign client để gọi Loans và Cards microservice
3. **Ánh Xạ Dữ Liệu**: Chuyển đổi entity sang DTO sử dụng các class mapper
4. **Xử Lý Exception**: Ném `ResourceNotFoundException` cho dữ liệu bị thiếu
5. **Dependency Injection**: Tất cả dependency được inject qua constructor

### Bước 5: Cập Nhật CustomerMapper

Thêm một phương thức mapper mới để hỗ trợ CustomerDetailsDto.

**File**: `src/main/java/com/easybank/accounts/mapper/CustomerMapper.java`

```java
package com.easybank.accounts.mapper;

import com.easybank.accounts.dto.CustomerDetailsDto;
import com.easybank.accounts.dto.CustomerDto;
import com.easybank.accounts.entity.Customer;

public class CustomerMapper {
    
    public static CustomerDto mapToCustomerDto(Customer customer, CustomerDto customerDto) {
        customerDto.setName(customer.getName());
        customerDto.setEmail(customer.getEmail());
        customerDto.setMobileNumber(customer.getMobileNumber());
        return customerDto;
    }
    
    public static Customer mapToCustomer(CustomerDto customerDto, Customer customer) {
        customer.setName(customerDto.getName());
        customer.setEmail(customerDto.getEmail());
        customer.setMobileNumber(customerDto.getMobileNumber());
        return customer;
    }
    
    // Phương thức mapper mới cho CustomerDetailsDto
    public static CustomerDetailsDto mapToCustomerDetailsDto(
            Customer customer, CustomerDetailsDto customerDetailsDto) {
        customerDetailsDto.setName(customer.getName());
        customerDetailsDto.setEmail(customer.getEmail());
        customerDetailsDto.setMobileNumber(customer.getMobileNumber());
        return customerDetailsDto;
    }
}
```

## Cách Hoạt Động Của Luồng Giao Tiếp

### Bên Trong Hệ Thống

Khi client gọi `GET /api/fetchCustomerDetails?mobileNumber=0123456789`:

1. **Yêu Cầu Đến** Accounts microservice `CustomerController`
2. **Controller** ủy quyền cho `CustomerServiceImpl`
3. **Tầng Service** thực thi:
   - Truy vấn database local cho dữ liệu customer
   - Truy vấn database local cho dữ liệu account
   - **Feign Client cho Loans**:
     - Liên hệ Eureka Server
     - Eureka trả về các instance Loans service khả dụng
     - Spring Cloud LoadBalancer chọn một instance
     - HTTP request được gửi đến Loans instance đã chọn
     - Response nhận được và parse thành `LoansDto`
   - **Feign Client cho Cards**:
     - Quy trình tương tự như Loans
     - Response nhận được và parse thành `CardsDto`
4. **Tổng Hợp Dữ Liệu**: Tất cả dữ liệu được merge vào `CustomerDetailsDto`
5. **Response Được Gửi** về cho client

### Quy Trình Khám Phá Dịch Vụ

```
Accounts Service
    ↓ (cần dữ liệu loans)
    → Feign Client
        ↓ (truy vấn)
        → Eureka Server
            ↓ (trả về)
            → Danh sách Loans service instance
        ↓ (chọn)
        → Spring Cloud LoadBalancer
            ↓ (instance được chọn)
            → Loans Service Instance #2
                ↓ (HTTP request)
                → Loans REST API
                    ↓ (response)
                    ← Dữ Liệu Loans
```

## Lợi Thế Chính

### 1. Không Hard-Code URL
```java
// ❌ Cách tiếp cận không tốt (hard-coded)
String url = "http://localhost:9090/api/fetch?mobileNumber=" + mobileNumber;

// ✅ Cách tiếp cận tốt (service discovery)
loansFeignClient.fetchLoanDetails(mobileNumber);
```

### 2. Cân Bằng Tải Tự Động
- Nhiều instance tự động được khám phá
- Cân bằng tải phía client với Spring Cloud LoadBalancer
- Không cần load balancer bên ngoài

### 3. REST Client Khai Báo
```java
@FeignClient(name = "loans")
public interface LoansFeignClient {
    @GetMapping("/api/fetch")
    ResponseEntity<LoansDto> fetchLoanDetails(@RequestParam String mobileNumber);
}
```

### 4. Phân Tách Trách Nhiệm
- Controller xử lý các vấn đề HTTP
- Service chứa logic nghiệp vụ
- Feign client trừu tượng hóa giao tiếp từ xa
- Mapper xử lý chuyển đổi dữ liệu

## Build và Chạy

### 1. Khởi Động Các Dịch Vụ Hạ Tầng

```bash
# Khởi động Config Server (port 8071)
cd configserver
mvn spring-boot:run

# Khởi động Eureka Server (port 8761)
cd eurekaserver
mvn spring-boot:run
```

### 2. Khởi Động Các Microservice

```bash
# Khởi động Accounts Microservice (port 8080)
cd accounts
mvn clean install
mvn spring-boot:run

# Khởi động Cards Microservice (port 9000)
cd cards
mvn spring-boot:run

# Khởi động Loans Microservice (port 8090)
cd loans
mvn spring-boot:run
```

### 3. Xác Minh Đăng Ký

Mở trình duyệt: `http://localhost:8761`

Bạn sẽ thấy cả ba microservice đã đăng ký:
- ACCOUNTS
- CARDS
- LOANS

## Kiểm Thử API

### Bước 1: Tạo Dữ Liệu Test

Vì chúng ta đang sử dụng H2 in-memory database, hãy tạo dữ liệu trong tất cả các microservice với cùng số điện thoại.

**Tạo Tài Khoản**:
```bash
POST http://localhost:8080/api/create
Content-Type: application/json

{
  "name": "Nguyễn Văn A",
  "email": "nguyenvana@example.com",
  "mobileNumber": "0123456789"
}
```

**Tạo Thẻ**:
```bash
POST http://localhost:9000/api/create
Content-Type: application/json

{
  "mobileNumber": "0123456789"
}
```

**Tạo Khoản Vay**:
```bash
POST http://localhost:8090/api/create
Content-Type: application/json

{
  "mobileNumber": "0123456789"
}
```

### Bước 2: Lấy Dữ Liệu Tổng Hợp

```bash
GET http://localhost:8080/api/fetchCustomerDetails?mobileNumber=0123456789
```

### Response Mong Đợi

```json
{
  "name": "Nguyễn Văn A",
  "email": "nguyenvana@example.com",
  "mobileNumber": "0123456789",
  "accountsDto": {
    "accountNumber": 1234567890,
    "accountType": "Savings",
    "branchAddress": "123 Đường Chính, Hà Nội"
  },
  "loansDto": {
    "mobileNumber": "0123456789",
    "loanNumber": "LN123456789",
    "loanType": "Home Loan",
    "totalLoan": 500000000,
    "amountPaid": 50000000,
    "outstandingAmount": 450000000
  },
  "cardsDto": {
    "mobileNumber": "0123456789",
    "cardNumber": "1234567890123456",
    "cardType": "Credit Card",
    "totalLimit": 100000000,
    "amountUsed": 25000000,
    "availableAmount": 75000000
  }
}
```

## Cấu Hình

### application.yml (Accounts Microservice)

```yaml
spring:
  application:
    name: accounts
  cloud:
    openfeign:
      client:
        config:
          default:
            connectTimeout: 5000
            readTimeout: 5000

eureka:
  client:
    serviceUrl:
      defaultZone: http://localhost:8761/eureka/
  instance:
    preferIpAddress: true
```

### Kích Hoạt Feign Client

**Main Application Class**:
```java
@SpringBootApplication
@EnableFeignClients
@EnableEurekaClient
public class AccountsApplication {
    public static void main(String[] args) {
        SpringApplication.run(AccountsApplication.class, args);
    }
}
```

## Best Practices (Phương Pháp Tốt Nhất)

### 1. Xử Lý Lỗi

Triển khai xử lý exception phù hợp cho các lỗi Feign client:

```java
@ControllerAdvice
public class GlobalExceptionHandler {
    
    @ExceptionHandler(FeignException.class)
    public ResponseEntity<ErrorResponse> handleFeignException(FeignException ex) {
        ErrorResponse error = new ErrorResponse(
            HttpStatus.SERVICE_UNAVAILABLE.value(),
            "Dịch vụ tạm thời không khả dụng"
        );
        return new ResponseEntity<>(error, HttpStatus.SERVICE_UNAVAILABLE);
    }
}
```

### 2. Cấu Hình Timeout

```yaml
spring:
  cloud:
    openfeign:
      client:
        config:
          loans:
            connectTimeout: 5000
            readTimeout: 5000
          cards:
            connectTimeout: 5000
            readTimeout: 5000
```

### 3. Circuit Breaker Pattern

Thêm Resilience4j để chịu lỗi:

```xml
<dependency>
    <groupId>io.github.resilience4j</groupId>
    <artifactId>resilience4j-spring-boot2</artifactId>
</dependency>
```

```java
@CircuitBreaker(name = "loansService", fallbackMethod = "getDefaultLoans")
public LoansDto getLoansData(String mobileNumber) {
    return loansFeignClient.fetchLoanDetails(mobileNumber).getBody();
}

public LoansDto getDefaultLoans(String mobileNumber, Exception ex) {
    return new LoansDto(); // Trả về dữ liệu mặc định hoặc cached
}
```

### 4. Logging

Bật logging Feign client:

```yaml
logging:
  level:
    com.easybank.accounts.service.client: DEBUG
```

```java
@Configuration
public class FeignConfig {
    @Bean
    Logger.Level feignLoggerLevel() {
        return Logger.Level.FULL;
    }
}
```

## Xử Lý Sự Cố

### Vấn Đề: Service Không Tìm Thấy

**Triệu chứng**: `FeignException: Service 'LOANS' not found`

**Giải pháp**:
1. Kiểm tra xem Loans microservice có đang chạy không
2. Xác minh Eureka dashboard hiển thị service
3. Kiểm tra `spring.application.name` khớp với tên Feign client
4. Đợi 30 giây để service đăng ký

### Vấn Đề: Connection Timeout

**Triệu chứng**: `SocketTimeoutException: Read timed out`

**Giải pháp**:
1. Tăng giá trị timeout trong cấu hình
2. Kiểm tra kết nối mạng
3. Xác minh service đích đang phản hồi
4. Kiểm tra các truy vấn database chậm

### Vấn Đề: Lỗi Load Balancer

**Triệu chứng**: `No instances available for LOANS`

**Giải pháp**:
1. Đảm bảo service được đăng ký với Eureka
2. Kiểm tra health endpoint của service
3. Xác minh `eureka.instance.preferIpAddress` được set đúng
4. Khởi động lại microservice

## Cân Nhắc Về Hiệu Suất

### 1. Gọi Song Song

Để hiệu suất tốt hơn, cân nhắc thực hiện các cuộc gọi Feign song song:

```java
CompletableFuture<LoansDto> loansFuture = 
    CompletableFuture.supplyAsync(() -> 
        loansFeignClient.fetchLoanDetails(mobileNumber).getBody());

CompletableFuture<CardsDto> cardsFuture = 
    CompletableFuture.supplyAsync(() -> 
        cardsFeignClient.fetchCardDetails(mobileNumber).getBody());

CompletableFuture.allOf(loansFuture, cardsFuture).join();

customerDetailsDto.setLoansDto(loansFuture.get());
customerDetailsDto.setCardsDto(cardsFuture.get());
```

### 2. Caching

Triển khai caching cho dữ liệu được truy cập thường xuyên:

```java
@Cacheable(value = "customerDetails", key = "#mobileNumber")
public CustomerDetailsDto fetchCustomerDetails(String mobileNumber) {
    // Triển khai
}
```

### 3. Connection Pooling

Cấu hình HTTP connection pool cho Feign:

```yaml
spring:
  cloud:
    openfeign:
      httpclient:
        enabled: true
        max-connections: 200
        max-connections-per-route: 50
```

## Giám Sát và Quan Sát

### 1. Distributed Tracing

Thêm Spring Cloud Sleuth và Zipkin:

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-sleuth</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-sleuth-zipkin</artifactId>
</dependency>
```

### 2. Metrics

Bật actuator endpoint:

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
```

### 3. Health Check

Triển khai health indicator:

```java
@Component
public class CustomHealthIndicator implements HealthIndicator {
    @Override
    public Health health() {
        // Kiểm tra tình trạng của downstream service
        return Health.up().build();
    }
}
```

## Kết Luận

Triển khai này minh họa một cách tiếp cận sẵn sàng cho production để xây dựng API tổng hợp trong kiến trúc microservices. Những điểm chính:

✅ **Service Discovery**: Định vị service động qua Eureka  
✅ **Declarative Client**: Định nghĩa interface Feign đơn giản  
✅ **Load Balancing**: Cân bằng tải phía client tự động  
✅ **Phân Tách Trách Nhiệm**: Kiến trúc sạch với controller, service và client  
✅ **Xử Lý Lỗi**: Quản lý exception mạnh mẽ  
✅ **Khả Năng Mở Rộng**: Có thể xử lý nhiều instance service  

Pattern được trình bày ở đây tạo nền tảng để xây dựng microservice có khả năng phục hồi, có thể mở rộng và giao tiếp hiệu quả mà không bị ràng buộc chặt chẽ. Khi hệ thống của bạn phát triển, bạn có thể thêm circuit breaker, caching và các pattern khác để tăng cường độ tin cậy và hiệu suất.

## Các Bước Tiếp Theo

1. Triển khai circuit breaker pattern với Resilience4j
2. Thêm API Gateway cho điểm entry thống nhất
3. Triển khai distributed tracing
4. Thêm xử lý lỗi toàn diện
5. Triển khai chiến lược caching
6. Thêm bảo mật với OAuth2/JWT
7. Containerize với Docker
8. Deploy lên Kubernetes

Chúc bạn code vui vẻ! 🚀