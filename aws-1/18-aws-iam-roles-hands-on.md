# AWS IAM Roles - Thực Hành

## Giới Thiệu

Trong bài thực hành này, chúng ta sẽ thực hành sử dụng IAM roles trong AWS. Roles là một cách thiết yếu để cấp quyền cho các thực thể AWS thực hiện các hành động trên các dịch vụ AWS.

## Truy Cập IAM Roles

1. Trong bảng điều khiển AWS IAM, nhấp vào **Roles** ở menu bên trái
2. Bạn có thể thấy một số roles đã được tạo sẵn cho tài khoản của bạn (2 hoặc nhiều hơn - điều này không quan trọng)

## Tạo IAM Role Mới

### Bước 1: Chọn Loại Role

Chúng ta sẽ tạo role của riêng mình. Có năm loại role khác nhau bạn có thể tạo, nhưng loại quan trọng nhất cho bài thực hành và kỳ thi là:

- **AWS Service Role** - Cho phép các dịch vụ AWS thực hiện các hành động thay mặt bạn

### Bước 2: Chọn Dịch Vụ

Trong hướng dẫn này, chúng ta sẽ tạo một role cho **EC2 instance**:

1. Chọn **EC2** từ các dịch vụ thường dùng (bạn cũng sẽ thấy Lambda và roles cho hầu hết mọi dịch vụ trên AWS)
2. Chọn use case: **EC2**
3. Bỏ qua các tùy chọn khác
4. Nhấp **Next**

### Bước 3: Gắn Policy Quyền

Bây giờ chúng ta cần gắn một policy để xác định role này sẽ có quyền gì:

1. Tìm kiếm và chọn **IAMReadOnlyAccess**
2. Policy này cho phép EC2 instance đọc thông tin từ IAM
3. Nhấp **Next**

### Bước 4: Cấu Hình Chi Tiết Role

1. Nhập tên role: `DemoRoleForEC2`
2. Xem lại phần **Trusted entities**:
   - Phần này cho thấy role có thể được sử dụng bởi dịch vụ EC2
   - Đây là điều xác định nó như một role cho Amazon EC2
3. Xác minh quyền hiển thị **IAMReadOnlyAccess**
4. Nhấp **Create role**

## Xác Minh

Sau khi tạo:
- Role sẽ xuất hiện trong danh sách roles của bạn
- Bạn có thể xác minh rằng các quyền đã được cấu hình chính xác cho role này
- Role hiện đã sẵn sàng để gắn vào các EC2 instances

## Lưu Ý Quan Trọng

- Chúng ta không thể sử dụng role này ngay lập tức trong phần này
- Chúng ta sẽ áp dụng role này cho EC2 instance khi đến phần EC2 của khóa học
- Đây là một mô hình rất phổ biến trong AWS và quan trọng để hiểu cho kỳ thi

## Tóm Tắt

Bạn đã học cách:
- Tạo một IAM role cho Amazon EC2
- Gắn các quyền phù hợp cho role
- Xác minh cấu hình role

Role này sẽ được sử dụng trong các bài giảng sắp tới khi chúng ta làm việc với EC2 instances.