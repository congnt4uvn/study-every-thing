# Tổng Quan về Bảo Mật Amazon S3

## Giới Thiệu

Bảo mật Amazon S3 là một khía cạnh quan trọng trong việc quản lý lưu trữ đám mây của bạn. Hướng dẫn này bao gồm các cơ chế bảo mật chính có sẵn để bảo vệ các bucket và object S3 của bạn.

## Các Cơ Chế Bảo Mật

### 1. Bảo Mật Dựa Trên Người Dùng (User-Based)

**IAM Policies** cho phép bạn kiểm soát các API call nào được phép cho các IAM user cụ thể. Các policy này xác thực quyền truy cập ở cấp độ người dùng, xác định những hành động nào mà mỗi người dùng có thể thực hiện trên tài nguyên S3.

### 2. Bảo Mật Dựa Trên Tài Nguyên (Resource-Based)

#### S3 Bucket Policies
- **Quy tắc áp dụng cho toàn bộ bucket** có thể được gán trực tiếp từ bảng điều khiển S3
- Cho phép người dùng cụ thể truy cập vào bucket của bạn
- Kích hoạt **truy cập cross-account** (cho phép người dùng từ các tài khoản AWS khác)
- Được sử dụng để làm cho bucket S3 công khai
- **Phương pháp phổ biến nhất** để cấu hình bảo mật S3

#### Object Access Control List (ACL)
- Cung cấp **bảo mật chi tiết hơn** ở cấp độ object
- Có thể bị vô hiệu hóa nếu không cần thiết
- Ít được sử dụng trong các triển khai hiện đại

#### Bucket ACL
- Kiểm soát bảo mật ở cấp độ bucket
- Ít phổ biến hơn nhiều so với bucket policies
- Cũng có thể bị vô hiệu hóa

### 3. Mã Hóa (Encryption)
Các object có thể được bảo mật bằng cách sử dụng **encryption keys** để bảo vệ dữ liệu khi lưu trữ.

## Hiểu về S3 Bucket Policies

### Cấu Trúc Policy

S3 Bucket policies là **các tài liệu dựa trên JSON** với các thành phần chính sau:

- **Resource**: Chỉ định bucket và object nào mà policy áp dụng
- **Effect**: `Allow` (Cho phép) hoặc `Deny` (Từ chối)
- **Action**: Các API call được cho phép hoặc bị từ chối (ví dụ: `GetObject`)
- **Principal**: Tài khoản hoặc người dùng mà policy áp dụng

### Ví Dụ: Quyền Đọc Công Khai

```json
{
  "Effect": "Allow",
  "Principal": "*",
  "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::example-bucket/*"
}
```

Policy này cho phép bất kỳ ai (`Principal: "*"`) truy xuất (`GetObject`) bất kỳ object nào (`/*`) từ bucket ví dụ.

### Các Trường Hợp Sử Dụng Phổ Biến

Bucket policies có thể được sử dụng để:
- Cấp **quyền truy cập công khai** cho bucket
- Buộc **các object phải được mã hóa** khi upload
- Cấp **quyền truy cập cho tài khoản AWS khác**

## Các Kịch Bản Kiểm Soát Truy Cập

### Khi Nào IAM Principal Có Thể Truy Cập Object S3?

Một IAM principal có thể truy cập object S3 khi:
1. IAM permissions cho phép, **HOẶC**
2. Resource policy cho phép, **VÀ**
3. **Không có từ chối rõ ràng** (explicit deny) trong hành động

### Kịch Bản 1: Truy Cập Công Khai qua Bucket Policy

```
[Khách Truy Cập Website] → [S3 Bucket với Public Bucket Policy] → [Được Phép Truy Cập]
```

Khách truy cập website từ internet có thể truy cập các file trong S3 bucket của bạn khi một bucket policy cho phép truy cập công khai được gán.

### Kịch Bản 2: Truy Cập của IAM User

```
[IAM User] + [IAM Permissions] → [S3 Bucket] → [Được Phép Truy Cập]
```

Một IAM user trong tài khoản AWS của bạn có thể truy cập S3 bằng cách có IAM permissions được gán thông qua một policy.

### Kịch Bản 3: Truy Cập từ EC2 Instance

```
[EC2 Instance] + [IAM Role] → [S3 Bucket] → [Được Phép Truy Cập]
```

Đối với các EC2 instance, IAM users không phù hợp. Thay vào đó:
- Tạo một **EC2 instance role** với các IAM permissions chính xác
- EC2 instance sau đó có thể truy cập các Amazon S3 bucket

### Kịch Bản 4: Truy Cập Cross-Account

```
[IAM User (Tài khoản B)] → [S3 Bucket Policy] → [S3 Bucket (Tài khoản A)] → [Được Phép Truy Cập]
```

Để truy cập cross-account:
- Sử dụng **S3 Bucket Policy**
- Cấu hình để cho phép truy cập cho các IAM user cụ thể từ tài khoản AWS khác
- IAM user bên ngoài sau đó có thể thực hiện các API call đến S3 bucket của bạn

## Cài Đặt Block Public Access

### Lớp Bảo Mật Bổ Sung

AWS cung cấp **cài đặt Block Public Access cho Bucket** như một lớp bảo mật bổ sung để ngăn chặn rò rỉ dữ liệu của công ty.

### Các Tính Năng Chính

- Ngay cả khi một S3 bucket policy sẽ làm cho bucket trở nên công khai, nếu các cài đặt này được kích hoạt, **bucket sẽ không bao giờ công khai**
- Ngăn chặn rò rỉ dữ liệu do cấu hình sai bucket policy
- Có thể được đặt ở **cấp độ bucket** hoặc **cấp độ tài khoản**

### Thực Hành Tốt Nhất

- Nếu bạn biết bucket của mình **không bao giờ nên công khai**, hãy để các cài đặt này được kích hoạt
- Để bảo vệ toàn tổ chức, hãy đặt cài đặt này ở **cấp độ tài khoản** để đảm bảo không có bucket S3 nào có thể được công khai

## Tóm Tắt

Bảo mật Amazon S3 cung cấp nhiều lớp bảo vệ:
- **Bảo mật dựa trên người dùng** thông qua IAM policies
- **Bảo mật dựa trên tài nguyên** thông qua bucket policies (phổ biến nhất)
- **Access control lists** (ACLs) để kiểm soát chi tiết
- **Mã hóa** để bảo vệ dữ liệu
- **Cài đặt Block Public Access** như một mạng lưới an toàn chống lại cấu hình sai

Sự kết hợp của các cơ chế bảo mật này cho phép bạn triển khai kiểm soát truy cập mạnh mẽ cho các tài nguyên S3 của mình trong khi ngăn chặn việc vô tình để lộ dữ liệu.