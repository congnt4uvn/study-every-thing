# Tích Hợp Microservices với Spring Cloud Config Server

## Tổng Quan

Hướng dẫn này trình bày cách kết nối một microservice (accounts) với Spring Cloud Config Server để quản lý cấu hình tập trung. Bằng cách chuyển các thuộc tính cấu hình sang một kho lưu trữ tập trung, bạn có thể quản lý nhiều môi trường (dev, qa, prod) hiệu quả hơn.

## Yêu Cầu Trước

- Microservice accounts đã được tạo
- Spring Cloud Config Server đã được thiết lập và đang chạy
- Các file cấu hình đã được lưu trữ trong Config Server (accounts.yml, accounts-prod.yml, accounts-qa.yml)

## Bước 1: Dọn Dẹp Các File Cấu Hình Local

Đầu tiên, xóa các file cấu hình theo profile không cần thiết khỏi microservice accounts:

1. Xóa các file `application-prod.yml` và `application-qa.yml`
2. Mở file `application.yml` và xóa:
   - Các câu lệnh config import
   - Cài đặt kích hoạt profile
   - Các thuộc tính build version

Chỉ giữ lại các thuộc tính thiết yếu như:
- Cổng server
- Cấu hình Spring Data JPA/database

## Bước 2: Cấu Hình Tên Application

Thêm tên application vào `application.yml`. Tên này phải khớp với tên các file cấu hình trong Config Server:

```yaml
spring:
  application:
    name: accounts  # Phải khớp với tiền tố file cấu hình (accounts.yml, accounts-prod.yml, v.v.)
  profiles:
    active: prod    # Kích hoạt profile mặc định
```

**Quan trọng**: Config Server sử dụng tên application này để xác định file cấu hình nào sẽ được cung cấp cho microservice này.

## Bước 3: Thêm Dependency Spring Cloud Config Client

Thêm dependency Spring Cloud Config Client vào `pom.xml`:

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-config</artifactId>
</dependency>
```

## Bước 4: Cấu Hình Phiên Bản Spring Cloud

Vì đây là dependency Spring Cloud đầu tiên trong microservice accounts, hãy thêm thuộc tính phiên bản Spring Cloud và quản lý dependency:

```xml
<properties>
    <java.version>17</java.version>
    <spring-cloud.version>2023.0.0</spring-cloud.version>
</properties>

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

Sau khi thêm các thay đổi này, tải lại các dependency Maven.

## Bước 5: Cấu Hình Kết Nối Config Server

Thêm URL Config Server vào `application.yml`:

```yaml
spring:
  config:
    import: "optional:configserver:http://localhost:8071"
```

**Các Điểm Chính**:
- Tiền tố `configserver:` - Cho biết kết nối đến Config Server
- Tiền tố `optional:` - Cho phép microservice khởi động ngay cả khi Config Server không khả dụng (sẽ hiển thị cảnh báo nhưng không thất bại)
- Cổng `8071` - Cổng mà Config Server đang chạy
- Xóa `optional:` nếu cấu hình là quan trọng và microservice không nên khởi động nếu thiếu nó

## Bước 6: Khởi Động và Kiểm Tra Microservice

1. Khởi động microservice accounts
2. Kiểm tra console logs để xác minh kết nối Config Server
3. Tìm các thông báo kích hoạt profile (ví dụ: "activated profile: prod")

### Kiểm Tra với Postman

Kiểm tra các endpoint sau để xác minh cấu hình được tải đúng:

**Contact Info API** (kiểm tra thuộc tính theo profile):
```
GET http://localhost:8080/api/contact-info
```
Kết quả mong đợi cho profile prod:
```json
{
    "message": "Properties from prod",
    "contactDetails": {
        "name": "Product Owner",
        "email": "call support"
    }
}
```

**Build Info API** (kiểm tra thuộc tính version):
```
GET http://localhost:8080/api/build-info
```
Kết quả mong đợi cho profile prod:
```json
{
    "version": "1.0"
}
```

## Bước 7: Ghi Đè Profile bằng Cấu Hình Bên Ngoài

Bạn có thể ghi đè profile mặc định bằng cách sử dụng tham số dòng lệnh:

1. Nhấp chuột phải vào ứng dụng accounts
2. Chọn "Modify Run Configurations"
3. Thêm vào Program Arguments:
```
--spring.profiles.active=qa
```
4. Apply và khởi động lại microservice

### Kiểm Tra Profile QA

Sau khi khởi động lại với profile QA:

**Build Info API**:
```
GET http://localhost:8080/api/build-info
```
Kết quả mong đợi:
```json
{
    "version": "2.0"
}
```

**Contact Info API**:
```
GET http://localhost:8080/api/contact-info
```
Kết quả mong đợi (thuộc tính profile QA):
```json
{
    "message": "Properties from qa",
    "contactDetails": {
        "name": "QA Team",
        "email": "qa support"
    }
}
```

## Cách Hoạt Động

1. **Khởi động**: Khi microservice accounts khởi động, nó đọc `spring.application.name` và `spring.profiles.active`
2. **Kết nối**: Nó kết nối đến Config Server tại URL đã chỉ định
3. **Yêu cầu**: Nó yêu cầu cấu hình theo mẫu: `{application-name}-{profile}.yml`
4. **Phản hồi**: Config Server trả về các file cấu hình phù hợp
5. **Tải**: Microservice tải các thuộc tính này và sử dụng chúng trong runtime

## Lợi Ích của Phương Pháp Này

- **Cấu Hình Tập Trung**: Tất cả thuộc tính theo môi trường ở một nơi
- **Cập Nhật Dễ Dàng**: Thay đổi cấu hình mà không cần rebuild microservices
- **Linh Hoạt Môi Trường**: Chuyển đổi giữa các môi trường bằng cấu hình bên ngoài
- **Quản Lý Phiên Bản**: Cấu hình có thể được quản lý phiên bản trong Git
- **Bảo Mật**: Các thuộc tính nhạy cảm có thể được mã hóa trong Config Server

## Bước Tiếp Theo

Áp dụng cùng một tích hợp cho các microservices khác (cards, loans):
1. Thêm các dependency tương tự
2. Cấu hình tên application
3. Thiết lập kết nối Config Server
4. Kiểm tra REST APIs để xác minh việc tải cấu hình

## Khắc Phục Sự Cố

**Vấn đề**: Microservice không khởi động được khi Config Server bị down
- **Giải pháp**: Thêm tiền tố `optional:` vào config import URL

**Vấn đề**: Thuộc tính profile sai đang được tải
- **Giải pháp**: Xác minh `spring.application.name` khớp chính xác với tên file Config Server

**Vấn đề**: Thuộc tính không cập nhật
- **Giải pháp**: Đảm bảo Config Server đang chạy và có thể truy cập được tại URL đã chỉ định

## Tóm Tắt

Bạn đã thành công:
- ✅ Dọn dẹp các file cấu hình local
- ✅ Cấu hình tên application và profile mặc định
- ✅ Thêm dependency Spring Cloud Config Client
- ✅ Kết nối microservice với Config Server
- ✅ Kiểm tra việc tải thuộc tính theo profile
- ✅ Trình bày ghi đè profile từ bên ngoài

Microservice accounts bây giờ tải tất cả cấu hình của nó từ Config Server tập trung, giúp quản lý dễ dàng hơn trên nhiều môi trường.