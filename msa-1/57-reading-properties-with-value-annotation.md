# Đọc Thuộc Tính với Annotation @Value trong Spring Boot

## Tổng Quan

Bài giảng này trình bày cách đọc các thuộc tính từ file cấu hình trong microservices Spring Boot bằng cách sử dụng annotation `@Value`. Chúng ta sẽ cập nhật các microservices để định nghĩa thuộc tính trong `application.yml` và đọc chúng trong code Java.

## Thiết Lập Dự Án

### Tạo Cấu Trúc Dự Án

1. Tạo cấu trúc thư mục mới:
   - `section6/v1-springboot/` - Chứa phiên bản 1 của microservices sử dụng các phương pháp cơ bản của Spring Boot
   - Sao chép các microservices từ section 4: accounts, cards, và loans

2. Mở dự án trong IntelliJ IDEA:
   - Nhấp vào nút **Open**
   - Điều hướng đến vị trí workspace: `microservices/section6/v1-springboot`
   - Chọn thư mục cha và nhấp **Open**
   - Nhấp **Load** để phát hiện tất cả các dự án Maven

## Chuyển Sang Google Jib để Tạo Docker Images

Vì chúng ta đã quyết định sử dụng Google Jib để tạo Docker images, cần cập nhật tất cả microservices:

### Microservice Cards (Đã Sử Dụng Jib)

1. Mở `pom.xml`
2. Điều hướng đến cấu hình Google Jib Maven plugin
3. Đổi tên image thành `s6` (cho section 6)
4. Load các thay đổi Maven
5. Sao chép chi tiết plugin

### Microservice Accounts

1. Xóa `Dockerfile` (không còn cần thiết)
2. Mở `pom.xml`
3. Xóa Spring Boot Maven plugin
4. Thay thế bằng Google Jib Maven plugin
5. Load các thay đổi Maven

### Microservice Loans

1. Mở `pom.xml`
2. Tìm Spring Boot Maven plugin
3. Thay thế bằng Google Jib Maven plugin
4. Load các thay đổi Maven

> **Lưu ý**: `project.artifactId` sẽ tự động tạo tên Docker image khác nhau cho mỗi microservice.

## Định Nghĩa Thuộc Tính trong application.yml

Trong microservice **accounts**, mở `application.yml` và thêm:

```yaml
build:
  version: 1.0
```

Điều này tạo một thuộc tính với key `build.version` và giá trị `1.0`.

## Đọc Thuộc Tính với Annotation @Value

### Bước 1: Tạo Field trong Controller

Trong `AccountsController.java`, thêm một field để chứa giá trị thuộc tính:

```java
@Value("${build.version}")
private String buildVersion;
```

**Giải Thích Cú Pháp**:
- Sử dụng annotation `@Value`
- Tuân theo cú pháp Spring Expression Language (SpEL): `"${property.key}"`
- Property key: `build.version`

### Bước 2: Tạo REST API Endpoint

Thêm một phương thức mới để xuất thông tin build version:

```java
@GetMapping("/build-info")
@Operation(
    summary = "Lấy Thông Tin Build",
    description = "Lấy thông tin build được triển khai vào accounts microservice"
)
@ApiResponses({
    @ApiResponse(
        responseCode = "200",
        description = "HTTP Status OK"
    ),
    @ApiResponse(
        responseCode = "500",
        description = "HTTP Status Internal Server Error",
        content = @Content(
            schema = @Schema(implementation = ErrorResponseDto.class)
        )
    )
})
public ResponseEntity<String> getBuildInfo() {
    return ResponseEntity
            .status(HttpStatus.OK)
            .body(buildVersion);
}
```

## Sửa Lỗi Constructor Autowiring

### Vấn Đề

Khi sử dụng `@AllArgsConstructor`, Lombok tạo constructor với TẤT CẢ các fields, bao gồm `buildVersion`. Spring cố gắng tìm một bean kiểu `String`, nhưng không tồn tại.

### Giải Pháp

1. Xóa annotation `@AllArgsConstructor`
2. Tạo constructor tùy chỉnh cho dependency injection:

```java
private final IAccountService iAccountService;

@Value("${build.version}")
private String buildVersion;

public AccountsController(IAccountService iAccountService) {
    this.iAccountService = iAccountService;
}
```

**Best Practices**:
- Sử dụng từ khóa `final` cho các dependencies được inject
- Annotation `@Autowired` là tùy chọn khi chỉ có một constructor
- Đây là phương pháp được khuyến nghị nhất cho constructor-based dependency injection

## Kiểm Thử API

1. Khởi động accounts microservice ở chế độ debug
2. Ứng dụng khởi động tại cổng 8080
3. Kiểm thử bằng Postman:
   - **Method**: GET
   - **URL**: `http://localhost:8080/api/build-info`
   - **Response**: `1.0`

> **Mẹo**: Import Postman collection từ GitHub repository để truy cập tất cả các API requests đã được cấu hình sẵn.

## Hạn Chế của Phương Pháp @Value Annotation

### Khi Nào Nên Sử Dụng

- **Được Khuyến Nghị**: Chỉ cho 1-2 thuộc tính
- Nhu cầu inject thuộc tính đơn giản

### Nhược Điểm

1. **Không Mở Rộng Được**: Tạo 100 fields cho 100 thuộc tính là không khả thi
2. **Tên Thuộc Tính Hardcoded**: Property keys được hardcode trong annotations
3. **Vấn Đề Bảo Trì**: Khó quản lý trong microservices lớn với nhiều thuộc tính
4. **Không Type Safe**: Giới hạn validation và chuyển đổi kiểu

### Giải Pháp Tốt Hơn

Cho nhiều thuộc tính hoặc cấu hình phức tạp, sử dụng:
- Annotation `@ConfigurationProperties` (sẽ đề cập trong bài giảng tiếp theo)
- Cung cấp cấu hình type-safe binding
- Nhóm các thuộc tính liên quan lại với nhau
- Hỗ trợ validation

## Tóm Tắt

- Thuộc tính có thể được định nghĩa trong `application.yml` hoặc `application.properties`
- Sử dụng `@Value("${property.key}")` để inject giá trị thuộc tính
- Constructor-based dependency injection là phương pháp được khuyến nghị
- Phương pháp này hoạt động tốt cho các tình huống đơn giản với ít thuộc tính
- Cho cấu hình phức tạp, sử dụng `@ConfigurationProperties` thay thế

## Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ khám phá phương pháp thứ hai sử dụng `@ConfigurationProperties` để quản lý thuộc tính mạnh mẽ hơn trong microservices.