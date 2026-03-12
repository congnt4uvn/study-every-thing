# AWS Route 53 - Hướng Dẫn Đăng Ký Tên Miền

## Giới Thiệu

Trong hướng dẫn này, chúng ta sẽ tìm hiểu quy trình đăng ký tên miền sử dụng Amazon Route 53, dịch vụ hệ thống tên miền (DNS) có khả năng mở rộng của AWS.

## Yêu Cầu Trước Khi Bắt Đầu

Trước khi bắt đầu, bạn cần:
- Có tài khoản AWS
- Sẵn sàng chi trả khoảng $12-13 mỗi năm cho việc đăng ký tên miền
- Có thông tin liên hệ hợp lệ để đăng ký tên miền

## Bắt Đầu Với Route 53

Khi lần đầu truy cập Route 53, bạn sẽ thấy:
- Không có hosted zone nào (nếu đây là lần đầu tiên)
- Không có tên miền đã đăng ký

Giao diện có thể hiển thị phiên bản console mới, đây là phiên bản được khuyến nghị sử dụng.

## Quy Trình Đăng Ký Tên Miền Từng Bước

### Bước 1: Truy Cập Phần Đăng Ký Tên Miền

1. Điều hướng đến bảng điều khiển Route 53
2. Ở phía bên trái, nhấp vào **"Register domains"** (Đăng ký tên miền)
3. Bạn sẽ thấy giao diện console phiên bản mới

### Bước 2: Chọn Tên Miền

1. Nhập tên miền mong muốn vào ô tìm kiếm
2. Đảm bảo đó là tên duy nhất chưa được ai đăng ký
3. Kiểm tra tính khả dụng - hệ thống sẽ hiển thị nếu tên miền còn trống
4. Xem lại giá (thường khoảng $13 USD mỗi năm)
5. Thêm tên miền vào giỏ hàng
6. Nhấp **"Proceed to checkout"** (Tiến hành thanh toán)

### Bước 3: Cấu Hình Thiết Lập Tên Miền

**Thiết Lập Thời Hạn:**
- Chọn thời hạn đăng ký (ví dụ: 1 năm)
- Cấu hình thiết lập tự động gia hạn:
  - **Bật tự động gia hạn**: Được khuyến nghị nếu bạn có kế hoạch giữ tên miền lâu dài
  - **Tắt tự động gia hạn**: Nếu bạn chỉ cần tên miền tạm thời (ví dụ: cho một khóa học)
  
> **Cảnh báo**: Nếu bạn tắt tự động gia hạn và quên gia hạn, người khác có thể mua tên miền của bạn sau khi nó hết hạn.

### Bước 4: Nhập Thông Tin Liên Hệ

1. Điền hoặc xác minh thông tin liên hệ được điền sẵn
2. Thông tin liên hệ quản trị và kỹ thuật có thể được đặt giống với người đăng ký
3. **Quan trọng**: Bật bảo vệ quyền riêng tư để:
   - Ngăn chặn thư rác
   - Ẩn thông tin cá nhân của bạn (địa chỉ, số điện thoại, v.v.) khỏi cơ sở dữ liệu WHOIS công khai

### Bước 5: Xem Lại và Gửi

1. Xem lại tất cả thông tin cẩn thận
2. Đọc và chấp nhận các điều khoản và điều kiện
3. Nhấp **"Submit"** (Gửi)

> **Quan trọng**: Việc gửi sẽ tính phí đăng ký (khoảng $13). Chỉ tiếp tục nếu bạn sẵn sàng thanh toán.

### Bước 6: Chờ Hoàn Tất Đăng Ký

- Việc đăng ký tên miền thường mất vài phút đến vài giờ
- Bạn sẽ nhận được xác nhận khi quy trình hoàn tất

## Xác Minh Đăng Ký Tên Miền

### Truy Cập Hosted Zones

1. Trong Route 53, điều hướng đến **"Hosted zones"** ở phía bên trái
2. Nhấp vào tên miền mới đăng ký của bạn (ví dụ: stefanetheteacher.com)

### Các Bản Ghi DNS Mặc Định

Bạn sẽ thấy ít nhất hai bản ghi mặc định:

1. **Bản Ghi NS (Name Server)**
   - Chỉ ra rằng AWS DNS nên được sử dụng cho các truy vấn DNS
   - Trỏ đến Route 53 làm dịch vụ DNS của bạn

2. **Bản Ghi SOA (Start of Authority)**
   - Chứa thông tin quản trị về vùng

## Hiểu Về Route 53 Là Nguồn DNS Chính Thức

Với hosted zone đã được cấu hình:
- Route 53 trở thành nguồn chính thức cho tất cả các bản ghi DNS trong tên miền của bạn
- Bất kỳ bản ghi DNS nào bạn tạo sẽ được quản lý bởi Route 53
- Bạn có thể thêm, sửa đổi hoặc xóa các bản ghi DNS theo nhu cầu

## Xem Xét Chi Phí

- Đăng ký tên miền: Khoảng $12-13 USD mỗi năm (tùy thuộc vào phần mở rộng tên miền)
- Hosted zone: $0.50 mỗi tháng cho mỗi hosted zone
- Truy vấn DNS: Định giá theo mức sử dụng

> **Lưu ý**: Nếu bạn không muốn trả phí đăng ký tên miền, bạn có thể bỏ qua phần thực hành và chỉ theo dõi nội dung video.

## Các Bước Tiếp Theo

Bây giờ bạn đã có tên miền đã đăng ký và hosted zone, bạn đã sẵn sàng để:
- Tạo các bản ghi DNS (được đề cập trong bài giảng tiếp theo)
- Cấu hình các chính sách định tuyến
- Thiết lập kiểm tra sức khỏe
- Triển khai các cấu hình DNS nâng cao

## Tóm Tắt

Bạn đã học thành công cách:
- Điều hướng bảng điều khiển Route 53
- Đăng ký tên miền mới
- Cấu hình thiết lập tên miền và thông tin liên hệ
- Hiểu những điều cơ bản về hosted zones và bản ghi DNS
- Xác minh đăng ký tên miền của bạn

Trong bài giảng tiếp theo, chúng ta sẽ khám phá cách tạo và quản lý các bản ghi DNS trong hosted zone của bạn.