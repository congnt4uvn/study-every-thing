# Bài Tập Spring Boot Profiles - Cards và Loans Microservices

## Tổng Quan

Bài giảng này cung cấp một bài tập để thực hành triển khai Spring Boot profiles và quản lý cấu hình trong các microservices Cards và Loans, tương tự như những gì đã được thực hiện trong Accounts microservice.

## Tình Trạng Hiện Tại

Tính đến thời điểm này, chúng ta đã:
- Cập nhật accounts microservice với các khái niệm về Spring Boot profiles
- Giới thiệu nhiều thuộc tính bên trong file `application.yml`
- Đọc các thuộc tính đó thông qua ba REST APIs khác nhau bên trong accounts microservice

## Hướng Dẫn Bài Tập

### Nhiệm Vụ Của Bạn

Bạn cần thực hiện các thay đổi tương tự bên trong **Cards** và **Loans** microservices. Bài tập này được thiết kế để dễ dàng và cung cấp thực hành thực tế.

### Tài Liệu Tham Khảo

Nếu bạn có câu hỏi về tên thuộc tính hoặc giá trị thuộc tính cần sử dụng, vui lòng tham khảo code trong GitHub repository:

**Repository:** `eazybytes/microservice`

**Đường dẫn:** Section 6 → thư mục `v1-springboot`

Bên trong thư mục này, bạn sẽ tìm thấy ba microservices:
- **Accounts** (đã hoàn thành)
- **Cards** (bài tập)
- **Loans** (bài tập)

### Hướng Dẫn Cấu Hình

Đối với Cards và Loans microservices:
- Sử dụng **cấu trúc thuộc tính giống** như Accounts microservice
- Cung cấp **giá trị khác nhau** cho:
  - Số điện thoại
  - Chi tiết liên hệ
  - Thông điệp

Bạn có thể tìm tất cả chi tiết thuộc tính cần thiết bằng cách:
1. Truy cập vào GitHub repository
2. Xem file `application.yml` cho mỗi microservice

## Tại Sao Bài Tập Này Quan Trọng

### Lợi Ích Của Việc Hoàn Thành Bài Tập

1. **Thực Hành Thực Tế**: Bài tập này cung cấp kinh nghiệm thực tế với các khái niệm
2. **Củng Cố Kiến Thức**: Triển khai thay đổi trên nhiều microservices giúp củng cố việc học
3. **Trí Nhớ Tiềm Thức**: Thực hành lặp đi lặp lại giúp nhúng các khái niệm này vào trí nhớ tiềm thức của bạn
4. **Sẵn Sàng Cho Phỏng Vấn**: Với đủ thực hành, bạn sẽ có thể trả lời các câu hỏi liên quan một cách tự tin, ngay cả khi được hỏi bất ngờ

### Phương Pháp Học Tập

- Khóa học giải thích các khái niệm sử dụng một microservice (Accounts)
- Bạn thực hành bằng cách triển khai các thay đổi tương tự trong hai microservices khác (Cards và Loans)
- Phương pháp này mang lại thực hành đáng kể và hiểu biết sâu sắc

## Nhận Trợ Giúp

### Nếu Bạn Gặp Vấn Đề

- **Đừng nản lòng** nếu bạn đối mặt với thử thách
- Bài giảng tiếp theo sẽ đề cập nhanh đến các thay đổi code cho Cards và Loans microservices
- Bạn luôn có thể tham khảo code trong GitHub repository để được hướng dẫn

### GitHub Repository

Tất cả các triển khai hoàn chỉnh đều có sẵn trong GitHub repository để tham khảo nếu cần.

## Các Bước Tiếp Theo

1. Mở Cards microservice
2. Triển khai Spring Boot profiles và các thuộc tính cấu hình
3. Tạo REST APIs để đọc các thuộc tính
4. Lặp lại cho Loans microservice
5. Kiểm tra các triển khai của bạn

## Kết Luận

Bài tập này là một cơ hội tuyệt vời để thực hành và củng cố hiểu biết của bạn về:
- Spring Boot profiles
- Quản lý cấu hình
- Externalization thuộc tính
- Phát triển REST API

Chúc bạn may mắn với bài tập! Bài giảng tiếp theo sẽ xem xét giải pháp hoàn chỉnh.