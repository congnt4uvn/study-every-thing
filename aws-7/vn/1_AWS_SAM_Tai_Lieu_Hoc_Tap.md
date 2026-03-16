# Tài Liệu Học Tập AWS SAM (Serverless Application Model)

## Giới Thiệu

AWS SAM là một framework để xây dựng các ứng dụng serverless trên AWS. Nó cung cấp cách đơn giản để định nghĩa Amazon API Gateway APIs, AWS Lambda functions, và Amazon DynamoDB tables cần thiết cho ứng dụng serverless của bạn.

## Các Khái Niệm Chính

### AWS SAM Là Gì?

- **AWS SAM** cho phép các lập trình viên viết các template YAML để định nghĩa cách ứng dụng hoạt động và được triển khai
- Về bản chất, nó là **lối tắt cho CloudFormation** nhưng thân thiện hơn với lập trình viên
- Nó đang trở thành một dịch vụ ngày càng phổ biến tại AWS
- Làm cho việc triển khai API serverless đơn giản hơn nhiều so với việc sử dụng CloudFormation trực tiếp

### Tại Sao Dùng SAM Thay Vì CloudFormation?

Mặc dù bạn có thể triển khai ứng dụng serverless bằng CloudFormation trực tiếp, SAM mang lại nhiều lợi ích:

1. **Cú Pháp Đơn Giản** - Ít dài dòng hơn so với CloudFormation templates
2. **Tích Hợp Best Practices** - Kết hợp các phương pháp hay nhất của AWS serverless
3. **Thân Thiện Với Lập Trình Viên** - Tự nhiên và trực quan hơn cho developers
4. **Phát Triển Nhanh** - Nhanh hơn để viết và triển khai ứng dụng serverless

## Các Thành Phần Cốt Lõi

### Cấu Trúc SAM Template

SAM templates là các file YAML (hoặc JSON) mô tả cơ sở hạ tầng ứng dụng serverless của bạn:

- **Lambda Functions** - Định nghĩa các serverless compute functions
- **API Gateway** - Cấu hình RESTful APIs
- **DynamoDB Tables** - Thiết lập cơ sở dữ liệu NoSQL
- **Event Sources** - Cấu hình triggers cho Lambda functions
- **Permissions** - Quản lý IAM roles và policies

### SAM CLI

SAM Command Line Interface cung cấp các lệnh để:
- Khởi tạo các dự án serverless mới
- Build ứng dụng serverless locally
- Test Lambda functions trên máy local
- Package ứng dụng để triển khai
- Deploy lên AWS

## Lợi Ích Của AWS SAM

1. **Infrastructure as Code** - Định nghĩa toàn bộ serverless stack trong code
2. **Test Cục Bộ** - Test Lambda functions và APIs locally trước khi deploy
3. **Triển Khai Đơn Giản** - Một lệnh duy nhất để deploy toàn bộ ứng dụng
4. **Kiểm Soát Phiên Bản** - Theo dõi thay đổi infrastructure trong Git
5. **Môi Trường Tái Tạo** - Triển khai nhất quán trên các môi trường khác nhau

## Ứng Dụng Thực Tế

AWS SAM lý tưởng để xây dựng:
- RESTful APIs
- Ứng dụng điều khiển bởi sự kiện (event-driven)
- Kiến trúc microservices
- Data processing pipelines
- Scheduled tasks và cron jobs

## Mẹo Cho Kỳ Thi

Đối với các kỳ thi chứng chỉ AWS:
- Hiểu rằng SAM đơn giản hóa CloudFormation cho các ứng dụng serverless
- Biết cấu trúc cơ bản của SAM templates (dựa trên YAML)
- Nhớ rằng SAM được thiết kế đặc biệt cho **ứng dụng serverless**
- Làm quen với SAM CLI và các lệnh cơ bản của nó
- Hiểu mối quan hệ giữa SAM và CloudFormation

## Bắt Đầu

Để bắt đầu sử dụng AWS SAM:
1. Cài đặt SAM CLI
2. Chạy `sam init` để tạo project mới
3. Viết code Lambda function của bạn
4. Định nghĩa resources trong `template.yaml`
5. Test locally với `sam local`
6. Deploy với `sam deploy`

## Tóm Tắt

AWS SAM chuyển đổi cách các lập trình viên triển khai ứng dụng serverless bằng cách cung cấp một abstraction đơn giản, thân thiện với developer trên CloudFormation. Đây là công cụ thiết yếu cho phát triển cloud hiện đại trên AWS và đang trở nên ngày càng quan trọng đối với các chuyên gia AWS.
