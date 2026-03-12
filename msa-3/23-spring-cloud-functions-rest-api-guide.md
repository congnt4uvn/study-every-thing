# Spring Cloud Functions: Hướng Dẫn Triển Khai REST API

## Tổng Quan

Hướng dẫn này trình bày sức mạnh và tính linh hoạt của Spring Cloud Functions trong việc xây dựng microservices hướng sự kiện. Bạn sẽ học cách viết logic nghiệp vụ dưới dạng các hàm và công khai chúng theo nhiều cách - REST APIs, xử lý sự kiện, hoặc serverless functions.

## Hiểu Về Spring Cloud Functions

Spring Cloud Functions cho phép lập trình viên viết logic nghiệp vụ dưới dạng các hàm đơn giản mà không cần lo lắng về cơ sở hạ tầng bên dưới. Các hàm này có thể:

- Được công khai như REST APIs
- Tích hợp với event brokers (RabbitMQ, Kafka)
- Triển khai lên các nền tảng serverless (AWS Lambda)

## Thêm Hỗ Trợ REST API

Để công khai các hàm của bạn thành REST APIs, thêm dependency sau vào `pom.xml`:

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-function-web</artifactId>
</dependency>
```

Thay thế dependency `spring-cloud-function-context` bằng `spring-cloud-starter-function-web`.

## Các Bước Triển Khai

### 1. Cấu Hình Maven

Sau khi thêm dependency:
1. Reload các thay đổi Maven
2. Build project
3. Khởi động ứng dụng ở chế độ debug

Ứng dụng sẽ khởi động trên cổng mặc định 8080.

### 2. Tự Động Công Khai Hàm

Khi ứng dụng khởi động, Spring Cloud Functions tự động:
- Nhận diện tất cả các function beans
- Công khai chúng thành REST endpoints
- Ánh xạ tên hàm thành đường dẫn API

### 3. Kiểm Thử Các Hàm Riêng Lẻ

#### Hàm Email

**Endpoint:** `POST http://localhost:8080/email`

**Request Body:**
```json
{
    "accountNumber": "1234567890",
    "name": "Nguyễn Văn A",
    "email": "nguyen@example.com",
    "mobileNumber": "0123456789"
}
```

Hàm nhận đối tượng `AccountsMsgDto` và xử lý gửi email.

**Response:** Trả về cùng đối tượng `AccountsMsgDto` đã gửi trong request.

**Console Output:** "Sending email with the details..."

#### Hàm SMS

**Endpoint:** `POST http://localhost:8080/sms`

**Request Body:**
```json
{
    "accountNumber": "1234567890",
    "name": "Nguyễn Văn A",
    "email": "nguyen@example.com",
    "mobileNumber": "0123456789"
}
```

Hàm SMS trả về số tài khoản (kiểu Long) làm kết quả đầu ra.

**Response:** Chỉ trả về giá trị số tài khoản.

**Console Output:** "Sending SMS with the details..."

## Kết Hợp Các Hàm (Function Composition)

### Cấu Hình

Tạo hoặc sửa file `application.yml`:

```yaml
server:
  port: 9010

spring:
  application:
    name: message
  cloud:
    function:
      definition: email|sms
```

### Các Điểm Cấu Hình Chính

- **Cấu Hình Cổng:** Đặt là 9010 để tránh xung đột với accounts microservice (cổng 8080)
- **Tên Ứng Dụng:** "message" - dùng để nhận diện service
- **Function Definition:** Sử dụng ký tự pipe `|` để kết hợp nhiều hàm thành một đơn vị logic duy nhất

### Cách Hoạt Động Của Function Composition

Ký tự pipe (`|`) cho phép bạn kết hợp bất kỳ số lượng hàm nào:
- Các hàm thực thi tuần tự
- Đầu ra của hàm này trở thành đầu vào cho hàm tiếp theo
- Tên endpoint kết hợp được tạo bằng cách nối các tên hàm

### Endpoint Hàm Kết Hợp

**Endpoint:** `POST http://localhost:9010/emailsms`

Khi gọi hàm kết hợp:
1. Gửi request theo định dạng mà hàm đầu tiên (email) yêu cầu
2. Cả hai hàm thực thi như một đơn vị logic duy nhất
3. Hàm email xử lý trước, sau đó đến hàm SMS
4. Kết quả cuối cùng là đầu ra từ hàm cuối cùng trong chuỗi (số tài khoản)

**Request Mẫu:**
```json
{
    "accountNumber": "1234567890",
    "name": "Nguyễn Văn A",
    "email": "nguyen@example.com",
    "mobileNumber": "0123456789"
}
```

**Kết Quả Mẫu:**
- Console logs: "Sending email..." theo sau là "Sending SMS..."
- Response: Số tài khoản (từ đầu ra của hàm SMS)

### Kiểm Thử Hàm Kết Hợp

1. Xóa console để thấy logs mới
2. Gọi endpoint `emailsms`
3. Quan sát cả hai log statements xuất hiện
4. Nhận số tài khoản trong response

Điều này xác nhận cả hai hàm đã thực thi như một đơn vị logic duy nhất.

## Lợi Ích Chính

1. **Không Cần Phát Triển REST API Thủ Công:** Các hàm tự động trở thành REST endpoints chỉ bằng cách thêm một dependency
2. **Tính Linh Hoạt:** Cùng một hàm có thể hoạt động như REST APIs, event handlers, hoặc serverless functions
3. **Dễ Dàng Kết Hợp:** Kết hợp nhiều hàm bằng ký tự pipe mà không cần code thêm
4. **Tùy Chọn Triển Khai:** Triển khai lên nhiều nền tảng khác nhau mà không cần thay đổi code

## Gọi Riêng Lẻ vs Kết Hợp

### Các Hàm Riêng Lẻ
- Ứng dụng client có thể gọi các hàm cụ thể một cách độc lập
- Dùng endpoint `email` cho giao tiếp chỉ qua email
- Dùng endpoint `sms` cho giao tiếp chỉ qua SMS
- Mỗi endpoint vẫn khả dụng ngay cả khi đã cấu hình function composition

### Các Hàm Kết Hợp
- Gọi nhiều hàm như một đơn vị logic duy nhất
- Dùng tên endpoint kết hợp (`emailsms`) để kích hoạt cả hai phương thức giao tiếp
- Các hàm thực thi tuần tự như đã định nghĩa trong cấu hình
- Không ảnh hưởng đến khả năng sử dụng các hàm riêng lẻ

## Điều Kỳ Diệu Của Spring Cloud Functions

**Không Cần REST Controller:** Bạn không cần viết bất kỳ REST controllers hoặc API endpoints thủ công. Chỉ cần:
1. Viết logic nghiệp vụ của bạn dưới dạng các hàm
2. Thêm dependency `spring-cloud-starter-function-web`
3. Các hàm tự động trở thành REST APIs

**Sức Mạnh:** Abstraction này cho phép bạn tập trung vào logic nghiệp vụ trong khi Spring Cloud Functions xử lý cơ sở hạ tầng.

## Bước Tiếp Theo: Tích Hợp Hướng Sự Kiện

Mặc dù REST APIs hữu ích cho việc demo, sức mạnh thực sự nằm ở việc tích hợp với event brokers:

1. **Tích Hợp Spring Cloud Stream:** Kết hợp Spring Cloud Functions với Spring Cloud Stream
2. **Tích Hợp RabbitMQ:** Kết nối các hàm với message brokers
3. **Kiến Trúc Hướng Sự Kiện:** Xây dựng microservices thực sự reactive

### Chuẩn Bị Cho Tích Hợp Event Broker

Để chuyển từ REST APIs sang kiến trúc hướng sự kiện:

1. Comment dependency `spring-cloud-starter-function-web`
2. Giữ lại các properties function definition (sẽ dùng với event brokers)
3. Các properties trong `application.yml` sẽ được tái sử dụng cho cấu hình event broker

```xml
<!-- Comment để chuyển sang phương pháp hướng sự kiện -->
<!--
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-function-web</artifactId>
</dependency>
-->
```

**Lưu ý:** Bạn không cần xóa các properties - chúng sẽ được tận dụng khi tích hợp với event brokers.

## Khoảnh Khắc "Wow"

Khi Spring Cloud Functions được tích hợp với Spring Cloud Stream và RabbitMQ, bạn sẽ trải nghiệm sức mạnh thực sự của kiến trúc này:
- Cùng một logic nghiệp vụ hoạt động trên nhiều cơ sở hạ tầng khác nhau
- Chuyển đổi giữa REST APIs, event brokers, hoặc serverless mà không cần thay đổi code
- Abstraction hoàn hảo cho các ứng dụng cloud-native hiện đại

## Kết Luận

Spring Cloud Functions cung cấp một abstraction mạnh mẽ để xây dựng logic nghiệp vụ với các đặc điểm:
- **Độc lập với cơ sở hạ tầng:** Hoạt động trên nhiều nền tảng khác nhau
- **Dễ dàng kiểm thử:** Các hàm đơn giản dễ dàng unit test
- **Linh hoạt trong triển khai:** Triển khai như REST APIs, event handlers, hoặc serverless
- **Hoàn hảo cho microservices hướng sự kiện:** Phù hợp tự nhiên với kiến trúc reactive

Sự kết hợp của Spring Cloud Functions với Spring Cloud Stream và RabbitMQ tạo ra nền tảng vững chắc cho kiến trúc microservices hiện đại.

## Những Điểm Chính Cần Nhớ

1. Viết logic nghiệp vụ dưới dạng các hàm đơn giản
2. Thêm một dependency để công khai như REST APIs
3. Kết hợp các hàm bằng ký tự pipe
4. Cùng một code hoạt động cho REST, events, hoặc serverless
5. Tập trung vào logic nghiệp vụ, không phải cơ sở hạ tầng

## Tài Liệu Tham Khảo

- Tài Liệu Spring Cloud Functions
- Spring Cloud Stream
- Tích Hợp RabbitMQ
- Các Mẫu Microservices Hướng Sự Kiện
- AWS Lambda với Spring Cloud Functions