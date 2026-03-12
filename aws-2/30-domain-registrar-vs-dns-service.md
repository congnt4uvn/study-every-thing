# Domain Registrar vs DNS Service (Nhà Đăng Ký Tên Miền vs Dịch Vụ DNS)

## Tổng Quan

Khi làm việc với tên miền và DNS trong AWS, điều quan trọng là phải hiểu được sự khác biệt giữa nhà đăng ký tên miền (domain registrar) và dịch vụ DNS (DNS service). Mặc dù các dịch vụ này thường được gói chung với nhau, nhưng chúng phục vụ các mục đích khác nhau và có thể được sử dụng độc lập.

## Nhà Đăng Ký Tên Miền (Domain Registrar)

Nhà đăng ký tên miền là dịch vụ nơi bạn mua và đăng ký tên miền của mình. Các điểm chính:

- Bạn phải trả phí hàng năm để duy trì quyền sở hữu tên miền
- Ví dụ về các nhà đăng ký tên miền phổ biến:
  - Amazon Registrar (thông qua console Route 53)
  - GoDaddy
  - Google Domains
  - Và nhiều nhà cung cấp khác

Hầu hết các nhà đăng ký tên miền đều bao gồm dịch vụ DNS để quản lý các bản ghi DNS của bạn như một phần trong gói dịch vụ.

## Dịch Vụ DNS (DNS Service)

Dịch vụ DNS quản lý các bản ghi DNS của bạn và xử lý các truy vấn DNS cho tên miền. Điều quan trọng cần hiểu là **bạn không bị ràng buộc phải sử dụng dịch vụ DNS do nhà đăng ký tên miền cung cấp**.

### Tính Linh Hoạt Trong Việc Lựa Chọn Dịch Vụ

Bạn có toàn quyền linh hoạt để kết hợp các nhà đăng ký tên miền và dịch vụ DNS:

1. **Tùy chọn 1**: Đăng ký tên miền với Amazon Registrar + Sử dụng Route 53 cho DNS
   - Đây là cấu hình mặc định khi đăng ký thông qua AWS

2. **Tùy chọn 2**: Đăng ký tên miền với Amazon Registrar + Sử dụng dịch vụ DNS của bên thứ ba
   - Bạn có thể chọn không sử dụng Route 53 để quản lý DNS

3. **Tùy chọn 3**: Đăng ký tên miền với nhà đăng ký bên thứ ba (ví dụ: GoDaddy) + Sử dụng Route 53 cho DNS
   - Đây là một cấu hình hoàn toàn chấp nhận được và phổ biến

## Cách Sử Dụng Route 53 với Nhà Đăng Ký Bên Thứ Ba

Nếu bạn đã mua tên miền từ nhà đăng ký bên thứ ba nhưng muốn sử dụng Amazon Route 53 làm dịch vụ DNS, hãy làm theo các bước sau:

### Bước 1: Tạo Public Hosted Zone trong Route 53

1. Truy cập vào console Amazon Route 53
2. Tạo một public hosted zone cho tên miền của bạn
3. Trong chi tiết hosted zone, tìm phần **name servers** ở phía bên phải
4. Bạn sẽ thấy bốn địa chỉ name server (ví dụ: ns-xxx.awsdns-xx.com)

### Bước 2: Cập Nhật Name Servers trên Nhà Đăng Ký Tên Miền

1. Đăng nhập vào website của nhà đăng ký tên miền (ví dụ: GoDaddy)
2. Tìm cài đặt tên miền của bạn
3. Tìm tùy chọn "Name Servers" hoặc "Custom Name Servers"
4. Thay thế các name server mặc định bằng bốn name server của Route 53 từ Bước 1

### Cách Hoạt Động

Sau khi cấu hình:
1. Khi một truy vấn DNS được thực hiện cho tên miền của bạn, nó sẽ đến nhà đăng ký tên miền trước
2. Nhà đăng ký phản hồi với thông tin name server (hiện đang trỏ đến Route 53)
3. Truy vấn sau đó được chuyển đến các name server của Amazon Route 53
4. Route 53 quản lý tất cả các bản ghi DNS và phản hồi các truy vấn từ console của nó

## Tóm Tắt

- **Domain Registrar (Nhà Đăng Ký Tên Miền)**: Nơi bạn mua và đăng ký tên miền
- **DNS Service (Dịch Vụ DNS)**: Nơi bạn quản lý các bản ghi DNS và xử lý truy vấn DNS
- **Điểm Chính**: Các dịch vụ này độc lập và có thể được sử dụng riêng biệt
- Bạn có thể mua tên miền từ bất kỳ nhà đăng ký nào và vẫn sử dụng Route 53 làm nhà cung cấp dịch vụ DNS
- Để sử dụng Route 53 với tên miền của bên thứ ba:
  1. Tạo một public hosted zone trong Route 53
  2. Cập nhật các bản ghi NS (name server) trên website của nhà đăng ký bên thứ ba
  3. Trỏ chúng đến các name server của Route 53

Tính linh hoạt này cho phép bạn tận dụng các tính năng DNS mạnh mẽ của AWS Route 53 bất kể bạn mua tên miền ở đâu.