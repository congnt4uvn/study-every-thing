# Tổng Quan Về Bảo Mật Mạng AWS VPC

## Giới Thiệu

Sau khi đã tìm hiểu tất cả các khía cạnh về việc định nghĩa mạng trong VPC, hãy cùng nói về bảo mật mạng. Bài giảng này tập trung vào các khái niệm Network ACL (NACL) và Security Groups, cũng như VPC Flow Logs để giám sát và xử lý sự cố.

## Network ACL (NACL)

### Network ACL là gì?

Network ACL (NACL) là một tường lửa kiểm soát lưu lượng truy cập từ và đến các subnet trong VPC của bạn.

### Đặc Điểm Chính

- **Mức Độ Kiểm Soát**: Hoạt động ở cấp độ subnet
- **Loại Quy Tắc**: Có thể có cả quy tắc **cho phép** và **từ chối**
- **Nội Dung Quy Tắc**: Quy tắc chỉ bao gồm địa chỉ IP
- **Tuyến Phòng Thủ Đầu Tiên**: Đóng vai trò là cơ chế phòng thủ đầu tiên cho các subnet công khai của bạn

### Cách Hoạt Động

Khi bạn gắn NACL ở cấp độ subnet, bạn có thể kiểm soát lưu lượng một cách rõ ràng:
- Cho phép lưu lượng từ các địa chỉ IP cụ thể
- Từ chối lưu lượng từ các địa chỉ IP cụ thể

Lưu lượng từ và đến internet phải đi qua Network ACL trước khi đến bất kỳ EC2 instance nào trong subnet.

### Hành Vi Mặc Định

Khi bạn có VPC mặc định:
- NACL mặc định **cho phép mọi thứ vào** và **cho phép mọi thứ ra**
- Đây là lý do tại sao bạn thường không cần phải sửa đổi NACL cho các cấu hình cơ bản

## Security Groups

### Security Group là gì?

Security Group là một tường lửa kiểm soát lưu lượng truy cập đến và đi từ ENI (Elastic Network Interface) hoặc EC2 instance.

### Đặc Điểm Chính

- **Mức Độ Kiểm Soát**: Hoạt động ở cấp độ instance hoặc ENI
- **Loại Quy Tắc**: Chỉ có thể có **quy tắc cho phép** (không có quy tắc từ chối rõ ràng)
- **Nội Dung Quy Tắc**: Có thể tham chiếu đến địa chỉ IP hoặc các security group khác
- **Tuyến Phòng Thủ Thứ Hai**: Đóng vai trò là cơ chế phòng thủ thứ hai sau NACL

### Cách Hoạt Động

Security groups được gắn trực tiếp vào các EC2 instance. Sau khi lưu lượng đi qua Network ACL, nó phải đi qua security group trước khi đến EC2 instance.

## So Sánh Network ACL và Security Group

| Tính Năng | Security Group | Network ACL |
|-----------|---------------|-------------|
| **Hoạt động ở** | Cấp độ Instance/ENI | Cấp độ Subnet |
| **Quy tắc** | Chỉ có quy tắc cho phép | Quy tắc cho phép và từ chối |
| **Trạng thái** | Stateful (tự động cho phép lưu lượng phản hồi) | Stateless (phải cho phép rõ ràng lưu lượng vào và ra) |
| **Áp dụng cho** | Instance hoặc ENI | Tất cả instance trong subnet |

### Lưu Ý Quan Trọng

- Security groups là **stateful**: Lưu lượng phản hồi được tự động cho phép bất kể quy tắc
- Network ACLs là **stateless**: Bạn phải cho phép rõ ràng lưu lượng theo cả hai hướng

## VPC Flow Logs

### VPC Flow Logs là gì?

VPC Flow Logs ghi lại thông tin về tất cả lưu lượng IP đi qua các giao diện mạng của bạn.

### Các Loại Flow Logs

1. **VPC Flow Logs**: Ghi lại lưu lượng ở cấp độ VPC
2. **Subnet Flow Logs**: Ghi lại lưu lượng ở cấp độ subnet
3. **ENI Flow Logs**: Ghi lại lưu lượng ở cấp độ Elastic Network Interface

### Trường Hợp Sử Dụng

Flow logs giúp bạn:
- **Giám sát** lưu lượng mạng trong VPC của bạn
- **Xử lý sự cố kết nối**, chẳng hạn như:
  - Tại sao subnet không thể truy cập internet
  - Tại sao các subnet có thể hoặc không thể giao tiếp với nhau
  - Các vấn đề kết nối từ internet đến subnet

### Thông Tin Được Ghi Lại

- **Lưu lượng được cho phép**: Thông tin về các kết nối được phép
- **Lưu lượng bị từ chối**: Thông tin về các kết nối bị chặn
- **Dịch Vụ AWS Được Quản Lý**: Thông tin mạng từ các dịch vụ như:
  - Elastic Load Balancers
  - ElastiCache
  - RDS (Relational Database Service)
  - Aurora

### Tùy Chọn Lưu Trữ

Dữ liệu VPC Flow Logs có thể được gửi đến:
- **Amazon S3**: Để lưu trữ và phân tích dài hạn
- **CloudWatch Logs**: Để giám sát và cảnh báo thời gian thực
- **Kinesis Data Firehose**: Để xử lý dữ liệu streaming

## Tóm Tắt

Trong bài giảng này, chúng ta đã đề cập đến ba thành phần quan trọng của bảo mật mạng VPC:

1. **Network ACLs (NACLs)**: Tường lửa cấp độ subnet với quy tắc cho phép và từ chối
2. **Security Groups**: Tường lửa cấp độ instance chỉ có quy tắc cho phép
3. **VPC Flow Logs**: Ghi log lưu lượng mạng để giám sát và xử lý sự cố

Hiểu rõ các lớp bảo mật này là điều cần thiết để xây dựng các ứng dụng an toàn và có kiến trúc tốt trên AWS.