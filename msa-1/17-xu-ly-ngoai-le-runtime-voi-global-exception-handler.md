# Xử Lý Ngoại Lệ Runtime với Global Exception Handler

## Tổng Quan

Trong bài giảng này, chúng ta sẽ học cách xử lý các ngoại lệ runtime trong các REST API của Accounts microservice bằng cách sử dụng phương pháp global exception handler. Điều này đảm bảo các phản hồi lỗi thích hợp được gửi đến ứng dụng client khi xảy ra lỗi không mong đợi.

## Tình Trạng Hiện Tại

Accounts microservice của chúng ta hiện có bốn REST API hỗ trợ các thao tác CRUD. `GlobalExceptionHandler` hiện tại chỉ xử lý hai ngoại lệ nghiệp vụ:
- `ResourceNotFoundException`
- `CustomerAlreadyExistException`

Đây là các ngoại lệ do người dùng định nghĩa, nhưng chúng ta cần xử lý các ngoại lệ runtime có thể xảy ra bất cứ lúc nào và ở bất kỳ vị trí nào trong ứng dụng.

## Triển Khai Xử Lý Ngoại Lệ Toàn Cục

### Bước 1: Thêm Exception Handler Tổng Quát

Để xử lý tất cả các ngoại lệ runtime, chúng ta cần thêm một phương thức exception handler mới trong lớp `GlobalExceptionHandler`:

```java
@ExceptionHandler(Exception.class)
public ResponseEntity<ErrorResponseDto> handleGlobalException(
    Exception exception,
    WebRequest webRequest
) {
    ErrorResponseDto errorResponseDto = new ErrorResponseDto(
        webRequest.getDescription(false),
        HttpStatus.INTERNAL_SERVER_ERROR,
        exception.getMessage(),
        LocalDateTime.now()
    );
    
    return new ResponseEntity<>(errorResponseDto, HttpStatus.INTERNAL_SERVER_ERROR);
}
```

### Cách Hoạt Động

1. **Phân Cấp Ngoại Lệ**: Lớp `Exception` trong Java đại diện cho tất cả các loại ngoại lệ (checked và unchecked)
2. **Xử Lý Ưu Tiên**: Spring Boot framework tìm kiếm các phương thức handler khớp chính xác với ngoại lệ trước
3. **Cơ Chế Dự Phòng**: Nếu không có handler cụ thể nào tồn tại, exception handler tổng quát sẽ được gọi

### Cấu Trúc Phản Hồi

Phản hồi lỗi bao gồm:
- **API Path**: Endpoint được gọi
- **HTTP Status**: `INTERNAL_SERVER_ERROR` (500)
- **Error Message**: Thông báo ngoại lệ thực tế từ Spring Boot
- **Timestamp**: Ngày và giờ hiện tại

## Cơ Hội Cải Tiến

Trong các ứng dụng thực tế, bạn có thể cải tiến phương thức này để:
- Kích hoạt thông báo email cho đội ngũ vận hành
- Ghi log vào bảng cơ sở dữ liệu để theo dõi ngoại lệ
- Tạo báo cáo để phân tích
- Triển khai logic nghiệp vụ tùy chỉnh dựa trên yêu cầu

## Kiểm Thử Global Exception Handler

### Tạo Kịch Bản Kiểm Thử

Để kiểm thử xử lý ngoại lệ runtime, chúng ta có thể cố ý tạo ra `NullPointerException`:

1. Xóa annotation `@AllArgsConstructor` khỏi `AccountsController`
2. Điều này chỉ để lại constructor mặc định
3. Không có constructor, autowiring sẽ không xảy ra
4. Trường `IAccountService` vẫn là null
5. Bất kỳ thao tác API nào cũng sẽ ném ra `NullPointerException`

### Các Bước Kiểm Thử

1. Thực hiện các thay đổi và rebuild ứng dụng
2. Kiểm thử bất kỳ endpoint API nào (ví dụ: Create Account API)
3. Gửi request đến endpoint

### Phản Hồi Mong Đợi

```json
{
    "apiPath": "/api/create",
    "errorCode": "INTERNAL_SERVER_ERROR",
    "errorMessage": "Cannot invoke method because object is null",
    "timestamp": "2024-03-09T10:30:00"
}
```

Mã trạng thái HTTP sẽ là **500 Internal Server Error**.

## Các Khái Niệm Chính

### Annotation @ControllerAdvice

Annotation này cho phép xử lý ngoại lệ toàn cục trên tất cả các controller trong ứng dụng.

### Annotation @ExceptionHandler

Annotation này đánh dấu một phương thức là exception handler cho các loại ngoại lệ cụ thể.

### Mẫu Triển Khai

Sự kết hợp của `@ControllerAdvice` và `@ExceptionHandler` cho phép bạn:
1. Tập trung hóa logic xử lý ngoại lệ
2. Xử lý ngoại lệ toàn cục trên tất cả các controller
3. Cung cấp phản hồi lỗi nhất quán
4. Tách biệt xử lý lỗi khỏi logic nghiệp vụ

## Câu Hỏi Phỏng Vấn

**Hỏi: Làm thế nào để triển khai logic ngoại lệ toàn cục trong ứng dụng Spring Boot?**

**Đáp:** Sử dụng sự kết hợp của các annotation `@ControllerAdvice` và `@ExceptionHandler`:
- Tạo một lớp được đánh dấu với `@ControllerAdvice`
- Định nghĩa các phương thức được đánh dấu với `@ExceptionHandler`
- Chỉ định (các) loại ngoại lệ cần xử lý
- Triển khai logic phản hồi lỗi trong phương thức

## Tóm Tắt

- Xử lý ngoại lệ toàn cục đảm bảo tất cả các ngoại lệ runtime được xử lý đúng cách
- Handler `Exception.class` hoạt động như bộ bắt lỗi cho tất cả các ngoại lệ chưa được xử lý
- Spring Boot ưu tiên các exception handler cụ thể hơn handler tổng quát
- Phương pháp này cung cấp phản hồi lỗi nhất quán cho ứng dụng client
- Kiến thức thiết yếu cho việc phát triển REST API với Spring Boot

## Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ tiếp tục xây dựng kiến trúc microservices với các tính năng và thực hành tốt nhất bổ sung.

---

**Lưu ý**: Xử lý ngoại lệ đúng cách là rất quan trọng đối với các ứng dụng production và thể hiện thực hành phát triển Spring Boot chuyên nghiệp.