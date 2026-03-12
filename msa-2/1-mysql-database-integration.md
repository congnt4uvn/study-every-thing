# Tích Hợp Cơ Sở Dữ Liệu MySQL cho Microservices

## Tổng Quan

Phần này tập trung vào việc di chuyển các microservices từ cơ sở dữ liệu H2 in-memory sang cơ sở dữ liệu MySQL để sẵn sàng cho môi trường production. Cơ sở dữ liệu H2 không được khuyến nghị cho các dự án thực tế hoặc ứng dụng production, do đó việc di chuyển này rất quan trọng cho các triển khai doanh nghiệp.

## Yêu Cầu Tiên Quyết

- Docker Desktop đã được cài đặt và đang chạy
- Ba microservices: accounts (tài khoản), loans (khoản vay), và cards (thẻ)
- Kiến thức về Spring Boot application
- Hiểu biết cơ bản về lệnh Docker

## Thiết Lập Dự Án

### 1. Cấu Trúc Thư Mục Dự Án

Tạo một thư mục section mới (Section 7) và sao chép codebase hiện có:

```
Section 7/
├── accounts/
├── loans/
├── cards/
├── configserver/
└── docker-compose/
```

Sao chép code từ `v2-spring-cloud-config` vào thư mục Section 7 mới.

### 2. Xóa Dependencies Spring Cloud Bus

Trước khi tích hợp MySQL, hãy xóa các dependencies Spring Cloud Bus và Config Monitor để giảm tải hệ thống và đơn giản hóa kiến trúc.

#### Thay Đổi Config Server

**pom.xml** - Xóa các dependencies:
- `spring-cloud-starter-bus-amqp`
- `spring-cloud-config-monitor`

**application.yml** - Xóa:
- Các thuộc tính kết nối RabbitMQ
- Giữ lại các thuộc tính actuator management để refresh thủ công
- Giữ lại cấu hình readiness và liveness probe

#### Thay Đổi Microservices (accounts, loans, cards)

Cho mỗi microservice:

**pom.xml** - Xóa:
- `spring-cloud-starter-bus-amqp`

**application.yml** - Xóa:
- Các thuộc tính kết nối RabbitMQ

## Thiết Lập Cơ Sở Dữ Liệu MySQL với Docker

### Tại Sao Dùng Docker cho MySQL?

- **Không cần cài đặt thủ công** - Tránh tiêu tốn dung lượng đĩa
- **Thiết lập nhanh** - Cơ sở dữ liệu sẵn sàng trong dưới 10 giây
- **Dễ dàng dọn dẹp** - Chỉ cần dừng/xóa containers khi hoàn tất
- **Môi trường cô lập** - Mỗi container chạy trong hệ sinh thái riêng

### Tạo MySQL Containers

#### 1. Cơ Sở Dữ Liệu Accounts

```bash
docker run -p 3306:3306 --name accountsdb -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=accountsdb -d mysql
```

**Giải thích các tham số:**
- `-p 3306:3306` - Ánh xạ cổng (host:container)
- `--name accountsdb` - Tên container
- `-e MYSQL_ROOT_PASSWORD=root` - Mật khẩu user root
- `-e MYSQL_DATABASE=accountsdb` - Tạo database khi khởi động
- `-d` - Chế độ detached (chạy nền)
- `mysql` - Tên Docker image

#### 2. Cơ Sở Dữ Liệu Loans

```bash
docker run -p 3307:3306 --name loansdb -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=loansdb -d mysql
```

**Lưu ý:** Cổng 3307 được sử dụng trên host vì 3306 đã bị accountsdb chiếm dụng.

#### 3. Cơ Sở Dữ Liệu Cards

```bash
docker run -p 3308:3306 --name cardsdb -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=cardsdb -d mysql
```

### Khái Niệm Quan Trọng về Ánh Xạ Cổng

- **Cổng nội bộ container** (3306): Giống nhau cho tất cả containers do mạng bị cô lập
- **Cổng ngoại vi host** (3306, 3307, 3308): Phải là duy nhất trên hệ thống local
- Mỗi container có hệ sinh thái mạng cô lập riêng
- Ánh xạ cổng bên ngoài cho phép các microservices local kết nối

## Xác Minh Kết Nối Cơ Sở Dữ Liệu

### Sử Dụng SQLElectron Client

SQLElectron là một SQL client nhẹ, đa nền tảng hỗ trợ nhiều loại cơ sở dữ liệu.

**Tải về:** [https://sqlectron.github.io/](https://sqlectron.github.io/)

### Cấu Hình Kết Nối

#### Cơ Sở Dữ Liệu Accounts
- **Địa chỉ Server:** localhost
- **Cổng:** 3306
- **Tên người dùng:** root
- **Mật khẩu:** root
- **Database:** accountsdb

#### Cơ Sở Dữ Liệu Loans
- **Địa chỉ Server:** localhost
- **Cổng:** 3307
- **Tên người dùng:** root
- **Mật khẩu:** root
- **Database:** loansdb

#### Cơ Sở Dữ Liệu Cards
- **Địa chỉ Server:** localhost
- **Cổng:** 3308
- **Tên người dùng:** root
- **Mật khẩu:** root
- **Database:** cardsdb

## Thực Hành Tốt Nhất

### Mẫu Database cho Mỗi Microservice

Mỗi microservice nên có cơ sở dữ liệu riêng để đảm bảo:
- **Cô lập dữ liệu** - Không có phụ thuộc dữ liệu giữa các services
- **Mở rộng độc lập** - Mở rộng databases dựa trên nhu cầu của từng service
- **Cô lập lỗi** - Vấn đề trong một database không ảnh hưởng đến các database khác
- **Linh hoạt công nghệ** - Các microservices khác nhau có thể sử dụng công nghệ database khác nhau

### Development vs Production

- **Development:** Sử dụng Docker containers cho MySQL databases local
- **Production:** Sử dụng các dịch vụ database được quản lý bởi đội ngũ infrastructure
- **QA/Dev Servers:** Kết nối đến các database servers dùng chung do đội ngũ infrastructure cung cấp

## Khắc Phục Sự Cố

### Lỗi Cổng Đã Được Sử Dụng

**Vấn đề:** `failed to start because port 3306 is already being used`

**Giải pháp:** Sử dụng cổng host khác (ví dụ: 3307, 3308) trong khi giữ cổng container là 3306

### Tên Container Đã Tồn Tại

**Vấn đề:** `container name already exists`

**Giải pháp:** Xóa container hiện có và thử lại
```bash
docker rm <tên-container>
```

## Cân Nhắc về Yêu Cầu Hệ Thống

- **Hệ thống 8GB RAM:** Cần lưu ý khi chạy nhiều containers
- **Hệ thống 16GB+ RAM:** Hiệu suất tốt hơn với nhiều containers
- Xóa các dependencies không cần thiết (như RabbitMQ) giúp giảm tải hệ thống

## Các Bước Tiếp Theo

Giai đoạn tiếp theo bao gồm:
1. Sửa đổi code microservice để kết nối với MySQL databases
2. Cấu hình các thuộc tính Spring Boot cho MySQL
3. Thiết lập JPA/Hibernate cho MySQL
4. Tạo database schemas và tables
5. Kiểm thử microservices với MySQL backend

## Tóm Tắt

- Di chuyển từ H2 sang MySQL để sẵn sàng cho production
- Sử dụng Docker để thiết lập và quản lý MySQL dễ dàng
- Tạo ba databases riêng biệt cho ba microservices
- Xóa các dependencies Spring Cloud Bus để tối ưu hóa việc sử dụng tài nguyên
- Xác minh kết nối database bằng SQLElectron client
- Sẵn sàng tích hợp MySQL với code microservices

---

**Thời lượng:** Thiết lập nhanh (dưới 10 giây mỗi database)  
**Độ khó:** Cơ bản đến Trung cấp  
**Công nghệ:** Docker, MySQL, Spring Boot, Microservices