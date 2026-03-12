# Xác Thực Các Thành Phần Grafana Trong Kubernetes Cluster Trên Google Cloud

## Tổng Quan

Hướng dẫn này trình bày cách xác thực các thành phần Grafana được triển khai trong Kubernetes cluster trên Google Cloud và cách truy cập các dịch vụ Grafana được expose dưới dạng ClusterIP.

## Cấu Hình Dịch Vụ Grafana

Theo mặc định, Grafana được triển khai dưới dạng dịch vụ **ClusterIP** trong Kubernetes cluster. Điều này có nghĩa là:
- Không có địa chỉ IP công khai được gán
- Không thể truy cập trực tiếp từ bên ngoài
- Cần kết nối thông qua Kubernetes cluster để truy cập

## Các Tùy Chọn Truy Cập Dịch Vụ ClusterIP

Quản trị viên Kubernetes có hai tùy chọn chính để cung cấp quyền truy cập vào dịch vụ ClusterIP:

### Tùy Chọn 1: Cập Nhật Thành LoadBalancer
- Sửa đổi Helm chart để thay đổi loại dịch vụ thành `LoadBalancer`
- Chạy lệnh `helm upgrade`
- Lập trình viên sau đó có thể truy cập Grafana thông qua IP công khai được cấp

### Tùy Chọn 2: Port Forwarding (Khuyến Nghị Cho Môi Trường Development)
- Kết nối với Kubernetes cluster từ hệ thống local của bạn
- Sử dụng thông tin xác thực Kubernetes của bạn (admin hoặc developer)
- Sử dụng lệnh `kubectl port-forward` để expose dịch vụ cục bộ

## Yêu Cầu Trước Khi Bắt Đầu

Trước khi truy cập Grafana, đảm bảo bạn có:
1. **Google Cloud CLI (gcloud)** đã được cài đặt và cấu hình
2. **kubectl** đã được cấu hình để kết nối với Kubernetes cluster của bạn
3. Thông tin xác thực Kubernetes phù hợp (quyền truy cập admin hoặc developer)

## Quy Trình Xác Thực Từng Bước

### Bước 1: Lấy Thông Tin Đăng Nhập Admin Của Grafana

Khi Grafana được cài đặt qua Helm, các hướng dẫn cài đặt sẽ được cung cấp trong terminal output. Để lấy mật khẩu admin:

```bash
# Lấy tên người dùng admin (thường là 'admin')
kubectl get secret --namespace default grafana -o jsonpath="{.data.admin-user}" | base64 --decode

# Lấy mật khẩu admin
kubectl get secret --namespace default grafana -o jsonpath="{.data.admin-password}" | base64 --decode
```

**Lưu ý:** Tên người dùng mặc định thường là `admin`.

### Bước 2: Thiết Lập Port Forwarding

Chạy lệnh kubectl port-forward để expose Grafana trên máy local của bạn:

```bash
kubectl port-forward --namespace default svc/grafana 8080:80
```

Lệnh này sẽ:
- Chuyển tiếp cổng local `8080` đến cổng dịch vụ Grafana `80`
- Tiếp tục chạy trong terminal (tiến trình nền)
- Làm cho Grafana có thể truy cập tại `localhost:8080`

### Bước 3: Truy Cập Giao Diện Web Grafana

1. Mở trình duyệt web của bạn
2. Truy cập `http://localhost:8080`
3. Nhập thông tin đăng nhập:
   - **Username:** `admin`
   - **Password:** (lấy từ Bước 1)
4. Nhấp vào nút **Login**

## Xác Thực Các Tích Hợp Grafana

Sau khi đăng nhập, xác minh rằng Grafana đã được tích hợp đúng cách với các thành phần giám sát:

### 1. Tích Hợp Loki (Log Aggregation - Tổng Hợp Log)

**Mục đích:** Xác thực khả năng thu thập và xem log

1. Điều hướng đến trang **Explore** trong Grafana
2. Mở menu dropdown nguồn dữ liệu
3. Chọn **Loki** làm nguồn dữ liệu
4. Cấu hình truy vấn:
   - **Label:** `container`
   - **Value:** `gateway-server` (hoặc tên microservice của bạn)
5. Nhấp vào **Run Query**
6. Xem lại các log được hiển thị cho container đã chọn

**Tính Năng Nâng Cao - Distributed Tracing:**
- Nhấp vào bất kỳ bản ghi log nào
- Tìm trường **Trace ID**
- Nhấp vào nút để điều hướng đến **Tempo**
- Xem chi tiết distributed tracing để phân tích hiệu suất

### 2. Tích Hợp Tempo (Distributed Tracing - Truy Vết Phân Tán)

**Mục đích:** Xác thực distributed tracing qua các microservice

1. Từ một bản ghi log Loki, nhấp vào liên kết Tempo
2. Đợi vài giây để dữ liệu trace được tải
3. Xác minh rằng chi tiết distributed tracing được hiển thị
4. Sử dụng thông tin này để:
   - Phân tích luồng request qua các service
   - Xác định các điểm nghẽn hiệu suất
   - Debug các vấn đề về độ trễ

### 3. Tích Hợp Prometheus (Metrics Collection - Thu Thập Số Liệu)

**Mục đích:** Xác thực thu thập và trực quan hóa số liệu

1. Điều hướng đến trang **Explore**
2. Chọn **Prometheus** làm nguồn dữ liệu
3. Cấu hình truy vấn metric:
   - **Metric:** `up` (số liệu về tính khả dụng hệ thống)
   - **Label filters:** `container` = (tên container của bạn)
   - **Time range:** Last 15 minutes (15 phút gần nhất)
4. Nhấp vào **Run Query**
5. Chuyển sang chế độ xem **Graph** để trực quan hóa
6. Bật **Stacked lines** để có hình ảnh đẹp hơn

**Kết Quả Mong Đợi:**
- Biểu đồ hiển thị dữ liệu metric theo thời gian
- Xác nhận Prometheus đang scrape metrics thành công

## Danh Sách Kiểm Tra Xác Thực

Đảm bảo tất cả các thành phần đang hoạt động chính xác:

- [x] Đăng nhập Grafana thành công
- [x] Tích hợp Loki hoạt động (log hiển thị)
- [x] Tích hợp Tempo hoạt động (trace có thể truy cập từ log)
- [x] Tích hợp Prometheus hoạt động (metric hiển thị)

## Lưu Ý Quan Trọng

### Cân Nhắc Về Bảo Mật
- Dịch vụ ClusterIP không được expose ra internet
- Chỉ người dùng có quyền truy cập Kubernetes cluster mới có thể sử dụng port-forward
- Điều này cung cấp một lớp bảo mật bổ sung cho các dịch vụ production

### Giới Hạn Của Port Forwarding
- Kết nối chỉ hoạt động khi lệnh đang chạy
- Nếu terminal bị đóng, port forwarding sẽ dừng
- Phù hợp cho development/debugging, không phải cho truy cập production

### Truy Cập Production
Đối với môi trường production, hãy xem xét:
- Sử dụng LoadBalancer hoặc Ingress cho truy cập vĩnh viễn
- Triển khai xác thực và ủy quyền phù hợp
- Thiết lập VPN hoặc bastion host cho truy cập an toàn

## Xử Lý Sự Cố

### Không Thể Kết Nối Với Grafana
- Xác minh kubectl đã kết nối với cluster đúng
- Đảm bảo cổng 8080 chưa được sử dụng
- Kiểm tra pod Grafana đang chạy: `kubectl get pods | grep grafana`

### Nguồn Dữ Liệu Không Hiển Thị
- Xác minh Prometheus, Loki và Tempo đã được triển khai và đang chạy
- Kiểm tra cấu hình nguồn dữ liệu Grafana
- Xem lại các network policy có thể chặn giao tiếp

### Không Có Log Hoặc Metric Hiển Thị
- Xác nhận microservice đang chạy và tạo dữ liệu
- Xác minh các collector agent (Promtail, OpenTelemetry) đã được triển khai
- Kiểm tra các service label và selector khớp với filter truy vấn

## Kết Luận

Việc xác thực thành công Grafana và các tích hợp của nó (Loki, Tempo, Prometheus) trong Kubernetes cluster trên Google Cloud đảm bảo rằng observability stack của bạn đang hoạt động chính xác. Thiết lập này cho phép khả năng giám sát, logging và tracing toàn diện cho các ứng dụng microservice được xây dựng bằng Java Spring Boot.

## Các Bước Tiếp Theo

- Cấu hình dashboard tùy chỉnh cho microservice của bạn
- Thiết lập các quy tắc cảnh báo trong Prometheus
- Khám phá truy vấn nâng cao với PromQL và LogQL
- Triển khai distributed tracing trong ứng dụng Spring Boot của bạn