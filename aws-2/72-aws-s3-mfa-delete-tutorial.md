# AWS S3 MFA Delete - Hướng Dẫn Thực Hành

## Tổng Quan

Hướng dẫn này trình bày cách kích hoạt và sử dụng tính năng Multi-Factor Authentication (MFA) Delete cho các bucket Amazon S3. MFA Delete bổ sung thêm một lớp bảo mật bằng cách yêu cầu xác thực MFA trước khi xóa vĩnh viễn các phiên bản đối tượng hoặc vô hiệu hóa versioning trên bucket.

## Yêu Cầu Trước Khi Bắt Đầu

- Quyền truy cập tài khoản AWS Root
- Thiết bị MFA đã được cấu hình cho tài khoản root
- AWS CLI đã được cài đặt và cấu hình
- Kiến thức cơ bản về S3 versioning

## Bước 1: Tạo S3 Bucket với Versioning

1. Truy cập vào giao diện Amazon S3 console
2. Tạo bucket mới với các cài đặt sau:
   - Tên bucket: `demo-stephane-mfa-delete-2020` (hoặc tên bạn chọn)
   - Region: `eu-west-1` (hoặc region bạn muốn)
   - Bật bucket versioning
3. Nhấp **Create bucket**

## Bước 2: Xác Minh Thiết Lập MFA Device

1. Đăng nhập vào AWS console với tài khoản root
2. Điều hướng đến **IAM** → **Security Credentials**
3. Trong phần **Multi-Factor Authentication (MFA)**, xác minh rằng thiết bị MFA ảo đã được cấu hình
4. Sao chép ARN của thiết bị MFA (bạn sẽ cần thông tin này sau)

## Bước 3: Cấu Hình AWS CLI với Root Credentials

> **Cảnh báo**: Không khuyến khích sử dụng thông tin xác thực tài khoản root cho các hoạt động thường xuyên. Chỉ sử dụng cho việc bật MFA Delete.

1. Tạo access keys cho tài khoản root:
   - Vào **IAM** → **Security Credentials**
   - Nhấp **Create access key**
   - Tải xuống và lưu file access key
   
2. Cấu hình AWS CLI với named profile:

```bash
aws configure --profile root-mfa-delete-demo
```

3. Nhập các thông tin khi được yêu cầu:
   - AWS Access Key ID: [Root access key của bạn]
   - AWS Secret Access Key: [Root secret key của bạn]
   - Default region name: `eu-west-1`
   - Default output format: [Nhấn Enter]

4. Kiểm tra profile:

```bash
aws s3 ls --profile root-mfa-delete-demo
```

## Bước 4: Kích Hoạt MFA Delete

Sử dụng AWS CLI để kích hoạt MFA Delete trên bucket:

```bash
aws s3api put-bucket-versioning \
  --bucket demo-stephane-mfa-delete-2020 \
  --versioning-configuration Status=Enabled,MFADelete=Enabled \
  --mfa "arn:aws:iam::ACCOUNT-ID:mfa/root-account-mfa-device MFA-CODE" \
  --profile root-mfa-delete-demo
```

Thay thế:
- `demo-stephane-mfa-delete-2020` bằng tên bucket của bạn
- `arn:aws:iam::ACCOUNT-ID:mfa/root-account-mfa-device` bằng ARN thiết bị MFA của bạn
- `MFA-CODE` bằng mã 6 chữ số hiện tại từ thiết bị MFA

## Bước 5: Xác Minh MFA Delete Đã Được Kích Hoạt

1. Vào bucket S3 trong console
2. Nhấp **Properties** → **Bucket Versioning** → **Edit**
3. Xác minh rằng cả hai đều:
   - Bucket versioning đã **Enabled**
   - MFA Delete đã **Enabled**

## Bước 6: Kiểm Tra Bảo Vệ MFA Delete

### Tải Lên Đối Tượng Thử Nghiệm

1. Tải lên một file thử nghiệm vào bucket (ví dụ: một ảnh JPEG)
2. Việc tải lên hoạt động bình thường

### Kiểm Tra Xóa với Delete Marker

1. Xóa đối tượng đã tải lên từ console
2. Thao tác này tạo delete marker (xóa mềm) - hoạt động không cần MFA

### Kiểm Tra Xóa Vĩnh Viễn (Xóa Version)

1. Điều hướng đến các phiên bản đối tượng
2. Thử xóa vĩnh viễn một phiên bản cụ thể
3. **Kết quả**: Bạn sẽ nhận được thông báo lỗi cho biết MFA Delete đã được kích hoạt
4. Xóa vĩnh viễn yêu cầu sử dụng AWS CLI với xác thực MFA

## Bước 7: Vô Hiệu Hóa MFA Delete

Để vô hiệu hóa MFA Delete, sử dụng lại AWS CLI:

```bash
aws s3api put-bucket-versioning \
  --bucket demo-stephane-mfa-delete-2020 \
  --versioning-configuration Status=Enabled,MFADelete=Disabled \
  --mfa "arn:aws:iam::ACCOUNT-ID:mfa/root-account-mfa-device MFA-CODE" \
  --profile root-mfa-delete-demo
```

Sau khi vô hiệu hóa, bạn có thể xóa vĩnh viễn các phiên bản đối tượng từ console mà không cần MFA.

## Thực Hành Bảo Mật Tốt Nhất

1. **Xóa Root Access Keys**: Sau khi hoàn thành hướng dẫn này, hãy xóa ngay các root access keys bạn đã tạo
   - Vào **IAM** → **Security Credentials**
   - Vô hiệu hóa và xóa các access keys
   
2. **Sử Dụng IAM Users**: Đối với các hoạt động thông thường, luôn sử dụng IAM users với quyền phù hợp thay vì thông tin xác thực root

3. **Bật MFA Delete cho Buckets Quan Trọng**: Cân nhắc bật MFA Delete cho các buckets chứa dữ liệu nhạy cảm hoặc quan trọng

## Lưu Ý Quan Trọng

- MFA Delete chỉ có thể được bật/tắt bằng AWS CLI, không thể thông qua AWS Console
- MFA Delete yêu cầu thông tin xác thực tài khoản root
- Chỉ chủ sở hữu bucket (tài khoản root) mới có thể bật hoặc tắt MFA Delete
- MFA Delete bảo vệ khỏi việc xóa vĩnh viễn các phiên bản đối tượng một cách vô ý
- Xóa mềm (thêm delete markers) không yêu cầu MFA

## Dọn Dẹp

1. Xóa các đối tượng thử nghiệm khỏi bucket
2. Xóa bucket thử nghiệm nếu không còn cần thiết
3. **Quan trọng**: Xóa root access keys từ IAM Security Credentials

## Kết Luận

MFA Delete cung cấp một lớp bảo mật bổ sung cho các S3 buckets của bạn bằng cách yêu cầu xác thực MFA trước khi xóa vĩnh viễn các phiên bản đối tượng. Mặc dù cần quyền truy cập tài khoản root để cấu hình, đây là một tính năng bảo mật có giá trị để bảo vệ dữ liệu quan trọng.

## Script Tham Khảo

Các lệnh được sử dụng trong hướng dẫn này có thể tìm thấy trong: `s3advanced.mfadelete.sh`

---

**Bước Tiếp Theo**: Khám phá các tính năng bảo mật S3 khác như bucket policies, mã hóa và access logging để bảo mật thêm cho các S3 buckets của bạn.