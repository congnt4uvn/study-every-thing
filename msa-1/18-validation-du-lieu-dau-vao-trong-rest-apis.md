# Validation Dữ Liệu Đầu Vào Trong REST APIs

## Tổng Quan

Khi xây dựng microservices và REST APIs, việc thực hiện validation trên dữ liệu đầu vào nhận từ các ứng dụng client là rất quan trọng. Bài học này đề cập đến việc triển khai input validation trong ứng dụng Spring Boot microservices để đảm bảo tính toàn vẹn dữ liệu và ngăn chặn các truy vấn cơ sở dữ liệu không cần thiết với dữ liệu không hợp lệ.

## Tại Sao Input Validation Quan Trọng

### Các Trường Hợp Validation Phổ Biến

- **Số Điện Thoại**: Người dùng có thể gửi 5 hoặc 9 chữ số thay vì 10 chữ số yêu cầu
- **Định Dạng Email**: Người dùng có thể không tuân theo định dạng email đúng (thiếu ký tự @, tên miền, v.v.)
- **Độ Dài Tên**: Người dùng có thể gửi tên quá ngắn (2-3 ký tự)
- **Trường Rỗng**: Người dùng có thể gửi giá trị rỗng hoặc null cho các trường bắt buộc

### Lợi Ích Của Input Validation

1. **Ngăn Chặn Truy Vấn Database Không Hợp Lệ**: Từ chối dữ liệu không hợp lệ trước khi nó đến tầng database
2. **Cải Thiện Hiệu Suất**: Tránh các thao tác database không cần thiết
3. **Trải Nghiệm Người Dùng Tốt Hơn**: Cung cấp thông báo lỗi rõ ràng cho clients
4. **Tính Toàn Vẹn Dữ Liệu**: Đảm bảo dữ liệu đáp ứng yêu cầu nghiệp vụ

## Các Bước Triển Khai

### Bước 1: Thêm Dependency Validation

Đảm bảo dependency sau có trong `pom.xml`:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-validation</artifactId>
</dependency>
```

Dependency này cung cấp tất cả các annotation và thư viện validation cần thiết.

### Bước 2: Thêm Validation Annotations Vào DTOs

#### Validations Cho CustomerDto

```java
public class CustomerDto {
    
    @NotEmpty(message = "Name cannot be null or empty")
    @Size(min = 5, max = 30, message = "The length of the customer name should be between 5 and 30")
    private String name;
    
    @NotEmpty(message = "Email address cannot be null or empty")
    @Email(message = "Email address should be a valid value")
    private String email;
    
    @Pattern(regexp = "(^$|[0-9]{10})", message = "Mobile number must be 10 digits")
    private String mobileNumber;
}
```

#### Validations Cho AccountsDto

```java
public class AccountsDto {
    
    @NotEmpty(message = "Account number cannot be null or empty")
    @Pattern(regexp = "(^$|[0-9]{10})", message = "Account number must be 10 digits")
    private Long accountNumber;
    
    @NotEmpty(message = "Account type cannot be null or empty")
    private String accountType;
    
    @NotEmpty(message = "Branch address cannot be null or empty")
    private String branchAddress;
}
```

### Bước 3: Các Annotation Validation Phổ Biến

Package `jakarta.validation.constraints` cung cấp nhiều annotation validation khác nhau:

- **@NotEmpty**: Trường không được null hoặc rỗng
- **@NotNull**: Trường không được null
- **@NotBlank**: Trường không được để trống (khoảng trắng)
- **@Size**: Chỉ định độ dài min và max
- **@Email**: Validate định dạng email
- **@Pattern**: Validate theo mẫu regex
- **@Digits**: Chỉ chấp nhận giá trị số
- **@Min / @Max**: Validate phạm vi số
- **@Future / @Past**: Validate ngày tháng
- **@Positive / @Negative**: Validate dấu của số

### Bước 4: Kích Hoạt Validation Trong Controller

Thêm các annotation validation vào controller:

```java
@RestController
@RequestMapping("/api")
@Validated
@AllArgsConstructor
public class AccountsController {
    
    @PostMapping("/create")
    public ResponseEntity<ResponseDto> createAccount(
        @Valid @RequestBody CustomerDto customerDto) {
        // Implementation
    }
    
    @PutMapping("/update")
    public ResponseEntity<ResponseDto> updateAccountDetails(
        @Valid @RequestBody CustomerDto customerDto) {
        // Implementation
    }
    
    @GetMapping("/fetch")
    public ResponseEntity<CustomerDto> fetchAccountDetails(
        @RequestParam 
        @Pattern(regexp = "(^$|[0-9]{10})", message = "Mobile number must be 10 digits")
        String mobileNumber) {
        // Implementation
    }
    
    @DeleteMapping("/delete")
    public ResponseEntity<ResponseDto> deleteAccountDetails(
        @RequestParam 
        @Pattern(regexp = "(^$|[0-9]{10})", message = "Mobile number must be 10 digits")
        String mobileNumber) {
        // Implementation
    }
}
```

**Các Annotation Chính:**
- **@Validated**: Kích hoạt validation trên controller class
- **@Valid**: Kích hoạt validation trên request body
- **@Pattern**: Validate request parameters theo regex

### Bước 5: Xử Lý Validation Exceptions

Tạo global exception handler để xử lý các lỗi validation:

```java
@ControllerAdvice
public class GlobalExceptionHandler extends ResponseEntityExceptionHandler {
    
    @Override
    protected ResponseEntity<Object> handleMethodArgumentNotValid(
            MethodArgumentNotValidException exception,
            HttpHeaders headers,
            HttpStatusCode status,
            WebRequest request) {
        
        Map<String, String> validationErrors = new HashMap<>();
        
        List<ObjectError> validationErrorList = exception.getBindingResult().getAllErrors();
        
        validationErrorList.forEach((error) -> {
            String fieldName = ((FieldError) error).getField();
            String validationMsg = error.getDefaultMessage();
            validationErrors.put(fieldName, validationMsg);
        });
        
        return new ResponseEntity<>(validationErrors, HttpStatus.BAD_REQUEST);
    }
}
```

**Chi Tiết Triển Khai:**
1. Kế thừa class `ResponseEntityExceptionHandler`
2. Override phương thức `handleMethodArgumentNotValid()`
3. Trích xuất tất cả lỗi validation từ exception
4. Tạo map các tên trường và thông báo lỗi
5. Trả về các lỗi dưới dạng response với status `BAD_REQUEST`

## Kiểm Thử Validation

### Ví Dụ 1: Request Create Không Hợp Lệ

**Request:**
```json
{
    "name": "A",
    "email": "invalid-email",
    "mobileNumber": "123456789"
}
```

**Response (400 Bad Request):**
```json
{
    "name": "The length of the customer name should be between 5 and 30",
    "email": "Email address should be a valid value",
    "mobileNumber": "Mobile number must be 10 digits"
}
```

### Ví Dụ 2: Request Create Hợp Lệ

**Request:**
```json
{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "mobileNumber": "1234567890"
}
```

**Response (200 OK):**
```json
{
    "statusCode": "201",
    "statusMsg": "Account created successfully"
}
```

### Ví Dụ 3: Query Parameter Không Hợp Lệ

**Request:**
```
GET /api/fetch?mobileNumber=12345
```

**Response (400 Bad Request):**
```json
{
    "mobileNumber": "Mobile number must be 10 digits"
}
```

## Best Practices

1. **Luôn validate dữ liệu đầu vào** ở tầng API trước khi xử lý
2. **Cung cấp thông báo lỗi rõ ràng** giúp clients hiểu vấn đề gì đã xảy ra
3. **Sử dụng annotation validation phù hợp** dựa trên yêu cầu nghiệp vụ
4. **Validate cả request body và query parameters** một cách nhất quán
5. **Không validate response DTOs** (như ResponseDto, ErrorResponseDto) vì chúng chỉ dùng để gửi dữ liệu cho clients
6. **Giữ các quy tắc validation đồng bộ** giữa các operations khác nhau (create, update, v.v.)
7. **Xem xét các validation đặc thù nghiệp vụ** ngoài các kiểm tra định dạng chuẩn

## Tóm Tắt

Input validation là một khía cạnh quan trọng trong việc xây dựng REST APIs mạnh mẽ. Bằng cách sử dụng validation framework của Spring Boot:

- Chúng ta đảm bảo chất lượng dữ liệu trước khi nó đến business logic
- Chúng ta cung cấp thông báo lỗi có ý nghĩa cho các ứng dụng client
- Chúng ta ngăn chặn các thao tác database không cần thiết
- Chúng ta tuân theo các best practices trong phát triển API

Validation framework rất linh hoạt và có thể được mở rộng dựa trên yêu cầu nghiệp vụ cụ thể.

---

**Bước Tiếp Theo**: Tiếp tục nâng cao microservices của bạn với các tính năng và best practices bổ sung.