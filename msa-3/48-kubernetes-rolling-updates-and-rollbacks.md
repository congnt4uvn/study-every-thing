# Kubernetes Rolling Updates và Rollbacks

## Tổng Quan

Hướng dẫn này trình bày cách triển khai các thay đổi mới vào Kubernetes cluster mà không gây gián đoạn dịch vụ, đồng thời cách rollback về phiên bản trước khi gặp sự cố. Chúng ta sẽ khám phá các chiến lược triển khai tích hợp sẵn của Kubernetes thông qua ví dụ về microservices Spring Boot.

## Yêu Cầu Trước

- Kubernetes cluster đang chạy
- Công cụ kubectl CLI đã được cấu hình
- Docker images đã được push lên registry
- Hiểu biết cơ bản về Kubernetes deployments

## Scaling Deployments (Mở Rộng Triển Khai)

### Phương Pháp 1: Sử Dụng Lệnh kubectl scale

Bạn có thể scale deployments trực tiếp từ dòng lệnh:

```bash
kubectl scale deployment accounts-deployment --replicas=1
```

Lệnh này scale `accounts-deployment` xuống còn 1 replica.

### Phương Pháp 2: Cập Nhật File YAML Manifest

Hoặc bạn có thể cập nhật trường `replicas` trong file Kubernetes manifest và apply các thay đổi:

```yaml
spec:
  replicas: 1
```

**Best Practice (Thực Hành Tốt Nhất):** Luôn cập nhật các file YAML manifest ngay cả khi sử dụng lệnh kubectl để đảm bảo tính nhất quán cho các lần triển khai sau.

### Kiểm Tra Deployments Đã Scale

Kiểm tra trạng thái pod hiện tại:

```bash
kubectl get pods
kubectl get replicaset
```

Output sẽ hiển thị số lượng replicas mong muốn và thực tế cho mỗi deployment.

## Rolling Updates (Cập Nhật Luân Chuyển)

### Hiểu Về Triển Khai Không Gián Đoạn

Kubernetes thực hiện rolling updates bằng cách:
1. Tạo pods mới với image đã cập nhật
2. Đợi pods mới sẵn sàng
3. Ngừng các pods cũ từng bước một
4. Không bao giờ kill tất cả instances cùng lúc

### Cập Nhật Container Images

#### Phương Pháp 1: Sử Dụng Lệnh kubectl set image

```bash
kubectl set image deployment/gatewayserver-deployment gatewayserver=eazybytes/gatewayserver:s11 --record
```

**Giải Thích Lệnh:**
- `deployment/gatewayserver-deployment` - Tên deployment đích
- `gatewayserver` - Tên container trong deployment
- `eazybytes/gatewayserver:s11` - Docker image mới với tag
- `--record` - Ghi lại lý do triển khai (đã deprecated nhưng vẫn hữu ích)

**Lưu Ý:** Flag `--record` đã bị deprecated và có thể bị loại bỏ trong các phiên bản Kubernetes tương lai. Nếu gặp lỗi, hãy xóa flag này.

#### Phương Pháp 2: Cập Nhật File YAML Manifest

Cập nhật image tag trong file deployment YAML và apply:

```yaml
spec:
  containers:
  - name: gatewayserver
    image: eazybytes/gatewayserver:s11
```

```bash
kubectl apply -f gateway.yaml
```

### Giám Sát Rolling Updates

Theo dõi quá trình triển khai:

```bash
kubectl get pods
```

Bạn sẽ quan sát thấy:
- Pods mới được tạo với trạng thái "ContainerCreating"
- Pods mới chuyển sang trạng thái "Running"
- Pods cũ chỉ bị terminate sau khi pods mới hoạt động ổn định

### Xử Lý Triển Khai Thất Bại

Nếu bạn chỉ định tag image không hợp lệ, Kubernetes sẽ:
1. Cố gắng pull image
2. Hiển thị trạng thái "ImagePullBackOff" hoặc "ErrImagePull"
3. **Giữ các pods hiện tại đang chạy** - Không có downtime!
4. Không terminate các pods đang hoạt động cho đến khi pods mới được tạo thành công

Ví dụ với image không hợp lệ:

```bash
kubectl set image deployment/gatewayserver-deployment gatewayserver=eazybytes/gatewayserver:s111
```

Kết quả: Các pods cũ tiếp tục phục vụ traffic trong khi pods mới không khởi động được.

### Xem Các Events Của Deployment

Kiểm tra events chi tiết để hiểu điều gì đã xảy ra:

```bash
kubectl get events
```

Events hiển thị:
- Các thao tác pull image
- Lên lịch pods
- Tạo containers
- Khởi động pods
- Terminate pods cũ

### Xác Minh Triển Khai

Kiểm tra phiên bản image hiện tại:

```bash
kubectl describe pod <pod-name>
```

Tìm trường `Image:` trong output để xác nhận phiên bản đã triển khai.

## Rollback Operations (Thao Tác Rollback)

### Xem Lịch Sử Rollout

Xem tất cả các revisions của deployment:

```bash
kubectl rollout history deployment/gatewayserver-deployment
```

Output hiển thị:
- Số revision
- Nguyên nhân thay đổi (nếu dùng --record)
- Cấu hình deployment

### Rollback Về Phiên Bản Trước

#### Rollback Về Revision Ngay Trước Đó

```bash
kubectl rollout undo deployment/gatewayserver-deployment
```

#### Rollback Về Revision Cụ Thể

```bash
kubectl rollout undo deployment/gatewayserver-deployment --to-revision=1
```

Lệnh này rollback về revision 1, khôi phục trạng thái hoạt động trước đó.

### Xác Minh Rollback

1. Kiểm tra trạng thái pod:
```bash
kubectl get pods
```

2. Xác minh phiên bản image:
```bash
kubectl describe pod <new-pod-name>
```

Image tag phải phản ánh revision trước đó.

## Hiểu Kiến Trúc Deployment Của Kubernetes

### Hệ Thống Phân Cấp Deployment

```
Deployment (Chỉ thị/Thông số kỹ thuật)
    ↓
ReplicaSet (Quản lý số lượng replicas mong muốn)
    ↓
Pods (Được tạo dựa trên số lượng replicas)
    ↓
Containers (Instances microservice thực tế)
```

**Biểu Diễn Trực Quan:**
- **Deployment**: Định nghĩa trạng thái mong muốn và thông số kỹ thuật
- **ReplicaSet**: Tạo và quản lý pods dựa trên số lượng replicas
- **Pods**: Lưu trữ các containers thực tế
- **Containers**: Chạy ứng dụng microservice

Nếu chỉ định `replicas: 2`, ReplicaSet sẽ tạo 2 pods, mỗi pod chứa container microservice.

## Auto-Scaling (Mở Rộng Tự Động - Nâng Cao)

Kubernetes hỗ trợ **Horizontal Pod Autoscaler (HPA)** cho việc scale tự động dựa trên:
- Sử dụng CPU
- Sử dụng Memory
- Custom metrics

Ví dụ cấu hình HPA:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: gatewayserver-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: gatewayserver-deployment
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 80
```

**Lưu Ý:** Auto-scaling thường được quản lý bởi Kubernetes administrators trong môi trường production. Để biết thông tin chi tiết, tham khảo [tài liệu chính thức của Kubernetes](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/).

## Best Practices (Thực Hành Tốt Nhất)

1. **Luôn test trong môi trường development** trước khi deploy lên production
2. **Giữ các file YAML manifests được cập nhật** để phản ánh trạng thái hiện tại
3. **Sử dụng image tags có ý nghĩa** (tránh `latest` trong production)
4. **Giám sát tiến trình rollout** với `kubectl get pods -w`
5. **Duy trì lịch sử rollout** để dễ dàng rollback
6. **Đặt resource limits phù hợp** để tránh vấn đề về memory/CPU
7. **Sử dụng health checks** (liveness và readiness probes)
8. **Ghi chép các thay đổi** trong deployment annotations

## Khắc Phục Sự Cố

### Các Vấn Đề Thường Gặp

1. **ImagePullBackOff**: Tên hoặc tag image không hợp lệ
   - Giải pháp: Xác minh image tồn tại trong registry

2. **CrashLoopBackOff**: Container khởi động nhưng ngay lập tức crash
   - Giải pháp: Kiểm tra logs ứng dụng với `kubectl logs <pod-name>`

3. **Insufficient Memory**: Pods không thể được scheduled
   - Giải pháp: Giảm số lượng replicas hoặc tăng tài nguyên node

4. **Pending Pods**: Không có tài nguyên khả dụng
   - Giải pháp: Scale cluster hoặc giảm resource requests

## Tóm Tắt

Kubernetes cung cấp các công cụ mạnh mẽ cho triển khai không gián đoạn:

- **Rolling Updates**: Triển khai thay đổi từng bước mà không làm gián đoạn dịch vụ
- **Rollbacks**: Nhanh chóng quay về phiên bản hoạt động trước đó
- **Scaling**: Điều chỉnh số lượng replicas một cách linh hoạt
- **Auto-scaling**: Tự động scale dựa trên nhu cầu (nâng cao)

Với những tính năng này, Kubernetes đảm bảo tính khả dụng cao và độ tin cậy cho kiến trúc microservices của bạn.

## Tài Liệu Tham Khảo

- [Kubernetes Official Documentation](https://kubernetes.io/docs/)
- [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Horizontal Pod Autoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)