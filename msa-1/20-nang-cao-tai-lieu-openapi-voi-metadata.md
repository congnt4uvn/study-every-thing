# Nâng Cao Tài Liệu OpenAPI Với Metadata

## Tổng Quan

Trong bài học này, chúng ta sẽ học cách nâng cao tài liệu REST API bằng cách thêm thông tin metadata toàn diện sử dụng các annotation OpenAPI trong Spring Boot. Chúng ta sẽ cải thiện phần đầu của tài liệu Swagger UI để bao gồm tiêu đề, mô tả, thông tin liên hệ, chi tiết giấy phép và các liên kết tài liệu bên ngoài.

## Vấn Đề

Hiện tại, phần đầu của tài liệu REST API thiếu các thông tin quan trọng:
- Mục đích của các REST API
- Tóm tắt và mô tả
- Thông tin liên hệ
- Thông tin giấy phép

Điều này khiến người sử dụng API khó hiểu về ngữ cảnh và hướng dẫn sử dụng API của chúng ta.

## Giải Pháp: Sử Dụng Các Annotation OpenAPI

### Bước 1: Định Vị Class Chính Spring Boot

Điều hướng đến class chính Spring Boot của bạn - trong ví dụ này là `AccountsApplication`. Đây là nơi chúng ta sẽ thêm các annotation metadata OpenAPI.

### Bước 2: Thêm Annotation @OpenApiDefinition

Thêm annotation `@OpenApiDefinition` vào class chính của bạn để cung cấp các chi tiết định nghĩa với OpenAPI.

```java
@OpenApiDefinition(
    info = @Info(
        title = "Accounts Microservice REST API Documentation",
        description = "EasyBank Accounts Microservice REST API Documentation",
        version = "v1",
        contact = @Contact(
            name = "Tên của bạn",
            email = "email.cua.ban@example.com",
            url = "https://www.eazybytes.com"
        ),
        license = @License(
            name = "Apache 2.0",
            url = "https://www.eazybytes.com"
        )
    ),
    externalDocs = @ExternalDocumentation(
        description = "EasyBank Accounts Microservice REST API Documentation",
        url = "https://www.eazybytes.com/swagger-ui.html"
    )
)
@SpringBootApplication
public class AccountsApplication {
    // Mã nguồn ứng dụng
}
```

## Giải Thích Các Tham Số Annotation

### Annotation @Info

Annotation `@Info` chấp nhận các tham số sau:

1. **title**: Tóm tắt ngắn gọn về các REST API của bạn
   - Ví dụ: "Accounts Microservice REST API Documentation"

2. **description**: Mô tả chi tiết về các REST API của bạn
   - Ví dụ: "EasyBank Accounts Microservice REST API Documentation"

3. **version**: Phiên bản của API
   - Ví dụ: "v1", "v2", "v3" dựa trên yêu cầu của bạn

4. **contact**: Thông tin liên hệ để được hỗ trợ

5. **license**: Chi tiết giấy phép cho API của bạn

### Annotation @Contact

Annotation `@Contact` bao gồm:
- **name**: Tên của người hoặc nhóm để liên hệ
- **email**: Email liên hệ (có thể là email cá nhân hoặc nhóm)
- **url**: URL trang web để liên hệ

### Annotation @License

Annotation `@License` chỉ định:
- **name**: Tên giấy phép (ví dụ: "Apache 2.0")
- **url**: URL nơi mọi người có thể đọc thêm về chi tiết giấy phép

### Annotation @ExternalDocumentation

Cung cấp các tài nguyên tài liệu bổ sung:
- **description**: Mô tả về tài liệu bên ngoài
- **url**: URL nơi mọi người có thể truy cập tài liệu chi tiết

## Các Tùy Chọn Cấu Hình Bổ Sung

Đặc tả OpenAPI hỗ trợ nhiều tùy chọn cấu hình nâng cao khác:

- **Chi tiết bảo mật**: Định nghĩa các schema xác thực và phân quyền
- **Chi tiết máy chủ**: Chỉ định các URL nơi REST API được lưu trữ
- **Tags**: Tổ chức các API thành các nhóm logic
- **Extensions**: Thêm các thuộc tính tùy chỉnh

Để có phạm vi bao quát toàn diện về đặc tả OpenAPI và hệ sinh thái Swagger, hãy cân nhắc các khóa đào tạo chuyên biệt.

## Kiểm Tra Các Thay Đổi

1. Lưu các thay đổi vào class chính của bạn
2. Build ứng dụng
3. Refresh trang Swagger UI HTML
4. Xác minh rằng phần đầu bây giờ hiển thị:
   - Tiêu đề và mô tả
   - Chi tiết liên hệ (email, website)
   - Thông tin giấy phép
   - Các liên kết tài liệu bên ngoài

## Lưu Ý Quan Trọng: Best Practices Về Cấu Trúc Package

### Cách Tiếp Cận Được Khuyến Nghị

Class chính Spring Boot của bạn nên ở trong package gốc, với tất cả các package khác là sub-package:

```
com.eazybytes.accounts (Class chính: AccountsApplication)
├── controller
├── service
├── repository
└── entity
```

Đây là **cách tiếp cận được khuyến nghị nhất** vì Spring Boot tự động quét tất cả các sub-package.

### Cách Tiếp Cận Thay Thế (Không Được Khuyến Nghị)

Nếu bạn tạo các package bên ngoài cấu trúc package chính, bạn **phải** chỉ định rõ ràng các vị trí component sử dụng các annotation này:

```java
@ComponentScan(basePackages = {
    "com.eazybytes.controller",
    "com.eazybytes.service"
})
@EnableJpaRepositories(basePackages = "com.eazybytes.repository")
@EntityScan(basePackages = "com.eazybytes.entity")
@SpringBootApplication
public class AccountsApplication {
    // Mã nguồn ứng dụng
}
```

**Quan trọng**: Nếu không có các annotation này, Spring Boot sẽ không phát hiện các component của bạn, và ứng dụng sẽ không hoạt động chính xác.

## Các Bước Tiếp Theo

Trong bài học tiếp theo, chúng ta sẽ nâng cao tài liệu ở cấp độ controller bằng cách:
- Loại bỏ thông tin kỹ thuật như tên class
- Ẩn chi tiết hostname
- Cung cấp dữ liệu ví dụ cho các request và response API
- Làm cho tài liệu thân thiện hơn với người dùng

## Những Điểm Chính

1. Sử dụng `@OpenApiDefinition` để thêm metadata toàn diện vào tài liệu API của bạn
2. Bao gồm thông tin title, description, version, contact và license
3. Cung cấp các liên kết tài liệu bên ngoài cho các tài nguyên bổ sung
4. Tuân theo các best practices về cấu trúc package Spring Boot
5. Luôn duy trì các sub-package dưới package ứng dụng chính
6. Tài liệu được nâng cao cải thiện khả năng sử dụng API và trải nghiệm developer

## Kết Luận

Bằng cách thêm metadata phù hợp vào tài liệu OpenAPI của bạn, bạn làm cho người sử dụng API dễ dàng hiểu mục đích, thông tin liên hệ và giấy phép của các REST API của bạn. Cách tiếp cận tài liệu chuyên nghiệp này là điều cần thiết cho các microservice sẵn sàng cho production.