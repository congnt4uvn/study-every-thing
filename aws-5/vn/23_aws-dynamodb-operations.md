# Hướng Dẫn Học AWS DynamoDB Operations

## Các Thao Tác Dọn Dẹp Bảng (Table Cleanup)

Khi bạn cần dọn dẹp một bảng DynamoDB, có hai cách tiếp cận chính:

### Tùy Chọn 1: Quét và Xóa (Scan and Delete)
- **Quy trình**: Quét tất cả các mục trong bảng và xóa từng mục một
- **Nhược điểm**:
  - Quá trình rất chậm
  - Chi phí cao - tiêu tốn nhiều RCU (Read Capacity Units) cho việc quét
  - Chi phí cao - tiêu tốn nhiều WCU (Write Capacity Units) cho việc xóa
  - Không được khuyến nghị sử dụng trong môi trường production

### Tùy Chọn 2: Xóa và Tạo Lại (Recommended)
- **Quy trình**: Xóa toàn bộ bảng và tạo lại bảng mới
- **Ưu điểm**:
  - Thực thi nhanh chóng
  - Hiệu quả cao
  - Tiết kiệm chi phí
- **Lưu ý quan trọng**: Đảm bảo tạo lại bảng với các cài đặt chính xác giống như cấu hình ban đầu

## Sao Chép Bảng DynamoDB

Có ba phương pháp chính để sao chép một bảng DynamoDB:

### 1. Dịch Vụ AWS Backup
- Tạo bản sao lưu (backup) của bảng nguồn
- Khôi phục (restore) bản sao lưu để tạo bảng mới
- Có thể khôi phục trong cùng tài khoản hoặc sang tài khoản khác
- Sử dụng dịch vụ được quản lý sẵn

### 2. AWS Glue (Dịch Vụ ETL)
- AWS Glue tạo một script tự động
- Script đọc dữ liệu từ bảng nguồn
- Có thể ghi dữ liệu đến bất kỳ đích nào bạn chỉ định
- Phù hợp cho các tác vụ chuyển đổi và di chuyển dữ liệu

### 3. Giải Pháp Code Tùy Chỉnh
- Viết code ứng dụng của riêng bạn
- Sử dụng các API call của DynamoDB:
  - `Scan` - để đọc các mục từ bảng nguồn
  - `PutItem` - để ghi từng mục riêng lẻ
  - `BatchWriteItem` - để ghi nhiều mục một cách hiệu quả
- Phức tạp hơn so với việc sử dụng dịch vụ được quản lý của AWS
- Cung cấp tính linh hoạt và kiểm soát tối đa

## Những Điểm Chính Cần Nhớ

- Để dọn dẹp bảng, luôn ưu tiên **Xóa và Tạo Lại** thay vì quét và xóa
- Để sao chép bảng, sử dụng **AWS Backup** cho sự đơn giản hoặc **AWS Glue** cho nhu cầu chuyển đổi dữ liệu
- Giải pháp code tùy chỉnh phức tạp hơn nhưng cung cấp khả năng kiểm soát cao nhất
- Cân nhắc về mức tiêu thụ RCU/WCU khi lựa chọn phương pháp
