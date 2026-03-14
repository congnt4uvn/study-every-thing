# AWS Lambda và Serverless Computing

## Tổng Quan

Tài liệu này đề cập đến AWS Lambda và kiến trúc serverless, đây là các chủ đề quan trọng cho kỳ thi AWS Developer.

## Serverless là gì?

Serverless không chỉ là một thuật ngữ thời thượng - đây là một xu hướng mới và mô hình mới trong điện toán đám mây. Nó cho phép các nhà phát triển xây dựng và chạy ứng dụng mà không cần quản lý máy chủ.

### Các Khái Niệm Chính

- **Không Cần Quản Lý Server**: Bạn không cần cung cấp hoặc quản lý máy chủ
- **Tự Động Mở Rộng**: Ứng dụng tự động mở rộng theo nhu cầu
- **Trả Theo Sử Dụng**: Bạn chỉ trả tiền cho thời gian tính toán bạn sử dụng
- **Hướng Sự Kiện**: Các hàm được kích hoạt bởi các sự kiện

## AWS Lambda

AWS Lambda là một trong những dịch vụ được sử dụng rộng rãi và phổ biến nhất trong AWS. Nó đã cách mạng hóa cách mọi người phát triển, triển khai và mở rộng ứng dụng.

### AWS Lambda là gì?

AWS Lambda là một dịch vụ tính toán serverless chạy mã của bạn để phản hồi các sự kiện và tự động quản lý các tài nguyên tính toán cơ bản.

### Các Tính Năng Chính

1. **Thực Thi Hướng Sự Kiện**: Các hàm Lambda thực thi để phản hồi các sự kiện từ các dịch vụ AWS
2. **Tự Động Mở Rộng**: Mở rộng từ vài yêu cầu mỗi ngày đến hàng nghìn yêu cầu mỗi giây
3. **Khả Năng Chịu Lỗi Tích Hợp**: Tính sẵn sàng cao được tích hợp trong dịch vụ
4. **Hỗ Trợ Nhiều Ngôn Ngữ**: Node.js, Python, Java, Go, Ruby, .NET Core, và các runtime tùy chỉnh

### Lambda Hoạt Động Như Thế Nào

1. Tải mã của bạn lên Lambda
2. Thiết lập mã của bạn để kích hoạt từ các sự kiện (API Gateway, S3, DynamoDB, v.v.)
3. Lambda chỉ chạy mã của bạn khi được kích hoạt
4. Bạn chỉ trả tiền cho thời gian tính toán đã sử dụng

### Các Trường Hợp Sử Dụng Lambda

- **Xử Lý File Thời Gian Thực**: Xử lý file ngay sau khi tải lên S3
- **Chuyển Đổi Dữ Liệu**: Các hoạt động ETL và xử lý dữ liệu
- **Ứng Dụng Web**: Xây dựng API serverless với API Gateway
- **Backend IoT**: Xử lý luồng dữ liệu từ thiết bị IoT
- **Tác Vụ Theo Lịch**: Chạy mã theo lịch trình sử dụng CloudWatch Events

### Các Thực Hành Tốt Nhất

1. **Giữ Hàm Nhỏ Gọn**: Nguyên tắc trách nhiệm đơn lẻ
2. **Giảm Thiểu Cold Start**: Giữ gói triển khai nhỏ, tái sử dụng kết nối
3. **Sử Dụng Biến Môi Trường**: Lưu cấu hình bên ngoài mã
4. **Giám Sát với CloudWatch**: Theo dõi các chỉ số và nhật ký
5. **Xử Lý Lỗi Một Cách Khéo Léo**: Triển khai xử lý lỗi và thử lại phù hợp

### Giá Lambda

- Gói Miễn Phí: 1 triệu yêu cầu mỗi tháng và 400,000 GB-giây thời gian tính toán
- Trả tiền cho: Số lượng yêu cầu và thời lượng thực thi

## Mẹo Chuẩn Bị Kỳ Thi

- Hiểu các trigger và nguồn sự kiện của Lambda
- Biết các giới hạn của Lambda (timeout, memory, kích thước gói triển khai)
- Thực hành tạo các hàm Lambda bằng các ngôn ngữ khác nhau
- Hiểu ngữ cảnh thực thi và vòng đời của Lambda
- Biết các mẫu tích hợp với các dịch vụ AWS khác

## Tóm Tắt

AWS Lambda là thiết yếu cho các ứng dụng đám mây hiện đại. Hiểu cách Lambda hoạt động ở cả kiến trúc mức cao và triển khai trong thực tế là rất quan trọng cho kỳ thi AWS Developer và phát triển đám mây thực tế.
