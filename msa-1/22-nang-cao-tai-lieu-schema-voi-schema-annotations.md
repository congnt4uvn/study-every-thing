# Nâng Cao Tài Liệu Schema với @Schema Annotations

## Tổng Quan

Trong hướng dẫn này, chúng ta sẽ học cách nâng cao tài liệu OpenAPI cho các đối tượng schema bằng cách sử dụng annotation `@Schema` trong microservices Spring Boot. Điều này cho phép chúng ta cung cấp tên thân thiện với nghiệp vụ, mô tả và các giá trị ví dụ cho các DTO và trường của chúng.

## Tại Sao Cần Nâng Cao Tài Liệu Schema?

- **Tên Thân Thiện với Nghiệp Vụ**: Thay thế tên class kỹ thuật bằng các thuật ngữ nghiệp vụ dễ hiểu hơn
- **Mô Tả Rõ Ràng**: Giải thích ý nghĩa của mỗi schema và trường
- **Giá Trị Ví Dụ**: Cung cấp dữ liệu mẫu giúp người dùng API hiểu định dạng mong đợi
- **Tài Liệu Chuyên Nghiệp**: Tạo tài liệu API toàn diện, dễ hiểu

## Nâng Cao CustomerDto

### Tài Liệu Cấp Class

Thêm annotation `@Schema` ở cấp class để cung cấp thông tin tổng quan:

```java
@Schema(
    name = "Customer",
    description = "Schema để lưu thông tin khách hàng và tài khoản"
)
public class CustomerDto {
    // các trường...
}
```

### Tài Liệu Cấp Trường

Thêm annotation `@Schema` cho từng trường:

```java
@Schema(
    description = "Tên của khách hàng",
    example = "Nguyễn Văn A"
)
private String name;

@Schema(
    description = "Địa chỉ email của khách hàng",
    example = "nguyenvana@example.com"
)
private String email;

@Schema(
    description = "Số điện thoại di động của khách hàng",
    example = "+84901234567"
)
private String mobileNumber;

@Schema(
    description = "Chi tiết tài khoản của khách hàng"
)
private AccountsDto accounts;
```

## Nâng Cao AccountsDto

### Cấu Hình Cấp Class

```java
@Schema(
    name = "Accounts",
    description = "Schema để lưu thông tin tài khoản"
)
public class AccountsDto {
    // các trường...
}
```

### Annotations Cấp Trường

```java
@Schema(
    description = "Số tài khoản của Easy Bank"
)
private Long accountNumber;

@Schema(
    description = "Loại tài khoản của Easy Bank",
    example = "Tiết kiệm"
)
private String accountType;

@Schema(
    description = "Địa chỉ chi nhánh của Easy Bank",
    example = "123 Hà Nội"
)
private String branchAddress;
```

**Lưu ý**: Tham số `example` là tùy chọn. Sử dụng nó ở những nơi mang lại giá trị cho người dùng API.

## Nâng Cao ResponseDto

### Phản Hồi Thành Công Chuẩn

```java
@Schema(
    name = "Response",
    description = "Schema để lưu thông tin phản hồi thành công"
)
public class ResponseDto {
    
    @Schema(
        description = "Mã trạng thái trong phản hồi",
        example = "200"
    )
    private String statusCode;
    
    @Schema(
        description = "Thông báo trạng thái trong phản hồi",
        example = "Yêu cầu được xử lý thành công"
    )
    private String statusMessage;
}
```

## Nâng Cao ErrorResponseDto

### Schema Phản Hồi Lỗi

```java
@Schema(
    name = "ErrorResponse",
    description = "Schema để lưu thông tin phản hồi lỗi"
)
public class ErrorResponseDto {
    
    @Schema(
        description = "Đường dẫn API được gọi bởi client"
    )
    private String apiPath;
    
    @Schema(
        description = "Mã lỗi đại diện cho lỗi đã xảy ra"
    )
    private String errorCode;
    
    @Schema(
        description = "Thông báo lỗi đại diện cho lỗi đã xảy ra"
    )
    private String errorMessage;
    
    @Schema(
        description = "Thời gian xảy ra lỗi"
    )
    private LocalDateTime errorTime;
}
```

**Lưu ý**: Có thể bỏ qua các giá trị ví dụ cho phản hồi lỗi vì chúng thay đổi theo từng tình huống.

## Tài Liệu Hóa Phản Hồi Lỗi trong Các API Operation

### Vấn Đề

`ErrorResponseDto` sẽ không tự động xuất hiện trong Swagger UI vì OpenAPI không thể quét logic `GlobalExceptionHandler`.

### Giải Pháp

Thêm schema phản hồi lỗi vào các API operation bằng cách sử dụng `@ApiResponse`:

```java
@ApiResponse(
    responseCode = "500",
    description = "Lỗi Máy Chủ Nội Bộ",
    content = @Content(
        schema = @Schema(implementation = ErrorResponseDto.class)
    )
)
```

### Ví Dụ Hoàn Chỉnh

```java
@Operation(
    summary = "REST API Cập Nhật Tài Khoản",
    description = "REST API để cập nhật chi tiết tài khoản"
)
@ApiResponse(
    responseCode = "200",
    description = "HTTP Status OK"
)
@ApiResponse(
    responseCode = "500",
    description = "Lỗi Máy Chủ Nội Bộ",
    content = @Content(
        schema = @Schema(implementation = ErrorResponseDto.class)
    )
)
@PutMapping("/update")
public ResponseEntity<ResponseDto> updateAccount(@RequestBody AccountsDto accountsDto) {
    // triển khai
}
```

## Xác Minh Tài Liệu

### Các Bước Xác Minh

1. **Lưu tất cả thay đổi** trong các class DTO
2. **Build dự án** để tạo lại OpenAPI specifications
3. **Truy cập Swagger UI** (thường tại `http://localhost:8080/swagger-ui.html`)
4. **Kiểm tra các mục sau**:
   - Các đối tượng schema có tên thân thiện với nghiệp vụ
   - Mỗi trường có thông tin mô tả
   - Các giá trị ví dụ xuất hiện trong tài liệu
   - Các schema phản hồi lỗi hiển thị được

### Những Gì Bạn Nên Thấy

- **Phần Schemas**: Tất cả DTO được liệt kê với tên tùy chỉnh (Customer, Accounts, Response, ErrorResponse)
- **Mô Tả Trường**: Mỗi trường hiển thị mục đích và giá trị ví dụ
- **API Operations**: Request/response body ví dụ được điền đầy đủ
- **Phản Hồi Lỗi**: Phản hồi lỗi 500 hiển thị cấu trúc schema ErrorResponse

## Thực Hành Tốt Nhất

1. **Sử Dụng Tên Thân Thiện với Nghiệp Vụ**: Đặt tên schema dễ hiểu cho các bên liên quan phi kỹ thuật
2. **Cung Cấp Mô Tả Rõ Ràng**: Giải thích mục đích của mỗi schema và trường
3. **Bao Gồm Các Ví Dụ Liên Quan**: Thêm giá trị ví dụ ở những nơi giúp làm rõ định dạng mong đợi
4. **Tài Liệu Hóa Phản Hồi Lỗi**: Định nghĩa rõ ràng các schema lỗi trong API operations
5. **Giữ Ví Dụ Thực Tế**: Sử dụng các ví dụ đại diện cho trường hợp sử dụng thực tế
6. **Nhất Quán**: Tuân theo cùng một mẫu tài liệu trên tất cả các DTO

## Lợi Ích

- **Tài Liệu Chuyên Nghiệp**: Tạo tài liệu API toàn diện, dễ hiểu
- **Trải Nghiệm Developer Tốt Hơn**: Người dùng API có thể nhanh chóng hiểu cách sử dụng API
- **Giảm Chi Phí Hỗ Trợ**: Tài liệu rõ ràng giảm thiểu câu hỏi và vấn đề tích hợp
- **Tuân Thủ Tiêu Chuẩn**: Tuân theo các thực hành tốt nhất của OpenAPI Specification

## Tóm Tắt

Bằng cách sử dụng annotation `@Schema` ở cả cấp class và cấp trường, chúng ta có thể nâng cao đáng kể tài liệu REST API. Điều này bao gồm:

- Tên thân thiện với nghiệp vụ tùy chỉnh cho các đối tượng schema
- Thông tin mô tả cho từng trường
- Giá trị ví dụ để hướng dẫn người dùng API
- Tài liệu hóa đúng các phản hồi lỗi

Những cải tiến này làm cho các API microservices của bạn chuyên nghiệp hơn và dễ sử dụng hơn.