# Chứng Chỉ SSL/TLS và Server Name Indication (SNI) trên AWS

## Giới Thiệu

Hướng dẫn này cung cấp tổng quan về chứng chỉ SSL/TLS và cách tích hợp chúng với AWS Load Balancers, bao gồm khái niệm quan trọng về Server Name Indication (SNI).

## Tổng Quan về Chứng Chỉ SSL/TLS

### Chứng Chỉ SSL/TLS là gì?

Chứng chỉ SSL cho phép lưu lượng giữa khách hàng và load balancer của bạn được mã hóa trong khi truyền tải. Đây được gọi là **mã hóa trong quá trình truyền tải** (in-flight encryption), nghĩa là dữ liệu khi đi qua mạng sẽ được mã hóa và chỉ có thể được giải mã bởi người gửi và người nhận.

### SSL và TLS

- **SSL** (Secure Sockets Layer): Giao thức ban đầu được sử dụng để mã hóa kết nối truyền tải
- **TLS** (Transport Layer Security): Phiên bản mới hơn của SSL

**Lưu ý:** Mặc dù chứng chỉ TLS là loại chứng chỉ chủ yếu được sử dụng ngày nay, mọi người thường vẫn gọi chúng là "chứng chỉ SSL" để đơn giản hóa và vì lý do lịch sử.

### Certificate Authorities (CAs) - Tổ Chức Cấp Chứng Chỉ

Chứng chỉ SSL công khai được cấp bởi các Certificate Authorities, bao gồm:
- Comodo
- Symantec
- GoDaddy
- GlobalSign
- Digicert
- Let's Encrypt

### Thuộc Tính của Chứng Chỉ

- Chứng chỉ SSL có ngày hết hạn và phải được gia hạn thường xuyên để đảm bảo tính xác thực
- Khi bạn truy cập một trang web có mã hóa SSL/TLS đúng cách, bạn sẽ thấy biểu tượng khóa trên trình duyệt
- Nếu không có mã hóa, trình duyệt sẽ hiển thị cảnh báo khuyên bạn không nên nhập thông tin nhạy cảm

## SSL/TLS với AWS Load Balancers

### Cách Hoạt Động

1. **Kết Nối từ Client**: Người dùng kết nối qua HTTPS (được mã hóa bằng chứng chỉ SSL) thông qua internet công cộng đến load balancer của bạn
2. **SSL Certificate Termination**: Load balancer xử lý việc kết thúc chứng chỉ SSL
3. **Giao Tiếp Backend**: Load balancer có thể giao tiếp với các EC2 instances sử dụng HTTP (không mã hóa) qua VPC, đây là mạng lưu lượng riêng tư

### Chứng Chỉ X.509

Load balancer tải chứng chỉ X.509 (chứng chỉ server SSL/TLS). Bạn có thể:
- Quản lý chứng chỉ SSL trong AWS bằng **ACM** (AWS Certificate Manager)
- Tải lên chứng chỉ của riêng bạn vào ACM

### Cấu Hình HTTPS Listener

Khi thiết lập HTTPS listener:
- Bạn phải chỉ định một **chứng chỉ mặc định**
- Bạn có thể thêm danh sách chứng chỉ tùy chọn để hỗ trợ nhiều tên miền
- Các client có thể sử dụng **SNI** (Server Name Indication) để chỉ định hostname mà họ muốn truy cập
- Bạn có thể đặt các chính sách bảo mật cụ thể để hỗ trợ các phiên bản SSL/TLS cũ hơn (legacy clients)

## Server Name Indication (SNI)

### SNI Giải Quyết Vấn Đề Gì?

SNI giải quyết vấn đề tải nhiều chứng chỉ SSL lên một web server để phục vụ nhiều trang web.

### SNI Hoạt Động Như Thế Nào?

1. SNI là một giao thức mới hơn yêu cầu client chỉ định hostname của server đích trong quá trình bắt tay SSL ban đầu
2. Client nói rằng, "Tôi muốn kết nối đến trang web này"
3. Server biết chứng chỉ nào cần tải dựa trên thông tin này

### Khả Năng Tương Thích của SNI

**Được Hỗ Trợ:**
- Application Load Balancer (ALB)
- Network Load Balancer (NLB)
- CloudFront

**Không Được Hỗ Trợ:**
- Classic Load Balancer (thế hệ cũ)

**Điểm Chính:** Khi bạn thấy nhiều chứng chỉ SSL trên load balancer, hãy nghĩ đến ALB hoặc NLB.

### Ví Dụ Sơ Đồ SNI

Xem xét một ALB với hai target groups:
- **www.mycorp.com**
- **Domain1.example.com**

Quy trình:
1. ALB có hai chứng chỉ SSL (một cho mỗi tên miền)
2. Client kết nối đến ALB và yêu cầu "www.mycorp.com" (sử dụng SNI)
3. ALB xác định hostname được yêu cầu và sử dụng chứng chỉ SSL đúng
4. ALB mã hóa lưu lượng và định tuyến đến target group chính xác (mycorp.com)
5. Nếu một client khác yêu cầu "Domain1.example.com", ALB sử dụng chứng chỉ thích hợp và định tuyến đến target group đó

Sử dụng SNI, bạn có thể có nhiều target groups cho các trang web khác nhau sử dụng các chứng chỉ SSL khác nhau.

## Hỗ Trợ Chứng Chỉ SSL theo Loại Load Balancer

### Classic Load Balancer (CLB)
- **Hỗ trợ:** Chỉ một chứng chỉ SSL
- **Nhiều Hostnames:** Sử dụng nhiều Classic Load Balancers

### Application Load Balancer (ALB v2)
- **Hỗ trợ:** Nhiều listeners với nhiều chứng chỉ SSL
- **Công nghệ:** Sử dụng SNI để hoạt động

### Network Load Balancer (NLB)
- **Hỗ trợ:** Nhiều listeners với nhiều chứng chỉ SSL
- **Công nghệ:** Sử dụng SNI để hoạt động

## Tóm Tắt

- Chứng chỉ SSL/TLS mã hóa lưu lượng giữa clients và load balancers
- Các load balancers AWS hiện đại (ALB và NLB) hỗ trợ nhiều chứng chỉ SSL thông qua SNI
- SNI cho phép một load balancer phục vụ nhiều trang web với các chứng chỉ SSL khác nhau
- Luôn quản lý và gia hạn chứng chỉ của bạn thường xuyên để đảm bảo bảo mật
- Sử dụng AWS Certificate Manager (ACM) để đơn giản hóa việc quản lý chứng chỉ