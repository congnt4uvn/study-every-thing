# AWS KMS – Hạn Mức Yêu Cầu & Xử Lý Throttling

## Tổng Quan

AWS KMS (Key Management Service) là một **dịch vụ nội bộ của AWS** và giống như mọi dịch vụ AWS khác, nó thực thi **hạn mức yêu cầu** (request quotas). Khi vượt quá hạn mức này, bạn sẽ nhận được lỗi `ThrottlingException`.

---

## ThrottlingException

Khi bạn vượt quá hạn mức yêu cầu của KMS, bạn sẽ nhận được lỗi như sau:

```
Status Code: 400
Error Code: ThrottlingException
```

Điều này có nghĩa là bạn đang gọi KMS quá nhanh — nhiều yêu cầu mỗi giây hơn mức hạn mức cho phép.

---

## Cách Hạn Mức KMS Hoạt Động

- Mọi **thao tác mã hóa** (encrypt, decrypt, GenerateDataKey, GenerateRandom, v.v.) đều **dùng chung một hạn mức**.
- Đây là hạn mức **dùng chung theo tài khoản và theo region**.
- Các dịch vụ AWS bên thứ ba hoạt động **thay mặt bạn** cũng tiêu thụ hạn mức này.
  - Ví dụ: **Amazon S3 với SSE-KMS** — mỗi lần S3 dùng khóa KMS của bạn để mã hóa/giải mã một đối tượng, nó sẽ được tính vào hạn mức của bạn.

### Giá Trị Hạn Mức Mặc Định (Symmetric CMK)

| Region | Yêu cầu mỗi giây |
|--------|-----------------|
| Hầu hết các region | 5.500 |
| Một số region | 10.000 |
| Một số region đặc biệt | 30.000 |

> Tất cả các thao tác mã hóa **dùng chung** giá trị hạn mức trên.

---

## Giải Pháp Xử Lý KMS Throttling

Có **3 cách** để xử lý KMS throttling:

### 1. Exponential Backoff *(dành cho throttling tạm thời)*
- Thử lại yêu cầu thất bại với thời gian chờ tăng dần theo cấp số nhân giữa các lần thử.
- Phù hợp khi throttling xảy ra tạm thời hoặc không thường xuyên.

### 2. DEK Caching với Envelope Encryption *(giảm số lần gọi API)*
- Nếu bạn đang dùng API `GenerateDataKey`, hãy bật **bộ nhớ đệm khóa mã hóa dữ liệu (DEK caching)**.
- Lưu DEK **cục bộ** để tái sử dụng cho nhiều thao tác mã hóa/giải mã.
- Điều này giúp giảm đáng kể số lần gọi đến KMS.
- DEK caching là tính năng của **AWS Encryption SDK**.

### 3. Yêu Cầu Tăng Hạn Mức *(khi sử dụng khối lượng lớn liên tục)*
- Nếu bạn liên tục chạm đến giới hạn hạn mức, hãy yêu cầu tăng thông qua:
  - Một **lệnh gọi AWS API**, hoặc
  - Mở **phiếu hỗ trợ** với AWS Support.

---

## Tóm Tắt Chính

| # | Giải Pháp | Khi Nào Nên Dùng |
|---|-----------|-----------------|
| 1 | Exponential Backoff | Throttling tạm thời / không thường xuyên |
| 2 | DEK Caching (Envelope Encryption SDK) | Tần suất mã hóa/giải mã cao |
| 3 | Yêu Cầu Tăng Hạn Mức | Liên tục vượt quá hạn mức |

---

## Các API KMS Liên Quan (Dùng Chung Hạn Mức)

- `Encrypt`
- `Decrypt`
- `GenerateDataKey`
- `GenerateDataKeyWithoutPlaintext`
- `GenerateRandom`
- `ReEncrypt`
- `Sign` / `Verify`

> Tất cả các thao tác trên đều **dùng chung** hạn mức thao tác mã hóa.

---

## Tham Chiếu Nhanh

```
ThrottlingException
    → Dùng Exponential Backoff (tạm thời)
    → Bật DEK Caching qua Encryption SDK (giảm số lần gọi)
    → Yêu Cầu Tăng Hạn Mức qua API / AWS Support (giải pháp lâu dài)
```
