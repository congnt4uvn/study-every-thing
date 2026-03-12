# Triển Khai Spring Boot Profiles trong Cards và Loans Microservices - Hướng Dẫn Giải Pháp

## Giới Thiệu

Bài giảng này cung cấp hướng dẫn đầy đủ về việc triển khai Spring Boot profiles và quản lý cấu hình trong Cards và Loans microservices, bao gồm tất cả các thay đổi code cần thiết để hoàn thành bài tập.

## Triển Khai Thay Đổi trong Loans Microservice

### Bước 1: Cập Nhật LoansController

Điều hướng đến class `LoansController` và thực hiện các thay đổi sau:

#### Dependency Injection và Autowiring

```java
@Autowired
private Environment environment;

@Autowired
private LoansContactInfoDto loansContactInfoDto;

@Value("${build.version}")
private String buildVersion;
```

#### Constructor Injection

```java
public LoansController(ILoanService loanService) {
    this.loanService = loanService;
}
```

#### Tạo Ba REST APIs

**1. Build Info API**

Trả về phiên bản build hiện tại:

```java
@GetMapping("/build-info")
@Operation(
    summary = "Get Build Info",
    description = "Get build version information"
)
@ApiResponses({
    @ApiResponse(
        responseCode = "200",
        description = "HTTP Status OK"
    )
})
public ResponseEntity<String> getBuildInfo() {
    return ResponseEntity.ok(buildVersion);
}
```

**2. Java Version API**

Đọc biến môi trường JAVA_HOME:

```java
@GetMapping("/java-version")
@Operation(
    summary = "Get Java Version",
    description = "Get Java version details"
)
@ApiResponses({
    @ApiResponse(
        responseCode = "200",
        description = "HTTP Status OK"
    )
})
public ResponseEntity<String> getJavaVersion() {
    return ResponseEntity.ok(environment.getProperty("JAVA_HOME"));
}
```

**3. Contact Info API**

Trả về tất cả các thuộc tính cấu hình:

```java
@GetMapping("/contact-info")
@Operation(
    summary = "Get Contact Info",
    description = "Get contact information"
)
@ApiResponses({
    @ApiResponse(
        responseCode = "200",
        description = "HTTP Status OK"
    )
})
public ResponseEntity<LoansContactInfoDto> getContactInfo() {
    return ResponseEntity.ok(loansContactInfoDto);
}
```

### Bước 2: Tạo LoansContactInfoDto

Tạo một record class với prefix `loans`:

```java
@ConfigurationProperties(prefix = "loans")
public record LoansContactInfoDto(
    String message,
    Map<String, String> contactDetails,
    List<String> onCallSupport
) {}
```

**Điểm Quan Trọng:**
- Sử dụng prefix `loans` để khớp với các thuộc tính trong application.yml
- Định nghĩa như một record class
- Chứa các trường: message, contactDetails, onCallSupport
- Kiểu dữ liệu khớp với các thuộc tính được định nghĩa trong application.yml

### Bước 3: Kích Hoạt Configuration Properties

Trong class `LoansApplication`:

```java
@EnableConfigurationProperties(value = {LoansContactInfoDto.class})
@SpringBootApplication
public class LoansApplication {
    public static void main(String[] args) {
        SpringApplication.run(LoansApplication.class, args);
    }
}
```

### Bước 4: Tạo Các File Cấu Hình

#### application.yml

```yaml
spring:
  profiles:
    active: qa
  config:
    import:
      - application_qa.yml
      - application_prod.yml

build:
  version: "1.0"

loans:
  message: "Chào mừng đến với Loans Microservice"
  contactDetails:
    name: "John Doe"
    email: "john.doe@example.com"
  onCallSupport:
    - "555-1234"
    - "555-5678"
```

#### application_qa.yml

```yaml
spring:
  config:
    activate:
      on-profile: qa

build:
  version: "2.0"

loans:
  message: "Chào mừng đến với Loans Microservice - Môi Trường QA"
  contactDetails:
    name: "QA Support Team"
    email: "qa@example.com"
  onCallSupport:
    - "555-QA-01"
    - "555-QA-02"
```

#### application_prod.yml

```yaml
spring:
  config:
    activate:
      on-profile: prod

build:
  version: "1.0"

loans:
  message: "Chào mừng đến với Loans Microservice - Production"
  contactDetails:
    name: "Production Support"
    email: "prod@example.com"
  onCallSupport:
    - "555-PROD-24/7"
```

### Bước 5: Kiểm Tra Loans Microservice

#### Kiểm Tra với QA Profile (Mặc Định)

1. Khởi động ứng dụng ở chế độ debug
2. Profile QA được kích hoạt mặc định trong application.yml

**Kiểm Tra Build Info API:**
```
GET http://localhost:8090/build-info
Response: "2.0"
```

**Kiểm Tra Java Version API:**
```
GET http://localhost:8090/java-version
Response: <Đường dẫn JAVA_HOME từ hệ thống local>
```

**Kiểm Tra Contact Info API:**
```
GET http://localhost:8090/contact-info
Response: Thuộc tính từ QA profile
```

#### Kiểm Tra với Production Profile

**Kích hoạt sử dụng Command Line Arguments:**

1. Dừng server
2. Click phải vào LoansApplication
3. Chọn "Modify Run Configuration"
4. Thêm program arguments: `--spring.profiles.active=prod`
5. Apply và khởi động ứng dụng

**Xác Nhận:**
- Contact Info API trả về thuộc tính production
- Build Info API trả về "1.0"

## Triển Khai Thay Đổi trong Cards Microservice

### Bước 1: Cập Nhật CardsController

Triển khai theo mẫu tương tự như Loans:

#### Autowiring và Dependency Injection

```java
@Autowired
private Environment environment;

@Autowired
private CardsContactInfoDto cardsContactInfoDto;

@Value("${build.version}")
private String buildVersion;
```

#### Tạo Ba REST APIs

1. **Build Info API** - Trả về phiên bản build
2. **Java Version API** - Trả về biến môi trường JAVA_HOME
3. **Contact Info API** - Trả về tất cả thuộc tính cấu hình từ CardsContactInfoDto

### Bước 2: Tạo CardsContactInfoDto

```java
@ConfigurationProperties(prefix = "cards")
public record CardsContactInfoDto(
    String message,
    Map<String, String> contactDetails,
    List<String> onCallSupport
) {}
```

**Quan Trọng:** Sử dụng prefix `cards` để khớp với các thuộc tính trong application.yml.

### Bước 3: Kích Hoạt Configuration Properties

Trong class `CardsApplication`:

```java
@EnableConfigurationProperties(value = {CardsContactInfoDto.class})
@SpringBootApplication
public class CardsApplication {
    public static void main(String[] args) {
        SpringApplication.run(CardsApplication.class, args);
    }
}
```

### Bước 4: Tạo Các File Cấu Hình

Tạo các file sau:
- `application.yml`
- `application_qa.yml`
- `application_prod.yml`

Sử dụng prefix `cards` cho tất cả các thuộc tính thay vì `loans`.

### Bước 5: Kiểm Tra Cards Microservice

#### Kiểm Tra với QA Profile

Khởi động ứng dụng ở chế độ debug. Mặc định, profile QA được kích hoạt.

**Kiểm Tra Build Info API:**
```
GET http://localhost:9000/build-info
Response: "2.0"
```

**Kiểm Tra Java Version API:**
```
GET http://localhost:9000/java-version
Response: <Đường dẫn JAVA_HOME>
```

**Kiểm Tra Contact Info API:**
```
GET http://localhost:9000/contact-info
Response: Thuộc tính từ QA profile
```

#### Kiểm Tra với Production Profile

1. Dừng server
2. Click phải vào CardsApplication
3. Chọn "Modify Run Configuration"
4. Thêm: `--spring.profiles.active=prod`
5. Apply và khởi động ứng dụng

**Xác Nhận:**
- Contact Info API trả về thuộc tính production
- Build Info API trả về "1.0"

## Những Điều Cần Lưu Ý Quan Trọng

### Khoảng Cách trong File YAML

**Quan Trọng:** Khoảng cách trong file YAML cực kỳ quan trọng.

❌ **Sai:**
```yaml
spring:
  config:
    profiles:  # Khoảng cách thừa - Vị trí sai!
      active: qa
```

✅ **Đúng:**
```yaml
spring:
  profiles:
    active: qa
```

**Cảnh Báo:** Ngay cả một khoảng cách thừa cũng có thể phá vỡ việc kích hoạt profile bằng cách đặt thuộc tính dưới phần tử cha sai.

### Tóm Tắt Ba Microservices

Tất cả các thay đổi đã được hoàn thành cho:
- ✅ Accounts Microservice
- ✅ Cards Microservice
- ✅ Loans Microservice

### Tài Nguyên Tham Khảo

Nếu bạn có bất kỳ câu hỏi nào, hãy tham khảo GitHub repository để xem các ví dụ triển khai đầy đủ.

## Hạn Chế của Phương Pháp Này

### Triển Khai Hiện Tại

Đây là **phương pháp cơ bản nhất** cho quản lý cấu hình trong microservices.

### Nhược Điểm

Mặc dù phương pháp này hoạt động, nó có **những nhược điểm nghiêm trọng** đối với các tổ chức xây dựng hàng trăm microservices:

1. Cấu hình phân tán trên nhiều microservices
2. Khó quản lý ở quy mô lớn
3. Không có quản lý cấu hình tập trung
4. Khó cập nhật cấu hình mà không cần triển khai lại
5. Hạn chế tính linh hoạt cho các thay đổi cấu hình động

### Tiếp Theo Là Gì

Bài giảng tiếp theo sẽ khám phá chi tiết các nhược điểm này và giới thiệu các phương pháp tốt hơn để quản lý cấu hình trong kiến trúc microservice quy mô lớn.

## Những Điểm Chính

1. Spring Boot profiles cho phép cấu hình theo môi trường
2. `@ConfigurationProperties` cung cấp ràng buộc cấu hình an toàn kiểu
3. Thuộc tính có thể được đọc bằng `@Value`, `Environment`, và DTOs
4. Kích hoạt profile có thể thực hiện qua application.yml hoặc command-line arguments
5. Khoảng cách trong YAML rất quan trọng để cấu hình đúng
6. Phương pháp cơ bản này cần cải thiện cho ứng dụng cấp doanh nghiệp

## Các Bước Tiếp Theo

Tiếp tục bài giảng tiếp theo để hiểu:
- Nhược điểm của phương pháp cấu hình hiện tại
- Các giải pháp thay thế tốt hơn cho kiến trúc microservice quy mô lớn
- Giải pháp quản lý cấu hình tập trung