# Triển khai Keycloak với Bitnami Helm Charts

## Giới thiệu

Một trong những ưu điểm lớn của Helm là có một cộng đồng hỗ trợ rất tốt. Điều này giúp bạn dễ dàng tìm thấy các Helm chart để cài đặt bất kỳ sản phẩm nào trong ngành công nghiệp phần mềm. Ví dụ, nếu bạn muốn cài đặt Kafka trong Kubernetes cluster của mình, bạn không cần phải chuẩn bị các tệp manifest Kubernetes thủ công. Thay vào đó, bạn có thể dựa vào các Helm chart có sẵn trên web.

## Bitnami Helm Charts

Bitnami là một công ty/cộng đồng duy trì các Helm chart với tiêu chuẩn sản xuất tuyệt vời. Bitnami giúp bạn dễ dàng chạy các phần mềm nguồn mở yêu thích trên bất kỳ nền tảng nào, bao gồm laptop, Kubernetes hoặc tất cả các đám mây lớn. Bitnami được hỗ trợ bởi VMware.

### Truy cập Bitnami Helm Charts

1. Tìm kiếm "bitnami helm charts github" trên Google
2. Điều hướng đến kho lưu trữ GitHub của Bitnami Helm charts
3. Mở thư mục Bitnami để xác định các Helm chart cho nhiều sản phẩm khác nhau

**Các sản phẩm có sẵn bao gồm:**
- Argo CD
- Cassandra
- Console
- Drupal
- Elasticsearch
- Grafana (bao gồm Grafana Loki, Grafana Tempo)
- Kafka
- Keycloak
- Kibana
- Kube Prometheus
- MongoDB
- Logstash
- MariaDB
- MySQL
- Nginx
- PostgreSQL
- RabbitMQ
- Redis

## Cài đặt Keycloak với Helm

### Bước 1: Tải xuống Bitnami Helm Charts

1. Điều hướng đến thư mục charts trong kho lưu trữ GitHub của Bitnami
2. Nhấp vào "Download Zip" để tải xuống tất cả Helm charts
3. Giải nén tệp zip đã tải xuống vào hệ thống cục bộ của bạn
4. Tìm thư mục Keycloak Helm chart
5. Sao chép thư mục Keycloak vào vị trí Helm charts của bạn

### Bước 2: Cấu hình Keycloak Helm Chart

Keycloak Helm chart chứa:
- `chart.yaml`
- Thư mục `templates`
- `values.yaml`

**Chỉnh sửa values.yaml:**

1. **Thay đổi loại Service:**
   - Tìm kiếm `cluster IP` trong tệp values.yaml
   - Thay thế `ClusterIP` bằng `LoadBalancer` để expose Keycloak ra bên ngoài

2. **Đặt mật khẩu Admin:**
   - Tìm kiếm biến `admin password`
   - Mặc định, admin user là `user` và password để trống (tạo mật khẩu ngẫu nhiên)
   - Đặt mật khẩu tùy chỉnh (ví dụ: `password`) để dễ dàng truy cập hơn

### Bước 3: Build Dependencies

Trước khi cài đặt, hãy build các dependencies của Helm chart:

```bash
cd keycloak
helm dependency build
```

Lệnh này biên dịch tất cả các dependencies và đóng gói chúng trong Keycloak Helm chart. Keycloak có dependency vào cơ sở dữ liệu PostgreSQL, sẽ được bao gồm.

### Bước 4: Cài đặt Keycloak

Điều hướng đến thư mục cha chứa Keycloak chart và chạy:

```bash
helm install keycloak keycloak
```

Trong đó:
- `keycloak` đầu tiên là tên release
- `keycloak` thứ hai là tên chart/thư mục

**Lưu ý:** Quá trình cài đặt sẽ xuất ra các hướng dẫn để truy cập Keycloak.

### Bước 5: Truy cập Keycloak

Đợi 1-2 phút để LoadBalancer được tạo. Sau đó truy cập Keycloak tại:
- URL: `http://localhost:80`
- Username: `user`
- Password: `password` (như đã cấu hình trong values.yaml)

## Cấu hình Keycloak cho Microservices

### Tạo Client

1. Điều hướng đến Administration Console
2. Nhấp vào "Clients"
3. Tạo một client mới với ID: `easybank-callcenter-cc`
4. Bật **Client Authentication**
5. Tắt **Standard Flow** và **Direct Access Grants**
6. Bật **Service Account Roles**
7. Lưu cấu hình
8. Vào tab "Credentials" và sao chép giá trị secret

### Tạo Roles

Tạo các role sau:
- `accounts`
- `cards`
- `loans`

### Gán Roles cho Client

1. Vào client (`easybank-callcenter-cc`)
2. Điều hướng đến "Service Account Roles"
3. Nhấp "Assign Role"
4. Gán tất cả các role cần thiết cho ứng dụng client

### Kiểm tra với Postman

Cập nhật URL access token trong Postman từ cổng `7080` sang cổng `80` để phù hợp với cấu hình Helm chart. Sau khi gán roles, bạn sẽ có thể lấy access token thành công.

## Hiểu về Keycloak DNS trong Kubernetes

Khi Helm cài đặt Keycloak, nó cung cấp một tên DNS để truy cập Keycloak từ bên trong cluster:

```
keycloak.<namespace>.svc.cluster.local
```

Tên DNS này nên được sử dụng trong cấu hình microservices của bạn (ví dụ: trong values.yaml của Helm chart cụ thể môi trường) để các dịch vụ như Gateway Server có thể kết nối với Keycloak từ trong cùng một Kubernetes cluster.

## Lợi ích của việc sử dụng Helm Charts

Sử dụng Helm charts cho việc cài đặt Keycloak mang lại:
- **Triển khai đơn giản:** Không cần tạo nhiều tệp manifest Kubernetes thủ công
- **Tiêu chuẩn Production:** Bitnami duy trì các chart theo các best practices
- **Quản lý Dependencies:** Tự động xử lý các dependencies như PostgreSQL
- **Tính nhất quán:** Quy trình triển khai giống nhau trên các môi trường

Thư mục templates trong Keycloak Helm chart chứa nhiều template đối tượng Kubernetes. Việc tạo tất cả các template này thủ công sẽ là một quá trình cực kỳ phức tạp.

## Cân nhắc về tài nguyên hệ thống

### Thiết lập phát triển cục bộ

Khi thực hiện nhiều cài đặt trong Kubernetes cluster của bạn, bạn có thể gặp phải các ràng buộc về bộ nhớ trên hệ thống cục bộ.

**Cài đặt Docker Desktop được khuyến nghị:**

1. Mở Docker Desktop Dashboard
2. Nhấp vào "Settings"
3. Điều hướng đến "Resources"
4. Tăng tài nguyên được phân bổ:
   - CPUs: 6 (từ mặc định 4)
   - Memory: 12GB (từ mặc định 8GB)

Các tài nguyên tăng lên này sẽ đảm bảo:
- Cài đặt nhanh hơn
- Thời gian phản hồi microservices tốt hơn
- Hiệu suất tổng thể mượt mà hơn

### Môi trường Production

Trong môi trường cloud production, các ràng buộc về bộ nhớ và CPU thường không phải là vấn đề vì bạn sẽ có quyền truy cập vào tài nguyên đáng kể.

### Giải pháp thay thế: Triển khai Cloud

Nếu laptop của bạn không thể đáp ứng yêu cầu tài nguyên, bạn có thể làm theo các quy trình triển khai tương tự trong môi trường cloud nơi tài nguyên có sẵn nhiều hơn.

## Các bước tiếp theo

Sau khi cài đặt thành công Keycloak, bạn sẽ cần thiết lập các thành phần khác:
- **Kafka** cho event streaming
- **Grafana** cho visualization
- **Prometheus** cho monitoring

Tất cả những thứ này có thể được cài đặt bằng cách sử dụng các Bitnami Helm chart tương ứng theo quy trình tương tự.

## Kết luận

Helm charts, đặc biệt là những chart từ Bitnami, đơn giản hóa đáng kể việc triển khai các ứng dụng phức tạp như Keycloak trong môi trường Kubernetes. Bằng cách tận dụng các chart này, bạn có thể tập trung vào việc cấu hình microservices của mình thay vì quản lý sự phức tạp của cơ sở hạ tầng.