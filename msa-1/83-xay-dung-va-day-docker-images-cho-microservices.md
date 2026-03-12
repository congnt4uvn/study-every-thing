# Xây Dựng và Đẩy Docker Images cho Microservices

## Tổng Quan

Hướng dẫn này bao gồm việc tạo Docker images cho tất cả các microservices bao gồm config server, và đẩy chúng lên Docker Hub. Chúng ta sẽ sử dụng Google Jib để xây dựng Docker images một cách hiệu quả cho các microservices: accounts, cards, loans và config server.

## Yêu Cầu Trước Khi Bắt Đầu

- Đã cài đặt Maven
- Đã cài đặt và chạy Docker Desktop
- Có tài khoản Docker Hub
- Dự án Spring Boot microservices (accounts, cards, loans, config server)

## Tại Sao Cần Tạo Lại Docker Images?

Chúng ta cần tạo lại Docker images cho các microservices accounts, loans và cards vì đã có nhiều thay đổi quan trọng liên quan đến quản lý cấu hình trong Spring Cloud Config.

## Cấu Trúc Dự Án

```
section-6/v2-spring-cloud-config/
├── accounts/
├── cards/
├── config-server/
└── loans/
```

## Xây Dựng Docker Images với Google Jib

### Bước 1: Xây Dựng Image cho Accounts Microservice

Điều hướng đến thư mục accounts microservice (nơi có file `pom.xml`) và chạy lệnh:

```bash
mvn compile jib:dockerBuild
```

**Lưu ý:** Chữ 'B' trong `dockerBuild` phải viết hoa.

Lệnh này sẽ:
- Tạo một Docker image mới cho accounts microservice
- Gắn thẻ (tag) là `S6`
- Hoàn thành trong khoảng 8 giây

**Tại sao dùng Jib?** Jib rất nhanh và vô cùng tiện lợi cho các hệ thống local, đó là lý do tại sao nó được sử dụng trong suốt khóa học này.

### Bước 2: Xây Dựng Image cho Cards Microservice

Điều hướng đến thư mục cards microservice và chạy cùng lệnh:

```bash
mvn compile jib:dockerBuild
```

Lệnh này tạo Docker image có tên `cards` với thẻ `S6`, hoàn thành trong khoảng 10 giây.

### Bước 3: Xây Dựng Image cho Loans Microservice

Điều hướng đến thư mục loans microservice và thực thi:

```bash
mvn compile jib:dockerBuild
```

### Bước 4: Cấu Hình Jib Plugin cho Config Server

**Quan trọng:** Lệnh tương tự sẽ không hoạt động cho config server ban đầu vì chúng ta chưa thêm thông tin plugin Jib vào file `pom.xml` của nó.

#### Thêm Jib Plugin vào Config Server

1. Mở file `pom.xml` của config server
2. Sao chép cấu hình Jib plugin từ file `pom.xml` của bất kỳ microservice nào khác
3. Thêm nó sau phần Spring Boot Maven plugin

**Ví Dụ Cấu Hình Plugin:**

```xml
<plugin>
    <groupId>com.google.cloud.tools</groupId>
    <artifactId>jib-maven-plugin</artifactId>
    <configuration>
        <to>
            <image>eazybytes/${project.artifactId}:S6</image>
        </to>
    </configuration>
</plugin>
```

Cấu hình bao gồm:
- Tên image: `eazybytes/config-server`
- Thẻ (tag): `S6`

4. Tải lại các thay đổi Maven
5. Điều hướng đến thư mục config server trong terminal
6. Chạy lệnh build:

```bash
mvn compile jib:dockerBuild
```

## Xác Minh Docker Images

### Sử Dụng Docker CLI

```bash
docker images
```

### Sử Dụng Docker Desktop Dashboard

1. Mở Docker Desktop
2. Điều hướng đến tab Images
3. Bạn sẽ thấy bốn images mới với thẻ `S6`:
   - accounts:S6
   - cards:S6
   - loans:S6
   - config-server:S6

## Dọn Dẹp Các Images Cũ

Để tiết kiệm dung lượng lưu trữ, xóa các Docker images không cần thiết từ các phần trước (ví dụ: images S4):

1. Mở Docker Desktop Dashboard
2. Điều hướng đến Images
3. Xóa các images không sử dụng:
   - Images buildpacks cũ
   - Images có thẻ Section 4 (S4) cho loans, cards, accounts
   - Các images không sử dụng khác

**Giữ lại các images sau:**
- RabbitMQ
- MySQL
- Keycloak (để test)
- Các images S6 mới nhất

### Dọn Dẹp Containers Không Sử Dụng

Kiểm tra các containers không sử dụng và xóa chúng. Ví dụ, nếu RabbitMQ container đang chạy, bạn có thể xóa nó vì Docker Compose sẽ tự động tạo lại khi cần.

## Đẩy Images Lên Docker Hub

### Yêu Cầu Trước Khi Đẩy

- Đảm bảo bạn đã đăng nhập vào Docker Desktop
- Docker phải đang chạy

### Định Dạng Lệnh Push

```bash
docker image push docker.io/<tên-docker-username>/<tên-image>:<thẻ>
```

### Quy Trình Đẩy Từng Bước

#### 1. Đẩy Accounts Image

```bash
docker image push docker.io/eazybytes/accounts:S6
```

**Lưu ý:** Image phải tồn tại trong hệ thống local của bạn thì lệnh push mới hoạt động.

Sau vài giây, Docker image của accounts sẽ được đẩy thành công lên Docker Hub.

#### 2. Đẩy Loans Image

```bash
docker image push docker.io/eazybytes/loans:S6
```

#### 3. Đẩy Cards Image

```bash
docker image push docker.io/eazybytes/cards:S6
```

#### 4. Đẩy Config Server Image

```bash
docker image push docker.io/eazybytes/config-server:S6
```

## Xác Minh Images Trên Docker Hub

1. Truy cập [Docker Hub](https://hub.docker.com/)
2. Đăng nhập vào tài khoản của bạn
3. Làm mới trang
4. Bạn sẽ thấy các repositories với images mới:
   - config-server
   - cards
   - loans
   - accounts

### Kiểm Tra Các Thẻ Image

Nhấp vào bất kỳ repository nào (ví dụ: accounts) để xem các thẻ có sẵn:
- **Thẻ S4:** Docker image từ Section 4
- **Thẻ S6:** Docker image mới nhất từ Section 6

**Lưu ý:** Config server sẽ chỉ có thẻ S6 vì không có image S4 nào được đẩy lên trước đó.

## Lợi Ích Của Việc Đẩy Lên Docker Hub

- **Lưu Trữ Từ Xa:** Images được lưu trữ trong repository từ xa
- **Truy Cập Dễ Dàng:** Bất kỳ ai cũng có thể pull và sử dụng các images này
- **Tính Công Khai:** Images được công khai để chia sẻ
- **Tích Hợp Docker Compose:** Khi chạy Docker Compose mà không có images local, nó sẽ tự động pull từ repository từ xa

## Tóm Tắt

Trong hướng dẫn này, chúng ta đã:
1. ✅ Tạo Docker images cho tất cả các microservices (accounts, cards, loans, config server) sử dụng Google Jib
2. ✅ Cấu hình Jib plugin trong file `pom.xml` của config server
3. ✅ Dọn dẹp các Docker images và containers cũ không sử dụng
4. ✅ Đẩy thành công tất cả Docker images lên Docker Hub với thẻ S6
5. ✅ Xác minh các images đã có sẵn trên Docker Hub

## Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ kiểm tra file Docker Compose với profile mặc định và xác minh rằng tất cả các thay đổi cấu hình đều hoạt động chính xác.

## Tham Khảo Các Lệnh Chính

| Hành Động | Lệnh |
|-----------|------|
| Xây dựng Docker image với Jib | `mvn compile jib:dockerBuild` |
| Liệt kê Docker images | `docker images` |
| Đẩy image lên Docker Hub | `docker image push docker.io/<username>/<image>:<tag>` |
| Xóa Docker image | `docker image rm <image-id>` |

---

**Khóa Học:** Microservices với Spring Boot  
**Phần:** 6 - Docker và Quản Lý Cấu Hình  
**Thời Gian:** Hoàn thành trong khoảng 30-40 phút