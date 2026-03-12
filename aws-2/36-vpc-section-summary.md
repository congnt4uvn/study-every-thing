# Tóm Tắt Phần VPC

## Tổng Quan

Phần này cung cấp tóm tắt toàn diện về các khái niệm AWS Virtual Private Cloud (VPC). Mặc dù đây là phần nặng về lý thuyết không có bài tập thực hành, các khái niệm chính được đề cập ở đây rất cần thiết để hiểu các nguyên tắc cơ bản về mạng AWS.

## Các Khái Niệm VPC Chính

### VPC (Virtual Private Cloud)

- **VPC** là viết tắt của Virtual Private Cloud (Đám mây riêng ảo)
- Chúng ta đã sử dụng VPC mặc định trong suốt khóa học này khi tạo các EC2 instance
- Có **một VPC mặc định cho mỗi AWS region**

### Subnets (Mạng con)

- Subnet được **gắn với các Availability Zone cụ thể**
- Đây là nơi chúng ta khởi chạy các EC2 instance
- Chúng đại diện cho **phân vùng mạng của VPC**

### Internet Gateway (Cổng Internet)

- Cung cấp quyền truy cập internet cho các instance trong **public subnet**
- Được định nghĩa ở **cấp độ VPC**

### NAT Gateway và NAT Instance

- Cung cấp quyền truy cập internet cho **private subnet**
- Cho phép các EC2 instance trong private subnet truy cập internet

## Bảo Mật Mạng

### Network ACL (NACL)

- Tường lửa cấp subnet **không trạng thái (stateless)**
- Kiểm soát lưu lượng **đến và đi**
- Áp dụng quy tắc cho toàn bộ subnet

### Security Group (Nhóm Bảo Mật)

- Tường lửa **có trạng thái (stateful)**
- Hoạt động ở **cấp độ EC2 instance** hoặc ENI (Elastic Network Interface)
- Có thể **tham chiếu đến các security group khác**

## Kết Nối VPC

### VPC Peering (Kết Nối VPC)

- Cho phép bạn **kết nối hai VPC với nhau**
- Các VPC phải có **dải CIDR không trùng lặp**
- **Không bắc cầu (non-transitive)** - bạn cần thiết lập kết nối peering riêng giữa từng cặp VPC
- Nếu muốn tất cả VPC được kết nối, bạn phải tạo kết nối peering giữa từng tổ hợp

### VPC Endpoint

- Cung cấp **quyền truy cập riêng tư vào các dịch vụ AWS** trong VPC của bạn
- Loại bỏ nhu cầu sử dụng internet gateway hoặc thiết bị NAT
- Sẽ được đề cập chi tiết cho các dịch vụ cụ thể trong các bài giảng sau

### VPC Flow Log

- Ghi lại **nhật ký lưu lượng mạng**
- Được sử dụng để gỡ lỗi các vấn đề kết nối
- Giúp xác định xem lưu lượng có:
  - Bị từ chối quyền truy cập
  - Bị chặn
  - Được cho phép trong VPC của bạn

## Kết Nối On-Premise

### Site-to-Site VPN

- Thiết lập **kết nối VPN qua internet công cộng**
- Kết nối trung tâm dữ liệu on-premise của bạn với AWS

### Direct Connect

- Cung cấp **kết nối riêng trực tiếp đến AWS**
- Không đi qua internet công cộng
- Cung cấp hiệu suất mạng ổn định hơn

## Tóm Lược

Phần này đã đề cập đến các khái niệm VPC cơ bản cần thiết cho kỳ thi AWS Certified Developer. Những điểm chính cần nhớ là:

1. Hiểu mối quan hệ giữa VPC, subnet và availability zone
2. Biết sự khác biệt giữa kết nối public subnet và private subnet
3. Hiểu bảo mật mạng không trạng thái so với có trạng thái (NACL vs Security Group)
4. Nhận biết các giới hạn của VPC Peering (không bắc cầu)
5. Hiểu các tùy chọn khác nhau để kết nối với AWS từ on-premise

Đừng lo lắng nếu bạn chưa hiểu hết mọi thứ ngay lập tức. Các khái niệm này sẽ trở nên rõ ràng hơn khi chúng ta sử dụng chúng trong các bài tập thực hành trong các phần tiếp theo của khóa học. Bạn luôn có thể quay lại xem lại phần này sau.