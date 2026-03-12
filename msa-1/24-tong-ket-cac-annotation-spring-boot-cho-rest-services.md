# Tổng Kết Các Annotation Spring Boot Cho REST Services

## Tổng Quan

Tài liệu này cung cấp bản tóm tắt toàn diện về các annotation và class thiết yếu của Spring Boot được sử dụng để xây dựng REST APIs trong kiến trúc microservices. Những annotation và component này là nền tảng khi phát triển REST services với Spring Boot.

## Các Annotation và Class Quan Trọng

### 1. @RestController

**Mục đích**: Đánh dấu một class là REST API controller.

**Cách sử dụng**:
- Đặt annotation này lên đầu class để expose các Java method dưới dạng REST APIs
- Hoạt động kết hợp với các HTTP mapping annotation như `@GetMapping`, `@PostMapping`
- Thông báo cho Spring Boot framework expose tất cả các Java method dưới dạng REST endpoints

**Ví dụ Tình huống**:
```java
@RestController
public class AccountsController {
    // Các REST API method
}
```

**Lưu ý**: `@RestController` là sự kết hợp của `@Controller` + `@ResponseBody`

---

### 2. @Controller vs @RestController

**@Controller**:
- Sử dụng khi bạn cần cả REST APIs và Spring MVC methods trong cùng một class
- Yêu cầu annotation `@ResponseBody` trên từng method riêng lẻ cần trả về JSON

**@RestController**:
- Sử dụng khi tất cả các method trong class là REST endpoints
- Tự động áp dụng `@ResponseBody` cho tất cả các method
- Được ưa chuộng cho các controller REST API thuần túy

---

### 3. @ResponseBody

**Mục đích**: Chỉ định rằng giá trị trả về của method nên được gắn vào response body của web.

**Cách sử dụng**:
- Sử dụng với annotation `@Controller`
- Thông báo cho Spring Boot trả về response ở định dạng JSON thay vì Spring MVC style (HTML/UI format)
- Không cần thiết khi sử dụng `@RestController` (đã được bao gồm sẵn)

**Khi nào sử dụng**:
- Khi sử dụng `@Controller` và cần các method cụ thể trả về JSON
- Controller hỗn hợp với cả REST và MVC methods

---

### 4. ResponseEntity

**Loại**: Class (không phải annotation)

**Mục đích**: Đại diện cho toàn bộ HTTP response bao gồm headers, status và body.

**Tính năng**:
- Cho phép gửi thông tin response đầy đủ (headers, status code, body)
- Sử dụng generics để chỉ định kiểu đối tượng trong response body
- Cung cấp toàn quyền kiểm soát HTTP response

**Ví dụ**:
```java
public ResponseEntity<CustomerDTO> getCustomer() {
    return ResponseEntity.ok(customerDTO);
}
```

**Lợi ích**:
- Kiểm soát hoàn toàn HTTP response
- Có thể đặt custom headers và status codes
- Response body an toàn về kiểu dữ liệu

---

### 5. @ControllerAdvice

**Mục đích**: Kích hoạt xử lý exception toàn cục trên tất cả các controller.

**Cách sử dụng**:
- Đặt trên một class để biến nó thành global exception handler
- Hoạt động với annotation `@ExceptionHandler`
- Chặn các exception được throw bởi bất kỳ controller nào

**Cách hoạt động**:
1. Tạo một class được annotate với `@ControllerAdvice`
2. Định nghĩa các method được annotate với `@ExceptionHandler`
3. Gắn mỗi method với các loại exception cụ thể
4. Khi exception đó xảy ra trong bất kỳ controller nào, handler method sẽ được thực thi

**Ví dụ Tình huống**:
```java
@ControllerAdvice
public class GlobalExceptionHandler {
    
    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleResourceNotFound(ResourceNotFoundException ex) {
        // Xử lý exception
    }
}
```

---

### 6. @RestControllerAdvice

**Mục đích**: Phiên bản chuyên biệt của `@ControllerAdvice` cho REST APIs.

**Cấu thành**: `@ControllerAdvice` + `@ResponseBody`

**Mối quan hệ**: Tương tự như mối quan hệ giữa `@Controller` và `@RestController`

**Khi nào sử dụng**:
- Khi bạn muốn các exception handler method trả về output JSON một cách nghiêm ngặt
- Cho các ứng dụng REST API thuần túy

**Lưu ý**: Cả `@ControllerAdvice` và `@RestControllerAdvice` đều hoạt động hiệu quả cho REST services. Ví dụ trong Accounts Microservice sử dụng `@ControllerAdvice` thành công.

---

### 7. RequestEntity

**Loại**: Class (tương tự ResponseEntity)

**Mục đích**: Đại diện cho một HTTP request bao gồm headers và body.

**Tình huống sử dụng**:
- Khi bạn cần nhận cả request body và request headers như một method parameter duy nhất
- Cung cấp quyền truy cập vào thông tin request đầy đủ

**Khi không cần thiết**:
- Khi bạn chỉ cần request body (sử dụng `@RequestBody` thay thế)
- Khi bạn chỉ cần các header cụ thể (sử dụng `@RequestHeader` thay thế)

**Ví dụ**:
```java
public ResponseEntity<String> processRequest(RequestEntity<CustomerDTO> requestEntity) {
    // Trích xuất headers và body từ requestEntity
    HttpHeaders headers = requestEntity.getHeaders();
    CustomerDTO body = requestEntity.getBody();
    // Thực thi logic nghiệp vụ
}
```

---

### 8. @RequestHeader

**Mục đích**: Gắn một method parameter với một request header.

**Cách sử dụng**:
- Trích xuất các giá trị header cụ thể từ HTTP request
- Truyền giá trị header như method parameter

**Ví dụ**:
```java
@GetMapping("/customer")
public ResponseEntity<CustomerDTO> getCustomer(
    @RequestHeader("Authorization") String authToken) {
    // Sử dụng authToken trong logic nghiệp vụ
}
```

---

### 9. @RequestBody

**Mục đích**: Gắn HTTP request body với một method parameter.

**Cách sử dụng**:
- Nhận toàn bộ request body dưới dạng một đối tượng Java
- Tự động deserialize JSON thành đối tượng Java

**Ví dụ**:
```java
@PostMapping("/account")
public ResponseEntity<String> createAccount(
    @RequestBody AccountDTO accountDTO) {
    // Sử dụng accountDTO trong logic nghiệp vụ
}
```

---

## Quy Trình Phát Triển REST API Hoàn Chỉnh

Khi xây dựng REST APIs với Spring Boot, hãy tuân theo trình tự này:

1. **Tạo Controller Class**
   - Annotate với `@RestController`

2. **Định nghĩa Java Methods**
   - Thêm HTTP mapping annotations (`@GetMapping`, `@PostMapping`, `@PutMapping`, `@DeleteMapping`)

3. **Xử lý Request Input**
   - Sử dụng `@RequestBody` cho request body
   - Sử dụng `@RequestHeader` cho các header cụ thể
   - Sử dụng `RequestEntity` cho request hoàn chỉnh (headers + body)

4. **Trả về Response**
   - Sử dụng `ResponseEntity` để kiểm soát hoàn toàn response

5. **Triển khai Global Exception Handling**
   - Tạo một class với `@ControllerAdvice` hoặc `@RestControllerAdvice`
   - Định nghĩa các method với `@ExceptionHandler` cho các loại exception khác nhau

---

## Mẹo Phỏng Vấn

Khi được hỏi "Làm thế nào để xây dựng REST APIs với Spring Boot?", hãy giải thích quy trình như một câu chuyện:

1. Bắt đầu bằng cách tạo một class và annotate nó với `@RestController`
2. Tạo các Java method và annotate chúng với HTTP mappings (`@GetMapping`, `@PostMapping`, v.v.)
3. Sử dụng `@RequestBody`, `@RequestHeader`, hoặc `RequestEntity` để nhận input
4. Triển khai logic nghiệp vụ trong các method
5. Trả về response sử dụng `ResponseEntity`
6. Định nghĩa global exception handling sử dụng `@ControllerAdvice` và `@ExceptionHandler`

Cách giải thích tuần tự này thể hiện sự hiểu biết hoàn chỉnh về quy trình phát triển REST API.

---

## Bảng Tóm Tắt

| Annotation/Class | Loại | Mục đích |
|-----------------|------|---------|
| `@RestController` | Annotation | Đánh dấu class là REST controller |
| `@Controller` | Annotation | Đánh dấu class là controller (REST + MVC) |
| `@ResponseBody` | Annotation | Trả về JSON response từ method |
| `ResponseEntity` | Class | Kiểm soát HTTP response hoàn chỉnh |
| `@ControllerAdvice` | Annotation | Xử lý exception toàn cục |
| `@RestControllerAdvice` | Annotation | Xử lý exception toàn cục cho REST |
| `RequestEntity` | Class | Đại diện HTTP request hoàn chỉnh |
| `@RequestHeader` | Annotation | Gắn request header với parameter |
| `@RequestBody` | Annotation | Gắn request body với parameter |

---

## Best Practices (Thực Hành Tốt Nhất)

1. **Sử dụng `@RestController`** cho các controller REST API thuần túy
2. **Sử dụng `ResponseEntity`** để xử lý response linh hoạt
3. **Triển khai global exception handling** với `@ControllerAdvice`
4. **Chọn annotation input phù hợp** dựa trên nhu cầu của bạn:
   - `@RequestBody` cho nội dung body
   - `@RequestHeader` cho các header cụ thể
   - `RequestEntity` khi bạn cần cả hai
5. **Giữ các annotation này sẵn sàng** cho phỏng vấn và phát triển

---

## Kết Luận

Những annotation và class này tạo thành nền tảng cho việc phát triển REST service với Spring Boot. Hiểu rõ mục đích, mối quan hệ và các tình huống sử dụng thích hợp của chúng là điều cần thiết để xây dựng microservices mạnh mẽ. Hãy giữ tài liệu tham khảo này sẵn sàng cho cả việc phát triển và chuẩn bị phỏng vấn.

---

**Khóa học**: Microservices với Spring Boot  
**Module**: Phát triển REST API  
**Chủ đề**: Tổng kết các Annotation Spring Boot