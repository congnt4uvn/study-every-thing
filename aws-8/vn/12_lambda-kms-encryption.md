# AWS Lambda & KMS — Mã Hóa Biến Môi Trường

## Tổng Quan

Hướng dẫn này trình bày cách **mã hóa biến môi trường trong Lambda** bằng **AWS KMS (Key Management Service)**, giúp bảo vệ dữ liệu nhạy cảm (như mật khẩu cơ sở dữ liệu) khỏi bị lộ ở dạng văn bản thuần túy.

---

## Vấn Đề Cần Giải Quyết

Khi xây dựng Lambda function cần kết nối cơ sở dữ liệu hoặc dịch vụ bên ngoài, chúng ta phải lưu trữ thông tin xác thực. Có ba cách tiếp cận, mỗi cách có mức độ bảo mật khác nhau:

| Cách tiếp cận | Mức độ rủi ro |
|---|---|
| Hardcode thông tin xác thực vào mã nguồn | **Cao** — bất kỳ ai có quyền xem code đều thấy được |
| Lưu dưới dạng biến môi trường văn bản thuần | **Trung bình** — có thể đọc được trong console cấu hình Lambda |
| Mã hóa biến môi trường bằng KMS | **Thấp** — chỉ ai có quyền truy cập KMS key mới giải mã được |

---

## Hướng Dẫn Từng Bước: Lambda + KMS

### 1. Tạo Lambda Function

- Runtime: **Python**
- Viết function đọc biến môi trường `DB_PASSWORD`

```python
import os

def lambda_handler(event, context):
    db_password = os.environ['DB_PASSWORD']
    return "great"
```

---

### 2. Thêm Biến Môi Trường (Văn Bản Thuần — Không An Toàn)

1. Vào **Configuration → Environment Variables**
2. Thêm key: `DB_PASSWORD`, value: `super_secret`

> **Vấn đề:** Bất kỳ ai có quyền truy cập cấu hình Lambda đều có thể đọc giá trị này trực tiếp.

---

### 3. Bật Mã Hóa KMS Cho Biến Môi Trường

1. Vào **Configuration → Environment Variables → Encryption Configuration**
2. Bật **Encryption Helpers**
3. Chọn KMS key (ví dụ: `tutorial-key`)
4. Nhấn **Encrypt** bên cạnh biến môi trường

Biến môi trường giờ sẽ được lưu trữ ở dạng mã hóa.

---

### 4. Cập Nhật Code Để Giải Mã Khi Chạy

AWS cung cấp **đoạn code giải mã** sẵn trong console. Dùng `boto3` KMS client để giải mã:

```python
import os
import boto3
from base64 import b64decode

ENCRYPTED = os.environ['DB_PASSWORD']

# Giải mã khi khởi động (đặt ngoài handler để tối ưu hiệu suất)
DECRYPTED = boto3.client('kms').decrypt(
    CiphertextBlob=b64decode(ENCRYPTED),
    EncryptionContext={'LambdaFunctionName': os.environ['AWS_LAMBDA_FUNCTION_NAME']}
)['Plaintext'].decode('utf-8')

def lambda_handler(event, context):
    print("Giá trị đã mã hóa:", ENCRYPTED)
    print("Giá trị đã giải mã:", DECRYPTED)
    return "great"
```

---

### 5. Tăng Thời Gian Timeout Của Function

- Timeout mặc định là **3 giây** — có thể không đủ cho lệnh gọi KMS.
- Vào **Configuration → General Configuration → Edit**
- Đặt timeout thành **10 giây** (hoặc giá trị phù hợp)

---

### 6. Cấp Quyền Giải Mã Cho IAM Role Của Lambda

IAM Role của Lambda phải được phép gọi `kms:Decrypt` trên key cụ thể.

**Các bước thực hiện:**

1. Vào **Configuration → Permissions**
2. Nhấn vào **IAM Role**
3. Thêm **Inline Policy**:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "kms:Decrypt",
      "Resource": "arn:aws:kms:<region>:<account-id>:key/<key-id>"
    }
  ]
}
```

4. Đặt tên policy: `allow-decrypt-kms`
5. Lưu policy

---

### 7. Kiểm Tra Function

- Deploy và chạy test event
- **Kết quả mong đợi trong log:**
  - Dòng 1: giá trị đã mã hóa (Base64) của `DB_PASSWORD`
  - Dòng 2: giá trị đã giải mã ở dạng văn bản (`super_secret`)
  - Kết quả trả về: `"great"`

---

## Các Khái Niệm Quan Trọng

| Khái niệm | Giải thích |
|---|---|
| **KMS** | AWS Key Management Service — dịch vụ quản lý khóa mã hóa |
| **Encryption at rest** | Dữ liệu được mã hóa khi lưu trữ, không chỉ trong quá trình truyền |
| **EncryptionContext** | Metadata dùng để gắn mã hóa với một tài nguyên cụ thể (ví dụ: tên Lambda function) |
| **IAM Inline Policy** | Policy được gắn trực tiếp vào một role, không dùng lại được |
| **boto3** | AWS SDK dành cho Python |
| **kms:Decrypt** | Quyền IAM cần thiết để giải mã dữ liệu được mã hóa bằng KMS |

---

## Thực Hành Bảo Mật Tốt Nhất

- **Không bao giờ hardcode thông tin xác thực** vào mã nguồn.
- **Dùng biến môi trường được mã hóa KMS** cho thông tin bí mật trong Lambda.
- **Áp dụng nguyên tắc quyền tối thiểu** — chỉ cấp `kms:Decrypt` trên đúng key ARN cần thiết.
- Cân nhắc dùng **AWS Secrets Manager** hoặc **SSM Parameter Store** cho việc quản lý bí mật phức tạp hơn.

---

## Lỗi Thường Gặp & Cách Khắc Phục

| Lỗi | Nguyên nhân | Cách khắc phục |
|---|---|---|
| `Task timed out` | Timeout mặc định 3s quá ngắn cho lệnh gọi KMS | Tăng timeout lên 10s trở lên |
| `AccessDeniedException` | Lambda role thiếu quyền `kms:Decrypt` | Thêm inline policy với `kms:Decrypt` trên ARN của key |

---

## Tóm Tắt

1. Lưu thông tin nhạy cảm dưới dạng **biến môi trường được mã hóa** bằng KMS.
2. Dùng **KMS SDK decrypt call** trong code Lambda để đọc giá trị khi chạy.
3. Đảm bảo **IAM role** của Lambda có quyền `kms:Decrypt` trên đúng key.
4. Cách này đảm bảo thông tin xác thực **không bao giờ hiển thị** dưới dạng văn bản thuần trong code hay console.
