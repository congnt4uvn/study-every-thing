# AWS CloudFormation Custom Resources (Tài Nguyên Tùy Chỉnh)

## Giới Thiệu

AWS CloudFormation hỗ trợ rất nhiều loại tài nguyên, nhưng có những trường hợp bạn cần vượt ra ngoài những gì được hỗ trợ sẵn. Custom resources (tài nguyên tùy chỉnh) cho phép bạn:

- Định nghĩa các tài nguyên chưa được CloudFormation hỗ trợ
- Định nghĩa logic provisioning tùy chỉnh cho các tài nguyên nằm ngoài CloudFormation
- Quản lý tài nguyên on-premises hoặc tài nguyên của bên thứ ba
- Chạy các script tùy chỉnh trong các giai đoạn tạo, cập nhật và xóa của CloudFormation stack

## Tổng Quan

Custom resources được hỗ trợ bởi:
- **Lambda functions** (phổ biến nhất)
- **SNS topics**

Các custom resources này cho phép bạn thực thi logic tùy chỉnh thông qua Lambda functions trong các hoạt động khác nhau của stack.

## Định Nghĩa Custom Resource

### Cú Pháp

Để định nghĩa một custom resource trong CloudFormation template:

```yaml
Type: Custom::MyCustomResourceTypeName
```

### Custom Resource Được Hỗ Trợ Bởi Lambda

Cách triển khai phổ biến nhất sử dụng Lambda function:

```yaml
MyCustomResource:
  Type: Custom::MyLambdaResource
  Properties:
    ServiceToken: <Lambda-Function-ARN-hoặc-SNS-ARN>
    # Tham số dữ liệu đầu vào
    Key1: Value1
    Key2: Value2
```

### Các Thành Phần Chính

- **ServiceToken**: ARN của Lambda function hoặc SNS topic (phải cùng region)
- **Properties**: Các tham số dữ liệu đầu vào được truyền cho Lambda function
- **Custom Logic**: Lambda function chứa logic để provision custom resource của bạn

## Trường Hợp Sử Dụng Phổ Biến: Làm Rỗng S3 Buckets

### Vấn Đề

CloudFormation không thể xóa một S3 bucket không rỗng. Bạn phải xóa tất cả các objects trong bucket trước khi có thể xóa bucket.

### Giải Pháp

Sử dụng custom resource được hỗ trợ bởi Lambda function để làm rỗng S3 bucket trước khi xóa.

### Cách Hoạt Động

1. Khi bạn chạy `delete stack` trên CloudFormation
2. Custom resource (được hỗ trợ bởi Lambda function) được kích hoạt
3. Lambda function thực thi các API calls để làm rỗng S3 bucket
4. Sau khi S3 bucket đã được làm rỗng
5. CloudFormation sau đó tiến hành xóa S3 bucket
6. Quá trình xóa stack hoàn thành thành công

### Sơ Đồ Quy Trình

```
CloudFormation Delete Stack
         ↓
Custom Resource Được Kích Hoạt
         ↓
Lambda Function Thực Thi
         ↓
API Calls Để Làm Rỗng S3 Bucket
         ↓
S3 Bucket Được Làm Rỗng
         ↓
CloudFormation Xóa S3 Bucket
         ↓
Thành Công
```

## Mẹo Cho Kỳ Thi

⚠️ **Câu Hỏi Thi Phổ Biến**: Làm thế nào để xóa một S3 bucket bằng CloudFormation khi nó chứa objects?

**Trả Lời**: Sử dụng custom resource được hỗ trợ bởi Lambda function để làm rỗng S3 bucket trước khi CloudFormation cố gắng xóa nó.

## Tóm Tắt

- Custom resources mở rộng khả năng của CloudFormation vượt ra ngoài các loại tài nguyên gốc
- Custom resources được hỗ trợ bởi Lambda là cách triển khai phổ biến nhất
- ServiceToken phải ở cùng region với stack của bạn
- Custom resources có thể chạy logic trong các hoạt động create, update và delete
- Một trường hợp sử dụng điển hình là làm rỗng S3 buckets trước khi xóa

---

*Tài liệu này dựa trên các best practices của AWS CloudFormation và các mẫu triển khai phổ biến.*