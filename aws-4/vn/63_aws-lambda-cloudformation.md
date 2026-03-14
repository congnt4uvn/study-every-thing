# Triển khai AWS Lambda với CloudFormation

## Tổng quan
Tài liệu này trình bày cách triển khai các hàm AWS Lambda sử dụng CloudFormation templates.

## Các phương pháp triển khai

### 1. Phương pháp Inline (nhúng trực tiếp)

**Mô tả:**
- Định nghĩa code Lambda function trực tiếp trong CloudFormation template
- Sử dụng thuộc tính `Code.ZipFile`

**Ưu điểm:**
- Đơn giản và trực quan
- Code hiển thị ngay trong template
- Không cần phụ thuộc bên ngoài

**Hạn chế:**
- Chỉ dành cho các hàm rất đơn giản
- Không thể bao gồm các thư viện phụ thuộc
- Không phù hợp cho ứng dụng phức tạp

**Cấu trúc ví dụ:**
```yaml
Resources:
  MyLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      Code:
        ZipFile: |
          # Code Lambda của bạn ở đây
```

### 2. Phương pháp S3 Zip File

**Mô tả:**
- Lưu trữ Lambda function dưới dạng file zip trong Amazon S3
- Tham chiếu đến vị trí S3 trong CloudFormation template

**Yêu cầu:**
- Lambda function zip phải được lưu trong Amazon S3
- Phải chỉ định vị trí S3 trong code CloudFormation

**Các thuộc tính chính:**
- **S3Bucket**: Bucket chứa file zip
- **S3Key**: Đường dẫn đầy đủ đến file zip trong S3
- **S3ObjectVersion**: Version ID (nếu sử dụng bucket có versioning)

**Best Practices (Thực hành tốt nhất):**
- Bật versioning trên S3 bucket (được khuyến nghị)
- Cập nhật S3ObjectVersion khi thay đổi code
- Điều này đảm bảo CloudFormation phát hiện và áp dụng các cập nhật

**Hành vi cập nhật:**
- Nếu bạn cập nhật code trong S3 nhưng không cập nhật S3Bucket, S3Key, hoặc S3ObjectVersion trong template, CloudFormation **sẽ không** cập nhật function
- Versioning giúp CloudFormation theo dõi thay đổi và cập nhật đúng cách

### 3. Triển khai đa tài khoản (Multi-Account)

**Kịch bản:**
Triển khai Lambda function từ một AWS account sang nhiều account khác.

**Thiết lập:**
- Account 1: Chứa S3 bucket với code Lambda
- Account 2 & 3: Các account đích để triển khai

**Quy trình:**
1. Khởi chạy CloudFormation trong Account 2
2. Tham chiếu S3 bucket từ Account 1
3. Đảm bảo quyền truy cập cross-account phù hợp

**Lưu ý quan trọng:**
- Account 2 phải có quyền truy cập vào S3 bucket của Account 1
- Cấu hình IAM policies và bucket policies thích hợp

## Tổng kết

| Phương pháp | Trường hợp sử dụng | Phụ thuộc | Độ phức tạp |
|-------------|-------------------|-----------|-------------|
| Inline | Hàm đơn giản | Không hỗ trợ | Thấp |
| S3 Zip | Sử dụng production | Hỗ trợ | Trung bình |
| Multi-Account | Triển khai doanh nghiệp | Hỗ trợ | Cao |

## Ghi chú quan trọng

- Đối với môi trường production, sử dụng phương pháp S3 zip với versioning
- Luôn bật S3 bucket versioning để theo dõi thay đổi tốt hơn
- Triển khai cross-account cần cấu hình IAM cẩn thận
- Cập nhật S3ObjectVersion trong template khi triển khai phiên bản code mới
