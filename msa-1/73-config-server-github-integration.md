# Lưu Trữ Thuộc Tính Cấu Hình trong GitHub Repository

## Tổng Quan

Hướng dẫn này giải thích cách cấu hình Spring Cloud Config Server để lưu trữ và tải các thuộc tính cấu hình từ kho lưu trữ GitHub. Đây là phương pháp được khuyến nghị nhất do các ưu điểm về bảo mật, quản lý phiên bản và khả năng kiểm tra.

## Ưu Điểm của Phương Pháp GitHub

- **Bảo mật**: Bảo vệ kho lưu trữ GitHub của bạn để kiểm soát quyền truy cập
- **Quản lý phiên bản**: Theo dõi các thay đổi theo thời gian với lịch sử Git
- **Kiểm tra**: Xem lại các cấu hình lịch sử từ nhiều tháng hoặc năm trước
- **Tốt hơn các giải pháp thay thế**: Phương pháp file system và classpath không hỗ trợ quản lý phiên bản

## Thiết Lập GitHub Repository

### Cấu Trúc Repository

Tạo một kho lưu trữ GitHub (ví dụ: `eazybytes-config`) với cấu trúc sau:

```
eazybytes-config/
├── accounts.yml
├── cards.yml
├── loans.yml
├── eureka-server.yml
└── gateway-server.yml
```

### Repository Công Khai vs Riêng Tư

- **Phát triển/Học tập**: Repository công khai có thể chấp nhận được
- **Môi trường Production**: Luôn sử dụng repository riêng tư với xác thực

## Cấu Hình Config Server

### Bước 1: Cập Nhật Application Profile

Trong `application.yml` của Config Server, thay đổi profile hoạt động từ `native` sang `git`:

```yaml
spring:
  profiles:
    active: git
```

### Bước 2: Cấu Hình Thuộc Tính Git

Comment cấu hình native và thêm cấu hình Git:

```yaml
spring:
  cloud:
    config:
      server:
        # native:
        #   search-locations: "classpath:/config"
        git:
          uri: https://github.com/your-username/eazybytes-config.git
          default-label: main
          timeout: 5
          clone-on-start: true
          force-pull: true
```

## Giải Thích Các Thuộc Tính Cấu Hình

### uri
- **Mô tả**: URL kho lưu trữ GitHub
- **Định dạng**: HTTPS URL của repository của bạn
- **Ví dụ**: `https://github.com/your-username/eazybytes-config.git`

### default-label
- **Mô tả**: Tên nhánh mặc định để sử dụng
- **Giá trị**: `main` (hoặc `master` tùy thuộc vào repository của bạn)
- **Mục đích**: Chỉ định nhánh nào để đọc cấu hình

### timeout
- **Mô tả**: Thời gian chờ tối đa cho kết nối GitHub
- **Giá trị**: `5` (giây)
- **Mục đích**: Fail nhanh nếu không thể kết nối đến kho lưu trữ GitHub
- **Lợi ích**: Cảnh báo ngoại lệ ngay lập tức cho nhóm vận hành/phát triển

### clone-on-start
- **Mô tả**: Clone repository trong quá trình khởi động
- **Giá trị**: `true`
- **Mục đích**: Đảm bảo cấu hình có sẵn ngay lập tức
- **Quan trọng**: Không có thuộc tính này, việc clone xảy ra khi có request đầu tiên, có thể gây ra vấn đề khởi động

### force-pull
- **Mô tả**: Ghi đè các thay đổi cục bộ khi khởi động lại
- **Giá trị**: `true`
- **Mục đích**: Luôn đồng bộ với remote repository (vị trí chính)
- **Lợi ích**: Ngăn chặn các thay đổi cục bộ ảnh hưởng đến cấu hình

## Kiểm Tra Cấu Hình

### 1. Xác Minh Config Server

Khởi động Config Server và xác minh nó đang sử dụng Git profile bằng cách kiểm tra console logs.

### 2. Kiểm Tra Truy Xuất Cấu Hình

Truy cập endpoint của Config Server:

```
http://localhost:8071/accounts/prod
```

Bạn sẽ thấy:
- Các thuộc tính cấu hình từ kho lưu trữ GitHub
- Liên kết URL GitHub trong response

### 3. Kiểm Tra Tích Hợp Microservices

Khởi động các microservices theo thứ tự:
1. Config Server
2. Accounts Microservice
3. Loans Microservice
4. Cards Microservice

Kiểm tra endpoint contact-info của từng microservice để xác minh chúng đang đọc cấu hình từ Config Server.

## Xác Thực cho Repository Riêng Tư

### Xác Thực Username/Password

Thêm vào `application.yml`:

```yaml
spring:
  cloud:
    config:
      server:
        git:
          uri: https://github.com/your-username/private-repo.git
          username: your-username
          password: your-password
```

### Xác Thực SSH

Để tăng cường bảo mật, sử dụng SSH keys thay vì username/password. Cấu hình:
- Host key
- Host key algorithm
- Private key

Tham khảo tài liệu chính thức của Spring Cloud Config để biết chi tiết thiết lập SSH.

## Các Tùy Chọn Backend Thay Thế

Spring Cloud Config Server hỗ trợ nhiều tùy chọn backend khác nhau:

### Các Backend Được Hỗ Trợ
- **Git Backend**: GitHub, GitLab, Bitbucket
- **AWS CodeCommit**: Kho lưu trữ Git được quản lý bởi AWS
- **Google Cloud Source**: Kho lưu trữ Git của Google Cloud
- **File System Backend**: Hệ thống tệp cục bộ (không khuyến nghị cho production)
- **Vault Backend**: Tích hợp HashiCorp Vault
- **CredHub Server**: Cloud Foundry CredHub
- **AWS Secrets Manager**: Quản lý bí mật của AWS
- **AWS Parameter Store**: AWS Systems Manager Parameter Store
- **JDBC Backend**: Lưu trữ cấu hình dựa trên cơ sở dữ liệu

## Thực Hành Tốt Nhất

1. **Luôn sử dụng repository riêng tư trong môi trường production**
2. **Bật `clone-on-start` để phát hiện sớm vấn đề cấu hình**
3. **Đặt giá trị timeout phù hợp cho hành vi fail-fast**
4. **Sử dụng `force-pull` để ngăn chặn vấn đề thay đổi cục bộ**
5. **Ghi chép các thay đổi cấu hình trong Git commit messages**
6. **Sử dụng chiến lược nhánh cho các môi trường khác nhau**

## Khắc Phục Sự Cố

### Config Server không khởi động được
- Xác minh URL kho lưu trữ GitHub là chính xác
- Kiểm tra kết nối mạng đến GitHub
- Xác minh default-label khớp với tên nhánh của bạn

### Microservices không thể đọc cấu hình
- Đảm bảo Config Server được khởi động trước
- Xác minh microservices được cấu hình với URL Config Server chính xác
- Kiểm tra logs của Config Server để tìm lỗi kết nối

## Đọc Thêm

Để biết các cấu hình nâng cao và tính năng bổ sung, tham khảo:
- [Tài Liệu Chính Thức Spring Cloud Config](https://spring.io/projects/spring-cloud-config)
- Tài liệu tham khảo Spring Cloud Config Server
- Hướng dẫn xác thực và cấu hình SSH

## Kết Luận

Sử dụng GitHub làm backend cho Spring Cloud Config Server cung cấp một phương pháp mạnh mẽ, có khả năng mở rộng và dễ bảo trì để quản lý cấu hình microservices. Khả năng quản lý phiên bản và kiểm tra làm cho nó trở thành lựa chọn được khuyến nghị cho môi trường production.

## Những Điểm Chính Cần Nhớ

- GitHub backend là phương pháp được khuyến nghị nhất
- Cấu hình đúng đảm bảo hành vi fail-fast
- Xác thực rất quan trọng cho repository riêng tư
- Tài liệu chính thức là nguồn tài nguyên tốt nhất cho các tình huống nâng cao
- Kiến thức và hiểu biết quan trọng hơn số năm kinh nghiệm