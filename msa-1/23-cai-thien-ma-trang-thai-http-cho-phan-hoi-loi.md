# Cải Thiện Mã Trạng Thái HTTP Cho Phản Hồi Lỗi

## Tổng Quan
Trong bài giảng này, chúng ta sẽ giải quyết vấn đề sử dụng cùng một mã trạng thái HTTP (500) cho các tình huống lỗi khác nhau trong REST APIs. Chúng ta sẽ triển khai các mã trạng thái phù hợp hơn để cung cấp sự rõ ràng tốt hơn cho các client sử dụng API.

## Vấn Đề
Trước đây, chúng ta đã sử dụng mã trạng thái HTTP 500 (Internal Server Error) trong nhiều tình huống:
- Xử lý RuntimeException trong GlobalExceptionHandler
- Các thao tác cập nhật thất bại
- Các thao tác xóa thất bại

Cách tiếp cận này tạo ra sự nhầm lẫn cho các client API vì họ không thể phân biệt giữa các loại lỗi khác nhau.

## Giải Pháp

### 1. Giới Thiệu Mã Trạng Thái HTTP 417
Chúng ta đã giới thiệu mã trạng thái HTTP 417 (Expectation Failed) cho các thao tác thất bại trong quá trình thực thi:

**Thao Tác Update (Cập Nhật):**
```java
// Bên trong controller class
if (!isUpdated) {
    return ResponseEntity
        .status(HttpStatus.EXPECTATION_FAILED)
        .body(new ResponseDto(STATUS_417, MESSAGE_417_UPDATE));
}
```

**Thao Tác Delete (Xóa):**
```java
if (!isDeleted) {
    return ResponseEntity
        .status(HttpStatus.EXPECTATION_FAILED)
        .body(new ResponseDto(STATUS_417, MESSAGE_417_DELETE));
}
```

### 2. Cập Nhật Constants (Hằng Số)
Tạo các hằng số mới cho status 417:
- `STATUS_417 = "417"`
- `MESSAGE_417_UPDATE = "Update operation failed. Please try again or contact dev team"`
- `MESSAGE_417_DELETE = "Delete operation failed. Please try again or contact dev team"`

Các hằng số cũ STATUS_500 và MESSAGE_500 đã được comment nhưng vẫn giữ lại để tham khảo.

### 3. Tài Liệu Phản Hồi API

Mỗi API giờ đây có các mã phản hồi được tài liệu hóa đầy đủ:

**Thao Tác Create và Fetch:**
- 200/201: Phản hồi thành công
- 500: RuntimeException với schema ErrorResponseDto

**Thao Tác Update:**
- 204: Thành công (No Content)
- 417: Expectation Failed (thao tác thất bại)
- 500: RuntimeException với schema ErrorResponseDto

**Thao Tác Delete:**
- 204: Thành công (No Content)
- 417: Expectation Failed (thao tác thất bại)
- 500: RuntimeException với schema ErrorResponseDto

### 4. Loại Bỏ Các Ví Dụ Gây Nhầm Lẫn

Chúng ta đã loại bỏ các giá trị example được hardcode từ ResponseDto:
```java
// Trước đây
@Schema(example = "200")
private String statusCode;

@Schema(example = "Request processed successfully")
private String statusMessage;

// Sau khi thay đổi
private String statusCode;
private String statusMessage;
```

Điều này ngăn chặn sự nhầm lẫn khi tài liệu OpenAPI hiển thị mã trạng thái 200 ngay cả đối với phản hồi 417 hoặc 500.

## Lợi Ích

1. **Phân Biệt Lỗi Rõ Ràng**: Các client giờ đây có thể phân biệt giữa:
   - Runtime exceptions (500)
   - Các lỗi thao tác dự kiến (417)
   - Các thao tác thành công (200/204)

2. **Tài Liệu API Tốt Hơn**: Tài liệu OpenAPI/Swagger giờ đây hiển thị rõ ràng tất cả các mã phản hồi có thể có cho mỗi endpoint

3. **Trải Nghiệm Client Được Cải Thiện**: Người sử dụng API có thể triển khai xử lý lỗi thông minh hơn dựa trên các mã trạng thái cụ thể

## Tóm Tắt

Bằng cách giới thiệu mã trạng thái HTTP 417 cho các lỗi thao tác và duy trì 500 cho runtime exceptions, chúng ta đã tạo ra một hợp đồng rõ ràng hơn giữa REST API của chúng ta và các client. Mỗi endpoint API giờ đây có các mã phản hồi được tài liệu hóa tốt, đại diện chính xác cho các tình huống khác nhau.

Schema ErrorResponseDto giờ đây được hiển thị đúng cách trong phần schemas của OpenAPI, và tất cả các định dạng phản hồi đều hiển thị rõ ràng trong tài liệu.

## Điểm Chính Cần Nhớ
- Sử dụng mã trạng thái HTTP phù hợp cho các tình huống lỗi khác nhau
- HTTP 417 phù hợp cho các lỗi expectation/operation failures
- HTTP 500 nên được dành riêng cho các runtime exceptions không mong đợi
- Loại bỏ các giá trị example có thể tạo ra nhầm lẫn trong tài liệu API
- Tài liệu hóa tất cả các mã phản hồi có thể có cho mỗi endpoint API