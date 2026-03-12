# Demo Distributed Tracing với OpenTelemetry

## Tổng quan

Hướng dẫn này trình bày cách triển khai và kiểm tra distributed tracing trong kiến trúc microservices sử dụng OpenTelemetry, Docker Compose và Grafana.

## Yêu cầu

- Tất cả Docker images của microservices đã được tạo với tích hợp OpenTelemetry
- Docker Compose đã được cài đặt
- Postman để kiểm tra API

## Khởi động Microservices

### Thiết lập ban đầu

Khởi động tất cả containers từ production profile sử dụng Docker Compose:

```bash
docker-compose up -d
```

**Quan trọng**: Đảm bảo tất cả Docker images của microservices đã được build với các thay đổi mới nhất liên quan đến OpenTelemetry trước khi chạy lệnh này.

## Xử lý sự cố Health Checks của Container

### Vấn đề: Containers thất bại trong Health Checks

Khi khởi động containers, bạn có thể gặp lỗi với accounts, cards và loans microservices. Điều này xảy ra vì:

1. OpenTelemetry Java agent JAR (20-30 MB) cần được load vào bộ nhớ
2. Quá trình loading này tốn thêm thời gian trong quá trình khởi động
3. Cấu hình health check mặc định không cho phép đủ thời gian để khởi tạo

### Giải pháp: Điều chỉnh tham số Health Check

Chỉnh sửa cài đặt health check trong file Docker Compose cho tất cả microservices:

**Cấu hình ban đầu:**
- Interval: 10s
- Retries: 10

**Cấu hình cập nhật:**
- Interval: 20s
- Retries: 20

Áp dụng những thay đổi này cho:
- Config Server
- Eureka Server
- Accounts Microservice
- Loans Microservice
- Cards Microservice
- Gateway Server (không cần health check)

### Khởi động lại Containers

Sau khi cập nhật cấu hình:

```bash
# Dừng và xóa các containers hiện tại
docker-compose down

# Khởi động containers với cấu hình đã cập nhật
docker-compose up -d
```

**Lưu ý**: Quá trình khởi động bây giờ sẽ mất khoảng 4+ phút do khoảng thời gian retry được mở rộng.

## Xác minh triển khai

### Kiểm tra trạng thái Container

1. Mở Docker Desktop
2. Xác minh tất cả containers đang chạy thành công
3. Kiểm tra logs của từng microservice

### Xác minh OpenTelemetry Agent được load

Trong logs của accounts microservice, bạn sẽ thấy:

```
Loading the Java Agent Library present inside /app/libs
```

Cấu trúc container bao gồm:
- Thư mục `/app/libs/` chứa tất cả JARs từ pom.xml
- OpenTelemetry JAR được load thông qua `JAVA_TOOL_OPTIONS` được định nghĩa trong Docker Compose

### Xác nhận Gateway Server

Xác minh Gateway Server đang chạy trên cổng 8072.

## Kiểm tra APIs

Sử dụng Postman để kiểm tra các endpoints sau:

### 1. Tạo tài khoản
- **Endpoint**: POST `/create` (Accounts Microservice)
- **Kết quả mong đợi**: 
  - Status Code: 201
  - Message: "Account created successfully"

### 2. Tạo thông tin thẻ
- **Endpoint**: POST `/create` (Cards Microservice)
- **Kết quả mong đợi**: 
  - Status: "Card details created successfully"

### 3. Tạo thông tin khoản vay
- **Endpoint**: POST `/create` (Loans Microservice)
- **Kết quả mong đợi**: 
  - Status: "Loan created successfully"

### 4. Lấy thông tin khách hàng
- **Endpoint**: GET `/fetchCustomerDetails`
- **Kết quả mong đợi**: 
  - Thông tin tài khoản
  - Thông tin khoản vay
  - Thông tin thẻ

## Xem Distributed Tracing trong Grafana

Sau khi kiểm tra thành công các APIs, truy cập Grafana để xem thông tin distributed tracing.

Dữ liệu tracing sẽ hiển thị:
- Luồng request qua các microservices
- Các phụ thuộc giữa các services
- Metrics về hiệu suất
- Độ trễ của request

## Những điểm chính

1. **Tích hợp OpenTelemetry**: Java agent tự động instrument các microservices của bạn cho distributed tracing
2. **Cấu hình Health Check**: Điều chỉnh các tham số health check dựa trên yêu cầu khởi động của ứng dụng
3. **Thời gian khởi động Container**: Việc load OpenTelemetry agent tăng thêm overhead khi khởi động
4. **End-to-End Tracing**: Tất cả API calls được trace qua toàn bộ hệ sinh thái microservices

## Các bước tiếp theo

Trong bài giảng tiếp theo, chúng ta sẽ khám phá cách phân tích và diễn giải thông tin tracing trong Grafana, bao gồm:
- Hiểu về trace spans
- Xác định các bottleneck về hiệu suất
- Phân tích các phụ thuộc giữa services
- Thiết lập alerts dựa trên dữ liệu tracing