# Tài Liệu Học Tập AWS DynamoDB

## Tổng Quan
Tài liệu này bao gồm các API call quan trọng của DynamoDB mà bạn cần biết cho kỳ thi.

## Ghi Dữ Liệu vào DynamoDB

### 1. PutItem
- **Mục đích**: Tạo mới hoặc thay thế hoàn toàn một item
- **Điểm Chính**:
  - Tạo item mới với Primary Key được chỉ định
  - Nếu item có cùng Primary Key đã tồn tại, nó sẽ thay thế hoàn toàn
  - Tiêu tốn Write Capacity Units (WCU)
  - Sử dụng khi bạn muốn thay thế toàn bộ hoặc ghi một item mới

### 2. UpdateItem
- **Mục đích**: Chỉnh sửa các thuộc tính của item hiện có hoặc thêm item mới
- **Điểm Chính**:
  - Khác với PutItem - chỉ chỉnh sửa các thuộc tính cụ thể, không phải tất cả thuộc tính
  - Thêm item mới nếu nó chưa tồn tại
  - Hiệu quả hơn khi bạn chỉ cần sửa đổi một vài thuộc tính
  - Có thể sử dụng với Atomic Counters

### 3. Conditional Writes (Ghi Có Điều Kiện)
- **Mục đích**: Chấp nhận write/update/delete chỉ khi điều kiện được đáp ứng
- **Điểm Chính**:
  - Hỗ trợ truy cập đồng thời vào các item
  - Đảm bảo tính toàn vẹn dữ liệu trong môi trường nhiều người dùng

## Đọc Dữ Liệu từ DynamoDB

### 1. GetItem
- **Mục đích**: Đọc dữ liệu dựa trên Primary Key
- **Điểm Chính**:
  - Đọc dựa trên Primary Key (HASH hoặc HASH+Range)
  - **Chế Độ Đọc**:
    - **Eventually Consistent Read** (mặc định): Có thể không phản ánh lần ghi gần nhất
    - **Strongly Consistent Read**: Luôn trả về dữ liệu cập nhật nhất (cần nhiều RCU hơn và có thể có độ trễ cao hơn)
  - **Projection Expression**: Chỉ định để chỉ nhận một số thuộc tính nhất định từ DynamoDB

### 2. Query
- **Mục đích**: Trả về các item dựa trên điều kiện key
- **Điểm Chính**:
  - **Key Condition Expression**:
    - Partition Key: Phải sử dụng toán tử equal (ví dụ: "John123")
    - Sort Key (tùy chọn): Có thể sử dụng equal, less than, greater than, begins_with, between, v.v.
  - **FilterExpression**: Lọc bổ sung được áp dụng SAU khi thao tác query đã hoàn thành
  - Hiệu quả hơn Scan khi bạn biết Partition Key

## Tóm Tắt Các Khái Niệm Chính

| Thao Tác | Trường Hợp Sử Dụng | Yêu Cầu Primary Key |
|----------|-------------------|---------------------|
| PutItem | Ghi/thay thế toàn bộ item | Có |
| UpdateItem | Cập nhật một phần thuộc tính | Có |
| GetItem | Lấy một item đơn lẻ | Có |
| Query | Nhiều item có cùng Partition Key | Có (Partition Key) |

## Mẹo Cho Kỳ Thi
- Biết sự khác biệt giữa PutItem (thay thế toàn bộ) và UpdateItem (cập nhật một phần)
- Hiểu Eventually Consistent và Strongly Consistent reads
- Nhớ rằng Query yêu cầu điều kiện Partition Key
- FilterExpression được áp dụng SAU thao tác query
