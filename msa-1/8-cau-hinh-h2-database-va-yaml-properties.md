# Cấu Hình H2 Database và YAML Properties trong Spring Boot

## Tổng Quan

Bài học này đề cập đến việc thiết lập cấu hình H2 database và sử dụng định dạng YAML cho các thuộc tính ứng dụng Spring Boot. Chúng ta sẽ học cách cấu hình database, kích hoạt H2 console và tạo database schema tự động trong quá trình khởi động ứng dụng.

## Yêu Cầu Tiên Quyết

- Đã hoàn thành tạo REST API từ bài học trước
- Dự án Spring Boot có dependency H2 database
- Hiểu biết cơ bản về khái niệm database

## Tại Sao Sử Dụng Định Dạng YAML?

### Properties Truyền Thống vs YAML

**Định dạng .properties truyền thống:**
```properties
server.port=8080
spring.datasource.url=jdbc:h2:mem:testdb
spring.datasource.driver-class-name=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=
```

**Định dạng YAML (.yml):**
```yaml
server:
  port: 8080

spring:
  datasource:
    url: jdbc:h2:mem:testdb
    driver-class-name: org.h2.Driver
    username: sa
    password: ''
```

### Ưu Điểm Của Định Dạng YAML

1. **Trực quan và dễ đọc** - Dễ hiểu cấu trúc
2. **Không lặp lại** - Các key không bị lặp lại không cần thiết
3. **Tiêu chuẩn công nghiệp** - Được sử dụng trong Docker, Kubernetes, AWS, GCP, Azure
4. **Hướng tới tương lai** - Spring Boot có khả năng chuyển sang định dạng YAML
5. **Tổ chức tốt hơn** - Cấu trúc phân cấp làm cho cấu hình rõ ràng hơn

## Cấu Hình Application Properties

### Bước 1: Đổi Tên File Properties

1. Điều hướng đến thư mục `src/main/resources`
2. Đổi tên `application.properties` thành `application.yml`
3. Cài đặt plugin YAML trong IDE của bạn để hỗ trợ cú pháp tốt hơn

### Bước 2: Cấu Hình Server Properties

```yaml
server:
  port: 8080
```

- Đặt port server ứng dụng là 8080 (port mặc định)
- Thực hành tốt là khai báo rõ ràng port
- Các microservices khác nhau sẽ cần số port khác nhau

### Bước 3: Cấu Hình H2 Database

```yaml
spring:
  datasource:
    url: jdbc:h2:mem:testdb
    driver-class-name: org.h2.Driver
    username: sa
    password: ''
```

**Chi Tiết Cấu Hình:**
- **url**: Chuỗi kết nối cho H2 in-memory database
- **driver-class-name**: H2 JDBC driver
- **username**: Username mặc định là "sa"
- **password**: Password trống (mặc định)

### Bước 4: Kích Hoạt H2 Console

```yaml
spring:
  h2:
    console:
      enabled: true
```

Điều này kích hoạt H2 web console có thể truy cập tại `http://localhost:8080/h2-console`

### Bước 5: Cấu Hình JPA Properties

```yaml
spring:
  jpa:
    database-platform: org.hibernate.dialect.H2Dialect
    hibernate:
      ddl-auto: update
    show-sql: true
```

**Giải Thích Cấu Hình JPA:**

- **database-platform**: Chỉ định H2 dialect cho Hibernate
- **ddl-auto: update**: Tự động tạo bảng trong quá trình khởi động nếu chúng chưa tồn tại
- **show-sql: true**: In tất cả các truy vấn SQL ra console để debug

## Quy Tắc Cú Pháp YAML

### Các Quy Tắc Quan Trọng Cần Tuân Theo:

1. **Indentation quan trọng** - Sử dụng khoảng cách nhất quán (thường là 2 spaces)
2. **Dấu hai chấm theo sau là khoảng trắng** - Luôn thêm khoảng trắng sau dấu hai chấm
3. **Cấu trúc phân cấp** - Sử dụng indentation để hiển thị mối quan hệ cha-con
4. **Không dùng tabs** - Sử dụng spaces cho indentation, không phải tabs

### Ví Dụ Cấu Trúc:

```yaml
parent:
  child1: value1
  child2:
    grandchild: value2
```

## Tạo Database Schema

### Bước 1: Tạo File schema.sql

Tạo một file có tên `schema.sql` trong thư mục `src/main/resources`.

### Bước 2: Định Nghĩa Cấu Trúc Bảng

**Bảng Customer:**
```sql
CREATE TABLE IF NOT EXISTS customer (
  customer_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL,
  mobile_number VARCHAR(20) NOT NULL,
  created_at DATE NOT NULL,
  created_by VARCHAR(20) NOT NULL,
  updated_at DATE DEFAULT NULL,
  updated_by VARCHAR(20) DEFAULT NULL
);
```

**Bảng Accounts:**
```sql
CREATE TABLE IF NOT EXISTS accounts (
  customer_id INT NOT NULL,
  account_number BIGINT AUTO_INCREMENT PRIMARY KEY,
  account_type VARCHAR(100) NOT NULL,
  branch_address VARCHAR(200) NOT NULL,
  created_at DATE NOT NULL,
  created_by VARCHAR(20) NOT NULL,
  updated_at DATE DEFAULT NULL,
  updated_by VARCHAR(20) DEFAULT NULL,
  FOREIGN KEY (customer_id) REFERENCES customer(customer_id) ON DELETE CASCADE
);
```

### Tiêu Chuẩn Các Cột Metadata

Mỗi bảng bao gồm bốn cột metadata này:
- **created_at**: Timestamp khi bản ghi được tạo
- **created_by**: Người dùng đã tạo bản ghi
- **updated_at**: Timestamp khi bản ghi được cập nhật lần cuối
- **updated_by**: Người dùng đã cập nhật lần cuối

Các cột này giúp theo dõi nguồn gốc dữ liệu và là thực hành tiêu chuẩn trong các dự án thực tế.

## Truy Cập H2 Console

### Bước 1: Khởi Động Ứng Dụng

Với Spring Boot DevTools, ứng dụng sẽ tự động khởi động lại khi phát hiện thay đổi.

### Bước 2: Truy Cập Console

Mở trình duyệt của bạn và điều hướng đến:
```
http://localhost:8080/h2-console
```

### Bước 3: Đăng Nhập

- **JDBC URL**: `jdbc:h2:mem:testdb`
- **Username**: `sa`
- **Password**: (để trống)
- Nhấp vào "Connect"

### Bước 4: Xác Minh Các Bảng

Bạn sẽ thấy hai bảng được tạo:
- **CUSTOMER** - với các cột: customer_id, name, email, mobile_number, created_at, created_by, updated_at, updated_by
- **ACCOUNTS** - với các cột: customer_id, account_number, account_type, branch_address, created_at, created_by, updated_at, updated_by

## Hiểu Về H2 In-Memory Database

### Các Đặc Điểm Chính:

1. **Lưu trữ tạm thời** - Dữ liệu chỉ được lưu trong bộ nhớ
2. **Mất dữ liệu khi tắt** - Tất cả dữ liệu và bảng bị xóa khi server dừng
3. **Hiệu suất nhanh** - Các thao tác trong bộ nhớ rất nhanh
4. **Tự động tạo lại** - Bảng được tạo lại khi khởi động bằng schema.sql
5. **Hoàn hảo cho phát triển** - Lý tưởng cho mục đích kiểm thử và phát triển

### Tại Sao Sử Dụng schema.sql?

Vì H2 là in-memory:
- Bảng biến mất khi ứng dụng dừng
- Tạo bảng thủ công mỗi lần rất tẻ nhạt
- `schema.sql` tự động hóa việc tạo bảng trong quá trình khởi động
- Spring Boot thực thi các script này tự động

## Ví Dụ application.yml Hoàn Chỉnh

```yaml
server:
  port: 8080

spring:
  datasource:
    url: jdbc:h2:mem:testdb
    driver-class-name: org.h2.Driver
    username: sa
    password: ''
  h2:
    console:
      enabled: true
  jpa:
    database-platform: org.hibernate.dialect.H2Dialect
    hibernate:
      ddl-auto: update
    show-sql: true
```

## Điểm Chính Cần Nhớ

1. **YAML được ưa chuộng** hơn file properties để dễ đọc và cấu trúc tốt hơn
2. **Indentation rất quan trọng** trong YAML - duy trì khoảng cách nhất quán
3. **H2 console** cung cấp truy cập dễ dàng để xem nội dung database
4. **schema.sql** tự động hóa việc tạo bảng trong quá trình khởi động
5. **Các cột metadata** (created_at, created_by, updated_at, updated_by) là thực hành tiêu chuẩn
6. **show-sql: true** giúp debug bằng cách hiển thị các truy vấn được thực thi
7. **In-memory databases** hoàn hảo cho phát triển nhưng dữ liệu không bền vững

## Các Bước Tiếp Theo

Trong bài học tiếp theo, chúng ta sẽ xây dựng code sử dụng Spring Data JPA để tương tác với H2 database và các bảng. Điều này sẽ cho phép chúng ta thực hiện các thao tác CRUD (Create, Read, Update, Delete) trên dữ liệu.

## Thực Hành Tốt Nhất

1. Luôn khai báo rõ ràng server port trong cấu hình
2. Sử dụng định dạng YAML để dễ bảo trì hơn
3. Kích hoạt H2 console trong quá trình phát triển để debug dễ dàng
4. Bao gồm các cột metadata trong tất cả các bảng
5. Sử dụng `show-sql: true` trong quá trình phát triển để hiểu việc thực thi truy vấn
6. Giữ cấu trúc bảng đơn giản để tập trung vào khái niệm microservices
7. Sử dụng `CREATE TABLE IF NOT EXISTS` để tránh lỗi khi khởi động lại

## Các Vấn Đề Thường Gặp và Giải Pháp

### Vấn đề: YAML không được nhận dạng
**Giải pháp**: Cài đặt plugin YAML trong IDE của bạn

### Vấn đề: Lỗi indentation
**Giải pháp**: Sử dụng spaces thay vì tabs, duy trì indentation 2-space nhất quán

### Vấn đề: Không truy cập được H2 console
**Giải pháp**: Đảm bảo `spring.h2.console.enabled: true` được đặt trong application.yml

### Vấn đề: Bảng không được tạo
**Giải pháp**: Xác minh schema.sql nằm trong thư mục `src/main/resources` và kiểm tra lỗi cú pháp SQL

## Tóm Tắt

Bài học này đề cập đến cấu hình cần thiết cho H2 database trong ứng dụng microservices Spring Boot. Chúng ta đã học về ưu điểm của định dạng YAML, cách cấu hình thuộc tính ứng dụng, tạo database schemas tự động và truy cập H2 console để quản lý database. Những bước nền tảng này chuẩn bị cho chúng ta để triển khai Spring Data JPA trong bài học tiếp theo.