# AWS API Gateway - Triển Khai Canary (Canary Deployments)

## Tổng Quan
Triển khai canary trên API Gateway cung cấp một cách an toàn để kiểm tra các thay đổi bằng cách định tuyến một phần nhỏ lưu lượng truy cập đến phiên bản mới trước khi triển khai hoàn toàn ra môi trường production.

## Các Khái Niệm Chính

### Triển Khai Canary Là Gì?
- Một chiến lược triển khai cho phép bạn kiểm tra một lượng nhỏ lưu lượng truy cập trên các thay đổi được thực hiện trên API Gateway
- Thường được thực hiện trong môi trường production
- Cho phép triển khai dần dần các phiên bản mới với rủi ro tối thiểu

### Cách Hoạt Động
1. **Trạng Thái Hiện Tại**: Stage production trỏ đến phiên bản 1
2. **Thiết Lập Canary**: Tạo prod stage canary cho phiên bản 2
3. **Phân Chia Lưu Lượng**: Cấu hình phân phối lưu lượng (ví dụ: 95% đến prod hiện tại, 5% đến canary)
4. **Giai Đoạn Kiểm Tra**: Giám sát metrics, logs và debug phiên bản canary
5. **Triển Khai Hoàn Toàn**: Khi đã tin tưởng, chuyển 100% lưu lượng sang canary stage

## Lợi Ích

### Giảm Thiểu Rủi Ro
- Kiểm tra các thay đổi với lưu lượng production thực tế
- Phạm vi tiếp xúc hạn chế giảm tác động của các vấn đề tiềm ẩn
- Dễ dàng rollback nếu phát hiện sự cố

### Giám Sát & Phân Tích
- Metrics riêng biệt cho canary và production stages
- Log streams độc lập để debug tốt hơn
- Cho phép so sánh trực tiếp giữa các phiên bản

### Tính Linh Hoạt
- Kiểm soát phần trăm chính xác lưu lượng định tuyến đến canary
- Ghi đè các stage variables cụ thể cho canary stage
- Tăng dần lưu lượng khi có sự tự tin

## Chi Tiết Kỹ Thuật

### Phân Phối Lưu Lượng
- Phần trăm phân chia có thể cấu hình (ví dụ: 95/5, 90/10, 80/20)
- Định tuyến tự động bởi API Gateway
- Không cần thay đổi phía client

### Stage Variables
- Có thể ghi đè bất kỳ stage variable nào cho canary stage
- Hữu ích để trỏ đến các tài nguyên backend khác nhau
- Cho phép kiểm tra các thay đổi backend (ví dụ: các phiên bản Lambda function khác nhau)

### So Sánh Với Blue/Green Deployment
- Triển khai canary tương đương với việc thực hiện blue/green deployment với Lambda và API Gateway
- Cả hai chiến lược đều giảm thiểu downtime và rủi ro
- Canary cung cấp quyền kiểm soát chi tiết hơn về phân phối lưu lượng

## Các Trường Hợp Sử Dụng

1. **Kiểm Tra Tính Năng Mới**: Xác thực các API endpoints hoặc chức năng mới
2. **Cập Nhật Backend**: Kiểm tra các phiên bản mới của Lambda functions hoặc các dịch vụ backend khác
3. **Kiểm Tra Hiệu Năng**: Đánh giá cải tiến hiệu năng dưới tải thực tế
4. **Thay Đổi Breaking**: Xác minh một cách an toàn khả năng tương thích ngược

## Thực Hành Tốt Nhất

- Bắt đầu với phần trăm nhỏ (5-10%) cho kiểm tra ban đầu
- Giám sát metrics chặt chẽ trong giai đoạn canary
- Thiết lập cảnh báo phù hợp cho canary stage
- Chuẩn bị sẵn kế hoạch rollback
- Tăng dần lưu lượng đến canary nếu metrics ổn định
- Giữ giai đoạn canary đủ ngắn để duy trì tốc độ phát triển

## Các Bước Triển Khai

1. Triển khai các thay đổi của bạn đến phiên bản mới
2. Kích hoạt cài đặt canary trên API Gateway stage
3. Cấu hình phần trăm phân chia lưu lượng
4. (Tùy chọn) Ghi đè stage variables cho canary
5. Giám sát metrics và logs
6. Điều chỉnh phần trăm lưu lượng hoặc promote canary lên triển khai đầy đủ
7. Tắt canary sau khi hoàn thành triển khai đầy đủ

## Các Dịch Vụ AWS Liên Quan
- **AWS Lambda**: Backend phổ biến cho API Gateway
- **Amazon CloudWatch**: Giám sát và logging
- **AWS X-Ray**: Distributed tracing để debug
- **AWS CloudFormation**: Infrastructure as Code cho tự động hóa triển khai
