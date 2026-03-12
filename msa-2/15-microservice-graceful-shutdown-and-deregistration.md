# Tắt Microservice Một Cách Linh Hoạt và Hủy Đăng Ký Khỏi Eureka Server

## Tổng Quan

Hướng dẫn này trình bày cách các microservice tự động hủy đăng ký khỏi Eureka Server trong quá trình tắt máy một cách linh hoạt, đảm bảo quản lý service registry đúng cách trong kiến trúc microservices Spring Boot.

## Yêu Cầu Trước

- Eureka Server đang chạy và được cấu hình
- Các microservice (Accounts, Loans, Cards) đã đăng ký với Eureka Server
- Spring Boot Actuator được cấu hình với shutdown endpoint
- Postman hoặc công cụ kiểm thử API tương tự

## Graceful Shutdown vs Forced Shutdown

### Forced Shutdown (Không Được Khuyến Nghị)
- Sử dụng nút stop của IDE (ví dụ: IntelliJ IDEA)
- Tắt ứng dụng ngay lập tức
- Không có quá trình hủy đăng ký
- **KHÔNG nên sử dụng trong các môi trường cao hơn (dev, qa, prod)**

### Graceful Shutdown (Được Khuyến Nghị)
- Sử dụng các script shutdown
- Sử dụng shutdown endpoint của Actuator
- Cho phép dọn dẹp và hủy đăng ký đúng cách
- **Thực hành chuẩn cho môi trường production**

## Cấu Hình

### Thiết Lập Actuator Shutdown Endpoint

Thêm các thuộc tính sau vào cấu hình microservices của bạn:

```yaml
management:
  endpoints:
    web:
      exposure:
        include: shutdown
  endpoint:
    shutdown:
      enabled: true
```

Các thuộc tính này kích hoạt shutdown endpoint trong Spring Boot Actuator cho mỗi microservice (Accounts, Loans, Cards).

## Chi Tiết Shutdown Endpoint

### Thông Tin Endpoint
- **URL Pattern**: `http://localhost:{port}/actuator/shutdown`
- **HTTP Method**: POST (không cho phép phương thức GET)
- **Response**: Thông báo JSON xác nhận bắt đầu shutdown

### Các URL Ví Dụ
- Accounts Service: `http://localhost:8080/actuator/shutdown`
- Cards Service: `http://localhost:9000/actuator/shutdown`
- Loans Service: `http://localhost:8090/actuator/shutdown` (điều chỉnh port theo cấu hình)

## Quy Trình Hủy Đăng Ký

### Các Bước Shutdown Chi Tiết

1. **Khởi Động Shutdown**: Gửi POST request tới `/actuator/shutdown`
2. **Grace Period**: Ứng dụng dành thời gian để thực hiện các tác vụ dọn dẹp
3. **Hủy Đăng Ký**: Microservice tự hủy đăng ký khỏi Eureka Server
4. **Xác Nhận**: Eureka Server trả về HTTP status 200
5. **Hoàn Thành Shutdown**: Ứng dụng dừng một cách linh hoạt

### Response Mong Đợi
```json
{
  "message": "Shutting down, bye..."
}
```

## Demo: Tắt Các Microservice

### Tắt Accounts Microservice

1. Mở Postman
2. Điều hướng đến folder Accounts microservice
3. Chọn request "Shutdown"
4. Xác minh URL: `http://localhost:8080/actuator/shutdown`
5. Click nút "Send"
6. Quan sát response: "Shutting down, Bye bye"

### Các Bước Xác Minh

1. **Kiểm Tra Eureka Dashboard**
   - Refresh trang Eureka Server dashboard
   - Xác minh rằng AccountsApplication không còn trong danh sách
   - Xác nhận hủy đăng ký thành công

2. **Kiểm Tra Application Logs**
   ```
   Stopping service...
   Unregistering...
   Account deregistered from Eureka Server
   Status: 200 (Success)
   ```

### Tắt Cards Microservice

1. Trong Postman, điều hướng đến folder Cards
2. Chọn request "Shutdown"
3. Đảm bảo URL sử dụng port 9000: `http://localhost:9000/actuator/shutdown`
4. Click nút "Send"
5. Xác minh đã nhận được response

### Tắt Loans Microservice

1. Trong Postman, điều hướng đến folder Loans
2. Chọn request "Shutdown"
3. Click nút "Send"
4. Xác minh đã nhận được response

## Xác Thực và Kiểm Chứng

### Xác Minh Trên Eureka Dashboard
Sau khi tắt tất cả các microservice:
- Refresh Eureka Server dashboard
- **Không nên có instance nào khả dụng**
- Xác nhận tất cả microservices đã hủy đăng ký thành công

### Xác Minh Console Log

**Logs của Cards Microservice:**
```
Unregistering...
Status: 200 from Eureka Server
```

**Logs của Loans Microservice:**
```
Unregistering...
Status: 200 from Eureka Server
```

## Những Điểm Chính Cần Ghi Nhớ

### Đăng Ký và Hủy Đăng Ký Tự Động
- **Khởi động**: Microservices tự động đăng ký với Eureka Server
- **Tắt máy**: Microservices tự động hủy đăng ký trong quá trình graceful shutdown

### Ý Nghĩa Đối Với Service Discovery
- Không có entry trong service registry = Không thể service discovery
- Hủy đăng ký đúng cách ngăn chặn các entry service cũ
- Đảm bảo thông tin tình trạng service chính xác

### Best Practices (Thực Hành Tốt Nhất)
1. Luôn sử dụng graceful shutdown trong môi trường production
2. Không bao giờ force-kill microservices bằng nút stop của IDE trong các môi trường cao hơn
3. Theo dõi logs hủy đăng ký để đảm bảo hoàn thành thành công (HTTP status 200)
4. Triển khai các shutdown script phù hợp cho automated deployments

## Khắc Phục Sự Cố

### Các Vấn Đề Thường Gặp

**Vấn đề**: Shutdown endpoint trả về 405 Method Not Allowed
- **Nguyên nhân**: Sử dụng GET thay vì POST
- **Giải pháp**: Sử dụng phương thức POST cho shutdown endpoint

**Vấn đề**: Không tìm thấy endpoint (404)
- **Nguyên nhân**: Actuator shutdown chưa được kích hoạt
- **Giải pháp**: Xác minh các thuộc tính cấu hình được thiết lập đúng

**Vấn đề**: Service vẫn xuất hiện trong Eureka Dashboard
- **Nguyên nhân**: Forced shutdown không có hủy đăng ký
- **Giải pháp**: Đợi lease expiration của Eureka hoặc restart Eureka Server

## Các Bước Tiếp Theo

Trong các bài giảng tiếp theo, chúng ta sẽ khám phá:
- **Cơ Chế Heartbeat**: Cách các microservice gửi heartbeat tới Eureka Server
- **Giám Sát Sức Khỏe**: Cơ chế health check của Eureka Server
- **Lease Renewal**: Hiểu về quá trình lease expiration và renewal

## Kết Luận

Graceful shutdown và hủy đăng ký đúng cách là rất quan trọng để duy trì một hệ sinh thái microservices khỏe mạnh. Bằng cách sử dụng Actuator shutdown endpoint, các microservice có thể tự loại bỏ khỏi service registry một cách sạch sẽ, đảm bảo rằng các ứng dụng client không cố gắng định tuyến request đến các service không khả dụng.

---

**Các Chủ Đề Liên Quan:**
- Đăng Ký Service
- Cấu Hình Eureka Server
- Spring Boot Actuator
- Giám Sát Sức Khỏe Microservices