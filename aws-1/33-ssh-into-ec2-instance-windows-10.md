# SSH vào EC2 Instance trên Windows 10

## Tổng quan

Hướng dẫn này trình bày cách kết nối đến Amazon EC2 instance sử dụng SSH trên Windows 10, bao gồm cả cách khắc phục các vấn đề về quyền truy cập với file PEM.

## Yêu cầu

- Windows 10 có sẵn lệnh SSH
- EC2 instance đang chạy trên AWS
- File khóa PEM đã tải xuống từ AWS
- Security group có mở cổng 22 cho SSH

## Kiểm tra SSH có sẵn

### Sử dụng Windows PowerShell

1. Mở Windows PowerShell
2. Gõ `ssh` và nhấn Enter
3. Nếu bạn thấy văn bản trợ giúp SSH, lệnh đã có sẵn

### Sử dụng Command Prompt

1. Mở Command Prompt
2. Gõ `ssh` và nhấn Enter
3. Nếu bạn thấy văn bản trợ giúp SSH, lệnh đã có sẵn

**Lưu ý:** Nếu lệnh SSH không có sẵn, bạn phải sử dụng phương pháp PuTTY thay thế.

## Kết nối đến EC2 Instance

### Bước 1: Di chuyển đến thư mục chứa file PEM

```powershell
# Di chuyển đến thư mục chứa file PEM của bạn
cd .\Desktop

# Liệt kê các file để xác nhận vị trí file PEM
ls
```

### Bước 2: Thực thi lệnh SSH

```powershell
ssh -i EC2Tutorial.pem ec2-user@<PUBLIC_IP>
```

**Giải thích lệnh:**
- `-i`: Chỉ định file khóa (identity file)
- `EC2Tutorial.pem`: Tên file khóa PEM của bạn
- `ec2-user`: Tên người dùng mặc định cho Amazon Linux instances
- `<PUBLIC_IP>`: Địa chỉ IP công khai của EC2 instance

### Bước 3: Chấp nhận xác thực host

Khi được nhắc "The authenticity of the host cannot be trusted, do you want to continue?", gõ `yes`.

## Khắc phục vấn đề quyền truy cập

Nếu bạn gặp lỗi quyền truy cập với file PEM, thực hiện các bước sau:

### Cấu hình quyền truy cập file

1. **Tìm file PEM của bạn**
   - Di chuyển đến thư mục chứa file PEM (ví dụ: Desktop)

2. **Truy cập thuộc tính bảo mật**
   - Nhấp chuột phải vào file PEM
   - Chọn "Properties"
   - Vào tab "Security"
   - Nhấp "Advanced"

3. **Đặt chủ sở hữu file**
   - Đảm bảo chủ sở hữu là bạn
   - Nếu không, nhấp "Change"
   - Trong "Object types", chọn loại người dùng của bạn
   - Đảm bảo "Locations" được đặt ở máy tính của bạn
   - Gõ tên người dùng của bạn và nhấp "Check Names"
   - Nhấp "OK" để xác nhận

4. **Xóa quyền thừa kế**
   - Nhấp "Disable inheritance"
   - Chọn "Remove all inherited permissions from this object"

5. **Xóa các thực thể không cần thiết**
   - Xóa các mục "SYSTEM" và "Administrators"
   - Các thực thể này không cần quyền truy cập vào file PEM của bạn

6. **Thêm người dùng của bạn với quyền Full Control**
   - Nhấp "Add"
   - Nhấp "Select a principal"
   - Gõ tên người dùng của bạn và nhấp "Check Names"
   - Nhấp "OK"
   - Cấp quyền "Full control"
   - Nhấp "OK" để lưu

7. **Xác minh quyền truy cập**
   - Nhấp "OK" trên tất cả các hộp thoại
   - Nhấp chuột phải vào file PEM lại và chọn "Properties"
   - Trong tab "Security", xác minh chỉ có tên người dùng của bạn xuất hiện với quyền đầy đủ

### Thử lại kết nối SSH

Sau khi sửa quyền truy cập, chạy lại lệnh SSH:

```powershell
ssh -i EC2Tutorial.pem ec2-user@<PUBLIC_IP>
```

Bạn sẽ không còn nhận được lỗi quyền truy cập hoặc nhắc xác thực host nữa.

## Sử dụng Command Prompt

Lệnh SSH tương tự hoạt động trong Command Prompt:

1. Mở Command Prompt
2. Di chuyển đến thư mục chứa file PEM
3. Thực thi lệnh SSH

```cmd
cd Desktop
ssh -i EC2Tutorial.pem ec2-user@<PUBLIC_IP>
```

## Ngắt kết nối khỏi EC2 Instance

Để thoát khỏi phiên SSH:

- Gõ `exit` và nhấn Enter, hoặc
- Nhấn `Ctrl + D`

## Mẹo

- Sử dụng phím Tab để tự động hoàn thành khi gõ tên file
- Đảm bảo security group của EC2 có quy tắc inbound cho phép SSH (cổng 22)
- Giữ file PEM của bạn an toàn và không bao giờ chia sẻ
- File `.ppk` chỉ cần thiết cho kết nối PuTTY

## Thực hành tốt về bảo mật

- Chỉ cấp quyền truy cập cho chính bạn đối với file PEM
- Lưu trữ file PEM ở vị trí an toàn
- Không bao giờ commit file PEM vào hệ thống quản lý phiên bản
- Sử dụng file PEM riêng biệt cho các môi trường khác nhau
- Thường xuyên thay đổi SSH keys

## Các vấn đề thường gặp

### Không tìm thấy lệnh SSH
- Cài đặt OpenSSH client từ Windows Features
- Thay thế: Sử dụng PuTTY cho kết nối SSH

### Timeout kết nối
- Xác minh security group cho phép inbound SSH (cổng 22)
- Kiểm tra EC2 instance đang chạy
- Xác minh bạn đang sử dụng đúng public IP

### Permission Denied (Từ chối quyền truy cập)
- Đảm bảo file PEM có quyền truy cập đúng (làm theo các bước sửa quyền)
- Xác minh bạn đang sử dụng đúng tên người dùng (ec2-user cho Amazon Linux)
- Xác nhận bạn đang sử dụng đúng file PEM cho instance

## Kết luận

Bây giờ bạn có thể SSH vào EC2 instance thành công trực tiếp từ Windows 10 sử dụng PowerShell hoặc Command Prompt. Với quyền truy cập file PEM được cấu hình đúng, bạn sẽ có quyền truy cập liền mạch vào cơ sở hạ tầng AWS của mình.