# Kiến Thức Cơ Bản Về DNS và Giới Thiệu Route 53

## Tổng Quan

Trước khi tìm hiểu về AWS Route 53, điều quan trọng là phải hiểu cách hoạt động của DNS (Domain Name System). Đây là một công nghệ nền tảng mà bạn đã sử dụng hàng ngày mà có thể không nhận ra đầy đủ cách nó hoạt động.

## DNS là gì?

**DNS (Domain Name System)** là hệ thống dịch tên miền thân thiện với con người thành địa chỉ IP của máy chủ đích.

### Ví dụ
Khi bạn nhập `www.google.com` vào trình duyệt web, DNS sẽ chuyển đổi nó thành địa chỉ IP mà trình duyệt có thể sử dụng để truy xuất dữ liệu từ máy chủ của Google.

> **Điểm Quan Trọng:** DNS là xương sống của internet, cho phép chuyển đổi URL và tên máy chủ thành địa chỉ IP.

## Cấu Trúc Phân Cấp DNS

DNS tuân theo cấu trúc phân cấp. Ví dụ, với `www.google.com`:

- `.com` ở cấp gốc (root)
- `google.com` chính xác hơn (tên miền cấp hai)
- `www.google.com` hoặc `api.google.com` đại diện cho các cấp độ khác nhau trong hệ thống phân cấp

## Thuật Ngữ DNS

### Domain Registrar (Nhà Đăng Ký Tên Miền)
Nơi bạn đăng ký tên miền của mình. Ví dụ:
- Amazon Route 53
- GoDaddy
- Các nhà đăng ký tên miền khác

### DNS Records (Bản Ghi DNS)
Các loại bản ghi DNS khác nhau, bao gồm:
- Bản ghi **A**
- Bản ghi **AAAA**
- Bản ghi **CNAME**
- Bản ghi **NS** (Name Server)
- Và nhiều loại khác...

### Zone File (File Vùng)
Chứa tất cả các bản ghi DNS và xác định cách khớp tên máy chủ với địa chỉ IP.

### Name Servers (Máy Chủ Tên)
Các máy chủ thực sự giải quyết các truy vấn DNS.

### Top Level Domains - TLD (Tên Miền Cấp Cao Nhất)
Ví dụ: `.com`, `.us`, `.in`, `.gov`, `.org`, v.v.

### Second Level Domain - SLD (Tên Miền Cấp Hai)
Ví dụ: `amazon.com`, `google.com` (hai từ giữa các dấu chấm)

## Fully Qualified Domain Name - FQDN (Tên Miền Đầy Đủ)

Hãy phân tích ví dụ này: `http://api.www.example.com`

| Thành Phần | Loại | Mô Tả |
|-----------|------|-------|
| `.` (ở cuối) | Root | Gốc của tất cả tên miền |
| `.com` | TLD | Tên Miền Cấp Cao Nhất |
| `example.com` | SLD | Tên Miền Cấp Hai |
| `www.example.com` | Subdomain | Tên Miền Con |
| `api.www.example.com` | FQDN | Tên Miền Đầy Đủ |
| `http://` | Protocol | Giao thức truyền tải |
| Chuỗi hoàn chỉnh | URL | Định Vị Tài Nguyên Thống Nhất |

## Cách DNS Hoạt Động

### Thiết Lập Kịch Bản
- Máy chủ web với IP công khai: `9.10.11.12` (ví dụ: một EC2 instance)
- Tên miền: `example.com`
- Mục tiêu: Truy cập máy chủ web bằng tên miền

### Quy Trình Phân Giải DNS

```
[Trình Duyệt Web]
      ↓ (1) Truy vấn: example.com?
[Local DNS Server - Máy Chủ DNS Cục Bộ]
      ↓ (2) Truy vấn: example.com?
[Root DNS Server - Máy Chủ DNS Gốc] (Quản lý bởi ICANN)
      ↓ (3) Phản hồi: "Tôi biết .com → NS tại 1.2.3.4"
[Local DNS Server]
      ↓ (4) Truy vấn: example.com?
[TLD DNS Server .com] (Quản lý bởi IANA)
      ↓ (5) Phản hồi: "Tôi biết example.com → NS tại 5.6.7.8"
[Local DNS Server]
      ↓ (6) Truy vấn: example.com?
[SLD DNS Server] (Quản lý bởi Nhà Đăng Ký, ví dụ: Route 53)
      ↓ (7) Phản hồi: "example.com → Bản ghi A → 9.10.11.12"
[Local DNS Server] (lưu kết quả vào cache)
      ↓ (8) Trả về: 9.10.11.12
[Trình Duyệt Web]
      ↓ (9) Kết nối tới: 9.10.11.12
[Máy Chủ Web]
```

### Giải Thích Từng Bước

1. **Trình duyệt yêu cầu** `example.com` từ Local DNS Server
2. **Local DNS Server** (được chỉ định bởi công ty hoặc ISP) truy vấn Root DNS Server
3. **Root DNS Server** (ICANN) phản hồi: "Tôi không có example.com, nhưng tôi biết tên miền .com → NS tại 1.2.3.4"
4. **Local DNS Server** truy vấn TLD DNS Server cho `.com`
5. **TLD DNS Server** (IANA) phản hồi: "Tôi biết example.com → NS tại 5.6.7.8"
6. **Local DNS Server** truy vấn Second Level Domain DNS Server
7. **SLD DNS Server** (Nhà Đăng Ký như Route 53) phản hồi: "example.com là bản ghi A → 9.10.11.12"
8. **Local DNS Server** lưu kết quả vào cache và gửi lại cho trình duyệt
9. **Trình duyệt** sử dụng địa chỉ IP `9.10.11.12` để truy cập máy chủ web

### DNS Caching (Lưu Trữ Tạm DNS)
Local DNS Server lưu trữ câu trả lời vào bộ nhớ cache để các truy vấn trong tương lai cho `example.com` có thể được giải quyết ngay lập tức mà không cần thực hiện lại toàn bộ quy trình.

## Sử Dụng Trong Thực Tế

Bạn đã sử dụng DNS suốt cuộc đời mà không nhận ra:
- Truy cập `www.google.com`
- Truy cập bất kỳ trang web nào
- Bất kỳ dịch vụ internet nào sử dụng tên miền

## Tiếp Theo Là Gì?

Bây giờ bạn đã hiểu cách DNS hoạt động, chúng ta sẽ khám phá AWS Route 53 và học cách quản lý máy chủ DNS của riêng bạn.

---

**Lưu ý:** Đây là kiến thức nền tảng sẽ giúp bạn hiểu rõ hơn về Route 53 và quản lý DNS trong AWS.