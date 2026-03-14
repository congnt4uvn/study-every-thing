# Tích Hợp AWS EventBridge và Lambda

## Tổng Quan
Tài liệu này trình bày cách tích hợp giữa CloudWatch Events/EventBridge và các hàm AWS Lambda.

## Phương Thức Tích Hợp

### 1. Thực Thi Theo Lịch (Serverless CRON hoặc Rate)
- **Mục đích**: Thực thi các hàm Lambda theo lịch trình
- **Cách hoạt động**:
  - Tạo một EventBridge Rule với biểu thức rate
  - Ví dụ: Kích hoạt mỗi 1 giờ
  - Rule tự động gọi hàm Lambda để thực hiện tác vụ
  - Trường hợp sử dụng: Xử lý dữ liệu định kỳ, bảo trì theo lịch, báo cáo tự động

### 2. Tích Hợp Hướng Sự Kiện
- **Mục đích**: Phản ứng với các thay đổi trạng thái của dịch vụ AWS
- **Ví dụ - Tích Hợp CodePipeline**:
  - Tạo EventBridge Rule để phát hiện thay đổi trạng thái CodePipeline
  - Khi trạng thái pipeline thay đổi, EventBridge gọi hàm Lambda
  - Hàm Lambda có thể thực hiện các hành động tùy chỉnh dựa trên sự kiện
  - Trường hợp sử dụng: Thông báo, triển khai tự động, điều phối workflow

## Các Khái Niệm Chính

### EventBridge Rule
- Định nghĩa mẫu sự kiện cần giám sát
- Chỉ định target (hàm Lambda) để gọi
- Có thể dựa trên:
  - Lịch trình (biểu thức rate hoặc cron)
  - Mẫu sự kiện (sự kiện từ dịch vụ AWS)

### Hàm Lambda Làm Target
- Nhận dữ liệu sự kiện từ EventBridge
- Thực thi logic nghiệp vụ tùy chỉnh
- Có thể tích hợp với các dịch vụ AWS khác

## Lợi Ích
- **Serverless**: Không cần quản lý hạ tầng
- **Khả năng mở rộng**: Tự động xử lý khối lượng công việc thay đổi
- **Tiết kiệm chi phí**: Chỉ trả tiền cho thời gian thực thi
- **Linh hoạt**: Hỗ trợ cả mẫu theo lịch và hướng sự kiện

## Trường Hợp Sử Dụng Phổ Biến
1. Sao lưu dữ liệu theo lịch
2. Dọn dẹp tài nguyên tự động
3. Thông báo CI/CD pipeline
4. Xử lý sự kiện thời gian thực
5. Hệ thống giám sát và cảnh báo
