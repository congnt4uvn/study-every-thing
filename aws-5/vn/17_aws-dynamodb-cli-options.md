# Tùy chọn CLI AWS DynamoDB

## Tổng quan
Tài liệu này bao gồm các tùy chọn CLI quan trọng cho DynamoDB có thể xuất hiện trong kỳ thi AWS.

## Các tùy chọn CLI chính

### 1. projection-expression
- **Mục đích**: Chỉ định một hoặc nhiều thuộc tính cần truy xuất
- **Trường hợp sử dụng**: Khi bạn không muốn truy xuất tất cả các cột/thuộc tính
- **Lợi ích**: Chỉ truy xuất một tập hợp con dữ liệu để giảm lượng dữ liệu truyền tải và chỉ lấy những gì cần thiết

### 2. filter-expression
- **Mục đích**: Lọc các mục được trả về từ truy vấn
- **Trường hợp sử dụng**: Áp dụng các điều kiện để lọc kết quả
- **Lợi ích**: Chỉ nhận được các mục đáp ứng tiêu chí cụ thể

## Tùy chọn phân trang

### page-size
- **Mục đích**: Kiểm soát kích thước của mỗi lời gọi API phụ đến AWS
- **Cách hoạt động**: 
  - Vẫn truy xuất toàn bộ tập dữ liệu
  - Mỗi lời gọi API đến AWS nhỏ hơn
  - Ngăn chặn timeout API
- **Ví dụ**:
  - Bảng có 10,000 mục
  - Không có page-size: 1 lời gọi API truy xuất toàn bộ 10,000 mục (có thể timeout)
  - Với page-size=100: 100 lời gọi API, mỗi lời gọi 100 mục (tránh timeout)
- **Lợi ích**: Tối ưu hóa để tránh timeout trong khi vẫn lấy được tất cả dữ liệu

### max-items
- **Mục đích**: Giới hạn số lượng mục được trả về trong một kết quả CLI duy nhất
- **Cách hoạt động**: Hoạt động kết hợp với NextToken/starting-token
- **Trường hợp sử dụng**: Phân trang qua các kết quả
- **Ví dụ**:
  - Đặt max-items=25 để nhận 25 mục
  - Sử dụng NextToken để truy xuất 25 mục tiếp theo
  - Tiếp tục phân trang khi cần thiết

### NextToken / starting-token
- **Mục đích**: Truy xuất tập kết quả phân trang tiếp theo
- **Cách hoạt động**: Được sử dụng sau khi nhận kết quả với max-items
- **Trường hợp sử dụng**: Lấy các trang dữ liệu tiếp theo

## Môi trường thực hành
- Truy cập bảng UserPosts để xem các mục
- Sử dụng AWS CLI (terminal đã cấu hình) hoặc AWS CloudShell để thực hành trực tiếp

## Điểm chính cần nhớ
- **projection-expression**: Chọn các thuộc tính cụ thể
- **filter-expression**: Lọc kết quả với các điều kiện
- **page-size**: Tối ưu hóa lời gọi API để tránh timeout (truy xuất tất cả dữ liệu)
- **max-items + NextToken**: Giới hạn kết quả và phân trang qua chúng
