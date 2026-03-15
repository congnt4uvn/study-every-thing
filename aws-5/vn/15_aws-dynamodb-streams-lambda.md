# Tài Liệu Học AWS: DynamoDB Streams với Lambda Triggers

## Tổng Quan
Hướng dẫn này giới thiệu cách kích hoạt và cấu hình DynamoDB Streams để tự động kích hoạt các hàm AWS Lambda xử lý dữ liệu theo thời gian thực.

## DynamoDB Streams là gì?

DynamoDB Streams ghi lại chuỗi các thay đổi cấp độ item theo thứ tự thời gian trong bất kỳ bảng DynamoDB nào và lưu trữ thông tin này trong nhật ký trong tối đa 24 giờ. Các ứng dụng có thể truy cập nhật ký này và xem dữ liệu như trước và sau khi được sửa đổi.

## Các Khái Niệm Chính

### 1. Kích Hoạt DynamoDB Streams

**Các bước:**
1. Điều hướng đến bảng DynamoDB của bạn (ví dụ: bảng `users_post`)
2. Chuyển đến tab **Exports and Streams**
3. Tìm phần **DynamoDB stream details**
4. Nhấp **Enable stream**

### 2. Các Loại Stream View

Khi kích hoạt stream, bạn có thể chọn thông tin nào được ghi:

- **Keys only** - Chỉ các thuộc tính khóa của item được sửa đổi
- **New image** - Toàn bộ item sau khi được sửa đổi
- **Old image** - Toàn bộ item trước khi được sửa đổi
- **New and old images** - Cả hình ảnh mới và cũ của item (khuyến nghị để có thông tin tối đa)

### 3. Tạo Lambda Triggers

Sau khi stream được kích hoạt, bạn có thể tạo triggers tự động gọi các hàm Lambda khi items được sửa đổi.

**Các bước tạo trigger:**

1. Cuộn xuống phần **Trigger** trong chi tiết stream
2. Nhấp **Create trigger**
3. Chọn hoặc tạo một hàm Lambda

### 4. Thiết Lập Hàm Lambda

**Sử dụng Blueprint:**
- Tìm kiếm "DynamoDB" trong blueprints
- Chọn **DynamoDB process stream Python**
- Blueprint này ghi lại tất cả các cập nhật được thực hiện cho bảng

**Cấu hình:**
- **Tên hàm**: ví dụ: `Lambda-demo-DynamoDB-stream`
- **Execution role**: Tạo role mới với quyền Lambda cơ bản
  - **Quan trọng**: Chỉnh sửa role để thêm quyền đọc từ DynamoDB
  
**Cấu hình Trigger:**
- **Bảng DynamoDB**: Chọn bảng của bạn (ví dụ: `users_post`)
- **Batch size**: 100 (số lượng bản ghi đọc cùng một lúc)
- **Batch window**: Thời gian thu thập bản ghi trước khi gọi hàm (để hiệu quả hơn)
- **Starting position**: Vị trí bắt đầu đọc (TRIM_HORIZON hoặc LATEST)

## Các Trường Hợp Sử Dụng

- **Phân tích theo thời gian thực**: Xử lý thay đổi dữ liệu ngay lập tức
- **Sao chép dữ liệu**: Nhân bản dữ liệu sang các cơ sở dữ liệu hoặc dịch vụ khác
- **Thông báo**: Gửi thông báo khi các item cụ thể thay đổi
- **Kiểm toán**: Theo dõi tất cả các thay đổi đối với các item trong cơ sở dữ liệu
- **Sao chép đa vùng**: Giữ nhiều vùng đồng bộ

## Các Phương Pháp Hay Nhất

1. **Chọn loại stream view phù hợp** dựa trên nhu cầu của bạn
2. **Cấu hình quyền IAM đúng cách** để Lambda có thể đọc streams
3. **Đặt batch size thích hợp** để cân bằng thông lượng và chi phí
4. **Xử lý lỗi một cách linh hoạt** với xử lý lỗi đúng cách trong Lambda
5. **Giám sát các chỉ số stream** bằng CloudWatch
6. **Xem xét batch window** để tối ưu hóa chi phí

## Quyền Quan Trọng

Lambda execution role cần các quyền:
- `dynamodb:GetRecords`
- `dynamodb:GetShardIterator`
- `dynamodb:DescribeStream`
- `dynamodb:ListStreams`

## Tóm Tắt

DynamoDB Streams với Lambda triggers cung cấp một cách mạnh mẽ để phản ứng với các thay đổi dữ liệu theo thời gian thực. Bằng cách cấu hình streams đúng cách và thiết lập các hàm Lambda với quyền phù hợp, bạn có thể xây dựng kiến trúc hướng sự kiện tự động mở rộng quy mô.
