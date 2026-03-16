# AWS SAM với DynamoDB - Tài Liệu Học Tập

## Tổng Quan
Tài liệu này bao gồm tích hợp AWS SAM (Serverless Application Model) với DynamoDB, bao gồm cách tạo, triển khai và kiểm tra các API serverless được hỗ trợ bởi bảng DynamoDB.

---

## AWS SAM là gì?

**AWS SAM (Serverless Application Model)** là một framework giúp đơn giản hóa việc phát triển và triển khai các ứng dụng serverless trên AWS. Nó cung cấp:
- Cú pháp đơn giản hơn so với CloudFormation thuần
- Định nghĩa dễ dàng các hàm serverless, API và cơ sở dữ liệu
- Khả năng kiểm tra cục bộ mà không cần triển khai lên AWS
- Lệnh triển khai và dọn dẹp nhanh chóng

---

## Các Thành Phần Chính

### 1. Các Lệnh SAM CLI

#### Khởi Tạo Dự Án Mới
```bash
sam init
```
- Sử dụng các mẫu quick start
- Chọn loại template (ví dụ: Serverless API)
- Chọn runtime (ví dụ: nodejs22)
- Cấu hình các tùy chọn (X-Ray, v.v.)

#### Triển Khai Ứng Dụng
```bash
sam deploy
```

#### Xóa Ứng Dụng
```bash
sam delete
```
**Quan trọng**: Luôn xóa các tài nguyên đã triển khai sau khi kiểm tra để tránh chi phí không cần thiết.

#### Các Lệnh Kiểm Tra Cục Bộ
```bash
# Gọi một hàm ở local
sam local invoke <TênHàm> -e <file-event>

# Khởi động API Gateway cục bộ
sam local start-api
```

---

## Cấu Trúc Template (template.yaml)

### Các Thành Phần Thiết Yếu

#### 1. Khai Báo Transform
```yaml
Transform: AWS::Serverless-2016-10-31
```
Dòng này **cực kỳ quan trọng** cho SAM - nó kích hoạt các loại tài nguyên đặc biệt của SAM và cú pháp đơn giản hóa.

#### 2. Phần Resources

**Ví Dụ Hàm Serverless:**
```yaml
Resources:
  GetAllItemsFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: ./src
      Handler: get-all-items.handler
      Runtime: nodejs22.x
      MemorySize: 128
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref SampleTable
      Events:
        GetAllItems:
          Type: Api
          Properties:
            Path: /
            Method: GET
```

**Ví Dụ Bảng DynamoDB:**
```yaml
  SampleTable:
    Type: AWS::Serverless::SimpleTable
    Properties:
      PrimaryKey:
        Name: id
        Type: String
      ProvisionedThroughput:
        ReadCapacityUnits: 2
        WriteCapacityUnits: 2
```

---

## IAM Policies Đơn Giản Hóa với SAM

### DynamoDBCrudPolicy
SAM cung cấp các mẫu policy đơn giản tự động tạo các IAM policy phù hợp:

```yaml
Policies:
  - DynamoDBCrudPolicy:
      TableName: !Ref SampleTable
```

Dòng duy nhất này thay thế các định nghĩa IAM policy phức tạp của CloudFormation với quyền truy cập CRUD đầy đủ vào bảng DynamoDB được chỉ định.

---

## Tích Hợp API Gateway

SAM làm cho việc định nghĩa API cực kỳ đơn giản:

### Endpoint GET
```yaml
Events:
  GetItems:
    Type: Api
    Properties:
      Path: /
      Method: GET
```

### Endpoint POST
```yaml
Events:
  CreateItem:
    Type: Api
    Properties:
      Path: /
      Method: POST
```

---

## Quy Trình Phát Triển Cục Bộ

### 1. Các Event Mẫu
Các dự án SAM thường bao gồm các file event mẫu trong thư mục `events/`. Các file JSON này mô phỏng các event từ API Gateway hoặc các dịch vụ AWS khác.

### 2. Gọi Hàm Cục Bộ
```bash
sam local invoke PutItemFunction -e events/put-item-event.json
sam local invoke GetAllItemsFunction -e events/get-all-items-event.json
```

**Yêu Cầu cho Kiểm Tra Cục Bộ:**
- Phải cài đặt Docker
- Các môi trường runtime cần thiết
- Không khả dụng trên AWS CloudShell

### 3. API Gateway Cục Bộ
```bash
sam local start-api
```
Lệnh này khởi động một API Gateway cục bộ trên máy tính của bạn, cho phép bạn:
- Kiểm tra toàn bộ API cục bộ
- Lặp lại nhanh chóng mà không cần triển khai AWS
- Thực hiện thay đổi và kiểm tra ngay lập tức
- Chỉ triển khai lên AWS khi sẵn sàng

---

## Ví Dụ API Serverless Hoàn Chỉnh

Một API serverless điển hình với DynamoDB bao gồm:

1. **Nhiều Lambda Functions** - cho các hoạt động khác nhau (GET, POST, PUT, DELETE)
2. **API Gateway Events** - định nghĩa các đường dẫn HTTP và phương thức
3. **Bảng DynamoDB** - để lưu trữ dữ liệu
4. **IAM Policies** - đơn giản hóa thông qua các mẫu policy của SAM
5. **Cấu Hình** - runtime, bộ nhớ, timeout settings

---

## Thực Hành Tốt Nhất

1. **Sử Dụng SAM Templates** - Tận dụng các template có sẵn với `sam init`
2. **Kiểm Tra Cục Bộ Trước** - Sử dụng lệnh `sam local` để kiểm tra trước khi triển khai
3. **Dọn Dẹp Tài Nguyên** - Luôn chạy `sam delete` sau khi kiểm tra
4. **Sử Dụng Simple Policies** - Tận dụng các mẫu policy của SAM thay vì IAM thuần
5. **Kiểm Soát Phiên Bản** - Giữ template.yaml của bạn trong version control
6. **Đọc Tài Liệu** - Kiểm tra các file README.md trong các dự án SAM để biết hướng dẫn cụ thể

---

## Cấu Trúc Dự Án

Một dự án SAM điển hình trông như sau:
```
sam-app-dynamodb/
├── template.yaml          # Định nghĩa SAM template
├── README.md              # Tài liệu dự án
├── events/                # Các file event mẫu
│   ├── put-item-event.json
│   └── get-all-items-event.json
└── src/                   # Mã nguồn Lambda function
    ├── get-all-items.js
    ├── put-item.js
    └── package.json
```

---

## Những Điểm Chính Cần Nhớ

✅ **SAM đơn giản hóa phát triển serverless** so với CloudFormation thuần
✅ **Kiểm tra cục bộ tiết kiệm thời gian và tiền bạc** bằng cách tránh triển khai AWS liên tục
✅ **Các mẫu policy giảm độ phức tạp** của cấu hình IAM
✅ **Định nghĩa API rất đơn giản** với cú pháp đơn giản hóa của SAM
✅ **API serverless full-stack** có thể được triển khai chỉ với một lệnh duy nhất

---

## Tài Nguyên Bổ Sung

- Tài liệu chính thức về AWS SAM
- Tài liệu AWS Lambda
- Tài liệu Amazon DynamoDB
- Tài liệu CloudFormation
- Hướng dẫn cài đặt Docker

---

*Học kỹ tài liệu này để hiểu sức mạnh của AWS SAM trong việc đơn giản hóa phát triển và triển khai ứng dụng serverless.*
