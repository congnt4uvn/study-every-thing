# Hướng Dẫn Các Hàm Intrinsic của AWS CloudFormation

## Tổng Quan

Các hàm intrinsic (hàm nội tại) là những hàm tích hợp sẵn mạnh mẽ trong AWS CloudFormation giúp bạn quản lý các stack một cách linh hoạt hơn. Hướng dẫn này đề cập đến các hàm intrinsic quan trọng nhất mà bạn cần biết, đặc biệt từ góc độ thi chứng chỉ.

## Danh Sách Các Hàm Intrinsic

CloudFormation cung cấp nhiều hàm intrinsic khác nhau, được phân loại như sau:

### Các Hàm Cốt Lõi (Bắt Buộc Phải Biết)
- **Ref** - Tham chiếu đến parameters hoặc resources
- **Fn::GetAtt** - Lấy các thuộc tính từ resources
- **Fn::FindInMap** - Truy xuất giá trị từ mappings
- **Fn::ImportValue** - Import các giá trị đã export từ stack khác
- **Fn::Join** - Nối các chuỗi với dấu phân cách
- **Fn::Sub** - Thay thế biến trong chuỗi
- **Fn::ForEach** - Lặp qua các collections
- **Fn::ToJsonString** - Chuyển đổi sang chuỗi JSON

### Các Hàm Điều Kiện
- **Fn::If** - Đánh giá có điều kiện
- **Fn::Not** - Phép toán NOT logic
- **Fn::Equals** - So sánh bằng
- **Fn::And** - Phép toán AND logic
- **Fn::Or** - Phép toán OR logic

### Các Hàm Tiện Ích
- **Fn::Base64** - Mã hóa chuỗi sang Base64
- **Fn::Cidr** - Tạo các khối CIDR
- **Fn::GetAZs** - Lấy danh sách availability zones
- **Fn::Select** - Chọn phần tử từ danh sách
- **Fn::Split** - Tách chuỗi
- **Fn::Transform** - Áp dụng macros
- **Fn::Length** - Lấy độ dài của mảng

> **Lưu ý:** Tất cả các hàm intrinsic đều được ghi chú trên trang web CloudFormation. Nếu một hàm nào đó không được đề cập chi tiết ở đây, vui lòng tham khảo tài liệu chính thức.

---

## 1. Hàm Ref

### Mục Đích
Hàm `Ref` trả về một tham chiếu đến một parameter hoặc resource được chỉ định.

### Hành Vi
- **Đối với Parameters:** Trả về giá trị của parameter
- **Đối với Resources:** Trả về ID vật lý của resource cơ bản đã được tạo (ví dụ: EC2 instance ID)

### Cú Pháp
```yaml
# Cú pháp đầy đủ
Ref: LogicalName

# Cú pháp rút gọn (YAML)
!Ref LogicalName
```

### Ví Dụ
```yaml
Resources:
  MySubnet:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref MyVPC
      # MyVPC có thể là resource khác hoặc là một parameter
```

Trong ví dụ này, chúng ta đang tạo một subnet và sử dụng `!Ref` để tham chiếu đến VPC mà subnet thuộc về.

---

## 2. Hàm Fn::GetAtt

### Mục Đích
Hàm `Fn::GetAtt` truy xuất giá trị của một thuộc tính từ một resource trong template của bạn.

### Khái Niệm Chính
- Mỗi resource có các thuộc tính ngoài ID tham chiếu của nó
- Các thuộc tính có sẵn khác nhau tùy theo loại resource
- Kiểm tra tài liệu CloudFormation để biết các thuộc tính được hỗ trợ của từng resource

### Tìm Các Thuộc Tính Có Sẵn

Để tìm các thuộc tính mà resource hỗ trợ:
1. Truy cập trang tài liệu CloudFormation của resource
2. Tìm phần **Return Values**
3. Kiểm tra phần **Fn::GetAtt**

#### Ví Dụ: Các Thuộc Tính của EC2 Instance

Đối với resource EC2 instance:
- **Ref** trả về: Instance ID
- **Fn::GetAtt** có thể trả về:
  - `AvailabilityZone` - AZ nơi instance được khởi chạy (ví dụ: us-east-1b)
  - `PrivateDnsName` - Tên DNS private
  - `PrivateIp` - Địa chỉ IP private
  - `PublicDnsName` - Tên DNS public
  - `PublicIp` - Địa chỉ IP public

### Cú Pháp
```yaml
# Cú pháp đầy đủ
Fn::GetAtt:
  - LogicalNameOfResource
  - AttributeName

# Cú pháp rút gọn (YAML)
!GetAtt LogicalNameOfResource.AttributeName
```

### Ví Dụ
```yaml
Resources:
  EC2Instance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: ami-12345678
      InstanceType: t2.micro

  EBSVolume:
    Type: AWS::EC2::Volume
    Properties:
      AvailabilityZone: !GetAtt EC2Instance.AvailabilityZone
      Size: 100
```

Trong ví dụ này:
- Chúng ta tạo một EC2 instance
- Chúng ta tạo một EBS volume phải nằm trong cùng AZ với instance
- Chúng ta sử dụng `!GetAtt EC2Instance.AvailabilityZone` để lấy AZ một cách động
- `EC2Instance` là tên logic của resource
- `AvailabilityZone` là tên thuộc tính được expose bởi resource

---

## 3. Hàm Fn::FindInMap

### Mục Đích
Truy xuất giá trị từ một key cụ thể trong một map cụ thể được định nghĩa trong phần Mappings.

### Sử Dụng
Được sử dụng khi bạn có mappings được định nghĩa trong template và cần truy xuất giá trị dựa trên các key.

### Ví Dụ Ngữ Cảnh
```yaml
Mappings:
  RegionMap:
    us-east-1:
      AMI: ami-12345678
    us-west-2:
      AMI: ami-87654321

Resources:
  MyInstance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: !FindInMap [RegionMap, !Ref "AWS::Region", AMI]
```

---

## 4. Hàm Fn::ImportValue

### Mục Đích
Import các giá trị đã được export từ các CloudFormation stack khác.

### Khái Niệm Chính
- Cho phép tham chiếu chéo giữa các stack
- Giá trị phải được export trong stack khác bằng thuộc tính `Export`
- Thúc đẩy tính module hóa và khả năng tái sử dụng

### Cú Pháp
```yaml
!ImportValue ExportedValueName
```

### Ví Dụ
```yaml
Resources:
  EC2Instance:
    Type: AWS::EC2::Instance
    Properties:
      SecurityGroupIds:
        - !ImportValue SSHSecurityGroup
```

Trong ví dụ này:
- Chúng ta tạo một EC2 instance
- Chúng ta import một security group ID đã được export từ stack khác
- Tên được export là `SSHSecurityGroup`

---

## 5. Hàm Fn::Base64

### Mục Đích
Chuyển đổi một chuỗi sang dạng biểu diễn Base64.

### Trường Hợp Sử Dụng Chính
Truyền user data đã được mã hóa cho các EC2 instance. CloudFormation yêu cầu user data phải được mã hóa Base64.

### Cú Pháp
```yaml
!Base64 chuoi_can_ma_hoa
```

### Ví Dụ
```yaml
Resources:
  MyInstance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: ami-12345678
      UserData:
        Fn::Base64: |
          #!/bin/bash
          yum update -y
          yum install -y httpd
          systemctl start httpd
```

> **Lưu ý:** Đây là trường hợp sử dụng chính (và thường là duy nhất) cho hàm Base64 trong các template CloudFormation.

---

## 6. Các Hàm Điều Kiện

### Mục Đích
Tạo logic điều kiện trong template để kiểm soát việc tạo và cấu hình resource.

### Các Hàm Điều Kiện Có Sẵn
- **Fn::And** - Trả về true nếu tất cả điều kiện đều đúng
- **Fn::Equals** - So sánh hai giá trị để kiểm tra bằng nhau
- **Fn::If** - Trả về một giá trị nếu đúng, giá trị khác nếu sai
- **Fn::Not** - Trả về giá trị ngược lại của điều kiện
- **Fn::Or** - Trả về true nếu bất kỳ điều kiện nào đúng

### Sử Dụng
Các hàm này được sử dụng trong phần `Conditions` và có thể được tham chiếu trong định nghĩa resource để tạo resource có điều kiện.

### Ví Dụ
```yaml
Conditions:
  IsProduction: !Equals [!Ref Environment, "production"]

Resources:
  ProductionOnlyResource:
    Type: AWS::EC2::Instance
    Condition: IsProduction
    Properties:
      InstanceType: m5.large
```

---

## Các Thực Hành Tốt

1. **Sử Dụng Ký Hiệu Rút Gọn**: Trong các template YAML, sử dụng ký hiệu rút gọn `!` (ví dụ: `!Ref`, `!GetAtt`) để code sạch hơn
2. **Kiểm Tra Tài Liệu**: Luôn xác minh các thuộc tính có sẵn trong tài liệu AWS CloudFormation
3. **Kết Hợp Các Hàm**: Các hàm intrinsic thường có thể lồng nhau để tạo các cấu hình động mạnh mẽ
4. **Export Có Chiến Lược**: Khi sử dụng `ImportValue`, lập kế hoạch cẩn thận cho các dependency của stack để tránh tham chiếu vòng

---

## Tóm Tắt

Các hàm intrinsic là công cụ thiết yếu để tạo các template CloudFormation động và có thể tái sử dụng. Các hàm quan trọng nhất cần thành thạo là:

- **Ref** - Để tham chiếu đến parameters và resource IDs
- **GetAtt** - Để truy cập các thuộc tính của resource
- **FindInMap** - Để truy xuất các giá trị đã map
- **ImportValue** - Để tham chiếu chéo giữa các stack
- **Base64** - Để mã hóa EC2 user data
- **Các Hàm Điều Kiện** - Để tạo resource có điều kiện

Hiểu các hàm này rất quan trọng cho cả việc sử dụng CloudFormation thực tế và chuẩn bị thi chứng chỉ.

---

## Tài Nguyên Bổ Sung

- [Tài Liệu Tham Khảo Hàm Intrinsic của AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference.html)
- Hướng Dẫn Sử Dụng AWS CloudFormation
- Tài liệu cụ thể của từng resource để biết các thuộc tính có sẵn

---

*Hướng dẫn này dựa trên các thực hành tốt nhất của AWS CloudFormation và tài liệu chuẩn bị thi chứng chỉ.*