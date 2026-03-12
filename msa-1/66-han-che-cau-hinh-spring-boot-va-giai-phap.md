# Hạn Chế Cấu Hình Spring Boot và Giải Pháp

## Tổng Quan

Tài liệu này thảo luận về các hạn chế và nhược điểm khi externalize (đưa ra ngoài) cấu hình chỉ sử dụng Spring Boot framework, và giới thiệu Spring Cloud Config Server như một giải pháp nâng cao để vượt qua những thách thức này.

## Hạn Chế của Quản Lý Cấu Hình Spring Boot

### 1. Quản Lý Cấu Hình Thủ Công

**Vấn Đề:**
- Externalize cấu hình thông qua CLI arguments, JVM properties và environment variables đòi hỏi thiết lập thủ công
- Việc inject cấu hình phải được thực hiện thủ công trong quá trình khởi động ứng dụng
- Thường liên quan đến việc thực thi các lệnh riêng biệt hoặc thiết lập ứng dụng thủ công
- Phụ thuộc nhiều vào CI/CD pipelines (GitHub Actions, Jenkins, v.v.)

**Tác Động:**
- Dẫn đến các lỗi tiềm ẩn trong quá trình triển khai
- Yêu cầu sự can thiệp của con người để thiết lập cấu hình
- Quản lý cấu hình trên tất cả các instance microservice trở nên khó khăn
- Nguy cơ sai sót cấu hình ngay cả khi có tự động hóa

### 2. Thiếu Kiểm Soát Phiên Bản và Audit

**Vấn Đề:**
- Với hàng trăm microservices, bạn sẽ có hàng nghìn thuộc tính cấu hình
- Các thuộc tính cấu hình phát triển và thay đổi hàng ngày
- Spring Boot profiles lưu trữ tất cả cấu hình trong source code
- Bất kỳ ai có quyền truy cập vào source code hoặc Docker images đều có thể xem tất cả cấu hình

**Tính Năng Cần Thiết:**
- Phiên bản hóa cấu hình dựa trên releases
- Chức năng audit:
  - Ai đã truy cập dữ liệu cấu hình
  - Client nào đã truy cập dữ liệu cấu hình
- Repository tập trung với version control
- Theo dõi các revisions và thay đổi

**Hạn Chế Hiện Tại:**
Spring Boot profiles đơn thuần không thể cung cấp những lợi thế này, khiến đây trở thành một hạn chế đáng kể.

### 3. Vấn Đề Bảo Mật

**Nhiều Vấn Đề Bảo Mật:**

#### a) Thiếu Kiểm Soát Truy Cập Chi Tiết
- Environment variables hiển thị cho tất cả quản trị viên server
- Thông tin đăng nhập database được lưu trữ dưới dạng environment variables bị lộ cho server admins
- Không có cơ chế kiểm soát truy cập chi tiết

#### b) Mật Khẩu Dạng Plain Text
- Mật khẩu database và dữ liệu nhạy cảm phải được lưu trữ ở dạng plain text
- Áp dụng cho tất cả các phương pháp: CLI, JVM properties, environment variables và Spring Boot profiles
- Không hỗ trợ mã hóa/giải mã
- Không thể lưu trữ secrets một cách bảo mật trong ứng dụng

#### c) Lộ Cấu Hình
- Cấu hình trong Spring Boot profiles được nhúng trong source code
- Bất kỳ ai có quyền truy cập code đều có thể xem tất cả cấu hình
- Không khôn ngoan khi để lộ tất cả cấu hình cho mọi người

### 4. Thách Thức Về Khả Năng Mở Rộng

**Kịch Bản:**
- 3 microservices (accounts, loans, cards)
- 3 instances mỗi microservice = 9 containers tổng cộng
- Mở rộng lên 100 microservices × 5 instances = 500 instances

**Vấn Đề:**
- Cung cấp cấu hình externalized cho hàng trăm instances cực kỳ khó khăn
- Các tác vụ thủ công phải được lặp lại cho từng microservice instance
- Phương pháp hiện tại không hoạt động cho nhiều microservice instances
- Quản lý cấu hình trở nên không thể quản lý được ở quy mô lớn

### 5. Không Cập Nhật Cấu Hình Tại Runtime

**Vấn Đề:**
- Bất kỳ thay đổi giá trị property nào đều yêu cầu restart ứng dụng
- Không thể thay đổi properties trong khi microservices đang chạy
- Phải restart tất cả containers/microservices để áp dụng thay đổi cấu hình

**Hành Vi Mong Muốn:**
- Microservices nên tự động đọc các giá trị property mới nhất
- Không cần restart cho việc cập nhật cấu hình
- Khả năng làm mới cấu hình động

## Kết Luận

Với tất cả những hạn chế này, chỉ riêng Spring Boot là không đủ để quản lý cấu hình trong các ứng dụng microservices.

### Khi Nào Chỉ Sử Dụng Spring Boot:

1. **Dự Án Nhỏ:** Số lượng properties rất hạn chế với các ứng dụng mức độ nghiêm trọng thấp
2. **Thiếu Kiến Thức:** Các team không biết về các tùy chọn quản lý cấu hình nâng cao

## Giải Pháp: Spring Cloud Config Server

Để vượt qua tất cả những thách thức này, giải pháp được đề xuất là **Spring Cloud Config Server**, cung cấp:

- Quản lý cấu hình tập trung
- Version control và auditing
- Tính năng bảo mật nâng cao
- Hỗ trợ mã hóa/giải mã
- Cập nhật cấu hình động không cần restart
- Quản lý cấu hình có thể mở rộng cho hàng trăm microservices

## Các Bước Tiếp Theo

Các bài giảng tiếp theo sẽ đề cập đến việc triển khai và sử dụng Spring Cloud Config Server để giải quyết tất cả các hạn chế đã thảo luận ở trên.

---

**Ghi Chú Khóa Học:** Nội dung này là một phần của khóa học microservices toàn diện tập trung vào các công nghệ Spring Boot và Spring Cloud.