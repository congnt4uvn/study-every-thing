# Hướng Dẫn Tham Khảo Nhanh Các Lệnh Helm

## Tổng Quan

Hướng dẫn này cung cấp một cái nhìn tổng quan toàn diện về các lệnh Helm thiết yếu được sử dụng để quản lý ứng dụng Kubernetes thông qua Helm charts. Các lệnh này bao gồm toàn bộ vòng đời quản lý Helm chart, từ khởi tạo đến triển khai và bảo trì.

## Các Lệnh Helm Thiết Yếu

### 1. Lệnh Helm Create

Lệnh `helm create` tạo ra một Helm chart trống hoặc mặc định với tên được chỉ định.

```bash
helm create <tên-chart>
```

Khi bạn tạo một Helm chart bằng lệnh này, thư mục chart sẽ chứa:
- `Chart.yaml` - Thông tin metadata của chart
- `values.yaml` - Các giá trị cấu hình mặc định
- Thư mục `charts/` - Dành cho các chart phụ thuộc
- Thư mục `templates/` - Các template manifest Kubernetes

### 2. Lệnh Helm Dependencies Build

Lệnh này xây dựng một Helm chart cụ thể và biên dịch tất cả các phụ thuộc được định nghĩa trong chart.

```bash
helm dependencies build
```

Tất cả các chart phụ thuộc sẽ được sao chép vào thư mục `charts/` trong quá trình này.

### 3. Lệnh Helm Install

Lệnh install triển khai Helm chart của bạn lên Kubernetes cluster.

```bash
helm install <tên-release> <thư-mục-chart>
```

Khi thực thi, Helm sẽ cài đặt tất cả các hướng dẫn triển khai từ chart của bạn và các chart phụ thuộc vào Kubernetes cluster.

### 4. Lệnh Helm Upgrade

Sử dụng lệnh này để triển khai các thay đổi mới sau khi cập nhật Helm chart của bạn.

```bash
helm upgrade <tên-release> <thư-mục-chart>
```

Đầu tiên, cập nhật và biên dịch lại Helm chart của bạn, sau đó chạy lệnh upgrade để áp dụng các thay đổi.

### 5. Lệnh Helm History

Xem lịch sử cài đặt của các Helm release để hiểu các phiên bản trước đó.

```bash
helm history <tên-release>
```

Điều này giúp bạn xác định phiên bản nào bạn muốn rollback nếu cần.

### 6. Lệnh Helm Rollback

Quay lại phiên bản hoạt động trước đó hoặc revision cụ thể.

```bash
helm rollback <tên-release> <số-revision>
```

Nếu bạn không chỉ định số revision, Helm sẽ rollback về revision ngay trước đó.

### 7. Lệnh Helm Uninstall

Gỡ bỏ hoàn toàn tất cả microservices khỏi Kubernetes cluster của bạn.

```bash
helm uninstall <tên-release>
```

Lệnh này xóa release được chỉ định và tất cả các tài nguyên liên quan.

### 8. Lệnh Helm Template

Render tất cả các file manifest Kubernetes mà Helm sẽ sử dụng trong quá trình cài đặt.

```bash
helm template <thư-mục-chart>
```

Điều này hữu ích cho việc debug bằng cách xem trước những gì sẽ được triển khai mà không thực sự cài đặt.

### 9. Lệnh Helm List

Liệt kê tất cả các release được quản lý bởi Helm trong cluster của bạn.

```bash
helm ls
```

Lệnh này cung cấp tổng quan về tất cả các Helm release hiện đang được triển khai.

## Tham Khảo GitHub Repository

Tất cả các file và chart Helm được thảo luận trong hướng dẫn này đều có sẵn trong GitHub repository dưới **Section 16** trong thư mục `helm/`. Bạn có thể sử dụng các chart này để thực hành các lệnh Helm trên hệ thống local hoặc trong bất kỳ môi trường cloud nào.

## Triển Khai Cloud

Trong các phần tiếp theo, những Helm chart này sẽ được triển khai lên môi trường cloud. Quy trình triển khai sẽ rất giống với triển khai local, với điểm khác biệt chính là dung lượng tăng lên của các Kubernetes cluster trên cloud.

## Kết Luận

Hướng dẫn này bao gồm tất cả các lệnh Helm thiết yếu để quản lý triển khai Kubernetes. Những lệnh này tạo thành nền tảng của quản lý Helm chart, từ khởi tạo ban đầu qua triển khai, cập nhật và bảo trì. Hãy giữ tài liệu tham khảo này bên cạnh khi làm việc với Helm để nhanh chóng ôn lại kiến thức của bạn.

## Tài Nguyên Bổ Sung

- Thực hành với các Helm chart được cung cấp trong GitHub repository
- Thử nghiệm với cả môi trường Kubernetes local và cloud
- Xem lại hướng dẫn này bất cứ khi nào bạn cần làm mới kiến thức về Helm

---

*Hướng dẫn này cung cấp cái nhìn tổng quan toàn diện về các lệnh Helm cho việc quản lý ứng dụng Kubernetes hiệu quả.*