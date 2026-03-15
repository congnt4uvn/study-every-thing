# Tài Liệu Học Tập AWS DynamoDB Indexes

## Tổng Quan
Amazon DynamoDB cung cấp hai loại chỉ mục để tối ưu hiệu suất truy vấn: Local Secondary Indexes (LSI) và Global Secondary Indexes (GSI).

## Local Secondary Index (LSI) - Chỉ Mục Phụ Cục Bộ

### Định Nghĩa
Local Secondary Index cung cấp một khóa sắp xếp thay thế cho bảng của bạn trong khi vẫn giữ nguyên khóa phân vùng từ bảng gốc.

### Đặc Điểm Chính
- **Cùng khóa phân vùng** với bảng gốc
- **Khóa sắp xếp thay thế** cho các mẫu truy vấn khác nhau
- Khóa sắp xếp bao gồm một thuộc tính vô hướng (chuỗi, số, hoặc nhị phân)
- Tối đa **5 LSI trên mỗi bảng**

### Ràng Buộc Quan Trọng
- **Phải được định nghĩa khi tạo bảng**
- Không thể thêm sau khi bảng đã được tạo
- Yêu cầu lập kế hoạch thiết kế bảng cẩn thận ngay từ đầu

### Chiếu Thuộc Tính
- Có thể bao gồm một số hoặc tất cả thuộc tính từ bảng chính
- Chọn các thuộc tính cụ thể dựa trên yêu cầu truy vấn
- Tối ưu hóa hiệu suất truy vấn và chi phí lưu trữ

### Ví Dụ Trường Hợp Sử Dụng

**Cấu Trúc Bảng Gốc:**
- Khóa phân vùng: `user_id`
- Khóa sắp xếp: `game_id`
- Các thuộc tính: `game_timestamp`, `score`, `result`

**Hạn Chế Truy Vấn Không Có LSI:**
- Có thể truy vấn theo `user_id` và `game_id`
- Không thể truy vấn hiệu quả theo `user_id` và `game_timestamp`
- Sẽ yêu cầu thao tác quét với lọc phía máy khách

**Giải Pháp Với LSI:**
- Tạo LSI trên thuộc tính `game_timestamp`
- Cho phép truy vấn hiệu quả như: "Lấy tất cả các trò chơi được chơi bởi người dùng này từ năm 2020 đến 2021"
- Cùng khóa phân vùng (`user_id`), khóa sắp xếp khác (`game_timestamp`)

## Global Secondary Index (GSI) - Chỉ Mục Phụ Toàn Cục

### Định Nghĩa
Global Secondary Index cung cấp một khóa chính thay thế, cho phép khóa phân vùng và khóa sắp xếp hoàn toàn khác so với bảng gốc.

### Đặc Điểm Chính
- **Khóa phân vùng khác** (hash key) so với bảng gốc
- Tùy chọn **khóa sắp xếp khác** nữa
- Tăng tốc truy vấn trên các thuộc tính không phải khóa
- Có thể sử dụng các thuộc tính vô hướng (chuỗi, số, nhị phân)

### Tính Linh Hoạt
- Có thể tạo bất kỳ lúc nào (không chỉ khi tạo bảng)
- Cho phép truy vấn trên các thuộc tính không phải là một phần của khóa chính
- Linh hoạt hơn LSI nhưng có đặc điểm hiệu suất khác

### Chiếu Thuộc Tính
- Chọn thuộc tính nào để đưa vào chỉ mục
- Cân bằng giữa hiệu suất truy vấn và chi phí lưu trữ

## So Sánh: LSI vs GSI

| Tính Năng | LSI | GSI |
|-----------|-----|-----|
| Khóa Phân Vùng | Giống bảng gốc | Có thể khác |
| Khóa Sắp Xếp | Khác với bảng gốc | Có thể khác |
| Thời Điểm Tạo | Phải khi tạo bảng | Có thể thêm bất kỳ lúc nào |
| Giới Hạn Trên Bảng | 5 | 20 (mặc định) |
| Trường Hợp Sử Dụng | Sắp xếp thay thế trên cùng phân vùng | Truy vấn các mẫu truy cập khác nhau |

## Thực Hành Tốt Nhất

1. **Lập kế hoạch LSI cẩn thận** - Chúng không thể sửa đổi sau khi tạo bảng
2. **Sử dụng GSI cho tính linh hoạt** - Khi bạn cần truy vấn trên các thuộc tính không phải khóa
3. **Chỉ chiếu các thuộc tính cần thiết** - Giảm thiểu chi phí lưu trữ
4. **Xem xét các mẫu truy vấn** - Thiết kế chỉ mục dựa trên các mẫu truy cập thực tế
5. **Giám sát hiệu suất** - Theo dõi việc sử dụng chỉ mục và điều chỉnh khi cần

## Tóm Tắt

Các chỉ mục DynamoDB là công cụ thiết yếu để tối ưu hóa hiệu suất truy vấn:
- **LSI**: Khóa sắp xếp thay thế với cùng khóa phân vùng, phải được định nghĩa khi tạo
- **GSI**: Khóa chính thay thế, có thể thêm bất kỳ lúc nào, cho phép các mẫu truy vấn linh hoạt

Chọn loại chỉ mục phù hợp dựa trên các mẫu truy cập dữ liệu và yêu cầu truy vấn của bạn.
