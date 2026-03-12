# Quản Lý Cấu Hình trong Spring Boot Microservices

## Giới Thiệu

Trong bài giảng này, chúng ta sẽ khám phá các nguyên tắc cơ bản về quản lý cấu hình trong các ứng dụng Spring Boot, đặc biệt trong bối cảnh kiến trúc microservices. Vì hầu hết các nhà phát triển và tổ chức trong hệ sinh thái Java sử dụng Spring Boot để phát triển microservices, việc hiểu về quản lý cấu hình là rất quan trọng để xây dựng các ứng dụng có khả năng mở rộng và dễ bảo trì.

## Thách Thức về Cấu Hình

### Vấn Đề Cốt Lõi

Thách thức chính mà chúng ta gặp phải là **tách biệt các thuộc tính cho microservices** sao cho cùng một artifact code bất biến có thể được sử dụng trên các môi trường khác nhau (phát triển, QA, production) mà không cần xây dựng lại ứng dụng.

### Mục Tiêu

- Tách biệt cấu hình khỏi mã nguồn
- Tách biệt cấu hình ra bên ngoài để hỗ trợ nhiều môi trường
- Cho phép thay đổi cấu hình mà không cần triển khai lại code

## Tách Biệt Cấu Hình trong Spring Boot

Spring Boot cung cấp hỗ trợ mạnh mẽ cho việc tách biệt cấu hình, cho phép bạn làm việc với cùng một mã ứng dụng trên các môi trường khác nhau mà không cần xây dựng lại.

### Các Phương Pháp Nguồn Cấu Hình

Spring Boot hỗ trợ nhiều phương pháp để cung cấp cấu hình:

1. **Tệp Thuộc Tính**: `application.properties` hoặc `application.yml`
2. **Biến Môi Trường**: Các biến môi trường cấp hệ điều hành
3. **Tham Số Dòng Lệnh**: Các tham số được truyền trong thời gian chạy khi khởi động ứng dụng
4. **Java System Properties**: Các thuộc tính hệ thống JVM
5. **JNDI Attributes**: Các thuộc tính Java Naming and Directory Interface
6. **Servlet Config Init Parameters**: Các tham số khởi tạo Servlet

## Thứ Tự Ưu Tiên Cấu Hình

Khi cùng một thuộc tính được định nghĩa ở nhiều vị trí, Spring Boot tuân theo thứ tự ưu tiên cụ thể (từ thấp đến cao):

1. **Tệp Application Properties/YAML** (Ưu tiên thấp nhất)
2. **Biến Môi Trường Hệ Điều Hành**
3. **Java System Properties**
4. **JNDI Attributes**
5. **Servlet Config Init Parameters**
6. **Tham Số Dòng Lệnh** (Ưu tiên cao nhất)

> **Quan Trọng**: Các giá trị ưu tiên thấp hơn sẽ bị ghi đè bởi các giá trị ưu tiên cao hơn. Tham số dòng lệnh có ưu tiên cao nhất và sẽ ghi đè tất cả các cấu hình khác.

## Hành Vi Cấu Hình Mặc Định

Theo mặc định, Spring Boot tìm kiếm cấu hình trong:
- `application.properties`
- `application.yml` (hoặc `application.yaml`)

Các tệp này được đặt trong vị trí classpath và thường được sử dụng trong các microservices như accounts, loans và cards.

### Hạn Chế của Phương Pháp Mặc Định

Mặc dù tiện lợi, việc lưu trữ tất cả cấu hình trong các tệp thuộc tính trong mã nguồn có những hạn chế:
- Cấu hình được đóng gói cùng với mã nguồn
- Khó thay đổi cấu hình mà không thay đổi code
- Không phù hợp cho các giá trị cụ thể theo môi trường (thông tin đăng nhập database, URLs, v.v.)

## Đọc Thuộc Tính trong Spring Boot

Spring Boot cung cấp ba phương pháp phổ biến để đọc thuộc tính trong logic nghiệp vụ của bạn:

### 1. Annotation @Value

Annotation `@Value` cho phép bạn inject các giá trị thuộc tính riêng lẻ vào các trường Java.

**Cách hoạt động:**
```java
@Value("${property.key.name}")
private String propertyValue;
```

- Định nghĩa một trường Java trong logic nghiệp vụ của bạn
- Đánh dấu nó với `@Value` và chỉ định key thuộc tính
- Spring Boot tự động điền giá trị vào trường trong quá trình khởi động ứng dụng
- Giá trị được giải quyết từ tất cả các nguồn đã cấu hình, tôn trọng thứ tự ưu tiên

**Trường Hợp Sử Dụng**: Đọc các thuộc tính riêng lẻ khi bạn chỉ có một vài giá trị cấu hình.

### 2. Environment Interface

Interface `Environment` cung cấp quyền truy cập vào các thuộc tính từ môi trường runtime của ứng dụng, đặc biệt hữu ích cho các biến môi trường.

**Cách hoạt động:**
```java
@Autowired
private Environment environment;

public void someMethod() {
    String value = environment.getProperty("property.name");
}
```

- Autowire interface `Environment` vào class của bạn
- Sử dụng phương thức `getProperty()` để lấy giá trị thuộc tính
- Truyền tên thuộc tính biến môi trường làm tham số

**Trường Hợp Sử Dụng**: Truy cập các biến môi trường hệ điều hành và thông tin nhạy cảm được cấu hình bởi quản trị viên máy chủ.

### 3. Annotation @ConfigurationProperties (Được Khuyến Nghị)

Đây là phương pháp được khuyến nghị nhất khi xử lý nhiều thuộc tính liên quan.

**Ưu Điểm:**
- Tránh hardcode các key thuộc tính
- Xử lý nhiều thuộc tính một cách hiệu quả
- Cung cấp binding cấu hình an toàn về kiểu dữ liệu
- Tổ chức và bảo trì tốt hơn

**Cách hoạt động:**
```java
@ConfigurationProperties(prefix = "myapp")
public class MyConfig {
    private String property1;
    private int property2;
    
    // Getters và setters
}
```

**Tệp cấu hình:**
```yaml
myapp:
  property1: value1
  property2: 123
```

**Các Điểm Chính:**
- Định nghĩa các thuộc tính với prefix chung trong tệp thuộc tính của bạn
- Tạo một class Java được đánh dấu với `@ConfigurationProperties`
- Chỉ định giá trị prefix trong annotation
- Định nghĩa các trường khớp với tên và kiểu thuộc tính
- Bao gồm getters và setters cho tất cả các trường
- Spring Boot tự động bind các giá trị thuộc tính vào các trường trong quá trình khởi động

**Trường Hợp Sử Dụng**: Quản lý nhiều thuộc tính cấu hình liên quan với tổ chức tốt hơn và an toàn về kiểu dữ liệu.

## So Sánh Các Phương Pháp

| Phương Pháp | Tốt Nhất Cho | Nhược Điểm |
|-------------|--------------|------------|
| @Value | Ít thuộc tính riêng lẻ | Keys bị hardcode, một thuộc tính một lúc |
| Environment | Biến môi trường, dữ liệu nhạy cảm | Truy xuất thủ công, keys bị hardcode |
| @ConfigurationProperties | Nhiều thuộc tính liên quan | Yêu cầu thiết lập class bổ sung |

## Thực Hành Tốt Nhất

1. **Sử dụng @ConfigurationProperties** cho các nhóm thuộc tính liên quan
2. **Tách biệt dữ liệu nhạy cảm** bằng cách sử dụng biến môi trường
3. **Ghi nhớ thứ tự ưu tiên** khi ghi đè thuộc tính
4. **Tài liệu hóa các thuộc tính** của bạn để team hiểu rõ
5. **Sử dụng phương pháp phù hợp** dựa trên số lượng thuộc tính

## Bước Tiếp Theo

Trong các bài giảng sắp tới, chúng ta sẽ:
- Triển khai cả ba phương pháp trong microservices của chúng ta
- Khám phá các demo thực tế của từng phương pháp
- Thảo luận về nhược điểm của các phương pháp cấu hình Spring Boot cơ bản
- Tìm hiểu về quản lý cấu hình nâng cao với Spring Cloud Config Server

## Tóm Tắt

Spring Boot cung cấp quản lý cấu hình linh hoạt thông qua nhiều phương pháp tách biệt. Hiểu thứ tự ưu tiên và chọn phương pháp phù hợp để đọc thuộc tính là điều cần thiết để xây dựng microservices có thể bảo trì. Trong khi các phương pháp cơ bản hoạt động tốt cho các tình huống đơn giản, các ứng dụng doanh nghiệp hưởng lợi từ các giải pháp nâng cao như Spring Cloud Config Server để quản lý cấu hình tập trung.