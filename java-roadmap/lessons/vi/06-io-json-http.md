# Bài 06 — I/O, JSON và HTTP client

## Mục tiêu

Đọc/ghi file bằng NIO, parse/serialize JSON, và gọi HTTP API bằng HTTP client của Java.

## Khái niệm chính

- Dùng `java.nio.file.Path` + `Files` cho thao tác file hiện đại.
- Chỉ rõ charset: UTF-8.
- JSON không có sẵn: thường dùng Jackson.
- HTTP client (Java 11+) hỗ trợ sync và async.

## Thực hành

### 1) Đọc/ghi file text

```java
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

Path p = Path.of("notes.txt");
Files.writeString(p, "hello\n", StandardCharsets.UTF_8);
String content = Files.readString(p, StandardCharsets.UTF_8);
System.out.println(content);
```

### 2) JSON với Jackson (mô hình)

Bạn sẽ add dependency ở Bài 10. Trước mắt hiểu cách model hoá:

```java
public record User(String id, String email) {}
```

Ví dụ Jackson thường như sau:

```java
// ObjectMapper mapper = new ObjectMapper();
// String json = mapper.writeValueAsString(new User("u1", "u1@example.com"));
// User user = mapper.readValue(json, User.class);
```

### 3) HTTP GET

```java
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

HttpClient client = HttpClient.newHttpClient();
HttpRequest req = HttpRequest.newBuilder()
  .uri(URI.create("https://httpbin.org/get"))
  .GET()
  .build();

HttpResponse<String> resp = client.send(req, HttpResponse.BodyHandlers.ofString());
System.out.println(resp.statusCode());
System.out.println(resp.body());
```

## Checklist

- Đọc/ghi file bằng `Path` và `Files`.
- Hiểu JSON library hoạt động thế nào trong project Java.
- Gọi HTTP endpoint và xử lý status code.

## Lỗi thường gặp

- Dùng charset mặc định của OS một cách vô ý.
- Bỏ qua timeout/retry khi gọi HTTP.
- Xử lý JSON như “string” thay vì map sang type.

## Tiếp theo

Concurrency: thread, executor, và chia sẻ trạng thái an toàn.
