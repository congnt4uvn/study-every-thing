# AWS S3 Bucket Key với Mã hóa SSE-KMS

## Tổng Quan

AWS S3 Bucket Key là một tính năng giúp tối ưu hóa đáng kể việc sử dụng **SSE-KMS** (Mã hóa phía máy chủ với AWS Key Management Service) cho Amazon S3.

---

## Vấn Đề Cần Giải Quyết

Khi bật SSE-KMS trên S3, **mỗi lần mã hóa/giải mã một đối tượng** đều yêu cầu một lệnh gọi API đến AWS KMS để tạo khóa dữ liệu. Ở quy mô lớn, điều này dẫn đến:

- **Số lượng lệnh gọi KMS API rất cao**
- **Chi phí lớn** từ việc sử dụng KMS
- Nguy cơ vượt quá **giới hạn tốc độ yêu cầu KMS**

---

## Cách Hoạt Động của S3 Bucket Key

Thay vì gọi KMS cho mọi đối tượng, S3 Bucket Key giới thiệu một lớp khóa trung gian:

```
AWS KMS (Customer Master Key - CMK)
        │
        ▼  (chỉ gọi thỉnh thoảng)
  S3 Bucket Key  ◄─── được tạo và xoay vòng định kỳ
        │
        ▼  (dùng cho nhiều đối tượng)
  Khóa Dữ Liệu  ──► Mã hóa từng đối tượng S3
```

1. AWS KMS sử dụng **Customer Master Key (CMK)** để tạo ra một **S3 Bucket Key** thỉnh thoảng một lần.
2. S3 Bucket Key được **xoay vòng định kỳ** (không phải mỗi đối tượng).
3. S3 Bucket Key sau đó tạo ra các **khóa dữ liệu** cục bộ bằng kỹ thuật **envelope encryption** để mã hóa các đối tượng S3.
4. Điều này làm giảm đáng kể số lần gọi trực tiếp đến KMS.

---

## Lợi Ích Chính

| Lợi Ích | Chi Tiết |
|---|---|
| **Giảm 99% lệnh gọi KMS API** | S3 xử lý mã hóa cục bộ bằng Bucket Key |
| **Giảm chi phí lên đến 99%** | Giá KMS tính theo khối lượng lệnh gọi API |
| **Không giảm bảo mật** | Độ mạnh mã hóa vẫn được đảm bảo như cũ |
| **Ít sự kiện CloudTrail hơn** | Hoạt động KMS ít hơn đồng nghĩa ít log KMS trong CloudTrail |

---

## Lưu Ý Quan Trọng

- S3 Bucket Key sử dụng **envelope encryption** để tạo nhiều khóa dữ liệu cục bộ.
- Bạn sẽ thấy **ít sự kiện liên quan KMS trong AWS CloudTrail** hơn — đây là hành vi bình thường, không phải mất khả năng giám sát.
- Tính năng này đặc biệt được khuyến nghị khi sử dụng **SSE-KMS ở quy mô lớn** với lưu lượng đối tượng cao.
- Tính năng có thể bật ở **cấp độ bucket** trong S3 Console.

---

## Cách Bật (S3 Console)

1. Truy cập **AWS S3 Console**.
2. Tạo bucket mới hoặc mở bucket hiện có.
3. Trong phần **Default encryption**, chọn **SSE-KMS**.
4. Bật tùy chọn **Bucket Key**.
5. Lưu thay đổi.

---

## Các Khái Niệm Cần Nhớ

| Thuật Ngữ | Mô Tả |
|---|---|
| **SSE-KMS** | Mã hóa phía máy chủ sử dụng khóa AWS KMS |
| **CMK** | Customer Master Key — khóa gốc được quản lý trong KMS |
| **S3 Bucket Key** | Khóa trung gian được tạo từ CMK, dùng để tạo khóa dữ liệu cục bộ |
| **Khóa Dữ Liệu (Data Key)** | Khóa thực sự dùng để mã hóa từng đối tượng S3 |
| **Envelope Encryption** | Kỹ thuật mã hóa khóa dữ liệu bằng một khóa khác (Bucket Key) |
| **CloudTrail** | Dịch vụ AWS ghi lại hoạt động API, bao gồm các lệnh gọi KMS |

---

## Tóm Tắt

> **S3 Bucket Key** là giải pháp tối ưu cho SSE-KMS, giúp giảm lệnh gọi KMS API lên đến **99%**, giảm đáng kể chi phí và nguy cơ vượt giới hạn tốc độ — tất cả mà không ảnh hưởng đến bảo mật.

---

*Chủ đề: AWS S3 | Mã hóa | KMS | Tối ưu Chi phí*
