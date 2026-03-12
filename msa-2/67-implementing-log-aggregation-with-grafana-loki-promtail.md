# Triển khai Log Aggregation với Grafana, Loki và Promtail

## Tổng quan

Hướng dẫn này sẽ giúp bạn triển khai tập hợp log (log aggregation) trong kiến trúc microservices sử dụng Grafana, Loki và Promtail. Giải pháp này cho phép ghi log tập trung cho các microservices Spring Boot chạy trên Docker.

## Yêu cầu trước khi bắt đầu

- Đã cài đặt Docker trên hệ thống
- Đã cài đặt Docker Compose
- Có sẵn dự án microservices (Section 11)

## Thiết lập dự án ban đầu

### 1. Chuẩn bị Workspace

1. Copy code từ section trước vào workspace của bạn
2. Đổi tên thư mục thành `section11`
3. Xóa các file cấu hình ẩn của IntelliJ IDEA
4. Mở project trong IntelliJ IDEA

### 2. Cập nhật Maven Projects

**Cập nhật Docker Image Tags:**
- Thay đổi tất cả Docker image tags từ `s10` thành `s11` trong các file `pom.xml`
- Build các projects và enable annotation processing

### 3. Cấu hình Timeout cho Gateway Server

Trong file `application.yml` của gateway server:

```yaml
# Tăng response timeout từ 2s lên 10s
response-timeout: 10s
```

**Lý do:** Khi chạy nhiều container trên local với bộ nhớ hạn chế, 2 giây có thể không đủ. Tăng lên 10 giây giúp tránh các vấn đề timeout khi test trên môi trường local.

## Hiểu về Log Aggregation Stack

### Kiến trúc các thành phần

1. **Grafana** - Giao diện trực quan hóa và truy vấn
2. **Loki** - Hệ thống tập hợp log (các thành phần Read/Write)
3. **Promtail** - Agent thu thập log
4. **Minio** - Backend lưu trữ local
5. **Nginx Gateway** - Định tuyến cho các thành phần Loki

## Cấu hình Docker Compose

### Các file YAML cần thiết

Download 3 file cấu hình:
1. `docker-compose.yml`
2. `promtail-local-config.yml`
3. `loki-config.yml`

### Hiểu về docker-compose.yml

#### Cấu hình Network

```yaml
version: "3"
networks:
  loki:
    driver: bridge
```

Tất cả services chạy trên cùng network `loki` để các container có thể giao tiếp với nhau.

#### Loki Read Component

```yaml
services:
  read:
    image: grafana/loki
    command: "-config.file=/etc/loki/config.yaml -target=read"
    ports:
      - "3101:3101"
    volumes:
      - ./loki-config.yml:/etc/loki/config.yaml
    depends_on:
      - minio
    healthcheck:
      # Cấu hình health check
    networks:
      loki:
        aliases:
          - loki
```

**Điểm chính:**
- Expose port `3101`
- Mount file `loki-config.yml` từ local vào container
- Sử dụng anchor `&loki-dns` để tái sử dụng cấu hình network

#### Loki Write Component

```yaml
  write:
    image: grafana/loki
    command: "-config.file=/etc/loki/config.yaml -target=write"
    ports:
      - "3102:3102"
    volumes:
      - ./loki-config.yml:/etc/loki/config.yaml
    depends_on:
      - minio
    networks:
      <<: *loki-dns  # Merge tham chiếu anchor
```

**Điểm chính:**
- Expose port `3102`
- Sử dụng merge operator `<<:` và alias `*loki-dns` để tái sử dụng cấu hình network

#### Promtail Service

```yaml
  promtail:
    image: grafana/promtail
    volumes:
      - ./promtail-local-config.yml:/etc/promtail/config.yml:ro
      - /var/run/docker.sock:/var/run/docker.sock
    command: "-config.file=/etc/promtail/config.yml"
    depends_on:
      - gateway
    networks:
      - loki
```

**Điểm chính:**
- Mount config dưới dạng read-only (`:ro`)
- Truy cập Docker socket để đọc log từ containers
- Phụ thuộc vào gateway để forward log

#### Minio Storage Service

```yaml
  minio:
    image: minio/minio
    entrypoint:
      - sh
      - -euc
      - mkdir -p /data/loki-data /data/loki-ruler && minio server /data
    environment:
      - MINIO_ROOT_USER=loki
      - MINIO_ROOT_PASSWORD=supersecret
    ports:
      - "9000:9000"
    volumes:
      - ./.data/minio:/data
```

**Điểm chính:**
- Tạo thư mục để lưu trữ log khi khởi động
- Lưu log trong thư mục local `.data/minio`
- Có thể thay thế bằng cloud storage (S3) trong môi trường production

#### Grafana Service

```yaml
  grafana:
    image: grafana/grafana
    environment:
      - GF_PATHS_PROVISIONING=/etc/grafana/provisioning
    entrypoint:
      - sh
      - -euc
      - |
        mkdir -p /etc/grafana/provisioning/datasources
        cat <<EOF > /etc/grafana/provisioning/datasources/ds.yml
        apiVersion: 1
        datasources:
          - name: Loki
            type: loki
            access: proxy
            url: http://gateway:3100
        EOF
        /run.sh
    ports:
      - "3000:3000"
    depends_on:
      - gateway
    networks:
      - loki
```

**Điểm chính:**
- Tự động cấu hình Loki datasource khi khởi động
- Expose UI trên port `3000`
- Kết nối với Loki thông qua gateway tại port `3100`

#### Nginx Gateway Service

```yaml
  gateway:
    image: nginx
    depends_on:
      - read
      - write
    entrypoint:
      - sh
      - -euc
      - |
        # Cấu hình routing Nginx
        # Route /loki/api/v1/push tới write component
        # Route các API khác tới read component
    ports:
      - "3100:3100"
    networks:
      - loki
```

**Điểm chính:**
- Route các write requests tới write component (port 3100)
- Route các read/query requests tới read component
- Cung cấp điểm truy cập duy nhất cho Loki services

### Hiểu về promtail-local-config.yml

```yaml
server:
  http_listen_port: 9080
  grpc_listen_port: 0

clients:
  - url: http://gateway:3100/loki/api/v1/push

scrape_configs:
  - job_name: flog_scrape
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
        refresh_interval: 5s
    relabel_configs:
      - source_labels: ['__meta_docker_container_name']
        regex: '/(.*)'
        target_label: 'container'
```

**Điểm chính:**
- Lắng nghe trên port `9080` cho HTTP
- Push log tới gateway tại port `3100`
- Scrape log từ Docker containers qua socket
- Refresh mỗi 5 giây
- Gán nhãn log với tên container

### Hiểu về loki-config.yml

```yaml
server:
  http_listen_port: 3100

common:
  storage:
    s3:
      endpoint: minio:9000
      bucketnames: loki-data
      access_key_id: loki
      secret_access_key: supersecret
      s3forcepathstyle: true
```

**Điểm chính:**
- Loki lắng nghe trên port `3100`
- Sử dụng Minio làm storage tương thích S3
- Lưu log trong bucket `loki-data`
- Có thể cấu hình cho cloud storage trong production

## Các khái niệm YAML được sử dụng

### Volumes
Map files/directories từ host vào container:
```yaml
volumes:
  - ./local-file.yml:/container/path/file.yml:ro
```

### Anchors và Aliases
Tạo các khối cấu hình có thể tái sử dụng:
```yaml
networks:
  loki:
    aliases:
      - loki
  &loki-dns  # Định nghĩa anchor

# Tham chiếu sau:
networks:
  <<: *loki-dns  # Merge nội dung anchor
```

### Merge Operator
`<<:` merge cấu hình được tham chiếu vào khối hiện tại

## Các bước triển khai

1. **Download các file cấu hình**
   - Đặt cả 3 file YAML vào cùng thư mục với file Docker Compose của bạn

2. **Cập nhật Docker Compose**
   - Tích hợp cấu hình Loki stack
   - Xóa service `flog` (không cần thiết cho microservices thực tế)

3. **Cấu hình Microservices**
   - Đảm bảo microservices tạo ra log đúng cách
   - Không cần thay đổi code để thu thập log

4. **Khởi động Stack**
   ```bash
   docker-compose up -d
   ```

5. **Truy cập Grafana**
   - Mở trình duyệt tại `http://localhost:3000`
   - Đăng nhập với thông tin mặc định
   - Bắt đầu truy vấn log từ Loki datasource

## Cân nhắc cho môi trường Production

### Lưu trữ
- Thay thế Minio bằng cloud storage (AWS S3, Azure Blob Storage, GCS)
- Cập nhật `loki-config.yml` với thông tin đăng nhập cloud provider

### Hiệu năng
- Điều chỉnh scrape intervals dựa trên khối lượng log
- Cấu hình retention policies
- Scale các read/write components khi cần

### Bảo mật
- Thay đổi mật khẩu mặc định
- Sử dụng secrets management
- Enable authentication trên Grafana

## Lợi ích

1. **Log tập trung** - Tất cả log của microservices ở một nơi
2. **Dễ dàng debug** - Tìm kiếm trên tất cả services cùng lúc
3. **Khả năng quan sát** - Hiểu rõ hơn về hành vi hệ thống
4. **Có thể mở rộng** - Xử lý log từ nhiều microservices

## Các bước tiếp theo

- Tích hợp cấu hình vào Docker Compose hiện có
- Test thu thập log từ microservices của bạn
- Tạo custom Grafana dashboards
- Thiết lập alerting dựa trên log patterns

## Tóm tắt

Implementation này cung cấp giải pháp log aggregation hoàn chỉnh cho microservices sử dụng:
- **Promtail** để thu thập log từ Docker containers
- **Loki** để lưu trữ và đánh index log hiệu quả
- **Grafana** để trực quan hóa và truy vấn
- **Minio** để lưu trữ local (có thể thay thế bằng cloud storage)

Giải pháp này sẵn sàng cho production với các điều chỉnh cấu hình phù hợp cho môi trường cụ thể của bạn.