# Hướng Dẫn Lệnh Helm Uninstall

## Tổng Quan

Giống như cách Helm cho phép bạn cài đặt toàn bộ hệ thống microservice chỉ với một lệnh duy nhất, nó cũng cung cấp khả năng gỡ cài đặt tất cả microservices chỉ bằng một lệnh. Hướng dẫn này sẽ trình bày cách sử dụng lệnh Helm Uninstall để xóa các microservices khỏi Kubernetes cluster.

## Tại Sao Sử Dụng Helm Uninstall?

Lệnh Helm Uninstall rất hữu ích khi bạn cần:
- Tắt toàn bộ Kubernetes cluster
- Dọn dẹp tài nguyên trong các môi trường phát triển
- Giải phóng tài nguyên hệ thống trong quá trình phát triển

## Liệt Kê Các Helm Release Hiện Tại

Trước khi gỡ cài đặt, bạn có thể xem tất cả các cài đặt Helm hiện tại bằng lệnh:

```bash
helm ls
```

Lệnh này hiển thị tất cả các release đã được cài đặt với Helm.

## Gỡ Cài Đặt Helm Releases

### Cú Pháp Lệnh Uninstall Cơ Bản

Cú pháp để gỡ cài đặt một Helm release:

```bash
helm uninstall <tên-release>
```

### Ví Dụ: Gỡ Cài Đặt Microservices

#### Bước 1: Gỡ Cài Đặt Ứng Dụng Chính
```bash
helm uninstall easybank
```

Lệnh này sẽ xóa tất cả các microservices được triển khai dưới Easy Bank release.

#### Bước 2: Gỡ Cài Đặt Các Thành Phần Bổ Sung

Gỡ cài đặt các thành phần còn lại theo thứ tự:

```bash
helm uninstall grafana
helm uninstall tempo
helm uninstall loki
helm uninstall prometheus
helm uninstall kafka
helm uninstall keycloak
```

### Xác Minh

Sau khi gỡ cài đặt tất cả các releases, xác minh việc dọn dẹp:

```bash
helm ls
```

Bạn sẽ thấy kết quả trống, xác nhận rằng tất cả các releases đã được xóa.

## Xác Minh Qua Kubernetes Dashboard

Bạn cũng có thể xác thực việc gỡ cài đặt thông qua Kubernetes dashboard:
- Truy cập vào Kubernetes dashboard của bạn
- Xác minh rằng các pods, deployments, services, config maps và secrets đã được xóa

## Quan Trọng: Persistent Volume Claims (PVCs)

### Vấn Đề Đã Biết

**Lưu Ý Quan Trọng**: Persistent Volume Claims (PVCs) **không tự động bị xóa** trong quá trình gỡ cài đặt Helm.

### Tại Sao Điều Này Quan Trọng

- PVCs còn sót lại có thể gây ra vấn đề khi cài đặt lại Helm charts
- Điều này đặc biệt ảnh hưởng đến các thành phần như Keycloak, Kafka và các ứng dụng có trạng thái khác
- Chưa rõ đây là lỗi hay hành vi cố ý của Helm

### Dọn Dẹp PVC Thủ Công

Để xóa persistent volume claims:

1. Chọn các PVCs trong Kubernetes dashboard
2. Nhấp vào nút delete
3. Lặp lại cho tất cả các PVCs còn lại

**Luôn xóa PVCs sau khi gỡ cài đặt Helm releases để tránh các vấn đề cài đặt trong tương lai.**

## Giải Pháp Thay Thế Cho Helm: Kustomize

### Kustomize Là Gì?

Kustomize (có sẵn tại [kustomize.io](https://kustomize.io)) là một đối thủ cạnh tranh với Helm, giải quyết các thách thức triển khai tương tự.

### So Sánh Kustomize vs Helm

#### Ưu Điểm của Kustomize:
- Dễ học hơn
- Đường cong học tập thấp hơn
- Cách tiếp cận cấu hình đơn giản hơn

#### Ưu Điểm của Helm:
- Hệ sinh thái mạnh mẽ hơn
- Nhiều community charts (Bitnami và các nguồn khác)
- Có thể cài đặt nhiều thành phần/sản phẩm dễ dàng
- Nhiều tính năng và khả năng hơn
- Tốt hơn cho các triển khai phức tạp

### Khuyến Nghị

**Sử dụng Helm** vì những lý do sau:
- Hỗ trợ cộng đồng mạnh mẽ hơn
- Truy cập vào các Bitnami charts và community charts có sẵn
- Khả năng toàn diện hơn
- Nhiều dự án bắt đầu với Kustomize cuối cùng cũng chuyển sang Helm

Tuy nhiên, nếu Kustomize đáp ứng các yêu cầu dự án của bạn và bạn thích sự đơn giản của nó, hãy thoải mái sử dụng nó.

## Tài Nguyên Bổ Sung

Để biết thêm chi tiết về Kustomize, tham khảo [tài liệu chính thức](https://kustomize.io).

## Tóm Tắt

- Sử dụng `helm ls` để liệt kê tất cả các releases đã cài đặt
- Sử dụng `helm uninstall <tên-release>` để xóa releases
- Luôn xóa thủ công Persistent Volume Claims sau khi gỡ cài đặt
- Helm cung cấp hệ sinh thái mạnh mẽ với sự hỗ trợ của cộng đồng
- Cân nhắc nhu cầu dự án khi lựa chọn giữa Helm và Kustomize

## Kết Luận

Helm cung cấp các lệnh mạnh mẽ để quản lý microservices trong Kubernetes clusters. Hiểu rõ quy trình gỡ cài đặt, bao gồm cả việc dọn dẹp đúng cách các PVCs, là điều thiết yếu để duy trì một môi trường Kubernetes khỏe mạnh.