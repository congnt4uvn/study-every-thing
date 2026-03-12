# Các Tùy Chọn Triển Khai Distributed Tracing cho Microservices

## Tổng Quan

Tài liệu này khám phá các tùy chọn có sẵn để triển khai distributed tracing (truy vết phân tán) trong microservices Java Spring Boot, so sánh các phương pháp khác nhau và giải thích tại sao OpenTelemetry là giải pháp được khuyến nghị.

## Các Tùy Chọn Có Sẵn

### 1. Spring Cloud Sleuth (Đã Ngừng Phát Triển)

Spring Cloud Sleuth là một dự án Spring Cloud được thiết kế để giúp triển khai distributed tracing trong microservices.

**Cách thức hoạt động:**
- Tự động thêm thông tin metadata, trace ID và span ID vào tất cả logs được tạo trong microservices
- Nhà phát triển không cần phải sửa đổi các câu lệnh log
- Chỉ cần thêm dependencies của Spring Cloud Sleuth
- Có thể tích hợp với Zipkin để xác định chi tiết truy vết và các điểm nghẽn hiệu suất

**Tại sao chúng ta không sử dụng:**
- Nhóm Spring Cloud Sleuth đã thông báo rằng phiên bản 3.1 sẽ là phiên bản nhỏ cuối cùng
- Dự án đang bị ngừng phát triển vì chức năng tracing đang được chuyển sang Micrometer Tracing
- Được coi là phương pháp lỗi thời mặc dù nhiều blog và khóa học vẫn đang giảng dạy nó

### 2. Micrometer Tracing

Micrometer Tracing là sản phẩm kế nhiệm của Spring Cloud Sleuth, được xây dựng trong cùng dự án Micrometer cung cấp khả năng expose metrics cho Prometheus.

**Tính năng:**
- Tài liệu toàn diện về dependencies, chi tiết triển khai, span IDs và trace IDs
- Tích hợp với Open Zipkin và OpenTelemetry
- Là một phần của hệ sinh thái Micrometer đã được thiết lập

**Hạn chế:**
- Yêu cầu nhiều thay đổi cấu hình và thiết lập properties từ nhà phát triển
- **Chỉ dành cho Java**: Chỉ có thể được sử dụng trong các ứng dụng Java
- Triển khai phức tạp hơn so với các phương án thay thế

### 3. OpenTelemetry (Được Khuyến Nghị)

OpenTelemetry là một framework observability mã nguồn mở, không phụ thuộc vào nhà cung cấp, được duy trì bởi Cloud Native Computing Foundation (CNCF).

**Ưu điểm:**
- **Hỗ trợ đa ngôn ngữ**: Hoạt động với C++, .NET, Erlang, Go, Java, JavaScript, PHP, Python, Ruby, Rust, Swift và nhiều ngôn ngữ khác
- **Triển khai dễ dàng**: Cực kỳ dễ dàng để thiết lập distributed tracing
- **Tích hợp framework**: Tích hợp với các framework phổ biến như Spring, ASP.NET, Express và Quarkus
- **Bền vững**: Có thể được sử dụng trên các ngăn xếp công nghệ khác nhau trong tổ chức của bạn

## Triển Khai OpenTelemetry

### Phương Pháp Automatic Instrumentation

OpenTelemetry cung cấp cả manual và automatic instrumentation. Chúng ta sẽ sử dụng **automatic instrumentation** vì nó yêu cầu ít thay đổi mã nguồn nhất.

### Các Bước Triển Khai

1. **Thêm OpenTelemetry Java Agent JAR** vào classpath của ứng dụng

2. **Cấu hình Java Agent** bằng một trong các phương pháp sau:

   **Tùy chọn A: Tham số dòng lệnh**
   ```bash
   java -javaagent:path/to/opentelemetry-javaagent.jar -jar your-application.jar
   ```

   **Tùy chọn B: Biến môi trường**
   ```bash
   JAVA_TOOL_OPTIONS=-javaagent:path/to/opentelemetry-javaagent.jar
   ```

3. **Đặt tên service** bằng một trong các phương pháp sau:

   **Tùy chọn A: System property**
   ```bash
   -Dotel.service.name=your-service-name
   ```

   **Tùy chọn B: Biến môi trường**
   ```bash
   OTEL_SERVICE_NAME=your-service-name
   ```

### Lợi Ích Chính

- **Thay đổi mã nguồn tối thiểu**: Không cần sửa đổi mã ứng dụng hiện có
- **Automatic instrumentation**: Chỉ cần đảm bảo JAR có trong classpath
- **Theo dõi metadata**: Tên service trở thành một phần của metadata trong distributed tracing
- **Tương thích đa nền tảng**: Cùng một phương pháp hoạt động trên các ngôn ngữ lập trình khác nhau

## Kết Luận

OpenTelemetry là phương pháp được khuyến nghị để triển khai distributed tracing trong microservices vì:
- Dễ dàng triển khai với cấu hình tối thiểu
- Hỗ trợ đa ngôn ngữ cho các ngăn xếp công nghệ đa dạng
- Được duy trì tích cực dưới CNCF
- Không phụ thuộc nhà cung cấp và mã nguồn mở
- Tích hợp mạnh mẽ với các framework hiện đại

Bằng cách sử dụng automatic instrumentation với OpenTelemetry Java Agent, bạn có thể triển khai distributed tracing với những thay đổi rất tối thiểu đối với kiến trúc microservices của mình.

## Tài Liệu Tham Khảo

- [Tài Liệu Chính Thức OpenTelemetry](https://opentelemetry.io/docs/)
- [OpenTelemetry Java - Automatic Instrumentation](https://opentelemetry.io/docs/languages/java/automatic/)
- [Cloud Native Computing Foundation](https://www.cncf.io/)