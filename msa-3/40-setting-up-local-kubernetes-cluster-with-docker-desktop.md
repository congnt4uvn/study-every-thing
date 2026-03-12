# Thiết Lập Kubernetes Cluster Cục Bộ với Docker Desktop

## Tổng Quan

Trong hướng dẫn này, chúng ta sẽ tìm hiểu cách thiết lập một Kubernetes cluster cục bộ sử dụng Docker Desktop. Cách tiếp cận này cung cấp môi trường Kubernetes giống production mà không cần đối mặt với độ phức tạp và chi phí của việc triển khai trên cloud trong giai đoạn học tập.

## Tại Sao Chọn Docker Desktop Thay Vì Minikube?

Mặc dù Minikube là lựa chọn phổ biến cho Kubernetes cluster cục bộ, chúng tôi khuyến nghị sử dụng Docker Desktop vì các lý do sau:

- **Tính Nhất Quán Của Lệnh**: Kubernetes trên Docker Desktop sử dụng các lệnh giống như Kubernetes cluster trong môi trường production
- **Không Có Sự Khác Biệt Về Kiến Thức**: Minikube có các lệnh đặc biệt khác với môi trường production
- **Tích Hợp Liền Mạch**: Nếu bạn đã cài đặt Docker Desktop, việc bật Kubernetes rất đơn giản

## Yêu Cầu Trước Khi Bắt Đầu

- Docker Desktop đã được cài đặt trên hệ thống của bạn
- Hiểu biết cơ bản về các khái niệm Kubernetes

## Các Bước Cài Đặt

### 1. Bật Kubernetes trong Docker Desktop

Làm theo các bước sau để bật Kubernetes:

1. Mở Docker Dashboard
2. Nhấp vào **Settings** (góc trên bên phải)
3. Chọn **Kubernetes** từ thanh bên trái
4. Đánh dấu vào **Enable Kubernetes**
5. **KHÔNG** đánh dấu vào "Show system containers" (trừ khi bạn cần xem các container nội bộ của Kubernetes)
6. Nhấp **Apply and Restart**

Docker Desktop sẽ khởi động lại và tạo một Kubernetes cluster cục bộ. Quá trình này có thể mất vài phút.

**Tài Liệu Tham Khảo**: https://docs.docker.com/desktop/kubernetes

### 2. Hiểu Về Cấu Hình Cluster Cục Bộ

Kubernetes cluster cục bộ được tạo bởi Docker Desktop có các đặc điểm sau:

- **Single Node Cluster**: Do hạn chế về tài nguyên hệ thống cục bộ (bộ nhớ và CPU), cluster chỉ bao gồm một node
- **Vai Trò Kết Hợp**: Node duy nhất này đóng vai trò cả master node và worker node
- **Container Ẩn**: Các container hệ thống của Kubernetes được ẩn khỏi các lệnh Docker như `docker ps` theo mặc định
- **Chỉ Báo Trạng Thái**: Khi Kubernetes đang chạy, bạn sẽ thấy chỉ báo trạng thái ở cuối Docker Desktop hiển thị "Kubernetes is running"

### 3. Xác Minh Cài Đặt Kubernetes

Sau khi cài đặt, bạn sẽ thấy hai chỉ báo trạng thái ở góc dưới bên trái của Docker Desktop:
- Docker engine đang chạy
- Kubernetes đang chạy

Bạn cũng sẽ thấy một phần **Kubernetes** mới trong menu Docker Desktop.

## Thiết Lập kubectl

`kubectl` là công cụ dòng lệnh được sử dụng để tương tác với các Kubernetes cluster. Docker Desktop tự động cài đặt kubectl trong quá trình thiết lập Kubernetes.

### Xác Minh Cài Đặt kubectl

Binary kubectl được cài đặt tại:
- **Mac**: Đường dẫn chuẩn do Docker Desktop thiết lập
- **Windows**: Đường dẫn chuẩn do Docker Desktop thiết lập

Đảm bảo vị trí này được thêm vào biến môi trường PATH của bạn (tương tự như JAVA_HOME và MAVEN_HOME).

### Kiểm Tra Các Lệnh kubectl

Chạy các lệnh sau để xác minh cài đặt của bạn:

#### 1. Lấy Danh Sách Contexts

```bash
kubectl config get-contexts
```

Lệnh này liệt kê tất cả các context Kubernetes có sẵn. Bạn sẽ thấy `docker-desktop` là context mặc định (được đánh dấu bằng dấu sao `*` trong cột CURRENT).

**Context**: Một môi trường cô lập cho phép ứng dụng client hoặc CLI của bạn tương tác với Kubernetes cluster.

#### 2. Lấy Danh Sách Clusters

```bash
kubectl config get-clusters
```

Lệnh này hiển thị tất cả các Kubernetes cluster đang chạy trên hệ thống cục bộ của bạn. Bạn sẽ thấy `docker-desktop` được liệt kê.

#### 3. Đặt Context Mặc Định (nếu cần)

Nếu bạn có nhiều context (ví dụ từ Minikube hoặc các cách cài đặt Kubernetes khác), hãy đặt Docker Desktop làm mặc định:

```bash
kubectl config use-context docker-desktop
```

**Lưu Ý**: Lệnh này chỉ cần thiết nếu bạn có nhiều context. Nếu docker-desktop đã được đánh dấu là current, bước này là tùy chọn.

#### 4. Xác Minh Nodes

```bash
kubectl get nodes
```

Lệnh này xác nhận số lượng node trong cluster của bạn. Bạn sẽ thấy một node được liệt kê, vì thiết lập cục bộ là single-node cluster.

**Ví Dụ Output**:
```
NAME             STATUS   ROLE           AGE   VERSION
docker-desktop   Ready    control-plane  5m    v1.x.x
```

## So Sánh Production vs Local Cluster

| Tính Năng | Local Cluster (Docker Desktop) | Production Cluster (Cloud) |
|-----------|-------------------------------|----------------------------|
| Số Lượng Nodes | 1 (kết hợp master + worker) | Nhiều (ví dụ: 1 master + 3 workers) |
| Sử Dụng Tài Nguyên | Giới hạn bởi hệ thống cục bộ | Có thể mở rộng theo yêu cầu |
| Chi Phí | Miễn phí | Trả theo sử dụng |
| Trường Hợp Sử Dụng | Phát triển, kiểm thử, học tập | Triển khai production |

## Xử Lý Sự Cố

Nếu các lệnh kubectl không hoạt động:

1. Xác minh kubectl đã được cài đặt: Kiểm tra xem binary kubectl có tồn tại trong đường dẫn cài đặt không
2. Cập nhật biến PATH: Đảm bảo thư mục cài đặt kubectl nằm trong PATH của hệ thống
3. Khởi động lại terminal: Đóng và mở lại terminal sau khi thay đổi PATH
4. Xác minh Docker Desktop: Đảm bảo Docker Desktop đang chạy và Kubernetes đã được bật

## Tắt Kubernetes

Nếu bạn cần tắt Kubernetes cluster:

1. Mở Docker Desktop Settings
2. Vào phần Kubernetes
3. Bỏ đánh dấu **Enable Kubernetes**
4. Nhấp **Apply and Restart**

## Bước Tiếp Theo

Bây giờ bạn đã có Kubernetes cluster cục bộ, bạn có thể:

- Khám phá các khái niệm Kubernetes một cách thực hành
- Triển khai microservices lên cluster
- Kiểm thử cấu hình trước khi chuyển sang môi trường cloud
- Học các lệnh kubectl trong môi trường an toàn

Sau khi đã quen thuộc với các khái niệm Kubernetes ở local, bạn có thể tiến hành tạo một Kubernetes cluster production-ready trong môi trường cloud với nhiều node.

## Tóm Tắt

Thiết lập Kubernetes cluster cục bộ với Docker Desktop cung cấp:
- Môi trường giống production để học tập
- Cách hiệu quả về chi phí để khám phá Kubernetes
- Quy trình thiết lập dễ dàng nếu Docker Desktop đã được cài đặt
- Cú pháp lệnh nhất quán với các cluster production

Thiết lập cục bộ này lý tưởng để hiểu các khái niệm Kubernetes trước khi triển khai lên môi trường cloud nơi thời gian chạy cluster sẽ phát sinh chi phí.

---

**Từ Khóa**: Kubernetes, Docker Desktop, kubectl, Local Cluster, Microservices, Container Orchestration, Môi Trường Phát Triển