# Kết nối SSH vào EC2 Instance (Linux/Mac)

## Giới thiệu

SSH (Secure Shell) là một trong những chức năng quan trọng nhất khi làm việc với Amazon Cloud. Nó cho phép bạn điều khiển một máy chủ từ xa bằng cách sử dụng terminal hoặc giao diện dòng lệnh của bạn.

## Cách SSH hoạt động với EC2

Khi bạn SSH vào một EC2 instance:

1. EC2 instance của bạn chạy Amazon Linux 2 và có địa chỉ IP công khai
2. Security group của bạn cho phép truy cập qua Port 22 (cổng SSH)
3. Máy tính cục bộ của bạn kết nối với EC2 instance qua web thông qua Port 22
4. Giao diện dòng lệnh của bạn hoạt động như thể bạn đang ở bên trong máy đó

## Yêu cầu trước khi bắt đầu

Trước khi bắt đầu, hãy đảm bảo bạn có:
- Một EC2 instance đang chạy với Amazon Linux 2
- File PEM đã tải xuống (ví dụ: `EC2Tutorial.pem`)
- Security group được cấu hình để cho phép SSH (Port 22) từ 0.0.0.0/0
- Địa chỉ IPv4 công khai của instance

## Hướng dẫn từng bước

### 1. Chuẩn bị file PEM

- Xóa bất kỳ khoảng trắng nào khỏi tên file (ví dụ: đổi tên `EC2 Tutorial.pem` thành `EC2Tutorial.pem`)
- Đặt file vào một thư mục bạn chọn (ví dụ: thư mục `aws-course`)

### 2. Lấy thông tin Instance

1. Điều hướng đến trang tổng quan EC2 instance
2. Tìm instance của bạn
3. Sao chép địa chỉ IPv4 công khai
4. Xác minh security group có quy tắc cho Port 22 (SSH) từ 0.0.0.0/0

### 3. Điều hướng đến đúng thư mục

Mở terminal và điều hướng đến nơi chứa file PEM của bạn:

```bash
# Kiểm tra thư mục hiện tại
pwd

# Liệt kê các file trong thư mục hiện tại
ls

# Chuyển đến thư mục chứa file PEM
cd aws-course

# Xác minh file PEM có mặt
ls
```

**Quan trọng**: Terminal của bạn phải ở cùng thư mục với file PEM để lệnh SSH hoạt động.

### 4. Thiết lập quyền đúng

Trước khi sử dụng file PEM, bạn cần thiết lập quyền chính xác:

```bash
chmod 0400 EC2Tutorial.pem
```

Lệnh này đảm bảo file khóa của bạn không thể xem công khai và bảo vệ nó khỏi truy cập trái phép.

### 5. Kết nối qua SSH

Sử dụng lệnh sau để kết nối với EC2 instance:

```bash
ssh -i EC2Tutorial.pem ec2-user@<IP_CONG_KHAI_CUA_BAN>
```

Thay thế `<IP_CONG_KHAI_CUA_BAN>` bằng địa chỉ IPv4 công khai của instance.

**Tại sao lại là `ec2-user`?** Amazon Linux 2 AMI đi kèm với một user được cấu hình sẵn tên là `ec2-user`.

### 6. Kết nối lần đầu

Lần kết nối đầu tiên, bạn có thể thấy một thông báo yêu cầu xác nhận tin cậy instance:
```
The authenticity of host '...' can't be established.
Are you sure you want to continue connecting (yes/no)?
```

Nhập `yes` và nhấn Enter.

## Làm việc với EC2 Instance

Sau khi kết nối, bạn có thể thực thi các lệnh trực tiếp trên EC2 instance:

```bash
# Kiểm tra user hiện tại
whoami

# Kiểm tra kết nối mạng
ping google.com
```

Để dừng một lệnh đang chạy, nhấn `Ctrl + C`.

## Ngắt kết nối khỏi Instance

Để thoát khỏi phiên SSH, bạn có thể:
- Nhập `exit` và nhấn Enter
- Nhấn `Ctrl + D`

## Kết nối lại

Để kết nối lại với instance sau này, sử dụng cùng lệnh SSH:

```bash
ssh -i EC2Tutorial.pem ec2-user@<IP_CONG_KHAI_CUA_BAN>
```

**Lưu ý quan trọng**: Nếu bạn dừng và sau đó khởi động lại EC2 instance, địa chỉ IP công khai có thể thay đổi. Hãy đảm bảo cập nhật địa chỉ IP trong lệnh SSH của bạn.

## Lỗi thường gặp và cách khắc phục

### "Too many authentication failures"
Điều này có nghĩa là bạn chưa chỉ định file khóa PEM. Sử dụng flag `-i` với file PEM của bạn.

### "Unprotected key file"
File PEM của bạn có quyền không chính xác. Chạy `chmod 0400 EC2Tutorial.pem` để khắc phục.

### "No such file or directory"
Terminal của bạn không ở đúng thư mục. Điều hướng đến thư mục chứa file PEM bằng lệnh `cd`.

## Tóm tắt

SSH cho phép bạn truy cập và điều khiển các EC2 instance từ xa một cách an toàn. Bằng cách làm theo các bước này, bạn có thể thiết lập kết nối đến Amazon Linux 2 instance và thực thi các lệnh như thể bạn đang sử dụng máy đó trực tiếp.