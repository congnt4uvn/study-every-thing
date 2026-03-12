# Triển khai Config Server lên Kubernetes Cluster

## Tổng quan

Trong hướng dẫn này, chúng ta sẽ học cách triển khai microservice Config Server vào Kubernetes cluster cục bộ. Đây thường là microservice đầu tiên bạn nên triển khai khi thiết lập kiến trúc microservices trong Kubernetes, vì các dịch vụ khác phụ thuộc vào nó để quản lý cấu hình.

## Yêu cầu trước khi bắt đầu

- Kubernetes cluster cục bộ đang chạy thành công
- Các Docker image đã được build cho microservices (phần trước)
- Hiểu biết cơ bản về file cấu hình YAML

## Bắt đầu

### 1. Thiết lập cấu trúc dự án

Đầu tiên, tạo cấu trúc thư mục cần thiết cho các cấu hình Kubernetes:

```bash
# Di chuyển đến workspace của bạn
cd section_15

# Tạo thư mục Kubernetes
mkdir Kubernetes
cd Kubernetes
```

### 2. Tạo file Kubernetes Manifest

Tạo file YAML mới cho việc triển khai Config Server:

```bash
touch configserver.yaml
```

**Lưu ý:** Trên Windows, nếu lệnh `touch` không hoạt động, hãy tạo file thủ công trong thư mục của bạn.

## Hiểu về cấu hình Kubernetes

### Các khái niệm chính

- **Kubernetes Manifest Files**: Các file cấu hình cung cấp hướng dẫn cho Kubernetes về cách triển khai và expose microservices
- **Docker Compose vs Kubernetes**: Kubernetes không hiểu định dạng Docker Compose; nó yêu cầu cú pháp YAML riêng
- **Trách nhiệm DevOps**: Trong các dự án thực tế, đội ngũ DevOps hoặc platform thường viết các cấu hình này, nhưng developers nên hiểu cú pháp cơ bản

### Cấu trúc cấu hình

File Kubernetes manifest bao gồm hai phần chính:

1. **Deployment Configuration** - Định nghĩa cách triển khai microservice
2. **Service Configuration** - Định nghĩa cách expose microservice

## Cấu hình Deployment

### Cấu trúc cơ bản

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: configserver-deployment
  labels:
    app: configserver
spec:
  replicas: 1
  selector:
    matchLabels:
      app: configserver
  template:
    metadata:
      labels:
        app: configserver
    spec:
      containers:
      - name: configserver
        image: eazybytes/configserver:s14
        ports:
        - containerPort: 8071
```

### Phân tích cấu hình

#### API Version và Kind
- `apiVersion: apps/v1` - Phiên bản API bắt buộc cho các đối tượng Deployment
- `kind: Deployment` - Chỉ định đây là cấu hình Deployment (đối tượng Kubernetes được định nghĩa trước)

#### Metadata
- `name: configserver-deployment` - Tên duy nhất cho deployment
- `labels: app: configserver` - Nhãn để nhận diện và tổ chức tài nguyên

#### Specification (spec)

**Replicas**
- `replicas: 1` - Số lượng instance pod cần triển khai
- Tăng số này (ví dụ: 3) để triển khai nhiều instance cho tính khả dụng cao

**Selector**
- `matchLabels` - Kết nối các specification với deployment bằng cách khớp nhãn
- Phải khớp với các labels được định nghĩa trong metadata

**Template**
- Định nghĩa pod template để tạo containers
- Chứa các phần metadata và spec riêng

**Container Specifications**
- `name` - Tên container
- `image` - Docker image sử dụng (ví dụ: `eazybytes/configserver:s14`)
  - Registry mặc định là Docker Hub (docker.io)
  - Đối với các registry khác (AWS ECR, Azure ACR, v.v.), bao gồm URL registry đầy đủ
- `containerPort` - Cổng mà container sẽ lắng nghe (8071 cho Config Server)

**Multiple Containers**
- Để thêm helper/sidecar containers, thêm các mục danh sách bổ sung dưới `containers:`
- Mỗi container yêu cầu name, image và ports configuration riêng

## Cấu hình Service

### Cấu trúc cơ bản

```yaml
---
apiVersion: v1
kind: Service
metadata:
  name: configserver
spec:
  selector:
    app: configserver
  type: LoadBalancer
  ports:
    - protocol: TCP
      port: 8071
      targetPort: 8071
```

### Phân tích cấu hình

#### Separator (Dấu phân cách)
- `---` - Ba dấu gạch ngang phân tách nhiều cấu hình YAML trong một file
- Kubernetes coi mỗi phần như một cấu hình riêng biệt

#### API Version và Kind
- `apiVersion: v1` - Phiên bản API cho các đối tượng Service
- `kind: Service` - Chỉ định đây là cấu hình Service

#### Metadata
- `name: configserver` - Tên service (hoạt động như hostname trong cluster)
- **Quan trọng:** Tên này được các microservices khác sử dụng để giao tiếp với Config Server

#### Specification

**Selector**
- `app: configserver` - Liên kết service với các pods có nhãn khớp từ deployment

**Type**
- `LoadBalancer` - Expose service ra bên ngoài (external to Kubernetes cluster)
- Các loại khác: ClusterIP (chỉ internal), NodePort (external trên cổng node cụ thể)

**Ports**
- `protocol: TCP` - Giao thức giao tiếp (TCP cho web communication)
- `port: 8071` - Cổng được expose ra thế giới bên ngoài
- `targetPort: 8071` - Cổng mà container lắng nghe bên trong
- **Quan trọng:** `targetPort` phải khớp với `containerPort` trong cấu hình deployment

## Hệ thống khớp nhãn (Label Matching)

Nhãn rất quan trọng để kết nối các tài nguyên Kubernetes. Nhãn `app: configserver` phải nhất quán trong:

1. Deployment metadata labels (dòng 6)
2. Deployment selector matchLabels (dòng 11)
3. Template metadata labels (dòng 15)
4. Service selector (dòng 28)

Điều này đảm bảo Kubernetes ánh xạ đúng các services tới deployments và pods.

## Best Practices (Thực hành tốt nhất)

1. **Đặt tên duy nhất**: Sử dụng tên mô tả, duy nhất cho deployments và services
2. **Tính nhất quán của nhãn**: Đảm bảo nhãn khớp nhau trong các cấu hình deployment và service
3. **Tổ chức file đơn**: Sử dụng dấu phân cách `---` để giữ các cấu hình liên quan trong một file
4. **Đặt tên Service**: Tên service trở thành DNS entries; chọn cẩn thận cho giao tiếp giữa các services
5. **Quản lý Replica**: Bắt đầu với 1 replica và mở rộng dựa trên nhu cầu traffic

## Các bước tiếp theo

Với file Kubernetes manifest đã được tạo, bạn đã sẵn sàng để:
1. Triển khai Config Server lên Kubernetes cluster
2. Xác minh trạng thái triển khai
3. Test truy cập external tới Config Server
4. Triển khai các microservices bổ sung theo cùng một pattern

## Tóm tắt

Bạn đã học:
- Cách cấu trúc các file Kubernetes manifest cho việc triển khai microservice
- Sự khác biệt giữa cấu hình Deployment và Service
- Cách sử dụng nhãn để ánh xạ tài nguyên
- Cách expose services ra thế giới bên ngoài
- Tầm quan trọng của việc đặt tên nhất quán và cấu hình cổng

Nền tảng này sẽ giúp bạn triển khai tất cả các microservices trong kiến trúc của mình lên Kubernetes một cách hiệu quả.

## Tài nguyên bổ sung

- [Tài liệu chính thức Kubernetes - Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Tài liệu chính thức Kubernetes - Services](https://kubernetes.io/docs/concepts/services-networking/service/)