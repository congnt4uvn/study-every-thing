# Cấu Hình Docker Compose Đa Môi Trường Cho Microservices

## Tổng Quan

Hướng dẫn này trình bày cách cấu hình và triển khai các microservices Spring Boot trên nhiều môi trường khác nhau (default, QA và production) sử dụng Docker Compose với các profile theo từng môi trường.

## Yêu Cầu Trước

- Đã cài đặt Docker Desktop
- Dự án Spring Boot microservices
- Các file cấu hình Docker Compose
- Repository Git cho quản lý cấu hình (eazybytes-config)

## Kiến Trúc

Thiết lập bao gồm các container sau:
- **RabbitMQ** - Message broker
- **Config Server** - Spring Cloud Config Server
- **Accounts Microservice** - Dịch vụ tài khoản
- **Loans Microservice** - Dịch vụ khoản vay
- **Cards Microservice** - Dịch vụ thẻ

## Tạo File Docker Compose Theo Môi Trường

### Bước 1: Dừng Các Container Đang Chạy

Trước khi tạo file Docker Compose mới, hãy dừng tất cả các container đang chạy:

```bash
docker compose down
```

Lệnh này sẽ dừng và xóa tất cả các container trong hệ thống của bạn.

### Bước 2: Tạo Cấu Hình Theo Profile

Quy trình rất đơn giản:

1. Sao chép hai file từ thư mục `default`
2. Dán chúng vào thư mục `prod`
3. Dán chúng vào thư mục `qa`

### Bước 3: Chỉnh Sửa Biến Môi Trường

Chỉ cần thay đổi duy nhất trong file `commonconfig.yml`:

**Cho môi trường Production:**
```yaml
spring:
  profiles:
    active: prod
```

**Cho môi trường QA:**
```yaml
spring:
  profiles:
    active: qa
```

## Lợi Ích Chính

### 1. Docker Image Bất Biến (Immutable)
- Sử dụng cùng một Docker image trên tất cả các môi trường
- Kiểm soát hành vi thông qua biến môi trường
- Duy trì tính nhất quán trong triển khai

### 2. Cấu Hình Theo Từng Môi Trường
- Tùy chỉnh tài nguyên cho từng môi trường
- Ví dụ: Tăng cấp phát bộ nhớ trong production
  ```yaml
  # commonconfig.yml - Production
  memory: 1024mb  # Thay vì 700mb trong default
  ```

### 3. Tích Hợp Spring Boot
- Tận dụng Spring profiles để quản lý cấu hình
- Tích hợp liền mạch với Docker containers
- Quản lý cấu hình bên ngoài

## Kiểm Tra Cấu Hình

### Khởi Động Container Với Profile Production

1. Di chuyển đến thư mục production:
   ```bash
   cd prod
   ```

2. Khởi động tất cả containers:
   ```bash
   docker compose up
   ```

3. Các container sau sẽ được khởi động:
   - RabbitMQ
   - Config Server
   - Loans Microservice
   - Cards Microservice
   - Accounts Microservice

### Xác Minh Trạng Thái Container

Kiểm tra trạng thái container trong Docker Desktop:
1. Mở Docker Desktop
2. Chọn profile `prod`
3. Xác minh từng container:
   - ✓ RabbitMQ - Khởi động thành công
   - ✓ Config Server - Khởi động thành công
   - ✓ Loans Microservice - Khởi động thành công
   - ✓ Cards Microservice - Khởi động thành công
   - ✓ Accounts Microservice - Khởi động thành công

## Kiểm Tra Thay Đổi Cấu Hình

### Kiểm Tra Cập Nhật Cấu Hình Động

1. **Chỉnh Sửa Cấu Hình:**
   - Truy cập repository `eazybytes-config`
   - Chỉnh sửa file `cards-prod.yml`
   - Thay đổi thuộc tính message:
     ```yaml
     message: "Docker APIs"
     ```
   - Commit thay đổi lên GitHub

2. **Kiểm Tra Thay Đổi:**
   - Sử dụng Postman để gọi API `contact-info` của Cards microservice
   - Kết quả trả về sẽ hiển thị: `"Docker APIs"`

3. **Hoàn Tác Thay Đổi:**
   - Chỉnh sửa `cards-prod.yml` một lần nữa
   - Đổi lại thành:
     ```yaml
     message: "Prod APIs"
     ```
   - Commit thay đổi lên GitHub

4. **Xác Minh Việc Hoàn Tác:**
   - Gọi API lại trong Postman
   - Kết quả trả về sẽ hiển thị: `"Prod APIs"`
   - Lưu ý: Có thể có độ trễ 5-10 giây để refresh thuộc tính

## Thực Hành Tốt Nhất

### 1. Quản Lý Cấu Hình
- Giữ cấu hình theo môi trường trong các file riêng biệt
- Sử dụng kiểm soát phiên bản (Git) cho repository cấu hình
- Triển khai theo dõi thay đổi phù hợp

### 2. Phương Pháp Học
- Hoàn thành khóa học theo tốc độ của riêng bạn
- Mục tiêu một phần mỗi ngày hoặc mỗi tuần
- Tránh cố gắng hoàn thành mọi thứ trong một lần
- Nghỉ ngơi để tiếp thu kiến thức

### 3. Phân Bổ Tài Nguyên
- Điều chỉnh tài nguyên container dựa trên nhu cầu môi trường
- Production thường yêu cầu nhiều bộ nhớ và CPU hơn
- Giám sát và tối ưu hóa dựa trên việc sử dụng thực tế

## Xử Lý Sự Cố

### Độ Trễ Refresh Cấu Hình
- Thay đổi cấu hình có thể mất 5-10 giây để lan truyền
- Đợi một chút trước khi kiểm tra sau khi commit thay đổi

### Vấn Đề Khởi Động Container
- Đảm bảo tất cả các port cần thiết đều khả dụng
- Kiểm tra Docker Desktop để xem log chi tiết của container
- Xác minh kết nối mạng giữa các container

## Tổng Kết

Thiết lập Docker Compose đa môi trường này cung cấp:
- ✓ Triển khai Docker image đơn lẻ trên tất cả các môi trường
- ✓ Quản lý cấu hình theo từng môi trường
- ✓ Tích hợp liền mạch với Spring Boot profiles
- ✓ Cập nhật cấu hình động mà không cần triển khai lại
- ✓ Linh hoạt tùy chỉnh tài nguyên theo từng môi trường

## Tài Nguyên và Hỗ Trợ

### Nhận Trợ Giúp
- **Website:** [eazybytes.com](https://eazybytes.com)
- **Email:** tutor@eazybytes.com
- **LinkedIn:** Theo dõi eazybytes để cập nhật thường xuyên
- **Udemy:** Gửi tin nhắn thông qua nền tảng khóa học

### Phản Hồi
Phản hồi của bạn rất có giá trị! Vui lòng:
- Cung cấp đánh giá khóa học
- Chia sẻ những gì bạn thích hoặc không thích
- Kết nối trên LinkedIn để phản hồi cá nhân
- Liên hệ qua email cho các câu hỏi cụ thể

---

**Bước Tiếp Theo:** Nghỉ ngơi và tiếp tục với phần tiếp theo khi sẵn sàng. Hãy nhớ, học tập đều đặn hiệu quả hơn việc học dồn!