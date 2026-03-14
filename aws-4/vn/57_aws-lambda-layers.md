# AWS Lambda Layers - Tài Liệu Học Tập

## Tổng Quan
Hướng dẫn này trình bày cách sử dụng AWS Lambda layers để thêm các thư viện bên ngoài vào các Lambda function mà không cần đóng gói chúng trực tiếp trong deployment package.

## Lambda Layers là gì?
Lambda layers là cơ chế phân phối cho các thư viện, custom runtime, và các dependencies khác của function. Chúng giúp bạn:
- Quản lý dependencies tách biệt khỏi mã nguồn function
- Chia sẻ các component chung giữa nhiều function
- Giữ deployment package nhỏ gọn

## Ví Dụ Thực Hành: Sử Dụng Thư Viện Pandas với Lambda Layers

### Bước 1: Tạo Lambda Function
1. Truy cập AWS Lambda console
2. Click "Create function"
3. **Tên function**: `Lambda-layer-demo`
4. **Runtime**: Python 3.13 (hoặc phiên bản mới nhất)
5. Click "Create function"

### Bước 2: Thêm Code với External Dependency
Code của function import và sử dụng thư viện Pandas để xử lý dữ liệu:

```python
import pandas as pd

# Tạo dữ liệu mẫu
# Lọc dữ liệu sử dụng thư viện Pandas
```

**Quan trọng**: Ở bước này, function sẽ lỗi vì Pandas không được bao gồm mặc định.

### Bước 3: Deploy và Test (Mong Đợi Lỗi)
1. Click "Deploy" để lưu code
2. Đi tới tab "Test"
3. Click "Test" để thực thi function
4. **Kết quả mong đợi**: Lỗi với thông báo "Unable to find the module pandas"

### Bước 4: Thêm Lambda Layer
1. Cuộn xuống phần "Layers" trong cấu hình function
2. Click "Add a layer" ở cuối trang
3. Chọn "AWS layers" (các layer được AWS cung cấp sẵn)
4. Chọn: **AWSSDK Pandas-Python313 Version 1**
5. Xác nhận thêm layer

### Bước 5: Test Lại (Thành Công)
Sau khi thêm layer, test function lại. Lúc này function sẽ chạy thành công với quyền truy cập vào thư viện Pandas.

## Các Khái Niệm Chính

### Lợi Ích của Lambda Layers
- **Tách biệt mối quan tâm**: Giữ các thư viện tách biệt khỏi application code
- **Khả năng tái sử dụng**: Chia sẻ layer giữa nhiều function
- **Cập nhật dễ dàng**: Cập nhật dependencies mà không cần sửa function code
- **Tối ưu kích thước**: Giữ function deployment package nhỏ hơn

### Các Loại Layer
- **AWS layers**: Layer được AWS cung cấp sẵn (ví dụ: AWS SDK, Pandas)
- **Custom layers**: Layer bạn tự tạo với các dependency cụ thể
- **Public layers**: Layer được cộng đồng chia sẻ

## Best Practices (Thực Hành Tốt Nhất)
1. Sử dụng AWS-provided layers khi có sẵn (được duy trì và tối ưu)
2. Giữ layer theo version cụ thể để đảm bảo tính nhất quán
3. Giới hạn kích thước layer: 50 MB (đã nén) mỗi layer
4. Tối đa 5 layers cho mỗi function
5. Layers được giải nén vào thư mục `/opt` trong môi trường thực thi Lambda

## Xử Lý Sự Cố
- Nếu không tìm thấy module sau khi thêm layer, hãy kiểm tra:
  - Phiên bản runtime khớp nhau (ví dụ: Python 3.13)
  - Layer tương thích với runtime của function
  - Layer đã được gắn đúng vào function

## Câu Hỏi Ôn Tập
1. Lambda layers giải quyết vấn đề gì?
2. Số lượng layer tối đa bạn có thể gắn vào một Lambda function là bao nhiêu?
3. Tại sao bạn nên chọn AWS-provided layer thay vì custom layer?
4. Điều gì xảy ra khi bạn test một Lambda function với external dependencies trước khi thêm layer cần thiết?

## Học Thêm
- Khám phá cách tạo custom Lambda layers
- Tìm hiểu về versioning và quản lý layer
- Nghiên cứu chia sẻ layer giữa các AWS account
- Tìm hiểu triển khai layer với các công cụ IaC (CloudFormation, Terraform)
