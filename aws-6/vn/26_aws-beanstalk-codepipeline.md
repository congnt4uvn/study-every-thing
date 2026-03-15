# Tài Liệu Học Tập AWS Elastic Beanstalk và Code Pipeline

## Tổng Quan
Tài liệu này hướng dẫn thiết lập và cấu hình môi trường AWS Elastic Beanstalk để sử dụng với AWS Code Pipeline, cho phép tự động hóa quy trình triển khai ứng dụng.

## Điều Kiện Tiên Quyết
Trước khi làm việc với Code Pipeline, bạn cần thiết lập các môi trường AWS Elastic Beanstalk làm đích triển khai.

## Thiết Lập AWS Elastic Beanstalk

### Tạo Môi Trường Đầu Tiên

**Bước 1: Cấu Hình Ứng Dụng**
- Tên Ứng Dụng: `my first web app Beanstalk`
- Loại Môi Trường: Web server environment (môi trường máy chủ web)
- Tên Môi Trường: `My first web app Beanstalk`

**Bước 2: Lựa Chọn Nền Tảng**
- Nền Tảng: Managed platform (nền tảng được quản lý)
- Runtime: Node.js (phiên bản mới nhất)
- Mã Ứng Dụng: Sample application (ứng dụng mẫu)
- Loại Instance: Single instance (instance đơn)

**Bước 3: Cấu Hình**
- Key Pair: Không xác định (tùy chọn)
- Xem lại và gửi cấu hình

**Bước 4: Triển Khai**
- Đợi môi trường được tạo và triển khai thành công
- Bạn sẽ thấy thông báo "Congratulations" khi triển khai thành công

### Tạo Môi Trường Thứ Hai (Production)

**Bước 1: Điều Hướng Đến Ứng Dụng**
- Vào bảng điều khiển ứng dụng
- Chọn "Create new environment" (Tạo môi trường mới)

**Bước 2: Cấu Hình Môi Trường**
- Loại Môi Trường: Web server environment
- Tên Môi Trường: `prod`
- Nền Tảng: Node.js
- Mã Ứng Dụng: Sample application

**Bước 3: Triển Khai**
- Bỏ qua để đến phần xem lại
- Gửi cấu hình
- Đợi triển khai hoàn tất

## Tích Hợp AWS Code Pipeline

### Mục Đích
Code Pipeline sẽ được sử dụng để triển khai các bản cập nhật đến cả hai môi trường Beanstalk:
1. Môi trường phát triển
2. Môi trường sản xuất

### Quy Trình Triển Khai
Code Pipeline cho phép tự động triển khai các bản cập nhật ứng dụng đến nhiều môi trường, tối ưu hóa quy trình CI/CD.

## Lưu Ý Quan Trọng

### Quản Lý Chi Phí
⚠️ **QUAN TRỌNG**: Nhớ xóa các môi trường sau khi hoàn thành bài lab:
- Các EC2 instance đang chạy sẽ phát sinh chi phí
- Luôn dọn dẹp tài nguyên khi không sử dụng
- Xóa cả hai môi trường để tránh chi phí không cần thiết

### Khái Niệm Chính
- **Elastic Beanstalk**: Dịch vụ AWS để triển khai và mở rộng quy mô ứng dụng web
- **Code Pipeline**: Dịch vụ tích hợp liên tục và phân phối liên tục
- **Environment (Môi trường)**: Một phiên bản ứng dụng đang chạy trên tài nguyên AWS
- **Single Instance**: Cấu hình triển khai sử dụng một EC2 instance

## Thực Hành Tốt Nhất
1. Luôn sử dụng ứng dụng mẫu để học và kiểm tra
2. Dọn dẹp tài nguyên sau khi hoàn thành hướng dẫn
3. Sử dụng nhiều môi trường cho quy trình triển khai phù hợp (dev, staging, prod)
4. Theo dõi bảng điều khiển thanh toán AWS thường xuyên

## Các Bước Tiếp Theo
- Hoàn thành cấu hình Code Pipeline thực hành
- Thực hành triển khai các bản cập nhật qua pipeline
- Khám phá các chiến lược triển khai đa môi trường
