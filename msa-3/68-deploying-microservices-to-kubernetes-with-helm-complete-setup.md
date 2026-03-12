# Triển khai Microservices lên Kubernetes với Helm - Thiết lập Hoàn chỉnh

## Tổng quan

Hướng dẫn này trình bày cách triển khai một kiến trúc microservices hoàn chỉnh lên Kubernetes cluster sử dụng Helm charts. Chúng ta sẽ triển khai nhiều microservices Spring Boot cùng với các thành phần hỗ trợ bao gồm Kafka, Grafana, Prometheus, Loki và Tempo.

## Yêu cầu Tiên quyết

- Kubernetes cluster đang chạy (local hoặc cloud)
- Helm đã được cài đặt
- Docker Desktop với Kubernetes được kích hoạt (cho thiết lập local)
- Tối thiểu 12GB RAM được phân bổ cho Docker/Kubernetes
- Helm charts theo môi trường đã được chuẩn bị (dev, prod, qa)

## Kiến trúc Triển khai

Hệ sinh thái microservices bao gồm:
- **Config Server** - Quản lý cấu hình tập trung
- **Eureka Server** - Service discovery (khám phá dịch vụ)
- **Gateway Server** - API Gateway với bảo mật OAuth2
- **Accounts Microservice** - Dịch vụ quản lý tài khoản
- **Cards Microservice** - Dịch vụ quản lý thẻ
- **Loans Microservice** - Dịch vụ quản lý khoản vay
- **Messages Microservice** - Dịch vụ nhắn tin theo sự kiện
- **Kafka** - Nền tảng streaming sự kiện
- **Grafana** - Giám sát và trực quan hóa
- **Prometheus** - Thu thập metrics
- **Loki** - Tổng hợp log
- **Tempo** - Distributed tracing (truy vết phân tán)
- **Keycloak** - Quản lý danh tính và truy cập

## Quy trình Triển khai

### Bước 1: Di chuyển đến Thư mục Environment

Đảm bảo bạn đang ở trong thư mục `environments` chứa ba charts:
- `dev-env` - Môi trường Development
- `qa-env` - Môi trường QA
- `prod-env` - Môi trường Production

### Bước 2: Triển khai sử dụng Helm

Để triển khai lên môi trường production, thực thi:

```bash
helm install easybank prod-env
```

**Giải thích lệnh:**
- `helm install` - Lệnh cài đặt Helm
- `easybank` - Tên release
- `prod-env` - Tên chart cho profile production

### Bước 3: Giám sát Triển khai

Sau khi thực thi lệnh, bạn sẽ nhận được xác nhận rằng việc triển khai đã được khởi động hoặc hoàn thành.

## Hiểu về Hành vi Khởi động Pod

### Thách thức Khởi động Ban đầu

Khi tất cả microservices khởi động đồng thời, chúng có thể thất bại ban đầu do:
- Config Server chưa sẵn sàng
- Eureka Server chưa sẵn sàng
- Các phụ thuộc giữa các service chưa sẵn sàng

### Tự động Phục hồi của Kubernetes

Kubernetes tự động xử lý lỗi pod:
- **Khởi động lại Tự động** - Pods được khởi động lại cho đến khi thành công hoặc đạt số lần thử tối đa
- **Exponential Backoff** - Độ trễ khởi động lại tăng dần (2s, 4s, 5s, v.v.)
- **Self-Healing** - Cluster tự động duy trì trạng thái mong muốn

## Xác minh Khởi động Microservices

### Truy cập Kubernetes Dashboard

Điều hướng đến Kubernetes dashboard để giám sát trạng thái pod và logs.

### Xác minh Từng bước

#### 1. Config Server (Quan trọng - Khởi động Đầu tiên)

Config Server phải khởi động trước vì các service khác phụ thuộc vào nó.

**Kiểm tra logs:**
- Click vào Config Server pod
- Chọn "View Logs"
- Bật "Auto refresh every 5 seconds"
- Đợi thông báo: "Config server started successfully"

**Lưu ý:** Trên hệ thống có tài nguyên hạn chế (16GB RAM với 12GB phân bổ cho Docker), quá trình khởi động có thể mất 5-10 phút.

#### 2. Eureka Server

Eureka Server phụ thuộc vào Config Server.

**Hành vi mong đợi:**
- Có thể hiển thị nhiều lần thử khởi động lại ban đầu
- Bộ đếm khởi động lại sẽ tăng cho đến khi Config Server sẵn sàng
- Tìm kiếm: "Started Eureka Server application in X seconds"

#### 3. Accounts Microservice

**Hành vi mong đợi:**
- Phụ thuộc vào cả Config Server và Eureka Server
- Sẽ khởi động lại cho đến khi các phụ thuộc sẵn sàng
- Nên kết nối thành công với Eureka Server khi đã khởi động

#### 4. Cards Microservice

**Xác minh:**
- Kiểm tra logs để xác nhận khởi động thành công
- Xác minh kết nối Eureka Server

#### 5. Loans Microservice

**Xác minh:**
- Kiểm tra logs để xác nhận khởi động thành công
- Xác minh kết nối Eureka Server

#### 6. Gateway Server

**Xác minh:**
- Tìm kiếm: "Gateway server application started successfully"
- Quan trọng cho việc định tuyến API và bảo mật

#### 7. Messages Microservice

**Hành vi mong đợi:**
- Không phụ thuộc vào Config Server hoặc Eureka Server
- Nên có số lần khởi động lại bằng không
- Xác minh kết nối Kafka broker

## Kiểm thử Microservices đã Triển khai

### 1. Kiểm thử Accounts Service

**Kiểm thử Configuration API:**
```bash
GET /contact-info
```

**Kết quả mong đợi:**
- Trả về properties từ production profile
- Xác nhận ứng dụng khởi động với profile đúng

### 2. Kiểm thử Cards Service

**Kiểm thử Java Version API:**
```bash
GET /api/java-version
```

### 3. Kiểm thử Loans Service

**Kiểm thử Build Info API:**
```bash
GET /api/build-info
```

### 4. Kiểm thử Tạo Account với OAuth2

**Lấy Access Token:**
```bash
POST /oauth2/token
- Bao gồm client secret
- Sử dụng Keycloak URL với port 80
```

**Tạo Account Mới:**
```bash
POST /api/accounts
Authorization: Bearer {access_token}
```

**Phản hồi mong đợi:** 201 Created - Account được tạo thành công

### 5. Kiểm thử Tạo Cards

**Các bước:**
1. Cập nhật client secret trong request
2. Cập nhật Keycloak port thành 80 trong access token URL
3. Lấy access token
4. Gọi Cards API với access token

### 6. Kiểm thử Tạo Loans

**Các bước:**
1. Cập nhật client secret trong request
2. Cập nhật port thành 80 trong access token URL
3. Lấy access token
4. Tạo loan mới cho số điện thoại đã cho

### 7. Kiểm thử Thông tin Khách hàng Tổng hợp

**Lấy Thông tin Khách hàng Hoàn chỉnh:**
```bash
GET /api/fetchCustomerDetails?mobileNumber={number}
Authorization: Bearer {access_token}
```

**Phản hồi mong đợi:**
- Thông tin accounts đầy đủ
- Thông tin loans
- Thông tin cards

**Lưu ý:** Có thể gặp timeout ở lần thử đầu tiên với tài nguyên hạn chế. Thử lại nếu cần.

## Thiết lập Giám sát và Quan sát

### Cấu hình Grafana

**Truy cập Grafana:**
- Được expose trên port 3000
- Sử dụng port forwarding: `kubectl port-forward svc/grafana 3000:3000`

### 1. Loki - Tổng hợp Log

**Xem Logs:**
1. Điều hướng đến "Explore" trong Grafana
2. Chọn "Loki" làm data source
3. Chọn label: "container"
4. Chọn tên container: "gateway-server"
5. Chạy query để xem tất cả Gateway Server logs

**Tích hợp Distributed Tracing:**
- Click vào bất kỳ log entry nào
- Truy cập link đến Tempo cho trace ID
- Xem chi tiết distributed tracing đầy đủ

### 2. Tempo - Distributed Tracing

**Tính năng:**
- Trực quan hóa trace hoàn chỉnh
- Luồng request qua các microservices
- Xác định điểm nghẽn hiệu suất
- Tích hợp với Loki để tương quan log-to-trace

### 3. Prometheus - Thu thập Metrics

**Xem Metrics:**
1. Điều hướng đến "Explore"
2. Chọn "Prometheus" làm data source
3. Tìm kiếm metric: "up"
4. Chọn label: "container"
5. Chạy query

**Trực quan hóa:**
- Xem biểu đồ cho 15 phút cuối
- Thay đổi kiểu biểu đồ thành "stacked lines"
- Giám sát uptime cho tất cả containers

**Phân tích Metric:**
- Metrics uptime cho containers đang chạy
- Chỉ số sức khỏe dịch vụ
- Xu hướng sử dụng tài nguyên

## Cân nhắc về Hiệu suất

### Môi trường Development Local

**Yêu cầu Hệ thống:**
- Tối thiểu 16GB RAM
- 12GB phân bổ cho Docker Desktop/Kubernetes
- Khuyến nghị SSD để có hiệu suất tốt hơn

**Hành vi Mong đợi:**
- Thời gian khởi động: 5-10 phút
- Nhiều lần khởi động lại pod trong quá trình initialization
- CPU sử dụng cao trong khi khởi động
- Trạng thái nhất quán cuối cùng khi tất cả services đang chạy

### Mẹo Tối ưu hóa Tài nguyên

1. Khởi động services theo thứ tự phụ thuộc khi có thể
2. Giám sát sử dụng tài nguyên qua Kubernetes dashboard
3. Điều chỉnh giới hạn tài nguyên trong Helm values
4. Sử dụng readiness và liveness probes
5. Triển khai retry logic phù hợp trong microservices

## Khắc phục Sự cố

### Vấn đề Thường gặp

**Pods Liên tục Khởi động lại:**
- Kiểm tra Config Server logs trước
- Xác minh kết nối Eureka Server
- Đảm bảo cấu hình profile đúng

**Lỗi Timeout:**
- Bình thường trong môi trường hạn chế tài nguyên
- Thử lại các request thất bại
- Cân nhắc tăng giá trị timeout

**Vấn đề Truy cập Port:**
- Xác minh port forwarding đang hoạt động
- Kiểm tra cấu hình service exposure
- Đảm bảo không có xung đột port

## Kết luận

Triển khai thành công một hệ sinh thái microservices hoàn chỉnh lên Kubernetes bao gồm:

✅ Helm charts theo môi trường (dev, qa, prod)  
✅ Sắp xếp khởi động và quản lý phụ thuộc phù hợp  
✅ Cơ chế tự động phục hồi của Kubernetes  
✅ Giám sát toàn diện với Grafana, Prometheus, Loki, Tempo  
✅ Truy cập bảo mật với tích hợp OAuth2/Keycloak  
✅ Event streaming với Kafka  
✅ Distributed tracing và tổng hợp log  

### Thành tựu Đã mở khóa

Bạn đã học thành công cách:
- Triển khai kiến trúc microservices phức tạp sử dụng Helm
- Quản lý cấu hình multi-environment
- Triển khai observability toàn diện
- Tích hợp bảo mật với Keycloak
- Thiết lập kiến trúc event-driven với Kafka
- Khắc phục sự cố triển khai Kubernetes

### Bước tiếp theo

Trong các phần sắp tới, chúng ta sẽ khám phá:
- Thiết lập môi trường trong hạ tầng cloud phù hợp
- Chiến lược triển khai production-grade
- Tính năng Kubernetes nâng cao
- Best practices cloud-native

## Điểm Chính Cần nhớ

1. **Helm đơn giản hóa triển khai** - Một lệnh duy nhất triển khai toàn bộ hệ sinh thái
2. **Kubernetes tự phục hồi** - Khởi động lại và phục hồi tự động
3. **Observability rất quan trọng** - Logs, metrics và traces là thiết yếu
4. **Tích hợp bảo mật** - OAuth2 với Keycloak cung cấp xác thực mạnh mẽ
5. **Kiến trúc Event-driven** - Kafka cho phép giao tiếp async có khả năng mở rộng
6. **Kiểm thử local khả thi** - Thiết lập giống production hoàn chỉnh trên máy local

---

**Chúc mừng!** Bây giờ bạn là một trong số ít các developer hiểu được quy trình hoàn chỉnh của việc triển khai và quản lý microservices trong Kubernetes với cơ sở hạ tầng hỗ trợ cấp doanh nghiệp.