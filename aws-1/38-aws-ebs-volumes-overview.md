# Tổng Quan về AWS EBS Volumes

## Giới Thiệu

Trong phần này, chúng ta sẽ khám phá các tùy chọn lưu trữ khác nhau có sẵn cho các EC2 instances, với trọng tâm chính là EBS (Elastic Block Store) volumes.

## EBS là gì?

**EBS (Elastic Block Store)** là một ổ đĩa mạng có thể được gắn vào các EC2 instances trong khi chúng đang chạy. EBS volumes đã được sử dụng trong các cấu hình trước đó, thường là không có nhận thức rõ ràng.

### Lợi Ích Chính

- **Lưu Trữ Dữ Liệu Bền Vững**: EBS volumes cho phép dữ liệu tồn tại ngay cả sau khi instance bị terminated
- **Khôi Phục Dữ Liệu**: Bạn có thể tạo lại một instance và mount lại EBS volume cũ để lấy lại dữ liệu
- **Linh Hoạt**: Volumes có thể được tháo rời và gắn lại vào các instances khác nhau

## Các Đặc Điểm Quan Trọng

### Ràng Buộc Availability Zone

Ở cấp độ Certified Cloud Practitioner (CCP):
- Một EBS volume chỉ có thể được mount vào **một instance tại một thời điểm**
- Khi được tạo, EBS volume được **ràng buộc với một availability zone cụ thể**
- Ví dụ: Một EBS volume được tạo trong US-East-1a không thể gắn vào instance trong US-East-1b

### Khái Niệm Ổ Đĩa Mạng

Hãy nghĩ về EBS volumes như **"USB sticks qua mạng"** - chúng có thể được chuyển giữa các máy tính mà không cần kết nối vật lý, hoạt động hoàn toàn qua mạng.

## Chi Tiết Kỹ Thuật

### Giao Tiếp Qua Mạng

- **Dựa trên mạng**: EBS không phải là ổ đĩa vật lý
- **Độ trễ**: Có thể có một chút độ trễ do giao tiếp mạng giữa instance và EBS volume
- **Tháo rời nhanh**: Volumes có thể được tháo rời nhanh chóng từ một EC2 instance và gắn vào instance khác
- **Trường hợp sử dụng**: Lý tưởng cho các tình huống failover

### Cung Cấp Dung Lượng

Bạn phải cung cấp dung lượng trước:
- **Kích thước**: Chỉ định số gigabytes (GB) cần thiết
- **IOPS**: Xác định I/O Operations Per Second (số thao tác I/O mỗi giây) cho yêu cầu hiệu năng
- **Thanh toán**: Tính phí dựa trên dung lượng được cung cấp
- **Khả năng mở rộng**: Dung lượng có thể được tăng lên theo thời gian để có hiệu năng tốt hơn hoặc dung lượng lưu trữ bổ sung

## Giải Thích Sơ Đồ Kiến Trúc

### Ví Dụ Trong Một Availability Zone (US-East-1a)

- **EC2 Instance 1**: Có thể có một hoặc nhiều EBS volumes được gắn vào
- **EC2 Instance 2**: Yêu cầu EBS volume(s) riêng của nó
- **Nhiều Volumes**: Một EC2 instance có thể có nhiều EBS volumes được gắn vào (giống như nhiều USB sticks qua mạng)
- **Hạn chế**: Ở cấp độ CCP, một EBS volume không thể được gắn vào hai instances cùng một lúc

### Xem Xét Giữa Các Availability Zones

- EBS volumes được liên kết với availability zone của chúng
- Tương tự như EC2 instances, EBS volumes bị ràng buộc với một AZ cụ thể
- Để sử dụng volumes trong các AZs khác nhau, bạn phải tạo chúng riêng biệt trong mỗi zone
- **Lưu ý**: Snapshots cho phép bạn di chuyển volumes giữa các availability zones

### Volumes Không Được Gắn Kết

- EBS volumes có thể tồn tại mà không được gắn vào bất kỳ EC2 instance nào
- Chúng có thể được gắn theo yêu cầu khi cần thiết
- Điều này cung cấp tính linh hoạt trong quản lý lưu trữ

## Thuộc Tính Delete on Termination

Đây là một chủ đề quan trọng trong các kỳ thi chứng chỉ AWS.

### Hành Vi Mặc Định

Khi tạo EC2 instance thông qua console:

1. **Root Volume**: 
   - Delete on Termination được **bật theo mặc định**
   - Root EBS volume bị xóa khi instance bị terminate

2. **EBS Volumes Bổ Sung**:
   - Delete on Termination được **tắt theo mặc định**
   - Các volumes bổ sung được giữ lại khi instance bị terminate

### Tùy Chọn Cấu Hình

Thuộc tính Delete on Termination có thể được kiểm soát qua giao diện console:
- Bạn có thể bật hoặc tắt nó cho bất kỳ volume nào
- Hữu ích cho việc bảo toàn dữ liệu khi instances bị terminate

### Ví Dụ Trường Hợp Sử Dụng

**Tình huống**: Bảo toàn dữ liệu root volume khi một instance bị terminate
- **Giải pháp**: Tắt "Delete on Termination" cho root volume
- **Kết quả**: Dữ liệu được lưu ngay cả sau khi instance bị terminate

> **Mẹo Thi**: Tình huống này thường xuất hiện trong các kỳ thi chứng chỉ AWS.

## Tóm Tắt

EBS volumes cung cấp lưu trữ linh hoạt, bền vững cho EC2 instances với các điểm chính sau:
- Lưu trữ khối dựa trên mạng
- Ràng buộc với các availability zones cụ thể
- Dung lượng và hiệu năng có thể cấu hình
- Hành vi xóa có thể quản lý được
- Thiết yếu cho tính bền vững dữ liệu và các tình huống failover

---

*Tài liệu này bao gồm các khái niệm cơ bản về AWS EBS volumes liên quan đến EC2 instances.*