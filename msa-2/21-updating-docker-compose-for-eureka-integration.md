# Cập Nhật Docker Compose Để Tích Hợp Eureka

## Tổng Quan

Hướng dẫn này sẽ hướng dẫn bạn quy trình cập nhật các tệp cấu hình Docker Compose để tích hợp Eureka Service Discovery vào môi trường microservices. Chúng ta sẽ cấu hình Eureka Server và cập nhật tất cả các microservices để đăng ký với nó.

## Yêu Cầu Trước

- Đã cài đặt Docker và Docker Compose
- Kiến trúc microservices hiện có với Config Server
- Hiểu biết cơ bản về Spring Boot và Eureka

## Bước 1: Xóa RabbitMQ Service

Đầu tiên, mở tệp Docker Compose trong thư mục profile mặc định và xóa RabbitMQ service vì nó không còn cần thiết nữa.

1. Xóa định nghĩa RabbitMQ service
2. Xóa cấu hình `depends_on` cho RabbitMQ dưới Config Server
3. Cập nhật phiên bản image từ S6 lên S8

## Bước 2: Thêm Eureka Server Service

Tạo một định nghĩa service mới cho Eureka Server:

```yaml
eurekaserver:
  image: eazybytes/eurekaserver:s8
  container_name: eurekaserver-ms
  ports:
    - "8070:8070"
  healthcheck:
    test: "curl --fail --silent localhost:8070/actuator/health/readiness | grep UP || exit 1"
    interval: 10s
    timeout: 5s
    retries: 10
    start_period: 10s
  extends:
    file: common-config.yml
    service: microservice-configserver-config
  depends_on:
    configserver:
      condition: service_healthy
  environment:
    SPRING_APPLICATION_NAME: "eurekaserver"
```

### Chi Tiết Cấu Hình Chính

- **Ánh Xạ Cổng**: Eureka Server chạy trên cổng 8070
- **Kiểm Tra Sức Khỏe**: Sử dụng actuator health endpoint để kiểm tra readiness
- **Phụ Thuộc**: Phụ thuộc vào Config Server phải healthy
- **Tên Ứng Dụng**: Đặt là "eurekaserver" để tải cấu hình từ Config Server

## Bước 3: Cập Nhật Cấu Hình Chung

Trong tệp `common-config.yml`, thêm các cấu hình liên quan đến Eureka sẽ được chia sẻ giữa tất cả các microservices:

### Thêm Phụ Thuộc Eureka Server

```yaml
microservice-configserver-config:
  depends_on:
    configserver:
      condition: service_healthy
    eurekaserver:
      condition: service_healthy
```

### Thêm Biến Môi Trường Eureka Client

```yaml
environment:
  EUREKA_CLIENT_SERVICEURL_DEFAULTZONE: http://eurekaserver:8070/eureka/
```

**Quan Trọng**: Sử dụng tên service (`eurekaserver`) thay vì `localhost` cho Docker networking.

### Xóa Cấu Hình RabbitMQ

Xóa bất kỳ biến môi trường nào liên quan đến RabbitMQ khỏi cấu hình chung.

## Bước 4: Cập Nhật Images Của Microservices

Cập nhật phiên bản Docker image cho tất cả các microservices:

- **Accounts Microservice**: Cập nhật từ S6 lên S8
- **Loans Microservice**: Cập nhật từ S6 lên S8
- **Cards Microservice**: Cập nhật từ S6 lên S8

## Bước 5: Sao Chép Cấu Hình Qua Các Môi Trường

Sao chép các tệp `docker-compose.yml` và `common-config.yml` đã cập nhật sang các profile môi trường khác:

### Cho Profile Production

1. Sao chép cả hai tệp vào thư mục `prod`
2. Cập nhật `SPRING_PROFILES_ACTIVE` từ `default` sang `prod` trong `common-config.yml`

### Cho Profile QA

1. Sao chép cả hai tệp vào thư mục `qa`
2. Cập nhật `SPRING_PROFILES_ACTIVE` từ `default` sang `qa` trong `common-config.yml`

## Lợi Ích Của Cấu Hình Dựa Trên Profile

Duy trì các tệp Docker Compose riêng biệt cho các môi trường khác nhau mang lại:

- **Linh Hoạt**: Dễ dàng tùy chỉnh cấu hình cho từng môi trường
- **Cách Ly**: Các thay đổi cụ thể cho môi trường không ảnh hưởng đến môi trường khác
- **Khả Năng Bảo Trì**: Tách biệt rõ ràng các mối quan tâm

## Luồng Phụ Thuộc Service

```
Accounts/Loans/Cards Microservices
         ↓
    Eureka Server
         ↓
    Config Server
```

Tất cả các microservices phụ thuộc vào cả Config Server và Eureka Server phải healthy trước khi khởi động.

## Cấu Hình Kiểm Tra Sức Khỏe

Cấu hình kiểm tra sức khỏe của Eureka Server đảm bảo:

- Các services chờ Eureka hoạt động hoàn toàn
- Health readiness endpoint được giám sát
- Tự động thử lại với khoảng thời gian có thể cấu hình
- Trình tự khởi động đúng của tất cả các services

## Các Bước Tiếp Theo

Sau khi cập nhật cấu hình Docker Compose:

1. Khởi động tất cả containers bằng Docker Compose
2. Xác minh Eureka Server dashboard tại `http://localhost:8070`
3. Xác nhận tất cả microservices đã đăng ký với Eureka
4. Kiểm tra service discovery và giao tiếp giữa các microservices

## Tóm Tắt

Bản cập nhật cấu hình này:

- ✅ Xóa RabbitMQ service đã lỗi thời
- ✅ Thêm Eureka Server với các kiểm tra sức khỏe phù hợp
- ✅ Cấu hình tất cả microservices làm Eureka clients
- ✅ Đảm bảo trình tự khởi động service đúng đắn
- ✅ Duy trì cấu hình cụ thể cho từng môi trường

Môi trường Docker hiện đã sẵn sàng để kiểm tra các pattern service discovery và registration dựa trên Eureka.