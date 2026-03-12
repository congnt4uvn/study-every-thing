# AWS Auto Scaling - Hướng Dẫn Thực Hành Chính Sách Mở Rộng Động

## Tổng Quan

Hướng dẫn này trình bày cách triển khai và kiểm tra các chính sách mở rộng tự động cho AWS Auto Scaling Groups (ASG), tập trung vào mở rộng động, mở rộng dự đoán và hành động theo lịch.

## Các Loại Chính Sách Mở Rộng

### 1. Hành Động Theo Lịch (Scheduled Actions)

Hành động theo lịch cho phép bạn lập kế hoạch các hoạt động mở rộng trước dựa trên các sự kiện có thể dự đoán.

**Tính Năng Chính:**
- Đặt công suất mong muốn, giá trị tối thiểu hoặc tối đa
- Cấu hình lịch trình định kỳ (hàng giờ, hàng tuần, v.v.)
- Xác định thời gian bắt đầu và kết thúc
- Hoàn hảo cho các sự kiện dự kiến trước (ví dụ: các chiến dịch khuyến mãi)

### 2. Chính Sách Mở Rộng Dự Đoán (Predictive Scaling)

Mở rộng dựa trên machine learning với dữ liệu lịch sử và dự báo.

**Tùy Chọn Cấu Hình:**
- Chọn các chỉ số để giám sát:
  - Sử dụng CPU
  - Mạng vào/ra
  - Số lượng yêu cầu Application Load Balancer
  - Chỉ số tùy chỉnh
- Đặt mức sử dụng mục tiêu (ví dụ: 50% CPU)
- Yêu cầu dữ liệu lịch sử (thường tối thiểu một tuần)

**Lưu ý:** Mở rộng dự đoán cần thời gian giám sát kéo dài để tạo ra dự báo chính xác.

### 3. Chính Sách Mở Rộng Động (Dynamic Scaling)

Mở rộng theo thời gian thực dựa trên cảnh báo CloudWatch và chỉ số hiện tại.

#### Các Loại Mở Rộng Động:

**Mở Rộng Đơn Giản (Simple Scaling):**
- Kích hoạt dựa trên cảnh báo CloudWatch đơn lẻ
- Thêm/xóa số lượng instance cố định hoặc theo phần trăm
- Ví dụ: Thêm 2 instance hoặc 10% kích thước nhóm

**Mở Rộng Theo Bước (Step Scaling):**
- Nhiều bước mở rộng dựa trên mức độ nghiêm trọng của cảnh báo
- Các hành động khác nhau cho các mức ngưỡng khác nhau
- Ví dụ: Thêm 10 instance cho tải trọng nghiêm trọng, 1 instance cho tải trọng vừa phải

**Mở Rộng Theo Dõi Mục Tiêu (Target Tracking):**
- Tự động duy trì chỉ số cụ thể ở giá trị mục tiêu
- Tạo cảnh báo CloudWatch tự động
- Đơn giản nhất để cấu hình và quản lý

## Thực Hành: Triển Khai Chính Sách Theo Dõi Mục Tiêu

### Yêu Cầu Trước
- Auto Scaling Group đang hoạt động
- Các EC2 instance đang chạy
- Quyền IAM phù hợp

### Bước 1: Cấu Hình Công Suất ASG

1. Đặt công suất tối thiểu: 1
2. Đặt công suất tối đa: 3
3. Đặt công suất mong muốn: 1

Điều này cho phép ASG mở rộng từ 1 đến 3 instance.

### Bước 2: Tạo Chính Sách Theo Dõi Mục Tiêu

1. Điều hướng đến Auto Scaling Group của bạn
2. Vào tab "Automatic scaling"
3. Tạo chính sách mở rộng động
4. Chọn "Target tracking scaling"
5. Cấu hình:
   - **Tên Chính Sách:** target tracking policy
   - **Chỉ Số:** Sử dụng CPU trung bình
   - **Giá Trị Mục Tiêu:** 40%
6. Tạo chính sách

### Bước 3: Hiểu Về Cảnh Báo CloudWatch

Chính sách theo dõi mục tiêu tự động tạo hai cảnh báo CloudWatch:

**AlarmHigh (Mở Rộng Ra):**
- Kích hoạt khi CPU > 40% trong 3 điểm dữ liệu (3 phút)
- Hành động: Thêm instance

**AlarmLow (Thu Hẹp Lại):**
- Kích hoạt khi CPU < 28% trong 15 điểm dữ liệu (15 phút)
- Hành động: Xóa instance

### Bước 4: Kiểm Tra Chính Sách Mở Rộng

#### Mô Phỏng Tải CPU Cao

1. Kết nối đến EC2 instance bằng EC2 Instance Connect
2. Cài đặt công cụ stress:
   ```bash
   sudo amazon-linux-extras install epel -y
   sudo yum install stress -y
   ```
3. Tạo tải CPU:
   ```bash
   stress -c 4
   ```
   Lệnh này sử dụng 4 vCPU ở công suất 100%.

#### Quan Sát Hành Vi Mở Rộng

1. **Giám Sát Hoạt Động:**
   - Vào ASG → tab Activity
   - Theo dõi các hoạt động mở rộng

2. **Kiểm Tra Số Lượng Instance:**
   - Vào Instance Management
   - Quan sát các instance mới được khởi chạy

3. **Xem Chỉ Số:**
   - Kiểm tra tab Monitoring
   - Sử dụng CPU nên tăng vọt lên ~100%
   - Theo dõi điểm kích hoạt mở rộng

4. **Xác Minh Cảnh Báo CloudWatch:**
   - Điều hướng đến dịch vụ CloudWatch
   - Kiểm tra phần Alarms
   - AlarmHigh nên ở trạng thái "In alarm"

### Bước 5: Kiểm Tra Hành Động Thu Hẹp

1. Dừng lệnh stress (Ctrl+C) hoặc khởi động lại instance
2. Sử dụng CPU giảm xuống ~0%
3. Đợi 15 phút cho thời gian cooldown thu hẹp
4. AlarmLow kích hoạt
5. ASG chấm dứt các instance thừa
6. Công suất trở về mức tối thiểu (1 instance)

## Kết Quả Mong Đợi

### Chuỗi Mở Rộng Ra:
1. CPU đạt 40% → AlarmHigh kích hoạt
2. Công suất mong muốn: 1 → 2 instance
3. Nếu CPU vẫn cao: 2 → 3 instance

### Chuỗi Thu Hẹp Lại:
1. CPU giảm dưới 28% trong 15 phút → AlarmLow kích hoạt
2. Công suất mong muốn: 3 → 2 instance
3. Sau cooldown: 2 → 1 instance

## Thực Hành Tốt Nhất

1. **Đặt Ngưỡng Phù Hợp:**
   - Xem xét yêu cầu của ứng dụng
   - Cân bằng giữa chi phí và hiệu suất

2. **Cấu Hình Thời Gian Cooldown:**
   - Ngăn chặn dao động mở rộng nhanh
   - Mặc định thu hẹp lại thận trọng hơn (15 phút)

3. **Giám Sát Hoạt Động Mở Rộng:**
   - Xem xét Activity History thường xuyên
   - Điều chỉnh chính sách dựa trên các mẫu

4. **Quản Lý Chi Phí:**
   - Đặt giới hạn công suất tối đa
   - Xóa các chính sách mở rộng không sử dụng
   - Giám sát chi phí cảnh báo CloudWatch

## Dọn Dẹp

Để dọn dẹp tài nguyên:

1. Xóa chính sách mở rộng theo dõi mục tiêu
2. Cảnh báo CloudWatch sẽ được tự động xóa
3. Chấm dứt bất kỳ EC2 instance thừa nếu cần
4. Cân nhắc xóa ASG nếu không còn cần thiết

## Tóm Tắt

Chính sách theo dõi mục tiêu cung cấp:
- ✅ Tự động tạo cảnh báo CloudWatch
- ✅ Cấu hình đơn giản
- ✅ Mở rộng hai chiều (ra và vào)
- ✅ Tự động hóa dựa trên chỉ số
- ✅ Sử dụng tài nguyên tiết kiệm chi phí

Điều này khiến chúng trở nên lý tưởng cho hầu hết các trường hợp sử dụng auto-scaling khi bạn muốn duy trì một chỉ số hiệu suất cụ thể ở giá trị mục tiêu.