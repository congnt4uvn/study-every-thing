# Xây Dựng Logic Nghiệp Vụ REST API và Tầng Service

## Giới Thiệu

Bạn có hào hứng để xây dựng logic nghiệp vụ thực tế không? Trong bài giảng này, chúng ta sẽ xây dựng một REST API hỗ trợ tạo mới tài khoản và thông tin chi tiết khách hàng trong cơ sở dữ liệu H2. Chúng ta sẽ đề cập đến nhiều tiêu chuẩn quan trọng bao gồm:
- Xử lý ngoại lệ
- Logic tầng service
- Tận dụng DTO pattern
- Mapper patterns
- Các best practices cho phát triển REST API

## Thiết Lập REST API Controller

### Thêm Request Mapping Prefix

Trong các dự án thực tế, luôn được khuyến nghị duy trì một đường dẫn API tiền tố chung cho tất cả các REST API trong lớp controller.

```java
@RestController
@RequestMapping(path = "/api", produces = MediaType.APPLICATION_JSON_VALUE)
public class AccountsController {
    // Các phương thức controller
}
```

**Các Điểm Chính:**
- **Path Prefix**: `/api` - Tiền tố chung cho tất cả API trong controller này
- **Versioning**: Một số dự án cũng duy trì số phiên bản như `/api/v1` hoặc `/api/v2`
- **Produces**: Chỉ định định dạng phản hồi là JSON sử dụng `MediaType.APPLICATION_JSON_VALUE`
- Đảm bảo import `MediaType` từ package `org.springframework.http`

### Tạo Phương Thức Create Account

```java
@PostMapping("/create")
public ResponseEntity<ResponseDto> createAccount(@RequestBody CustomerDto customerDto) {
    accountsService.createAccount(customerDto);
    
    return ResponseEntity
            .status(HttpStatus.CREATED)
            .body(new ResponseDto(AccountsConstants.STATUS_201, 
                                  AccountsConstants.MESSAGE_201));
}
```

**Phân Tích Phương Thức:**
- **@PostMapping("/create")**: Ánh xạ đến endpoint `/api/create`
- **@RequestBody**: Ánh xạ request body thành đối tượng `CustomerDto`
- **ResponseEntity<ResponseDto>**: Cho phép gửi status, body và headers trong response
- **HttpStatus.CREATED**: Trả về mã trạng thái 201 cho việc tạo thành công

### Hiểu Về ResponseEntity

`ResponseEntity` là một lớp mạnh mẽ trong Spring Framework cho phép bạn:
- Gửi mã trạng thái HTTP
- Gửi response body
- Gửi custom headers
- Gửi thông tin content type

**Các phương thức có sẵn:**
- `status()` - Đặt mã trạng thái HTTP
- `body()` - Đặt response body
- `header()` - Thêm custom headers
- `contentType()` - Đặt content type

**Tại sao sử dụng ResponseEntity?**
Nếu bạn chỉ trả về `ResponseDto`, chỉ nội dung body được gửi. Với `ResponseEntity`, bạn có toàn quyền kiểm soát:
- Trạng thái HTTP tổng thể
- Response headers
- Response body
- Thông tin metadata

## Tạo Lớp Constants

Đây là tiêu chuẩn được khuyến nghị để duy trì tất cả các giá trị hằng số trong một file riêng biệt.

### Tạo Package Constants và Class

```java
package com.example.accounts.constants;

public class AccountsConstants {
    
    private AccountsConstants() {
        // Constructor private để ngăn khởi tạo
    }
    
    public static final String STATUS_201 = "201";
    public static final String MESSAGE_201 = "Account created successfully";
    public static final String STATUS_200 = "200";
    public static final String MESSAGE_200 = "Request processed successfully";
    public static final String STATUS_500 = "500";
    public static final String MESSAGE_500 = "An error occurred. Please try again or contact support";
}
```

**Best Practices cho Constants:**
1. **Static và Final**: Hằng số nên là `static final` để không thể thay đổi
2. **Đặt Tên Viết Hoa**: Sử dụng chữ cái viết hoa cho tên hằng số (ví dụ: `STATUS_201`)
3. **Dấu Gạch Dưới Phân Cách**: Sử dụng gạch dưới để phân cách từ (ví dụ: `MESSAGE_201`)
4. **Constructor Private**: Ngăn chặn việc khởi tạo lớp constants
5. **Truy Cập Static**: Sử dụng hằng số thông qua tên lớp mà không cần tạo đối tượng

**Tại sao Constructor Private?**
- Ngăn chặn việc tạo đối tượng của lớp constants
- Đảm bảo lớp chỉ được sử dụng để chứa hằng số
- Ngăn chặn "ô nhiễm" với các phương thức hoặc logic nghiệp vụ

## Tạo Tầng Service

### Service Interface

Tạo một service interface để định nghĩa hợp đồng:

```java
package com.example.accounts.service;

/**
 * Service interface cho các thao tác Account
 */
public interface IAccountsService {
    
    /**
     * Tạo một tài khoản mới
     * @param customerDto - Đối tượng CustomerDto chứa thông tin chi tiết khách hàng
     */
    void createAccount(CustomerDto customerDto);
}
```

**Quy Ước Đặt Tên:**
- Thêm tiền tố `I` cho tên interface (ví dụ: `IAccountsService`)
- Điều này chỉ rõ đây là một interface
- Lưu ý: Chúng ta không sử dụng quy ước này cho Repository interfaces vì chúng không có lớp implementation

**JavaDoc Comments:**
- Thêm tài liệu ở cấp độ phương thức
- Mô tả tham số và giá trị trả về
- Giải thích logic phức tạp cho các thành viên team trong tương lai
- Giúp duy trì code tốt hơn

### Service Implementation

```java
package com.example.accounts.service.impl;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class AccountsServiceImpl implements IAccountsService {
    
    private AccountsRepository accountsRepository;
    private CustomerRepository customerRepository;
    
    @Override
    public void createAccount(CustomerDto customerDto) {
        // Triển khai logic nghiệp vụ
    }
}
```

**Các Điểm Chính:**
1. **@Service**: Đánh dấu lớp là một component tầng service
2. **@AllArgsConstructor**: Lombok tạo constructor với tất cả các trường
3. **Constructor Injection**: Spring tự động autowire các dependency khi chỉ có một constructor
4. **Không cần @Autowired**: Với một constructor duy nhất, Spring thực hiện autowiring tự động

**Cách Constructor Injection Hoạt Động:**
- Lombok tạo constructor chấp nhận tất cả các trường
- Spring phát hiện constructor duy nhất
- Tự động inject các repository bean
- Code sạch hơn không cần annotation `@Autowired` tường minh

## Tạo Các Lớp Mapper

Chúng ta cần logic mapper để chuyển đổi giữa các lớp DTO và Entity.

### AccountsMapper

```java
package com.example.accounts.mapper;

public class AccountsMapper {
    
    public static AccountsDto mapToAccountsDto(Accounts accounts, AccountsDto accountsDto) {
        accountsDto.setAccountNumber(accounts.getAccountNumber());
        accountsDto.setAccountType(accounts.getAccountType());
        accountsDto.setBranchAddress(accounts.getBranchAddress());
        return accountsDto;
    }
    
    public static Accounts mapToAccounts(AccountsDto accountsDto, Accounts accounts) {
        accounts.setAccountNumber(accountsDto.getAccountNumber());
        accounts.setAccountType(accountsDto.getAccountType());
        accounts.setBranchAddress(accountsDto.getBranchAddress());
        return accounts;
    }
}
```

### CustomerMapper

```java
package com.example.accounts.mapper;

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
}
```

**Giải Thích Logic Mapper:**
- **Static Methods**: Có thể gọi mà không cần tạo đối tượng mapper
- **Ánh Xạ Hai Chiều**: 
  - `mapToDto`: Entity → DTO
  - `mapToEntity`: DTO → Entity
- **Dựa Trên Setter/Getter**: Sử dụng phương thức getter/setter đơn giản cho việc ánh xạ

## Thư Viện Mapper Thay Thế

### Các Thư Viện Mapper Phổ Biến

Có các thư viện hỗ trợ ánh xạ tự động:

1. **ModelMapper**
2. **MapStruct**

Các thư viện này có thể tự động chuyển đổi giữa DTO và Entity với code tối thiểu.

### Tại Sao Không Sử Dụng Chúng Trong Khóa Học Này?

**Lý do cho việc ánh xạ thủ công:**

1. **Công Nhận Chính Thức**: 
   - Lombok được Spring công nhận chính thức (có sẵn trên start.spring.io)
   - ModelMapper và MapStruct không được liệt kê chính thức

2. **Vấn Đề Bảo Mật**:
   - Các thư viện mã nguồn mở có thể có lỗ hổng bảo mật
   - Có thể cần sự chấp thuận của client/kiến trúc sư
   - Một số website thiếu chứng chỉ chính thức

3. **Kiểm Soát Hoàn Toàn**:
   - Logic serialization tùy chỉnh
   - Che dấu dữ liệu (ví dụ: ẩn một phần số điện thoại)
   - Tính linh hoạt cho các chuyển đổi phức tạp

**Ví Dụ Use Case:**
```java
// Che dấu số điện thoại - chỉ hiển thị 4 số cuối
public static CustomerDto mapToCustomerDto(Customer customer, CustomerDto customerDto) {
    customerDto.setName(customer.getName());
    customerDto.setEmail(customer.getEmail());
    String mobile = customer.getMobileNumber();
    customerDto.setMobileNumber("****" + mobile.substring(mobile.length() - 4));
    return customerDto;
}
```

Tính linh hoạt này có thể không dễ dàng có sẵn với các thư viện mapper tự động.

### Khi Nào Sử Dụng Automated Mappers

Nếu client và project lead của bạn chấp thuận:
- Chúng dễ học
- Chúng dễ sử dụng
- Chúng giảm code boilerplate
- Chúng phù hợp cho các ánh xạ đơn giản

**Tiêu Chí Quyết Định:**
- Chấp thuận của client ✓
- Chấp thuận của project lead ✓
- Không có logic chuyển đổi phức tạp ✓
- Đánh giá bảo mật hoàn tất ✓

## Tóm Tắt

Trong bài giảng này, chúng ta đã đề cập:

1. **Thiết Lập REST API**:
   - Request mapping với path prefix
   - Cấu hình content type phản hồi
   - POST endpoint để tạo tài khoản

2. **Quản Lý Constants**:
   - Tạo lớp constants chuyên dụng
   - Best practices cho đặt tên hằng số
   - Pattern constructor private

3. **Kiến Trúc Tầng Service**:
   - Thiết kế dựa trên interface
   - Triển khai service
   - Dependency injection dựa trên constructor

4. **Mapper Pattern**:
   - Chuyển đổi thủ công DTO ↔ Entity
   - Phương thức mapper static
   - Kiểm soát hoàn toàn việc chuyển đổi dữ liệu

5. **ResponseEntity**:
   - Kiểm soát phản hồi toàn diện
   - Mã trạng thái, headers và body
   - Thiết kế API chuyên nghiệp

## Các Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ tiếp tục triển khai logic nghiệp vụ để tạo tài khoản và khách hàng trong cơ sở dữ liệu. Chúng ta cũng sẽ khám phá xử lý ngoại lệ và validation.

---

**Hãy nghỉ ngơi và hẹn gặp lại trong bài giảng tiếp theo!**