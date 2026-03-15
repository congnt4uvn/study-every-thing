# AWS DynamoDB - Time To Live (TTL)

## Tổng Quan
Time To Live (TTL) là tính năng cho phép bạn tự động xóa các mục (items) sau khi timestamp hết hạn trong bảng DynamoDB.

## Cách Hoạt Động

### Khái Niệm Cơ Bản
- Định nghĩa một cột cụ thể chứa timestamp hết hạn
- Khi thời gian hiện tại vượt quá giá trị trong cột này, DynamoDB sẽ tự động xóa mục đó
- **Không tiêu tốn Write Capacity Units (WCU)** - xóa hoàn toàn miễn phí

### Định Dạng Timestamp
- Phải là một **số** đại diện cho giá trị **Unix Epoch timestamp**
- Ví dụ: 1710518400 (đại diện cho 15/3/2025 00:00:00 UTC)

## Quy Trình Hoạt Động của TTL

### Ví Dụ: Bảng Dữ Liệu Session
| User ID | Session ID | Expired Time (TTL) |
|---------|------------|-------------------|
| user123 | sess456    | 1710518400        |

### Quy Trình Xóa
1. **Đánh Dấu Hết Hạn**: DynamoDB định kỳ quét bảng
   - So sánh thời gian hiện tại với giá trị cột TTL
   - Đánh dấu các mục có TTL < thời gian hiện tại

2. **Xóa Mục**: Một quy trình thứ hai quét và xóa các mục đã được đánh dấu
   - Xóa tự động
   - Mục cũng được xóa khỏi các index (LSI và GSI)

## Những Điểm Quan Trọng Cần Lưu Ý

### Thời Gian
- Các mục hết hạn được xóa **trong vòng vài ngày** sau khi hết hạn (không ngay lập tức)
- Có thể mất **tới 48 giờ** để thấy các mục bị xóa hoàn toàn

### Đọc Các Mục Đã Hết Hạn
- ⚠️ **Các mục đã hết hạn nhưng chưa bị xóa vẫn sẽ xuất hiện** trong:
  - Thao tác Read (đọc)
  - Thao tác Query (truy vấn)
  - Thao tác Scan (quét)
- **Giải pháp**: Triển khai lọc phía client để loại trừ các mục đã hết hạn

### Tích Hợp DynamoDB Streams
- Mỗi lần xóa TTL tạo ra một mục nhập thao tác xóa trong DynamoDB Streams
- Cho phép khôi phục hoặc theo dõi các mục đã bị xóa nếu cần

### Hành Vi của Index
- Các mục hết hạn được tự động xóa khỏi:
  - Local Secondary Indexes (LSI)
  - Global Secondary Indexes (GSI)

## Các Trường Hợp Sử Dụng

1. **Quản Lý Lưu Trữ Dữ Liệu**
   - Chỉ giữ lại các mục hiện tại, có liên quan
   - Tự động loại bỏ dữ liệu cũ

2. **Tuân Thủ Quy Định**
   - Tuân thủ chính sách lưu trữ dữ liệu
   - Tự động tuân thủ các yêu cầu GDPR, HIPAA

3. **Quản Lý Session**
   - Tự động hết hạn session người dùng sau thời gian không hoạt động
   - Dọn dẹp dữ liệu session tạm thời

4. **Tối Ưu Chi Phí**
   - Giảm chi phí lưu trữ bằng cách xóa dữ liệu lỗi thời
   - Không có chi phí bổ sung cho việc xóa

## Thực Hành Tốt Nhất

- ✅ Đặt giá trị TTL phù hợp dựa trên trường hợp sử dụng
- ✅ Triển khai lọc phía client cho các thao tác đọc nếu cần tính nhất quán ngay lập tức
- ✅ Sử dụng DynamoDB Streams để lưu trữ hoặc backup các mục đã xóa
- ✅ Giám sát việc xóa TTL thông qua CloudWatch metrics
- ✅ Kiểm tra hành vi TTL trong môi trường phát triển trước khi triển khai production

## Những Điểm Chính Cần Nhớ

- **Xóa miễn phí** - không tiêu tốn WCU
- **Xóa theo thời gian** - không ngay lập tức (tới 48 giờ)
- **Tích hợp Stream** - các mục đã xóa xuất hiện trong DynamoDB Streams
- **Khuyến nghị lọc phía client** - cho các truy vấn liên quan đến mục TTL
