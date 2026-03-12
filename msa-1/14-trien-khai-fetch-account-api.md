# Triển Khai Fetch Account API

## Tổng Quan
Trong phần này, chúng ta sẽ tạo một REST API để truy xuất thông tin tài khoản và khách hàng từ cơ sở dữ liệu bằng cách nhận số điện thoại làm đầu vào. API sẽ trả về thông tin đầy đủ về khách hàng và tài khoản ngân hàng dựa trên số điện thoại được cung cấp.

## Bước 1: Tạo Phương Thức Controller

Đầu tiên, thêm một phương thức mới trong lớp `AccountsController`:

```java
@GetMapping("/fetch")
public ResponseEntity<CustomerDto> fetchAccountDetails(@RequestParam String mobileNumber) {
    CustomerDto customerDto = iAccountService.fetchAccount(mobileNumber);
    return ResponseEntity.status(HttpStatus.OK).body(customerDto);
}
```

**Các Điểm Chính:**
- Phương thức trả về `CustomerDto` được bọc trong `ResponseEntity`
- Sử dụng `@RequestParam` để nhận số điện thoại dưới dạng tham số truy vấn
- Ánh xạ đến endpoint `/api/fetch`
- Sử dụng annotation `@GetMapping` cho các thao tác đọc dữ liệu

## Bước 2: Định Nghĩa Phương Thức Service Interface

Thêm phương thức trừu tượng trong `IAccountService`:

```java
CustomerDto fetchAccount(String mobileNumber);
```

## Bước 3: Tạo ResourceNotFoundException

Tạo một lớp exception tùy chỉnh mới trong package exception:

```java
@ResponseStatus(value = HttpStatus.NOT_FOUND)
public class ResourceNotFoundException extends RuntimeException {
    
    public ResourceNotFoundException(String resourceName, String fieldName, String fieldValue) {
        super(String.format("%s not found with the given input data %s : '%s'", 
            resourceName, fieldName, fieldValue));
    }
}
```

**Chi Tiết Exception:**
- Trả về trạng thái `404 NOT_FOUND`
- Nhận ba tham số: tên resource, tên trường, và giá trị trường
- Cung cấp thông báo lỗi chi tiết cho client

## Bước 4: Thêm Phương Thức Global Exception Handler

Thêm xử lý exception trong `GlobalExceptionHandler`:

```java
@ExceptionHandler(ResourceNotFoundException.class)
public ResponseEntity<ErrorResponseDto> handleResourceNotFoundException(
        ResourceNotFoundException exception,
        WebRequest webRequest) {
    
    ErrorResponseDto errorResponseDto = new ErrorResponseDto(
        webRequest.getDescription(false),
        HttpStatus.NOT_FOUND,
        exception.getMessage(),
        LocalDateTime.now()
    );
    
    return new ResponseEntity<>(errorResponseDto, HttpStatus.NOT_FOUND);
}
```

## Bước 5: Triển Khai Logic Service

Triển khai phương thức `fetchAccount()` trong `AccountsServiceImpl`:

```java
@Override
public CustomerDto fetchAccount(String mobileNumber) {
    // Lấy thông tin khách hàng
    Customer customer = customerRepository.findByMobileNumber(mobileNumber)
        .orElseThrow(() -> new ResourceNotFoundException(
            "Customer", "mobileNumber", mobileNumber));
    
    // Lấy thông tin tài khoản
    Accounts accounts = accountsRepository.findByCustomerId(customer.getCustomerId())
        .orElseThrow(() -> new ResourceNotFoundException(
            "Account", "customerId", customer.getCustomerId().toString()));
    
    // Chuyển đổi sang DTOs
    CustomerDto customerDto = CustomerMapper.mapToCustomerDto(customer, new CustomerDto());
    customerDto.setAccountsDto(AccountsMapper.mapToAccountsDto(accounts, new AccountsDto()));
    
    return customerDto;
}
```

## Bước 6: Thêm Phương Thức Repository

Tạo phương thức mới trong `AccountsRepository`:

```java
Optional<Accounts> findByCustomerId(Long customerId);
```

Phương thức này truy vấn tài khoản theo customer ID, tận dụng khả năng tự động tạo query của Spring Data JPA.

## Bước 7: Cải Tiến CustomerDto

Thêm trường `AccountsDto` lồng nhau vào `CustomerDto` để trả về thông tin kết hợp:

```java
@Data
public class CustomerDto {
    private String name;
    private String email;
    private String mobileNumber;
    private AccountsDto accountsDto;  // Trường mới
}
```

**Các Tùy Chọn Thiết Kế:**
- **Tùy chọn 1:** Thêm trường `AccountsDto` trong `CustomerDto` (được khuyến nghị cho ứng dụng nhỏ)
- **Tùy chọn 2:** Tạo lớp DTO tổng hợp riêng biệt (tốt hơn cho ứng dụng phức tạp với nhiều trường)

## Kiểm Thử API

### Yêu Cầu Thành Công
**Endpoint:** `GET http://localhost:8080/api/fetch?mobileNumber=1234567890`

**Phản hồi:**
```json
{
    "name": "John Doe",
    "email": "john@example.com",
    "mobileNumber": "1234567890",
    "accountsDto": {
        "accountNumber": 123456789,
        "accountType": "Savings",
        "branchAddress": "123 Main Street"
    }
}
```

### Trường Hợp Lỗi
**Endpoint:** `GET http://localhost:8080/api/fetch?mobileNumber=9999999999`

**Phản hồi (404 NOT FOUND):**
```json
{
    "apiPath": "/api/fetch",
    "errorCode": "NOT_FOUND",
    "errorMessage": "Customer not found with the given input data mobileNumber : '9999999999'",
    "errorTime": "2024-03-09T10:30:45"
}
```

## Các Lưu Ý Quan Trọng

1. **Mất Dữ Liệu H2 Database:** Dữ liệu bị mất khi server khởi động lại (vấn đề tạm thời cho đến khi chuyển sang MySQL)
2. **Tham Số Truy Vấn:** Đảm bảo tên `@RequestParam` khớp với tên tham số
3. **Xử Lý Exception:** Luôn xác minh các exception handler được cấu hình đúng
4. **Kiểm Thử:** Unit testing và debugging rất quan trọng để phát hiện các lỗi nhỏ

## Các Điểm Chính Cần Nhớ

- Sử dụng `@GetMapping` cho các thao tác đọc dữ liệu
- `@RequestParam` nhận các tham số truy vấn
- Exception tùy chỉnh cung cấp thông tin lỗi chi tiết
- DTO pattern ngăn chặn việc lộ thông tin entity nhạy cảm
- Phương thức Repository có thể được tự động tạo bởi Spring Data JPA
- DTO lồng nhau cho phép trả về phản hồi tổng hợp

## Các Bước Tiếp Theo

Trong phần tiếp theo, chúng ta sẽ triển khai các thao tác cập nhật và xóa để hoàn thiện chức năng CRUD cho accounts microservice.