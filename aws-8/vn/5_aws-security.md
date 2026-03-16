# Tài Liệu Học AWS Security

> Đây là một trong những phần quan trọng nhất trong kỳ thi — có rất nhiều câu hỏi về bảo mật. Phần này bao gồm các dịch vụ bảo mật AWS theo hướng thực tế, kết hợp thực hành với AWS Lambda.

---

## Mục Lục

1. [Tại Sao Bảo Mật AWS Quan Trọng](#1-tại-sao-bảo-mật-aws-quan-trọng)
2. [AWS KMS – Dịch Vụ Quản Lý Khóa](#2-aws-kms--dịch-vụ-quản-lý-khóa)
3. [Mã Hóa trong AWS](#3-mã-hóa-trong-aws)
4. [AWS Systems Manager – Parameter Store](#4-aws-systems-manager--parameter-store)
5. [AWS Lambda & Tích Hợp Bảo Mật](#5-aws-lambda--tích-hợp-bảo-mật)
6. [Các Dịch Vụ Bảo Mật Quan Trọng Khác](#6-các-dịch-vụ-bảo-mật-quan-trọng-khác)
7. [Mẹo Ôn Thi](#7-mẹo-ôn-thi)

---

## 1. Tại Sao Bảo Mật AWS Quan Trọng

- Bảo mật là **trách nhiệm chung** giữa AWS và khách hàng.
- AWS bảo vệ **hạ tầng** (phần cứng, mạng, cơ sở vật chất).
- Khách hàng chịu trách nhiệm **mọi thứ họ đưa lên đám mây** (dữ liệu, IAM, mã hóa, cấu hình mạng).
- Hầu hết các dịch vụ AWS đều có tích hợp bảo mật.

---

## 2. AWS KMS – Dịch Vụ Quản Lý Khóa

### KMS là gì?
AWS Key Management Service (KMS) giúp **tạo và quản lý khóa mật mã** và kiểm soát việc sử dụng chúng trên các dịch vụ AWS.

### Các Khái Niệm Chính

| Thuật Ngữ | Mô Tả |
|---|---|
| **CMK** (Customer Master Key) | Tài nguyên chính trong KMS; dùng để mã hóa/giải mã dữ liệu |
| **Khóa Đối Xứng** | Một khóa duy nhất dùng cho cả mã hóa và giải mã (AES-256) |
| **Khóa Bất Đối Xứng** | Cặp khóa (công khai/bí mật) dùng để mã hóa/giải mã hoặc ký/xác minh |
| **Data Key** | Được tạo bởi KMS để mã hóa lượng lớn dữ liệu (envelope encryption) |
| **Chính Sách Khóa** | Chính sách dựa trên tài nguyên kiểm soát quyền truy cập vào CMK |

### Các Loại CMK

- **AWS Managed Keys** – AWS tạo và quản lý thay bạn (ví dụ: `aws/s3`)
- **Customer Managed Keys** – Bạn tự tạo, sở hữu và quản lý
- **AWS Owned Keys** – AWS sử dụng nội bộ; bạn không có quyền kiểm soát

### Mã Hóa Phong Bì (Envelope Encryption)

1. KMS tạo ra một **Data Encryption Key (DEK)**
2. Dữ liệu được mã hóa bằng DEK cục bộ
3. Bản thân DEK được mã hóa bởi CMK và lưu trữ cùng với dữ liệu
4. Để giải mã: KMS giải mã DEK → DEK giải mã dữ liệu

### KMS Tích Hợp với Các Dịch Vụ AWS

- **S3** – Mã hóa phía máy chủ với KMS (SSE-KMS)
- **EBS** – Volume được mã hóa bằng CMK
- **RDS** – Cơ sở dữ liệu được mã hóa
- **Lambda** – Mã hóa biến môi trường
- **Secrets Manager / Parameter Store** – Bí mật được mã hóa

### Điểm Quan Trọng Trong Thi

- Khóa KMS mang tính **khu vực** — không thể dùng trực tiếp giữa các region
- Các lệnh gọi API KMS được **kiểm tra qua CloudTrail**
- Bạn có thể **xoay vòng khóa** tự động (hàng năm cho CMK do khách hàng quản lý)
- Phân biệt `GenerateDataKey` và `Encrypt` API

---

## 3. Mã Hóa trong AWS

### Mã Hóa Khi Lưu Trữ (At Rest)

Bảo vệ dữ liệu được lưu trên đĩa:
- S3, EBS, RDS, DynamoDB, Glacier đều hỗ trợ mã hóa khi lưu trữ
- Sử dụng KMS hoặc AES-256

### Mã Hóa Khi Truyền Tải (In Transit)

Bảo vệ dữ liệu di chuyển qua mạng:
- Sử dụng **TLS/SSL** (HTTPS)
- AWS Certificate Manager (ACM) quản lý chứng chỉ TLS
- Bắt buộc qua chính sách bucket (`aws:SecureTransport`) hoặc endpoint HTTPS

### Các Tùy Chọn Mã Hóa S3

| Loại | Mô Tả |
|---|---|
| **SSE-S3** | AWS quản lý khóa bằng AES-256 |
| **SSE-KMS** | Sử dụng CMK của KMS; có nhật ký kiểm tra, xoay khóa |
| **SSE-C** | Khách hàng tự cung cấp khóa mã hóa |
| **Mã Hóa Phía Client** | Mã hóa trước khi tải lên S3 |

---

## 4. AWS Systems Manager – Parameter Store

### Parameter Store là gì?
Là kho lưu trữ phân cấp, bảo mật cho **dữ liệu cấu hình và bí mật** (API key, mật khẩu, chuỗi kết nối).

### Các Cấp Độ

| Cấp | Mô Tả |
|---|---|
| **Standard** | Tối đa 10.000 tham số, không tính phí thêm |
| **Advanced** | Tối đa 100.000 tham số, hỗ trợ chính sách, kích thước giá trị lớn hơn |

### Các Loại Tham Số

- `String` – Văn bản thuần
- `StringList` – Danh sách ngăn cách bằng dấu phẩy
- `SecureString` – Được mã hóa bằng KMS

### Ví Dụ Phân Cấp

```
/myapp/
  /dev/
    db_password      → SecureString
    api_key          → SecureString
  /prod/
    db_password      → SecureString
```

### Tích Hợp
- Dùng với **Lambda**, **EC2**, **ECS** để đưa cấu hình vào runtime
- Kiểm soát truy cập qua **chính sách IAM**
- Mọi truy cập được ghi lại trong **CloudTrail**

### So Sánh Parameter Store và Secrets Manager

| Tính Năng | Parameter Store | Secrets Manager |
|---|---|---|
| Chi Phí | Miễn phí (Standard) | Trả phí theo bí mật |
| Xoay tự động | Thủ công | Tự động (tích hợp RDS) |
| Liên tài khoản | Hạn chế | Hỗ trợ |
| Trường hợp dùng | Cấu hình + bí mật đơn giản | Thông tin xác thực nhạy cảm |

---

## 5. AWS Lambda & Tích Hợp Bảo Mật

### Mã Hóa Biến Môi Trường
- Lambda mã hóa biến môi trường **khi lưu trữ** bằng KMS theo mặc định
- Bạn có thể dùng CMK riêng để kiểm soát bổ sung

### IAM Execution Role
- Mỗi hàm Lambda có một **execution role**
- Cấp quyền truy cập các dịch vụ AWS (S3, DynamoDB, KMS, v.v.)
- Nguyên tắc **đặc quyền tối thiểu** luôn được áp dụng

### Truy Cập Bí Mật từ Lambda

```python
import boto3

ssm = boto3.client('ssm')
secret = ssm.get_parameter(Name='/myapp/prod/db_password', WithDecryption=True)
print(secret['Parameter']['Value'])
```

### Tích Hợp VPC
- Lambda có thể chạy trong **VPC** để truy cập tài nguyên riêng tư
- Yêu cầu cấu hình VPC, subnet và security group

### Lambda & KMS
```python
import boto3, base64

kms = boto3.client('kms')
encrypted = kms.encrypt(KeyId='alias/my-key', Plaintext=b'my-secret')
ciphertext = base64.b64encode(encrypted['CiphertextBlob'])
```

---

## 6. Các Dịch Vụ Bảo Mật Quan Trọng Khác

### AWS IAM
- **Người dùng, Nhóm, Vai trò, Chính sách**
- Ưu tiên dùng **role** thay vì thông tin xác thực dài hạn
- Bật **MFA** cho tất cả người dùng có đặc quyền
- Dùng **IAM Access Analyzer** để phát hiện quyền truy cập công khai/liên tài khoản ngoài ý muốn

### AWS Secrets Manager
- Lưu trữ và **tự động xoay vòng** bí mật (mật khẩu DB, API key)
- Tích hợp gốc với RDS, Redshift, DocumentDB
- Tính phí theo bí mật mỗi tháng

### AWS CloudTrail
- Ghi lại **tất cả lệnh gọi API** trong tài khoản AWS của bạn
- Dùng để kiểm tra bảo mật và tuân thủ
- Tích hợp với CloudWatch để cảnh báo hoạt động đáng ngờ

### AWS Shield
- **Shield Standard** – Bảo vệ DDoS miễn phí cho tất cả khách hàng AWS
- **Shield Advanced** – Có phí; bảo vệ DDoS nâng cao + hỗ trợ DRT 24/7

### AWS WAF (Tường Lửa Ứng Dụng Web)
- Bảo vệ ứng dụng web khỏi các cuộc tấn công phổ biến (SQLi, XSS)
- Gắn vào **CloudFront**, **ALB**, **API Gateway**
- Tạo **Web ACL** với các quy tắc và nhóm quy tắc

### Amazon GuardDuty
- Dịch vụ **phát hiện mối đe dọa** thông minh
- Phân tích CloudTrail, VPC Flow Logs, nhật ký DNS
- Phát hiện: lệnh gọi API bất thường, khai thác tiền điện tử, EC2 bị xâm phạm

### Amazon Macie
- Dùng ML để **khám phá và bảo vệ dữ liệu nhạy cảm** trong S3
- Nhận diện PII, dữ liệu tài chính, thông tin xác thực

---

## 7. Mẹo Ôn Thi

- **KMS mang tính khu vực** — sao chép liên region yêu cầu mã hóa lại
- **CloudTrail** ghi lại mọi lệnh gọi API KMS — quan trọng cho tuân thủ
- Ưu tiên **Secrets Manager** cho thông tin xác thực cần xoay tự động; **Parameter Store** cho cấu hình
- Luôn dùng **IAM role** thay vì access key khi có thể
- `SSE-KMS` cho khả năng kiểm tra; `SSE-S3` đơn giản hơn nhưng ít kiểm soát hơn
- Biến môi trường Lambda nên dùng **KMS** cho giá trị nhạy cảm
- Nắm rõ sự khác biệt: **mã hóa khi lưu trữ** vs **khi truyền tải**
- **GuardDuty** = phát hiện mối đe dọa; **Macie** = khám phá dữ liệu nhạy cảm; **Inspector** = đánh giá lỗ hổng bảo mật

---

*Mẹo học tập: Thực hành tạo khóa KMS, lưu trữ giá trị trong Parameter Store và truy cập chúng từ hàm Lambda trên AWS Console.*
