# Triển Khai và Xác Thực Microservices trên Kubernetes Cloud

## Tổng Quan

Hướng dẫn này bao gồm việc triển khai và xác thực các microservices Spring Boot trong cụm Kubernetes trên Google Cloud Platform (GCP), bao gồm Gateway Server, xác thực Keycloak và kiểm thử REST APIs với Postman.

## Yêu Cầu Trước Khi Bắt Đầu

- Tài khoản Google Cloud Platform với cụm Kubernetes đã được tạo
- kubectl CLI đã được cấu hình
- Postman để kiểm thử API
- Helm charts đã chuẩn bị cho microservices
- Hiểu biết cơ bản về các khái niệm Kubernetes

## Chờ Đợi Quá Trình Triển Khai Hoàn Tất

Sau khi triển khai ứng dụng lên Kubernetes:

**Quan trọng:** Hãy đợi ít nhất **10 phút** để tất cả các cài đặt hoàn thành. Mặc dù một số triển khai có thể hoàn tất trong vòng 5 phút, nhưng nên đợi đủ 10 phút trước khi cho rằng có vấn đề xảy ra.

## Xác Thực Triển Khai Kubernetes

### 1. Kiểm Tra Các Node trong Cluster

1. Điều hướng đến cụm Kubernetes của bạn trong GCP Console
2. Vào phần **Nodes** để xem tất cả các node trong cluster (thường là 3 nodes)
3. Click vào bất kỳ node nào để xem các pod đang chạy trong node đó
4. Thay đổi "rows per page" thành 30 hoặc 50 để xem tất cả pods cùng lúc

### 2. Xác Minh Trạng Thái Pod

Tìm kiếm các dấu hiệu triển khai thành công:
- **Dấu tick màu xanh** bên cạnh tất cả các pods
- Trạng thái Running cho tất cả containers
- Các thành phần chính có thể thấy:
  - Pods liên quan đến Prometheus
  - Pods liên quan đến Loki
  - Pods liên quan đến Kafka
  - Pod Gateway Server
  - Pods Microservice (accounts, cards, loans)

### 3. Định Vị Pod Gateway Server

#### Sử Dụng Lệnh kubectl

```bash
# Lấy danh sách tất cả pods
kubectl get pods

# Tìm pod Gateway Server (tìm pod có tên bắt đầu bằng "gateway-server")
# Copy tên đầy đủ của pod

# Mô tả pod để lấy thông tin chi tiết
kubectl describe pod <gateway-server-pod-name>
```

Kết quả lệnh `describe` hiển thị:
- Node nơi pod được cài đặt
- Container images được sử dụng
- Events và thông tin trạng thái

#### Sử Dụng GCP Console

1. Điều hướng đến **Workloads** để xem tất cả deployments
2. Vào **Services and Ingress** để xem tất cả services
3. Tìm kiếm pod "gateway-server"
4. Click vào pod để xem:
   - Trạng thái container
   - Log events
   - Logs của container

## Hiểu Về Các Thành Phần Kubernetes

### Workloads (Deployments)

Xem tất cả các deployments tạo ra replicas, pods và containers trong cụm Kubernetes của bạn.

### Services

- **Cluster IP**: Hầu hết các microservices chỉ được expose nội bộ
- **LoadBalancer**: Gateway Server và Keycloak được expose ra bên ngoài
  - Tự động tạo địa chỉ IP công khai
  - Có thể được map đến tên miền bởi Kubernetes admins

### ConfigMaps và Secrets

Xác minh rằng tất cả configuration maps và secrets đã được tạo thành công trong phần **Config and Storage**.

## Cấu Hình Xác Thực Keycloak

### 1. Truy Cập Keycloak Admin Console

1. Điều hướng đến **Services and Ingress**
2. Copy địa chỉ IP công khai của Keycloak service
3. Mở URL trong tab trình duyệt ẩn danh (incognito)
4. Click vào **Administration Console**
5. Đăng nhập với thông tin mặc định:
   - **Username**: `admin`
   - **Password**: `password`

### 2. Tạo OAuth2 Client

1. Vào phần **Clients**
2. Click **Create Client**
3. Nhập client ID: `easybank-callcenter-cc`
4. Click **Next**
5. Bật **Client Authentication**
6. Tắt tất cả các tùy chọn khác trừ **Service Account Roles**
7. Click **Next**, sau đó **Save**
8. Vào tab **Credentials**
9. Copy **Client Secret** để sử dụng trong Postman

### 3. Tạo Các Roles

Tạo các roles sau trong Keycloak:
1. `accounts`
2. `cards`
3. `loans`

**Các bước:**
1. Vào **Realm Roles**
2. Click **Create Role**
3. Nhập tên role
4. Save và lặp lại cho cả ba roles

### 4. Gán Roles cho Service Account

1. Vào **Clients** → `easybank-callcenter-cc`
2. Click tab **Service Account Roles**
3. Gán cả ba roles: `accounts`, `cards`, `loans`
4. Lưu role mapping

## Kiểm Thử APIs Microservices với Postman

### 1. Cấu Hình Postman OAuth2 Settings

Cập nhật những thông tin sau trong Postman:
- **Access Token URL**: Thay thế `localhost` bằng IP công khai của Keycloak
  - Định dạng: `http://<keycloak-public-ip>/realms/<realm-name>/protocol/openid-connect/token`
- **Client ID**: `easybank-callcenter-cc`
- **Client Secret**: (paste secret đã copy từ Keycloak)

### 2. Kiểm Thử GET APIs (Không Yêu Cầu Xác Thực)

Thay thế `localhost` bằng IP công khai của Gateway Server trong tất cả requests.

#### Thông Tin Liên Hệ Accounts
```
GET http://<gateway-public-ip>:8080/eazybank/accounts/api/contact-info
```

#### Thông Tin Liên Hệ Cards
```
GET http://<gateway-public-ip>:8080/eazybank/cards/api/contact-info
```

#### Thông Tin Liên Hệ Loans
```
GET http://<gateway-public-ip>:8080/eazybank/loans/api/contact-info
```

**Kết quả mong đợi**: Thành công với dữ liệu cấu hình

### 3. Kiểm Thử POST APIs (Với Xác Thực OAuth2)

#### Lấy Access Token
1. Trong Postman, vào tab **Authorization**
2. Chọn **OAuth 2.0**
3. Click **Get New Access Token**
4. Click **Proceed** và **Use Token**

#### Tạo Account
```
POST http://<gateway-public-ip>:8080/eazybank/accounts/api/create
```

**Kết quả mong đợi**: `201 Account created successfully`

#### Tạo Card
```
POST http://<gateway-public-ip>:8080/eazybank/cards/api/create
```

**Kết quả mong đợi**: `201 Card created successfully`

#### Tạo Loan
```
POST http://<gateway-public-ip>:8080/eazybank/loans/api/create
```

**Kết quả mong đợi**: `201 Loan created successfully`

### 4. Kiểm Thử Composite API

#### Lấy Thông Tin Chi Tiết Khách Hàng (Accounts + Cards + Loans)
```
GET http://<gateway-public-ip>:8080/eazybank/accounts/api/fetchCustomerDetails
```

**Kết quả mong đợi**: JSON với dữ liệu khách hàng kết hợp từ cả ba microservices

## Danh Sách Kiểm Tra Xác Thực

- ✅ Tất cả pods hiển thị dấu tick màu xanh
- ✅ Pod Gateway Server chạy thành công
- ✅ Keycloak có thể truy cập qua IP công khai
- ✅ OAuth2 client được tạo với cấu hình đúng
- ✅ Roles được tạo và gán
- ✅ GET APIs trả về responses thành công
- ✅ Access token được tạo thành công
- ✅ POST APIs tạo resources thành công
- ✅ Composite API trả về dữ liệu kết hợp

## Điểm Chính Cần Nhớ

1. **Kiên Nhẫn Với Triển Khai**: Luôn đợi 10 phút cho các triển khai Kubernetes
2. **Loại Service Quan Trọng**: LoadBalancer expose services ra ngoài với IP công khai
3. **Gateway Pattern**: Tất cả traffic đi qua Gateway Server
4. **Bảo Mật OAuth2**: Keycloak cung cấp xác thực tập trung
5. **Xác Thực Cloud**: Kiểm thử tất cả APIs với IP công khai, không phải localhost

## Các Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ xác thực các **thành phần Grafana** để giám sát và quan sát kiến trúc microservices.

## Xử Lý Sự Cố

### Pods Không Khởi Động
- Kiểm tra logs của pod: `kubectl logs <pod-name>`
- Mô tả pod để xem events: `kubectl describe pod <pod-name>`
- Xác minh resource quotas và limits

### Không Thể Truy Cập Services
- Xác minh LoadBalancer đã tạo IP công khai
- Kiểm tra firewall rules trong GCP
- Đảm bảo số port đúng

### Lỗi Xác Thực
- Xác minh client secret đúng
- Kiểm tra định dạng access token URL
- Đảm bảo roles được gán cho service account

## Kết Luận

Triển khai và xác thực microservices thành công trong môi trường Kubernetes trên cloud đòi hỏi sự chú ý cẩn thận đến thời gian, cấu hình đúng các thành phần bảo mật như Keycloak, và kiểm thử kỹ lưỡng tất cả các API endpoints. Thiết lập này minh họa một kiến trúc microservices sẵn sàng production với API Gateway, service discovery và bảo mật OAuth2.