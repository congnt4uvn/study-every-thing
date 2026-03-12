# Thiết Lập Discovery Server trong Kubernetes với Spring Cloud Kubernetes

## Tổng Quan

Hướng dẫn này giải thích cách thiết lập service discovery và load balancing phía server trong Kubernetes cluster sử dụng Spring Cloud Kubernetes. Mặc định, Kubernetes không bao gồm server để service discovery và registration, vì vậy chúng ta cần tự cấu hình.

## Yêu Cầu Trước

- Kubernetes cluster (local hoặc cloud)
- Hiểu biết cơ bản về Spring Boot và microservices
- Quen thuộc với các khái niệm Kubernetes (pods, services, deployments)

## Giới Thiệu về Spring Cloud Kubernetes

Spring Cloud Kubernetes là một dự án Spring Cloud giúp triển khai service discovery và load balancing trong môi trường Kubernetes. Khác với các triển khai truyền thống có thể sử dụng Eureka Server, Kubernetes yêu cầu một phương pháp tiếp cận chuyên biệt.

## Bắt Đầu

### Tài Liệu Chính Thức

Nhóm Spring Cloud Kubernetes đã xuất bản một blog vào năm 2021 giới thiệu các khả năng service discovery và registration. Blog này cung cấp một file Kubernetes manifest làm nền tảng để thiết lập Discovery Server.

### Cấu Trúc Dự Án

Tạo cấu trúc thư mục như sau:
```
section_17/
  └── Kubernetes/
      └── kubernetes-discoveryserver.yaml
```

## Cấu Hình Kubernetes Manifest

### Tạo File Manifest

Tạo file có tên `kubernetes-discoveryserver.yaml` với cấu trúc sau:

### 1. API Version và Kind

```yaml
apiVersion: v1
kind: List
```

`kind: List` cho phép bạn tạo nhiều đối tượng Kubernetes trong phần `items`.

### 2. Cấu Hình Service

```yaml
- apiVersion: v1
  kind: Service
  metadata:
    labels:
      app: spring-cloud-kubernetes-discoveryserver
    name: spring-cloud-kubernetes-discoveryserver
  spec:
    ports:
    - port: 80
      targetPort: 8761
    type: ClusterIP
```

**Điểm Chính:**
- **Port 80**: Cổng bên ngoài được expose cho các microservices khác
- **TargetPort 8761**: Cổng nội bộ nơi Discovery Server chạy
- **Service Type**: ClusterIP (không xung đột với Keycloak service trên port 80)

### 3. Service Account

```yaml
- apiVersion: v1
  kind: ServiceAccount
  metadata:
    name: spring-cloud-kubernetes-discoveryserver
```

Service account này sẽ được deployment Discovery Server sử dụng.

### 4. Role Binding

```yaml
- apiVersion: rbac.authorization.k8s.io/v1
  kind: RoleBinding
  metadata:
    name: spring-cloud-kubernetes-discoveryserver:view
  roleRef:
    kind: Role
    name: namespace-reader
  subjects:
  - kind: ServiceAccount
    name: spring-cloud-kubernetes-discoveryserver
```

Điều này liên kết role `namespace-reader` với service account.

### 5. Cấu Hình Role

```yaml
- apiVersion: rbac.authorization.k8s.io/v1
  kind: Role
  metadata:
    name: namespace-reader
  rules:
  - apiGroups: [""]
    resources:
    - services
    - endpoints
    - pods
    verbs:
    - get
    - list
    - watch
```

**Cập Nhật Quan Trọng:** Blog gốc từ 2021 chỉ bao gồm `services` và `endpoints`, nhưng dựa trên yêu cầu hiện tại, bạn phải thêm `pods` vào danh sách resources để Discovery Server hoạt động đúng cách.

### 6. Cấu Hình Deployment

```yaml
- apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: spring-cloud-kubernetes-discoveryserver-deployment
  spec:
    selector:
      matchLabels:
        app: spring-cloud-kubernetes-discoveryserver
    template:
      metadata:
        labels:
          app: spring-cloud-kubernetes-discoveryserver
      spec:
        serviceAccountName: spring-cloud-kubernetes-discoveryserver
        containers:
        - name: spring-cloud-kubernetes-discoveryserver
          image: springcloud/spring-cloud-kubernetes-discoveryserver:3.0.4
          imagePullPolicy: IfNotPresent
```

**Cập Nhật Chính:**
- **Image Tag**: Sử dụng `3.0.4` thay vì phiên bản cũ `2.1.0-M3`
- **Image Pull Policy**: `IfNotPresent` - chỉ pull image nếu không có sẵn trong local

### 7. Cấu Hình Health Probes

#### Readiness Probe

```yaml
          readinessProbe:
            httpGet:
              path: /actuator/health/readiness
              port: 8761
            initialDelaySeconds: 100
            periodSeconds: 30
```

#### Liveness Probe

```yaml
          livenessProbe:
            httpGet:
              path: /actuator/health/liveness
              port: 8761
            initialDelaySeconds: 100
            periodSeconds: 30
```

**Tham Số Cấu Hình Quan Trọng:**

- **initialDelaySeconds: 100**: Kubernetes đợi 100 giây trước khi thực hiện health check đầu tiên. Điều này ngăn việc restart sớm trong quá trình khởi động ứng dụng.
- **periodSeconds: 30**: Sau lần check đầu tiên, Kubernetes thực hiện health check mỗi 30 giây.

**Tại Sao Các Giá Trị Này Quan Trọng:**

Nếu không có các cấu hình này, Kubernetes sử dụng giá trị mặc định (thường là 10-15 giây), có thể gây ra:
- Các lần restart sớm
- Vòng lặp restart liên tục
- Triển khai thất bại

Nếu 100 giây không đủ cho môi trường của bạn, tăng lên 150 hoặc 200 giây.

### 8. Cấu Hình Port

```yaml
          ports:
          - containerPort: 8761
```

## Hiểu về Health Probes

### Readiness Probe
- Xác định khi nào pod sẵn sàng nhận traffic
- Sử dụng endpoint: `/actuator/health/readiness`
- Nếu thất bại, Kubernetes ngừng định tuyến traffic đến pod

### Liveness Probe
- Xác định ứng dụng có đang chạy đúng cách không
- Sử dụng endpoint: `/actuator/health/liveness`
- Nếu thất bại, Kubernetes restart pod

## Ưu Điểm của Kubernetes so với Docker Compose

Mặc dù chúng ta định nghĩa health probes cho Discovery Server, nó không thực sự cần thiết cho tất cả microservices trong Kubernetes bởi vì:

1. **Tự Động Restart**: Kubernetes tự động restart các pod bị lỗi
2. **Quản Lý Replica**: Kubernetes duy trì số lượng replica mong muốn
3. **Tự Phục Hồi**: Kubernetes liên tục giám sát và phục hồi cluster

Trong môi trường Docker Compose, containers không tự động restart, làm cho health checks trở nên quan trọng hơn.

## Chi Tiết Docker Image

Nhóm Spring Cloud Kubernetes cung cấp Docker image đã được build sẵn:
- **Image**: `springcloud/spring-cloud-kubernetes-discoveryserver`
- **Tag Khuyến Nghị**: `3.0.4` (phiên bản ổn định)
- **Docker Hub**: Có sẵn tại Docker Hub để kiểm tra phiên bản

Bạn không cần build ứng dụng Discovery Server của riêng mình - chỉ cần sử dụng image được cung cấp.

## Các Bước Triển Khai

1. Tạo file `kubernetes-discoveryserver.yaml` với tất cả cấu hình
2. Apply manifest:
   ```bash
   kubectl apply -f kubernetes-discoveryserver.yaml
   ```
3. Xác minh deployment:
   ```bash
   kubectl get pods
   kubectl get services
   ```

## Xử Lý Sự Cố

### Pod Liên Tục Restart
- Tăng `initialDelaySeconds` lên 150 hoặc 200
- Kiểm tra logs của pod: `kubectl logs <pod-name>`

### Service Không Truy Cập Được
- Xác minh service type là ClusterIP
- Kiểm tra ánh xạ port (80 → 8761)

### Vấn Đề Role Binding
- Đảm bảo resource `pods` được bao gồm trong Role
- Xác minh service account binding

## Best Practices (Thực Hành Tốt Nhất)

1. **Luôn sử dụng stable image tags** thay vì phiên bản development
2. **Cấu hình thời gian health probe phù hợp** dựa trên thời gian khởi động ứng dụng
3. **Sử dụng ClusterIP cho internal services** để tránh xung đột port
4. **Bao gồm pods trong Role resources** cho các phiên bản Kubernetes hiện tại
5. **Giám sát trạng thái pod** sau khi deploy để đảm bảo khởi động thành công

## Kết Luận

Thiết lập Discovery Server trong Kubernetes sử dụng Spring Cloud Kubernetes khá đơn giản với cấu hình phù hợp. Điều quan trọng là đảm bảo:
- Quyền role đúng (bao gồm pods)
- Thời gian health probe phù hợp
- Phiên bản Docker image ổn định mới nhất

Trong các bước tiếp theo, bạn sẽ apply manifest file này vào Kubernetes cluster và xác minh Discovery Server đang chạy đúng cách.

## Tài Nguyên Bổ Sung

- [Tài Liệu Spring Cloud Kubernetes](https://spring.io/projects/spring-cloud-kubernetes)
- [Tài Liệu Chính Thức Kubernetes](https://kubernetes.io/docs/)
- [Spring Boot Actuator Health Endpoints](https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html)