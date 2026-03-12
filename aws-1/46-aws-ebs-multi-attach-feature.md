# Tính năng Multi-Attach của AWS EBS

## Tổng quan

Tính năng Multi-Attach của Amazon EBS volumes cho phép bạn gắn kết cùng một EBS volume với nhiều EC2 instances trong cùng một Availability Zone. Khả năng này mang lại sự linh hoạt cao hơn cho các ứng dụng cluster yêu cầu truy cập lưu trữ chia sẻ.

## Cách thức hoạt động

Tính năng Multi-Attach cho phép:
- Một EBS volume duy nhất có thể được gắn kết đồng thời với nhiều EC2 instances
- Tất cả các instances được gắn kết chia sẻ cùng một volume hiệu suất cao
- Chỉ khả dụng cho họ EBS volume **io1** và **io2**

### Kiến trúc

```
┌─────────────┐
│  EC2 Instance 1  │───┐
└─────────────┘   │
                  │    ┌──────────────┐
┌─────────────┐   ├────│  io2 Volume  │
│  EC2 Instance 2  │───┤    (Multi-   │
└─────────────┘   │    │   Attach)    │
                  │    └──────────────┘
┌─────────────┐   │
│  EC2 Instance 3  │───┘
└─────────────┘
```

## Các tính năng chính

### Quyền Đọc và Ghi
- Mỗi instance được gắn kết có **quyền đọc và ghi đầy đủ** đối với volume
- Tất cả các instances có thể đọc và ghi đồng thời vào volume hiệu suất cao

### Các trường hợp sử dụng

1. **Tính khả dụng ứng dụng cao hơn**
   - Lý tưởng cho các ứng dụng Linux cluster
   - Ví dụ: Teradata clusters

2. **Thao tác ghi đồng thời**
   - Các ứng dụng phải quản lý các thao tác ghi đồng thời
   - Lưu trữ chia sẻ cho khối lượng công việc đa instance

## Giới hạn và Yêu cầu

### Giới hạn Availability Zone
- Multi-Attach chỉ khả dụng **trong cùng một Availability Zone**
- Không thể gắn kết EBS volume từ một AZ này sang các instances ở AZ khác

### Giới hạn số lượng Instance
- **Tối đa 16 EC2 instances** có thể gắn kết đồng thời với cùng một volume
- Đây là giới hạn quan trọng cần nhớ cho các kỳ thi chứng chỉ AWS

### Yêu cầu về File System
- Phải sử dụng **file system có khả năng nhận biết cluster**
- Khác với các file system tiêu chuẩn như XFS hoặc EXT4
- File system phải có khả năng quản lý truy cập đồng thời từ nhiều instances

## Hỗ trợ loại Volume

| Loại Volume | Hỗ trợ Multi-Attach |
|-------------|---------------------|
| io1         | ✅ Có               |
| io2         | ✅ Có               |
| gp2         | ❌ Không            |
| gp3         | ❌ Không            |
| st1         | ❌ Không            |
| sc1         | ❌ Không            |

## Điểm quan trọng cho kỳ thi

- Multi-Attach chỉ khả dụng cho loại volume **io1** và **io2**
- Tối đa **16 instances** cho mỗi volume
- Phải nằm trong **cùng một Availability Zone**
- Yêu cầu **file system có khả năng nhận biết cluster**

## Tóm tắt

Tính năng EBS Multi-Attach là một khả năng mạnh mẽ cho các trường hợp sử dụng cụ thể yêu cầu lưu trữ chia sẻ giữa nhiều EC2 instances. Mặc dù có một số giới hạn nhất định, nó cung cấp chức năng thiết yếu cho các ứng dụng cluster và kiến trúc có tính khả dụng cao trong AWS.