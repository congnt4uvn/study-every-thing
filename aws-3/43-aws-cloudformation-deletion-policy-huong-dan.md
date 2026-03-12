# Hướng Dẫn AWS CloudFormation DeletionPolicy

## Tổng Quan

DeletionPolicy là một thiết lập bạn có thể áp dụng cho các tài nguyên trong CloudFormation template của mình, cho phép bạn kiểm soát điều gì xảy ra với tài nguyên khi nó bị xóa khỏi CloudFormation template hoặc khi CloudFormation stack bị xóa. Đây là cách để bạn bảo vệ và sao lưu tài nguyên.

## Hành Vi Mặc Định

Theo mặc định, khi bạn xóa một CloudFormation template, tất cả các tài nguyên bên trong cũng sẽ bị xóa. Điều này có nghĩa là DeletionPolicy mặc định là **Delete**, vì vậy bạn không cần phải chỉ định nó một cách rõ ràng.

## Các Tùy Chọn DeletionPolicy

### 1. Delete

Chính sách **Delete** sẽ xóa tài nguyên khi CloudFormation stack bị xóa.

**Ví dụ - EC2 Instance:**
```yaml
MyEC2Instance:
  Type: AWS::EC2::Instance
  DeletionPolicy: Delete
  Properties:
    # ... thuộc tính instance
```

EC2 instance sẽ bị xóa bất cứ khi nào CloudFormation stack bị xóa.

**Ví dụ - S3 Bucket (Trường Hợp Đặc Biệt):**
```yaml
MyS3Bucket:
  Type: AWS::S3::Bucket
  DeletionPolicy: Delete
  Properties:
    # ... thuộc tính bucket
```

**Ngoại Lệ Quan Trọng:** Đối với S3 bucket với `DeletionPolicy: Delete`, việc xóa chỉ hoạt động nếu S3 bucket trống. Nếu không trống, việc xóa sẽ thất bại.

**Giải Pháp Cho S3 Bucket Không Trống:**
- Xóa thủ công mọi thứ trong S3 bucket trước khi xóa CloudFormation template
- Triển khai một custom resource để tự động xóa mọi thứ trong S3 bucket trước khi bucket bị xóa

### 2. Retain

Chính sách **Retain** chỉ định các tài nguyên bạn muốn bảo vệ khi xóa CloudFormation template của mình.

**Ví dụ - DynamoDB Table:**
```yaml
MyDynamoDBTable:
  Type: AWS::DynamoDB::Table
  DeletionPolicy: Retain
  Properties:
    # ... thuộc tính table
```

Ngay cả khi bạn xóa CloudFormation template, DynamoDB table này sẽ được giữ lại, bảo vệ dữ liệu bên trong. Điều này hoạt động với bất kỳ loại tài nguyên nào.

### 3. Snapshot

Chính sách **Snapshot** tạo một snapshot cuối cùng trước khi xóa tài nguyên. Điều này rất hữu ích cho mục đích sao lưu và an toàn.

**Các Tài Nguyên Được Hỗ Trợ:**
- EBS volumes
- ElastiCache Cluster
- ElastiCache ReplicationGroup
- RDS DBInstance
- RDS DB Cluster
- Amazon Redshift
- Amazon Neptune
- Amazon DocumentDB
- Và có thể nhiều hơn nữa

**Ví dụ - RDS Instance:**
```yaml
MyRDSInstance:
  Type: AWS::RDS::DBInstance
  DeletionPolicy: Snapshot
  Properties:
    # ... thuộc tính RDS
```

RDS database instance sẽ bị xóa, nhưng một snapshot cuối cùng sẽ được tạo trước khi instance biến mất.

## Ví Dụ Thực Hành

Hãy xem một ví dụ thực tế với file có tên `deletionpolicy.yaml`:

```yaml
MySecurityGroup:
  Type: AWS::EC2::SecurityGroup
  DeletionPolicy: Retain
  Properties:
    # ... thuộc tính security group

MyEBSVolume:
  Type: AWS::EC2::Volume
  DeletionPolicy: Snapshot
  Properties:
    # ... thuộc tính volume
```

### Tạo Stack

1. Tạo một stack có tên `DeletionPolicyDemo`
2. Upload template file `deletionpolicy.yaml`
3. Stack sẽ nhanh chóng tạo hai tài nguyên:
   - Một EBS volume
   - Một EC2 security group

### Xóa Stack

Khi bạn xóa stack, hãy quan sát hành vi sau:

**Security Group (Chính Sách Retain):**
- Security group hiển thị "delete skipped" trong events
- Security group vẫn còn trong tài khoản AWS của bạn
- Bạn phải xóa thủ công nếu muốn xóa hoàn toàn

**EBS Volume (Chính Sách Snapshot):**
- EBS volume bị xóa
- Một snapshot được tạo thành công trước khi xóa
- Bạn có thể tìm thấy snapshot (ví dụ: 1 GB) trong phần Snapshots
- EBS volume gốc đã biến mất

### Dọn Dẹp

Để dọn dẹp hoàn toàn:
1. Xóa thủ công snapshot được tạo từ EBS volume
2. Xóa thủ công security group được giữ lại

## Những Điểm Chính

- **Delete** (mặc định): Tài nguyên bị xóa cùng với stack
- **Retain**: Tài nguyên được bảo vệ ngay cả sau khi xóa stack
- **Snapshot**: Một snapshot sao lưu được tạo trước khi xóa tài nguyên
- S3 bucket với chính sách Delete phải trống để có thể xóa thành công
- Các tài nguyên được giữ lại phải được xóa thủ công bên ngoài CloudFormation
- Các snapshot được tạo bởi chính sách Snapshot cũng phải được xóa thủ công

## Kết Luận

DeletionPolicy cung cấp khả năng kiểm soát mạnh mẽ đối với quản lý vòng đời tài nguyên trong CloudFormation, cho phép bạn bảo vệ dữ liệu và tài nguyên quan trọng khỏi việc xóa nhầm trong khi vẫn duy trì tính linh hoạt trong việc quản lý hạ tầng của bạn.