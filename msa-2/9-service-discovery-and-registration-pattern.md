# Mẫu Khám Phá và Đăng Ký Dịch Vụ trong Microservices

## Tổng Quan

Trong các ứng dụng cloud-native và kiến trúc microservices, mẫu Service Discovery (Khám phá dịch vụ) cung cấp giải pháp hiệu quả để khắc phục những hạn chế của load balancer truyền thống. Mẫu này giải quyết thách thức cơ bản về cách các microservices giao tiếp với nhau trong môi trường động, nơi địa chỉ IP thay đổi thường xuyên.

## Service Discovery là gì?

Mẫu Service Discovery liên quan đến việc theo dõi và lưu trữ tất cả thông tin về các instance dịch vụ đang chạy trong một **service registry** (sổ đăng ký dịch vụ). Cách tiếp cận tập trung này cho phép các microservices định vị và giao tiếp với nhau một cách hiệu quả trên mạng.

### Các Thành Phần Chính

1. **Service Registry (Sổ đăng ký dịch vụ)**: Một máy chủ trung tâm (hoặc nhiều máy chủ) duy trì cái nhìn toàn cục về tất cả các instance dịch vụ đang chạy và địa chỉ của chúng.

2. **Service Registration (Đăng ký dịch vụ)**: Quá trình mà các instance microservice tự đăng ký với service registry khi chúng khởi động.

3. **Service Discovery (Khám phá dịch vụ)**: Cơ chế cho phép các microservices truy vấn registry để tìm và kết nối với các dịch vụ khác.

## Cách Thức Hoạt Động

### Quy Trình Đăng Ký

Khi một instance microservice mới khởi động:

1. **Đăng ký ban đầu**: Instance microservice kết nối với máy chủ trung tâm và đăng ký địa chỉ IP và thông tin cổng của nó
2. **Giám sát sức khỏe**: Instance gửi heartbeat định kỳ để xác nhận trạng thái sức khỏe của nó
3. **Hủy đăng ký tự động**: Khi heartbeat dừng lại hoặc instance tắt, nó sẽ tự động bị xóa khỏi registry

### Khám Phá và Giao Tiếp

Khi một microservice cần giao tiếp với dịch vụ khác:

1. Dịch vụ gọi (ví dụ: accounts microservice) truy vấn service registry
2. Registry trả về các instance khả dụng của dịch vụ đích (ví dụ: loans microservice)
3. Nếu có nhiều instance, load balancing sẽ tự động được áp dụng để phân phối workload

## Cân Bằng Tải (Load Balancing)

Service registry công nhận rằng nhiều instance của cùng một ứng dụng có thể hoạt động đồng thời. Khi có nhiều instance khả dụng:

- Registry thực hiện tra cứu để xác định các địa chỉ IP khả dụng
- Bên dưới, nó áp dụng chiến lược cân bằng tải
- Workload được phân phối đều cho tất cả các instance đang chạy

## Các Loại Service Discovery

### 1. Client-Side Service Discovery (Khám phá dịch vụ phía client)
- Client (microservice gọi) chịu trách nhiệm xác định vị trí mạng của các instance dịch vụ khả dụng
- Client truy vấn service registry và thực hiện load balancing
- **Cách tiếp cận này được đề cập trong phần này**

### 2. Server-Side Service Discovery (Khám phá dịch vụ phía server)
- Một router hoặc load balancer truy vấn service registry
- Client thực hiện request đến router, router xử lý service discovery
- **Cách tiếp cận này sẽ được demo sau khi triển khai với Kubernetes**

## Lợi Ích

1. **Hỗ trợ môi trường động**: Xử lý thay đổi địa chỉ IP trong quá trình auto-scaling hoặc các tình huống lỗi
2. **Load Balancing tự động**: Phân phối traffic giữa nhiều instance mà không cần cấu hình thủ công
3. **Tính khả dụng cao**: Tự động loại bỏ các instance không khỏe mạnh khỏi rotation
4. **Giao tiếp đơn giản**: Microservices không cần biết vị trí chính xác của các dịch vụ khác

## Chiến Lược Triển Khai

Để triển khai mẫu này:

1. Tạo một máy chủ trung tâm riêng biệt dành cho service discovery và registration
2. Cấu hình microservices tự đăng ký khi khởi động
3. Triển khai cơ chế heartbeat để giám sát sức khỏe
4. Cho phép microservices truy vấn registry để tìm vị trí dịch vụ
5. Cấu hình các chiến lược load balancing phía client

## Tóm Tắt

Mẫu Service Discovery và Registration rất quan trọng đối với kiến trúc microservices vì nó:

- Giải quyết vấn đề về cách các microservices giao tiếp với nhau
- Loại bỏ nhu cầu hardcode địa chỉ IP và cổng
- Cung cấp khả năng load balancing tự động
- Thích ứng với các tình huống scaling động và lỗi
- Duy trì cái nhìn tập trung về tất cả các instance dịch vụ đang chạy

Mẫu này là nền tảng để xây dựng các ứng dụng cloud-native có khả năng phục hồi và mở rộng, nơi các instance dịch vụ có thể được tạo, hủy và scale động mà không cần can thiệp thủ công.

## Các Bước Tiếp Theo

Trong các bài giảng tiếp theo, chúng ta sẽ đi sâu vào:
- Triển khai chi tiết client-side service discovery
- Ví dụ thực tế sử dụng Spring Boot và Spring Cloud
- Cấu hình và các phương pháp hay nhất
- Tích hợp với các mẫu microservices khác