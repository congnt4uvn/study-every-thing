# Tài Liệu Học AWS DynamoDB

## Tổng Quan
Tài liệu này bao gồm các thao tác API dữ liệu DynamoDB quan trọng và các phương pháp hay nhất để tương tác với bảng DynamoDB.

## Mục Lục
1. [Thao Tác Scan](#thao-tác-scan)
2. [Put Item](#put-item)
3. [Update Item](#update-item)
4. [Get Item](#get-item)
5. [Thao Tác Batch](#thao-tác-batch)
6. [Query vs Scan](#query-vs-scan)

---

## Thao Tác Scan

### Mô Tả
Thao tác **Scan** đọc mọi item trong bảng và trả về tất cả thuộc tính dữ liệu theo mặc định.

### Cách Sử Dụng
1. Chọn bảng của bạn
2. Chọn tùy chọn 'Scan'
3. Nhấp 'Run'

### Điểm Chính
- Quét **toàn bộ bảng**
- Trả về nhiều item
- Có thể không hiệu quả cho bảng lớn
- Bộ lọc được áp dụng **phía client** (trong trình duyệt web của bạn)

### Trường Hợp Sử Dụng
- Bảng nhỏ
- Khi bạn cần tất cả dữ liệu
- Các tác vụ quản trị

---

## Put Item

### Mô Tả
Thao tác **PutItem** tạo một item mới hoặc thay thế item hiện có bằng item mới.

### Ví Dụ
```
User ID: Alice456
Timestamp: T050600
Content: Alice blog
```

### Điểm Chính
- Gửi một item mới vào DynamoDB
- Yêu cầu các thuộc tính khóa chính (user_id, post_timestamp)
- Nếu item tồn tại, nó sẽ được thay thế
- Tạo item mới nếu nó chưa tồn tại

### Khi Nào Sử Dụng
- Tạo bản ghi mới
- Thay thế hoàn toàn các item hiện có

---

## Update Item

### Mô Tả
Thao tác **UpdateItem** sửa đổi các thuộc tính hiện có của một item hoặc thêm các thuộc tính mới.

### Cách Thực Hiện
1. Chọn item
2. Chọn 'Actions' → 'Edit'
3. Sửa đổi các thuộc tính cụ thể
4. Nhấp 'Save changes'

### Ví Dụ
```
Ban đầu: Alice blog
Sau khi cập nhật: Alice blog edited
```

### Điểm Chính
- Chỉ cập nhật các thuộc tính được chỉ định
- Hiệu quả hơn PutItem cho các cập nhật từng phần
- Giữ nguyên các thuộc tính khác
- Có thể thêm thuộc tính mới vào các item hiện có

---

## Get Item

### Mô Tả
Thao tác **GetItem** trả về một item duy nhất từ bảng bằng cách truy cập khóa chính của nó.

### Cách Hoạt Động
- Nhấp vào một hàng cụ thể trong bảng
- 'Item editor' hiển thị nội dung
- Phía sau, một lệnh gọi API get_item được thực thi

### Điểm Chính
- Truy xuất nội dung của một item cụ thể
- Nhanh và hiệu quả
- Yêu cầu biết khóa chính
- Trả về tất cả thuộc tính của item

### Hiệu Suất
- Cách hiệu quả nhất để truy xuất một item duy nhất
- Tra cứu khóa trực tiếp
- Tùy chọn đọc nhất quán hoặc đọc cuối cùng nhất quán

---

## Thao Tác Batch

### Batch Write
- Thực hiện nhiều thao tác PutItem hoặc DeleteItem trong một yêu cầu duy nhất
- Hiệu quả hơn các thao tác riêng lẻ

### Batch Delete
1. Chọn các item để xóa
2. Chọn 'Actions' → 'Delete Items'
3. Thực thi batch write với các yêu cầu xóa

### Điểm Chính
- Có thể xử lý tối đa 25 item mỗi yêu cầu
- Giảm số lượng lệnh gọi API
- Tiết kiệm chi phí hơn

---

## Xóa Tất Cả Dữ Liệu

### Tùy Chọn 1: Scan và Batch Delete
- Quét toàn bộ bảng
- Sử dụng batch delete trên kết quả
- **Không hiệu quả** cho bảng lớn

### Tùy Chọn 2: Xóa Bảng (Được Khuyến Nghị)
- Đơn giản là xóa và tạo lại bảng
- Nhanh hơn nhiều để xóa tất cả dữ liệu
- Tốt nhất cho việc đặt lại bảng hoàn toàn

---

## Query vs Scan

### Scan
- **Đọc toàn bộ bảng**
- Trả về tất cả item
- Bộ lọc áp dụng phía client
- Kém hiệu quả cho bảng lớn
- Chi phí cao hơn

### Query
- Thao tác **hiệu quả hơn**
- Sử dụng partition key (và tùy chọn sort key)
- Bộ lọc áp dụng phía server
- Chi phí thấp hơn
- Hiệu suất nhanh hơn

### Phương Pháp Tốt Nhất
- Sử dụng **Query** khi bạn biết partition key
- Chỉ sử dụng **Scan** khi cần thiết (bảng nhỏ hoặc cần tất cả dữ liệu)

---

## Tóm Tắt

| Thao Tác | Trường Hợp Sử Dụng | Hiệu Quả |
|----------|-------------------|----------|
| Scan | Lấy tất cả item | Thấp |
| Query | Lấy item theo khóa | Cao |
| GetItem | Lấy item đơn lẻ | Rất Cao |
| PutItem | Tạo/Thay thế item | Cao |
| UpdateItem | Sửa đổi thuộc tính | Cao |
| Batch Operations | Nhiều thao tác | Cao |

---

## Các Phương Pháp Hay Nhất

1. **Ưu tiên Query hơn Scan** bất cứ khi nào có thể
2. **Sử dụng thao tác batch** cho nhiều item
3. **Update Item** thay vì Put Item cho cập nhật từng phần
4. **Xóa bảng** thay vì quét và xóa tất cả item
5. **Thiết kế partition key** để cho phép truy vấn hiệu quả
6. Xem xét **read/write capacity** khi thực hiện các thao tác

---

## Mẹo Học Tập

- Thực hành từng thao tác trong AWS Console
- Hiểu sự khác biệt giữa Query và Scan
- Biết khi nào sử dụng thao tác batch
- Nhớ rằng bộ lọc trong Scan là phía client
- Hiểu yêu cầu khóa chính cho từng thao tác

---

## Thuật Ngữ Quan Trọng

- **Partition Key**: Khóa phân vùng - khóa chính được sử dụng để phân phối dữ liệu
- **Sort Key**: Khóa sắp xếp - khóa phụ để sắp xếp dữ liệu trong cùng partition
- **Item**: Một bản ghi trong bảng DynamoDB
- **Attribute**: Thuộc tính - một trường dữ liệu trong item
- **Scan**: Quét - đọc toàn bộ bảng
- **Query**: Truy vấn - tìm kiếm dựa trên khóa
- **Batch Operation**: Thao tác hàng loạt - xử lý nhiều item cùng lúc
