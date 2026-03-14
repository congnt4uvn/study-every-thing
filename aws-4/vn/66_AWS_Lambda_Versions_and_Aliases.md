# AWS Lambda Versions và Aliases

## Tổng Quan
Tài liệu này trình bày các khái niệm chính về Lambda Versions và Aliases trong AWS.

## Lambda Versions (Phiên Bản)

### Phiên Bản $LATEST
- Khi làm việc với Lambda functions, bạn sử dụng phiên bản **$LATEST** theo mặc định
- Phiên bản này là **mutable** (có thể thay đổi) - bạn có thể chỉnh sửa code, biến môi trường và cấu hình

### Xuất Bản Phiên Bản
- Khi bạn hài lòng với code của mình, bạn có thể **publish** (xuất bản) Lambda function để tạo phiên bản mới
- Sau khi publish, nó trở thành **V1**, **V2**, **V3**, v.v.
- Các phiên bản đã publish là **immutable** (không thể thay đổi)

### Immutable Nghĩa Là Gì?
- Bạn **không thể thay đổi** code
- Bạn **không thể thay đổi** biến môi trường
- Bạn **không thể thay đổi** bất kỳ cấu hình nào sau đó
- Phiên bản được cố định vĩnh viễn

### Đặc Điểm Của Phiên Bản
- Các phiên bản có **số thứ tự tăng dần** (V1 → V2 → V3)
- Mỗi phiên bản **độc lập** với nhau
- Mỗi phiên bản có **ARN riêng** (Amazon Resource Name - Tên Tài Nguyên Amazon)
- Mỗi phiên bản chứa cả code và cấu hình được khóa lại

### Trường Hợp Sử Dụng
- Tuyệt vời cho **phát triển lặp đi lặp lại**
- Đánh dấu **tiến trình** và sự tiến bộ
- Kiểm soát **phát hành** Lambda function của bạn

## Lambda Aliases (Bí Danh)

### Mục Đích
- Cung cấp **endpoint chuẩn** cho người dùng cuối
- Tránh việc lộ số phiên bản thay đổi cho người dùng

### Aliases Là Gì?
- **Con trỏ** trỏ đến các phiên bản Lambda function
- Là **mutable** (có thể thay đổi để trỏ đến các phiên bản khác nhau)
- Có thể được sử dụng để tạo các môi trường khác nhau

### Ví Dụ Về Aliases Phổ Biến
- **DEV** - trỏ đến phiên bản phát triển
- **TEST** - trỏ đến phiên bản kiểm thử
- **PROD** - trỏ đến phiên bản sản xuất

### Cách Hoạt Động Của Aliases
```
$LATEST (phiên bản có thể thay đổi)
   ↓
  V1 (phiên bản không thể thay đổi)
   ↓
  V2 (phiên bản không thể thay đổi)
   ↑
DEV Alias → trỏ đến V2
TEST Alias → trỏ đến V1
PROD Alias → trỏ đến V1
```

### Sự Khác Biệt Chính
- **Versions**: Immutable (không thể thay đổi)
- **Aliases**: Mutable (có thể cập nhật để trỏ đến các phiên bản khác nhau)

## Lợi Ích
1. **Quản Lý Phiên Bản**: Theo dõi các phiên bản khác nhau của Lambda function
2. **Quản Lý Môi Trường**: Tách biệt môi trường DEV, TEST và PROD
3. **Triển Khai An Toàn**: Kiểm thử phiên bản mới trước khi đưa vào sản xuất
4. **Endpoints Ổn Định**: Người dùng truy cập tên alias cố định thay vì số phiên bản thay đổi
