# Triển Khai Microservices Lên Google Cloud Kubernetes

## Tổng Quan

Hướng dẫn này sẽ giúp bạn triển khai các microservices Spring Boot lên Google Cloud Kubernetes cluster, bao gồm việc thiết lập cluster, cấu hình kết nối, và triển khai các thành phần khác nhau sử dụng Helm charts và Kubernetes manifests.

## Yêu Cầu Trước Khi Bắt Đầu

- Tài khoản Google Cloud có kích hoạt billing
- Google Cloud CLI (gcloud) đã cài đặt trên máy local
- kubectl đã cài đặt
- Docker Desktop với Kubernetes được bật
- Helm đã cài đặt
- Dự án microservices với Helm charts đã chuẩn bị sẵn

## Tạo Kubernetes Cluster Trên Google Cloud

### Tạo Cluster

1. Truy cập Google Cloud Console
2. Tạo một Kubernetes cluster mới
3. Đợi khoảng 5 phút để cluster được tạo xong
4. Xác nhận trạng thái cluster hiển thị dấu tích màu xanh

### Chi Tiết Cluster

Sau khi tạo xong, bạn có thể xem thông tin chi tiết về cluster:

- **Vị trí**: Zone và quốc gia nơi cluster được triển khai
- **Nodes**: Danh sách các nodes trong cluster (mặc định: 3 nodes)
- **Tài nguyên**: Thông tin CPU, memory, và disk cho mỗi node
- **Pods**: Các system pods được Google Cloud cài đặt để quản lý cluster

#### Các System Pods Mặc Định

Google Cloud tự động cài đặt một số pods để quản lý cluster:

- **gke-metrics-agent**: Thu thập các metrics về CPU, memory, và disk
- Các pods quản lý khác để duy trì sức khỏe của cluster

### Thêm Nodes

Nếu cần mở rộng cluster:
1. Click vào cluster trong Google Cloud Console
2. Chọn "Add node pool"
3. Cấu hình các thiết lập cho node pool mới

## Kết Nối Tới Google Cloud Kubernetes Cluster

### Thiết Lập Kết Nối

1. Trong Google Cloud Console, click vào ba chấm bên cạnh cluster của bạn
2. Chọn "Connect"
3. Copy lệnh gcloud được cung cấp
4. Thực thi lệnh trong terminal local của bạn:

```bash
gcloud container clusters get-credentials [CLUSTER_NAME] --zone [ZONE] --project [PROJECT_ID]
```

### Xác Minh Kết Nối

```bash
kubectl get nodes
```

Bạn sẽ thấy output hiển thị cả ba nodes trong cluster.

## Quản Lý Kubernetes Contexts

### Hiểu Về Contexts

Kubernetes contexts cho phép bạn kết nối đến nhiều clusters và chuyển đổi giữa chúng dễ dàng.

### Xem Các Contexts Có Sẵn

Trong Docker Desktop:
1. Click vào biểu tượng Docker Desktop
2. Vào phần cài đặt Kubernetes
3. Xem tất cả các contexts có sẵn

### Chuyển Đổi Contexts

Để chuyển sang local Kubernetes cluster:
```bash
# Chuyển sang Docker Desktop context
kubectl config use-context docker-desktop

# Xác minh - sẽ hiển thị 1 node
kubectl get nodes
```

Để chuyển lại sang Google Cloud cluster:
```bash
# Chuyển sang GKE context
kubectl config use-context [GKE_CONTEXT_NAME]

# Xác minh - sẽ hiển thị 3 nodes
kubectl get nodes
```

## Triển Khai Các Thành Phần Lên Kubernetes

### Cấu Trúc Dự Án

Di chuyển đến thư mục section_17 chứa:
- Các Kubernetes manifest files
- Helm charts cho microservices
- Các configuration files

### 1. Triển Khai Discovery Server

Đầu tiên, triển khai Eureka Discovery Server:

```bash
cd kubernetes
kubectl apply -f kubernetes-discoveryserver.yaml
```

**Lưu ý**: Nếu gặp lỗi connection timeout, chạy lại lệnh kết nối gcloud và thử lại.

### 2. Kiểm Tra Các Helm Installations

Kiểm tra các Helm installations hiện có:
```bash
helm ls
```

Ban đầu, sẽ không có installations nào trong remote cluster.

### 3. Triển Khai Keycloak (Quản Lý Định Danh và Truy Cập)

```bash
cd ../helm
helm install keycloak keycloak
```

Lệnh này triển khai Keycloak cho các dịch vụ authentication và authorization.

### 4. Triển Khai Kafka (Nền Tảng Message Streaming)

```bash
helm install kafka kafka
```

Lệnh này thiết lập Apache Kafka cho việc giao tiếp microservices theo hướng event-driven.

### 5. Triển Khai Prometheus (Giám Sát)

```bash
helm install prometheus kube-prometheus
```

Prometheus cung cấp khả năng thu thập metrics và giám sát.

### 6. Triển Khai Loki (Tập Hợp Logs)

```bash
helm install loki grafana-loki
```

Loki tập hợp logs từ tất cả microservices để quản lý logs tập trung.

### 7. Triển Khai Tempo (Distributed Tracing)

```bash
helm install tempo grafana-tempo
```

Tempo cung cấp khả năng distributed tracing để theo dõi requests qua các microservices.

### 8. Triển Khai Grafana (Trực Quan Hóa)

```bash
helm install grafana grafana
```

Grafana cung cấp dashboards để trực quan hóa metrics, logs, và traces.

### 9. Triển Khai Microservices Với Helm

Cuối cùng, triển khai tất cả Spring Boot microservices:

```bash
cd ../environments
helm install easybank prod-env
```

Lệnh này:
- Triển khai tất cả microservices được định nghĩa trong prod-env Helm chart
- Sử dụng cấu hình môi trường production
- Tạo tất cả các Kubernetes resources cần thiết (Deployments, Services, ConfigMaps, v.v.)

## Quy Trình Triển Khai

### Thời Gian

- Discovery Server: ~2-3 phút
- Mỗi Helm chart: ~3-5 phút
- Triển khai Microservices: ~5-10 phút

### Giám Sát Quá Trình Triển Khai

Kiểm tra trạng thái pods:
```bash
kubectl get pods
```

Kiểm tra trạng thái deployments:
```bash
kubectl get deployments
```

Xem các service endpoints:
```bash
kubectl get services
```

## Sự Khác Biệt So Với Local Kubernetes

### Điểm Tương Đồng

- Cùng Helm charts và Kubernetes manifests
- Cùng các lệnh và quy trình triển khai
- Cùng kiến trúc microservices

### Điểm Khác Biệt

- **Dung lượng**: Cloud cluster có nhiều CPU, memory, và storage hơn
- **Tính Sẵn Sàng Cao**: Nhiều nodes cung cấp khả năng dự phòng
- **Khả Năng Mở Rộng**: Dễ dàng thêm nodes khi cần
- **Dịch Vụ Quản Lý**: Google Cloud xử lý bảo trì cluster
- **Mạng**: Thiết lập networking khác so với local

## Xử Lý Sự Cố

### Lỗi Connection Timeout

Nếu gặp lỗi connection timeout:
1. Chạy lại lệnh kết nối gcloud
2. Kiểm tra kết nối internet
3. Xác minh cluster đang chạy trong Google Cloud Console

### Vấn Đề Context

Nếu các lệnh kubectl không hoạt động:
1. Xác minh bạn đang ở đúng context: `kubectl config current-context`
2. Chuyển sang context phù hợp nếu cần
3. Chạy `kubectl get nodes` để xác nhận kết nối

### Lỗi Triển Khai

Nếu pods không khởi động:
1. Kiểm tra logs của pods: `kubectl logs [POD_NAME]`
2. Mô tả pod để xem events: `kubectl describe pod [POD_NAME]`
3. Xác minh resource limits và tính khả dụng
4. Kiểm tra ConfigMaps và Secrets được tạo đúng cách

## Các Bước Tiếp Theo

Sau khi triển khai hoàn tất (5-10 phút):
1. Xác minh tất cả pods đang chạy
2. Truy cập Grafana dashboard để giám sát
3. Kiểm thử các endpoints của microservices
4. Cấu hình Keycloak với users và roles
5. Thiết lập ingress cho truy cập từ bên ngoài

## Best Practices (Thực Hành Tốt Nhất)

1. **Sử dụng namespaces** để tổ chức resources
2. **Đặt resource limits** cho tất cả containers
3. **Cấu hình health checks** (liveness và readiness probes)
4. **Sử dụng ConfigMaps và Secrets** cho cấu hình
5. **Bật monitoring và logging** ngay từ đầu
6. **Triển khai RBAC đúng cách** cho bảo mật
7. **Sao lưu định kỳ** dữ liệu persistent
8. **Sử dụng Helm cho deployments nhất quán** qua các môi trường

## Tóm Tắt

Hướng dẫn này đã trình bày quy trình hoàn chỉnh để triển khai Spring Boot microservices lên Google Cloud Kubernetes, bao gồm:
- Tạo và kết nối đến GKE cluster
- Quản lý nhiều Kubernetes contexts
- Triển khai các thành phần cơ sở hạ tầng (Keycloak, Kafka, Prometheus, Loki, Tempo, Grafana)
- Triển khai microservices sử dụng Helm charts

Cloud Kubernetes cluster cung cấp môi trường production-ready với tính sẵn sàng cao, khả năng mở rộng, và cơ sở hạ tầng được quản lý.