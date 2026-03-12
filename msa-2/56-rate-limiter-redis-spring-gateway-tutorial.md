# Triển Khai Rate Limiter Pattern trong Spring Cloud Gateway với Redis

## Tổng Quan

Hướng dẫn này trình bày cách triển khai Rate Limiter pattern trong Spring Cloud Gateway sử dụng Redis để kiểm soát số lượng request mà người dùng có thể thực hiện trong một khoảng thời gian cụ thể.

## Yêu Cầu Tiên Quyết

- Ứng dụng Spring Cloud Gateway
- Docker đã được cài đặt và đang chạy
- Dự án Maven đã được thiết lập
- Redis container

## Bước 1: Thêm Dependency Redis

Thêm dependency Redis reactive vào file `pom.xml`:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis-reactive</artifactId>
</dependency>
```

Sau khi thêm dependency, thực hiện Maven reload để tải các thư viện cần thiết.

## Bước 2: Cấu Hình Các Bean Rate Limiter

Trong class `GatewayserverApplication`, tạo hai bean quan trọng:

### 1. Bean KeyResolver

Bean này xác định key mà Rate Limiter pattern sẽ hoạt động dựa trên:

```java
@Bean
public KeyResolver userKeyResolver() {
    return exchange -> Mono.justOrEmpty(exchange.getRequest()
            .getHeaders()
            .getFirst("user"))
            .defaultIfEmpty("anonymous");
}
```

**Giải thích:**
- Trích xuất header `user` từ request
- Nếu không có header `user`, gán giá trị mặc định là `anonymous`
- Trong môi trường production, tùy chỉnh logic này dựa trên yêu cầu của bạn

### 2. Bean RedisRateLimiter

Cấu hình các tham số giới hạn tốc độ:

```java
@Bean
public RedisRateLimiter redisRateLimiter() {
    return new RedisRateLimiter(replenishRate, burstCapacity, requestedTokens);
}
```

**Các Tham Số Cấu Hình:**
- **replenishRate**: 1 (thêm một token mỗi giây)
- **burstCapacity**: 1 (số token tối đa có sẵn)
- **requestedTokens**: 1 (chi phí mỗi request)

Với các cài đặt này, mỗi người dùng chỉ có thể thực hiện **một request mỗi giây**.

## Bước 3: Áp Dụng Rate Limiter cho Routes

Thêm filter Rate Limiter vào cấu hình routing. Ví dụ, áp dụng cho cards microservice:

```java
.route(p -> p
    .path("/eazybank/cards/**")
    .filters(f -> f
        .addResponseHeader("X-Response-Time", LocalDateTime.now().toString())
        .requestRateLimiter(c -> c
            .setRateLimiter(redisRateLimiter())
            .setKeyResolver(userKeyResolver()))
    )
    .uri("lb://CARDS"))
```

Cấu hình này áp dụng Rate Limiter pattern cho tất cả các API trong cards microservice.

## Bước 4: Khởi Động Redis Container

Khởi động Redis container sử dụng Docker:

```bash
docker run -p 6379:6379 --name eazyredis -d redis
```

**Giải thích lệnh:**
- `-p 6379:6379`: Map cổng mặc định của Redis
- `--name eazyredis`: Đặt tên cho container
- `-d`: Chạy ở chế độ detached (nền)
- `redis`: Tên image

Redis sẽ duy trì các bucket với tên người dùng và xử lý các cấu hình rate limiting.

## Bước 5: Cấu Hình Kết Nối Redis

Thêm các thuộc tính kết nối Redis vào `application.yml` trong gateway server:

```yaml
spring:
  application:
    name: gatewayserver
  config:
    import: "optional:configserver:http://localhost:8071"
  cloud:
    gateway:
      # ... các cấu hình gateway khác
  data:
    redis:
      connect-timeout: 2s
      host: localhost
      port: 6379
      timeout: 1s
```

Lưu các thay đổi và rebuild ứng dụng.

## Bước 6: Kiểm Tra Rate Limiter

### Khởi Động Các Service Cần Thiết

Đảm bảo các service sau đang chạy:
1. Config Server
2. Eureka Server
3. Cards Microservice
4. Gateway Server

### Kiểm Tra Tải với Apache Benchmark

Sử dụng Apache Benchmark (AB) để kiểm tra hành vi rate limiting:

```bash
ab -n 10 -c 2 -v 3 http://localhost:8072/eazybank/cards/api/contact-info
```

**Các Tham Số:**
- `-n 10`: Gửi tổng cộng 10 request
- `-c 2`: Duy trì mức độ đồng thời là 2 (gửi 2 request cùng lúc)
- `-v 3`: Mức độ chi tiết 3 (báo cáo chi tiết)

### Kết Quả Mong Đợi

**Tóm tắt:**
- Tổng số request: 10
- Request thành công: 1 (HTTP 200)
- Request thất bại: 9 (HTTP 429 - Too Many Requests)
- Thời gian xử lý: ~0.5 giây

**Mẫu Response:**
- Request đầu tiên: `200 OK`
- Các request còn lại: `429 Too Many Requests`

Mã trạng thái `429` cho biết giới hạn tốc độ đã bị vượt quá, xác nhận rằng Rate Limiter pattern đang hoạt động chính xác.

## Cách Hoạt Động

1. **Thuật Toán Token Bucket**: Redis duy trì một token bucket cho mỗi người dùng (được xác định bởi KeyResolver)
2. **Bổ Sung Token**: Một token được thêm vào bucket mỗi giây
3. **Xử Lý Request**: Mỗi request tiêu thụ một token
4. **Giới Hạn Tốc Độ**: Khi không còn token, các request nhận mã trạng thái `429`

## Kiểm Tra với Header User Tùy Chỉnh

Để kiểm tra với người dùng cụ thể, thêm header `user` vào request:

```bash
ab -n 10 -c 2 -v 3 -H "user: john.doe" http://localhost:8072/eazybank/cards/api/contact-info
```

**Lưu ý:** Trong môi trường local với một người dùng duy nhất, hành vi vẫn giống nhau. Sự khác biệt thực sự trở nên rõ ràng trong production với nhiều người dùng, nơi mỗi người dùng có giới hạn tốc độ riêng.

## Cài Đặt Apache Benchmark

### Unix/Mac
Apache Benchmark thường được cài đặt sẵn. Kiểm tra bằng:
```bash
ab -V
```

### Windows
1. Tải Apache HTTP Server từ trang web chính thức của Apache
2. Giải nén file archive
3. Thêm thư mục `bin` vào PATH của hệ thống
4. Kiểm tra cài đặt: `ab -V`

Để biết hướng dẫn cài đặt chi tiết, tìm kiếm các hướng dẫn "Apache Benchmark installation" cụ thể cho hệ điều hành của bạn.

## Best Practices (Thực Hành Tốt Nhất)

1. **Logic KeyResolver Tùy Chỉnh**: Triển khai KeyResolver dựa trên yêu cầu cụ thể của bạn (user ID, API key, địa chỉ IP, v.v.)
2. **Cấu Hình Rate Limit**: Điều chỉnh `replenishRate`, `burstCapacity` và `requestedTokens` dựa trên khả năng API và yêu cầu kinh doanh
3. **Giám Sát**: Giám sát hiệu suất Redis và các số liệu rate limiting trong production
4. **Xử Lý Lỗi**: Triển khai xử lý lỗi phù hợp và thông báo thân thiện với người dùng cho các request bị giới hạn tốc độ
5. **Tốc Độ Khác Nhau cho Mỗi Service**: Áp dụng các giới hạn tốc độ khác nhau cho các microservice khác nhau dựa trên mức độ quan trọng và khả năng tải

## Kết Luận

Rate Limiter pattern trong Spring Cloud Gateway cung cấp một cách hiệu quả để bảo vệ các microservice của bạn khỏi bị quá tải bởi quá nhiều request. Bằng cách tận dụng Redis và thuật toán token bucket, bạn có thể đảm bảo sử dụng công bằng và duy trì sự ổn định của service trong toàn bộ hệ thống phân tán.

## Các Pattern Liên Quan

- Circuit Breaker Pattern (cho accounts microservice)
- Retry Pattern (cho loans microservice)
- Load Balancing với Eureka
- Service Discovery

---

*Triển khai này đảm bảo rằng các microservice của bạn duy trì hiệu suất tối ưu trong khi ngăn chặn lạm dụng và đảm bảo phân phối tài nguyên công bằng cho tất cả người dùng.*