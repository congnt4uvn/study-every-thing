# Demo Giám Sát Prometheus và Tích Hợp với Grafana

## Tổng Quan

Hướng dẫn này trình bày cách triển khai và sử dụng Prometheus để giám sát các microservices trong ứng dụng Spring Boot, bao gồm tích hợp với Grafana để nâng cao khả năng trực quan hóa.

## Yêu Cầu Tiên Quyết

- Đã cài đặt Docker và Docker Compose
- Các microservices đã cấu hình dependencies Micrometer
- Đã cập nhật `application.yml` và `pom.xml` với cấu hình Micrometer

## Tái Tạo Docker Images

Trước khi khởi động containers, đảm bảo tất cả Docker images được tái tạo với các thay đổi mã nguồn mới nhất liên quan đến Micrometer:

1. **Cập Nhật Dependencies**: Đảm bảo `pom.xml` bao gồm các dependencies Micrometer
2. **Cấu Hình Metrics**: Cập nhật `application.yml` với cấu hình endpoints Prometheus
3. **Tái Tạo Images**: Tạo Docker images mới với tag (ví dụ: S11) sau khi thực hiện thay đổi

```bash
# Build images cho tất cả microservices
docker build -t <tên-service>:S11 .
```

## Khởi Động Services với Docker Compose

Di chuyển đến thư mục Docker Compose và khởi động tất cả services:

```bash
# Di chuyển đến thư mục docker-compose
cd docker-compose/prod

# Khởi động tất cả services ở chế độ detached
docker compose up -d
```

Đợi 1-2 phút để tất cả containers khởi động hoàn toàn.

## Kiểm Tra Trạng Thái Container

### Sử Dụng Docker Desktop

1. Mở Docker Desktop
2. Kiểm tra tất cả containers đang ở trạng thái "Running"
3. Xác minh container Prometheus đang chạy trên port 9090
4. Xác nhận Gateway Server đã khởi động thành công

### Kiểm Tra Actuator Endpoints

Kiểm tra endpoint actuator Prometheus cho bất kỳ microservice nào:

```
GET http://localhost:<port>/actuator/prometheus
```

Ví dụ cho accounts microservice:
```
GET http://localhost:8080/actuator/prometheus
```

Bạn sẽ nhận được dữ liệu metrics ở định dạng Prometheus.

## Truy Cập Dashboard Prometheus

### Xem Targets

1. Mở trình duyệt và truy cập: `http://localhost:9090/targets`
2. Xem tất cả microservices được giám sát và trạng thái sức khỏe của chúng
3. Click "unhealthy" để xem các instances lỗi
4. Click "all" để xem tất cả containers được giám sát

**Các Services Dự Kiến:**
- accounts
- cards
- configserver
- eurekaserver
- gatewayserver
- loans

### Xem Chi Tiết Target

Click "show more" trên bất kỳ target nào để xem:
- Trạng thái (up/down)
- Thông tin label
- Chi tiết cấu hình job
- Thời gian scrape cuối cùng
- Thời gian scrape

## Làm Việc với Metrics và Graphs

### Tìm Kiếm Metrics

1. Di chuyển đến tab "Graph"
2. Tìm kiếm metrics cụ thể trong ô query
3. Click "Execute" để hiển thị dữ liệu

### Các Metrics Phổ Biến

**Sử Dụng CPU:**
```
system_cpu_usage
```

**Thời Gian Hoạt Động Process:**
```
process_uptime_seconds
```

**Thông Tin Thread:**
```
jvm_threads_live
jvm_threads_daemon
```

**Metrics Kết Nối Database:**
```
hikaricp_connections_active
hikaricp_connections_idle
```

### Trực Quan Hóa Dữ Liệu

**Chế Độ Xem Bảng:**
- Click "Execute" để xem giá trị metrics ở định dạng bảng
- Hiển thị dữ liệu cho tất cả instances microservice

**Chế Độ Xem Đồ Thị:**
- Click tab "Graph" để xem trực quan hóa chuỗi thời gian
- Di chuột qua các đường để làm nổi bật dữ liệu microservice cụ thể
- Điều chỉnh khoảng thời gian (ví dụ: 15 phút, 1 giờ)
- Phóng to/thu nhỏ để xem rõ hơn

**Kiểu Đồ Thị:**
- Chuyển đổi giữa các kiểu trực quan hóa khác nhau
- Lọc để hiển thị metrics microservice cụ thể
- Xem dữ liệu service riêng lẻ hoặc kết hợp

### Metrics Explorer

Để khám phá các metrics có sẵn:

1. Click biểu tượng quả địa cầu trong query builder
2. Duyệt danh sách đầy đủ các metrics được theo dõi
3. Chọn bất kỳ metric nào để thêm vào query của bạn
4. Metrics được thu thập tự động thông qua tích hợp Micrometer

## Tùy Chỉnh Dashboard

### Tùy Chọn Theme

- Click biểu tượng chuyển đổi theme để chuyển giữa chế độ tối và sáng
- Chế độ sáng cung cấp khả năng phân biệt màu tốt hơn cho nhiều đồ thị

### Lựa Chọn Khoảng Thời Gian

- Sử dụng bộ chọn khoảng thời gian để tập trung vào các giai đoạn cụ thể
- Khoảng thời gian ngắn hơn cung cấp độ phân giải đồ thị chi tiết hơn
- Các khoảng phổ biến: 5m, 15m, 1h, 6h, 24h

## Giám Sát Sức Khỏe Container

### Giám Sát Trạng Thái Sức Khỏe

Prometheus liên tục giám sát sức khỏe microservice bằng cách:
- Định kỳ scrape các endpoints `/actuator/prometheus`
- Đánh dấu services là "up" khi phản hồi thành công
- Đánh dấu services là "down" khi không thể truy cập

### Kiểm Tra Phát Hiện Sức Khỏe

**Mô Phỏng Lỗi Service:**

1. Dừng một container microservice (ví dụ: cards service)
2. Đợi 10-15 giây để Prometheus phát hiện lỗi
3. Refresh trang targets
4. Service đã dừng xuất hiện màu đỏ trong "unhealthy"
5. Click "show more" để xem chi tiết lỗi (ví dụ: "no such host")

**Khôi Phục Service:**

1. Khởi động lại container đã dừng
2. Đợi 10-15 giây để Prometheus phát hiện khôi phục
3. Refresh trang targets
4. Service quay trở lại trạng thái "healthy" với state "up"

## Hạn Chế của Prometheus

Mặc dù Prometheus cung cấp khả năng giám sát thiết yếu, nó có hạn chế cho môi trường doanh nghiệp:

- **Trực Quan Hóa Hạn Chế**: Chức năng đồ thị cơ bản có thể không đủ cho nhu cầu giám sát phức tạp
- **Xem Metric Đơn Lẻ**: UI mặc định tập trung vào metrics riêng lẻ thay vì dashboards toàn diện
- **Không Có UI Quản Lý Alert**: Thiếu dashboard cảnh báo tích hợp
- **Phân Tích Lịch Sử Hạn Chế**: Trực quan hóa chuỗi thời gian cơ bản

## Tích Hợp với Grafana

Đối với môi trường production và các dự án phức tạp, tích hợp Prometheus với Grafana để có được:

- **Dashboards Nâng Cao**: Tạo dashboards toàn diện, đa metrics
- **Trực Quan Hóa Tốt Hơn**: Các loại biểu đồ phong phú và tùy chọn tùy chỉnh
- **Quản Lý Alert**: Cấu hình và quản lý cảnh báo trực quan
- **Template Variables**: Lọc dashboard động
- **Tương Quan Dữ Liệu**: Kết hợp metrics từ nhiều nguồn

### Cấu Hình Grafana

Tích hợp Grafana được cấu hình thông qua cài đặt data source:

1. Thêm Prometheus làm data source trong Grafana
2. Cấu hình URL Prometheus (thường là `http://prometheus:9090`)
3. Kiểm tra kết nối
4. Tạo dashboards sử dụng metrics Prometheus

## Thực Hành Tốt Nhất

1. **Giám Sát Thường Xuyên**: Kiểm tra trang targets Prometheus thường xuyên để xem sức khỏe service
2. **Lựa Chọn Metric**: Chọn metrics liên quan dựa trên yêu cầu giám sát của bạn
3. **Tối Ưu Khoảng Thời Gian**: Điều chỉnh khoảng thời gian để đồ thị rõ ràng tối ưu
4. **Cấu Hình Alert**: Thiết lập quy tắc cảnh báo cho các metrics quan trọng
5. **Lập Kế Hoạch Tài Nguyên**: Giám sát CPU, bộ nhớ và metrics connection pool để lập kế hoạch năng lực
6. **Tổ Chức Dashboard**: Sử dụng Grafana để tổ chức metrics thành các dashboards logic

## Khắc Phục Sự Cố

### Service Hiển Thị Down

1. Kiểm tra xem container có đang chạy trong Docker Desktop không
2. Xác minh service có thể truy cập trên port được chỉ định
3. Kiểm tra logs service để tìm lỗi khởi động
4. Đảm bảo endpoint `/actuator/prometheus` được kích hoạt

### Không Hiển Thị Metrics

1. Xác minh dependencies Micrometer trong `pom.xml`
2. Kiểm tra `application.yml` cho cấu hình Prometheus
3. Đảm bảo Docker images đã được tái tạo sau khi thay đổi cấu hình
4. Xác minh cấu hình scrape Prometheus

### Vấn Đề Kết Nối

1. Kiểm tra cấu hình mạng Docker
2. Xác minh service discovery đang hoạt động chính xác
3. Đảm bảo quy tắc firewall cho phép giao tiếp giữa các containers
4. Kiểm tra file cấu hình Prometheus cho định nghĩa target chính xác

## Kết Luận

Prometheus cung cấp nền tảng vững chắc cho giám sát microservices với thu thập metrics thời gian thực và trực quan hóa cơ bản. Đối với các ứng dụng doanh nghiệp yêu cầu khả năng giám sát nâng cao, tích hợp Prometheus với Grafana mang lại dashboards giám sát toàn diện và thông tin chi tiết vận hành nâng cao.

## Các Bước Tiếp Theo

- Khám phá tạo dashboard Grafana
- Cấu hình quy tắc cảnh báo trong Prometheus
- Thiết lập lưu trữ metrics dài hạn
- Triển khai metrics tùy chỉnh trong microservices của bạn
- Tạo service-level objectives (SLOs) dựa trên metrics đã thu thập