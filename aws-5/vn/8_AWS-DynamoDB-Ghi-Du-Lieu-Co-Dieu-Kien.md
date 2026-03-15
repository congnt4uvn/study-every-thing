# AWS DynamoDB - Ghi Dữ Liệu Có Điều Kiện (Conditional Writes)

## Tổng Quan
Ghi dữ liệu có điều kiện trong DynamoDB cho phép bạn chỉ định các điều kiện xác định mục nào nên được sửa đổi trong quá trình thực hiện các thao tác ghi. Điều này đảm bảo tính toàn vẹn dữ liệu và ngăn chặn các thay đổi không mong muốn.

## Các Thao Tác Ghi Hỗ Trợ Điều Kiện
- **PutItem** - Chèn hoặc thay thế một mục
- **UpdateItem** - Sửa đổi một mục hiện có
- **DeleteItem** - Xóa một mục
- **BatchWriteItem** - Thực hiện nhiều thao tác ghi

## Các Hàm Biểu Thức Điều Kiện

### Kiểm Tra Sự Tồn Tại
- `attribute_exists` - Kiểm tra xem thuộc tính có tồn tại không
- `attribute_not_exists` - Kiểm tra xem thuộc tính không tồn tại
- `attribute_type` - Xác minh kiểu dữ liệu của thuộc tính

### Thao Tác Chuỗi
- `contains` - Kiểm tra xem chuỗi có chứa chuỗi con không
- `begins_with` - Kiểm tra xem chuỗi bắt đầu bằng tiền tố cụ thể không

### So Sánh Giá Trị
- `IN` - Kiểm tra xem giá trị có trong danh sách giá trị không
  - Ví dụ: Kiểm tra xem danh mục sản phẩm có trong nhiều danh mục không
- `BETWEEN` - Kiểm tra xem giá trị có nằm trong khoảng không
  - Ví dụ: `Price BETWEEN :low AND :high`
- Toán tử so sánh: `>`, `<`, `>=`, `<=`, `=`

### Các Hàm Khác
- `size` - Lấy độ dài/kích thước của thuộc tính (hữu ích cho chuỗi, danh sách, v.v.)

## So Sánh Filter Expressions vs Condition Expressions

| Khía Cạnh | Filter Expressions | Condition Expressions |
|-----------|-------------------|----------------------|
| **Mục đích** | Lọc kết quả của truy vấn đọc | Kiểm soát thao tác ghi nào thành công |
| **Thao tác** | Query, Scan | PutItem, UpdateItem, DeleteItem, BatchWriteItem |
| **Khi áp dụng** | Sau khi đọc dữ liệu | Trước khi ghi dữ liệu |
| **Hiệu ứng** | Giảm kết quả trả về | Ngăn ghi nếu điều kiện thất bại |

## Ví Dụ: UpdateItem với Condition Expression

### Lệnh
```bash
aws dynamodb update-item \
  --table-name product_catalog \
  --key '{"id": {"N": "456"}}' \
  --update-expression "SET price = price - :discount" \
  --condition-expression "price > :limit" \
  --expression-attribute-values file://values.json
```

### File Giá Trị (values.json)
```json
{
  ":discount": {"N": "150"},
  ":limit": {"N": "500"}
}
```

### Hành Vi
1. **Trạng Thái Ban Đầu**: Mục có ID 456 có giá = 650
2. **Cập Nhật Lần Đầu**: 
   - Điều kiện: 650 > 500 ✓ (đạt)
   - Giá mới: 650 - 150 = 500
   - **Kết quả**: Thành công, giá được cập nhật thành 500

3. **Cập Nhật Lần Hai** (cùng lệnh):
   - Điều kiện: 500 > 500 ✗ (thất bại)
   - **Kết quả**: Cập nhật bị từ chối, giá vẫn là 500

## Những Điểm Chính
- Biểu thức điều kiện ngăn chặn ghi khi điều kiện không được đáp ứng
- Chúng được đánh giá **trước khi** thao tác ghi xảy ra
- Điều kiện thất bại sẽ ném ra ngoại lệ `ConditionalCheckFailedException`
- Sử dụng biểu thức điều kiện để triển khai khóa lạc quan (optimistic locking) và quy tắc nghiệp vụ
- Luôn kiểm tra biểu thức điều kiện của bạn để đảm bảo chúng hoạt động như mong đợi

## Thực Hành Tốt Nhất
1. Sử dụng `attribute_not_exists` để ngăn ghi đè trong PutItem
2. Kết hợp nhiều điều kiện bằng toán tử `AND`, `OR`, `NOT`
3. Sử dụng tên thuộc tính biểu thức cho các từ khóa dành riêng
4. Kiểm tra kỹ lưỡng các điều kiện trước khi triển khai lên production
5. Xử lý ngoại lệ `ConditionalCheckFailedException` một cách phù hợp trong mã ứng dụng của bạn
