# Kiểm Thử Kubernetes Discovery Server với Microservices

## Tổng Quan

Hướng dẫn này trình bày cách kiểm thử triển khai Kubernetes Discovery Server với các microservices Spring Boot, bao gồm xác minh cân bằng tải và hiểu các lợi ích của việc sử dụng service discovery tích hợp Kubernetes.

## Yêu Cầu Trước

- Cụm Kubernetes với microservices đã triển khai
- Keycloak được cấu hình cho xác thực OAuth2
- Postman hoặc công cụ kiểm thử API tương tự
- Nhiều bản sao (replicas) của accounts microservice đang chạy
- Gateway server đã được cấu hình và đang hoạt động

## Chuẩn Bị Kiểm Thử

### 1. Cấu Hình Client Keycloak

Một client đã được tạo trong Keycloak với các chi tiết sau:
- **Tên Client**: `easybank-callcenter-cc`
- **Vai trò**: Các vai trò cần thiết được gán để truy cập microservices

### 2. Kiến Trúc Microservices

- **Accounts Microservice**: Chạy với 2 bản sao (replicas)
- Mỗi bản sao có cơ sở dữ liệu H2 in-memory riêng
- Gateway Server: Định tuyến các yêu cầu đến microservices
- Discovery Server: Service discovery tích hợp Kubernetes

## Quy Trình Kiểm Thử

### Bước 1: Lấy Access Token

1. Mở Postman
2. Yêu cầu access token mới sử dụng Keycloak client đã cấu hình
3. Sử dụng token thu được cho các lần gọi API tiếp theo

### Bước 2: Kiểm Thử API Tạo Tài Khoản

**Endpoint**: `POST /api/create` (qua Accounts microservice)

1. Gọi API tạo tài khoản thông qua gateway
2. Kết quả mong đợi: "Account created successfully"
3. Lưu ý: Yêu cầu đầu tiên có thể mất vài giây

**Số điện thoại mẫu**: Kết thúc bằng `88`

### Bước 3: Kiểm Thử API Lấy Thông Tin Tài Khoản

**Endpoint**: `GET localhost:8072/easybank/accounts/api/fetch`

**Tham số truy vấn**: Số điện thoại đã sử dụng khi tạo tài khoản

#### Kiểm Thử Cân Bằng Tải

1. Gọi API fetch nhiều lần
2. Ban đầu, các yêu cầu trả về dữ liệu tài khoản thành công
3. Sau nhiều yêu cầu, bạn có thể nhận được lỗi "Not Found"
4. Điều này xác nhận cân bằng tải đang hoạt động - các yêu cầu được phân phối đến các pods khác nhau

## Hiểu Về Sticky Sessions

### Sticky Session Là Gì?

Cụm Kubernetes có thể duy trì sticky sessions khi:
- Các yêu cầu từ cùng một client (cùng địa chỉ IP)
- Được chuyển tiếp đến cùng một pod đã xử lý yêu cầu ban đầu
- Hành vi này là có chủ ý để duy trì tính nhất quán của phiên làm việc

### Kiểm Thử Không Có Sticky Sessions

Để xem phản hồi từ các pods khác nhau:

1. **Đợi 1-2 phút** giữa các yêu cầu
2. Sử dụng **chế độ ẩn danh của trình duyệt** để mô phỏng client khác
3. Hoặc sử dụng các IP client hoặc công cụ khác nhau

### Hành Vi Quan Sát Được

- Yêu cầu thường xuyên từ cùng client → Phản hồi từ cùng pod (sticky session)
- Yêu cầu sau khoảng thời gian nghỉ hoặc từ client khác → Phản hồi từ pod khác
- Điều này xác nhận Kubernetes Discovery Server đang định tuyến lưu lượng một cách thông minh

## Lợi Ích Của Kubernetes Discovery Server

### 1. Giảm Gánh Nặng Cho Nhà Phát Triển

- **Không cần bảo trì Eureka Server**
- Microservices không cần tự đăng ký trong quá trình khởi động
- Không cần gửi heartbeats thường xuyên
- Kubernetes xử lý service discovery một cách tự nhiên

### 2. Kiến Trúc Đơn Giản Hóa

- Kubernetes tự động giám sát và theo dõi tất cả các instances đang chạy
- Tích hợp tự nhiên với cụm Kubernetes
- Giảm độ phức tạp trong cấu hình microservices

### 3. Tự Động Service Discovery

- Các pods được Kubernetes tự động phát hiện
- Các endpoints của service được cập nhật động
- Không cần các thành phần cơ sở hạ tầng bổ sung

## Đánh Đổi và Cân Nhắc

### Kiểm Soát Cân Bằng Tải Hạn Chế

**Hạn chế**: Với Kubernetes Discovery Server, bạn có quyền kiểm soát hạn chế đối với các thuật toán cân bằng tải.

**Giải pháp thay thế**: Nếu bạn cần kiểm soát chi tiết cân bằng tải:
- Sử dụng **Spring Cloud Load Balancer**
- Triển khai **Eureka Server** cho cân bằng tải phía client
- Cấu hình các chiến lược cân bằng tải tùy chỉnh

### Khi Nào Sử Dụng Từng Phương Pháp

| Tính năng | Kubernetes Discovery | Eureka Server |
|-----------|---------------------|---------------|
| Độ phức tạp cài đặt | Thấp | Cao |
| Bảo trì | Tối thiểu | Cần quản lý |
| Kiểm soát cân bằng tải | Hạn chế | Toàn quyền kiểm soát |
| Tích hợp Kubernetes | Có | Không |
| Phù hợp nhất cho | Triển khai cloud-native | Yêu cầu tùy chỉnh |

## Kết Quả Xác Minh

✅ **Cân bằng tải hoạt động chính xác**
- Các yêu cầu được phân phối qua nhiều pods
- Các phản hồi khác nhau xác nhận việc phân phối lưu lượng

✅ **Kubernetes Discovery Server hoạt động**
- Các pods được tự động phát hiện và đăng ký
- Định tuyến service hoạt động như mong đợi

✅ **Hành vi sticky session**
- Định tuyến nhất quán cho các yêu cầu thường xuyên từ cùng client
- Tối ưu hóa hiệu suất thông qua session affinity

## Thực Hành Tốt Nhất

1. **Kiểm thử với nhiều clients** để xác minh cân bằng tải
2. **Giám sát sức khỏe pod** thông qua bảng điều khiển Kubernetes
3. **Sử dụng timeouts phù hợp** cho các yêu cầu API
4. **Triển khai logging đúng cách** để theo dõi pod nào phục vụ yêu cầu
5. **Cân nhắc sticky sessions** khi thiết kế ứng dụng có trạng thái

## Kết Luận

Kubernetes Discovery Server cung cấp một phương pháp đơn giản hóa cho service discovery trong kiến trúc microservices. Mặc dù nó cung cấp độ phức tạp và chi phí bảo trì giảm, các nhà phát triển nên cân nhắc yêu cầu cân bằng tải của họ khi lựa chọn giữa discovery tích hợp Kubernetes và các giải pháp phía client như Eureka Server.

## Các Bước Tiếp Theo

- Các Docker images cho section 17 sẽ được đẩy lên Docker Hub
- Code được check in vào kho GitHub trong thư mục `section_17`
- Xem lại code để biết chi tiết triển khai
- Tham khảo `section_17` cho các câu hỏi và tài liệu tham khảo

## Tài Nguyên

- **GitHub Repository**: Thư mục section_17
- **Docker Hub**: Các images liên quan đến Section 17
- **Tài liệu**: Tham khảo tài liệu dự án để biết cấu hình chi tiết

---

*Nếu có câu hỏi hoặc cần làm rõ, vui lòng tham khảo code trong thư mục section_17 của repository.*