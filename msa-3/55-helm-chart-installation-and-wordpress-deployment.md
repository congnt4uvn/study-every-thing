# Hướng Dẫn Cài Đặt Helm Chart và Triển Khai WordPress

## Giới Thiệu

Hướng dẫn này minh họa sức mạnh của Helm thông qua việc cài đặt một chart mẫu từ tài liệu chính thức. Chúng ta sẽ triển khai một website WordPress trên Kubernetes cluster cục bộ sử dụng Helm charts.

## Yêu Cầu Trước Khi Bắt Đầu

Trước khi bắt đầu, hãy đảm bảo Kubernetes cluster cục bộ của bạn đang hoạt động.

### Kiểm Tra Trạng Thái Kubernetes Cluster

1. **Sử dụng Docker Dashboard:**
   - Mở Docker Dashboard
   - Xác nhận thông báo: "Kubernetes is running"

2. **Sử dụng lệnh kubectl:**
   ```bash
   kubectl get services
   ```
   Lệnh này liệt kê tất cả các services trong Kubernetes cluster cục bộ. Ban đầu, bạn chỉ thấy service mặc định của Kubernetes.

### Kiểm Tra Helm

Kiểm tra các cài đặt Helm hiện có trong cluster:

```bash
helm ls
```

Nếu chưa cài đặt chart nào, lệnh này sẽ trả về danh sách rỗng.

## Helm Kết Nối Với Kubernetes Như Thế Nào

Helm tự động kết nối với Kubernetes cluster bằng cách đọc thông tin cấu hình được lưu trữ cục bộ trên hệ thống của bạn.

### Vị Trí File Cấu Hình Kubernetes

- **Windows:** `C:\Users\<username>\.kube\config`
- **Linux/Mac:** `~/.kube/config`

File config này chứa tất cả thông tin kết nối mà cả `kubectl` và `helm` sử dụng để tương tác với Kubernetes cluster. Cấu hình thường bao gồm chi tiết về Docker Desktop cluster hoặc các Kubernetes cluster khác mà bạn đã kết nối.

## Tìm Kiếm Helm Charts

Helm cung cấp chức năng tìm kiếm mạnh mẽ để tìm các chart từ các repository công khai.

### Sử Dụng Helm Search Hub

Để tìm kiếm các chart WordPress:

```bash
helm search hub wordpress
```

Lệnh này tìm kiếm trên Artifact Hub tất cả các chart WordPress có sẵn từ nhiều repository khác nhau. Bạn sẽ thấy kết quả từ nhiều nguồn, bao gồm Bitnami - một repository nổi tiếng với các Helm chart sẵn sàng cho production.

## Thêm Repository Bitnami

Trước khi cài đặt chart từ Bitnami, bạn cần thêm repository vào cấu hình Helm cục bộ.

### Thêm Repository Bitnami

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
```

Nếu repository đã tồn tại, bạn sẽ nhận được thông báo cho biết nó đã được cấu hình. Nếu chưa, nó sẽ được thêm thành công.

## Cài Đặt WordPress Sử Dụng Helm

Bây giờ bạn có thể cài đặt Helm chart WordPress từ repository Bitnami.

### Lệnh Cài Đặt

```bash
helm install happy-panda bitnami/wordpress
```

**Giải Thích Lệnh:**
- `helm install` - Lệnh cài đặt
- `happy-panda` - Tên release (bạn có thể chọn tên bất kỳ)
- `bitnami/wordpress` - Tên repository và tên chart

### Sau Khi Cài Đặt

Sau khi chạy lệnh, Helm sẽ:
1. Triển khai tất cả các Kubernetes resources cần thiết
2. Cung cấp hướng dẫn truy cập trang WordPress
3. Hiển thị các lệnh để lấy URL và thông tin đăng nhập WordPress

**Lưu ý:** Có thể mất 1-2 phút để LoadBalancer IP khả dụng.

## Truy Cập WordPress

### Lấy URL WordPress

Chạy các lệnh được cung cấp trong output cài đặt để lấy URL:

```bash
# Các lệnh cụ thể sẽ được hiển thị trong terminal output của bạn
```

Thông thường, bạn sẽ truy cập:
- **Trang Công Khai:** `http://localhost`
- **Trang Quản Trị:** `http://localhost/admin`

### Lấy Thông Tin Đăng Nhập Admin

Lấy username:
```bash
echo Username: user
```

Lấy password:
```bash
# Lệnh sẽ được cung cấp trong installation output
```

## Helm Đã Triển Khai Gì Đằng Sau

Lệnh `helm install` duy nhất đã tạo ra nhiều Kubernetes resources:

### Deployments
- WordPress application deployment
- MariaDB database deployment

### Pods
- WordPress pod(s)
- MariaDB pod(s)

### ReplicaSets
- Đảm bảo số lượng pod replicas mong muốn

### Services
- **WordPress:** LoadBalancer service type (có thể truy cập từ bên ngoài cluster)
- **MariaDB:** ClusterIP service type (chỉ truy cập nội bộ)

### ConfigMaps
- Chứa các thuộc tính môi trường và cài đặt cấu hình

### Secrets
- `happy-panda-wordpress` - Thông tin đăng nhập WordPress
- Thông tin đăng nhập database MariaDB

Tất cả các resources này làm việc cùng nhau để tạo ra một website WordPress sẵn sàng cho production.

## Khám Phá Các File Helm Chart

### Xác Định Vị Trí Cache Helm Chart

Tìm nơi Helm lưu trữ các chart đã tải xuống:

```bash
helm env
```

Tìm biến `HELM_CACHE_HOME`, thường là:
- **Windows:** `C:\Users\<username>\Library\Caches\Helm`
- **Linux/Mac:** `~/.cache/helm`

### Cấu Trúc Chart

Điều hướng đến thư mục cache:
```
<HELM_CACHE_HOME>/repository/wordpress
```

Giải nén file chart đã nén để xem cấu trúc. Chart chứa:
- Các file manifest Kubernetes (YAML)
- Templates
- File values
- Metadata của chart
- Dependencies

Các file này định nghĩa tất cả các Kubernetes resources đã được triển khai.

## Lợi Ích Của Việc Sử Dụng Helm

1. **Triển Khai Đơn Giản:** Triển khai ứng dụng phức tạp chỉ với một lệnh
2. **Sẵn Sàng Production:** Sử dụng các chart được cộng đồng duy trì với best practices
3. **Cấu Hình Nhất Quán:** Quản lý nhiều deployment dễ dàng
4. **Kiểm Soát Phiên Bản:** Theo dõi và quản lý các phiên bản ứng dụng
5. **Cập Nhật Dễ Dàng:** Nâng cấp ứng dụng với các lệnh đơn giản
6. **Khả Năng Rollback:** Quay lại phiên bản trước nếu cần

## Xác Minh Triển Khai

### Sử Dụng Docker Dashboard

Kiểm tra các phần sau:
- **Deployments:** Xem các deployment WordPress và MariaDB
- **Pods:** Xác minh các pod đang chạy
- **Services:** Kiểm tra các LoadBalancer và ClusterIP services
- **ConfigMaps:** Xem lại dữ liệu cấu hình
- **Secrets:** Xem thông tin đăng nhập được lưu trữ (đã mã hóa)

### Sử Dụng Các Lệnh kubectl

```bash
# Liệt kê deployments
kubectl get deployments

# Liệt kê pods
kubectl get pods

# Liệt kê services
kubectl get services

# Liệt kê configmaps
kubectl get configmaps

# Liệt kê secrets
kubectl get secrets
```

## Kết Luận

Helm charts đơn giản hóa đáng kể việc triển khai các ứng dụng phức tạp trên Kubernetes. Chỉ với một lệnh `helm install`, bạn đã triển khai một website WordPress đầy đủ chức năng với database backend, networking phù hợp, quản lý cấu hình và bảo mật - tất cả tuân theo các tiêu chuẩn sẵn sàng cho production.

Điều này chứng minh sức mạnh và hiệu quả của việc sử dụng Helm cho các triển khai Kubernetes, đặc biệt khi làm việc với kiến trúc microservices trong các ứng dụng Spring Boot hoặc bất kỳ ứng dụng container hóa nào khác.

## Các Bước Tiếp Theo

- Khám phá cấu trúc helm chart chi tiết
- Học cách tùy chỉnh Helm values
- Hiểu về Helm chart templating
- Thực hành tạo Helm charts của riêng bạn