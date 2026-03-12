# Tích Hợp Ứng Dụng AWS - Giới Thiệu

## Tổng Quan

Sau khi triển khai một ứng dụng bằng cách sử dụng Elastic Beanstalk theo cách hoàn toàn tự động, được hỗ trợ bởi CloudFormation và được giám sát đầy đủ, thách thức tiếp theo là triển khai và tích hợp nhiều ứng dụng.

## Các Mô Hình Giao Tiếp và Tích Hợp

Khi làm việc với nhiều ứng dụng trên AWS, chúng cần giao tiếp với nhau. Phần này khám phá các mô hình giao tiếp và tích hợp có sẵn trên AWS.

## Các Dịch Vụ Tích Hợp AWS Chính

### Amazon SQS (Simple Queue Service - Dịch Vụ Hàng Đợi Đơn Giản)
- **Lưu ý**: SQS thực sự là dịch vụ AWS lâu đời nhất
- Đây là chủ đề quan trọng cho các kỳ thi chứng chỉ AWS
- Kỳ vọng nhiều câu hỏi thi tập trung vào SQS

### Amazon SNS (Simple Notification Service - Dịch Vụ Thông Báo Đơn Giản)
- Dịch vụ nhắn tin pub/sub cho giao tiếp ứng dụng-với-ứng dụng

### Amazon Kinesis
- Dịch vụ streaming thời gian thực cho big data
- Trường hợp sử dụng: Khi bạn cần truyền tải khối lượng lớn dữ liệu theo thời gian thực

## Trọng Tâm Quan Trọng Cho Kỳ Thi

⚠️ **Chú Ý**: Phần này là một phần tìm hiểu sâu, đặc biệt cho SQS. Kỳ thi sẽ hỏi nhiều câu hỏi về các dịch vụ tích hợp này, đặc biệt là SQS.

## Những Gì Bạn Sẽ Học

Trong phần này, bạn sẽ có kinh nghiệm thực hành với:
- Thiết lập hàng đợi tin nhắn với SQS
- Triển khai các mô hình pub/sub với SNS
- Streaming dữ liệu thời gian thực với Kinesis
- Các phương pháp hay nhất để tích hợp ứng dụng trên AWS

---

*Hãy cùng thực hành và học cách tích hợp các ứng dụng của chúng ta với nhau!*