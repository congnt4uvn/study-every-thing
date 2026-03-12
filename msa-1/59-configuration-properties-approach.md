# Đọc Nhiều Configuration Properties với @ConfigurationProperties

## Tổng Quan

Bài giảng này trình bày cách tiếp cận thứ ba để đọc các thuộc tính cấu hình trong Spring Boot microservices sử dụng annotation `@ConfigurationProperties`. Cách tiếp cận này cho phép đọc nhiều thuộc tính cùng lúc bằng một POJO class duy nhất, khắc phục các hạn chế của annotation `@Value` và interface `Environment`.

## Hạn Chế của Các Cách Tiếp Cận Trước

Hai cách tiếp cận đầu tiên (annotation `@Value` và interface `Environment`) có một số hạn chế:

1. **Hardcode tên khóa thuộc tính** trong code Java
2. **Chỉ đọc được một thuộc tính tại một thời điểm**
3. **Trùng lặp code** khi cần sử dụng cùng các thuộc tính ở nhiều controller class
4. **Khó bảo trì** khi xử lý nhiều thuộc tính

## Cách Tiếp Cận @ConfigurationProperties

### Bước 1: Định Nghĩa Properties với Prefix Chung

Trong file `application.yml`, định nghĩa các thuộc tính với prefix chung:

```yaml
accounts:
  message: "Chào mừng đến với Accounts Microservice"
  contactDetails:
    name: "Nguyễn Văn A"
    email: "nguyenvana@example.com"
  onCallSupport:
    - "123-456-7890"
    - "098-765-4321"
```

**Các Điểm Quan Trọng:**
- Tất cả thuộc tính chia sẻ prefix chung (`accounts`)
- Thuộc tính có thể là string đơn giản, map, hoặc list
- Hỗ trợ các thuộc tính lồng nhau

### Bước 2: Tạo POJO Class

Tạo DTO class để đại diện cho các thuộc tính cấu hình. Bạn có thể sử dụng POJO class truyền thống hoặc Java Record (giới thiệu trong Java 17).

#### Sử Dụng Java Record (Khuyến Nghị)

```java
public record AccountsContactInfoDto(
    String message,
    Map<String, String> contactDetails,
    List<String> onCallSupport
) {}
```

**Lợi Ích của Java Record:**
- Hoạt động như một data carrier bất biến
- Tự động tạo constructor, getter, `equals()`, `hashCode()`, và `toString()`
- Không có phương thức setter (các field là final)
- Code sạch hơn và ngắn gọn hơn

### Bước 3: Đánh Dấu với @ConfigurationProperties

Thêm annotation `@ConfigurationProperties` vào DTO class:

```java
@ConfigurationProperties(prefix = "accounts")
public record AccountsContactInfoDto(
    String message,
    Map<String, String> contactDetails,
    List<String> onCallSupport
) {}
```

**Quan Trọng:** Giá trị prefix phải khớp với prefix được định nghĩa trong `application.yml`.

### Bước 4: Kích Hoạt Configuration Properties

Trong Spring Boot main class, kích hoạt configuration properties:

```java
@SpringBootApplication
@EnableConfigurationProperties(AccountsContactInfoDto.class)
public class AccountsApplication {
    public static void main(String[] args) {
        SpringApplication.run(AccountsApplication.class, args);
    }
}
```

### Bước 5: Sử Dụng Configuration trong Controller

Inject và sử dụng configuration DTO trong controller:

```java
@RestController
@RequestMapping("/api")
public class AccountsController {
    
    @Autowired
    private AccountsContactInfoDto accountsContactInfoDto;
    
    @GetMapping("/contact-info")
    @Operation(
        summary = "Lấy Thông Tin Liên Hệ",
        description = "Thông tin liên hệ có thể được sử dụng trong trường hợp có vấn đề"
    )
    public AccountsContactInfoDto getContactInfo() {
        return accountsContactInfoDto;
    }
}
```

## Cách Hoạt Động

1. Trong quá trình khởi động ứng dụng, Spring Boot đọc tất cả các thuộc tính với prefix `accounts`
2. Spring tạo bean của `AccountsContactInfoDto` và ánh xạ các giá trị thuộc tính vào các field
3. Bean có sẵn để dependency injection trong toàn bộ ứng dụng
4. Tên field trong DTO class phải khớp với tên thuộc tính trong `application.yml`
5. Kiểu dữ liệu phải tương thích (String, Map<String, String>, List<String>, v.v.)

## Kiểm Thử API

Sau khi triển khai, bạn có thể kiểm thử API bằng Postman hoặc bất kỳ HTTP client nào:

**Request:**
```
GET http://localhost:8080/api/contact-info
```

**Response:**
```json
{
  "message": "Chào mừng đến với Accounts Microservice",
  "contactDetails": {
    "name": "Nguyễn Văn A",
    "email": "nguyenvana@example.com"
  },
  "onCallSupport": [
    "123-456-7890",
    "098-765-4321"
  ]
}
```

## Ưu Điểm của @ConfigurationProperties

1. **Cấu hình type-safe** - Xác thực kiểu thuộc tính tại thời điểm compile
2. **Single source of truth** - Một DTO class cho tất cả các thuộc tính liên quan
3. **Không hardcode** - Tên thuộc tính không được hardcode trong business logic
4. **Tái sử dụng** - Inject cùng một DTO ở bất kỳ đâu trong ứng dụng
5. **Khả năng mở rộng** - Dễ dàng xử lý hàng trăm thuộc tính
6. **Được khuyến nghị bởi Spring Team** - Best practice chính thức

## So Sánh với Các Cách Tiếp Cận Khác

| Cách Tiếp Cận | Thuộc Tính Đơn | Nhiều Thuộc Tính | Type Safety | Tái Sử Dụng | Khuyến Nghị |
|---------------|----------------|------------------|-------------|-------------|-------------|
| @Value | ✓ | ✗ | ✗ | ✗ | ✗ |
| Environment | ✓ | ✗ | ✗ | Hạn chế | Chỉ cho biến môi trường |
| @ConfigurationProperties | ✓ | ✓ | ✓ | ✓ | ✓ |

## Best Practices

1. **Sử dụng prefix có ý nghĩa** phản ánh tên microservice hoặc tính năng của bạn
2. **Khớp chính xác tên field** với tên thuộc tính trong file cấu hình
3. **Sử dụng kiểu dữ liệu phù hợp** (String, Map, List) dựa trên cấu trúc thuộc tính
4. **Cân nhắc sử dụng Java Records** cho các configuration DTO bất biến
5. **Sử dụng @ConfigurationProperties cho application properties**, Environment interface cho biến môi trường

## Các Bước Tiếp Theo

Cách tiếp cận này hoạt động tốt cho một môi trường duy nhất, nhưng nếu bạn cần các giá trị thuộc tính khác nhau cho các môi trường khác nhau (dev, QA, production) thì sao?

Trong bài giảng tiếp theo, chúng ta sẽ khám phá các tính năng nâng cao của Spring Boot để quản lý cấu hình đặc thù cho từng môi trường bằng cách sử dụng **Spring Profiles**.

## Tóm Tắt

- `@ConfigurationProperties` là cách tiếp cận trưởng thành và được khuyến nghị nhất để đọc các thuộc tính cấu hình
- Nó loại bỏ việc trùng lặp code và hardcode tên thuộc tính
- Java Records cung cấp cách clean để tạo các configuration DTO bất biến
- Các thuộc tính được tự động ánh xạ vào các POJO field trong quá trình khởi động ứng dụng
- Cách tiếp cận này mở rộng tốt cho các ứng dụng có nhiều thuộc tính cấu hình