# Xây Dựng Loans Microservice - Tổng Quan

## Giới Thiệu

Phần này trình bày cách triển khai microservice Loans (Quản lý Khoản vay), tuân theo cùng các mẫu kiến trúc và tiêu chuẩn mã hóa như microservice Accounts. Microservice này sẽ xử lý các thao tác về khoản vay bao gồm tạo, đọc, cập nhật và xóa (CRUD).

## Cấu Hình Dự Án

### Các Dependency Maven (pom.xml)

Loans microservice sử dụng các dependency chính sau:

- **Spring Boot Actuator** - Để giám sát và quản lý
- **Spring Data JPA** - Cho các thao tác cơ sở dữ liệu
- **Spring Boot Starter Validation** - Để xác thực đầu vào
- **Spring Boot Starter Web** - Để phát triển REST API
- **Spring Boot DevTools** - Tiện ích phát triển
- **H2 Database** - Cơ sở dữ liệu trong bộ nhớ
- **Lombok** - Giảm code boilerplate
- **SpringDoc OpenAPI** - Để tài liệu hóa API
- **Spring Boot Starter Test** - Để kiểm thử

**Chi Tiết Dự Án:**
- Group ID: `com.easybytes`
- Artifact ID: `loans`
- Phiên Bản Java: 17
- Cổng: **8090** (quan trọng để duy trì xuyên suốt khóa học)

### Cấu Hình Application (application.yaml)

```yaml
server:
  port: 8090

spring:
  datasource:
    url: jdbc:h2:mem:loansdb
    driver-class-name: org.h2.Driver
    username: sa
    password: ''
  h2:
    console:
      enabled: true
  jpa:
    database-platform: org.hibernate.dialect.H2Dialect
    hibernate:
      ddl-auto: update
    show-sql: true
```

**Quan Trọng:** Luôn sử dụng cổng 8090 cho Loans microservice để tránh các vấn đề cấu hình với Docker và Kubernetes ở các phần sau.

## Cấu Trúc Cơ Sở Dữ Liệu

### Cấu Trúc Bảng Loans

Loans microservice sử dụng một bảng duy nhất tên là `loans`:

| Tên Cột | Kiểu Dữ Liệu | Mô Tả |
|---------|--------------|-------|
| loan_id | Primary Key | Định danh duy nhất tự động sinh |
| mobile_number | String | Số điện thoại khách hàng (liên kết với Accounts microservice) |
| loan_number | String | Mã số khoản vay được sinh ra |
| loan_type | String | Loại khoản vay (ví dụ: Vay mua nhà, Vay mua xe) |
| total_loan | Decimal | Tổng số tiền vay |
| amount_paid | Decimal | Số tiền đã trả |
| outstanding_amount | Decimal | Số tiền còn lại phải trả |
| created_at | Timestamp | Thời điểm tạo bản ghi |
| created_by | String | Người tạo bản ghi |
| updated_at | Timestamp | Thời điểm cập nhật cuối |
| updated_by | String | Người cập nhật cuối cùng |

**Lưu Ý Thiết Kế:** Loans microservice không có bảng customer riêng. Nó sử dụng số điện thoại để liên kết với khách hàng đã tạo trong Accounts microservice.

## Các Lớp Entity

### Base Entity

Chứa các trường audit chung:
- `created_at` - Thời điểm tạo
- `created_by` - Thông tin người tạo
- `updated_at` - Thời điểm sửa đổi cuối
- `updated_by` - Thông tin người sửa đổi cuối

### Loans Entity

```java
@Entity
public class Loans extends BaseEntity {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long loanId;
    
    private String mobileNumber;
    private String loanNumber;
    private String loanType;
    private Integer totalLoan;
    private Integer amountPaid;
    private Integer outstandingAmount;
}
```

**Điểm Chính:**
- Kế thừa `BaseEntity` để có các trường audit
- Việc sinh khóa chính được ủy thác cho Spring Data JPA
- Tên trường khớp với tên cột (không cần annotation `@Column`)
- Loan ID không được expose trong DTOs (chi tiết kỹ thuật, không phải thông tin nghiệp vụ)

## Data Transfer Objects (DTOs)

### Loans DTO

Chỉ chứa các trường liên quan đến nghiệp vụ:
- `mobileNumber` - Số điện thoại khách hàng
- `loanNumber` - Định danh khoản vay
- `loanType` - Loại khoản vay
- `totalLoan` - Tổng số tiền vay
- `amountPaid` - Số tiền đã trả
- `outstandingAmount` - Số dư còn lại

**Lợi Ích Của DTO Pattern:**
- Tách biệt biểu diễn nội bộ với API bên ngoài
- Ẩn các chi tiết kỹ thuật (như khóa chính)
- Cho phép validation và annotation tài liệu hóa

### Các Annotation Validation

- `@NotEmpty` - Đảm bảo trường không rỗng
- `@Pattern` - Xác thực theo mẫu regex
- `@Positive` - Chỉ chấp nhận số dương (không cho phép số 0)
- `@PositiveOrZero` - Chấp nhận số 0 và số dương

### Các Annotation OpenAPI

- `@Schema` - Thêm mô tả và metadata vào tài liệu API

## Tầng Repository

### Loans Repository

```java
public interface LoansRepository extends JpaRepository<Loans, Long> {
    Optional<Loans> findByMobileNumber(String mobileNumber);
    Optional<Loans> findByLoanNumber(String loanNumber);
}
```

**Các Phương Thức Tùy Chỉnh:**
- `findByMobileNumber` - Lấy khoản vay theo số điện thoại khách hàng
- `findByLoanNumber` - Lấy khoản vay theo mã số khoản vay

Các phương thức này cần thiết vì khóa chính là `loanId`, nhưng các thao tác nghiệp vụ sử dụng số điện thoại và số khoản vay.

## Tầng Controller

### Loans Controller

**Cấu Hình Cơ Bản:**
- `@RestController` - Đánh dấu là REST controller
- `@RequestMapping("/api")` - Đường dẫn cơ sở cho tất cả API
- Trả về response dạng JSON
- Inject `ILoanService` cho logic nghiệp vụ

### Các API Endpoints

1. **Tạo Khoản Vay** - `POST /api/create`
   - Nhận số điện thoại làm query parameter
   - Tạo bản ghi khoản vay mới
   - Trả về 201 (Created) khi thành công

2. **Lấy Chi Tiết Khoản Vay** - `GET /api/fetch`
   - Nhận số điện thoại làm query parameter
   - Trả về chi tiết khoản vay
   - Trả về 200 (OK) với dữ liệu khoản vay

3. **Cập Nhật Chi Tiết Khoản Vay** - `PUT /api/update`
   - Nhận Loans DTO trong request body
   - Cập nhật thông tin khoản vay
   - Trả về 200 (OK) khi thành công
   - Trả về 417 (Expectation Failed) khi thất bại

4. **Xóa Chi Tiết Khoản Vay** - `DELETE /api/delete`
   - Nhận số điện thoại làm query parameter
   - Xóa bản ghi khoản vay
   - Trả về 200 (OK) khi thành công

**Tài Liệu OpenAPI:**
Tất cả endpoints bao gồm:
- `@Operation` - Tóm tắt và mô tả operation
- `@ApiResponse` - Mã response và mô tả

## Tầng Service

### Interface ILoanService

Định nghĩa bốn phương thức trừu tượng:
- `createLoan(String mobileNumber)`
- `fetchLoan(String mobileNumber)`
- `updateLoan(LoansDto loansDto)`
- `deleteLoan(String mobileNumber)`

### Triển Khai Loan Service

#### Logic Tạo Khoản Vay

```java
public void createLoan(String mobileNumber) {
    // Kiểm tra khoản vay đã tồn tại chưa
    Optional<Loans> optionalLoans = loansRepository.findByMobileNumber(mobileNumber);
    if(optionalLoans.isPresent()) {
        throw new LoanAlreadyExistsException("Loan already exists");
    }
    
    // Tạo khoản vay mới
    loansRepository.save(createNewLoan(mobileNumber));
}
```

**Giá Trị Mặc Định Khoản Vay Mới:**
- Mã Số Khoản Vay: Số ngẫu nhiên 12 chữ số
- Loại Khoản Vay: Vay mua nhà (mặc định)
- Tổng Khoản Vay: 100,000 (sử dụng dấu gạch dưới để dễ đọc: `100_000`)
- Số Tiền Đã Trả: 0
- Số Tiền Còn Lại: 100,000

**Lưu Ý Tính Năng Java:** Dấu gạch dưới trong các giá trị số (được giới thiệu trong Java 7/8) cải thiện khả năng đọc. JVM loại bỏ chúng trong quá trình biên dịch.

#### Logic Lấy Khoản Vay

```java
public LoansDto fetchLoan(String mobileNumber) {
    Loans loans = loansRepository.findByMobileNumber(mobileNumber)
        .orElseThrow(() -> new ResourceNotFoundException("Loan", "mobileNumber", mobileNumber));
    
    return LoansMapper.mapToLoansDto(loans, new LoansDto());
}
```

- Lấy khoản vay theo số điện thoại
- Ném `ResourceNotFoundException` nếu không tìm thấy
- Chuyển đổi entity sang DTO bằng mapper

#### Logic Cập Nhật Khoản Vay

```java
public boolean updateLoan(LoansDto loansDto) {
    Loans loans = loansRepository.findByLoanNumber(loansDto.getLoanNumber())
        .orElseThrow(() -> new ResourceNotFoundException("Loan", "loanNumber", loansDto.getLoanNumber()));
    
    LoansMapper.mapToLoans(loansDto, loans);
    loansRepository.save(loans);
    return true;
}
```

- Lấy theo mã số khoản vay (định danh bất biến)
- Map các giá trị DTO vào entity
- Phương thức Save thực hiện UPDATE (không phải INSERT) khi bản ghi đã tồn tại
- Trả về true khi thành công

#### Logic Xóa Khoản Vay

```java
public boolean deleteLoan(String mobileNumber) {
    Loans loans = loansRepository.findByMobileNumber(mobileNumber)
        .orElseThrow(() -> new ResourceNotFoundException("Loan", "mobileNumber", mobileNumber));
    
    loansRepository.deleteById(loans.getLoanId());
    return true;
}
```

- Lấy khoản vay theo số điện thoại
- Xóa theo khóa chính (loanId)
- Trả về true khi thành công

## Xử Lý Exception

### Các Exception Tùy Chỉnh

- **LoanAlreadyExistsException** - Ném khi cố gắng tạo khoản vay trùng lặp
- **ResourceNotFoundException** - Ném khi không tìm thấy khoản vay

### Global Exception Handler

Xử lý:
- Lỗi validation đầu vào
- Runtime exceptions
- Custom business exceptions

Trả về error response phù hợp với:
- Thông báo lỗi
- Mã trạng thái
- Timestamp
- Đường dẫn API

## Kiểm Thử Với Postman

### Các Kịch Bản Test

**1. Tạo Khoản Vay**
```
POST http://localhost:8090/api/create?mobileNumber=1234567890
Response: 201 - Tạo khoản vay thành công
```

**2. Lấy Khoản Vay**
```
GET http://localhost:8090/api/fetch?mobileNumber=1234567890
Response: 200 - Trả về chi tiết khoản vay
```

**3. Cập Nhật Khoản Vay**
```
PUT http://localhost:8090/api/update
Body: {
  "mobileNumber": "1234567890",
  "loanNumber": "123456789012",
  "loanType": "Vehicle Loan",
  "totalLoan": 100000,
  "amountPaid": 10000,
  "outstandingAmount": 90000
}
Response: 200 - Cập nhật khoản vay thành công
```

**4. Xóa Khoản Vay**
```
DELETE http://localhost:8090/api/delete?mobileNumber=1234567890
Response: 200 - Xóa khoản vay thành công
```

### Các Test Case Tiêu Cực

**Lỗi Validation:**
- Số tiền âm → Lỗi validation
- Định dạng số điện thoại không hợp lệ → Lỗi validation
- Mã khoản vay > 12 chữ số → Lỗi validation

**Lỗi Nghiệp Vụ:**
- Số điện thoại không tồn tại → ResourceNotFoundException
- Tạo khoản vay trùng lặp → LoanAlreadyExistsException

## Ghi Chú Quan Trọng

1. **Tính Nhất Quán Số Điện Thoại:** Sử dụng cùng một số điện thoại xuyên suốt các microservices Accounts, Loans và Cards để kiểm thử tích hợp ở các phần sau.

2. **Số Cổng:** Luôn sử dụng cổng 8090 cho Loans microservice để tránh vấn đề với cấu hình Docker và Kubernetes.

3. **Chiến Lược Lặp Lại:** Khóa học lặp lại mỗi khái niệm ba lần trên ba microservices (Accounts, Loans, Cards) để củng cố kiến thức và xây dựng trí nhớ cơ bắp.

4. **Tiêu Chuẩn Code:** Tuân theo cùng các tiêu chuẩn và mẫu code trên tất cả microservices để đảm bảo tính nhất quán.

## Bước Tiếp Theo

Bài giảng tiếp theo sẽ đề cập đến Cards microservice, tuân theo các mẫu và tiêu chuẩn tương tự. Bạn có thể bỏ qua nếu đã nắm vững các khái niệm, hoặc xem lại để củng cố.

## Tóm Tắt

Loans microservice minh họa:
- Cấu trúc dự án Spring Boot tiêu chuẩn
- Phát triển REST API với các HTTP method phù hợp
- JPA entities và repositories với các truy vấn tùy chỉnh
- DTO pattern cho thiết kế API
- Input validation và xử lý exception
- Tài liệu OpenAPI
- Triển khai logic nghiệp vụ trong tầng service
- Các thao tác CRUD với xử lý lỗi phù hợp

Tất cả các mẫu và thực hành sẽ được lặp lại trong Cards microservice để củng cố kiến thức.