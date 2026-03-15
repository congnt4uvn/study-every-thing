# Hướng Dẫn Học AWS DynamoDB

## Tổng Quan
DynamoDB là dịch vụ cơ sở dữ liệu NoSQL serverless do AWS cung cấp. Khác với cơ sở dữ liệu truyền thống, bạn tạo bảng trực tiếp mà không cần quản lý hạ tầng cơ sở dữ liệu.

## Các Khái Niệm Chính

### 1. **Tính Chất Serverless**
- DynamoDB là dịch vụ được quản lý hoàn toàn, serverless
- Không cần tạo cơ sở dữ liệu - cơ sở dữ liệu đã được tạo sẵn cho bạn
- Bạn chỉ cần tạo và quản lý các bảng

### 2. **Tạo Bảng (Table)**
Khi tạo một bảng DynamoDB, bạn cần chỉ định:
- **Tên Bảng (Table Name)**: Định danh duy nhất cho bảng của bạn (ví dụ: "Users")
- **Partition Key (Khóa Phân Vùng)**: Khóa bắt buộc để phân phối dữ liệu
  - Ví dụ: `user_ID`
  - Các kiểu dữ liệu: String (Chuỗi), Number (Số), hoặc Binary (Nhị phân)
- **Sort Key (Khóa Sắp Xếp)**: Khóa phụ tùy chọn để sắp xếp dữ liệu trong một phân vùng

### 3. **Các Lớp Bảng (Table Classes)**
DynamoDB cung cấp hai lớp bảng:
- **DynamoDB Standard**: 
  - Lớp bảng đa mục đích
  - Được khuyến nghị cho hầu hết các trường hợp sử dụng
  - Phù hợp cho các hoạt động đọc/ghi thường xuyên
  
- **DynamoDB Standard-IA (Infrequent Access - Truy Cập Không Thường Xuyên)**:
  - Dành cho dữ liệu được lưu trữ trong thời gian dài
  - Tối ưu hóa cho đọc và ghi không thường xuyên
  - Cung cấp tối ưu hóa chi phí cho dữ liệu hiếm khi được truy cập

### 4. **Chế Độ Dung Lượng (Capacity Modes)**
Hai chế độ có sẵn cho dung lượng đọc và ghi:

#### Chế Độ Dung Lượng Được Cấp Phát (Provisioned Capacity Mode)
- Nằm trong AWS Free Tier
- Bạn thiết lập các đơn vị dung lượng đọc và ghi cố định
- Có thể bật/tắt tự động mở rộng (auto-scaling)
- Free tier bao gồm số lượng đơn vị dung lượng được cấp phát giới hạn

#### Chế Độ Theo Nhu Cầu (On-Demand Capacity Mode)
- Giá theo yêu cầu
- Tự động mở rộng dựa trên khối lượng công việc
- Không cần lập kế hoạch dung lượng

### 5. **Cài Đặt Dung Lượng**
- **Read Capacity Units (Đơn vị Dung Lượng Đọc)**: Kiểm soát thông lượng đọc
- **Write Capacity Units (Đơn vị Dung Lượng Ghi)**: Kiểm soát thông lượng ghi
- **Auto Scaling (Tự Động Mở Rộng)**: Có thể được bật hoặc tắt
- **Free Tier**: Bao gồm một số lượng đơn vị dung lượng nhất định

### 6. **Công Cụ Tính Dung Lượng (Capacity Calculator)**
AWS cung cấp công cụ tính toán dung lượng để giúp bạn ước tính dung lượng cần thiết dựa trên mô hình khối lượng công việc của bạn.

## Thực Hành Tốt Nhất
1. Chọn lớp bảng phù hợp dựa trên mô hình truy cập
2. Bắt đầu với dung lượng được cấp phát nếu bạn nằm trong giới hạn free tier
3. Sử dụng Standard-IA cho dữ liệu lưu trữ hoặc truy cập không thường xuyên
4. Lập kế hoạch cẩn thận cho partition key và sort key để phân phối dữ liệu tối ưu

## Ghi Chú
- DynamoDB được thiết kế cho các ứng dụng hiệu suất cao, có khả năng mở rộng
- Hiểu các chế độ dung lượng rất quan trọng để tối ưu hóa chi phí
- Thiết kế khóa phù hợp là thiết yếu cho hiệu suất truy vấn
