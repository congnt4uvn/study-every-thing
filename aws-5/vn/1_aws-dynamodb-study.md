# Tài liệu học AWS DynamoDB

## Tổng quan

Tài liệu này bao gồm các giải pháp điện toán phân tán và lưu trữ dữ liệu có khả năng mở rộng bằng các dịch vụ AWS, tập trung chủ yếu vào DynamoDB và AWS Lambda.

## AWS Lambda

AWS Lambda là dịch vụ điện toán serverless cho phép bạn:
- Chạy code mà không cần cung cấp hoặc quản lý server
- Xây dựng ứng dụng điện toán phân tán
- Tự động mở rộng quy mô dựa trên nhu cầu
- Chỉ trả tiền cho thời gian tính toán bạn sử dụng

## Thách thức lưu trữ dữ liệu

Khi xây dựng ứng dụng phân tán và có khả năng mở rộng, một câu hỏi quan trọng được đặt ra: **Chúng ta lưu trữ thông tin và dữ liệu ở đâu?**

Đối với kiến trúc serverless, chúng ta cần một giải pháp cơ sở dữ liệu:
- Tự động mở rộng quy mô
- Yêu cầu quản lý tối thiểu
- Tích hợp liền mạch với các dịch vụ AWS khác

## DynamoDB - Giải pháp cơ sở dữ liệu Serverless

**Amazon DynamoDB** là dịch vụ cơ sở dữ liệu NoSQL được quản lý hoàn toàn bởi AWS, cung cấp:

### Tính năng chính
- **Được quản lý hoàn toàn**: AWS xử lý tất cả việc quản lý hạ tầng
- **Tự động mở rộng**: Mở rộng quy mô để phù hợp với khối lượng công việc của bạn
- **Serverless**: Không cần cung cấp hoặc quản lý server
- **Tích hợp AWS**: Tích hợp tuyệt vời với AWS Lambda và các dịch vụ AWS khác
- **Hiệu suất cao**: Hiệu suất nhanh và nhất quán ở mọi quy mô

### Các chủ đề cốt lõi cần nắm vững

1. **Thiết kế bảng (Table Design)**
   - Thiết kế đúng cách các bảng DynamoDB để có hiệu suất tối ưu
   - Hiểu về partition keys và sort keys
   - Các phương pháp hay nhất cho mô hình hóa dữ liệu

2. **DynamoDB Streams**
   - Kích hoạt streams để ghi lại hoạt động của bảng
   - Xử lý các bản ghi stream với Lambda
   - Các mẫu xử lý dữ liệu thời gian thực

3. **Bảo mật (Security)**
   - Đảm bảo các bảng DynamoDB được bảo mật đầy đủ
   - Chính sách và vai trò IAM
   - Mã hóa khi lưu trữ và truyền tải
   - VPC endpoints và bảo mật mạng

## Mục tiêu học tập

Sau khi hoàn thành tài liệu này, bạn sẽ có thể:
- Thiết kế cấu trúc bảng DynamoDB hiệu quả
- Triển khai DynamoDB Streams cho xử lý thời gian thực
- Bảo mật các bảng DynamoDB theo các phương pháp hay nhất của AWS
- Tích hợp DynamoDB với AWS Lambda cho các ứng dụng serverless

## Bước tiếp theo

Hãy cùng tìm hiểu sâu vào từng chủ đề và xây dựng kỹ năng thực tế với AWS DynamoDB!
