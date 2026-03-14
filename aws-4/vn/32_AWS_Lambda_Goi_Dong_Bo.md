# AWS Lambda - Gọi Đồng Bộ (Synchronous Invocation)

## Tổng Quan

Tài liệu này trình bày về mô hình gọi đồng bộ (synchronous invocation) cho các hàm AWS Lambda.

## Gọi Đồng Bộ Là Gì?

Gọi đồng bộ có nghĩa là bạn **đang chờ đợi kết quả**, và kết quả sẽ được trả về trực tiếp cho bạn. Đây là loại gọi hàm chúng ta sử dụng khi:

- Sử dụng AWS CLI
- Sử dụng AWS SDK
- Làm việc với API Gateway
- Sử dụng Application Load Balancer

## Đặc Điểm Chính

### Phản Hồi Trực Tiếp
- Bạn chờ đợi hàm hoàn thành
- Kết quả được trả về ngay lập tức
- Client nhận phản hồi trực tiếp

### Xử Lý Lỗi
- Lỗi phải được xử lý ở **phía client**
- Nếu hàm Lambda thất bại, client phải quyết định phải làm gì
- Client chịu trách nhiệm về logic thử lại (retry)
- Chiến lược exponential backoff nên được triển khai bởi client

## Luồng Ví Dụ

### Gọi Đơn Giản Qua CLI/SDK
```
Client → Hàm Lambda → Phản hồi về Client
```

### Mô Hình API Gateway
```
Client → API Gateway → Hàm Lambda
                    ↓
Client ← API Gateway ← Phản hồi
```

Client gọi API Gateway, API Gateway chuyển tiếp yêu cầu đến Lambda. Lambda xử lý yêu cầu và trả về phản hồi thông qua API Gateway về cho client. Trong suốt quá trình này, client đang chờ đợi phản hồi.

## Các Dịch Vụ Sử Dụng Gọi Đồng Bộ

### Các Dịch Vụ Được Đề Cập Trong Khóa Học
- **Elastic Load Balancing (Application Load Balancer)**
- **API Gateway**
- **CloudFront (Lambda@Edge)**
- **Amazon Cognito**
- **AWS Step Functions**

### Các Dịch Vụ Khác (Không Được Đề Cập)
- Amazon S3 Batch
- Amazon Lex
- Amazon Alexa
- Amazon Kinesis Data Firehose

## Khi Nào Sử Dụng Gọi Đồng Bộ

Sử dụng gọi đồng bộ khi:
- Bạn cần phản hồi ngay lập tức từ hàm
- Thao tác được kích hoạt bởi người dùng
- Bạn cần chờ đợi kết quả trước khi tiếp tục
- Ứng dụng của bạn yêu cầu phản hồi trực tiếp

## Các Phương Pháp Hay Nhất

1. **Triển khai logic thử lại** ở phía client
2. **Sử dụng exponential backoff** cho các yêu cầu thất bại
3. **Xử lý timeout** một cách thích hợp
4. **Giám sát thời gian thực thi hàm** để tối ưu trải nghiệm người dùng
5. **Cân nhắc xử lý lỗi** ở cấp độ ứng dụng

## Tóm Tắt

Gọi đồng bộ là một mô hình đơn giản trong đó client chờ đợi Lambda hoàn thành việc thực thi và trả về kết quả. Xử lý lỗi là trách nhiệm của client, do đó việc triển khai các cơ chế thử lại mạnh mẽ và logic xử lý lỗi trong ứng dụng của bạn là rất quan trọng.
