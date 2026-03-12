# SSH vào EC2 Instance sử dụng Windows với PuTTY

## Giới thiệu

SSH (Secure Shell) là một trong những chức năng quan trọng nhất khi làm việc với Amazon Cloud. Nó cho phép bạn điều khiển máy chủ từ xa bằng giao diện dòng lệnh.

## Tổng quan

Trong hướng dẫn này, bạn sẽ học cách:
- Kết nối đến EC2 instance đang chạy Amazon Linux 2
- Sử dụng PuTTY làm SSH client trên Windows
- Cấu hình xác thực sử dụng file khóa PPK

### SSH hoạt động như thế nào

Máy EC2 của bạn chạy Amazon Linux 2 với địa chỉ IP công khai. Với security group SSH được cấu hình cho phép SSH trên cổng 22, máy Windows của bạn có thể kết nối qua internet trực tiếp đến EC2 instance và điều khiển nó bằng dòng lệnh.

## Yêu cầu

- Windows 7, Windows 8, hoặc Windows 10
- EC2 instance với security group SSH đã được cấu hình (cổng 22 mở)
- File key pair EC2 (định dạng .pem)

## Bước 1: Tải và Cài đặt PuTTY

PuTTY là SSH client miễn phí cho Windows.

1. Tải PuTTY từ trang web chính thức
2. Chọn bản cài đặt 64-bit (khuyến nghị)
3. Chạy file cài đặt và hoàn tất quá trình cài đặt
4. Click qua các bước cài đặt (Next → Next → Yes → Install)

Sau khi cài đặt, bạn sẽ có hai ứng dụng quan trọng:
- **PuTTY**: SSH client
- **PuTTYgen**: Công cụ chuyển đổi khóa

## Bước 2: Chuyển đổi PEM sang định dạng PPK (nếu cần)

Nếu bạn đã tải key pair EC2 ở định dạng PEM, bạn cần chuyển đổi nó sang định dạng PPK cho PuTTY.

1. Mở **PuTTYgen**
2. Click **Load**
3. Điều hướng đến vị trí file khóa của bạn (ví dụ: Desktop)
4. Thay đổi bộ lọc file thành "All Files (*.*)" ở góc dưới bên phải
5. Chọn file `.pem` của bạn (ví dụ: `EC2tutorial.pem`)
6. Click **Open** - bạn sẽ thấy thông báo thành công
7. Click **Save private key**
8. Khi được hỏi về passphrase, click **Yes** (nếu bạn không muốn đặt passphrase)
9. Lưu file dưới tên `EC2tutorial.ppk`

File PEM của bạn đã được chuyển đổi thành công sang định dạng PPK.

## Bước 3: Cấu hình Kết nối PuTTY

1. Mở ứng dụng **PuTTY**
2. Trong danh mục Session:
   - Nhập địa chỉ IPv4 công khai của EC2 instance vào trường "Host Name"
   - Định dạng: `ec2-user@<địa-chỉ-ip-công-khai>`
   - Ví dụ: `ec2-user@54.123.45.67`
   - Đảm bảo loại kết nối là **SSH**
   - Port phải là **22**
3. Lưu phiên này:
   - Nhập tên trong "Saved Sessions" (ví dụ: "EC2 Instance")
   - Click **Save**

## Bước 4: Cấu hình Xác thực

1. Trong cửa sổ PuTTY Configuration, điều hướng đến:
   - **Connection** → **SSH** → **Auth**
2. Click **Browse** bên cạnh "Private key file for authentication"
3. Điều hướng đến vị trí file `.ppk` của bạn
4. Chọn file PPK của bạn (ví dụ: `EC2tutorial.ppk`)
5. Quay lại danh mục **Session**
6. Click **Save** một lần nữa để lưu profile hoàn chỉnh

## Bước 5: Kết nối đến EC2 Instance

1. Trong PuTTY, chọn phiên đã lưu của bạn (ví dụ: "EC2 Instance")
2. Click **Load**
3. Click **Open**
4. Ở lần kết nối đầu tiên, chấp nhận cảnh báo bảo mật bằng cách click **Yes**
5. Bây giờ bạn đã được kết nối đến Amazon Linux 2 instance

## Xác minh Kết nối

Sau khi kết nối, bạn có thể xác minh kết nối với các lệnh sau:

```bash
whoami
# Output: ec2-user

ping google.com
# Nhấn Ctrl+C để dừng
```

## Mẹo

- **Saved Sessions**: Sau khi cấu hình, bạn chỉ cần load phiên đã lưu và click Open cho các lần kết nối sau
- **Thoát**: Gõ `exit` hoặc đơn giản đóng cửa sổ PuTTY để kết thúc phiên
- **Dừng Lệnh**: Nhấn `Ctrl+C` để dừng các lệnh đang chạy

## Xử lý Sự cố

Nếu bạn gặp vấn đề xác thực:
1. Xác minh file PPK được cấu hình đúng trong SSH → Auth
2. Đảm bảo username `ec2-user` được bao gồm trong hostname
3. Kiểm tra security group EC2 cho phép SSH (cổng 22) từ IP của bạn
4. Xác minh bạn đang sử dụng đúng key pair được liên kết với instance

## Các Bước Tiếp theo

- Đối với người dùng Windows 10, có phương pháp SSH thay thế sử dụng SSH client tích hợp của Windows
- Thực hành chạy các lệnh Linux cơ bản trên EC2 instance
- Tìm hiểu về các phương pháp bảo mật tốt nhất của EC2

## Tóm tắt

Bạn đã học thành công cách:
- Cài đặt PuTTY trên Windows
- Chuyển đổi khóa PEM sang định dạng PPK sử dụng PuTTYgen
- Cấu hình và lưu profile kết nối PuTTY
- SSH vào EC2 instances sử dụng PuTTY

Bất cứ khi nào khóa học đề cập đến "SSH vào instance", người dùng Windows nên sử dụng PuTTY để kết nối.