# AWS DynamoDB Indexes - Tài Liệu Học Tập

## Tổng Quan
Tài liệu này hướng dẫn cách tạo và sử dụng các indexes trong Amazon DynamoDB, bao gồm Local Secondary Indexes (LSI) và Global Secondary Indexes (GSI).

## Cơ Bản Về Cấu Trúc Bảng

### Primary Keys (Khóa Chính)
- **Partition Key (Khóa phân vùng)**: Thuộc tính chính dùng để phân phối dữ liệu (ví dụ: `user_id`)
- **Sort Key (Khóa sắp xếp)**: Thuộc tính tùy chọn cho phép sắp xếp và truy vấn theo khoảng (ví dụ: `game_timestamp`)

## Các Loại Index

### 1. Local Secondary Index (LSI) - Index Phụ Cục Bộ
- **Thời điểm tạo**: CHỈ có thể tạo khi tạo bảng
- **Partition Key**: PHẢI sử dụng cùng partition key với bảng gốc
- **Sort Key**: PHẢI chỉ định sort key KHÁC với bảng gốc
- **Trường hợp sử dụng**: Truy vấn cùng partition key với sort key khác

**Ví dụ:**
- Bảng gốc: Partition Key = `user_id`, Sort Key = `game_timestamp`
- LSI: Partition Key = `user_id`, Sort Key = `game_id`

### 2. Global Secondary Index (GSI) - Index Phụ Toàn Cục
- **Thời điểm tạo**: Có thể tạo khi tạo bảng HOẶC sau đó
- **Partition Key**: Có thể chỉ định partition key KHÁC
- **Sort Key**: Có thể tùy chọn chỉ định sort key KHÁC
- **Trường hợp sử dụng**: Truy vấn dữ liệu theo các mẫu truy cập khác nhau

## Chiếu Thuộc Tính (Attribute Projection)

Khi tạo index, bạn phải chọn thuộc tính nào để chiếu:

1. **All (Tất cả)**: Chiếu tất cả thuộc tính từ bảng gốc
2. **Keys Only (Chỉ khóa)**: Chỉ chiếu các thuộc tính khóa
3. **Include (Bao gồm)**: Chiếu các thuộc tính cụ thể mà bạn chỉ định

## Provisioned Capacity (Dung Lượng Cung Cấp)

Các index có thể có cài đặt dung lượng riêng:
- **RCU** (Read Capacity Units - Đơn vị dung lượng đọc)
- **WCU** (Write Capacity Units - Đơn vị dung lượng ghi)

## Tạo Bảng Với Indexes

### Quy Trình Từng Bước:
1. Điều hướng đến DynamoDB Tables
2. Tạo bảng mới (ví dụ: `demo_indexes`)
3. Chọn Partition key (`user_id`)
4. Chọn Sort key (`game_timestamp`)
5. Tùy chỉnh cài đặt cho Provisioned capacity
6. Định nghĩa các secondary indexes:
   - Thêm Local Secondary Index với sort key khác
   - (Tùy chọn) Thêm Global Secondary Index với partition/sort keys khác
7. Chọn chiến lược chiếu thuộc tính
8. Tạo bảng

## Truy Vấn Với Indexes

Khi truy vấn, bạn có thể chọn:
- **Truy vấn bảng**: Sử dụng các khóa chính của bảng
- **Truy vấn index**: Sử dụng các khóa của index cho các mẫu truy cập khác nhau

## Bảng So Sánh Các Tính Năng

| Tính Năng | Local Secondary Index | Global Secondary Index |
|-----------|----------------------|------------------------|
| Thời điểm tạo | Chỉ khi tạo bảng | Bất kỳ lúc nào |
| Partition Key | Giống bảng gốc | Có thể khác |
| Sort Key | Phải khác | Có thể khác |
| Dung lượng | Chia sẻ với bảng | Dung lượng riêng |

## Thực Hành Tốt Nhất

1. Lập kế hoạch cho các indexes cẩn thận trong quá trình thiết kế bảng
2. Sử dụng LSI khi cần thứ tự sắp xếp thay thế cho cùng một partition key
3. Sử dụng GSI khi cần truy vấn bằng các thuộc tính hoàn toàn khác
4. Chọn chiếu cẩn thận để cân bằng chi phí lưu trữ và hiệu suất truy vấn
5. Giám sát dung lượng index riêng biệt với dung lượng bảng

## Các Trường Hợp Sử Dụng Phổ Biến

- **Theo Dõi Hoạt Động Người Dùng**: Truy vấn theo user_id và sắp xếp theo các timestamps hoặc IDs khác nhau
- **Bảng Xếp Hạng Game**: Truy vấn theo game_id thay vì user_id
- **Ứng Dụng Đa Thuê Bao**: Truy vấn theo tenant_id với các mẫu sắp xếp khác nhau

## Thuật Ngữ Quan Trọng

- **Index**: Chỉ mục - cấu trúc dữ liệu giúp truy vấn nhanh hơn
- **Partition Key**: Khóa phân vùng - xác định cách dữ liệu được phân phối
- **Sort Key**: Khóa sắp xếp - cho phép sắp xếp dữ liệu trong một partition
- **Projection**: Chiếu - chọn thuộc tính nào được sao chép vào index
- **Capacity Units**: Đơn vị dung lượng - đo lường thông lượng đọc/ghi

---

*Mẹo học tập: Thực hành tạo bảng với cả hai loại indexes trong AWS Console để hiểu rõ sự khác biệt thông qua thực hành.*
