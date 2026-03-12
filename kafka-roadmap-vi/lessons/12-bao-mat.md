# Bài 12 — Bảo mật: TLS, SASL, ACLs, quản lý secrets

## Mục tiêu
- Hiểu các lớp bảo mật của Kafka ở mức tổng quan
- Biết mục đích của TLS, SASL, ACLs
- Tránh các lỗi quản lý secrets phổ biến

## Các lớp bảo mật
Bảo mật Kafka thường gồm:
- **Mã hoá khi truyền** (TLS)
- **Xác thực** (SASL như SCRAM, OAUTHBEARER)
- **Phân quyền** (ACLs)

## TLS (mã hoá)
TLS bảo vệ dữ liệu khi truyền và giảm rủi ro MITM.

Ghi chú thực tế:
- TLS tăng độ phức tạp vận hành (vòng đời chứng chỉ)
- Nên chuẩn hoá cấp phát và xoay vòng cert

## SASL (xác thực)
SASL xác nhận client là ai.

Pattern phổ biến:
- SCRAM username/password
- OAuth/JWT tích hợp trong một số môi trường

## ACLs (phân quyền)
ACLs định nghĩa principal nào được:
- Read topic
- Write topic
- Create/alter topic
- Dùng consumer groups

## Vệ sinh secrets
- Không commit credentials lên git
- Tránh nhúng secrets vào container image
- Ưu tiên secret manager và inject lúc runtime

## Thực hành (khái niệm)
Trong cluster thực tế, bạn sẽ:
- Bật TLS
- Yêu cầu SASL
- Tạo ACL least-privilege theo từng app

Với local learning, hãy ưu tiên hiểu mô hình trước khi thêm độ phức tạp.

## Checklist
- Tôi giải thích được TLS vs SASL vs ACLs
- Tôi hiểu vì sao least privilege quan trọng
- Tôi có kế hoạch xử lý secrets an toàn

## Lỗi hay gặp
- Chạy production Kafka ở chế độ PLAINTEXT
- Cấp quyền topic quá rộng cho mọi app
