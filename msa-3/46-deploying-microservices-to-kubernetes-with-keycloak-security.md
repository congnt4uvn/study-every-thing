# Triển khai Microservices lên Kubernetes với Bảo mật Keycloak

## Tổng quan

Hướng dẫn này bao gồm quy trình đầy đủ để triển khai các microservices Spring Boot lên Kubernetes cluster với bảo mật OAuth2 sử dụng Keycloak làm máy chủ xác thực. Bạn sẽ học cách triển khai nhiều microservices theo đúng thứ tự, cấu hình bảo mật và kiểm tra toàn bộ hệ thống.

## Yêu cầu trước khi bắt đầu

- Kubernetes cluster đã được thiết lập (Docker Desktop hoặc tương tự)
- kubectl CLI đã được cấu hình
- Các file Kubernetes manifest đã chuẩn bị sẵn
- Hiểu biết cơ bản về kiến trúc microservices

## Kiến trúc Triển khai

Triển khai bao gồm các thành phần sau:
- **Keycloak** - Máy chủ xác thực
- **Config Server** - Quản lý cấu hình tập trung
- **Eureka Server** - Service discovery (phát hiện dịch vụ)
- **Gateway Server** - API gateway với bảo mật OAuth2
- **Business Microservices** - Các dịch vụ Accounts, Loans và Cards

## Quy trình Triển khai từng bước

### 1. Triển khai Keycloak Authorization Server

Bắt đầu bằng cách triển khai dịch vụ Keycloak:

```bash
kubectl apply -f 1_keycloak.yaml
```

Lệnh này tạo dịch vụ Keycloak để xử lý xác thực và phân quyền cho tất cả microservices.

### 2. Triển khai ConfigMaps

Áp dụng các configuration maps:

```bash
kubectl apply -f 2_configmaps.yaml
```

**Lưu ý quan trọng**: Kubernetes đủ thông minh để phát hiện nếu không có thay đổi nào. Nếu bạn áp dụng cùng một cấu hình lần nữa, nó sẽ trả về trạng thái "unchanged" (không thay đổi), cho biết không cần thực hiện hành động nào. Đây là một trong những tính năng mạnh mẽ của cách tiếp cận declarative của Kubernetes.

### 3. Triển khai Config Server

Triển khai Config Server với image đã cập nhật:

```bash
kubectl apply -f 3_configserver.yaml
```

**Thay đổi chính**: Phiên bản image đã được cập nhật từ S14 sang S12. Khi bạn thực thi lệnh này:
- **Deployment** sẽ được cấu hình lại với image mới
- **Service** giữ nguyên không đổi (không phát hiện thay đổi)

**Xác minh**: 
- Truy cập Kubernetes dashboard
- Điều hướng đến namespace mặc định
- Kiểm tra pods và xem logs của Config Server
- Đảm bảo bạn thấy thông báo "Successfully started Config Server"

⚠️ **Quan trọng**: Luôn đợi Config Server triển khai hoàn tất thành công trước khi tiếp tục bước tiếp theo.

### 4. Triển khai Eureka Server

Sau khi Config Server đang chạy:

```bash
kubectl apply -f 4_eurekaserver.yaml
```

**Xác minh**:
- Kiểm tra trạng thái pod trong Kubernetes dashboard
- Xem logs để xác nhận "Eureka Server successfully started"
- Đợi khởi động hoàn toàn trước khi tiếp tục

### 5. Triển khai các Business Microservices

Triển khai ba business microservices:

```bash
kubectl apply -f 5_accounts.yaml
kubectl apply -f 6_loans.yaml
kubectl apply -f 7_cards.yaml
```

**Quản lý Dependencies quan trọng**:
- Không giống Docker Compose, Kubernetes không có chức năng `depends_on` tích hợp sẵn
- Bạn phải đảm bảo thủ công các dịch vụ phụ thuộc đã khởi động hoàn toàn trước khi triển khai các dịch vụ phụ thuộc vào chúng
- Đợi cả ba microservices (Accounts, Loans, Cards) khởi động hoàn toàn trước khi triển khai Gateway

**Tại sao điều này quan trọng**:
- Nếu dependencies chưa sẵn sàng, containers sẽ khởi động lại nhiều lần
- Cuối cùng, deployment sẽ thành công, nhưng gây ra khởi động lại không cần thiết
- Trong môi trường production, các đội DevOps sử dụng công cụ orchestration nâng cao để quản lý thứ tự triển khai

**Xác minh**:
- Truy cập Eureka dashboard
- Xác nhận cả ba microservices đã được đăng ký
- Kiểm tra trạng thái đăng ký trước khi tiếp tục

### 6. Triển khai Gateway Server

Cuối cùng, triển khai API Gateway:

```bash
kubectl apply -f 8_gatewayserver.yaml
```

**Xác minh**:
- Làm mới Eureka dashboard
- Xác nhận Gateway Server đã đăng ký thành công

## Cấu hình Bảo mật Keycloak

### Truy cập Keycloak Admin Console

1. Điều hướng đến `http://localhost:7080`
2. Click "Administration Console"
3. Thông tin đăng nhập:
   - Username: `admin`
   - Password: `admin`

### Tạo Client Application

1. Vào phần **Clients**
2. Click **Create Client**
3. Cấu hình client:
   - **Client ID**: `easybank-callcenter-cc`
   - Click **Next**
4. Bật **Client Authentication**
5. Tắt **Standard Flow** và **Direct Access Grants**
6. Bật **Service Account Roles**
7. Click **Next** → **Next** → **Save**
8. Sao chép **Client Secret** từ tab Credentials (cần cho việc test API)

### Tạo Client Roles

Tạo ba roles cho client:

1. Điều hướng đến **Roles** (cho client của bạn)
2. Click **Create Role**
3. Tạo các roles sau:
   - `accounts`
   - `cards`
   - `loans`

### Gán Roles cho Client

1. Quay lại **Clients** → Chọn `easybank-callcenter-cc`
2. Click **Service Account Roles**
3. Click **Assign Role**
4. Chọn cả ba roles (accounts, cards, loans)
5. Click **Assign**

## Kiểm tra Triển khai

### Thiết lập Postman

Đối với tất cả các API requests, bạn cần lấy access token sử dụng OAuth2 Client Credentials flow.

**Cấu hình Token**:
- Grant Type: Client Credentials
- Access Token URL: `http://localhost:7080/realms/master/protocol/openid-connect/token`
- Client ID: `easybank-callcenter-cc`
- Client Secret: [Secret bạn đã sao chép]

### Test 1: Tạo Account

**Endpoint**: `POST /api/accounts`
**Số điện thoại**: `688`

1. Click **Get New Access Token**
2. Sử dụng token trong request
3. Click **Send**
4. Kết quả mong đợi: "Account details successfully created"

### Test 2: Tạo Cards

**Endpoint**: `POST /api/cards`
**Số điện thoại**: `688`

1. Cập nhật client secret trong request (giống như trên)
2. Lấy access token mới
3. Click **Send**
4. Kết quả mong đợi: "Cards details created successfully"

### Test 3: Tạo Loans

**Endpoint**: `POST /api/loans`
**Số điện thoại**: `688`

1. Cập nhật client secret trong request
2. Lấy access token mới
3. Click **Send**
4. Kết quả mong đợi: "Loans details created successfully"

### Test 4: Lấy Customer Details

**Endpoint**: `GET /api/accounts/fetchCustomerDetails?mobileNumber=688`

Đây là thao tác GET để lấy thông tin khách hàng đầy đủ bao gồm accounts, loans và cards.

1. Không cần xác thực cho GET (nếu được cấu hình)
2. Cập nhật số điện thoại thành `688`
3. Click **Send**
4. Kết quả mong đợi: Thông tin khách hàng đầy đủ với accounts, loans và cards

**Xử lý sự cố**:
- Nếu nhận được "Customer not found" → Xác minh số điện thoại khớp với số bạn đã sử dụng khi tạo
- Nếu nhận được "Unauthorized" → Lấy access token mới
- Đảm bảo tất cả các thao tác tạo đã sử dụng cùng một số điện thoại

## Hiểu về Kubernetes Manifest Files

### Định nghĩa ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: [configmap-name]
data:
  key1: value1
  key2: value2
```

ConfigMaps lưu trữ dữ liệu cấu hình dưới dạng các cặp key-value có thể được sử dụng bởi pods.

### Định nghĩa Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: [deployment-name]
  labels:
    app: [app-name]
spec:
  replicas: 1
  selector:
    matchLabels:
      app: [app-name]
  template:
    metadata:
      labels:
        app: [app-name]
    spec:
      containers:
      - name: [container-name]
        image: [image:tag]
        ports:
        - containerPort: [port]
```

**Các thành phần chính**:
- **replicas**: Số lượng pod instances
- **selector**: Khớp với pods để quản lý
- **template**: Đặc tả pod bao gồm chi tiết container

### Định nghĩa Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: [service-name]
spec:
  selector:
    app: [app-name]
  type: ClusterIP
  ports:
  - protocol: TCP
    port: [external-port]
    targetPort: [container-port]
```

**Các loại Service**:
- **ClusterIP**: Chỉ truy cập nội bộ cluster (mặc định)
- **LoadBalancer**: Truy cập từ bên ngoài với load balancing
- **NodePort**: Expose service trên IP của mỗi node

### Liên kết Deployments và Services

Kết nối giữa Deployment và Service được thiết lập thông qua **labels**:

```yaml
# Trong Deployment metadata
labels:
  app: accounts

# Trong Service selector
selector:
  app: accounts
```

Cả hai phải sử dụng cùng giá trị label để thiết lập liên kết. Service định tuyến traffic đến các pods khớp với selector labels.

## Những điểm quan trọng cần nhớ

1. **Kubernetes Intelligence**: Kubernetes phát hiện thay đổi cấu hình và chỉ áp dụng những gì khác biệt
2. **Thứ tự Triển khai quan trọng**: Đảm bảo dependencies đã khởi động hoàn toàn trước khi triển khai các dịch vụ phụ thuộc
3. **Không có Dependencies tự động**: Không giống Docker Compose, Kubernetes không có quản lý dependency tích hợp sẵn
4. **Thực hành Production**: Các đội DevOps sử dụng công cụ nâng cao cho triển khai tự động, có thứ tự
5. **Label Binding**: Services tìm pods thông qua label selectors khớp
6. **Service Types**: Chọn ClusterIP cho dịch vụ nội bộ, LoadBalancer cho expose ra ngoài

## Tiếp theo là gì?

Triển khai này minh họa các khái niệm cơ bản về chạy microservices trong Kubernetes. Tuy nhiên, Kubernetes cung cấp nhiều tính năng mạnh mẽ hơn:
- Auto-scaling dựa trên tải
- Khả năng tự phục hồi (self-healing)
- Rolling updates và rollbacks
- Networking và ingress nâng cao
- Quản lý ConfigMap và Secret
- Resource limits và quotas

Những chủ đề nâng cao này sẽ được đề cập trong các bài giảng sắp tới, nơi bạn sẽ khám phá sức mạnh và "phép màu" thực sự của Kubernetes.

## Trách nhiệm của Developer vs. DevOps

**Là một Developer**:
- Hiểu các manifest files được cung cấp bởi đội DevOps
- Debug các vấn đề production trong mạng microservice
- Biết các khái niệm và lệnh Kubernetes cơ bản

**Bạn không cần**:
- Thành thạo viết các Kubernetes manifests phức tạp từ đầu
- Xử lý orchestration triển khai nâng cao
- Quản lý các Kubernetes clusters production

Tập trung vào việc xây dựng các microservices tuyệt vời, và làm việc cộng tác với đội DevOps của bạn cho các chiến lược triển khai.

## Kết luận

Bạn đã triển khai thành công một kiến trúc microservices hoàn chỉnh lên Kubernetes với bảo mật OAuth2 sử dụng Keycloak. Hệ thống bao gồm service discovery, cấu hình tập trung, API gateway, và nhiều business services - tất cả đều được bảo mật và giao tiếp trong Kubernetes cluster.

Nền tảng này chuẩn bị cho bạn khám phá các tính năng Kubernetes nâng cao hơn trong các bài giảng tiếp theo!