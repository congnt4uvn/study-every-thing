# AWS Lambda Concurrency và Throttling

## Tổng Quan

Lambda functions có thể tự động mở rộng quy mô để xử lý các khối lượng công việc khác nhau. Hiểu về concurrency và throttling là rất quan trọng để xây dựng các ứng dụng serverless đáng tin cậy.

## Lambda Concurrency (Đồng Thời)

### Concurrency là gì?

- **Concurrency** là số lượng Lambda function instances đang chạy cùng một lúc
- Lambda có thể mở rộng nhanh chóng và dễ dàng để xử lý tải tăng cao
- Ở quy mô thấp: có thể có 2 executions đồng thời
- Ở quy mô cao: có thể đạt tới 1,000 executions đồng thời (mặc định)

### Reserved Concurrency (Concurrency Dự Trữ)

- **Mục đích**: Giới hạn số lượng executions đồng thời cho một Lambda function cụ thể
- **Cấp độ**: Được thiết lập ở cấp độ function
- **Lợi ích**: Ngăn chặn một function tiêu thụ toàn bộ concurrency có sẵn

**Quan trọng**: Giới hạn 1,000 concurrent executions áp dụng cho **tất cả functions** trong tài khoản AWS của bạn. Nếu một function tiêu thụ hết concurrency, các functions khác sẽ bị throttled.

## Throttling (Điều Tiết)

### Throttling là gì?

Khi số lượng invocations vượt quá giới hạn concurrency, Lambda kích hoạt **throttle**.

### Hành Vi Throttle Theo Loại Invocation

#### Synchronous Invocation (Gọi đồng bộ)
- Trả về **Throttle Error 429**
- Người gọi phải xử lý lỗi và thử lại

#### Asynchronous Invocation (Gọi bất đồng bộ)
- Tự động thử lại
- Event được gửi đến Dead Letter Queue (DLQ) sau khi hết số lần thử

### Yêu Cầu Giới Hạn Cao Hơn

Nếu bạn cần hơn 1,000 concurrent executions, hãy mở support ticket với AWS để yêu cầu giới hạn cao hơn.

## Vấn Đề Concurrency Thường Gặp

### Tình Huống: Một Function Chiếm Hết Concurrency

**Thiết lập:**
- Ứng dụng 1: Load balancer → Lambda Function
- Ứng dụng 2: Một số users → API Gateway → Lambda Function  
- Ứng dụng 3: SDK/CLI → Lambda Function

**Vấn đề:**
Khi Ứng dụng 1 trải qua đợt tăng đột biến (vd: khuyến mãi), nó có thể tiêu thụ cả 1,000 concurrent executions, khiến Ứng dụng 2 và 3 bị throttled.

**Giải pháp:**
Thiết lập reserved concurrency cho mỗi function để đảm bảo phân bổ tài nguyên công bằng.

## Asynchronous Invocations và Throttling

### Ví dụ: S3 Event Notifications

**Luồng xử lý:**
1. Nhiều files được upload lên S3 bucket cùng lúc
2. Mỗi lần upload kích hoạt một Lambda function
3. Nếu đạt giới hạn concurrency, các requests bổ sung sẽ bị throttled

### Cơ Chế Thử Lại

Đối với asynchronous invocations có lỗi throttling (429) hoặc system errors (5xx):
- Lambda trả event về **internal event queue**
- Cố gắng chạy function lại trong **tối đa 6 giờ**
- Khoảng thời gian thử lại tăng theo cấp số nhân: 1 giây → tối đa 5 phút
- Cho phép Lambda cuối cùng tìm được concurrency khả dụng

## Cold Starts (Khởi Động Lạnh)

### Cold Start là gì?

- Xảy ra khi một Lambda function instance mới được tạo
- Code phải được load và initialization code (bên ngoài handler) phải chạy
- Request đầu tiên có **latency cao hơn** so với các requests tiếp theo

### Tác Động

- Initialization lớn (nhiều dependencies, kết nối database, tạo SDK) mất thời gian
- Users có thể trải qua độ trễ (vd: 3 giây)
- Có thể ảnh hưởng tiêu cực đến trải nghiệm người dùng

## Provisioned Concurrency (Concurrency Được Cung Cấp Sẵn)

### Giải Pháp Cho Cold Starts

**Provisioned Concurrency** phân bổ concurrency **trước khi** function được gọi:
- Loại bỏ cold start
- Tất cả invocations có latency thấp và ổn định
- Có thể quản lý bằng **Application Auto Scaling** (theo lịch trình hoặc target tracking)

### Cải Tiến Cold Start cho VPC

**Lưu ý lịch sử**: Lambda functions trong VPC từng có vấn đề cold start nghiêm trọng.

**Cập nhật quan trọng** (Tháng 10/11 năm 2019): AWS đã giảm đáng kể tác động cold start cho Lambda functions trong VPC. Lambda functions hiện đại có vấn đề cold start VPC tối thiểu.

## Tóm Tắt Các Khái Niệm Chính

| Khái Niệm | Mô Tả |
|-----------|-------|
| **Concurrent Executions** | Số lượng Lambda instances đang chạy cùng lúc |
| **Reserved Concurrency** | Giới hạn được đặt ở cấp function để giới hạn concurrent executions |
| **Throttling** | Xảy ra khi invocations vượt quá giới hạn concurrency |
| **Cold Start** | Latency ban đầu khi instance mới được tạo |
| **Provisioned Concurrency** | Dung lượng được phân bổ sẵn để loại bỏ cold starts |

## Best Practices (Thực Hành Tốt Nhất)

1. **Thiết lập Reserved Concurrency** cho các functions quan trọng để tránh throttling
2. **Giám sát Concurrency** trên tất cả functions trong tài khoản của bạn
3. **Sử dụng Provisioned Concurrency** cho các ứng dụng nhạy cảm về latency
4. **Triển khai DLQ** cho asynchronous invocations
5. **Yêu cầu Giới Hạn Cao Hơn** khi cần thông qua AWS support

## Tài Nguyên Bổ Sung

Để xem các biểu đồ chi tiết giải thích về reserved concurrency và provisioned concurrency, hãy tham khảo tài liệu AWS và các bài blog chính thức.

---

**Mẹo Học Tập**: Hiểu sự khác biệt giữa reserved concurrency (giới hạn tối đa) và provisioned concurrency (làm nóng instances trước) là rất quan trọng cho các kỳ thi chứng chỉ AWS.
