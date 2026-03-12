# Kết Nối Đến EC2 Instances: Tổng Quan Về SSH

## Giới Thiệu

Một trong những phần khó khăn khi vận hành trên Cloud là hiểu cách kết nối vào bên trong máy chủ của bạn để thực hiện bảo trì hoặc các hành động khác. Đối với máy chủ Linux, chúng ta sử dụng SSH (Secure Shell) để kết nối an toàn đến các instances.

## Các Phương Thức Kết Nối Theo Hệ Điều Hành

Phương thức bạn sử dụng phụ thuộc vào hệ điều hành của bạn:

### Mac và Linux
- **SSH Command Line Interface**: Tiện ích tích hợp sẵn trên hệ thống Mac và Linux
- Cũng có sẵn trên Windows 10 và các phiên bản mới hơn

### Windows (Trước Phiên Bản 10)
- **PuTTY**: Một ứng dụng SSH client dành riêng cho Windows
- Cung cấp chức năng tương tự như SSH
- Tương thích với mọi phiên bản Windows

### Tất Cả Các Nền Tảng
- **EC2 Instance Connect**: Phương thức kết nối dựa trên trình duyệt web
- Hoạt động trên Mac, Linux và mọi phiên bản Windows
- Không cần cài đặt
- Hiện tại hỗ trợ các instances Amazon Linux 2

## Bạn Nên Sử Dụng Phương Thức Nào?

### Cho Người Dùng Mac hoặc Linux
Xem bài giảng SSH trên Mac/Linux để học cách sử dụng tiện ích SSH tích hợp sẵn.

### Cho Người Dùng Windows
Bạn có nhiều lựa chọn:
- **Windows 10 trở lên**: Sử dụng tiện ích SSH tích hợp sẵn (xem bài giảng SSH trên Windows 10)
- **Bất kỳ phiên bản Windows nào**: Sử dụng PuTTY (xem bài giảng PuTTY)

### Khuyến Nghị Cho Tất Cả Người Dùng
**EC2 Instance Connect** được khuyến nghị cao vì:
- Đơn giản và thân thiện với người dùng
- Không cần cài đặt
- Hoạt động thông qua trình duyệt web
- Không cần kiến thức về dòng lệnh
- Tương thích với mọi hệ điều hành

## Khắc Phục Sự Cố

Kết nối SSH là một trong những thách thức phổ biến nhất mà học viên gặp phải trong khóa học này. Nếu bạn gặp vấn đề:

1. **Xem lại bài giảng** - Bạn có thể đã bỏ lỡ một bước quan trọng
2. **Kiểm tra các vấn đề thường gặp**:
   - Quy tắc security group
   - Cú pháp lệnh
   - Lỗi chính tả trong thông tin kết nối
3. **Xem hướng dẫn khắc phục sự cố** được cung cấp sau các bài giảng này
4. **Thử EC2 Instance Connect** - Phương pháp này thường giải quyết được các vấn đề kết nối

## Lưu Ý Quan Trọng

- **Bạn chỉ cần MỘT phương thức hoạt động** - Nếu một phương thức kết nối hoạt động, bạn đã sẵn sàng
- **Đừng lo lắng nếu SSH không hoạt động** - Đây là khóa học giới thiệu và việc sử dụng SSH là tối thiểu
- **Hạn chế của EC2 Instance Connect** - Hiện tại chỉ hoạt động với Amazon Linux 2 (đây là lý do chúng ta sử dụng nó trong hướng dẫn này)

## Các Bước Tiếp Theo

Tìm bài giảng phù hợp với hệ điều hành và phương thức kết nối bạn ưa thích, và hẹn gặp lại bạn trong bài giảng tiếp theo!