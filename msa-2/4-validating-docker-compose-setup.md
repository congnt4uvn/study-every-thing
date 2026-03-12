# Xác Thực và Khắc Phục Sự Cố Docker Compose với MySQL Databases

## Tổng Quan

Hướng dẫn này hướng dẫn quy trình xác thực cấu hình Docker Compose, xác định và khắc phục các vấn đề thường gặp, và kiểm thử toàn bộ thiết lập microservices với MySQL databases. Chúng ta sẽ đề cập đến các khái niệm quan trọng về Docker networking và kỹ thuật khắc phục sự cố.

## Yêu Cầu Tiên Quyết

- Hoàn thành cấu hình Docker Compose từ phần trước
- Docker Desktop đã cài đặt và đang chạy
- Tất cả Docker images được build với tag `s7`
- Truy cập Terminal/Command prompt
- SQL client (SQL Electron hoặc tương tự) để xác minh database
- Postman để kiểm thử API

## Bước 1: Cập Nhật Docker Image Tags

Trước khi chạy Docker Compose, đảm bảo tất cả microservice images sử dụng tag đúng.

### Vấn Đề

Nếu bạn sử dụng image tags cũ (như `s6`), những images đó chứa cấu hình H2 database, không phải MySQL. Điều này sẽ gây lỗi kết nối.

### Giải Pháp

Mở `docker-compose.yml` và cập nhật tất cả image tags từ `s6` sang `s7`:

**Trước:**
```yaml
services:
  configserver:
    image: "eazybytes/configserver:s6"  # ❌ Tag cũ
  
  accounts:
    image: "eazybytes/accounts:s6"  # ❌ Tag cũ
  
  loans:
    image: "eazybytes/loans:s6"  # ❌ Tag cũ
  
  cards:
    image: "eazybytes/cards:s6"  # ❌ Tag cũ
```

**Sau:**
```yaml
services:
  configserver:
    image: "eazybytes/configserver:s7"  # ✅ Tag mới
  
  accounts:
    image: "eazybytes/accounts:s7"  # ✅ Tag mới
  
  loans:
    image: "eazybytes/loans:s7"  # ✅ Tag mới
  
  cards:
    image: "eazybytes/cards:s7"  # ✅ Tag mới
```

**Tại sao điều này quan trọng:** Images `s7` bao gồm MySQL dependencies và configurations, trong khi images `s6` có thiết lập H2 database.

## Bước 2: Xóa Dependencies Đã Lỗi Thời

### Xóa RabbitMQ Dependency khỏi Config Server

Vì chúng ta đã xóa Spring Cloud Bus, Config Server không còn phụ thuộc vào RabbitMQ.

**Tìm đoạn này trong docker-compose.yml:**
```yaml
configserver:
  image: "eazybytes/configserver:s7"
  depends_on:
    - rabbit  # ❌ Service này không còn tồn tại
```

**Sửa:**
```yaml
configserver:
  image: "eazybytes/configserver:s7"
  # Xóa depends_on hoàn toàn, hoặc xóa rabbit khỏi danh sách
```

**Lỗi bạn sẽ thấy nếu không sửa:**
```
Error: config server depends on undefined service: rabbit
```

## Bước 3: Lần Thử Docker Compose Đầu Tiên

Điều hướng đến thư mục Docker Compose và chạy lệnh.

### Điều Hướng Đến Thư Mục

```bash
cd docker-compose/default
```

### Chạy Docker Compose

```bash
docker-compose up
```

**Điều gì xảy ra:**
- Database containers khởi động trước
- Sau khi healthy, microservices bắt đầu khởi động
- Logs xuất hiện trong terminal (chưa dùng detached mode)

### Thứ Tự Khởi Động Mong Đợi

1. **Database containers** (accountsdb, loansdb, cardsdb)
2. **Config Server** (sau khi databases healthy)
3. **Microservices** (accounts, loans, cards - sau khi Config Server healthy)

## Bước 4: Xác Định Vấn Đề Cấu Hình Port

### Vấn Đề Bất Ngờ

Sau khi đợi containers khởi động, bạn sẽ nhận thấy:

✅ **Khởi động thành công:**
- accountsdb
- loansdb
- cardsdb
- configserver
- accounts microservice

❌ **Thất bại khi khởi động:**
- cards microservice
- loans microservice

### Xem Lỗi

**Trong Docker Desktop:**
1. Click vào container thất bại (cards hoặc loans)
2. Kiểm tra logs

**Thông báo lỗi:**
```
Unable to connect to database
Connection refused to loansdb:3307
Connection refused to cardsdb:3308
```

## Bước 5: Hiểu Về Docker Networking

### Nguyên Nhân Gốc Rễ

**Cấu hình của bạn:**
```yaml
loans:
  environment:
    SPRING_DATASOURCE_URL: jdbc:mysql://loansdb:3307/loansDB  # ❌ Port sai

cards:
  environment:
    SPRING_DATASOURCE_URL: jdbc:mysql://cardsdb:3308/cardsDB  # ❌ Port sai
```

### Tại Sao Điều Này Sai

**Khái niệm quan trọng:** Có sự khác biệt giữa **external ports** (host) và **internal ports** (container network).

**Cú pháp port mapping:** `HOST_PORT:CONTAINER_PORT`

```yaml
loansdb:
  ports:
    - "3307:3306"  # Host port 3307 → Container port 3306

cardsdb:
  ports:
    - "3308:3306"  # Host port 3308 → Container port 3306
```

### Giao Tiếp External vs Internal

**Giao Tiếp External** (từ máy host của bạn):
- Sử dụng: `localhost:3307` cho loansdb
- Sử dụng: `localhost:3308` cho cardsdb
- Ví dụ: SQL Electron kết nối từ máy tính của bạn

**Giao Tiếp Internal** (giữa các containers):
- Sử dụng: `loansdb:3306` (service name + internal port)
- Sử dụng: `cardsdb:3306` (service name + internal port)
- Ví dụ: Microservices kết nối đến databases

### Tại Sao Port Mapping Tồn Tại

**Câu hỏi:** Nếu containers giao tiếp trên port 3306, tại sao map sang 3307 và 3308?

**Trả lời:** Port mapping chỉ dành cho **truy cập external**:
- Cho phép SQL clients trên host kết nối
- Kích hoạt debugging và xác minh dữ liệu
- Ngăn xung đột port (không thể có ba services trên port 3306 trên host)

**Quan trọng:** Port mapping **không cần thiết** cho giao tiếp container-to-container. Nó hoàn toàn dành cho truy cập từ host.

## Bước 6: Sửa Cấu Hình Port

Cập nhật datasource URLs để sử dụng internal container ports.

### Cấu Hình Đúng

```yaml
accounts:
  environment:
    SPRING_DATASOURCE_URL: jdbc:mysql://accountsdb:3306/accountsDB  # ✅ Đúng

loans:
  environment:
    SPRING_DATASOURCE_URL: jdbc:mysql://loansdb:3306/loansDB  # ✅ Đã sửa

cards:
  environment:
    SPRING_DATASOURCE_URL: jdbc:mysql://cardsdb:3306/cardsDB  # ✅ Đã sửa
```

**Điểm chính:** Tất cả kết nối database từ microservices sử dụng port **3306** (internal container port), không phải các external mapped ports.

## Bước 7: Khởi Động Lại Docker Compose

### Dừng Containers Đang Chạy

Nhấn `Ctrl+C` trong terminal nơi `docker-compose up` đang chạy.

**Điều này chỉ dừng containers, không xóa chúng.**

### Xóa Containers

```bash
docker-compose down
```

**Lệnh này:**
- Dừng tất cả containers
- Xóa tất cả containers
- Xóa network
- KHÔNG xóa volumes hoặc images

### Khởi Động với Detached Mode

```bash
docker-compose up -d
```

**Flag `-d`:**
- Chạy containers ở background (detached mode)
- Giải phóng terminal cho các lệnh khác
- Logs vẫn truy cập được qua `docker logs` hoặc Docker Desktop

## Bước 8: Cập Nhật Cấu Hình QA và Prod

Áp dụng các sửa chữa tương tự cho các môi trường khác.

### Copy Cấu Hình Default

**Cho Prod:**
1. Mở `docker-compose-prod.yml`
2. Copy tất cả nội dung từ `docker-compose.yml` (default)
3. Paste vào `docker-compose-prod.yml`

**Cho QA:**
1. Mở `docker-compose-qa.yml`
2. Copy tất cả nội dung từ `docker-compose.yml` (default)
3. Paste vào `docker-compose-qa.yml`

### Cập Nhật Common Config cho Prod

**Trong common-config.yml cho prod:**
```yaml
microservice-configserver-config:
  extends:
    service: microservice-base-config
  environment:
    SPRING_PROFILES_ACTIVE: prod  # ✅ Đổi thành prod
    SPRING_CONFIG_IMPORT: configserver:http://configserver:8071/
    SPRING_DATASOURCE_USERNAME: root
    SPRING_DATASOURCE_PASSWORD: root
```

### Cập Nhật Common Config cho QA

**Trong common-config.yml cho qa:**
```yaml
microservice-configserver-config:
  extends:
    service: microservice-base-config
  environment:
    SPRING_PROFILES_ACTIVE: qa  # ✅ Đổi thành qa
    SPRING_CONFIG_IMPORT: configserver:http://configserver:8071/
    SPRING_DATASOURCE_USERNAME: root
    SPRING_DATASOURCE_PASSWORD: root
```

## Bước 9: Xác Minh Khởi Động Thành Công

### Kiểm Tra Docker Desktop

Mở Docker Desktop và xác minh tất cả 7 containers đang chạy:

✅ **Database Containers:**
- accountsdb
- loansdb
- cardsdb

✅ **Application Containers:**
- configserver
- accounts
- loans
- cards

### Giám Sát Logs Khởi Động

Click vào từng microservice container để xem logs:

**Cho Cards microservice:**
```
Added connection to database
Created connection pool
Started CardsApplication in X seconds
```

**Cho Loans microservice:**
```
Added connection to database
Created connection pool
Started LoansApplication in X seconds
```

**Các thông báo log này xác nhận kết nối database thành công.**

## Bước 10: Kiểm Thử REST APIs với Postman

Xác minh tất cả microservices hoạt động đúng.

### Kiểm Thử Create Account

**Request:**
- Method: POST
- URL: `http://localhost:8080/api/create`
- Body:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "mobileNumber": "9876543210"
}
```

**Response Mong Đợi:**
- Status: 201 Created
- Thông báo thành công

### Kiểm Thử Create Card

**Request:**
- Method: POST
- URL: `http://localhost:9000/api/create`
- Body:
```json
{
  "mobileNumber": "9876543210"
}
```

**Response Mong Đợi:**
- Status: 201 Created
- Chi tiết card được trả về

### Kiểm Thử Create Loan

**Request:**
- Method: POST
- URL: `http://localhost:8090/api/create`
- Body:
```json
{
  "mobileNumber": "9876543210"
}
```

**Response Mong Đợi:**
- Status: 201 Created
- Chi tiết loan được trả về

**Kết quả:** Cả ba APIs nên trả về responses thành công.

## Bước 11: Xác Minh Tính Bền Vững Database

Sử dụng SQL Electron (hoặc bất kỳ MySQL client nào) để xác minh dữ liệu đã được lưu.

### Chi Tiết Kết Nối

**Accounts Database:**
- Host: localhost
- Port: 3306
- Database: accountsDB
- Username: root
- Password: root

**Loans Database:**
- Host: localhost
- Port: 3307 ⭐ (external port)
- Database: loansDB
- Username: root
- Password: root

**Cards Database:**
- Host: localhost
- Port: 3308 ⭐ (external port)
- Database: cardsDB
- Username: root
- Password: root

### Xác Minh Dữ Liệu

**Trong Accounts Database:**
1. Kết nối đến accountsdb
2. Kiểm tra bảng `accounts` - nên có dữ liệu account
3. Kiểm tra bảng `customer` - nên có dữ liệu customer

**Trong Loans Database:**
1. Kết nối đến loansdb
2. Kiểm tra bảng `loans` - nên có dữ liệu loan

**Trong Cards Database:**
1. Kết nối đến cardsdb
2. Kiểm tra bảng `cards` - nên có dữ liệu card

**Thành công:** Tất cả bảng chứa dữ liệu bạn đã tạo qua REST APIs.

## Bước 12: Kết Nối Với External Databases

### Kịch Bản: Sử Dụng Cloud hoặc Remote Databases

Nếu bạn không sử dụng local Docker database containers? Nếu bạn có:
- Development database trong cloud (AWS RDS, Azure SQL, v.v.)
- Shared development database server
- Managed database service

### Thay Đổi Đơn Giản

**Bạn không cần database containers trong docker-compose.yml.**

Xóa các services này:
```yaml
# Xóa hoàn toàn
accountsdb:
  # ... tất cả cấu hình database

loansdb:
  # ... tất cả cấu hình database

cardsdb:
  # ... tất cả cấu hình database
```

### Cập Nhật Datasource URLs

Trỏ trực tiếp đến external databases:

```yaml
accounts:
  environment:
    SPRING_DATASOURCE_URL: jdbc:mysql://dev-db.example.com:3306/accountsDB
    # Hoặc sử dụng public IP: jdbc:mysql://52.123.45.67:3306/accountsDB

loans:
  environment:
    SPRING_DATASOURCE_URL: jdbc:mysql://dev-db.example.com:3306/loansDB

cards:
  environment:
    SPRING_DATASOURCE_URL: jdbc:mysql://dev-db.example.com:3306/cardsDB
```

### Cập Nhật Credentials

Sử dụng credentials phù hợp cho external database:

```yaml
microservice-configserver-config:
  environment:
    SPRING_DATASOURCE_USERNAME: dev_user  # Không phải root
    SPRING_DATASOURCE_PASSWORD: secure_password
```

**Best Practice:** Sử dụng environment variables hoặc secrets cho production credentials:

```yaml
environment:
  SPRING_DATASOURCE_USERNAME: ${DB_USERNAME}
  SPRING_DATASOURCE_PASSWORD: ${DB_PASSWORD}
```

### Xóa Database Dependencies

Xóa `depends_on` cho databases:

```yaml
accounts:
  depends_on:
    configserver:
      condition: service_healthy
    # Xóa accountsdb dependency
```

**Tại sao:** External databases đã chạy rồi; không cần đợi chúng khởi động.

## Tóm Tắt Khái Niệm Docker Networking

### Container Networks

Khi sử dụng Docker Compose:
- Tất cả services trong cùng compose file chia sẻ một network
- Containers giao tiếp sử dụng **service names** làm hostnames
- Không cần biết địa chỉ IP

### Giải Thích Port Mapping

**Cú pháp:** `HOST_PORT:CONTAINER_PORT`

```yaml
ports:
  - "8080:8080"  # Host 8080 → Container 8080
  - "3307:3306"  # Host 3307 → Container 3306
```

**Hai góc nhìn:**

**Từ Host (máy tính của bạn):**
- Truy cập accounts microservice: `http://localhost:8080`
- Truy cập loans database: `localhost:3307`

**Từ Bên Trong Containers:**
- Truy cập accounts microservice: `http://accounts:8080`
- Truy cập loans database: `loansdb:3306`

### Khi Nào Port Mapping Cần Thiết

✅ **Cần port mapping:**
- Truy cập services từ máy host
- Sử dụng SQL clients từ máy tính của bạn
- Kiểm thử APIs từ Postman trên host
- Debugging từ IDE trên host

❌ **Không cần port mapping:**
- Giao tiếp container-to-container
- Microservice kết nối đến database
- Service discovery trong Docker network

**Ví dụ:** Nếu bạn chỉ cần microservices giao tiếp với databases (không truy cập external), bạn có thể bỏ qua port mapping hoàn toàn:

```yaml
loansdb:
  # Không cần phần ports cho truy cập chỉ internal
  image: mysql:latest
```

## Hướng Dẫn Khắc Phục Sự Cố

### Vấn Đề 1: Lỗi Undefined Service

**Lỗi:**
```
Error: configserver depends on undefined service: rabbit
```

**Nguyên nhân:** Tham chiếu đến service không tồn tại trong docker-compose.yml

**Giải pháp:** Xóa dependency hoặc thêm service còn thiếu

### Vấn Đề 2: Connection Refused

**Lỗi:**
```
Unable to connect to database
Connection refused to loansdb:3307
```

**Nguyên nhân:** Sử dụng external port thay vì internal container port

**Giải pháp:** Đổi datasource URL để sử dụng internal port (3306)

### Vấn Đề 3: Cấu Hình Database Sai

**Lỗi:**
```
Table doesn't exist
Schema not found
```

**Nguyên nhân:** Sử dụng Docker images cũ với cấu hình H2

**Giải pháp:** Rebuild images với tag đúng và MySQL dependencies

### Vấn Đề 4: Container Không Khởi Động

**Lỗi:**
```
Container exits immediately
Unhealthy status
```

**Nguyên nhân:** Nhiều khả năng
- Dependencies còn thiếu
- Lỗi cấu hình
- Health check thất bại

**Giải pháp:** 
- Kiểm tra logs: `docker logs <tên-container>`
- Xác minh cấu hình health check
- Đảm bảo dependencies healthy trước

### Vấn Đề 5: Không Thể Truy Cập Từ Host

**Lỗi:**
```
Cannot connect to localhost:3307 from SQL client
```

**Nguyên nhân:** Port mapping chưa được cấu hình

**Giải pháp:** Thêm port mapping trong docker-compose.yml

## Các Lệnh Docker Compose Hữu Ích

### Khởi Động Services

```bash
# Khởi động ở foreground (xem logs)
docker-compose up

# Khởi động ở background (detached)
docker-compose up -d

# Khởi động service cụ thể
docker-compose up -d accounts

# Rebuild và khởi động
docker-compose up --build
```

### Dừng Services

```bash
# Dừng containers (không xóa)
docker-compose stop

# Dừng và xóa containers, networks
docker-compose down

# Dừng và xóa containers, networks, volumes
docker-compose down -v

# Dừng service cụ thể
docker-compose stop accounts
```

### Xem Trạng Thái và Logs

```bash
# Liệt kê containers đang chạy
docker-compose ps

# Xem logs (tất cả services)
docker-compose logs

# Xem logs (service cụ thể)
docker-compose logs accounts

# Theo dõi logs real-time
docker-compose logs -f

# Xem 100 dòng cuối
docker-compose logs --tail=100
```

### Khởi Động Lại Services

```bash
# Khởi động lại tất cả services
docker-compose restart

# Khởi động lại service cụ thể
docker-compose restart accounts
```

### Thực Thi Lệnh Trong Containers

```bash
# Mở shell trong container
docker-compose exec accounts sh

# Chạy lệnh trong container
docker-compose exec accountsdb mysql -u root -p
```

## Best Practices

✅ **Luôn sử dụng detached mode trong production** (flag `-d`)  
✅ **Sử dụng internal ports đúng cho giao tiếp container**  
✅ **Giữ image tags cập nhật và nhất quán**  
✅ **Giám sát logs sau khởi động để xác minh kết nối**  
✅ **Sử dụng health checks cho tất cả services**  
✅ **Xóa dependencies lỗi thời**  
✅ **Kiểm thử APIs sau deployment**  
✅ **Xác minh tính bền vững database**  

❌ **Không sử dụng external ports cho giao tiếp container-to-container**  
❌ **Không để lại service dependencies lỗi thời**  
❌ **Không sử dụng image tags cũ với cấu hình sai**  
❌ **Không bỏ qua xác minh logs**  
❌ **Không hardcode production credentials**  

## Tóm Tắt

### Những Gì Chúng Ta Đã Hoàn Thành

✅ Cập nhật Docker image tags từ s6 sang s7  
✅ Xóa RabbitMQ dependencies lỗi thời  
✅ Xác định và sửa vấn đề cấu hình port  
✅ Hiểu các khái niệm Docker networking  
✅ Khởi động thành công tất cả 7 containers  
✅ Kiểm thử tất cả REST APIs  
✅ Xác minh tính bền vững database  
✅ Học về cấu hình external database  

### Điểm Chính Cần Nhớ

1. **Image Tags Quan Trọng:** Sử dụng tags đúng khớp với cấu hình của bạn
2. **Internal vs External Ports:** Containers dùng internal ports (3306), host dùng mapped ports (3307, 3308)
3. **Service Names:** Sử dụng service names cho giao tiếp container-to-container
4. **Health Checks:** Quan trọng cho thứ tự khởi động đúng
5. **Detached Mode:** Sử dụng `-d` cho thực thi background
6. **External Databases:** Có thể bỏ qua database containers khi sử dụng remote databases
7. **Troubleshooting:** Kiểm tra logs và hiểu thông báo lỗi

### Điểm Chính Docker Networking

- **Service Name = Hostname** trong Docker networks
- **Port Mapping** chỉ dành cho external access
- **Giao tiếp internal** luôn sử dụng container ports
- **Xung đột external port** được ngăn chặn bởi mappings khác nhau

## Bước Tiếp Theo

Bây giờ mọi thứ đã hoạt động:

1. **Khám phá Docker volumes** cho tính bền vững dữ liệu
2. **Triển khai secrets management** cho credentials
3. **Thêm monitoring và observability**
4. **Học Docker Compose scaling**
5. **Khám phá Kubernetes** cho production deployments
6. **Triển khai CI/CD pipelines**
7. **Thêm API Gateway** cho unified access point
8. **Triển khai service mesh** cho advanced networking

---

**Chúc Mừng!** Bạn đã xác thực và khắc phục sự cố thành công toàn bộ thiết lập Docker Compose với Spring Boot microservices và MySQL databases. Bây giờ bạn hiểu Docker networking và có thể tự tin deploy containerized microservices.