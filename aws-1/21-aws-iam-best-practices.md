# Các Phương Pháp Hay Nhất cho AWS IAM

## Tổng Quan

Tài liệu này bao gồm các hướng dẫn chung và phương pháp hay nhất cho AWS Identity and Access Management (IAM) để giúp bạn tránh các lỗi phổ biến khi sử dụng AWS.

## Các Phương Pháp Hay Nhất

### 1. Sử Dụng Tài Khoản Root

- **Không sử dụng tài khoản root** ngoại trừ khi bạn thiết lập tài khoản AWS
- Đến bây giờ bạn nên có hai tài khoản:
  - Một tài khoản root
  - Tài khoản cá nhân của riêng bạn

### 2. Một Người Dùng Cho Mỗi Người Thực

- Hãy nhớ: **Một người dùng AWS tương đương với một người thực**
- Nếu bạn bè muốn sử dụng AWS, đừng đưa thông tin đăng nhập của bạn cho họ
- Thay vào đó, hãy tạo một người dùng khác cho họ

### 3. Nhóm Người Dùng và Quyền

- Gán người dùng vào các nhóm
- Gán quyền cho nhóm để đảm bảo bảo mật được quản lý ở cấp độ nhóm
- Tạo một chính sách mật khẩu mạnh

### 4. Xác Thực Đa Yếu Tố (MFA)

- Sử dụng và thực thi MFA để đảm bảo rằng tài khoản của bạn được an toàn khỏi tin tặc
- MFA cung cấp một lớp bảo mật bổ sung

### 5. IAM Roles cho các Dịch Vụ AWS

- Tạo và sử dụng roles bất cứ khi nào bạn cấp quyền cho các dịch vụ AWS
- Điều này bao gồm các EC2 instances (máy chủ ảo)

### 6. Bảo Mật Access Keys

- Nếu bạn sử dụng AWS theo chương trình hoặc sử dụng CLI/SDK, bạn phải tạo access keys
- Access keys giống như mật khẩu - chúng rất bí mật
- Giữ chúng cho riêng bạn

### 7. Kiểm Tra Quyền của Bạn

- Sử dụng **IAM Credentials Report** để kiểm tra quyền
- Sử dụng tính năng **IAM Access Advisor** để xem xét các mẫu truy cập

### 8. Không Bao Giờ Chia Sẻ Thông Tin Đăng Nhập

- **Không bao giờ, không bao giờ, không bao giờ chia sẻ người dùng IAM và access keys của bạn**
- Điều này rất quan trọng cho bảo mật tài khoản

## Kết Luận

Tuân thủ các phương pháp hay nhất về IAM này sẽ giúp đảm bảo tài khoản AWS của bạn luôn an toàn và được quản lý đúng cách. Những hướng dẫn này tạo nền tảng cho bảo mật AWS.