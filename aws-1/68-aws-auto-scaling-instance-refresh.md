# AWS Auto Scaling Group - Instance Refresh

## Tổng Quan

Instance Refresh là một tính năng gốc của AWS Auto Scaling groups cho phép bạn cập nhật toàn bộ Auto Scaling group với một launch template mới bằng cách thay thế có hệ thống tất cả các EC2 instances.

## Instance Refresh Là Gì?

Instance Refresh là một tính năng tiện lợi giúp bạn cập nhật Auto Scaling group khi bạn đã tạo một launch template mới. Thay vì phải thủ công terminate từng instance một và chờ đợi chúng khởi động lại, bạn có thể sử dụng tính năng tự động có sẵn này.

## Cách Hoạt Động

### Thiết Lập Ban Đầu

Xem xét kịch bản sau:
- Bạn có một Auto Scaling group với các EC2 instances được khởi chạy bằng launch template cũ
- Bạn tạo một launch template mới (ví dụ: với AMI đã được cập nhật)
- Bạn muốn thay thế tất cả các instances hiện tại bằng các instances mới sử dụng template đã cập nhật

### Quy Trình

1. **Khởi Động Refresh**: Gọi API `Start Instance Refresh`
2. **Đặt Minimum Healthy Percentage**: Xác định bao nhiêu instances phải duy trì trạng thái khỏe mạnh trong quá trình refresh (ví dụ: 60%)
3. **Thay Thế Dần Dần**: 
   - Các instances được terminate dần dần
   - Các instances mới được khởi chạy với launch template mới
   - Quá trình tiếp tục cho đến khi tất cả instances cũ được thay thế

### Các Tham Số Chính

#### Minimum Healthy Percentage (Phần Trăm Khỏe Mạnh Tối Thiểu)
- Xác định có bao nhiêu instances có thể bị xóa theo thời gian
- Ví dụ: Đặt 60% có nghĩa là ít nhất 60% công suất của bạn phải duy trì trạng thái khỏe mạnh trong quá trình refresh
- Điều này kiểm soát tốc độ thay thế instances

#### Warm-up Time (Thời Gian Khởi Động)
- Chỉ định thời gian chờ đợi cho đến khi một EC2 instance mới được coi là sẵn sàng sử dụng
- Đảm bảo các instances có đủ thời gian để được khởi tạo đầy đủ và sẵn sàng phục vụ traffic
- Giúp ngăn chặn việc gán instance quá sớm

## Lợi Ích

- **Quy Trình Tự Động**: Không cần can thiệp thủ công để thay thế instances
- **Không Downtime**: Duy trì phần trăm khỏe mạnh tối thiểu trong suốt quá trình refresh
- **Cập Nhật An Toàn**: Triển khai dần dần đảm bảo tính khả dụng của dịch vụ
- **Kiểm Soát Linh Hoạt**: Cấu hình tốc độ và thời gian thay thế instances

## Các Trường Hợp Sử Dụng

- Cập nhật AMI (Amazon Machine Image) cho các instances của bạn
- Áp dụng cấu hình launch template mới
- Triển khai các phiên bản ứng dụng đã cập nhật
- Triển khai các bản vá bảo mật trên tất cả instances

## Tóm Tắt

Instance Refresh là một cách hiệu quả để cập nhật toàn bộ Auto Scaling group của bạn mà không cần quản lý instances thủ công. Bằng cách đặt phần trăm khỏe mạnh tối thiểu và thời gian warm-up phù hợp, bạn có thể đảm bảo quá trình chuyển đổi suôn sẻ từ instances cũ sang instances mới trong khi vẫn duy trì tính khả dụng của dịch vụ.