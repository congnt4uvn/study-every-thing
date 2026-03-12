# Kubernetes Self-Healing và Quản Lý Replica

## Tổng Quan

Hướng dẫn này trình bày khả năng tự phục hồi (self-healing) của Kubernetes và cách quản lý replica cho các microservices được triển khai trong Kubernetes cluster. Chúng ta sẽ khám phá cách Kubernetes tự động duy trì trạng thái mong muốn của containers bằng cách tạo lại chúng khi bị lỗi hoặc bị xóa.

## Yêu Cầu Tiên Quyết

- Tất cả microservices đã được triển khai lên Kubernetes cluster
- Đã cài đặt và cấu hình kubectl CLI tool
- Hiểu biết cơ bản về Kubernetes deployments và pods

## Hiểu về Kubernetes Self-Healing

Kubernetes cung cấp khả năng tự phục hồi mà Docker hoặc Docker Compose truyền thống không thể đạt được. Khi Kubernetes phát hiện một container không hoạt động đúng cách hoặc đã hoàn toàn dừng lại, nó sẽ tự động tạo lại một container mới để thay thế container bị lỗi.

Khả năng này đảm bảo tính khả dụng cao và độ tin cậy cho microservices của bạn mà không cần can thiệp thủ công.

## Kiểm Tra Replica Sets

### Xem Replica Sets Hiện Tại

Đầu tiên, hãy kiểm tra các replica sets hiện tại cho tất cả deployments:

```bash
kubectl get replicaset
```

Lệnh này hiển thị:
- **Desired state**: Số lượng replicas được chỉ định trong deployment của bạn
- **Current state**: Số lượng replicas hiện đang chạy
- **Ready**: Số lượng containers sẵn sàng phục vụ các ứng dụng client

Bạn sẽ thấy replica sets cho tất cả deployments:
- accounts
- cards
- config-server
- eureka-server
- gateway-server
- keycloak
- loans

### Xem Các Pods Đang Chạy

Để xem tất cả các pods đang chạy:

```bash
kubectl get pods
```

Ban đầu, bạn sẽ thấy một pod duy nhất cho mỗi deployment vì số lượng replica được đặt là 1.

## Mở Rộng Replicas

### Cập Nhật Số Lượng Replica

Hãy tăng số lượng replicas cho accounts microservice:

1. Mở file deployment `accounts.yaml`
2. Thay đổi giá trị `replicas` từ `1` thành `2`
3. Lưu file

### Áp Dụng Các Thay Đổi

```bash
kubectl apply -f 5_accounts.yaml
```

Kubernetes thông minh phát hiện các thay đổi và cập nhật deployment tương ứng.

### Xác Minh Việc Mở Rộng

Kiểm tra lại replica set:

```bash
kubectl get replicaset
```

Đối với accounts deployment, bạn sẽ thấy:
- Desired: 2
- Current: 2
- Ready: 2

Xác nhận bằng:

```bash
kubectl get pods
```

Bạn sẽ thấy hai pods cho accounts microservice:
- Pod gốc (được tạo trước đó)
- Pod mới (vừa được tạo để khớp với trạng thái mong muốn)

## Thực Hành Self-Healing

### Xóa Pod Thủ Công

Để minh họa khả năng tự phục hồi, hãy xóa thủ công một trong các pods của accounts microservice:

```bash
kubectl delete pod <tên-pod>
```

Thay thế `<tên-pod>` bằng tên thực tế của một trong các pods accounts của bạn.

### Quan Sát Khôi Phục Tự Động

Ngay lập tức kiểm tra replica set:

```bash
kubectl get replicaset
```

Giá trị current nên vẫn là 2 vì Kubernetes đã đang làm việc để khôi phục trạng thái mong muốn.

Kiểm tra các pods:

```bash
kubectl get pods
```

Bạn sẽ nhận thấy:
- Pod bị xóa đã biến mất
- Một pod mới đã được tự động tạo ra (tuổi: vài giây)
- Trạng thái mong muốn khớp với trạng thái hiện tại

### Xem Các Sự Kiện Kubernetes

Để xem những gì đã xảy ra đằng sau hậu trường:

```bash
kubectl get events --sort-by=.metadata.creationTimestamp
```

Lệnh này hiển thị tất cả các sự kiện được sắp xếp theo thời gian tạo. Bạn sẽ thấy:
1. **Killing event**: Khi bạn xóa pod thủ công
2. **Create event**: Khi Kubernetes tự động tạo pod thay thế

Ví dụ về các thông báo đầu ra:
- "Killing pod..."
- "Successfully created pod..."
- "Created pod accounts-deployment-..."

## Những Điểm Chính

1. **Self-Healing**: Kubernetes liên tục giám sát các containers và tự động thay thế những containers không khỏe mạnh hoặc bị tắt
2. **Quản Lý Trạng Thái Mong Muốn**: Kubernetes luôn làm việc để khớp trạng thái hiện tại với trạng thái mong muốn được định nghĩa trong các deployment files
3. **Tính Khả Dụng Cao**: Việc khôi phục tự động này đảm bảo microservices của bạn vẫn khả dụng mà không cần can thiệp thủ công
4. **Vượt Trội hơn Docker Compose**: Những khả năng này không có sẵn trong Docker độc lập hoặc Docker Compose, làm cho Kubernetes trở nên thiết yếu cho môi trường production

## Thực Tiễn Tốt Nhất

- Định nghĩa số lượng replica phù hợp dựa trên yêu cầu tải của ứng dụng
- Giám sát các sự kiện Kubernetes thường xuyên để hiểu hành vi của cluster
- Sử dụng health checks và readiness probes để giúp Kubernetes đưa ra quyết định có căn cứ
- Test khả năng tự phục hồi trong môi trường non-production trước

## Kết Luận

Khả năng tự phục hồi của Kubernetes là một trong những tính năng mạnh mẽ nhất để chạy microservices trong môi trường production. Bằng cách tự động duy trì trạng thái mong muốn, Kubernetes đảm bảo tính khả dụng cao và giảm gánh nặng vận hành cho các nhóm phát triển. Các nền tảng điều phối container như Kubernetes là thiết yếu để quản lý các kiến trúc microservice phức tạp ở quy mô lớn.

---

*Hướng dẫn này là một phần của loạt bài toàn diện về microservices bao gồm Spring Boot, Kubernetes và kiến trúc cloud-native.*