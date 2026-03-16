# Hướng Dẫn AWS SAM (Serverless Application Model)

## Tổng Quan
AWS SAM (Serverless Application Model) là một framework để xây dựng ứng dụng serverless trên AWS. Nó cung cấp cách thức đơn giản để định nghĩa và triển khai các hàm Lambda, API, cơ sở dữ liệu và event source mappings.

## Bắt Đầu Với AWS SAM

### 1. Khởi Động AWS Cloud Shell
- Mở AWS Console và nhấp vào biểu tượng Cloud Shell
- Đợi môi trường chuẩn bị terminal của bạn
- Cloud Shell đã cài đặt sẵn SAM CLI

### 2. Kiểm Tra Cài Đặt SAM CLI
```bash
sam --version
```
Lệnh này xác nhận rằng SAM CLI đã được cài đặt và hiển thị phiên bản.

## Tạo Ứng Dụng SAM

### Khởi Tạo Dự Án SAM Mới
```bash
sam init
```

### Các Tùy Chọn Cấu Hình
Khi khởi tạo, bạn sẽ được nhắc với nhiều tùy chọn:

1. **Chọn Template**: Chọn Quick Start template (tùy chọn 1)
2. **Loại Template**: Chọn từ hơn 16 tùy chọn bao gồm:
   - Hello World Example (Ví dụ Hello World)
   - Data Processing (Xử lý dữ liệu)
   - Serverless API
   - DynamoDB Example (Ví dụ DynamoDB)
   - Và nhiều hơn nữa...

3. **Chọn Runtime**: Chọn phiên bản Python ưa thích (ví dụ: Python 3.9, 3.13)
4. **Tính Năng Bổ Sung**:
   - X-ray tracing: Bật/tắt distributed tracing
   - CloudWatch Insights: Bật/tắt giám sát nâng cao
   - JSON log format: Bật/tắt structured logging
5. **Tên Dự Án**: Nhập tên ứng dụng của bạn (mặc định: sam-app)

## Cấu Trúc Dự Án

Sau khi khởi tạo, ứng dụng SAM của bạn sẽ chứa:

### Các Thư Mục Chính
- **hello_world/**: Chứa mã nguồn ứng dụng của bạn
- **tests/**: Chứa các file test
- **events/**: Chứa các sample event payloads để testing

### Các File Quan Trọng

#### 1. `hello_world/app.py`
Mã nguồn hàm Lambda chính của bạn:
```python
import json

def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps('Hello world')
    }
```

#### 2. `requirements.txt`
Định nghĩa các Python packages/dependencies cần thiết cho ứng dụng:
```
requests
```

#### 3. `samconfig.toml`
File cấu hình cho ứng dụng SAM của bạn chứa:
- Thông tin phiên bản
- Tên stack
- Tham số build
- Cài đặt triển khai

#### 4. `template.yaml`
Template ứng dụng serverless - file quan trọng nhất:
```yaml
Transform: AWS::Serverless
Resources:
  HelloWorldFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: hello_world/
      Handler: app.lambda_handler
      Runtime: python3.9
      Timeout: 3
```

Các thành phần chính:
- **Transform**: Chỉ định đây là template SAM
- **Type**: AWS::Serverless::Function cho hàm Lambda
- **CodeUri**: Vị trí mã nguồn hàm của bạn
- **Handler**: Entry point cho hàm của bạn
- **Runtime**: Phiên bản Python sử dụng

## Build Ứng Dụng SAM

### Di Chuyển Vào Thư Mục Dự Án
```bash
cd sam-app
```

### Xem Các File Trong Dự Án
```bash
find . -print
```

### Build Ứng Dụng
```bash
sam build
```

Lệnh này:
- Đóng gói ứng dụng của bạn
- Giải quyết dependencies
- Tạo build artifacts trong thư mục `.aws-sam/`

## Xử Lý Lỗi

### Vấn Đề Về Phiên Bản Python
Nếu bạn gặp lỗi phiên bản Python trong quá trình build:

1. **Kiểm Tra Phiên Bản Python Có Sẵn**:
   ```bash
   python --version
   ```

2. **Cập Nhật template.yaml**:
   ```bash
   nano template.yaml
   ```
   
3. **Sửa Đổi Runtime**:
   Thay đổi runtime để khớp với phiên bản Python có sẵn:
   ```yaml
   Runtime: python3.9  # Sử dụng phiên bản có sẵn trong môi trường của bạn
   ```

4. **Lưu và Kiểm Tra**:
   - Nhấn `Ctrl+X`, sau đó `Y`, rồi `Enter` để lưu
   - Kiểm tra thay đổi: `cat template.yaml`

5. **Build Lại**:
   ```bash
   sam build
   ```

## Các Bước Tiếp Theo

Sau khi build thành công:
- Triển khai ứng dụng của bạn bằng `sam deploy`
- Test locally bằng `sam local invoke`
- Giám sát logs bằng CloudWatch
- Lặp lại và cải thiện ứng dụng serverless của bạn

## Lợi Ích Chính Của AWS SAM

- **Cú Pháp Đơn Giản**: Dễ dàng hơn CloudFormation thuần
- **Test Local**: Test các hàm Lambda trên máy local
- **Best Practices Tích Hợp Sẵn**: Security, monitoring và logging
- **Quick Start Templates**: Các ví dụ có sẵn để bắt đầu nhanh chóng
- **Tích Hợp**: Hoạt động liền mạch với các dịch vụ AWS

## Best Practices (Thực Hành Tốt Nhất)

1. Luôn chỉ định đúng phiên bản Python runtime
2. Giữ requirements.txt của bạn được cập nhật
3. Sử dụng biến môi trường cho cấu hình
4. Bật X-ray tracing cho các ứng dụng production
5. Triển khai xử lý lỗi phù hợp trong các hàm Lambda
6. Sử dụng CloudWatch Logs để debugging và monitoring

## Các Lệnh CLI SAM Quan Trọng

| Lệnh | Mô Tả |
|------|-------|
| `sam init` | Khởi tạo dự án SAM mới |
| `sam build` | Build ứng dụng SAM |
| `sam deploy` | Triển khai ứng dụng lên AWS |
| `sam local invoke` | Test hàm Lambda locally |
| `sam local start-api` | Chạy API Gateway locally |
| `sam logs` | Lấy logs từ CloudWatch |
| `sam validate` | Kiểm tra template có hợp lệ không |

## Thuật Ngữ Quan Trọng

- **Serverless**: Kiến trúc không cần quản lý server
- **Lambda Function**: Hàm chạy trên AWS Lambda
- **Template**: File YAML định nghĩa infrastructure
- **Build Artifacts**: Các file được tạo ra sau khi build
- **Runtime**: Môi trường thực thi (Python, Node.js, v.v.)
- **Handler**: Hàm entry point được Lambda gọi
- **Event**: Dữ liệu đầu vào được truyền cho Lambda function

---

**Ghi Chú**: Hướng dẫn này dựa trên phiên thực hành Cloud Shell minh họa các kiến thức cơ bản về AWS SAM framework để phát triển ứng dụng serverless.
