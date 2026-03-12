# AWS CloudFormation Parameters - Tìm Hiểu Sâu

## Giới Thiệu

CloudFormation parameters là một cách mạnh mẽ để cung cấp đầu vào cho các template CloudFormation của bạn. Parameters cho phép người dùng cung cấp giá trị khi tạo hoặc cập nhật stack, giúp template có thể tái sử dụng và linh hoạt trên các môi trường và trường hợp sử dụng khác nhau.

## CloudFormation Parameters Là Gì?

Parameters được định nghĩa như một phần của CloudFormation template và hoạt động như các biến đầu vào. Chúng được giới thiệu sớm trong việc sử dụng CloudFormation, chẳng hạn như khi cung cấp mô tả cho security group. Parameters rất quan trọng cho:

- **Khả Năng Tái Sử Dụng Template**: Cho phép nhiều người dùng trong công ty sử dụng cùng một template với các cấu hình khác nhau
- **Cấu Hình Động**: Xử lý các đầu vào không thể xác định trước
- **Ngăn Ngừa Lỗi**: Cung cấp validation và kiểm tra kiểu dữ liệu để ngăn chặn lỗi cấu hình

## Khi Nào Nên Sử Dụng Parameters

Khi quyết định có nên sử dụng parameter hay không, hãy tự hỏi bản thân:

> **"Cấu hình tài nguyên CloudFormation này có khả năng thay đổi trong tương lai không?"**

Nếu câu trả lời là có, hãy biến nó thành parameter. Cách tiếp cận này có nghĩa là:
- Bạn sẽ không cần tải lại template để thay đổi giá trị
- Người dùng có thể tùy chỉnh template mà không cần sửa đổi mã nguồn
- Cấu hình không thể xác định trước có thể được chỉ định tại thời điểm chạy

## Cài Đặt và Kiểu Dữ Liệu của Parameters

CloudFormation parameters hỗ trợ nhiều cài đặt và kiểu dữ liệu:

### Các Kiểu Parameter
- **String**: Giá trị văn bản đơn giản
- **Number**: Giá trị số
- **CommaDelimitedList**: Danh sách giá trị phân tách bằng dấu phẩy
- **List<Number>**: Danh sách giá trị số
- **AWS-Specific Parameters**: Giúp phát hiện giá trị không hợp lệ cho tài nguyên AWS
- **SSM Parameter**: Tham chiếu đến AWS Systems Manager Parameter Store

### Thuộc Tính của Parameters
- **Description**: Giải thích mục đích của parameter
- **ConstraintDescription**: Mô tả hiển thị khi vi phạm ràng buộc
- **MinLength / MaxLength**: Ràng buộc độ dài chuỗi
- **MinValue / MaxValue**: Ràng buộc giá trị số
- **Default**: Giá trị mặc định nếu không được cung cấp
- **AllowedValues**: Danh sách các giá trị hợp lệ (tạo dropdown)
- **AllowedPattern**: Mẫu regex để validation
- **NoEcho**: Ẩn giá trị parameter trong log và console (cho dữ liệu nhạy cảm)

## Các Ví Dụ Quan Trọng Về Parameters

### 1. AllowedValues - Lựa Chọn Có Kiểm Soát

```yaml
Parameters:
  InstanceType:
    Description: Chọn loại EC2 Instance
    Type: String
    Default: t2.micro
    AllowedValues:
      - t2.micro
      - t2.small
      - t2.medium

Resources:
  EC2Instance:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: !Ref InstanceType
```

Cấu hình này tạo ra một menu dropdown chỉ với ba tùy chọn hợp lệ, cho phép người dùng lựa chọn trong khi vẫn kiểm soát các loại instance được phép.

### 2. NoEcho - Bảo Vệ Dữ Liệu Nhạy Cảm

```yaml
Parameters:
  DatabasePassword:
    Description: Mật khẩu Database
    Type: String
    NoEcho: true
```

Thiết lập `NoEcho: true` ngăn mật khẩu hiển thị trong log, console hoặc API call, giữ an toàn cho dữ liệu nhạy cảm.

## Sử Dụng Parameters với Hàm !Ref

Hàm `!Ref` (viết tắt của `Fn::Ref`) được sử dụng để tham chiếu parameters trong template.

### Ví Dụ Tham Chiếu Parameter

```yaml
Parameters:
  SecurityGroupDescription:
    Description: Mô tả Security Group
    Type: String

Resources:
  SecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: !Ref SecurityGroupDescription
```

### Lưu Ý Quan Trọng Về !Ref

Hàm `!Ref` có hai mục đích:
1. **Tham Chiếu Parameters**: Truy cập giá trị parameter do người dùng cung cấp
2. **Tham Chiếu Resources**: Tham chiếu các tài nguyên khác được định nghĩa trong template

**Best Practice**: Đảm bảo tên resource và tên parameter là duy nhất để tránh nhầm lẫn.

### Ví Dụ Tham Chiếu Resource

```yaml
Resources:
  MyInstance:
    Type: AWS::EC2::Instance
    Properties:
      # ... thuộc tính instance ...

  SSHSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      # ... thuộc tính security group ...

  MyEC2Instance:
    Type: AWS::EC2::Instance
    Properties:
      SecurityGroups:
        - !Ref SSHSecurityGroup
        - !Ref ServiceSecurityGroup

  MyElasticIP:
    Type: AWS::EC2::EIP
    Properties:
      InstanceId: !Ref MyInstance
```

## Pseudo Parameters

AWS cung cấp các pseudo parameter tích hợp sẵn tự động có sẵn trong mọi CloudFormation template mà không cần định nghĩa rõ ràng.

### Các Pseudo Parameters Thường Dùng

| Pseudo Parameter | Trả Về |
|-----------------|---------|
| `AWS::AccountId` | AWS Account ID của bạn |
| `AWS::Region` | AWS region nơi stack được tạo |
| `AWS::StackId` | ID của stack |
| `AWS::StackName` | Tên của stack |
| `AWS::NotificationARNs` | Danh sách notification ARN cho stack |
| `AWS::NoValue` | Xóa thuộc tính tương ứng |

### Ví Dụ Sử Dụng

```yaml
Resources:
  MyResource:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub "my-bucket-${AWS::Region}-${AWS::AccountId}"
      Tags:
        - Key: Region
          Value: !Ref AWS::Region
        - Key: AccountId
          Value: !Ref AWS::AccountId
```

### Lợi Ích của Pseudo Parameters

- **Ngữ Cảnh Tự Động**: Template tự động biết ngữ cảnh thực thi của chúng
- **Không Cần Đầu Vào Người Dùng**: Người dùng không cần chỉ định region hoặc account ID
- **Tính Di Động**: Template hoạt động trên các region và account khác nhau mà không cần sửa đổi
- **Cấu Hình Động**: Cho phép hành vi cụ thể theo region hoặc account

Các pseudo parameter được sử dụng phổ biến nhất là `AWS::Region` và `AWS::AccountId`, vì chúng cho phép template tự động thích ứng với môi trường triển khai.

## Tóm Tắt

CloudFormation parameters rất quan trọng để tạo các template linh hoạt, có thể tái sử dụng và bảo mật. Những điểm chính cần nhớ:

- Sử dụng parameters cho các giá trị có thể thay đổi hoặc không thể xác định trước
- Tận dụng các tính năng validation (AllowedValues, patterns, constraints) để đảm bảo an toàn
- Sử dụng `NoEcho` cho dữ liệu nhạy cảm như mật khẩu
- Tham chiếu parameters và resources bằng hàm `!Ref`
- Tận dụng pseudo parameters để nhận biết ngữ cảnh tự động

Bằng cách thành thạo parameters, bạn có thể tạo các CloudFormation template vừa mạnh mẽ vừa dễ sử dụng trong toàn tổ chức của mình.