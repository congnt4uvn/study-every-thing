# Chuyển Gateway Server sang Kubernetes Discovery

## Tổng Quan

Bài giảng này hướng dẫn cách chuyển đổi Gateway Server từ Eureka Discovery sang Kubernetes Discovery Server, bao gồm cập nhật các dependency cần thiết, thay đổi cấu hình và chuẩn bị triển khai.

## Bước 1: Cập Nhật Maven Dependencies

### Xóa Eureka Client Dependency

Mở file `pom.xml` và tìm dependency Eureka client cần được thay thế.

### Thêm Kubernetes Discovery Client

Thay thế dependency Eureka bằng Spring Cloud Kubernetes Discovery Client:

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-kubernetes-client-discovery</artifactId>
</dependency>
```

### Cập Nhật Version Tag

Tìm tag `s14` và cập nhật thành `s17`:

```xml
<tag>s17</tag>
```

Sau khi thực hiện các thay đổi này, tải lại Maven changes và thực hiện build.

## Bước 2: Cập Nhật Gateway Server Main Class

Điều hướng đến main class của Gateway Server (`GatewayserverApplication`).

### Thêm Discovery Client Annotation

Thêm annotation `@EnableDiscoveryClient` để kích hoạt service discovery:

```java
@EnableDiscoveryClient
@SpringBootApplication
public class GatewayserverApplication {
    // ...
}
```

### Cập Nhật URI Routing Configurations

#### Cấu Hình Hiện Tại (Dựa trên Eureka)

Cấu hình routing hiện tại sử dụng load balancer URIs:
- `lb://ACCOUNTS`
- `lb://LOANS`
- `lb://CARDS`

Tiền tố `lb` chỉ định Spring Cloud Load Balancer, thực hiện load balancing phía client tại Gateway Server.

#### Cấu Hình Mới (Dựa trên Kubernetes)

Vì chúng ta không còn sử dụng Eureka nữa, hãy cập nhật các URI để sử dụng URL service trực tiếp:

**Accounts Service:**
```
http://accounts:8080
```

**Loans Service:**
```
http://loans:8090
```

**Cards Service:**
```
http://cards:9000
```

**Lợi Ích Chính:** Các cấu hình này sử dụng tên service của Kubernetes (accounts, loans, cards) mà không cần hardcode hostname hoặc domain name. Miễn là các microservices được triển khai với tên service khớp, tích hợp Gateway Server sẽ hoạt động liền mạch.

## Bước 3: Cập Nhật Cấu Hình application.yml

### Xóa Các Properties Của Eureka

Xóa các properties liên quan đến Eureka server sau:

```yaml
spring:
  cloud:
    gateway:
      discovery:
        locator:
          enabled: true
          lowerCaseServiceId: true
```

### Thêm Kubernetes Discovery Properties

Thêm các properties đặc thù cho Kubernetes:

```yaml
spring:
  cloud:
    kubernetes:
      discovery:
        enabled: true
        all-namespaces: true
    discovery:
      client:
        health-indicator:
          enabled: false
```

#### Giải Thích Các Properties

**`spring.cloud.kubernetes.discovery.enabled: true`**
- Yêu cầu Gateway Server tận dụng Kubernetes discovery server để định tuyến request đến các microservices (accounts, cards, loans)

**`spring.cloud.kubernetes.discovery.all-namespaces: true`**
- Kích hoạt service discovery trên tất cả các namespace của Kubernetes

**`spring.cloud.discovery.client.health-indicator.enabled: false`**
- Vô hiệu hóa health indicator bean mặc định
- **Tại sao cần thiết:** Điều này ngăn chặn một vấn đề đã biết khi thư viện Kubernetes discovery client không thể tạo bean cần thiết
- **Trạng thái:** Đây là giải pháp tạm thời cho một issue đang mở trên GitHub của dự án Spring Cloud Kubernetes
- **Tương lai:** Property này có thể được xóa bỏ khi issue được giải quyết bởi team Spring Cloud Kubernetes

> **Lưu ý:** Các properties bổ sung này được yêu cầu đặc biệt cho Gateway Server vì nó hoạt động như một edge server chịu trách nhiệm xử lý tất cả traffic đến.

## Bước 4: Build và Deploy

### Tạo Docker Images

Tạo Docker images cho tất cả microservices với tag `s17`:

```bash
docker build -t <service-name>:s17 .
```

Điều này sẽ được thực hiện cho tất cả các microservices.

### Chuẩn Bị Kubernetes Cluster

Thiết lập Kubernetes cluster với tất cả các thành phần cần thiết:
- Apache Kafka
- Keycloak
- Grafana
- Prometheus

### Cập Nhật Helm Charts

Cập nhật Helm charts của Easy Bank với tag name mới nhất (`s17`):

```yaml
image:
  tag: s17
```

### Triển Khai Microservices

Sử dụng Helm charts đã cập nhật để triển khai tất cả microservices lên Kubernetes cluster:

```bash
helm upgrade --install <release-name> <chart-path>
```

## Tóm Tắt

Quá trình chuyển đổi này bao gồm:

1. ✅ Thay thế Eureka client dependency bằng Kubernetes discovery client
2. ✅ Cập nhật version tags từ s14 lên s17
3. ✅ Thêm annotation `@EnableDiscoveryClient`
4. ✅ Thay thế load balancer URIs bằng Kubernetes service URLs trực tiếp
5. ✅ Xóa các properties cấu hình đặc thù của Eureka
6. ✅ Thêm các properties cấu hình Kubernetes discovery
7. ✅ Áp dụng giải pháp tạm thời cho health indicator do issue đã biết
8. ✅ Build Docker images với tag s17
9. ✅ Cập nhật và triển khai Helm charts

## Những Điểm Chính Cần Nhớ

- **Không Load Balancing Phía Client:** Kubernetes xử lý service discovery và load balancing một cách native
- **Service Name Resolution:** Sử dụng tên service của Kubernetes để tích hợp liền mạch
- **Cấu Hình Edge Server:** Gateway Server yêu cầu các properties discovery bổ sung
- **Giải Pháp Tạm Thời Cho Issue Đã Biết:** Health indicator phải được tạm thời vô hiệu hóa
- **Triển Khai Dựa Trên Helm:** Đơn giản hóa việc triển khai microservices bằng Helm charts

## Các Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ xác minh việc triển khai và kiểm tra toàn bộ thiết lập microservices trong Kubernetes cluster.