# Tạo Helm Charts Riêng Cho Từng Môi Trường Microservices

## Tổng Quan

Hướng dẫn này sẽ giúp bạn tạo các Helm charts riêng cho từng môi trường, cho phép triển khai toàn bộ microservices với một lệnh Helm duy nhất. Phương pháp này đơn giản hóa việc triển khai trên các môi trường khác nhau (dev, QA, production) trong khi vẫn duy trì cấu hình riêng cho từng môi trường.

## Yêu Cầu Tiên Quyết

- Đã có sẵn Eazy Bank Common và Eazy Bank Services Helm charts
- Hiểu biết cơ bản về Helm và Kubernetes
- Có quyền truy cập terminal với Helm CLI đã cài đặt

## Tạo Cấu Trúc Thư Mục Environments

Đầu tiên, tạo một thư mục mới có tên `Environments` trong cùng thư mục chứa `Eazy Bank Command` và `Eazy Bank Services`.

```bash
mkdir Environments
cd Environments
```

## Tạo Helm Chart Cho Môi Trường Development

### Bước 1: Tạo Helm Chart

Tạo một Helm chart mới cho môi trường development:

```bash
helm create dev-env
```

### Bước 2: Dọn Dẹp Templates Mặc Định

Di chuyển vào thư mục `dev-env` vừa tạo và:
1. Xóa tất cả các file trong thư mục `templates`
2. Xóa tất cả các giá trị trong file `values.yaml`

### Bước 3: Cấu Hình Chart.yaml

Mở file `chart.yaml` và cập nhật `appVersion` để đảm bảo tính nhất quán:

```yaml
apiVersion: v2
name: dev-env
description: A Helm chart for development environment
appVersion: "1.0.0"
```

### Bước 4: Định Nghĩa Dependencies

Thêm phần dependencies vào `chart.yaml`:

```yaml
dependencies:
  - name: easybank-common
  - name: configserver
  - name: eurekaserver
  - name: accounts
  - name: cards
  - name: loans
  - name: gatewayserver
  - name: message
```

## Hiểu Về Templates Riêng Cho Môi Trường

**Lưu Ý Quan Trọng:** Helm charts cho môi trường không cần các file manifest deployment và service vì những file này đã có sẵn trong các Helm charts riêng của từng microservice. Charts cho môi trường chỉ cần template ConfigMap vì cấu hình ConfigMap được chia sẻ cho tất cả microservices.

### Bước 5: Tạo ConfigMap Template

Tạo file `config.yaml` trong thư mục `templates` để import template ConfigMap chung:

```yaml
{{- template "common.configmap" . }}
```

Dòng này import template ConfigMap đã được định nghĩa trong Eazy Bank Common Helm chart.

## Cấu Hình Values Cho Môi Trường Development

### Bước 6: Điền Thông Tin values.yaml

Thêm cấu hình sau vào `values.yaml`:

```yaml
global:
  configMapName: easybank-dev-configmap
  activeProfile: default
  configServerUrl: http://configserver:8071
  eurekaServerUrl: http://eurekaserver:8070/eureka
  keycloakUrl: http://keycloak.default.svc.cluster.local:80
  openTelemetryJarPath: /path/to/opentelemetry.jar
  tempoUrl: http://tempo.default.svc.cluster.local:9411
  otelMetricsExporter: none
  kafkaBrokerUrl: kafka-service:9092
```

### Giải Thích Các Cấu Hình Chính

- **global prefix**: Dùng để chỉ ra các giá trị này áp dụng cho tất cả microservices
- **activeProfile**: Đặt là "default" cho môi trường development
- **Service URLs**: Sử dụng tên service trong Kubernetes (phải khớp với tên service được định nghĩa trong các file service.yaml)
- **Keycloak/Kafka URLs**: Tuân theo định dạng `servicename.namespace.svc.cluster.local` cho triển khai theo tiêu chuẩn production

## Build Helm Chart

### Bước 7: Compile Dependencies

Di chuyển vào thư mục `dev-env` và chạy lệnh:

```bash
helm dependencies build
```

Lệnh này sẽ compile tất cả các dependent Helm charts và lưu trữ chúng trong thư mục `charts` ở dạng nén.

## Tạo Các Môi Trường Bổ Sung

### Tạo Môi Trường QA

1. Copy thư mục `dev-env` và đổi tên thành `qa-env`
2. Cập nhật `chart.yaml`:
   ```yaml
   name: qa-env
   ```
3. Cập nhật `values.yaml`:
   ```yaml
   global:
     configMapName: easybank-qa-configmap
     activeProfile: qa
     # Giữ nguyên các giá trị khác hoặc tùy chỉnh theo nhu cầu
   ```
4. Build dependencies:
   ```bash
   cd qa-env
   helm dependencies build
   ```

### Tạo Môi Trường Production

1. Copy thư mục `qa-env` và đổi tên thành `prod-env`
2. Cập nhật `chart.yaml`:
   ```yaml
   name: prod-env
   ```
3. Cập nhật `values.yaml`:
   ```yaml
   global:
     configMapName: easybank-prod-configmap
     activeProfile: prod
     # Giữ nguyên các giá trị khác hoặc tùy chỉnh theo nhu cầu
   ```
4. Build dependencies:
   ```bash
   cd prod-env
   helm dependencies build
   ```

## Chiến Lược Triển Khai

Sau khi tạo xong các Helm charts riêng cho từng môi trường, bạn có thể triển khai toàn bộ microservices vào một môi trường cụ thể chỉ với một lệnh duy nhất:

```bash
# Cho môi trường development
helm install dev-deployment ./dev-env

# Cho môi trường QA
helm install qa-deployment ./qa-env

# Cho môi trường production
helm install prod-deployment ./prod-env
```

Đằng sau hậu trường, lệnh duy nhất này sẽ:
- Cài đặt tất cả các microservices phụ thuộc (config server, Eureka server, accounts, cards, loans, gateway, message)
- Tạo ConfigMap riêng cho môi trường
- Cấu hình tất cả services với các thiết lập môi trường phù hợp

## Sử Dụng ConfigMap

ConfigMap được tạo bởi các Helm charts này chứa các thuộc tính cấu hình mà tất cả microservices có thể đọc tại runtime. Điều này tương tự như cách Docker Compose inject các thuộc tính vào microservices, nhưng được triển khai theo cách native của Kubernetes.

## Các Bước Tiếp Theo

Trước khi triển khai microservices vào Kubernetes cluster, bạn cần thiết lập các thành phần bổ sung:
- Keycloak (cho xác thực và phân quyền)
- Apache Kafka (cho event streaming)
- Grafana (cho giám sát)

Các thành phần này có sẵn Helm charts được xây dựng trước từ cộng đồng open-source, sẽ được đề cập trong các bài giảng tiếp theo.

## Tóm Tắt

Phương pháp này cung cấp:
- **Triển khai với một lệnh duy nhất**: Triển khai toàn bộ kiến trúc microservice với một lệnh
- **Cách ly môi trường**: Cấu hình riêng biệt cho dev, QA, và production
- **Cấu hình tập trung**: ConfigMap được chia sẻ cho tất cả microservices
- **Dễ bảo trì**: Dễ dàng cập nhật và kiểm soát phiên bản cho các thiết lập riêng của môi trường
- **Sẵn sàng cho production**: Tuân theo các best practices của Kubernetes cho việc đặt tên và khám phá service

## Best Practices (Thực Hành Tốt Nhất)

1. Luôn compile các dependent charts sau khi thay đổi common charts
2. Validate Helm templates trước khi cài đặt bằng lệnh `helm template .`
3. Sử dụng quy ước đặt tên nhất quán giữa các môi trường
4. Lưu trữ dữ liệu nhạy cảm trong Kubernetes Secrets, không phải ConfigMaps
5. Kiểm soát phiên bản cho tất cả các thay đổi Helm chart
6. Test ở môi trường thấp hơn trước khi đưa lên production

## Các Lỗi Thường Gặp và Cách Khắc Phục

### Lỗi Template

Nếu gặp lỗi khi chạy `helm template .`, kiểm tra:
- Tên biến trong template có đúng không
- Cú pháp trong các file YAML có hợp lệ không
- Các dependencies đã được build chưa

### Lỗi Dependencies

Nếu không thể build dependencies:
- Đảm bảo đường dẫn đến các charts phụ thuộc là chính xác
- Kiểm tra kết nối mạng nếu pull từ remote repository
- Xác nhận rằng tất cả các charts phụ thuộc tồn tại và có phiên bản phù hợp

## Kết Luận

Việc tạo các Helm charts riêng cho từng môi trường là một phương pháp mạnh mẽ để quản lý triển khai microservices qua nhiều môi trường khác nhau. Nó cung cấp sự linh hoạt, dễ bảo trì và tuân theo các best practices của Kubernetes. Với cách tiếp cận này, bạn có thể dễ dàng mở rộng và quản lý hệ thống microservices phức tạp một cách hiệu quả.