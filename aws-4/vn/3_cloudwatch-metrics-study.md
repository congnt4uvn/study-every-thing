# Ghi chú học AWS — Amazon CloudWatch Metrics

## CloudWatch Metrics là gì?
- **CloudWatch Metrics** cung cấp các số đo dạng chuỗi thời gian (time-series) cho nhiều dịch vụ AWS.
- Dùng metrics để **quan sát hệ thống** và **troubleshoot** ở mức cơ bản.
- Tên metric thường gợi ý ý nghĩa (ví dụ: `CPUUtilization`, `NetworkIn`).

## Khái niệm cốt lõi (Cần nhớ)
### Namespace
- Metrics được nhóm theo **namespace** (thường tương ứng với dịch vụ).
- Trên Console bạn sẽ thấy các namespace như **EC2**, **EBS**, **ELB**, **Auto Scaling**, **EFS**, ...

### Dimension
- **Dimension** là thuộc tính giúp định danh/thu hẹp metric theo tài nguyên cụ thể.
- Ví dụ: **InstanceId**, **Environment**, ...
- Dùng dimension để lọc đúng resource bạn cần xem.
- Có thể chọn **tối đa 30 dimensions cho mỗi metric**.

### Timestamp
- Mỗi điểm dữ liệu metric có **timestamp**.
- Chu kỳ (granularity/period) quyết định độ “mịn” của dữ liệu (ví dụ 5 phút vs 1 phút).

## Dashboard
- Bạn có thể tạo **CloudWatch Dashboard** từ metrics để theo dõi nhanh.
- Có nhiều kiểu hiển thị: line, stacked area, number, pie, ...

## Tần suất metric của EC2 (Mặc định vs Detailed Monitoring)
### Mặc định
- EC2 publish metrics mỗi **5 phút**.

### Detailed Monitoring (tính phí)
- Bật **Detailed Monitoring** sẽ có metrics mỗi **1 phút**.
- Lợi ích: **phản ứng nhanh hơn** khi metric thay đổi.
- Có thể hữu ích cho **Auto Scaling Group (ASG)** nếu scale dựa trên alarm.
- Ghi chú theo nội dung nguồn: detailed monitoring có **10 detailed monitoring metrics**.

## Custom Metrics (Điểm hay bị nhầm)
- **RAM/Memory usage không được đẩy lên mặc định** trong CloudWatch metrics của EC2.
- Muốn xem RAM bạn cần publish dưới dạng **custom metric** từ instance (agent/script).

## Cách xem Metrics trong Console (Thực hành nhanh)
1. Mở **CloudWatch**.
2. Vào **Metrics**.
3. Chọn **namespace** (ví dụ **EC2**).
4. Chọn phần theo resource (ví dụ **Per-Instance Metrics**).
5. Chọn metric cần xem (ví dụ trong nguồn: **CPU credit balance**).
6. Chọn khoảng thời gian (ví dụ **1 tháng**) để có dữ liệu đủ dài.
7. Thử các tùy chọn hiển thị và filter.
8. Có thể **Add to dashboard**.
9. Có thể **Download CSV** hoặc **Share**.

## Cách đọc một metric (Mẹo học nhanh)
- Đọc tên metric để hiểu nó đo gì.
- Nhìn xu hướng theo thời gian và liên hệ với sự kiện (deploy, scale, traffic spike).
- Khi troubleshoot nên kết hợp nhiều metric (CPU + Network + disk signals).

## Câu hỏi tự kiểm tra
- Namespace trong CloudWatch là gì? Kể 2 ví dụ.
- Dimension là gì? Dùng để làm gì?
- EC2 mặc định publish metrics mỗi bao lâu? Detailed Monitoring thay đổi gì?
- Vì sao RAM không có sẵn trong CloudWatch metrics của EC2?
- Khi nào cần 1-minute metrics thay vì 5-minute metrics?

## Mini Lab (10–15 phút)
- Chọn một EC2 instance và vẽ biểu đồ 1 tuần cho:
  - `CPUUtilization`
  - `NetworkIn`
  - Một metric liên quan đến credit (nếu có)
- Đổi period và so sánh biểu đồ “mượt” vs “nhiễu”.
- Lưu biểu đồ vào một CloudWatch dashboard.
