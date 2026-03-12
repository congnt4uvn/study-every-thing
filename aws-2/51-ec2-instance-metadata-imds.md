# EC2 Instance Metadata (IMDS)

## Tổng Quan

Dịch vụ EC2 Instance Metadata Service (IMDS) là một tính năng mạnh mẽ cho phép các EC2 instance tự tìm hiểu thông tin về chính chúng mà không cần sử dụng IAM Role. Tính năng này không được nhiều nhà phát triển biết đến nhưng là một phần cơ bản trong cách hoạt động của EC2 instance.

## IMDS là gì?

Instance Metadata Service (IMDS) cho phép các EC2 instance truy xuất thông tin về chính chúng bằng cách truy cập một URL endpoint cụ thể:

```
http://169.254.169.254
```

## Thông Tin Có Sẵn

Thông qua metadata service, bạn có thể truy xuất:

- **Tên instance**
- **Địa chỉ IP công khai**
- **Địa chỉ IP riêng tư**
- **Tên IAM Role**
- **Thông tin xác thực bảo mật tạm thời** (nếu có IAM role được gán)
- **User data** (các script khởi chạy)

**Lưu ý:** Mặc dù bạn có thể truy xuất tên IAM Role và thông tin xác thực, bạn không thể truy xuất chính sách IAM được gán cho role thông qua metadata service.

## Metadata và User Data

- **Metadata**: Thông tin về chính EC2 instance
- **User Data**: Các script khởi chạy và dữ liệu cấu hình được sử dụng trong quá trình khởi động instance

Cả hai đều có thể được truy cập thông qua cùng một URL endpoint.

## Các Phiên Bản IMDS

### IMDSv1 (Phiên Bản Cũ)

Phiên bản gốc của Instance Metadata Service:

- **Phương thức truy cập**: Truy cập URL trực tiếp
- **Bảo mật**: Mô hình bảo mật cơ bản
- **Sử dụng**: Các yêu cầu GET đơn giản đến metadata endpoint

```bash
# Ví dụ yêu cầu IMDSv1
curl http://169.254.169.254/latest/meta-data/
```

### IMDSv2 (Được Khuyến Nghị)

Được giới thiệu và bật mặc định từ năm 2023, IMDSv2 cung cấp bảo mật nâng cao:

- **Phương thức truy cập**: Yêu cầu theo phiên làm việc
- **Bảo mật**: Yêu cầu xác thực bằng session token
- **Sử dụng**: Quy trình hai bước

#### Các Bước Truy Cập IMDSv2

**Bước 1: Lấy session token**

Sử dụng yêu cầu PUT để lấy session token:

```bash
TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`
```

**Bước 2: Sử dụng token để truy cập metadata**

Truyền token trong header của yêu cầu:

```bash
curl http://169.254.169.254/latest/meta-data/ \
  -H "X-aws-ec2-metadata-token: $TOKEN"
```

## Cải Tiến Bảo Mật trong IMDSv2

IMDSv2 được AWS giới thiệu để tăng cường bảo mật:

- **Định hướng phiên**: Yêu cầu xác thực dựa trên token
- **Bảo vệ chống tấn công SSRF**: Giảm nguy cơ tấn công Server-Side Request Forgery
- **Token hết hạn**: Token có TTL (Time To Live) có thể cấu hình
- **Chi phí bổ sung**: Yêu cầu quy trình hai bước nhưng cung cấp bảo mật tốt hơn

## Thực Hành Tốt Nhất

1. **Sử dụng IMDSv2**: Luôn ưu tiên IMDSv2 thay vì IMDSv1 để có bảo mật tốt hơn
2. **Quản lý token**: Đặt giá trị TTL phù hợp cho session token
3. **Truy cập an toàn**: Đảm bảo metadata service chỉ có thể truy cập từ bên trong instance
4. **Giám sát sử dụng**: Theo dõi truy cập metadata service để kiểm toán bảo mật

## Tóm Tắt

EC2 Instance Metadata Service là một tính năng quan trọng cho phép các instance tự khám phá cấu hình và thông tin xác thực của chúng. Với việc giới thiệu IMDSv2, AWS đã cải thiện đáng kể tính bảo mật của dịch vụ này trong khi vẫn duy trì chức năng. Hiểu cách sử dụng đúng IMDS là điều cần thiết cho quản lý và bảo mật EC2 instance.