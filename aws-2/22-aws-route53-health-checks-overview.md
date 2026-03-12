# Tổng Quan về Health Checks trong AWS Route 53

## Giới Thiệu

Health checks (kiểm tra sức khỏe) trong Route 53 là một cách mạnh mẽ để giám sát tình trạng hoạt động của chủ yếu là các tài nguyên công khai, với các tùy chọn có sẵn để giám sát cả các tài nguyên riêng tư. Chúng cho phép chuyển đổi dự phòng DNS tự động và đảm bảo tính khả dụng cao cho ứng dụng của bạn trên nhiều vùng.

## Trường Hợp Sử Dụng: Tính Khả Dụng Cao Đa Vùng

Xem xét một thiết lập đa vùng điển hình:
- Hai Load Balancer ở các vùng khác nhau (ví dụ: us-east-1 và eu-west-1)
- Cả hai đều là load balancer công khai với ứng dụng chạy phía sau
- Các bản ghi DNS của Route 53 định hướng người dùng đến load balancer gần nhất (sử dụng định tuyến dựa trên độ trễ)
- Health checks đảm bảo người dùng không bị định hướng đến các vùng không khỏe mạnh

Khi người dùng truy cập tên miền của bạn (ví dụ: mydomain.com), Route 53 chuyển hướng họ đến load balancer gần nhất và khỏe mạnh, cung cấp chuyển đổi dự phòng DNS tự động.

## Các Loại Health Checks

Route 53 hỗ trợ ba loại health checks:

### 1. Endpoint Health Checks (Kiểm Tra Điểm Cuối)

Giám sát một điểm cuối công khai như:
- Ứng dụng
- Máy chủ
- Tài nguyên AWS (ví dụ: Application Load Balancers)

**Cách hoạt động:**
- Khoảng 15 trình kiểm tra sức khỏe toàn cầu gửi yêu cầu từ khắp nơi trên thế giới
- Điểm cuối phải phản hồi với mã trạng thái 200 OK (hoặc mã bạn đã định nghĩa)
- Nếu hơn 18% trình kiểm tra báo cáo khỏe mạnh, Route 53 coi điểm cuối là khỏe mạnh

**Tùy chọn cấu hình:**
- **Khoảng thời gian**: 30 giây (tiêu chuẩn) hoặc 10 giây (kiểm tra nhanh - chi phí cao hơn)
- **Giao thức được hỗ trợ**: HTTP, HTTPS, TCP
- **Mã trạng thái**: Phải trả về mã trạng thái 2xx hoặc 3xx
- **Khớp văn bản**: Có thể kiểm tra 5.120 byte đầu tiên của phản hồi dựa trên văn bản để tìm nội dung cụ thể
- **Vị trí tùy chỉnh**: Chọn vị trí nào sử dụng cho health checks

**Yêu cầu mạng quan trọng:**
Các trình kiểm tra sức khỏe phải có khả năng truy cập các điểm cuối của bạn. Bạn phải cho phép các yêu cầu đến từ dải địa chỉ IP của trình kiểm tra sức khỏe Route 53 (có sẵn trong tài liệu AWS).

### 2. Calculated Health Checks (Kiểm Tra Sức Khỏe Được Tính Toán)

Kết hợp kết quả từ nhiều health checks thành một health check duy nhất.

**Cấu trúc:**
- **Child health checks (Kiểm tra con)**: Giám sát các tài nguyên riêng lẻ (ví dụ: ba EC2 instances)
- **Parent health check (Kiểm tra cha)**: Giám sát các child health checks

**Cấu hình:**
- **Toán tử logic**: Điều kiện OR, AND hoặc NOT
- **Dung lượng**: Giám sát tối đa 256 child health checks
- **Ngưỡng**: Chỉ định bao nhiêu child health checks phải vượt qua để parent vượt qua

**Trường hợp sử dụng:**
Thực hiện bảo trì trên trang web của bạn mà không gây ra tất cả các health checks thất bại bằng cách sử dụng calculated health checks với ngưỡng phù hợp.

### 3. CloudWatch Alarm Health Checks

Giám sát CloudWatch Alarms, đặc biệt hữu ích cho các tài nguyên riêng tư.

## Giám Sát Tài Nguyên Riêng Tư

**Thách thức:**
Các trình kiểm tra sức khỏe Route 53 hoạt động trên web công khai, bên ngoài VPC của bạn, vì vậy chúng không thể truy cập trực tiếp các điểm cuối riêng tư (VPC riêng hoặc tài nguyên on-premises).

**Giải pháp:**
Sử dụng tích hợp CloudWatch:

1. Tạo CloudWatch Metric để giám sát tài nguyên riêng tư của bạn (ví dụ: EC2 instance trong subnet riêng)
2. Tạo CloudWatch Alarm dựa trên metric đó
3. Tạo Route 53 health check để giám sát CloudWatch Alarm
4. Khi metric bị vi phạm và alarm chuyển sang trạng thái alarm, health check tự động trở nên không khỏe mạnh

Đây là cách tiếp cận phổ biến nhất để giám sát các tài nguyên riêng tư.

## Số Liệu Health Check

Tất cả các health checks đều có số liệu riêng có thể xem trong CloudWatch, cho phép bạn giám sát và phân tích trạng thái sức khỏe của tài nguyên theo thời gian.

## Những Điểm Chính Cần Nhớ

- Health checks cho phép chuyển đổi dự phòng DNS tự động để có tính khả dụng cao
- Ba loại: Giám sát điểm cuối, Calculated health checks, và giám sát CloudWatch Alarm
- Các trình kiểm tra sức khỏe toàn cầu (khoảng 15) xác minh tình trạng điểm cuối từ nhiều vị trí
- Ngưỡng 18% xác định trạng thái sức khỏe tổng thể
- Tích hợp CloudWatch cho phép giám sát các tài nguyên riêng tư
- Cấu hình security group phù hợp là cần thiết để cho phép truy cập trình kiểm tra sức khỏe
- Số liệu health check có sẵn trong CloudWatch để phân tích

## Thực Hành Tốt Nhất

1. Luôn cấu hình health checks khi sử dụng Route 53 cho triển khai đa vùng
2. Đảm bảo security groups và network ACLs cho phép lưu lượng từ dải IP của trình kiểm tra sức khỏe Route 53
3. Sử dụng calculated health checks cho các tình huống phức tạp với nhiều phụ thuộc
4. Tận dụng CloudWatch Alarms để giám sát tài nguyên riêng tư
5. Đặt khoảng thời gian kiểm tra sức khỏe phù hợp dựa trên yêu cầu khả dụng và ngân sách của bạn
6. Giám sát số liệu health check trong CloudWatch để xác định các mẫu và vấn đề tiềm ẩn