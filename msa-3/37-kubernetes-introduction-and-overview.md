# Giới Thiệu và Tổng Quan về Kubernetes

## Giới Thiệu

Kubernetes là một nền tảng điều phối container thiết yếu mà chúng ta sẽ sử dụng để triển khai và quản lý microservices. Hướng dẫn này cung cấp phần giới thiệu toàn diện về Kubernetes và các khái niệm cốt lõi của nó.

## Kubernetes là gì?

Kubernetes là một **hệ thống mã nguồn mở để tự động hóa việc triển khai, mở rộng và quản lý các ứng dụng được đóng gói trong container**. Nó đã trở thành nền tảng điều phối nổi tiếng nhất hiện có trên thị trường ngày nay.

### Các Ưu Điểm Chính

- **Trung Lập với Cloud**: Các khái niệm Kubernetes vẫn nhất quán bất kể bạn triển khai ở đâu - dù trên hệ thống local, AWS, GCP hay Azure
- **Đã Được Kiểm Nghiệm Thực Chiến**: Được phát triển và sử dụng nội bộ bởi Google trong hơn 15 năm trước khi được mã nguồn mở vào năm 2015
- **Sẵn Sàng Cho Production**: Cung cấp năng lượng cho các sản phẩm lớn của Google bao gồm YouTube, Google Photos và Gmail

## Lịch Sử và Bối Cảnh

Kubernetes được Google phát triển trong khoảng thời gian 15 năm như một dự án nội bộ. Vào khoảng năm 2015, Google quyết định mã nguồn mở công nghệ này để các tổ chức khác có thể hưởng lợi từ nó.

Thành tích đã được chứng minh trong việc xử lý lưu lượng truy cập khổng lồ của Google (không có ứng dụng nào trên thế giới nhận được lưu lượng truy cập nhiều hơn các sản phẩm của Google) cho thấy rằng Kubernetes có thể hỗ trợ bất kỳ tổ chức nào và xử lý bất kỳ lượng traffic nào.

## Khả Năng Cốt Lõi

### 1. Quản Lý Hệ Thống Phân Tán
Kubernetes giúp bạn chạy các hệ thống phân tán một cách linh hoạt, bao gồm:
- Ứng dụng cloud-native
- Kiến trúc microservices

### 2. Tự Động Mở Rộng và Chuyển Đổi Dự Phòng
- Tự động mở rộng ứng dụng dựa trên nhu cầu
- Xử lý chuyển đổi dự phòng ứng dụng một cách liền mạch
- Các mẫu triển khai đảm bảo không có downtime

### 3. Service Discovery và Cân Bằng Tải
Kubernetes hoạt động như một service discovery agent và cung cấp khả năng cân bằng tải tích hợp:
- **Thay Thế Eureka Server**: Khi sử dụng Kubernetes, bạn có thể loại bỏ nhu cầu về Eureka Server
- **Cân Bằng Tải Phía Server**: Khác với cân bằng tải phía client với Eureka, Kubernetes cung cấp cân bằng tải phía server
- Tự động phân phối traffic qua các microservices của bạn

### 4. Điều Phối Container và Storage
- Kiểm soát bất kỳ số lượng container nào
- Quản lý yêu cầu storage cho các container của bạn
- Phân bổ tài nguyên tự động

### 5. Tự Động Rollout và Rollback
- Triển khai phiên bản mới một cách an toàn
- Tự động rollback nếu phát hiện vấn đề

### 6. Tự Phục Hồi (Self-Healing)
- Tự động khởi động lại các container bị lỗi
- Thay thế và lên lịch lại các container khi node chết
- Ngừng các container không phản hồi với health check

### 7. Quản Lý Cấu Hình và Secret
- Quản lý cấu hình ứng dụng
- Lưu trữ và quản lý thông tin nhạy cảm (secrets) một cách an toàn
- Cập nhật cấu hình mà không cần build lại container image

## Tên Gọi "Kubernetes"

### Nguồn Gốc
Từ **Kubernetes** có nguồn gốc từ tiếng Hy Lạp, có nghĩa là "người lái tàu" hoặc "thủy thủ" - người điều khiển và điều hướng con tàu.

### Logo
Logo Kubernetes có hình bánh lái tàu, đại diện cho khái niệm người lái tàu. Giống như người lái tàu kiểm soát toàn bộ con tàu và điều hướng nó một cách an toàn, Kubernetes kiểm soát tất cả các container trong mạng lưới microservice của bạn.

### Phép Tương Tự Thực Tế
Trong thế giới thực, các container được vận chuyển trên tàu từ nơi này sang nơi khác, được kiểm soát bởi thuyền trưởng hoặc người lái tàu. Tương tự, Kubernetes kiểm soát các container (được phát triển với Docker hoặc các công nghệ containerization khác) và điều phối việc triển khai và quản lý chúng.

### Dạng Viết Tắt: K8s
Kubernetes thường được viết tắt là **K8s**:
- **K** = Chữ cái đầu tiên của Kubernetes
- **8** = Tám ký tự giữa K và s
- **s** = Chữ cái cuối cùng của Kubernetes

Khi bạn thấy "K8s" trong các blog hoặc website, nó đề cập đến Kubernetes.

## Tích Hợp với Microservices

Kubernetes cung cấp một số lợi thế khi làm việc với microservices:

1. **Loại bỏ nhu cầu về Eureka Server** trong service discovery
2. **Cung cấp cân bằng tải phía server** thay vì cân bằng tải phía client
3. **Xử lý điều phối container** cho tất cả các microservices
4. **Quản lý cấu hình** và secrets trên tất cả các services
5. **Đảm bảo tính khả dụng cao** và triển khai không downtime

## Kết Luận

Kubernetes là một nền tảng điều phối container mạnh mẽ, đã được chứng minh trong production, có thể đơn giản hóa đáng kể việc triển khai và quản lý các kiến trúc microservices. Cách tiếp cận trung lập với cloud của nó, kết hợp với sự hỗ trợ của Google và sự chấp nhận rộng rãi trong ngành, khiến nó trở thành lựa chọn tuyệt vời cho việc triển khai ứng dụng hiện đại.

Trong các bài giảng sắp tới, chúng ta sẽ khám phá cách thiết lập Kubernetes cho việc triển khai microservices và cách tận dụng các tính năng của nó để xây dựng các ứng dụng linh hoạt, có khả năng mở rộng.

---

**Bước Tiếp Theo**: Trong bài giảng tiếp theo, chúng ta sẽ đi sâu hơn vào kiến trúc Kubernetes và bắt đầu thiết lập Kubernetes cluster đầu tiên của chúng ta.