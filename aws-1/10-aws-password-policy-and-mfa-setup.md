# Hướng Dẫn Thiết Lập Chính Sách Mật Khẩu và MFA trên AWS

## Tổng Quan

Hướng dẫn này bao gồm hai biện pháp bảo mật thiết yếu cho tài khoản AWS:
1. Thiết lập chính sách mật khẩu
2. Cấu hình xác thực đa yếu tố (MFA) cho tài khoản root

## Thiết Lập Chính Sách Mật Khẩu

### Truy Cập Cài Đặt Chính Sách Mật Khẩu

1. Điều hướng đến **Account Settings** (Cài đặt tài khoản) ở phía bên trái của bảng điều khiển IAM
2. Tìm mục **Password Policy** (Chính sách mật khẩu)
3. Nhấp **Edit** (Chỉnh sửa) để thay đổi chính sách

### Các Tùy Chọn Chính Sách Mật Khẩu

Bạn có hai tùy chọn chính:

#### Tùy Chọn 1: Chính Sách Mật Khẩu Mặc Định của IAM
Sử dụng chính sách mật khẩu mặc định được cấu hình sẵn của AWS với các yêu cầu tiêu chuẩn.

#### Tùy Chọn 2: Chính Sách Mật Khẩu Tùy Chỉnh
Tùy chỉnh các yêu cầu mật khẩu của bạn với các tùy chọn sau:

- **Độ dài tối thiểu của mật khẩu**
- **Yêu cầu chữ in hoa**
- **Yêu cầu chữ thường**
- **Yêu cầu số**
- **Yêu cầu ký tự đặc biệt** (không phải chữ và số)
- **Thời hạn mật khẩu** (ví dụ: hết hạn sau 90 ngày)
- **Yêu cầu đặt lại bởi quản trị viên** cho mật khẩu hết hạn
- **Cho phép người dùng thay đổi mật khẩu của họ**
- **Ngăn chặn tái sử dụng mật khẩu**

Chính sách mật khẩu có thể được chỉnh sửa trực tiếp từ bảng điều khiển IAM, cung cấp lớp bảo mật đầu tiên cho tài khoản.

## Cấu Hình Xác Thực Đa Yếu Tố (MFA)

### Tại Sao MFA Quan Trọng

Xác thực đa yếu tố thêm một lớp bảo mật bổ sung cho tài khoản root của bạn, đây là tài khoản quan trọng nhất trong môi trường AWS của bạn.

### ⚠️ Cảnh Báo Quan Trọng

**Trước khi tiếp tục**: Một số người dùng đã bị khóa tài khoản sau khi mất quyền truy cập vào thiết bị MFA của họ. Nếu bạn lo ngại về việc mất điện thoại hoặc thiết bị MFA:
- Cân nhắc chỉ xem hướng dẫn này mà không thực hiện
- Đảm bảo bạn có thể duy trì quyền truy cập vào thiết bị MFA của mình
- Nhớ rằng bạn có thể xóa thiết bị MFA sau khi kích hoạt nếu cần

### Thiết Lập MFA

#### Bước 1: Truy Cập Thông Tin Bảo Mật

1. Nhấp vào **tên tài khoản** của bạn ở thanh điều hướng trên cùng
2. Chọn **Security Credentials** (Thông tin bảo mật)
3. Nếu đăng nhập bằng tài khoản root, bạn sẽ thấy "My security credentials root user"

#### Bước 2: Gán Thiết Bị MFA

1. Nhấp vào **Assign MFA device** (Gán thiết bị MFA)
2. Đặt tên cho thiết bị của bạn (ví dụ: "my iPhone")
3. Chọn loại thiết bị MFA:
   - **Authenticator app** (Ứng dụng xác thực) - khuyến nghị cho hầu hết người dùng
   - **Security key** (Khóa bảo mật)
   - **Hardware TOTP token** (Token TOTP phần cứng)

#### Bước 3: Cấu Hình Ứng Dụng Xác Thực

1. AWS cung cấp danh sách các ứng dụng tương thích cho cả Android và iOS
2. Ứng dụng được khuyến nghị: **Twilio Authenticator** (hoặc các ứng dụng tương tự như Google Authenticator, Microsoft Authenticator)
3. Nhấp **Show QR code** (Hiển thị mã QR)

#### Bước 4: Quét Mã QR

1. Mở ứng dụng xác thực trên điện thoại của bạn
2. Thêm tài khoản mới
3. Quét mã QR hiển thị trên bảng điều khiển AWS
4. Lưu tài khoản trong ứng dụng của bạn

#### Bước 5: Xác Minh Cài Đặt

1. Ứng dụng xác thực sẽ tạo mã 6 chữ số thay đổi định kỳ
2. AWS yêu cầu hai mã liên tiếp để xác minh cài đặt đúng:
   - Nhập **mã MFA thứ nhất** (ví dụ: 301935)
   - Đợi mã thay đổi
   - Nhập **mã MFA thứ hai** (ví dụ: 792843)
3. Nhấp **Add MFA** (Thêm MFA)

### Quản Lý Thiết Bị MFA

- Bạn có thể thêm tối đa **8 thiết bị MFA** cho mỗi tài khoản
- Xem tất cả các thiết bị MFA đã cấu hình trong phần thông tin bảo mật
- Xóa thiết bị MFA nếu cần bằng cách chọn chúng từ danh sách

## Sử Dụng MFA Để Đăng Nhập

Sau khi thiết lập MFA, quy trình đăng nhập của bạn sẽ thay đổi:

1. Điều hướng đến trang đăng nhập AWS
2. Nhập **email tài khoản root và mật khẩu** của bạn
3. Sau khi xác thực thành công, bạn sẽ được nhắc nhập **mã MFA**
4. Mở ứng dụng xác thực của bạn
5. Nhập mã 6 chữ số hiện tại
6. Nhấp **Submit** (Gửi)

Bây giờ bạn sẽ được đăng nhập với mức độ bảo mật được nâng cao trên tài khoản của mình.

## Kết Luận

Bằng cách triển khai cả chính sách mật khẩu mạnh và MFA, bạn đã cải thiện đáng kể tư thế bảo mật của tài khoản AWS. Đây là những thực hành bảo mật cơ bản nên được triển khai trên tất cả các tài khoản AWS, đặc biệt là những tài khoản có quyền truy cập root.

## Các Bước Tiếp Theo

- Cân nhắc triển khai MFA cho tất cả người dùng IAM, không chỉ tài khoản root
- Thường xuyên xem xét và cập nhật chính sách mật khẩu của bạn
- Giữ thiết bị MFA của bạn an toàn và có sao lưu
- Ghi chép thiết lập MFA của bạn cho mục đích khắc phục thảm họa