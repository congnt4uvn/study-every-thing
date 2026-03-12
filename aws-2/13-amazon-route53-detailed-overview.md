# Amazon Route 53 - Tổng Quan Chi Tiết

## Giới Thiệu về Amazon Route 53

Amazon Route 53 là một **dịch vụ DNS có tính ủy quyền, được quản lý hoàn toàn, có khả năng mở rộng cao và tính sẵn sàng cao**. Thuật ngữ "ủy quyền" (authoritative) có nghĩa là khách hàng có toàn quyền kiểm soát để cập nhật các bản ghi DNS theo nhu cầu.

### Cách Route 53 Hoạt Động

Quy trình làm việc điển hình như sau:

1. Khách hàng muốn truy cập EC2 Instance của bạn bằng tên miền như `example.com`
2. EC2 Instance của bạn chỉ có địa chỉ IP công khai
3. Bạn tạo các bản ghi DNS trong hosted zone của Amazon Route 53
4. Khi khách hàng yêu cầu `example.com`, Route 53 phản hồi với IP tương ứng (ví dụ: `54.22.33.44`)
5. Khách hàng sau đó có thể kết nối trực tiếp đến EC2 Instance của bạn

### Tính Năng Chính

- **Đăng Ký Tên Miền**: Route 53 có thể đăng ký các tên miền như `example.com`
- **Kiểm Tra Sức Khỏe**: Khả năng giám sát tình trạng của các tài nguyên
- **100% Availability SLA**: Dịch vụ AWS duy nhất cung cấp cam kết này
- **Nguồn Gốc Tên Gọi**: Được gọi là "Route 53" vì cổng 53 là cổng DNS truyền thống

## Bản Ghi DNS trong Route 53

Các bản ghi DNS xác định cách định tuyến lưu lượng đến một tên miền cụ thể. Mỗi bản ghi chứa:

- **Tên Miền/Tên Miền Phụ**: ví dụ: `example.com`
- **Loại Bản Ghi**: ví dụ: A hoặc AAAA
- **Giá Trị**: ví dụ: `12.34.56.78`
- **Chính Sách Định Tuyến**: Cách Route 53 phản hồi các truy vấn
- **TTL (Time To Live)**: Thời gian bản ghi được lưu cache tại DNS resolvers

### Các Loại Bản Ghi DNS Được Hỗ Trợ

Route 53 hỗ trợ nhiều loại bản ghi DNS:

#### Các Loại Bản Ghi Cần Biết (Quan Trọng Cho Kỳ Thi)
- **A** - Ánh xạ tên máy chủ đến IPv4
- **AAAA** - Ánh xạ tên máy chủ đến IPv6
- **CNAME** - Ánh xạ tên máy chủ đến tên máy chủ khác
- **NS** - Name servers cho hosted zone

#### Các Loại Bản Ghi Nâng Cao
Nhiều loại bản ghi khác có sẵn nhưng không bắt buộc cho mục đích thi.

## Giải Thích Chi Tiết Các Loại Bản Ghi DNS Quan Trọng

### Bản Ghi A
Ánh xạ tên máy chủ đến **địa chỉ IPv4**.

**Ví dụ**: `example.com` → `1.2.3.4`

### Bản Ghi AAAA
Ánh xạ tên máy chủ đến **địa chỉ IPv6**.

### Bản Ghi CNAME
Ánh xạ tên máy chủ đến tên máy chủ khác. Tên máy chủ đích có thể là bản ghi A hoặc AAAA.

**Hạn Chế Quan Trọng**:
- ❌ Không thể tạo bản ghi CNAME cho nút cấp cao nhất (Zone Apex)
- ❌ Không thể tạo CNAME cho `example.com`
- ✅ Có thể tạo CNAME cho `www.example.com`

### Bản Ghi NS (Name Server)
Chứa tên DNS hoặc địa chỉ IP của các máy chủ có thể phản hồi các truy vấn DNS cho hosted zone của bạn. Kiểm soát cách lưu lượng được định tuyến đến một tên miền.

## Hosted Zones (Vùng Lưu Trữ)

**Hosted zones** là các container chứa các bản ghi định nghĩa cách định tuyến lưu lượng đến tên miền và các tên miền phụ.

### Các Loại Hosted Zones

#### 1. Public Hosted Zones (Vùng Công Khai)
- Phản hồi các truy vấn từ khách hàng công khai (bất kỳ ai trên internet)
- Được sử dụng cho các tên miền có thể truy cập công khai
- Ví dụ: `application1.mypublicdomain.com`

#### 2. Private Hosted Zones (Vùng Riêng Tư)
- Chỉ có thể truy cập trong Virtual Private Cloud (VPC) của bạn
- Được sử dụng cho các tên miền nội bộ không có sẵn công khai
- Ví dụ: `application1.company.internal`

### Trường Hợp Sử Dụng Private Hosted Zone

Trong môi trường VPC, bạn có thể có:

| Tài Nguyên | Tên Miền Nội Bộ | IP Riêng |
|------------|-----------------|----------|
| EC2 Instance (Web App) | `webapp.example.internal` | 10.0.0.5 |
| EC2 Instance (API) | `api.example.internal` | 10.0.0.10 |
| Database | `database.example.internal` | 10.0.0.15 |

**Ví Dụ Quy Trình**:
1. EC2 Instance 1 yêu cầu `api.example.internal`
2. Private hosted zone trả về IP riêng `10.0.0.10`
3. EC2 Instance 1 kết nối đến EC2 Instance 2
4. EC2 Instance 2 yêu cầu `database.example.internal`
5. Private hosted zone trả về IP riêng `10.0.0.15`
6. EC2 Instance 2 kết nối đến database

## So Sánh Public và Private Hosted Zones

| Tính Năng | Public Hosted Zone | Private Hosted Zone |
|-----------|-------------------|---------------------|
| **Khả năng truy cập** | Bất kỳ ai trên internet | Chỉ trong VPC |
| **Trường hợp sử dụng** | Website/dịch vụ công khai | Tài nguyên nội bộ công ty |
| **Nguồn truy vấn** | Khách hàng công khai (trình duyệt web) | Tài nguyên riêng trong VPC |
| **Ví dụ tên miền** | `example.com` | `webapp.example.internal` |
| **Khả năng hiển thị** | Có thể truy cập toàn cầu | Bị giới hạn trong VPC |

## Sự Khác Biệt Chính

### Public Hosted Zone
- Cho phép bất kỳ ai từ internet truy vấn các bản ghi của bạn
- Được sử dụng cho các tài nguyên hướng công chúng
- Phản hồi các truy vấn từ bất kỳ DNS resolver nào

### Private Hosted Zone
- Chỉ được truy vấn từ bên trong các tài nguyên riêng của bạn (ví dụ: VPC)
- Được sử dụng cho giao tiếp nội bộ
- Không thể truy cập từ internet công cộng
- Tương tự như các URL nội bộ của công ty chỉ hoạt động trong mạng công ty

## Bảng Giá

| Dịch Vụ | Chi Phí |
|---------|---------|
| Hosted Zone | **$0.50 mỗi tháng** cho mỗi hosted zone |
| Đăng Ký Tên Miền | **Tối thiểu $12 mỗi năm** |

> ⚠️ **Quan Trọng**: Route 53 **không phải là dịch vụ miễn phí**. Phần này có chi phí.

## Tóm Tắt

### Những Điểm Chính Cần Nhớ

1. **Route 53 là dịch vụ DNS được quản lý của AWS** với SLA 100% availability
2. **Hỗ trợ nhiều loại bản ghi**: A (IPv4), AAAA (IPv6), CNAME (ánh xạ tên máy chủ), NS (name servers)
3. **Cung cấp hai loại hosted zones**:
   - Public: Cho các tài nguyên có thể truy cập từ internet
   - Private: Cho các tài nguyên nội bộ VPC
4. **Hoạt động như cả**:
   - Dịch vụ DNS để định tuyến lưu lượng
   - Công cụ đăng ký tên miền để mua tên miền
5. **Rất quan trọng để định tuyến lưu lượng** đến các tài nguyên AWS bằng tên miền
6. **Được đặt tên "Route 53"** theo cổng DNS truyền thống (cổng 53)

### Khi Nào Sử Dụng Mỗi Loại Hosted Zone

**Sử dụng Public Hosted Zone khi**:
- Xây dựng website hoặc ứng dụng công khai
- Cần người dùng bên ngoài truy cập tài nguyên của bạn
- Tên miền cần được phân giải từ bất kỳ đâu trên internet

**Sử dụng Private Hosted Zone khi**:
- Xây dựng ứng dụng nội bộ trong VPC của bạn
- Cần service discovery giữa các microservices
- Muốn sử dụng tên thân thiện cho các tài nguyên riêng
- Bảo mật yêu cầu giữ các bản ghi DNS ở chế độ riêng tư

## Các Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ:
1. Đăng ký tên miền
2. Tạo hosted zones
3. Cấu hình các bản ghi DNS
4. Kiểm tra phân giải DNS

---

*Tài liệu này dựa trên tài liệu đào tạo AWS và bao gồm các khái niệm nền tảng về Amazon Route 53.*