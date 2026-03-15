# AWS CodeGuru Profiler - Cấu Hình Agent

## Tổng Quan
AWS CodeGuru Profiler sử dụng một agent có thể được cấu hình để tinh chỉnh hành vi và khả năng giám sát hiệu suất.

## Các Tham Số Cấu Hình Chính

### 1. MaxStackDepth (Độ Sâu Stack Tối Đa)
**Mục đích:** Xác định lượng code được biểu diễn trong profile

**Cách hoạt động:**
- Đếm độ sâu của các lệnh gọi method trong code của bạn
- Ví dụ: Nếu Method A → Method B → Method C → Method D (độ sâu = 4)
- Nếu MaxStackDepth được đặt là 2, chỉ Method A và Method B sẽ được profile

**Quan trọng:** Nếu bạn cần profile các call stack sâu hơn, hãy tăng tham số này.

### 2. Memory Usage Limit Percent (Giới Hạn Phần Trăm Sử Dụng Bộ Nhớ)
**Mục đích:** Kiểm soát lượng bộ nhớ mà profiler agent được phép sử dụng

**Cấu hình:** Đặt dưới dạng giá trị phần trăm để giới hạn mức tiêu thụ bộ nhớ của profiler

### 3. Minimum Time for Reporting (Thời Gian Báo Cáo Tối Thiểu - milliseconds)
**Mục đích:** Đặt khoảng thời gian tối thiểu giữa các lần gửi báo cáo

**Lưu ý:** Khoảng thời gian báo cáo thực tế sẽ được giới hạn bởi giá trị tối thiểu này

### 4. Reporting Interval (Khoảng Thời Gian Báo Cáo - milliseconds)
**Mục đích:** Cho agent biết tần suất báo cáo dữ liệu profiling đã thu thập

**Cấu hình:** Có thể tăng dựa trên nhu cầu giám sát của bạn

### 5. Sampling Interval (Khoảng Thời Gian Lấy Mẫu - milliseconds)
**Mục đích:** Kiểm soát khoảng thời gian lấy mẫu được sử dụng để profile các mẫu

**Điểm Chính:**
- **Giá trị thấp hơn** = Lấy mẫu thường xuyên hơn = Tỷ lệ lấy mẫu cao hơn
- Tỷ lệ lấy mẫu cao cho phép bạn bắt được nhiều lệnh gọi function/method hơn
- Đánh đổi giữa chi tiết và hiệu suất overhead

## Mẹo Thi
- Bạn không cần ghi nhớ tất cả giá trị tham số
- Hiểu cách mỗi thiết lập ảnh hưởng đến hành vi của CodeGuru agent
- Có khả năng xác định tham số đúng dựa trên tình huống trong câu hỏi thi
- Tập trung hiểu mối quan hệ giữa:
  - MaxStackDepth → phạm vi độ sâu call stack
  - Sampling Interval → độ chi tiết của profiling
  - Reporting Interval → tần suất gửi dữ liệu

## Tóm Tắt
Cấu hình agent của CodeGuru Profiler cho phép bạn cân bằng giữa:
- **Độ sâu profiling** (MaxStackDepth)
- **Sử dụng tài nguyên** (Memory Usage Limit)
- **Tần suất lấy mẫu** (Sampling Interval)
- **Tần suất báo cáo** (Reporting Interval)

Cấu hình các tham số này dựa trên nhu cầu cụ thể và yêu cầu hiệu suất của ứng dụng của bạn.
