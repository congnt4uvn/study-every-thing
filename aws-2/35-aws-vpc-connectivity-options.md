# Các Tùy Chọn Kết Nối AWS VPC

## Tổng Quan

Hướng dẫn này bao gồm các phương pháp khác nhau để thiết lập kết nối giữa các VPC và các cấu trúc mạng khác trong AWS, bao gồm VPC peering, VPC endpoints và kết nối đến các trung tâm dữ liệu on-premises.

## VPC Peering

### VPC Peering Là Gì?

VPC peering cho phép bạn kết nối hai Virtual Private Cloud (VPC) một cách riêng tư bằng cách sử dụng cơ sở hạ tầng mạng của AWS. Kết nối này làm cho các VPC hoạt động như thể chúng là một phần của cùng một mạng.

### Đặc Điểm Chính

- **Kết Nối Riêng Tư**: Các VPC kết nối sử dụng mạng riêng của AWS
- **Đa Tài Khoản & Đa Vùng**: Hoạt động giữa các tài khoản AWS hoặc vùng khác nhau
- **Dải IP Không Trùng Lặp**: Các dải địa chỉ IP của các VPC được peering không được trùng lặp
- **Không Bắc Cầu**: Kết nối peering chỉ trực tiếp - nếu VPC A peer với VPC B, và VPC A peer với VPC C, thì VPC B và VPC C không thể giao tiếp với nhau nếu không có kết nối peering riêng của chúng

### Ví Dụ Tình Huống

```
VPC A ←→ VPC B (Kết nối Peering)
VPC A ←→ VPC C (Kết nối Peering)
VPC B ← X → VPC C (Không có kết nối - không bắc cầu)
```

Để cho phép giao tiếp giữa VPC B và VPC C, bạn phải tạo một kết nối peering riêng biệt giữa chúng.

## VPC Endpoints

### Mục Đích

VPC endpoints cho phép bạn kết nối với các dịch vụ AWS bằng mạng riêng thay vì internet công cộng. Điều này cung cấp:

- **Bảo Mật Nâng Cao**: Lưu lượng truy cập ở trong mạng AWS
- **Độ Trễ Thấp Hơn**: Kết nối riêng trực tiếp đến các dịch vụ AWS
- **Truy Cập Riêng Tư**: Không cần internet gateway hoặc thiết bị NAT

### Các Loại VPC Endpoints

#### 1. VPC Endpoint Gateway

- **Dịch Vụ Được Hỗ Trợ**: Chỉ Amazon S3 và DynamoDB
- **Trường Hợp Sử Dụng**: Truy cập riêng tư đến S3 và DynamoDB từ các subnet riêng
- **Luồng Lưu Lượng**: Không đi qua internet

#### 2. VPC Endpoint Interface

- **Dịch Vụ Được Hỗ Trợ**: Hầu hết các dịch vụ AWS khác (ví dụ: CloudWatch)
- **Triển Khai**: Sử dụng Elastic Network Interface (ENI) trong VPC của bạn
- **Trường Hợp Sử Dụng**: Truy cập riêng tư đến các dịch vụ AWS từ bên trong các subnet riêng của bạn

### Kiến Trúc Ví Dụ

```
Subnet Riêng Tư
    └── EC2 Instance
        ├── VPC Endpoint Gateway → S3 & DynamoDB
        └── VPC Endpoint Interface → CloudWatch
```

## Kết Nối Đến Trung Tâm Dữ Liệu On-Premises

### Site-to-Site VPN

#### Tổng Quan

Site-to-Site VPN kết nối thiết bị VPN on-premises của bạn với AWS qua một kết nối được mã hóa.

#### Tính Năng Chính

- **Loại Kết Nối**: Đường hầm được mã hóa qua internet công cộng
- **Thời Gian Thiết Lập**: Thiết lập nhanh (vài phút)
- **Chi Phí**: Tùy chọn chi phí thấp hơn
- **Bảo Mật**: Tự động được mã hóa

#### Trường Hợp Sử Dụng

- Yêu cầu kết nối nhanh chóng
- Triển khai nhạy cảm về chi phí
- Môi trường thử nghiệm và phát triển

### AWS Direct Connect

#### Tổng Quan

Direct Connect thiết lập kết nối vật lý chuyên dụng giữa trung tâm dữ liệu on-premises của bạn và AWS.

#### Tính Năng Chính

- **Loại Kết Nối**: Đường dây vật lý riêng
- **Mạng**: Không sử dụng internet công cộng
- **Hiệu Năng**: An toàn và nhanh chóng
- **Thời Gian Thiết Lập**: Ít nhất một tháng để thiết lập
- **Chi Phí**: Chi phí cao hơn nhưng hiệu năng tốt hơn

#### Trường Hợp Sử Dụng

- Khối lượng công việc sản xuất yêu cầu hiệu năng ổn định
- Yêu cầu băng thông cao
- Tuân thủ quy định yêu cầu kết nối riêng tư
- Yêu cầu độ trễ thấp

### So Sánh: VPN vs Direct Connect

| Tính Năng | Site-to-Site VPN | Direct Connect |
|-----------|------------------|----------------|
| Kết Nối | Internet công cộng (được mã hóa) | Mạng riêng |
| Thời Gian Thiết Lập | Vài phút | 1+ tháng |
| Chi Phí | Thấp hơn | Cao hơn |
| Hiệu Năng | Biến đổi | Ổn định, hiệu năng cao |
| Bảo Mật | Đường hầm được mã hóa | Kết nối riêng tư |

## Tóm Tắt

AWS cung cấp nhiều tùy chọn kết nối để đáp ứng các yêu cầu khác nhau:

- **VPC Peering**: Để kết nối các VPC với nhau một cách riêng tư
- **VPC Endpoints**: Để truy cập riêng tư đến các dịch vụ AWS từ bên trong VPC của bạn
- **Site-to-Site VPN**: Để kết nối nhanh, được mã hóa đến mạng on-premises
- **Direct Connect**: Để kết nối riêng tư chuyên dụng, hiệu năng cao đến mạng on-premises

Chọn tùy chọn phù hợp dựa trên yêu cầu của bạn về tốc độ, chi phí, bảo mật và hiệu năng.

## Mẹo Thi

- Nhớ rằng VPC peering **không bắc cầu**
- VPC endpoints cung cấp **truy cập riêng tư** đến các dịch vụ AWS
- **Gateway endpoints** chỉ dành cho S3 và DynamoDB
- Site-to-Site VPN sử dụng **internet công cộng** (nhưng được mã hóa)
- Direct Connect cung cấp **kết nối vật lý riêng tư**
- Khi được hỏi về kết nối riêng tư đến các dịch vụ AWS, hãy nghĩ đến **VPC endpoints**