# Cài Đặt Grafana, Loki và Tempo trong Kubernetes

## Tổng Quan

Hướng dẫn này sẽ giúp bạn triển khai các thành phần liên quan đến Grafana (Loki, Tempo và Grafana) trong Kubernetes cluster bằng cách sử dụng Helm charts. Các thành phần này hoạt động cùng nhau để cung cấp khả năng quan sát toàn diện cho microservices:

- **Loki**: Tổng hợp logs từ các microservices riêng lẻ
- **Tempo**: Xử lý distributed tracing (theo dõi phân tán)
- **Grafana**: Trực quan hóa logs và traces

## Yêu Cầu Trước Khi Bắt Đầu

- Kubernetes cluster đang chạy trên máy local
- Helm đã được cài đặt và cấu hình
- Các microservices có OpenTelemetry Java agent

## Bước 1: Cài Đặt Grafana Loki

### Quy Trình Cài Đặt

1. **Sao Chép Helm Charts**: Sao chép các thư mục `grafana-loki` và `grafana-tempo` vào thư mục Helm của bạn.

2. **Điều Hướng đến Thư Mục Loki**:
   ```bash
   cd grafana-loki
   ```

3. **Build Dependencies**: Loki có dependencies với các charts khác như Memcached. Build chúng trước:
   ```bash
   helm dependencies build
   ```

4. **Cài Đặt Loki**: Quay lại thư mục cha và cài đặt chart:
   ```bash
   cd ..
   helm install loki grafana-loki
   ```

### Các Thành Phần Được Cài Đặt

Quá trình cài đặt Loki sẽ tạo ra nhiều thành phần trong Kubernetes cluster:
- Ingester
- Distributor
- Querier
- Promtail
- Compactor
- Gateway

### Lợi Ích Khi Sử Dụng Helm

Việc cài đặt thủ công các thành phần này sẽ yêu cầu:
- Sự hợp tác sâu rộng giữa Kubernetes administrators, developers và Grafana admins
- Hàng tháng nỗ lực để cấu hình đúng cách
- Quản lý cấu hình phức tạp

Với Helm, toàn bộ quá trình setup được đơn giản hóa và tự động hóa.

## Bước 2: Cài Đặt Grafana Tempo

### Thay Đổi Cấu Hình

1. **Mở File Values**: Điều hướng đến thư mục `grafana-tempo` và mở file `values.yaml`.

2. **Bật OpenTelemetry Protocol (OTLP)**: Tìm kiếm `otlp` trong file. Mặc định, cả HTTP và gRPC protocols đều bị tắt. Hãy bật chúng lên:
   ```yaml
   otlp:
     http:
       enabled: true
     grpc:
       enabled: true
   ```

   Thay đổi này là cần thiết để OpenTelemetry Java agent trong microservices của bạn có thể gửi chi tiết tracing đến Tempo.

### Quy Trình Cài Đặt

1. **Build Dependencies**:
   ```bash
   cd grafana-tempo
   helm dependencies build
   ```

2. **Cài Đặt Tempo**:
   ```bash
   cd ..
   helm install tempo grafana-tempo
   ```

### Các Thành Phần Được Cài Đặt

Quá trình cài đặt Tempo sẽ tạo ra:
- Ingester
- Distributor
- Querier
- Query-frontend
- Compactor
- Vulture

## Bước 3: Cấu Hình Microservices Kết Nối với Tempo

### Tìm URL Service Tempo

1. **Liệt Kê Các Kubernetes Services**:
   ```bash
   kubectl get services
   ```

2. **Xác Định Distributor Service**: Trong số tất cả các services liên quan đến Tempo (gossip-ring, ingester, generator, querier, vulture, compactor, distributor), OpenTelemetry agent nên kết nối đến service **distributor**.

3. **Cấu Hình Chi Tiết Kết Nối**:
   - Tên service: `tempo-distributor` (hoặc tương tự, dựa trên cài đặt của bạn)
   - Port: `4317`

### Cập Nhật ConfigMap

Thêm URL Tempo vào ConfigMap của microservices:
```yaml
tempo:
  url: tempo-distributor:4317
```

Điều này thiết lập kết nối giữa OpenTelemetry agent của microservices và Grafana Tempo.

### Hiểu Về Việc Chọn Service

Việc chọn distributor service dựa trên:
- Tài liệu chính thức của Grafana Tempo
- Best practices cho kiến trúc distributed tracing
- Vai trò của distributor trong việc nhận và xử lý dữ liệu trace đến

**Mẹo**: Luôn tham khảo tài liệu chính thức khi gặp các thách thức cấu hình tương tự.

## Bước Tiếp Theo

Với Loki và Tempo đã được cài đặt thành công, bước cuối cùng là cài đặt Grafana, công cụ sẽ cung cấp lớp visualization cho logs và traces của bạn.

## Những Điểm Chính Cần Nhớ

- Helm charts đơn giản hóa đáng kể các triển khai Kubernetes phức tạp
- Loki tổng hợp logs từ tất cả microservices
- Tempo xử lý distributed tracing với OpenTelemetry
- Cấu hình service đúng cách rất quan trọng cho giao tiếp giữa các microservices
- Luôn tham khảo tài liệu chính thức để biết chi tiết cấu hình