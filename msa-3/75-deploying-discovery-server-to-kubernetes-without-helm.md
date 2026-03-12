# Triển Khai Discovery Server lên Kubernetes Không Sử Dụng Helm

## Tổng Quan

Hướng dẫn này trình bày cách triển khai Discovery Server lên Kubernetes cluster bằng cách sử dụng các file manifest của Kubernetes thay vì Helm charts. Chúng ta sẽ tìm hiểu tại sao phương pháp này phù hợp cho thành phần này và thực hiện quy trình triển khai từng bước.

## Tại Sao Không Sử Dụng Helm Charts?

Có hai lý do chính để chọn sử dụng file manifest thay vì Helm charts cho việc triển khai Discovery Server:

### 1. Thiết Lập Một Lần
Discovery Server là một thiết lập một lần duy nhất bên trong Kubernetes cluster của bạn. Không giống như các microservices cần cập nhật và thay đổi cấu hình thường xuyên, Discovery Server không cần nhiều sửa đổi theo thời gian. Đối với các hoạt động một lần như vậy, việc chạy các file manifest thủ công là hoàn toàn chấp nhận được và đơn giản.

### 2. Thiếu Helm Charts Từ Cộng Đồng
Hiện tại, chưa có Helm chart nào được phát triển bởi cộng đồng Helm, bao gồm cả Bitnami, dành riêng cho Discovery Server. Mặc dù có thể tích hợp các file manifest vào một Helm chart tùy chỉnh (như Helm chart của easybank), nhưng công sức cần thiết sẽ rất lớn và không xứng đáng cho một thành phần chỉ cần triển khai một lần.

## Quy Trình Triển Khai

### Yêu Cầu Trước
- Quyền truy cập vào Kubernetes cluster
- Công cụ kubectl CLI đã được cài đặt và cấu hình
- File manifest của Discovery Server (`kubernetes-discoveryserver.yaml`)

### Lệnh Triển Khai

Để triển khai Discovery Server, thực thi lệnh sau từ terminal của bạn:

```bash
kubectl apply -f kubernetes-discoveryserver.yaml
```

### Các Tài Nguyên Được Tạo

Lệnh này sẽ tạo các tài nguyên Kubernetes sau:
- **Service**: Expose Discovery Server trong cluster
- **Service Account**: Cung cấp định danh cho các pod của Discovery Server
- **Role Binding**: Liên kết role với service account
- **Role**: Định nghĩa quyền cho Discovery Server
- **Deployment**: Quản lý vòng đời pod của Discovery Server

## Các Bước Xác Minh

### 1. Truy Cập Kubernetes Dashboard
Điều hướng đến Kubernetes dashboard để giám sát trạng thái triển khai.

### 2. Kiểm Tra Trạng Thái Pod
- Vào phần Pods
- Tìm pod của Discovery Server
- Xác minh rằng nó đang ở trạng thái running (chỉ báo màu xanh)

### 3. Xem Logs
Mở logs của pod để xác nhận khởi động thành công:
- Discovery Server nên khởi động trong khoảng 20 giây
- Tìm các log từ Spring Boot xác nhận đây là ứng dụng Spring Boot
- Xác minh không có thông báo lỗi

### Kết Quả Log Mong Đợi
Bạn sẽ thấy các log từ Spring Framework cho biết Discovery Server đã khởi động thành công. Điều này xác nhận rằng:
- Triển khai hoạt động chính xác
- Discovery Server là một ứng dụng Spring Boot
- Tất cả các thành phần (deployment, pods, replica sets) đều khỏe mạnh

## Chuẩn Bị Code Microservices

### Di Chuyển Code
Sau khi triển khai thành công Discovery Server, chuẩn bị code microservices của bạn:

1. **Sao Chép Microservices từ Section 14**
   - accounts
   - cards
   - config server
   - gateway server
   - loans
   - message

2. **Loại Trừ Các Mục Sau**
   - Eureka Server (đang được thay thế bởi Kubernetes Discovery Server)
   - Các file Docker Compose (không cần thiết cho triển khai Kubernetes)

3. **Sao Chép Thư Mục Helm từ Section 16**
   - Thư mục này sẽ cần sửa đổi để loại bỏ các tham chiếu đến Eureka Server

### Thiết Lập Môi Trường Phát Triển

1. Mở thư mục section_17 trong IntelliJ IDEA
2. Load các project như Maven projects
3. Bật annotation processing khi được nhắc
4. Build các project

## Các Bước Tiếp Theo

Sau khi triển khai thành công Discovery Server:

1. **Cập Nhật Code Microservices**
   - Loại bỏ các dependency và configuration liên quan đến Eureka
   - Thêm tích hợp với Kubernetes Discovery Server

2. **Sửa Đổi Helm Charts**
   - Loại bỏ các tham chiếu đến Eureka Server
   - Cập nhật cấu hình service discovery

3. **Xác Minh Trạng Thái Cluster**
   - Đảm bảo tất cả các deployment hiển thị trạng thái màu xanh
   - Xác nhận pods và replica sets đều khỏe mạnh
   - Kiểm tra rằng Discovery Server đang chạy không có vấn đề

## Kết Luận

Discovery Server hiện đã được triển khai thành công và đang chạy trong Kubernetes cluster của bạn. Với tất cả các thành phần hiển thị trạng thái màu xanh (deployment, pods, replica sets), nền tảng đã sẵn sàng để triển khai và cấu hình các microservices của bạn hoạt động với cơ chế discovery tích hợp sẵn của Kubernetes.

## Các Điểm Chính Cần Nhớ

- Discovery Server là thành phần thiết lập một lần
- Các file manifest của Kubernetes đủ cho việc triển khai này
- Discovery Server chạy như một ứng dụng Spring Boot
- Kubernetes cung cấp khả năng service discovery tích hợp sẵn
- Các microservices sẽ được cập nhật để sử dụng Kubernetes Discovery Server thay vì Eureka