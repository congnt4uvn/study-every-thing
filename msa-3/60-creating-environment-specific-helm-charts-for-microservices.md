# Tạo Helm Charts Cho Từng Môi Trường Triển Khai Microservices

## Tổng Quan

Hướng dẫn này trình bày cách tạo các Helm chart riêng biệt cho từng môi trường, cho phép bạn triển khai tất cả microservices chỉ với một lệnh duy nhất. Thay vì quản lý việc triển khai từng microservice riêng lẻ, bạn sẽ tạo các Helm chart thống nhất cho các môi trường khác nhau (Dev, QA, Production).

## Yêu Cầu Trước Khi Bắt Đầu

- Đã có các Helm chart cho microservices (Eazy Bank Command và Eazy Bank Services)
- Hiểu biết cơ bản về Helm charts
- Có quyền truy cập vào Kubernetes cluster
- Đã cài đặt Helm trên hệ thống

## Tạo Cấu Trúc Thư Mục Môi Trường

### Bước 1: Thiết Lập Thư Mục Environments

Tạo một thư mục mới có tên `Environments` trong cùng thư mục với `Eazy Bank Command` và `Eazy Bank Services`.

```bash
mkdir Environments
cd Environments
```

## Tạo Helm Chart Cho Môi Trường Dev

### Bước 2: Khởi Tạo Helm Chart Cơ Bản

Tạo một Helm chart mới cho môi trường development:

```bash
helm create dev-ENV
```

Lệnh này tạo ra cấu trúc Helm chart cơ bản với tên `dev-ENV`.

### Bước 3: Dọn Dẹp Templates Mặc Định

1. Điều hướng đến thư mục `templates` bên trong `dev-ENV`
2. Xóa tất cả các file template mặc định
3. Mở file `values.yaml` và xóa tất cả các giá trị mặc định

### Bước 4: Cấu Hình Chart.yaml

Mở file `chart.yaml` và cập nhật `appVersion`:

```yaml
apiVersion: v2
name: dev-ENV
description: Helm chart cho môi trường Dev
type: application
version: 0.1.0
appVersion: "1.0.0"
```

### Bước 5: Định Nghĩa Dependencies

Thêm tất cả các microservice phụ thuộc vào `chart.yaml`:

```yaml
dependencies:
  - name: eazybank-command
    version: "1.0.0"
    repository: "file://../eazybank-command"
  - name: configserver
    version: "1.0.0"
    repository: "file://../configserver"
  - name: eurekaserver
    version: "1.0.0"
    repository: "file://../eurekaserver"
  - name: accounts
    version: "1.0.0"
    repository: "file://../accounts"
  - name: cards
    version: "1.0.0"
    repository: "file://../cards"
  - name: loans
    version: "1.0.0"
    repository: "file://../loans"
  - name: gatewayserver
    version: "1.0.0"
    repository: "file://../gatewayserver"
  - name: message
    version: "1.0.0"
    repository: "file://../message"
```

## Thiết Lập ConfigMap Template

### Bước 6: Tạo ConfigMap Template

Trong thư mục `templates`, tạo file `configmap.yaml`. Thay vì định nghĩa một ConfigMap template mới, hãy tham chiếu đến ConfigMap template chung:

```yaml
{{- include "common.configmap" . }}
```

Cách này import và sử dụng ConfigMap template từ Eazy Bank Common Helm chart (`common.configmap`).

### Tại Sao Chỉ Cần ConfigMap Templates?

- **Deployment và Service manifests** KHÔNG cần thiết trong environment charts
- Chúng đã có sẵn trong các Helm chart của từng microservice
- **ConfigMap được chia sẻ** giữa tất cả microservices, rất phù hợp cho cấu hình cấp môi trường

## Cấu Hình Values Cho Môi Trường Dev

### Bước 7: Điền Thông Tin vào values.yaml

Thêm các giá trị sau vào `values.yaml`:

```yaml
global:
  configMapName: "eazybank-dev-configmap"
  activeProfile: "default"
  configServerUrl: "http://configserver:8071"
  eurekaServerUrl: "http://eurekaserver:8070/eureka/"
  keycloakUrl: "http://keycloak.default.svc.cluster.local:80"
  otelJarPath: "/app/libs/opentelemetry-javaagent.jar"
  tempoUrl: "http://tempo.default.svc.cluster.local:4317"
  otelMetricsExporter: "none"
  kafkaBrokerUrl: "kafka.default.svc.cluster.local:9092"
```

### Hiểu Về Các Giá Trị Cấu Hình

#### Tiền Tố Global
- Tiền tố `global` cho biết các giá trị này áp dụng cho tất cả microservices
- Đây là quy ước tùy chỉnh để tổ chức (không phải chuẩn Helm)

#### Các Tham Số Cấu Hình Chính

1. **configMapName**: Tên của ConfigMap resource (`eazybank-dev-configmap`)

2. **activeProfile**: Spring Boot profile sử dụng (`default` cho môi trường Dev)

3. **configServerUrl**: URL service của Config Server
   - Hostname khớp với tên service định nghĩa trong `service.yaml`

4. **eurekaServerUrl**: URL service của Eureka Server
   - Định dạng: `http://servicename:port/eureka/`

5. **keycloakUrl**: URL service xác thực Keycloak
   - Sử dụng DNS nội bộ Kubernetes: `servicename.namespace.svc.cluster.local`
   - Port 80 (chuẩn cho triển khai Helm chart production)

6. **otelJarPath**: Đường dẫn đến file JAR OpenTelemetry Java agent

7. **tempoUrl**: URL service Grafana Tempo cho distributed tracing
   - Tuân theo quy ước đặt tên service Kubernetes

8. **otelMetricsExporter**: Cấu hình OpenTelemetry metrics exporter

9. **kafkaBrokerUrl**: URL service Kafka broker
   - Sử dụng định dạng DNS nội bộ Kubernetes

### Bước 8: Build Dependencies

Biên dịch Helm chart và tải về tất cả dependencies:

```bash
cd dev-ENV
helm dependency build
```

Lệnh này:
- Biên dịch tất cả các Helm chart phụ thuộc
- Tải về và đóng gói chúng vào thư mục `charts`
- Tạo phiên bản nén/đóng gói của mỗi dependency

## Tạo Helm Chart Cho Môi Trường QA

### Bước 9: Thiết Lập Môi Trường QA

1. Sao chép thư mục `dev-ENV` và đổi tên thành `qa-ENV`

2. Cập nhật `chart.yaml`:
```yaml
name: qa-ENV
```

3. Cập nhật `values.yaml`:
```yaml
global:
  configMapName: "eazybank-qa-configmap"
  activeProfile: "qa"
  # Giữ nguyên các giá trị khác hoặc cập nhật theo nhu cầu QA
  configServerUrl: "http://configserver:8071"
  eurekaServerUrl: "http://eurekaserver:8070/eureka/"
  # ... phần còn lại của cấu hình
```

**Thay Đổi Chính:**
- `activeProfile` đổi thành `"qa"`
- `configMapName` đổi thành `"eazybank-qa-configmap"`
- Các giá trị khác có thể tùy chỉnh nếu môi trường QA có hostname/service name khác

## Tạo Helm Chart Cho Môi Trường Production

### Bước 10: Thiết Lập Môi Trường Production

1. Sao chép thư mục `qa-ENV` và đổi tên thành `prod-ENV`

2. Cập nhật `chart.yaml`:
```yaml
name: prod-ENV
```

3. Cập nhật `values.yaml`:
```yaml
global:
  configMapName: "eazybank-prod-configmap"
  activeProfile: "prod"
  # Giữ nguyên các giá trị khác hoặc cập nhật theo nhu cầu Production
  configServerUrl: "http://configserver:8071"
  eurekaServerUrl: "http://eurekaserver:8070/eureka/"
  # ... phần còn lại của cấu hình
```

**Thay Đổi Chính:**
- `activeProfile` đổi thành `"prod"`
- `configMapName` đổi thành `"eazybank-prod-configmap"`

## Triển Khai

### Cách Triển Khai

Để triển khai tất cả microservices cho một môi trường cụ thể, chỉ cần cài đặt Helm chart tương ứng:

**Môi Trường Dev:**
```bash
helm install eazybank-dev ./dev-ENV
```

**Môi Trường QA:**
```bash
helm install eazybank-qa ./qa-ENV
```

**Môi Trường Production:**
```bash
helm install eazybank-prod ./prod-ENV
```

### Điều Gì Xảy Ra Đằng Sau

Khi bạn cài đặt một environment-specific Helm chart:

1. **Tất cả microservices phụ thuộc** được tự động cài đặt
2. **ConfigMap được tạo** với các giá trị riêng của môi trường
3. **Tất cả microservices đọc** cấu hình từ ConfigMap dùng chung tại runtime
4. **Service discovery** và **configuration management** hoạt động liền mạch

## Lợi Ích Của Phương Pháp Này

1. **Triển Khai Một Lệnh**: Triển khai toàn bộ kiến trúc microservice với một lệnh
2. **Cô Lập Môi Trường**: Cấu hình riêng biệt cho Dev, QA và Production
3. **Cấu Hình Tập Trung**: ConfigMap cung cấp cấu hình dùng chung cho tất cả services
4. **Tính Nhất Quán**: Quy trình triển khai giống nhau trên tất cả môi trường
5. **Dễ Cập Nhật**: Chỉnh sửa giá trị môi trường ở một nơi duy nhất
6. **Kiểm Soát Phiên Bản**: Theo dõi cấu hình môi trường trong Git

## So Sánh Với Docker Compose

Các giá trị cấu hình trong Helm charts tương tự như các biến môi trường bạn sẽ inject trong Docker Compose files. Cả hai phương pháp đều đạt được mục tiêu cung cấp cấu hình runtime cho microservices, nhưng Helm được thiết kế cho orchestration trên Kubernetes.

## Thực Hành Tốt Nhất

1. **Sử dụng Kubernetes Internal DNS** cho giao tiếp service-to-service
2. **Tuân theo quy ước đặt tên** cho ConfigMaps (tên riêng cho từng môi trường)
3. **Tách secrets riêng** khỏi ConfigMaps (sử dụng Kubernetes Secrets)
4. **Ghi chú sự khác biệt giữa các môi trường** trong comment của values.yaml
5. **Kiểm tra từng environment chart** trước khi triển khai production
6. **Quản lý phiên bản** tất cả Helm charts và values files

## Xử Lý Sự Cố

### Các Vấn Đề Thường Gặp

1. **Dependency Build Thất Bại**: Đảm bảo tất cả charts được tham chiếu tồn tại tại đường dẫn đã chỉ định
2. **Không Tìm Thấy Service**: Kiểm tra tên service khớp với tên trong file service.yaml
3. **ConfigMap Không Được Áp Dụng**: Kiểm tra template common.configmap được import đúng cách

## Kết Luận

Bạn đã tạo thành công các Helm chart riêng cho từng môi trường, giúp đơn giản hóa việc triển khai microservice. Phương pháp này cung cấp giải pháp production-ready để quản lý nhiều môi trường với chi phí tối thiểu và tính nhất quán tối đa.