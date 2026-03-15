# AWS DynamoDB & S3: Chiến Lược Tích Hợp

## Tổng Quan
Tài liệu này trình bày hai mẫu tích hợp mạnh mẽ giữa Amazon DynamoDB và Amazon S3, cho phép bạn tận dụng điểm mạnh của cả hai dịch vụ để đạt hiệu suất và hiệu quả chi phí tối ưu.

---

## Hiểu Giới Hạn Của DynamoDB

**Ràng buộc quan trọng**: DynamoDB chỉ có thể lưu trữ tối đa **400 KB** dữ liệu cho mỗi mục.

Giới hạn này khiến DynamoDB không phù hợp để lưu trữ:
- Hình ảnh
- Video
- Tài liệu lớn
- Các đối tượng nhị phân lớn khác

---

## Chiến Lược 1: Lưu Trữ Đối Tượng Lớn Bằng S3 Với Metadata Trong DynamoDB

### Mẫu Kiến Trúc
Sử dụng S3 để lưu trữ đối tượng lớn và DynamoDB để lưu trữ metadata tham chiếu.

### Cách Hoạt Động

#### Quy Trình Tải Lên
1. **Tải đối tượng lớn** (ví dụ: hình ảnh) lên Amazon S3
2. **Nhận khóa đối tượng** từ S3
3. **Lưu metadata** trong DynamoDB với tham chiếu đến S3

#### Ví Dụ Cấu Trúc Bảng DynamoDB
```
Bảng Products:
┌──────────────┬──────────────┬─────────────────────────────┐
│ Product ID   │ Product Name │ Image URL                   │
├──────────────┼──────────────┼─────────────────────────────┤
│ 12345       │ Laptop       │ s3://bucket/images/12345.jpg│
└──────────────┴──────────────┴─────────────────────────────┘
```

#### Quy Trình Đọc
1. **Truy vấn DynamoDB** để lấy metadata (bao gồm URL S3)
2. **Lấy đối tượng lớn** từ S3 bằng URL
3. **Tái tạo dữ liệu hoàn chỉnh** bằng cách kết hợp metadata và đối tượng

### Lợi Ích
- ✅ **Dung lượng nhỏ trong DynamoDB**: Chỉ lưu metadata
- ✅ **Khả năng mở rộng**: Có thể xử lý số lượng sản phẩm không giới hạn
- ✅ **Tiết kiệm chi phí**: Mỗi dịch vụ được sử dụng theo điểm mạnh
- ✅ **Lập chỉ mục nhanh**: DynamoDB cung cấp tra cứu metadata nhanh chóng

### Trường Hợp Sử Dụng Tốt Nhất
- Danh mục sản phẩm thương mại điện tử với hình ảnh
- Hồ sơ người dùng với ảnh đại diện
- Hệ thống quản lý tài liệu
- Thư viện phương tiện

---

## Chiến Lược 2: Sử Dụng DynamoDB Để Lập Chỉ Mục Metadata Đối Tượng S3

### Mẫu Kiến Trúc
Sử dụng DynamoDB làm chỉ mục có thể truy vấn cho metadata đối tượng S3.

### Cách Hoạt Động

#### Luồng Thiết Lập
1. **Tải đối tượng** lên Amazon S3
2. **Thông báo sự kiện S3** được kích hoạt khi tải đối tượng
3. **Hàm Lambda** được gọi tự động
4. **Lambda lưu metadata** vào bảng DynamoDB

#### Ví Dụ Metadata
Lưu trữ các thuộc tính như:
- Kích thước đối tượng
- Ngày/thời gian tải lên
- Người tạo/chủ sở hữu
- Loại nội dung
- Thẻ tùy chỉnh
- Quyền truy cập

### Tại Sao Cần Lập Chỉ Mục Metadata S3?

#### Vấn Đề Khi Chỉ Dùng S3
- S3 **không được thiết kế để truy vấn**
- S3 được tối ưu hóa để **lưu trữ** đối tượng lớn
- Khả năng tìm kiếm/lọc đối tượng hạn chế
- Không có khả năng truy vấn giống cơ sở dữ liệu

#### Giải Pháp Với DynamoDB
DynamoDB cung cấp khả năng truy vấn mạnh mẽ cho các đối tượng S3.

### Ví Dụ Truy Vấn Có Thể Thực Hiện

| Loại Truy Vấn | Mô Tả |
|--------------|-------|
| **Theo Timestamp** | Tìm tất cả đối tượng được tải lên sau một ngày cụ thể |
| **Theo Khách Hàng** | Tính tổng dung lượng lưu trữ được sử dụng bởi khách hàng |
| **Theo Thuộc Tính** | Liệt kê tất cả đối tượng có thẻ hoặc thuộc tính cụ thể |
| **Phạm Vi Ngày** | Tìm tất cả đối tượng được tải lên trong một khoảng thời gian |
| **Theo Kích Thước** | Truy vấn các đối tượng lớn hơn một kích thước nhất định |

### Quy Trình Làm Việc
1. **Truy vấn DynamoDB** với tiêu chí tìm kiếm
2. **Nhận kết quả** với tham chiếu đối tượng S3
3. **Lấy đối tượng** từ bucket S3 khi cần

---

## Bảng So Sánh

| Khía Cạnh | Chiến Lược 1: Đối Tượng Lớn | Chiến Lược 2: Lập Chỉ Mục Metadata |
|-----------|----------------------------|-----------------------------------|
| **Mục Đích Chính** | Lưu trữ tệp lớn với metadata | Làm cho S3 có thể tìm kiếm/truy vấn |
| **Luồng Dữ Liệu** | App → S3 → DynamoDB | S3 → Lambda → DynamoDB |
| **Trường Hợp Dùng** | Danh mục sản phẩm, media | Phân tích, tìm kiếm, kiểm toán |
| **Đối Tượng Truy Vấn** | Metadata sản phẩm/mục | Metadata đối tượng S3 |
| **Kích Hoạt** | Tải lên từ ứng dụng | Thông báo sự kiện S3 |

---

## Phương Pháp Hay Nhất Cho Kiến Trúc

### Phương Pháp Hay Nhất Chiến Lược 1
1. Chỉ lưu trữ metadata thiết yếu trong DynamoDB
2. Sử dụng quy ước đặt tên nhất quán cho khóa S3
3. Triển khai xử lý lỗi phù hợp cho các lỗi S3
4. Xem xét sử dụng URL được ký trước của S3 để truy cập an toàn
5. Thiết lập các chính sách vòng đời S3 thích hợp

### Phương Pháp Hay Nhất Chiến Lược 2
1. Sử dụng Lambda để lập chỉ mục metadata thời gian thực
2. Bao gồm metadata toàn diện để truy vấn tốt hơn
3. Thiết lập các chỉ mục DynamoDB (GSI/LSI) cho các truy vấn phổ biến
4. Xử lý lỗi Lambda với cơ chế thử lại
5. Xem xét chi phí cho các lần gọi Lambda

---

## Lợi Thế Chính Của Tích Hợp

### Sử Dụng Mỗi Dịch Vụ Theo Điểm Mạnh
- **Amazon S3**: Xuất sắc để lưu trữ đối tượng lớn
- **DynamoDB**: Hoàn hảo để lưu trữ metadata có thể lập chỉ mục, truy vấn
- **Kết Hợp**: Hiệu suất và hiệu quả chi phí tối ưu

### Khả Năng Mở Rộng
- Cả hai chiến lược đều mở rộng độc lập
- S3 có thể lưu trữ số lượng đối tượng không giới hạn
- DynamoDB có thể xử lý khối lượng truy vấn khổng lồ

### Tối Ưu Hóa Chi Phí
- Chỉ trả cho lưu trữ S3 cho các đối tượng lớn
- Chỉ trả cho DynamoDB cho lưu trữ metadata
- Tiết kiệm hơn so với lưu trữ mọi thứ trong một dịch vụ

---

## Các Trường Hợp Sử Dụng Phổ Biến

### Thương Mại Điện Tử
- Hình ảnh sản phẩm với thuộc tính có thể tìm kiếm
- Lưu trữ tài liệu khách hàng
- Quản lý hóa đơn và biên lai

### Truyền Thông & Giải Trí
- Thư viện tệp video/audio
- Tạo và lập chỉ mục hình thu nhỏ
- Quản lý metadata nội dung

### Y Tế
- Hình ảnh y tế (tệp DICOM)
- Lưu trữ tài liệu bệnh nhân
- Tuân thủ và theo dõi kiểm toán

### Doanh Nghiệp
- Hệ thống quản lý tài liệu
- Giải pháp sao lưu và lưu trữ
- Lưu trữ và phân tích tệp nhật ký

---

## Mẹo Thi Cử 🎯

Các mẫu tích hợp này **thường được kiểm tra** trong các kỳ thi chứng chỉ AWS:

1. Nhớ **giới hạn 400 KB** cho các mục DynamoDB
2. Hiểu khi nào sử dụng **S3 + DynamoDB** so với các giải pháp khác
3. Biết **hai chiến lược tích hợp chính**
4. Nhận biết các kịch bản yêu cầu **lập chỉ mục metadata**
5. Hiểu vai trò của **Lambda** trong lập chỉ mục theo sự kiện

---

## Các Dịch Vụ AWS Liên Quan

- **Amazon S3**: Lưu trữ đối tượng
- **Amazon DynamoDB**: Cơ sở dữ liệu NoSQL
- **AWS Lambda**: Điện toán serverless
- **S3 Event Notifications**: Kích hoạt sự kiện khi tải lên
- **DynamoDB Streams**: Theo dõi thay đổi trong DynamoDB

---

*Tài Liệu Học Tập | Tích Hợp AWS DynamoDB & S3*
