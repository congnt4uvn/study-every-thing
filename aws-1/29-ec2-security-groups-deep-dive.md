# Tìm Hiểu Sâu Về EC2 Security Groups

## Tổng Quan

Sau khi khởi chạy một EC2 instance, điều quan trọng là phải hiểu cách hoạt động của security groups để kiểm soát quyền truy cập vào instance của bạn. Hướng dẫn này cung cấp một cách thực hành về EC2 security groups, các quy tắc inbound/outbound và khắc phục các vấn đề kết nối phổ biến.

## Truy Cập Security Groups

Có hai cách để xem security groups cho EC2 instance của bạn:

1. **Xem Nhanh**: Nhấp vào tab "Security" trong trang chi tiết EC2 instance
   - Hiển thị tổng quan về các security groups được gắn kèm
   - Hiển thị các quy tắc inbound và outbound

2. **Xem Đầy Đủ**: Điều hướng đến trang Security Groups chuyên dụng
   - Vào menu bên trái
   - Trong mục "Networking and Security", nhấp "Security Groups"

## Hiểu Về Security Groups

### Khái Niệm Cơ Bản Về Security Group

Khi bạn tạo EC2 instance đầu tiên, bạn sẽ thấy ít nhất hai security groups trong console:

- **Default Security Group**: Được AWS tạo tự động
- **Launch Wizard Security Group**: Được tạo khi bạn khởi chạy EC2 instance đầu tiên (ví dụ: "launch-wizard-1")

Mỗi security group có một **Security Group ID** duy nhất, tương tự như cách EC2 instances có instance IDs.

### Quy Tắc Inbound

Quy tắc inbound kiểm soát kết nối **từ bên ngoài vào EC2 instance của bạn**.

#### Ví Dụ Cấu Hình Ban Đầu

Khi khởi chạy một EC2 instance, thông thường bạn có hai quy tắc inbound:

1. **Quy Tắc SSH**
   - Loại: SSH
   - Cổng: 22
   - Nguồn: 0.0.0.0/0 (bất kỳ đâu)

2. **Quy Tắc HTTP**
   - Loại: HTTP
   - Cổng: 80
   - Nguồn: 0.0.0.0/0 (bất kỳ đâu)

Quy tắc HTTP trên cổng 80 là điều cho phép bạn truy cập web server thông qua địa chỉ IPv4 công khai của instance qua trình duyệt.

## Thực Hành: Kiểm Tra Quy Tắc Security Group

### Xóa Quyền Truy Cập HTTP

Để hiểu cách hoạt động của security groups, hãy thực hiện một bài kiểm tra:

1. Chỉnh sửa các quy tắc inbound và **xóa quy tắc HTTP (cổng 80)**
2. Lưu các thay đổi
3. Thử truy cập EC2 instance của bạn qua HTTP trong trình duyệt

**Kết quả**: Trang sẽ hiển thị màn hình tải vô hạn và cuối cùng sẽ timeout. Điều này chứng minh rằng nếu không có quy tắc security group thích hợp, bạn không thể truy cập instance.

### Mẹo Khắc Phục Sự Cố Quan Trọng

**Nếu bạn gặp phải timeout khi kết nối với EC2 instance**, nguyên nhân **100% liên quan đến cấu hình security group**.

Các tình huống timeout phổ biến:
- Kết nối SSH timeout
- Yêu cầu HTTP/HTTPS timeout
- Bất kỳ nỗ lực kết nối nào khác timeout

**Giải pháp**: Kiểm tra các quy tắc security group của bạn và đảm bảo chúng được cấu hình đúng cho loại truy cập bạn cần.

### Khôi Phục Quyền Truy Cập HTTP

Để khắc phục vấn đề timeout:

1. Thêm lại quy tắc inbound HTTP
2. Chọn HTTP từ menu thả xuống loại (tự động đặt cổng 80)
3. Đặt nguồn thành 0.0.0.0/0 (bất kỳ đâu IPv4)
4. Lưu quy tắc

Sau khi thêm lại quy tắc, làm mới trình duyệt của bạn và trang web sẽ tải thành công.

## Cấu Hình Quy Tắc Inbound Tùy Chỉnh

Bạn có sự linh hoạt trong việc tạo các quy tắc inbound:

### Cấu Hình Cổng

- Xác định các cổng cụ thể (ví dụ: cổng 443 cho HTTPS)
- Xác định phạm vi cổng
- Sử dụng menu thả xuống loại cho các giao thức phổ biến:
  - HTTP → Cổng 80
  - HTTPS → Cổng 443
  - SSH → Cổng 22
  - Và nhiều hơn nữa...

### Cấu Hình Nguồn

Bạn có thể chỉ định nguồn lưu lượng được phép:

1. **CIDR Blocks**
   - Ký hiệu CIDR block tùy chỉnh
   - `0.0.0.0/0` = Bất kỳ đâu (tất cả địa chỉ IPv4)

2. **My IP**
   - Hạn chế truy cập chỉ cho địa chỉ IP hiện tại của bạn
   - **Cảnh báo**: Nếu địa chỉ IP của bạn thay đổi, bạn sẽ gặp timeout và mất quyền truy cập vào instance

3. **Security Groups** (sẽ được đề cập sau trong khóa học)

4. **Prefix Lists** (sẽ được đề cập sau trong khóa học)

## Quy Tắc Outbound

Quy tắc outbound kiểm soát lưu lượng **từ EC2 instance của bạn ra bên ngoài**.

### Cấu Hình Mặc Định

Theo mặc định, security groups cho phép:
- Tất cả lưu lượng trên tất cả các cổng
- Đến bất kỳ đích nào (0.0.0.0/0)
- Giao thức: Tất cả

Cấu hình này cung cấp cho EC2 instance của bạn kết nối internet đầy đủ.

## Các Khái Niệm Nâng Cao Về Security Group

### Nhiều Security Groups Trên Một Instance

Một EC2 instance có thể có nhiều security groups được gắn kèm:
- Bạn có thể gắn 1, 2, 3, 5 hoặc nhiều security groups vào một instance
- Các quy tắc từ tất cả các security groups được gắn kèm sẽ được kết hợp
- Các quy tắc có tính tích lũy (chúng cộng lại với nhau)

### Tái Sử Dụng Security Groups

Security groups là tài nguyên có thể tái sử dụng:
- Một security group (ví dụ: "launch-wizard-1") có thể được gắn vào nhiều EC2 instances
- Điều này thúc đẩy tính nhất quán và quản lý dễ dàng hơn trong cơ sở hạ tầng của bạn

### Tóm Tắt Về Tính Linh Hoạt

- **Nhiều security groups** → Một EC2 instance
- **Một security group** → Nhiều EC2 instances
- Kết hợp theo nhu cầu cho kiến trúc của bạn

## Điểm Chính Cần Nhớ

1. Security groups hoạt động như tường lửa ảo cho EC2 instances của bạn
2. Quy tắc inbound kiểm soát lưu lượng đến, quy tắc outbound kiểm soát lưu lượng đi
3. **Lỗi timeout = Cấu hình sai security group** (100% trường hợp)
4. Security groups có trạng thái (lưu lượng trả về được tự động cho phép)
5. Nhiều security groups có thể được gắn vào một instance
6. Security groups có thể được tái sử dụng trên nhiều instances
7. Luôn xác minh các quy tắc security group khi khắc phục sự cố kết nối

## Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ khám phá các cấu hình security group nâng cao hơn và các phương pháp tốt nhất để bảo mật cơ sở hạ tầng AWS của bạn.