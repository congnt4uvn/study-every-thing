# Cài Đặt Apache Kafka Trong Môi Trường Local

## Tổng Quan

Hướng dẫn này sẽ giúp bạn thực hiện quá trình cài đặt và thiết lập Apache Kafka trong môi trường phát triển local để giao tiếp giữa các microservices.

## Yêu Cầu Trước Khi Bắt Đầu

- Đã cài đặt Docker trên hệ thống local
- Hiểu biết cơ bản về kiến trúc microservices
- IntelliJ IDEA (hoặc IDE ưa thích)

## Bắt Đầu Với Apache Kafka

### Bước 1: Truy Cập Website Apache Kafka

1. Truy cập website chính thức của Apache Kafka: [kafka.apache.org](https://kafka.apache.org)
2. Khám phá các khả năng cốt lõi, hệ sinh thái và các trường hợp sử dụng của Kafka
3. Lưu ý rằng Apache Kafka được sử dụng bởi hơn 80% các công ty Fortune 100

### Bước 2: Truy Cập Hướng Dẫn Nhanh

1. Di chuột qua menu "Get Started"
2. Click vào "Quick Start"
3. Trang Quick Start cung cấp nhiều tùy chọn cài đặt khác nhau

### Bước 3: Cài Đặt Với Docker (Khuyến Nghị)

Cách dễ nhất để cài đặt Kafka là sử dụng Docker, phù hợp với việc sử dụng Docker trong suốt khóa học.

**Quan trọng:** Đảm bảo sao chép lệnh Docker dưới tiêu đề **JVM based**, không phải từ phần GraalVM.

#### Chạy Kafka Với Docker

Thực thi lệnh Docker trong terminal của bạn. Lệnh này sẽ:
- Khởi động Kafka trên cổng **9092** trong hệ thống local
- Khởi tạo Kafka broker
- Sẵn sàng cho các kết nối

#### Xác Minh

Sau vài giây, bạn sẽ thấy các console logs cho biết Kafka đang chờ kết nối tại cổng 9092.

### Bước 4: Cấu Hình Microservices

Sau khi Kafka đang chạy, bạn cần cấu hình nó trong các microservices:

1. **Message Microservice** - Cấu hình để tạo ra các events
2. **Account Microservice** - Cấu hình để tiêu thụ các events

Các services này sẽ giao tiếp bất đồng bộ bằng cách tận dụng khả năng event streaming của Kafka.

## Tích Hợp Docker Compose

Sau khi test thành công mọi thứ trong môi trường IntelliJ local, bạn có thể cập nhật file `docker-compose.yml` để bao gồm cài đặt Kafka nhằm dễ dàng triển khai và quản lý hơn.

## Các Điểm Chính

- Kafka chạy trên cổng **9092** theo mặc định
- Được sử dụng cho giao tiếp bất đồng bộ giữa các microservices
- Kích hoạt khả năng event streaming
- Được chấp nhận rộng rãi bởi các tổ chức doanh nghiệp
- Docker cung cấp phương pháp cài đặt dễ nhất

## Các Bước Tiếp Theo

- Cấu hình Spring Cloud Stream trong microservices của bạn
- Triển khai producers và consumers
- Test giao tiếp event-driven
- Cập nhật cấu hình Docker Compose

---

*Việc cài đặt này rất quan trọng để triển khai kiến trúc microservices hướng sự kiện với Apache Kafka.*