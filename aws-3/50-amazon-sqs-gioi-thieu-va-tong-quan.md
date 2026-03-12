# Amazon SQS - Giới Thiệu và Tổng Quan

## Mục Lục
- [Giới thiệu về SQS](#giới-thiệu-về-sqs)
- [Các Khái Niệm Cốt Lõi](#các-khái-niệm-cốt-lõi)
- [Tính Năng Chính](#tính-năng-chính)
- [Message Producers (Nhà Sản Xuất Thông Điệp)](#message-producers-nhà-sản-xuất-thông-điệp)
- [Message Consumers (Người Tiêu Thụ Thông Điệp)](#message-consumers-người-tiêu-thụ-thông-điệp)
- [Mở Rộng Quy Mô với SQS](#mở-rộng-quy-mô-với-sqs)
- [Trường Hợp Sử Dụng: Tách Rời Ứng Dụng](#trường-hợp-sử-dụng-tách-rời-ứng-dụng)
- [Bảo Mật SQS](#bảo-mật-sqs)

## Giới Thiệu về SQS

Amazon SQS (Simple Queue Service) là dịch vụ hàng đợi thông điệp được quản lý hoàn toàn, cho phép bạn tách rời và mở rộng quy mô các microservices, hệ thống phân tán và ứng dụng serverless.

### Hàng Đợi (Queue) là gì?

Cốt lõi của SQS là một **hàng đợi (queue)** - một bộ đệm lưu trữ thông điệp giữa producers và consumers. Hàng đợi hoạt động như một kho lưu trữ tạm thời nơi các thông điệp chờ được xử lý.

### Bối Cảnh Lịch Sử

- SQS là một trong những dịch vụ AWS lâu đời nhất (hơn 10 năm tuổi)
- Đây là một trong những dịch vụ đầu tiên trên AWS
- Là dịch vụ được quản lý hoàn toàn được thiết kế để tách rời các ứng dụng

**Lưu Ý Quan Trọng cho Kỳ Thi:** Bất cứ khi nào bạn thấy "application decoupling" (tách rời ứng dụng) trong kỳ thi, hãy nghĩ đến Amazon SQS.

## Các Khái Niệm Cốt Lõi

### Producers (Nhà Sản Xuất)

**Producers** là các thực thể gửi thông điệp vào hàng đợi SQS.

- Bạn có thể có một hoặc nhiều producers
- Producers gửi thông điệp bằng AWS SDK
- API call để gửi thông điệp là `SendMessage`
- Thông điệp được lưu trữ liên tục trong hàng đợi SQS cho đến khi được xử lý

**Ví Dụ Nội Dung Thông Điệp:**
- Xử lý đơn hàng này
- Xử lý video này
- Order ID, Customer ID, Địa chỉ, v.v.

### Consumers (Người Tiêu Thụ)

**Consumers** là các ứng dụng nhận và xử lý thông điệp từ hàng đợi.

- Consumers **poll** (truy vấn) hàng đợi để lấy thông điệp (họ chủ động yêu cầu thông điệp)
- Có thể chạy trên:
  - EC2 instances (máy chủ ảo)
  - Máy chủ on-premises (tại chỗ)
  - AWS Lambda functions (serverless)

**Quy Trình Hoạt Động của Consumer:**
1. Consumer hỏi hàng đợi: "Bạn có thông điệp nào cho tôi không?"
2. Hàng đợi phản hồi với tối đa 10 thông điệp mỗi lần
3. Consumer xử lý các thông điệp (ví dụ: chèn đơn hàng vào cơ sở dữ liệu RDS)
4. Consumer xóa thông điệp khỏi hàng đợi bằng API `DeleteMessage`
5. Điều này đảm bảo không có consumer nào khác sẽ thấy các thông điệp này

## Tính Năng Chính

### Đặc Điểm của Standard Queue

| Tính Năng | Mô Tả |
|-----------|-------|
| **Throughput (Thông Lượng)** | Không giới hạn - gửi bao nhiêu thông điệp mỗi giây tùy thích |
| **Dung Lượng Hàng Đợi** | Số lượng thông điệp không giới hạn trong hàng đợi |
| **Lưu Trữ Thông Điệp** | Mặc định: 4 ngày, Tối đa: 14 ngày |
| **Độ Trễ (Latency)** | Độ trễ thấp - dưới 10ms khi publish và receive |
| **Kích Thước Thông Điệp** | Tối đa 1,024 KB (1 MB) mỗi thông điệp |
| **Đảm Bảo Giao Hàng** | At least once delivery (có thể trùng lặp) |
| **Thứ Tự Thông Điệp** | Best effort ordering (thông điệp có thể không theo thứ tự) |

### Các Điểm Quan Trọng Cần Lưu Ý

- **Thông Điệp Trùng Lặp:** Có khả năng thông điệp được giao nhiều hơn một lần
- **Thứ Tự:** Thông điệp có thể không đến theo đúng thứ tự đã gửi
- **Lưu Trữ:** Thông điệp phải được xử lý trong thời gian lưu trữ nếu không sẽ bị mất

## Message Producers (Nhà Sản Xuất Thông Điệp)

Producers gửi thông điệp đến SQS thông qua quy trình sau:

1. Sử dụng AWS SDK (Software Development Kit)
2. Gọi API `SendMessage`
3. Thông điệp được lưu trữ liên tục trong hàng đợi SQS
4. Thông điệp vẫn còn cho đến khi consumer đọc và xóa nó

### Ví Dụ Trường Hợp Sử Dụng

Xử lý đơn hàng:
- Gửi thông tin đơn hàng vào hàng đợi (order ID, customer ID, địa chỉ)
- Xử lý đơn hàng theo tốc độ của bạn
- Đóng gói và gửi hàng cho người nhận

## Message Consumers (Người Tiêu Thụ Thông Điệp)

### Mô Hình Single Consumer (Consumer Đơn)

```
SQS Queue → Consumer (EC2) → Xử Lý Thông Điệp → Xóa khỏi Queue
```

### Mô Hình Multiple Consumers (Nhiều Consumers)

- Hàng đợi SQS hỗ trợ nhiều consumers xử lý thông điệp song song
- Mỗi consumer nhận một tập hợp thông điệp khác nhau
- Nếu một thông điệp không được xử lý đủ nhanh bởi một consumer, nó có thể được nhận bởi consumer khác
- Xử lý song song này cho phép mở rộng quy mô theo chiều ngang

**Trách Nhiệm của Consumer:**
1. Poll (truy vấn) hàng đợi để lấy thông điệp
2. Nhận tối đa 10 thông điệp mỗi lần
3. Xử lý các thông điệp (mã tùy chỉnh của bạn)
4. Xóa các thông điệp đã xử lý khỏi hàng đợi

## Mở Rộng Quy Mô với SQS

### Horizontal Scaling (Mở Rộng Theo Chiều Ngang)

Để tăng thông lượng:
- Thêm nhiều consumers hơn
- Triển khai mở rộng theo chiều ngang
- Hoàn hảo để sử dụng với Auto Scaling Groups (ASG)

### Tích Hợp Auto Scaling

**Kiến Trúc:**
```
SQS Queue → EC2 Instances (trong Auto Scaling Group) → Xử Lý Thông Điệp
                    ↑
              CloudWatch Metric
            (Độ Dài Queue/ApproximateNumberOfMessages)
                    ↑
              CloudWatch Alarm
                    ↓
          Scale Up/Down ASG
```

**Cách Hoạt Động:**
1. Thiết lập CloudWatch metric: **ApproximateNumberOfMessages** (độ dài hàng đợi)
2. Tạo CloudWatch alarm khi độ dài hàng đợi vượt quá ngưỡng
3. Alarm kích hoạt Auto Scaling Group để tăng dung lượng
4. Nhiều EC2 instances hơn được thêm vào để xử lý thông điệp nhanh hơn
5. Xử lý sự gia tăng nhu cầu (ví dụ: tăng đột biến đơn hàng trên website)

**Lưu Ý cho Kỳ Thi:** Tích hợp SQS + Auto Scaling Group này là một mô hình rất phổ biến trong kỳ thi.

## Trường Hợp Sử Dụng: Tách Rời Ứng Dụng

### Vấn Đề: Kiến Trúc Nguyên Khối (Monolithic)

Một ứng dụng đơn xử lý cả:
- Yêu cầu Frontend
- Xử lý video (thao tác chậm)

**Vấn Đề:** Thời gian xử lý dài làm chậm toàn bộ website.

### Giải Pháp: Kiến Trúc Tách Rời

**Trước:**
```
Frontend Application → Xử Lý Video → S3 Bucket
(Mất quá nhiều thời gian, chặn các yêu cầu)
```

**Sau:**
```
Frontend Tier → SQS Queue → Backend Processing Tier → S3 Bucket
(Lớp Yêu Cầu)              (Auto Scaling Group)
```

### Lợi Ích của Việc Tách Rời

1. **Mở Rộng Độc Lập:** Mở rộng frontend và backend một cách độc lập
2. **Hàng Đợi Không Giới Hạn:** SQS xử lý thông lượng và thông điệp không giới hạn
3. **Kiến Trúc Vững Chắc:** Thiết kế linh hoạt và có khả năng mở rộng
4. **Tối Ưu Instances:**
   - Frontend: Sử dụng EC2 instances tối ưu cho web serving
   - Backend: Sử dụng GPU instances cho xử lý video
5. **Hiệu Suất:** Frontend phản hồi nhanh trong khi backend xử lý không đồng bộ

**Lưu Ý cho Kỳ Thi:** Mô hình kiến trúc tách rời này sẽ xuất hiện trong kỳ thi và là kiến thức được yêu cầu.

## Bảo Mật SQS

### Mã Hóa

| Loại | Mô Tả |
|------|-------|
| **Encryption in Flight (Mã Hóa Trong Quá Trình Truyền)** | Thông điệp được mã hóa bằng HTTPS API trong quá trình truyền |
| **At-Rest Encryption (Mã Hóa Khi Lưu Trữ)** | Sử dụng AWS KMS (Key Management Service) keys |
| **Client-Side Encryption (Mã Hóa Phía Client)** | Client thực hiện mã hóa/giải mã (không được SQS hỗ trợ sẵn) |

### Kiểm Soát Truy Cập

#### IAM Policies
- Điều chỉnh quyền truy cập vào SQS API
- Kiểm soát ai có thể gửi/nhận thông điệp

#### SQS Access Policies
- Tương tự như S3 bucket policies
- Hữu ích cho:
  - **Cross-account access** (Truy cập xuyên tài khoản) đến hàng đợi SQS
  - **Service-to-service access** (Truy cập giữa các dịch vụ) (ví dụ: SNS hoặc S3 ghi vào SQS)
  - Thông báo sự kiện S3 đến SQS

**Ví Dụ Trường Hợp Sử Dụng:**
- Cho phép SNS ghi vào hàng đợi SQS
- Cho phép sự kiện S3 kích hoạt thông điệp đến SQS
- Cấp quyền truy cập hàng đợi của bạn cho tài khoản AWS khác

## Tóm Tắt

Amazon SQS là một dịch vụ hàng đợi thông điệp mạnh mẽ, được quản lý hoàn toàn:

- ✅ Tách rời các ứng dụng và cho phép mở rộng độc lập
- ✅ Cung cấp thông lượng và dung lượng hàng đợi không giới hạn
- ✅ Độ trễ thấp (< 10ms)
- ✅ Hỗ trợ nhiều producers và consumers
- ✅ Tích hợp mượt mà với Auto Scaling Groups
- ✅ Cho phép kiến trúc vững chắc, có khả năng mở rộng
- ✅ Cung cấp nhiều tùy chọn bảo mật (mã hóa và kiểm soát truy cập)

**Điểm Chính:** Hãy nghĩ đến SQS bất cứ khi nào bạn cần tách rời các thành phần ứng dụng hoặc xử lý không đồng bộ ở quy mô lớn.

---

*Tài liệu này cung cấp tổng quan về Amazon SQS. Để thực hành thực tế, hãy tiếp tục với bài giảng tiếp theo.*