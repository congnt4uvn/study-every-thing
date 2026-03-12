# Tối Ưu Hóa Docker Compose Với Cấu Hình Chung

## Tổng Quan

Trong bài học này, chúng ta sẽ học cách tối ưu hóa file `docker-compose.yml` bằng cách loại bỏ nội dung lặp lại và tạo các template cấu hình có thể tái sử dụng thông qua file `common-config.yml` riêng biệt.

## Tạo File Cấu Hình Chung

### Bước 1: Tạo common-config.yml

Tạo một file mới có tên `common-config.yml` trong cùng thư mục với file `docker-compose.yml`:

```yaml
services:
  network-deploy-service:
    networks:
      - eazybank
```

### Bước 2: Định Nghĩa Các Service Cấu Hình Cơ Bản

#### Network Deploy Service

Service này chứa cấu hình liên quan đến network mà tất cả các service cần:

```yaml
services:
  network-deploy-service:
    networks:
      - eazybank
```

#### Microservice Base Config

Service này kế thừa network service và thêm các cấu hình chung cho microservices:

```yaml
  microservice-base-config:
    extends:
      service: network-deploy-service
    deploy:
      resources:
        limits:
          memory: 700m
```

**Lưu ý:** Biến môi trường `SPRING_PROFILES_ACTIVE` ban đầu được xem xét ở đây nhưng đã được chuyển sang service tiếp theo để giữ cấu hình RabbitMQ riêng biệt.

#### Microservice ConfigServer Config

Service này dành cho các microservices phụ thuộc vào config server:

```yaml
  microservice-configserver-config:
    extends:
      service: microservice-base-config
    depends_on:
      configserver:
        condition: service_healthy
    environment:
      SPRING_PROFILES_ACTIVE: default
      SPRING_CONFIG_IMPORT: configserver:http://configserver:8071/
```

## Phân Cấp Cấu Hình Service

### Cấu Trúc Cấu Hình Ba Tầng

1. **network-deploy-service**: Cấu hình network cơ bản
2. **microservice-base-config**: Kế thừa network service + thêm cấu hình deployment
3. **microservice-configserver-config**: Kế thừa base config + thêm phụ thuộc config server

### Tại Sao Phải Tách Riêng Các Service?

- **RabbitMQ** chỉ cần cấu hình network (sử dụng `network-deploy-service`)
- **Config Server** cần cấu hình network + deployment (sử dụng `microservice-base-config`)
- **Microservices nghiệp vụ** (accounts, loans, cards) cần tất cả cấu hình bao gồm phụ thuộc config server (sử dụng `microservice-configserver-config`)

## Cập Nhật docker-compose.yml

### RabbitMQ Service

Thay thế cấu hình network bằng:

```yaml
rabbitmq:
  image: rabbitmq:3.13-management
  hostname: rabbitmq
  ports:
    - "5672:5672"
    - "15672:15672"
  healthcheck:
    test: rabbitmq-diagnostics check_port_connectivity
    interval: 10s
    timeout: 5s
    retries: 10
    start_period: 5s
  extends:
    file: common-config.yml
    service: network-deploy-service
```

### Config Server

```yaml
configserver:
  image: "eazybytes/configserver:s6"
  container_name: configserver-ms
  ports:
    - "8071:8071"
  healthcheck:
    test: "curl --fail --silent localhost:8071/actuator/health/readiness | grep UP || exit 1"
    interval: 10s
    timeout: 5s
    retries: 10
    start_period: 10s
  extends:
    file: common-config.yml
    service: microservice-base-config
```

### Microservices Nghiệp Vụ (Accounts, Loans, Cards)

Với mỗi microservice, xóa bỏ:
- Phần `depends_on`
- Phần `deploy`
- Phần `networks`
- Biến môi trường `SPRING_CONFIG_IMPORT`
- Biến môi trường `SPRING_PROFILES_ACTIVE`

Thay thế bằng:

```yaml
accounts:
  image: "eazybytes/accounts:s6"
  container_name: accounts-ms
  ports:
    - "8080:8080"
  environment:
    SPRING_APPLICATION_NAME: "accounts"
  extends:
    file: common-config.yml
    service: microservice-configserver-config
```

## Lợi Ích Của Phương Pháp Này

1. **Nguồn Chân Lý Duy Nhất**: Tên network, giới hạn bộ nhớ và cấu hình chung ở một nơi
2. **Bảo Trì Dễ Dàng Hơn**: Thay đổi cấu hình một lần, áp dụng cho tất cả services
3. **Cải Thiện Khả Năng Đọc**: File `docker-compose.yml` ngắn gọn và sạch hơn
4. **Tổ Chức Tốt Hơn**: Tách biệt các mối quan tâm giữa cấu hình chung và cấu hình đặc thù của service
5. **Giảm Trùng Lặp**: Không còn các khối cấu hình lặp lại

## Những Điểm Chính Cần Nhớ

- Các cấu hình chung được trích xuất vào `common-config.yml`
- Các service kế thừa cấu hình cơ bản bằng từ khóa `extends`
- Phân cấp cấu hình cho phép các mẫu tái sử dụng linh hoạt
- RabbitMQ, Config Server và microservices nghiệp vụ mỗi cái kế thừa các base service phù hợp
- Các thay đổi tương lai đối với cấu hình chung chỉ cần thực hiện ở một nơi

## Bước Tiếp Theo

Trong bài học tiếp theo, chúng ta sẽ tạo các Docker image để kiểm tra các thay đổi docker-compose này.