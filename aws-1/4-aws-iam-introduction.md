# AWS IAM - Giới thiệu về Quản lý Danh tính và Truy cập

## Tổng quan

Chào mừng bạn đến với phần tìm hiểu sâu đầu tiên về dịch vụ AWS - **IAM (Identity and Access Management - Quản lý Danh tính và Truy cập)**.

IAM là một **dịch vụ toàn cầu** cho phép bạn tạo người dùng và tổ chức họ thành các nhóm để quản lý quyền truy cập vào tài khoản AWS của bạn.

## Tài khoản Root

Khi bạn tạo một tài khoản AWS, một **tài khoản root** sẽ tự động được tạo ra. Đây là người dùng root của tài khoản với quyền truy cập đầy đủ vào tất cả các dịch vụ và tài nguyên AWS.

### Nguyên tắc quan trọng cho Tài khoản Root:
- ⚠️ Chỉ sử dụng tài khoản root cho việc thiết lập tài khoản ban đầu
- ⚠️ Không sử dụng cho các hoạt động hàng ngày
- ⚠️ Không bao giờ chia sẻ thông tin đăng nhập tài khoản root

## Người dùng và Nhóm

### Người dùng (Users)
- **Người dùng** đại diện cho từng cá nhân trong tổ chức của bạn
- Mỗi người nên có tài khoản IAM user riêng
- Nên tạo người dùng thay vì chia sẻ tài khoản root

### Nhóm (Groups)
Nhóm giúp tổ chức người dùng có vai trò hoặc trách nhiệm tương tự.

**Ví dụ về Cấu trúc Tổ chức:**

Giả sử bạn có 6 người trong tổ chức: Alice, Bob, Charles, David, Edward và Fred.

- **Nhóm Developers**: Alice, Bob, Charles
- **Nhóm Operations**: David, Edward
- **Nhóm Audit**: Charles, David (người dùng có thể thuộc nhiều nhóm)
- **Không có Nhóm**: Fred (không được khuyến nghị, nhưng có thể)

### Quy tắc quan trọng:
- ✅ Nhóm chỉ có thể chứa người dùng, không chứa nhóm khác
- ✅ Người dùng có thể thuộc nhiều nhóm
- ⚠️ Người dùng không nhất thiết phải thuộc nhóm nào (không phải best practice)

## Chính sách IAM (IAM Policies)

Để cho phép người dùng truy cập các dịch vụ AWS, bạn phải cấp quyền cho họ thông qua **Chính sách IAM**.

### Chính sách IAM là gì?
- Một tài liệu JSON định nghĩa các quyền
- Chỉ định người dùng có thể thực hiện hành động gì trên dịch vụ AWS nào
- Có thể được gắn vào người dùng hoặc nhóm

### Ví dụ về Chính sách:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:Describe*",
        "elasticloadbalancing:Describe*",
        "cloudwatch:*"
      ],
      "Resource": "*"
    }
  ]
}
```

Chính sách này cho phép người dùng:
- Sử dụng dịch vụ EC2 (các thao tác mô tả)
- Sử dụng dịch vụ Elastic Load Balancing (các thao tác mô tả)
- Sử dụng dịch vụ CloudWatch (tất cả các thao tác)

## Nguyên tắc Đặc quyền Tối thiểu

AWS tuân theo **nguyên tắc đặc quyền tối thiểu** (principle of least privilege):

- 🔒 Không cấp cho người dùng nhiều quyền hơn mức họ cần
- 🔒 Chỉ cấp quyền truy cập vào các dịch vụ cụ thể mà người dùng yêu cầu
- 🔒 Ngăn chặn rủi ro bảo mật và chi phí không mong muốn

### Tại sao điều này quan trọng:
- Ngăn người dùng vô tình khởi chạy các dịch vụ tốn kém
- Giảm lỗ hổng bảo mật
- Duy trì kiểm soát tốt hơn đối với môi trường AWS của bạn

## Tóm tắt

IAM rất cần thiết cho:
- ✅ Tạo tài khoản người dùng cá nhân
- ✅ Tổ chức người dùng thành các nhóm
- ✅ Quản lý quyền thông qua các chính sách
- ✅ Tuân theo các thực tiễn bảo mật tốt nhất
- ✅ Tránh sử dụng tài khoản root cho hoạt động hàng ngày

## Bước tiếp theo

Trong bài giảng tiếp theo, chúng ta sẽ thực hành:
- Tạo người dùng IAM
- Tạo nhóm IAM
- Gán người dùng vào nhóm
- Gắn chính sách để kiểm soát quyền truy cập