# Tích Hợp AWS Lambda và S3

## Tổng Quan
Hướng dẫn này trình bày cách cấu hình một hàm AWS Lambda để tự động được kích hoạt khi các đối tượng được tải lên bucket S3.

## Yêu Cầu Trước Khi Bắt Đầu
- Tài khoản AWS có quyền truy cập vào dịch vụ Lambda và S3
- Hiểu biết cơ bản về các dịch vụ AWS
- Quyền tạo các hàm Lambda và bucket S3

## Hướng Dẫn Từng Bước

### 1. Tạo Hàm Lambda
1. Truy cập vào dịch vụ AWS Lambda
2. Tạo một hàm mới có tên **Lambda-S3**
3. Chọn **Python 3.8** làm runtime
4. Nhấp "Create function" (Tạo hàm)

### 2. Tạo Bucket S3
1. Truy cập vào dịch vụ S3
2. Tạo một bucket mới với tên duy nhất (ví dụ: `demo-s3-event-stephane`)
3. **Quan trọng**: Đảm bảo bucket nằm trong cùng region với hàm Lambda của bạn (ví dụ: Ireland)
4. Cuộn xuống và nhấp "Create Bucket" (Tạo Bucket)

### 3. Cấu Hình Thông Báo Sự Kiện S3
1. Vào bucket vừa tạo
2. Chuyển đến tab **Properties** (Thuộc tính)
3. Cuộn xuống tìm phần **Event notifications** (Thông báo sự kiện)
4. Nhấp "Create event notification" (Tạo thông báo sự kiện)
5. Cấu hình thông báo:
   - **Name** (Tên): invoke-lambda
   - **Prefix** (Tiền tố): (để trống cho tất cả đối tượng)
   - **Suffix** (Hậu tố): (để trống cho tất cả đối tượng)
   - **Event types** (Loại sự kiện): Chọn "All object create events" (Tất cả sự kiện tạo đối tượng)
6. Đặt đích đến:
   - Chọn **Lambda function** (Hàm Lambda)
   - Chọn hàm Lambda của bạn từ danh sách thả xuống (Lambda-S3)
7. Lưu các thay đổi

### 4. Xác Minh Tích Hợp
1. Làm mới trang hàm Lambda của bạn
2. Bây giờ bạn sẽ thấy **S3** ở phía bên trái như một trigger (bộ kích hoạt)
3. Điều này xác nhận rằng S3 đã được cấu hình để gọi hàm Lambda của bạn

### 5. Chỉnh Sửa Hàm Lambda
Cập nhật mã của hàm Lambda để in dữ liệu sự kiện:

```python
import json

def lambda_handler(event, context):
    print(event)
    # Xử lý sự kiện S3 tại đây
    return {
        'statusCode': 200,
        'body': json.dumps('Xin chào từ Lambda!')
    }
```

Triển khai các thay đổi.

### 6. Hiểu Về Quyền
- Chuyển đến **Configuration** (Cấu hình) → **Permissions** (Quyền) trong hàm Lambda của bạn
- Xem xét IAM role và execution policies
- Hàm Lambda cần có quyền phù hợp để được S3 gọi

## Các Khái Niệm Chính

### Thông Báo Sự Kiện S3
- S3 có thể gửi thông báo khi các sự kiện cụ thể xảy ra trong bucket
- Các đích hỗ trợ: Lambda, SNS, SQS
- Các loại sự kiện bao gồm: tạo đối tượng, xóa, khôi phục, v.v.

### Trigger Lambda
- S3 hoạt động như một nguồn sự kiện cho Lambda
- Khi một đối tượng được tải lên, S3 tự động gọi hàm Lambda
- Đối tượng sự kiện chứa metadata về hoạt động S3

### Nhất Quán Về Region
- **Quan trọng**: Hàm Lambda và bucket S3 phải nằm trong cùng một AWS region
- Các trigger xuyên region không được hỗ trợ trực tiếp

## Các Thực Hành Tốt Nhất
1. Luôn kiểm tra với các đối tượng nhỏ trước
2. Theo dõi nhật ký thực thi Lambda trong CloudWatch
3. Đặt giá trị timeout phù hợp cho hàm Lambda của bạn
4. Xem xét xử lý lỗi và logic thử lại
5. Lưu ý giới hạn đồng thời của Lambda khi xử lý tải S3 lượng lớn

## Các Trường Hợp Sử Dụng Phổ Biến
- Xử lý hình ảnh/video khi tải lên
- Xác thực và chuyển đổi dữ liệu
- Chuyển đổi định dạng tệp
- Kích hoạt quy trình làm việc dựa trên tải tệp lên
- Ghi nhật ký và kiểm tra các hoạt động S3

## Khắc Phục Sự Cố
- Nếu trigger không xuất hiện, kiểm tra quyền IAM
- Xác minh cả hai dịch vụ đều ở cùng một region
- Kiểm tra nhật ký CloudWatch để tìm lỗi thực thi
- Đảm bảo hàm Lambda có role thực thi phù hợp

## Tài Nguyên Bổ Sung
- Tài liệu AWS Lambda
- Tài liệu AWS S3 Event Notifications
- Các Thực Hành Tốt Nhất về AWS IAM
