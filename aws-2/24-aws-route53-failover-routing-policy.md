# AWS Route 53 - Chính Sách Định Tuyến Failover

## Tổng Quan

Chính sách định tuyến failover trong Amazon Route 53 cho phép bạn tạo cấu hình chuyển đổi dự phòng chủ động-bị động (active-passive) cho các ứng dụng của mình. Chính sách định tuyến này cho phép Route 53 tự động chuyển hướng lưu lượng từ tài nguyên chính không khỏe mạnh sang tài nguyên phụ (khôi phục thảm họa) còn hoạt động tốt.

## Kiến Trúc

Chính sách định tuyến failover bao gồm các thành phần sau:

- **Route 53**: Dịch vụ DNS ở giữa quản lý định tuyến lưu lượng
- **EC2 Instance Chính**: Tài nguyên chính xử lý lưu lượng trong điều kiện bình thường
- **EC2 Instance Phụ**: Instance khôi phục thảm họa tiếp quản khi instance chính gặp sự cố

## Cách Hoạt Động

1. **Cấu Hình Bản Ghi Chính**: Bản ghi chính phải được liên kết với health check (bắt buộc)
2. **Giám Sát Sức Khỏe**: Route 53 liên tục giám sát trạng thái health check
3. **Failover Tự Động**: Khi health check trở nên không khỏe mạnh, Route 53 tự động chuyển sang EC2 instance phụ
4. **Phản Hồi DNS**: Route 53 trả về bản ghi phù hợp dựa trên trạng thái sức khỏe

### Đặc Điểm Chính

- **Chỉ Hai Bản Ghi**: Chỉ có thể có một bản ghi chính và một bản ghi phụ
- **Health Check Bắt Buộc**: Bản ghi chính phải có health check được liên kết
- **Health Check Phụ Tùy Chọn**: Bản ghi phụ có thể tùy chọn có health check
- **Hành Vi Client**: Clients tự động nhận địa chỉ IP của tài nguyên khỏe mạnh

## Hướng Dẫn Thực Hành

### Bước 1: Tạo Bản Ghi Failover Chính

1. Điều hướng đến hosted zone của bạn trong Route 53
2. Tạo bản ghi mới với các thiết lập sau:
   - **Tên bản ghi**: `failover.stephanetheteacher.com`
   - **Loại bản ghi**: A record
   - **Giá trị**: Địa chỉ IP của instance EU-central-1
   - **Chính sách định tuyến**: Failover
   - **TTL**: 60 giây (đặt thấp để failover nhanh)
   - **Loại bản ghi failover**: Primary (Chính)
   - **Health check**: Liên kết với health check EU-central-1 (bắt buộc)
   - **Record ID**: E

### Bước 2: Tạo Bản Ghi Failover Phụ

1. Thêm bản ghi mới với cùng tên bản ghi
2. Cấu hình bản ghi phụ:
   - **Tên bản ghi**: `failover.stephanetheteacher.com`
   - **Loại bản ghi**: A record
   - **Giá trị**: Địa chỉ IP của instance US-east-1
   - **Chính sách định tuyến**: Failover
   - **TTL**: 60 giây
   - **Loại bản ghi failover**: Secondary (Phụ)
   - **Health check**: Tùy chọn (health check US-East-1)
   - **Record ID**: US

3. Tạo bản ghi - nó sẽ được tạo thành công

### Bước 3: Kiểm Tra Failover

#### Trạng Thái Ban Đầu
1. Kiểm tra xem cả hai health check đều khỏe mạnh
2. Truy cập vào `failover.stephanetheteacher.com`
3. Xác minh bạn nhận được phản hồi từ EU-central-1c (chính)

#### Kích Hoạt Failover
1. Đi đến vùng EU-central-1
2. Tìm EC2 instance của bạn và xác định security group của nó
3. Chỉnh sửa inbound rules
4. Xóa HTTP rule trên port 80
5. Điều này làm cho instance không thể truy cập được bởi health checkers

#### Giám Sát Failover
1. Chờ health check trở nên không khỏe mạnh
2. Làm mới trạng thái health check trong Route 53
3. Health check EU-central-1 sẽ hiển thị là không khỏe mạnh
4. Kiểm tra tab monitoring để xem khi nào nó trở nên không khỏe mạnh
5. Quan sát phần trăm health checker giảm từ dương xuống không

#### Xác Minh Failover Thành Công
1. Làm mới trình duyệt của bạn tại `failover.stephanetheteacher.com`
2. Bây giờ bạn sẽ nhận được phản hồi từ US-east-1 (phụ)
3. Failover đã hoạt động một cách liền mạch ở hậu trường

### Bước 4: Khôi Phục Dịch Vụ Chính

1. Quay lại security group EU-central-1
2. Chỉnh sửa inbound rules
3. Thêm lại HTTP rule
4. Health check sẽ tự động pass lại
5. Route 53 sẽ failover trở lại vị trí chính

## Những Điểm Chính

- Chính sách định tuyến failover cung cấp khôi phục thảm họa tự động
- Bản ghi chính yêu cầu health check bắt buộc
- Chỉ tồn tại hai tùy chọn failover: chính và phụ
- Giá trị TTL thấp cho phép phản hồi failover nhanh hơn
- Failover xảy ra tự động khi health check thất bại
- Khôi phục dịch vụ là tự động khi health check pass lại

## Trường Hợp Sử Dụng

- **Khôi Phục Thảm Họa**: Duy trì tính liên tục của doanh nghiệp trong trường hợp tài nguyên chính gặp sự cố
- **Tính Khả Dụng Cao**: Đảm bảo ứng dụng của bạn luôn có thể truy cập được
- **Kiến Trúc Chủ Động-Bị Động**: Giải pháp failover hiệu quả về chi phí cho các ứng dụng quan trọng

---

*Hướng dẫn này trình bày chính sách định tuyến failover của AWS Route 53, cho phép chuyển hướng lưu lượng tự động cho các tình huống tính khả dụng cao và khôi phục thảm họa.*