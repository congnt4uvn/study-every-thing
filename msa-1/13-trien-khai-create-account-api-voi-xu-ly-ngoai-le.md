# Triển Khai Create Account API Với Xử Lý Ngoại Lệ

## Giới Thiệu

Chào mừng trở lại! Trong bài giảng này, chúng ta sẽ hoàn thành việc triển khai logic nghiệp vụ tạo tài khoản, bao gồm:
- Chuyển đổi DTO thành Entity và lưu vào database
- Xử lý ngoại lệ tùy chỉnh
- Global exception handler
- Derived named methods trong Spring Data JPA
- Kiểm thử API với Postman
- Xử lý các trường audit

## Triển Khai Logic Tầng Service

### Bước 1: Chuyển Đổi DTO Thành Entity

Trong `AccountsServiceImpl`, chúng ta cần chuyển đổi `CustomerDto` đầu vào thành entity `Customer`:

```java
@Override
public void createAccount(CustomerDto customerDto) {
    Customer customer = CustomerMapper.mapToCustomer(customerDto, new Customer());
    Customer savedCustomer = customerRepository.save(customer);
    accountsRepository.save(createNewAccount(savedCustomer));
}
```

**Giải Thích:**
1. Sử dụng `CustomerMapper.mapToCustomer()` để chuyển đổi DTO thành Entity
2. Truyền DTO và một đối tượng `Customer()` mới
3. Dữ liệu từ `CustomerDto` được chuyển sang entity `Customer`

### Bước 2: Lưu Customer Vào Database

```java
Customer savedCustomer = customerRepository.save(customer);
```

**Điều Gì Xảy Ra Đằng Sau:**
Spring Data JPA tự động xử lý:
- Tạo câu lệnh SQL
- Mở kết nối database
- Thực thi câu lệnh
- Commit transaction
- Đóng kết nối

**Lưu Ý Quan Trọng:**
- Phương thức `save()` đến từ `JpaRepository` (mà `CustomerRepository` extends)
- Khi lưu, `customerId` được tự động tạo bởi Spring Data JPA
- Lưu kết quả vào `savedCustomer` để truy cập ID được tạo

### Bước 3: Tạo Account Cho Customer

Tạo một phương thức private để tạo account mới:

```java
private Accounts createNewAccount(Customer customer) {
    Accounts newAccount = new Accounts();
    newAccount.setCustomerId(customer.getCustomerId());
    
    long randomAccNumber = 1000000000L + new Random().nextInt(900000000);
    newAccount.setAccountNumber(randomAccNumber);
    newAccount.setAccountType(AccountsConstants.SAVINGS);
    newAccount.setBranchAddress("123 Main Street, New York");
    
    newAccount.setCreatedAt(LocalDateTime.now());
    newAccount.setCreatedBy("Anonymous");
    
    return newAccount;
}
```

**Các Điểm Chính:**
1. **CustomerId**: Liên kết account với customer
2. **Account Number**: Số ngẫu nhiên 10 chữ số do developer tạo
3. **Account Type**: Sử dụng hằng số `SAVINGS` từ `AccountsConstants`
4. **Branch Address**: Địa chỉ mặc định được gán
5. **Audit Fields**: Được điền thủ công bây giờ (sẽ tự động hóa sau)

### Bước 4: Lưu Account Vào Database

```java
accountsRepository.save(createNewAccount(savedCustomer));
```

Điều này thiết lập liên kết giữa customer và account thông qua `customerId`.

## Xử Lý Ngoại Lệ

### Vấn Đề

Chúng ta cần ngăn chặn customer trùng lặp dựa trên số điện thoại:
- Chỉ một customer cho mỗi số điện thoại
- Nhiều customer có thể có cùng email hoặc tên
- Số điện thoại phải là duy nhất

### Tạo Custom Exception

Tạo một lớp exception tùy chỉnh:

```java
package com.example.accounts.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(value = HttpStatus.BAD_REQUEST)
public class CustomerAlreadyExistsException extends RuntimeException {
    
    public CustomerAlreadyExistsException(String message) {
        super(message);
    }
}
```

**Các Điểm Chính:**
1. **Extends RuntimeException**: Bắt buộc cho custom exceptions
2. **Constructor với Message**: Nhận thông điệp exception và truyền cho parent
3. **@ResponseStatus**: Tự động trả về `400 BAD_REQUEST` khi được throw

### Tạo Derived Named Method

Chúng ta cần query theo số điện thoại, nhưng `CustomerRepository` chỉ có phương thức cho `customerId` (primary key).

**Thêm vào CustomerRepository:**

```java
public interface CustomerRepository extends JpaRepository<Customer, Long> {
    
    Optional<Customer> findByMobileNumber(String mobileNumber);
}
```

**Cách Derived Named Methods Hoạt Động:**
- **Quy Ước Đặt Tên**: `findBy` + `TênTrường`
- Spring Data JPA tự động tạo query
- Tên trường phải khớp với trường entity (không phân biệt hoa thường)
- Cho nhiều cột: `findByMobileNumberAndEmail(String mobile, String email)`

**Các Pattern Ví Dụ:**
- `findByMobileNumber` → SELECT * FROM customer WHERE mobile_number = ?
- `findByEmail` → SELECT * FROM customer WHERE email = ?
- `findByNameAndEmail` → SELECT * FROM customer WHERE name = ? AND email = ?

### Validate Trước Khi Lưu

Thêm logic validation trong `AccountsServiceImpl`:

```java
@Override
public void createAccount(CustomerDto customerDto) {
    // Validate nếu customer đã tồn tại
    Optional<Customer> optionalCustomer = customerRepository
            .findByMobileNumber(customerDto.getMobileNumber());
    
    if(optionalCustomer.isPresent()) {
        throw new CustomerAlreadyExistsException(
            "Customer already registered with given mobile number: " 
            + customerDto.getMobileNumber()
        );
    }
    
    // Tạo customer và account
    Customer customer = CustomerMapper.mapToCustomer(customerDto, new Customer());
    customer.setCreatedAt(LocalDateTime.now());
    customer.setCreatedBy("Anonymous");
    
    Customer savedCustomer = customerRepository.save(customer);
    accountsRepository.save(createNewAccount(savedCustomer));
}
```

**Luồng Logic:**
1. Query database theo số điện thoại
2. Nếu customer tồn tại (`isPresent()` trả về true), throw exception
3. Nếu không, tiến hành tạo account

## Global Exception Handler

### Vấn Đề Với Xử Lý Exception Cục Bộ

Nếu chúng ta xử lý exception trong mỗi phương thức controller:
- Code trùng lặp qua nhiều controller
- Khó bảo trì
- Phản hồi lỗi không nhất quán

### Giải Pháp: Global Exception Handler

Tạo một exception handler tập trung:

```java
package com.example.accounts.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.context.request.WebRequest;

import java.time.LocalDateTime;

@ControllerAdvice
public class GlobalExceptionHandler {
    
    @ExceptionHandler(CustomerAlreadyExistsException.class)
    public ResponseEntity<ErrorResponseDto> handleCustomerAlreadyExistsException(
            CustomerAlreadyExistsException exception,
            WebRequest webRequest) {
        
        ErrorResponseDto errorResponseDto = new ErrorResponseDto(
            webRequest.getDescription(false),
            HttpStatus.BAD_REQUEST,
            exception.getMessage(),
            LocalDateTime.now()
        );
        
        return new ResponseEntity<>(errorResponseDto, HttpStatus.BAD_REQUEST);
    }
}
```

**Các Thành Phần Chính:**

1. **@ControllerAdvice**: Báo cho Spring lớp này xử lý exception toàn cục cho tất cả controller

2. **@ExceptionHandler**: Chỉ định exception nào phương thức này xử lý
   - Tham số: `CustomerAlreadyExistsException.class`
   - Phương thức được gọi khi exception này được throw

3. **Tham Số WebRequest**: 
   - `getDescription(false)` → Chỉ trả về đường dẫn API
   - `getDescription(true)` → Trả về đường dẫn API + IP client + chi tiết khác

4. **Tạo ErrorResponseDto**:
   - **apiPath**: Endpoint mà client cố gắng gọi
   - **errorCode**: `HttpStatus.BAD_REQUEST` (400)
   - **errorMsg**: Thông điệp exception
   - **errorTime**: Timestamp hiện tại

5. **Return**: `ResponseEntity` với chi tiết lỗi và HTTP status

### Lợi Ích Của Global Exception Handler

- ✅ Xử lý exception tập trung
- ✅ Phản hồi lỗi nhất quán
- ✅ Dễ dàng thêm exception handler mới
- ✅ Không trùng lặp code
- ✅ Định tuyến exception tự động

## Cập Nhật Controller

### Autowiring Service

Sử dụng constructor-based dependency injection:

```java
@RestController
@RequestMapping(path = "/api", produces = MediaType.APPLICATION_JSON_VALUE)
@AllArgsConstructor
public class AccountsController {
    
    private IAccountsService accountsService;
    
    @PostMapping("/create")
    public ResponseEntity<ResponseDto> createAccount(@RequestBody CustomerDto customerDto) {
        accountsService.createAccount(customerDto);
        
        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(new ResponseDto(AccountsConstants.STATUS_201, 
                                      AccountsConstants.MESSAGE_201));
    }
}
```

**Tại Sao Constructor Injection?**
- ✅ Cách tiếp cận được khuyến nghị hơn field injection
- ✅ Với `@AllArgsConstructor`, Lombok tạo constructor
- ✅ Constructor duy nhất → Không cần annotation `@Autowired`
- ✅ Spring tự động thực hiện dependency injection

**Luồng Exception:**
1. Nếu không có exception → Trả về phản hồi thành công (201)
2. Nếu exception xảy ra → Không bao giờ đến controller
3. Exception được bắt bởi `GlobalExceptionHandler`
4. Phản hồi lỗi được gửi đến client

## Kiểm Thử Với Postman

### Thiết Lập Postman

1. **Tải Postman**: Tải công cụ từ website chính thức
2. **Import Collection**: 
   - Tải collection JSON từ GitHub repo
   - File → Import → Thả file JSON
   - Tất cả request được tải tự động

### Request Tạo Account

**Endpoint:** `POST http://localhost:8080/api/create`

**Request Body:**
```json
{
    "name": "Madan Reddy",
    "email": "madan@example.com",
    "mobileNumber": "1234567890"
}
```

**Lưu Ý Quan Trọng:**
- Tên trường JSON phải khớp với các trường `CustomerDto`: `name`, `email`, `mobileNumber`
- Spring Boot sử dụng thư viện Jackson để chuyển đổi JSON ↔ POJO
- Chuyển đổi xảy ra tự động

### Request Đầu Tiên - Phản Hồi Thành Công

**Response:**
```json
{
    "statusCode": "201",
    "statusMsg": "Account created successfully"
}
```

**HTTP Status:** `201 CREATED`

### Request Thứ Hai - Số Điện Thoại Trùng Lặp

**Response:**
```json
{
    "apiPath": "uri=/api/create",
    "errorCode": "BAD_REQUEST",
    "errorMsg": "Customer already registered with given mobile number: 1234567890",
    "errorTime": "2026-03-09T10:30:45"
}
```

**HTTP Status:** `400 BAD_REQUEST`

## Sửa Lỗi Audit Fields

### Lỗi Ban Đầu

Lần thử đầu tiên thất bại vì `createdAt` và `createdBy` là null (vi phạm ràng buộc not-null).

### Giải Pháp - Điền Thủ Công

Thêm audit fields trước khi lưu:

```java
// Cho Customer
customer.setCreatedAt(LocalDateTime.now());
customer.setCreatedBy("Anonymous");

// Cho Account
newAccount.setCreatedAt(LocalDateTime.now());
newAccount.setCreatedBy("Anonymous");
```

**Lưu Ý:** Chúng ta sẽ tự động hóa điều này sử dụng Spring Data JPA auditing trong các bài giảng sau.

## Xác Minh Dữ Liệu Trong H2 Console

### Truy Cập H2 Console

1. Điều hướng đến: `http://localhost:8080/h2-console`
2. Kết nối đến database
3. Chạy queries để xác minh dữ liệu

### Query Bảng Customer

```sql
SELECT * FROM customer;
```

**Kết Quả:**
- Chi tiết customer được insert thành công
- `customerId` được tự động tạo

### Query Bảng Accounts

```sql
SELECT * FROM accounts;
```

**Kết Quả:**
- Số tài khoản ngẫu nhiên 10 chữ số được tạo
- `customerId` liên kết đến bảng customer
- Loại tài khoản và địa chỉ chi nhánh được điền

## Xử Lý Vấn Đề Dev Tools Restart

### Vấn Đề: Hot Swap Thất Bại

Khi thực hiện nhiều thay đổi, Spring DevTools có thể thất bại trong việc hot reload:
```
Hot swap failed
```

### Giải Pháp

1. **Dừng server thủ công**
2. **Clean và rebuild**: `mvn clean install`
3. **Khởi động lại server**

Điều này đảm bảo tất cả thay đổi được tải đúng cách.

## Tóm Tắt

Trong bài giảng toàn diện này, chúng ta đã triển khai:

### ✅ Triển Khai Tầng Service
- Chuyển đổi DTO thành Entity sử dụng mappers
- Lưu customer vào database
- Tạo và lưu account với số tài khoản ngẫu nhiên
- Liên kết account với customer qua `customerId`

### ✅ Xử Lý Custom Exception
- Tạo `CustomerAlreadyExistsException`
- Extends `RuntimeException`
- Sử dụng annotation `@ResponseStatus`

### ✅ Derived Named Methods
- `findByMobileNumber()` trong repository
- Tự động tạo query bởi Spring Data JPA
- Validation trước khi lưu

### ✅ Global Exception Handler
- Xử lý exception tập trung với `@ControllerAdvice`
- `@ExceptionHandler` cho exception cụ thể
- Phản hồi lỗi nhất quán

### ✅ Triển Khai Controller
- Constructor-based dependency injection
- `@AllArgsConstructor` cho constructor tự động
- Sử dụng `ResponseEntity` đúng cách

### ✅ Kiểm Thử
- Thiết lập và sử dụng Postman
- Validation kịch bản thành công
- Validation kịch bản exception
- Xác minh database qua H2 console

## Các Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ triển khai:
- **Read API** (lấy thông tin chi tiết account)
- **Update API** (sửa đổi account/customer)
- **Delete API** (xóa account)

Điều này sẽ hoàn thành các thao tác CRUD đầy đủ cho Accounts Microservice!

---

**Bạn có hào hứng không? Hãy tiếp tục xây dựng trong bài giảng tiếp theo!**