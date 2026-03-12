# Triển khai Kafka lên Kubernetes với Helm Charts

## Tổng quan

Hướng dẫn này trình bày cách triển khai Apache Kafka vào Kubernetes cluster sử dụng Helm charts, sau khi đã cài đặt thành công Keycloak. Chúng ta sẽ tìm hiểu các lưu ý quan trọng cho môi trường phát triển local và giải quyết các vấn đề thường gặp khi cài đặt Helm.

## Yêu cầu tiên quyết

- Kubernetes cluster đang chạy trên máy local
- Helm đã được cài đặt và cấu hình
- Keycloak đã được triển khai trong cluster
- kubectl đã được cấu hình để truy cập cluster

## Xác minh cài đặt Keycloak

Trước khi tiến hành với Kafka, hãy xác minh rằng Keycloak đã được cài đặt đúng cách:

1. **Kiểm tra Pods**: Điều hướng đến phần Pods trong Kubernetes dashboard
   - Bạn sẽ thấy hai pods:
     - Pod Keycloak
     - Pod Keycloak PostgreSQL

2. **Kiểm tra Services**: Xác minh các services liên quan đến Keycloak đang chạy
   - Tất cả services phải hiển thị trong phần Services

3. **Kiểm tra ConfigMaps và Secrets**: Xác nhận các thành phần Keycloak có mặt trong cả ConfigMaps và Secrets

## Quan trọng: Hạn chế của Helm Uninstall

### Vấn đề với PVC

Có một lỗi đã biết trong Helm liên quan đến Persistent Volume Claims (PVCs):

- Khi bạn gỡ cài đặt Helm chart bằng lệnh `helm uninstall`, các PVCs được tạo trong quá trình cài đặt **không tự động bị xóa**
- PVCs cho phép pods yêu cầu không gian lưu trữ bên trong worker nodes
- Các PVCs còn tồn tại có thể gây ra vấn đề khi cài đặt lại cùng một Helm chart

### Kiểm tra các PVCs hiện có

Để xem tất cả PVCs trong cluster của bạn:

```bash
kubectl get pvc
```

### Xóa PVCs

Bạn có hai cách để xóa PVCs:

**Cách 1: Sử dụng Kubernetes Dashboard**
1. Điều hướng đến phần PVC
2. Chọn PVC bạn muốn xóa
3. Nhấp vào nút delete

**Cách 2: Sử dụng lệnh kubectl**

```bash
kubectl delete pvc <tên-pvc>
```

Ví dụ: Nếu bạn thấy các PVCs từ cài đặt WordPress trước đó, hãy xóa chúng trước khi cài đặt lại để tránh xung đột.

## Triển khai Kafka với Helm

### Bước 1: Chuẩn bị Kafka Helm Chart

1. Lấy Kafka Helm chart và đặt nó vào thư mục Helm charts của bạn
2. Chart sẽ được commit vào GitHub repository với tất cả các cấu hình cần thiết

### Bước 2: Chỉnh sửa values.yaml cho môi trường phát triển Local

Kafka Helm chart mặc định được cấu hình cho môi trường production, điều này có thể tiêu tốn quá nhiều tài nguyên cho phát triển local.

#### Giảm số lượng Replica

1. Mở file `values.yaml` trong thư mục Kafka Helm chart
2. Tìm kiếm `replicaCount`
3. Thay đổi giá trị từ `3` thành `1`:

```yaml
replicaCount: 1
```

**Lưu ý**: Trong môi trường production, quản trị viên Kafka của bạn sẽ quản lý số lượng replica và các cài đặt production khác.

#### Đơn giản hóa cấu hình bảo mật

Mặc định, Kafka sử dụng các giao thức truyền thông bảo mật phù hợp cho production. Đối với môi trường test local, chúng ta có thể đơn giản hóa điều này.

1. Tìm kiếm `SASL_PLAINTEXT` trong `values.yaml`
2. Thay thế tất cả các lần xuất hiện của `SASL_PLAINTEXT` bằng `PLAINTEXT`

**Các giá trị giao thức hợp lệ**:
- `PLAINTEXT` (cho phát triển local)
- `SSL`
- `SASL_PLAINTEXT`
- `SASL_SSL`

**Quan trọng**: Chỉ thay đổi các giá trị trong cấu hình thực tế, không thay đổi trong phần comments.

### Bước 3: Build Dependencies

Trước khi cài đặt, build các dependencies của Helm chart:

```bash
cd kafka
helm dependencies build
```

### Bước 4: Cài đặt Kafka

Quay lại thư mục cha và chạy:

```bash
helm install kafka kafka
```

## Xác minh cài đặt Kafka

### Thông tin kết nối

Sau khi cài đặt, bạn sẽ thấy output chứa các thông tin kết nối quan trọng:

- **Port**: 9092
- **DNS Name**: Mỗi Kafka broker có thể được truy cập bởi producers thông qua DNS name được cung cấp

Các DNS names này cần được cấu hình trong các microservices của bạn (accounts microservice và message microservice) để kích hoạt giao tiếp bất đồng bộ với Kafka.

### Xác minh trong Kubernetes Dashboard

1. **Kiểm tra Pods**: Điều hướng đến phần Pods
   - Xác minh các pods liên quan đến Kafka đang chạy

2. **Kiểm tra Services**: Điều hướng đến phần Services
   - Xác nhận các services Kafka đã có mặt
   - Tất cả services phải được định nghĩa là loại `ClusterIP`

3. **Kiểm tra ConfigMaps**: Xác minh các giá trị ConfigMap bao gồm chi tiết kết nối Kafka
   - Các giá trị này được định nghĩa trong các Helm charts theo từng environment

## Cấu hình ConfigMap

Đảm bảo các giá trị ConfigMap trong các Helm charts theo environment của bạn bao gồm các DNS names của Kafka broker. Điều này cho phép các microservices của bạn kết nối với Kafka để truyền tin bất đồng bộ.

## Kiểm tra thiết lập

Mặc dù output của Helm installation cung cấp hướng dẫn để kiểm tra với các tin nhắn mẫu, bạn có thể xác thực thiết lập thông qua các ứng dụng của mình. Các accounts và message microservices của bạn sẽ gửi các tin nhắn thực tế để kiểm tra tích hợp Kafka.

## Tóm tắt

Bạn đã hoàn thành thành công:
- ✅ Xác minh cài đặt Keycloak trong Kubernetes
- ✅ Hiểu rõ hạn chế PVC của Helm và quy trình dọn dẹp
- ✅ Cấu hình Kafka Helm chart cho phát triển local
- ✅ Triển khai Kafka lên Kubernetes cluster
- ✅ Xác minh cài đặt và services của Kafka

Kubernetes cluster của bạn giờ đã sẵn sàng với cả Keycloak cho authentication/authorization và Kafka cho giao tiếp bất đồng bộ hướng sự kiện giữa các microservices.

## Các bước tiếp theo

Trong bài giảng tiếp theo, chúng ta sẽ cấu hình các microservices để giao tiếp với Kafka và triển khai các mẫu hướng sự kiện cho messaging bất đồng bộ.