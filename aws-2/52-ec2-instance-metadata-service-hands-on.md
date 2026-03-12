# Dịch Vụ EC2 Instance Metadata (IMDS) - Hướng Dẫn Thực Hành

## Giới Thiệu

Hướng dẫn này trình bày cách sử dụng Dịch vụ EC2 Instance Metadata để truy vấn thông tin instance và lấy thông tin xác thực IAM role từ bên trong một EC2 instance.

## Yêu Cầu Trước

- Tài khoản AWS
- Hiểu biết cơ bản về EC2 instances
- Quen thuộc với các thao tác dòng lệnh

## Tạo EC2 Instance

### Bước 1: Cấu Hình Khởi Chạy Instance

1. Tạo một EC2 instance mới với tên **DemoEC2**
2. Chọn **Amazon Linux 2023 AMI** (phiên bản mới nhất)
3. Di chuyển đến phần **Advanced Details**
4. Tìm cài đặt **Metadata version**

### Bước 2: Hiểu Về Các Phiên Bản Metadata

- **Amazon Linux 2023**: Mặc định là **IMDSv2 only** (chỉ IMDSv2)
- **Amazon Linux 2**: Cho phép chọn giữa **V1 and V2** hoặc **V2 only**

Trong hướng dẫn này, chúng ta sẽ sử dụng Amazon Linux 2023 với IMDSv2.

### Bước 3: Cấu Hình Bảo Mật

1. Tiếp tục **không cần key pair** (tùy chọn)
2. Tạo security group mới:
   - Cho phép **SSH from anywhere** (SSH từ mọi nơi)
3. Để trống **IAM instance profile** ban đầu (chúng ta sẽ thêm sau)

### Bước 4: Khởi Chạy Instance

Khởi chạy instance và kết nối bằng **EC2 Instance Connect**.

## Làm Việc Với Instance Metadata Service

### Hiểu Về IMDSv1 vs IMDSv2

#### Kiểm Tra IMDSv1 (Sẽ Thất Bại Trên Amazon Linux 2023)

```bash
curl http://169.254.169.254/latest/meta-data/
```

**Kết quả**: `401 Unauthorized` (Không được phép)

IMDSv1 bị vô hiệu hóa trên Amazon Linux 2023 vì lý do bảo mật.

### Sử Dụng IMDSv2 (Được Khuyến Nghị)

#### Bước 1: Lấy Session Token

```bash
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
```

Lệnh này:
- Truy vấn endpoint `/latest/api/token`
- Thiết lập thời gian hết hạn token (TTL) trong header
- Lưu token vào biến `TOKEN`

Xác minh token:
```bash
echo $TOKEN
```

#### Bước 2: Truy Vấn Metadata Với Token

```bash
curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/
```

**Kết quả**: Bạn sẽ thấy danh sách các metadata endpoint có sẵn.

## Khám Phá Các Metadata Endpoint

### Hiểu Về Kết Quả Trả Về

- **Có dấu gạch chéo (/)**: Cho biết một thư mục có nhiều dữ liệu bên trong
- **Không có dấu gạch chéo**: Cho biết một giá trị trực tiếp

### Lấy Metadata Cụ Thể

#### Lấy Hostname

```bash
curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/hostname
```

#### Lấy Địa Chỉ IPv4 Nội Bộ

```bash
curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/local-ipv4
```

## Lấy Thông Tin Xác Thực IAM Role

### Thử Nghiệm Ban Đầu (Không Có IAM Role)

Di chuyển đến identity credentials:

```bash
curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/iam/security-credentials/
```

**Kết quả**: `Not found` - Chưa có IAM role nào được gắn kết.

### Gắn Kết IAM Role

1. Trong AWS Console, chọn EC2 instance của bạn
2. Vào **Actions** → **Security** → **Modify IAM role**
3. Chọn bất kỳ IAM role nào (role cụ thể không quan trọng cho demo này)
4. Đợi khoảng 30 giây để thay đổi có hiệu lực

### Lấy Thông Tin Xác Thực

#### Liệt Kê Các Role Có Sẵn

```bash
curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/iam/security-credentials/
```

**Kết quả**: Trả về tên role (ví dụ: `EC2Instance`)

#### Lấy Thông Tin Xác Thực Của Role

```bash
curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/iam/security-credentials/EC2Instance
```

**Kết quả**: Phản hồi JSON chứa:
- `AccessKeyId`: Access key tạm thời
- `SecretAccessKey`: Secret key tạm thời
- `Token`: Session token
- `Expiration`: Thời điểm hết hạn thông tin xác thực (thường là 1 giờ)

### Ví Dụ Phản Hồi

```json
{
  "Code": "Success",
  "LastUpdated": "2024-XX-XXTXX:XX:XXZ",
  "Type": "AWS-HMAC",
  "AccessKeyId": "ASIA...",
  "SecretAccessKey": "...",
  "Token": "...",
  "Expiration": "2024-XX-XXTXX:XX:XXZ"
}
```

## Cách IAM Role Hoạt Động Với EC2

Điều này minh họa cơ chế hoạt động bên dưới:

1. EC2 instance được gán một IAM role
2. AWS tự động cung cấp thông tin xác thực tạm thời qua IMDS
3. AWS CLI và SDK tự động lấy các thông tin xác thực này
4. Thông tin xác thực được xoay vòng trước khi hết hạn

**Quan trọng**: Bạn không cần phải lấy thông tin xác thực này thủ công trong ứng dụng của mình - AWS SDK tự động xử lý việc này.

## Những Điểm Chính

- **IMDSv2** an toàn hơn và bắt buộc trên Amazon Linux 2023
- **Xác thực dựa trên token** ngăn chặn các cuộc tấn công SSRF
- **Thông tin xác thực IAM role** được cung cấp thông qua dịch vụ metadata
- **Xoay vòng thông tin xác thực tự động** đảm bảo bảo mật
- Dịch vụ metadata cho phép EC2 instance tự khám phá cấu hình của chúng

## Dọn Dẹp

Khi hoàn thành hướng dẫn:

1. Di chuyển đến EC2 Console
2. Chọn instance **DemoEC2**
3. **Terminate** (Chấm dứt) instance

## Kết Luận

EC2 Instance Metadata Service là một tính năng mạnh mẽ cho phép các instance truy cập dữ liệu cấu hình và thông tin xác thực IAM một cách an toàn. Mặc dù AWS SDK xử lý hầu hết các thao tác tự động, việc hiểu cơ chế bên dưới rất có giá trị cho việc khắc phục sự cố và các trường hợp sử dụng nâng cao.

---

**Các Bước Tiếp Theo**: Khám phá các dịch vụ AWS khác tích hợp với EC2 metadata service, chẳng hạn như AWS Systems Manager và CloudWatch.