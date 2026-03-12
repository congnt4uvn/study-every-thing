# Cấu Hình Docker Compose cho Microservices Spring Boot với Config Server

## Tổng Quan

Hướng dẫn này trình bày cách cấu hình Docker Compose cho nhiều microservices Spring Boot với Config Server tập trung, hỗ trợ nhiều môi trường (default, QA và production).

## Yêu Cầu Tiên Quyết

- Các microservices đang hoạt động: Accounts, Loans và Cards
- Config Server đã được triển khai
- Hiểu biết về Docker và Docker Compose
- Kiến thức về Spring Cloud Config

## Cấu Trúc Dự Án

Cấu hình Docker Compose được tổ chức theo môi trường:

```
v2-spring-cloud-config/
└── docker-compose/
    ├── default/
    │   └── docker-compose.yml
    ├── qa/
    │   └── docker-compose.yml
    └── prod/
        └── docker-compose.yml
```

## Cấu Hình Docker Compose

### Cấu Hình Các Services

File Docker Compose bao gồm bốn services:
1. **Config Server** - Quản lý cấu hình tập trung
2. **Accounts Microservice** - Dịch vụ tài khoản
3. **Loans Microservice** - Dịch vụ cho vay
4. **Cards Microservice** - Dịch vụ thẻ

### Config Server Service

```yaml
configserver:
  image: eazybytes/configserver:s6
  container_name: configserver-ms
  ports:
    - "8071:8071"
  deploy:
    resources:
      limits:
        memory: 700m
  networks:
    - eazybank
```

### Ví Dụ Cấu Hình Microservice (Accounts)

```yaml
accounts:
  image: eazybytes/accounts:s6
  container_name: accounts-ms
  ports:
    - "8080:8080"
  environment:
    SPRING_CONFIG_IMPORT: configserver:http://configserver:8071/
    SPRING_PROFILES_ACTIVE: default
    SPRING_APPLICATION_NAME: accounts
  deploy:
    resources:
      limits:
        memory: 700m
  networks:
    - eazybank
```

## Các Khái Niệm Cấu Hình Quan Trọng

### 1. Biến Môi Trường (Environment Variables)

Biến môi trường được sử dụng để ghi đè các thuộc tính ứng dụng trong môi trường Docker:

- **SPRING_CONFIG_IMPORT**: Chỉ định kết nối đến Config Server
  - Định dạng: `configserver:http://configserver:8071/`
  - Xóa tiền tố `optional:` trong môi trường production
  - Sử dụng tên service thay vì `localhost`

- **SPRING_PROFILES_ACTIVE**: Định nghĩa Spring profile đang active
  - Giá trị: `default`, `qa`, hoặc `prod`
  - Phải khớp với vị trí file Docker Compose

- **SPRING_APPLICATION_NAME**: Định danh ứng dụng
  - Phải khớp với tiền tố file cấu hình trong Config Server
  - Bắt buộc do bug trong Spring Cloud Config Server (workaround)

### 2. Tên Service vs Localhost

**Quan trọng**: Trong môi trường Docker, các microservices không thể sử dụng `localhost` để giao tiếp với nhau.

- ❌ **Sai**: `http://localhost:8071`
- ✅ **Đúng**: `http://configserver:8071`

Mỗi Docker container chạy trong mạng cô lập riêng. Khi sử dụng `localhost`, container cố gắng kết nối với chính nó, không phải với các container khác.

### 3. Cấu Hình Network

Tất cả services phải ở trên cùng một Docker network để giao tiếp:

```yaml
networks:
  - eazybank
```

Điều này cho phép các services tham chiếu lẫn nhau bằng tên service (ví dụ: `configserver`, `accounts`).

### 4. Giới Hạn Bộ Nhớ

Giới hạn tài nguyên ngăn containers tiêu thụ quá nhiều bộ nhớ:

```yaml
deploy:
  resources:
    limits:
      memory: 700m
```

## Quản Lý Phụ Thuộc Services

### Thách Thức

Docker Compose khởi động containers theo thứ tự nhưng không đợi services sẵn sàng hoàn toàn. Điều này tạo ra vấn đề:

1. Config Server container khởi động
2. Microservices khởi động ngay lập tức (không đợi)
3. Microservices thất bại vì Config Server chưa sẵn sàng nhận request

### Giải Pháp

Để đảm bảo thứ tự khởi động và sẵn sàng đúng, chúng ta cần:

1. Triển khai các probe **liveness** và **readiness** trong Config Server
2. Thêm cấu hình phụ thuộc trong Docker Compose cho microservices
3. Đợi Config Server khỏe mạnh trước khi khởi động các services phụ thuộc

Các khái niệm này (liveness và readiness) sẽ được đề cập trong bài học tiếp theo.

## Cấu Hình Theo Môi Trường

### Môi Trường Default

- Vị trí: `docker-compose/default/`
- Profile: `default`
- Sử dụng cho: Phát triển và test local

### Môi Trường QA

- Vị trí: `docker-compose/qa/`
- Profile: `qa`
- Sử dụng cho: Kiểm thử đảm bảo chất lượng

### Môi Trường Production

- Vị trí: `docker-compose/prod/`
- Profile: `prod`
- Sử dụng cho: Triển khai production

## Các Bước Migration

1. **Tạo cấu trúc thư mục**
   ```
   docker-compose/
   ├── default/
   ├── qa/
   └── prod/
   ```

2. **Copy file Docker Compose hiện có** vào thư mục `default/`

3. **Cập nhật image tags** từ `s4` sang `s6` (hoặc section hiện tại)

4. **Thêm Config Server service** vào Docker Compose

5. **Thêm biến môi trường** cho tất cả microservices

6. **Cấu hình phụ thuộc services** (bước tiếp theo)

## Best Practices (Thực Hành Tốt Nhất)

1. **Xóa tiền tố `optional:`** trong Config Server imports cho production
2. **Sử dụng tên services** thay vì `localhost` trong môi trường Docker
3. **Tách file Docker Compose** cho các môi trường khác nhau
4. **Đặt giới hạn bộ nhớ** cho tất cả containers
5. **Sử dụng cùng network** cho tất cả services liên quan
6. **Đánh version Docker images** với tags có ý nghĩa (ví dụ: `s6`)

## Các Vấn Đề Thường Gặp và Giải Pháp

### Vấn Đề 1: Microservice Không Thể Kết Nối Config Server

**Triệu chứng**: Lỗi connection refused hoặc timeout

**Giải pháp**: 
- Kiểm tra tên service đúng (`configserver` không phải `localhost`)
- Xác minh tất cả services trên cùng network
- Đảm bảo port mapping của Config Server đúng (8071:8071)

### Vấn Đề 2: Load Sai Configuration Profile

**Triệu chứng**: Ứng dụng sử dụng properties sai

**Giải pháp**:
- Xác minh biến môi trường `SPRING_PROFILES_ACTIVE`
- Kiểm tra vị trí file Docker Compose khớp với môi trường mong muốn
- Xác nhận Config Server có files đúng theo profile

### Vấn Đề 3: Config Server Chưa Sẵn Sàng

**Triệu chứng**: Microservices thất bại khi khởi động với lỗi connection

**Giải pháp**:
- Triển khai health checks và readiness probes
- Thêm phụ thuộc services trong Docker Compose
- Sử dụng `depends_on` với điều kiện health

## Các Bước Tiếp Theo

1. Hiểu các khái niệm **liveness** và **readiness**
2. Triển khai health checks trong Config Server
3. Thêm cấu hình phụ thuộc trong Docker Compose
4. Test trình tự khởi động với `docker-compose up`
5. Triển khai lên Kubernetes cluster

## Tóm Tắt

Cấu hình này cho phép:
- ✅ Hỗ trợ đa môi trường (default, QA, prod)
- ✅ Quản lý cấu hình tập trung
- ✅ Giao tiếp giữa các container
- ✅ Quản lý tài nguyên với giới hạn bộ nhớ
- ✅ Kiến trúc microservices có thể mở rộng

Bước tiếp theo là triển khai health checks và phụ thuộc services phù hợp để đảm bảo thứ tự khởi động đáng tin cậy.