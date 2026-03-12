# Amazon S3 Pre-Signed URLs (URL Đã Ký Trước)

## Tổng Quan

Amazon S3 Pre-Signed URLs là các URL tạm thời cung cấp quyền truy cập an toàn vào các đối tượng S3 riêng tư mà không cần phải công khai chúng. Các URL này có thể được tạo bằng S3 console, AWS CLI hoặc SDK.

## Tính Năng Chính

### Phương Thức Tạo URL
- **S3 Console**: Tạo URL với thời gian hết hạn lên đến 12 giờ
- **AWS CLI/SDK**: Tạo URL với thời gian hết hạn lên đến 168 giờ (7 ngày)

### Kế Thừa Quyền Truy Cập
Khi bạn tạo một pre-signed URL, người dùng nhận được URL đó sẽ kế thừa quyền của người đã tạo ra URL. Điều này áp dụng cho cả thao tác GET (tải xuống) và PUT (tải lên).

## Cách Hoạt Động Của Pre-Signed URLs

1. **Tạo URL**: Với vai trò chủ sở hữu bucket hoặc người dùng được ủy quyền, bạn tạo một pre-signed URL cho một file cụ thể trong S3 bucket riêng tư của mình
2. **Nhúng Thông Tin Xác Thực**: URL mang theo thông tin xác thực của bạn về quyền truy cập file đó
3. **Phân Phối URL**: Bạn gửi URL này cho người dùng mục tiêu cần quyền truy cập tạm thời
4. **Truy Cập File**: Người dùng truy cập file bằng pre-signed URL
5. **Truyền Tải An Toàn**: File được lấy từ S3 bucket trong khi vẫn duy trì tính riêng tư của bucket

## Các Trường Hợp Sử Dụng

Pre-signed URLs thường được sử dụng để cung cấp quyền truy cập tạm thời vào các file cụ thể cho cả việc tải xuống và tải lên:

### Các Tình Huống Tải Xuống
- **Truy Cập Nội Dung Premium**: Chỉ cho phép người dùng đã đăng nhập tải xuống video premium từ S3 bucket của bạn
- **Phân Phối File Động**: Cho phép danh sách người dùng thay đổi liên tục tải xuống file bằng cách tạo URL một cách động
- **Chia Sẻ File Tạm Thời**: Cung cấp quyền truy cập tạm thời vào các file cụ thể mà không ảnh hưởng đến bảo mật bucket

### Các Tình Huống Tải Lên
- **Quyền Tải Lên Tạm Thời**: Cho phép người dùng tạm thời tải file lên một vị trí cụ thể trong S3 bucket của bạn trong khi vẫn giữ bucket ở chế độ riêng tư

## Lợi Ích Về Bảo Mật

- Duy trì tính riêng tư của S3 bucket
- Cung cấp quyền truy cập có giới hạn thời gian
- Không cần phải công khai các file
- Kiểm soát chi tiết quyền truy cập file
- Tự động hết hạn quyền truy cập

## Tóm Tắt

Amazon S3 Pre-Signed URLs là một tính năng mạnh mẽ để cung cấp quyền truy cập an toàn, tạm thời vào các đối tượng S3 riêng tư. Chúng cho phép bạn chia sẻ file mà không làm tổn hại đến tình trạng bảo mật của bucket, khiến chúng trở nên lý tưởng cho các tình huống phân phối và tải lên file có kiểm soát.