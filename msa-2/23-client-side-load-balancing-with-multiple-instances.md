# Cân Bằng Tải Phía Client với Nhiều Instance Microservice

## Tổng Quan

Hướng dẫn này trình bày cách triển khai và kiểm tra cân bằng tải phía client bằng cách chạy nhiều instance của một microservice với Spring Boot, Eureka Service Discovery và Docker Compose.

## Yêu Cầu Trước

- Đã cài đặt Docker và Docker Compose
- Kiến trúc microservices Spring Boot với Eureka Server
- Hiểu biết cơ bản về service discovery và cân bằng tải

## Tạo Nhiều Instance với Docker Compose

### Bước 1: Nhân Bản Cấu Hình Service

Để tạo nhiều instance của loans microservice, bạn cần nhân bản cấu hình service trong file `docker-compose.yml`.

**Các điểm quan trọng:**
- Tên service phải là duy nhất (ví dụ: `loans`, `loans1`)
- Tên container phải là duy nhất (ví dụ: `loans-ms`, `loans-ms1`)
- Các port mapping phải khác nhau để tránh xung đột

### Bước 2: Cập Nhật Cấu Hình Docker Compose

```yaml
services:
  loans:
    container_name: loans-ms
    ports:
      - "8090:8090"
    # ... các cấu hình khác

  loans1:
    container_name: loans-ms1
    ports:
      - "8091:8090"  # Port host khác
    # ... các cấu hình khác
```

### Bước 3: Khởi Động Các Services

Chạy lệnh sau để khởi động tất cả services:

```bash
docker-compose up -d
```

**Hành vi mong đợi:**
- Thời gian khởi động: 3-4 phút cho nhiều containers
- Sử dụng CPU cao là bình thường (có thể đạt 200-500% với nhiều cores)
- Tất cả instances sẽ đăng ký với Eureka Server độc lập

## Xác Minh Đăng Ký Service

### Kiểm Tra Eureka Dashboard

Truy cập Eureka dashboard để xác minh nhiều instances đã được đăng ký:

- URL: `http://localhost:8070/eureka/apps`
- Tìm số lượng instance trong dấu ngoặc (ví dụ: LOANS (2))
- Mỗi instance sẽ có thông tin đăng ký riêng biệt

### Kết Quả Đăng Ký Mong Đợi

- **Accounts Microservice:** 1 instance
- **Cards Microservice:** 1 instance
- **Loans Microservice:** 2 instances

## Kiểm Tra Cân Bằng Tải Phía Client

### Hiểu Kịch Bản Kiểm Tra

Vì mỗi instance microservice sử dụng database H2 riêng trong demo này:
- Dữ liệu tạo trên một instance sẽ không có sẵn trên instance khác
- Điều này mô phỏng hành vi cân bằng tải
- Trong production, tất cả instances sẽ chia sẻ cùng database (MySQL, PostgreSQL, v.v.)

### Các Bước Kiểm Tra

1. **Tạo dữ liệu test trên một instance:**
   - Tạo thông tin tài khoản
   - Tạo thông tin thẻ
   - Tạo thông tin khoản vay chỉ sử dụng port 8090

2. **Kiểm tra API Fetch Customer Details:**
   ```
   GET /api/fetchCustomerDetails?mobileNumber={number}
   ```

3. **Quan sát kết quả:**
   - Một số request sẽ thành công (được route đến instance có dữ liệu)
   - Một số request sẽ thất bại với lỗi "Loan not found" (được route đến instance không có dữ liệu)
   - Hành vi luân phiên này chứng minh cân bằng tải đang hoạt động

## Cách Hoạt Động của Cân Bằng Tải Phía Client

### Các Thành Phần Chính

1. **Eureka Server:** Duy trì service registry
2. **Eureka Client:** Mỗi instance microservice tự đăng ký
3. **OpenFeign Client:** Xử lý cân bằng tải ở cấp độ client
4. **Service Discovery:** Tự động phát hiện các instances có sẵn

### Luồng Cân Bằng Tải

1. Account service truy vấn Eureka để lấy các instances Loans service khả dụng
2. OpenFeign Client nhận danh sách tất cả instances đã đăng ký
3. Các requests được phân phối qua các instances sử dụng thuật toán cân bằng tải
4. Mỗi request có thể được route đến một instance khác nhau

## Các Cân Nhắc về Hiệu Suất

### Môi Trường Development Cục Bộ

- **Sử Dụng CPU:** Có thể đạt 200-500% với nhiều containers
- **Tài Nguyên Docker:** Phân bổ ít nhất 5 cores cho hiệu suất tối ưu
- **Thời Gian Khởi Động:** 3-4 phút để khởi tạo hoàn toàn
- **Memory:** Giám sát phân bổ memory của Docker

### Môi Trường Production

- Tất cả instances nên kết nối đến database được chia sẻ (MySQL, PostgreSQL)
- Cân nhắc sử dụng Kubernetes cho orchestration tốt hơn
- Cân bằng tải phía server có thể được triển khai cùng với phía client

## Những Điểm Chính Cần Nhớ

1. **Nhiều Instances:** Dễ dàng tạo bằng cách nhân bản cấu hình Docker Compose
2. **Tự Động Phát Hiện:** Eureka tự động theo dõi tất cả instances
3. **Cân Bằng Tải Phía Client:** OpenFeign xử lý phân phối một cách trong suốt
4. **Không Cần Load Balancer Bên Ngoài:** Cân bằng tải xảy ra ở cấp độ ứng dụng
5. **Khả Năng Mở Rộng:** Thêm hoặc xóa instances mà không cần thay đổi code

## Các Bước Tiếp Theo

- Khám phá service discovery phía server với Kubernetes
- Triển khai health checks và graceful shutdown
- Cấu hình các thuật toán cân bằng tải tùy chỉnh
- Thiết lập databases cấp production cho shared state

## Kết Luận

Cân bằng tải phía client với Spring Cloud và Eureka cung cấp một cách tiếp cận phi tập trung mạnh mẽ để phân phối requests qua nhiều instances của service. Thư viện OpenFeign Client tích hợp liền mạch với Eureka Service Discovery để cho phép cân bằng tải tự động mà không cần load balancers bên ngoài.

---

**Các Chủ Đề Liên Quan:**
- Service Discovery và Registration
- Cấu Hình Eureka Server
- Triển Khai OpenFeign Client
- Docker Compose cho Microservices
- Các Mẫu Khả Năng Mở Rộng Microservice