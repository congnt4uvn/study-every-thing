# Spring Boot Profiles cho Cấu Hình Theo Môi Trường

## Tổng Quan

Spring Boot profiles cung cấp một cơ chế mạnh mẽ để quản lý các cấu hình theo từng môi trường cụ thể trong các ứng dụng microservices. Tính năng này cho phép bạn duy trì các giá trị thuộc tính khác nhau cho các môi trường khác nhau mà không cần xây dựng lại ứng dụng.

## Thách Thức

Khi triển khai microservices trên nhiều môi trường (development, QA, production), việc sử dụng cùng một giá trị thuộc tính cho tất cả các môi trường tạo ra những thách thức đáng kể:

- Thông tin xác thực cơ sở dữ liệu phải khác nhau giữa các môi trường
- Cài đặt cấu hình cần các giá trị cụ thể cho từng môi trường
- Yêu cầu bảo mật thay đổi theo môi trường
- Phân bổ tài nguyên khác nhau dựa trên nhu cầu môi trường

## Spring Boot Profiles Là Gì?

Spring Boot profiles là công cụ để nhóm các cấu hình và thuộc tính dựa trên môi trường mục tiêu. Chúng cho phép bạn:

- Tạo các bộ file cấu hình khác nhau
- Kích hoạt cấu hình cụ thể dựa trên môi trường hiện tại
- Chạy cùng một mã nguồn với các thuộc tính riêng cho từng môi trường
- Kiểm soát việc tạo bean dựa trên profile đang hoạt động

## Lợi Ích Của Việc Sử Dụng Profiles

1. **Tính Linh Hoạt Theo Môi Trường**: Các giá trị cấu hình khác nhau cho các môi trường khác nhau
2. **Mã Nguồn Duy Nhất**: Cùng một mã nguồn chạy trong tất cả các môi trường với các cấu hình khác nhau
3. **Kiểm Soát Bean**: Tạo bean có điều kiện dựa trên profile đang hoạt động
4. **Không Cần Xây Dựng Lại**: Kích hoạt các profile khác nhau mà không cần xây dựng lại ứng dụng

## Profile Mặc Định

Theo mặc định, Spring Boot kích hoạt **profile mặc định**. Tất cả các thuộc tính được định nghĩa trong:
- `application.properties`
- `application.yml`

Các file này thuộc về profile mặc định và luôn được kích hoạt trừ khi bị ghi đè.

## Tạo Profiles Tùy Chỉnh

Để tạo các profile theo môi trường cụ thể, hãy tuân theo quy ước đặt tên sau:

### Đối Với File Properties:
```
application-{tên-profile}.properties
```

### Đối Với File YAML:
```
application-{tên-profile}.yml
```

### Ví Dụ:
- `application-prod.yml` - Profile production
- `application-qa.yml` - Profile QA
- `application-dev.yml` - Profile development

## Kích Hoạt Profiles

### Sử Dụng Thuộc Tính Cấu Hình

Đặt profile hoạt động bằng thuộc tính `spring.profiles.active`:

```yaml
spring:
  profiles:
    active: prod
```

### Kích Hoạt Nhiều Profiles

Bạn có thể kích hoạt nhiều profile cùng lúc bằng các giá trị phân cách bằng dấu phẩy:

```yaml
spring:
  profiles:
    active: prod,monitoring,security
```

### Kích Hoạt Từ Dòng Lệnh

Kích hoạt profile khi khởi động ứng dụng:

```bash
java -jar application.jar --spring.profiles.active=prod
```

### Biến Môi Trường

Đặt qua biến môi trường:

```bash
export SPRING_PROFILES_ACTIVE=prod
```

## Ví Dụ Cấu Trúc Profile

Với ba profile được cấu hình, cấu trúc ứng dụng của bạn sẽ là:

```
src/main/resources/
├── application.yml (profile mặc định)
├── application-dev.yml (profile development)
├── application-qa.yml (profile QA)
└── application-prod.yml (profile production)
```

## Thực Hành Tốt Nhất

### 1. Không Xây Dựng Lại Cho Các Môi Trường Khác Nhau

Một khi ứng dụng của bạn đã được xây dựng và đóng gói, nó **không nên được sửa đổi**. Điều này đặc biệt quan trọng trong kiến trúc microservices, nơi việc xây dựng lại cho từng môi trường là:
- Phức tạp và rườm rà
- Tốn thời gian
- Dễ xảy ra lỗi
- Không có khả năng mở rộng

### 2. Xử Lý Thông Tin Nhạy Cảm Cẩn Thận

Đối với thông tin nhạy cảm không thể lưu trữ trong file cấu hình:
- Cung cấp thuộc tính từ bên ngoài trong quá trình khởi động ứng dụng
- Sử dụng biến môi trường
- Tận dụng hệ thống quản lý bí mật (HashiCorp Vault, AWS Secrets Manager, v.v.)
- Xem xét Spring Cloud Config Server

### 3. Tổ Chức Profile

- **Profile Mặc Định**: Cài đặt phát triển cục bộ
- **Profile Dev**: Môi trường phát triển
- **Profile QA**: Môi trường kiểm thử
- **Profile Prod**: Môi trường sản xuất

### 4. Thứ Tự Ưu Tiên Thuộc Tính

Spring Boot tuân theo thứ tự cụ thể khi tải thuộc tính:
1. Thuộc tính theo profile cụ thể (`application-{profile}.yml`)
2. Thuộc tính profile mặc định (`application.yml`)
3. Nguồn cấu hình bên ngoài

## Cân Nhắc Cho Microservices

Trong kiến trúc microservices, profiles trở nên quan trọng hơn:

- **Khả Năng Mở Rộng**: Quản lý hàng chục hoặc hàng trăm dịch vụ
- **Tính Nhất Quán**: Đảm bảo tất cả các dịch vụ tuân theo cùng một chiến lược profile
- **Triển Khai**: Kích hoạt profile chính xác trong quá trình điều phối
- **Quản Lý Cấu Hình**: Cấu hình tập trung khi có thể

## Kiểm Soát Việc Tạo Bean

Bạn có thể tạo bean có điều kiện dựa trên profile đang hoạt động bằng annotation `@Profile`:

```java
@Configuration
public class DatabaseConfig {
    
    @Bean
    @Profile("dev")
    public DataSource devDataSource() {
        // Cấu hình cơ sở dữ liệu development
    }
    
    @Bean
    @Profile("prod")
    public DataSource prodDataSource() {
        // Cấu hình cơ sở dữ liệu production
    }
}
```

## Tùy Chọn Cấu Hình Bên Ngoài

Khi thuộc tính không thể được duy trì trong file cấu hình, hãy xem xét:

1. **Tham số dòng lệnh**
2. **Biến môi trường**
3. **File cấu hình bên ngoài**
4. **Spring Cloud Config Server**
5. **Công cụ quản lý bí mật**
6. **Kubernetes ConfigMaps và Secrets**

## Tóm Tắt

Spring Boot profiles cung cấp:
- Quản lý cấu hình theo môi trường cụ thể
- Tính linh hoạt mà không cần thay đổi mã nguồn
- Một artifact xây dựng duy nhất cho tất cả các môi trường
- Tạo bean có kiểm soát
- Quy trình triển khai đơn giản hóa

Cách tiếp cận này đảm bảo microservices của bạn có thể được triển khai trên các môi trường khác nhau một cách hiệu quả trong khi vẫn duy trì tính nhất quán và bảo mật.

## Các Bước Tiếp Theo

Trong các phần sắp tới, chúng ta sẽ thực hiện:
- Tạo profile QA và production cho accounts microservice
- Cấu hình thuộc tính theo môi trường cụ thể
- Kích hoạt profile trong các kịch bản triển khai khác nhau
- Quản lý thông tin xác thực nhạy cảm từ bên ngoài

---

**Ghi Nhớ**: Xây dựng một lần, triển khai mọi nơi với các cấu hình khác nhau bằng cách sử dụng Spring Boot profiles!