# Kiến Trúc Serverless AWS - Tài Liệu Học Tập

## Serverless là gì?

Serverless là một phương pháp điện toán đám mây hiện đại, nơi các nhà phát triển không cần phải quản lý máy chủ. Điều quan trọng cần hiểu là **serverless không có nghĩa là không có máy chủ** - nó chỉ có nghĩa là bạn không thấy chúng hoặc không cần tự cấu hình chúng.

### Các Khái Niệm Chính

- **Không Quản Lý Máy Chủ**: Nhà phát triển triển khai code mà không cần quản lý hạ tầng
- **Function as a Service (FaaS)**: Ban đầu, serverless nghĩa là triển khai các hàm
- **Phạm Vi Rộng Hơn**: Hiện nay bao gồm bất kỳ dịch vụ được quản lý từ xa nào mà bạn không cần cấu hình máy chủ

## Các Dịch Vụ Serverless của AWS

### Dịch Vụ Cốt Lõi

1. **AWS Lambda**
   - Tiên phong trong điện toán serverless
   - Thực thi code mà không cần cấu hình máy chủ
   - Chỉ trả tiền cho thời gian tính toán được sử dụng

2. **Amazon DynamoDB**
   - Cơ sở dữ liệu NoSQL được quản lý hoàn toàn
   - Tự động mở rộng quy mô
   - Lưu trữ và truy xuất dữ liệu dễ dàng

3. **API Gateway**
   - Tạo, xuất bản và quản lý REST API
   - Gọi các hàm Lambda
   - Xử lý các yêu cầu API ở quy mô lớn

4. **Amazon Cognito**
   - Xác thực danh tính và người dùng
   - Đăng nhập và quản lý người dùng an toàn
   - Lưu trữ danh tính cho ứng dụng

5. **Amazon S3**
   - Lưu trữ nội dung tĩnh
   - Lưu trữ website
   - Lưu trữ đối tượng có khả năng mở rộng

6. **Amazon CloudFront**
   - Mạng phân phối nội dung (CDN)
   - Phân phối nội dung tĩnh toàn cầu
   - Hoạt động với S3 để phân phối website

### Các Dịch Vụ Serverless Bổ Sung

- **Amazon SNS** (Simple Notification Service)
  - Nhắn tin và thông báo
  - Không cần quản lý máy chủ
  - Tự động mở rộng

- **Amazon SQS** (Simple Queue Service)
  - Hàng đợi thông điệp
  - Tách biệt các thành phần ứng dụng
  - Tự động mở rộng quy mô

- **Amazon Kinesis Data Firehose**
  - Luồng dữ liệu thời gian thực
  - Tự động mở rộng quy mô
  - Dịch vụ được quản lý hoàn toàn

## Kiến Trúc Serverless Tham Khảo

Luồng ứng dụng serverless điển hình trong AWS:

```
Người dùng → CloudFront + S3 (nội dung tĩnh)
  ↓
Cognito (xác thực/đăng nhập)
  ↓
API Gateway (REST API)
  ↓
Lambda Functions (logic nghiệp vụ)
  ↓
DynamoDB (lưu trữ dữ liệu)
```

## Lợi Ích của Serverless

- **Không Quản Lý Hạ Tầng**: Tập trung vào code, không phải máy chủ
- **Tự Động Mở Rộng**: Dịch vụ tự động mở rộng theo nhu cầu
- **Tiết Kiệm Chi Phí**: Chỉ trả tiền cho những gì bạn sử dụng
- **Phát Triển Nhanh Hơn**: Triển khai code nhanh chóng
- **Tính Sẵn Sàng Cao**: Dự phòng tích hợp sẵn

## Các Lĩnh Vực Cần Tập Trung Học Tập

1. Hiểu về triển khai và thực thi hàm Lambda
2. Thiết kế và vận hành bảng DynamoDB
3. Cấu hình và tích hợp API Gateway
4. Quản lý user pool trong Cognito
5. Chính sách S3 bucket và hosting website tĩnh
6. Các mô hình tích hợp giữa các dịch vụ serverless
7. Chiến lược tối ưu hóa chi phí
8. Best practices về bảo mật cho ứng dụng serverless

---

*Ghi chú học tập: Các dịch vụ Serverless của AWS*
