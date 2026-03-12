# Kết Nối Spring Boot Microservices với MySQL Database Cục Bộ

## Tổng Quan

Hướng dẫn này trình bày cách kết nối các Spring Boot microservices (accounts, cards và loans) với cơ sở dữ liệu MySQL chạy cục bộ trong các Docker containers. Chúng ta sẽ thay thế cơ sở dữ liệu H2 in-memory bằng MySQL để có môi trường phát triển và kiểm thử thực tế hơn.

## Yêu Cầu Tiên Quyết

- Docker Desktop đã được cài đặt và đang chạy
- Spring Boot microservices (accounts, cards, loans)
- Config Server (cho cấu hình tập trung)
- Maven để quản lý dependencies
- Các MySQL Docker containers đang chạy cục bộ
- Postman hoặc công cụ kiểm thử API tương tự

## Bước 1: Cập Nhật Maven Dependencies

### Xóa H2 Database Dependency

Bước đầu tiên là xóa H2 database dependency khỏi `pom.xml` trong tất cả các microservices. Khi Spring Boot phát hiện H2 trong classpath, nó sẽ tự động cấu hình và khởi tạo H2, điều này chúng ta muốn tránh khi sử dụng MySQL.

**Trong pom.xml, xóa:**
```xml
<dependency>
    <groupId>com.h2database</groupId>
    <artifactId>h2</artifactId>
</dependency>
```

### Thêm MySQL Connector Dependency

Thay thế H2 dependency bằng MySQL connector:

```xml
<dependency>
    <groupId>com.mysql</groupId>
    <artifactId>mysql-connector-j</artifactId>
</dependency>
```

**Áp dụng thay đổi này cho cả ba microservices:**
1. Accounts microservice
2. Cards microservice
3. Loans microservice

Sau khi thực hiện các thay đổi này, tải lại Maven dependencies để tải xuống MySQL connector.

> **Lưu ý:** Config Server không sử dụng bất kỳ database nào, do đó không cần thay đổi gì ở đây.

## Bước 2: Cấu Hình Kết Nối Database trong application.yml

### Cấu Hình Accounts Microservice

Mở file `application.yml` trong accounts microservice và thay thế cấu hình datasource H2 bằng MySQL:

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/accountsDB
    username: root
    password: root
    sql:
      init:
        mode: always
  jpa:
    show-sql: true
```

**Chi Tiết Cấu Hình:**

- **Định Dạng URL**: `jdbc:mysql://<hostname>:<port>/<tên-database>`
- **Hostname**: `localhost` (vì MySQL đang chạy cục bộ)
- **Port**: `3306` (port của accounts database)
- **Tên Database**: `accountsDB`
- **Username/Password**: `root/root` (chỉ dùng cho phát triển cục bộ)
- **sql.init.mode**: `always` - yêu cầu Spring Boot thực thi `schema.sql` mỗi khi khởi động
- **show-sql**: `true` - hiển thị các câu lệnh SQL được thực thi trong console

### Cấu Hình Cards Microservice

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3308/cardsDB
    username: root
    password: root
    sql:
      init:
        mode: always
  jpa:
    show-sql: true
```

**Điểm Khác Biệt:**
- **Port**: `3308` (port của cards database)
- **Tên Database**: `cardsDB`

### Cấu Hình Loans Microservice

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3307/loansDB
    username: root
    password: root
    sql:
      init:
        mode: always
  jpa:
    show-sql: true
```

**Điểm Khác Biệt:**
- **Port**: `3307` (port của loans database)
- **Tên Database**: `loansDB`

### Xóa Các Properties Không Cần Thiết Dành Cho H2

Xóa các properties sau đây khỏi tất cả microservices:
- `spring.datasource.driver-class-name`
- `spring.h2.console.enabled`
- `spring.h2.console.path`
- `spring.jpa.database-platform`
- `spring.jpa.hibernate.ddl-auto: update`

Giữ lại `spring.jpa.show-sql: true` để xem các câu lệnh SQL trong console logs.

## Bước 3: Cấu Hình Khởi Tạo Schema Tự Động

### Hiểu Về Hành Vi Khởi Tạo Schema

**H2 Database:**
- Tự động tìm và thực thi `schema.sql` trong quá trình khởi động Spring Boot
- Không cần cấu hình bổ sung

**MySQL Database:**
- KHÔNG tự động thực thi `schema.sql`
- Mong đợi developers đã tạo sẵn database schemas
- Yêu cầu cấu hình rõ ràng để thực thi schema scripts

### Kích Hoạt Thực Thi Schema Script

Thêm property sau để kích hoạt thực thi schema tự động:

```yaml
spring:
  datasource:
    sql:
      init:
        mode: always
```

**Quan trọng:** Property này phải nằm dưới `spring.datasource`, KHÔNG phải dưới `spring.jpa`.

**Vị trí sai:**
```yaml
spring:
  jpa:
    sql:
      init:
        mode: always  # ❌ Sai - không hoạt động ở đây
```

**Vị trí đúng:**
```yaml
spring:
  datasource:
    sql:
      init:
        mode: always  # ✅ Đúng
```

### Sử Dụng IF NOT EXISTS trong SQL Scripts

Đảm bảo các file `schema.sql` của bạn sử dụng `IF NOT EXISTS` để tránh lỗi khi khởi động lại:

```sql
CREATE TABLE IF NOT EXISTS customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    mobile_number VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS accounts (
    account_number BIGINT PRIMARY KEY,
    customer_id INT NOT NULL,
    account_type VARCHAR(100) NOT NULL,
    branch_address VARCHAR(200) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);
```

**Không có `IF NOT EXISTS`:** Ứng dụng sẽ báo lỗi khi khởi động lại vì các bảng đã tồn tại.

## Bước 4: Thông Tin Đăng Nhập Database - Vấn Đề Bảo Mật

### Môi Trường Development

Đối với phát triển và kiểm thử cục bộ, việc hardcode credentials trong `application.yml` là chấp nhận được:

```yaml
spring:
  datasource:
    username: root
    password: root
```

### Môi Trường Production

**Không bao giờ hardcode credentials của production database** trong các file cấu hình ứng dụng. Thay vào đó, sử dụng các phương pháp cấu hình externalized:

1. **Biến Môi Trường (Environment Variables)**
   ```yaml
   spring:
     datasource:
       username: ${DB_USERNAME}
       password: ${DB_PASSWORD}
   ```

2. **Tham Số Dòng Lệnh (Command-Line Arguments)**
   ```bash
   java -jar app.jar --spring.datasource.username=user --spring.datasource.password=pass
   ```

3. **Biến Hệ Thống JVM (JVM System Variables)**
   ```bash
   java -Dspring.datasource.username=user -Dspring.datasource.password=pass -jar app.jar
   ```

4. **Docker Compose Environment Variables**
   ```yaml
   services:
     accounts:
       environment:
         - SPRING_DATASOURCE_USERNAME=user
         - SPRING_DATASOURCE_PASSWORD=pass
   ```

5. **Kubernetes ConfigMaps và Secrets**
   - Sử dụng ConfigMaps cho cấu hình không nhạy cảm
   - Sử dụng Secrets cho credentials nhạy cảm
   - Mount chúng dưới dạng biến môi trường hoặc volume files

## Bước 5: Khởi Động Docker MySQL Containers

Đảm bảo tất cả MySQL Docker containers đang chạy trước khi khởi động các microservices.

**Accounts Database Container:**
```bash
docker run -d -p 3306:3306 --name accountsDB -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=accountsDB mysql:latest
```

**Cards Database Container:**
```bash
docker run -d -p 3308:3306 --name cardsDB -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=cardsDB mysql:latest
```

**Loans Database Container:**
```bash
docker run -d -p 3307:3306 --name loansDB -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=loansDB mysql:latest
```

## Bước 6: Khởi Động Các Microservices

### Trình Tự Khởi Động

Khởi động các microservices theo thứ tự sau:

1. **Config Server Trước**
   - Các microservices khác phụ thuộc vào Config Server
   - Đợi cho đến khi nó khởi động thành công

2. **Accounts Application**
   - Khởi động ở chế độ debug để dễ khắc phục sự cố

3. **Cards Application**
   - Khởi động ở chế độ debug

4. **Loans Application**
   - Khởi động ở chế độ debug

### Xác Minh Khởi Động Thành Công

Kiểm tra console logs của mỗi microservice để đảm bảo:
- Không có lỗi kết nối
- Schema scripts được thực thi thành công
- Các bảng được tạo trong database

## Bước 7: Xác Minh Tạo Bảng Database

Sử dụng MySQL client (như MySQL Workbench, DBeaver, hoặc SQL Electron) để xác minh việc tạo bảng.

### Accounts Database

**Chi Tiết Kết Nối:**
- Host: localhost
- Port: 3306
- Database: accountsDB
- Username: root
- Password: root

**Các Bảng Mong Đợi:**
- Bảng `customer`
- Bảng `accounts`

### Cards Database

**Chi Tiết Kết Nối:**
- Host: localhost
- Port: 3308
- Database: cardsDB
- Username: root
- Password: root

**Các Bảng Mong Đợi:**
- Bảng `cards`

### Loans Database

**Chi Tiết Kết Nối:**
- Host: localhost
- Port: 3307
- Database: loansDB
- Username: root
- Password: root

**Các Bảng Mong Đợi:**
- Bảng `loans`

## Bước 8: Kiểm Thử API Endpoints

Sử dụng Postman để kiểm thử các thao tác CRUD và xác minh tính bền vững của dữ liệu.

### Tạo Account

**Request:**
- Method: POST
- URL: `http://localhost:8080/api/create`
- Body:
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "mobileNumber": "1234567890"
  }
  ```

**Response:**
- Status: 201 Created
- Xác minh dữ liệu được lưu trong accounts database

### Tạo Card

**Request:**
- Method: POST
- URL: `http://localhost:9000/api/create`
- Body:
  ```json
  {
    "mobileNumber": "1234567890"
  }
  ```

**Response:**
- Status: 201 Created
- Xác minh dữ liệu được lưu trong cards database

### Tạo Loan

**Request:**
- Method: POST
- URL: `http://localhost:8090/api/create`
- Body:
  ```json
  {
    "mobileNumber": "1234567890"
  }
  ```

**Response:**
- Status: 201 Created
- Xác minh dữ liệu được lưu trong loans database

### Lấy Dữ Liệu (Fetch Data)

Kiểm thử các GET endpoints để truy xuất dữ liệu:

**Fetch Account:**
- Method: GET
- URL: `http://localhost:8080/api/fetch?mobileNumber=1234567890`

**Fetch Card:**
- Method: GET
- URL: `http://localhost:9000/api/fetch?mobileNumber=1234567890`

**Fetch Loan:**
- Method: GET
- URL: `http://localhost:8090/api/fetch?mobileNumber=1234567890`

Tất cả các request nên trả về dữ liệu đã tạo trước đó.

## Tính Bền Vững Dữ Liệu Docker Container

### Cảnh Báo Quan Trọng: Mất Dữ Liệu Khi Xóa Container

Docker containers lưu trữ dữ liệu nội bộ trong hệ thống file của chúng. **Khi bạn xóa một container, tất cả dữ liệu được lưu bên trong sẽ bị mất vĩnh viễn.**

### Các Thao Tác Vòng Đời Container

**Dừng Container:**
```bash
docker stop accountsDB
```
- Container ngừng chạy
- **Dữ liệu được bảo toàn**
- Có thể khởi động lại sau với `docker start accountsDB`

**Xóa Container:**
```bash
docker rm accountsDB
```
- Container bị xóa vĩnh viễn
- **Tất cả dữ liệu bị mất mãi mãi**
- Phải tạo container mới từ đầu

### Minh Họa: Kịch Bản Mất Dữ Liệu

Hãy minh họa điều gì xảy ra khi bạn xóa một container:

1. **Trạng Thái Ban Đầu:**
   - Cả ba database containers đang chạy
   - Dữ liệu được lưu trong tất cả databases
   - Tất cả microservices đang chạy và được kết nối

2. **Dừng Tất Cả Microservices:**
   - Dừng accounts application
   - Dừng cards application
   - Dừng loans application

3. **Dừng Tất Cả Database Containers:**
   - Dừng accounts database container
   - Dừng loans database container
   - Dừng cards database container

4. **Xóa Cards Database Container:**
   ```bash
   docker rm cardsDB
   ```
   - Cards database và tất cả dữ liệu của nó đã biến mất

5. **Khởi Động Lại Accounts và Loans Containers:**
   ```bash
   docker start accountsDB
   docker start loansDB
   ```
   - Các containers này vẫn còn dữ liệu của chúng

6. **Tạo Lại Cards Database Container:**
   ```bash
   docker run -d -p 3308:3306 --name cardsDB -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=cardsDB mysql:latest
   ```
   - Container mới được tạo
   - Database trống không có bảng hoặc dữ liệu

7. **Khởi Động Lại Tất Cả Microservices:**
   - Khởi động config server
   - Khởi động accounts application (sẽ tạo bảng qua schema.sql)
   - Khởi động cards application (sẽ tạo bảng qua schema.sql - trống rỗng)
   - Khởi động loans application (sẽ tạo bảng qua schema.sql)

8. **Kiểm Thử API Endpoints:**
   - **Fetch Account:** ✅ Hoạt động - trả về dữ liệu đã lưu
   - **Fetch Card:** ❌ Không trả về dữ liệu - database đã bị xóa
   - **Fetch Loan:** ✅ Hoạt động - trả về dữ liệu đã lưu

### Best Practices cho Quản Lý Container

**NÊN:**
- ✅ Sử dụng `docker stop` để dừng containers khi không sử dụng
- ✅ Sử dụng `docker start` để khởi động lại containers đã dừng
- ✅ Triển khai backup database thường xuyên
- ✅ Sử dụng Docker volumes để lưu trữ dữ liệu bền vững
- ✅ Ghi chép các containers nào chứa dữ liệu quan trọng

**KHÔNG NÊN:**
- ❌ Xóa containers có dữ liệu quan trọng
- ❌ Sử dụng `docker rm` mà không backup dữ liệu trước
- ❌ Chỉ dựa vào lưu trữ container cho dữ liệu quan trọng
- ❌ Quên containers nào đang dừng so với đã xóa

### Sử Dụng Docker Volumes để Bền Vững

Để ngăn chặn mất dữ liệu, sử dụng Docker volumes:

```bash
docker run -d -p 3306:3306 \
  --name accountsDB \
  -e MYSQL_ROOT_PASSWORD=root \
  -e MYSQL_DATABASE=accountsDB \
  -v accounts-data:/var/lib/mysql \
  mysql:latest
```

**Lợi Ích:**
- Dữ liệu được lưu trong named volume `accounts-data`
- Tồn tại sau khi xóa container
- Có thể tái sử dụng với containers mới
- Có thể backup riêng biệt

## Xử Lý Sự Cố

### Vấn Đề: Không Tạo Được Bảng

**Triệu Chứng:**
- Ứng dụng khởi động thành công
- Không có lỗi trong logs
- Database tồn tại nhưng không có bảng

**Nguyên Nhân:**
Property `spring.datasource.sql.init.mode: always` được đặt sai vị trí

**Giải Pháp:**
Xác minh property nằm dưới `spring.datasource`:

```yaml
spring:
  datasource:
    sql:
      init:
        mode: always  # Phải ở đây
```

### Vấn Đề: Connection Refused

**Triệu Chứng:**
- Ứng dụng không khởi động được
- Lỗi: "Connection refused" hoặc "Unable to connect to database"

**Nguyên Nhân và Giải Pháp Có Thể:**

1. **Docker container không chạy**
   - Kiểm tra: `docker ps`
   - Giải pháp: Khởi động container với `docker start <tên-container>`

2. **Số port sai**
   - Kiểm tra application.yml khớp với port mapping của container
   - Accounts: 3306, Cards: 3308, Loans: 3307

3. **Tên database sai**
   - Kiểm tra tên database trong application.yml khớp với database của container
   - Nên là: accountsDB, cardsDB, loansDB

4. **Credentials sai**
   - Kiểm tra username và password khớp với cấu hình container
   - Mặc định: root/root

### Vấn Đề: Lỗi Table Already Exists

**Triệu Chứng:**
- Lỗi khi khởi động: "Table 'accounts' already exists"

**Nguyên Nhân:**
Thiếu `IF NOT EXISTS` trong SQL scripts

**Giải Pháp:**
Cập nhật `schema.sql`:

```sql
CREATE TABLE IF NOT EXISTS accounts (
    -- định nghĩa các cột
);
```

## Tóm Tắt

### Những Gì Chúng Ta Đã Hoàn Thành

✅ Thay thế H2 in-memory database bằng MySQL  
✅ Cấu hình ba microservices kết nối với các MySQL databases riêng biệt  
✅ Kích hoạt thực thi schema tự động khi khởi động  
✅ Kiểm thử tính bền vững dữ liệu trên tất cả microservices  
✅ Hiểu vòng đời dữ liệu container và rủi ro  

### Điểm Chính Cần Nhớ

1. **Quản Lý Dependency**: Thay H2 bằng MySQL connector trong pom.xml
2. **Cấu Hình**: Đặt đúng database URL, port và credentials trong application.yml
3. **Khởi Tạo Schema**: Sử dụng `spring.datasource.sql.init.mode: always` cho MySQL
4. **SQL Scripts**: Luôn sử dụng `IF NOT EXISTS` để tránh lỗi
5. **Bảo Mật**: Không bao giờ hardcode credentials production
6. **Tính Bền Vững Dữ Liệu**: Docker containers mất dữ liệu khi bị xóa
7. **Quản Lý Container**: Dừng containers, đừng xóa chúng
8. **Best Practice**: Sử dụng Docker volumes cho dữ liệu quan trọng

### Ưu Điểm của Cấu Hình Này

✅ **Thiết Lập Nhanh**: Tạo databases nhanh chóng với Docker  
✅ **Môi Trường Cô Lập**: Mỗi microservice có database riêng  
✅ **Dễ Kiểm Thử**: Có thể tạo lại toàn bộ môi trường nhanh chóng  
✅ **Không Cần Cài Đặt**: Không cần cài MySQL trên máy host  
✅ **Di Động**: Cùng một cấu hình hoạt động trên các máy phát triển khác nhau  

### Nhược Điểm và Hạn Chế

❌ **Rủi Ro Mất Dữ Liệu**: Xóa containers làm mất tất cả dữ liệu vĩnh viễn  
❌ **Không Bền Vững Volume**: Lưu trữ container là tạm thời theo mặc định  
❌ **Quản Lý Thủ Công**: Cần nhớ dừng, không xóa containers  
❌ **Chưa Sẵn Sàng Production**: Yêu cầu cấu hình volume phù hợp cho production  
❌ **Phức Tạp Backup**: Cần các chiến lược bổ sung cho backup dữ liệu  

## Bước Tiếp Theo

1. **Triển Khai Docker Volumes**: Cấu hình lưu trữ bền vững cho databases
2. **Docker Compose**: Quản lý tất cả containers với một file compose duy nhất
3. **Biến Môi Trường**: Externalize tất cả cấu hình
4. **Di Chuyển Kubernetes**: Học container orchestration cho production
5. **Giám Sát**: Thêm giám sát database và health checks
6. **Chiến Lược Backup**: Triển khai backup database tự động

---

**Chúc Mừng!** Bạn đã tích hợp thành công các Spring Boot microservices của mình với MySQL databases cục bộ chạy trong Docker containers. Cấu hình này cung cấp môi trường phát triển thực tế hơn so với H2 in-memory databases.