# Lesson 06 — I/O, JSON, and HTTP client

## Goal

Read/write files using NIO, parse/serialize JSON, and call an HTTP API using Java’s HTTP client.

## Key concepts

- Use `java.nio.file.Path` + `Files` for modern file operations.
- Prefer explicit character sets: UTF-8.
- JSON is not built-in: you typically use Jackson.
- Java HTTP client (Java 11+) supports sync and async requests.

## Hands-on

### 1) Read and write a text file

```java
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

Path p = Path.of("notes.txt");
Files.writeString(p, "hello\n", StandardCharsets.UTF_8);
String content = Files.readString(p, StandardCharsets.UTF_8);
System.out.println(content);
```

### 2) JSON with Jackson (conceptual)

You’ll add the dependency in Lesson 10 (Maven/Gradle). For now, learn the model:

```java
public record User(String id, String email) {}
```

Typical Jackson usage looks like:

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

- You can read and write files using `Path` and `Files`.
- You understand how JSON libraries fit into Java projects.
- You can call an HTTP endpoint and handle status codes.

## Common pitfalls

- Using platform-default charset unintentionally.
- Ignoring timeouts and retries for HTTP calls.
- Treating JSON as a “stringly typed” blob instead of mapping to types.

## Next

Concurrency: threads, executors, and safe shared state.
