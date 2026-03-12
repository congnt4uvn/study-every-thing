# Hướng Dẫn Về Resources Trong AWS CloudFormation

## Giới Thiệu Về CloudFormation Resources

Resources (Tài nguyên) là thành phần cốt lõi của các template CloudFormation và đại diện cho **phần bắt buộc duy nhất** trong toàn bộ template CloudFormation của bạn. Các resources này đại diện cho các thành phần AWS khác nhau sẽ được tạo và cấu hình như một phần của template.

## Đặc Điểm Chính

- Resources được khai báo và có thể tham chiếu lẫn nhau
- AWS tự động xử lý việc tạo, cập nhật và xóa các resources
- Hiện tại có hơn 700 loại resources khả dụng
- Số lượng các loại resources luôn tăng lên

## Định Danh Loại Resource

Định danh loại resource tuân theo định dạng:

```
service-provider::service-name::data-type-name
```

**Ví dụ:** `AWS::EC2::Instance`

## Tìm Tài Liệu Về Resources

AWS cung cấp tài liệu đầy đủ cho tất cả các resources CloudFormation. Bạn có thể tìm tài liệu resources thông qua:

1. Duyệt tất cả các resources CloudFormation có thể có trên trang tài liệu AWS
2. Chọn các loại resources cụ thể (ví dụ: Amazon Kinesis, Amazon EC2)
3. Điều hướng đến tài liệu resources cụ thể

### Cấu Trúc Tài Liệu

Tài liệu bao gồm:

- **Cú pháp** ở cả định dạng JSON và YAML
- **Properties** (Thuộc tính) dưới dạng các cặp key-value
- **Chi tiết thuộc tính** với thông tin click-through
- **Giá trị trả về**
- **Ví dụ** ở cả YAML và JSON
- **Liên kết tham khảo bổ sung**

## Hiểu Về Các Thuộc Tính Resources

### Ví Dụ: EC2 Instance

Đối với resource `AWS::EC2::Instance`, bạn có thể chỉ định các thuộc tính như:

- `AvailabilityZone` (Vùng khả dụng)
- `ImageId` (ID của AMI)
- `InstanceType` (Loại instance)
- `SecurityGroups` (Nhóm bảo mật - dưới dạng mảng chuỗi)
- `IamInstanceProfile` (Hồ sơ IAM - tùy chọn)

### Đặc Điểm Của Thuộc Tính

Tài liệu của mỗi thuộc tính bao gồm:

- Trạng thái **Bắt buộc/Tùy chọn**
- **Kiểu dữ liệu** (String, Array, v.v.)
- **Hành vi cập nhật**:
  - Không gián đoạn
  - Yêu cầu thay thế
  - Yêu cầu dừng/khởi động

**Ví dụ:** Thay đổi `ImageId` (AMI ID) yêu cầu thay thế, trong khi thêm `IamInstanceProfile` không yêu cầu gián đoạn.

## Làm Việc Với Các Loại Resources Khác Nhau

### Ví Dụ EC2 Instance

```yaml
Type: AWS::EC2::Instance
Properties:
  AvailabilityZone: us-east-1a
  ImageId: ami-xxxxxxxxx
  InstanceType: t2.micro
  SecurityGroups:
    - !Ref SSHSecurityGroup
```

### Security Groups (Nhóm Bảo Mật)

Security groups được chỉ định dưới dạng mảng các chuỗi chứa tên của các security groups.

### Elastic IP

Đối với các resources như Elastic IP, bạn có thể:

1. Tìm kiếm "elastic IP cloudformation" trong tài liệu AWS
2. Tìm trang tài liệu chính xác
3. Xem phần ví dụ để có hướng dẫn triển khai

## Thực Hành Tốt Nhất

1. **Đọc tài liệu** - Tất cả cấu hình console thường có thể được chỉ định thông qua CloudFormation
2. **Sử dụng tham chiếu** - Resources có thể tham chiếu lẫn nhau bằng `!Ref` hoặc `!GetAtt`
3. **Kiểm tra yêu cầu thuộc tính** - Hiểu thuộc tính nào là bắt buộc và tùy chọn
4. **Xem xét hành vi cập nhật** - Biết tác động của việc thay đổi thuộc tính đối với resources hiện có

## Câu Hỏi Thường Gặp

### Tôi có thể tạo số lượng resources động không?

**Trả lời:** Có, bạn có thể sử dụng CloudFormation Macros và Transform, mặc dù đây là chủ đề nâng cao. Theo mặc định, mọi thứ bạn viết trong template là những gì được tạo - bạn không thể tạo resources động mà không có các tính năng nâng cao này.

### Có phải mọi dịch vụ AWS đều được hỗ trợ không?

**Trả lời:** Hầu hết các dịch vụ đều được hỗ trợ. Chỉ một số ít thứ chưa có sẵn. Đối với các dịch vụ chưa được hỗ trợ, bạn có thể giải quyết hạn chế này bằng cách sử dụng **CloudFormation Custom Resources**.

## Điểm Chính Cần Nhớ

- Resources là phần bắt buộc cốt lõi của template CloudFormation
- Có hơn 700 loại resources khả dụng và đang phát triển
- Tồn tại tài liệu đầy đủ cho tất cả các loại resources
- Thuộc tính có thể là bắt buộc hoặc tùy chọn
- Hành vi cập nhật khác nhau tùy theo thuộc tính
- Custom Resources có thể mở rộng khả năng của CloudFormation

## Kết Luận

Hiểu cách tạo resources và điều hướng tài liệu là điều cần thiết để làm việc với CloudFormation. Với kiến thức về cú pháp resources, thuộc tính và cấu trúc tài liệu, bạn có thể xây dựng và quản lý hạ tầng AWS dưới dạng mã một cách hiệu quả.