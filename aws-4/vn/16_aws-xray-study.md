# AWS X-Ray — Ghi chú học tập

## X-Ray là gì?
**AWS X-Ray** là dịch vụ **distributed tracing (truy vết phân tán)** giúp bạn **trực quan hóa**, **phân tích** và **debug** luồng request chạy qua ứng dụng—đặc biệt hữu ích trong kiến trúc **microservices**.

### Vì sao quan trọng? (vấn đề X-Ray giải quyết)
Debug production theo “cách cũ” thường là:
- Cố gắng tái hiện lỗi ở máy local (khó/không thể)
- Thêm rất nhiều log
- Redeploy lên production rồi đọc log để đoán nguyên nhân

Khi hệ thống lớn lên, việc này càng đau đầu vì:
- Nhiều service log khác format
- CloudWatch Logs khó điều hướng và làm analytics khi dữ liệu phân tán
- Microservices thiếu cái nhìn “end-to-end” cho một request

X-Ray cung cấp **cái nhìn end-to-end** (service map + trace) cho từng request.

## Bạn nhận được gì?
- **Service map (đồ thị)** mô tả kiến trúc theo những gì X-Ray quan sát
- Khả năng nhìn thấy:
  - Tỷ lệ lỗi (biết service/phụ thuộc nào đang lỗi)
  - Latency và điểm nghẽn (bottleneck)
  - Phụ thuộc giữa các service
  - Hành vi theo từng request (trace) và exception/error tương ứng

## Khái niệm cốt lõi (hay gặp trong đề)
### Tracing (truy vết)
Tracing là theo dõi **một request** đi qua tất cả thành phần liên quan (LB, app, DB, queue, …).

### Segment / Subsegment
- Một **trace** được tạo từ nhiều **segment**.
- Segment có thể chứa **subsegment**.
- Mỗi thành phần xử lý request đóng góp dữ liệu vào trace.

### Annotations
Thêm metadata dạng key/value vào trace để tra cứu/đánh dấu ngữ cảnh (ví dụ: tenant, userType, orderId).

### Sampling
Không bắt buộc trace mọi request. Có thể:
- Lấy theo phần trăm tổng request, hoặc
- Giới hạn theo tần suất (ví dụ vài trace mỗi phút)

## Tương thích / chạy ở đâu
X-Ray tích hợp với nhiều dịch vụ AWS, ví dụ:
- AWS Lambda
- Elastic Beanstalk
- Amazon ECS
- Elastic Load Balancing (ELB)
- Amazon API Gateway
- Amazon EC2

Ngoài ra có thể dùng với ứng dụng **on-premises**.

## X-Ray hoạt động thế nào (tổng quan)
1. Ứng dụng nhận request.
2. Code đã instrument thu thập trace cho:
   - AWS SDK calls
   - HTTP/HTTPS calls
   - DB calls (MySQL, PostgreSQL, DynamoDB)
   - (và các tích hợp khác như queue nếu hỗ trợ)
3. Trace data được gửi lên X-Ray (thường thông qua daemon, tùy môi trường).
4. X-Ray tổng hợp segments để tạo **service map**.

## Bật X-Ray (phần dễ bị hỏi)
Có 2 bước chính:

### 1) Instrument code (X-Ray SDK)
- Ứng dụng cần import/sử dụng **AWS X-Ray SDK**.
- Ngôn ngữ được nhắc tới: Java, Python, Go, Node.js, .NET.
- “Ít sửa code” nhưng vẫn phải sửa một chút.

SDK có thể capture:
- Gọi AWS services qua AWS SDK
- HTTP/HTTPS requests
- DB calls cho MySQL/PostgreSQL/DynamoDB

### 2) Đảm bảo có “daemon/tích hợp”
Hai trường hợp phổ biến:

**A. EC2 / on-prem / server tự quản**
- Bạn phải **cài và chạy X-Ray daemon**.
- Daemon là chương trình nhỏ nhận dữ liệu trace (mô tả như chặn/thu UDP ở mức thấp) rồi **gom batch và gửi** lên AWS X-Ray (thường mỗi giây).

**B. Tích hợp sẵn (ví dụ Lambda và một số dịch vụ AWS)**
- Nền tảng có thể chạy daemon/tích hợp giúp bạn.
- Bạn chủ yếu cần bật tracing và instrument code.

### IAM permissions (bắt buộc)
Ứng dụng/service role cần quyền IAM để **ghi (write) trace data** lên X-Ray.

## Checklist xử lý sự cố
### “Chạy local OK nhưng lên EC2 không chạy”
Nguyên nhân hay gặp:
- Local có chạy daemon, nhưng **EC2 chưa chạy daemon**
- IAM role của EC2 thiếu quyền **ghi dữ liệu lên X-Ray**

Checklist nhanh cho EC2:
- [ ] Code đã instrument bằng X-Ray SDK
- [ ] X-Ray daemon đã cài và đang chạy trên instance
- [ ] IAM role của instance có quyền publish trace data

### Lambda không thấy trace
Kiểm tra:
- [ ] Lambda execution role có quyền X-Ray cần thiết
- [ ] Code có import/sử dụng X-Ray SDK/instrumentation (nếu cần)
- [ ] Đã bật **Active tracing** cho function

## Dạng câu hỏi thường gặp trong đề
- “Bật X-Ray trên EC2 khác gì Lambda?”
- “Vì sao X-Ray chạy trên máy cá nhân nhưng deploy EC2 thì không?”
- “X-Ray daemon làm gì?”
- “Segment khác subsegment thế nào?”
- “Service map giúp gì khi dùng microservices?”

## Tự kiểm tra nhanh
1. X-Ray giải quyết vấn đề gì mà chỉ log thôi khó làm trong microservices?
2. Hai bước chính để bật X-Ray là gì?
3. Khi nào bạn phải tự cài X-Ray daemon?
4. X-Ray cần những quyền gì để hoạt động?
5. Segment và subsegment khác nhau thế nào?
