# Khám Phá Dịch Vụ và Cân Bằng Tải Phía Máy Chủ trong Kubernetes

## Tổng Quan

Tài liệu này giải thích sự khác biệt giữa các phương pháp khám phá dịch vụ và cân bằng tải phía client và phía server trong kiến trúc microservices, tập trung vào việc triển khai khám phá phía server sử dụng Kubernetes.

## Khám Phá và Cân Bằng Tải Phía Client (Phương Pháp Eureka Server)

### Cách Hoạt Động

Trong phương pháp phía client sử dụng Eureka Server:

1. **Đăng Ký Dịch Vụ**: Tất cả microservices tự đăng ký với Eureka Server trong quá trình khởi động
2. **Cơ Chế Heartbeat**: Microservices gửi heartbeat định kỳ để chứng minh trạng thái khỏe mạnh
3. **Khám Phá Dịch Vụ**: Khi một microservice cần giao tiếp với microservice khác, nó truy vấn Eureka Server để lấy các instance khả dụng
4. **Cân Bằng Tải**: Client microservice thực hiện cân bằng tải sử dụng Spring Cloud Load Balancer

### Ví Dụ Luồng Giao Tiếp

Xét tình huống microservice Accounts muốn giao tiếp với microservice Loans:

**Bước 1**: Các instance của microservice Loans đăng ký với Eureka Server trong quá trình khởi động, cung cấp thông tin như hostname, port number và thông tin instance

**Bước 2**: Microservice Accounts truy vấn Eureka Server để lấy thông tin chi tiết về microservice Loans

**Bước 3**: Eureka Server phản hồi với tất cả thông tin instance của microservice Loans khả dụng (ví dụ: hai địa chỉ IP)

**Bước 4**: Microservice Accounts thực hiện cân bằng tải sử dụng Spring Cloud Load Balancer và chuyển tiếp request đến một trong các instance được chọn

### Ưu Điểm

- **Kiểm Soát Hoàn Toàn**: Ứng dụng client có toàn quyền kiểm soát các chiến lược cân bằng tải
- **Nhiều Chiến Lược**: Spring Cloud Load Balancer cung cấp nhiều thuật toán cân bằng tải khác nhau
- **Linh Hoạt**: Developer có thể tùy chỉnh hành vi cân bằng tải

### Nhược Điểm

- **Bảo Trì Thủ Công**: Developer phải bảo trì Eureka Server một cách thủ công
- **Chi Phí Cấu Hình**: Yêu cầu tạo ứng dụng Spring Boot và chuyển đổi nó thành Eureka Server
- **Thay Đổi Microservice**: Tất cả microservices cần thay đổi cấu hình để kết nối với Eureka Server
- **Gánh Nặng Phát Triển**: Trách nhiệm cấu hình và bảo trì thêm cho developer

## Khám Phá và Cân Bằng Tải Phía Server (Phương Pháp Kubernetes)

### Yêu Cầu Tiên Quyết

Phương pháp này **chỉ** có thể được sử dụng khi triển khai microservices lên Kubernetes cluster.

### Cách Hoạt Động

Trong phương pháp phía server sử dụng Kubernetes:

1. **Khám Phá Tự Động**: Kubernetes Discovery Server tự động giám sát tất cả các instance ứng dụng
2. **Không Cần Đăng Ký Rõ Ràng**: Ứng dụng không cần tự đăng ký
3. **Tích Hợp Kubernetes API**: Discovery server sử dụng Kubernetes APIs để lấy thông tin dịch vụ và endpoint
4. **Cân Bằng Tải Minh Bạch**: Cân bằng tải xảy ra ở cấp độ Kubernetes service

### Ví Dụ Luồng Giao Tiếp

Sử dụng cùng tình huống microservice Accounts và Loans:

**Bước 1**: Kubernetes Discovery Server truy vấn Kubernetes API để lấy tất cả thông tin instance của microservice Loans (không cần đăng ký rõ ràng)

**Bước 2**: Microservice Accounts gửi request trực tiếp đến Kubernetes service sử dụng tên service làm hostname/DNS

**Bước 3**: Kubernetes service làm việc với Discovery Server để thực hiện cân bằng tải

**Bước 4**: Request được chuyển tiếp đến một trong các instance của microservice Loans

### Điểm Khác Biệt Chính So Với Phương Pháp Phía Client

- **Không Có Discovery Client**: Ứng dụng client không kết nối với bất kỳ discovery server nào
- **Tên Service Làm Endpoint**: Request được gửi đến Kubernetes service sử dụng tên service
- **Cân Bằng Tải Phía Server**: Cân bằng tải xảy ra trong Kubernetes cluster
- **Không Cần Cấu Hình Phía Client**: Microservice Accounts không xử lý cân bằng tải hoặc khám phá dịch vụ

### Ưu Điểm

- **Không Cần Bảo Trì**: Không cần bảo trì Eureka Server thủ công
- **Không Thay Đổi Cấu Hình**: Microservices không yêu cầu cấu hình kết nối discovery server
- **Khám Phá Tự Động**: Kubernetes Discovery Server tự động lấy các instance microservice đang chạy
- **Kiến Trúc Đơn Giản**: Giảm độ phức tạp trong code microservice

### Nhược Điểm

- **Không Kiểm Soát Cân Bằng Tải**: Developer và ứng dụng client không có quyền kiểm soát chiến lược cân bằng tải
- **Phụ Thuộc Kubernetes**: Thuật toán cân bằng tải được quyết định hoàn toàn bởi Kubernetes cluster
- **Tùy Chỉnh Hạn Chế**: Không thể triển khai các chiến lược cân bằng tải tùy chỉnh

## Bảng So Sánh Tổng Kết

| Khía Cạnh | Phía Client (Eureka) | Phía Server (Kubernetes) |
|-----------|---------------------|--------------------------|
| Đăng Ký Dịch Vụ | Yêu cầu đăng ký thủ công | Tự động qua Kubernetes API |
| Kiểm Soát Cân Bằng Tải | Kiểm soát đầy đủ với nhiều chiến lược | Không kiểm soát, do Kubernetes xử lý |
| Bảo Trì | Yêu cầu bảo trì Eureka Server | Không cần bảo trì server thêm |
| Cấu Hình | Cấu hình microservice rộng rãi | Cấu hình tối thiểu |
| Yêu Cầu Triển Khai | Bất kỳ môi trường nào | Chỉ Kubernetes cluster |
| Gánh Nặng Developer | Cao hơn | Thấp hơn |

## Phương Pháp Triển Khai

### Chuyển Đổi Sang Khám Phá Phía Server

Khi chuyển sang khám phá dịch vụ và cân bằng tải phía server trong Kubernetes:

1. Loại bỏ Eureka Server khỏi mạng microservice
2. Triển khai microservices lên Kubernetes cluster
3. Tạo Kubernetes services (các loại ClusterIP hoặc LoadBalancer)
4. Sử dụng tên service làm DNS endpoint cho giao tiếp giữa các service
5. Để Kubernetes tự động xử lý khám phá dịch vụ và cân bằng tải

## Lựa Chọn Phương Pháp Phù Hợp

Không có phương pháp nào "tốt" hay "xấu" một cách tuyệt đối. Lựa chọn phụ thuộc vào:

- **Môi Trường Triển Khai**: Kubernetes bắt buộc cho phương pháp phía server
- **Yêu Cầu Kiểm Soát**: Nhu cầu về các chiến lược cân bằng tải tùy chỉnh
- **Tài Nguyên Phát Triển**: Năng lực của team trong việc bảo trì cơ sở hạ tầng bổ sung
- **Yêu Cầu Kinh Doanh**: Nhu cầu cụ thể của tổ chức và các ràng buộc

Cả hai phương pháp đều hợp lệ và có các trường hợp sử dụng riêng. Hiểu cả hai giúp bạn đưa ra quyết định kiến trúc có cơ sở cho hệ sinh thái microservices của mình.

## Kết Luận

Khám phá dịch vụ và cân bằng tải phía server trong Kubernetes cung cấp một phương pháp đơn giản hóa cho giao tiếp microservice bằng cách loại bỏ nhu cầu đăng ký dịch vụ rõ ràng và cân bằng tải phía client. Mặc dù nó giảm gánh nặng cho developer và chi phí bảo trì, nó cũng hạn chế quyền kiểm soát các chiến lược cân bằng tải. Chìa khóa là hiểu cả hai phương pháp và chọn phương pháp phù hợp nhất với yêu cầu cụ thể của bạn.