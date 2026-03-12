# AWS SSL/TLS Certificates trên Load Balancers

## Tổng quan

Hướng dẫn này giải thích cách kích hoạt chứng chỉ SSL/TLS trên AWS Application Load Balancer (ALB) và Network Load Balancer (NLB) để bảo mật ứng dụng của bạn với giao thức HTTPS/TLS.

## Kích hoạt Chứng chỉ SSL trên Application Load Balancer (ALB)

### Thêm HTTPS Listener

Để kích hoạt chứng chỉ SSL trên ALB, bạn cần thêm một listener với cấu hình sau:

1. **Thêm listener mới**
   - Giao thức: `HTTPS`
   - Cổng: `443` (cổng HTTPS mặc định)

2. **Cấu hình định tuyến**
   - Khi client sử dụng cổng 443 với giao thức HTTPS
   - Chuyển tiếp lưu lượng đến target group cụ thể

### Cài đặt Secure Listener

#### Chính sách Bảo mật SSL
- Thiết lập chính sách bảo mật SSL để xác định cách thương lượng chứng chỉ
- Cấu hình dựa trên yêu cầu tương thích với các phiên bản SSL/TLS cũ hơn
- Cài đặt mặc định phù hợp với hầu hết các trường hợp sử dụng

#### Các tùy chọn vị trí Chứng chỉ

Bạn có ba tùy chọn để cung cấp chứng chỉ SSL/TLS:

1. **AWS Certificate Manager (ACM)** - Được khuyến nghị
   - Quản lý chứng chỉ tập trung
   - Gia hạn tự động
   - Chứng chỉ SSL/TLS miễn phí cho tài nguyên AWS

2. **IAM Certificate Store**
   - Không được khuyến nghị làm phương pháp chính
   - Tùy chọn cũ để lưu trữ chứng chỉ

3. **Import Chứng chỉ Thủ công**
   - Dán private key
   - Dán certificate body
   - Dán certificate chain (nếu cần)
   - Chứng chỉ sẽ được import trực tiếp vào ACM

## Kích hoạt Chứng chỉ TLS trên Network Load Balancer (NLB)

### Thêm TLS Listener

Quy trình cho NLB tương tự như ALB:

1. **Điều hướng đến NLB listeners**
   - Thêm listener mới
   - Giao thức: `TLS`

2. **Cấu hình định tuyến**
   - Chuyển tiếp đến target group

3. **Chính sách Bảo mật**
   - Chọn chính sách bảo mật phù hợp
   - Các tùy chọn tương tự như ALB

4. **Cấu hình Chứng chỉ**
   - Chọn nguồn chứng chỉ: ACM, IAM, hoặc Import
   - Cấu hình Application Layer Protocol Negotiation (ALPN)
   - ALPN là cài đặt TLS nâng cao cho thương lượng giao thức

## Sự khác biệt chính

| Tính năng | ALB | NLB |
|-----------|-----|-----|
| Giao thức | HTTPS | TLS |
| Cổng mặc định | 443 | 443 |
| Hỗ trợ ALPN | Không | Có |
| Lớp | Layer 7 | Layer 4 |

## Best Practices (Thực hành tốt nhất)

1. **Sử dụng AWS Certificate Manager (ACM)**
   - Đơn giản hóa quản lý chứng chỉ
   - Gia hạn tự động
   - Không tốn thêm chi phí

2. **Chọn chính sách bảo mật phù hợp**
   - Cân bằng giữa bảo mật và khả năng tương thích
   - Thường xuyên cập nhật lên các phiên bản TLS mới hơn

3. **Lên kế hoạch cho việc xoay vòng chứng chỉ**
   - Thiết lập cảnh báo trước khi hết hạn
   - Sử dụng ACM để gia hạn tự động

## Tóm tắt

Chứng chỉ SSL/TLS trên AWS load balancers cung cấp kết nối mã hóa giữa client và ứng dụng của bạn. Cả ALB và NLB đều hỗ trợ cấu hình chứng chỉ thông qua ACM, IAM, hoặc import thủ công, với ACM là phương pháp được khuyến nghị cho việc quản lý dễ dàng và gia hạn tự động.