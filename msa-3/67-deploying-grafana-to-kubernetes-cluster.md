# Triển khai Grafana lên Kubernetes Cluster với Helm

## Tổng quan

Hướng dẫn này đề cập đến quá trình thiết lập Grafana trong Kubernetes cluster sử dụng Helm charts, bao gồm cấu hình các nguồn dữ liệu (data sources) để tích hợp với Prometheus, Loki và Tempo.

## Yêu cầu trước khi bắt đầu

- Kubernetes cluster đang hoạt động
- Helm đã được cài đặt
- Bitnami Helm charts có sẵn
- Prometheus, Loki và Tempo đã được triển khai trong cluster

## Các bước cài đặt

### 1. Chuẩn bị Grafana Helm Chart

Đầu tiên, sao chép Grafana Helm chart từ thư mục Bitnami vào thư mục helm của bạn:

```bash
# Sao chép Grafana helm chart vào thư mục helm
cp -r bitnami/grafana helm/grafana
```

**Lưu ý**: Khuyến nghị sử dụng các Helm charts đã được commit vào GitHub repository để tránh phải thực hiện các thay đổi cấu hình thủ công trong file `values.yaml`.

### 2. Cấu hình Data Sources

Trước khi triển khai Grafana, bạn cần cấu hình các kết nối data source tới Prometheus, Loki và Tempo trong file `values.yaml`.

#### Xác định vị trí cấu hình Data Source

Mở file `values.yaml` và tìm kiếm "data source". Bạn sẽ tìm thấy một phần về data sources nơi bạn cần định nghĩa chi tiết data source dưới phần tử `secretDefinition`.

#### Cấu hình Data Source

Thay thế cấu hình mặc định bằng cấu trúc sau:

```yaml
secretDefinition:
  apiVersion: 1
  deleteDatasources:
    - name: Prometheus
    - name: Tempo
    - name: Loki
  datasources:
    - name: Prometheus
      type: prometheus
      url: http://prometheus-server-dns-name
      access: proxy
      isDefault: true
    
    - name: Tempo
      type: tempo
      url: http://grafana-tempo-query-frontend:3200
      access: proxy
    
    - name: Loki
      type: loki
      url: http://loki-gateway:80
      access: proxy
      jsonData:
        derivedFields:
          - datasourceUid: tempo
            matcherRegex: "traceId=(\\w+)"
            name: TraceId
            url: "$${__value.raw}"
```

#### Chi tiết cấu hình quan trọng

- **Prometheus**: Sử dụng tên DNS của Prometheus service trong Kubernetes cluster
- **Tempo**: Kết nối tới service `grafana-tempo-query-frontend` trên port 3200
- **Loki**: Kết nối tới service `loki-gateway` trên port 80
- **Derived Fields**: Được cấu hình để tích hợp Loki với Tempo cho việc tương quan traces

### 3. Build Helm Chart

Di chuyển vào thư mục Grafana và build dependencies:

```bash
cd helm/grafana
helm dependencies build
```

### 4. Cài đặt Grafana

Quay lại thư mục cha và cài đặt Grafana:

```bash
cd ..
helm install grafana grafana
```

Mặc định, Grafana sẽ được expose dưới dạng ClusterIP service.

### 5. Truy cập Grafana

Để truy cập Grafana cho mục đích debug hoặc quản trị, sử dụng kubectl port forwarding:

```bash
kubectl port-forward service/grafana 3000:3000
```

**Lưu ý**: Ban đầu, bạn có thể thử port 8080, nhưng nếu có microservices khác (như accounts microservice) đang sử dụng port đó, hãy chuyển sang port 3000 để tránh xung đột.

Truy cập Grafana trong trình duyệt tại: `http://localhost:3000`

### 6. Thông tin đăng nhập

- **Username**: `admin`
- **Password**: Lấy bằng các lệnh sau:

```bash
kubectl get secret grafana-admin -o jsonpath="{.data.admin-password}" | base64 --decode
```

Nhập thông tin đăng nhập vào trang login để truy cập Grafana.

### 7. Xác minh kết nối Data Source

Sau khi đăng nhập:

1. Điều hướng tới **Explore** trong giao diện Grafana
2. Kiểm tra menu dropdown - bạn sẽ thấy ba data sources:
   - Loki
   - Prometheus
   - Tempo

Điều này xác nhận rằng thiết lập Grafana của bạn đã hoàn tất và tất cả các data sources đã được cấu hình đúng cách.

## Quản lý Helm Releases

Để xem tất cả các Helm releases trong cluster:

```bash
helm ls
```

Lệnh này sẽ hiển thị tất cả các installations bao gồm:
- Grafana
- Kafka
- Keycloak
- Loki
- Prometheus
- Tempo

## Quản lý Port Forwarding

Để dừng port forwarding, chỉ cần kết thúc lệnh bằng `Ctrl+C`. Bạn có thể khởi động lại bất cứ lúc nào cần truy cập Grafana bằng cách chạy lại lệnh port-forward.

## Các bước tiếp theo

Với Grafana đã được triển khai và cấu hình thành công, bạn đã sẵn sàng triển khai các microservices của mình lên Kubernetes cluster. Observability stack (Prometheus, Loki, Tempo và Grafana) giờ đây đã sẵn sàng để giám sát và khắc phục sự cố cho các microservices của bạn.

## Tóm tắt

Trong hướng dẫn này, bạn đã học cách:
- Cấu hình data sources của Grafana trong `values.yaml`
- Build và cài đặt Grafana sử dụng Helm
- Truy cập Grafana sử dụng kubectl port-forward
- Xác minh kết nối data sources
- Quản lý Helm releases trong Kubernetes cluster

Thiết lập Grafana cung cấp một nền tảng giám sát và observability tập trung cho kiến trúc microservices của bạn.