# Sử Dụng IAM Roles với EC2 Instances - Hướng Dẫn Thực Hành

## Tổng Quan

Hướng dẫn này trình bày cách đúng đắn để cung cấp AWS credentials cho các EC2 instances bằng cách sử dụng IAM roles, thay vì hardcode access keys trực tiếp trên instance.

## Yêu Cầu Trước

- Tài khoản AWS với EC2 instance đang chạy
- Kiến thức cơ bản về IAM roles và policies
- Quyền truy cập EC2 Instance Connect hoặc SSH

## Kết Nối Đến EC2 Instance

Có nhiều cách để kết nối đến EC2 instance:

- **SSH** - Sử dụng terminal hoặc command line
- **EC2 Instance Connect** - Kết nối qua trình duyệt
- **PuTTY** - Dành cho người dùng Windows

Trong hướng dẫn này, chúng ta sẽ sử dụng **EC2 Instance Connect** vì nó đơn giản hơn và hoạt động trực tiếp trên trình duyệt web.

Sau khi kết nối, bạn sẽ thấy dấu nhắc tương tự như:
```
ec2-user@<private-ip>
```

## Kiểm Tra Các Lệnh Linux Cơ Bản

Bạn có thể xác minh kết nối bằng cách chạy các lệnh Linux cơ bản:

```bash
ping google.com
```

Nhấn `Ctrl + C` để dừng lệnh ping.

Để xóa màn hình:
```bash
clear
```

## AWS CLI trên Amazon Linux

Amazon Linux AMI đi kèm với AWS CLI được cài đặt sẵn, vì vậy bạn có thể ngay lập tức bắt đầu sử dụng các lệnh AWS.

## ❌ Cách Làm Sai: Sử Dụng AWS Configure

Bạn có thể bị cám dỗ để chạy:

```bash
aws iam list-users
```

Lệnh này sẽ trả về lỗi về việc không thể xác định credentials, và gợi ý bạn chạy `aws configure`.

### **KHÔNG BAO GIỜ LÀM ĐIỀU NÀY!**

Chạy `aws configure` và nhập Access Key ID và Secret Access Key cá nhân của bạn trực tiếp trên EC2 instance là một **thực hành bảo mật rất tệ**.

### Tại Sao Điều Này Nguy Hiểm:

- Bất kỳ ai có quyền truy cập vào tài khoản AWS của bạn đều có thể kết nối đến EC2 instance
- Họ có thể lấy được credentials đã lưu trữ của bạn
- IAM credentials cá nhân của bạn có thể bị xâm phạm

> **Nguyên Tắc Vàng**: Không bao giờ, không bao giờ, không bao giờ nhập IAM API keys (Access Key ID và Secret Access Key) vào EC2 instance.

## ✅ Cách Làm Đúng: Sử Dụng IAM Roles

### Bước 1: Tạo IAM Role

1. Vào IAM console
2. Điều hướng đến **Roles**
3. Tạo một role (ví dụ: `DemoRoleForEC2`)
4. Gắn policy cần thiết (ví dụ: `IAMReadOnlyAccess`)

### Bước 2: Gắn IAM Role vào EC2 Instance

1. Vào EC2 instance của bạn
2. Điều hướng đến tab **Security**
3. Bạn sẽ thấy hiện tại chưa có IAM role nào được gắn
4. Nhấp vào **Actions** → **Security** → **Modify IAM role**
5. Chọn IAM role của bạn (ví dụ: `DemoRoleForEC2`)
6. Nhấp **Save**

### Bước 3: Xác Minh Role Đang Hoạt Động

Quay lại tab **Security** và xác nhận IAM role đã được gắn.

Bây giờ, trong terminal EC2 instance của bạn, chạy:

```bash
aws iam list-users
```

**Thành công!** Bạn sẽ thấy phản hồi với danh sách IAM users, mặc dù bạn chưa bao giờ chạy `aws configure`.

## Kiểm Tra Quyền Của Role

### Gỡ Bỏ Quyền

1. Vào IAM role trong console
2. Tách policy `IAMReadOnlyAccess`
3. Chạy lại lệnh trong EC2 instance:

```bash
aws iam list-users
```

Bạn sẽ nhận được lỗi **Access Denied**, chứng minh role được liên kết trực tiếp với EC2 instance.

### Gắn Lại Quyền

1. Quay lại IAM và gắn lại policy `IAMReadOnlyAccess`
2. Chạy lại lệnh

**Lưu ý**: Bạn có thể nhận được lỗi access denied ban đầu. Các thay đổi IAM có thể mất một chút thời gian để lan truyền. Thử chạy lại lệnh sau vài giây, và bạn sẽ thấy kết quả mong đợi.

## Điểm Quan Trọng Cần Nhớ

- ✅ **Luôn sử dụng IAM roles** để cung cấp credentials cho EC2 instances
- ❌ **Không bao giờ sử dụng `aws configure`** để lưu trữ credentials cá nhân trên EC2 instances
- 🔒 IAM roles cung cấp quản lý credentials tạm thời và tự động
- ⏱️ Các thay đổi IAM policy có thể mất vài phút để lan truyền

## Thực Hành Tốt Nhất

1. Tạo các IAM roles cụ thể cho các mục đích EC2 instance khác nhau
2. Tuân theo nguyên tắc đặc quyền tối thiểu - chỉ cấp quyền cần thiết
3. Thường xuyên kiểm tra quyền của IAM role
4. Sử dụng IAM roles cho tất cả xác thực giữa các AWS resources

## Kết Luận

Sử dụng IAM roles cho EC2 instances là cách an toàn và được khuyến nghị để cung cấp AWS credentials. Phương pháp này đảm bảo credentials là tạm thời, tự động xoay vòng, và không bao giờ bị lộ trên chính instance.

---

*Hướng dẫn thực hành này trình bày các thực hành bảo mật AWS thiết yếu để quản lý credentials trong EC2 instances.*