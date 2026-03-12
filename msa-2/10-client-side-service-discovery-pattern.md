# Mô Hình Service Discovery Phía Client Trong Microservices

## Tổng Quan

Trong kiến trúc microservices, service discovery (khám phá dịch vụ) cùng với service registration (đăng ký dịch vụ) giải quyết các vấn đề khi thiết lập giao tiếp nội bộ giữa các dịch vụ. Có hai cách tiếp cận khác nhau để triển khai service discovery:

1. **Client-Side Service Discovery** (Khám phá dịch vụ phía client)
2. **Server-Side Service Discovery** (Khám phá dịch vụ phía server)

Tài liệu này tập trung vào mô hình client-side service discovery và cách nó hoạt động trong microservices Spring Boot.

## Client-Side Service Discovery Là Gì?

Trong cách tiếp cận client-side service discovery, các ứng dụng chịu trách nhiệm:
- Tự đăng ký với service registry khi khởi động
- Hủy đăng ký khi tắt
- Truy vấn service registry để khám phá các dịch vụ khác
- Triển khai logic cân bằng tải để chọn instance dịch vụ

### Đặc Điểm Chính

Trách nhiệm chọn instance nào của dịch vụ backend để giao tiếp nằm ở **microservice client**. Đó là lý do được gọi là khám phá dịch vụ "phía client".

## Cách Hoạt Động

### Bước 1: Thiết Lập Service Registry

Trước khi khởi động microservices, service registry phải chạy như một server riêng biệt trong mạng microservice của bạn.

### Bước 2: Đăng Ký Dịch Vụ

Khi các instance microservice khởi động (ví dụ: hai instance của loans microservice):
- Mỗi instance kết nối với service registry
- Chúng đăng ký thông tin chi tiết: địa chỉ IP, hostname và số cổng
- Chúng gửi các **tín hiệu heartbeat** đều đặn để xác nhận tình trạng sức khỏe

### Bước 3: Khám Phá Dịch Vụ

Khi một client microservice (ví dụ: accounts microservice) muốn giao tiếp với dịch vụ khác (ví dụ: loans microservice):
1. Accounts microservice truy vấn service registry để lấy thông tin loans microservice
2. Service registry xác thực yêu cầu
3. Registry trả về danh sách tất cả địa chỉ IP khả dụng của loans microservice

### Bước 4: Cân Bằng Tải

Client microservice nhận được nhiều địa chỉ IP và:
- Áp dụng chiến lược cân bằng tải (round-robin, weighted round-robin, least connections, hoặc tùy chỉnh)
- Chuyển tiếp yêu cầu đến một instance được chọn
- Tự xử lý logic cân bằng tải

## Ưu Điểm

### 1. Chiến Lược Cân Bằng Tải Linh Hoạt

Bạn có thể chọn từ nhiều thuật toán:
- **Round Robin**: Phân phối yêu cầu đều trên các instance
- **Weighted Round Robin**: Gán trọng số cho các instance khác nhau
- **Least Connections**: Định tuyến đến instance có ít kết nối hoạt động nhất
- **Custom Algorithms**: Triển khai logic của riêng bạn

### 2. Kiểm Soát Phía Client

Client có toàn quyền kiểm soát việc chọn dịch vụ và quyết định định tuyến.

## Nhược Điểm

### 1. Tăng Trách Nhiệm Cho Developer

Developers phải:
- Thay đổi code trong từng microservice
- Triển khai giao tiếp với service registration
- Xử lý logic cân bằng tải

### 2. Yêu Cầu Hạ Tầng

Bạn cần duy trì một server tập trung cho:
- Đăng ký dịch vụ
- Hỗ trợ khám phá dịch vụ

## So Sánh Client-Side vs Server-Side Discovery

### Server-Side Discovery

- Sử dụng khi triển khai microservices trong môi trường **Kubernetes**
- Yêu cầu đội operations và platform chuyên dụng
- Chi phí hạ tầng cao hơn
- Tốt hơn cho các dự án có ngân sách và nguồn lực

### Client-Side Discovery

- Phù hợp cho các dự án không thể chi trả cho việc bảo trì Kubernetes cluster
- Phát triển server tập trung riêng cho service registration
- Developer tham gia nhiều hơn nhưng chi phí hạ tầng thấp hơn

## Kiến Trúc Service Discovery Layer

### Các Thành Phần

Service discovery layer bao gồm:
- Nhiều service discovery nodes (có thể triển khai bao nhiêu tùy theo tải)
- Không cần bảo trì địa chỉ IP thủ công
- Đồng bộ tự động giữa các nodes

### Giao Thức Gossip

Khi một microservice đăng ký với một service discovery node:
- Thông tin chi tiết được chia sẻ ngay lập tức với các nodes khác thông qua **giao thức gossip**
- Tất cả nodes duy trì thông tin đồng bộ và cập nhật
- Đảm bảo tính nhất quán trên toàn service discovery layer

### Luồng Giao Tiếp

1. Microservices đăng ký khi khởi động với IP, hostname và cổng
2. Tín hiệu heartbeat đều đặn duy trì trạng thái sức khỏe
3. Client microservices truy vấn bằng tên dịch vụ logic (ví dụ: "accounts", "loans")
4. Service discovery layer trả về danh sách địa chỉ IP
5. Client thực hiện cân bằng tải và gọi dịch vụ đích

## Client-Side Caching

### Chiến Lược Cache

Để giảm gánh nặng cho service discovery layer:
1. Client microservices cache địa chỉ IP sau lần truy vấn đầu tiên
2. Các yêu cầu tiếp theo sử dụng địa chỉ IP đã cache
3. Cache tự động làm mới mỗi 10-20 giây
4. Cache invalidation xảy ra ngay lập tức khi có exception

### Lợi Ích

- Giảm tải cho service discovery layer
- Thời gian phản hồi nhanh hơn cho các yêu cầu tiếp theo
- Quản lý cache tự động ở hậu trường

### Cache Invalidation

Khi giao tiếp thất bại:
- Cache phía client bị vô hiệu hóa ngay lập tức
- Thông tin địa chỉ IP mới được lấy từ service discovery layer
- Đảm bảo kết nối với các instance dịch vụ khỏe mạnh

## Triển Khai Với Spring Cloud

Spring Cloud cung cấp các công cụ đơn giản và mạnh mẽ để triển khai client-side service discovery trong microservices Spring Boot. Framework tự động xử lý hầu hết độ phức tạp:

- Không cần code thủ công logic đăng ký dịch vụ
- Cơ chế caching tích hợp sẵn
- Tự động làm mới và vô hiệu hóa cache
- Tích hợp với các giải pháp service discovery phổ biến

### Yêu Cầu Cho Developer

Developers chỉ cần:
- Biết các dự án Spring Cloud nào cần sử dụng
- Cấu hình chúng đúng cách trong microservices
- Hiểu mô hình và kiến trúc tổng thể

## Ví Dụ Thực Tế

### Kịch Bản

- **Accounts microservice** cần giao tiếp với **Loans** và **Cards** microservices
- Nhiều instances của mỗi dịch vụ đang chạy

### Luồng Hoạt Động

1. Tất cả microservices đăng ký với service discovery layer khi khởi động
2. Accounts microservice kiểm tra cache cục bộ cho thông tin loans microservice
3. Nếu cache miss, truy vấn service discovery layer
4. Nhận danh sách địa chỉ IP và cache chúng
5. Áp dụng chiến lược cân bằng tải
6. Chuyển tiếp yêu cầu đến instance được chọn
7. Sử dụng địa chỉ đã cache cho các yêu cầu tương lai

### Khả Năng Mở Rộng

Trong production với 100+ microservices:
- Mỗi dịch vụ có thể có 10+ instances
- Client-side caching ngăn không làm quá tải service discovery layer
- Tự động làm mới cache đảm bảo thông tin cập nhật
- Xử lý exception kích hoạt cache invalidation ngay lập tức

## Kết Luận

Client-side service discovery cung cấp một mô hình linh hoạt và mạnh mẽ cho giao tiếp microservices. Mặc dù yêu cầu developer tham gia nhiều hơn so với server-side discovery, nó mang lại:

- Chi phí hạ tầng thấp hơn
- Kiểm soát tốt hơn về cân bằng tải
- Hiệu suất xuất sắc với client-side caching
- Triển khai đơn giản với Spring Cloud

Mô hình hoạt động trơn tru ở hậu trường khi được cấu hình đúng cách, cho phép developers tập trung vào logic nghiệp vụ thay vì lo lắng về hạ tầng.

---

**Bước Tiếp Theo**: Chi tiết triển khai với các dự án Spring Cloud và ví dụ cấu hình sẽ được đề cập trong các bài giảng tiếp theo.