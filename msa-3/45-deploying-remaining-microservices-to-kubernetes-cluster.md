# Triển Khai Các Microservices Còn Lại Lên Kubernetes Cluster

## Tổng Quan

Hướng dẫn này giải thích quy trình triển khai tất cả các microservices còn lại vào Kubernetes cluster. Chúng ta sẽ tìm hiểu cách chuẩn bị các file manifest Kubernetes và thứ tự triển khai phù hợp để đảm bảo tất cả services hoạt động ăn khớp với nhau.

## Yêu Cầu Trước Khi Bắt Đầu

- Kubernetes cluster đã được cài đặt (Docker Desktop hoặc tương tự)
- Hiểu biết cơ bản về các khái niệm Kubernetes (Deployments, Services, ConfigMaps)
- Các microservices đã được build và có sẵn dưới dạng Docker images

## Thứ Tự Triển Khai

Để triển khai microservices vào một cluster mới, hãy tuân theo thứ tự cụ thể sau:

1. **Keycloak** (Authentication Server - Máy chủ xác thực)
2. **ConfigMap** (Lưu trữ cấu hình)
3. **Config Server** (Cấu hình tập trung)
4. **Eureka Server** (Service discovery - Phát hiện dịch vụ)
5. **Accounts Microservice** (Microservice tài khoản)
6. **Loans Microservice** (Microservice khoản vay)
7. **Cards Microservice** (Microservice thẻ)
8. **Gateway Server** (API Gateway - Cổng API)

## Cấu Trúc File Manifest Kubernetes

Tất cả các file manifest được tổ chức với tiền tố số (1, 2, 3, 4, 5, 6, 7, 8) để chỉ ra thứ tự triển khai. Quy ước đặt tên này giúp dễ dàng triển khai các services theo đúng trình tự.

## Triển Khai Keycloak

### Cấu Hình Deployment

Deployment của Keycloak bao gồm:

- **Label**: `keycloak`
- **Replicas**: 1
- **Container Image**: Keycloak image chính thức
- **Chế độ khởi động**: Development mode (`start-dev`)

### Biến Môi Trường

Keycloak yêu cầu hai biến môi trường quan trọng được inject từ ConfigMap:

```yaml
env:
  - name: KEYCLOAK_ADMIN
    valueFrom:
      configMapKeyRef:
        name: easybank-configmap
        key: KEYCLOAK_ADMIN
  - name: KEYCLOAK_ADMIN_PASSWORD
    valueFrom:
      configMapKeyRef:
        name: easybank-configmap
        key: KEYCLOAK_ADMIN_PASSWORD
```

### Cấu Hình Service

- **Loại**: LoadBalancer
- **Cổng External**: 7080
- **Target Port**: 8080 (cổng container)

## Triển Khai Eureka Server

### Điểm Chính

- **Image Tag**: `s12` (phiên bản Section 12)
- Sử dụng tag Section 12 để tránh phụ thuộc vào Kafka/RabbitMQ từ Sections 13-14
- Đơn giản hóa việc triển khai bằng cách tập trung vào các microservices cốt lõi

### Biến Môi Trường

```yaml
env:
  - name: SPRING_APPLICATION_NAME
    valueFrom:
      configMapKeyRef:
        name: easybank-configmap
        key: EUREKA_APPLICATION_NAME
  - name: SPRING_CONFIG_IMPORT
    valueFrom:
      configMapKeyRef:
        name: easybank-configmap
        key: SPRING_CONFIG_IMPORT
```

- **Application Name**: Lấy từ ConfigMap dưới key `EUREKA_APPLICATION_NAME`
- **Config Server URL**: Trỏ đến `config-server:8071`

### Cấu Hình Service

- **Loại**: LoadBalancer
- Cho phép truy cập từ bên ngoài để giám sát service registry

## Triển Khai Accounts Microservice

### Cấu Hình

- **Image Tag**: `s12`
- Bao gồm tất cả các thông số deployment tiêu chuẩn

### Biến Môi Trường

Biến môi trường quan trọng cho service discovery:

```yaml
- name: EUREKA_CLIENT_SERVICEURL_DEFAULTZONE
  valueFrom:
    configMapKeyRef:
      name: easybank-configmap
      key: EUREKA_CLIENT_SERVICEURL_DEFAULTZONE
```

Điều này cho phép Accounts microservice đăng ký với Eureka Server.

### Cấu Hình Service

- **Loại**: LoadBalancer
- Expose microservice để truy cập từ bên ngoài

## Loans và Cards Microservices

Cả hai đều tuân theo cùng pattern như Accounts microservice:

- Sử dụng image tag `s12`
- Inject biến môi trường từ ConfigMap
- Đăng ký với Eureka Server
- Expose dưới dạng LoadBalancer services

## Triển Khai Gateway Server

### Cấu Hình Đặc Biệt

Gateway Server yêu cầu thêm một biến môi trường cho tích hợp OAuth2:

```yaml
- name: SPRING_SECURITY_OAUTH2_RESOURCESERVER_JWT_JWK_SET_URI
  valueFrom:
    configMapKeyRef:
      name: easybank-configmap
      key: SPRING_SECURITY_OAUTH2_RESOURCESERVER_JWT_JWK_SET_URI
```

URL này trỏ đến certificate endpoint của Keycloak để xác thực JWT.

### Image Tag

- Sử dụng phiên bản `s12` để nhất quán với các microservices khác

## Best Practices Cho ConfigMap

### Quy Ước Đặt Tên Key

- Sử dụng tên key mô tả rõ ràng trong ConfigMap (ví dụ: `EUREKA_APPLICATION_NAME`)
- Tên biến môi trường trong deployment phải khớp với yêu cầu của Spring Boot
- Key trong ConfigMap có thể sử dụng tên tùy chỉnh để tổ chức tốt hơn

### Cấu Trúc Ví Dụ

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: easybank-configmap
data:
  KEYCLOAK_ADMIN: "admin"
  KEYCLOAK_ADMIN_PASSWORD: "admin"
  EUREKA_APPLICATION_NAME: "eurekaserver"
  SPRING_CONFIG_IMPORT: "configserver:http://config-server:8071/"
  EUREKA_CLIENT_SERVICEURL_DEFAULTZONE: "http://eureka-server:8070/eureka/"
```

## Pattern Triển Khai Chung

Tất cả microservices tuân theo pattern tiêu chuẩn này:

1. **Deployment Object**
   - Định nghĩa metadata với labels
   - Đặt số lượng replica
   - Chỉ định selector khớp với labels
   - Cấu hình thông số container
   - Inject biến môi trường từ ConfigMap
   - Định nghĩa các container ports

2. **Service Object**
   - Khớp deployment labels với service selector
   - Đặt loại service (LoadBalancer)
   - Map external port với target port (container port)

## Cấu Hình Port

### Lưu Ý Quan Trọng

- **Container Port**: Cổng mà ứng dụng chạy bên trong container
- **Target Port**: Phải khớp với container port
- **External Port**: Cổng được expose cho clients bên ngoài qua LoadBalancer

### Ví Dụ

```yaml
ports:
  - containerPort: 8080  # Cổng container nội bộ
---
ports:
  - port: 7080           # Cổng external
    targetPort: 8080     # Phải khớp với containerPort
```

## Các Lệnh Triển Khai

Apply các manifest files theo thứ tự:

```bash
kubectl apply -f 1-keycloak.yaml
kubectl apply -f 2-configmaps.yaml
kubectl apply -f 3-configserver.yaml
kubectl apply -f 4-eurekaserver.yaml
kubectl apply -f 5-accounts.yaml
kubectl apply -f 6-loans.yaml
kubectl apply -f 7-cards.yaml
kubectl apply -f 8-gateway.yaml
```

## Các Bước Xác Thực

Sau khi triển khai, xác thực từng service:

```bash
# Kiểm tra deployments
kubectl get deployments

# Kiểm tra services
kubectl get services

# Kiểm tra pods
kubectl get pods

# Xem logs
kubectl logs <pod-name>
```

## Tại Sao Sử Dụng Images Section 12?

Quyết định sử dụng image tags `s12` thay vì `s14`:

- **Section 13-14**: Bao gồm kiến trúc event-driven với RabbitMQ/Kafka
- **Section 15**: Tập trung vào triển khai microservices cơ bản
- **Đơn giản hóa**: Tránh độ phức tạp bổ sung của message broker setup
- **Cải tiến tương lai**: Helm charts (các sections sắp tới) sẽ đơn giản hóa setup event-driven

## Tóm Tắt

Chiến lược triển khai này đảm bảo:

- **Trình tự đúng đắn**: Services triển khai theo thứ tự phụ thuộc
- **Quản lý cấu hình**: Tập trung qua ConfigMap
- **Service Discovery**: Tất cả microservices đăng ký với Eureka
- **Bảo mật**: Tích hợp OAuth2 với Keycloak
- **Khả năng mở rộng**: LoadBalancer services cho phép truy cập từ bên ngoài

Bằng cách tuân theo phương pháp có cấu trúc này, bạn có thể triển khai đáng tin cậy toàn bộ kiến trúc microservices lên bất kỳ Kubernetes cluster nào.

## Các Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ:
- Apply tất cả manifest files vào Kubernetes cluster
- Xác thực deployments và service registrations
- Kiểm tra end-to-end communication giữa các microservices
- Xác minh tích hợp bảo mật OAuth2

---

**Lưu ý**: Hướng dẫn này là một phần của khóa học toàn diện về Spring Boot microservices bao gồm các pattern triển khai Kubernetes.