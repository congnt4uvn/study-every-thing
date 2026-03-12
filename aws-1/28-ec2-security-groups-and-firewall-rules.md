# Nhóm Bảo Mật EC2 và Quy Tắc Tường Lửa

## Giới Thiệu Về Nhóm Bảo Mật (Security Groups)

Nhóm bảo mật là thành phần cơ bản để triển khai bảo mật mạng trong AWS cloud. Chúng hoạt động như tường lửa xung quanh các EC2 instance của bạn, kiểm soát cách lưu lượng truy cập được phép vào và ra khỏi các instance.

### Đặc Điểm Chính

- **Chỉ Có Quy Tắc Cho Phép**: Nhóm bảo mật chỉ chứa các quy tắc cho phép - bạn chỉ định những gì được phép vào và ra
- **Tham Chiếu Linh Hoạt**: Quy tắc có thể tham chiếu đến địa chỉ IP hoặc các nhóm bảo mật khác
- **Kiểm Soát Hai Chiều**: Quản lý cả lưu lượng vào và ra

## Cách Hoạt Động Của Nhóm Bảo Mật

Khi bạn đang ở trên máy tính của mình (internet công cộng) và cố gắng truy cập vào một EC2 instance, nhóm bảo mật hoạt động như một tường lửa xung quanh instance đó. Nhóm bảo mật chứa các quy tắc xác định:

- **Lưu Lượng Vào (Inbound)**: Liệu lưu lượng từ bên ngoài có thể đến EC2 instance hay không
- **Lưu Lượng Ra (Outbound)**: Liệu EC2 instance có thể giao tiếp với internet hay không

## Các Thành Phần Của Nhóm Bảo Mật

Nhóm bảo mật điều chỉnh quyền truy cập thông qua nhiều cơ chế:

### Các Yếu Tố Kiểm Soát Truy Cập

1. **Truy Cập Cổng**: Kiểm soát cổng nào có thể truy cập được
2. **Dải Địa Chỉ IP**: Cho phép các dải địa chỉ IPv4 hoặc IPv6 cụ thể
3. **Mạng Vào**: Kiểm soát lưu lượng từ bên ngoài vào instance
4. **Mạng Ra**: Kiểm soát lưu lượng từ instance ra bên ngoài

### Cấu Trúc Quy Tắc Nhóm Bảo Mật

Mỗi quy tắc bao gồm:
- **Loại**: Loại lưu lượng
- **Giao Thức**: TCP, UDP, v.v.
- **Phạm Vi Cổng**: Cổng nào lưu lượng có thể sử dụng trên instance
- **Nguồn**: Dải địa chỉ IP (ví dụ: `0.0.0.0/0` có nghĩa là tất cả, `/32` có nghĩa là một IP cụ thể)

## Ví Dụ Về Luồng Lưu Lượng

Xem xét một EC2 instance với nhóm bảo mật chứa các quy tắc vào và ra:

### Lưu Lượng Vào
- **Máy Tính Được Ủy Quyền**: Nếu máy tính của bạn được ủy quyền trên cổng 22, lưu lượng sẽ đi qua đến EC2 instance
- **Máy Tính Không Được Ủy Quyền**: Máy tính từ các địa chỉ IP khác sẽ bị chặn bởi tường lửa, dẫn đến timeout

### Lưu Lượng Ra
- **Hành Vi Mặc Định**: Theo mặc định, EC2 instance cho phép tất cả lưu lượng ra
- **Kết Nối Do Instance Khởi Tạo**: EC2 instance có thể truy cập trang web và khởi tạo kết nối mà không bị hạn chế

## Các Khái Niệm Quan Trọng Về Nhóm Bảo Mật

### Gắn Kết Đa Instance
- Nhóm bảo mật có thể được gắn vào nhiều instance (không phải quan hệ một-một)
- Một instance có thể có nhiều nhóm bảo mật

### Phạm Vi Khu Vực
- Nhóm bảo mật bị khóa với một tổ hợp region/VPC cụ thể
- Chuyển đổi region hoặc VPC yêu cầu tạo nhóm bảo mật mới

### Bên Ngoài EC2
- Nhóm bảo mật tồn tại bên ngoài EC2 instance
- Lưu lượng bị chặn không bao giờ đến được EC2 instance

### Thực Hành Tốt Nhất
- **Nhóm Bảo Mật SSH Riêng Biệt**: Duy trì một nhóm bảo mật riêng cho truy cập SSH, vì đây là điều quan trọng nhất cần cấu hình đúng

## Khắc Phục Sự Cố Kết Nối

### Lỗi Timeout
- **Triệu Chứng**: Ứng dụng không thể truy cập được, kết nối bị treo
- **Nguyên Nhân**: Vấn đề về nhóm bảo mật - lưu lượng đang bị chặn

### Lỗi Connection Refused
- **Triệu Chứng**: Nhận được thông báo "connection refused" rõ ràng
- **Nguyên Nhân**: Nhóm bảo mật đã hoạt động (lưu lượng đi qua), nhưng bản thân ứng dụng có lỗi hoặc không chạy

### Hành Vi Mặc Định
- **Tất cả lưu lượng vào**: Bị chặn theo mặc định
- **Tất cả lưu lượng ra**: Được cho phép theo mặc định

## Tính Năng Nâng Cao: Tham Chiếu Nhóm Bảo Mật

Nhóm bảo mật có thể tham chiếu đến các nhóm bảo mật khác trong quy tắc của chúng, điều này đặc biệt hữu ích cho load balancer.

### Cách Thức Hoạt Động

Nếu một EC2 instance có Security Group 1 với các quy tắc vào cho phép:
- Security Group 1
- Security Group 2

Thì:
- Bất kỳ EC2 instance nào có Security Group 2 đều có thể kết nối trực tiếp với các instance có Security Group 1
- Bất kỳ EC2 instance nào có Security Group 1 đều có thể giao tiếp với các instance khác cũng có Security Group 1
- EC2 instance có Security Group 3 sẽ bị từ chối truy cập

### Lợi Ích
- Không cần quản lý địa chỉ IP
- Giao tiếp instance động và linh hoạt
- Mẫu phổ biến cho cấu hình load balancer

## Các Cổng Cần Nhớ

### SSH (Cổng 22)
- **Mục Đích**: Đăng nhập vào EC2 instance trên Linux
- **Giao Thức**: Secure Shell

### FTP (Cổng 21)
- **Mục Đích**: Tải file lên file share
- **Giao Thức**: File Transfer Protocol

### SFTP (Cổng 22)
- **Mục Đích**: Tải file an toàn bằng SSH
- **Giao Thức**: Secure File Transfer Protocol

### HTTP (Cổng 80)
- **Mục Đích**: Truy cập trang web không bảo mật
- **Định Dạng**: `http://địa-chỉ-website`

### HTTPS (Cổng 443)
- **Mục Đích**: Truy cập trang web bảo mật (tiêu chuẩn hiện đại)
- **Định Dạng**: `https://địa-chỉ-website`

### RDP (Cổng 3389)
- **Mục Đích**: Đăng nhập vào Windows instance
- **Giao Thức**: Remote Desktop Protocol

## Tóm Tắt

| Cổng | Giao Thức | Trường Hợp Sử Dụng | Hệ Điều Hành |
|------|-----------|-------------------|--------------|
| 22 | SSH | Đăng nhập vào Linux instance | Linux |
| 22 | SFTP | Truyền file an toàn | Linux |
| 21 | FTP | Truyền file | Bất kỳ |
| 80 | HTTP | Truy cập web không bảo mật | Bất kỳ |
| 443 | HTTPS | Truy cập web bảo mật | Bất kỳ |
| 3389 | RDP | Đăng nhập vào Windows instance | Windows |

Nhóm bảo mật là nền tảng của bảo mật mạng EC2. Hiểu cách chúng kiểm soát luồng lưu lượng, hành vi mặc định và cách khắc phục các sự cố thường gặp là điều cần thiết để làm việc hiệu quả với AWS EC2 instance.