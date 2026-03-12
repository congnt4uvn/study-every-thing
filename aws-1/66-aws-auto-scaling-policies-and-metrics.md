# Chính Sách và Chỉ Số Auto Scaling trong AWS

## Tổng Quan

Tài liệu này trình bày các chính sách mở rộng khác nhau có sẵn cho AWS Auto Scaling Groups (ASG), cùng với các chỉ số được khuyến nghị và các phương pháp hay nhất.

## Các Chính Sách Scaling

AWS Auto Scaling Groups hỗ trợ nhiều loại chính sách scaling để giúp quản lý cơ sở hạ tầng của bạn một cách tự động.

### 1. Dynamic Scaling (Mở Rộng Động)

Dynamic scaling điều chỉnh dung lượng dựa trên các chỉ số và điều kiện thời gian thực.

#### Target Tracking Scaling (Theo Dõi Mục Tiêu)

- **Mô tả**: Chính sách scaling đơn giản nhất để thiết lập
- **Cách hoạt động**: 
  - Định nghĩa một chỉ số cho ASG của bạn (ví dụ: mức sử dụng CPU)
  - Đặt giá trị mục tiêu (ví dụ: 40%)
  - ASG tự động mở rộng hoặc thu hẹp để duy trì chỉ số xung quanh giá trị mục tiêu

#### Simple or Step Scaling (Mở Rộng Đơn Giản hoặc Theo Bước)

- **Mô tả**: Mở rộng dựa trên các cảnh báo CloudWatch
- **Cách hoạt động**:
  - Định nghĩa các cảnh báo CloudWatch kích hoạt khi cần thay đổi dung lượng
  - Cảnh báo có thể kích hoạt để thêm hoặc xóa các đơn vị dung lượng khỏi ASG
  - Cung cấp kiểm soát chi tiết hơn đối với các hành động mở rộng

### 2. Scheduled Scaling (Mở Rộng Theo Lịch)

- **Mô tả**: Dự đoán mở rộng dựa trên các mẫu sử dụng đã biết
- **Trường hợp sử dụng**: Khi bạn có các mẫu lưu lượng có thể dự đoán
- **Ví dụ**: Tăng dung lượng tối thiểu lên 10 vào mỗi thứ Sáu lúc 5:00 chiều khi người dùng mới thường xuất hiện

### 3. Predictive Scaling (Mở Rộng Dự Đoán)

- **Mô tả**: Sử dụng machine learning để dự báo tải và lên lịch các hành động mở rộng
- **Cách hoạt động**:
  - Liên tục phân tích dữ liệu tải lịch sử
  - Tạo dự báo dựa trên các mẫu
  - Lên lịch các hành động mở rộng trước
- **Tốt nhất cho**: Các ứng dụng có mẫu tuần hoàn hoặc lặp lại

## Các Chỉ Số Scaling Được Khuyến Nghị

Chọn đúng chỉ số là rất quan trọng cho việc auto scaling hiệu quả. Dưới đây là các chỉ số thường được sử dụng nhất:

### 1. CPU Utilization (Mức Sử Dụng CPU)

- **Tại sao hiệu quả**: Hầu hết các yêu cầu đều liên quan đến tính toán sử dụng CPU
- **Chỉ báo**: Mức sử dụng CPU trung bình cao hơn trên các instance có nghĩa là chúng đang được sử dụng nhiều hơn
- **Tốt nhất cho**: Các ứng dụng tính toán cao

### 2. RequestCountPerTarget (Số Lượng Yêu Cầu Trên Mỗi Target)

- **Mô tả**: Chỉ số dành riêng cho ứng dụng dựa trên các yêu cầu load balancer
- **Cách sử dụng**: 
  - Xác định số lượng yêu cầu tối ưu cho mỗi EC2 instance thông qua kiểm thử
  - Ví dụ: Đặt mục tiêu là 1.000 yêu cầu cho mỗi instance
- **Trường hợp sử dụng**: 
  - Auto Scaling Group với 3 EC2 instances
  - ALB phân phối yêu cầu trên tất cả các instances
  - Nếu mỗi instance trung bình có 3 yêu cầu đang chờ xử lý, giá trị chỉ số là 3

### 3. Network In/Out (Mạng Vào/Ra)

- **Tốt nhất cho**: Các ứng dụng bị giới hạn bởi mạng
- **Trường hợp sử dụng**: Các ứng dụng có nhiều tải lên/tải xuống
- **Cách hoạt động**: Mở rộng dựa trên các chỉ số mạng vào hoặc ra trung bình
- **Lợi ích**: Ngăn mạng trở thành điểm nghẽn cổ chai

### 4. Custom Metrics (Chỉ Số Tùy Chỉnh)

- **Mô tả**: Các chỉ số dành riêng cho ứng dụng được đẩy lên CloudWatch
- **Tính linh hoạt**: Định nghĩa bất kỳ chỉ số nào liên quan đến ứng dụng của bạn
- **Tốt nhất cho**: Các ứng dụng chuyên biệt có yêu cầu mở rộng độc đáo

## Thời Gian Cooldown của Scaling

### Cooldown là gì?

Sau một hoạt động mở rộng (thêm hoặc xóa instances), ASG sẽ vào thời gian cooldown.

### Chi Tiết Chính

- **Thời lượng mặc định**: 5 phút (300 giây)
- **Mục đích**: 
  - Cho phép các chỉ số ổn định
  - Để các instance mới có hiệu lực
  - Quan sát các giá trị chỉ số mới
- **Hành vi**: Trong thời gian cooldown, ASG sẽ không khởi chạy hoặc chấm dứt các instances bổ sung

### Quy Trình Quyết Định

Khi một hành động mở rộng được kích hoạt:
1. Có cooldown mặc định đang có hiệu lực không?
   - **Có**: Bỏ qua hành động
   - **Không**: Tiến hành hành động mở rộng (khởi chạy hoặc chấm dứt instances)

## Các Phương Pháp Hay Nhất

### 1. Sử Dụng AMI Sẵn Sàng

- **Lợi ích**: Giảm thời gian cấu hình cho các EC2 instances
- **Kết quả**: Instances có thể phục vụ yêu cầu nhanh hơn
- **Tác động**: Cho phép thời gian cooldown ngắn hơn và mở rộng linh hoạt hơn

### 2. Bật Detailed Monitoring (Giám Sát Chi Tiết)

- **Tần suất**: Nhận chỉ số mỗi 1 phút thay vì 5 phút
- **Lợi ích**: Phản ứng nhanh hơn với các thay đổi về nhu cầu
- **Kết quả**: Các quyết định mở rộng chính xác và kịp thời hơn

### 3. Tối Ưu Hóa Thời Gian Cooldown

- Bằng cách giảm thời gian khởi động instance với các AMI được cấu hình sẵn
- Bạn có thể giảm thời gian cooldown
- Điều này cho phép mở rộng phản ứng nhanh hơn

## Tóm Tắt

AWS Auto Scaling Groups cung cấp các tùy chọn mở rộng linh hoạt thông qua các chính sách động, theo lịch trình và dự đoán. Chọn đúng chỉ số và tối ưu hóa thời gian cooldown của bạn là chìa khóa để duy trì hiệu suất tối ưu và hiệu quả chi phí.