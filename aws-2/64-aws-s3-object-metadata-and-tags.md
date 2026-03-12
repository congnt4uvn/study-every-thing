# AWS S3 Object Metadata và Tags

## Tổng quan

Hướng dẫn này trình bày về metadata do người dùng định nghĩa và các thẻ (tags) của đối tượng S3, giải thích mục đích, sự khác biệt và cách tìm kiếm các đối tượng trong S3 buckets.

## Metadata của Đối tượng do Người dùng Định nghĩa

### Metadata của Đối tượng là gì?

Khi bạn tải một đối tượng lên S3, bạn có thể gán metadata cho nó. Metadata về cơ bản là các cặp key-value được đính kèm vào đối tượng của bạn, cung cấp thông tin về chính đối tượng đó.

### Quy ước Đặt tên Metadata

- **Metadata do người dùng định nghĩa** phải có tên bắt đầu bằng `x-amz-meta-`
- AWS cũng tự động tạo metadata riêng của mình

### Ví dụ về Metadata

Đối với một đối tượng S3, bạn có thể thấy:

- `Content-Length`: 7.5 kilobytes (do AWS cung cấp)
- `Content-Type`: html (do AWS cung cấp)
- `x-amz-meta-origin`: paris (do người dùng định nghĩa)

Metadata có thể được truy xuất trong khi lấy đối tượng.

## Tags của Đối tượng S3

### Tags của Đối tượng là gì?

Tags của đối tượng S3 là các cặp key-value cho các đối tượng của bạn trong Amazon S3. Chúng được sử dụng phổ biến hơn metadata cho các mục đích cụ thể.

### Tags so với Metadata

Tags khác với metadata theo nhiều cách quan trọng:

- **Phân quyền chi tiết**: Tags có thể được sử dụng để cấp quyền truy cập vào các đối tượng cụ thể với các tags cụ thể
- **Mục đích phân tích**: Các công cụ như S3 Analytics có thể nhóm kết quả theo tags

### Ví dụ về Tags

Đối với một đối tượng S3, bạn có thể gán:

- `Project`: Blue
- `PHI` (Thông tin Sức khỏe Cá nhân): True

## Hạn chế Quan trọng: Khả năng Tìm kiếm

### Điểm Chính cần Ghi nhớ

⚠️ **Metadata và tags KHÔNG thể tìm kiếm trên Amazon S3**

- Bạn không thể lọc theo metadata
- Bạn không thể lọc theo tags
- Đây không phải là khả năng gốc của S3

## Cách Tìm kiếm Đối tượng S3

### Giải pháp: Chỉ mục Bên ngoài

Nếu bạn cần tìm kiếm S3 buckets của mình dựa trên metadata hoặc tags, bạn phải:

1. **Xây dựng chỉ mục bên ngoài** trong cơ sở dữ liệu (như DynamoDB)
2. **Lưu trữ tất cả metadata và tags** trong chỉ mục có thể tìm kiếm
3. **Thực hiện tìm kiếm** trên cơ sở dữ liệu bên ngoài (DynamoDB)
4. **Trích xuất kết quả** dưới dạng các đối tượng từ Amazon S3

### Mô hình Kiến trúc

```
Đối tượng S3 (với metadata/tags)
    ↓
Chỉ mục Bên ngoài (DynamoDB)
    ↓
Truy vấn Tìm kiếm → DynamoDB
    ↓
Kết quả → Đối tượng S3
```

### Mẹo Thi

Đây là một câu hỏi phổ biến trong kỳ thi và là một mô hình kiến trúc quan trọng cần hiểu cho các chứng chỉ AWS.

## Tóm tắt

- **Metadata**: Các cặp key-value cung cấp thông tin về đối tượng (do người dùng định nghĩa phải bắt đầu bằng `x-amz-meta-`)
- **Tags**: Các cặp key-value được sử dụng cho phân quyền và phân tích
- **Không thể tìm kiếm**: Cả metadata và tags đều không thể tìm kiếm trực tiếp trong S3
- **Giải pháp**: Xây dựng chỉ mục có thể tìm kiếm bên ngoài trong cơ sở dữ liệu như DynamoDB

---

*Tài liệu này dựa trên các phương pháp tốt nhất của AWS S3 và các mô hình kiến trúc phổ biến.*