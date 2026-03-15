# AWS DynamoDB Transactions (Giao dịch)

## Tổng quan

Giao dịch DynamoDB cung cấp **thao tác tất cả hoặc không** trên nhiều mục trong một hoặc nhiều bảng. Tất cả các thao tác đều thành công hoặc không có thao tác nào thành công.

## Tính năng chính

### Thuộc tính ACID
Giao dịch cung cấp cho DynamoDB các tính năng ACID sau:
- **Atomicity (Tính nguyên tử)** - Tất cả thao tác hoàn thành hoặc không có thao tác nào hoàn thành
- **Consistency (Tính nhất quán)** - Dữ liệu luôn ở trạng thái nhất quán
- **Isolation (Tính cô lập)** - Các giao dịch được cô lập với nhau
- **Durability (Tính bền vững)** - Các giao dịch đã commit được lưu trữ lâu dài

## Chế độ giao dịch

### Chế độ đọc (Read Modes)
DynamoDB hỗ trợ ba mức độ nhất quán khi đọc:

1. **Eventual Consistency (Nhất quán cuối cùng)** - Có thể không phản ánh ghi gần nhất
2. **Strong Consistency (Nhất quán mạnh)** - Luôn phản ánh ghi gần nhất
3. **Transactional Consistency (Nhất quán giao dịch)** - Cung cấp chế độ xem nhất quán trên nhiều bảng đồng thời

### Chế độ ghi (Write Modes)

1. **Standard (Tiêu chuẩn)** - Nhiều thao tác ghi trên các bảng, một số có thể thất bại độc lập
2. **Transactional (Giao dịch)** - Tất cả thao tác ghi thành công trên tất cả bảng, hoặc không có thao tác nào thành công

## Chi phí

⚠️ **Quan trọng**: Giao dịch tiêu thụ **gấp đôi đơn vị dung lượng** (cả đọc và ghi) vì DynamoDB thực hiện hai thao tác ở background:
1. Chuẩn bị giao dịch (Prepare)
2. Commit giao dịch (Commit)

## Các API

### TransactGetItems
- Thực hiện một hoặc nhiều thao tác `GetItem` như một phần của giao dịch
- Được sử dụng để đọc nhất quán trên nhiều mục/bảng

### TransactWriteItems
- Thực hiện một hoặc nhiều thao tác sau như một phần của giao dịch:
  - `PutItem` - Thêm mục
  - `UpdateItem` - Cập nhật mục
  - `DeleteItem` - Xóa mục

## Trường hợp sử dụng

Giao dịch DynamoDB lý tưởng cho các tình huống yêu cầu thuộc tính ACID:

- 💰 **Giao dịch tài chính** - Đảm bảo cập nhật số dư tài khoản là nguyên tử
- 🛒 **Quản lý đơn hàng** - Cập nhật hàng tồn kho và đơn hàng cùng lúc
- 🎮 **Game nhiều người chơi** - Điều phối thay đổi trạng thái game
- 📊 **Bất kỳ tình huống nào yêu cầu tính nhất quán dữ liệu** trên nhiều thao tác

## Thực hành tốt nhất

- Chỉ sử dụng giao dịch khi cần thuộc tính ACID
- Cân nhắc yếu tố chi phí gấp đôi khi thiết kế ứng dụng
- Nhóm các thao tác liên quan lại để giảm thiểu số lượng giao dịch
- Giám sát mức tiêu thụ dung lượng chặt chẽ khi sử dụng giao dịch

---

*Ghi chú học tập: Giao dịch DynamoDB rất mạnh mẽ nhưng đi kèm với chi phí tăng cao. Sử dụng chúng một cách thận trọng cho các thao tác thực sự yêu cầu tính nhất quán nguyên tử.*
