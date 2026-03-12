# Hướng Dẫn Cấu Hình AWS CLI Access Keys

## Tổng Quan

Hướng dẫn này trình bày cách tạo và cấu hình AWS access keys cho truy cập CLI, bao gồm thiết lập thông tin xác thực AWS CLI và hiểu về quyền IAM.

## Tạo Access Keys

### Bước 1: Truy Cập Security Credentials

1. Click vào tên người dùng của bạn trong AWS Console
2. Chọn **Security credentials** (Thông tin xác thực bảo mật)
3. Cuộn xuống để tìm phần access keys

### Bước 2: Tạo Access Key

1. Click vào **Create access key** (Tạo access key)
2. Chọn trường hợp sử dụng của bạn (ví dụ: truy cập CLI)
3. AWS sẽ đưa ra các khuyến nghị thay thế dựa trên lựa chọn của bạn:
   - Cho CLI: CloudShell (được khuyến nghị)
   - Cho CLI: CLI V2 với xác thực IAM Identity Center
   - Cho ứng dụng code cục bộ chạy bên ngoài AWS
   - Cho ứng dụng chạy trong AWS

> **Lưu ý**: Vì mục đích học tập, chúng ta sẽ tiếp tục với access keys truyền thống để hiểu cách chúng hoạt động, mặc dù có các khuyến nghị khác.

4. Đánh dấu vào ô xác nhận: "I understand the above recommendation" (Tôi hiểu các khuyến nghị trên)
5. Click **Create access key** (Tạo access key)

### Bước 3: Lưu Thông Tin Xác Thực

⚠️ **Quan trọng**: Đây là **lần duy nhất** bạn có thể xem cả hai thông tin:
- Access Key ID
- Secret Access Key

Hãy chắc chắn lưu các thông tin xác thực này một cách an toàn trước khi đóng hộp thoại.

## Cấu Hình AWS CLI

### Cấu Hình Ban Đầu

Mở terminal và chạy lệnh:

```bash
aws configure
```

Bạn sẽ được yêu cầu nhập các thông tin sau:

1. **AWS Access Key ID**: Nhập access key ID của bạn
2. **AWS Secret Access Key**: Nhập secret access key của bạn
3. **Default region name**: Chọn region gần với bạn (ví dụ: `eu-west-1`)
   - Bạn có thể tìm mã region trong menu dropdown region của AWS Console
4. **Default output format**: Nhấn Enter để sử dụng mặc định

### Ví Dụ Cấu Hình

```bash
$ aws configure
AWS Access Key ID [None]: YOUR_ACCESS_KEY_ID
AWS Secret Access Key [None]: YOUR_SECRET_ACCESS_KEY
Default region name [None]: eu-west-1
Default output format [None]: 
```

## Kiểm Tra Cấu Hình

### Xác Minh Quyền Truy Cập CLI

Kiểm tra cấu hình của bạn bằng cách liệt kê các IAM users:

```bash
aws iam list-users
```

Lệnh này sẽ trả về thông tin về tất cả users trong tài khoản của bạn, bao gồm:
- Tên người dùng
- User ID
- ARN (Amazon Resource Name)
- Ngày tạo
- Ngày sử dụng mật khẩu lần cuối

Kết quả từ CLI sẽ tương tự như thông tin hiển thị trong IAM Management Console.

## Hiểu Về Quyền IAM

### Kiểm Tra Thay Đổi Quyền

Để minh họa cách quyền IAM hoạt động:

1. **Xóa user khỏi nhóm admin** (sử dụng tài khoản root):
   - Điều hướng đến IAM Groups
   - Chọn nhóm admin
   - Xóa user của bạn khỏi nhóm

2. **Kiểm tra quyền truy cập trong Management Console**:
   - Refresh trang IAM
   - Bạn sẽ nhận được lỗi cho biết không đủ quyền

3. **Kiểm tra quyền truy cập qua CLI**:
   ```bash
   aws iam list-users
   ```
   - Lệnh sẽ bị từ chối (không có phản hồi)
   - Quyền CLI khớp chính xác với quyền IAM Console

### Khôi Phục Quyền

⚠️ **Quan trọng**: Đừng quên khôi phục quyền của bạn!

1. Vào **IAM Groups**
2. Chọn nhóm **admin**
3. Thêm user của bạn trở lại vào nhóm
4. Quyền administrator của bạn đã được khôi phục

## Những Điểm Chính

- AWS có thể được truy cập thông qua:
  - **Management Console** (giao diện web)
  - **AWS CLI** (giao diện dòng lệnh sử dụng access keys)
  
- Access keys bao gồm:
  - **Access Key ID** (giống như tên người dùng)
  - **Secret Access Key** (giống như mật khẩu)

- **Thực Hành Bảo Mật Tốt Nhất**:
  - Lưu trữ access keys một cách an toàn
  - Không bao giờ chia sẻ secret access key của bạn
  - Xoay vòng access keys thường xuyên
  - Sử dụng IAM roles khi có thể cho các ứng dụng chạy trên AWS

- Quyền CLI giống hệt với quyền Management Console
- IAM policies kiểm soát quyền truy cập cho cả hai giao diện một cách bình đẳng

## Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ khám phá:
- AWS CloudShell như một giải pháp thay thế cho CLI cục bộ
- Các thực hành bảo mật bổ sung
- IAM roles và thông tin xác thực tạm thời

---

*Hướng dẫn này là một phần của loạt bài AWS IAM cơ bản*