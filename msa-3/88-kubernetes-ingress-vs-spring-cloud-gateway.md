# Kubernetes Ingress: Hiểu về Ingress và Vai trò của nó trong Kiến trúc Microservices

## Giới thiệu

Trong bài giảng này, chúng ta sẽ tìm hiểu sâu về Kubernetes Ingress và so sánh nó với các phương pháp khác để expose microservices ra bên ngoài.

## LoadBalancer Service Type vs Kubernetes Ingress

### LoadBalancer Service Type

Khi bạn sử dụng service type là LoadBalancer, bạn đang expose một microservice cụ thể ra bên ngoài Kubernetes cluster. Mỗi microservice với LoadBalancer service type sẽ có:

- Địa chỉ IP public riêng
- LoadBalancer riêng được cung cấp bởi cloud provider
- Cấu hình expose riêng cho từng service

**Ví dụ:** Nếu bạn có 5 microservices với LoadBalancer service type, bạn sẽ có 5 địa chỉ IP public khác nhau và 5 LoadBalancer riêng biệt.

### Nhu cầu về Một Điểm Truy cập Duy nhất

Đôi khi chúng ta cần một **điểm truy cập duy nhất** vào Kubernetes cluster có khả năng:
- Chuyển tiếp tất cả các request từ bên ngoài đến container hoặc microservice phù hợp
- Hoạt động như một gateway tập trung để quản lý traffic

## Kubernetes Ingress là gì?

**Kubernetes Ingress** expose các route HTTP và HTTPS từ bên ngoài cluster đến các services bên trong cluster. Nó hoạt động như một edge server trong kiến trúc microservices của bạn.

### Các Khả năng Chính của Ingress

1. **Traffic Routing** - Định tuyến traffic dựa trên các rules được định nghĩa trong Ingress resource
2. **Load Balancing** - Phân phối traffic giữa nhiều instances
3. **SSL/TLS Termination** - Xử lý các kết nối bảo mật
4. **Name-based Virtual Hosting** - Hỗ trợ nhiều domains
5. **Authentication & Authorization** - Có thể tích hợp với các sản phẩm OAuth2/OIDC như Keycloak hoặc Okta

## Spring Cloud Gateway vs Kubernetes Ingress

### Phương pháp Spring Cloud Gateway

**Spring Cloud Gateway** là phương pháp tập trung vào developer, trong đó:
- Developers xây dựng ứng dụng Spring Boot sử dụng dependencies của Spring Cloud Gateway
- Developers tự implement các cross-cutting concerns
- Cung cấp tính linh hoạt để viết custom business logic bằng Java
- Hiện đang hoạt động như edge server trong mạng microservice của chúng ta

### Phương pháp Kubernetes Ingress

**Kubernetes Ingress** là phương pháp tập trung vào infrastructure, trong đó:
- DevOps team cấu hình routing rules một cách declarative
- Các khả năng built-in xử lý các cross-cutting concerns phổ biến
- Được quản lý ở cấp độ Kubernetes cluster

### Khi nào nên Chọn từng Phương pháp?

#### Chọn Spring Cloud Gateway khi:
1. Bạn có các developers tài năng có khả năng xây dựng edge servers phức tạp
2. Bạn cần custom business logic mà Kubernetes Ingress không thể đáp ứng
3. Bạn cần tính linh hoạt của Java programming cho các kịch bản routing phức tạp

#### Chọn Kubernetes Ingress khi:
1. Bạn có các thành viên DevOps team có kinh nghiệm và hiểu sâu về Kubernetes
2. Các yêu cầu routing của bạn có thể được đáp ứng bằng declarative configurations
3. Bạn muốn tận dụng các khả năng native của Kubernetes

### Các Yếu tố Quyết định Chính

Sự lựa chọn phụ thuộc vào:
- **Cấu trúc Team** - Chuyên môn của developer vs DevOps
- **Sở thích của Tổ chức** - Bạn muốn đặt trách nhiệm ở đâu
- **Yêu cầu Business** - Độ phức tạp của routing logic cần thiết

> **Lưu ý:** Cả hai phương pháp đều đạt được cùng một mục tiêu. Quyết định phụ thuộc vào việc bạn muốn developers hay DevOps team members sở hữu trách nhiệm này.

## Hiểu về Ingress Resources

### Cấu hình Ingress Mẫu

```yaml
kind: Ingress
metadata:
  name: example-ingress
spec:
  rules:
    - host: example.com
      http:
        paths:
          - path: /accounts
            backend:
              service:
                name: account-service
                port:
                  number: 80
```

### Các Thành phần Cấu hình

- **kind: Ingress** - Chỉ ra đây là một Ingress resource
- **metadata.name** - Tên của Ingress resource
- **spec.rules** - Định nghĩa các routing rules
  - **host** - Hostname cơ sở của tổ chức bạn
  - **paths** - Các cấu hình routing dựa trên path
  - **backend.service** - Service đích bên trong cluster

> **Quan trọng:** Bạn không cần phải nhớ các cấu hình này. Đây chủ yếu là trách nhiệm của các thành viên DevOps team hoặc Kubernetes administrators.

## Ingress Controller

### Ingress Controller là gì?

**Ingress Controller** là một component có nhiệm vụ:
- Implement các routing rules được định nghĩa trong Ingress resources
- Theo dõi các Ingress resources và cấu hình các network components tương ứng
- Phải được cài đặt và cấu hình trong Kubernetes cluster của bạn

**Quan trọng:** Mặc định, Ingress resources không thể hoạt động nếu không có Ingress Controller.

### Các Ingress Controllers Phổ biến

1. **NGINX Ingress Controller** - Được sử dụng phổ biến nhất, open-source
2. **Traefik** - Reverse proxy và load balancer HTTP hiện đại
3. **HAProxy Ingress** - Load balancer hiệu suất cao

Kubernetes chính thức hỗ trợ hơn 30 Ingress Controllers khác nhau. Các tổ chức lựa chọn dựa trên yêu cầu cụ thể của họ.

> **Lưu ý:** NGINX Ingress Controller là lựa chọn phổ biến nhất vì nó là open-source và được maintain bởi NGINX team.

## Luồng Traffic với Kubernetes Ingress

### Tổng quan Kiến trúc

```
External Client (Client Bên ngoài)
    ↓
Ingress-Managed Load Balancer
    ↓
Ingress Controller (có thể có nhiều instances)
    ↓
Service (ClusterIP)
    ↓
Pod
    ↓
Container (Accounts/Loans/Cards)
```

### Luồng Chi tiết

1. **Triển khai Microservices**
   - Containers (accounts, loans, cards) chạy bên trong pods
   - Services được expose sử dụng ClusterIP (chỉ internal)
   - Không thể truy cập trực tiếp từ bên ngoài cluster

2. **Service Layer**
   - Mỗi microservice có một Service object tương ứng
   - Services chuyển tiếp requests đến các containers phù hợp
   - Ví dụ: Account Service → Account Container

3. **Ingress Layer**
   - External clients gửi requests đến Ingress-managed Load Balancer
   - Load Balancer chuyển tiếp đến một trong các Ingress Controller instances
   - Ingress Controller áp dụng các routing rules

4. **Ví dụ về Routing Rules**
   - `example.com/accounts` → Account Service → Account Container
   - `example.com/loans` → Loan Service → Loan Container
   - `example.com/cards` → Card Service → Card Container

### Load Balancing

Các tổ chức có thể triển khai nhiều Ingress Controller instances để đảm bảo high availability. Trong trường hợp này:
- Một Ingress-managed Load Balancer phân phối traffic giữa các Ingress Controller instances
- Mỗi controller có thể xử lý requests một cách độc lập

## So sánh với Spring Cloud Gateway

Cả hai phương pháp đều tương tự ở chỗ:
- Hoạt động như một edge server cho Kubernetes cluster
- Phục vụ như điểm truy cập cho external traffic
- Xử lý routing và quản lý traffic

Sự khác biệt chính là **ai quản lý và cấu hình** edge server:
- **Spring Cloud Gateway**: Được quản lý bởi developers
- **Kubernetes Ingress**: Được quản lý bởi DevOps/Infrastructure team

## Tóm tắt

- **Kubernetes Ingress** cung cấp một cách native của Kubernetes để expose services
- **Ingress Controller** là cần thiết để implement Ingress rules
- Lựa chọn giữa Spring Cloud Gateway và Kubernetes Ingress dựa trên:
  - Chuyên môn và cấu trúc team
  - Độ phức tạp của business logic
  - Sở thích của tổ chức
- Cả hai phương pháp đều hợp lệ và đạt được cùng một mục tiêu
- Có nhiều Ingress Controllers khác nhau để đáp ứng các yêu cầu khác nhau

## Các Bước Tiếp theo

Trong bài giảng tiếp theo, chúng ta sẽ khám phá thêm các chi tiết về cấu hình Kubernetes Ingress và triển khai thực tế.

---

*Tài liệu này được tạo dựa trên bài giảng kỹ thuật về Kubernetes Ingress và kiến trúc microservices với Spring Boot.*