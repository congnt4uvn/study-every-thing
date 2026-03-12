# AWS Route 53 Health Checks - Hướng Dẫn Thực Hành

## Tổng Quan

Hướng dẫn này trình bày cách tạo và cấu hình health checks trong AWS Route 53 để giám sát các EC2 instance trên nhiều region. Chúng ta sẽ khám phá các loại health check khác nhau bao gồm giám sát endpoint, calculated health checks và giám sát dựa trên CloudWatch alarm.

## Tạo Health Checks Cơ Bản

### Bước 1: Truy Cập Health Checks

1. Điều hướng đến Route 53 console
2. Ở menu bên trái, click vào **Health Checks**
3. Chúng ta sẽ tạo health checks cho tất cả các EC2 instance

### Bước 2: Tạo Health Check Đầu Tiên (US East 1)

1. Click **Create Health Check**
2. Cấu hình các thiết lập sau:
   - **Name**: US East 1
   - **Type**: Endpoint
   - **Specify endpoint by**: IP address (hoặc domain name)
   - **IP Address**: Nhập IP của instance US East 1
   - **Port**: 80 (cổng HTTP)
   - **Path**: `/` (thư mục gốc của website)

> **Lưu ý**: Trong các ứng dụng thực tế, thường sử dụng một endpoint health chuyên dụng như `/health` để trả về trạng thái sức khỏe của ứng dụng.

### Bước 3: Cấu Hình Nâng Cao

Xem xét các thiết lập nâng cao:

- **Interval** (Khoảng thời gian):
  - Standard (mỗi 30 giây) - được khuyến nghị để tiết kiệm chi phí
  - Fast (mỗi 10 giây) - tùy chọn đắt hơn

- **Failure Threshold** (Ngưỡng lỗi): Số lần thất bại liên tiếp trước khi đánh dấu là không khỏe mạnh

- **String Matching** (Khớp chuỗi): Tùy chọn tìm kiếm một chuỗi cụ thể trong 5,120 bytes đầu tiên của phản hồi

- **Latency Graph** (Biểu đồ độ trễ): Bật để theo dõi xu hướng độ trễ theo thời gian

- **Invert Health Check Status** (Đảo ngược trạng thái): Đảo ngược trạng thái khỏe mạnh/không khỏe mạnh

- **Health Checker Regions** (Các region kiểm tra): Sử dụng khuyến nghị hoặc tùy chỉnh các region cụ thể

- **Alarm Notification** (Thông báo cảnh báo): Tùy chọn tạo CloudWatch alarm để nhận thông báo (chọn No cho hướng dẫn này)

### Bước 4: Tạo Các Health Check Bổ Sung

Lặp lại quy trình cho các region khác:

**Health Check Thứ Hai (AP Southeast 1 - Singapore)**
1. Tạo health check
2. Name: AP Southeast 1
3. Nhập địa chỉ IP (không phải hostname)
4. Click Next và Create

**Health Check Thứ Ba (EU Central 1)**
1. Tạo health check
2. Name: EU Central 1
3. Nhập địa chỉ IP
4. Click Next và Create

## Kiểm Tra Lỗi Health Check

Để xác minh health checks hoạt động đúng, chúng ta sẽ mô phỏng một lỗi:

1. Điều hướng đến EC2 console
2. Chọn instance Singapore
3. Vào **Security Group** liên quan
4. Click **Actions** → **Edit Inbound Rules**
5. Xóa quy tắc HTTP (cổng 80)
6. Lưu thay đổi

**Kết quả**: Health check cho AP Southeast 1 sẽ chuyển sang trạng thái **Unhealthy** sau khi đạt ngưỡng lỗi.

## Giám Sát Trạng Thái Health Check

Sau một khoảng thời gian ngắn (30-60 giây), bạn sẽ thấy:

- **Ba health checks** đã được tạo
- **Một không khỏe mạnh** (AP Southeast 1 - do security group bị chặn)
- **Hai khỏe mạnh** (US East 1 và EU Central 1)

### Xem Chi Tiết Health Check

1. Click vào bất kỳ health check nào để xem thông tin chi tiết
2. Kiểm tra timestamp **Last Checked**
3. Đối với các health check không khỏe mạnh, click **View Last Failed Check**
   - Hiển thị chi tiết lỗi (ví dụ: "Connection timeout")
   - Chỉ ra nguyên nhân: "Requests có thể bị chặn bởi firewall" (security group)

## Các Loại Health Check Nâng Cao

### Calculated Health Checks

Calculated health checks giám sát trạng thái của các health check khác và báo cáo dựa trên kết quả kết hợp.

**Tạo Calculated Health Check:**

1. Click **Create Health Check**
2. Chọn loại **Calculated**
3. Name: "Calculated Health Check"
4. Chọn các child health check để giám sát (cả ba regional checks)
5. Cấu hình ngưỡng báo cáo:
   - Báo cáo khỏe mạnh khi **1 trong 3** khỏe mạnh (logic OR)
   - Báo cáo khỏe mạnh khi **2 trong 3** khỏe mạnh
   - Báo cáo khỏe mạnh khi **tất cả** đều khỏe mạnh (logic AND)
6. Trong ví dụ này, chọn "healthy when all checks are healthy"
7. Click Next và Create

**Kết quả**: Calculated health check sẽ hiển thị là **Unhealthy** vì một child health check (AP Southeast 1) không khỏe mạnh.

### Health Checks Dựa Trên CloudWatch Alarm

Loại này giám sát trạng thái của CloudWatch alarm, hữu ích cho việc giám sát tài nguyên private.

**Trường hợp sử dụng**: Giám sát các EC2 instance private không thể truy cập trực tiếp bởi Route 53 health checkers.

**Các Bước Cấu Hình:**
1. Tạo health check
2. Chọn **State of CloudWatch alarm**
3. Chỉ định region nơi alarm tồn tại
4. Chọn CloudWatch alarm
5. Alarm có thể giám sát các metrics từ các EC2 instance private

> **Lưu ý**: Tùy chọn này yêu cầu CloudWatch alarm đã được cấu hình sẵn.

## Lợi Ích Chính Của Route 53 Health Checks

- **Giám sát đa region**: Theo dõi sức khỏe trên toàn bộ hạ tầng toàn cầu
- **Phát hiện lỗi linh hoạt**: Tùy chỉnh ngưỡng và khoảng thời gian
- **Calculated checks**: Kết hợp nhiều checks với các phép toán logic
- **Giám sát tài nguyên private**: Sử dụng CloudWatch alarms để giám sát tài nguyên nội bộ
- **Tích hợp với Route 53 routing**: Sử dụng health checks với các routing policies (sẽ được đề cập trong bài giảng tiếp theo)

## Tóm Tắt

Trong hướng dẫn này, chúng ta đã học cách:
- Tạo endpoint-based health checks cho các EC2 instance
- Cấu hình khoảng thời gian và ngưỡng health check
- Kiểm tra lỗi health check bằng cách sử dụng quy tắc security group
- Tạo calculated health checks cho giám sát kết hợp
- Hiểu về health checks dựa trên CloudWatch alarm

Health checks là một tính năng mạnh mẽ sẽ được sử dụng cùng với Route 53 records và routing policies trong các bài học sắp tới.

## Các Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ khám phá cách sử dụng các health checks này với Route 53 routing policies để triển khai automatic failover và intelligent traffic routing.