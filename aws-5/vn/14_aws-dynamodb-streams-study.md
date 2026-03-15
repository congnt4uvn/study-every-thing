# AWS DynamoDB Streams - Tài Liệu Học Tập

## Tổng Quan

DynamoDB Streams là tính năng ghi lại danh sách có thứ tự các thay đổi ở cấp độ item (tạo mới, cập nhật, xóa) xảy ra trong bảng DynamoDB.

## Khái Niệm Chính

### DynamoDB Streams Là Gì?

- **Luồng có thứ tự** các thay đổi ở cấp độ item trong bảng
- Ghi lại tất cả thay đổi: thêm mới, cập nhật và xóa
- Đại diện cho chuỗi thay đổi theo thời gian

### Điểm Đến Của Stream

Các bản ghi stream có thể được gửi đến nhiều dịch vụ AWS:

1. **Kinesis Data Streams (KDS)**
   - Chuyển tiếp DynamoDB Streams sang Kinesis để xử lý thêm

2. **AWS Lambda Functions**
   - Đọc trực tiếp từ DynamoDB Streams
   - Cho phép xử lý theo sự kiện không cần máy chủ

3. **Kinesis Client Library (KCL) Applications**
   - Ứng dụng tùy chỉnh có thể đọc dữ liệu stream trực tiếp

## Giới Hạn Quan Trọng

- **Thời Gian Lưu Trữ**: Chỉ 24 giờ
- **Hành Động Cần Thiết**: Lưu trữ dữ liệu vào nơi lưu trữ bền vững (ví dụ: Kinesis Data Streams) hoặc xử lý nhanh với Lambda/KCL

## Các Trường Hợp Sử Dụng Phổ Biến

### 1. Phản Ứng Thời Gian Thực
Phản ứng với các thay đổi trong bảng DynamoDB khi chúng xảy ra

### 2. Tương Tác Người Dùng
- Gửi email chào mừng cho người dùng mới
- Kích hoạt thông báo dựa trên thay đổi dữ liệu

### 3. Phân Tích
- Thực hiện phân tích thời gian thực trên các thay đổi dữ liệu
- Truyền dữ liệu đến nền tảng phân tích

### 4. Chuyển Đổi Dữ Liệu
- Tạo các bảng phát sinh trong DynamoDB
- Chuyển đổi và làm phong phú dữ liệu theo thời gian thực

### 5. Khả Năng Tìm Kiếm
- Gửi dữ liệu đến Amazon OpenSearch để lập chỉ mục
- Cho phép tìm kiếm toàn văn bản trên dữ liệu DynamoDB

### 6. Global Tables
- Cho phép sao chép giữa các vùng
- Nền tảng cho tính năng DynamoDB Global Tables

## Ví Dụ Kiến Trúc

```
Ứng Dụng
    ↓
  (tạo/cập nhật/xóa)
    ↓
Bảng DynamoDB
    ↓
DynamoDB Stream
    ↓
Kinesis Data Streams (KDS)
    ↓
Kinesis Data Firehose
    ↓
Amazon Redshift (Phân Tích)
```

**Mô Tả Luồng:**
1. Ứng dụng thực hiện các thao tác CRUD trên bảng DynamoDB
2. Thay đổi xuất hiện trong DynamoDB Stream
3. Stream được chuyển tiếp đến Kinesis Data Streams
4. Kinesis Data Firehose xử lý stream
5. Dữ liệu được tải vào Amazon Redshift để thực hiện truy vấn phân tích

## Thực Hành Tốt Nhất

- ✅ Xử lý streams trong khung thời gian lưu trữ 24 giờ
- ✅ Sử dụng Lambda cho xử lý theo sự kiện đơn giản
- ✅ Chuyển tiếp sang Kinesis Data Streams để lưu trữ lâu hơn
- ✅ Triển khai xử lý lỗi và logic thử lại
- ✅ Giám sát xử lý stream với CloudWatch

## Mẹo Học Tập

- Hiểu rõ giới hạn lưu trữ 24 giờ
- Biết các phương thức đọc dữ liệu khác nhau (Lambda, KDS, KCL)
- Nắm vững các trường hợp sử dụng phổ biến cho kịch bản thi
- Nhớ rằng streams là bắt buộc cho Global Tables

---

**Các Dịch Vụ AWS Liên Quan:**
- Amazon DynamoDB
- AWS Lambda
- Amazon Kinesis Data Streams
- Amazon Kinesis Data Firehose
- Amazon OpenSearch
- Amazon Redshift
