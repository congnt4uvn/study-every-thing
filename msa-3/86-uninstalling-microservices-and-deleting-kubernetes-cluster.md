# Gỡ Cài Đặt Microservices và Xóa Kubernetes Cluster Trên Google Cloud

## Tổng Quan

Sau khi triển khai và xác thực thành công tất cả các microservices trong Google Cloud Kubernetes cluster, việc dọn dẹp tài nguyên một cách đúng đắn là rất quan trọng để tránh các khoản phí bất ngờ. Hướng dẫn này sẽ đi qua toàn bộ quy trình gỡ cài đặt tất cả các thành phần và xóa Kubernetes cluster.

## Yêu Cầu Trước Khi Bắt Đầu

- Tất cả microservices và các thành phần hỗ trợ đã được triển khai và xác thực
- Helm đã được cài đặt và cấu hình
- kubectl đã được cấu hình để truy cập Google Cloud Kubernetes cluster của bạn
- Có quyền truy cập vào Google Cloud Console

## Xác Thực Trước Khi Dọn Dẹp

Trước khi tiến hành gỡ cài đặt, hãy đảm bảo tất cả các thành phần đang hoạt động đúng:

1. **Trạng Thái Microservices**: Tất cả microservices và các thành phần hỗ trợ phải hoạt động như mong đợi
2. **Kịch Bản Event-Driven**: Kiểm tra logs của accounts và message microservices để xác thực các kịch bản event-driven dựa trên Kafka
3. **Tình Trạng Tổng Thể**: Xác minh rằng toàn bộ hệ thống đang hoạt động bình thường

## Gỡ Cài Đặt Các Thành Phần Với Helm

Quy trình gỡ cài đặt sử dụng Helm để xóa tất cả các releases đã triển khai. Thực hiện theo các bước sau theo thứ tự:

### Bước 1: Gỡ Cài Đặt Microservices Release

```bash
helm uninstall easybank
```

Lệnh này sẽ xóa tất cả microservices được triển khai dưới tên release `easybank`.

### Bước 2: Gỡ Cài Đặt Grafana

```bash
helm uninstall grafana
```

### Bước 3: Gỡ Cài Đặt Tempo

```bash
helm uninstall tempo
```

### Bước 4: Gỡ Cài Đặt Loki

```bash
helm uninstall loki
```

### Bước 5: Gỡ Cài Đặt Prometheus

```bash
helm uninstall prometheus
```

Đợi quá trình gỡ cài đặt hoàn tất trước khi tiếp tục.

### Bước 6: Gỡ Cài Đặt Kafka

```bash
helm uninstall kafka
```

### Bước 7: Gỡ Cài Đặt Keycloak

```bash
helm uninstall keycloak
```

### Bước 8: Xác Minh Các Helm Releases

Sau khi gỡ cài đặt tất cả các thành phần, hãy xác minh rằng không còn release nào:

```bash
helm ls
```

Kết quả đầu ra không nên hiển thị bất kỳ release nào, xác nhận rằng tất cả các cài đặt dựa trên Helm đã được xóa.

## Gỡ Cài Đặt Discovery Server

Discovery Server được triển khai bằng các file manifest của Kubernetes, không phải Helm, do đó cần một cách tiếp cận gỡ cài đặt khác.

### Di Chuyển Đến Thư Mục Kubernetes

```bash
cd kubernetes
```

### Xóa Bằng Kubectl

```bash
kubectl delete -f <tên-file-manifest>
```

Thay thế `<tên-file-manifest>` bằng tên thực tế của file manifest Discovery Server của bạn.

## Xác Minh Việc Gỡ Cài Đặt Hoàn Toàn

Trước khi xóa cluster, hãy xác minh rằng tất cả tài nguyên đã được xóa:

### Kiểm Tra Workloads

Điều hướng đến phần Kubernetes workloads trong Google Cloud Console. Xác minh rằng tất cả workloads đã trống.

### Kiểm Tra Services

Điều hướng đến phần Services. Đảm bảo tất cả services đã được xóa.

### Kiểm Tra Secrets và ConfigMaps

Điều hướng đến các phần Secrets và ConfigMaps. Xác nhận rằng tất cả tài nguyên liên quan đến các triển khai của bạn đã được xóa.

## Xóa Kubernetes Cluster

Sau khi tất cả các thành phần đã được gỡ cài đặt và xác minh, hãy tiến hành xóa cluster:

### Bước 1: Điều Hướng Đến Clusters

Trong Google Cloud Console, điều hướng đến trang Kubernetes Engine > Clusters.

### Bước 2: Chọn Cluster Của Bạn

Chọn cluster bạn muốn xóa (ví dụ: `cluster-one`).

### Bước 3: Xóa Cluster

1. Nhấp vào nút **Delete**
2. Một hộp thoại xác nhận sẽ xuất hiện
3. Nhập tên cluster của bạn (ví dụ: `cluster-one`) để xác nhận
4. Nhấp vào nút **Delete** để bắt đầu quá trình xóa

### Bước 4: Đợi Quá Trình Xóa

Quá trình xóa cluster mất khoảng 2-3 phút. Hãy đợi quá trình hoàn tất.

### Bước 5: Xác Minh Việc Xóa

Sau khi xóa, trang clusters nên trống rỗng, xác nhận rằng Kubernetes cluster của bạn đã được xóa vĩnh viễn.

## Các Cân Nhắc Về Chi Phí

- **Thời Gian Sử Dụng**: Cluster được sử dụng trong khoảng 1 giờ
- **Chi Phí Ước Tính**: $0.30 - $0.50 (cho cả tài khoản miễn phí và trả phí)
- **Quan Trọng**: Luôn xóa cluster của bạn sau khi hoàn thành công việc để tránh các khoản phí bất ngờ

## Các Thực Hành Tốt Nhất

1. **Luôn Dọn Dẹp**: Tạo thói quen xóa tài nguyên ngay lập tức sau khi hoàn thành công việc
2. **Xác Minh Việc Xóa**: Luôn xác nhận rằng các cluster đã được xóa hoàn toàn trước khi đóng console
3. **Theo Dõi Hóa Đơn**: Kiểm tra bảng điều khiển thanh toán Google Cloud thường xuyên
4. **Thiết Lập Cảnh Báo**: Cấu hình các cảnh báo thanh toán để thông báo cho bạn về các khoản phí bất ngờ

## Những Điểm Chính Cần Nhớ

- Quy trình triển khai và quản lý nhất quán giữa các Kubernetes clusters cục bộ và trên cloud
- Các lệnh giống nhau hoạt động trên các môi trường Kubernetes khác nhau
- Việc dọn dẹp đúng cách là cần thiết cho quản lý chi phí
- Cả Helm releases và các tài nguyên được triển khai bằng kubectl cần được xóa riêng biệt

## Kết Luận

Bạn đã triển khai, xác thực và dọn dẹp thành công các microservices từ Google Cloud Kubernetes cluster. Quy trình được trình bày ở đây áp dụng cho dịch vụ Kubernetes của bất kỳ nhà cung cấp cloud nào, đảm bảo bạn có kỹ năng để quản lý các triển khai microservices trên các nền tảng khác nhau.

## Các Bước Tiếp Theo

Tiếp tục đến phần tiếp theo để khám phá thêm các chủ đề nâng cao về triển khai và quản lý microservices.