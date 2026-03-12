# Làm Mới Cấu Hình Microservices Không Cần Khởi Động Lại

## Tổng Quan

Hướng dẫn này trình bày cách làm mới các thuộc tính cấu hình động trong microservices Spring Boot mà không cần khởi động lại các instance, sử dụng Spring Boot Actuator và Spring Cloud Config Server.

## Vấn Đề

Trong kiến trúc microservices với Spring Cloud Config Server, các thuộc tính được tải trong quá trình khởi động ứng dụng. Tuy nhiên, khi bạn cần thay đổi cấu hình tại runtime:

- **Thách Thức Khởi Động Lại Thủ Công**: Với hàng trăm microservices và nhiều instance cho mỗi service (ví dụ: 100 microservices × 5 instances = 500 instances), việc khởi động lại tất cả các instance thủ công rất khó khăn
- **Ảnh Hưởng Downtime**: Việc khởi động lại ảnh hưởng đến traffic production
- **Use Case Phổ Biến**: Feature flags cần được bật/tắt động để kiểm soát hành vi business logic

## Giải Pháp: Spring Boot Actuator Refresh Endpoint

### Điều Kiện Tiên Quyết

1. **Spring Boot Actuator Dependency** - Đã được thêm vào microservices:
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

### Bước 1: Sửa Đổi Các Lớp DTO

**Vấn Đề với Record Classes**: Các record class trong Java có các trường final không thể sửa đổi sau khi đối tượng được tạo.

**Giải Pháp**: Chuyển đổi record classes thành các class thông thường với getters/setters.

#### Trước (Record Class):
```java
public record AccountsContactInfoDto(
    String message,
    Map<String, String> contactDetails,
    List<String> onCallSupport
) {}
```

#### Sau (Regular Class):
```java
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class AccountsContactInfoDto {
    private String message;
    private Map<String, String> contactDetails;
    private List<String> onCallSupport;
}
```

Áp dụng các thay đổi tương tự cho:
- `LoansContactInfoDto`
- `CardsContactInfoDto`

### Bước 2: Kích Hoạt Actuator Endpoints

Thêm cấu hình vào `application.yml` trong tất cả microservices (accounts, loans, cards):

```yaml
management:
  endpoints:
    web:
      exposure:
        include: "*"
```

**Lưu ý**: Sử dụng `"*"` để expose tất cả management endpoints. Đối với production, nên chỉ expose `refresh`:
```yaml
management:
  endpoints:
    web:
      exposure:
        include: refresh
```

### Bước 3: Kiểm Tra Configuration Refresh

#### 1. Khởi Động Tất Cả Các Ứng Dụng
- Khởi động Config Server
- Khởi động Accounts Microservice
- Khởi động Cards Microservice
- Khởi động Loans Microservice

#### 2. Xác Minh Cấu Hình Ban Đầu
Kiểm tra contact-info endpoint cho mỗi microservice:
- `GET http://localhost:8080/contact-info` (Accounts)
- `GET http://localhost:8090/contact-info` (Cards)
- `GET http://localhost:8100/contact-info` (Loans)

Thông báo ban đầu: `"Hello, welcome to EazyBank accounts related prod APIs"`

#### 3. Cập Nhật Cấu Hình trong GitHub Repository

Sửa đổi các file thuộc tính trong config repository:
- `accounts-prod.yml`
- `cards-prod.yml`
- `loans-prod.yml`

Thay đổi: `prod APIs` → `production APIs`

#### 4. Xác Minh Config Server Có Giá Trị Mới Nhất
```
GET http://localhost:8888/accounts/prod
GET http://localhost:8888/cards/prod
GET http://localhost:8888/loans/prod
```

Config Server luôn lấy từ GitHub (không có cache cục bộ), nên nó hiển thị giá trị đã cập nhật ngay lập tức.

#### 5. Microservices Vẫn Hiển Thị Giá Trị Cũ
Nếu không refresh, microservices vẫn giữ giá trị cấu hình từ lúc khởi động.

#### 6. Gọi Actuator Refresh Endpoint

**Quan Trọng**: Sử dụng phương thức HTTP POST (không phải GET)

```
POST http://localhost:8080/actuator/refresh
```

**Response**:
```json
[
    "accounts.message",
    "config.client.version"
]
```

Response cho biết các thuộc tính nào đã được làm mới.

#### 7. Xác Minh Cấu Hình Đã Cập Nhật
```
GET http://localhost:8080/contact-info
```

Thông báo bây giờ hiển thị: `"Hello, welcome to EazyBank accounts related production APIs"`

**Thành Công!** Cấu hình đã được cập nhật mà không cần khởi động lại.

#### 8. Lặp Lại Cho Các Microservices Khác
```
POST http://localhost:8090/actuator/refresh  (Cards)
POST http://localhost:8100/actuator/refresh  (Loans)
```

## Quy Trình Configuration Refresh

```
┌─────────────────────────────────────────────────────────────┐
│ Bước 1: Push cấu hình mới vào Config Repository (GitHub)   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Bước 2: Gọi POST /actuator/refresh trên microservice       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Bước 3: Microservice yêu cầu các thuộc tính đã cập nhật    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Bước 4: Config Server pull phiên bản mới nhất từ GitHub    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Bước 5-6: Config Server trả về các thuộc tính đã thay đổi  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Bước 7: Microservice reload cấu hình (không restart!)      │
└─────────────────────────────────────────────────────────────┘
```

## Tóm Tắt Các Bước

1. ✅ Thêm Spring Boot Actuator dependency vào `pom.xml`
2. ✅ Kích hoạt refresh endpoint trong `application.yml`:
   ```yaml
   management.endpoints.web.exposure.include: refresh
   ```
3. ✅ Chuyển đổi các DTO record classes thành regular classes với `@Getter` và `@Setter`
4. ✅ Cập nhật cấu hình trong Config Repository
5. ✅ Gọi `POST /actuator/refresh` trên mỗi microservice instance

## Thách Thức Còn Lại

**Vấn Đề Khả Năng Mở Rộng**: Với 500+ microservice instances, việc gọi refresh endpoint thủ công trên mỗi instance là không thực tế.

### Các Giải Pháp Tạm Thời Hiện Tại
- **CI/CD Scripts**: Tự động hóa việc gọi refresh endpoint qua pipelines
- **Jenkins Jobs**: Lên lịch các jobs để gọi refresh trên tất cả instances

### Cần Giải Pháp Tốt Hơn
Các giải pháp tạm thời này có thể không thuận tiện cho tất cả các dự án. Cần một giải pháp tốt hơn để broadcast các thay đổi cấu hình đến tất cả các microservice instances cùng lúc.

**Chủ Đề Tiếp Theo**: Khám phá các giải pháp thay thế tốt hơn cho việc làm mới cấu hình động ở quy mô lớn (sẽ được đề cập trong các bài giảng tiếp theo).

## Những Điểm Chính

- ✅ Spring Boot Actuator cung cấp `/actuator/refresh` endpoint để cập nhật cấu hình runtime
- ✅ Không cần khởi động lại ứng dụng
- ✅ Config Server luôn lấy phiên bản mới nhất từ repository
- ✅ Microservices cần trigger refresh rõ ràng
- ⚠️ Gọi thủ công không mở rộng tốt cho các triển khai lớn
- 🔍 Cần các giải pháp broadcasting tốt hơn cho môi trường production

## Công Nghệ Sử Dụng

- Spring Boot
- Spring Cloud Config Server
- Spring Boot Actuator
- Lombok
- GitHub (Config Repository)

## Các Microservices Liên Quan

- **Accounts Microservice** (Port 8080)
- **Cards Microservice** (Port 8090)
- **Loans Microservice** (Port 8100)
- **Config Server** (Port 8888)