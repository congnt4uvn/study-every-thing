# Triển Khai Spring Boot Profiles trong Microservices

## Giới Thiệu

Hướng dẫn này minh họa cách triển khai thực tế Spring Boot profiles trong accounts microservice. Cách tiếp cận tương tự có thể áp dụng cho các microservices khác như loans và cards.

## Tạo File Cấu Hình Theo Profile

### Bước 1: Tạo File YAML Theo Profile

Tạo hai file YAML bổ sung trong thư mục `resources` cùng với file `application.yml` hiện có:

1. **Profile QA**: `application-qa.yml`
2. **Profile Production**: `application-prod.yml`

Cấu trúc thư mục resources của bạn sẽ như sau:

```
src/main/resources/
├── application.yml (profile mặc định)
├── application-qa.yml (profile QA)
└── application-prod.yml (profile production)
```

## Xác Định Thuộc Tính Theo Môi Trường

### Thuộc Tính KHÔNG Nên Thay Đổi

Một số thuộc tính nên giữ nguyên trong tất cả các môi trường:

- **Cổng Server**: Giữ số cổng nhất quán giữa các môi trường
- **Cấu Hình Database**: Cài đặt cơ sở dữ liệu H2 (trong ví dụ này)
- **Cấu Hình Tĩnh**: Các giá trị không thay đổi theo môi trường

### Thuộc Tính NÊN Thay Đổi

Xác định các thuộc tính cần giá trị khác nhau cho mỗi môi trường:

- **Build Version**: Theo dõi các phiên bản khác nhau trong mỗi môi trường
- **Thông Điệp Ứng Dụng**: Thông điệp cụ thể cho từng môi trường
- **Chi Tiết Liên Hệ**: Thông tin liên hệ hỗ trợ khác nhau cho mỗi môi trường
- **Cài Đặt Riêng**: API endpoints, timeouts, v.v.

## Cấu Hình Profile Mặc Định

### application.yml (Profile Mặc Định)

```yaml
# Profile mặc định cho phát triển cục bộ
build:
  version: "3.0"

accounts:
  message: "Chào mừng đến EasyBank Accounts - APIs Phát Triển Cục Bộ"
  contactDetails:
    name: "John Doe - Lập Trình Viên"
    email: "john.doe@easybank.com"
  onCallSupport:
    - "(555) 123-4567"
    - "(555) 123-4568"
```

## Cấu Hình Profile QA

### application-qa.yml

```yaml
spring:
  config:
    activate:
      on-profile: "qa"

build:
  version: "2.0"

accounts:
  message: "Chào mừng đến EasyBank Accounts - APIs QA"
  contactDetails:
    name: "Jane Smith - Trưởng Nhóm QA"
    email: "jane.smith@easybank.com"
  onCallSupport:
    - "(555) 234-5678"
    - "(555) 234-5679"
```

### Các Phần Tử Cấu Hình Chính

Thuộc tính `spring.config.activate.on-profile` cho Spring Boot biết khi nào kích hoạt file này:

```yaml
spring:
  config:
    activate:
      on-profile: "qa"
```

Điều này có nghĩa là: "Kích hoạt file này khi profile QA được kích hoạt."

## Cấu Hình Profile Production

### application-prod.yml

```yaml
spring:
  config:
    activate:
      on-profile: "prod"

build:
  version: "1.0"

accounts:
  message: "Chào mừng đến EasyBank Accounts - APIs Production"
  contactDetails:
    name: "Sarah Johnson - Chủ Sở Hữu Sản Phẩm"
    email: "sarah.johnson@easybank.com"
  onCallSupport:
    - "(555) 345-6789"
    - "(555) 345-6790"
```

## Import File Profile

### Cập Nhật application.yml

Thêm cấu hình import để cho Spring Boot biết về các file profile của bạn:

```yaml
spring:
  config:
    import:
      - application-qa.yml
      - application-prod.yml
```

Ví dụ hoàn chỉnh:

```yaml
spring:
  config:
    import:
      - application-qa.yml
      - application-prod.yml
  profiles:
    active: qa  # Kích hoạt profile QA

server:
  port: 8080

build:
  version: "3.0"

accounts:
  message: "Chào mừng đến EasyBank Accounts - APIs Phát Triển Cục Bộ"
  contactDetails:
    name: "John Doe - Lập Trình Viên"
    email: "john.doe@easybank.com"
  onCallSupport:
    - "(555) 123-4567"
    - "(555) 123-4568"
```

## Kích Hoạt Profiles

### Phương Pháp 1: Trong application.yml

Thêm thuộc tính `spring.profiles.active`:

```yaml
spring:
  profiles:
    active: qa
```

### Phương Pháp 2: Dòng Lệnh (Được Khuyên Dùng Cho Production)

Kích hoạt profile từ bên ngoài mà không sửa đổi code:

```bash
java -jar accounts-service.jar --spring.profiles.active=prod
```

### Phương Pháp 3: Biến Môi Trường

```bash
export SPRING_PROFILES_ACTIVE=prod
java -jar accounts-service.jar
```

### Phương Pháp 4: Biến Môi Trường Docker

```bash
docker run -e SPRING_PROFILES_ACTIVE=prod accounts-service:latest
```

## Kiểm Tra Kích Hoạt Profile

### Bước 1: Kiểm Tra Profile Mặc Định

1. Không kích hoạt profile nào (hoặc comment dòng `spring.profiles.active`)
2. Build và khởi động lại ứng dụng
3. Kiểm tra các endpoint:

**Endpoint Build Info:**
```json
GET /actuator/build-info
Response: { "version": "3.0" }
```

**Endpoint Contact Info:**
```json
GET /contact-info
Response: {
  "message": "Chào mừng đến EasyBank Accounts - APIs Phát Triển Cục Bộ",
  "contactDetails": {
    "name": "John Doe - Lập Trình Viên",
    "email": "john.doe@easybank.com"
  },
  "onCallSupport": ["(555) 123-4567", "(555) 123-4568"]
}
```

### Bước 2: Kiểm Tra Profile QA

1. Đặt `spring.profiles.active: qa` trong `application.yml`
2. Build và khởi động lại ứng dụng
3. Kiểm tra các endpoint:

**Endpoint Build Info:**
```json
GET /actuator/build-info
Response: { "version": "2.0" }
```

**Endpoint Contact Info:**
```json
GET /contact-info
Response: {
  "message": "Chào mừng đến EasyBank Accounts - APIs QA",
  "contactDetails": {
    "name": "Jane Smith - Trưởng Nhóm QA",
    "email": "jane.smith@easybank.com"
  },
  "onCallSupport": ["(555) 234-5678", "(555) 234-5679"]
}
```

### Bước 3: Kiểm Tra Profile Production

1. Đặt `spring.profiles.active: prod` trong `application.yml`
2. Build và khởi động lại ứng dụng
3. Xác minh các giá trị cụ thể cho production được trả về

## Cách Hoạt Động Của Profile Override

Khi một profile được kích hoạt, Spring Boot tuân theo thứ tự ưu tiên này:

1. **Thuộc Tính Profile Đang Hoạt Động** (ví dụ: `application-qa.yml`) - **Ưu Tiên Cao Nhất**
2. **Thuộc Tính Profile Mặc Định** (ví dụ: `application.yml`) - **Ưu Tiên Thấp Hơn**

Nếu cùng một key thuộc tính tồn tại trong cả hai file:
- Giá trị từ profile đang hoạt động **ghi đè** giá trị mặc định
- Các thuộc tính chỉ có trong profile mặc định vẫn khả dụng
- Các thuộc tính chỉ có trong profile đang hoạt động được thêm vào

### Ví Dụ:

**application.yml:**
```yaml
build:
  version: "3.0"
server:
  port: 8080
```

**application-qa.yml:**
```yaml
build:
  version: "2.0"
```

**Kết quả khi profile QA được kích hoạt:**
```yaml
build:
  version: "2.0"  # Bị ghi đè bởi profile QA
server:
  port: 8080      # Kế thừa từ profile mặc định
```

## Thực Hành Tốt Nhất Cho Quản Lý Profile

### 1. Giữ Code Không Thay Đổi (Immutable)

**Vấn Đề**: Thay đổi `spring.profiles.active` trong `application.yml` yêu cầu rebuild Docker image cho mỗi môi trường.

**Giải Pháp**: Sử dụng các phương pháp cấu hình bên ngoài (dòng lệnh, biến môi trường) để kích hoạt profile.

### 2. Quy Ước Đặt Tên

- Sử dụng chữ thường cho tên profile: `qa`, `prod`, `dev`
- Nhất quán giữa tất cả các microservices
- Khớp tên profile trong tên file và thuộc tính kích hoạt

### 3. Tổ Chức Thuộc Tính

```yaml
# Nhóm các thuộc tính liên quan
build:
  version: "1.0"

accounts:
  message: "..."
  contactDetails:
    name: "..."
    email: "..."
  onCallSupport:
    - "..."
```

### 4. Không Nhân Bản Thuộc Tính Tĩnh

Chỉ bao gồm các thuộc tính thay đổi giữa các môi trường trong các file theo profile cụ thể.

### 5. Chiến Lược Version

Xem xét chiến lược version có ý nghĩa cho deployment của bạn:
- **Dev**: Version cao nhất (tính năng mới nhất)
- **QA**: Version trung gian (đang kiểm thử)
- **Prod**: Version ổn định (đã phát hành)

## Tùy Chọn Cấu Hình Bên Ngoài

Để triển khai thực sự không thay đổi, sử dụng cấu hình bên ngoài:

### 1. Tham Số Dòng Lệnh
```bash
java -jar app.jar --spring.profiles.active=prod --accounts.message="Thông điệp tùy chỉnh"
```

### 2. Biến Môi Trường
```bash
SPRING_PROFILES_ACTIVE=prod
ACCOUNTS_MESSAGE="Thông điệp tùy chỉnh"
```

### 3. ConfigMaps (Kubernetes)
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: accounts-config
data:
  spring.profiles.active: "prod"
```

### 4. Spring Cloud Config Server
Quản lý cấu hình tập trung cho tất cả các microservices.

## Bài Tập

Áp dụng cùng cách triển khai profile cho:
- **Loans Microservice**
- **Cards Microservice**

Tạo các profile sau cho mỗi dịch vụ:
- `application-qa.yml`
- `application-prod.yml`

Đảm bảo mỗi dịch vụ có các thông tin riêng cho từng môi trường:
- Build versions
- Thông điệp chào mừng
- Chi tiết liên hệ
- Thông tin hỗ trợ

## Tóm Tắt

Triển khai này minh họa:
- ✅ Tạo nhiều file profile
- ✅ Cấu hình thuộc tính theo profile cụ thể
- ✅ Kích hoạt profile theo nhiều cách khác nhau
- ✅ Kiểm tra hành vi của profile
- ✅ Hiểu cơ chế ghi đè thuộc tính
- ✅ Thực hành tốt nhất cho triển khai production

## Các Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ khám phá:
- **Phương pháp cấu hình thuộc tính bên ngoài**
- **Kích hoạt profile động**
- **Tránh thay đổi code khi chuyển môi trường**
- **Chiến lược profile cho Docker và Kubernetes**

---

**Ghi Nhớ**: Xây dựng một lần, triển khai mọi nơi bằng cách sử dụng kích hoạt profile từ bên ngoài!