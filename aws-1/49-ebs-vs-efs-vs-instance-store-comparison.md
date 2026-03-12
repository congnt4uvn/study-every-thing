# So Sánh EBS vs EFS vs Instance Store: Các Tùy Chọn Lưu Trữ AWS

## Tổng Quan

Tài liệu này giải thích các điểm khác biệt chính giữa các tùy chọn lưu trữ AWS: EBS volumes, EFS file systems và EC2 Instance Store.

## EBS (Elastic Block Store) Volumes

### Đặc Điểm Chính

- **Gắn Kết**: EBS volumes được gắn vào **một instance tại một thời điểm**
  - Ngoại lệ: Tính năng multi-attach cho các loại volume io1 và io2 (chỉ dành cho các trường hợp sử dụng cụ thể)

- **Khóa Theo Availability Zone**: EBS volumes bị khóa ở cấp độ AZ (Availability Zone)
  - Ví dụ: Một EBS volume ở AZ 1 không thể gắn trực tiếp vào EC2 instance ở AZ 2

### Các Loại Volume và Hiệu Suất

#### gp2 (General Purpose SSD)
- IO tăng tỷ lệ thuận với dung lượng ổ đĩa

#### gp3 và io1 (Provisioned IOPS SSD)
- IO có thể tăng độc lập với dung lượng ổ đĩa
- Cấu hình hiệu suất linh hoạt hơn

### Di Chuyển Giữa Các Availability Zones

Để di chuyển EBS volume giữa các AZ:
1. Tạo **snapshot** của EBS volume
2. Lưu trữ snapshot vào EBS Snapshots
3. Khôi phục snapshot tại AZ đích

### Lưu Ý Về Sao Lưu

- Sao lưu EBS volume sử dụng tài nguyên IO
- **Thực Hành Tốt**: Tránh chạy sao lưu trong thời gian lưu lượng truy cập cao để tránh ảnh hưởng đến hiệu suất

### Hành Vi Khi Xóa Instance

- Root EBS volumes **bị xóa theo mặc định** khi EC2 instance bị xóa
- Hành vi này có thể được tắt nếu cần

## EFS (Elastic File System)

### Đặc Điểm Chính

- **Network File System**: Được thiết kế cho truy cập chia sẻ trên nhiều instances
- **Hỗ Trợ Multi-AZ**: Có thể gắn vào hàng trăm instances trên các availability zones khác nhau đồng thời

### Kiến Trúc

- Một EFS file system có thể có nhiều mount targets ở các AZ khác nhau
- Nhiều instances có thể chia sẻ cùng một file system
- Cho phép các workloads cộng tác và truy cập dữ liệu chia sẻ

### Các Trường Hợp Sử Dụng

- **Triển khai WordPress**: Nhiều web servers chia sẻ cùng nội dung
- Các ứng dụng yêu cầu truy cập file chia sẻ giữa các instances

### Yêu Cầu Nền Tảng

- **Chỉ dành cho Linux instances** (sử dụng hệ thống file POSIX)

### Cân Nhắc Về Chi Phí

- Giá cao hơn so với EBS
- **Tối Ưu Chi Phí**: Tận dụng các storage tiers của EFS để tiết kiệm chi phí

## EC2 Instance Store

### Đặc Điểm Chính

- **Gắn vật lý** vào EC2 instance
- Cung cấp lưu trữ local với hiệu suất cao

### Hạn Chế Quan Trọng

- **Lưu trữ tạm thời (Ephemeral)**: Nếu bạn mất EC2 instance, bạn cũng mất dữ liệu lưu trữ
- Dữ liệu không tồn tại khi instance dừng hoặc bị xóa

## Bảng So Sánh Tổng Hợp

| Tính Năng | EBS | EFS | Instance Store |
|-----------|-----|-----|----------------|
| Gắn Kết | Một instance (trừ io1/io2 multi-attach) | Hàng trăm instances | Gắn vật lý vào một instance |
| Khả Dụng | Khóa theo AZ | Multi-AZ | Theo instance |
| Tính Bền Vững | Bền vững (tồn tại sau khi xóa instance nếu được cấu hình) | Bền vững | Tạm thời |
| Trường Hợp Sử Dụng | Block storage cho một instance | Hệ thống file chia sẻ | Lưu trữ tạm thời hiệu suất cao |
| Nền Tảng | Tất cả hệ điều hành | Chỉ Linux (POSIX) | Tất cả hệ điều hành |
| Giá | Trung bình | Cao hơn (có tùy chọn tier) | Bao gồm trong instance |

## Thực Hành Tốt Nhất

1. **EBS**: Sử dụng cho nhu cầu lưu trữ block bền vững, cấu hình bảo vệ xóa cho dữ liệu quan trọng
2. **EFS**: Sử dụng khi nhiều instances cần chia sẻ files, tận dụng storage tiers để tối ưu chi phí
3. **Instance Store**: Chỉ sử dụng cho dữ liệu tạm thời, cache hoặc buffers có thể mất

---

*Hiểu rõ những điểm khác biệt này là rất quan trọng để thiết kế kiến trúc AWS có khả năng phục hồi và hiệu quả về chi phí.*