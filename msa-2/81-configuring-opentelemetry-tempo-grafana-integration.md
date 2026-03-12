# Cấu hình Tích hợp OpenTelemetry, Tempo và Grafana cho Distributed Tracing

## Tổng quan

Hướng dẫn này sẽ giúp bạn cập nhật cấu hình Docker Compose để tích hợp OpenTelemetry, Tempo và Grafana nhằm theo dõi phân tán (distributed tracing) trong kiến trúc microservices Spring Boot.

## Yêu cầu

- Đã cài đặt Docker và Docker Compose
- Kiến trúc microservices hiện có với Grafana và Prometheus
- Đã thêm dependency OpenTelemetry vào pom.xml

## Bước 1: Cấu hình Thuộc tính Môi trường Chung

Mở file `common-config.yml` trong thư mục docker-compose (profile prod).

Thêm các thuộc tính môi trường vào `microservice-base-config` (không phải `microservice-configserver-config` để đảm bảo tất cả microservices đều nhận được các thuộc tính này):

```yaml
microservice-base-config:
  environment:
    JAVA_TOOL_OPTIONS: "-javaagent:/path/to/opentelemetry-javaagent.jar"
    OTEL_EXPORTER_OTLP_ENDPOINT: "http://tempo:4317"
    OTEL_METRICS_EXPORTER: "none"
```

### Chi tiết Cấu hình

- **JAVA_TOOL_OPTIONS**: Chỉ định tham số javaagent với đường dẫn đến file JAR của OpenTelemetry (có sẵn trong containers sau khi thêm dependency vào pom.xml)
- **OTEL_EXPORTER_OTLP_ENDPOINT**: Định nghĩa endpoint của dịch vụ Tempo nơi OpenTelemetry sẽ gửi thông tin tracing
- **OTEL_METRICS_EXPORTER**: Đặt giá trị "none" vì Prometheus đã được sử dụng để xuất metrics

## Bước 2: Cấu hình Biến Môi trường cho từng Service

Trong file `docker-compose.yml`, thêm thuộc tính môi trường `OTEL_SERVICE_NAME` cho mỗi microservice:

### Config Server
```yaml
configserver:
  environment:
    OTEL_SERVICE_NAME: "configserver"
```

### Eureka Server
```yaml
eurekaserver:
  environment:
    OTEL_SERVICE_NAME: "eurekaserver"
```

### Accounts Microservice
```yaml
accounts:
  environment:
    OTEL_SERVICE_NAME: "accounts"
```

### Loans Microservice
```yaml
loans:
  environment:
    OTEL_SERVICE_NAME: "loans"
```

### Cards Microservice
```yaml
cards:
  environment:
    OTEL_SERVICE_NAME: "cards"
```

### Gateway Server
```yaml
gatewayserver:
  environment:
    OTEL_SERVICE_NAME: "gatewayserver"
```

**Lưu ý**: `OTEL_SERVICE_NAME` nên khớp với `SPRING_APPLICATION_NAME` để đảm bảo tính nhất quán, mặc dù điều này không bắt buộc.

## Bước 3: Tạo Cấu hình Tempo

Tạo cấu trúc thư mục mới: `observability/tempo/`

Tạo file cấu hình `tempo.yml` với nội dung sau:

```yaml
server:
  http_listen_port: 3100

distributor:
  receivers:
    otlp:
      protocols:
        grpc:
        http:

storage:
  trace:
    backend: local
    local:
      path: /tmp/tempo/traces
    wal:
      path: /tmp/tempo/wal
    pool:
      max_workers: 100
      queue_depth: 10000

query_frontend:
  search:
    max_duration: 0s

compactor:
  compaction:
    block_retention: 1h

metrics_generator:
  registry:
    external_labels:
      source: tempo
  storage:
    path: /tmp/tempo/generator/wal
```

### Các Tham số Cấu hình

- **http_listen_port**: 3100 - Cổng mà Tempo lắng nghe các yêu cầu HTTP
- **trace_idle_period**: 10 giây - Thời gian trước khi coi một trace là idle
- **max_block_bytes**: Kích thước tối đa của các block trace
- **max_block_duration**: Thời gian tối đa cho các block trace

**Lưu ý**: Các cấu hình này nên tuân theo tài liệu chính thức của Tempo và thường được quản lý bởi đội platform trong môi trường production.

## Bước 4: Thêm Service Tempo vào Docker Compose

Thêm service Tempo trong file `docker-compose.yml` (phía trên service Grafana):

```yaml
tempo:
  image: grafana/tempo:latest
  container_name: tempo
  command: [ "-config.file=/etc/tempo-config.yml" ]
  ports:
    - "3110:3100"  # Cổng external khác vì 3100 đã được gateway sử dụng
    - "4317:4317"
  volumes:
    - ./observability/tempo/tempo.yml:/etc/tempo-config.yml:ro
  networks:
    - microservices-network
```

**Quan trọng**: Cổng 3100 được map sang 3110 ở bên ngoài vì cổng 3100 đã được gateway service sử dụng.

## Bước 5: Cấu hình Data Source Grafana cho Tempo

Cập nhật file `datasource.yml` trong thư mục cấu hình Grafana.

Thêm data source Tempo cùng với Prometheus và Loki hiện có:

```yaml
apiVersion: 1

deleteDatasources:
  - name: Tempo
    orgId: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    
  - name: Loki
    type: loki
    access: proxy
    url: http://loki:3100

  - name: Tempo
    type: tempo
    access: proxy
    uid: tempo
    url: http://tempo:3100
    jsonData:
      httpMethod: GET
      tracesToLogs:
        datasourceUid: loki
```

### Cấu hình Data Source

- **name**: Tempo
- **type**: tempo
- **uid**: tempo (định danh duy nhất)
- **url**: http://tempo:3100 - Grafana kết nối với Tempo thông qua tên service và cổng này

## Tổng quan Kiến trúc

```
Microservices (với OpenTelemetry Agent)
    ↓ (traces qua OTLP)
Tempo (Cổng 4317)
    ↓ (truy vấn traces)
Grafana (Cổng 3000)
    → Tempo Data Source
```

## Kiểm tra

Sau khi áp dụng các thay đổi này:

1. Khởi động tất cả ứng dụng bằng Docker Compose
2. Truy cập Grafana dashboard
3. Điều hướng đến Explore → Chọn data source Tempo
4. Thực hiện một số request qua các microservices của bạn
5. Xem distributed traces trong Grafana

## Lợi ích

- **Tầm nhìn end-to-end**: Theo dõi các request qua nhiều microservices
- **Tối ưu hiệu suất**: Xác định các điểm nghẽn và vấn đề về độ trễ
- **Debug**: Theo dõi luồng request qua hệ thống
- **Tích hợp**: Tích hợp liền mạch với Grafana, Prometheus và Loki hiện có

## Bước tiếp theo

Trong bài giảng tiếp theo, chúng ta sẽ khởi động tất cả các ứng dụng và xem distributed tracing hoạt động.

## Tóm tắt

Cấu hình này cho phép distributed tracing cho các microservices Spring Boot sử dụng:
- **OpenTelemetry**: Instrumentation tracing dựa trên agent
- **Tempo**: Backend distributed tracing
- **Grafana**: Giao diện trực quan hóa và truy vấn

Thiết lập này cung cấp khả năng quan sát toàn diện cùng với hạ tầng metrics (Prometheus) và logs (Loki) hiện có.