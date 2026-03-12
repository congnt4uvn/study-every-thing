# Lưu Trữ Cấu Hình Spring Cloud Config Server Trong File System

## Tổng Quan

Hướng dẫn này giải thích cách chuyển các file cấu hình từ classpath sang vị trí file system trong Spring Cloud Config Server. Phương pháp này cung cấp bảo mật và kiểm soát truy cập tốt hơn cho môi trường production.

## Tại Sao Sử Dụng Phương Pháp File System?

### Ưu Điểm

1. **Bảo Mật Tăng Cường**: Các file cấu hình được lưu trữ tại vị trí server nơi microservice được triển khai
2. **Kiểm Soát Truy Cập**: Quản trị viên server có thể thực thi các hạn chế bảo mật trên thư mục
3. **Truy Cập Hạn Chế**: Chỉ ứng dụng Config Server mới có thể truy cập các file cấu hình
4. **Sẵn Sàng Production**: Ngăn chặn truy cập trái phép vào dữ liệu cấu hình nhạy cảm

### Trường Hợp Sử Dụng

- Môi trường production yêu cầu bảo mật nghiêm ngặt
- Tổ chức có đội ngũ quản trị server chuyên dụng
- Dự án xử lý dữ liệu cấu hình nhạy cảm
- Yêu cầu tuân thủ cho quản lý cấu hình

## Yêu Cầu Trước

- Spring Cloud Config Server đã được thiết lập
- Các file cấu hình hiện tại trong classpath (thư mục resources/config)
- Vị trí file system đã được chuẩn bị để lưu trữ cấu hình

## Bước 1: Sao Chép Các File Cấu Hình Vào File System

### Xác Định Các File Cấu Hình

Từ project Config Server của bạn, xác định tất cả các file cấu hình trong:
```
src/main/resources/config/
├── accounts.yml
├── accounts-prod.yml
├── accounts-qa.yml
├── loans.yml
├── loans-prod.yml
├── loans-qa.yml
├── cards.yml
├── cards-prod.yml
└── cards-qa.yml
```

### Tạo Thư Mục File System

Chọn một vị trí trên server/hệ thống local của bạn để lưu trữ cấu hình.

**Ví Dụ Vị Trí**:

**macOS/Linux**:
```
/Users/eazybytes/documents/config
```

**Windows**:
```
C:\config
```
hoặc
```
D:\config
```

### Sao Chép Files

Sao chép tất cả các file cấu hình từ classpath đến vị trí file system bạn đã chọn.

**Xác Minh**: Điều hướng đến thư mục và đảm bảo tất cả các file có mặt:
```
users/
└── eazybytes/
    └── documents/
        └── config/
            ├── accounts.yml
            ├── accounts-prod.yml
            ├── accounts-qa.yml
            ├── loans.yml
            ├── loans-prod.yml
            ├── loans-qa.yml
            ├── cards.yml
            ├── cards-prod.yml
            └── cards-qa.yml
```

## Bước 2: Cập Nhật Cấu Hình Config Server

### Chỉnh Sửa application.yml

Mở `application.yml` trong project Config Server của bạn và cập nhật vị trí tìm kiếm.

#### Cấu Hình Hiện Tại (Classpath)

```yaml
spring:
  profiles:
    active: native
  cloud:
    config:
      server:
        native:
          search-locations: classpath:/config
```

#### Cấu Hình Mới (File System)

**Cho macOS/Linux**:
```yaml
spring:
  profiles:
    active: native  # Phải giữ 'native' cho phương pháp file system
  cloud:
    config:
      server:
        native:
          # search-locations: classpath:/config  # Comment vị trí cũ
          search-locations: file:///Users/eazybytes/documents/config
```

**Cho Windows (ổ C:)**:
```yaml
spring:
  profiles:
    active: native
  cloud:
    config:
      server:
        native:
          search-locations: file:///C:/config
```

**Cho Windows (ổ D:)**:
```yaml
spring:
  profiles:
    active: native
  cloud:
    config:
      server:
        native:
          search-locations: file:///D:/config
```

### Quy Tắc Cú Pháp Quan Trọng

1. **Tiền tố**: Sử dụng `file:` thay vì `classpath:`
2. **Dấu gạch chéo sau file:**: Sử dụng **ba dấu gạch chéo** (`///`) sau `file:`
3. **Dấu phân cách đường dẫn**: Sử dụng **hai dấu gạch chéo** (`//`) giữa các tên thư mục
4. **Profile**: Phải giữ `active: native` (không thay đổi điều này)
5. **Dấu gạch chéo**: Luôn sử dụng dấu gạch chéo (`/`), ngay cả trên Windows

### Ví Dụ Phân Tích Đường Dẫn

**Đường Dẫn macOS/Linux**:
```
file:///Users/eazybytes/documents/config
│    │   │                          │
│    │   └─ cấu trúc thư mục        └─ thư mục cấu hình
│    └─────── ba dấu gạch chéo
└────────────── tiền tố file
```

**Đường Dẫn Windows**:
```
file:///C:/config
│    │   │  │
│    │   │  └─ thư mục cấu hình
│    │   └──── ký tự ổ đĩa
│    └──────── ba dấu gạch chéo
└───────────── tiền tố file
```

## Bước 3: Rebuild và Khởi Động Lại Services

### Build Config Server

```bash
# Điều hướng đến thư mục config server
cd configserver

# Build project
mvn clean install
```

### Khởi Động Lại Theo Đúng Thứ Tự

**Quan Trọng**: Luôn khởi động Config Server trước khi khởi động các microservices khác.

1. **Dừng tất cả các services đang chạy**:
   - Microservice Accounts
   - Microservice Loans
   - Microservice Cards
   - Config Server

2. **Khởi động Config Server**:
   ```bash
   # Khởi động Config Server trên cổng 8071
   java -jar configserver.jar
   ```
   Đợi khởi động thành công.

3. **Khởi động microservices**:
   ```bash
   # Khởi động Accounts (cổng 8080)
   java -jar accounts.jar
   
   # Khởi động Loans (cổng 8090)
   java -jar loans.jar
   
   # Khởi động Cards (cổng 9000)
   java -jar cards.jar
   ```

## Bước 4: Xác Minh Việc Tải Cấu Hình

### Kiểm Tra Endpoints Config Server

Sử dụng trình duyệt hoặc Postman để xác minh Config Server có thể đọc từ file system.

#### Kiểm Tra Loans Prod Profile

```
GET http://localhost:8071/loans/prod
```

**Kết Quả Mong Đợi**:
```json
{
  "name": "loans",
  "profiles": ["prod"],
  "label": null,
  "version": null,
  "state": null,
  "propertySources": [
    {
      "name": "file:///Users/eazybytes/documents/config/loans-prod.yml",
      "source": {
        "build": {
          "version": "1.0"
        },
        "accounts": {
          "message": "Properties from prod profile",
          "contactDetails": {
            "name": "Product Owner",
            "email": "call support"
          }
        }
      }
    }
  ]
}
```

**Xác Minh Chính**: Xem thuộc tính `name` dưới `propertySources`. Nó phải hiển thị **đường dẫn file system**, không phải `classpath`.

#### Kiểm Tra Cards Profile

```
GET http://localhost:8071/cards/prod
```

**Mong Đợi**: Phản hồi phải hiển thị đường dẫn `file:///...` cho biết vị trí file system.

#### Kiểm Tra Accounts Profile

```
GET http://localhost:8071/accounts/prod
```

**Mong Đợi**: Xác nhận đường dẫn file system tương tự.

### Kiểm Tra Tích Hợp Microservice

Xác minh rằng các microservices tải thành công cấu hình từ Config Server.

#### Kiểm Tra Cards Contact Info

```
GET http://localhost:9000/api/contact-info
```

**Kết Quả Mong Đợi** (thuộc tính profile prod):
```json
{
  "message": "Properties from prod profile",
  "contactDetails": {
    "name": "Product Owner",
    "email": "call support"
  }
}
```

Điều này xác nhận:
- ✅ Config Server đọc từ file system
- ✅ Microservice Cards kết nối với Config Server
- ✅ Profile prod được kích hoạt theo mặc định
- ✅ Thuộc tính được tải đúng

#### Kiểm Tra Ngẫu Nhiên

Bạn có thể kiểm tra ngẫu nhiên các microservices khác:

```
GET http://localhost:8080/api/contact-info  # Accounts
GET http://localhost:8090/api/contact-info  # Loans
```

Tất cả phải trả về thuộc tính profile prod.

## Tóm Tắt Cấu Hình

### Những Gì Đã Thay Đổi

| Khía Cạnh | Trước (Classpath) | Sau (File System) |
|--------|-------------------|---------------------|
| Vị trí | `src/main/resources/config/` | `/Users/eazybytes/documents/config/` |
| Truy cập | Bất kỳ ai có quyền truy cập code | Bị hạn chế bởi admin server |
| Cú pháp | `classpath:/config` | `file:///Users/eazybytes/documents/config` |
| Profile | `native` | `native` (không thay đổi) |
| Bảo mật | Thấp | Cao |

### Những Gì Không Thay Đổi

- ✅ Profile phải vẫn là `native`
- ✅ Tên file cấu hình không thay đổi
- ✅ Cấu hình microservice không thay đổi
- ✅ REST API endpoints không thay đổi
- ✅ Cơ chế kích hoạt profile không thay đổi

## Ví Dụ Đường Dẫn Theo Hệ Điều Hành

### macOS

```yaml
search-locations: file:///Users/username/documents/config
search-locations: file:///opt/config
search-locations: file:///var/config
```

### Linux

```yaml
search-locations: file:///home/username/config
search-locations: file:///opt/config
search-locations: file:///etc/config
```

### Windows

```yaml
search-locations: file:///C:/config
search-locations: file:///D:/project/config
search-locations: file:///C:/Users/username/documents/config
```

## Thực Hành Bảo Mật Tốt Nhất

### Quyền Thư Mục

**Linux/macOS**:
```bash
# Đặt quyền hạn chế
chmod 700 /Users/eazybytes/documents/config

# Chỉ user config server có thể đọc
chown configserver:configserver /Users/eazybytes/documents/config
```

**Windows**:
- Nhấp chuột phải vào thư mục → Properties → Security
- Xóa tất cả users trừ tài khoản service Config Server
- Cấp quyền chỉ đọc cho Config Server

### Quyền File

```bash
# Đặt các file cấu hình ở chế độ chỉ đọc
chmod 400 /Users/eazybytes/documents/config/*.yml
```

### Mã Hóa

Đối với các thuộc tính nhạy cảm, xem xét:
- Mã hóa Spring Cloud Config
- Quản lý secret bên ngoài (Vault, AWS Secrets Manager)
- Biến môi trường cho credentials

## Khắc Phục Sự Cố

### Config Server Không Tìm Thấy Files

**Triệu Chứng**: Config Server khởi động nhưng trả về cấu hình rỗng

**Giải Pháp**:
1. Xác minh đường dẫn file là chính xác (kiểm tra ký tự ổ đĩa, tên thư mục)
2. Đảm bảo ba dấu gạch chéo sau `file:`
3. Kiểm tra quyền thư mục
4. Xác minh files tồn tại tại vị trí đã chỉ định
5. Sử dụng đường dẫn tuyệt đối, không phải đường dẫn tương đối

### Định Dạng Đường Dẫn Sai

**Lỗi Phổ Biến**:

❌ `file:/Users/...` (chỉ một dấu gạch chéo)  
✅ `file:///Users/...` (ba dấu gạch chéo)

❌ `file:///C:\config` (dấu gạch chéo ngược trên Windows)  
✅ `file:///C:/config` (dấu gạch chéo xuôi)

❌ `file:///Users\eazybytes\...` (dấu gạch chéo hỗn hợp)  
✅ `file:///Users/eazybytes/...` (tất cả dấu gạch chéo xuôi)

### Microservices Không Thể Kết Nối

**Triệu Chứng**: Microservices không khởi động được hoặc không thể tải thuộc tính

**Giải Pháp**:
1. Đảm bảo Config Server khởi động thành công trước
2. Xác minh Config Server có thể truy cập tại `http://localhost:8071`
3. Kiểm tra logs microservice cho lỗi kết nối
4. Kiểm tra endpoints Config Server trực tiếp trong trình duyệt

### Lỗi Permission Denied

**Triệu Chứng**: Logs Config Server hiển thị "Access Denied" hoặc "Permission Denied"

**Giải Pháp**:
1. Kiểm tra quyền thư mục (cần quyền đọc)
2. Xác minh user process Config Server có quyền truy cập
3. Trên Windows, kiểm tra file không bị khóa bởi process khác

## Lợi Ích Đạt Được

Bằng cách chuyển sang phương pháp file system:

- ✅ **Bảo Mật Tốt Hơn**: Cấu hình được tách riêng khỏi code ứng dụng
- ✅ **Kiểm Soát Truy Cập**: Admin server có thể hạn chế truy cập thư mục
- ✅ **Linh Hoạt Triển Khai**: Cấu hình tách riêng khỏi artifacts triển khai
- ✅ **Quản Lý Phiên Bản**: Vẫn có thể sử dụng Git cho việc versioning cấu hình
- ✅ **Sẵn Sàng Production**: Đáp ứng yêu cầu bảo mật doanh nghiệp
- ✅ **Cập Nhật Dễ Dàng**: Cập nhật cấu hình mà không cần redeploy Config Server

## Bước Tiếp Theo

Xem xét các cải tiến sau:

1. **Git Backend**: Lưu trữ cấu hình trong repository Git thay vì file system
2. **Mã Hóa**: Mã hóa các thuộc tính nhạy cảm bằng mã hóa Spring Cloud Config
3. **Nhiều Vị Trí**: Cấu hình nhiều vị trí tìm kiếm cho tính dự phòng
4. **Refresh Scope**: Triển khai làm mới thuộc tính động mà không cần khởi động lại
5. **Giám Sát**: Thêm giám sát cho các thay đổi cấu hình

## Tóm Tắt

Bạn đã thành công:

- ✅ Sao chép các file cấu hình từ classpath sang file system
- ✅ Cập nhật Config Server để sử dụng vị trí file system
- ✅ Thay đổi `search-locations` từ `classpath:` sang `file:`
- ✅ Duy trì yêu cầu profile `native`
- ✅ Xác minh Config Server tải từ file system
- ✅ Kiểm tra tích hợp microservice
- ✅ Tăng cường bảo mật với phương pháp file system

**Điểm Chính**: Thay đổi duy nhất cần thiết là cập nhật thuộc tính `search-locations` trong Config Server. Tất cả microservices tiếp tục hoạt động mà không cần bất kỳ sửa đổi nào, đồng thời đạt được bảo mật cải thiện thông qua lưu trữ file system.