# AWS SES – Dịch Vụ Email Đơn Giản

## Tổng Quan

**Amazon SES (Simple Email Service)** là một trong những dịch vụ đơn giản nhất trong AWS. Nó được thiết kế chuyên biệt để **gửi và nhận email**.

---

## Tính Năng Chính

- **Gửi email** thông qua:
  - Giao thức SMTP
  - AWS SDK

- **Nhận email** và tích hợp với các dịch vụ AWS khác:
  - Amazon S3
  - Amazon SNS
  - AWS Lambda

- Sử dụng **IAM permissions** để kiểm soát truy cập, tích hợp hoàn toàn với SES.

---

## Khi Nào Dùng SES?

| Tình huống | Dùng SES? |
|---|---|
| Cần gửi email giao dịch hoặc marketing | ✅ Có |
| Cần nhận và xử lý email đến | ✅ Có |
| Thông báo không liên quan đến email | ❌ Không |

---

## Mẹo Thi

> **SES = Email**

- Nếu câu hỏi thi đề cập đến **email**, SES rất có thể là đáp án đúng.
- Chú ý — đề thi có thể cố tình đánh lừa bạn dùng SES cho các tình huống không phải email.
- Nhớ: SES **chỉ** dùng cho việc gửi và nhận email.

---

## Tóm Tắt Nhanh

| Thuộc tính | Chi tiết |
|---|---|
| Tên đầy đủ | Simple Email Service |
| Trường hợp sử dụng | Gửi & nhận email |
| Giao diện | SMTP hoặc AWS SDK |
| Tích hợp | S3, SNS, Lambda |
| Kiểm soát truy cập | IAM permissions |

---

## Dịch Vụ Liên Quan

- **SNS** – Simple Notification Service (thông báo đẩy, SMS, v.v.)
- **S3** – Có thể lưu trữ nội dung email đã nhận
- **Lambda** – Có thể kích hoạt hàm khi nhận email
