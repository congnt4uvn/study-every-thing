# AWS SAM Policy Templates (Mẫu Chính Sách SAM)

## Tổng Quan
SAM (Serverless Application Model) policy templates là danh sách các mẫu được định nghĩa sẵn mà bạn có thể áp dụng để cấp quyền cho các Lambda functions. Các mẫu này giúp dễ dàng xác định những gì Lambda function có thể làm mà không cần lo lắng về việc cấu hình phức tạp của IAM roles.

## Khái Niệm Chính
- **Mục đích**: Đơn giản hóa việc quản lý quyền cho Lambda functions
- **Lợi ích**: Nhóm các quyền liên quan thành các mẫu dễ hiểu
- **Cách sử dụng**: Áp dụng mẫu thay vì tạo IAM roles thủ công

## Các SAM Policy Templates Quan Trọng

### 1. S3ReadPolicy
- **Chức năng**: Cung cấp quyền chỉ đọc (read-only) đối với các objects trong S3
- **Trường hợp sử dụng**: Khi Lambda function cần đọc dữ liệu từ S3 buckets

### 2. SQSPollerPolicy
- **Chức năng**: Cho phép Lambda function thăm dò (poll) một SQS queue
- **Trường hợp sử dụng**: Khi Lambda cần nhận messages từ SQS

### 3. DynamoDBCrudPolicy
- **Chức năng**: Cho phép các thao tác Create, Read, Update, Delete (CRUD) trên bảng DynamoDB
- **Trường hợp sử dụng**: Khi Lambda cần quyền truy cập đầy đủ để quản lý dữ liệu DynamoDB

## Ví Dụ Triển Khai

```yaml
MyFunction:
  Type: AWS::Serverless::Function
  Properties:
    Runtime: python2.7
    Policies:
      - SQSPollerPolicy:
          QueueName: !GetAtt MyQueue.QueueName
```

## Cách Hoạt Động
1. Định nghĩa policy template trong SAM template (ví dụ: `SQSPollerPolicy`)
2. Chỉ định các tham số cần thiết (ví dụ: tên queue)
3. SAM framework tự động chuyển đổi nó thành một IAM policy
4. Policy được gán vào Lambda function của bạn

## Mẹo Cho Kỳ Thi
- Tên của policy template thường rất rõ ràng và dễ hiểu
- Nắm vững ba ví dụ chính: S3ReadPolicy, SQSPollerPolicy, DynamoDBCrudPolicy
- Hiểu rằng CRUD có nghĩa là Create (Tạo), Read (Đọc), Update (Cập nhật), Delete (Xóa)
- SAM templates giúp đơn giản hóa việc quản lý IAM roles

## Tài Liệu Tham Khảo
- [Danh sách đầy đủ các SAM Policy Templates](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-policy-templates.html)
