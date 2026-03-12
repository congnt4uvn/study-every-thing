# Tài Liệu Hóa REST APIs với OpenAPI Specification

## Tại Sao Cần Tài Liệu Hóa REST APIs?

Khi xây dựng microservices và REST APIs, việc tài liệu hóa trở nên cực kỳ quan trọng khi:
- Cung cấp APIs cho các bên ngoài hoặc các team khác trong tổ chức
- Làm việc với team UI hoặc team phát triển ứng dụng mobile
- Hợp tác với team testing cần hiểu về hành vi của API

Không có tài liệu phù hợp, bạn sẽ phải trả lời liên tục các câu hỏi về:
- Định dạng request
- Định dạng response
- Các quy tắc validation

Thay vì phải tổ chức nhiều cuộc họp để giải thích về APIs, việc tài liệu hóa chúng theo tiêu chuẩn công nghiệp sẽ tiết kiệm thời gian và công sức.

## OpenAPI Specification

OpenAPI là một tiêu chuẩn cộng đồng mã nguồn mở cung cấp phương thức chuẩn hóa để định nghĩa các HTTP APIs như REST APIs. Nó cho phép người tiêu dùng:
- Nhanh chóng khám phá cách một API hoạt động
- Cấu hình cơ sở hạ tầng
- Tự động sinh client code và server code
- Tạo các test cases tự động

## Bắt Đầu với SpringDoc OpenAPI

Việc tài liệu hóa trở nên đơn giản với thư viện **SpringDoc OpenAPI** có sẵn tại [springdoc.org](https://springdoc.org).

### Thêm Dependency

Thêm Maven dependency sau vào file `pom.xml` của bạn:

```xml
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>${springdoc.version}</version>
</dependency>
```

**Lưu Ý Quan Trọng Về Phiên Bản:**
- Cho Spring Boot 3.x trở lên: Sử dụng phiên bản springdoc-openapi mới nhất
- Cho Spring Boot 2.x hoặc 1.x: Sử dụng springdoc-openapi v1.7.0

### Các Bước Triển Khai

1. Thêm dependency vào file `pom.xml`
2. Load các thay đổi Maven để tải dependency
3. Build và khởi động lại ứng dụng
4. Truy cập Swagger UI tại: `http://localhost:8080/swagger-ui/index.html`

## Tính Năng Của Tài Liệu Tự Động

Sau khi cấu hình, SpringDoc OpenAPI tự động quét các REST APIs và tạo tài liệu bao gồm:

### Các API Endpoints
- Tất cả các đường dẫn REST API từ controllers
- Các thao tác HTTP được hỗ trợ (GET, POST, PUT, DELETE)

### Thông Tin Request
- Các tham số request (path variables, query params)
- Định dạng và cấu trúc request body
- Các trường bắt buộc và tùy chọn
- Quy tắc validation (min/max length, patterns, v.v.)

### Thông Tin Response
- Mã status code
- Cấu trúc response body
- Định dạng thành công và lỗi

### Tài Liệu Schema
Tất cả các DTO objects (Data Transfer Objects) được tài liệu hóa với:
- Tên và kiểu dữ liệu của các trường
- Ràng buộc validation từ các annotations
- Cấu trúc đối tượng lồng nhau

## Ví Dụ: Tài Liệu AccountsController

Tài liệu được tạo ra sẽ hiển thị:

**Update Account API (PUT)**
- Chấp nhận: JSON body với cấu trúc CustomerDto
- Các trường bắt buộc: name, email, mobile number
- Validation: Định dạng email, pattern số điện thoại
- Response: Status code 200 với statusCode và statusMessage

**Create Account API (POST)**
- Chấp nhận: Schema CustomerDto
- Response: Status code và status message

**Fetch Account API (GET)**
- Chấp nhận: Query parameter (mobile number) - bắt buộc
- Response: CustomerDto với đầy đủ thông tin customer và account

**Delete Account API (DELETE)**
- Chấp nhận: Query parameter (mobile number)
- Response: Status code và status message

## Lợi Ích

1. **Tự Kiểm Thử**: Developers có thể test APIs trực tiếp từ Swagger UI
2. **Giao Tiếp Rõ Ràng**: Loại bỏ việc giải thích lặp đi lặp lại
3. **Tài Liệu Chuyên Nghiệp**: Định dạng theo tiêu chuẩn công nghiệp
4. **Dễ Dàng Tích Hợp**: Yêu cầu thiết lập tối thiểu
5. **Cập Nhật Tự Động**: Tài liệu cập nhật khi code thay đổi

## Thực Hành Tốt Nhất

- Luôn thêm SpringDoc OpenAPI dependency vào microservices của bạn
- Tài liệu hóa trước khi deploy lên production
- Tránh việc phải giải thích APIs thủ công cho từng người tiêu dùng
- Sử dụng đây là baseline; nâng cao thêm với các annotations tùy chỉnh cho output chuyên nghiệp hơn

## Bước Tiếp Theo

Mặc dù tài liệu cơ bản đã hoạt động tốt, bạn có thể nâng cao thêm bằng cách:
- Thêm mô tả và ví dụ tùy chỉnh
- Sử dụng các annotations của SpringDoc để làm rõ hơn
- Cung cấp giá trị mẫu cho các DTOs
- Làm cho tài liệu chuyên nghiệp và sẵn sàng cho production hơn

Thiết lập cơ bản này cung cấp tài liệu xuất sắc với nỗ lực tối thiểu, giúp REST APIs của bạn dễ dàng sử dụng và kiểm thử.