# Lưu Trữ Cấu Hình Microservices Trong Config Server

## Tổng Quan
Bài học này trình bày cách lưu trữ tất cả cấu hình của microservices bên trong classpath của Spring Cloud Config Server và làm cho chúng có thể truy cập được bởi các microservices riêng lẻ.

## Thiết Lập Tên Ứng Dụng Cho Config Server

Đầu tiên, cấu hình tên ứng dụng cho Config Server trong file `application.yml`:

```yaml
spring:
  application:
    name: configserver
```

**Quan trọng:** Tất cả các ứng dụng Spring Boot nên có tên được gán thông qua thuộc tính `spring.application.name`. Điều này rất cần thiết để Spring Cloud Config Server hoạt động đúng cách.

## Tạo Cấu Trúc Thư Mục Cấu Hình

1. Tạo thư mục `config` bên trong thư mục `resources`
2. Thư mục này sẽ lưu trữ tất cả cấu hình liên quan đến microservices

## Quy Ước Đặt Tên Cho File Cấu Hình

### Thách Thức
Nếu nhiều microservices sử dụng cùng tên file (ví dụ: `application.yml`, `application-prod.yml`), sẽ tạo ra sự nhầm lẫn cho Config Server.

### Giải Pháp
Đặt tên file cấu hình sử dụng tên microservice/ứng dụng làm tiền tố:

- `accounts.yml` - Profile mặc định cho microservice accounts
- `accounts-prod.yml` - Profile production cho microservice accounts
- `accounts-qa.yml` - Profile QA cho microservice accounts

**Quan trọng:** Sử dụng dấu gạch ngang (`-`) không phải dấu gạch dưới (`_`) làm ký tự phân cách.

## Thiết Lập File Cấu Hình

### File Cho Microservice Accounts

Tạo ba file cấu hình trong thư mục `config`:

1. **accounts.yml** - Chứa thuộc tính profile mặc định
2. **accounts-prod.yml** - Chứa thuộc tính profile production  
3. **accounts-qa.yml** - Chứa thuộc tính profile QA

### Hướng Dẫn Về Nội Dung

Mỗi file nên chứa:
- Thông tin phiên bản build
- Thông điệp đặc thù cho microservice
- Chi tiết liên hệ
- Thông tin hỗ trợ on-call

**Loại bỏ khỏi các file này:**
- Cấu hình `server.port`
- Thuộc tính kết nối cơ sở dữ liệu (ví dụ: cài đặt H2)
- Câu lệnh `spring.config.import`

Các thuộc tính này được quản lý bởi các microservices riêng lẻ, không được externalize.

### Microservices Cards và Loans

Theo cùng mẫu, tạo:
- `cards.yml`, `cards-prod.yml`, `cards-qa.yml`
- `loans.yml`, `loans-prod.yml`, `loans-qa.yml`

## Cấu Hình Spring Cloud Config Server

Cập nhật file `application.yml` của Config Server:

```yaml
spring:
  application:
    name: configserver
  profiles:
    active: native
  cloud:
    config:
      server:
        native:
          search-locations: classpath:/config
```

### Giải Thích Cấu Hình

- **`spring.profiles.active: native`** - Kích hoạt profile native, bắt buộc khi sử dụng classpath để lưu trữ cấu hình
- **`spring.cloud.config.server.native.search-locations`** - Chỉ định vị trí lưu trữ cấu hình (`classpath:/config`)

## Build và Khởi Động Config Server

1. Bật annotation processing (cần thiết cho Lombok)
2. Build ứng dụng
3. Khởi động ở chế độ debug
4. Server sẽ khởi động trên cổng 8071

## Xác Thực Configuration Server

### Các API Endpoint

Config Server cung cấp các đường dẫn GET API để lấy cấu hình:

```
http://localhost:8071/{application}/{profile}
```

### Ví Dụ

- `http://localhost:8071/accounts/prod` - Profile production cho accounts
- `http://localhost:8071/accounts/qa` - Profile QA cho accounts
- `http://localhost:8071/accounts/default` - Profile mặc định cho accounts
- `http://localhost:8071/loans/prod` - Profile production cho loans
- `http://localhost:8071/cards/qa` - Profile QA cho cards

### Hành Vi Mong Đợi

Khi truy cập một profile cụ thể:
- Các thuộc tính từ profile được yêu cầu sẽ được tải
- Các thuộc tính từ profile mặc định cũng được tải
- Trong quá trình khởi động microservice, các thuộc tính của profile cụ thể sẽ ghi đè giá trị mặc định

### Định Dạng Response

API trả về JSON chứa:
- Thuộc tính của profile cụ thể
- Thuộc tính của profile mặc định
- Metadata cấu hình

**Mẹo:** Cài đặt extension Chrome "JSON View" để xem response JSON được định dạng đẹp.

## Các Vấn Đề Thường Gặp

### Đặt Tên File Không Đúng
**Vấn đề:** Sử dụng dấu gạch dưới (`_`) thay vì dấu gạch ngang (`-`) trong tên file (ví dụ: `accounts_prod.yml`)

**Giải pháp:** Sử dụng dấu gạch ngang: `accounts-prod.yml`

Đây là quy ước đặt tên quan trọng - thậm chí một lỗi ký tự đơn cũng có thể gây ra lỗi tải cấu hình.

## Tóm Tắt

Đã hoàn thành thành công:
1. ✅ Tạo Config Server với tên ứng dụng
2. ✅ Thiết lập cấu trúc thư mục cấu hình
3. ✅ Tạo file cấu hình cho microservices accounts, cards, và loans
4. ✅ Cấu hình native profile cho lưu trữ classpath
5. ✅ Khởi động và xác thực Config Server
6. ✅ Xác minh tất cả profiles tải đúng thông qua các API endpoint

## Các Bước Tiếp Theo

Bài học tiếp theo sẽ đề cập đến việc thiết lập kết nối giữa các microservices riêng lẻ và Spring Cloud Config Server, cho phép các microservices lấy cấu hình của chúng trong quá trình khởi động dựa trên profile đang hoạt động.