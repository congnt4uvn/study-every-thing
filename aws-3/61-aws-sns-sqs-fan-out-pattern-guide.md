# Hướng Dẫn AWS SNS + SQS Fan-Out Pattern

## Tổng Quan

Mô hình fan-out SNS + SQS là một kiến trúc mạnh mẽ để phân phối thông điệp đến nhiều hàng đợi SQS. Thay vì gửi thông điệp riêng lẻ đến từng hàng đợi (có thể gây ra vấn đề khi ứng dụng gặp sự cố, lỗi phân phối, hoặc mở rộng quy mô), mô hình này sử dụng Amazon SNS như một trung tâm để phát thông điệp đến nhiều người đăng ký.

## Mô Hình Fan-Out

### Cách Hoạt Động

1. **Đẩy một lần vào SNS topic**: Ứng dụng của bạn gửi thông điệp đến một SNS topic duy nhất
2. **Đăng ký nhiều hàng đợi SQS**: Mỗi hàng đợi SQS đăng ký với SNS topic
3. **Phân phối tự động**: Tất cả các hàng đợi đã đăng ký nhận thông điệp tự động

### Ví Dụ Kiến Trúc

```
Dịch Vụ Mua Hàng
    ↓
SNS Topic
    ↓ ↓
Hàng Đợi Dịch Vụ Chống Gian Lận    Hàng Đợi Dịch Vụ Vận Chuyển
```

### Lợi Ích Chính

- **Mô hình tách biệt hoàn toàn**: Các dịch vụ không cần biết về nhau
- **Không mất dữ liệu**: Thông điệp được phân phối đáng tin cậy đến tất cả người đăng ký
- **Lưu trữ dữ liệu bền vững**: SQS cung cấp lưu trữ thông điệp lâu dài
- **Xử lý trì hoãn**: Xử lý thông điệp theo tốc độ của bạn
- **Khả năng thử lại**: Có thể thử lại khi xử lý thất bại
- **Khả năng mở rộng**: Thêm nhiều hàng đợi SQS làm người đăng ký theo thời gian
- **Phân phối liên vùng**: SNS topics có thể gửi thông điệp đến các hàng đợi SQS ở các vùng khác nhau

### Điều Kiện Tiên Quyết

Đảm bảo **chính sách truy cập hàng đợi SQS** của bạn cho phép SNS topic ghi vào hàng đợi. Điều này rất quan trọng để mô hình fan-out hoạt động đúng cách.

## Trường Hợp Sử Dụng: Sự Kiện S3 Đến Nhiều Hàng Đợi

### Vấn Đề

Amazon S3 có một hạn chế: đối với một tổ hợp loại sự kiện (ví dụ: tạo object) và tiền tố (ví dụ: `images/`), bạn chỉ có thể có **một quy tắc sự kiện S3**.

### Giải Pháp

Sử dụng mô hình fan-out để phân phối sự kiện S3 đến nhiều đích:

```
S3 Bucket (tạo object)
    ↓
SNS Topic
    ↓ ↓ ↓
Hàng Đợi SQS 1    Hàng Đợi SQS 2    Lambda Function
```

Mô hình này cho phép bạn:
- Gửi sự kiện S3 đến nhiều hàng đợi SQS
- Đăng ký các dịch vụ khác (Lambda functions, thông báo email, v.v.)
- Định tuyến sự kiện đến nhiều đích khác nhau

## SNS Đến S3 Qua Kinesis Data Firehose

Bạn có thể lưu trữ thông điệp SNS trực tiếp vào Amazon S3 bằng Kinesis Data Firehose (KDF):

```
Dịch Vụ Mua Hàng
    ↓
SNS Topic
    ↓
Kinesis Data Firehose
    ↓
Amazon S3 (hoặc các đích KDF khác)
```

Kiến trúc này cung cấp khả năng mở rộng cho việc lưu trữ thông điệp từ SNS topic của bạn đến các đích khác nhau được hỗ trợ bởi Kinesis Data Firehose.

## Mô Hình Fan-Out SNS FIFO + SQS FIFO

### Tổng Quan

Amazon SNS hỗ trợ khả năng **FIFO (First-In-First-Out)** để duy trì thứ tự thông điệp.

### Kiến Trúc

```
Nhà Sản Xuất (gửi: 1, 2, 3, 4)
    ↓
SNS FIFO Topic
    ↓ ↓
Hàng Đợi SQS FIFO 1    Hàng Đợi SQS FIFO 2
(nhận: 1, 2, 3, 4)     (nhận: 1, 2, 3, 4)
```

### Tính Năng

- **Sắp xếp theo message group ID**: Các thông điệp trong cùng nhóm được xử lý theo thứ tự
- **Khử trùng lặp**: Sử dụng deduplication ID hoặc khử trùng dựa trên nội dung
- **Tương thích người đăng ký**: Cả hàng đợi SQS standard và FIFO đều có thể đăng ký
- **Giới hạn thông lượng**: Giới hạn ở mức thông lượng giống như hàng đợi SQS FIFO

### Khi Nào Sử Dụng

Sử dụng SNS FIFO khi bạn cần:
- Khả năng fan-out
- Sắp xếp thông điệp
- Khử trùng lặp

### Ví Dụ

```
Dịch Vụ Mua Hàng
    ↓
SNS FIFO Topic
    ↓ ↓
Dịch Vụ Chống Gian Lận (SQS FIFO)    Dịch Vụ Vận Chuyển (SQS FIFO)
```

## Lọc Thông Điệp Trong SNS

### Lọc Thông Điệp Là Gì?

Lọc thông điệp sử dụng **chính sách JSON** để lọc thông điệp nào được phân phối đến mỗi đăng ký. Nếu một đăng ký không có chính sách lọc, nó sẽ nhận mọi thông điệp (hành vi mặc định).

### Ví Dụ Tình Huống

Một dịch vụ mua hàng gửi thông điệp giao dịch đến SNS topic:

```json
{
  "orderNumber": "12345",
  "product": "pencil",
  "quantity": 4,
  "state": "placed"
}
```

### Ví Dụ Chính Sách Lọc

**Cho Đơn Hàng Đã Đặt:**
```json
{
  "state": ["placed"]
}
```

**Cho Đơn Hàng Đã Hủy:**
```json
{
  "state": ["canceled"]
}
```

**Cho Đơn Hàng Bị Từ Chối:**
```json
{
  "state": ["declined"]
}
```

### Kiến Trúc Với Lọc

```
Dịch Vụ Mua Hàng
    ↓
SNS Topic
    ↓ ↓ ↓ ↓
Hàng Đợi Đơn Đã Đặt    Hàng Đợi Đơn Đã Hủy    Email Đơn Hủy    Hàng Đợi Tất Cả Đơn
(lọc: placed)          (lọc: canceled)         (lọc: canceled)  (không lọc)
```

### Lợi Ích

- **Giảm xử lý**: Người đăng ký chỉ nhận thông điệp liên quan
- **Tối ưu chi phí**: Ít overhead xử lý thông điệp hơn
- **Linh hoạt**: Người tiêu dùng khác nhau có thể lọc cho các loại thông điệp khác nhau
- **Khả năng mở rộng**: Dễ dàng thêm đăng ký được lọc mới

## Điểm Chính Cần Nhớ

1. **Mô hình fan-out** giải quyết vấn đề phân phối thông điệp đến nhiều đích
2. **Chính sách truy cập SQS** phải cho phép SNS ghi vào hàng đợi
3. **Phân phối liên vùng** được hỗ trợ đầy đủ
4. **Hạn chế sự kiện S3** có thể được khắc phục bằng mô hình fan-out
5. **FIFO topics và queues** duy trì thứ tự trong khi hỗ trợ fan-out
6. **Lọc thông điệp** cho phép phân phối thông điệp có mục tiêu đến người đăng ký cụ thể
7. Mô hình cung cấp **kiến trúc tách biệt, có khả năng mở rộng** không mất dữ liệu

## Mẹo Thi

- Hiểu khi nào sử dụng fan-out so với thông điệp hàng đợi trực tiếp
- Biết cách cấu hình chính sách truy cập SQS cho SNS
- Nhớ hạn chế quy tắc sự kiện S3 và giải pháp fan-out
- Hiểu các tính năng FIFO: sắp xếp, khử trùng lặp và giới hạn thông lượng
- Quen thuộc với chính sách lọc thông điệp và các trường hợp sử dụng của chúng
- Biết tích hợp giữa SNS và Kinesis Data Firehose

---

*Hướng dẫn này bao gồm các khái niệm thiết yếu về mô hình fan-out AWS SNS + SQS, khả năng FIFO và lọc thông điệp để xây dựng kiến trúc thông điệp có khả năng mở rộng và tách biệt.*