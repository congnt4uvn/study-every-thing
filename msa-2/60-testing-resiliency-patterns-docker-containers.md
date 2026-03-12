# Kiểm Tra Các Mẫu Thiết Kế Khả Năng Phục Hồi trong Docker Containers

## Tổng Quan

Hướng dẫn này bao gồm việc kiểm tra các mẫu thiết kế khả năng phục hồi (resiliency patterns) trong microservices sử dụng Docker containers, bao gồm các pattern RateLimiter, Circuit Breaker và Retry với Spring Cloud Gateway và tích hợp Redis.

## Yêu Cầu Trước Khi Bắt Đầu

- Đã cài đặt Docker và Docker Compose
- Tài khoản Docker Hub để push images
- Tất cả microservices đã cập nhật dependencies
- Redis service cho RateLimiter pattern

## Xây Dựng Docker Images

### Cập Nhật Cấu Hình Maven

Trước khi tạo Docker images, cập nhật file `pom.xml` trong tất cả microservices:

- Thay đổi tag từ `S9` sang `S10`
- Điều này đảm bảo việc quản lý phiên bản đúng cho section mới

### Tạo Images với Google Jib

Sử dụng lệnh sau để tạo Docker images:

```bash
# Lệnh tạo Docker images với Google Jib
mvn clean compile jib:dockerBuild
```

### Đẩy Images lên Docker Hub

Sau khi build images, push chúng lên Docker Hub:

```bash
# Lệnh push Docker images
docker push <ten-dockerhub-cua-ban>/<ten-image>:s10
```

Xác minh images đã có trên Docker Hub bằng cách kiểm tra repository của bạn. Tất cả microservices phải có tag `s10`.

## Cấu Hình Docker Compose

### Thêm Redis Service

Redis là bắt buộc để triển khai RateLimiter pattern với Spring Cloud Gateway.

**Cấu Hình Docker Compose:**

```yaml
redis:
  image: redis
  ports:
    - "6379:6379"
  healthcheck:
    test: ["CMD", "redis-cli", "ping"]
    timeout: 10s
    retries: 10
  extends:
    file: common-config.yml
    service: network-deploy-service
```

**Chi Tiết Cấu Hình:**
- **Tên Service:** redis
- **Image:** Redis image chính thức
- **Port Mapping:** 6379:6379
- **Health Check:** Sử dụng lệnh `redis-cli ping`
- **Network:** Mở rộng từ easybank network trong common-config

### Cấu Hình Gateway Server

Gateway Server yêu cầu cấu hình bổ sung cho tích hợp Redis.

**Dependencies:**

Thêm Redis dependency vào Gateway Server. Gateway Server có nhiều dependencies và nên khởi động sau các service khác.

**Biến Môi Trường:**

```yaml
environment:
  SPRING_DATA_REDIS_CONNECT_TIMEOUT: 2s
  SPRING_DATA_REDIS_HOST: redis
  SPRING_DATA_REDIS_PORT: 6379
  SPRING_DATA_REDIS_TIMEOUT: 1s
```

**Lưu Ý Quan Trọng:**
- Sử dụng tên service `redis` thay vì `localhost` cho host
- Cấu hình các giá trị timeout phù hợp
- Cập nhật image tag thành `s10`

### Cập Nhật Profiles

Sau khi cập nhật Docker Compose file cho production:
- Sao chép cùng cấu hình sang QA profile
- Sao chép cùng cấu hình sang default profile
- Không cần thay đổi trong `common-config.yml`

## Triển Khai và Kiểm Tra

### Khởi Động Containers

Di chuyển đến thư mục production profile và thực thi:

```bash
docker compose up -d
```

Lệnh này khởi động tất cả containers ở chế độ detached. Quá trình mất khoảng 1-2 phút.

### Xác Minh Triển Khai

**Kiểm Tra Docker Desktop:**
1. Mở Docker Desktop
2. Điều hướng đến logs của Gateway Server
3. Xác nhận message: "GatewayserverApplication started successfully"

**Kiểm Tra Trạng Thái Container:**

```bash
docker ps
```

Xác minh tất cả sáu services đang chạy với trạng thái healthy.

## Kiểm Tra Các Resiliency Patterns

### Kiểm Tra RateLimiter trong Accounts Microservice

**API Endpoint:**

```
GET http://localhost:8072/easybank/accounts/api/java-version
```

**Kiểm Tra Request Đơn:**
- Gửi một request đơn
- Kết quả mong đợi: Thông tin phiên bản Java (ví dụ: "Java 17")

**Kiểm Tra Nhiều Requests:**
- Gửi nhiều requests trong vòng một giây
- Kết quả mong đợi: Cơ chế fallback được kích hoạt
- Response cho biết đã vượt quá giới hạn rate

### Kiểm Tra RateLimiter trong Gateway Server

Sử dụng Apache Benchmark để kiểm tra RateLimiter pattern với RedisRateLimiter.

**Lệnh:**

```bash
ab -n 10 -c 2 http://localhost:8072/easybank/accounts/api/contact-info
```

**Kết Quả Mong Đợi:**
- Tổng requests: 10
- Failed requests: 8 (xấp xỉ)
- HTTP Status: 429 Too Many Requests
- Điều này xác nhận rate limiter hoạt động đúng

### Kiểm Tra Các Patterns Khác

**Circuit Breaker và Retry Patterns:**

Mặc dù các patterns này đã được triển khai và kiểm tra locally, việc kiểm tra chúng trong Docker yêu cầu:
- Cố ý tạo RuntimeExceptions
- Tạo lại Docker images với test code

Vì các patterns này đã được xác minh trong môi trường local, chúng sẽ hoạt động tương tự trong Docker containers.

## Thực Hành Tốt Nhất

### Cấu Hình Rate Limiting

- Cấu hình các giới hạn rate phù hợp dựa trên nhu cầu ứng dụng
- Triển khai cơ chế fallback để có trải nghiệm người dùng tốt hơn
- Giám sát các metrics về rate limit trong production

### Quản Lý Docker Image

- Sử dụng tags có ý nghĩa cho versioning (ví dụ: s10 cho section 10)
- Giữ Docker Hub repository được tổ chức tốt
- Ghi chép các thay đổi giữa các phiên bản

### Chiến Lược Kiểm Tra

- Kiểm tra trong môi trường local trước
- Xác thực với Docker containers trước khi production
- Sử dụng các công cụ như Apache Benchmark cho load testing
- Giám sát logs và health checks

## Code Repository

Tất cả các thay đổi code cho section này có sẵn trong GitHub repository:

**Repository:** microservices
**Branch/Tag:** section_10

Xem xét repository để tìm:
- Cấu hình Docker Compose hoàn chỉnh
- Code microservice đã cập nhật
- Configuration files cho tất cả profiles

## Khắc Phục Sự Cố

### Các Vấn Đề Thường Gặp

**Vấn Đề Kết Nối Redis:**
- Xác minh Redis container đang chạy
- Kiểm tra cấu hình network
- Đảm bảo hostname đúng (sử dụng tên service, không phải localhost)

**Rate Limiter Không Hoạt Động:**
- Xác nhận Redis dependency đã được thêm
- Kiểm tra environment variables trong Gateway Server
- Xác minh Redis có thể truy cập từ Gateway

**Vấn Đề Khởi Động Container:**
- Kiểm tra thứ tự dependency trong Docker Compose
- Xem xét cấu hình health check
- Kiểm tra container logs để tìm lỗi

## Tóm Tắt

Trong section này, chúng ta đã:

1. **Build và Deploy:** Tạo Docker images với tag `s10` và push lên Docker Hub
2. **Cấu Hình Redis:** Thêm Redis service để hỗ trợ RateLimiter pattern
3. **Cập Nhật Gateway:** Cấu hình Spring Cloud Gateway với tích hợp Redis
4. **Kiểm Tra Patterns:** Xác thực chức năng RateLimiter trong cả Accounts microservice và Gateway Server
5. **Xác Minh Triển Khai:** Xác nhận tất cả services chạy thành công trong môi trường Docker

Các microservices hiện tại đã trưởng thành hơn và có khả năng chịu lỗi tốt hơn với các resiliency patterns được triển khai hoạt động đúng trong môi trường container hóa.

## Các Bước Tiếp Theo

- Nghỉ ngơi để tiếp thu các khái niệm đã học
- Đừng vội vàng xem hết tài liệu khóa học
- Thực hành triển khai các patterns này trong dự án của riêng bạn
- Chuyển sang section tiếp theo khi đã sẵn sàng

---

**Quan Trọng:** Học các khái niệm phức tạp cần thời gian và nghỉ ngơi. Đừng cố gắng hoàn thành mọi thứ trong một lần. Hãy nghỉ ngơi, thực hành, và quay lại với tinh thần sảng khoái cho section tiếp theo.