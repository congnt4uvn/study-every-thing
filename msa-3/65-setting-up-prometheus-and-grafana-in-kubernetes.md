# Cài Đặt Prometheus và Grafana trong Kubernetes

## Tổng Quan

Hướng dẫn này trình bày cách cài đặt Prometheus để thu thập metrics và chuẩn bị triển khai Grafana trong Kubernetes cluster để giám sát các microservices được xây dựng bằng Java Spring Boot.

## Yêu Cầu Trước Khi Bắt Đầu

- Kubernetes cluster đang hoạt động
- Đã cài đặt Helm
- Đã tải về Bitnami Helm charts repository
- Các microservices đã được cấu hình Spring Boot Actuator

## Cài Đặt Prometheus

### Bước 1: Chuẩn Bị Helm Chart

1. Điều hướng đến Bitnami repository và tìm thư mục `kube-prometheus`
2. Sao chép thư mục `kube-prometheus` vào thư mục helm của bạn

```bash
# Sao chép thư mục kube-prometheus vào thư mục helm
cp -r bitnami/kube-prometheus ./helm/
```

### Bước 2: Cấu Hình values.yaml

Mở file `values.yaml` trong thư mục `kube-prometheus` và thực hiện các thay đổi sau:

#### Bật Additional Scrape Configs

Tìm kiếm "additional scrape configs" và chỉnh sửa:

```yaml
additionalScrapeConfigs:
  enabled: true
  type: internal  # Thay đổi từ external sang internal
```

**Lý do**: Chúng ta đặt type là `internal` vì tất cả microservices đều nằm trong Kubernetes cluster, nên không cần thu thập metrics từ các nguồn bên ngoài.

#### Cấu Hình Jobs Cho Microservices

Trong danh sách internal job list, thêm cấu hình cho từng microservice theo định dạng JSON:

```json
[
  {
    "job_name": "config-server",
    "metrics_path": "/actuator/prometheus",
    "static_configs": [
      {
        "targets": ["configserver:8071"]
      }
    ]
  },
  {
    "job_name": "eureka-server",
    "metrics_path": "/actuator/prometheus",
    "static_configs": [
      {
        "targets": ["eurekaserver:8070"]
      }
    ]
  },
  {
    "job_name": "accounts",
    "metrics_path": "/actuator/prometheus",
    "static_configs": [
      {
        "targets": ["accounts:8080"]
      }
    ]
  },
  {
    "job_name": "loans",
    "metrics_path": "/actuator/prometheus",
    "static_configs": [
      {
        "targets": ["loans:8090"]
      }
    ]
  },
  {
    "job_name": "cards",
    "metrics_path": "/actuator/prometheus",
    "static_configs": [
      {
        "targets": ["cards:9000"]
      }
    ]
  },
  {
    "job_name": "gateway-server",
    "metrics_path": "/actuator/prometheus",
    "static_configs": [
      {
        "targets": ["gatewayserver:8072"]
      }
    ]
  }
]
```

**Chi Tiết Cấu Hình**:
- **job_name**: Định danh cho microservice
- **metrics_path**: Endpoint của Actuator để expose metrics cho Prometheus
- **targets**: Tên service và port trong Kubernetes cluster

### Bước 3: Build Helm Chart

Điều hướng đến thư mục `kube-prometheus` và build các dependencies:

```bash
cd helm/kube-prometheus
helm dependency build
```

### Bước 4: Cài Đặt Prometheus

Cài đặt Prometheus sử dụng Helm:

```bash
cd ..
helm install prometheus ./kube-prometheus
```

Lệnh này cài đặt Prometheus với tên release là "prometheus".

### Bước 5: Truy Cập Prometheus (Tùy Chọn)

Mặc định, Prometheus được cài đặt với ClusterIP, khiến nó không thể truy cập từ bên ngoài cluster. Để truy cập tạm thời, sử dụng port forwarding:

```bash
kubectl port-forward svc/prometheus-kube-prometheus-prometheus 9090:9090
```

**Lưu ý**: Đợi 1-2 phút sau khi cài đặt để tất cả pods sẵn sáng trước khi chạy lệnh port-forward.

### Bước 6: Xác Minh Cài Đặt Prometheus

1. Mở trình duyệt và truy cập `http://localhost:9090`
2. Vào **Status → Targets** để xem tất cả các targets đã cấu hình
3. Ban đầu, các microservices sẽ hiển thị trạng thái màu đỏ (down) vì chúng chưa được triển khai
4. Prometheus cũng sẽ tự động giám sát các thành phần khác của Kubernetes cluster

### Bước 7: Dừng Port Forwarding

Nhấn `Ctrl+C` trong terminal để dừng port forwarding. Sau khi dừng, Prometheus sẽ không còn truy cập được từ hệ thống local của bạn.

## Các Bước Tiếp Theo

Sau khi cài đặt thành công Prometheus, giai đoạn tiếp theo bao gồm:

1. Cài đặt **Grafana** để trực quan hóa dữ liệu
2. Cấu hình **Loki** để tổng hợp logs
3. Cài đặt **Tempo** cho distributed tracing
4. Tích hợp Grafana với Prometheus để tạo dashboards cho metrics
5. Triển khai microservices lên Kubernetes cluster để kiểm thử end-to-end

## Những Điểm Chính Cần Nhớ

- Prometheus yêu cầu cấu hình scrape tùy chỉnh cho từng microservice
- Tất cả cấu hình sử dụng tên service và port nội bộ trong Kubernetes
- Endpoint actuator Prometheus (`/actuator/prometheus`) expose metrics theo định dạng mà Prometheus có thể scrape
- Prometheus tự động giám sát nhiều thành phần của Kubernetes cluster trong các thiết lập production-ready
- Port forwarding hữu ích cho việc truy cập tạm thời các services được cấu hình với ClusterIP

## Khắc Phục Sự Cố

**Vấn đề**: Lệnh port forward thất bại  
**Giải pháp**: Đợi cho pods của Prometheus hoàn toàn sẵn sàng. Kiểm tra trạng thái pod bằng `kubectl get pods`

**Vấn đề**: Targets hiển thị trạng thái down  
**Giải pháp**: Điều này là bình thường trước khi triển khai microservices. Triển khai microservices của bạn để thấy chúng hoạt động.

**Vấn đề**: Không thể truy cập Prometheus sau khi dừng port-forward  
**Giải pháp**: Đây là hành vi mong đợi. Khởi động lại lệnh port-forward hoặc cấu hình Ingress để truy cập vĩnh viễn.

## Kết Luận

Bạn đã cài đặt thành công Prometheus trong Kubernetes cluster của mình. Nền tảng giám sát đã sẵn sàng để thu thập metrics từ các Spring Boot microservices của bạn sau khi chúng được triển khai.