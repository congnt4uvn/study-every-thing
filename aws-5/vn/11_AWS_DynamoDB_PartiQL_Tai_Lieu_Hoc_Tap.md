# AWS DynamoDB - Tài Liệu Học Tập PartiQL

## Tổng Quan

PartiQL là ngôn ngữ truy vấn tương thích với SQL, cho phép bạn tương tác với các bảng DynamoDB bằng cú pháp giống SQL quen thuộc. Điều này giúp DynamoDB trở nên dễ tiếp cận hơn với các lập trình viên đã quen thuộc với SQL.

## Các Khái Niệm Chính

### PartiQL là gì?

- **Cú pháp giống SQL** cho các thao tác DynamoDB
- Được thiết kế cho các lập trình viên quen thuộc với SQL
- Hỗ trợ các thao tác CRUD chuẩn
- Tương thích với cấu trúc NoSQL của DynamoDB

### Các Thao Tác Được Hỗ Trợ

PartiQL hỗ trợ các thao tác sau trên bảng DynamoDB:

1. **INSERT** - Thêm item mới vào bảng
2. **UPDATE** - Sửa đổi các item hiện có
3. **SELECT** - Truy vấn và lấy các item
4. **DELETE** - Xóa các item khỏi bảng

### Thao Tác Hàng Loạt (Batch Operations)

PartiQL cũng hỗ trợ thao tác hàng loạt, cho phép bạn thực hiện nhiều thao tác một cách hiệu quả trong một yêu cầu duy nhất.

## Sử Dụng PartiQL trong AWS Console

### Truy Cập PartiQL Editor

1. Điều hướng đến DynamoDB trong AWS Console
2. Chọn bảng của bạn từ thanh bên trái
3. Mở **PartiQL editor**

### Các Ví Dụ Thao Tác

#### Tạo Dữ Liệu Mẫu

**Bảng Users:**
```json
{
  "user_id": "123",
  "name": "Stephan"
}
```

**Bảng Users Post:**
```json
{
  "user_id": "123",
  "post_id": "456"
}
```

**Bảng Demo Indexes:**
```json
{
  "user_id": "123",
  "game_timestamp": "2022",
  "game_id": "456"
}
```

#### Thao Tác SELECT

**Quét toàn bộ bảng:**
```sql
SELECT * FROM users
```

**Truy vấn với điều kiện:**
```sql
SELECT * FROM demo_indexes 
WHERE user_id = '123' 
AND game_timestamp = 'Sort key value'
```

Lưu ý: Điều kiện sort key là tùy chọn trong truy vấn.

### Làm Việc Với Kết Quả

- Xem kết quả ở **định dạng JSON** để tích hợp vào code
- **Tải xuống kết quả** dưới dạng CSV để phân tích dữ liệu
- Kết quả item được hiển thị cùng với các thuộc tính của chúng

## Thực Hành Tốt Nhất

1. **Sử dụng Query thay vì Scan** khi có thể để có hiệu suất tốt hơn
2. **Chỉ định điều kiện** để giới hạn dữ liệu được trả về
3. **Xác thực câu lệnh SQL** trước khi thực thi
4. **Sử dụng thao tác hàng loạt** cho nhiều item để cải thiện hiệu quả
5. **Hiểu về partition keys và sort keys** để truy vấn hiệu quả

## Các Trường Hợp Sử Dụng Phổ Biến

- Di chuyển dữ liệu từ cơ sở dữ liệu SQL
- Khám phá và gỡ lỗi dữ liệu nhanh chóng
- Truy vấn tức thời cho phân tích
- Phát triển và kiểm thử

## Lưu Ý Quan Trọng

- Các câu lệnh PartiQL phải được định dạng đúng (cú pháp đúng)
- Nhớ rằng DynamoDB vẫn là NoSQL ở bên dưới
- Partition keys là bắt buộc cho các thao tác Query
- Sort keys là tùy chọn nhưng cải thiện độ chính xác của truy vấn

## Tài Nguyên Bổ Sung

- Tài liệu AWS DynamoDB
- Đặc tả ngôn ngữ PartiQL
- Hướng dẫn Thực hành Tốt nhất DynamoDB
