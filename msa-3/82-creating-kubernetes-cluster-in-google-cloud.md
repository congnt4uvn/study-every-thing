# Tạo Kubernetes Cluster trên Google Cloud (GKE)

## Tổng Quan

Hướng dẫn này sẽ giúp bạn thực hiện các bước tạo một Kubernetes cluster trên Google Cloud Platform (GCP) sử dụng Google Kubernetes Engine (GKE). Đây là bước quan trọng để triển khai các microservices được xây dựng bằng Java Spring Boot lên môi trường Kubernetes trên cloud.

## Yêu Cầu Trước Khi Bắt Đầu

- Tài khoản Google Cloud Platform đang hoạt động
- Đã kích hoạt tính năng thanh toán (billing) trên tài khoản GCP
- Quyền truy cập vào Google Cloud Console

## Các Bước Tạo GKE Cluster

### 1. Truy Cập Kubernetes Engine

Có hai cách để truy cập Kubernetes Engine:

- **Tùy chọn 1**: Nhấp vào "Create a GKE cluster" từ dashboard chính
- **Tùy chọn 2**: Sử dụng ô tìm kiếm để tìm "Kubernetes" và chọn "Kubernetes Engine"

### 2. Kích Hoạt Kubernetes Engine API

Khi truy cập Kubernetes Engine lần đầu tiên trong tài khoản của bạn:

1. Hệ thống sẽ yêu cầu bạn kích hoạt **Kubernetes Engine API**
2. Nhấp vào nút **Enable** (Kích hoạt)
3. Bạn cũng cần **kích hoạt billing** nếu chưa thực hiện
4. Nhấp vào tùy chọn **Enable billing**

### 3. Tạo Cluster

Sau khi Kubernetes Engine API được kích hoạt:

1. Nhấp vào tùy chọn **tạo Kubernetes cluster**
2. Bạn sẽ thấy giao diện tạo cluster

### 4. Chọn Loại Cluster: Standard vs Autopilot

Mặc định, GCP hiển thị tùy chọn **Autopilot cluster**:

#### Autopilot Cluster
- Tự động điều chỉnh dung lượng cluster dựa trên lưu lượng truy cập
- Google Cloud xử lý phần lớn công việc nặng nhọc
- Tùy chọn dễ nhất cho các tổ chức
- Hạn chế trong việc khám phá chi tiết về Kubernetes cluster

#### Standard Cluster (Khuyến Nghị cho Việc Học)
- Kiểm soát nhiều hơn về cấu hình cluster
- Tốt hơn cho việc học và khám phá các tính năng Kubernetes
- Bắt buộc cho khóa học này

**Hành động**: Nhấp vào **"Switch to Standard Cluster"** và xác nhận lựa chọn của bạn.

### 5. Cấu Hình Cluster

1. **Tên Cluster**: Chấp nhận tên mặc định `cluster-1` hoặc đặt tên riêng
2. **Cài Đặt Mặc Định**: Giữ nguyên tất cả các giá trị mặc định cho hướng dẫn này
3. Di chuyển đến cuối trang cấu hình

### 6. Xem Xét Chi Phí

Trước khi tạo cluster, hãy xem xét chi phí ước tính:

- **Chi phí ước tính hàng tháng**: $176 (nếu chạy liên tục trong một tháng)
- **Phí theo giờ**: $0.24 mỗi giờ
- **Lưu ý**: Nếu bạn làm theo hướng dẫn và sử dụng credits miễn phí, bạn sẽ không bị tính phí
- Hướng dẫn sẽ hoàn thành trong vòng một giờ

### 7. Tạo Cluster

1. Nhấp vào nút **Create** (Tạo)
2. Quá trình tạo Kubernetes cluster sẽ bắt đầu
3. **Dung lượng mặc định**: 3 nodes
4. **Thời gian tạo**: Khoảng 5 phút

### 8. Đợi Hoàn Thành

Quá trình tạo cluster mất khoảng 5 phút. Hãy đợi cluster được tạo thành công trước khi tiến hành các bước tiếp theo.

## Các Bước Tiếp Theo

Sau khi Kubernetes cluster của bạn được tạo, bạn có thể:

- Khám phá chi tiết và cấu hình của cluster
- Triển khai các Spring Boot microservices lên cluster
- Cấu hình networking và service mesh
- Thiết lập monitoring và logging
- Triển khai CI/CD pipelines

## Mẹo Quản Lý Chi Phí

- Xóa cluster khi không sử dụng để tránh phát sinh chi phí
- Sử dụng credits miễn phí do GCP cung cấp
- Thường xuyên theo dõi bảng điều khiển thanh toán
- Thiết lập cảnh báo thanh toán để tránh chi phí bất ngờ

## Tóm Tắt

Việc tạo Kubernetes cluster trên Google Cloud là một quy trình đơn giản, cung cấp nền tảng mạnh mẽ để triển khai và quản lý microservices. Tùy chọn Standard cluster mang lại nhiều quyền kiểm soát và cơ hội học tập hơn, làm cho nó trở nên lý tưởng để hiểu các khái niệm Kubernetes trong môi trường cloud.

## Tài Nguyên Bổ Sung

- Tài liệu Google Kubernetes Engine
- Tài liệu Kubernetes chính thức
- Best Practices cho Spring Boot trên Kubernetes