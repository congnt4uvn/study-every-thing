# Khả Năng Mở Rộng và Tính Sẵn Sàng Cao trên AWS

## Giới Thiệu

Bài học này trình bày các khái niệm cơ bản về khả năng mở rộng (scalability) và tính sẵn sàng cao (high availability) trên AWS. Những khái niệm này rất quan trọng để hiểu cách xây dựng các ứng dụng đám mây mạnh mẽ và linh hoạt.

## Khả Năng Mở Rộng là gì?

Khả năng mở rộng có nghĩa là ứng dụng hoặc hệ thống của bạn có thể xử lý tải lớn hơn bằng cách thích ứng. Có hai loại khả năng mở rộng chính:

1. **Mở Rộng Theo Chiều Dọc** (Vertical Scalability)
2. **Mở Rộng Theo Chiều Ngang** (Horizontal Scalability) - còn gọi là Elasticity

> **Lưu ý:** Khả năng mở rộng khác với tính sẵn sàng cao - chúng có liên quan nhưng là các khái niệm khác biệt.

## Mở Rộng Theo Chiều Dọc (Vertical Scalability)

### Định Nghĩa

Mở rộng theo chiều dọc có nghĩa là tăng kích thước của instance.

### Ví Dụ Trung Tâm Cuộc Gọi

Hãy nghĩ về một nhân viên điện thoại trong trung tâm cuộc gọi:
- **Nhân viên cấp Junior**: Có thể xử lý 5 cuộc gọi mỗi phút
- **Nhân viên cấp Senior**: Có thể xử lý 10 cuộc gọi mỗi phút

Khi bạn thăng cấp nhân viên junior lên senior, bạn đã mở rộng năng lực của họ. Đây là mở rộng theo chiều dọc - đi lên phía trên!

### Ví Dụ EC2

- Ứng dụng của bạn chạy trên instance `t2.micro`
- Để nâng cấp, bạn chuyển sang instance `t2.large`

### Khi Nào Sử Dụng Mở Rộng Theo Chiều Dọc

Mở rộng theo chiều dọc rất phổ biến cho **các hệ thống không phân tán**, chẳng hạn như:
- Cơ sở dữ liệu (Database)
- Amazon RDS
- Amazon ElastiCache

Bạn có thể mở rộng các dịch vụ này theo chiều dọc bằng cách nâng cấp loại instance cơ bản.

### Giới Hạn

Thường có giới hạn về mức độ mở rộng theo chiều dọc do ràng buộc phần cứng. Tuy nhiên, mở rộng theo chiều dọc phù hợp với nhiều trường hợp sử dụng.

## Mở Rộng Theo Chiều Ngang (Horizontal Scalability)

### Định Nghĩa

Mở rộng theo chiều ngang có nghĩa là tăng số lượng instance hoặc hệ thống cho ứng dụng của bạn.

### Ví Dụ Trung Tâm Cuộc Gọi

Bắt đầu với một nhân viên bị quá tải:
1. Thuê nhân viên thứ hai → tăng gấp đôi năng lực
2. Thuê nhân viên thứ ba → tăng gấp ba năng lực
3. Thuê sáu nhân viên → năng lực tăng 6 lần

Đây là mở rộng theo chiều ngang - mở rộng ra bên ngoài!

### Đặc Điểm Chính

- Ngụ ý **hệ thống phân tán** (distributed systems)
- Phổ biến cho các ứng dụng web và ứng dụng hiện đại
- **Lưu ý:** Không phải mọi ứng dụng đều có thể là hệ thống phân tán

### Lợi Thế Đám Mây

Mở rộng theo chiều ngang rất dễ dàng với các dịch vụ đám mây như Amazon EC2. Bạn chỉ cần khởi chạy instance mới bằng vài cú nhấp chuột, và ứng dụng của bạn đã được mở rộng theo chiều ngang.

## Tính Sẵn Sàng Cao (High Availability)

### Định Nghĩa

Tính sẵn sàng cao có nghĩa là chạy ứng dụng hoặc hệ thống của bạn trong ít nhất hai trung tâm dữ liệu hoặc vùng khả dụng (availability zones - AZs) trên AWS.

### Mục Tiêu

Mục tiêu của tính sẵn sàng cao là có thể tồn tại khi mất một trung tâm dữ liệu. Nếu một trung tâm ngừng hoạt động, hệ thống vẫn tiếp tục chạy.

### Ví Dụ Trung Tâm Cuộc Gọi

- **Tòa nhà 1 (New York)**: 3 nhân viên điện thoại
- **Tòa nhà 2 (San Francisco)**: 3 nhân viên điện thoại

Nếu tòa nhà New York mất kết nối internet hoặc kết nối cuộc gọi, tòa nhà San Francisco vẫn có thể nhận cuộc gọi. Trung tâm cuộc gọi vẫn sẵn sàng cao.

### Các Loại Tính Sẵn Sàng Cao

1. **Tính Sẵn Sàng Cao Thụ Động** (Passive High Availability)
   - Ví dụ: RDS Multi-AZ
   - Các hệ thống dự phòng sẵn sàng tiếp quản

2. **Tính Sẵn Sàng Cao Chủ Động** (Active High Availability)
   - Xảy ra với mở rộng theo chiều ngang
   - Tất cả các hệ thống đều xử lý yêu cầu đồng thời
   - Ví dụ: Nhiều tòa nhà cùng nhận cuộc gọi cùng một lúc

## Khả Năng Mở Rộng và Tính Sẵn Sàng Cao trên EC2

### Mở Rộng Theo Chiều Dọc

- **Scale Up/Down**: Tăng hoặc giảm kích thước instance
- **Phạm Vi**: 
  - Nhỏ nhất: `t2.nano` (0.5 GB RAM, 1 vCPU)
  - Lớn nhất: `u-12tb1.metal` (12.3 TB RAM, 450 vCPU)
- Bạn có thể mở rộng từ instance rất nhỏ đến cực kỳ lớn

### Mở Rộng Theo Chiều Ngang

- **Scale Out**: Tăng số lượng instance
- **Scale In**: Giảm số lượng instance
- **Trường Hợp Sử Dụng**:
  - Auto Scaling Groups (Nhóm Tự Động Mở Rộng)
  - Load Balancers (Bộ Cân Bằng Tải)

### Tính Sẵn Sàng Cao

- Chạy cùng một instance ứng dụng trên nhiều AZ
- **Triển Khai**:
  - Auto Scaling Group với multi-AZ được bật
  - Load Balancer với multi-AZ được bật

## Tóm Tắt

Hiểu về khả năng mở rộng và tính sẵn sàng cao là rất quan trọng cho các chứng chỉ AWS và ứng dụng thực tế:

- **Mở Rộng Theo Chiều Dọc**: Tăng kích thước instance (scale up/down)
- **Mở Rộng Theo Chiều Ngang**: Tăng số lượng instance (scale out/in)
- **Tính Sẵn Sàng Cao**: Chạy trên nhiều trung tâm dữ liệu/AZ

### Điểm Chính Cần Nhớ

Hãy nhớ **ví dụ về trung tâm cuộc gọi** khi suy nghĩ về các khái niệm này:
- Mở rộng theo chiều dọc = Đào tạo nhân viên xử lý nhiều cuộc gọi hơn
- Mở rộng theo chiều ngang = Thuê thêm nhiều nhân viên
- Tính sẵn sàng cao = Có nhân viên ở nhiều tòa nhà

Những khái niệm này là nền tảng và có thể xuất hiện trong các câu hỏi thi, vì vậy hãy đảm bảo bạn hiểu rõ chúng!