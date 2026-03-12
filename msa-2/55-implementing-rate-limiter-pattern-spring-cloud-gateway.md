# Triển khai Rate Limiter Pattern với Spring Cloud Gateway

## Tổng quan

Hướng dẫn này giải thích cách triển khai rate limiter pattern sử dụng Spring Cloud Gateway để kiểm soát và giới hạn số lượng requests có thể được xử lý bởi các microservices của bạn.

## Rate Limiter Pattern là gì?

Rate limiting là một kỹ thuật được sử dụng để kiểm soát tốc độ xử lý requests. Khi triển khai với Spring Cloud Gateway, nó xác định liệu một request hiện tại có được phép tiếp tục hay nên bị chặn. Nếu một request vượt quá giới hạn được định nghĩa, mã trạng thái HTTP 429 (Too Many Requests - Quá nhiều yêu cầu) sẽ được trả về theo mặc định.

## Các trường hợp sử dụng Rate Limiting

Theo kinh nghiệm triển khai của Stripe, rate limiting là cần thiết cho một số kịch bản sau:

1. **Bảo vệ khỏi Traffic Spike**: Một user duy nhất gây ra tăng đột biến traffic và ảnh hưởng đến tất cả users khác
2. **Scripts hoạt động sai**: Một user có script vô tình gửi quá nhiều requests
3. **Tấn công có chủ ý**: Một user cố ý cố gắng làm quá tải servers của bạn
4. **Quản lý ưu tiên**: Requests có độ ưu tiên thấp không nên ảnh hưởng đến traffic có độ ưu tiên cao
5. **Suy giảm hệ thống**: Khi xảy ra sự cố nội bộ, loại bỏ các requests có độ ưu tiên thấp để duy trì các hoạt động quan trọng

## Hiểu về KeyResolver

`KeyResolver` là một thành phần quan trọng xác định tiêu chí để thực thi giới hạn rate. Bạn có thể triển khai rate limiting dựa trên:

- **User**: Giới hạn requests cho từng người dùng
- **Session**: Giới hạn requests cho từng phiên làm việc
- **IP Address**: Giới hạn requests cho từng địa chỉ IP
- **Server**: Giới hạn requests cho từng server

### Triển khai mặc định

Spring cung cấp triển khai mặc định `PrincipalNameKeyResolver` hoạt động với Spring Security. Nó lấy username của người dùng hiện đang đăng nhập để thực thi giới hạn rate theo từng user.

**Quan trọng**: Nếu `KeyResolver` không tìm thấy key, các requests sẽ bị từ chối theo mặc định. Hành vi này có thể được điều chỉnh thông qua các thuộc tính cấu hình.

## Triển khai dựa trên Redis

Spring Cloud Gateway sử dụng Redis làm hệ thống lưu trữ cơ bản để triển khai rate limiting. Triển khai này dựa trên công việc được thực hiện bởi đội ngũ Stripe.

### Dependency cần thiết

Thêm dependency sau vào `pom.xml` của bạn:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis-reactive</artifactId>
</dependency>
```

## Thuật toán Token Bucket

Rate limiter sử dụng **Thuật toán Token Bucket** với ba thuộc tính chính:

### 1. ReplenishRate

Xác định số lượng requests được phép mỗi giây (tốc độ mà tokens được thêm vào bucket).

- **Ví dụ**: Nếu `replenishRate = 100`, thì 100 tokens được thêm vào bucket mỗi giây
- Sau 2 giây mà không có tiêu thụ, bucket sẽ có 200 tokens

### 2. BurstCapacity

Xác định số lượng tokens tối đa mà bucket có thể chứa (ngăn chặn việc tràn đầy).

- **Ví dụ**: Nếu `burstCapacity = 200`, bucket không thể chứa nhiều hơn 200 tokens
- Các tokens thừa từ `replenishRate` sẽ bị loại bỏ khi bucket đã đầy

### 3. RequestedTokens

Xác định số lượng tokens mà mỗi request tiêu thụ.

- **Mặc định**: 1 token cho mỗi request
- Có thể được điều chỉnh dựa trên độ phức tạp hoặc độ ưu tiên của request

## Các ví dụ cấu hình

### Tốc độ ổn định (Không có Bursting)

Đặt `replenishRate` và `burstCapacity` cùng một giá trị:

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: my-service
          filters:
            - name: RequestRateLimiter
              args:
                redis-rate-limiter.replenishRate: 100
                redis-rate-limiter.burstCapacity: 100
                redis-rate-limiter.requestedTokens: 1
```

Cấu hình này thêm 100 tokens mỗi giây, và các tokens không sử dụng sẽ bị loại bỏ.

### Cho phép Bursts tạm thời

Đặt `burstCapacity` cao hơn `replenishRate`:

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: my-service
          filters:
            - name: RequestRateLimiter
              args:
                redis-rate-limiter.replenishRate: 100
                redis-rate-limiter.burstCapacity: 200
                redis-rate-limiter.requestedTokens: 1
```

Điều này cho phép users tích lũy tokens và sử dụng tới 200 requests trong một burst.

### Một Request mỗi Phút

Để chỉ cho phép một request mỗi phút:

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: my-service
          filters:
            - name: RequestRateLimiter
              args:
                redis-rate-limiter.replenishRate: 1
                redis-rate-limiter.burstCapacity: 60
                redis-rate-limiter.requestedTokens: 60
```

**Giải thích**:
- `replenishRate = 1`: Thêm 1 token mỗi giây (60 tokens mỗi phút)
- `burstCapacity = 60`: Tối đa 60 tokens trong bucket
- `requestedTokens = 60`: Mỗi request tiêu thụ 60 tokens

Kết quả: Chỉ có thể thực hiện 1 request mỗi phút.

## Triển khai KeyResolver tùy chỉnh

Bạn có thể tạo một bean `KeyResolver` tùy chỉnh để xác định tiêu chí giới hạn rate của mình:

```java
@Bean
public KeyResolver userKeyResolver() {
    return exchange -> Mono.just(
        exchange.getRequest()
                .getQueryParams()
                .getFirst("user")
    );
}
```

Ví dụ này trích xuất user từ một query parameter để thực thi giới hạn rate theo từng user.

## Cấu hình dựa trên Java

Thay vì YAML, bạn có thể cấu hình rate limiting sử dụng Java:

```java
@Bean
public RouteLocator customRouteLocator(RouteLocatorBuilder builder) {
    return builder.routes()
        .route("rate_limited_route", r -> r.path("/api/**")
            .filters(f -> f.requestRateLimiter(c -> c
                .setRateLimiter(redisRateLimiter())
                .setKeyResolver(userKeyResolver())))
            .uri("lb://MY-SERVICE"))
        .build();
}
```

## Lưu ý quan trọng

⚠️ **Cảnh báo**: Đặt `burstCapacity = 0` sẽ chặn tất cả các requests. Đảm bảo giá trị này luôn lớn hơn 0 để rate limiting hoạt động bình thường.

## Các bước tiếp theo

Trong các phần tiếp theo, chúng ta sẽ triển khai rate limiter pattern này trong Gateway Server với các ví dụ thực tế và trình bày cách cấu hình dựa trên các yêu cầu kinh doanh khác nhau.

## Tóm tắt

- Rate limiting bảo vệ microservices của bạn khỏi traffic spikes và các cuộc tấn công
- Thuật toán Token Bucket cung cấp rate limiting linh hoạt với ba tham số chính
- Redis cung cấp bộ nhớ lưu trữ cho distributed rate limiting
- KeyResolver xác định tiêu chí để áp dụng giới hạn rate
- Cấu hình có thể được thực hiện thông qua YAML hoặc các phương pháp dựa trên Java