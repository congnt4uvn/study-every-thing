# Triển Khai Loki và Promtail trong Cấu Hình Docker Compose

## Tổng Quan

Hướng dẫn này sẽ giúp bạn cấu hình Grafana Loki và Promtail để tổng hợp log trong kiến trúc microservices Spring Boot sử dụng Docker Compose.

## Yêu Cầu Tiên Quyết

- Đã cài đặt Docker và Docker Compose
- Dự án microservices Spring Boot
- Hiểu biết cơ bản về Docker Compose
- IntelliJ IDEA (hoặc IDE bất kỳ)

## Bước 1: Tải Xuống Các File Cấu Hình

Đầu tiên, tải xuống các file cấu hình cần thiết:
- `loki-config.yml`
- `promtail-local-config.yml`

Các file cấu hình này rất quan trọng cho việc thiết lập dịch vụ Loki và Promtail.

## Bước 2: Tạo Cấu Trúc Thư Mục

Tạo cấu trúc thư mục có tổ chức cho các công cụ observability:

```
observability/
├── loki/
│   └── loki-config.yml
└── promtail/
    └── promtail-local-config.yml
```

### Tạo Các Thư Mục

1. Tạo thư mục mới tên `observability` trong thư mục gốc dự án
2. Trong `observability`, tạo thư mục `loki`
3. Copy file `loki-config.yml` vào thư mục `loki`
4. Tạo thư mục `promtail` trong `observability`
5. Copy file `promtail-local-config.yml` vào thư mục `promtail`

## Bước 3: Cập Nhật File Docker Compose

### Chọn Profile Môi Trường

Chọn file Docker Compose để chỉnh sửa (default, prod, hoặc qa). Trong ví dụ này, chúng ta sẽ sử dụng file `docker-compose.yml` trong thư mục `prod`.

Sau khi test trong prod, cấu hình tương tự có thể được copy sang các profile khác.

### Xóa Các Service Không Cần Thiết

Để tối ưu tài nguyên hệ thống, xóa container Redis (từ phần rate limiter pattern trước đó):

1. Xóa định nghĩa service Redis
2. Xóa các biến môi trường liên quan đến Redis khỏi cấu hình gateway server
3. Xóa các dependency Redis khỏi gateway server

### Cập Nhật Version Tags

Thay thế tất cả các tag `s10` bằng tag `s11` để sử dụng phiên bản mới nhất của các service.

## Bước 4: Thêm Các Service Loki và Promtail

### Cấu Hình Loki Read Component

Thêm service Loki read với các lưu ý sau:

**Cấu Hình Volume:**
```yaml
volumes:
  - ./observability/loki/loki-config.yml:/etc/loki/config.yml
```

**Cấu Hình Network:**
- Thay đổi tên network từ `loki` thành `easybank` (khớp với common-config.yml của bạn)
- Giữ alias là `loki` để tham chiếu nội bộ
- Đặt anchor cho cấu hình với tên `loki-dns`

### Cấu Hình Loki Write Component

Tương tự như read component:
- Cập nhật đường dẫn volume để trỏ đến `./observability/loki/loki-config.yml`
- Sử dụng cùng cấu hình network `loki-dns`
- Đảm bảo nó tham chiếu đến network `easybank`

### Cấu Hình Promtail Service

**Cấu Hình Volume:**
```yaml
volumes:
  - ./observability/promtail/promtail-local-config.yml:/etc/promtail/config.yml
```

**Cấu Hình Network:**
Thay vì hardcode tên network, tham chiếu đến cấu hình chung:

```yaml
extends:
  file: common-config.yml
  service: network-deploy-service
```

### Cấu Hình MinIO Service

Chỉ cập nhật cấu hình network để sử dụng pattern extends:

```yaml
extends:
  file: common-config.yml
  service: network-deploy-service
```

### Cấu Hình Grafana Service

Cập nhật cấu hình network để sử dụng pattern extends, tương tự như các service khác.

### Cập Nhật Gateway Service

Cuộn xuống cuối định nghĩa gateway service và thêm cấu hình network sử dụng pattern extends.

## Bước 5: Tạo Docker Images

Tạo Docker images mới với tag `S11` cho tất cả các microservices để đảm bảo tương thích với cấu hình đã cập nhật.

## Tổng Kết

Trong quá trình triển khai này, chúng ta đã:

1. ✅ Tạo cấu trúc thư mục có tổ chức cho cấu hình Loki và Promtail
2. ✅ Cập nhật file Docker Compose với volume mappings phù hợp
3. ✅ Cấu hình network settings để sử dụng cấu hình chung
4. ✅ Thêm các service Loki (read/write), Promtail, MinIO và Grafana
5. ✅ Tối ưu hóa thiết lập bằng cách xóa các service không cần thiết (Redis)
6. ✅ Cập nhật tất cả các tag service lên phiên bản S11

## Các Bước Tiếp Theo

Sau khi tạo Docker images, bạn có thể:
- Test thiết lập log aggregation
- Truy cập Grafana dashboards
- Xem các log được tổng hợp từ tất cả microservices
- Cấu hình các truy vấn log và cảnh báo tùy chỉnh

## Lợi Ích

Thiết lập Grafana Loki và Promtail cung cấp:
- Tổng hợp log tập trung
- Truy vấn và lọc log dễ dàng
- Phân tích log trực quan thông qua Grafana
- Lưu trữ log có khả năng mở rộng với MinIO
- Giám sát log thời gian thực trên các microservices

---

*Lưu ý: Đảm bảo tất cả các file cấu hình được đặt đúng vị trí trong các thư mục tương ứng trước khi chạy Docker Compose.*