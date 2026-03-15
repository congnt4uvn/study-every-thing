# AWS Lambda Stage Variables với API Gateway

## Tổng Quan
Hướng dẫn này trình bày cách sử dụng stage variables trong API Gateway để gọi các phiên bản và alias Lambda function khác nhau một cách động. Đây là một mẫu mạnh mẽ để quản lý nhiều môi trường (DEV, TEST, PROD) với một cấu hình API Gateway duy nhất.

## Các Khái Niệm Chính

### Lambda Versions (Phiên Bản)
- **Versions** là các bản chụp nhanh bất biến của code Lambda function
- Mỗi version có một số phiên bản duy nhất (v1, v2, v.v.)
- Version **$LATEST** đại diện cho phiên bản hiện tại có thể chỉnh sửa
- Versions cho phép bạn duy trì nhiều bản phát hành ổn định

### Lambda Aliases (Bí Danh)
- **Aliases** là con trỏ trỏ đến các Lambda versions cụ thể
- Chúng cung cấp một lớp trừu tượng giữa API và các phiên bản function
- Quy ước đặt tên alias phổ biến: DEV, TEST, PROD
- Aliases có thể được cập nhật để trỏ đến các versions khác nhau

### Stage Variables (Biến Giai Đoạn)
- Stage variables là các cặp key-value trong API Gateway
- Chúng cho phép bạn tham số hóa cấu hình API
- Trường hợp sử dụng: Chuyển đổi giữa các Lambda aliases dựa trên deployment stage

## Các Bước Thực Hiện

### 1. Tạo Lambda Function
```
Tên function: api-gateway-stage-variables-get
Runtime: Python 3.11
```

### 2. Tạo Nhiều Versions

**Version 1:**
```python
# Code Lambda
return "Hello from Lambda v1"
```
- Deploy code
- Test nó
- Publish dưới dạng Version 1

**Version 2:**
```python
# Code Lambda
return "Hello from Lambda v2"
```
- Cập nhật code
- Deploy và test
- Publish dưới dạng Version 2

**Latest (DEV):**
```python
# Code Lambda
return "Hello from Lambda in DEV"
```
- Cập nhật code
- Deploy và test
- KHÔNG publish (giữ lại dưới dạng $LATEST)

### 3. Tạo Aliases

| Alias | Trỏ Đến | Mục Đích |
|-------|---------|----------|
| **DEV** | $LATEST | Development - luôn sử dụng code mới nhất |
| **TEST** | Version 2 | Testing - sử dụng phiên bản published mới nhất |
| **PROD** | Version 1 | Production - sử dụng phiên bản ổn định nhất |

### 4. Cấu Hình API Gateway

1. Tạo một resource tên là "stage variables"
2. Tạo một GET method cho Lambda function
3. Bật Lambda proxy integration
4. Sử dụng Lambda ARN với stage variable:
   ```
   arn:aws:lambda:region:account-id:function:api-gateway-stage-variables-get:${stageVariables.LambdaAlias}
   ```

### 5. Thiết Lập Quyền

Khi sử dụng stage variables, bạn cần cấp quyền cho API Gateway để gọi mỗi alias:
```bash
# Chạy lệnh này trong CloudShell cho từng alias
aws lambda add-permission \
  --function-name <function-name>:<alias> \
  --statement-id apigateway-access \
  --action lambda:InvokeFunction \
  --principal apigateway.amazonaws.com
```

## Lợi Ích

1. **Quản Lý Môi Trường**: Cấu hình API đơn lẻ cho nhiều môi trường
2. **Kiểm Soát Phiên Bản**: Dễ dàng rollback bằng cách cập nhật con trỏ alias
3. **Testing**: Test các phiên bản mới một cách độc lập trước khi đưa vào production
4. **Linh Hoạt**: Thay đổi các Lambda versions backend mà không cần sửa đổi API Gateway

## Các Thực Hành Tốt Nhất

- Sử dụng semantic versioning cho Lambda versions
- Giữ PROD trỏ đến phiên bản ổn định và đã được kiểm tra nhất
- Sử dụng DEV cho phát triển liên tục
- Đưa các versions qua TEST trước khi đến PROD
- Tài liệu hóa nội dung của từng alias và version

## Tóm Tắt

Stage variables trong API Gateway kết hợp với Lambda aliases cung cấp một chiến lược triển khai mạnh mẽ. Mẫu này cho phép:
- Blue-green deployments
- Canary releases
- Định tuyến theo môi trường cụ thể
- Quản lý phiên bản mà không cần triển khai lại API
