# Kiểm Tra Sức Khỏe và Phụ Thuộc Dịch Vụ trong Docker Compose

## Tổng Quan

Hướng dẫn này giải thích cách cấu hình kiểm tra sức khỏe (health checks) và phụ thuộc dịch vụ trong Docker Compose cho kiến trúc microservices sử dụng Spring Boot, Config Server và RabbitMQ.

## Mục Lục

1. [Cấu Hình Health Checks cho Config Server](#cấu-hình-health-checks-cho-config-server)
2. [Thiết Lập Phụ Thuộc Dịch Vụ](#thiết-lập-phụ-thuộc-dịch-vụ)
3. [Thêm Dịch Vụ RabbitMQ](#thêm-dịch-vụ-rabbitmq)
4. [Tối Ưu Cấu Hình Docker Compose](#tối-ưu-cấu-hình-docker-compose)

## Cấu Hình Health Checks cho Config Server

### Tại Sao Cần Health Checks?

Health checks cho phép Docker Compose xác định xem một dịch vụ đã khởi động thành công và sẵn sàng nhận yêu cầu hay chưa. Không có health checks, Docker Compose chỉ biết khi nào dịch vụ bắt đầu khởi động, chứ không biết khi nào nó hoạt động đầy đủ.

### Thêm Cấu Hình Health Check

Trong dịch vụ `config-server` của file `docker-compose.yml`, thêm phần `healthcheck` sau cấu hình `ports`:

```yaml
config-server:
  ports:
    - "8071:8071"
  healthcheck:
    test: "curl --fail --silent localhost:8071/actuator/health/readiness | grep UP || exit 1"
    interval: 10s
    timeout: 5s
    retries: 10
    start_period: 10s
```

### Giải Thích Các Tham Số Health Check

- **test**: Lệnh kiểm tra sức khỏe dịch vụ. Sử dụng `curl` để gọi endpoint readiness của actuator và tìm kiếm trạng thái "UP" bằng `grep`
- **interval**: Thời gian giữa các lần thử health check (10 giây)
- **timeout**: Thời gian tối đa chờ phản hồi cho mỗi lần kiểm tra (5 giây)
- **retries**: Số lần thử lại trước khi coi dịch vụ không khỏe mạnh (10 lần)
- **start_period**: Thời gian trễ ban đầu trước khi bắt đầu health checks (10 giây)

## Thiết Lập Phụ Thuộc Dịch Vụ

### Cấu Hình depends_on với Điều Kiện Sức Khỏe

Để microservice `accounts` đợi Config Server hoàn toàn khỏe mạnh, thêm cấu hình sau:

```yaml
accounts:
  ports:
    - "8080:8080"
  depends_on:
    config-server:
      condition: service_healthy
```

### Các Tùy Chọn Điều Kiện Có Sẵn

- **service_started**: Chỉ đợi cho đến khi dịch vụ khởi động (không kiểm tra sức khỏe)
- **service_healthy**: Đợi cho đến khi health check thành công (được khuyến nghị)
- **service_completed_successfully**: Đợi dịch vụ hoàn thành thành công (phiên bản Docker mới hơn)

### Tại Sao Nên Dùng service_healthy

Sử dụng `condition: service_healthy` đảm bảo các dịch vụ phụ thuộc chỉ khởi động sau khi health check của Config Server thành công, tránh lỗi kết nối và lỗi khởi động.

### Áp Dụng Phụ Thuộc Cho Các Microservices Khác

Áp dụng cấu hình tương tự cho microservices `loans` và `cards`:

```yaml
loans:
  ports:
    - "8090:8090"
  depends_on:
    config-server:
      condition: service_healthy

cards:
  ports:
    - "9000:9000"
  depends_on:
    config-server:
      condition: service_healthy
```

## Thêm Dịch Vụ RabbitMQ

### Tại Sao Cần RabbitMQ?

RabbitMQ được yêu cầu cho Spring Cloud Bus, cho phép cập nhật cấu hình động trên các microservices mà không cần khởi động lại.

### Cấu Hình Dịch Vụ RabbitMQ

```yaml
rabbit:
  image: rabbitmq:3-management
  hostname: rabbitmq
  ports:
    - "5672:5672"
    - "15672:15672"
  healthcheck:
    test: rabbitmq-diagnostics -q ping
    interval: 10s
    timeout: 5s
    retries: 10
    start_period: 10s
  networks:
    - easybank
```

### Hiểu Về Các Cổng RabbitMQ

- **5672**: Cổng nhắn tin RabbitMQ cốt lõi
- **15672**: Cổng giao diện quản lý

RabbitMQ có hai thành phần yêu cầu các cổng riêng biệt:
1. Chức năng nhắn tin cốt lõi
2. Giao diện quản lý

### Health Check RabbitMQ

Health check sử dụng lệnh `rabbitmq-diagnostics -q ping`, đây là phương pháp chính thức được khuyến nghị trong tài liệu RabbitMQ.

### Thêm Phụ Thuộc RabbitMQ vào Config Server

```yaml
config-server:
  # ... các cấu hình khác
  depends_on:
    rabbit:
      condition: service_healthy
```

## Trình Tự Khởi Động Dịch Vụ

Với các cấu hình này, thứ tự khởi động là:

1. **RabbitMQ** khởi động trước và đợi health check thành công
2. **Config Server** khởi động sau khi RabbitMQ khỏe mạnh
3. **Accounts, Loans và Cards** microservices khởi động song song sau khi Config Server khỏe mạnh

### Phụ Thuộc Bắc Cầu

Các microservices accounts, loans và cards không cần phụ thuộc trực tiếp vào RabbitMQ vì:
- Chúng đã phụ thuộc vào Config Server
- Config Server phụ thuộc vào RabbitMQ
- Docker Compose tự động xử lý phụ thuộc bắc cầu

Tuy nhiên, bạn có thể thêm phụ thuộc RabbitMQ một cách rõ ràng nếu muốn mà không gây vấn đề gì.

## Tối Ưu Cấu Hình Docker Compose

### Vấn Đề: Cấu Hình Lặp Lại

File docker-compose.yml hiện tại chứa các cấu hình trùng lặp trên các dịch vụ:
- Hướng dẫn deploy lặp lại cho nhiều dịch vụ
- Cấu hình network lặp lại cho mỗi dịch vụ

### Giải Pháp: File Cấu Hình Chung

Chuyển các cấu hình lặp lại vào file chung và import chúng. Cách tiếp cận này:
- Loại bỏ sự trùng lặp
- Làm cho việc cập nhật dễ dàng hơn (thay đổi một lần, áp dụng mọi nơi)
- Cải thiện khả năng bảo trì

### Quan Trọng: Cấu Hình Network cho RabbitMQ

**Rất quan trọng**: Đừng quên thêm cấu hình network vào dịch vụ RabbitMQ:

```yaml
rabbit:
  # ... các cấu hình khác
  networks:
    - easybank
```

Không có cấu hình này, RabbitMQ sẽ khởi động trong một mạng cô lập, ngăn chặn giao tiếp với các microservices khác.

### Định Nghĩa Network

Ở cuối file docker-compose.yml, định nghĩa mạng chia sẻ:

```yaml
networks:
  easybank:
    driver: bridge
```

Tất cả các dịch vụ nên tham chiếu mạng này để đảm bảo chúng có thể giao tiếp với nhau.

## Tóm Tắt

Cấu hình này đảm bảo:
- ✅ Các dịch vụ khởi động theo đúng thứ tự
- ✅ Health checks xác thực sự sẵn sàng của dịch vụ
- ✅ Phụ thuộc ngăn chặn khởi động dịch vụ sớm
- ✅ Tất cả dịch vụ có thể giao tiếp trên cùng một mạng
- ✅ Cấu hình có thể bảo trì và mở rộng

## Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ tối ưu file docker-compose.yml bằng cách:
- Trích xuất các cấu hình chung
- Tạo các template cấu hình có thể tái sử dụng
- Giảm thêm sự trùng lặp