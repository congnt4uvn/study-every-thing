# Nâng Cấp và Khôi Phục Microservices với Helm

## Tổng Quan

Khi quản lý các microservices được triển khai bằng Helm charts trong Kubernetes, bạn sẽ thường xuyên cần triển khai các thay đổi mới hoặc cập nhật deployments. Hướng dẫn này trình bày cách nâng cấp và khôi phục microservices bằng các lệnh Helm, tương tự như chức năng rollout và rollback của `kubectl`.

## Các Trường Hợp Sử Dụng Phổ Biến

- **Mở rộng ứng dụng**: Tăng hoặc giảm số lượng replica (ví dụ: từ 1 lên 2 hoặc từ 2 lên 5)
- **Triển khai Docker images mới**: Cập nhật lên phiên bản mới hơn của microservices
- **Thay đổi cấu hình**: Điều chỉnh các thiết lập ứng dụng và giá trị theo môi trường

## Yêu Cầu Trước Khi Bắt Đầu

- Helm charts đã được cài đặt trong Kubernetes cluster
- Quyền truy cập vào cấu trúc thư mục helm chart
- Biết tên release và các chart dependencies

## Nâng Cấp Microservices với Helm

### Bước 1: Di Chuyển Đến Thư Mục Helm Chart

```bash
cd helm/environments/prod-env
```

### Bước 2: Thực Hiện Thay Đổi Values

Chỉnh sửa file `values.yaml` cho microservice cụ thể. Ví dụ, để thay đổi image tag của Gateway Server:

```yaml
# gateway-server/values.yaml
image:
  tag: s11  # Đã thay đổi từ s14 sang s11
```

### Bước 3: Build Lại Chart Dependencies

Nếu environment chart của bạn có dependencies với các microservice charts riêng lẻ, hãy build lại chúng:

```bash
cd prod-env
helm dependency build
```

### Bước 4: Thực Thi Lệnh Helm Upgrade

Di chuyển trở lại thư mục cha và chạy lệnh upgrade:

```bash
cd ..
helm upgrade easybank prod-env
```

**Điểm quan trọng:**
- `easybank` là tên release
- `prod-env` là tên helm chart
- Helm tự động nhận diện các thay đổi và chỉ triển khai những gì cần thiết
- Mỗi lần upgrade sẽ tăng số revision (ví dụ: revision 2, 3, v.v.)

## Giám Sát Quá Trình Nâng Cấp

### Kiểm Tra Kubernetes Dashboard

1. Truy cập vào phần Pods
2. Tìm kiếm pods có tên microservice của bạn (ví dụ: gateway-server)
3. Kiểm tra tuổi của pod để xác định pods mới được tạo
4. Xem logs để xác nhận khởi động thành công

### Xác Minh Triển Khai

Sau khi ứng dụng khởi động thành công, hãy kiểm tra các API của bạn để xác nhận các thay đổi hoạt động như mong đợi. Ví dụ:

```bash
# Kiểm tra một endpoint không cần xác thực (nếu đã loại bỏ security)
POST http://gateway-server/api/accounts
```

## Xử Lý Các Vấn Đề Thường Gặp

### Sai Image Tag

**Vấn đề**: Triển khai sai tag của Docker image (ví dụ: s12 thay vì s11)

**Giải pháp**: 
1. Sửa lại tag trong `values.yaml`
2. Build lại dependencies: `helm dependency build`
3. Chạy lại upgrade: `helm upgrade easybank prod-env`
4. Số revision sẽ tăng (ví dụ: lên revision 3)

## Các Phương Pháp Hay Nhất

### 1. **Quản Lý Số Lượng Replica**

Bạn có thể dễ dàng scale microservices bằng cách cập nhật replica count:

```yaml
replicaCount: 3  # Đã thay đổi từ 1 lên 3
```

### 2. **Cân Nhắc Tài Nguyên**

Lưu ý về tài nguyên hệ thống khi scaling:
- Giám sát CPU và memory usage
- Cân nhắc khả năng hạ tầng trước khi tăng replicas
- Kiểm tra ở các môi trường thấp hơn trước

### 3. **Quản Lý Phiên Bản**

- Luôn theo dõi các thay đổi trong files `values.yaml`
- Sử dụng Git để duy trì lịch sử phiên bản
- Ghi chép lý do cho mỗi lần upgrade

## Khôi Phục với Helm

Trong khi hướng dẫn này tập trung vào nâng cấp, Helm cũng cung cấp khả năng rollback. Nếu việc nâng cấp gây ra vấn đề, bạn có thể rollback về revision trước đó bằng cách sử dụng:

```bash
helm rollback easybank <revision-number>
```

## Quy Trình Ví Dụ

```bash
# 1. Di chuyển đến thư mục chart
cd helm/environments/prod-env

# 2. Chỉnh sửa values
vi gateway-server/values.yaml

# 3. Build lại dependencies
helm dependency build

# 4. Quay lại thư mục cha
cd ..

# 5. Nâng cấp release
helm upgrade easybank prod-env

# 6. Xác minh deployment
kubectl get pods
kubectl logs <gateway-server-pod-name>
```

## Tóm Tắt

Chức năng upgrade của Helm cung cấp một cách mạnh mẽ để quản lý các deployments microservices:
- **Triển khai thông minh**: Chỉ các tài nguyên thay đổi mới được cập nhật
- **Theo dõi revision**: Mỗi lần upgrade được phiên bản hóa để dễ dàng rollback
- **Quản lý dependencies**: Tự động xử lý các chart dependencies
- **Giảm thiểu downtime**: Rolling updates đảm bảo tính khả dụng của dịch vụ

Bằng cách làm theo các bước này, bạn có thể tự tin quản lý và cập nhật microservices của mình trong môi trường Kubernetes bằng Helm charts.