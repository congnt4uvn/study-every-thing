# Bài 11 — Spring Boot + REST API

## Mục tiêu

Xây REST API nhỏ với Spring Boot: routing, validation, cấu hình, và error handling.

## Khái niệm chính

- Spring quản lý object bằng dependency injection.
- Controller map HTTP request sang method.
- DTO thể hiện shape request/response.
- Validation bằng Jakarta Validation.

## Thực hành

### 1) Tạo Spring Boot project

Dùng Spring Initializr với:

- Spring Web
- Validation

### 2) Controller tối thiểu

```java
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class HelloController {
  @GetMapping("/hello")
  public String hello(@RequestParam(defaultValue = "world") String name) {
    return "Hello, " + name;
  }
}
```

### 3) DTO + validation

```java
import jakarta.validation.constraints.*;

public record CreateUserRequest(
  @NotBlank String email,
  @Min(1) int age
) {}
```

Controller:

```java
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.*;

@PostMapping("/users")
public String createUser(@Valid @RequestBody CreateUserRequest req) {
  return "created:" + req.email();
}
```

### 4) Error handling cơ bản

Spring Boot mặc định trả 400 + chi tiết validation khi DTO không hợp lệ.

## Checklist

- Chạy được app Spring Boot local.
- Tạo được endpoint GET và POST.
- Validate được request body.

## Lỗi thường gặp

- Trả entity trực tiếp (dính DB model vào API).
- Bỏ qua HTTP status code.
- Nhét business logic vào controller.

## Tiếp theo

Lưu dữ liệu chuẩn bằng SQL và JPA, hiểu transaction.
