# AWS CLI: Quản Lý Nhiều Tài Khoản với Profiles

## Tổng Quan

Khi làm việc với nhiều tài khoản AWS, bạn cần một cách để quản lý các bộ thông tin xác thực và cấu hình khác nhau. AWS CLI cung cấp giải pháp thông qua **profiles**, cho phép bạn tổ chức và chuyển đổi giữa nhiều tài khoản AWS một cách liền mạch.

## Hiểu Về Cấu Hình Mặc Định

Theo mặc định, AWS CLI lưu trữ thông tin xác thực và cấu hình của bạn trong hai tệp:

- **`~/.aws/credentials`**: Chứa AWS access key ID và secret access key
- **`~/.aws/config`**: Chứa cài đặt region và định dạng output

Cả hai tệp đều chứa phần `[default]` được sử dụng khi không chỉ định profile cụ thể.

## Tạo Profiles Bổ Sung

### Sử Dụng Lệnh Configure

Để tạo một profile mới, sử dụng lệnh `aws configure` với cờ `--profile`:

```bash
aws configure --profile my-other-aws-account
```

Bạn sẽ được yêu cầu nhập:
- AWS Access Key ID
- AWS Secret Access Key
- Tên region mặc định (ví dụ: `us-west-2`)
- Định dạng output mặc định (tùy chọn)

### Những Thay Đổi Trong Tệp Cấu Hình

Sau khi tạo profile mới, các tệp của bạn sẽ được cập nhật:

**Tệp credentials:**
```ini
[default]
aws_access_key_id = YOUR_DEFAULT_KEY
aws_secret_access_key = YOUR_DEFAULT_SECRET

[my-other-aws-account]
aws_access_key_id = YOUR_OTHER_KEY
aws_secret_access_key = YOUR_OTHER_SECRET
```

**Tệp config:**
```ini
[default]
region = us-east-1

[profile my-other-aws-account]
region = us-west-2
```

## Sử Dụng Profiles Trong Lệnh

### Profile Mặc Định

Khi bạn chạy lệnh AWS CLI mà không chỉ định profile, profile mặc định sẽ được sử dụng:

```bash
aws s3 ls
```

### Profile Cụ Thể

Để sử dụng một profile cụ thể, thêm cờ `--profile` vào lệnh của bạn:

```bash
aws s3 ls --profile my-other-aws-account
```

Điều này áp dụng cho **mọi lệnh AWS CLI**. Cờ `--profile` có thể được sử dụng với tất cả các dịch vụ và thao tác AWS.

## Thực Hành Tốt Nhất

1. **Sử dụng tên profile mô tả rõ ràng**: Chọn tên xác định rõ tài khoản hoặc môi trường (ví dụ: `production`, `development`, `ten-khach-hang`)

2. **Giữ thông tin xác thực an toàn**: Không bao giờ commit các tệp `~/.aws/credentials` hoặc `~/.aws/config` vào version control

3. **Xác minh profile đang hoạt động**: Luôn kiểm tra kỹ profile bạn đang sử dụng, đặc biệt khi làm việc với các tài khoản production

4. **Tổ chức theo môi trường**: Cân nhắc sử dụng profiles cho các môi trường khác nhau (dev, staging, production)

## Điểm Chính Cần Nhớ

- Profiles cho phép bạn quản lý nhiều tài khoản AWS từ một cài đặt CLI duy nhất
- Sử dụng `aws configure --profile <tên>` để tạo profiles mới
- Sử dụng cờ `--profile <tên>` với bất kỳ lệnh AWS CLI nào để chỉ định tài khoản muốn sử dụng
- Đây là kiến thức thiết yếu cho các developers làm việc với nhiều tài khoản AWS, mặc dù thường không bắt buộc cho các kỳ thi chứng chỉ

## Ứng Dụng Thực Tế

Với vai trò là một developer, bạn sẽ thường xuyên cần:
- Chuyển đổi giữa các tài khoản development và production
- Quản lý tài nguyên trên nhiều tài khoản khách hàng khác nhau
- Làm việc với các AWS regions khác nhau cho cùng một tài khoản

Profiles giúp tất cả các tình huống này trở nên dễ quản lý và giúp ngăn chặn các sai lầm tốn kém do chạy lệnh nhầm tài khoản.