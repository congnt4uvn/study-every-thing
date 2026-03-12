# Tổng quan về AWS Gateway Load Balancer

## Giới thiệu

**Gateway Load Balancer (GWLB)** là loại load balancer mới nhất trong AWS, được thiết kế để triển khai, mở rộng và quản lý các thiết bị mạng ảo của bên thứ ba trong AWS.

## Các trường hợp sử dụng

Bạn nên sử dụng Gateway Load Balancer khi cần:

- **Bảo vệ Tường lửa**: Định tuyến toàn bộ lưu lượng mạng qua các thiết bị tường lửa của bạn
- **Hệ thống Phát hiện và Ngăn chặn Xâm nhập (IDPS)**: Kiểm tra lưu lượng để phát hiện các mối đe dọa bảo mật
- **Kiểm tra Gói tin Sâu**: Phân tích nội dung gói tin ở cấp độ mạng
- **Sửa đổi Payload**: Điều chỉnh payload mạng ở tầng mạng

## Cách hoạt động

### Kiến trúc Truyền thống
Trước đây, người dùng có thể truy cập ứng dụng trực tiếp thông qua load balancer (như Application Load Balancer), với luồng lưu lượng: Người dùng → ALB → Ứng dụng.

### Kiến trúc Gateway Load Balancer

Với Gateway Load Balancer, luồng lưu lượng trở thành:

1. **Lưu lượng Người dùng** → Gateway Load Balancer
2. **GWLB** → Thiết bị Ảo Bên thứ ba (Target Group)
3. **Thiết bị Ảo** phân tích lưu lượng:
   - Nếu được phê duyệt → Lưu lượng quay lại GWLB
   - Nếu bị từ chối → Lưu lượng bị loại bỏ
4. **GWLB** → Ứng dụng (nếu lưu lượng được phê duyệt)

### Chi tiết Triển khai Chính

- **Sửa đổi Route Table**: GWLB cập nhật các route table của VPC ở hậu trường
- **Trong suốt với Ứng dụng**: Ứng dụng không biết lưu lượng đã được kiểm tra
- **Điểm Vào/Ra Duy nhất**: Toàn bộ lưu lượng VPC đi qua GWLB

## Thông số Kỹ thuật

### Tầng Mạng
- **Hoạt động ở Layer 3**: Tầng mạng (IP packets)
- **Giao thức**: Sử dụng giao thức GENEVE trên cổng 6081

### Hai Chức năng Chính
1. **Cổng Mạng Trong suốt**: Điểm vào và ra duy nhất cho toàn bộ lưu lượng VPC
2. **Load Balancer**: Phân phối lưu lượng trên các thiết bị ảo trong target group

## Target Groups (Nhóm Đích)

Gateway Load Balancer hỗ trợ các loại target sau:

### EC2 Instances
- Đăng ký theo Instance ID
- Thiết bị ảo chạy trên AWS EC2

### Địa chỉ IP
- Phải là địa chỉ IP private
- Hữu ích cho các thiết bị ảo chạy trên:
  - Mạng riêng của bạn
  - Data center tại chỗ (on-premises)
  - Yêu cầu đăng ký IP thủ công

## Điểm Chính Cần Nhớ

- **Hoạt động Layer 3**: Làm việc ở tầng mạng với các gói tin IP
- **Thiết bị Bên thứ ba**: Được thiết kế cho các thiết bị kiểm tra và bảo mật mạng
- **Giao thức GENEVE**: Sử dụng cổng 6081 (mẹo thi)
- **Tích hợp Trong suốt**: Ứng dụng không nhận biết việc kiểm tra lưu lượng
- **Đăng ký Target Linh hoạt**: Hỗ trợ EC2 instances và địa chỉ IP private

## Kết luận

Gateway Load Balancer đơn giản hóa quy trình phức tạp trước đây của việc định tuyến lưu lượng qua các thiết bị mạng bên thứ ba. Nó cung cấp một giải pháp tập trung, có khả năng mở rộng cho bảo mật mạng và kiểm tra lưu lượng trong môi trường AWS.

---

*Lưu ý: Việc triển khai thực hành Gateway Load Balancer khá phức tạp và thường yêu cầu kiến thức mạng nâng cao cùng với cấu hình thiết bị bên thứ ba phù hợp.*