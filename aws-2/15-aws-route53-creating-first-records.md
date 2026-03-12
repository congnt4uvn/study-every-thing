# Tạo Bản Ghi Đầu Tiên trong AWS Route 53

## Giới Thiệu

Trong hướng dẫn này, chúng ta sẽ tìm hiểu cách tạo bản ghi DNS đầu tiên trong Amazon Route 53, dịch vụ DNS (Domain Name System) có khả năng mở rộng và độ khả dụng cao của AWS.

## Tạo Bản Ghi trong Route 53

### Bước 1: Truy Cập Hosted Zone

Điều hướng đến hosted zone của Route 53, nơi bạn sẽ tạo các bản ghi DNS đơn giản.

### Bước 2: Tạo Bản Ghi Mới

1. Nhấp vào **Create record** (Tạo bản ghi) trong hosted zone của bạn
2. Nhập tên bản ghi (ví dụ: `test.stephanetheteacher.com`)
   - Bạn có thể nhập bất kỳ subdomain nào bạn muốn
   - Đây là cách bạn tạo tên miền của mình

### Bước 3: Cấu Hình Loại Bản Ghi

Trong ví dụ này, chúng ta sẽ sử dụng **A record**:
- **Loại Bản Ghi**: A record
- **Mục Đích**: Định tuyến địa chỉ IPv4 đến tên miền
- **Giá Trị**: `11.22.33.44` (địa chỉ IP mẫu)
  - Lưu ý: Đây chỉ là giá trị minh họa, không phải IP thực mà chúng ta sở hữu
  - Sau này, chúng ta sẽ định tuyến đến một EC2 instance thực

### Bước 4: Thiết Lập TTL và Routing Policy

- **TTL (Time to Live)**: 300 giây
- **Routing Policy**: Simple routing (định tuyến đơn giản - mặc định)

### Bước 5: Tạo Bản Ghi

Nhấp **Create record** để lưu cấu hình. Bản ghi của bạn đã được tạo thành công!

## Cách Hoạt Động của DNS Resolution

Khi bạn truy cập `test.stephanetheteacher.com`:
1. Trình duyệt truy vấn hosted zone
2. Route 53 phản hồi với giá trị: `11.22.33.44`
3. Trình duyệt cố gắng kết nối đến địa chỉ IP đó

**Lưu ý**: Vì `11.22.33.44` không phải là máy chủ thực mà chúng ta sở hữu, nên việc truy cập URL trong trình duyệt web sẽ không hiển thị nội dung gì.

## Kiểm Tra Bản Ghi DNS với Command Line

### Sử Dụng AWS CloudShell

Để kiểm tra DNS resolution, chúng ta sẽ sử dụng AWS CloudShell (hoặc terminal cục bộ của bạn):

1. Mở AWS Management Console
2. Nhấp để mở **CloudShell**
3. CloudShell cung cấp giao diện dòng lệnh Linux chuẩn

### Cài Đặt Công Cụ DNS

Nếu các công cụ DNS chưa được cài đặt, chạy lệnh:

```bash
sudo yum install -y bind-utils
```

Lệnh này cài đặt cả hai lệnh `nslookup` và `dig`.

### Sử Dụng nslookup

```bash
nslookup test.stephanetheteacher.com
```

**Kết Quả**: Hiển thị rằng `test.stephanetheteacher.com` được phân giải thành `11.22.33.44`

### Sử Dụng dig (Được Khuyến Nghị)

```bash
dig test.stephanetheteacher.com
```

**Kết Quả**: 
- Hiển thị phần answer với A record
- Cho thấy `test.stephanetheteacher.com` trỏ đến `11.22.33.44`
- Bao gồm giá trị TTL
- Hiển thị loại bản ghi (A record)

Lệnh `dig` được ưu tiên hơn vì nó cung cấp thông tin chi tiết hơn bao gồm TTL và loại bản ghi.

## Tổng Kết

Trong hướng dẫn này, chúng ta đã:
- ✅ Tạo bản ghi DNS đầu tiên trong Route 53
- ✅ Cấu hình A record trỏ đến địa chỉ IPv4
- ✅ Truy vấn thành công bản ghi bằng lệnh terminal

Mặc dù trang web không tải được (vì chúng ta sử dụng IP giả), chúng ta đã minh họa thành công việc tạo và phân giải bản ghi DNS. Trong các bài học tiếp theo, chúng ta sẽ định tuyến đến các máy chủ thực và xem quy trình hoàn chỉnh hoạt động.

## Các Bước Tiếp Theo

- Tìm hiểu về các loại bản ghi Route 53 khác nhau
- Định tuyến traffic đến EC2 instances thực
- Khám phá các routing policies nâng cao
- Hiểu về tối ưu hóa TTL

---

**Lưu ý**: Hướng dẫn này là một phần của loạt bài đào tạo AWS. Hãy đảm bảo thực hành theo để có trải nghiệm học tập tốt nhất.