# Xây Dựng Helm Charts Tùy Chỉnh Cho Microservices

## Giới Thiệu

Trong các dự án thực tế và tổ chức doanh nghiệp, các nhóm cần xây dựng Helm charts riêng dựa trên yêu cầu cụ thể của microservices. Hướng dẫn này sẽ giúp bạn tạo một Helm chart tùy chỉnh có thể triển khai tất cả microservices lên Kubernetes cluster chỉ với một lệnh duy nhất.

## Bắt Đầu

### Tạo Cấu Trúc Dự Án

1. Tạo cấu trúc thư mục mới:
   - Tạo thư mục có tên `Section_16`
   - Bên trong, tạo thư mục con có tên `Helm`

2. Điều hướng đến thư mục Helm trong terminal:
   ```bash
   cd Section_16/Helm
   ```

### Tạo Helm Chart Cơ Bản

Tạo một Helm chart chung sẽ đóng vai trò là template cho tất cả microservices:

```bash
helm create eazybank-common
```

Lệnh này tạo một Helm chart với các tệp và thư mục được định nghĩa sẵn.

## Dọn Dẹp Chart Mặc Định

Helm chart mặc định chứa các template triển khai website NGINX. Vì chúng ta đang xây dựng nội dung riêng:

1. **Xóa tất cả các tệp template** trong thư mục `templates`
2. **Xóa nội dung tệp `values.yaml`** - loại bỏ tất cả giá trị liên quan đến NGINX
3. **Xác minh không có dependencies** trong thư mục `charts`

## Cấu Hình Chart.yaml

Cập nhật tệp `Chart.yaml` với thông tin cụ thể của bạn:

```yaml
apiVersion: v2
name: eazybank-common
description: A Helm chart for Kubernetes
type: application
version: 0.1.0
appVersion: "1.0.0"
```

Các trường quan trọng:
- **version**: Phiên bản của Helm chart (0.1.0)
- **appVersion**: Phiên bản của ứng dụng (1.0.0)

## Tạo Các Tệp Template

Để triển khai microservices lên Kubernetes, chúng ta cần ba tệp manifest chính:
1. Deployment manifest
2. Service manifest
3. ConfigMap

### 1. Service Template (service.yaml)

```yaml
{{- define "common.service" -}}
apiVersion: v1
kind: Service
metadata:
  name: {{ .Values.serviceName }}
spec:
  selector:
    app: {{ .Values.appLabel }}
  type: {{ .Values.service.type }}
  ports:
    - name: http
      protocol: TCP
      port: {{ .Values.service.port }}
      targetPort: {{ .Values.service.targetPort }}
{{- end }}
```

**Tính Năng Chính:**
- Sử dụng `define` để tạo template có thể tái sử dụng với tên `common.service`
- Các giá trị động được inject từ `values.yaml`:
  - `serviceName`: Tên của service
  - `appLabel`: Nhãn ứng dụng cho selector
  - `service.type`: Loại service (ClusterIP, NodePort, LoadBalancer)
  - `service.port`: Cổng service
  - `service.targetPort`: Cổng đích

### 2. Deployment Template (deployment.yaml)

```yaml
{{- define "common.deployment" -}}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Values.appLabel }}
  labels:
    app: {{ .Values.appLabel }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: {{ .Values.appLabel }}
  template:
    metadata:
      labels:
        app: {{ .Values.appLabel }}
    spec:
      containers:
      - name: {{ .Values.appLabel }}
        image: {{ .Values.image.repository }}:{{ .Values.image.tag }}
        ports:
        - containerPort: {{ .Values.service.targetPort }}
          protocol: TCP
        env:
        {{- if .Values.appname_enabled }}
        - name: SPRING_APPLICATION_NAME
          value: {{ .Values.appName }}
        {{- end }}
        {{- if .Values.profile_enabled }}
        - name: SPRING_PROFILES_ACTIVE
          valueFrom:
            configMapKeyRef:
              name: {{ .Values.global.configMapName }}
              key: SPRING_PROFILES_ACTIVE
        {{- end }}
        {{- if .Values.config_enabled }}
        - name: SPRING_CONFIG_IMPORT
          valueFrom:
            configMapKeyRef:
              name: {{ .Values.global.configMapName }}
              key: SPRING_CONFIG_IMPORT
        {{- end }}
        {{- if .Values.eureka_enabled }}
        - name: EUREKA_CLIENT_SERVICEURL_DEFAULTZONE
          valueFrom:
            configMapKeyRef:
              name: {{ .Values.global.configMapName }}
              key: EUREKA_CLIENT_SERVICEURL_DEFAULTZONE
        {{- end }}
        {{- if .Values.resourceserver_enabled }}
        - name: SPRING_SECURITY_OAUTH2_RESOURCESERVER_JWT_JWK_SET_URI
          valueFrom:
            configMapKeyRef:
              name: {{ .Values.global.configMapName }}
              key: SPRING_SECURITY_OAUTH2_RESOURCESERVER_JWT_JWK_SET_URI
        {{- end }}
        {{- if .Values.otel_enabled }}
        - name: JAVA_TOOL_OPTIONS
          valueFrom:
            configMapKeyRef:
              name: {{ .Values.global.configMapName }}
              key: JAVA_TOOL_OPTIONS
        - name: OTEL_EXPORTER_OTLP_ENDPOINT
          value: {{ .Values.otel.endpoint }}
        - name: OTEL_METRICS_EXPORTER
          value: {{ .Values.otel.metricsExporter }}
        - name: OTEL_SERVICE_NAME
          value: {{ .Values.appName }}
        {{- end }}
        {{- if .Values.kafka_enabled }}
        - name: SPRING_CLOUD_STREAM_KAFKA_BINDER_BROKERS
          valueFrom:
            configMapKeyRef:
              name: {{ .Values.global.configMapName }}
              key: SPRING_CLOUD_STREAM_KAFKA_BINDER_BROKERS
        {{- end }}
{{- end }}
```

**Tính Năng Chính:**
- Số lượng replica động
- Cấu hình container image
- Biến môi trường có điều kiện sử dụng câu lệnh `if`:
  - **appname_enabled**: Tên ứng dụng Spring
  - **profile_enabled**: Spring profiles (dev, QA, prod)
  - **config_enabled**: Spring config import
  - **eureka_enabled**: URL dịch vụ Eureka
  - **resourceserver_enabled**: Cấu hình OAuth2 resource server (cho Gateway)
  - **otel_enabled**: Cấu hình OpenTelemetry cho observability
  - **kafka_enabled**: Cấu hình Kafka broker cho event-driven microservices

### 3. ConfigMap Template (configmap.yaml)

```yaml
{{- define "common.configmap" -}}
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Values.global.configMapName }}
data:
  SPRING_PROFILES_ACTIVE: {{ .Values.global.activeProfile }}
  SPRING_CONFIG_IMPORT: {{ .Values.global.configImport }}
  EUREKA_CLIENT_SERVICEURL_DEFAULTZONE: {{ .Values.global.eurekaServiceURL }}
  SPRING_SECURITY_OAUTH2_RESOURCESERVER_JWT_JWK_SET_URI: {{ .Values.global.keycloakURL }}
  JAVA_TOOL_OPTIONS: {{ .Values.global.javaToolOptions }}
{{- end }}
```

**Tính Năng Chính:**
- Sử dụng tiền tố `global` cho các giá trị chung cho tất cả microservices
- Cấu hình cụ thể theo môi trường (dev, QA, prod)
- Quản lý cấu hình tập trung

## Hiểu Cấu Trúc Template

### Ngôn Ngữ Template Helm

Helm sử dụng **ngôn ngữ template Go** và **ngôn ngữ template Sprig**. Các khái niệm chính:

- **`{{ .Values }}`**: Object chứa các giá trị từ `values.yaml`
- **`{{- -}}`**: Dấu gạch ngang loại bỏ khoảng trắng trước/sau câu lệnh
- **`{{- define "name" -}}`**: Định nghĩa một template có tên
- **`{{- end }}`**: Đóng khối define hoặc if
- **`{{- if .Values.property }}`**: Rendering có điều kiện

### Giá Trị Global vs. Giá Trị Cụ Thể Của Microservice

- **Giá trị Global**: Chung cho tất cả microservices (ví dụ: tên ConfigMap, URL Eureka)
- **Giá trị cụ thể của Microservice**: Riêng cho từng service (ví dụ: tên service, số lượng replica)

## Cấu Hình Values.yaml

Chart `eazybank-common` giữ `values.yaml` của nó **trống** vì:
- Đây là một common/library chart được sử dụng bởi các Helm charts khác
- Mỗi Helm chart của microservice cung cấp `values.yaml` riêng
- Templates có thể tái sử dụng, nhưng giá trị cụ thể cho từng microservice

## Lợi Ích Của Phương Pháp Này

1. **Triển Khai Bằng Một Lệnh**: Triển khai tất cả microservices chỉ với một lệnh
2. **Gỡ Cài Đặt Bằng Một Lệnh**: Xóa tất cả microservices chỉ với một lệnh
3. **Bảo Trì Dễ Dàng**: Quản lý bất kỳ số lượng Kubernetes manifests nào cho nhiều microservices
4. **Tái Sử Dụng**: Templates chung được chia sẻ cho tất cả microservices
5. **Linh Hoạt Môi Trường**: Các giá trị khác nhau cho môi trường dev, QA và prod

## Các Bước Tiếp Theo

Bước tiếp theo là tạo các Helm charts riêng cho từng microservice (accounts, loans, cards, v.v.) sẽ:
- Tận dụng chart `eazybank-common` như một dependency
- Cung cấp `values.yaml` riêng với cấu hình cụ thể cho microservice

## Tóm Tắt

Phương pháp Helm chart tùy chỉnh này cung cấp:
- Template chung cho service, deployment và ConfigMap
- Inject biến môi trường có điều kiện
- Hỗ trợ Spring Boot, Eureka, OAuth2, OpenTelemetry và Kafka
- Quản lý cấu hình linh hoạt qua các môi trường
- Đơn giản hóa việc triển khai microservices lên Kubernetes

Bằng cách tạo nền tảng này, các nhóm có thể quản lý hiệu quả kiến trúc microservice phức tạp trong Kubernetes với chi phí vận hành tối thiểu.