# Tự Động Làm Mới Cấu Hình với GitHub Webhooks và Spring Cloud Config Monitor

## Tổng Quan

Hướng dẫn này trình bày cách tự động làm mới các thuộc tính cấu hình trong microservices mà không cần can thiệp thủ công, sử dụng GitHub webhooks kết hợp với Spring Cloud Bus và Spring Cloud Config Monitor.

## Vấn Đề Đặt Ra

Trước đây, chúng ta có thể làm mới thuộc tính tại runtime bằng cách gọi:
- API `/bus-refresh` trên bất kỳ instance nào
- API `/refresh` trên tất cả các microservice instances

Tuy nhiên, cả hai phương pháp đều yêu cầu **gọi thủ công**. Chúng ta cần một giải pháp tự động làm mới thuộc tính khi có thay đổi được push lên configuration repository.

## Kiến Trúc Giải Pháp

Phương pháp tự động được xây dựng dựa trên Spring Cloud Bus và bổ sung:
- **Spring Cloud Config Monitor** - Mở endpoint `/monitor`
- **GitHub Webhooks** - Tự động kích hoạt làm mới khi có thay đổi cấu hình

### Cách Hoạt Động

1. Một thay đổi được push lên GitHub configuration repository
2. GitHub webhook gửi POST request đến endpoint `/monitor` trên Config Server
3. Config Server tự động kích hoạt sự kiện refresh qua Spring Cloud Bus và RabbitMQ
4. Tất cả microservices nhận thông báo refresh và cập nhật cấu hình

## Các Bước Triển Khai

### Bước 1: Thêm Dependency Config Monitor

Thêm dependency Spring Cloud Config Monitor **chỉ vào Config Server** trong `pom.xml`:

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-config-monitor</artifactId>
</dependency>
```

Dependency này mở endpoint REST API `/monitor` (không phải actuator endpoint).

### Bước 2: Cấu Hình Config Server

Cập nhật `application.yaml` của Config Server:

```yaml
management:
  endpoints:
    web:
      exposure:
        include: "*"

spring:
  rabbitmq:
    host: localhost
    port: 5672
    username: guest
    password: guest
```

**Tại sao phải mở tất cả management endpoints?**
Config Server cần tự động gọi API `bus-refresh` ở hậu trường.

### Bước 3: Thiết Lập RabbitMQ

Đảm bảo RabbitMQ đang chạy với cấu hình mặc định:
- Host: localhost
- Port: 5672
- Username: guest
- Password: guest

### Bước 4: Cấu Hình GitHub Webhook

#### Truy Cập Cài Đặt Webhook
1. Điều hướng đến GitHub configuration repository của bạn
2. Vào **Settings** → **Webhooks**
3. Click **Add webhook**

#### Thách Thức Cấu Hình Webhook

**Vấn đề:** GitHub không thể truy cập `http://localhost:8071/monitor` vì:
- Đây là URL cục bộ không có IP công khai
- GitHub servers không thể phân giải localhost

**Giải pháp:** Sử dụng dịch vụ relay webhook như [hookdeck.com](https://hookdeck.com)

### Bước 5: Thiết Lập Hookdeck để Test Cục Bộ

#### Cài Đặt Hookdeck CLI

Cho macOS:
```bash
brew install hookdeck
```

#### Đăng Nhập vào Hookdeck
```bash
hookdeck login
```

#### Tạo Connection
```bash
hookdeck listen 8071
```

Khi được nhắc:
- **Path:** `/monitor`
- **Connection label:** `localhost`

Lệnh này tạo một webhook URL công khai chuyển hướng đến Config Server cục bộ của bạn.

#### Cấu Hình GitHub Webhook

1. Copy URL webhook Hookdeck đã tạo
2. Trong cài đặt webhook GitHub:
   - **Payload URL:** `https://<hookdeck-url>/monitor`
   - **Content type:** `application/json`
   - **Events:** Chọn "Just the push event"
3. Click **Add webhook**

## Kiểm Tra Thiết Lập

### Bước 1: Khởi Động Tất Cả Services

Khởi động services theo thứ tự:
1. RabbitMQ (qua Docker)
2. Config Server (port 8071)
3. Accounts microservice
4. Loans microservice
5. Cards microservice

### Bước 2: Xác Minh Cấu Hình Hiện Tại

Test Config Server endpoint:
```
GET http://localhost:8071/cards/prod
```

Test microservice endpoint:
```
GET http://localhost:9000/contact-info
```

Cả hai phải trả về giá trị thuộc tính hiện tại (ví dụ: `prod`).

### Bước 3: Thực Hiện Thay Đổi Cấu Hình

1. Chỉnh sửa file cấu hình trong GitHub (ví dụ: `cards-prod.yaml`)
2. Thay đổi giá trị thuộc tính (ví dụ: từ `prod` thành `webhook`)
3. Commit thay đổi

### Bước 4: Quan Sát Làm Mới Tự Động

**Điều gì xảy ra:**
1. GitHub kích hoạt webhook
2. Hookdeck chuyển tiếp request đến `localhost:8071/monitor`
3. Config Server logs hiển thị POST request với response 200
4. Config Server tự động kích hoạt `/bus-refresh`
5. Tất cả microservices nhận thông báo refresh

### Bước 5: Xác Minh Cấu Hình Đã Cập Nhật

Test lại microservice endpoint:
```
GET http://localhost:9000/contact-info
```

Response phải phản ánh giá trị thuộc tính mới (ví dụ: `webhook`) **mà không cần can thiệp thủ công**.

## Chi Tiết Webhook

### Thông Tin Webhook Payload

Khi xem webhook delivery trong GitHub Settings:
- **Delivery Status:** Success/Failure
- **Request Headers:** Content-Type, User-Agent, v.v.
- **Request Body:** Bao gồm chi tiết commit, files đã sửa đổi, commit message
- **Response:** Status code và response body

### Ví Dụ Dữ Liệu Webhook Event
```json
{
  "commits": [{
    "id": "commit-id",
    "message": "update cards-prod.yaml",
    "modified": ["cards-prod.yaml"]
  }]
}
```

## Sơ Đồ Kiến Trúc Hoàn Chỉnh

```
┌─────────────┐         ┌──────────────┐         ┌───────────────┐
│   GitHub    │ webhook │   Hookdeck   │ forward │ Config Server │
│ Repository  ├────────►│   (relay)    ├────────►│  /monitor     │
└─────────────┘         └──────────────┘         └───────┬───────┘
                                                          │
                                                          │ /bus-refresh
                                                          ▼
                                                  ┌───────────────┐
                                                  │   RabbitMQ    │
                                                  │   (AMQP Bus)  │
                                                  └───────┬───────┘
                                                          │
                        ┌─────────────────────────────────┼─────────────────┐
                        │                                 │                 │
                        ▼                                 ▼                 ▼
                ┌───────────────┐               ┌────────────┐     ┌──────────┐
                │   Accounts    │               │   Loans    │     │  Cards   │
                │ Microservice  │               │Microservice│     │Microservice
                └───────────────┘               └────────────┘     └──────────┘
```

## Tóm Tắt Các Bước Cấu Hình

1. **Thêm Actuator dependency** vào tất cả microservices và Config Server
2. **Bật endpoint bus-refresh** qua thuộc tính management
3. **Thêm Spring Cloud Bus AMQP dependency** vào tất cả ứng dụng
4. **Thêm Spring Cloud Config Monitor dependency** chỉ vào Config Server (mở `/monitor`)
5. **Khởi động RabbitMQ** sử dụng lệnh Docker
6. **Tạo GitHub webhook** gửi POST requests đến `/monitor` khi có push events

## Khác Biệt Chính So Với Phương Pháp Thủ Công

| Khía Cạnh | Phương Pháp Thủ Công | Phương Pháp Tự Động |
|-----------|---------------------|---------------------|
| Kích hoạt | Gọi API thủ công đến `/bus-refresh` hoặc `/refresh` | Tự động khi Git push |
| Can thiệp thủ công | Yêu cầu | Không yêu cầu |
| Thành phần bổ sung | Spring Cloud Bus + RabbitMQ | Spring Cloud Bus + RabbitMQ + Config Monitor + Webhook |
| Sẵn sàng production | Hạn chế | Cao |

## Xem Xét Production

### Trong Môi Trường Production

- Đội ngũ vận hành cấu hình **IP công khai hoặc domain name** thay vì localhost
- Không cần dịch vụ relay như Hookdeck
- Webhook trực tiếp từ GitHub đến endpoint công khai của Config Server

### Lợi Ích

- **Cập nhật cấu hình không downtime**
- **Lan truyền ngay lập tức** đến tất cả microservice instances
- **Không cần can thiệp thủ công**
- **Audit trail** qua GitHub commits và webhook delivery logs

## Các Bước Tiếp Theo

Sau khi thành thạo quản lý cấu hình:
1. **Dockerize microservices** - Chuyển ứng dụng thành Docker images
2. **Docker Compose deployment** - Điều phối tất cả services
3. **Production deployment** - Triển khai lên môi trường cloud

## Xử Lý Sự Cố

### Webhook Không Kích Hoạt
- Xác minh webhook delivery status trong GitHub Settings
- Kiểm tra console Hookdeck để xem relay logs
- Đảm bảo Config Server đang chạy trên port đúng

### Thuộc Tính Không Làm Mới
- Xác minh endpoint `/bus-refresh` đã được bật
- Kiểm tra kết nối RabbitMQ trong tất cả services
- Đảm bảo annotation `@RefreshScope` trên các configuration beans
- Xem lại logs của Config Server và microservices

### Vấn Đề Kết Nối RabbitMQ
- Xác minh RabbitMQ đang chạy: `docker ps`
- Kiểm tra thuộc tính connection trong tất cả services
- Đảm bảo firewall cho phép port 5672

## Kết Luận

Phương pháp tự động này loại bỏ các bước làm mới cấu hình thủ công, khiến kiến trúc microservices của bạn thực sự sẵn sàng cho production. Bằng cách kết hợp Spring Cloud Bus, Config Monitor và GitHub webhooks, bạn đạt được:

- **Tự động hóa** - Không cần gọi API thủ công
- **Độ tin cậy** - Cấu hình nhất quán trên tất cả instances
- **Khả năng kiểm toán** - Git commits đóng vai trò change logs
- **Khả năng mở rộng** - Hoạt động với số lượng microservice instances bất kỳ

Càng chịu trách nhiệm nhiều (chạy RabbitMQ, cấu hình webhooks), kiến trúc microservices của bạn càng mang lại nhiều quyền lực và tính linh hoạt.