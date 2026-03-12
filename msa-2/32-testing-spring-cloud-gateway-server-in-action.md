# Kiểm Thử Spring Cloud Gateway Server Trong Thực Tế

## Tổng Quan
Hướng dẫn này trình bày cách kiểm thử và xác thực Spring Cloud Gateway Server trong kiến trúc microservices sử dụng Spring Boot, Eureka Service Discovery và Spring Cloud Gateway.

## Yêu Cầu Tiên Quyết

Trước khi khởi động Gateway Server, đảm bảo các dịch vụ sau đang chạy theo đúng thứ tự:

1. **Config Server** - Phải khởi động trước tiên
2. **Eureka Server** - Khởi động sau Config Server
3. **Microservices** (Accounts, Cards, Loans) - Khởi động theo thứ tự bất kỳ sau Eureka Server
4. **Gateway Server** - Phải khởi động cuối cùng (Cổng: 8072)

### Tại Sao Phải Khởi Động Gateway Server Cuối Cùng?

Gateway Server cần:
- Kết nối với Eureka Server
- Lấy thông tin chi tiết về tất cả microservices đã đăng ký
- Xử lý định tuyến traffic cho các microservices nội bộ

Nếu khởi động trước các microservices khác, Eureka Server sẽ không có thông tin về các microservices để chia sẻ với Gateway.

## Xác Minh Cài Đặt

### 1. Kiểm Tra Eureka Dashboard

Truy cập Eureka Dashboard để xác minh tất cả dịch vụ đã được đăng ký:
- Microservice Accounts
- Microservice Cards
- Microservice Loans
- Gateway Server

Nhấp vào bất kỳ liên kết dịch vụ nào để xem thông tin được cấu hình trong file `application.yml`.

### 2. Kiểm Tra Gateway Actuator Endpoints

Truy cập Gateway Server actuator tại:
```
http://localhost:8072/actuator
```

**Mẹo:** Cài đặt plugin Chrome "JSON View" để hiển thị JSON được định dạng tốt hơn.

#### Xem Gateway Routes

Truy cập endpoint routes:
```
http://localhost:8072/actuator/gateway/routes
```

Endpoint này hiển thị thông tin định tuyến cho từng microservice.

## Hiểu Cấu Hình Định Tuyến Gateway

### Cấu Trúc Route

Mỗi route microservice chứa:

1. **Predicate**: Khớp các request đến dựa trên đường dẫn
2. **URI**: Đích đến với tiền tố load balancer (`lb://`)
3. **Filters**: Quy tắc viết lại và chuyển đổi đường dẫn

### Ví Dụ: Route Microservice Loans

Khi một request được gửi đến Gateway Server với đường dẫn `/loans`:

- **Port**: Chuyển tiếp đến cổng 8090 (cổng của loans microservice)
- **Load Balancer**: Sử dụng định dạng `lb://LOANS`
  - `lb` = load balancer (cân bằng tải)
  - `LOANS` = tên ứng dụng trong Eureka Server
- **Service Discovery**: Tận dụng Eureka để tìm các instances
- **Load Balancing**: Sử dụng chiến lược Spring Cloud Load Balancer

### Path Rewriting Filter

Filter **RewritePath**:
- Loại bỏ tiền tố (ví dụ: `/loans`) khỏi đường dẫn đến
- Chỉ chuyển tiếp phần đường dẫn còn lại đến microservice đích
- Ví dụ: `/loans/api/create` trở thành `/api/create` khi được chuyển tiếp

Cấu hình này áp dụng tương tự cho microservices **Accounts** và **Cards**.

### Gateway Server Self-Routing

Gateway Server cũng có thể định tuyến request đến chính nó:
- Yêu cầu tiền tố đường dẫn `gatewayserver`
- Sử dụng cổng 8072
- Đăng ký trong Eureka với tên "Gateway Server"

## Kiểm Thử Với Postman

### Test 1: Tạo Tài Khoản Qua Gateway

**Cấu Hình Request:**
```
POST http://localhost:8072/ACCOUNTS/api/create
```

**Các Điểm Chính:**
- Cổng `8072`: Cổng của Gateway Server
- `ACCOUNTS`: Tên logic đăng ký trong Eureka (sử dụng CHỮ HOA)
- `/api/create`: Đường dẫn endpoint thực tế trong accounts microservice

**Request Body:**
```json
{
  "name": "Nguyễn Văn A",
  "email": "nguyenvana@example.com",
  "mobileNumber": "0123456789"
}
```

**Luồng Xử Lý:**
1. Request được gửi đến Gateway Server
2. Gateway khớp cấu hình định tuyến cho đường dẫn `/ACCOUNTS`
3. Loại bỏ tiền tố `/ACCOUNTS`
4. Chuyển tiếp đường dẫn còn lại (`/api/create`) đến accounts microservice
5. Sử dụng Eureka cho service discovery với load balancer

**Kết Quả:** Phản hồi tạo tài khoản thành công

### Test 2: Lấy Thông Tin Tài Khoản

**Cấu Hình Request:**
```
GET http://localhost:8072/ACCOUNTS/api/fetch?mobileNumber=0123456789
```

**Các Điểm Chính:**
- Logic định tuyến giống như Test 1
- Tham số query được truyền qua accounts microservice
- Số điện thoại phải khớp với tài khoản đã đăng ký

**Kết Quả:** Chi tiết tài khoản được trả về thành công

### Test 3: Truy Cập Loans Microservice

**Cấu Hình Request:**
```
GET http://localhost:8072/LOANS/api/fetch?mobileNumber=0123456789
```

Các client bên ngoài gửi request với tiền tố đường dẫn `/loans` để truy cập loans microservice thông qua Gateway.

**Lưu Ý:** Nếu không tồn tại khoản vay nào cho số điện thoại, bạn sẽ nhận được lỗi "not found".

## Lợi Ích Của Việc Sử Dụng Gateway Server

### Mô Hình Edge Server

- Tất cả traffic bên ngoài đi qua Gateway Server
- Các microservices nội bộ không được expose trực tiếp cho client bên ngoài
- Gateway hoạt động như một điểm vào duy nhất (edge server)

### Các Cân Nhắc Về Bảo Mật

**Cài Đặt Hiện Tại:**
- Client vẫn có thể gọi trực tiếp microservices nếu biết URLs
- Truy cập trực tiếp về mặt kỹ thuật vẫn khả thi với cấu hình hiện tại

**Cải Tiến Tương Lai:**
- Các chính sách bảo mật sẽ được áp dụng trong các phần tiếp theo
- Client sẽ được yêu cầu chỉ truy cập microservices thông qua Gateway
- Việc gọi trực tiếp microservice sẽ bị chặn

## Tóm Tắt

Với cài đặt Spring Cloud Gateway Server này, bạn đã thành công:

✅ Cấu hình một edge server cho mạng microservices của bạn  
✅ Triển khai service discovery với Eureka  
✅ Thiết lập cân bằng tải tự động với Spring Cloud Load Balancer  
✅ Cấu hình các quy tắc viết lại đường dẫn và định tuyến  
✅ Tạo một điểm vào duy nhất cho các request từ client bên ngoài  

Gateway Server có thể được tối ưu hóa và bảo mật thêm trong các triển khai tiếp theo.

## Các Bước Tiếp Theo

- Triển khai bảo mật và xác thực
- Thêm rate limiting và circuit breakers
- Cấu hình custom filters cho logging và monitoring
- Tối ưu hóa hiệu suất Gateway Server

---

**Lưu Ý:** Đảm bảo tất cả tên dịch vụ trong Eureka đều ở dạng CHỮ HOA theo mặc định để cấu hình định tuyến hoạt động đúng.