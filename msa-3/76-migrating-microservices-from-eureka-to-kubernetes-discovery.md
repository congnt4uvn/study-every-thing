# Chuyển đổi Microservices từ Eureka sang Kubernetes Discovery Server

## Tổng quan

Hướng dẫn này trình bày quy trình chuyển đổi các microservices Spring Boot từ Netflix Eureka Server sang Kubernetes Discovery Server tích hợp sẵn. Việc di chuyển này loại bỏ nhu cầu có một thành phần service discovery riêng biệt bằng cách tận dụng cơ chế service discovery có sẵn trong Kubernetes.

## Yêu cầu trước

- Kiến trúc microservices Spring Boot
- Kubernetes cluster
- Maven để quản lý dependencies
- Hiểu biết cơ bản về Spring Cloud và Kubernetes

## Thay đổi Kiến trúc

Khi chuyển từ Eureka sang Kubernetes Discovery:
- **Eureka Server**: Thành phần service registry riêng biệt (được loại bỏ)
- **Kubernetes Discovery**: DNS và service discovery tích hợp sẵn trong Kubernetes (native)
- **Service Communication**: Sử dụng tên service của Kubernetes thay vì tên application của Eureka

## Các bước Di chuyển

### 1. Accounts Microservice

#### Cập nhật Dependencies (pom.xml)

**Xóa dependency Eureka:**
```xml
<!-- Xóa dependency này -->
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
</dependency>
```

**Thêm dependency Kubernetes Discovery:**
```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-kubernetes-discovery-client</artifactId>
</dependency>
```

**Cập nhật Docker image tag:**
```xml
<tag>s17</tag>
```

#### Sửa Import HTTP Status

Sau khi xóa dependencies Eureka, cập nhật import HTTP status trong `CustomerController`:
```java
import org.apache.hc.core5.http.HttpStatus;
```

#### Kích hoạt Discovery Client

Thêm annotation vào class application chính (`AccountsApplication`):
```java
@EnableDiscoveryClient
public class AccountsApplication {
    // ... code hiện có
}
```

#### Cập nhật Cấu hình Application (application.yml)

**Xóa tất cả cấu hình Eureka:**
- Tìm kiếm và xóa tất cả các properties `eureka.*`

**Thêm cấu hình Kubernetes Discovery:**
```yaml
spring:
  cloud:
    kubernetes:
      discovery:
        all-namespaces: true
```

**Mục đích của `all-namespaces: true`:**
- Cho phép service discovery trên nhiều namespaces của Kubernetes
- Cần thiết khi microservices được triển khai trong các namespaces khác nhau
- Hỗ trợ sử dụng namespace mặc định nhưng cung cấp tính linh hoạt

#### Cập nhật Feign Clients

**Thay đổi CardsFeignClient và LoansFeignClient:**

Vấn đề với Kubernetes Discovery là không giống Eureka, không có tích hợp service registry tự động. Chúng ta cần cung cấp URL service một cách rõ ràng.

**Ví dụ CardsFeignClient:**
```java
@FeignClient(name = "cards", url = "http://cards:9000")
public interface CardsFeignClient {
    // ... các methods hiện có
}
```

**Ví dụ LoansFeignClient:**
```java
@FeignClient(name = "loans", url = "http://loans:8090")
public interface LoansFeignClient {
    // ... các methods hiện có
}
```

**Điểm chính:**
- `name`: Định danh application (giữ nguyên để nhất quán)
- `url`: Tên service và port của Kubernetes
- Định dạng: `http://<tên-service>:<port>`
- Chỉ hoạt động bên trong Kubernetes cluster
- Để test local, sử dụng URLs `localhost`

**Lưu ý về Load Balancing:**
- Feign client chuyển tiếp requests trực tiếp đến Kubernetes service
- Load balancing được xử lý bởi Kubernetes service, không phải client
- Không có load balancing phía client như với Eureka

### 2. Cards Microservice

#### Cập nhật Dependencies (pom.xml)

Thay thế dependency Eureka bằng Kubernetes Discovery:
```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-kubernetes-discovery-client</artifactId>
</dependency>
```

Cập nhật tag: `s14` → `s17`

#### Kích hoạt Discovery Client

Thêm annotation vào `CardsApplication`:
```java
@EnableDiscoveryClient
public class CardsApplication {
    // ... code hiện có
}
```

#### Cập nhật Cấu hình Application (application.yml)

Xóa tất cả properties Eureka và thêm:
```yaml
spring:
  cloud:
    kubernetes:
      discovery:
        all-namespaces: true
```

**Lưu ý:** Cards microservice không có tích hợp Feign client, nên không cần thay đổi thêm.

### 3. Loans Microservice

#### Cập nhật Cấu hình Application (application.yml)

Thêm cấu hình Kubernetes Discovery:
```yaml
spring:
  cloud:
    kubernetes:
      discovery:
        all-namespaces: true
```

#### Cập nhật Dependencies (pom.xml)

Xóa dependency Eureka và thêm Kubernetes Discovery client:
```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-kubernetes-discovery-client</artifactId>
</dependency>
```

Cập nhật tag: `s14` → `s17`

#### Kích hoạt Discovery Client

Thêm annotation vào `LoansApplication`:
```java
@EnableDiscoveryClient
public class LoansApplication {
    // ... code hiện có
}
```

### 4. Config Server

#### Thay đổi Tối thiểu

Config Server không tích hợp với Eureka, nên chỉ cần thay đổi tối thiểu:
- Cập nhật Docker image tag lên `s17` để nhất quán
- Không cần thay đổi dependency
- Không cần thay đổi cấu hình

### 5. Message Microservice

#### Thay đổi Tối thiểu

Message microservice cũng không có tích hợp Eureka:
- Cập nhật Docker image tag: `s14` → `s17`
- Không cần thay đổi khác

### 6. Gateway Server

**Lưu ý:** Các thay đổi cho Gateway server sẽ được trình bày trong phần/bài giảng tiếp theo.

## Tóm tắt Thay đổi

| Microservice | Dependencies | Cấu hình | Annotations | Feign Clients |
|--------------|-------------|-----------|-------------|---------------|
| Accounts | ✓ Đã cập nhật | ✓ Đã cập nhật | ✓ @EnableDiscoveryClient | ✓ Đã thêm URLs |
| Cards | ✓ Đã cập nhật | ✓ Đã cập nhật | ✓ @EnableDiscoveryClient | N/A |
| Loans | ✓ Đã cập nhật | ✓ Đã cập nhật | ✓ @EnableDiscoveryClient | N/A |
| Config Server | Chỉ tag | Không đổi | Không đổi | N/A |
| Message | Chỉ tag | Không đổi | Không đổi | N/A |
| Gateway | Đang chờ | Đang chờ | Đang chờ | N/A |

## Sự khác biệt chính: Eureka vs Kubernetes Discovery

### Eureka Discovery
- Yêu cầu triển khai Eureka Server riêng
- Load balancing phía client
- Đăng ký application với Eureka Server
- Service discovery thông qua Eureka client
- Hoạt động ngoài Kubernetes

### Kubernetes Discovery
- Sử dụng DNS tích hợp của Kubernetes
- Load balancing phía server (thông qua Kubernetes Service)
- Không cần discovery server riêng
- Service discovery thông qua Kubernetes API
- Chỉ hoạt động trong Kubernetes cluster

## Cân nhắc về Testing

### Trong Kubernetes Cluster
- Sử dụng tên service của Kubernetes (ví dụ: `http://cards:9000`)
- Phân giải DNS tự động
- Load balancing thông qua Kubernetes Service

### Phát triển Local (Ngoài Kubernetes)
- Tên service Kubernetes sẽ không phân giải được
- Sử dụng `localhost` hoặc URLs host thực tế
- Cân nhắc sử dụng profiles cho các môi trường khác nhau

## Best Practices

1. **Chiến lược Namespace**: Sử dụng `all-namespaces: true` cho cross-namespace discovery
2. **Đặt tên Service**: Giữ tên Kubernetes service nhất quán với tên application
3. **Cấu hình Port**: Ghi chú rõ ràng các ports của service
4. **Quản lý Tag**: Giữ đồng bộ Docker image tags giữa các services
5. **Testing**: Test cả trong cluster và môi trường phát triển local

## Xử lý Sự cố

### Các vấn đề thường gặp

**Vấn đề**: Feign client không thể phân giải tên service
- **Giải pháp**: Đảm bảo service đã được triển khai trong Kubernetes và URL được chỉ định đúng

**Vấn đề**: Lỗi import HTTP status sau khi xóa Eureka
- **Giải pháp**: Cập nhật import thành `org.apache.hc.core5.http.HttpStatus`

**Vấn đề**: Service discovery thất bại giữa các namespaces
- **Giải pháp**: Xác minh `all-namespaces: true` đã được cấu hình

## Các bước tiếp theo

- Hoàn thành di chuyển Gateway Server
- Triển khai các microservices đã cập nhật lên Kubernetes
- Xác minh giao tiếp giữa các services
- Giám sát hiệu suất service discovery

## Kết luận

Di chuyển từ Eureka sang Kubernetes Discovery đơn giản hóa kiến trúc microservices bằng cách tận dụng các khả năng tích hợp sẵn của Kubernetes. Điều này loại bỏ chi phí vận hành việc duy trì một service registry riêng biệt trong khi vẫn cung cấp service discovery mạnh mẽ trong hệ sinh thái Kubernetes.