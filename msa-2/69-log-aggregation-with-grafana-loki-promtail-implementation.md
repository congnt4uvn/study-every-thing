# Triển khai Thu thập Log Tập trung với Grafana, Loki và Promtail

## Tổng quan

Hướng dẫn này trình bày cách triển khai thu thập log tập trung trong kiến trúc microservices sử dụng Grafana, Loki và Promtail, mà không cần thay đổi bất kỳ dòng code nào trong các microservices hiện có.

## Yêu cầu tiên quyết

- Docker và Docker Compose đã được cài đặt
- Nhiều microservices (Accounts, Cards, Loans, Gateway Server, Eureka Server)
- Các Docker images đã được build với tag `s11`

## Các thành phần kiến trúc

### 1. **Grafana**
- Nền tảng trực quan hóa và phân tích dựa trên web
- Chạy trên cổng 3000
- Cung cấp giao diện người dùng để tìm kiếm và xem logs

### 2. **Loki**
- Hệ thống thu thập log của Grafana Labs
- Lưu trữ và đánh index logs hiệu quả
- Tách thành các thành phần đọc và ghi để tăng khả năng mở rộng

### 3. **Promtail**
- Agent thu thập logs
- Scrape logs từ các Docker containers
- Đẩy logs lên Loki

### 4. **Minio**
- Object storage để lưu trữ logs lâu dài
- Giải pháp thay thế cục bộ cho cloud storage (AWS S3)

## Các bước triển khai

### Bước 1: Cấu hình Docker Compose

Đảm bảo file `docker-compose.yml` của bạn bao gồm tất cả các services cần thiết với căn lề đúng:

```yaml
services:
  # Microservices
  accounts:
    # ... cấu hình
  
  cards:
    # ... cấu hình
  
  loans:
    # ... cấu hình
  
  gateway:
    # ... cấu hình
  
  # Log aggregation stack
  grafana:
    # ... cấu hình
  
  loki-read:
    # ... cấu hình
  
  loki-write:
    # ... cấu hình
  
  promtail:
    # ... cấu hình
  
  minio:
    # ... cấu hình
```

**Quan trọng**: Đảm bảo căn lề YAML đúng. Tất cả services phải có cùng mức độ căn lề.

### Bước 2: Cấu hình Data Source cho Grafana

Cấu hình Grafana để kết nối với Loki tự động qua Docker Compose entry point:

```yaml
grafana:
  entrypoint:
    - sh
    - -euc
    - |
      mkdir -p /etc/grafana/provisioning/datasources
      cat <<EOF > /etc/grafana/provisioning/datasources/ds.yaml
      apiVersion: 1
      datasources:
        - name: Loki
          type: loki
          access: proxy
          url: http://loki-read:3100
          jsonData:
            httpHeaderName1: "X-Scope-OrgID"
          secureJsonData:
            httpHeaderValue1: "tenant1"
      EOF
      /run.sh
```

### Bước 3: Cấu hình Promtail

Cấu hình Promtail để scrape logs từ Docker containers:

```yaml
scrape_configs:
  - job_name: containers
    static_configs:
      - targets:
          - localhost
        labels:
          job: containerlogs
          __path__: /var/lib/docker/containers/*/*log
    relabel_configs:
      - source_labels: ['__path__']
        target_label: 'container'
```

Label `container` sẽ chứa tên Docker container để dễ dàng lọc.

### Bước 4: Cấu hình Storage

Mount local storage cho Minio:

```yaml
minio:
  volumes:
    - ./data/minio:/data
```

Điều này tạo thư mục `.data` trong thư mục làm việc của bạn để lưu trữ logs cục bộ.

## Triển khai

### 1. Di chuyển đến Production Profile

```bash
cd section_11/docker-compose/prod
```

### 2. Khởi động tất cả Services

```bash
docker-compose up -d
```

### 3. Kiểm tra trạng thái Container

Đợi 1-2 phút để tất cả containers khởi động. Kiểm tra logs của gateway server để xác nhận:

```bash
docker logs gatewayserver-ms
```

Tìm dòng: "Started Gateway server successfully"

## Xử lý sự cố

### Vấn đề căn lề YAML

Nếu gặp lỗi khi chạy `docker-compose up`, kiểm tra căn lề YAML:
- Chọn các services bị lệch
- Nhấn `Shift + Tab` để di chuyển chúng về lại một mức căn lề
- Đảm bảo tất cả services ở cùng mức độ

### Vấn đề tài nguyên thấp

Nếu containers không khởi động được do thiếu memory/CPU:

```yaml
healthcheck:
  interval: 20s  # Tăng từ 10s
  retries: 20    # Tăng từ 10
```

## Kiểm tra thiết lập

### 1. Tạo Logs

Sử dụng Postman hoặc bất kỳ API client nào để gọi các endpoints của microservices:

```http
POST http://localhost:8080/api/create
GET http://localhost:8080/api/fetchCustomerDetails?mobileNumber=1234567890
```

### 2. Truy cập Grafana

Mở trình duyệt và truy cập:
```
http://localhost:3000
```

### 3. Xem Logs trong Grafana

1. Click vào **Toggle Menu** → **Connections** → **Data Sources**
2. Xác nhận data source Loki đã được cấu hình
3. Điều hướng đến phần **Explore**
4. Chọn label: `container`
5. Chọn tên container (ví dụ: `accounts-ms`, `cards-ms`, `gateway-ms`)
6. Click **Run Query**

### 4. Live Streaming

Bật live streaming để xem logs theo thời gian thực khi chúng được tạo (làm mới mỗi 5 giây).

## Lọc Log nâng cao

### Lọc theo nội dung văn bản

Tìm kiếm các mẫu văn bản cụ thể trong logs:

1. Chọn container (ví dụ: `gateway-ms`)
2. Chọn loại filter: **Line contains**
3. Nhập từ khóa tìm kiếm (ví dụ: `easybank-correlation-id`)
4. Click **Run Query**

### Các tùy chọn Filter có sẵn

- **Line contains**: Tìm kiếm văn bản không phân biệt chữ hoa chữ thường
- **Line does not contain**: Loại trừ các dòng có văn bản cụ thể
- **Line contains case sensitive**: Khớp chính xác chữ hoa chữ thường
- **Regex match**: Tìm kiếm dựa trên pattern
- **Line filter expression**: Biểu thức LogQL nâng cao

## Vị trí lưu trữ Log

### Development cục bộ

Logs được lưu trữ tại:
```
section_11/docker-compose/prod/.data/
├── loki-data/
└── loki-ruler/
```

### Triển khai Production

Đối với production, thay thế Minio bằng cloud storage:
- **AWS S3**
- **Google Cloud Storage**
- **Azure Blob Storage**

Điều này cho phép lưu trữ logs không giới hạn cho bất kỳ số lượng microservices nào.

## Lợi ích chính

### 1. **Không thay đổi Code**
Không cần sửa đổi code trong microservices - hoàn toàn là giải pháp dựa trên infrastructure.

### 2. **Truy cập tập trung**
Tất cả logs của microservices có thể truy cập từ một giao diện duy nhất.

### 3. **Kiến trúc có khả năng mở rộng**
Hỗ trợ 100+ microservices trong môi trường production.

### 4. **Tìm kiếm mạnh mẽ**
Tìm kiếm trên tất cả logs sử dụng text filters, regex và LogQL queries.

### 5. **Giám sát thời gian thực**
Live streaming hiển thị logs khi chúng được tạo ra.

## Development cục bộ vs Production

### Development cục bộ
- Sử dụng console output của IDE
- Đặt breakpoints để debug
- Truy cập trực tiếp vào application logs
- Không cần thiết lập log aggregation phức tạp

### Môi trường Dev/Production
- Triển khai Grafana + Loki + Promtail
- Quản lý log tập trung
- Cộng tác giữa các nhóm phát triển
- Bắt buộc đối với microservices phân tán

## Cấu hình Health Check

Cấu hình health checks phù hợp cho container orchestration:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8080/actuator/health"]
  interval: 10s
  timeout: 5s
  retries: 10
  start_period: 40s
```

## Best Practices (Thực hành tốt nhất)

1. **Phân bổ tài nguyên**: Đảm bảo đủ CPU, memory và RAM cho production
2. **Hợp tác với Platform Team**: Làm việc với platform team để cấu hình cloud storage
3. **Chính sách lưu giữ Log**: Định nghĩa logs nên được lưu trong bao lâu
4. **Kiểm soát truy cập**: Triển khai xác thực phù hợp cho Grafana trong production
5. **Phân đoạn mạng**: Sử dụng Docker networks để cô lập services

## Các trụ cột của Observability (Khả năng quan sát)

Triển khai này giải quyết trụ cột **Logs** của observability:

✅ **Logs** - Thu thập log tập trung (đã đề cập trong hướng dẫn này)  
⏭️ **Metrics** - Các chỉ số hiệu suất ứng dụng (chủ đề tiếp theo)  
⏭️ **Traces** - Distributed tracing qua các services

## Triển khai Correlation ID

Hướng dẫn đề cập đến việc sử dụng correlation IDs (ví dụ: `easybank-correlation-id`) để theo dõi requests qua các microservices. Điều này giúp:

- Theo dõi một request duy nhất qua nhiều services
- Debug các distributed transactions
- Phân tích hiệu suất của các flows end-to-end

## Kết luận

Bây giờ bạn đã có một hệ thống thu thập log hoàn chỉnh:
- Thu thập logs từ tất cả microservices tự động
- Cung cấp tìm kiếm và trực quan hóa tập trung
- Không yêu cầu thay đổi code ứng dụng
- Mở rộng để hỗ trợ kiến trúc microservices lớn

Giải pháp này giúp các developers hiểu trạng thái bên trong của microservices và nhanh chóng xử lý sự cố trong môi trường phân tán.

## Các bước tiếp theo

Trong bài giảng tiếp theo, chúng ta sẽ khám phá **Metrics** - trụ cột thứ hai của observability và monitoring cho microservices.