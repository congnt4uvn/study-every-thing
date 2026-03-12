# Cài Đặt AWS CLI Trên Windows

## Tổng Quan

Hướng dẫn này sẽ giúp bạn cài đặt AWS Command Line Interface (CLI) phiên bản 2 trên Windows bằng trình cài đặt MSI.

## Yêu Cầu

- Hệ điều hành Windows
- Kết nối Internet để tải trình cài đặt
- Quyền quản trị viên để cài đặt

## Các Bước Cài Đặt

### 1. Tìm Kiếm Trình Cài Đặt AWS CLI

1. Mở trình duyệt web của bạn
2. Tìm kiếm "aws CLI install windows" trên Google
3. Tìm trang cài đặt AWS CLI phiên bản 2 cho Windows

### 2. Tải Trình Cài Đặt MSI

1. Truy cập trang tài liệu chính thức của AWS
2. Cuộn xuống phần "Install on Windows"
3. Nhấp vào liên kết tải xuống trình cài đặt MSI
4. Trình cài đặt sẽ được tải xuống máy tính của bạn

### 3. Chạy Trình Cài Đặt

1. Tìm và chạy trình cài đặt MSI đã tải xuống
2. Nhấp **Next** trên màn hình chào mừng
3. Chấp nhận các điều khoản của thỏa thuận cấp phép
4. Nhấp **Next** để tiếp tục
5. Nhấp **Install** để bắt đầu cài đặt
6. Nếu được nhắc bởi User Account Control, nhấp **Yes** để cho phép cài đặt
7. Đợi quá trình cài đặt hoàn tất
8. Nhấp **Finish** khi hoàn tất

### 4. Xác Minh Cài Đặt

1. Mở Command Prompt (tìm kiếm "Command Prompt" trong Windows)
2. Gõ lệnh sau và nhấn Enter:
   ```bash
   aws --version
   ```
3. Bạn sẽ thấy kết quả tương tự như:
   ```
   aws-cli/2.x.x Python/x.x.x Windows/x.x.x
   ```

Nếu bạn thấy phiên bản bắt đầu bằng "2", AWS CLI của bạn đã được cài đặt đúng cách và sẵn sàng sử dụng.

## Nâng Cấp AWS CLI

Để nâng cấp AWS CLI lên phiên bản mới nhất:

1. Tải trình cài đặt MSI mới nhất từ trang web AWS
2. Chạy trình cài đặt
3. Quá trình cài đặt sẽ tự động nâng cấp phiên bản hiện tại của bạn

## Có Gì Mới Trong Phiên Bản 2

AWS CLI phiên bản 2 cung cấp một số cải tiến so với phiên bản 1:

- **Hiệu Suất Được Cải Thiện**: Tốc độ thực thi và hiệu quả tốt hơn
- **Khả Năng Nâng Cao**: Các tính năng và chức năng bổ sung
- **API Giống Nhau**: Cấu trúc lệnh vẫn giống như phiên bản 1
- **Trình Cài Đặt Tốt Hơn**: Quá trình cài đặt đơn giản hơn

## Kết Luận

Bạn đã cài đặt thành công AWS CLI trên Windows và giờ đây đã sẵn sàng tương tác với các dịch vụ AWS từ dòng lệnh. Bạn có thể tiếp tục cấu hình thông tin xác thực AWS và bắt đầu sử dụng các lệnh AWS CLI.

## Các Bước Tiếp Theo

- Cấu hình AWS CLI với thông tin xác thực của bạn
- Học các lệnh AWS CLI cơ bản
- Khám phá các lệnh dành riêng cho dịch vụ AWS