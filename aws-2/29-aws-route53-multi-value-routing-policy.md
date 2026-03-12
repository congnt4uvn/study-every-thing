# Chính Sách Định Tuyến Multi-Value của AWS Route 53

## Tổng Quan

Chính sách định tuyến Multi-Value là chính sách định tuyến cuối cùng trong AWS Route 53, được thiết kế để định tuyến lưu lượng đến nhiều tài nguyên. Route 53 trả về nhiều giá trị hoặc tài nguyên để phản hồi các truy vấn DNS, cung cấp một hình thức cân bằng tải phía client.

## Tính Năng Chính

### Định Tuyến Nhiều Tài Nguyên
- Định tuyến lưu lượng đến nhiều tài nguyên đồng thời
- Trả về nhiều giá trị để phản hồi truy vấn DNS
- Cho phép cân bằng tải phía client

### Tích Hợp Health Check
- Có thể được liên kết với Health Checks (Kiểm tra sức khỏe)
- Chỉ trả về các tài nguyên vượt qua kiểm tra sức khỏe
- Tối đa **8 bản ghi khỏe mạnh** được trả về cho mỗi truy vấn Multi-Value

### So Sánh với ELB
- Mặc dù trông tương tự như Elastic Load Balancer (ELB), nhưng **không phải là thay thế**
- Cung cấp cân bằng tải phía client thay vì cân bằng tải phía server
- Client nhận nhiều bản ghi và chọn bản ghi nào để sử dụng

## Cách Hoạt Động

### Quy Trình Truy Vấn
1. Nhiều A Records được thiết lập cho một tên miền (ví dụ: example.com)
2. Mỗi bản ghi được liên kết với một Health Check
3. Khi client thực hiện truy vấn Multi-Value, họ nhận được tối đa 8 bản ghi
4. Client sau đó chọn một trong các bản ghi được trả về
5. Tất cả các bản ghi được trả về đều được đảm bảo là khỏe mạnh

### Ưu Điểm So Với Simple Routing
Chính sách định tuyến Multi-Value khác với Simple routing theo những cách quan trọng:

- **Chính Sách Simple Routing**:
  - Không cho phép Health Checks
  - Có thể trả về tài nguyên không khỏe mạnh
  - Không có xác thực sức khỏe

- **Chính Sách Multi-Value Routing**:
  - Hỗ trợ Health Checks
  - Chỉ trả về tài nguyên khỏe mạnh
  - Đáng tin cậy và an toàn hơn cho client

## Hướng Dẫn Thực Hành

### Tạo Các Bản Ghi Multi-Value

#### Bản Ghi 1: Khu Vực Đông Mỹ
```
Tên Bản Ghi: multi.example.com
Giá Trị: Địa chỉ IP cho us-east-1
Chính Sách Định Tuyến: Multivalue
Health Check: us-east-1
ID Bản Ghi: US
TTL: 60 giây
```

#### Bản Ghi 2: Khu Vực Châu Á Thái Bình Dương
```
Tên Bản Ghi: multi.example.com
Giá Trị: Địa chỉ IP cho ap-southeast-1
Chính Sách Định Tuyến: Multivalue answer
Health Check: ap-southeast-1
ID Bản Ghi: Asia
TTL: 60 giây (1 phút)
```

#### Bản Ghi 3: Khu Vực Châu Âu
```
Tên Bản Ghi: multi.example.com
Giá Trị: Địa chỉ IP cho eu-central-1
Chính Sách Định Tuyến: Multivalue answer
Health Check: eu-central-1
ID Bản Ghi: EU
TTL: 60 giây (1 phút)
```

### Kiểm Tra Cấu Hình

#### Kiểm Tra 1: Tất Cả Health Checks Đều Khỏe Mạnh
Sử dụng AWS CloudShell, chạy lệnh `dig` để truy vấn bản ghi:

```bash
dig multi.example.com
```

**Kết Quả**: Ba địa chỉ IP được trả về vì cả ba health checks đều khỏe mạnh.

#### Kiểm Tra 2: Mô Phỏng Instance Không Khỏe Mạnh
1. Chỉnh sửa health check eu-central-1
2. Bật "Invert health status" (Đảo ngược trạng thái sức khỏe) để làm cho nó không khỏe mạnh
3. Chạy lại lệnh `dig`

**Kết Quả**: Chỉ có hai địa chỉ IP được trả về. Chính sách định tuyến Multi-Value đã lọc thành công tài nguyên không khỏe mạnh.

#### Kiểm Tra 3: Hoàn Nguyên Health Check
1. Chỉnh sửa lại health check eu-central-1
2. Tắt "Invert health check status"
3. Health check quay trở lại trạng thái khỏe mạnh

**Kết Quả**: Cả ba địa chỉ IP được trả về lại như ban đầu.

## Lợi Ích

1. **Tính Khả Dụng Cao**: Tự động loại trừ các tài nguyên không khỏe mạnh
2. **Phân Phối Tải Phía Client**: Client nhận nhiều tùy chọn và chọn tùy chọn nào để sử dụng
3. **Triển Khai Đơn Giản**: Dễ thiết lập so với các giải pháp cân bằng tải phức tạp hơn
4. **Tiết Kiệm Chi Phí**: Không cần cơ sở hạ tầng bổ sung ngoài Route 53 và health checks
5. **Linh Hoạt**: Có thể trả về tối đa 8 bản ghi khỏe mạnh cho mỗi truy vấn

## Thực Hành Tốt Nhất

- Luôn liên kết các bản ghi Multi-Value với Health Checks
- Đặt giá trị TTL phù hợp dựa trên nhu cầu của bạn (thường là 60 giây hoặc 1 phút)
- Sử dụng các Record ID có ý nghĩa để xác định các tài nguyên khác nhau
- Giám sát trạng thái health check thường xuyên
- Xem xét phân phối địa lý của tài nguyên để có hiệu suất tốt hơn

## Trường Hợp Sử Dụng

- Phân phối lưu lượng truy cập trên nhiều web server
- Cung cấp dự phòng cho các dịch vụ quan trọng
- Triển khai cân bằng tải đơn giản mà không cần cơ sở hạ tầng bổ sung
- Tạo các ứng dụng có tính khả dụng cao với chuyển đổi dự phòng tự động

## Kết Luận

Chính sách định tuyến Multi-Value cung cấp một cách mạnh mẽ để nâng cao tính khả dụng và độ tin cậy của ứng dụng bằng cách kết hợp phân phối lưu lượng dựa trên DNS với kiểm tra sức khỏe. Mặc dù không phải là sự thay thế cho một load balancer đầy đủ, nó cung cấp một giải pháp đơn giản và hiệu quả cho nhiều trường hợp sử dụng nơi cân bằng tải phía client là chấp nhận được.