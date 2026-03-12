# Hướng Dẫn Cập Nhật Helm Charts cho Kubernetes Discovery Server

## Tổng Quan

Hướng dẫn này cung cấp quy trình từng bước để cập nhật Helm charts của microservices nhằm di chuyển từ Netflix Eureka sang Spring Cloud Kubernetes Discovery Server. Bao gồm giải quyết vấn đề cấu hình, cập nhật dependencies và triển khai thành công lên Kubernetes cluster.

## Bối Cảnh

Các microservices trước đây sử dụng Netflix Eureka cho service discovery. Sau khi tạo Docker images với các thay đổi section 17 (được tag là `s17`), hệ thống cần chuyển sang service discovery gốc của Kubernetes sử dụng Spring Cloud Kubernetes Discovery Server.

## Trạng Thái Ban Đầu

### Các Thành Phần Đã Cài Đặt
- **Keycloak**: Quản lý danh tính và truy cập
- **Kafka**: Nền tảng streaming sự kiện
- **Grafana**: Giám sát và quan sát
- **Prometheus**: Thu thập metrics
- **Tất cả microservices**: Docker images được tag là `s17`

## Quy Trình Di Chuyển Từng Bước

### Giai Đoạn 1: Dọn Dẹp Helm Chart

#### 1.1 Xóa Folder Eureka Server
Điều hướng đến thư mục Helm charts và xóa folder Eureka server:

```bash
cd section17/helm/easybank-services
# Xóa folder eureka-server
```

#### 1.2 Cập Nhật Image Tags

Cập nhật `values.yaml` cho từng microservice:

**Accounts Microservice** (`accounts/values.yaml`):
```yaml
replicaCount: 2  # Để demo load balancing
image:
  tag: s17
```

**Cards Microservice** (`cards/values.yaml`):
```yaml
image:
  tag: s17
```

**Config Server** (`config-server/values.yaml`):
```yaml
image:
  tag: s17
```

**Gateway Server** (`gateway/values.yaml`):
```yaml
image:
  tag: s17
```

**Loans Microservice** (`loans/values.yaml`):
```yaml
image:
  tag: s17
```

**Message Microservice** (`message/values.yaml`):
```yaml
image:
  tag: s17
```

### Giai Đoạn 2: Cập Nhật Cấu Hình Môi Trường

#### 2.1 Xóa Dependencies Eureka

Cho mỗi folder môi trường (dev-env, prod-env, qa-env), chỉnh sửa `chart.yaml`:

**Trước:**
```yaml
dependencies:
  - name: eureka-server
    version: 1.0.0
    repository: file://../easybank-services/eureka-server
  # ... các dependencies khác
```

**Sau:**
```yaml
dependencies:
  # Đã xóa dependency eureka server
  # ... các dependencies khác
```

#### 2.2 Dọn Dẹp và Rebuild Dependencies

Xóa các file lock và rebuild dependencies cho từng môi trường:

```bash
cd helm/environments/dev-env
rm chart.lock
helm dependency build

cd ../prod-env
rm chart.lock
helm dependency build

cd ../qa-env
rm chart.lock
helm dependency build
```

### Giai Đoạn 3: Thử Triển Khai Lần Đầu

Triển khai các microservices:

```bash
cd environments
helm install easybank prod-env
```

**Kết quả**: Triển khai được khởi động nhưng các microservices không thể khởi động.

### Giai Đoạn 4: Xử Lý Sự Cố và Giải Quyết

#### 4.1 Xác Định Vấn Đề

Sau khi theo dõi Kubernetes dashboard, các microservices sau không khởi động được:
- Gateway Server
- Loans Microservice
- Cards Microservice
- Accounts Microservice

**Thông Báo Lỗi:**
```
Discovery server URL not provided
```

**Phân Tích Nguyên Nhân:**
Các microservices yêu cầu thuộc tính `spring.cloud.kubernetes.discovery.discovery-server-url` được cấu hình, nhưng nó không có trong Helm charts.

#### 4.2 Các Bước Giải Quyết

**Bước 1: Gỡ Cài Đặt Triển Khai Thất Bại**
```bash
helm uninstall easybank
```

**Bước 2: Cập Nhật Common Helm Chart**

Điều hướng đến Helm chart `easybank-common`:

**File: `templates/configmap.yaml`**

Thay thế cấu hình Eureka:
```yaml
EUREKA.CLIENT.SERVICE-URL.DEFAULT-ZONE: {{ .Values.eurekaServerURL }}
```

Bằng cấu hình Kubernetes Discovery:
```yaml
SPRING.CLOUD.KUBERNETES.DISCOVERY.DISCOVERY-SERVER-URL: {{ .Values.discoveryServerURL }}
```

**File: `templates/deployment.yaml`**

Cập nhật việc inject biến môi trường:

**Trước:**
```yaml
{{- if .Values.eurekaEnabled }}
- name: EUREKA_CLIENT_SERVICEURL_DEFAULTZONE
  valueFrom:
    configMapKeyRef:
      name: {{ .Values.name }}-configmap
      key: EUREKA_CLIENT_SERVICEURL_DEFAULTZONE
{{- end }}
```

**Sau:**
```yaml
{{- if .Values.discoveryEnabled }}
- name: SPRING_CLOUD_KUBERNETES_DISCOVERY_DISCOVERY_SERVER_URL
  valueFrom:
    configMapKeyRef:
      name: {{ .Values.name }}-configmap
      key: SPRING_CLOUD_KUBERNETES_DISCOVERY_DISCOVERY_SERVER_URL
{{- end }}
```

**Bước 3: Cập Nhật Values của Từng Microservice**

Cho mỗi microservice (accounts, cards, config-server, gateway, loans, message), cập nhật `values.yaml`:

**Trước:**
```yaml
eurekaEnabled: true
```

**Sau:**
```yaml
discoveryEnabled: true
```

**Bước 4: Cập Nhật Values Môi Trường**

Cho mỗi môi trường (dev-env, prod-env, qa-env), cập nhật `values.yaml`:

**Trước:**
```yaml
eurekaServerURL: http://eureka-server:8070/eureka/
```

**Sau:**
```yaml
discoveryServerURL: http://spring-cloud-kubernetes-discoveryserver:80
```

**Lưu ý:** Tên service `spring-cloud-kubernetes-discoveryserver` được định nghĩa trong file Kubernetes manifest dùng để triển khai Discovery Server.

### Giai Đoạn 5: Biên Dịch Lại

Biên dịch lại tất cả Helm charts sau các thay đổi:

**Microservices:**
```bash
cd helm/easybank-services/accounts
helm dependency build

cd ../cards
helm dependency build

cd ../config-server
helm dependency build

cd ../gateway
helm dependency build

cd ../loans
helm dependency build

cd ../message
helm dependency build
```

**Môi Trường:**
```bash
cd ../../environments/dev-env
helm dependency build

cd ../prod-env
helm dependency build

cd ../qa-env
helm dependency build
```

### Giai Đoạn 6: Xác Thực

Trước khi triển khai, xác thực các Helm charts:

```bash
cd environments
helm template easybank prod-env
```

**Các Điểm Xác Minh:**
- Kiểm tra biến môi trường Discovery Server URL có mặt
- Xác minh ConfigMap chứa thuộc tính đúng
- Đảm bảo không có lỗi biên dịch

**Xác Minh Đầu Ra Mẫu:**
Tìm biến môi trường trong deployment của loans microservice:
```yaml
env:
  - name: SPRING_CLOUD_KUBERNETES_DISCOVERY_DISCOVERY_SERVER_URL
    valueFrom:
      configMapKeyRef:
        name: loans-configmap
        key: SPRING_CLOUD_KUBERNETES_DISCOVERY_DISCOVERY_SERVER_URL
```

### Giai Đoạn 7: Triển Khai Cuối Cùng

Triển khai với cấu hình đã sửa:

```bash
cd environments
helm install easybank prod-env
```

### Giai Đoạn 8: Giám Sát

Theo dõi triển khai trong Kubernetes Dashboard:

1. **Kiểm Tra Config Server Trước:**
   - Config Server phải khởi động thành công trước các microservices khác
   - Xem lại logs để đảm bảo khởi động đúng

2. **Theo Dõi Các Microservices Khác:**
   - Accounts: Nên hiển thị 2 pods (replica count = 2)
   - Cards, Loans, Message, Gateway: Nên hiển thị 1 pod mỗi cái

3. **Đợi Khởi Động:**
   - Khởi động ban đầu có thể mất vài phút
   - Hạn chế tài nguyên trên hệ thống local có thể làm chậm quá trình

## Tài Liệu Tham Khảo Cấu Hình

### Các Thuộc Tính Quan Trọng

**Thuộc Tính Spring Cloud Kubernetes Discovery:**
```properties
spring.cloud.kubernetes.discovery.discovery-server-url=http://spring-cloud-kubernetes-discoveryserver:80
```

**Cấu Trúc ConfigMap:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Values.name }}-configmap
data:
  SPRING_CLOUD_KUBERNETES_DISCOVERY_DISCOVERY_SERVER_URL: {{ .Values.discoveryServerURL }}
```

**Biến Môi Trường Deployment:**
```yaml
env:
  - name: SPRING_CLOUD_KUBERNETES_DISCOVERY_DISCOVERY_SERVER_URL
    valueFrom:
      configMapKeyRef:
        name: {{ .Values.name }}-configmap
        key: SPRING_CLOUD_KUBERNETES_DISCOVERY_DISCOVERY_SERVER_URL
```

## Kiến Trúc Microservices

### Tổng Quan Thành Phần

| Thành Phần | Replicas | Mục Đích |
|-----------|----------|----------|
| Accounts | 2 | Dịch vụ tài khoản ngân hàng cốt lõi (load balanced) |
| Cards | 1 | Quản lý thẻ tín dụng/ghi nợ |
| Loans | 1 | Ứng dụng và quản lý khoản vay |
| Message | 1 | Spring Cloud Functions messaging |
| Config Server | 1 | Quản lý cấu hình tập trung |
| Gateway | 1 | API Gateway với OAuth2 Resource Server |
| Discovery Server | 1 | Spring Cloud Kubernetes service discovery |

### Các Dependencies của Service

```
Gateway Server
  ├─→ Discovery Server (service discovery)
  ├─→ Config Server (configuration)
  ├─→ Keycloak (authentication)
  └─→ Backend Services
        ├─→ Accounts (2 replicas)
        ├─→ Cards
        ├─→ Loans
        └─→ Message
```

## Hướng Dẫn Xử Lý Sự Cố

### Vấn Đề: Pods Không Khởi Động

**Triệu Chứng:**
- Pods vẫn ở trạng thái `Pending` hoặc `CrashLoopBackOff`
- Error logs hiển thị "Discovery server URL not provided"

**Giải Pháp:**
1. Xác minh `discoveryEnabled: true` trong tất cả file `values.yaml` của microservice
2. Kiểm tra `discoveryServerURL` được đặt trong `values.yaml` của môi trường
3. Xác nhận biến môi trường được inject đúng bằng `helm template`
4. Đảm bảo Discovery Server service đang chạy và có thể truy cập

### Vấn Đề: Helm Dependency Build Thất Bại

**Triệu Chứng:**
- Thông báo lỗi về dependencies xung đột
- Xung đột file Chart.lock

**Giải Pháp:**
1. Xóa các file `chart.lock` trong thư mục bị ảnh hưởng
2. Chạy lại `helm dependency build`
3. Xác minh dependencies trong `chart.yaml` được chỉ định đúng

### Vấn Đề: Config Server Không Khởi Động

**Triệu Chứng:**
- Các microservices khác đợi vô thời hạn
- Config Server pod hiển thị lỗi

**Giải Pháp:**
1. Kiểm tra logs của Config Server cho các lỗi cụ thể
2. Xác minh kết nối Git repository (nếu sử dụng Git backend)
3. Đảm bảo phân bổ tài nguyên đúng trong Kubernetes
4. Kiểm tra cấu hình ConfigMap và Secret

### Vấn Đề: Triển Khai Chậm Trên Hệ Thống Local

**Triệu Chứng:**
- Pods mất hơn 5 phút để khởi động
- Hiệu suất hệ thống giảm

**Giải Pháp:**
1. Tăng phân bổ tài nguyên Docker Desktop
2. Giảm số lượng replicas tạm thời
3. Triển khai các thành phần từng bước
4. Cân nhắc sử dụng Kubernetes cluster trên cloud

## Thực Hành Tốt Nhất

### 1. Triển Khai Từng Bước
- Triển khai Config Server trước và xác minh khởi động
- Triển khai Discovery Server tiếp theo
- Triển khai các microservices còn lại sau khi hạ tầng sẵn sàng

### 2. Quản Lý Helm Chart
- Luôn sử dụng `helm template` để xác thực trước khi cài đặt
- Giữ các file `chart.lock` trong version control (sau khi build thành công)
- Sử dụng quy ước đặt tên nhất quán qua các môi trường

### 3. Quản Lý Cấu Hình
- Sử dụng các file `values.yaml` theo môi trường
- Externalize cấu hình nhạy cảm vào Kubernetes Secrets
- Tài liệu hóa tất cả thuộc tính cấu hình tùy chỉnh

### 4. Giám Sát và Quan Sát
- Bật Prometheus metrics trên tất cả microservices
- Cấu hình Grafana dashboards để giám sát
- Thiết lập cảnh báo cho các lỗi service quan trọng
- Xem lại logs thường xuyên trong quá trình triển khai

### 5. Load Balancing
- Cấu hình nhiều replicas cho các services có lưu lượng cao
- Sử dụng load balancing của Kubernetes service
- Triển khai client-side load balancing với Spring Cloud LoadBalancer

## Tham Chiếu Lệnh Helm

### Các Lệnh Cơ Bản

```bash
# Cài đặt một release
helm install <release-name> <chart-path>

# Gỡ cài đặt một release
helm uninstall <release-name>

# Nâng cấp một release
helm upgrade <release-name> <chart-path>

# Liệt kê các releases
helm list

# Lấy trạng thái release
helm status <release-name>

# Xác thực template (dry-run)
helm template <release-name> <chart-path>

# Build dependencies
helm dependency build

# Liệt kê dependencies
helm dependency list
```

### Các Lệnh Debug

```bash
# Lấy rendered templates
helm get manifest <release-name>

# Lấy values được sử dụng cho release
helm get values <release-name>

# Hiển thị thông tin chart
helm show chart <chart-path>

# Hiển thị default values
helm show values <chart-path>
```

## Tài Nguyên Bổ Sung

### Tài Liệu Spring Cloud Kubernetes
- Tài liệu tham khảo chính thức Spring Cloud Kubernetes: [https://spring.io/projects/spring-cloud-kubernetes](https://spring.io/projects/spring-cloud-kubernetes)
- Hướng dẫn cấu hình Discovery Server

### Tài Liệu Helm
- Thực hành tốt nhất của Helm charts
- Quản lý dependency
- Template functions và pipelines

### Tài Nguyên Kubernetes
- Service discovery trong Kubernetes
- Quản lý ConfigMaps và Secrets
- Vòng đời Pod và xử lý sự cố

## Kết Luận

Di chuyển thành công từ Eureka sang Kubernetes Discovery Server yêu cầu:

1. **Cấu Hình Đúng**: Đặt thuộc tính `discovery-server-url` chính xác
2. **Cập Nhật Helm Chart**: Cập nhật templates và values qua tất cả charts
3. **Phương Pháp Có Hệ Thống**: Tuân theo quy trình triển khai có cấu trúc
4. **Xác Thực**: Sử dụng `helm template` để phát hiện vấn đề trước triển khai
5. **Giám Sát**: Theo dõi tích cực logs và metrics trong quá trình triển khai

Bằng cách làm theo hướng dẫn này, bạn có thể đảm bảo quá trình chuyển đổi mượt mà sang service discovery gốc của Kubernetes trong khi duy trì độ tin cậy và khả năng mở rộng của kiến trúc microservices của bạn.