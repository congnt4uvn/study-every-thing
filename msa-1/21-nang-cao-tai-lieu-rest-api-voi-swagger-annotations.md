# Nâng Cao Tài Liệu REST API với Swagger Annotations

## Tổng Quan
Hướng dẫn này trình bày cách nâng cao tài liệu REST API sử dụng các annotation OpenAPI/Swagger trong ứng dụng Spring Boot. Chúng ta sẽ cải thiện tài liệu cho AccountsController bằng cách thêm mô tả chi tiết, tóm tắt và thông tin phản hồi.

## Tình Trạng Hiện Tại
Tài liệu REST API hiện tại hiển thị:
- Tên kỹ thuật `AccountsController` không có thông tin mô tả
- Không có mô tả cho các API trong controller
- Thông tin hạn chế về các hoạt động API và phản hồi

## Nâng Cao Tài Liệu Cấp Controller

### Sử Dụng Annotation @Tag
Để cung cấp thông tin về tất cả các API trong một controller class, sử dụng annotation `@Tag`:

```java
@Tag(
    name = "CRUD REST APIs cho Accounts trong EasyBank",
    description = "CRUD REST APIs trong EasyBank để tạo, cập nhật, lấy và xóa thông tin tài khoản"
)
@RestController
public class AccountsController {
    // ... các phương thức controller
}
```

**Điểm Chính:**
- Annotation `@Tag` thuộc package Swagger/OpenAPI SpringDoc
- `name` cung cấp tóm tắt cho tất cả các API trong controller
- `description` đưa ra thông tin chi tiết về mục đích của controller

**Kết Quả:** Thay vì chỉ thấy "AccountsController", khách hàng sẽ thấy mô tả chuyên nghiệp giải thích rằng phần này chứa bốn REST API để xử lý các thao tác tạo, cập nhật, lấy và xóa.

## Nâng Cao Tài Liệu Cấp API Operation

### Sử Dụng Annotation @Operation

Đối với các API operation riêng lẻ, sử dụng annotation `@Operation`:

```java
@Operation(
    summary = "Create Account REST API",
    description = "REST API để tạo Customer và Account mới trong EasyBank"
)
@PostMapping("/create")
public ResponseEntity<ResponseDto> createAccount(@RequestBody AccountDto accountDto) {
    // ... implementation
}
```

**Điểm Chính:**
- `summary` cung cấp tiêu đề ngắn gọn cho API
- `description` đưa ra thông tin chi tiết về chức năng của API

## Tùy Chỉnh Tài Liệu Response

### Sử Dụng Annotation @ApiResponse

Theo mặc định, tài liệu hiển thị phản hồi 200 OK. Để tùy chỉnh:

```java
@Operation(
    summary = "Create Account REST API",
    description = "REST API để tạo Customer và Account mới trong EasyBank"
)
@ApiResponse(
    responseCode = "201",
    description = "HttpStatus.CREATED"
)
@PostMapping("/create")
public ResponseEntity<ResponseDto> createAccount(@RequestBody AccountDto accountDto) {
    // ... implementation
}
```

**Điểm Chính:**
- `@ApiResponse` ghi đè phản hồi 200 mặc định
- `responseCode` chỉ định mã trạng thái HTTP thực tế được trả về
- `description` giải thích ý nghĩa của mã trạng thái

## Xử Lý Nhiều Mã Response

### Sử Dụng Annotation @ApiResponses

Đối với các operation trả về nhiều phản hồi có thể:

```java
@Operation(
    summary = "Update Account Details REST API",
    description = "REST API để cập nhật thông tin Customer và Account dựa trên số tài khoản"
)
@ApiResponses({
    @ApiResponse(
        responseCode = "200",
        description = "HttpStatus.OK"
    ),
    @ApiResponse(
        responseCode = "500",
        description = "HttpStatus.INTERNAL_SERVER_ERROR"
    )
})
@PutMapping("/update")
public ResponseEntity<ResponseDto> updateAccount(@RequestBody AccountDto accountDto) {
    // ... implementation
}
```

**Điểm Chính:**
- Sử dụng `@ApiResponses` (số nhiều) để định nghĩa nhiều phản hồi
- Mỗi `@ApiResponse` được phân cách bằng dấu phẩy
- Điều này cung cấp thông tin trước cho khách hàng và nhà phát triển về các phản hồi có thể xảy ra

## Ví Dụ: Tài Liệu API Hoàn Chỉnh

### Fetch Account API
```java
@Operation(
    summary = "Fetch Account Details REST API",
    description = "REST API để lấy thông tin Customer và Account dựa trên số tài khoản"
)
@ApiResponse(
    responseCode = "200",
    description = "HttpStatus.OK"
)
@GetMapping("/fetch")
public ResponseEntity<AccountDto> fetchAccount(@RequestParam String accountNumber) {
    // ... implementation
}
```

### Delete Account API
```java
@Operation(
    summary = "Delete Account REST API",
    description = "REST API để xóa Customer và Account dựa trên số tài khoản"
)
@ApiResponses({
    @ApiResponse(
        responseCode = "200",
        description = "HttpStatus.OK"
    ),
    @ApiResponse(
        responseCode = "500",
        description = "HttpStatus.INTERNAL_SERVER_ERROR"
    )
})
@DeleteMapping("/delete")
public ResponseEntity<ResponseDto> deleteAccount(@RequestParam String accountNumber) {
    // ... implementation
}
```

## Lợi Ích

Sau khi triển khai các cải tiến này:
1. **Tài Liệu Chuyên Nghiệp**: Khách hàng thấy thông tin rõ ràng, mô tả thay vì tên kỹ thuật
2. **Hiểu Rõ Hơn**: Nhà phát triển và tester biết chính xác chức năng của từng API
3. **Rõ Ràng Về Response**: Chỉ dẫn rõ ràng về các mã trạng thái HTTP có thể và ý nghĩa của chúng
4. **Cải Thiện Trải Nghiệm Developer**: Giúp việc tích hợp với các API dễ dàng hơn

## Response Schema

Tài liệu hiện nay hiển thị:
- Mã trạng thái HTTP chính xác (201, 200, 500, v.v.)
- Định dạng phản hồi (application/json)
- Cấu trúc schema (status code và status message)

## Các Bước Tiếp Theo

Cải tiến tiếp theo sẽ tập trung vào:
- Cải thiện tài liệu schema object
- Thêm dữ liệu mẫu vào schema objects
- Thay thế tên kỹ thuật bằng tên mô tả hơn
- Cung cấp giá trị mẫu để rõ ràng hơn

## Tóm Tắt

Bằng cách sử dụng các annotation `@Tag`, `@Operation`, `@ApiResponse`, và `@ApiResponses`, bạn có thể nâng cao đáng kể tài liệu REST API của mình. Điều này làm cho các API của bạn chuyên nghiệp hơn, dễ hiểu hơn và đơn giản hơn để tích hợp cho các ứng dụng khách và nhóm phát triển.