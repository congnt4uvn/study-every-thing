# AWS Elastic Beanstalk - Sao Chép Môi Trường

## Tổng Quan

AWS Elastic Beanstalk cung cấp một tính năng hữu ích cho phép bạn sao chép một môi trường hiện có sang một môi trường mới với cấu hình hoàn toàn giống nhau. Điều này cực kỳ hữu ích khi bạn đã có phiên bản production của ứng dụng và muốn triển khai phiên bản test với các cài đặt giống hệt nhau.

## Các Tính Năng Chính

### Bảo Toàn Cấu Hình

Khi sao chép một môi trường, tất cả các tài nguyên và cấu hình từ môi trường gốc đều được bảo toàn, bao gồm:

- **Load Balancer**: Loại và cấu hình thiết lập
- **RDS Database**: Loại và cấu hình cơ sở dữ liệu (lưu ý: dữ liệu không được sao chép, chỉ có cấu hình)
- **Biến Môi Trường**: Tất cả các biến đặc thù cho môi trường
- **Cài Đặt Platform**: Tất cả các cấu hình và thiết lập nền tảng

### Tùy Chỉnh Sau Khi Sao Chép

Sau khi sao chép một môi trường, bạn có thể thay đổi các cài đặt của nó thông qua tab Configuration, cho phép bạn tùy chỉnh môi trường đã sao chép theo nhu cầu.

## Cách Sao Chép Môi Trường

### Sử Dụng AWS Console

1. Điều hướng đến ứng dụng Elastic Beanstalk của bạn
2. Chọn môi trường bạn muốn sao chép (ví dụ: "My Application dev")
3. Nhấp vào **Actions** → **Clone Environment**
4. Cấu hình các thiết lập sao chép:
   - Cung cấp tên môi trường mới (ví dụ: "dev-2", "test", v.v.)
   - Tùy chọn chọn phiên bản platform khác
   - Chọn service role phù hợp
5. Nhấp **Clone** để tạo môi trường mới

### Tùy Chọn Sao Chép

Giao diện sao chép cung cấp các tùy chọn hạn chế nhưng thiết yếu:
- Tên môi trường mới
- Phiên bản platform (nâng cấp tùy chọn)
- Lựa chọn service role

## Các Trường Hợp Sử Dụng

### Kiểm Thử và Phát Triển

Trường hợp sử dụng chính của việc sao chép môi trường là tạo một môi trường testing phản ánh thiết lập production của bạn. Điều này cho phép bạn:

1. Triển khai các phiên bản mới một cách an toàn
2. Thực hiện kiểm thử toàn diện trong môi trường giống production
3. Xác thực các thay đổi trước khi ảnh hưởng đến người dùng production

### Hoán Đổi Môi Trường

Sau khi kiểm thử trong môi trường đã sao chép, bạn có thể thực hiện hoán đổi URL môi trường để đưa phiên bản đã được kiểm thử lên production một cách mượt mà.

## Các Thực Hành Tốt Nhất

- Sử dụng quy ước đặt tên mô tả cho các môi trường đã sao chép (ví dụ: "prod", "staging", "test")
- Xem xét và tùy chỉnh các cài đặt trong tab Configuration sau khi sao chép
- Nhớ rằng dữ liệu RDS database không được sao chép - chỉ có cấu hình
- Xem xét hoán đổi môi trường cho các triển khai blue-green

## Tóm Tắt

Tính năng sao chép môi trường của Elastic Beanstalk đơn giản hóa quá trình tạo các môi trường giống hệt nhau cho mục đích testing và development. Bằng cách bảo toàn tất cả các cấu hình trong khi cho phép tùy chỉnh sau khi sao chép, nó cung cấp một cách tiếp cận linh hoạt để quản lý nhiều môi trường ứng dụng.