# Tạo Spring Cloud Config Server

## Tổng Quan
Hướng dẫn này trình bày cách tạo một Config Server riêng biệt sử dụng Spring Cloud Config để quản lý cấu hình tập trung trong kiến trúc microservices.

## Thiết Lập Cấu Trúc Dự Án

### Trạng Thái Hiện Tại
- Vị trí: `section6/v1-springboot`
- Chứa ba microservices:
  - Accounts (Tài khoản)
  - Cards (Thẻ)
  - Loans (Khoản vay)
- Quản lý cấu hình: Chỉ sử dụng Spring Boot

### Chuyển Sang Spring Cloud Config
Thay vì chỉnh sửa thư mục v1-springboot hiện tại, chúng ta sẽ tạo phiên bản mới:

1. **Sao chép thư mục** `v1-springboot`
2. **Đổi tên thành** `v2-spring-cloud-config`
3. Cách này giữ lại tham chiếu cho cả hai phương pháp:
   - v1: Cấu hình Spring Boot
   - v2: Spring Cloud Config

### Dọn Dẹp
- Xóa thư mục `.idea` (thư mục workspace của IntelliJ)
- Thư mục này thuộc về workspace trước đó

## Tạo Dự Án Config Server

### Sử Dụng Spring Initializr

Truy cập [start.spring.io](https://start.spring.io) và cấu hình:

#### Metadata Dự Án
- **Loại Dự Án:** Maven
- **Ngôn Ngữ:** Java
- **Phiên Bản Spring Boot:** 3.1.2 (hoặc phiên bản ổn định mới nhất)
- **Group:** `com.eazybytes`
- **Artifact ID:** `configserver`
- **Tên:** `configserver`
- **Mô Tả:** `Config Server for EazyBank Microservices`
- **Packaging:** JAR

> **Lưu Ý:** Luôn sử dụng phiên bản Spring Boot ổn định mới nhất. Repository GitHub sẽ được cập nhật hàng quý.

#### Dependencies (Thư Viện Phụ Thuộc)
Thêm các dependencies sau:

1. **Config Server**
   - Mục đích: Quản lý cấu hình tập trung qua Git, SVN, hoặc HashiCorp Vault
   - Sử dụng để xây dựng configuration server

2. **Spring Boot Actuator**
   - Mục đích: Giám sát và quản lý ứng dụng
   - Tính năng: Kiểm tra health, metrics, quản lý session

### Hiểu Về Versioning Spring Cloud

Khi bạn xem `pom.xml`:
- **Phiên Bản Spring Boot:** 3.1.2
- **Phiên Bản Spring Cloud:** 2022.0.3

#### Tại Sao Số Phiên Bản Khác Nhau?
- Spring Boot và Spring Cloud là các dự án riêng biệt trong hệ sinh thái Spring
- Mỗi dự án có số phiên bản độc lập
- `start.spring.io` tự động ánh xạ các phiên bản tương thích

#### Tham Chiếu Ánh Xạ Phiên Bản
Truy cập [trang web Spring Cloud](https://spring.io/projects/spring-cloud) để xem release train:

| Phiên Bản Spring Boot | Phiên Bản Spring Cloud |
|----------------------|------------------------|
| 3.0.x - 3.1.x       | 2022.0.3              |
| Phiên bản cũ hơn     | Xem tài liệu          |

#### Sự Thật Thú Vị: Tên Phiên Bản Spring Cloud
Các phiên bản Spring Cloud được đặt tên theo các ga tàu điện ngầm London:
- Dalston
- Edgware
- Finchley
- Greenwich
- Hoxton
- Ilford
- Jubilee
- Kilburn

Chú ý thứ tự theo bảng chữ cái: D, E, F, G, H, I, J, K!

## Thiết Lập Config Server

### 1. Giải Nén và Import Dự Án

1. **Generate** dự án từ Spring Initializr
2. **Giải nén** file `configserver.zip` đã tải xuống
3. **Sao chép** vào thư mục `v2-spring-cloud-config`
4. **Mở** trong IntelliJ IDEA

### 2. Cấu Hình Main Application Class

Mở `ConfigServerApplication.java` và thêm annotation:

```java
@EnableConfigServer
@SpringBootApplication
public class ConfigServerApplication {
    public static void main(String[] args) {
        SpringApplication.run(ConfigServerApplication.class, args);
    }
}
```

Annotation `@EnableConfigServer` kích hoạt chức năng Config Server.

### 3. Cấu Hình Application Properties

1. **Đổi tên** `application.properties` thành `application.yml`
2. **Cấu hình** cổng server:

```yaml
server:
  port: 8071
```

> **Quan Trọng:** Sử dụng cổng 8071 nhất quán trong suốt khóa học để tránh các vấn đề cấu hình.

## Tùy Chọn Lưu Trữ Cấu Hình

Config Server cần một vị trí tập trung để đọc cấu hình. Có nhiều tùy chọn khả dụng:

### 1. Classpath
Lưu trữ cấu hình trong classpath của Config Server.

### 2. File System (Hệ Thống File)
Lưu trữ cấu hình trong bất kỳ thư mục nào trên server hoặc hệ thống local của bạn.

### 3. Git Repository (Phổ Biến Nhất)
Lưu trữ cấu hình trong repository GitHub.

### Các Tùy Chọn Khác
- Database (Cơ sở dữ liệu)
- AWS S3
- HashiCorp Vault

## Các Bước Tiếp Theo

Trong các bài giảng tiếp theo, chúng ta sẽ khám phá ba phương pháp:
1. Cấu hình dựa trên Classpath
2. Cấu hình dựa trên File System
3. Cấu hình dựa trên GitHub

## Cấu Trúc Dự Án Sau Khi Thiết Lập

```
v2-spring-cloud-config/
├── accounts/
├── cards/
├── loans/
└── configserver/
```

Tất cả bốn dự án Maven nên được load trong IntelliJ workspace của bạn.

## Tóm Tắt

- Đã tạo một dự án Config Server riêng biệt sử dụng Spring Cloud Config
- Đã cấu hình server chạy trên cổng 8071
- Đã chuẩn bị cho quản lý cấu hình tập trung
- Duy trì khả năng tương thích ngược với v1 (chỉ Spring Boot)

## Các Annotation Chính
- `@EnableConfigServer` - Kích hoạt chức năng Spring Cloud Config Server

## Các Dependencies Chính
- `spring-cloud-config-server` - Triển khai Config Server
- `spring-boot-starter-actuator` - Giám sát và quản lý ứng dụng

---

*Đây là một phần của khóa học EazyBank Microservices về Spring Cloud Config.*