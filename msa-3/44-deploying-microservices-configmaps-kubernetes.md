# Triển khai Microservices với ConfigMaps trong Kubernetes

## Tổng quan

Hướng dẫn này giải thích cách tạo và sử dụng ConfigMaps trong Kubernetes để quản lý các biến môi trường cho việc triển khai microservices. ConfigMaps cho phép bạn lưu trữ dữ liệu cấu hình không bảo mật dưới dạng các cặp key-value có thể được container sử dụng như biến môi trường, tham số dòng lệnh, hoặc file cấu hình.

## Yêu cầu trước khi bắt đầu

- Kubernetes cluster đang chạy
- kubectl CLI đã được cấu hình
- Các file Docker compose với cấu hình biến môi trường
- Hiểu biết cơ bản về các đối tượng Kubernetes

## Sự khác biệt giữa ConfigMaps và Secrets

### ConfigMaps
- Được sử dụng để lưu trữ dữ liệu **không bảo mật** dưới dạng cặp key-value
- Container có thể sử dụng ConfigMaps như:
  - Biến môi trường
  - Tham số dòng lệnh
  - File cấu hình trong volume
- Dữ liệu hiển thị dưới dạng văn bản thuần trong Kubernetes Dashboard

### Secrets
- Được sử dụng để lưu trữ dữ liệu **bảo mật**
- Dữ liệu được mã hóa base64 theo mặc định
- Ẩn khỏi chế độ xem trực tiếp trong Kubernetes Dashboard
- **Lưu ý**: "Secrets trong Kubernetes không thực sự là bí mật" - có những cách tốt hơn để lưu trữ secrets trong môi trường cloud, thường được quản lý bởi team Platform/DevOps

## Các biến môi trường cần thiết

Để triển khai microservices, chúng ta cần các biến môi trường sau:

- **Activated profile**: Profile Spring nào sẽ được sử dụng
- **Spring config import URL**: Vị trí của configuration server
- **Eureka server URL**: Vị trí của service discovery server
- **Tên ứng dụng**: Cho config server, Eureka server, accounts, loans, cards, gateway
- **Cấu hình Keycloak**:
  - Tên người dùng admin
  - Mật khẩu admin
  - URL Keycloak để resource server lấy certificate

## Tạo file Manifest ConfigMap

### Bước 1: Tạo file YAML

Tạo file mới có tên `configmaps.yml` trong thư mục Kubernetes của bạn.

### Bước 2: Định nghĩa cấu trúc ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: easybank-configmap
data:
  SPRING_PROFILE: "default"
  SPRING_CONFIG_IMPORT: "configserver:http://configserver:8071/"
  EUREKA_SERVER_URL: "http://eurekaserver:8070/eureka/"
  CONFIG_SERVER_APP_NAME: "configserver"
  EUREKA_SERVER_APP_NAME: "eurekaserver"
  ACCOUNTS_APP_NAME: "accounts"
  LOANS_APP_NAME: "loans"
  CARDS_APP_NAME: "cards"
  GATEWAY_APP_NAME: "gateway"
  KEYCLOAK_ADMIN_USERNAME: "admin"
  KEYCLOAK_ADMIN_PASSWORD: "admin"
  KEYCLOAK_SERVER_URL: "http://keycloak:7080"
```

### Các điểm chính:

1. **apiVersion**: Đặt là `v1` cho ConfigMaps
2. **kind**: Phải là `ConfigMap`
3. **metadata.name**: Chọn tên mô tả rõ ràng (ví dụ: `easybank-configmap`)
4. **data**: Chứa tất cả các thuộc tính môi trường dưới dạng cặp key-value

### Cấu hình tên Service

Các hostname trong biến môi trường phải khớp với tên Kubernetes service của bạn:
- Tên service Config Server: `configserver`
- Tên service Eureka Server: `eurekaserver`
- Tên service Keycloak: `keycloak` (expose trên cổng 7080)

## Triển khai ConfigMap lên Kubernetes

### Áp dụng ConfigMap

Chạy lệnh kubectl sau:

```bash
kubectl apply -f configmaps.yaml
```

Kết quả mong đợi:
```
configmap/easybank-configmap created
```

### Xác minh việc tạo ConfigMap

#### Sử dụng kubectl:
```bash
kubectl get configmaps
kubectl describe configmap easybank-configmap
```

#### Sử dụng Kubernetes Dashboard:

1. Truy cập Kubernetes Dashboard
2. Lấy authentication token (nếu phiên đã hết hạn)
3. Chọn namespace `default`
4. Điều hướng đến mục **Config Maps**
5. Click vào ConfigMap của bạn để xem tất cả các biến môi trường

## Lưu ý quan trọng

### Các thành phần không được bao gồm

ConfigMap này không bao gồm các thuộc tính cho:
- Kafka
- RabbitMQ
- OpenTelemetry
- Grafana

**Lý do**: Các thành phần tiêu chuẩn công nghiệp này sẽ được triển khai bằng Helm Charts trong các bài giảng sau, điều này dễ dàng hơn và ít phức tạp hơn so với việc viết file manifest Kubernetes thủ công.

### Yêu cầu về Keycloak

Việc triển khai Keycloak là **bắt buộc** vì:
- Gateway server được bảo mật bằng OAuth2
- Không có Keycloak server, bạn không thể truy cập bất kỳ API nào
- Cần thiết để tạo dữ liệu bên trong microservices

## Các bước tiếp theo

Với ConfigMap đã được tạo thành công, bây giờ bạn có thể:
1. Triển khai các microservices còn lại lên Kubernetes cluster
2. Tham chiếu các biến môi trường này trong deployment manifest của bạn
3. Tiến hành thiết lập Keycloak cho xác thực và phân quyền

## ConfigMap vs Secrets: Xem dữ liệu

### Khả năng hiển thị dữ liệu ConfigMap
- Dữ liệu hiển thị trực tiếp trong Kubernetes Dashboard
- Định dạng văn bản thuần
- Phù hợp cho cấu hình không nhạy cảm

### Khả năng hiển thị dữ liệu Secrets
- Dữ liệu bị ẩn theo mặc định trong Kubernetes Dashboard
- Được mã hóa Base64 (không phải mã hóa thực sự)
- Click vào tùy chọn "View" để xem giá trị token
- **Lưu ý bảo mật**: Không phải là cách hoàn hảo để bảo mật secrets; môi trường cloud cung cấp các giải pháp quản lý secret tốt hơn

## Kết luận

ConfigMaps cung cấp một cách hiệu quả để quản lý các biến môi trường trong Kubernetes clusters. Bằng cách tập trung hóa dữ liệu cấu hình, bạn có thể dễ dàng inject các biến giống nhau vào nhiều triển khai microservices, làm cho cơ sở hạ tầng của bạn dễ bảo trì và mở rộng hơn.