# Lesson 11 — Spring Boot + REST API

## Goal

Build a small REST API with Spring Boot: routing, validation, configuration, and error handling.

## Key concepts

- Spring manages objects via dependency injection.
- Controllers map HTTP requests to Java methods.
- DTOs represent request/response shapes.
- Validation with Jakarta Validation annotations.

## Hands-on

### 1) Create a Spring Boot project

Use Spring Initializr (web UI) with:

- Spring Web
- Validation

### 2) A minimal controller

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

### 3) Request DTO + validation

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

### 4) Error handling basics

Spring Boot will automatically return a 400 with validation details when DTO validation fails.

## Checklist

- You can run a Spring Boot app locally.
- You can create a GET endpoint and a POST endpoint.
- You can validate request bodies.

## Common pitfalls

- Returning entities directly (couples DB model to API).
- Ignoring HTTP status codes.
- Doing “business logic” inside controllers.

## Next

Persist data properly with SQL and JPA, and learn transactions.
