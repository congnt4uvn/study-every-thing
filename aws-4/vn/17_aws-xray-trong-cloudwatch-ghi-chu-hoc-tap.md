# AWS X-Ray (trong CloudWatch) — Ghi chú học tập

## Mục tiêu của bài thực hành
- Biết **X-Ray** hiện nằm trong **CloudWatch** console (giao diện mới)
- Tạo dữ liệu trace bằng cách triển khai một demo stack qua **CloudFormation**
- Đọc **Service map**, điều tra **lỗi**, và phân tích **traces**
- Nhớ **xóa stack** sau khi xong để tránh phát sinh chi phí

## Ý chính cần nhớ
- **X-Ray được tích hợp vào CloudWatch**: bạn có thể xem **Service map** và **Traces** ngay trong CloudWatch.
- **Service map** thể hiện quan hệ phụ thuộc giữa các thành phần/dịch vụ AWS (microservices và các lời gọi downstream).
- Khi có vấn đề, X-Ray sẽ highlight (ví dụ node màu cam/đỏ), và bạn có thể drill down để xem:
  - độ trễ (latency)
  - số lượng request
  - lỗi/fault
  - phân bố thời gian phản hồi
- **Traces** giúp bạn:
  - chạy query (có thể bắt đầu bằng query rỗng để xem tất cả)
  - lọc theo service/resource cụ thể
  - mở một trace để xem **timeline breakdown** (segments/subsegments)

## Quy trình thực hành (theo nội dung transcript)
### 1) Tìm X-Ray trong CloudWatch
1. Mở **CloudWatch console**.
2. Ở thanh điều hướng bên trái, tìm các mục của X-Ray như **Service map**.
3. Ban đầu có thể chưa có dữ liệu.

### 2) Triển khai demo app (CloudFormation)
Mục tiêu: tạo traffic để đẩy traces vào X-Ray.

1. Mở **CloudFormation** → **Create stack**.
2. Chọn **Upload a template file**.
3. Chọn template được nhắc trong transcript (bản “Scorekeep” X-Ray đơn giản).
4. Đặt tên stack, ví dụ **Scorekeep X-Ray**.
5. Giữ mặc định, chỉ chỉnh 3 thông số mạng ở cuối:
   - **Subnet 1**: chọn subnet thứ nhất
   - **Subnet 2**: chọn subnet thứ hai
   - **VPC ID**: chọn VPC mục tiêu
6. **Next** → **Next** → xác nhận capabilities → **Submit**.

Ghi chú (nhìn tổng quan):
- Demo triển khai một ứng dụng chạy trên **ECS** (front-end + back-end) có instrument X-Ray
- Thấy các tài nguyên liên quan như **DynamoDB tables** và **SNS** (quan sát được trên service map)

### 3) Dùng app để tạo traces
1. Trong stack, mở tab **Outputs**.
2. Lấy URL của **Load Balancer** và mở trên trình duyệt.
3. Dùng UI để tạo game mẫu (transcript dùng **Tic Tac Toe**).
4. Khi bạn thao tác trong app, traces sẽ được gửi vào X-Ray.

### 4) Phân tích trong X-Ray
#### Service map
- Mở **Service map** và nhận diện các node như:
  - ECS service/container
  - các DynamoDB tables
  - SNS topic
- Nếu thấy node báo lỗi (ví dụ **SNS error 100%**), click để xem:
  - latency theo thời gian
  - request theo thời gian
  - số fault
  - phân bố response time

#### Traces
1. Chọn **View traces**.
2. Chạy query (có thể để trống).
3. Thu hẹp kết quả bằng cách thêm điều kiện theo service/resource.
4. Nhìn biểu đồ phân bố latency để tìm các request chậm bất thường.
5. Mở một trace cụ thể để xem:
   - trace map của riêng request đó
   - chi tiết thời gian từng bước (ví dụ các call tới DynamoDB như `GetItem`, ...)
   - segment details, annotations, metadata, và thông tin lỗi

## Khác biệt console (mới vs cũ)
- Giao diện X-Ray mới trong CloudWatch có thể tập trung vào **Service map** và **Traces**.
- Ở **X-Ray console cũ** vẫn có các phần cấu hình như **sampling**, **encryption**, **groups**.

## Dọn dẹp (rất quan trọng)
- Xóa CloudFormation stack (ví dụ **Scorekeep X-Ray**) sau khi làm xong.

## Tự kiểm tra (câu hỏi)
1. Hiện tại bạn tìm Service map của X-Ray ở đâu trong console?
2. Service map thể hiện điều gì?
3. Khi thấy “SNS có lỗi”, bạn làm gì để truy ra các request gây lỗi?
4. Vì sao cần mở một trace cụ thể thay vì chỉ nhìn biểu đồ tổng quan?
5. Kết thúc lab cần làm gì để tránh tốn chi phí?
