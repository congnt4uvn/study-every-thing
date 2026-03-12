# Hướng Dẫn AWS CloudFormation Outputs

## Tổng Quan

Phần outputs trong AWS CloudFormation là một tính năng tùy chọn nhưng rất mạnh mẽ, cho phép bạn khai báo các giá trị đầu ra từ stack của mình. Các outputs này cho phép bạn:

- Xuất các giá trị có thể được import vào các stack khác
- Liên kết các CloudFormation stack khác nhau với nhau
- Xem các giá trị trong AWS Console hoặc qua CLI
- Cho phép cộng tác giữa các nhóm và stack

## Tại Sao Sử Dụng Outputs?

Outputs đặc biệt hữu ích khi bạn muốn:

1. **Liên Kết Các Stack**: Tạo một network stack xuất VPC ID, sau đó có thể được tham chiếu bởi application stack
2. **Xem Các Giá Trị Quan Trọng**: Hiển thị thông tin quan trọng như VPC IDs và Subnet IDs trong console
3. **Cho Phép Cộng Tác Cross-Stack**: Cho phép các nhóm khác nhau quản lý stack của riêng họ trong khi chia sẻ các tài nguyên cần thiết
4. **Tái Sử Dụng Tài Nguyên**: Tham chiếu các tài nguyên được tạo trong một stack từ stack khác

## Cú Pháp Output

Đây là ví dụ về việc tạo output cho một SSH Security Group:

```yaml
Outputs:
  SSHSecurityGroupOutput:
    Description: SSH Security Group ID
    Value: !Ref SSHSecurityGroup
    Export:
      Name: SSHSecurityGroup
```

### Các Thành Phần Chính:

- **Value**: Tham chiếu đến tài nguyên bạn muốn xuất ra (trong trường hợp này là SSH Security Group)
- **Export Block**: Làm cho giá trị có thể được import trong các stack khác
- **Export Name**: Phải là duy nhất trong tất cả các exports trong một region cụ thể

## Import Outputs Từ Các Stack Khác

Để sử dụng một giá trị đã được export từ stack khác, sử dụng hàm `ImportValue`:

```yaml
Resources:
  MyEC2Instance:
    Type: AWS::EC2::Instance
    Properties:
      SecurityGroups:
        - !ImportValue SSHSecurityGroup
```

Trong ví dụ này:
- EC2 instance import giá trị security group từ stack khác
- Hàm `ImportValue` tham chiếu đến tên export từ stack đầu tiên

## Những Điều Quan Trọng Cần Lưu Ý

### Phụ Thuộc Stack

Khi bạn liên kết các stack sử dụng outputs và imports:

- **Bạn không thể xóa stack đang export** cho đến khi tất cả các stack đang import không còn tham chiếu đến các giá trị đã export của nó
- Điều này tạo ra một chuỗi phụ thuộc bảo vệ các tài nguyên quan trọng khỏi bị xóa nhầm

### Tính Duy Nhất Của Export Name

- Tên export phải là duy nhất trong một region
- Chọn các tên mô tả rõ ràng cho biết tài nguyên nào đang được export
- Xem xét sử dụng quy ước đặt tên cho tổ chức của bạn

## Best Practices (Thực Hành Tốt Nhất)

1. **Định Nghĩa Export Rõ Ràng**: Export các tài nguyên thường được các stack khác cần (VPC IDs, Subnet IDs, Security Groups, v.v.)
2. **Sử Dụng Tên Mô Tả**: Làm cho tên export tự giải thích
3. **Ghi Chép Phụ Thuộc**: Theo dõi stack nào phụ thuộc vào export nào
4. **Mẫu Network Stack**: Tạo một network stack chuyên dụng xuất các tài nguyên mạng cho các application stack sử dụng

## Ví Dụ: Network Stack Với Exports

```yaml
# network-stack.yaml
Resources:
  MyVPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16

  SSHSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: SSH Security Group
      VpcId: !Ref MyVPC

Outputs:
  VPCId:
    Description: VPC ID
    Value: !Ref MyVPC
    Export:
      Name: NetworkStack-VPC-ID

  SSHSecurityGroupId:
    Description: SSH Security Group ID
    Value: !Ref SSHSecurityGroup
    Export:
      Name: SSHSecurityGroup
```

## Ví Dụ: Application Stack Import Các Giá Trị

```yaml
# app-stack.yaml
Resources:
  MyEC2Instance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: ami-12345678
      InstanceType: t2.micro
      SecurityGroups:
        - !ImportValue SSHSecurityGroup
      SubnetId: !ImportValue NetworkStack-Subnet-ID
```

## Tóm Tắt

CloudFormation outputs cung cấp một cơ chế mạnh mẽ để:
- Tạo các infrastructure template có tính module hóa và tái sử dụng
- Cho phép cộng tác nhóm thông qua việc tách biệt stack
- Bảo vệ các tài nguyên quan trọng thông qua quản lý phụ thuộc
- Xem các định danh tài nguyên quan trọng một cách dễ dàng

Bằng cách sử dụng outputs một cách hiệu quả, bạn có thể xây dựng các giải pháp infrastructure-as-code dễ bảo trì và cộng tác hơn.