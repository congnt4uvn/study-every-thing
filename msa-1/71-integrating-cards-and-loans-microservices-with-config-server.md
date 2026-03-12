# Tích Hợp Microservices Cards và Loans với Config Server

## Tổng Quan

Hướng dẫn này trình bày quy trình từng bước để tích hợp các microservices Cards và Loans với Spring Cloud Config Server. Quy trình giống hệt nhau cho cả hai microservices và tuân theo cùng một mẫu đã sử dụng cho microservice Accounts.

## Yêu Cầu Trước

- Các microservices Cards và Loans đã được tạo
- Spring Cloud Config Server đang chạy trên cổng 8071
- Các file cấu hình đã được chuẩn bị trong Config Server:
  - `loans.yml`, `loans-prod.yml`, `loans-qa.yml`
  - `cards.yml`, `cards-prod.yml`, `cards-qa.yml`

## Phần 1: Tích Hợp Microservice Loans

### Bước 1: Dọn Dẹp Các File Cấu Hình

Điều hướng đến microservice Loans và thực hiện dọn dẹp sau:

1. Vào thư mục `resources`
2. Xóa các file YAML theo profile:
   - `application-prod.yml`
   - `application-qa.yml`
3. Mở `application.yml` và xóa tất cả các thuộc tính đã định nghĩa trước đó

### Bước 2: Cấu Hình application.yml cho Loans

Thay thế nội dung trong `application.yml` bằng cấu hình sau:

```yaml
spring:
  application:
    name: loans  # Phải khớp với tên file Config Server (loans.yml, loans-prod.yml, v.v.)
  profiles:
    active: prod  # Kích hoạt profile mặc định
  config:
    import: "optional:configserver:http://localhost:8071"
```

**Lưu Ý Quan Trọng**:
- `spring.application.name` phải là **loans** để khớp với tên file cấu hình trong Config Server
- Profile mặc định được đặt là `prod`
- Tiền tố `optional:` cho phép microservice khởi động ngay cả khi Config Server không khả dụng

### Bước 3: Cập Nhật pom.xml cho Loans

Thêm các cấu hình sau vào `pom.xml`:

#### Thêm Thuộc Tính Phiên Bản Spring Cloud

```xml
<properties>
    <java.version>17</java.version>
    <spring-cloud.version>2022.0.3</spring-cloud.version>
</properties>
```

#### Thêm Dependency Spring Cloud Config

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-config</artifactId>
</dependency>
```

#### Thêm Dependency Management

Thêm phần này trước phần `<build>` với các plugins:

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-dependencies</artifactId>
            <version>${spring-cloud.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

**Quan Trọng**: Các cấu hình này rất cần thiết để tích hợp giữa Spring Cloud và Spring Boot hoạt động đúng cách.

### Bước 4: Rebuild và Khởi Động Microservice Loans

1. Rebuild ứng dụng để tải xuống các dependencies
2. Khởi động microservice Loans trên cổng **8090**
3. Xác minh logs khởi động hiển thị kết nối đến Config Server

### Bước 5: Kiểm Tra Tích Hợp Microservice Loans

Sử dụng Postman để kiểm tra các endpoint sau:

#### Build Info API

```
GET http://localhost:8090/api/build-info
```

**Kết Quả Mong Đợi** (từ profile prod):
```json
{
    "version": "1.0"
}
```

#### Contact Info API

```
GET http://localhost:8090/api/contact-info
```

**Kết Quả Mong Đợi** (từ profile prod):
```json
{
    "message": "Properties from prod profile",
    "contactDetails": {
        "name": "Product Owner",
        "email": "call support"
    }
}
```

✅ **Thành Công**: Nếu bạn nhận được các phản hồi này, microservice Loans đã được tích hợp thành công với Config Server!

---

## Phần 2: Tích Hợp Microservice Cards

Quy trình cho microservice Cards giống hệt với Loans. Làm theo các bước tương tự với các giá trị khác nhau.

### Bước 1: Dọn Dẹp Các File Cấu Hình

Điều hướng đến microservice Cards:

1. Vào thư mục `resources`
2. Xóa các file YAML theo profile:
   - `application-prod.yml`
   - `application-qa.yml`
3. Mở `application.yml` và xóa các thuộc tính không cần thiết

### Bước 2: Cấu Hình application.yml cho Cards

Cập nhật `application.yml` với cấu hình sau:

```yaml
spring:
  application:
    name: cards  # Phải khớp với tên file Config Server (cards.yml, cards-prod.yml, v.v.)
  profiles:
    active: prod  # Kích hoạt profile mặc định
  config:
    import: "optional:configserver:http://localhost:8071"
```

**Quan Trọng**: `spring.application.name` phải là **cards** để khớp với tên file cấu hình trong Config Server.

### Bước 3: Cập Nhật pom.xml cho Cards

Thêm các cấu hình tương tự vào `pom.xml` của microservice Cards:

#### Thêm Thuộc Tính Phiên Bản Spring Cloud

```xml
<properties>
    <java.version>17</java.version>
    <spring-cloud.version>2022.0.3</spring-cloud.version>
</properties>
```

#### Thêm Dependency Spring Cloud Config

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-config</artifactId>
</dependency>
```

#### Thêm Dependency Management

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-dependencies</artifactId>
            <version>${spring-cloud.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

### Bước 4: Rebuild và Khởi Động Microservice Cards

1. **Quan Trọng**: Rebuild microservice Cards sau khi thực hiện tất cả các thay đổi
2. Khởi động microservice Cards trên cổng **9000**
3. Xác minh microservice đang ở trạng thái running

### Bước 5: Kiểm Tra Tích Hợp Microservice Cards

Sử dụng Postman để kiểm tra các endpoint sau:

#### Build Info API

```
GET http://localhost:9000/api/build-info
```

**Kết Quả Mong Đợi** (từ profile prod):
```json
{
    "version": "1.2"
}
```

#### Contact Info API

```
GET http://localhost:9000/api/contact-info
```

**Kết Quả Mong Đợi** (từ profile prod):
```json
{
    "message": "Properties from prod profile",
    "contactDetails": {
        "name": "Product Owner",
        "email": "call support"
    }
}
```

✅ **Thành Công**: Microservice Cards bây giờ đã được tích hợp thành công với Config Server!

---

## Tóm Tắt

### Những Gì Chúng Ta Đã Hoàn Thành

Cả ba microservices (Accounts, Loans, Cards) giờ đã được tích hợp với Spring Cloud Config Server:

| Microservice | Cổng | Tên Application | Trạng Thái |
|-------------|------|------------------|--------|
| Accounts    | 8080 | accounts         | ✅ Đã Tích Hợp |
| Loans       | 8090 | loans            | ✅ Đã Tích Hợp |
| Cards       | 9000 | cards            | ✅ Đã Tích Hợp |

### Lợi Ích Chính

- **Quản Lý Tập Trung**: Tất cả thuộc tính microservice giờ được quản lý bởi Spring Cloud Config Server
- **Khả Năng Mở Rộng**: Quy trình tương tự hoạt động cho dù bạn có 3 hay 100 microservices
- **Tính Nhất Quán**: Tất cả microservices tuân theo cùng một mẫu cấu hình

### Tóm Tắt Thay Đổi Cấu Hình

Cho mỗi microservice, chúng ta đã:

1. ✅ Xóa các file YAML theo profile
2. ✅ Cập nhật `application.yml` với:
   - Tên application
   - Profile mặc định
   - Kết nối Config Server
3. ✅ Cập nhật `pom.xml` với:
   - Phiên bản Spring Cloud
   - Dependency Config Client
   - Dependency management
4. ✅ Rebuild và khởi động lại microservice
5. ✅ Kiểm tra REST APIs để xác minh tích hợp

### Hạn Chế Kiến Trúc Hiện Tại

⚠️ **Lưu Ý Quan Trọng**: Hiện tại, tất cả cấu hình được lưu trữ bên trong **classpath** của chính Config Server.

**Vấn Đề Tiềm Ẩn**:
- Bất kỳ ai có quyền truy cập vào code Config Server đều có thể xem tất cả các thuộc tính
- Không lý tưởng cho môi trường production
- Vấn đề bảo mật với dữ liệu nhạy cảm

### Bước Tiếp Theo

Trong phần tiếp theo, chúng ta sẽ giải quyết hạn chế này bằng cách:
- Chuyển cấu hình sang một **vị trí file system bên ngoài**
- Tách riêng cấu hình khỏi code Spring Cloud Config Server
- Cải thiện bảo mật và kiểm soát truy cập

## Danh Sách Kiểm Tra Khắc Phục Sự Cố

Nếu tích hợp không hoạt động, hãy xác minh:

- [ ] Tên application khớp chính xác với tên file Config Server
- [ ] Config Server đang chạy trên cổng 8071
- [ ] Phiên bản Spring Cloud được định nghĩa đúng cách
- [ ] Phần dependency management đã được thêm
- [ ] Ứng dụng đã được rebuild sau khi thay đổi pom.xml
- [ ] Cổng đúng được sử dụng cho mỗi microservice
- [ ] Tên profile khớp với các profile có sẵn trong Config Server

## Thực Hành Tốt Nhất

1. **Đặt Tên Nhất Quán**: Sử dụng tên application nhất quán trên các file Config Server và microservices
2. **Quản Lý Phiên Bản**: Giữ các phiên bản Spring Cloud đồng bộ trên tất cả microservices
3. **Luôn Rebuild**: Luôn rebuild sau khi thay đổi dependencies
4. **Kiểm Tra Kỹ Lưỡng**: Kiểm tra tất cả REST APIs sau khi tích hợp
5. **Xác Minh Logs**: Kiểm tra logs khởi động cho các thông báo kết nối Config Server

---

**Chúc Mừng!** Bạn đã tích hợp thành công tất cả các microservices với Spring Cloud Config Server. Quản lý cấu hình tập trung giờ đã được thiết lập và sẵn sàng cho các cải tiến tiếp theo.