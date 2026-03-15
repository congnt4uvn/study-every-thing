# AWS API Gateway Mapping Templates (Mẫu Ánh Xạ)

## Tổng quan
Hướng dẫn này giới thiệu về mapping templates (mẫu ánh xạ) trong AWS API Gateway và cách chúng tích hợp với Lambda functions để chuyển đổi dữ liệu request và response.

## Các khái niệm chính

### 1. Các kiểu tích hợp API Gateway
- **Lambda Proxy Integration**: Lambda function trả về trực tiếp status code và body
- **Direct Integration**: API Gateway xử lý định dạng response, Lambda chỉ trả về dữ liệu

### 2. Mapping Templates (Mẫu ánh xạ)
Mapping templates cho phép bạn chuyển đổi input và output của các API Gateway integrations.

## Ví dụ thực hành: Tạo Mapping Template

### Bước 1: Tạo API Gateway Resource
1. Tạo resource mới có tên `mapping`
2. Thêm phương thức GET vào resource này
3. Chọn Lambda function integration

### Bước 2: Tạo Lambda Function
```python
# Tên function: API-gateway-mapping-get
# Runtime: Python 3.11
def lambda_handler(event, context):
    return {
        "example": "hello world"
    }
```

**Quan trọng**: KHÔNG bật Lambda proxy integration cho ví dụ này.

### Bước 3: Kiểm tra thiết lập ban đầu
- Lambda function trả về: `{"example": "hello world"}`
- API Gateway chuyển kết quả này qua với status 200
- Không cần wrapper cho status code hoặc body (chế độ non-proxy)

### Bước 4: Thêm Mapping Template

#### Vị trí
Vào **Integration Response** → **Mapping Templates**

#### Cấu hình
- **Content Type**: `application/json`
- **Template Body**:
```json
{
    "myKey": "myValue",
    "renamedKey": $input.json('$.example')
}
```

#### Giải thích cú pháp Template
- `$input`: Đại diện cho JSON nhận được từ input
- `$input.json('$.example')`: Trích xuất giá trị của khóa "example"
- Template chuyển đổi output của Lambda thành cấu trúc mới

### Bước 5: Kiểm tra kết quả
**Trước khi dùng mapping template**:
```json
{
    "example": "hello world"
}
```

**Sau khi dùng mapping template**:
```json
{
    "myKey": "myValue",
    "renamedKey": "hello world"
}
```

## Các trường hợp sử dụng Mapping Templates

1. **Chuyển đổi dữ liệu**: Đổi tên khóa, cấu trúc lại JSON
2. **Thêm dữ liệu tĩnh**: Bao gồm các giá trị cố định trong mọi response
3. **Integration Request**: Chuyển đổi API requests trước khi gửi đến Lambda
4. **Integration Response**: Chuyển đổi response của Lambda trước khi trả về API
5. **Tích hợp hệ thống cũ**: Điều chỉnh giữa các định dạng dữ liệu khác nhau

## Lưu ý quan trọng

- Mapping templates có sẵn cho một số loại integration nhất định
- Có thể dùng cho cả Integration Request và Integration Response
- Cú pháp có thể phức tạp, nhưng với kỳ thi AWS, bạn chỉ cần biết chúng tồn tại
- Hữu ích để làm các hệ thống khác nhau hoạt động cùng nhau mà không cần thay đổi code

## Thực hành tốt nhất

1. Sử dụng proxy integration cho các trường hợp pass-through đơn giản
2. Sử dụng mapping templates khi cần chuyển đổi dữ liệu
3. Kiểm tra kỹ mapping templates trong API Gateway console
4. Ghi chép lại logic của template cho các thành viên trong nhóm

## Mẹo cho kỳ thi

- **Ghi nhớ**: Mapping templates cho phép chuyển đổi input/output
- Bạn không cần ghi nhớ cú pháp chính xác cho các kỳ thi AWS
- Tập trung hiểu KHI NÀO nên sử dụng mapping templates
- Biết sự khác biệt giữa proxy và non-proxy integration

## Tóm tắt

Mapping templates trong API Gateway cung cấp khả năng chuyển đổi mạnh mẽ:
- Chuyển đổi responses của Lambda mà không cần thay đổi code function
- Thêm hoặc xóa các trường dữ liệu một cách linh hoạt
- Tích hợp với các hệ thống cũ yêu cầu định dạng cụ thể
- Có sẵn cho cấu hình Integration Request và Response

## Thuật ngữ quan trọng

- **Mapping Template**: Mẫu ánh xạ - công cụ để chuyển đổi dữ liệu
- **Integration Response**: Phản hồi tích hợp
- **Lambda Proxy Integration**: Tích hợp Lambda proxy
- **Direct Integration**: Tích hợp trực tiếp
- **Content Type**: Loại nội dung

---
**Ngày tạo**: 15 tháng 3, 2026
**Chủ đề**: AWS API Gateway, Lambda Integration, Mapping Templates
