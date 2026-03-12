# Giới Thiệu Spring Cloud Gateway

## Tổng Quan

Spring Cloud Gateway là một dự án trong Spring Cloud cho phép các lập trình viên dễ dàng tạo ra các edge service đạt chuẩn production và sẵn sàng triển khai. Gateway này đóng vai trò là điểm tiếp nhận cho mọi giao tiếp bên ngoài trong mạng lưới microservices của bạn.

## Tính Năng Chính

### Xây Dựng Trên Spring Reactive Framework

Spring Cloud Gateway được xây dựng trên nền tảng Spring Reactive framework, cho phép:
- Xử lý mượt mà mọi khối lượng công việc
- Xử lý hiệu quả lượng traffic lớn
- Hoạt động với yêu cầu bộ nhớ và thread tối thiểu
- Cung cấp các thao tác reactive không chặn (non-blocking)

### Đóng Vai Trò Gatekeeper (Người Gác Cổng)

Gateway nằm giữa các ứng dụng client và microservices, cung cấp:
- **Điểm Vào Tập Trung**: Mọi traffic đến đều phải đi qua gateway
- **Bảo Mật**: Các ứng dụng client không thể tương tác trực tiếp với từng microservice riêng lẻ
- **Trong Suốt Vị Trí**: Client không cần biết địa chỉ vật lý của các instance microservice

## Dễ Dàng Phát Triển

Xây dựng gateway với Spring Cloud Gateway rất đơn giản:
- Tương tự như xây dựng bất kỳ ứng dụng Spring Boot nào khác
- Yêu cầu code tối thiểu
- Cấu hình đơn giản
- Ít dependency cần thêm vào

Nếu bạn đã là lập trình viên Spring Boot, bạn sẽ thấy rất dễ dàng khi làm việc với Spring Cloud Gateway.

## Khả Năng và Trường Hợp Sử Dụng

### Định Tuyến Động (Dynamic Routing)

Gateway có thể định tuyến động các request dựa trên nhiều ngữ cảnh khác nhau:
- **Định Tuyến Theo Phiên Bản API**: Định tuyến request đến các microservice backend có phiên bản phù hợp dựa trên giá trị trong request header
- **Định Tuyến Dựa Trên Ngữ Cảnh**: Định tuyến thông minh dựa trên các thuộc tính của request

### Sticky Sessions

Hỗ trợ duy trì phiên làm việc của người dùng:
- Đảm bảo request của một người dùng cụ thể luôn đến cùng một instance microservice
- Duy trì tính nhất quán của session giữa các request

### Cross-Cutting Concerns (Mối Quan Tâm Xuyên Suốt)

Spring Cloud Gateway xử lý nhiều yêu cầu phi chức năng:
- Bảo mật
- Logging
- Auditing
- Thu thập metrics
- Giám sát
- Khả năng phục hồi (Resiliency)

### Điểm Thực Thi Chính Sách Tập Trung

Là một vị trí tập trung, gateway có thể thực thi:
- Chính sách định tuyến tĩnh và động
- Chính sách bảo mật
- Giới hạn tốc độ request (Rate limiting)
- Viết lại đường dẫn (Path rewriting)

## Spring Cloud Gateway vs. Zuul

Mặc dù **Zuul** là một lựa chọn phổ biến khác để xây dựng API gateway trong Java, Spring Cloud Gateway được ưa chuộng hơn vì:

| Tính Năng | Spring Cloud Gateway | Zuul |
|-----------|---------------------|------|
| Framework | Spring Reactor (Reactive) | Blocking |
| Hiệu Suất | Tốt hơn | Tốt |
| Tích Hợp Circuit Breaker | ✓ | Hạn chế |
| Tích Hợp Service Discovery | ✓ | ✓ |
| Non-blocking | ✓ | ✗ |

## Các Thành Phần Chính

### Predicates (Vị Từ)
Predicates được sử dụng để khớp các route dựa trên bất kỳ thuộc tính request nào, cho phép quyết định định tuyến linh hoạt.

### Filters (Bộ Lọc)
Filters dành riêng cho các route và có thể sửa đổi request và response khi chúng đi qua gateway.

### Điểm Tích Hợp
- **Circuit Breaker**: Hỗ trợ circuit breaker tích hợp sẵn
- **Spring Cloud Discovery Client**: Tích hợp với service discovery (ví dụ: Eureka Server)
- **Rate Limiting**: Khả năng giới hạn tốc độ request
- **Path Rewriting**: Sửa đổi đường dẫn động

## Tài Nguyên Chính Thức

Để biết thêm thông tin, truy cập dự án Spring Cloud Gateway chính thức tại [spring.io](https://spring.io):
1. Điều hướng đến Projects
2. Chọn Spring Cloud
3. Chọn Spring Cloud Gateway

### Mục Tiêu Dự Án

Theo tài liệu chính thức, Spring Cloud Gateway hướng đến:
- Cung cấp cách đơn giản và hiệu quả để định tuyến đến APIs
- Cung cấp các cross-cutting concerns như bảo mật, giám sát và khả năng phục hồi
- Cho phép dễ dàng triển khai predicates và filters
- Hỗ trợ giới hạn tốc độ request và viết lại đường dẫn

## Tóm Tắt

Spring Cloud Gateway là một giải pháp mạnh mẽ, sẵn sàng production để triển khai edge servers trong kiến trúc microservices. Tính chất reactive, dễ sử dụng và bộ tính năng toàn diện của nó làm cho nó trở thành lựa chọn xuất sắc để xử lý các yêu cầu API gateway trong các ứng dụng cloud-native hiện đại.

## Bước Tiếp Theo

Trong các bài giảng tiếp theo, chúng ta sẽ khám phá:
- Kiến trúc nội bộ của Spring Cloud Gateway
- Cách predicates và filters hoạt động
- Các ví dụ triển khai thực tế
- Các tùy chọn cấu hình nâng cao

---

*Tài liệu này là một phần của khóa học microservices toàn diện sử dụng Spring Boot và Spring Cloud.*