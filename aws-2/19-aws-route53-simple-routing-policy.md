# AWS Route 53 - Chính Sách Định Tuyến Đơn Giản (Simple Routing Policy)

## Giới Thiệu Về Chính Sách Định Tuyến

Chính sách định tuyến Route 53 giúp phản hồi các truy vấn DNS. Điều quan trọng là không nên nhầm lẫn định tuyến DNS với định tuyến load balancer:

- **Định tuyến DNS**: KHÔNG định tuyến lưu lượng thực tế
- **Định tuyến Load Balancer**: Định tuyến lưu lượng đến các instance EC2 backend

DNS chỉ phản hồi các truy vấn DNS, giúp client biết nên sử dụng endpoint nào. DNS chuyển đổi tên máy chủ thành các endpoint thực tế mà client có thể sử dụng cho các truy vấn HTTP.

## Các Loại Chính Sách Định Tuyến Route 53

Route 53 hỗ trợ các chính sách định tuyến sau:

1. **Simple (Đơn giản)**
2. **Weighted (Có trọng số)**
3. **Failover (Chuyển đổi dự phòng)**
4. **Latency-based (Dựa trên độ trễ)**
5. **Geolocation (Vị trí địa lý)**
6. **Multi-value answer (Đa giá trị)**
7. **Geoproximity (Địa lý gần)**

## Chính Sách Định Tuyến Đơn Giản (Simple Routing Policy)

### Tổng Quan

Chính sách định tuyến Simple được sử dụng để định tuyến lưu lượng đến một tài nguyên duy nhất, mặc dù nó có thể chỉ định nhiều giá trị trong cùng một bản ghi.

### Đặc Điểm Chính

- **Mục Tiêu Tài Nguyên Đơn**: Thường định tuyến đến một tài nguyên
- **Nhiều Giá Trị**: Có thể chỉ định nhiều giá trị trong cùng một bản ghi
- **Lựa Chọn Ngẫu Nhiên**: Nếu nhiều giá trị được trả về, client sẽ chọn ngẫu nhiên một giá trị
- **Bản Ghi Alias**: Chỉ có thể chỉ định một tài nguyên AWS làm mục tiêu khi sử dụng bản ghi alias
- **Không Có Health Check**: Không thể kết hợp với health check

### Cách Hoạt Động

**Ví dụ Giá Trị Đơn:**
```
Client → foo.example.com
Route 53 → Trả về địa chỉ IP đơn (bản ghi A)
```

**Ví dụ Nhiều Giá Trị:**
```
Client → foo.example.com
Route 53 → Trả về ba địa chỉ IP được nhúng trong bản ghi A
Client → Chọn ngẫu nhiên một địa chỉ IP
```

## Hướng Dẫn Thực Hành

### Tạo Bản Ghi Simple Routing Policy

1. **Tạo bản ghi:**
   - Tên bản ghi: `simple.stephanetheteacher.com`
   - Loại bản ghi: A record
   - Giá trị: IP instance trong `ap-southeast-1`
   - TTL: 20 giây
   - Chính sách định tuyến: Simple

2. **Kiểm tra bản ghi:**
   - Truy cập `simple.stephanetheteacher.com`
   - Kết quả: "Hello World from my instance in ap-southeast-1b"

3. **Xác minh bằng lệnh dig:**
   ```bash
   sudo yum install bind-utils
   dig simple.stephanetheteacher.com
   ```
   - Hiển thị bản ghi A với TTL 20 giây trỏ đến IP

### Thêm Nhiều IP Vào Bản Ghi Simple

1. **Chỉnh sửa bản ghi:**
   - Thêm nhiều địa chỉ IP:
     - Một địa chỉ trong `ap-southeast-1`
     - Một địa chỉ trong `us-east-1`
   
2. **Lưu và đợi TTL hết hạn** (20 giây)

3. **Xác minh bằng CloudShell:**
   ```bash
   dig simple.stephanetheteacher.com
   ```
   - Trả về hai địa chỉ IP trong phản hồi
   - Lựa chọn phía client quyết định sử dụng IP nào

4. **Kiểm tra hành vi:**
   - Làm mới trang web
   - Cơ hội ngẫu nhiên (50/50) để kết nối đến một trong hai vùng
   - Sau khi TTL hết hạn, có thể kết nối đến vùng khác
   - Ví dụ: Lần đầu kết nối đến `ap-southeast-1b`, sau đó đến `us-east-1a`

## Kết Luận

Chính sách định tuyến Simple thể hiện chức năng bản ghi DNS cơ bản với:
- Cấu hình dễ dàng
- Hỗ trợ nhiều giá trị
- Lựa chọn ngẫu nhiên phía client
- Không tích hợp health check

Đây là nền tảng để hiểu các chính sách định tuyến Route 53 phức tạp hơn.