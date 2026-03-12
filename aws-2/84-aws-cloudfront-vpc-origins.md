# AWS CloudFront VPC Origins

## Tổng quan

Tài liệu này giải thích cách kết nối CloudFront với application load balancer hoặc EC2 instance làm origin, bao gồm cả phương pháp hiện đại sử dụng VPC origins và phương pháp cũ sử dụng mạng công khai.

## Phương pháp hiện đại: VPC Origins

### VPC Origins là gì?

VPC Origins là cách **tốt hơn và mới hơn** để kết nối CloudFront với các ứng dụng backend của bạn. Tính năng này cho phép bạn:

- Phân phối nội dung trực tiếp từ các ứng dụng được lưu trữ trong **private subnet** bên trong VPC của bạn
- Giữ mọi thứ ở chế độ riêng tư mà không cần phơi bày tài nguyên ra internet
- Phân phối traffic đến:
  - Private Application Load Balancers (ALB)
  - Network Load Balancers (NLB)
  - EC2 instances

### Cách hoạt động của VPC Origins

1. Tạo một **CloudFront distribution** với nhiều edge location
2. Người dùng truy cập CloudFront thông qua các edge location này
3. Tạo một **VPC origin** trong CloudFront
4. Kết nối VPC origin với backend của bạn (ALB, NLB, hoặc EC2 instance)
5. CloudFront định tuyến traffic thông qua VPC origin đến private subnet và ứng dụng của bạn

### Lợi ích về bảo mật

Từ góc độ mạng, VPC Origins cung cấp **một trong những thiết lập bảo mật nhất** bởi vì:

- Ứng dụng vẫn được lưu trữ riêng tư và nội bộ
- Bạn kiểm soát chính xác những gì được phơi bày thông qua CloudFront
- Không cần phơi bày ra internet công cộng

## Phương pháp cũ: Public Network (Trước VPC Origins)

### Tổng quan

Trước khi VPC Origins ra đời, bạn phải sử dụng mạng công khai để kết nối CloudFront với origin của mình. Mặc dù vẫn hoạt động, phương pháp này phức tạp hơn và kém bảo mật hơn.

### Phương pháp Public EC2 Instance

**Yêu cầu:**
- EC2 instance phải là **public**
- Lấy danh sách các IP công khai của CloudFront edge location
- Cấu hình security group để chỉ cho phép IP của CloudFront

**Quy trình:**
1. Tìm danh sách tất cả các địa chỉ IP của CloudFront
2. Cập nhật security group của EC2 instance
3. Chỉ cho phép các IP công khai của CloudFront truy cập instance của bạn
4. Instance trở thành public nhưng chỉ giới hạn cho các edge location

### Phương pháp Public Application Load Balancer

**Kiến trúc:**
- ALB phải là **public**
- EC2 instance đằng sau ALB có thể vẫn là **private**
- Mạng riêng tư giữa ALB và EC2 instance được bảo mật bằng security group

**Quy trình:**
1. Đảm bảo ALB có thể truy cập công khai
2. Giữ các EC2 instance trong private subnet
3. Cấu hình security group để cho phép giao tiếp riêng tư giữa ALB và EC2
4. Cập nhật security group của ALB để cho phép tất cả IP công khai của CloudFront

### Nhược điểm của phương pháp cũ

1. **Cấu hình phức tạp:**
   - Phải tìm và duy trì thủ công các IP công khai của CloudFront
   - Cần cập nhật security group

2. **Rủi ro bảo mật:**
   - Nếu ai đó thay đổi security group của ALB hoặc EC2 instance của bạn
   - Tài nguyên của bạn trở thành public với nhiều hơn chỉ CloudFront
   - Tăng bề mặt tấn công

3. **Chi phí bảo trì:**
   - Các dải IP của CloudFront có thể thay đổi
   - Yêu cầu giám sát và cập nhật liên tục

## Khuyến nghị

**Sử dụng VPC Origins** cho tất cả các triển khai mới. Phương pháp hiện đại này cung cấp:
- ✅ Tư thế bảo mật tốt hơn
- ✅ Cấu hình đơn giản hơn
- ✅ Kiến trúc mạng riêng tư
- ✅ Giảm chi phí bảo trì

Phương pháp mạng công khai cũ chỉ nên được xem xét cho các triển khai hiện có chưa được di chuyển.

---

*Hướng dẫn này dựa trên các phương pháp hay nhất và khuyến nghị bảo mật của AWS CloudFront.*