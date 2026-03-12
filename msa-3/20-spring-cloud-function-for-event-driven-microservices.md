# Spring Cloud Function cho Microservices Hướng Sự Kiện

## Giới Thiệu về Message Microservice

Để bắt đầu triển khai giao tiếp bất đồng bộ với sự trợ giúp của RabbitMQ, trước tiên chúng ta cần tạo **message microservice**.

Message microservice này chịu trách nhiệm cho:
- Nhận tin nhắn từ message broker
- Gửi thông tin liên lạc đến người dùng cuối qua SMS và email

## Tại Sao Sử Dụng Spring Cloud Function?

Thay vì xây dựng microservice này bằng cách tiếp cận truyền thống với các REST services (các annotation như RestController, GetMapping, PostMapping), chúng ta sẽ tận dụng **Spring Cloud Function**.

### Spring Cloud Function là gì?

Spring Cloud Function hỗ trợ phát triển logic nghiệp vụ bằng cách sử dụng các hàm (functions). Các nhà phát triển chỉ cần viết logic nghiệp vụ của họ bên trong các hàm, và các vấn đề về cơ sở hạ tầng sẽ được Spring Cloud Function framework đảm nhiệm.

## Các Giao Diện Function Chuẩn

Spring Cloud Function tận dụng các giao diện function chuẩn được giới thiệu trong Java 8:

### 1. Supplier (Nhà Cung Cấp)
- **Định nghĩa**: Một hàm hoặc biểu thức lambda tạo ra đầu ra mà không yêu cầu bất kỳ đầu vào nào
- **Còn được gọi là**: Producer (Nhà sản xuất), Publisher (Nhà xuất bản), hoặc Source (Nguồn)
- **Đặc điểm**: 
  - Không yêu cầu đầu vào
  - Luôn tạo ra đầu ra
  - Cung cấp đầu ra mà không cần đầu vào

### 2. Function (Hàm)
- **Định nghĩa**: Nhận đầu vào và tạo ra đầu ra
- **Còn được gọi là**: Processor (Bộ xử lý)
- **Đặc điểm**:
  - Nhận một đầu vào
  - Xử lý đầu vào
  - Tạo ra đầu ra

### 3. Consumer (Người Tiêu Dùng)
- **Định nghĩa**: Một hàm hoặc biểu thức lambda tiêu thụ đầu vào nhưng không tạo ra đầu ra
- **Còn được gọi là**: Subscriber (Người đăng ký) hoặc Sink (Bồn chứa)
- **Đặc điểm**:
  - Luôn có đầu vào
  - Không bao giờ tạo ra đầu ra
  - Chỉ tiêu thụ dữ liệu

## Ưu Điểm của Spring Cloud Function

### 1. Linh Hoạt trong Các Mô Hình Triển Khai
- **Mặc định**: Tất cả các hàm tự động được phơi bày dưới dạng REST APIs
- **Event Brokers**: Có thể tích hợp với RabbitMQ, Apache Kafka bằng cách thêm Spring Cloud Stream
- **Serverless**: Có thể được đóng gói cho AWS Lambda và các môi trường serverless khác

### 2. Các Phương Pháp Phát Triển
- Phương pháp Reactive (Phản ứng)
- Phương pháp Imperative (Mệnh lệnh)
- Phương pháp Hybrid (Kết hợp)

### 3. Các Hàm POJO Đơn Giản
- Logic nghiệp vụ được triển khai với các hàm POJO đơn giản
- Nhiều hàm có thể được kết hợp để đạt được đầu ra mong muốn

### 4. Tùy Chọn Triển Khai Đa Dạng
- HTTP endpoints với REST services
- Stream dữ liệu bằng cách tích hợp với Apache Kafka hoặc RabbitMQ sử dụng Spring Cloud Stream
- Triển khai standalone cho các môi trường mục tiêu như AWS Lambda

### 5. Độc Lập với Cơ Sở Hạ Tầng
Logic nghiệp vụ tương tự được viết bằng functions có thể được sử dụng như:
- REST APIs
- Ứng dụng streaming dữ liệu
- Triển khai serverless

## Tại Sao Chọn Spring Cloud Function Thay Vì REST APIs Truyền Thống?

Khi xây dựng với REST APIs truyền thống, bạn chỉ giới hạn ở các tình huống mà REST được hỗ trợ. Spring Cloud Function cung cấp:

- **Linh hoạt**: Dễ dàng di chuyển giữa các công nghệ với cấu hình tối thiểu
- **Tách rời**: Chu kỳ phát triển của logic nghiệp vụ được tách rời khỏi các runtime targets cụ thể
- **Khả năng thích ứng**: Khi yêu cầu về cơ sở hạ tầng thay đổi, chỉ cần thay đổi tối thiểu
- **Tập trung**: Các nhà phát triển tập trung vào logic nghiệp vụ; cơ sở hạ tầng được xử lý thông qua cấu hình trong `application.yml`

## Trường Hợp Sử Dụng Tốt Nhất: Kiến Trúc Hướng Sự Kiện

Spring Cloud Function phù hợp nhất cho kiến trúc hướng sự kiện vì:
- Functions cung cấp tính linh hoạt để triển khai logic nghiệp vụ ở bất cứ đâu
- Dễ dàng di chuyển giữa các công nghệ
- Yêu cầu thay đổi cấu hình tối thiểu
- Cùng một code có thể chạy như web endpoint, stream processor, hoặc task

## Hỗ Trợ Nền Tảng

Spring Cloud Function hỗ trợ tích hợp với các nhà cung cấp cloud lớn:
- **AWS Lambda**
- **Microsoft Azure Functions**
- **Google Cloud Functions**
- **Apache OpenWhisk**

## Các Tùy Chọn Triển Khai

1. **Ứng dụng Web Standalone**: Triển khai như ứng dụng web truyền thống
2. **Ứng dụng Streaming Standalone**: Triển khai cho xử lý streaming dữ liệu
3. **Packaged Function**: Đóng gói và triển khai lên nhiều nền tảng khác nhau
4. **Nền tảng Serverless**: Triển khai lên AWS Lambda, Azure, Google Cloud Functions

## Mục Tiêu Triển Khai

Spring Cloud Function thúc đẩy và triển khai:
- Logic nghiệp vụ thông qua functions
- Tách rời chu kỳ phát triển khỏi các runtime targets cụ thể
- Cùng một code chạy như:
  - Web endpoints (REST APIs)
  - Stream processors
  - Tasks
  - Ứng dụng standalone (local hoặc môi trường PaaS)

## Các Bước Tiếp Theo

Trong các bài giảng sắp tới, chúng ta sẽ xây dựng message microservice của mình bằng cách tận dụng Spring Cloud Function, minh họa cách triển khai microservices hướng sự kiện bằng framework mạnh mẽ này.

---

*Phương pháp này đảm bảo các microservices của chúng ta linh hoạt, dễ bảo trì và sẵn sàng cho kiến trúc cloud-native hiện đại.*