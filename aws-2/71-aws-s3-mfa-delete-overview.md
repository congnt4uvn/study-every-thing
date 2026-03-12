# Tổng Quan về AWS S3 MFA Delete

## Giới Thiệu

MFA Delete là một tính năng bảo mật trong Amazon S3 cung cấp thêm một lớp bảo vệ cho các thao tác quan trọng trên bucket. MFA là viết tắt của **Multi-Factor Authentication** (Xác thực Đa Yếu Tố), yêu cầu người dùng phải tạo mã code trên thiết bị vật lý hoặc ảo trước khi thực hiện các hành động có tính phá hủy nhất định.

## MFA Delete là gì?

MFA Delete bắt buộc người dùng phải cung cấp mã xác minh từ một thiết bị xác thực trước khi thực thi các thao tác quan trọng trên S3 bucket. Thiết bị xác thực này có thể là:

- Điện thoại di động với ứng dụng xác thực (ví dụ: Google Authenticator)
- Thiết bị phần cứng MFA
- Bất kỳ thiết bị tạo mã token MFA tương thích nào khác

Mã code được tạo ra phải được nhập vào Amazon S3 trước khi hệ thống cho phép thao tác được tiếp tục.

## Khi Nào Cần MFA?

### Các Thao Tác Yêu Cầu MFA:

1. **Xóa vĩnh viễn một phiên bản đối tượng** - Cung cấp bảo vệ chống lại việc xóa vĩnh viễn do nhầm lẫn hoặc ác ý
2. **Tạm ngừng Versioning trên bucket** - Đây là thao tác phá hủy loại bỏ tính năng bảo vệ phiên bản

### Các Thao Tác KHÔNG Yêu Cầu MFA:

1. **Bật Versioning** - Đây là hành động bảo vệ, không phải phá hủy
2. **Liệt kê các phiên bản đã xóa** - Đây là thao tác chỉ đọc

## Điều Kiện Tiên Quyết và Yêu Cầu

Để sử dụng MFA Delete, bạn phải:

1. **Bật Versioning** trên bucket trước - MFA Delete liên quan trực tiếp đến tính năng Versioning
2. **Sử dụng tài khoản root** - Chỉ chủ sở hữu bucket (tài khoản root) mới có thể bật hoặc tắt MFA Delete

## Những Lưu Ý Quan Trọng

- Việc sử dụng tài khoản root không được khuyến khích cho các thao tác thường xuyên, nhưng lại bắt buộc để quản lý cài đặt MFA Delete
- MFA Delete cung cấp thêm một lớp bảo vệ được thiết kế đặc biệt để ngăn chặn việc xóa vĩnh viễn các phiên bản đối tượng
- Cả việc xóa vĩnh viễn đối tượng và tạm ngừng versioning đều được coi là các thao tác phá hủy, đó là lý do tại sao chúng yêu cầu xác thực MFA

## Tóm Tắt

MFA Delete là một tính năng bảo mật thiết yếu bổ sung xác thực đa yếu tố cho các thao tác quan trọng trên S3 bucket. Bằng cách yêu cầu mã xác thực dựa trên thời gian cho các hành động phá hủy như xóa vĩnh viễn đối tượng và tạm ngừng versioning, nó giảm đáng kể nguy cơ mất dữ liệu do nhầm lẫn hoặc truy cập trái phép.