# Thiết Lập Tích Hợp Prometheus và Grafana cho Microservices

## Tổng Quan

Hướng dẫn này trình bày cách thiết lập Prometheus để giám sát microservices và tích hợp với Grafana để trực quan hóa dữ liệu. Chúng ta sẽ cấu hình Prometheus để thu thập metrics từ các microservices Spring Boot và thiết lập kết nối với Grafana bằng Docker Compose.

## Yêu Cầu Tiên Quyết

- Đã cài đặt Docker và Docker Compose
- Các microservices Spring Boot đang expose metrics qua Actuator và Micrometer
- Có cấu trúc thư mục observability trong dự án
- Các microservices đang chạy (accounts, loans, cards, gateway server, Eureka, config server)

## Bước 1: Tạo Cấu Hình Prometheus

Đầu tiên, tạo một thư mục mới cho Prometheus bên trong thư mục observability:

```
observability/
  └── prometheus/
      └── prometheus.yml
```

### File Cấu Hình Prometheus (prometheus.yml)

```yaml
global:
  scrape_interval: 5s
  evaluation_interval: 5s

scrape_configs:
  - job_name: 'accounts'
    metrics_path: '/actuator/prometheus'
    static_configs:
      - targets: ['accounts:8080']
  
  - job_name: 'loans'
    metrics_path: '/actuator/prometheus'
    static_configs:
      - targets: ['loans:8090']
  
  - job_name: 'cards'
    metrics_path: '/actuator/prometheus'
    static_configs:
      - targets: ['cards:9000']
  
  - job_name: 'gatewayserver'
    metrics_path: '/actuator/prometheus'
    static_configs:
      - targets: ['gatewayserver:8072']
  
  - job_name: 'eurekaserver'
    metrics_path: '/actuator/prometheus'
    static_configs:
      - targets: ['eurekaserver:8070']
  
  - job_name: 'configserver'
    metrics_path: '/actuator/prometheus'
    static_configs:
      - targets: ['configserver:8071']
```

### Giải Thích Cấu Hình

- **scrape_interval**: Prometheus thu thập metrics từ microservices mỗi 5 giây
- **evaluation_interval**: Prometheus đánh giá và cập nhật dashboard mỗi 5 giây
- **scrape_configs**: Định nghĩa các job cho từng microservice
  - **job_name**: Định danh microservice đang được giám sát
  - **metrics_path**: Đường dẫn mà Actuator expose metrics Prometheus (`/actuator/prometheus`)
  - **static_configs/targets**: Tên service và port theo định dạng mạng Docker

## Bước 2: Cấu Hình Prometheus trong Docker Compose

Thêm service Prometheus vào file `docker-compose.yml` trong profile prod:

```yaml
services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./observability/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
    extends:
      file: network-deploy-service.yml
      service: network-deploy-service
```

### Chi Tiết Cấu Hình

- **image**: Image Docker chính thức của Prometheus
- **ports**: Expose giao diện Prometheus UI trên port 9090
- **volumes**: Mount file cấu hình prometheus.yml vào container
- **extends**: Đảm bảo Prometheus chạy trong cùng mạng Docker với các microservices khác

## Bước 3: Tạo Cấu Hình Data Source cho Grafana

Tạo thư mục Grafana bên trong observability và thêm file cấu hình datasource:

```
observability/
  └── grafana/
      └── datasource.yml
```

### Cấu Hình Data Source (datasource.yml)

```yaml
apiVersion: 1

deleteDatasources:
  - name: Prometheus
  - name: Loki

datasources:
  - name: Prometheus
    type: prometheus
    uid: prometheus-uid
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true
    jsonData:
      timeInterval: "5s"
  
  - name: Loki
    type: loki
    uid: loki-uid
    access: proxy
    url: http://loki:3100
    editable: true
```

### Giải Thích Cấu Hình

- **apiVersion**: Phiên bản API chuẩn cho datasources của Grafana
- **deleteDatasources**: Xóa các datasources hiện có cùng tên để tránh xung đột
- **datasources**: Định nghĩa chi tiết kết nối cho Prometheus và Loki
  - **url**: Sử dụng tên service Docker (prometheus:9090, loki:3100) cho giao tiếp mạng nội bộ
  - **access**: Chế độ proxy cho phép Grafana truy cập data sources thay mặt người dùng

## Bước 4: Cập Nhật Service Grafana trong Docker Compose

Thay thế cấu hình entrypoint trước đó của Grafana bằng volume mount:

```yaml
services:
  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    volumes:
      - ./observability/grafana/datasource.yml:/etc/grafana/provisioning/datasources/datasource.yml
    extends:
      file: network-deploy-service.yml
      service: network-deploy-service
```

### Những Thay Đổi Chính

- **Đã xóa**: Các lệnh entrypoint phức tạp tạo ds.yml trực tiếp
- **Đã thêm**: Volume mount cho file datasource.yml
- **Lợi ích**: Cấu hình Docker Compose gọn gàng hơn với định nghĩa data source được tách riêng

## Bước 5: Triển Khai với Docker Compose

1. Dừng tất cả các instances đang chạy
2. Khởi động các services:

```bash
docker-compose -f docker-compose-prod.yml up -d
```

3. Kiểm tra các services đang chạy:

```bash
docker-compose -f docker-compose-prod.yml ps
```

## Truy Cập Các Services

- **Prometheus UI**: http://localhost:9090
- **Grafana Dashboard**: http://localhost:3000

## Các Bước Kiểm Tra

1. Mở Prometheus UI và điều hướng đến Status > Targets để xác minh tất cả microservices đang được scrape
2. Mở Grafana và kiểm tra Configuration > Data Sources để xác nhận kết nối Prometheus và Loki
3. Tạo dashboards trong Grafana sử dụng Prometheus làm data source

## Kiến Trúc Mạng

Tất cả các services chạy trong cùng một mạng Docker, cho phép service discovery theo tên:
- Microservices expose metrics tại `/actuator/prometheus`
- Prometheus scrape metrics sử dụng tên service (ví dụ: `accounts:8080`)
- Grafana kết nối với Prometheus sử dụng `prometheus:9090`

## Thực Hành Tốt Nhất

1. **Scrape Interval**: Điều chỉnh dựa trên nhu cầu giám sát và ràng buộc tài nguyên
2. **Service Discovery**: Sử dụng tên service Docker thay vì localhost cho giao tiếp giữa các container
3. **Quản Lý Data Source**: Sử dụng provisioning files (datasource.yml) thay vì cấu hình thủ công
4. **Lưu Trữ Volume**: Cân nhắc thêm volumes để lưu trữ dữ liệu Prometheus trong môi trường production

## Khắc Phục Sự Cố

- **Targets Down**: Kiểm tra xem microservices có đang chạy và expose metrics không
- **Connection Refused**: Xác minh tất cả services đều trong cùng mạng Docker
- **Không Có Dữ Liệu trong Grafana**: Xác nhận Prometheus đang scrape metrics thành công từ targets

## Các Bước Tiếp Theo

- Cấu hình các dashboards Grafana tùy chỉnh cho microservices của bạn
- Thiết lập các alerting rules trong Prometheus
- Khám phá các Grafana dashboards có sẵn cho ứng dụng Spring Boot

## Kết Luận

Bạn đã thiết lập thành công Prometheus để thu thập metrics và tích hợp với Grafana để trực quan hóa. Stack observability này cho phép giám sát thời gian thực kiến trúc microservices của bạn.