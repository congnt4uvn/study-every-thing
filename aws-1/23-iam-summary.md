# Tóm Tắt IAM

## Tổng Quan

Tài liệu này cung cấp bản tóm tắt toàn diện về các khái niệm và tính năng chính của AWS Identity and Access Management (IAM).

## IAM Users (Người Dùng IAM)

Người dùng IAM nên được ánh xạ tới những người dùng thực tế trong tổ chức của bạn. Mỗi người dùng sẽ có:

- Mật khẩu để truy cập AWS Console
- Danh tính và thông tin xác thực riêng

## IAM Groups (Nhóm IAM)

Người dùng có thể được tổ chức thành các nhóm để quản lý dễ dàng hơn:

- Nhóm chỉ chứa người dùng
- Policies có thể được gán cho nhóm
- Người dùng kế thừa quyền từ nhóm của họ

## IAM Policies (Chính Sách IAM)

Policies là các tài liệu JSON xác định quyền hạn:

- Có thể được gán cho người dùng hoặc nhóm
- Quy định những hành động nào được phép hoặc bị từ chối
- Xác định mức độ truy cập vào các tài nguyên AWS

## IAM Roles (Vai Trò IAM)

Roles là các danh tính được thiết kế cho:

- Các EC2 instances
- Các dịch vụ AWS khác
- Ứng dụng cần truy cập tài nguyên AWS
- Các tình huống truy cập tạm thời

## Tính Năng Bảo Mật

### Xác Thực Đa Yếu Tố (MFA)

- Bật MFA để tăng cường bảo mật
- Thêm một lớp bảo vệ bổ sung ngoài mật khẩu

### Chính Sách Mật Khẩu

- Đặt các yêu cầu mật khẩu mạnh
- Xác định quy tắc độ phức tạp mật khẩu
- Thực thi việc thay đổi mật khẩu định kỳ

## Phương Thức Truy Cập

### AWS CLI (Giao Diện Dòng Lệnh)

- Quản lý dịch vụ AWS từ dòng lệnh
- Yêu cầu access keys để xác thực

### AWS SDK (Bộ Công Cụ Phát Triển Phần Mềm)

- Quản lý dịch vụ AWS bằng ngôn ngữ lập trình
- Truy cập lập trình vào tài nguyên AWS
- Yêu cầu access keys để xác thực

## Access Keys (Khóa Truy Cập)

Access keys được yêu cầu để sử dụng:

- AWS CLI
- AWS SDK
- Truy cập lập trình vào dịch vụ AWS

## Kiểm Toán và Giám Sát

### IAM Credentials Report (Báo Cáo Thông Tin Xác Thực IAM)

- Tạo báo cáo về việc sử dụng thông tin xác thực
- Xem xét tất cả người dùng IAM và trạng thái thông tin xác thực của họ

### IAM Access Advisor (Cố Vấn Truy Cập IAM)

- Giám sát việc truy cập dịch vụ của người dùng
- Xác định các quyền không được sử dụng
- Tối ưu hóa bảo mật bằng cách tuân theo nguyên tắc đặc quyền tối thiểu

## Kết Luận

IAM là một dịch vụ cơ bản để bảo mật môi trường AWS của bạn. Bằng cách triển khai đúng cách người dùng, nhóm, chính sách, vai trò và các tính năng bảo mật như MFA, bạn có thể duy trì một cơ sở hạ tầng đám mây mạnh mẽ và an toàn.