# Xác Thực Đa Yếu Tố AWS với CLI và SDK

## Tổng Quan

Hướng dẫn này trình bày cách sử dụng Xác thực Đa yếu tố (MFA) với AWS CLI và SDK bằng cách tạo phiên tạm thời sử dụng AWS Security Token Service (STS).

## Khái Niệm Chính

### API STS GetSessionToken

Để sử dụng MFA với CLI hoặc SDK, bạn phải tạo một phiên tạm thời bằng API **STS GetSessionToken**. Đây là lệnh gọi API quan trọng cần nhớ cho mục đích thi cử.

### Các Tham Số Bắt Buộc

Khi gọi `GetSessionToken`, bạn cần cung cấp:
- **Số serial** của thiết bị MFA
- **Mã token** từ thiết bị MFA
- **Thời lượng** hiệu lực của credentials

### Kết Quả Trả Về

API trả về các credentials tạm thời bao gồm:
- Access Key ID
- Secret Access Key
- Session Token
- Thời gian hết hạn

## Hướng Dẫn Từng Bước

### Bước 1: Gán Thiết Bị MFA

1. Truy cập **IAM** trong AWS Console
2. Vào tài khoản người dùng của bạn (ví dụ: "Stephane")
3. Nhấp vào **Security credentials**
4. Nhấp **Assign MFA device**
5. Chọn **Virtual MFA device**
6. Quét mã QR bằng ứng dụng xác thực (ví dụ: Authy, Google Authenticator)
7. Nhập hai mã MFA liên tiếp từ ứng dụng của bạn
8. Nhấp **Assign MFA**
9. **Quan trọng**: Sao chép ARN của thiết bị MFA - bạn sẽ cần nó cho lệnh CLI

### Bước 2: Lấy Session Token Tạm Thời qua CLI

Chạy lệnh sau:

```bash
aws sts get-session-token --serial-number <MFA_DEVICE_ARN> --token-code <MFA_CODE>
```

**Ví dụ kết quả trả về:**
```json
{
  "Credentials": {
    "AccessKeyId": "ASIA...",
    "SecretAccessKey": "...",
    "SessionToken": "...",
    "Expiration": "2024-01-01T12:00:00Z"
  }
}
```

### Bước 3: Cấu Hình AWS Profile với Credentials Tạm Thời

1. Tạo một profile mới cho credentials MFA:
```bash
aws configure --profile mfa
```

2. Nhập **Access Key ID** tạm thời khi được yêu cầu
3. Nhập **Secret Access Key** tạm thời khi được yêu cầu
4. Đặt region mặc định (hoặc nhấn Enter để giữ nguyên)
5. Đặt định dạng output (hoặc nhấn Enter để giữ nguyên)

### Bước 4: Thêm Session Token vào File Credentials

1. Mở file AWS credentials:
   - **Linux/Mac**: `~/.aws/credentials`
   - **Windows**: `%USERPROFILE%\.aws\credentials`

2. Thêm session token vào profile MFA của bạn:
```ini
[mfa]
aws_access_key_id = ASIA...
aws_secret_access_key = ...
aws_session_token = <DÁN_SESSION_TOKEN_DÀI_VÀO_ĐÂY>
```

3. Lưu file

### Bước 5: Sử Dụng Profile MFA

Bây giờ bạn có thể thực hiện các lệnh gọi API sử dụng profile MFA:

```bash
aws s3 ls --profile mfa
```

Lệnh này sẽ sử dụng credentials tạm thời đã được xác thực MFA để liệt kê các S3 buckets.

## Lưu Ý Quan Trọng

- **Credentials tạm thời**: Các credentials này có thời hạn và sẽ hết hạn (thường là sau 1 giờ theo mặc định)
- **Session token**: Session token có thể rất dài - hãy chắc chắn sao chép đầy đủ
- **Bảo mật**: Vì đây là credentials tạm thời nên chúng an toàn hơn credentials dài hạn
- **Mẹo thi**: Nhớ rằng **STS GetSessionToken** là API được sử dụng để tạo session token tạm thời với MFA

## Tóm Tắt

Để sử dụng MFA với AWS CLI/SDK:
1. Gán thiết bị MFA cho IAM user của bạn
2. Gọi `aws sts get-session-token` với số serial thiết bị MFA và mã token
3. Cấu hình AWS profile mới với credentials tạm thời
4. Thêm session token vào file credentials
5. Sử dụng flag `--profile` để thực hiện các lệnh gọi API đã xác thực

Điểm chính cần nhớ là **STS GetSessionToken** tạo ra credentials tạm thời (Access Key, Secret Key và Session Token) có thể được sử dụng cho các lệnh gọi API đã xác thực MFA.