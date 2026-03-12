# Xây Dựng Cards Microservice - Tổng Quan

## Giới Thiệu

Phần này trình bày cách triển khai microservice Cards (Quản lý Thẻ), microservice thứ ba và cuối cùng trong bộ ba dịch vụ nghiệp vụ cốt lõi của chúng ta (Accounts, Loans và Cards). Vì các mẫu thiết kế và tiêu chuẩn đã được giải thích hai lần trước đó, phần này sẽ là một hướng dẫn nhanh tập trung vào các chi tiết triển khai chính.

## Cấu Hình Dự Án

### Các Maven Dependencies (pom.xml)

**Chi Tiết Dự Án:**
- Group ID: `com.easybytes`
- Artifact ID: `cards`
- Name: `cards`
- Phiên Bản Java: 17

**Các Dependency Chính:**
- Spring Boot Actuator
- Spring Data JPA
- Spring Boot Starter Validation
- Spring Boot Starter Web
- Spring Boot DevTools
- H2 Database
- Lombok
- SpringDoc OpenAPI
- Spring Boot Starter Test

### Cấu Hình Application (application.yaml)

```yaml
server:
  port: 9000

spring:
  datasource:
    url: jdbc:h2:mem:cardsdb
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

### Tóm Tắt Phân Bổ Số Cổng

| Microservice | Số Cổng |
|-------------|---------|
| Accounts | 8080 |
| Loans | 8090 |
| Cards | 9000 |

**Quan Trọng:** Luôn sử dụng cổng 9000 cho Cards microservice xuyên suốt khóa học để đảm bảo tính nhất quán với cấu hình Docker và Kubernetes.

## Cấu Trúc Cơ Sở Dữ Liệu

### Cấu Trúc Bảng Cards

Cards microservice sử dụng một bảng duy nhất có tên `cards`:

| Tên Cột | Kiểu Dữ Liệu | Mô Tả |
|---------|--------------|-------|
| card_id | Primary Key | Định danh duy nhất tự động sinh |
| mobile_number | String | Số điện thoại khách hàng (liên kết với Accounts microservice) |
| card_number | String | Số thẻ được sinh ra (12 chữ số) |
| card_type | String | Loại thẻ (ví dụ: Thẻ tín dụng, Thẻ ghi nợ) |
| total_limit | Decimal | Tổng hạn mức tín dụng/ghi nợ |
| amount_used | Decimal | Số tiền đã sử dụng/chi tiêu |
| available_amount | Decimal | Số tiền còn lại có thể sử dụng |
| created_at | Timestamp | Thời điểm tạo bản ghi |
| created_by | String | Người tạo bản ghi |
| updated_at | Timestamp | Thời điểm cập nhật cuối |
| updated_by | String | Người cập nhật cuối cùng |

**Triết Lý Thiết Kế:**
- Giữ microservices đơn giản để tập trung vào tiêu chuẩn và khái niệm
- Tránh logic nghiệp vụ phức tạp thay đổi theo từng dự án
- Tập trung vào các mẫu kiến trúc và thực hành tốt nhất
- Sử dụng số điện thoại nhất quán trên tất cả microservices để tích hợp

## Các Lớp Entity

### Base Entity

Chứa các trường audit:
- `created_at`
- `created_by`
- `updated_at`
- `updated_by`

### Cards Entity

```java
@Entity
public class Cards extends BaseEntity {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long cardId;
    
    private String mobileNumber;
    private String cardNumber;
    private String cardType;
    private Integer totalLimit;
    private Integer amountUsed;
    private Integer availableAmount;
}
```

**Tính Năng Chính:**
- Tự động sinh khóa chính được xử lý bởi Spring Data JPA
- Kế thừa `BaseEntity` cho audit trail
- Tên trường khớp với tên cột (không cần `@Column`)

## Data Transfer Objects (DTOs)

### Cards DTO

```java
public class CardsDto {
    @Schema(description = "Số điện thoại khách hàng")
    @NotEmpty(message = "Số điện thoại không được để trống")
    @Pattern(regexp = "^[0-9]{10}$", message = "Số điện thoại phải có 10 chữ số")
    private String mobileNumber;
    
    @Schema(description = "Số thẻ")
    @NotEmpty(message = "Số thẻ không được để trống")
    @Pattern(regexp = "^[0-9]{12}$", message = "Số thẻ phải có 12 chữ số")
    private String cardNumber;
    
    @Schema(description = "Loại thẻ")
    @NotEmpty(message = "Loại thẻ không được để trống")
    private String cardType;
    
    @Schema(description = "Tổng hạn mức")
    @Positive(message = "Tổng hạn mức phải là số dương")
    private Integer totalLimit;
    
    @Schema(description = "Số tiền đã sử dụng")
    @PositiveOrZero(message = "Số tiền đã sử dụng phải là số dương hoặc 0")
    private Integer amountUsed;
    
    @Schema(description = "Số tiền còn lại")
    @PositiveOrZero(message = "Số tiền còn lại phải là số dương hoặc 0")
    private Integer availableAmount;
}
```

**Lợi Ích Của DTO:**
- Triển khai DTO pattern để tách biệt biểu diễn nội bộ và bên ngoài
- Bao gồm các annotation validation
- Tài liệu OpenAPI schema
- Các giá trị ví dụ cho tài liệu API tốt hơn

### Error Response DTO

Cấu trúc error response chuẩn cho xử lý lỗi nhất quán.

## Tầng Repository

### Cards Repository

```java
public interface CardsRepository extends JpaRepository<Cards, Long> {
    Optional<Cards> findByMobileNumber(String mobileNumber);
    Optional<Cards> findByCardNumber(String cardNumber);
}
```

**Các Phương Thức Tùy Chỉnh:**
- `findByMobileNumber` - Lấy thẻ theo số điện thoại khách hàng
- `findByCardNumber` - Lấy thẻ theo số thẻ

Cần thiết vì khóa chính là `cardId`, nhưng các thao tác nghiệp vụ sử dụng số điện thoại và số thẻ.

## Tầng Controller

### Cards Controller

**Cấu Hình:**
- `@RestController` - Đánh dấu là REST controller
- `@RequestMapping("/api")` - Đường dẫn cơ sở cho tất cả endpoints
- Trả về response dạng JSON
- Auto-wire `ICardService`

### Các API Endpoints

#### 1. Tạo Thẻ
```
POST /api/create?mobileNumber={mobileNumber}
Response: 201 Created
```
- Nhận số điện thoại làm query parameter
- Tạo thẻ mới cho khách hàng
- Trả về 201 khi thành công

#### 2. Lấy Chi Tiết Thẻ
```
GET /api/fetch?mobileNumber={mobileNumber}
Response: 200 OK
```
- Lấy chi tiết thẻ theo số điện thoại
- Trả về thông tin thẻ dạng JSON

#### 3. Cập Nhật Chi Tiết Thẻ
```
PUT /api/update
Body: CardsDto
Response: 200 OK hoặc 417 Expectation Failed
```
- Nhận Cards DTO trong request body
- Cập nhật thông tin thẻ
- Trả về 200 khi thành công, 417 khi thất bại

#### 4. Xóa Chi Tiết Thẻ
```
DELETE /api/delete?mobileNumber={mobileNumber}
Response: 200 OK hoặc 417 Expectation Failed
```
- Xóa thẻ theo số điện thoại
- Trả về 200 khi thành công, 417 khi thất bại

## Tầng Service

### Interface ICardService

Định nghĩa bốn phương thức trừu tượng:
- `createCard(String mobileNumber)`
- `fetchCard(String mobileNumber)`
- `updateCard(CardsDto cardsDto)`
- `deleteCard(String mobileNumber)`

### Triển Khai Card Service

#### Logic Tạo Thẻ

```java
public void createCard(String mobileNumber) {
    // Kiểm tra thẻ đã tồn tại chưa
    Optional<Cards> optionalCards = cardsRepository.findByMobileNumber(mobileNumber);
    if(optionalCards.isPresent()) {
        throw new CardAlreadyExistsException("Thẻ đã tồn tại với số điện thoại này");
    }
    
    // Tạo và lưu thẻ mới
    cardsRepository.save(createNewCard(mobileNumber));
}

private Cards createNewCard(String mobileNumber) {
    Cards newCard = new Cards();
    long randomCardNumber = 100000000000L + new Random().nextInt(900000000);
    newCard.setCardNumber(Long.toString(randomCardNumber));
    newCard.setMobileNumber(mobileNumber);
    newCard.setCardType("Credit Card");
    newCard.setTotalLimit(100_000); // Sử dụng underscore để dễ đọc
    newCard.setAmountUsed(0);
    newCard.setAvailableAmount(100_000);
    return newCard;
}
```

**Giá Trị Mặc Định Cho Thẻ Mới:**
- **Số Thẻ:** Số ngẫu nhiên 12 chữ số
- **Loại Thẻ:** Thẻ tín dụng (mặc định)
- **Tổng Hạn Mức:** 100,000 (100K)
- **Số Tiền Đã Sử Dụng:** 0
- **Số Tiền Còn Lại:** 100,000

**Lưu Ý:** Dấu gạch dưới trong các giá trị số (ví dụ: `100_000`) cải thiện khả năng đọc. Được giới thiệu trong Java 7/8, chúng bị loại bỏ trong quá trình biên dịch.

#### Logic Lấy Thẻ

```java
public CardsDto fetchCard(String mobileNumber) {
    Cards cards = cardsRepository.findByMobileNumber(mobileNumber)
        .orElseThrow(() -> new ResourceNotFoundException("Card", "mobileNumber", mobileNumber));
    
    return CardMapper.mapToCardsDto(cards, new CardsDto());
}
```

- Lấy thẻ theo số điện thoại
- Ném `ResourceNotFoundException` nếu không tìm thấy
- Chuyển đổi entity sang DTO bằng mapper

#### Logic Cập Nhật Thẻ

```java
public boolean updateCard(CardsDto cardsDto) {
    Cards cards = cardsRepository.findByCardNumber(cardsDto.getCardNumber())
        .orElseThrow(() -> new ResourceNotFoundException("Card", "cardNumber", cardsDto.getCardNumber()));
    
    CardMapper.mapToCards(cardsDto, cards);
    cardsRepository.save(cards);
    return true;
}
```

- Lấy theo số thẻ (định danh bất biến)
- Map DTO sang entity
- Phương thức Save thực hiện UPDATE (khóa chính đã tồn tại)
- Trả về true khi thành công

#### Logic Xóa Thẻ

```java
public boolean deleteCard(String mobileNumber) {
    Cards cards = cardsRepository.findByMobileNumber(mobileNumber)
        .orElseThrow(() -> new ResourceNotFoundException("Card", "mobileNumber", mobileNumber));
    
    cardsRepository.deleteById(cards.getCardId());
    return true;
}
```

- Lấy thẻ theo số điện thoại
- Xóa theo khóa chính (cardId)
- Phương án thay thế: Phương thức tùy chỉnh `deleteByMobileNumber` (được sử dụng trong Accounts microservice)
- Trả về true khi thành công

## Xử Lý Exception

### Các Exception Tùy Chỉnh

- **CardAlreadyExistsException** - Ném khi cố gắng tạo thẻ trùng lặp
- **ResourceNotFoundException** - Ném khi không tìm thấy thẻ

### Global Exception Handler

Xử lý:
- Lỗi validation đầu vào
- Runtime exceptions
- Business exceptions

Trả về error responses nhất quán với:
- Thông báo lỗi
- Mã trạng thái HTTP
- Timestamp
- Đường dẫn API

## Các Component Bổ Sung

### Card Mapper

Lớp tiện ích với các phương thức static:
- `mapToCardsDto(Cards cards, CardsDto cardsDto)` - Entity sang DTO
- `mapToCards(CardsDto cardsDto, Cards cards)` - DTO sang Entity

### Constants File

Chứa các hằng số ứng dụng.

### Audit Aware Implementation

Xử lý việc điền các trường audit cho `created_by` và `updated_by`.

## Kiểm Thử Với Postman

### Khởi Động Application

1. Chạy lớp main `CardsApplication` ở chế độ debug
2. Application khởi động trên cổng 9000
3. Xác minh logs khởi động xác nhận cổng 9000

### Các Kịch Bản Test

#### 1. Tạo Thẻ

```
POST http://localhost:9000/api/create?mobileNumber=1234567890
Response: 201 - Tạo thẻ thành công
```

#### 2. Lấy Chi Tiết Thẻ

```
GET http://localhost:9000/api/fetch?mobileNumber=1234567890

Response:
{
  "mobileNumber": "1234567890",
  "cardNumber": "123456789012",
  "cardType": "Credit Card",
  "totalLimit": 100000,
  "amountUsed": 0,
  "availableAmount": 100000
}
```

#### 3. Cập Nhật Chi Tiết Thẻ

```
PUT http://localhost:9000/api/update

Body:
{
  "mobileNumber": "1234567890",
  "cardNumber": "123456789012",
  "cardType": "Debit Card",
  "totalLimit": 100000,
  "amountUsed": 10000,
  "availableAmount": 90000
}

Response: 200 - Cập nhật thẻ thành công
```

**Sau Khi Cập Nhật - Lấy Lại:**
- Loại Thẻ: Đã đổi thành "Debit Card"
- Số Tiền Đã Sử Dụng: 10,000
- Số Tiền Còn Lại: 90,000

#### 4. Xóa Chi Tiết Thẻ

```
DELETE http://localhost:9000/api/delete?mobileNumber=1234567890
Response: 200 - Xóa thẻ thành công
```

**Xác Minh:**
- Cố gắng lấy sau khi xóa trả về 404 Not Found

### Các Test Case Tiêu Cực

#### Lỗi Validation

**Test Đầu Vào Không Hợp Lệ:**
```json
{
  "mobileNumber": "1234567890",
  "cardNumber": "1234567890123", // 13 chữ số - không hợp lệ
  "cardType": "Debit Card",
  "totalLimit": -100000,          // số âm - không hợp lệ
  "amountUsed": -10000,           // số âm - không hợp lệ
  "availableAmount": -90000       // số âm - không hợp lệ
}
```

**Kết Quả:** Trả về nhiều lỗi validation

#### Validation Số Điện Thoại

**Số điện thoại 9 chữ số:**
```
GET http://localhost:9000/api/fetch?mobileNumber=123456789
Response: 400 - Lỗi validation
```

#### Resource Not Found

**Số điện thoại không tồn tại:**
```
GET http://localhost:9000/api/fetch?mobileNumber=9999999999
Response: 404 - Không tìm thấy thẻ với dữ liệu đầu vào
```

## Tài Liệu Swagger UI

### Truy Cập Swagger UI

```
URL: http://localhost:9000/swagger-ui/index.html
```

**Tài Liệu Có Sẵn:**
- Bốn API endpoints (Create, Fetch, Update, Delete)
- Cards schema với mô tả trường
- Error Response schema
- Cấu trúc Response DTO
- Chức năng try-it-out để test

### Tài Liệu Schema

Tất cả DTOs bao gồm:
- Mô tả trường
- Quy tắc validation
- Giá trị ví dụ
- Kiểu dữ liệu

## Những Lưu Ý Quan Trọng

### 1. Thiết Lập Microservices Hoàn Chỉnh

Cả ba microservices (Accounts, Loans, Cards) đã hoàn thiện với:
- ✅ Cấu trúc dự án chuẩn
- ✅ Triển khai logic nghiệp vụ
- ✅ Xử lý exception
- ✅ Input validation
- ✅ Tài liệu OpenAPI
- ✅ Tích hợp H2 database
- ✅ Các thao tác CRUD

### 2. Khuyến Nghị Học Tập

**Dành Thời Gian:**
- Dành 4-8 giờ hoặc cả ngày để hiểu code
- Xem xét từng dòng code trong các microservices này
- Thiết lập tất cả microservices trong IDE local của bạn
- Test tất cả APIs bằng Postman collection được cung cấp
- Xác minh mọi thứ hoạt động với H2 database

### 3. Nền Tảng Cho Các Khái Niệm Tương Lai

Ba microservices này là **bước đệm** cho tất cả các khái niệm trong tương lai của khóa học:
- Docker containerization
- Kubernetes deployment
- Service discovery
- API Gateway
- Circuit breakers
- Distributed tracing
- Và nhiều hơn nữa...

### 4. Lợi Ích Của Chiến Lược Lặp Lại

Bằng cách triển khai ba microservices tương tự:
- Mỗi khái niệm được thực hành ba lần
- Các mẫu trở thành trí nhớ cơ bắp
- Tiêu chuẩn được củng cố
- Tự tin tăng lên với sự lặp lại
- Học tập tiềm thức xảy ra

### 5. Tính Nhất Quán Số Điện Thoại

**Quan Trọng:** Sử dụng cùng một số điện thoại trên cả ba microservices cho:
- Kiểm thử tích hợp
- Lấy response kết hợp
- Các thao tác xuyên service
- Demo Spring Cloud trong tương lai

## Triết Lý Thiết Kế

### Tập Trung Vào Sự Đơn Giản

Các microservices được cố ý giữ đơn giản để:
- **Tập Trung Vào Tiêu Chuẩn** - Học các mẫu kiến trúc
- **Tập Trung Vào Khái Niệm** - Hiểu công nghệ microservices
- **Tập Trung Vào Phương Pháp** - Thành thạo các thực hành phát triển
- **Tránh Phức Tạp** - Logic nghiệp vụ thay đổi theo dự án
- **Tối Đa Hóa Học Tập** - Các mẫu chung có lợi cho tất cả developers

### Không Phải Về Logic Nghiệp Vụ

Logic nghiệp vụ là:
- Khác nhau cho mỗi dự án
- Không áp dụng được phổ quát
- Tốn thời gian để triển khai
- Không phải mục tiêu học tập chính

Thay vào đó, tập trung vào:
- Các mẫu kiến trúc
- Tiêu chuẩn code
- Thực hành tốt nhất
- Khả năng của framework
- Kỹ thuật tích hợp

## Tóm Tắt

Cards microservice hoàn thiện bộ ba của chúng ta, minh họa:

1. **Kiến Trúc Nhất Quán** trên cả ba services
2. **Các Mẫu Chuẩn** - Tầng Repository, Service, Controller
3. **DTO Pattern** - Tách biệt mối quan tâm
4. **Validation** - Input validation với annotations
5. **Exception Handling** - Global error handling
6. **Documentation** - Tích hợp OpenAPI/Swagger
7. **Database Integration** - H2 với Spring Data JPA
8. **RESTful APIs** - Các phương thức HTTP và mã trạng thái phù hợp

### Thành Tựu Chính

✅ Ba microservices hoạt động đầy đủ  
✅ Tiêu chuẩn code nhất quán  
✅ Xử lý exception toàn diện  
✅ Input validation trên tất cả endpoints  
✅ Tài liệu API với Swagger  
✅ Sẵn sàng cho Docker/Kubernetes  
✅ Nền tảng cho các khái niệm nâng cao  

## Bước Tiếp Theo

1. **Nghỉ ngơi xứng đáng** - Bạn đã làm tốt lắm!
2. **Xem lại code** - Đảm bảo hiểu hoàn toàn
3. **Test kỹ lưỡng** - Xác thực tất cả kịch bản
4. **Chuẩn bị cho phần tiếp theo** - Các khái niệm microservices nâng cao đang chờ đợi

Hành trình tiếp tục ở phần tiếp theo, nơi các microservices này sẽ được nâng cao với các tính năng cấp doanh nghiệp!

---

**Chúc mừng bạn đã hoàn thành các microservices nền tảng! 🎉**