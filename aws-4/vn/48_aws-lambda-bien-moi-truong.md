# AWS Lambda - Biến Môi Trường và Cấu Hình

## Tổng Quan

Hướng dẫn này bao gồm các cấu hình AWS Lambda, triển khai, và sử dụng biến môi trường để quản lý hành vi của hàm một cách hiệu quả.

## Cấu Hình và Triển Khai Lambda

Sau khi hiểu về các lời gọi Lambda (Lambda invocations), điều quan trọng là tìm hiểu về cấu hình và triển khai Lambda. Những khái niệm này giúp bạn quản lý và tối ưu hóa các hàm Lambda trong môi trường production.

## Biến Môi Trường (Environment Variables)

### Biến Môi Trường là gì?

Biến môi trường trong AWS Lambda là **các cặp khóa-giá trị ở dạng chuỗi** giúp bạn điều chỉnh hành vi của hàm mà không cần cập nhật mã nguồn.

### Các Tính Năng Chính

- **Có thể truy cập từ mã của bạn**: Biến môi trường có sẵn cho mã hàm Lambda của bạn tại thời điểm runtime
- **Biến hệ thống**: Lambda Service tự động thêm các biến môi trường hệ thống của riêng nó bên cạnh các biến tùy chỉnh của bạn
- **Mẫu lập trình phổ biến**: Sử dụng biến môi trường là một thực hành chuẩn trong phát triển phần mềm, và Lambda hỗ trợ đầy đủ cách tiếp cận này

## Bảo Mật: Mã Hóa Biến Môi Trường

### Tại Sao Cần Mã Hóa?

Biến môi trường thường chứa thông tin nhạy cảm như API keys, thông tin đăng nhập cơ sở dữ liệu, hoặc các bí mật khác. AWS cung cấp khả năng mã hóa để bảo vệ các giá trị này.

### Các Tùy Chọn Mã Hóa

1. **Lambda Service Key**: 
   - Mã hóa mặc định được cung cấp bởi AWS Lambda
   - Được quản lý hoàn toàn bởi AWS
   - Không cần cấu hình bổ sung

2. **Customer Master Key (CMK)**:
   - Sử dụng khóa KMS (Key Management Service) của riêng bạn
   - Kiểm soát tốt hơn việc quản lý khóa
   - Khả năng thiết lập chính sách khóa tùy chỉnh và lịch trình xoay khóa

### Sử Dụng KMS để Mã Hóa

AWS Key Management Service (KMS) có thể được sử dụng để mã hóa biến môi trường và lưu trữ các giá trị bí mật một cách an toàn:
- Các bí mật được mã hóa khi lưu trữ (at rest)
- Giải mã diễn ra tự động khi hàm Lambda thực thi
- Lựa chọn giữa khóa do AWS quản lý hoặc khóa do khách hàng quản lý

## Các Thực Hành Tốt Nhất

1. **Sử dụng biến môi trường** cho các giá trị cấu hình có thể thay đổi giữa các môi trường (dev, staging, production)
2. **Luôn mã hóa dữ liệu nhạy cảm** sử dụng KMS
3. **Tránh hardcode các bí mật** trong mã hàm Lambda của bạn
4. **Sử dụng customer master keys** để tăng cường kiểm soát mã hóa và đáp ứng yêu cầu tuân thủ
5. **Thường xuyên xoay các bí mật** được lưu trữ trong biến môi trường

## Thực Hành

Để thành thạo với biến môi trường Lambda:
- Tạo một hàm Lambda và thêm các biến môi trường
- Cấu hình mã hóa KMS cho các giá trị nhạy cảm
- Kiểm tra việc truy cập biến môi trường từ mã hàm của bạn
- Thực hành sử dụng cả khóa do AWS quản lý và khóa do khách hàng quản lý

## Tóm Tắt

Biến môi trường là một tính năng mạnh mẽ trong AWS Lambda cho phép quản lý cấu hình linh hoạt và an toàn. Bằng cách kết hợp biến môi trường với mã hóa KMS, bạn có thể xây dựng các hàm Lambda vừa dễ thay đổi vừa an toàn.
