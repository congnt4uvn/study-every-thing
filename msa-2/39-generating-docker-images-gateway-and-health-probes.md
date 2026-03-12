# Tạo Docker Images cho Gateway Server và Cấu hình Health Probes

## Tổng quan

Hướng dẫn này bao gồm quy trình xây dựng Docker images cho các microservices trong Phần 9, bao gồm cấu hình health probes cho Edge server (API Gateway) và tạo Docker images sử dụng Maven và Jib.

## Yêu cầu trước

- Các dự án microservices đã hoàn thành (accounts, loans, cards, config server, Eureka server, gateway server)
- Docker Desktop đã được cài đặt và đang chạy
- Maven đã được cài đặt
- Tài khoản Docker Hub (để push images)

## Bước 1: Kích hoạt Health Probes trong Microservices

Trước khi tạo Docker images, chúng ta cần kích hoạt các endpoints liên quan đến health (readiness và liveness probes) trong các microservices accounts, loans và cards. Điều này rất quan trọng để Docker Compose quản lý đúng các phụ thuộc của service.

### Tại sao cần Health Probes?

Gateway server chỉ nên khởi động sau khi các microservices accounts, cards và loans đã hoạt động tốt và khỏe mạnh. Health probes cho phép Docker Compose kiểm tra tình trạng health của service trước khi khởi động các services phụ thuộc.

### Các bước cấu hình

#### 1. Microservice Accounts

Trong file `application.yml`, thêm các thuộc tính sau:

**Dưới `management.endpoints`:**
```yaml
management:
  endpoints:
    web:
      exposure:
        include: "*"
    shutdown:
      enabled: true
    health:
      probes:
        enabled: true
```

**Thêm cấu hình health:**
```yaml
management:
  health:
    readinessstate:
      enabled: true
    livenessstate:
      enabled: true
```

#### 2. Microservice Cards

Áp dụng cùng cấu hình trong `cards/application.yml`:

- Thêm health probes enabled dưới `management.endpoints`
- Thêm cấu hình readiness và liveness state dưới `management.health`

#### 3. Microservice Loans

Áp dụng cùng cấu hình trong `loans/application.yml`:

- Thêm health probes enabled dưới `management.endpoints`
- Thêm cấu hình readiness và liveness state dưới `management.health`

## Bước 2: Chuẩn bị cho việc tạo Docker Image

### Kiểm tra cấu hình POM

Trước khi build Docker images, đảm bảo tất cả các microservices có tag đúng trong file `pom.xml`:

```xml
<image>
    <name>docker.io/yourusername/${project.artifactId}:s9</name>
</image>
```

Tag nên là `s9` để chỉ ra images của Phần 9.

### Làm sạch môi trường Docker

1. Mở Docker Desktop
2. Xóa bất kỳ images microservice hiện có nào
3. Đảm bảo không có containers liên quan đang chạy

## Bước 3: Build Docker Images với Maven và Jib

Điều hướng đến từng thư mục microservice và chạy lệnh Maven để build Docker images sử dụng Jib.

### Cú pháp lệnh

```bash
mvn compile jib:dockerBuild
```

**Lưu ý:** Chữ 'B' trong dockerBuild phải viết hoa.

### Trình tự Build

#### 1. Microservice Accounts

```bash
cd section9/accounts
mvn compile jib:dockerBuild
```

#### 2. Microservice Loans

```bash
cd ../loans
mvn compile jib:dockerBuild
```

#### 3. Microservice Cards

```bash
cd ../cards
mvn compile jib:dockerBuild
```

#### 4. Config Server

```bash
cd ../configserver
mvn compile jib:dockerBuild
```

#### 5. Eureka Server

```bash
cd ../eurekaserver
mvn compile jib:dockerBuild
```

#### 6. Gateway Server

```bash
cd ../gatewayserver
mvn compile jib:dockerBuild
```

### Ưu điểm của Jib

- **Build nhanh:** Jib tạo Docker images nhanh hơn nhiều so với Buildpacks
- **Không cần Docker daemon:** Có thể build mà không cần Docker đang chạy
- **Phân lớp hiệu quả:** Tối ưu hóa layer caching để rebuild nhanh hơn

Buildpacks thường mất ít nhất 1 phút mỗi image, trong khi Jib hoàn thành trong vài giây.

## Bước 4: Xác minh Docker Images

### Sử dụng Command Line

```bash
docker images
```

Tìm 6 images với tag `s9`:
1. accounts:s9
2. loans:s9
3. cards:s9
4. configserver:s9
5. eurekaserver:s9
6. gatewayserver:s9

### Sử dụng Docker Desktop

1. Mở Docker Desktop
2. Điều hướng đến phần Images
3. Tìm kiếm images với tag `s9`
4. Xác minh tất cả 6 images đều có mặt

## Bước 5: Push Images lên Docker Hub

Để chia sẻ images của bạn hoặc triển khai chúng đến các môi trường khác, push chúng lên Docker Hub.

### Cú pháp lệnh Push

```bash
docker image push docker.io/yourusername/imagename:s9
```

### Ví dụ: Push Microservice Accounts

```bash
docker image push docker.io/eazybytes/accounts:s9
```

### Push tất cả Images

Lặp lại lệnh cho từng microservice:

```bash
docker image push docker.io/yourusername/accounts:s9
docker image push docker.io/yourusername/loans:s9
docker image push docker.io/yourusername/cards:s9
docker image push docker.io/yourusername/configserver:s9
docker image push docker.io/yourusername/eurekaserver:s9
docker image push docker.io/yourusername/gatewayserver:s9
```

## Các bước tiếp theo

1. Cập nhật file Docker Compose để bao gồm cấu hình gateway server
2. Định nghĩa các phụ thuộc service sử dụng health checks
3. Kiểm tra toàn bộ mạng microservices với Docker containers
4. Xác minh routing và filtering của gateway server

## Best Practices (Thực hành tốt nhất)

- **Tạo Image thường xuyên:** Build Docker images tại các mốc quan trọng để dễ dàng kiểm tra
- **Quản lý Tag:** Sử dụng tags mô tả (như số phần) để kiểm soát phiên bản
- **GitHub Repository:** Lưu trữ các lệnh Maven trong repository của bạn
- **Môi trường sạch:** Xóa các images cũ trước khi build images mới để tránh xung đột

## Tóm tắt

Trong hướng dẫn này, chúng ta đã:
- Kích hoạt health probes trong các microservices accounts, loans và cards
- Cấu hình readiness và liveness endpoints để kiểm tra health của service
- Tạo Docker images cho tất cả 6 microservices sử dụng Maven và Jib
- Xác minh việc tạo image trong Docker Desktop
- Push images lên Docker Hub để phân phối

Các bước này chuẩn bị microservices của bạn cho việc triển khai container hóa và cho phép quản lý phụ thuộc đúng cách trong Docker Compose.