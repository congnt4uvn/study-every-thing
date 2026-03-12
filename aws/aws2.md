

FILE: 1-aws-rds-overview.md


# Tổng Quan về AWS RDS

## Giới Thiệu về AWS RDS

**RDS** là viết tắt của **Relational Database Service** (Dịch vụ Cơ sở Dữ liệu Quan hệ). Đây là một dịch vụ cơ sở dữ liệu được quản lý cho các cơ sở dữ liệu sử dụng SQL làm ngôn ngữ truy vấn. SQL là ngôn ngữ có cấu trúc được thiết kế để truy vấn cơ sở dữ liệu, được thích ứng tốt và chạy trên nhiều engine khác nhau.

RDS cho phép bạn tạo các cơ sở dữ liệu trên đám mây được quản lý bởi AWS, mang lại nhiều lợi ích.

## Các Database Engine Được Hỗ Trợ

AWS RDS hỗ trợ các database engine sau:

- **PostgreSQL**
- **MySQL**
- **MariaDB**
- **Oracle**
- **Microsoft SQL Server**
- **IBM DB2**
- **Amazon Aurora** (cơ sở dữ liệu độc quyền của AWS)

## Tại Sao Nên Sử Dụng RDS Thay Vì EC2?

Mặc dù bạn có thể triển khai dịch vụ cơ sở dữ liệu của riêng mình trên EC2 instance, RDS là một **dịch vụ được quản lý** cung cấp nhiều lợi thế đáng kể:

### Lợi Ích Chính của RDS

- **Cung Cấp Tự Động**: Việc cung cấp cơ sở dữ liệu được tự động hóa hoàn toàn, bao gồm cả việc vá lỗi hệ điều hành cơ bản
- **Sao Lưu Liên Tục**: Tự động sao lưu với khả năng Point in Time Restore để khôi phục về một thời điểm cụ thể
- **Dashboard Giám Sát**: Xem hiệu suất của cơ sở dữ liệu
- **Read Replicas**: Cải thiện hiệu suất đọc với các bản sao đọc chuyên dụng
- **Thiết Lập Multi-AZ**: Kích hoạt khả năng khôi phục thảm họa
- **Cửa Sổ Bảo Trì**: Lên lịch các cửa sổ nâng cấp
- **Khả Năng Mở Rộng**:
  - **Mở Rộng Dọc**: Tăng loại instance
  - **Mở Rộng Ngang**: Thêm read replicas
- **Lưu Trữ EBS**: Lưu trữ được hỗ trợ bởi Amazon EBS

### Hạn Chế

- **Không Có Quyền Truy Cập SSH**: Bạn không thể SSH vào các RDS instances vì đây là dịch vụ được quản lý hoàn toàn

Tuy nhiên, hạn chế này được bù đắp bởi tất cả các tính năng tự động mà AWS cung cấp, mà nếu không bạn phải tự thiết lập trên EC2.

## RDS Storage Auto Scaling

### Tổng Quan

RDS Storage Auto Scaling là một tính năng có thể xuất hiện trong các kỳ thi AWS. Khi bạn tạo một cơ sở dữ liệu RDS, bạn chỉ định dung lượng lưu trữ ban đầu (ví dụ: 20 GB). Nếu cơ sở dữ liệu của bạn được sử dụng nhiều và sắp hết dung lượng lưu trữ, RDS có thể tự động mở rộng dung lượng lưu trữ mà không cần can thiệp thủ công.

### Cách Hoạt Động

1. Ứng dụng của bạn thực hiện nhiều thao tác đọc và ghi vào cơ sở dữ liệu RDS
2. Khi đạt đến các ngưỡng nhất định, dung lượng lưu trữ tự động mở rộng
3. Không có thời gian chết hoặc thao tác thủ công nào được yêu cầu

### Cấu Hình

Để sử dụng tính năng này:

- **Đặt Ngưỡng Lưu Trữ Tối Đa**: Xác định giới hạn tối đa cho việc tăng trưởng lưu trữ để ngăn việc mở rộng vô hạn
- **Kích Hoạt Tự Động Khi**:
  - Dung lượng lưu trữ trống nhỏ hơn 10% dung lượng đã phân bổ
  - Tình trạng dung lượng thấp kéo dài hơn 5 phút
  - Ít nhất 6 giờ đã trôi qua kể từ lần sửa đổi cuối cùng

### Trường Hợp Sử Dụng

Tính năng này đặc biệt hữu ích cho:
- Các ứng dụng có khối lượng công việc không thể đoán trước
- Tránh các thao tác mở rộng lưu trữ cơ sở dữ liệu thủ công
- Được hỗ trợ bởi tất cả các database engine của RDS

## Tổng Kết

AWS RDS là một dịch vụ cơ sở dữ liệu được quản lý mạnh mẽ, giúp đơn giản hóa việc quản trị cơ sở dữ liệu trong khi cung cấp tính khả dụng cao, sao lưu tự động và khả năng mở rộng liền mạch. Hiểu về RDS và các tính năng của nó là điều cần thiết cho các kỳ thi chứng chỉ AWS và triển khai đám mây thực tế.




FILE: 10-aws-elasticache-caching-strategies.md


# Chiến Lược Caching với AWS ElastiCache

## Tổng Quan

Hướng dẫn này cung cấp kiến thức chuyên sâu về các chiến lược caching khác nhau cho AWS ElastiCache, bao gồm các cân nhắc triển khai và thực tiễn tốt nhất.

## Cache Có An Toàn và Hiệu Quả Không?

### Các Cân Nhắc Về An Toàn

Nhìn chung, caching là an toàn, nhưng có những điều quan trọng cần xem xét:

- **Độ Mới Của Dữ Liệu**: Dữ liệu của bạn có thể đã lỗi thời, dẫn đến tính nhất quán cuối cùng (eventual consistency)
- **Tính Phù Hợp Của Loại Dữ Liệu**: Không phải tập dữ liệu nào cũng phù hợp để cache
- Chỉ cache dữ liệu khi có thể chấp nhận được việc dữ liệu có thể cũ

### Đánh Giá Hiệu Quả

Caching hiệu quả nhất khi:

- ✅ Dữ liệu thay đổi chậm
- ✅ Một vài key được truy cập thường xuyên
- ✅ Cấu trúc key-value hoặc kết quả tổng hợp

Caching kém hiệu quả (anti-patterns):

- ❌ Dữ liệu thay đổi rất nhanh
- ❌ Bạn cần tất cả các key trong dataset thường xuyên
- ❌ Cấu trúc dữ liệu không phù hợp với mẫu truy vấn

### Các Câu Hỏi Quan Trọng

1. **Có an toàn khi cache dữ liệu này không?**
2. **Caching có hiệu quả với dữ liệu này không?**
3. **Dữ liệu đã được cấu trúc đúng cách cho caching chưa?**
4. **Mẫu thiết kế caching nào phù hợp nhất?**

## Chiến Lược Caching 1: Lazy Loading

**Còn được gọi là**: Cache-Aside, Lazy Population

### Cách Hoạt Động

1. **Cache Hit**: Ứng dụng yêu cầu dữ liệu → ElastiCache có dữ liệu → Trả về ngay lập tức
2. **Cache Miss**: Ứng dụng yêu cầu dữ liệu → ElastiCache không có → Đọc từ database (RDS) → Ghi vào cache → Trả về dữ liệu

### Luồng Kiến Trúc

```
Ứng dụng → ElastiCache (Cache Miss) 
        → Amazon RDS (Đọc) 
        → ElastiCache (Ghi) 
        → Trả về Dữ liệu
```

### Ưu Điểm

- ✅ **Hiệu Quả**: Chỉ cache dữ liệu được yêu cầu
- ✅ **Không Gây Lỗi Nghiêm Trọng**: Nếu cache bị lỗi, hệ thống vẫn hoạt động (với độ trễ tăng)
- ✅ **Tự Phục Hồi**: Cache tự động làm ấm khi có requests

### Nhược Điểm

- ❌ **Phạt Cache Miss**: Ba lượt đi về (app → cache → database → cache)
- ❌ **Trải Nghiệm Người Dùng**: Độ trễ đáng chú ý khi cache miss
- ❌ **Dữ Liệu Cũ**: Cập nhật trong RDS không tự động cập nhật cache

### Ví Dụ Pseudocode

```python
def get_user(user_id):
    # Kiểm tra cache trước
    record = cache.get(user_id)
    
    if record is None:
        # Cache miss - truy vấn database
        record = db.query("SELECT * FROM users WHERE id = ?", user_id)
        
        # Điền vào cache
        cache.set(user_id, record)
    
    return record

# Cách sử dụng
user = get_user(17)
```

## Chiến Lược Caching 2: Write Through

### Cách Hoạt Động

- Ứng dụng ghi vào database
- Đồng thời ghi vào cache
- Các lần đọc luôn trúng dữ liệu mới trong cache

### Luồng Kiến Trúc

```
Ứng dụng → Amazon RDS (Ghi) 
        → ElastiCache (Ghi)
        
Ứng dụng → ElastiCache (Đọc - Cache Hit)
```

### Ưu Điểm

- ✅ **Không Bao Giờ Cũ**: Dữ liệu trong cache luôn cập nhật
- ✅ **Kỳ Vọng Người Dùng**: Người dùng mong đợi ghi chậm hơn đọc
- ✅ **Hiệu Suất Đọc**: Tất cả các lần đọc đều nhanh (cache hits)

### Nhược Điểm

- ❌ **Phạt Ghi**: Hai lần gọi mỗi lần ghi (database + cache)
- ❌ **Thiếu Dữ Liệu**: Cache không có dữ liệu cho đến khi nó được ghi vào database
- ❌ **Cache Churn**: Có thể cache dữ liệu không bao giờ được đọc (lãng phí không gian)

### Ví Dụ Pseudocode

```python
def save_user(user_id, values):
    # Lưu vào database trước
    record = db.query("UPDATE users ... ", user_id, values)
    
    # Cập nhật cache
    cache.set(user_id, record)
    
    return record
```

### Thực Tiễn Tốt Nhất: Kết Hợp Các Chiến Lược

Kết hợp Write Through với Lazy Loading để xử lý các trường hợp dữ liệu bị thiếu.

## Cache Eviction và Time-to-Live (TTL)

### Các Trigger Xóa Cache

1. **Xóa Rõ Ràng**: Xóa items thủ công
2. **Bộ Nhớ Đầy**: Các items Ít Được Sử Dụng Gần Đây nhất (LRU) bị xóa
3. **Hết Hạn TTL**: Items hết hạn sau thời gian đặt

### Chiến Lược TTL

- Hiệu quả cho: Bảng xếp hạng, Bình luận, Luồng hoạt động
- Phạm vi: Vài giây đến hàng giờ hoặc ngày
- Ngay cả TTL ngắn (vài giây) cũng có thể rất hiệu quả cho dữ liệu được truy cập thường xuyên

### Khi Nào Cần Scale

Nếu bạn gặp quá nhiều evictions:
- Scale up: Tăng kích thước node
- Scale out: Thêm nhiều nodes hơn

## Thực Tiễn Tốt Nhất và Khuyến Nghị

### 1. Bắt Đầu Với Lazy Loading
- Dễ triển khai
- Hoạt động như một nền tảng vững chắc
- Cải thiện hiệu suất đọc trong hầu hết các tình huống

### 2. Thêm Write Through Như Một Tối Ưu Hóa
- Triển khai sau Lazy Loading
- Sử dụng để giảm tính cũ của cache
- Thường không phải là chiến lược độc lập

### 3. Triển Khai TTL Một Cách Khôn Ngoan
- Sử dụng TTL trong hầu hết các trường hợp (trừ Write Through thuần túy)
- Đặt giá trị hợp lý cho ứng dụng của bạn
- Cân bằng giữa độ mới và hiệu suất

### 4. Cache Có Chọn Lọc
- ✅ Ứng viên tốt: Hồ sơ người dùng, blogs, danh mục sản phẩm
- ❌ Ứng viên kém: Dữ liệu giá cả, số dư tài khoản ngân hàng, dữ liệu thời gian thực quan trọng

## Suy Nghĩ Cuối Cùng

> "Có hai điều khó khăn trong Khoa học Máy tính: vô hiệu hóa cache và đặt tên cho mọi thứ."

Caching rất phức tạp và đầy thách thức. Hướng dẫn này bao gồm các kiến thức cơ bản cần thiết cho các kỳ thi chứng chỉ AWS, nhưng caching là cả một lĩnh vực của Khoa học Máy tính.

### Trọng Tâm Kỳ Thi

Đối với các kỳ thi AWS, cần hiểu:
- Các chiến lược caching khác nhau (Lazy Loading, Write Through)
- Các mẫu pseudocode
- Đánh đổi và ý nghĩa của từng phương pháp

---

**Điểm Chính**: Chọn chiến lược caching dựa trên trường hợp sử dụng cụ thể, đặc điểm dữ liệu và yêu cầu hiệu suất của bạn.




FILE: 11-amazon-memorydb-for-redis-overview.md


# Tổng Quan về Amazon MemoryDB for Redis

## Giới Thiệu

Amazon MemoryDB for Redis là một dịch vụ cơ sở dữ liệu trong bộ nhớ (in-memory database), tương thích với Redis và có tính bền vững, mang đến cách tiếp cận độc đáo trong việc quản lý dữ liệu trong hệ sinh thái AWS.

## Sự Khác Biệt Chính so với Redis

Trong khi Redis truyền thống được sử dụng như một bộ nhớ cache với một số tính năng bền vững, **MemoryDB for Redis** về cơ bản là một cơ sở dữ liệu cung cấp API tương thích với Redis. Sự phân biệt này rất quan trọng để hiểu khi nào nên sử dụng mỗi dịch vụ.

## Đặc Điểm Hiệu Suất

- **Hiệu suất siêu nhanh**: Hơn 160 triệu yêu cầu mỗi giây
- **Lưu trữ dữ liệu trong bộ nhớ**: Cung cấp tốc độ vượt trội
- **Lưu trữ bền vững**: Không giống như cache thông thường, dữ liệu được lưu trữ lâu dài
- **Transaction log Multi-AZ**: Đảm bảo tính bền vững và tính sẵn sàng cao của dữ liệu

## Khả Năng Mở Rộng

MemoryDB for Redis mở rộng liền mạch từ:
- Điểm khởi đầu: Hàng chục gigabyte
- Dung lượng tối đa: Hàng trăm terabyte lưu trữ

## Các Trường Hợp Sử Dụng

Amazon MemoryDB for Redis lý tưởng cho:

- **Ứng dụng web và di động**: Truy cập dữ liệu hiệu suất cao
- **Game trực tuyến**: Truy xuất dữ liệu độ trễ thấp
- **Phát trực tuyến media**: Phân phối nội dung nhanh chóng
- **Kiến trúc microservices**: Khi nhiều dịch vụ cần truy cập vào cơ sở dữ liệu trong bộ nhớ tương thích Redis

## Lợi Ích Kiến Trúc

Khi bạn có nhiều microservices yêu cầu truy cập vào cơ sở dữ liệu trong bộ nhớ tương thích Redis, MemoryDB for Redis cung cấp:

1. **Tốc độ trong bộ nhớ siêu nhanh**: Hiệu suất tối ưu cho các ứng dụng thời gian thực
2. **Transaction log Multi-AZ**: Dữ liệu được lưu trữ trên nhiều Availability Zone
3. **Khôi phục nhanh**: Phục hồi nhanh chóng trong trường hợp xảy ra sự cố
4. **Tính bền vững của dữ liệu**: Đảm bảo dữ liệu được lưu trữ lâu dài khi cần thiết

## Liên Quan Đến Kỳ Thi

Tổng quan này bao gồm các khái niệm thiết yếu cần thiết cho các kỳ thi chứng chỉ AWS. Hiểu được sự khác biệt giữa Redis như một cache và MemoryDB như một cơ sở dữ liệu bền vững là điều quan trọng.

---

*Lưu ý: Nội dung này dựa trên các dịch vụ AWS và có liên quan đến việc chuẩn bị chứng chỉ AWS.*




FILE: 12-dns-fundamentals-and-route53-introduction.md


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




FILE: 13-amazon-route53-detailed-overview.md


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




FILE: 14-aws-route53-domain-registration-tutorial.md


# AWS Route 53 - Hướng Dẫn Đăng Ký Tên Miền

## Giới Thiệu

Trong hướng dẫn này, chúng ta sẽ tìm hiểu quy trình đăng ký tên miền sử dụng Amazon Route 53, dịch vụ hệ thống tên miền (DNS) có khả năng mở rộng của AWS.

## Yêu Cầu Trước Khi Bắt Đầu

Trước khi bắt đầu, bạn cần:
- Có tài khoản AWS
- Sẵn sàng chi trả khoảng $12-13 mỗi năm cho việc đăng ký tên miền
- Có thông tin liên hệ hợp lệ để đăng ký tên miền

## Bắt Đầu Với Route 53

Khi lần đầu truy cập Route 53, bạn sẽ thấy:
- Không có hosted zone nào (nếu đây là lần đầu tiên)
- Không có tên miền đã đăng ký

Giao diện có thể hiển thị phiên bản console mới, đây là phiên bản được khuyến nghị sử dụng.

## Quy Trình Đăng Ký Tên Miền Từng Bước

### Bước 1: Truy Cập Phần Đăng Ký Tên Miền

1. Điều hướng đến bảng điều khiển Route 53
2. Ở phía bên trái, nhấp vào **"Register domains"** (Đăng ký tên miền)
3. Bạn sẽ thấy giao diện console phiên bản mới

### Bước 2: Chọn Tên Miền

1. Nhập tên miền mong muốn vào ô tìm kiếm
2. Đảm bảo đó là tên duy nhất chưa được ai đăng ký
3. Kiểm tra tính khả dụng - hệ thống sẽ hiển thị nếu tên miền còn trống
4. Xem lại giá (thường khoảng $13 USD mỗi năm)
5. Thêm tên miền vào giỏ hàng
6. Nhấp **"Proceed to checkout"** (Tiến hành thanh toán)

### Bước 3: Cấu Hình Thiết Lập Tên Miền

**Thiết Lập Thời Hạn:**
- Chọn thời hạn đăng ký (ví dụ: 1 năm)
- Cấu hình thiết lập tự động gia hạn:
  - **Bật tự động gia hạn**: Được khuyến nghị nếu bạn có kế hoạch giữ tên miền lâu dài
  - **Tắt tự động gia hạn**: Nếu bạn chỉ cần tên miền tạm thời (ví dụ: cho một khóa học)
  
> **Cảnh báo**: Nếu bạn tắt tự động gia hạn và quên gia hạn, người khác có thể mua tên miền của bạn sau khi nó hết hạn.

### Bước 4: Nhập Thông Tin Liên Hệ

1. Điền hoặc xác minh thông tin liên hệ được điền sẵn
2. Thông tin liên hệ quản trị và kỹ thuật có thể được đặt giống với người đăng ký
3. **Quan trọng**: Bật bảo vệ quyền riêng tư để:
   - Ngăn chặn thư rác
   - Ẩn thông tin cá nhân của bạn (địa chỉ, số điện thoại, v.v.) khỏi cơ sở dữ liệu WHOIS công khai

### Bước 5: Xem Lại và Gửi

1. Xem lại tất cả thông tin cẩn thận
2. Đọc và chấp nhận các điều khoản và điều kiện
3. Nhấp **"Submit"** (Gửi)

> **Quan trọng**: Việc gửi sẽ tính phí đăng ký (khoảng $13). Chỉ tiếp tục nếu bạn sẵn sàng thanh toán.

### Bước 6: Chờ Hoàn Tất Đăng Ký

- Việc đăng ký tên miền thường mất vài phút đến vài giờ
- Bạn sẽ nhận được xác nhận khi quy trình hoàn tất

## Xác Minh Đăng Ký Tên Miền

### Truy Cập Hosted Zones

1. Trong Route 53, điều hướng đến **"Hosted zones"** ở phía bên trái
2. Nhấp vào tên miền mới đăng ký của bạn (ví dụ: stefanetheteacher.com)

### Các Bản Ghi DNS Mặc Định

Bạn sẽ thấy ít nhất hai bản ghi mặc định:

1. **Bản Ghi NS (Name Server)**
   - Chỉ ra rằng AWS DNS nên được sử dụng cho các truy vấn DNS
   - Trỏ đến Route 53 làm dịch vụ DNS của bạn

2. **Bản Ghi SOA (Start of Authority)**
   - Chứa thông tin quản trị về vùng

## Hiểu Về Route 53 Là Nguồn DNS Chính Thức

Với hosted zone đã được cấu hình:
- Route 53 trở thành nguồn chính thức cho tất cả các bản ghi DNS trong tên miền của bạn
- Bất kỳ bản ghi DNS nào bạn tạo sẽ được quản lý bởi Route 53
- Bạn có thể thêm, sửa đổi hoặc xóa các bản ghi DNS theo nhu cầu

## Xem Xét Chi Phí

- Đăng ký tên miền: Khoảng $12-13 USD mỗi năm (tùy thuộc vào phần mở rộng tên miền)
- Hosted zone: $0.50 mỗi tháng cho mỗi hosted zone
- Truy vấn DNS: Định giá theo mức sử dụng

> **Lưu ý**: Nếu bạn không muốn trả phí đăng ký tên miền, bạn có thể bỏ qua phần thực hành và chỉ theo dõi nội dung video.

## Các Bước Tiếp Theo

Bây giờ bạn đã có tên miền đã đăng ký và hosted zone, bạn đã sẵn sàng để:
- Tạo các bản ghi DNS (được đề cập trong bài giảng tiếp theo)
- Cấu hình các chính sách định tuyến
- Thiết lập kiểm tra sức khỏe
- Triển khai các cấu hình DNS nâng cao

## Tóm Tắt

Bạn đã học thành công cách:
- Điều hướng bảng điều khiển Route 53
- Đăng ký tên miền mới
- Cấu hình thiết lập tên miền và thông tin liên hệ
- Hiểu những điều cơ bản về hosted zones và bản ghi DNS
- Xác minh đăng ký tên miền của bạn

Trong bài giảng tiếp theo, chúng ta sẽ khám phá cách tạo và quản lý các bản ghi DNS trong hosted zone của bạn.




FILE: 15-aws-route53-creating-first-records.md


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




FILE: 16-aws-route53-multi-region-ec2-setup.md


# Thiết Lập EC2 Đa Vùng và ALB cho Route 53

## Tổng Quan

Hướng dẫn này sẽ giúp bạn thiết lập ba EC2 instance trên các vùng AWS khác nhau và cấu hình Application Load Balancer (ALB) để chuẩn bị cho việc cấu hình Route 53.

## Tổng Quan Kiến Trúc

Chúng ta sẽ tạo:
- 3 EC2 instance ở các vùng khác nhau (Frankfurt, Northern Virginia, Singapore)
- 1 Application Load Balancer tại Frankfurt
- Target group để định tuyến lưu lượng

## Bước 1: Khởi Động EC2 Instance Đầu Tiên (Frankfurt - EU Central 1)

### Cấu Hình Instance

1. Truy cập dịch vụ EC2 và click **Launch Instance**
2. Chọn **Amazon Linux 2** AMI
3. Chọn instance type **t2.micro**
4. **Key Pair**: Chọn "Proceed without a key pair" (chúng ta sẽ dùng EC2 Instance Connect)

### Cài Đặt Security Group

Tạo security group mới với các rule sau:
- **SSH**: Port 22, Source: Anywhere
- **HTTP**: Port 80, Source: Anywhere

### Script User Data

Trong phần Advanced Details, thêm bootstrap script sau:

```bash
#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd
EC2_AVAIL_ZONE=$(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone)
echo "<h1>Hello World from $(hostname -f) in AZ $EC2_AVAIL_ZONE</h1>" > /var/www/html/index.html
```

Script này sẽ:
- Cài đặt Apache HTTP server
- Hiển thị hostname của instance và availability zone
- Sử dụng EC2 metadata để lấy thông tin AZ

4. Click **Launch Instance**

## Bước 2: Khởi Động EC2 Instance Thứ Hai (Northern Virginia - US East 1)

1. Chuyển sang vùng **US East 1** (Northern Virginia)
2. Khởi động instance với cùng cấu hình:
   - Amazon Linux 2
   - t2.micro
   - Không cần key pair
   - Security group: Cho phép SSH và HTTP
   - Cùng user data script từ Bước 1
3. Khởi động instance

## Bước 3: Khởi Động EC2 Instance Thứ Ba (Singapore - AP Southeast 1)

1. Chuyển sang vùng **AP Southeast 1** (Singapore)
2. Khởi động instance với cài đặt tương tự:
   - Amazon Linux 2
   - t2.micro
   - Không cần key pair
   - Security group: Cho phép SSH và HTTP
   - Cùng user data script
3. Khởi động instance

## Bước 4: Tạo Application Load Balancer (Frankfurt)

### Cấu Hình ALB

1. Quay lại vùng **Frankfurt (EU Central 1)**
2. Truy cập **Load Balancers** và click **Create Load Balancer**
3. Chọn **Application Load Balancer**

### Cấu Hình Cơ Bản

- **Name**: `DemoRoute53ALB`
- **Scheme**: Internet-facing
- **IP address type**: IPv4

### Network Mapping

- Chọn **3 availability zones** (tất cả subnet có sẵn)

### Security Groups

- Chọn security group đã tạo trước đó (có HTTP và SSH được bật)

### Listeners và Routing

- **Protocol**: HTTP
- **Port**: 80
- Tạo target group mới

## Bước 5: Tạo Target Group

1. **Target type**: Instances
2. **Name**: `demo-tg-route53`
3. **Protocol**: HTTP
4. **Port**: 80
5. Click **Next**

### Đăng Ký Target

1. Chọn EC2 instance tại Frankfurt
2. Click **Include as pending below**
3. Xem lại và click **Create target group**

## Bước 6: Hoàn Tất Tạo ALB

1. Quay lại trang tạo Load Balancer
2. Refresh và chọn target group vừa tạo: `demo-tg-route53`
3. Xem lại cài đặt và click **Create Load Balancer**
4. Click **View Load Balancer**

## Bước 7: Kiểm Tra

### Test EC2 Instances

Kiểm tra từng instance bằng cách truy cập địa chỉ IP công khai qua HTTP:

**Instance Frankfurt (EU Central 1)**
- Copy địa chỉ IPv4 công khai
- Truy cập qua trình duyệt: `http://<public-ip>`
- Kết quả mong đợi: `Hello World from <hostname> in AZ eu-central-1b`

**Instance Northern Virginia (US East 1)**
- Copy địa chỉ IPv4 công khai
- Truy cập qua trình duyệt: `http://<public-ip>`
- Kết quả mong đợi: `Hello World from <hostname> in AZ us-east-1a`

**Instance Singapore (AP Southeast 1)**
- Copy địa chỉ IPv4 công khai
- Truy cập qua trình duyệt: `http://<public-ip>`
- Kết quả mong đợi: `Hello World from <hostname> in AZ ap-southeast-1b`

### Test Application Load Balancer

1. Copy tên DNS của ALB từ chi tiết Load Balancer
2. Truy cập qua trình duyệt: `http://<alb-dns-name>`
3. ALB có thể mất vài phút để provisioning
4. Khi đã hoạt động, bạn sẽ thấy: `Hello World from <hostname> in AZ eu-central-1b`

## Tóm Tắt

Bạn đã tạo thành công:
- ✅ 3 EC2 instance trên 3 vùng AWS khác nhau
- ✅ 1 Application Load Balancer tại Frankfurt
- ✅ 1 Target group với instance đã đăng ký
- ✅ Tất cả instance đang phục vụ HTTP traffic với thông tin vùng

## Tham Chiếu Chi Tiết Instance

Lưu giữ thông tin tài nguyên của bạn:

| Vùng | Mã Vùng | IP Công Khai | Availability Zone |
|------|---------|--------------|-------------------|
| Frankfurt | eu-central-1 | `<ip-của-bạn>` | eu-central-1b |
| Northern Virginia | us-east-1 | `<ip-của-bạn>` | us-east-1a |
| Singapore | ap-southeast-1 | `<ip-của-bạn>` | ap-southeast-1b |

**Tên DNS ALB**: `<tên-dns-alb-của-bạn>`

## Các Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ cấu hình Route 53 để triển khai:
- Chính sách định tuyến theo địa lý (Geographic routing)
- Định tuyến dựa trên độ trễ (Latency-based routing)
- Cấu hình failover
- Health checks

Hãy lưu giữ thông tin này để cấu hình Route 53!




FILE: 17-aws-route53-ttl-explained.md


# Giải Thích AWS Route 53 TTL (Time To Live)

## Giới Thiệu

Trong hướng dẫn này, chúng ta sẽ tìm hiểu về DNS TTL (Time To Live) và cách nó hoạt động với AWS Route 53. Chúng ta sẽ đề cập đến lý thuyết về TTL và thực hành với một ví dụ cụ thể.

## TTL Là Gì?

TTL của bản ghi DNS là giá trị **Time To Live** (Thời Gian Tồn Tại) xác định thời gian một phản hồi DNS được lưu cache bởi client.

### Cách TTL Hoạt Động

Hãy xem xét một ví dụ trong đó client truy cập web server thông qua DNS Route 53:

1. **Yêu Cầu DNS**: Client thực hiện yêu cầu DNS cho `myapp.example.com`
2. **Phản Hồi DNS**: Route 53 phản hồi với:
   - Một bản ghi A
   - Địa chỉ IP
   - Giá trị TTL (ví dụ: 300 giây)
3. **Client Cache**: Client lưu cache kết quả trong khoảng thời gian TTL
4. **Các Yêu Cầu Tiếp Theo**: Trong thời gian cache, client không truy vấn DNS nữa - nó sử dụng phản hồi đã được cache

### Tại Sao Sử Dụng TTL?

Mục đích của TTL là giảm các truy vấn DNS không cần thiết. Vì các bản ghi DNS không thay đổi thường xuyên, việc cache phản hồi giúp cải thiện hiệu suất và giảm lưu lượng đến hệ thống DNS.

## Đánh Đổi Khi Chọn Giá Trị TTL

Việc chọn giá trị TTL phù hợp liên quan đến việc cân bằng hai yếu tố:

### TTL Cao (ví dụ: 24 giờ)

**Ưu Điểm:**
- Ít lưu lượng đến Route 53
- Ít truy vấn DNS từ client
- Chi phí thấp hơn (Route 53 tính phí theo số truy vấn)

**Nhược Điểm:**
- Bản ghi có thể bị lỗi thời
- Thay đổi mất tới 24 giờ để lan truyền
- Khó thực hiện cập nhật nhanh

### TTL Thấp (ví dụ: 60 giây)

**Ưu Điểm:**
- Bản ghi luôn cập nhật
- Thay đổi lan truyền nhanh
- Dễ dàng cập nhật bản ghi

**Nhược Điểm:**
- Nhiều lưu lượng đến Route 53
- Chi phí cao hơn do nhiều truy vấn
- Tăng tải cho DNS server

## Chiến Lược Thay Đổi TTL

Khi lên kế hoạch thay đổi bản ghi DNS:

1. **Giảm TTL** 24 giờ trước khi thay đổi (ví dụ: từ 24 giờ xuống 60 giây)
2. **Chờ đợi** TTL thấp lan truyền đến tất cả client
3. **Cập nhật bản ghi** - thay đổi sẽ lan truyền nhanh chóng
4. **Tăng TTL** trở lại giá trị ban đầu sau khi hoàn thành thay đổi

## Lưu Ý Quan Trọng

- TTL là **bắt buộc** cho mọi bản ghi DNS
- **Ngoại lệ**: Bản ghi Alias (sẽ được đề cập trong bài giảng riêng) không yêu cầu TTL

## Thực Hành Demo

### Tạo Bản Ghi Thử Nghiệm

Hãy tạo một bản ghi demo để quan sát hành vi của TTL:

1. **Tên Bản Ghi**: `demo.stephanetheteacher.com`
2. **Loại Bản Ghi**: Bản ghi A
3. **Giá Trị**: Địa chỉ IP của EC2 instance trong `eu-central-1`
4. **TTL**: 120 giây (2 phút)

### Kiểm Tra Bản Ghi

#### Sử Dụng Trình Duyệt Web

Truy cập `demo.stephanetheteacher.com` trên Google Chrome - bạn sẽ thấy ứng dụng chạy trên instance eu-central-1.

#### Sử Dụng Công Cụ Dòng Lệnh

**Lệnh nslookup:**
```bash
nslookup demo.stephanetheteacher.com
```

**Lệnh dig:**
```bash
dig demo.stephanetheteacher.com
```

Lệnh `dig` hiển thị TTL còn lại trong phần answer. Ví dụ, nếu bạn thấy `115`, có nghĩa là bản ghi sẽ được cache thêm 115 giây nữa.

### Quan Sát TTL Hoạt Động

1. **Truy Vấn Đầu Tiên**: Chạy `dig` - bạn có thể thấy TTL là 115 giây
2. **Truy Vấn Lại**: Chạy `dig` ngay lập tức - TTL giảm xuống 98 giây (hoặc tương tự)
3. **Thay Đổi Bản Ghi**: Chỉnh sửa bản ghi để trỏ đến IP khác (ví dụ: ap-southeast-1)
4. **Truy Vấn Lại**: Mặc dù đã cập nhật, IP cũ vẫn được trả về vì nó được cache
5. **Chờ TTL Hết Hạn**: Sau khi cache hết hạn (120 giây), IP mới được trả về

### Kết Quả Sau Khi TTL Hết Hạn

Sau khi chờ TTL hết hạn:

- **Trình Duyệt Web**: Refresh hiển thị instance mới (ap-southeast-1b)
- **Lệnh dig**: Hiển thị TTL mới là 120 giây và địa chỉ IP mới
- **CloudShell**: Xác nhận bản ghi DNS hiện trỏ đến server mới

## Những Điểm Chính Cần Nhớ

1. **TTL kiểm soát cache**: Nó xác định thời gian client cache phản hồi DNS
2. **Cân bằng là quan trọng**: Chọn giá trị TTL dựa trên tần suất cập nhật và chi phí
3. **Thay đổi không tức thì**: Thay đổi DNS mất thời gian để lan truyền dựa trên TTL
4. **Lên kế hoạch trước**: Giảm TTL trước khi thực hiện thay đổi quan trọng
5. **Sử dụng dig/nslookup**: Các công cụ này giúp xác minh thay đổi DNS và giám sát TTL

## Kết Luận

Hiểu về TTL là rất quan trọng để quản lý bản ghi DNS hiệu quả trong AWS Route 53. Giá trị TTL phù hợp phụ thuộc vào trường hợp sử dụng cụ thể của bạn - tần suất cập nhật bản ghi so với chi phí lưu lượng DNS mà bạn sẵn sàng chi trả.

Trong bài giảng tiếp theo, chúng ta sẽ khám phá bản ghi Alias, một loại bản ghi DNS đặc biệt không yêu cầu cấu hình TTL.




FILE: 18-aws-route53-cname-vs-alias-records.md


# AWS Route 53: So sánh CNAME và Alias Records

## Tổng quan

Hướng dẫn này giải thích sự khác biệt giữa CNAME và Alias records trong AWS Route 53, bao gồm các trường hợp sử dụng, hạn chế và cách triển khai thực tế.

## Hiểu vấn đề

Khi bạn có một AWS Resource (ví dụ: Load Balancer hoặc CloudFront), nó sẽ cung cấp một hostname. Bạn thường muốn ánh xạ hostname đó tới một domain bạn sở hữu. Ví dụ: ánh xạ Load Balancer tới `myapp.mydomain.com`.

## Hai giải pháp: CNAME vs Alias

### CNAME Records

**CNAME là gì?**
- CNAME cho phép bạn trỏ một hostname tới bất kỳ hostname nào khác
- Ví dụ: `app.mydomain.com` → `blabla.anything.com`

**Hạn chế:**
- ❌ Chỉ hoạt động với **tên miền phụ** (ví dụ: `something.mydomain.com`)
- ❌ **KHÔNG** hoạt động với apex/root domain (ví dụ: `mydomain.com`)
- 💰 Áp dụng phí truy vấn DNS tiêu chuẩn

### Alias Records

**Alias là gì?**
- Đặc thù của Route 53
- Cho phép bạn trỏ hostname tới một AWS Resource cụ thể
- Ví dụ: `app.mydomain.com` → `blabla.amazonaws.com`

**Ưu điểm:**
- ✅ Hoạt động với cả **root domain** và **non-root domain**
- ✅ Có thể sử dụng `mydomain.com` (apex) trỏ tới AWS resources
- ✅ **Miễn phí** - không có phí truy vấn DNS
- ✅ Khả năng **health check tích hợp sẵn**
- ✅ Tự động cập nhật khi IP của tài nguyên thay đổi

## Chi tiết về Alias Record

### Đặc điểm chính

- **Đặc thù AWS**: Chỉ ánh xạ tới các tài nguyên AWS
- **Mở rộng DNS**: Mở rộng chức năng DNS tiêu chuẩn
- **Tự động cập nhật**: Tự động nhận biết thay đổi IP trong tài nguyên (ví dụ: ALB)
- **Hỗ trợ Zone Apex**: Có thể sử dụng cho node cao nhất của DNS namespace (Zone Apex)
- **Loại Record**: Luôn là **A** (IPv4) hoặc **AAAA** (IPv6)
- **TTL**: Không thể đặt thủ công - được Route 53 tự động thiết lập

### Các đích hỗ trợ cho Alias

Alias records có thể trỏ tới:
- ✅ Elastic Load Balancers (ELB, ALB, NLB)
- ✅ CloudFront Distributions
- ✅ API Gateway
- ✅ Elastic Beanstalk environments
- ✅ S3 Websites (không phải S3 Buckets, chỉ khi được bật như websites)
- ✅ VPC Interface Endpoints
- ✅ Global Accelerator
- ✅ Route 53 records trong cùng hosted zone

**Hạn chế quan trọng:**
- ❌ **KHÔNG thể** đặt alias cho EC2 DNS name

## Ví dụ thực hành

### Tạo CNAME Record

1. Truy cập Route 53 và tạo record
2. **Subdomain**: `myapp.stephanetheteacher.com`
3. **Record Type**: CNAME
4. **Value**: Tên DNS của ALB (ví dụ: `my-alb-123456.us-east-1.elb.amazonaws.com`)
5. Tạo record

**Kết quả:** Truy cập `myapp.stephanetheteacher.com` sẽ chuyển hướng tới ALB

### Tạo Alias Record

1. Tạo record mới
2. **Subdomain**: `myalias.stephanetheteacher.com`
3. **Record Type**: A (cho IPv4 traffic)
4. **Enable Alias**: Có
5. **Route traffic to**: Application and Classic Load Balancer
6. **Region**: Chọn region của bạn (ví dụ: eu-central-1)
7. **Load Balancer**: Chọn ALB của bạn
8. **Evaluate target health**: Có
9. Tạo record

**Kết quả:** 
- Truy cập `myalias.stephanetheteacher.com` hoạt động tương tự
- Truy vấn này **miễn phí** (không có phí Route 53 query)

### Thử thách với Apex Domain

**Thử tạo CNAME tại Apex (Sẽ không hoạt động):**
1. Thử tạo CNAME record không có subdomain (apex: `stephanetheteacher.com`)
2. Trỏ tới tên DNS của ALB
3. **Lỗi**: "Bad request. CNAME is not permitted at apex of this zone"

**Giải pháp - Sử dụng Alias:**
1. Tạo record không có subdomain (apex)
2. **Record Type**: A
3. **Enable Alias**: Có
4. **Route traffic to**: Application and Classic Load Balancer
5. Chọn region và load balancer
6. Tạo record

**Kết quả:** Truy cập thành công ứng dụng qua `stephanetheteacher.com` (apex domain)

## Điểm quan trọng cho kỳ thi

🎯 **Ghi nhớ cho các kỳ thi AWS:**
1. CNAME không thể được sử dụng tại Zone Apex (root domain)
2. Alias records CÓ THỂ được sử dụng tại Zone Apex
3. Alias records miễn phí
4. Alias records có khả năng health check tích hợp
5. EC2 DNS names không thể là đích cho Alias records
6. Alias records là đặc thù của AWS (không phải DNS tiêu chuẩn)

## Tóm tắt

| Tính năng | CNAME | Alias |
|-----------|-------|-------|
| Hoạt động tại apex | ❌ Không | ✅ Có |
| Chi phí | Tính phí | Miễn phí |
| Health checks | Không | Có |
| Đặc thù AWS | Không | Có |
| Loại record | CNAME | A hoặc AAAA |
| Kiểm soát TTL | Có | Không (tự động) |
| Đích | Bất kỳ hostname | Chỉ AWS resources |

## Kết luận

Hiểu rõ sự khác biệt giữa CNAME và Alias records là rất quan trọng để cấu hình AWS Route 53. Alias records cung cấp nhiều ưu điểm khi làm việc với các tài nguyên AWS, đặc biệt là cho apex domain và tối ưu hóa chi phí.




FILE: 19-aws-route53-simple-routing-policy.md


# AWS Route 53 - Chính Sách Định Tuyến Đơn Giản (Simple Routing Policy)

## Giới Thiệu Về Chính Sách Định Tuyến

Chính sách định tuyến Route 53 giúp phản hồi các truy vấn DNS. Điều quan trọng là không nên nhầm lẫn định tuyến DNS với định tuyến load balancer:

- **Định tuyến DNS**: KHÔNG định tuyến lưu lượng thực tế
- **Định tuyến Load Balancer**: Định tuyến lưu lượng đến các instance EC2 backend

DNS chỉ phản hồi các truy vấn DNS, giúp client biết nên sử dụng endpoint nào. DNS chuyển đổi tên máy chủ thành các endpoint thực tế mà client có thể sử dụng cho các truy vấn HTTP.

## Các Loại Chính Sách Định Tuyến Route 53

Route 53 hỗ trợ các chính sách định tuyến sau:

1. **Simple (Đơn giản)**
2. **Weighted (Có trọng số)**
3. **Failover (Chuyển đổi dự phòng)**
4. **Latency-based (Dựa trên độ trễ)**
5. **Geolocation (Vị trí địa lý)**
6. **Multi-value answer (Đa giá trị)**
7. **Geoproximity (Địa lý gần)**

## Chính Sách Định Tuyến Đơn Giản (Simple Routing Policy)

### Tổng Quan

Chính sách định tuyến Simple được sử dụng để định tuyến lưu lượng đến một tài nguyên duy nhất, mặc dù nó có thể chỉ định nhiều giá trị trong cùng một bản ghi.

### Đặc Điểm Chính

- **Mục Tiêu Tài Nguyên Đơn**: Thường định tuyến đến một tài nguyên
- **Nhiều Giá Trị**: Có thể chỉ định nhiều giá trị trong cùng một bản ghi
- **Lựa Chọn Ngẫu Nhiên**: Nếu nhiều giá trị được trả về, client sẽ chọn ngẫu nhiên một giá trị
- **Bản Ghi Alias**: Chỉ có thể chỉ định một tài nguyên AWS làm mục tiêu khi sử dụng bản ghi alias
- **Không Có Health Check**: Không thể kết hợp với health check

### Cách Hoạt Động

**Ví dụ Giá Trị Đơn:**
```
Client → foo.example.com
Route 53 → Trả về địa chỉ IP đơn (bản ghi A)
```

**Ví dụ Nhiều Giá Trị:**
```
Client → foo.example.com
Route 53 → Trả về ba địa chỉ IP được nhúng trong bản ghi A
Client → Chọn ngẫu nhiên một địa chỉ IP
```

## Hướng Dẫn Thực Hành

### Tạo Bản Ghi Simple Routing Policy

1. **Tạo bản ghi:**
   - Tên bản ghi: `simple.stephanetheteacher.com`
   - Loại bản ghi: A record
   - Giá trị: IP instance trong `ap-southeast-1`
   - TTL: 20 giây
   - Chính sách định tuyến: Simple

2. **Kiểm tra bản ghi:**
   - Truy cập `simple.stephanetheteacher.com`
   - Kết quả: "Hello World from my instance in ap-southeast-1b"

3. **Xác minh bằng lệnh dig:**
   ```bash
   sudo yum install bind-utils
   dig simple.stephanetheteacher.com
   ```
   - Hiển thị bản ghi A với TTL 20 giây trỏ đến IP

### Thêm Nhiều IP Vào Bản Ghi Simple

1. **Chỉnh sửa bản ghi:**
   - Thêm nhiều địa chỉ IP:
     - Một địa chỉ trong `ap-southeast-1`
     - Một địa chỉ trong `us-east-1`
   
2. **Lưu và đợi TTL hết hạn** (20 giây)

3. **Xác minh bằng CloudShell:**
   ```bash
   dig simple.stephanetheteacher.com
   ```
   - Trả về hai địa chỉ IP trong phản hồi
   - Lựa chọn phía client quyết định sử dụng IP nào

4. **Kiểm tra hành vi:**
   - Làm mới trang web
   - Cơ hội ngẫu nhiên (50/50) để kết nối đến một trong hai vùng
   - Sau khi TTL hết hạn, có thể kết nối đến vùng khác
   - Ví dụ: Lần đầu kết nối đến `ap-southeast-1b`, sau đó đến `us-east-1a`

## Kết Luận

Chính sách định tuyến Simple thể hiện chức năng bản ghi DNS cơ bản với:
- Cấu hình dễ dàng
- Hỗ trợ nhiều giá trị
- Lựa chọn ngẫu nhiên phía client
- Không tích hợp health check

Đây là nền tảng để hiểu các chính sách định tuyến Route 53 phức tạp hơn.




FILE: 2-aws-rds-read-replicas-and-multi-az.md


# AWS RDS: Read Replicas và Multi-AZ

## Tổng Quan

Hiểu được sự khác biệt giữa RDS Read Replicas và Multi-AZ là vô cùng quan trọng cho các kỳ thi AWS. Hướng dẫn này trình bày các trường hợp sử dụng, cấu hình và thực hành tốt nhất của chúng.

## RDS Read Replicas

### Read Replicas Là Gì?

Read Replicas giúp bạn mở rộng khả năng đọc dữ liệu bằng cách tạo các instance cơ sở dữ liệu bổ sung có thể xử lý lưu lượng đọc. Điều này hữu ích khi instance cơ sở dữ liệu chính của bạn nhận quá nhiều yêu cầu đọc và không thể mở rộng đủ.

### Tính Năng Chính

- **Khả năng mở rộng**: Tạo tối đa **15 Read Replicas**
- **Tùy chọn triển khai**:
  - Trong cùng một availability zone
  - Cross availability zone (giữa các AZ)
  - Cross region (giữa các vùng)

### Cơ Chế Nhân Bản

- **Nhân bản bất đồng bộ (Asynchronous Replication)**: Dữ liệu được nhân bản bất đồng bộ giữa instance cơ sở dữ liệu RDS chính và các Read Replicas
- **Eventually Consistent (Nhất quán cuối cùng)**: Các thao tác đọc là nhất quán cuối cùng, nghĩa là nếu ứng dụng của bạn đọc từ Read Replica trước khi nó nhân bản dữ liệu mới nhất, bạn có thể nhận được dữ liệu cũ

### Thăng Cấp Thành Cơ Sở Dữ Liệu Độc Lập

Read Replicas có thể được thăng cấp thành cơ sở dữ liệu độc lập:
- Sau khi thăng cấp, replica thoát khỏi cơ chế nhân bản
- Nó trở thành cơ sở dữ liệu độc lập với vòng đời riêng
- Sau đó nó có thể chấp nhận các thao tác ghi

### Yêu Cầu Triển Khai

Để sử dụng Read Replicas hiệu quả:
- Cập nhật connection string của ứng dụng để tận dụng tất cả Read Replicas
- Phân phối lưu lượng đọc trên các replica

## Trường Hợp Sử Dụng: Phân Tích và Báo Cáo

### Tình Huống

Một cơ sở dữ liệu production đang xử lý tải bình thường với các thao tác đọc và ghi. Một nhóm mới muốn chạy báo cáo và phân tích trên dữ liệu.

### Vấn Đề

Kết nối ứng dụng báo cáo trực tiếp vào instance cơ sở dữ liệu RDS chính sẽ:
- Làm quá tải cơ sở dữ liệu
- Làm chậm ứng dụng production

### Giải Pháp

1. Tạo một Read Replica
2. Nhân bản bất đồng bộ xảy ra giữa cơ sở dữ liệu chính và Read Replica
3. Ứng dụng báo cáo thực hiện đọc từ Read Replica
4. Ứng dụng production không bị ảnh hưởng

### Ràng Buộc Quan Trọng

Read Replicas chỉ hỗ trợ **các câu lệnh SELECT** (thao tác đọc):
- ✅ **Được phép**: Các truy vấn SELECT
- ❌ **Không được phép**: Các thao tác INSERT, UPDATE, DELETE

## Chi Phí Mạng Cho Read Replicas

### Nhân Bản Trong Cùng Region

**Không tính phí bổ sung** khi Read Replica ở cùng region nhưng khác availability zone:
- Ví dụ: Instance RDS ở `us-east-1a` với Read Replica ở `us-east-1b`
- Lưu lượng nhân bản là **miễn phí** vì RDS là dịch vụ được quản lý
- Truyền dữ liệu giữa các AZ được bao gồm miễn phí

### Nhân Bản Cross-Region

**Phát sinh chi phí mạng** khi Read Replica ở region khác:
- Ví dụ: Instance RDS ở `us-east-1` với Read Replica ở `eu-west-1`
- Lưu lượng nhân bản cross-region sẽ phát sinh phí nhân bản

## RDS Multi-AZ

### Mục Đích

Multi-AZ chủ yếu được sử dụng cho **Disaster Recovery (Khôi phục thảm họa)** và **tính sẵn sàng cao**, không phải để mở rộng quy mô.

### Kiến Trúc

- **Master Database**: Nằm ở Availability Zone A
- **Standby Database**: Nằm ở Availability Zone B
- **Nhân bản đồng bộ (Synchronous Replication)**: Mọi thay đổi ở Master được nhân bản đồng bộ sang Standby

### Cách Hoạt Động

1. Ứng dụng thực hiện đọc và ghi vào Master database
2. Các thay đổi được nhân bản đồng bộ sang Standby instance
3. Cả Master và Standby chia sẻ **một tên DNS**
4. Trong trường hợp lỗi, tự động failover sang Standby database

### Các Tình Huống Failover

Failover tự động xảy ra trong trường hợp:
- Mất toàn bộ availability zone
- Lỗi mạng
- Lỗi instance
- Lỗi storage trên Master database

### Đặc Điểm Chính

- **Failover không downtime**: Ứng dụng tự động kết nối lại qua tên DNS
- **Không cần can thiệp thủ công**: Failover hoàn toàn tự động
- **Không phải để mở rộng**: Standby database:
  - Không thể đọc từ nó
  - Không thể ghi vào nó
  - Chỉ tồn tại cho mục đích failover

## Kết Hợp Read Replicas và Multi-AZ

### Câu Hỏi

Có thể thiết lập Read Replicas với Multi-AZ cho Disaster Recovery không?

### Trả Lời

**Có!** Bạn có thể cấu hình Read Replicas của mình với Multi-AZ được bật. Đây là một câu hỏi thi phổ biến.

## Chuyển Đổi Từ Single-AZ Sang Multi-AZ

### Thao Tác Không Downtime

Chuyển đổi cơ sở dữ liệu RDS từ Single-AZ sang Multi-AZ là **thao tác không downtime**:
- Không cần dừng cơ sở dữ liệu
- Chỉ cần nhấp "Modify" cho cơ sở dữ liệu và bật Multi-AZ

### Quy Trình Diễn Ra Phía Sau

1. **Tạo Snapshot**: RDS tự động tạo snapshot của cơ sở dữ liệu chính
2. **Khôi phục**: Snapshot được khôi phục để tạo Standby database mới
3. **Đồng bộ hóa**: Thiết lập đồng bộ hóa giữa Master và Standby
4. **Catch-up**: Standby database bắt kịp Master database
5. **Hoàn tất**: Thiết lập Multi-AZ sẵn sàng

## Bảng Tóm Tắt Sự Khác Biệt

| Tính Năng | Read Replicas | Multi-AZ |
|-----------|--------------|----------|
| **Mục đích chính** | Mở rộng thao tác đọc | Khôi phục thảm họa & tính sẵn sàng cao |
| **Loại nhân bản** | Bất đồng bộ | Đồng bộ |
| **Số lượng instances** | Tối đa 15 replicas | 1 standby instance |
| **Thao tác đọc** | Có - trường hợp sử dụng chính | Không - standby là passive |
| **Thao tác ghi** | Không (trừ khi được thăng cấp) | Chỉ trên Master |
| **Failover tự động** | Không | Có |
| **Trường hợp sử dụng** | Workload nặng về đọc, phân tích | Tính sẵn sàng cao, chịu lỗi |
| **Tùy chọn triển khai** | Cùng AZ, Cross-AZ, Cross-Region | Chỉ Cross-AZ |

## Mẹo Cho Kỳ Thi

1. **Hiểu rõ sự khác biệt** giữa Read Replicas (mở rộng) và Multi-AZ (khôi phục thảm họa)
2. **Ghi nhớ**: Read Replicas sử dụng nhân bản bất đồng bộ; Multi-AZ sử dụng đồng bộ
3. **Biết rằng**: Chuyển đổi sang Multi-AZ là thao tác không downtime
4. **Nhớ**: Có thể tạo tối đa 15 Read Replicas
5. **Quan trọng**: Read Replicas có thể được cấu hình với Multi-AZ được bật
6. **Nhận thức về chi phí**: Read Replicas cùng region không có chi phí nhân bản; cross-region thì có

## Kết Luận

Hiểu về RDS Read Replicas và Multi-AZ là rất quan trọng cho kỳ thi AWS. Hãy nhớ rằng Read Replicas dùng để mở rộng khả năng đọc, trong khi Multi-AZ dùng cho khôi phục thảm họa. Cả hai có thể được sử dụng cùng nhau để tạo kiến trúc cơ sở dữ liệu có tính sẵn sàng cao và khả năng mở rộng.




FILE: 20-aws-route53-weighted-routing-policy.md


# AWS Route 53 - Chính Sách Định Tuyến Có Trọng Số (Weighted Routing Policy)

## Tổng Quan

**Chính sách định tuyến có trọng số (Weighted Routing Policy)** trong AWS Route 53 cho phép bạn kiểm soát phần trăm các yêu cầu được chuyển đến các tài nguyên cụ thể bằng cách sử dụng trọng số. Điều này cho phép phân phối lưu lượng chính xác trên nhiều điểm cuối.

## Cách Thức Hoạt Động

### Khái Niệm Cơ Bản

- Amazon Route 53 có thể phân phối lưu lượng truy cập trên nhiều EC2 instance (hoặc tài nguyên khác) dựa trên trọng số được gán
- Ví dụ: Ba EC2 instance với trọng số là 70, 20 và 10
- 70% phản hồi DNS chuyển hướng đến instance thứ nhất, 20% đến instance thứ hai và 10% đến instance thứ ba

### Tính Toán Trọng Số

Phần trăm lưu lượng gửi đến mỗi bản ghi được tính như sau:

```
Phần Trăm Lưu Lượng = (Trọng Số của Bản Ghi) / (Tổng Tất Cả Trọng Số)
```

**Lưu Ý Quan Trọng:**
- Trọng số không cần phải tổng bằng 100
- Trọng số là chỉ số tương đối của phân phối lưu lượng
- Các bản ghi DNS phải có cùng tên và loại
- Có thể được liên kết với health checks (kiểm tra sức khỏe)

## Các Trường Hợp Sử Dụng

1. **Cân Bằng Tải**: Phân phối lưu lượng trên các vùng khác nhau
2. **Kiểm Thử A/B**: Gửi một lượng nhỏ lưu lượng để kiểm tra phiên bản ứng dụng mới
3. **Di Chuyển Dần Dần**: Chuyển dịch lưu lượng theo thời gian bằng cách điều chỉnh trọng số
4. **Kiểm Soát Lưu Lượng**: Đặt trọng số về 0 để ngừng gửi lưu lượng đến tài nguyên cụ thể

**Trường Hợp Đặc Biệt**: Nếu tất cả các bản ghi tài nguyên có trọng số bằng 0, tất cả các bản ghi sẽ được trả về với trọng số bằng nhau.

## Hướng Dẫn Thực Hành

### Bước 1: Tạo Bản Ghi Có Trọng Số Đầu Tiên

1. Tạo bản ghi mới: `weighted.stephanetheteacher.com`
2. Loại bản ghi: **A record**
3. Chính sách định tuyến: **Weighted** (Có trọng số)
4. Giá trị: IP từ vùng `ap-southeast-1`
5. Trọng số: **10**
6. TTL: **3 giây** (chỉ để demo - không khuyến nghị cho môi trường production)
7. Record ID: **southeast**

### Bước 2: Tạo Bản Ghi Có Trọng Số Thứ Hai

1. Cùng tên miền: `weighted.stephanetheteacher.com`
2. Chính sách định tuyến: **Weighted**
3. Giá trị: IP từ vùng `us-east-1`
4. Trọng số: **70**
5. TTL: **3 giây**
6. Record ID: **US East**

### Bước 3: Tạo Bản Ghi Có Trọng Số Thứ Ba

1. Cùng tên miền: `weighted.stephanetheteacher.com`
2. Chính sách định tuyến: **Weighted**
3. Giá trị: IP từ vùng `eu-central-1`
4. Trọng số: **20**
5. TTL: **3 giây**
6. Record ID: **EU**

### Bước 4: Xác Minh Cấu Hình

Sau khi tạo các bản ghi, bạn sẽ thấy:
- **Ba bản ghi riêng biệt** trong bảng (khác với định tuyến đơn giản chỉ hiển thị một bản ghi với nhiều giá trị)
- Mỗi bản ghi có một giá trị với trọng số tương ứng (10, 20, 70)

## Kiểm Tra Định Tuyến Có Trọng Số

### Kiểm Tra Trên Trình Duyệt

1. Truy cập `weighted.stephanetheteacher.com`
2. Phản hồi đầu tiên có thể từ `us-east-1a` (trọng số 70%)
3. Làm mới trang mỗi 3 giây để thấy các phản hồi khác nhau
4. Đôi khi, bạn sẽ nhận được phản hồi từ các vùng khác dựa trên trọng số của chúng

### Kiểm Tra Bằng Dòng Lệnh

Sử dụng lệnh `dig` để xem phản hồi DNS:

```bash
dig weighted.stephanetheteacher.com
```

**Kết Quả Mong Đợi:**
- TTL là 3 giây
- Hầu hết phản hồi từ us-east-1 (xác suất 70%)
- Đôi khi có phản hồi từ eu-central-1 (xác suất 20%)
- Hiếm khi có phản hồi từ ap-southeast-1 (xác suất 10%)

## Những Điểm Chính Cần Nhớ

- Định tuyến có trọng số chuyển hướng hầu hết các truy vấn đến các bản ghi có trọng số cao hơn
- Các bản ghi khác vẫn nhận lưu lượng tỷ lệ thuận với trọng số của chúng
- Hệ thống hoạt động chính xác như thiết kế - cung cấp phân phối lưu lượng theo xác suất
- Hoàn hảo cho các kịch bản triển khai dần dần và cân bằng tải

## Những Lưu Ý Quan Trọng

- **Cài Đặt TTL**: TTL 3 giây được sử dụng trong demo này chỉ để minh họa. Hãy sử dụng giá trị TTL phù hợp trong môi trường production
- **Health Checks**: Có thể được liên kết với các bản ghi có trọng số để chuyển đổi dự phòng tự động
- **Trọng Số Bằng Không**: Đặt trọng số về 0 sẽ ngừng lưu lượng đến tài nguyên đó một cách hiệu quả

---

**Ghi Chú**: Chính sách định tuyến này thể hiện sức mạnh và tính linh hoạt của weighted records trong Route 53 cho các chiến lược quản lý lưu lượng phức tạp.




FILE: 21-aws-route53-latency-based-routing-policy.md


# AWS Route 53 - Chính Sách Định Tuyến Dựa Trên Độ Trễ (Latency-Based Routing Policy)

## Tổng Quan

Chính sách định tuyến dựa trên độ trễ là một trong những chính sách định tuyến dễ hiểu nhất trong AWS Route 53. Chính sách này chuyển hướng người dùng đến tài nguyên có độ trễ thấp nhất, rất lý tưởng khi độ trễ là mối quan tâm chính cho trang web hoặc ứng dụng của bạn.

## Cách Hoạt Động

### Đo Lường Độ Trễ

Độ trễ được đo dựa trên tốc độ người dùng có thể kết nối đến vùng AWS gần nhất được xác định cho bản ghi đó. Route 53 đánh giá độ trễ và tự động định tuyến lưu lượng đến vị trí tối ưu.

### Ví Dụ Kịch Bản

- **Vị trí người dùng**: Đức
- **Vùng có độ trễ thấp nhất**: Mỹ
- **Kết quả**: Người dùng sẽ được chuyển hướng đến tài nguyên ở Mỹ

Chính sách định tuyến này có thể được kết hợp với kiểm tra sức khỏe (health checks) để tăng cường độ tin cậy.

## Ví Dụ Kiến Trúc

Xem xét một kịch bản triển khai với các ứng dụng ở hai vùng khác nhau:
- **us-east-1** (Mỹ Đông - Virginia)
- **ap-southeast-1** (Châu Á Thái Bình Dương - Singapore)

Người dùng phân bố trên toàn cầu sẽ được tự động định tuyến:
- Người dùng có độ trễ thấp nhất đến **us-east-1** → Được chuyển đến ALB ở Mỹ
- Người dùng khác → Được chuyển đến **ap-southeast-1**

## Triển Khai Thực Hành

### Tạo Các Bản Ghi Độ Trễ

#### Bản Ghi 1: Châu Á Thái Bình Dương (Singapore)

1. **Tên bản ghi**: `latency.stephanetheteacher.com`
2. **Giá trị**: Địa chỉ IP từ ap-southeast-1
3. **Chính sách định tuyến**: Latency (Độ trễ)
4. **Vùng**: ap-southeast-1 (Singapore)
5. **ID bản ghi**: ap-southeast-1

**Lưu ý**: Khi sử dụng địa chỉ IP, bạn phải chỉ định vùng thủ công vì Route 53 không thể tự động xác định vùng chỉ từ địa chỉ IP.

#### Bản Ghi 2: Mỹ Đông

1. **Tên bản ghi**: `latency.stephanetheteacher.com`
2. **Giá trị**: Địa chỉ IP từ us-east-1
3. **Chính sách định tuyến**: Latency (Độ trễ)
4. **Vùng**: us-east-1
5. **ID bản ghi**: us-east-1

#### Bản Ghi 3: Châu Âu (Frankfurt)

1. **Tên bản ghi**: `latency.stephanetheteacher.com`
2. **Giá trị**: Địa chỉ IP từ eu-central-1
3. **Chính sách định tuyến**: Latency (Độ trễ)
4. **Vùng**: eu-central-1
5. **ID bản ghi**: eu-central-1

## Kiểm Tra Cấu Hình

### Kiểm Tra Từ Châu Âu

**Vị trí**: Châu Âu
**Kết quả mong đợi**: Được định tuyến đến eu-central-1

```bash
# Sử dụng lệnh dig
dig latency.stephanetheteacher.com
```

**Phản hồi**: Trả về địa chỉ IP của instance eu-central-1c
**Kiểm tra trình duyệt**: Hiển thị "Hello World from eu-central-1c"

### Kiểm Tra Từ Canada (sử dụng VPN)

**Vị trí**: Canada
**Kết quả mong đợi**: Được định tuyến đến us-east-1 (vùng Mỹ gần nhất)

**Phản hồi**: Trả về "Hello World from us-east-1a"

**Lưu ý**: Thay đổi vị trí qua VPN sẽ xóa bộ nhớ cache DNS cục bộ, cho phép cập nhật định tuyến ngay lập tức.

### Kiểm Tra Từ Hồng Kông (sử dụng VPN)

**Vị trí**: Hồng Kông (gần Singapore)
**Kết quả mong đợi**: Được định tuyến đến ap-southeast-1

**Phản hồi**: Trả về "Hello World from ap-southeast-1b"

## Những Điểm Quan Trọng Cần Lưu Ý

### Kiểm Tra Với CloudShell

Khi sử dụng AWS CloudShell để kiểm tra:
- Vị trí của CloudShell được cố định ở vùng mà nó được khởi chạy
- Nếu CloudShell ở eu-central-1, các truy vấn DNS sẽ luôn phân giải đến vùng gần nhất từ vị trí đó
- Thay đổi VPN cục bộ không ảnh hưởng đến hành vi định tuyến của CloudShell

### Bộ Nhớ Cache DNS và TTL

- Bộ nhớ cache DNS cục bộ tuân thủ giá trị TTL (Time To Live)
- Thay đổi vị trí vật lý (hoặc sử dụng VPN) có thể xóa bộ nhớ cache DNS cục bộ
- CloudShell duy trì bộ nhớ cache DNS riêng độc lập với máy cục bộ

## Lợi Ích Của Định Tuyến Dựa Trên Độ Trễ

1. **Cải Thiện Trải Nghiệm Người Dùng**: Người dùng tự động được chuyển đến tài nguyên nhanh nhất có sẵn
2. **Hiệu Suất Toàn Cầu**: Tối ưu hóa hiệu suất cho người dùng phân bố trên toàn thế giới
3. **Tối Ưu Hóa Tự Động**: Route 53 liên tục đánh giá và định tuyến dựa trên độ trễ thời gian thực
4. **Trường Hợp Sử Dụng Phổ Biến**: Rất phổ biến và thường được sử dụng cho các ứng dụng production

## Thực Hành Tốt Nhất

- Triển khai ứng dụng ở nhiều vùng để tối đa hóa tối ưu hóa độ trễ
- Kết hợp với kiểm tra sức khỏe để chuyển đổi dự phòng tự động
- Sử dụng giá trị TTL phù hợp để cân bằng giữa chi phí truy vấn DNS và tính linh hoạt định tuyến
- Kiểm tra từ nhiều vị trí địa lý để xác minh hành vi định tuyến

## Kết Luận

Chính sách định tuyến dựa trên độ trễ là một lựa chọn tuyệt vời cho các ứng dụng mà trải nghiệm người dùng và hiệu suất là quan trọng. Chúng hoạt động liền mạch với cơ sở hạ tầng toàn cầu của AWS để cung cấp các quyết định định tuyến tối ưu một cách tự động.




FILE: 22-aws-route53-health-checks-overview.md


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




FILE: 23-aws-route53-health-checks-hands-on-tutorial.md


# AWS Route 53 Health Checks - Hướng Dẫn Thực Hành

## Tổng Quan

Hướng dẫn này trình bày cách tạo và cấu hình health checks trong AWS Route 53 để giám sát các EC2 instance trên nhiều region. Chúng ta sẽ khám phá các loại health check khác nhau bao gồm giám sát endpoint, calculated health checks và giám sát dựa trên CloudWatch alarm.

## Tạo Health Checks Cơ Bản

### Bước 1: Truy Cập Health Checks

1. Điều hướng đến Route 53 console
2. Ở menu bên trái, click vào **Health Checks**
3. Chúng ta sẽ tạo health checks cho tất cả các EC2 instance

### Bước 2: Tạo Health Check Đầu Tiên (US East 1)

1. Click **Create Health Check**
2. Cấu hình các thiết lập sau:
   - **Name**: US East 1
   - **Type**: Endpoint
   - **Specify endpoint by**: IP address (hoặc domain name)
   - **IP Address**: Nhập IP của instance US East 1
   - **Port**: 80 (cổng HTTP)
   - **Path**: `/` (thư mục gốc của website)

> **Lưu ý**: Trong các ứng dụng thực tế, thường sử dụng một endpoint health chuyên dụng như `/health` để trả về trạng thái sức khỏe của ứng dụng.

### Bước 3: Cấu Hình Nâng Cao

Xem xét các thiết lập nâng cao:

- **Interval** (Khoảng thời gian):
  - Standard (mỗi 30 giây) - được khuyến nghị để tiết kiệm chi phí
  - Fast (mỗi 10 giây) - tùy chọn đắt hơn

- **Failure Threshold** (Ngưỡng lỗi): Số lần thất bại liên tiếp trước khi đánh dấu là không khỏe mạnh

- **String Matching** (Khớp chuỗi): Tùy chọn tìm kiếm một chuỗi cụ thể trong 5,120 bytes đầu tiên của phản hồi

- **Latency Graph** (Biểu đồ độ trễ): Bật để theo dõi xu hướng độ trễ theo thời gian

- **Invert Health Check Status** (Đảo ngược trạng thái): Đảo ngược trạng thái khỏe mạnh/không khỏe mạnh

- **Health Checker Regions** (Các region kiểm tra): Sử dụng khuyến nghị hoặc tùy chỉnh các region cụ thể

- **Alarm Notification** (Thông báo cảnh báo): Tùy chọn tạo CloudWatch alarm để nhận thông báo (chọn No cho hướng dẫn này)

### Bước 4: Tạo Các Health Check Bổ Sung

Lặp lại quy trình cho các region khác:

**Health Check Thứ Hai (AP Southeast 1 - Singapore)**
1. Tạo health check
2. Name: AP Southeast 1
3. Nhập địa chỉ IP (không phải hostname)
4. Click Next và Create

**Health Check Thứ Ba (EU Central 1)**
1. Tạo health check
2. Name: EU Central 1
3. Nhập địa chỉ IP
4. Click Next và Create

## Kiểm Tra Lỗi Health Check

Để xác minh health checks hoạt động đúng, chúng ta sẽ mô phỏng một lỗi:

1. Điều hướng đến EC2 console
2. Chọn instance Singapore
3. Vào **Security Group** liên quan
4. Click **Actions** → **Edit Inbound Rules**
5. Xóa quy tắc HTTP (cổng 80)
6. Lưu thay đổi

**Kết quả**: Health check cho AP Southeast 1 sẽ chuyển sang trạng thái **Unhealthy** sau khi đạt ngưỡng lỗi.

## Giám Sát Trạng Thái Health Check

Sau một khoảng thời gian ngắn (30-60 giây), bạn sẽ thấy:

- **Ba health checks** đã được tạo
- **Một không khỏe mạnh** (AP Southeast 1 - do security group bị chặn)
- **Hai khỏe mạnh** (US East 1 và EU Central 1)

### Xem Chi Tiết Health Check

1. Click vào bất kỳ health check nào để xem thông tin chi tiết
2. Kiểm tra timestamp **Last Checked**
3. Đối với các health check không khỏe mạnh, click **View Last Failed Check**
   - Hiển thị chi tiết lỗi (ví dụ: "Connection timeout")
   - Chỉ ra nguyên nhân: "Requests có thể bị chặn bởi firewall" (security group)

## Các Loại Health Check Nâng Cao

### Calculated Health Checks

Calculated health checks giám sát trạng thái của các health check khác và báo cáo dựa trên kết quả kết hợp.

**Tạo Calculated Health Check:**

1. Click **Create Health Check**
2. Chọn loại **Calculated**
3. Name: "Calculated Health Check"
4. Chọn các child health check để giám sát (cả ba regional checks)
5. Cấu hình ngưỡng báo cáo:
   - Báo cáo khỏe mạnh khi **1 trong 3** khỏe mạnh (logic OR)
   - Báo cáo khỏe mạnh khi **2 trong 3** khỏe mạnh
   - Báo cáo khỏe mạnh khi **tất cả** đều khỏe mạnh (logic AND)
6. Trong ví dụ này, chọn "healthy when all checks are healthy"
7. Click Next và Create

**Kết quả**: Calculated health check sẽ hiển thị là **Unhealthy** vì một child health check (AP Southeast 1) không khỏe mạnh.

### Health Checks Dựa Trên CloudWatch Alarm

Loại này giám sát trạng thái của CloudWatch alarm, hữu ích cho việc giám sát tài nguyên private.

**Trường hợp sử dụng**: Giám sát các EC2 instance private không thể truy cập trực tiếp bởi Route 53 health checkers.

**Các Bước Cấu Hình:**
1. Tạo health check
2. Chọn **State of CloudWatch alarm**
3. Chỉ định region nơi alarm tồn tại
4. Chọn CloudWatch alarm
5. Alarm có thể giám sát các metrics từ các EC2 instance private

> **Lưu ý**: Tùy chọn này yêu cầu CloudWatch alarm đã được cấu hình sẵn.

## Lợi Ích Chính Của Route 53 Health Checks

- **Giám sát đa region**: Theo dõi sức khỏe trên toàn bộ hạ tầng toàn cầu
- **Phát hiện lỗi linh hoạt**: Tùy chỉnh ngưỡng và khoảng thời gian
- **Calculated checks**: Kết hợp nhiều checks với các phép toán logic
- **Giám sát tài nguyên private**: Sử dụng CloudWatch alarms để giám sát tài nguyên nội bộ
- **Tích hợp với Route 53 routing**: Sử dụng health checks với các routing policies (sẽ được đề cập trong bài giảng tiếp theo)

## Tóm Tắt

Trong hướng dẫn này, chúng ta đã học cách:
- Tạo endpoint-based health checks cho các EC2 instance
- Cấu hình khoảng thời gian và ngưỡng health check
- Kiểm tra lỗi health check bằng cách sử dụng quy tắc security group
- Tạo calculated health checks cho giám sát kết hợp
- Hiểu về health checks dựa trên CloudWatch alarm

Health checks là một tính năng mạnh mẽ sẽ được sử dụng cùng với Route 53 records và routing policies trong các bài học sắp tới.

## Các Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ khám phá cách sử dụng các health checks này với Route 53 routing policies để triển khai automatic failover và intelligent traffic routing.




FILE: 24-aws-route53-failover-routing-policy.md


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




FILE: 25-aws-route53-geolocation-routing-policy.md


# Chính Sách Định Tuyến Theo Vị Trí Địa Lý AWS Route 53

## Tổng Quan

**Chính Sách Định Tuyến Theo Vị Trí Địa Lý (Geolocation Routing Policy)** trong AWS Route 53 có sự khác biệt cơ bản so với chính sách định tuyến dựa trên độ trễ. Phương pháp định tuyến này dựa trên vị trí địa lý thực tế của người dùng, cho phép bạn điều hướng lưu lượng truy cập dựa trên nơi người dùng của bạn đang ở.

## Cách Hoạt Động Của Định Tuyến Theo Vị Trí Địa Lý

Định tuyến theo vị trí địa lý cho phép bạn chỉ định việc định tuyến lưu lượng dựa trên:
- Cấp độ **Châu lục**
- Cấp độ **Quốc gia**
- Cấp độ **Tiểu bang Hoa Kỳ** (chính xác nhất)

Khi có nhiều chỉ định vị trí, Route 53 sẽ chọn **vị trí khớp chính xác nhất** trước và định tuyến đến địa chỉ IP tương ứng.

## Tính Năng Chính

### Bản Ghi Mặc Định
Bạn nên luôn tạo một **bản ghi mặc định** để xử lý các trường hợp không có kết quả khớp về vị trí. Điều này đảm bảo rằng tất cả người dùng có thể truy cập ứng dụng của bạn bất kể vị trí của họ.

### Các Trường Hợp Sử Dụng
- **Bản địa hóa trang web** - Phục vụ nội dung bằng ngôn ngữ bản địa của người dùng
- **Hạn chế phân phối nội dung** - Tuân thủ các yêu cầu cấp phép theo khu vực
- **Cân bằng tải** - Phân phối lưu lượng truy cập qua các tài nguyên theo khu vực
- **Tích hợp kiểm tra sức khỏe** - Các bản ghi này có thể được liên kết với kiểm tra sức khỏe để đảm bảo tính khả dụng cao

## Ví Dụ Thực Tế

Xem xét một kịch bản với ứng dụng châu Âu:

### Cấu Hình Định Tuyến
- **Đức** → IP Đức (phiên bản tiếng Đức của ứng dụng)
- **Pháp** → IP Pháp (phiên bản tiếng Pháp của ứng dụng)
- **Mặc định** → IP mặc định (phiên bản tiếng Anh của ứng dụng)

Thiết lập này đảm bảo người dùng nhận được phiên bản bản địa hóa phù hợp dựa trên vị trí địa lý của họ.

## Hướng Dẫn Thực Hành

### Bước 1: Tạo Bản Ghi Định Tuyến Theo Vị Trí Địa Lý Cho Châu Á

1. Điều hướng đến bảng điều khiển Route 53
2. Nhấp **Create record** (Tạo bản ghi)
3. Cấu hình bản ghi:
   - **Loại bản ghi**: A
   - **Giá trị**: Liên kết đến EC2 instance `ap-southeast-1`
   - **Chính sách định tuyến**: Geolocation (Vị trí địa lý)
   - **Vị trí**: Asia (toàn châu lục)
   - **ID bản ghi**: Asia
4. Tùy chọn: Liên kết kiểm tra sức khỏe

### Bước 2: Tạo Bản Ghi Định Tuyến Theo Vị Trí Địa Lý Cho Hoa Kỳ

1. Tạo bản ghi khác
2. Cấu hình:
   - **Loại bản ghi**: A
   - **Giá trị**: Liên kết đến EC2 instance `us-east-1`
   - **Chính sách định tuyến**: Geolocation (Vị trí địa lý)
   - **Vị trí**: United States (cụ thể quốc gia)
   - **ID bản ghi**: U.S.

### Bước 3: Tạo Bản Ghi Mặc Định

1. Tạo bản ghi cuối cùng
2. Cấu hình:
   - **Loại bản ghi**: A
   - **Giá trị**: Liên kết đến EC2 instance `eu-central-1`
   - **Chính sách định tuyến**: Geolocation (Vị trí địa lý)
   - **Vị trí**: Default (Mặc định)
   - **ID bản ghi**: Default EU

Vị trí mặc định này xử lý tất cả lưu lượng truy cập không khớp với Châu Á hoặc Hoa Kỳ.

## Kiểm Tra Cấu Hình

### Kiểm Tra 1: Vị Trí Mặc Định (Châu Âu)
- **Vị trí người dùng**: Châu Âu (không phải Hoa Kỳ, không phải Châu Á)
- **Kết quả mong đợi**: Lưu lượng được định tuyến đến khu vực `eu-central-1`
- **Kết quả**: ✅ Bản ghi mặc định hoạt động đúng

### Kiểm Tra 2: Vị Trí Châu Á
1. Kết nối qua VPN đến Ấn Độ
2. Làm mới trang
3. **Kết quả mong đợi**: Lưu lượng được định tuyến đến instance `ap-southeast-1`

**Lưu Ý Khắc Phục Sự Cố**: Nếu bạn gặp timeout (hết thời gian chờ):
- Kiểm tra cài đặt **Security Groups** (Nhóm bảo mật)
- Đảm bảo quy tắc HTTP được bật trong Inbound rules (Quy tắc vào)
- Điều hướng đến đúng khu vực (ví dụ: Singapore cho ap-southeast-1)
- Thêm lại quy tắc HTTP nếu nó đã bị xóa để kiểm tra sức khỏe

### Kiểm Tra 3: Vị Trí Hoa Kỳ
- **Vị trí người dùng**: Hoa Kỳ
- **Kết quả mong đợi**: Lưu lượng được định tuyến đến `us-east-1a`
- **Kết quả**: ✅ Hoạt động hoàn hảo

### Kiểm Tra 4: Vị Trí Lân Cận (Mexico)
- **Vị trí người dùng**: Mexico (gần Hoa Kỳ nhưng là quốc gia khác)
- **Kết quả mong đợi**: Lưu lượng được định tuyến đến `eu-central-1c` (bản ghi mặc định)
- **Lý do**: Mexico không được chỉ định trong quy tắc định tuyến theo vị trí địa lý

## Những Điểm Chính Cần Ghi Nhớ

1. **Định tuyến theo vị trí địa lý** dựa trên vị trí vật lý của người dùng, không phải độ trễ mạng
2. **Độ chính xác quan trọng** - Các vị trí cụ thể hơn (tiểu bang) được ưu tiên hơn các vị trí rộng hơn (châu lục)
3. **Luôn tạo bản ghi mặc định** để xử lý các vị trí không khớp
4. **Kiểm tra sức khỏe** có thể được tích hợp để đảm bảo tính khả dụng cao
5. **Security groups** rất quan trọng - timeout thường cho thấy cấu hình sai của security groups
6. **Kiểm tra bằng VPN** là cách hiệu quả để xác minh hành vi định tuyến theo vị trí địa lý

## Kết Luận

Chính Sách Định Tuyến Theo Vị Trí Địa Lý là một công cụ mạnh mẽ để cung cấp nội dung bản địa hóa, quản lý tuân thủ theo khu vực và tối ưu hóa trải nghiệm người dùng dựa trên vị trí địa lý. Bằng cách cấu hình đúng các bản ghi định tuyến theo vị trí địa lý với các giá trị mặc định và kiểm tra sức khỏe phù hợp, bạn có thể tạo một kiến trúc ứng dụng phân tán toàn cầu mạnh mẽ.




FILE: 26-aws-route53-geoproximity-routing-policy.md


# Chính Sách Định Tuyến Geoproximity của AWS Route 53

## Tổng Quan

Định tuyến Geoproximity là một chính sách định tuyến nâng cao trong AWS Route 53 cho phép bạn định tuyến lưu lượng truy cập đến tài nguyên của mình dựa trên vị trí địa lý của người dùng và tài nguyên. Mặc dù ban đầu có vẻ phức tạp, việc hiểu khái niệm bias (độ lệch) sẽ giúp bạn sử dụng tính năng này một cách dễ dàng.

## Cách Thức Hoạt Động của Định Tuyến Geoproximity

Định tuyến Geoproximity cho phép bạn kiểm soát phân phối lưu lượng bằng cách sử dụng một giá trị số được gọi là **bias**. Tính năng này cho phép bạn chuyển nhiều hoặc ít lưu lượng hơn đến các tài nguyên cụ thể dựa trên vị trí địa lý của chúng.

### Các Khái Niệm Chính

- **Giá Trị Bias**: Một tham số số học kiểm soát kích thước vùng địa lý cho định tuyến
- **Chuyển Đổi Lưu Lượng**: Khả năng thu hút nhiều hoặc ít người dùng hơn đến các tài nguyên cụ thể
- **Phạm Vi Địa Lý**: Xác định người dùng nào được định tuyến đến tài nguyên nào

## Cấu Hình Giá Trị Bias

### Tăng Lưu Lượng Đến Một Tài Nguyên

Để hướng nhiều lưu lượng hơn đến một tài nguyên cụ thể, **tăng giá trị bias** (sử dụng số dương). Điều này mở rộng vùng địa lý được định tuyến đến tài nguyên đó.

### Giảm Lưu Lượng Đến Một Tài Nguyên

Để giảm lưu lượng đến một tài nguyên, **giảm giá trị bias** (sử dụng số âm). Điều này thu nhỏ vùng địa lý liên quan đến tài nguyên đó.

## Các Loại Tài Nguyên

Định tuyến Geoproximity hỗ trợ hai loại tài nguyên:

### Tài Nguyên AWS

- Chỉ định **AWS region** nơi tài nguyên được đặt
- Route 53 tự động tính toán định tuyến chính xác dựa trên region

### Tài Nguyên Không Thuộc AWS

- Sử dụng cho trung tâm dữ liệu tại chỗ hoặc tài nguyên bên ngoài
- Chỉ định tọa độ **vĩ độ và kinh độ**
- Cho phép Route 53 xác định vị trí tài nguyên

## Cấu Hình Nâng Cao

Để tận dụng tính năng bias, bạn cần sử dụng **Route 53 Traffic Flow**, đây là công cụ cấu hình nâng cao để tạo các chính sách định tuyến phức tạp.

## Ví Dụ Thực Tế

### Ví Dụ 1: Phân Phối Đều (Bias = 0)

**Kịch Bản**: Tài nguyên ở cả `us-west-1` và `us-east-1` với bias được đặt là 0

**Kết Quả**:
- Một đường phân chia chia Hoa Kỳ thành hai phần
- Người dùng ở phía tây đường phân chia → định tuyến đến `us-west-1`
- Người dùng ở phía đông đường phân chia → định tuyến đến `us-east-1`
- Lưu lượng được phân phối dựa hoàn toàn trên khoảng cách gần nhất đến tài nguyên

### Ví Dụ 2: Phân Phối Chuyển Dịch (Bias Dương)

**Kịch Bản**: 
- `us-west-1`: bias = 0
- `us-east-1`: bias = +50

**Kết Quả**:
- Đường phân chia dịch chuyển sang trái (về phía tây)
- Diện tích địa lý được bao phủ bởi `us-east-1` lớn hơn
- Nhiều người dùng hơn được định tuyến đến `us-east-1` do phạm vi mở rộng
- `us-east-1` thu hút thêm lưu lượng nhờ bias dương

## Các Trường Hợp Sử Dụng

Định tuyến Geoproximity đặc biệt hữu ích khi bạn cần:

- **Chuyển lưu lượng giữa các region**: Tăng bias ở region đích để thu hút nhiều người dùng hơn
- **Cân bằng tải theo khu vực**: Phân phối người dùng trên nhiều vị trí địa lý
- **Xử lý công suất theo khu vực**: Hướng nhiều lưu lượng hơn đến các region có công suất khả dụng
- **Kiểm thử triển khai theo khu vực**: Dần dần chuyển lưu lượng đến các region mới

## Lưu Ý Cho Kỳ Thi

Khi chuẩn bị cho các kỳ thi chứng chỉ AWS, hãy nhớ:

- **Định tuyến Geoproximity** là giải pháp khi bạn cần **chuyển lưu lượng từ region này sang region khác**
- Sử dụng **giá trị bias dương** để thu hút nhiều lưu lượng hơn đến một region cụ thể
- Sử dụng **giá trị bias âm** để giảm lưu lượng đến một region
- Giá trị bias kiểm soát vùng phạm vi địa lý cho các quyết định định tuyến

## Tóm Tắt

Chính sách Định tuyến Geoproximity cung cấp khả năng kiểm soát chi tiết việc phân phối lưu lượng trên các khu vực địa lý. Bằng cách điều chỉnh các giá trị bias, bạn có thể động chuyển lưu lượng người dùng để tối ưu hóa hiệu suất, quản lý công suất, hoặc hỗ trợ các yêu cầu kinh doanh cụ thể. Chính sách định tuyến này rất quan trọng đối với các ứng dụng toàn cầu cần quản lý lưu lượng địa lý linh hoạt.




FILE: 27-aws-route53-traffic-flow-geoproximity-tutorial.md


# Hướng Dẫn AWS Route 53 Traffic Flow - Định Tuyến Geoproximity

## Tổng Quan

Hướng dẫn này sẽ trình bày cách xây dựng các bản ghi geoproximity phức tạp bằng tính năng Traffic Flow của AWS Route 53. Traffic Flow cung cấp một trình soạn thảo trực quan cho phép bạn quản lý các cây quyết định định tuyến phức tạp một cách hiệu quả.

## Traffic Flow Là Gì?

Traffic Flow là một tính năng mạnh mẽ trong Route 53 cung cấp:

- **Giao Diện UI Trực Quan**: Giao diện đồ họa để quản lý các quyết định định tuyến phức tạp
- **Quản Lý Policy**: Lưu cấu hình định tuyến dưới dạng Traffic Flow Policies
- **Phiên Bản**: Theo dõi và quản lý các phiên bản khác nhau của policies
- **Khả Năng Tái Sử Dụng**: Áp dụng policies cho nhiều hosted zones khác nhau
- **Cập Nhật Dễ Dàng**: Sửa đổi và triển khai thay đổi vào hosted zones một cách nhanh chóng

Thay vì tạo các bản ghi DNS thủ công từng cái một trong Route 53, Traffic Flow cho phép bạn quản lý tất cả các quy tắc định tuyến một cách trực quan.

## Bắt Đầu Với Traffic Flow

### Bước 1: Truy Cập Traffic Policies

1. Điều hướng đến bảng điều khiển Route 53
2. Nhấp vào bảng điều khiển bên trái
3. Chọn **Traffic policies**

### Bước 2: Tạo Traffic Policy

1. Nhấp **Create a Traffic Policy**
2. Đặt tên cho policy của bạn (ví dụ: "DemoGeoPolicy")
3. Nhấp **Next**

### Bước 3: Cấu Hình Loại Record

Tại điểm khởi đầu, bạn cần chỉ định loại record muốn tạo:

- **A Record**: Địa chỉ IPv4
- **AAAA Record**: Địa chỉ IPv6
- **CNAME**: Tên chuẩn (Canonical name)
- Và các loại record khác

## Các Loại Quy Tắc Định Tuyến Có Sẵn

Traffic Flow hỗ trợ nhiều loại quy tắc định tuyến:

- **Weighted rule**: Phân phối lưu lượng dựa trên trọng số được chỉ định
- **Failover rule**: Định tuyến lưu lượng đến tài nguyên dự phòng khi tài nguyên chính gặp sự cố
- **Geolocation rule**: Định tuyến dựa trên vị trí địa lý của người dùng
- **Latency rule**: Định tuyến đến endpoint có độ trễ thấp nhất
- **Multivalue**: Trả về nhiều địa chỉ IP
- **Geoproximity**: Định tuyến dựa trên vị trí địa lý với điều chỉnh bias
- **Endpoint**: Định tuyến trực tiếp đơn giản đến một giá trị cụ thể

## Tạo Record Đơn Giản

Để cấu hình cơ bản:

1. Chọn **A record**
2. Kết nối đến một **endpoint**
3. Chỉ định địa chỉ IPv4 (ví dụ: 1.2.3.4.5.6.7)

## Xây Dựng Policies Phức Tạp

Bạn có thể tạo các policies định tuyến phức tạp bằng cách kết hợp nhiều quy tắc:

- Kết nối A record đến một **Weighted rule**
- Thêm nhiều trọng số với các giá trị khác nhau
- Kết nối thêm các quy tắc như **Failover**
- Kết nối đến các endpoints theo nhu cầu

Giao diện trực quan giúp dễ dàng hiểu và quản lý logic định tuyến phức tạp.

## Triển Khai Định Tuyến Geoproximity

### Bước 1: Chọn Geoproximity Rule

1. Chọn **Geoproximity rule** thay vì Weighted rule
2. Bật **Show Map** để có phản hồi trực quan

### Bước 2: Cấu Hình Region Đầu Tiên

1. Chọn vị trí endpoint đầu tiên
2. Chọn từ các regions của AWS hoặc nhập tọa độ tùy chỉnh
3. Trong ví dụ này: **US-East-1**
4. Đặt giá trị bias (bắt đầu với 0)
5. Kết nối đến một **endpoint** mới
6. Nhập địa chỉ IP của EC2 instance US-East-1 của bạn

### Bước 3: Cấu Hình Region Thứ Hai

1. Thêm region thứ hai
2. Trong ví dụ này: **Singapore (AP-Southeast-1)**
3. Kết nối đến một **endpoint** mới
4. Nhập địa chỉ IP của AP-Southeast-1 instance của bạn

### Bước 4: Xem Bản Đồ Geoproximity

Nhấp **Show Map** để trực quan hóa phân phối định tuyến:

- Bản đồ hiển thị đường phân chia giữa các regions
- Phía màu xanh định tuyến đến instance đầu tiên
- Phía màu cam định tuyến đến instance thứ hai

### Hiểu Về Bias

Giá trị **bias** ảnh hưởng đến phân phối địa lý của lưu lượng:

- **Bias dương** (ví dụ: +34): Tăng diện tích định tuyến đến instance đó
- **Bias âm**: Giảm diện tích, chuyển lưu lượng sang các instances khác
- **Bias bằng không**: Phân phối đồng đều dựa trên khoảng cách địa lý

Bạn có thể điều chỉnh giá trị bias và ngay lập tức thấy tác động trên bản đồ.

### Bước 5: Thêm Các Regions Bổ Sung

Bạn có thể thêm nhiều hơn hai regions:

1. Nhấp **Add another geoproximity location**
2. Trong ví dụ này: **Frankfurt (EU-Central-1)**
3. Kết nối đến một **endpoint** mới
4. Nhập địa chỉ IP cho EU-Central-1 instance
5. Điều chỉnh giá trị bias theo nhu cầu
6. Nhấp **Create traffic policy**

## Triển Khai Traffic Policy

### Bước 1: Triển Khai Policy Record

1. Nhấp **Deploy** để áp dụng policy
2. Chọn hosted zone của bạn (ví dụ: stephanetheteacher.com)
3. Đặt tên policy record (ví dụ: proximity.stephanetheteacher.com)
4. Chỉ định giá trị TTL

### Thông Tin Quan Trọng Về Giá Cả

⚠️ **Cảnh Báo Chi Phí**: Traffic Flow policy records có chi phí **$50 mỗi tháng** cho mỗi policy record. Giá được tính theo tỷ lệ dựa trên thời gian sử dụng. Nếu bạn muốn ở trong gói miễn phí của AWS, hãy tránh tạo policy records.

### Bước 2: Tạo Policy Record

Nhấp **Create policy record** để hoàn tất triển khai.

## Quản Lý Các Phiên Bản Policy

Sau khi tạo, bạn có thể:

- Xem tất cả các phiên bản policy
- Chỉnh sửa policy để tạo phiên bản mới
- Xem tất cả các records được tạo bằng policy
- Xem bản đồ geoproximity cho policy đã triển khai

## Kiểm Tra Định Tuyến Geoproximity

Sau khi policy record được áp dụng, hãy kiểm tra định tuyến:

### Kiểm Tra Từ Châu Âu
- Vị trí: Pháp
- Kết quả mong đợi: Định tuyến đến instance **EU-Central-1**

### Kiểm Tra Từ Nam Mỹ
- Vị trí: Brazil
- Kết quả mong đợi: Định tuyến đến instance **US-East-1** (instance Mỹ)

### Kiểm Tra Từ Châu Á
- Vị trí: Thái Lan
- Kết quả mong đợi: Định tuyến đến instance **AP-Southeast-1b**

## Xem Record Trong Route 53

1. Quay lại Route 53 và làm mới
2. Sử dụng **Filter** và nhập "proximity"
3. Record proximity hiển thị nó đang định tuyến đến một traffic policy record
4. Nhấp **Edit** để được đưa trực tiếp đến giao diện Traffic Policy

## Chỉnh Sửa Traffic Policy Records

Cách duy nhất để chỉnh sửa traffic policy record là thông qua giao diện Traffic Policy. Chỉnh sửa record tiêu chuẩn không khả dụng cho các records dựa trên policy.

## Dọn Dẹp

Để tránh chi phí liên tục:

1. Điều hướng đến policy records của bạn
2. Chọn policy record
3. Nhấp **Delete policy record**

Điều này ngăn chặn khoản phí $50 hàng tháng trong khi vẫn giữ policy template để sử dụng trong tương lai.

## Tóm Tắt

AWS Route 53 Traffic Flow cung cấp một giao diện trực quan mạnh mẽ để quản lý các tình huống định tuyến phức tạp, đặc biệt là định tuyến geoproximity. Lợi ích chính bao gồm:

- Tạo và quản lý policy trực quan
- Trực quan hóa bản đồ phân phối lưu lượng theo thời gian thực
- Điều chỉnh bias linh hoạt để tinh chỉnh luồng lưu lượng
- Phiên bản policy và khả năng tái sử dụng
- Hỗ trợ nhiều quy tắc định tuyến và kết hợp

Mặc dù tính năng này có giá cao ($50/tháng cho mỗi policy record), nó đơn giản hóa đáng kể việc quản lý các cấu hình định tuyến toàn cầu phức tạp.

## Các Bước Tiếp Theo

- Khám phá các policies định tuyến khác (Weighted, Latency, Failover)
- Kết hợp nhiều quy tắc định tuyến cho các tình huống nâng cao
- Kiểm tra thay đổi policy trong môi trường phát triển trước khi triển khai production
- Giám sát hiệu quả định tuyến bằng các metrics CloudWatch




FILE: 28-aws-route53-ip-based-routing-policy.md


# Chính Sách Định Tuyến Dựa Trên IP Của AWS Route 53

## Tổng Quan

Định tuyến dựa trên IP trong AWS Route 53 cho phép bạn điều hướng lưu lượng dựa trên địa chỉ IP của client. Chính sách định tuyến này cung cấp khả năng kiểm soát chi tiết việc phân phối lưu lượng bằng cách xác định các khối CIDR cụ thể (dải IP) và ánh xạ chúng đến các endpoint tương ứng.

## Cách Hoạt Động

Với định tuyến dựa trên IP, bạn xác định:
- Danh sách các khối CIDR (dải IP) cho các client của bạn
- Các vị trí hoặc endpoint cụ thể nơi lưu lượng từ mỗi khối CIDR sẽ được điều hướng đến

Route 53 sau đó sẽ định tuyến các yêu cầu đến dựa trên địa chỉ IP của client, khớp nó với các khối CIDR đã được xác định.

## Các Trường Hợp Sử Dụng

### 1. Tối Ưu Hóa Hiệu Suất
Khi bạn biết trước địa chỉ IP của client, bạn có thể định tuyến họ đến các endpoint gần hơn về mặt địa lý hoặc được tối ưu hóa hơn để cải thiện hiệu suất.

### 2. Giảm Chi Phí Mạng
Bằng cách biết các IP đến từ đâu, bạn có thể định tuyến lưu lượng hiệu quả để giảm chi phí mạng và tối ưu hóa chi tiêu cho cơ sở hạ tầng của bạn.

### 3. Định Tuyến Theo ISP Cụ Thể
Nếu bạn biết rằng một Nhà Cung Cấp Dịch Vụ Internet (ISP) cụ thể sử dụng một dải CIDR cụ thể, bạn có thể định tuyến lưu lượng của họ đến các endpoint chuyên dụng được tối ưu hóa cho nhà cung cấp đó.

## Ví Dụ Cấu Hình

### Bước 1: Xác Định Các Vị Trí Với Khối CIDR

Trong Route 53, bạn xác định các vị trí với các khối CIDR liên quan:

- **Vị trí 1**: Khối CIDR bắt đầu với `203.x.x.x`
- **Vị trí 2**: Khối CIDR bắt đầu với `200.x.x.x`

### Bước 2: Tạo Bản Ghi DNS

Liên kết các vị trí với các giá trị bản ghi cụ thể cho tên miền của bạn (ví dụ: `example.com`):

| Vị Trí | Khối CIDR | IP Endpoint | Mô Tả |
|--------|-----------|-------------|-------|
| Vị trí 1 | 203.x.x.x/x | 1.2.3.4 | EC2 Instance 1 |
| Vị trí 2 | 200.x.x.x/x | 5.6.7.8 | EC2 Instance 2 |

### Bước 3: Định Tuyến Lưu Lượng

Khi người dùng thực hiện truy vấn DNS:

- **Người dùng A** với địa chỉ IP từ khối CIDR của Vị trí 1 nhận được phản hồi DNS: `1.2.3.4`
  - Lưu lượng được điều hướng đến EC2 Instance 1
  
- **Người dùng B** với địa chỉ IP từ khối CIDR của Vị trí 2 nhận được phản hồi DNS: `5.6.7.8`
  - Lưu lượng được điều hướng đến EC2 Instance 2

## Lợi Ích

- **Kiểm Soát Chính Xác**: Định tuyến lưu lượng dựa trên các dải IP cụ thể
- **Tối Ưu Hóa Chi Phí**: Giảm chi phí mạng thông qua định tuyến thông minh
- **Hiệu Suất**: Cải thiện trải nghiệm người dùng bằng cách định tuyến đến các endpoint tối ưu
- **Linh Hoạt**: Tùy chỉnh định tuyến cho các ISP hoặc nhóm client cụ thể

## Những Điểm Chính Cần Nhớ

- Định tuyến dựa trên IP cung cấp khả năng kiểm soát chi tiết việc phân phối lưu lượng
- Lý tưởng khi bạn có các dải IP client có thể dự đoán được
- Hoàn hảo để tối ưu hóa hiệu suất và giảm chi phí
- Đơn giản để cấu hình và duy trì trong Route 53

---

*Chính sách định tuyến này đặc biệt hữu ích cho các doanh nghiệp có dải IP client đã biết hoặc khi làm việc với các ISP cụ thể để tối ưu hóa trải nghiệm của người dùng của họ.*




FILE: 29-aws-route53-multi-value-routing-policy.md


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




FILE: 3-aws-rds-hands-on-tutorial.md


# Hướng Dẫn Thực Hành AWS RDS

## Giới Thiệu

Hướng dẫn này sẽ giúp bạn tạo và quản lý một instance cơ sở dữ liệu Amazon RDS (Relational Database Service), bao gồm kết nối và thực hiện các thao tác cơ bản.

## Tạo Cơ Sở Dữ Liệu RDS

### Bước 1: Truy Cập RDS Console

1. Điều hướng đến Aurora và RDS console
2. Nhấp vào **Databases** ở thanh bên trái
3. Nhấp vào **Create database**

### Bước 2: Cấu Hình Cơ Sở Dữ Liệu

#### Chọn Engine
- Chọn giữa **Standard Create** hoặc **Easy Create**
- Cho hướng dẫn này, chọn **Standard Create** để xem tất cả các tùy chọn
- Chọn **MySQL** làm loại engine
- Giữ phiên bản engine mặc định

#### Templates (Mẫu)
Chọn từ ba tùy chọn mẫu:
- **Production**: Nhiều cài đặt hơn, triển khai multi-AZ
- **Dev/Test**: Cài đặt môi trường phát triển
- **Free Tier**: Giới hạn triển khai single AZ (khuyến nghị cho hướng dẫn này)

> **Lưu ý**: Mẫu Production cung cấp triển khai multi-AZ DB instance (2 instances) hoặc triển khai multi-AZ DB cluster (3 instances) để có tính sẵn sàng cao.

### Bước 3: Cài Đặt Cơ Sở Dữ Liệu

#### Định Danh Cơ Sở Dữ Liệu
- Giữ database identifier mặc định
- Master username: `admin`

#### Quản Lý Thông Tin Xác Thực
Bạn có hai tùy chọn:
1. **Self-managed**: Tự tạo và quản lý mật khẩu
2. **AWS Secrets Manager**: An toàn hơn nhưng có chi phí thêm

Cho hướng dẫn này:
- Chọn **Self-managed**
- Master password: Nhập mật khẩu của bạn (ví dụ: `password`)
- Xác nhận master password
- Bật **Password authentication only**

> **Lưu ý**: Xác thực IAM cũng có sẵn như một tùy chọn.

### Bước 4: Cấu Hình Instance

- **Instance type**: Chọn `db.t4g.micro` (hoặc tùy chọn free tier có sẵn)
- **Storage type**: 20 GB dung lượng được phân bổ
- **Storage autoscaling**: Tùy chọn - có thể mở rộng lên đến 1000 GB nếu cần

### Bước 5: Cài Đặt Kết Nối

- **EC2 connection**: Chọn "Don't connect to an EC2 compute resource"
- **VPC**: Sử dụng VPC mặc định
- **Subnet group**: Giữ mặc định
- **Public access**: Chọn **Yes** (để truy cập cơ sở dữ liệu với IP công khai)
- **VPC security group**: Chọn **Create new**
  - Name: `demo-rds`
- **Availability Zone**: Không ưu tiên
- **RDS Proxy**: Không yêu cầu
- **Port**: 3306 (cổng MySQL mặc định)

### Bước 6: Cấu Hình Bổ Sung

- **Monitoring**: Standard insights (Enhanced monitoring có sẵn nếu cần)
- **Log exports**: Tùy chọn
- **Estimated cost**: Xem xét thông tin RDS free tier (có sẵn trong 12 tháng)

### Bước 7: Tạo Cơ Sở Dữ Liệu

Nhấp vào **Create database** và chờ instance được tạo.

## Cài Đặt SQL Client

Trong khi cơ sở dữ liệu đang được tạo, tải xuống và cài đặt **SQLectron**:

1. Truy cập trang web SQLectron
2. Nhấp vào **Download GUI**
3. Chọn phiên bản phù hợp cho nền tảng của bạn:
   - Windows: Tải xuống trình cài đặt Windows mới nhất
   - Mac: Tải xuống file DMG
4. Cài đặt ứng dụng

## Kết Nối Đến Cơ Sở Dữ Liệu RDS

### Bước 1: Xác Minh Việc Tạo Cơ Sở Dữ Liệu

Khi cơ sở dữ liệu được tạo và hiển thị là **Available**:
1. Ghi chú địa chỉ **endpoint**
2. Xác minh **port** (3306)
3. Kiểm tra cài đặt **security group**

### Bước 2: Cấu Hình Security Group

1. Nhấp vào security group
2. Xem xét **inbound rules**
3. Đảm bảo cổng TCP 3306 được mở cho địa chỉ IP của bạn
4. Nếu cần, sửa đổi để cho phép truy cập từ mọi nơi (0.0.0.0/0 cho IPv4)

> **Cảnh Báo Bảo Mật**: Đối với môi trường production, hạn chế quyền truy cập chỉ cho các địa chỉ IP cụ thể.

### Bước 3: Kết Nối Sử Dụng SQLectron

1. Mở SQLectron
2. Nhấp **Add** để thêm kết nối cơ sở dữ liệu mới
3. Cấu hình kết nối:
   - **Name**: RDS demo
   - **Database Type**: MySQL
   - **Server Address**: Dán endpoint RDS của bạn
   - **Port**: 3306
   - **User**: admin
   - **Password**: Mật khẩu của bạn
   - **Initial Database**: mydb

4. Nhấp **Test** để xác minh kết nối
5. Nếu thành công, nhấp **Save** và **Connect**

### Khắc Phục Sự Cố Kết Nối

Nếu kết nối thất bại, kiểm tra:
- Cơ sở dữ liệu được đặt thành **public access**
- Security group cho phép IP của bạn trên cổng 3306
- Endpoint và thông tin xác thực chính xác được sử dụng

## Làm Việc Với Cơ Sở Dữ Liệu

### Tạo Bảng

Sau khi kết nối, bạn có thể thực thi các câu lệnh SQL:

```sql
CREATE TABLE mytable (
    name VARCHAR(20),
    firstname VARCHAR(20)
);
```

Thực thi câu lệnh này để tạo một bảng mới.

### Chèn Dữ Liệu

```sql
INSERT INTO mytable VALUES ('Maarek', 'Stephane');
```

### Truy Vấn Dữ Liệu

Nhấp **Select Rows** hoặc thực thi:

```sql
SELECT * FROM mytable;
```

Bạn sẽ thấy dữ liệu đã chèn được hiển thị.

## Tính Năng Quản Lý RDS

### Tạo Read Replicas

1. Chọn cơ sở dữ liệu của bạn
2. Nhấp **Actions** → **Create read replica**
3. Cấu hình cài đặt read replica
4. Chọn có bật multi-AZ cho replica hay không
5. Tạo replica để tăng khả năng đọc

### Giám Sát

Điều hướng đến tab **Monitoring** để xem:
- **CPU utilization**: Theo dõi việc sử dụng tài nguyên
- **Database connections**: Giám sát các kết nối đang hoạt động
- Nhiều metric khác để điều chỉnh hiệu suất

Sử dụng các metric này để xác định khi nào cần mở rộng instance cơ sở dữ liệu.

### Snapshots và Backups

**Tạo Snapshots**:
1. Chọn cơ sở dữ liệu của bạn
2. Nhấp **Actions** → **Take snapshot**
3. Snapshot có thể được khôi phục bất kỳ lúc nào

**Tùy Chọn Khôi Phục**:
- Khôi phục đến một thời điểm
- Khôi phục từ snapshot
- Di chuyển snapshot sang region khác

## Lợi Ích Của Amazon RDS

- **Fully managed**: AWS xử lý bảo trì, backups và cập nhật
- **Read replicas**: Mở rộng khả năng đọc
- **Multi-AZ deployment**: Tính sẵn sàng cao và khắc phục thảm họa
- **Easy scaling**: Tăng loại instance khi cần
- **Automated backups**: Khôi phục point-in-time
- **Monitoring**: Metric CloudWatch tích hợp

## Dọn Dẹp

### Xóa Cơ Sở Dữ Liệu

Để tránh các khoản phí đang diễn ra:

1. Chọn cơ sở dữ liệu của bạn
2. Nhấp **Modify**
3. Cuộn xuống cuối
4. **Tắt deletion protection**
5. Nhấp **Continue** → **Apply immediately**
6. Chờ việc sửa đổi hoàn tất
7. Chọn lại cơ sở dữ liệu
8. Nhấp **Actions** → **Delete**
9. Chọn các tùy chọn:
   - Bỏ chọn **Create final snapshot** (tùy chọn)
   - Gõ `delete me` để xác nhận
   - Xác nhận rằng tất cả dữ liệu sẽ bị mất
10. Nhấp **Delete**

## Kết Luận

Bạn đã tạo, cấu hình, kết nối và quản lý thành công cơ sở dữ liệu Amazon RDS MySQL. RDS cung cấp giải pháp cơ sở dữ liệu được quản lý mạnh mẽ với các tính năng như read replicas, triển khai multi-AZ, backup tự động và khả năng mở rộng dễ dàng - tất cả đều cần thiết cho các ứng dụng production.

## Lưu Ý Quan Trọng

- Hướng dẫn này sử dụng các tùy chọn free tier khi có sẵn
- Free tier có sẵn trong 12 tháng
- Luôn bảo mật cơ sở dữ liệu của bạn đúng cách trong production
- Giám sát chi phí bằng AWS Budgets
- Cân nhắc sử dụng AWS Secrets Manager để quản lý mật khẩu trong môi trường production




FILE: 30-domain-registrar-vs-dns-service.md


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




FILE: 31-aws-route53-cleanup-tutorial.md


# Hướng Dẫn Dọn Dẹp AWS Route 53 và EC2

## Tổng Quan

Hướng dẫn này sẽ giúp bạn dọn dẹp các tài nguyên AWS đã tạo trong các bài thực hành về Route 53 để tránh chi phí không cần thiết. Chúng ta sẽ xóa hosted zones, EC2 instances, và Application Load Balancers trên nhiều regions.

---

## Các Yếu Tố Chi Phí

### Tên Miền (Domain Name)
- Tên miền bạn đã mua sẽ vẫn còn trong tài khoản
- Chi phí gia hạn hàng năm: **$12/năm** (hoặc cao hơn đối với tên miền cao cấp)
- Bản thân đăng ký tên miền không thể xóa, chỉ có thể để nó hết hạn

### Route 53 Hosted Zone
- Nếu bạn không sử dụng hosted zone, bạn nên xóa nó
- Chi phí: **$0.50/tháng** nếu giữ hoạt động
- Số lượng records trong hosted zone không ảnh hưởng đến chi phí
- Bạn có thể giữ nguyên các records mà không tốn thêm phí

---

## Các Bước Dọn Dẹp

### 1. Xóa Route 53 Hosted Zone

Để xóa hosted zone của bạn:

1. Truy cập Route 53 trong AWS Console
2. Chọn hosted zone của bạn
3. **Đầu tiên, xóa tất cả các records** (ngoại trừ NS và SOA records mặc định)
4. Sau đó xóa hosted zone

> **Lưu ý:** Bạn phải xóa hết tất cả custom records trước khi có thể xóa hosted zone.

### 2. Xóa EC2 Instances

Trong bài hướng dẫn này, chúng ta đã tạo EC2 instances ở ba regions khác nhau. Bạn cần dọn dẹp từng region riêng biệt:

#### Region 1: Frankfurt (eu-central-1)
1. Truy cập EC2 console ở region Frankfurt
2. Chọn và terminate EC2 instance

#### Region 2: US East (us-east-1)
1. Chuyển sang region US East
2. Chọn và terminate EC2 instance

#### Region 3: Singapore (ap-southeast-1)
1. Chuyển sang region Singapore
2. Chọn và terminate EC2 instance

### 3. Xóa Application Load Balancer

Ở region mà bạn đã tạo ALB (trong ví dụ này là Frankfurt):

1. Truy cập EC2 → Load Balancers
2. Chọn Application Load Balancer của bạn
3. Xóa load balancer
4. Xóa **target group** liên quan

> **Quan trọng:** Đảm bảo xóa cả load balancer VÀ target group của nó để tránh bị tính phí.

---

## Danh Sách Kiểm Tra Dọn Dẹp Theo Region

Thực hiện các bước sau ở mỗi region mà bạn đã triển khai tài nguyên:

- [ ] Terminate EC2 instances
- [ ] Xóa Application Load Balancers
- [ ] Xóa các target groups liên quan
- [ ] Xác nhận không còn tài nguyên nào đang chạy

---

## Sau Khi Dọn Dẹp

Sau khi hoàn thành tất cả các bước dọn dẹp:

✅ Bạn sẽ không phải trả thêm chi phí nào từ bài hướng dẫn này  
✅ Chỉ còn phí đăng ký tên miền (nếu bạn chọn giữ tên miền)  
✅ Chi phí hosted zone sẽ dừng sau khi xóa

---

## Tóm Tắt

Bằng cách làm theo hướng dẫn dọn dẹp này, bạn đã thành công:

- Hiểu được các tác động chi phí của tài nguyên Route 53
- Xóa hosted zone để tránh chi phí hàng tháng
- Terminate EC2 instances trên nhiều regions
- Xóa Application Load Balancers và target groups
- Đảm bảo không có chi phí không cần thiết từ tài nguyên bài hướng dẫn

Cảm ơn bạn đã theo dõi phần này. Hẹn gặp lại ở bài giảng tiếp theo!




FILE: 32-vpc-section-introduction.md


# Giới Thiệu Phần VPC

## Tổng Quan

Chào mừng bạn đến với phần học về **VPC** (Virtual Private Cloud - Đám Mây Riêng Ảo). Phần này cung cấp cái nhìn tổng quan về các khái niệm VPC cần thiết cho chứng chỉ AWS và công việc phát triển.

## Về Phần Học Này

### Đối Tượng Học Viên

Phần tổng quan về VPC này được thiết kế cho cấp độ **AWS Certified Developer**. Mặc dù kiến thức VPC rất quan trọng cho:
- AWS Certified Solutions Architect Associate
- AWS Certified SysOps Administrator Associate

Với vai trò developer, bạn cần hiểu VPC ở **mức độ tổng quan** thay vì chuyên sâu, vì thường chỉ có khoảng **1-3 câu hỏi** về VPC trong kỳ thi chứng chỉ Developer.

### Nội Dung Học

Khóa học cấp tốc này bao gồm các thành phần VPC sau:

- **VPC** (Virtual Private Cloud - Đám Mây Riêng Ảo)
- **Subnets** (Mạng con)
- **Internet Gateways** (Cổng Internet)
- **NAT Gateways** (Cổng NAT)
- **Security Groups** (Nhóm Bảo Mật)
- **Network ACL (NACL)** (Danh Sách Kiểm Soát Truy Cập Mạng)
- **VPC Flow Logs** (Nhật Ký Luồng VPC)
- **VPC Peering** (Kết Nối Ngang Hàng VPC)
- **VPC Endpoints** (Điểm Cuối VPC)
- **Site-to-Site VPN** (VPN Kết Nối Điểm-Điểm)
- **Direct Connect** (Kết Nối Trực Tiếp)

## Phương Pháp Học

Đừng lo lắng nếu bạn không nhớ hết mọi thứ trong phần này ngay lập tức. Trong suốt khóa học, bất cứ khi nào các khái niệm VPC xuất hiện, chúng sẽ được làm nổi bật và giải thích lại để củng cố sự hiểu biết của bạn.

### Bạn Có Nên Học Phần Này?

- **Bỏ qua phần này** nếu bạn đã hoàn thành phần VPC trong:
  - Khóa học chứng chỉ SysOps Administrator
  - Khóa học Certified Solutions Architect Associate
  
- **Học phần này** nếu bạn:
  - Mới làm quen với các khái niệm VPC
  - Muốn ôn tập và làm mới kiến thức VPC của mình

## Bước Tiếp Theo

Tiến hành bài giảng tiếp theo để bắt đầu học về các khái niệm cơ bản của VPC.




FILE: 33-aws-vpc-networking-fundamentals.md


# AWS VPC và Subnets - Giới Thiệu

## Tổng Quan

Hướng dẫn này cung cấp phần giới thiệu về Amazon Virtual Private Cloud (VPC) và subnets, những khái niệm mạng cơ bản trong AWS.

## VPC là gì?

**VPC (Virtual Private Cloud)** là một mạng riêng trong AWS cloud cho phép bạn triển khai các tài nguyên của mình. Đặc điểm chính:

- VPC là **tài nguyên cấp vùng (regional resource)**
- Mỗi vùng AWS có thể có các VPC khác nhau
- VPC là cấu trúc logic chứa hạ tầng mạng của bạn

## Hiểu Về Subnets

**Subnets** cho phép bạn phân vùng mạng bên trong VPC:

- Subnets được định nghĩa ở **cấp độ availability zone (AZ)**
- Bạn có thể có nhiều subnets trong một VPC
- Có hai loại subnets chính:

### Public Subnets (Mạng Con Công Khai)

- Có thể truy cập từ internet
- Có thể truy cập World Wide Web
- Có thể được truy cập từ World Wide Web
- Thường chứa các tài nguyên cần truy cập internet (ví dụ: web servers)

### Private Subnets (Mạng Con Riêng Tư)

- Không thể truy cập từ internet
- Cung cấp bảo mật và quyền riêng tư cao hơn
- Lý tưởng cho các tài nguyên backend như cơ sở dữ liệu
- Các tài nguyên vẫn có thể truy cập internet thông qua NAT gateways

## Route Tables (Bảng Định Tuyến)

**Route tables** định nghĩa cách lưu lượng mạng di chuyển giữa các subnets:

- Kiểm soát quyền truy cập internet và giữa các subnets
- Xác định điều gì làm cho một subnet công khai hay riêng tư
- Mỗi subnet được liên kết với một route table

## Kiến Trúc VPC

Một kiến trúc VPC điển hình bao gồm:

- **CIDR Range**: Một tập hợp các dải IP được phép trong VPC của bạn
- **Nhiều Availability Zones**: Để đảm bảo tính sẵn sàng cao
- **Public và Private Subnets**: Trong mỗi AZ
- **EC2 Instances**: Được triển khai trong các subnets phù hợp

### Ví Dụ Kiến Trúc

```
Vùng (Region)
└── VPC (với CIDR range)
    ├── Availability Zone 1
    │   ├── Public Subnet
    │   └── Private Subnet
    └── Availability Zone 2
        ├── Public Subnet
        └── Private Subnet
```

## Default VPC (VPC Mặc Định)

Khi bạn bắt đầu sử dụng AWS:

- AWS tạo một **default VPC** trong mỗi vùng
- Chỉ chứa các public subnets
- Một public subnet cho mỗi availability zone
- Sẵn sàng sử dụng ngay lập tức

## Internet Gateways (Cổng Internet)

**Internet Gateway (IGW)** cho phép các instances trong VPC kết nối với internet:

- Nằm trong VPC của bạn
- Public subnets có tuyến đường trực tiếp đến internet gateway
- Định tuyến này làm cho subnet trở thành "công khai"
- Cho phép giao tiếp hai chiều với internet

## NAT Gateways và NAT Instances

**NAT (Network Address Translation)** gateways cho phép các instances trong private subnet truy cập internet trong khi vẫn giữ tính riêng tư:

### NAT Gateway vs NAT Instance

| Tính Năng | NAT Gateway | NAT Instance |
|-----------|-------------|--------------|
| Quản lý | Được AWS quản lý | Tự quản lý |
| Cung cấp | Tự động | Thủ công |
| Mở rộng | Tự động | Thủ công |

### Cách NAT Hoạt Động

1. NAT gateway/instance được triển khai trong **public subnet**
2. Private subnet tạo tuyến đường đến NAT gateway/instance
3. NAT gateway định tuyến đến internet gateway
4. Private instances có thể truy cập internet mà không bị truy cập trực tiếp từ internet

### Luồng Kiến Trúc

```
Private Subnet → NAT Gateway (trong Public Subnet) → Internet Gateway → Internet
```

## Các Trường Hợp Sử Dụng

- **Public Subnets**: Web servers, application load balancers, bastion hosts
- **Private Subnets**: Cơ sở dữ liệu, application servers, Lambda functions
- **NAT Gateways**: Cho phép cập nhật phần mềm cho các private instances

## Những Điểm Chính Cần Nhớ

- VPCs cung cấp môi trường mạng cô lập trong AWS
- Subnets phân vùng VPC của bạn ở cấp độ AZ
- Public subnets có tuyến đường trực tiếp đến internet gateway
- Private subnets sử dụng NAT cho truy cập internet đi ra
- Route tables kiểm soát tất cả luồng lưu lượng mạng
- Hạ tầng này là nền tảng cho các triển khai AWS an toàn

## Các Bước Tiếp Theo

Tiếp tục tìm hiểu về các khái niệm VPC bổ sung bao gồm:
- Security Groups (Nhóm Bảo Mật)
- Network ACLs (Danh Sách Kiểm Soát Truy Cập Mạng)
- VPC Peering (Kết Nối VPC)
- VPN Connections (Kết Nối VPN)
- Direct Connect (Kết Nối Trực Tiếp)

---

*Lưu ý: Đây là phần tổng quan ở mức độ cao. Các hướng dẫn thực hành chi tiết hơn sẽ được đề cập trong các bài giảng tiếp theo.*




FILE: 34-aws-vpc-network-security-overview.md


# Tổng Quan Về Bảo Mật Mạng AWS VPC

## Giới Thiệu

Sau khi đã tìm hiểu tất cả các khía cạnh về việc định nghĩa mạng trong VPC, hãy cùng nói về bảo mật mạng. Bài giảng này tập trung vào các khái niệm Network ACL (NACL) và Security Groups, cũng như VPC Flow Logs để giám sát và xử lý sự cố.

## Network ACL (NACL)

### Network ACL là gì?

Network ACL (NACL) là một tường lửa kiểm soát lưu lượng truy cập từ và đến các subnet trong VPC của bạn.

### Đặc Điểm Chính

- **Mức Độ Kiểm Soát**: Hoạt động ở cấp độ subnet
- **Loại Quy Tắc**: Có thể có cả quy tắc **cho phép** và **từ chối**
- **Nội Dung Quy Tắc**: Quy tắc chỉ bao gồm địa chỉ IP
- **Tuyến Phòng Thủ Đầu Tiên**: Đóng vai trò là cơ chế phòng thủ đầu tiên cho các subnet công khai của bạn

### Cách Hoạt Động

Khi bạn gắn NACL ở cấp độ subnet, bạn có thể kiểm soát lưu lượng một cách rõ ràng:
- Cho phép lưu lượng từ các địa chỉ IP cụ thể
- Từ chối lưu lượng từ các địa chỉ IP cụ thể

Lưu lượng từ và đến internet phải đi qua Network ACL trước khi đến bất kỳ EC2 instance nào trong subnet.

### Hành Vi Mặc Định

Khi bạn có VPC mặc định:
- NACL mặc định **cho phép mọi thứ vào** và **cho phép mọi thứ ra**
- Đây là lý do tại sao bạn thường không cần phải sửa đổi NACL cho các cấu hình cơ bản

## Security Groups

### Security Group là gì?

Security Group là một tường lửa kiểm soát lưu lượng truy cập đến và đi từ ENI (Elastic Network Interface) hoặc EC2 instance.

### Đặc Điểm Chính

- **Mức Độ Kiểm Soát**: Hoạt động ở cấp độ instance hoặc ENI
- **Loại Quy Tắc**: Chỉ có thể có **quy tắc cho phép** (không có quy tắc từ chối rõ ràng)
- **Nội Dung Quy Tắc**: Có thể tham chiếu đến địa chỉ IP hoặc các security group khác
- **Tuyến Phòng Thủ Thứ Hai**: Đóng vai trò là cơ chế phòng thủ thứ hai sau NACL

### Cách Hoạt Động

Security groups được gắn trực tiếp vào các EC2 instance. Sau khi lưu lượng đi qua Network ACL, nó phải đi qua security group trước khi đến EC2 instance.

## So Sánh Network ACL và Security Group

| Tính Năng | Security Group | Network ACL |
|-----------|---------------|-------------|
| **Hoạt động ở** | Cấp độ Instance/ENI | Cấp độ Subnet |
| **Quy tắc** | Chỉ có quy tắc cho phép | Quy tắc cho phép và từ chối |
| **Trạng thái** | Stateful (tự động cho phép lưu lượng phản hồi) | Stateless (phải cho phép rõ ràng lưu lượng vào và ra) |
| **Áp dụng cho** | Instance hoặc ENI | Tất cả instance trong subnet |

### Lưu Ý Quan Trọng

- Security groups là **stateful**: Lưu lượng phản hồi được tự động cho phép bất kể quy tắc
- Network ACLs là **stateless**: Bạn phải cho phép rõ ràng lưu lượng theo cả hai hướng

## VPC Flow Logs

### VPC Flow Logs là gì?

VPC Flow Logs ghi lại thông tin về tất cả lưu lượng IP đi qua các giao diện mạng của bạn.

### Các Loại Flow Logs

1. **VPC Flow Logs**: Ghi lại lưu lượng ở cấp độ VPC
2. **Subnet Flow Logs**: Ghi lại lưu lượng ở cấp độ subnet
3. **ENI Flow Logs**: Ghi lại lưu lượng ở cấp độ Elastic Network Interface

### Trường Hợp Sử Dụng

Flow logs giúp bạn:
- **Giám sát** lưu lượng mạng trong VPC của bạn
- **Xử lý sự cố kết nối**, chẳng hạn như:
  - Tại sao subnet không thể truy cập internet
  - Tại sao các subnet có thể hoặc không thể giao tiếp với nhau
  - Các vấn đề kết nối từ internet đến subnet

### Thông Tin Được Ghi Lại

- **Lưu lượng được cho phép**: Thông tin về các kết nối được phép
- **Lưu lượng bị từ chối**: Thông tin về các kết nối bị chặn
- **Dịch Vụ AWS Được Quản Lý**: Thông tin mạng từ các dịch vụ như:
  - Elastic Load Balancers
  - ElastiCache
  - RDS (Relational Database Service)
  - Aurora

### Tùy Chọn Lưu Trữ

Dữ liệu VPC Flow Logs có thể được gửi đến:
- **Amazon S3**: Để lưu trữ và phân tích dài hạn
- **CloudWatch Logs**: Để giám sát và cảnh báo thời gian thực
- **Kinesis Data Firehose**: Để xử lý dữ liệu streaming

## Tóm Tắt

Trong bài giảng này, chúng ta đã đề cập đến ba thành phần quan trọng của bảo mật mạng VPC:

1. **Network ACLs (NACLs)**: Tường lửa cấp độ subnet với quy tắc cho phép và từ chối
2. **Security Groups**: Tường lửa cấp độ instance chỉ có quy tắc cho phép
3. **VPC Flow Logs**: Ghi log lưu lượng mạng để giám sát và xử lý sự cố

Hiểu rõ các lớp bảo mật này là điều cần thiết để xây dựng các ứng dụng an toàn và có kiến trúc tốt trên AWS.




FILE: 35-aws-vpc-connectivity-options.md


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




FILE: 36-vpc-section-summary.md


# Tóm Tắt Phần VPC

## Tổng Quan

Phần này cung cấp tóm tắt toàn diện về các khái niệm AWS Virtual Private Cloud (VPC). Mặc dù đây là phần nặng về lý thuyết không có bài tập thực hành, các khái niệm chính được đề cập ở đây rất cần thiết để hiểu các nguyên tắc cơ bản về mạng AWS.

## Các Khái Niệm VPC Chính

### VPC (Virtual Private Cloud)

- **VPC** là viết tắt của Virtual Private Cloud (Đám mây riêng ảo)
- Chúng ta đã sử dụng VPC mặc định trong suốt khóa học này khi tạo các EC2 instance
- Có **một VPC mặc định cho mỗi AWS region**

### Subnets (Mạng con)

- Subnet được **gắn với các Availability Zone cụ thể**
- Đây là nơi chúng ta khởi chạy các EC2 instance
- Chúng đại diện cho **phân vùng mạng của VPC**

### Internet Gateway (Cổng Internet)

- Cung cấp quyền truy cập internet cho các instance trong **public subnet**
- Được định nghĩa ở **cấp độ VPC**

### NAT Gateway và NAT Instance

- Cung cấp quyền truy cập internet cho **private subnet**
- Cho phép các EC2 instance trong private subnet truy cập internet

## Bảo Mật Mạng

### Network ACL (NACL)

- Tường lửa cấp subnet **không trạng thái (stateless)**
- Kiểm soát lưu lượng **đến và đi**
- Áp dụng quy tắc cho toàn bộ subnet

### Security Group (Nhóm Bảo Mật)

- Tường lửa **có trạng thái (stateful)**
- Hoạt động ở **cấp độ EC2 instance** hoặc ENI (Elastic Network Interface)
- Có thể **tham chiếu đến các security group khác**

## Kết Nối VPC

### VPC Peering (Kết Nối VPC)

- Cho phép bạn **kết nối hai VPC với nhau**
- Các VPC phải có **dải CIDR không trùng lặp**
- **Không bắc cầu (non-transitive)** - bạn cần thiết lập kết nối peering riêng giữa từng cặp VPC
- Nếu muốn tất cả VPC được kết nối, bạn phải tạo kết nối peering giữa từng tổ hợp

### VPC Endpoint

- Cung cấp **quyền truy cập riêng tư vào các dịch vụ AWS** trong VPC của bạn
- Loại bỏ nhu cầu sử dụng internet gateway hoặc thiết bị NAT
- Sẽ được đề cập chi tiết cho các dịch vụ cụ thể trong các bài giảng sau

### VPC Flow Log

- Ghi lại **nhật ký lưu lượng mạng**
- Được sử dụng để gỡ lỗi các vấn đề kết nối
- Giúp xác định xem lưu lượng có:
  - Bị từ chối quyền truy cập
  - Bị chặn
  - Được cho phép trong VPC của bạn

## Kết Nối On-Premise

### Site-to-Site VPN

- Thiết lập **kết nối VPN qua internet công cộng**
- Kết nối trung tâm dữ liệu on-premise của bạn với AWS

### Direct Connect

- Cung cấp **kết nối riêng trực tiếp đến AWS**
- Không đi qua internet công cộng
- Cung cấp hiệu suất mạng ổn định hơn

## Tóm Lược

Phần này đã đề cập đến các khái niệm VPC cơ bản cần thiết cho kỳ thi AWS Certified Developer. Những điểm chính cần nhớ là:

1. Hiểu mối quan hệ giữa VPC, subnet và availability zone
2. Biết sự khác biệt giữa kết nối public subnet và private subnet
3. Hiểu bảo mật mạng không trạng thái so với có trạng thái (NACL vs Security Group)
4. Nhận biết các giới hạn của VPC Peering (không bắc cầu)
5. Hiểu các tùy chọn khác nhau để kết nối với AWS từ on-premise

Đừng lo lắng nếu bạn chưa hiểu hết mọi thứ ngay lập tức. Các khái niệm này sẽ trở nên rõ ràng hơn khi chúng ta sử dụng chúng trong các bài tập thực hành trong các phần tiếp theo của khóa học. Bạn luôn có thể quay lại xem lại phần này sau.




FILE: 37-aws-three-tier-architecture-and-solution-patterns.md


# Kiến Trúc Ba Tầng AWS và Các Mẫu Giải Pháp

## Tổng Quan

Tài liệu này đề cập đến các kiến trúc giải pháp AWS điển hình, tập trung vào mẫu kiến trúc ba tầng, triển khai LAMP stack và lưu trữ WordPress trên AWS.

## Kiến Trúc Giải Pháp Ba Tầng

### Các Thành Phần Kiến Trúc

Kiến trúc ba tầng là một mẫu phổ biến được sử dụng trong AWS, cung cấp bảo mật, khả năng mở rộng và tách biệt các mối quan tâm.

#### Tầng 1: Cân Bằng Tải (Public Subnet)

- **Elastic Load Balancer (ELB)** được triển khai trên nhiều Vùng Khả Dụng (Availability Zones)
- Phải nằm trong **public subnets** để có thể truy cập từ internet
- Người dùng truy cập ứng dụng thông qua truy vấn DNS của **Route 53**
- Phân phối lưu lượng đến tầng ứng dụng

#### Tầng 2: Tầng Ứng Dụng (Private Subnet)

- **EC2 instances** trong một **Auto Scaling Group**
- Được triển khai trong **private subnets** để tăng cường bảo mật
- Chỉ có thể truy cập từ ELB, không trực tiếp từ internet
- Phân bổ trên ba Vùng Khả Dụng để đảm bảo tính sẵn sàng cao
- Lưu lượng được định tuyến từ public subnets đến private subnets sử dụng **route tables**

#### Tầng 3: Tầng Dữ Liệu (Data Subnet)

- Nằm trong private subnet thứ hai (mức sâu hơn)
- Còn được gọi là **data subnet**
- Bao gồm:
  - **Amazon RDS**: Cơ sở dữ liệu chính cho các thao tác đọc/ghi
  - **ElastiCache**: Tầng cache để:
    - Lưu cache dữ liệu từ RDS
    - Lưu trữ dữ liệu phiên (session) trong bộ nhớ
    - Cải thiện hiệu suất ứng dụng

### Lợi Ích Bảo Mật

- Tài nguyên tính toán được cô lập trong private subnets
- Tăng cường bảo mật thông qua phân đoạn mạng
- Kiến trúc phòng thủ nhiều lớp

## LAMP Stack trên EC2

### Các Thành Phần

**LAMP** là một stack ứng dụng web phổ biến bao gồm:

- **L**inux: Hệ điều hành cho EC2 instances
- **A**pache: Web server chạy trên Linux
- **M**ySQL: Cơ sở dữ liệu (có thể sử dụng RDS MySQL)
- **P**HP: Logic ứng dụng để render các trang web

### Các Thành Phần Bổ Sung

- **Redis hoặc Memcached** (ElastiCache): Cho công nghệ caching
- **EBS (Elastic Block Store)**: Để lưu trữ dữ liệu cục bộ, bao gồm:
  - Cache cục bộ
  - Dữ liệu ứng dụng
  - Lưu trữ phần mềm

## WordPress trên AWS

### Tổng Quan Kiến Trúc

Triển khai WordPress trên AWS sử dụng kiến trúc nhiều tầng với khả năng lưu trữ chia sẻ.

### Các Thành Phần Chính

#### Cân Bằng Tải và Tính Toán
- **Elastic Load Balancer**: Phân phối lưu lượng người dùng
- **EC2 Instances**: Lưu trữ ứng dụng WordPress
- **Auto Scaling Group**: Quản lý việc mở rộng EC2 instances

#### Giải Pháp Lưu Trữ Chia Sẻ

**Vấn Đề**: Nhiều EC2 instances cần chia sẻ hình ảnh do người dùng tải lên

**Giải Pháp**: **Amazon EFS (Elastic File System)**
- Hệ thống file mạng có thể truy cập trên tất cả EC2 instances
- Tạo Elastic Network Interfaces trong mỗi Vùng Khả Dụng
- Cho phép chia sẻ file trên tất cả các máy chủ ứng dụng
- Hoàn hảo cho việc lưu trữ và truy cập hình ảnh chia sẻ

### Kiến Trúc WordPress Quy Mô Đầy Đủ

AWS cung cấp một kiến trúc tham chiếu WordPress toàn diện bao gồm:

- NAT Gateways và Internet Gateways
- Auto Scaling Groups
- Nhiều subnets (public và private)
- Cơ sở dữ liệu Amazon Aurora
- Amazon EFS cho lưu trữ chia sẻ
- Công nghệ cân bằng tải
- CloudFront và S3 (để phân phối nội dung)

## Những Điểm Chính Cần Nhớ

1. **Kiến trúc ba tầng** là một mẫu cơ bản trong thiết kế giải pháp AWS
2. **Phân đoạn mạng** thông qua subnets cung cấp các lớp bảo mật
3. **Các khái niệm VPC** là thiết yếu để hiểu kiến trúc AWS
4. Các tầng khác nhau phục vụ các mục đích khác nhau:
   - Public subnets cho các thành phần hướng internet
   - Private subnets cho logic ứng dụng
   - Data subnets cho cơ sở dữ liệu và caching
5. **EFS** là lý tưởng cho lưu trữ file chia sẻ trên nhiều instances
6. Các mẫu này thường xuyên xuất hiện trong các kỳ thi chứng chỉ AWS

## Kết Luận

Hiểu các mẫu kiến trúc này là rất quan trọng cho:
- Thiết kế các giải pháp AWS an toàn và có khả năng mở rộng
- Vượt qua các kỳ thi chứng chỉ AWS
- Làm việc hiệu quả với vai trò nhà phát triển AWS

Hãy dành thời gian nghiên cứu các sơ đồ kiến trúc này và hiểu cách các dịch vụ AWS khác nhau hoạt động cùng nhau để tạo ra các ứng dụng mạnh mẽ, sẵn sàng cho sản xuất.




FILE: 38-amazon-s3-introduction.md


# Giới thiệu về Amazon S3

## Tổng quan

Chào mừng bạn đến với phần học về Amazon S3. Phần này rất quan trọng vì Amazon S3 là một trong những khối xây dựng chính của AWS và được quảng cáo là dịch vụ lưu trữ có khả năng mở rộng vô hạn.

Trên thực tế, rất nhiều trang web phụ thuộc vào Amazon S3. Ví dụ, nhiều website sử dụng Amazon S3 làm nền tảng và nhiều dịch vụ AWS cũng sử dụng Amazon S3 để tích hợp.

Trong phần này, chúng ta sẽ có cách tiếp cận từng bước với Amazon S3 để tìm hiểu các tính năng chính.

## Các trường hợp sử dụng

Có rất nhiều trường hợp sử dụng cho Amazon S3 vì về cốt lõi nó là dịch vụ lưu trữ. S3 được sử dụng cho:

- **Sao lưu và Lưu trữ** - Cho các tệp tin, đĩa của bạn, v.v.
- **Khôi phục thảm họa** - Di chuyển dữ liệu của bạn sang một region khác. Trong trường hợp một region gặp sự cố, dữ liệu của bạn được sao lưu ở nơi khác
- **Lưu trữ** - Lưu trữ các tệp tin trong Amazon S3 và truy xuất nó vào giai đoạn sau với chi phí rẻ hơn nhiều
- **Lưu trữ đám mây kết hợp** - Trong trường hợp bạn có lưu trữ tại chỗ nhưng muốn mở rộng nó lên đám mây
- **Lưu trữ ứng dụng** - Lưu trữ các ứng dụng và phương tiện như tệp video, hình ảnh, v.v.
- **Data Lake** - Lưu trữ nhiều dữ liệu và thực hiện phân tích dữ liệu lớn
- **Cập nhật phần mềm** - Cung cấp các bản cập nhật phần mềm
- **Website tĩnh** - Lưu trữ các website tĩnh

### Ví dụ thực tế

- **Nasdaq** lưu trữ bảy năm dữ liệu vào dịch vụ S3 Glacier, đây là dịch vụ lưu trữ của Amazon S3
- **Sysco** chạy phân tích trên dữ liệu của mình và thu được thông tin chi tiết về kinh doanh từ Amazon S3

## S3 Buckets

Amazon S3 lưu trữ các tệp tin vào **buckets**. Buckets có thể được xem như các thư mục cấp cao nhất.

### Đặc điểm chính

- Các tệp tin trong S3 buckets được gọi là **objects** (đối tượng)
- Buckets được tạo trong tài khoản của bạn và phải có **tên duy nhất toàn cầu**
- Tên phải là duy nhất trên tất cả các region, tất cả các tài khoản tồn tại trên AWS
- Buckets được định nghĩa ở **cấp độ region**
- S3 trông giống như một dịch vụ toàn cầu, nhưng buckets thực sự được tạo trong một AWS region cụ thể

### Quy ước đặt tên

Tên bucket phải tuân theo các quy tắc sau:

- Không có chữ hoa
- Không có dấu gạch dưới
- Phải dài từ 3 đến 63 ký tự
- Không được là địa chỉ IP
- Phải bắt đầu bằng chữ thường hoặc số thường
- Sử dụng chữ cái, số và dấu gạch ngang

## S3 Objects

Objects là các tệp tin có cái gọi là **key** (khóa).

### Object Keys

Khóa đối tượng Amazon S3 là **đường dẫn đầy đủ** của tệp tin của bạn.

**Ví dụ:**

- Tệp đơn giản: `my_file.txt`
- Tệp lồng nhau: `my_folder_1/another_folder/my_file.txt`

Key được tạo thành từ:
- **Prefix** (tiền tố): `my_folder_1/another_folder`
- **Object name** (tên đối tượng): `my_file.txt`

### Khái niệm quan trọng

Amazon S3 không có khái niệm thư mục như vậy, mặc dù khi bạn nhìn vào console, giao diện người dùng sẽ khiến bạn nghĩ ngược lại và bạn thực sự sẽ tạo các thư mục. Nhưng bất cứ thứ gì trong Amazon S3 thực sự đều là một **key**. Keys chỉ là những tên rất dài chứa dấu gạch chéo và được tạo thành từ prefix và object name.

### Thuộc tính của Object

**Giá trị Object:**
- Nội dung của phần thân
- Bạn có thể tải lên bất kỳ tệp nào vào Amazon S3
- Kích thước đối tượng tối đa: **5 terabytes** (5.000 gigabytes)
- Nếu tải lên tệp lớn hơn 5 gigabytes, bạn phải sử dụng **multi-part upload** (tải lên nhiều phần)

**Thuộc tính bổ sung:**

- **Metadata** - Danh sách các cặp key-value có thể được đặt bởi hệ thống hoặc người dùng để chỉ ra một số yếu tố về tệp tin
- **Tags** (thẻ) - Các cặp key-value Unicode (tối đa 10), hữu ích cho bảo mật và quản lý vòng đời
- **Version ID** - Nếu bạn đã bật tính năng versioning (phiên bản)

## Các bước tiếp theo

Bây giờ bạn đã có phần giới thiệu về Amazon S3, hãy cùng vào console để bắt đầu thực hành.




FILE: 39-amazon-s3-fundamentals-and-core-concepts.md


# Amazon S3: Kiến Thức Nền Tảng và Các Khái Niệm Cốt Lõi

## Giới Thiệu về Amazon S3

Amazon S3 (Simple Storage Service) là một trong những thành phần xây dựng chính của AWS, được quảng cáo là dịch vụ lưu trữ có khả năng mở rộng vô hạn. Nó đóng vai trò là xương sống cho nhiều trang web và dịch vụ AWS, khiến nó trở thành một thành phần quan trọng của cơ sở hạ tầng đám mây hiện đại.

## Các Trường Hợp Sử Dụng Chính

Amazon S3 hỗ trợ nhiều trường hợp sử dụng khác nhau:

- **Sao Lưu và Lưu Trữ**: Lưu trữ tệp tin, đĩa và dữ liệu khác một cách an toàn
- **Khôi Phục Thảm Họa**: Sao chép dữ liệu giữa các vùng để đảm bảo tính liên tục kinh doanh
- **Lưu Trữ**: Lưu trữ dài hạn với chi phí thấp hơn
- **Lưu Trữ Đám Mây Lai**: Mở rộng lưu trữ on-premises lên đám mây
- **Lưu Trữ Media**: Lưu trữ và phân phối video, hình ảnh và các tệp media khác
- **Data Lake**: Kho lưu trữ tập trung cho phân tích dữ liệu lớn
- **Cập Nhật Phần Mềm**: Phân phối các bản cập nhật và bản vá ứng dụng
- **Lưu Trữ Website Tĩnh**: Lưu trữ nội dung web tĩnh

### Ví Dụ Thực Tế

- **Nasdaq**: Lưu trữ dữ liệu bảy năm trong S3 Glacier
- **Sysco**: Chạy phân tích trên dữ liệu S3 để có được những hiểu biết kinh doanh

## S3 Buckets

### Bucket là gì?

Bucket là các thư mục cấp cao nhất trong Amazon S3 để lưu trữ các tệp tin (được gọi là objects).

### Đặc Điểm của Bucket

- **Tên Duy Nhất Toàn Cầu**: Tên bucket phải là duy nhất trên tất cả các vùng AWS và tài khoản
- **Định Nghĩa Theo Vùng**: Mặc dù đặt tên toàn cầu, các bucket được tạo trong các vùng AWS cụ thể
- **Tài Nguyên Cấp Tài Khoản**: Bucket được tạo trong tài khoản AWS của bạn

### Quy Ước Đặt Tên

Tên bucket S3 phải tuân theo các quy tắc sau:

- Không có chữ hoa hoặc dấu gạch dưới
- Từ 3 đến 63 ký tự
- Không được là địa chỉ IP
- Phải bắt đầu bằng chữ thường hoặc số
- Chỉ sử dụng chữ thường, số và dấu gạch ngang

## S3 Objects

### Cấu Trúc Object

Object là các tệp tin được lưu trữ trong S3 bucket, bao gồm:

#### Key (Đường Dẫn)
Đường dẫn đầy đủ đến tệp tin của bạn:
- Ví dụ đơn giản: `my-file.txt`
- Ví dụ lồng nhau: `my-folder-1/another-folder/my-file.txt`

Key được tạo thành từ:
- **Prefix**: Đường dẫn thư mục (ví dụ: `my-folder-1/another-folder/`)
- **Object Name**: Tên tệp tin (ví dụ: `my-file.txt`)

**Lưu Ý Quan Trọng**: S3 không có khái niệm thư mục thực sự. Mọi thứ đều là một key với dấu gạch chéo trong tên, mặc dù giao diện console làm cho nó trông giống như cấu trúc thư mục.

#### Value (Nội Dung)
Nội dung/thân thực tế của tệp tin.

### Giới Hạn Kích Thước Object

- **Kích thước object tối đa**: 5 terabyte (5,000 GB)
- **Tải lên tệp tin lớn**: Các tệp tin lớn hơn 5 GB phải sử dụng multi-part upload
- **Yêu cầu multi-part**: Tệp tin phải được chia thành nhiều phần (ví dụ: tệp tin 5 TB yêu cầu ít nhất 1,000 phần mỗi phần 5 GB)

### Các Thuộc Tính Bổ Sung của Object

#### Metadata
- Các cặp key-value mô tả object
- Có thể được định nghĩa bởi hệ thống hoặc người dùng
- Được sử dụng để lưu trữ thông tin về tệp tin

#### Tags
- Các cặp key-value Unicode (tối đa 10 tags mỗi object)
- Hữu ích cho các chính sách bảo mật và quản lý vòng đời
- Giúp tổ chức và phân loại các object

#### Version ID
- Có mặt khi versioning được bật trên bucket
- Cho phép theo dõi và quản lý nhiều phiên bản của một object

## Kết Luận

Amazon S3 là một dịch vụ AWS cơ bản cung cấp lưu trữ object có khả năng mở rộng, bền vững và có tính khả dụng cao. Hiểu về bucket, object, key và các thuộc tính khác nhau là điều cần thiết để tận dụng hiệu quả S3 trong kiến trúc đám mây của bạn.




FILE: 4-amazon-aurora-overview.md


# Tổng Quan về Amazon Aurora

## Giới Thiệu

Amazon Aurora là một chủ đề quan trọng trong các kỳ thi chứng chỉ AWS, đòi hỏi sự hiểu biết vững chắc ở cấp độ tổng quan về kiến trúc và tính năng của nó. Hướng dẫn này cung cấp kiến thức toàn diện về các khái niệm và khả năng chính của Aurora.

## Amazon Aurora là gì?

Amazon Aurora là một **công nghệ cơ sở dữ liệu độc quyền của AWS** (không mã nguồn mở) cung cấp:

- **Tương Thích Cơ Sở Dữ Liệu**: Tương thích với PostgreSQL và MySQL
- **Hỗ Trợ Driver**: Hoạt động với các driver cơ sở dữ liệu PostgreSQL và MySQL hiện có
- **Thiết Kế Tối Ưu Hóa Cloud**: Được xây dựng đặc biệt cho môi trường cloud với các tối ưu hóa đáng kể

## Lợi Thế về Hiệu Suất

Aurora mang lại cải thiện hiệu suất vượt trội so với RDS tiêu chuẩn:

- **Cải thiện hiệu suất 5 lần** so với MySQL trên RDS
- **Cải thiện hiệu suất 3 lần** so với PostgreSQL trên RDS
- Các cải tiến hiệu suất bổ sung trên nhiều khía cạnh

## Tính Năng Chính

### Tự Động Mở Rộng Dung Lượng

Một trong những tính năng nổi bật của Aurora là khả năng tự động tăng dung lượng lưu trữ:

- **Dung Lượng Ban Đầu**: 10 GB
- **Dung Lượng Tối Đa**: 256 TB
- **Tăng Trưởng Tự Động**: Mở rộng tự động khi dữ liệu tăng lên
- **Lợi Ích**: Không cần giám sát dung lượng đĩa - bộ nhớ tự động tăng theo dữ liệu của bạn

### Read Replicas (Bản Sao Đọc)

- **Hỗ trợ tối đa 15 read replicas**
- **Sao Chép Nhanh Hơn**: Nhanh hơn đáng kể so với sao chép MySQL
- **Độ Trễ Thấp**: Độ trễ replica thường dưới 10 mili giây
- **Hỗ Trợ Đa Vùng**: Read replicas có thể được triển khai trên nhiều region

### Tính Khả Dụng Cao

- **Chuyển Đổi Dự Phòng Tức Thì**: Nhanh hơn nhiều so với chuyển đổi dự phòng Multi-AZ trên RDS tiêu chuẩn
- **Thời Gian Chuyển Đổi Trung Bình**: Dưới 30 giây
- **Thiết Kế Cloud-Native**: Tính khả dụng cao được tích hợp sẵn

### Hiệu Quả Chi Phí

- **Chi Phí**: Cao hơn khoảng 20% so với RDS tiêu chuẩn
- **Giá Trị**: Hiệu quả hơn đáng kể ở quy mô lớn, dẫn đến tiết kiệm chi phí tổng thể

## Kiến Trúc Tính Khả Dụng Cao

### Sao Chép Dữ Liệu

Aurora triển khai chiến lược sao chép mạnh mẽ:

- **Sáu bản sao** dữ liệu trên **ba Availability Zones**
- **Yêu Cầu Ghi**: Cần 4 trong 6 bản sao khả dụng
- **Yêu Cầu Đọc**: Cần 3 trong 6 bản sao khả dụng
- **Tự Phục Hồi**: Sao chép ngang hàng tự động sửa chữa dữ liệu bị hỏng
- **Lưu Trữ Phân Tán**: Dữ liệu được lưu trữ trên hàng trăm volume (không chỉ một)

### Thiết Kế Storage Volume

Aurora sử dụng shared storage volume với các tính năng nâng cao:

- **Logical Volume**: Xuất hiện như một volume lưu trữ duy nhất
- **Sao Chép Tự Động**: Dữ liệu được sao chép qua nhiều AZ
- **Tự Phục Hồi**: Tự động phục hồi từ dữ liệu bị hỏng
- **Tự Động Mở Rộng**: Tăng trưởng tự động theo khối lượng dữ liệu
- **Striping**: Dữ liệu được phân phối trên các volume để có hiệu suất tối ưu

## Kiến Trúc Cluster

### Master Instance (Instance Chính)

- **Single Master**: Chỉ một instance xử lý các thao tác ghi
- **Chuyển Đổi Nhanh**: Tự động chuyển đổi dự phòng trong vòng chưa đầy 30 giây
- **Writer Endpoint**: Tên DNS luôn trỏ đến master hiện tại
  - Tự động chuyển hướng client đến instance đúng sau khi chuyển đổi dự phòng
  - Cung cấp quản lý kết nối liền mạch

### Read Replicas (Bản Sao Đọc)

- **Khả Năng Mở Rộng**: Tối đa 15 read replicas để phân phối khối lượng công việc đọc
- **Auto-Scaling**: Có thể cấu hình tự động mở rộng read replicas
- **Khả Năng Chuyển Đổi**: Bất kỳ read replica nào cũng có thể trở thành master nếu cần
- **Reader Endpoint**: Điểm kết nối cân bằng tải
  - Tự động kết nối đến read replicas khả dụng
  - Cung cấp cân bằng tải ở cấp độ kết nối (không phải cấp độ câu lệnh)
  - Đơn giản hóa quản lý kết nối ứng dụng

### Các Thành Phần Cluster Chính Cần Nhớ

1. **Một Master** - xử lý tất cả các thao tác ghi
2. **Nhiều Replicas** - xử lý đọc với auto-scaling
3. **Writer Endpoint** - luôn trỏ đến master
4. **Reader Endpoint** - cân bằng tải giữa các read replicas
5. **Shared Storage Volume** - tự động mở rộng và tự phục hồi

## Tính Năng Nâng Cao

### Tính Năng Vận Hành

- **Chuyển Đổi Dự Phòng Tự Động**: Chuyển đổi liền mạch khi có sự cố
- **Sao Lưu và Phục Hồi**: Khả năng sao lưu tích hợp sẵn
- **Cô Lập và Bảo Mật**: Các tính năng bảo mật cấp doanh nghiệp
- **Tuân Thủ Ngành**: Đáp ứng các tiêu chuẩn tuân thủ khác nhau
- **Push-Button Scaling**: Cấu hình auto-scaling dễ dàng
- **Vá Lỗi Không Downtime**: Cập nhật tự động mà không gián đoạn
- **Giám Sát Nâng Cao**: Công cụ giám sát toàn diện
- **Bảo Trì Định Kỳ**: Các hoạt động bảo trì được quản lý hoàn toàn

### Tính Năng Backtrack

Aurora bao gồm khả năng **Backtrack** độc đáo:

- **Phục Hồi Theo Thời Điểm**: Khôi phục dữ liệu về bất kỳ thời điểm nào trước đó
- **Không Phụ Thuộc Backup**: Không dựa vào các bản sao lưu truyền thống
- **Linh Hoạt**: Dễ dàng chuyển đổi giữa các thời điểm khác nhau
- **Ví Dụ**: Có thể khôi phục về "hôm qua lúc 4:00 chiều" sau đó thay đổi thành "hôm qua lúc 5:00 chiều"

## Mẹo Cho Kỳ Thi

Các điểm chính cần nhớ cho các kỳ thi chứng chỉ AWS:

1. ✅ Aurora được tối ưu hóa cho cloud và là độc quyền của AWS
2. ✅ Tương thích với PostgreSQL và MySQL
3. ✅ Hiệu suất gấp 5 lần MySQL RDS, gấp 3 lần PostgreSQL RDS
4. ✅ Bộ nhớ tự động tăng từ 10 GB đến 256 TB
5. ✅ Tối đa 15 read replicas với sao chép nhanh
6. ✅ Sáu bản sao dữ liệu trên ba AZ
7. ✅ Writer endpoint cho kết nối master
8. ✅ Reader endpoint cho kết nối đọc cân bằng tải
9. ✅ Chuyển đổi dự phòng trong vòng chưa đầy 30 giây
10. ✅ Cân bằng tải xảy ra ở cấp độ kết nối, không phải cấp độ câu lệnh

## Tóm Tắt

Amazon Aurora đại diện cho giải pháp của AWS cho cơ sở dữ liệu quan hệ hiệu suất cao và khả dụng cao trong môi trường cloud. Kiến trúc độc đáo với việc tách biệt lưu trữ và tính toán, khả năng mở rộng tự động, và các tính năng nâng cao như backtrack khiến nó trở thành lựa chọn xuất sắc cho các khối lượng công việc production yêu cầu cả hiệu suất và độ tin cậy.




FILE: 40-amazon-s3-security-overview.md


# Tổng Quan về Bảo Mật Amazon S3

## Giới Thiệu

Bảo mật Amazon S3 là một khía cạnh quan trọng trong việc quản lý lưu trữ đám mây của bạn. Hướng dẫn này bao gồm các cơ chế bảo mật chính có sẵn để bảo vệ các bucket và object S3 của bạn.

## Các Cơ Chế Bảo Mật

### 1. Bảo Mật Dựa Trên Người Dùng (User-Based)

**IAM Policies** cho phép bạn kiểm soát các API call nào được phép cho các IAM user cụ thể. Các policy này xác thực quyền truy cập ở cấp độ người dùng, xác định những hành động nào mà mỗi người dùng có thể thực hiện trên tài nguyên S3.

### 2. Bảo Mật Dựa Trên Tài Nguyên (Resource-Based)

#### S3 Bucket Policies
- **Quy tắc áp dụng cho toàn bộ bucket** có thể được gán trực tiếp từ bảng điều khiển S3
- Cho phép người dùng cụ thể truy cập vào bucket của bạn
- Kích hoạt **truy cập cross-account** (cho phép người dùng từ các tài khoản AWS khác)
- Được sử dụng để làm cho bucket S3 công khai
- **Phương pháp phổ biến nhất** để cấu hình bảo mật S3

#### Object Access Control List (ACL)
- Cung cấp **bảo mật chi tiết hơn** ở cấp độ object
- Có thể bị vô hiệu hóa nếu không cần thiết
- Ít được sử dụng trong các triển khai hiện đại

#### Bucket ACL
- Kiểm soát bảo mật ở cấp độ bucket
- Ít phổ biến hơn nhiều so với bucket policies
- Cũng có thể bị vô hiệu hóa

### 3. Mã Hóa (Encryption)
Các object có thể được bảo mật bằng cách sử dụng **encryption keys** để bảo vệ dữ liệu khi lưu trữ.

## Hiểu về S3 Bucket Policies

### Cấu Trúc Policy

S3 Bucket policies là **các tài liệu dựa trên JSON** với các thành phần chính sau:

- **Resource**: Chỉ định bucket và object nào mà policy áp dụng
- **Effect**: `Allow` (Cho phép) hoặc `Deny` (Từ chối)
- **Action**: Các API call được cho phép hoặc bị từ chối (ví dụ: `GetObject`)
- **Principal**: Tài khoản hoặc người dùng mà policy áp dụng

### Ví Dụ: Quyền Đọc Công Khai

```json
{
  "Effect": "Allow",
  "Principal": "*",
  "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::example-bucket/*"
}
```

Policy này cho phép bất kỳ ai (`Principal: "*"`) truy xuất (`GetObject`) bất kỳ object nào (`/*`) từ bucket ví dụ.

### Các Trường Hợp Sử Dụng Phổ Biến

Bucket policies có thể được sử dụng để:
- Cấp **quyền truy cập công khai** cho bucket
- Buộc **các object phải được mã hóa** khi upload
- Cấp **quyền truy cập cho tài khoản AWS khác**

## Các Kịch Bản Kiểm Soát Truy Cập

### Khi Nào IAM Principal Có Thể Truy Cập Object S3?

Một IAM principal có thể truy cập object S3 khi:
1. IAM permissions cho phép, **HOẶC**
2. Resource policy cho phép, **VÀ**
3. **Không có từ chối rõ ràng** (explicit deny) trong hành động

### Kịch Bản 1: Truy Cập Công Khai qua Bucket Policy

```
[Khách Truy Cập Website] → [S3 Bucket với Public Bucket Policy] → [Được Phép Truy Cập]
```

Khách truy cập website từ internet có thể truy cập các file trong S3 bucket của bạn khi một bucket policy cho phép truy cập công khai được gán.

### Kịch Bản 2: Truy Cập của IAM User

```
[IAM User] + [IAM Permissions] → [S3 Bucket] → [Được Phép Truy Cập]
```

Một IAM user trong tài khoản AWS của bạn có thể truy cập S3 bằng cách có IAM permissions được gán thông qua một policy.

### Kịch Bản 3: Truy Cập từ EC2 Instance

```
[EC2 Instance] + [IAM Role] → [S3 Bucket] → [Được Phép Truy Cập]
```

Đối với các EC2 instance, IAM users không phù hợp. Thay vào đó:
- Tạo một **EC2 instance role** với các IAM permissions chính xác
- EC2 instance sau đó có thể truy cập các Amazon S3 bucket

### Kịch Bản 4: Truy Cập Cross-Account

```
[IAM User (Tài khoản B)] → [S3 Bucket Policy] → [S3 Bucket (Tài khoản A)] → [Được Phép Truy Cập]
```

Để truy cập cross-account:
- Sử dụng **S3 Bucket Policy**
- Cấu hình để cho phép truy cập cho các IAM user cụ thể từ tài khoản AWS khác
- IAM user bên ngoài sau đó có thể thực hiện các API call đến S3 bucket của bạn

## Cài Đặt Block Public Access

### Lớp Bảo Mật Bổ Sung

AWS cung cấp **cài đặt Block Public Access cho Bucket** như một lớp bảo mật bổ sung để ngăn chặn rò rỉ dữ liệu của công ty.

### Các Tính Năng Chính

- Ngay cả khi một S3 bucket policy sẽ làm cho bucket trở nên công khai, nếu các cài đặt này được kích hoạt, **bucket sẽ không bao giờ công khai**
- Ngăn chặn rò rỉ dữ liệu do cấu hình sai bucket policy
- Có thể được đặt ở **cấp độ bucket** hoặc **cấp độ tài khoản**

### Thực Hành Tốt Nhất

- Nếu bạn biết bucket của mình **không bao giờ nên công khai**, hãy để các cài đặt này được kích hoạt
- Để bảo vệ toàn tổ chức, hãy đặt cài đặt này ở **cấp độ tài khoản** để đảm bảo không có bucket S3 nào có thể được công khai

## Tóm Tắt

Bảo mật Amazon S3 cung cấp nhiều lớp bảo vệ:
- **Bảo mật dựa trên người dùng** thông qua IAM policies
- **Bảo mật dựa trên tài nguyên** thông qua bucket policies (phổ biến nhất)
- **Access control lists** (ACLs) để kiểm soát chi tiết
- **Mã hóa** để bảo vệ dữ liệu
- **Cài đặt Block Public Access** như một mạng lưới an toàn chống lại cấu hình sai

Sự kết hợp của các cơ chế bảo mật này cho phép bạn triển khai kiểm soát truy cập mạnh mẽ cho các tài nguyên S3 của mình trong khi ngăn chặn việc vô tình để lộ dữ liệu.




FILE: 41-aws-s3-bucket-policy-tutorial.md


# Hướng Dẫn Bucket Policy Cho AWS S3

## Tổng Quan

Hướng dẫn này trình bày cách tạo và áp dụng bucket policy công khai cho Amazon S3 bucket, cho phép truy cập công khai vào các object thông qua URL của chúng.

## Yêu Cầu Trước Khi Bắt Đầu

- Tài khoản AWS với quyền truy cập S3
- S3 bucket đã tồn tại
- Hiểu biết cơ bản về AWS IAM policies

## Bước 1: Cho Phép Truy Cập Công Khai

Theo mặc định, tất cả quyền truy cập công khai vào S3 bucket đều bị chặn vì lý do bảo mật. Để cho phép truy cập công khai:

1. Điều hướng đến S3 bucket của bạn
2. Vào tab **Permissions** (Quyền)
3. Nhấp **Edit** (Chỉnh sửa) trên cài đặt "Block public access" (Chặn truy cập công khai)
4. Bỏ chọn checkbox để cho phép truy cập công khai
5. Xác nhận thay đổi bằng cách gõ "confirm"

> **Cảnh báo**: Chỉ bật truy cập công khai khi bạn thực sự cần thiết. Việc công khai bucket chứa dữ liệu nhạy cảm của công ty có thể dẫn đến rò rỉ dữ liệu. Đây là hành động nguy hiểm và nên được sử dụng thận trọng.

## Bước 2: Xác Minh Trạng Thái Truy Cập Công Khai

Sau khi bật truy cập công khai:
- Trong **Permissions overview**, bạn sẽ thấy "Objects can be public" (Các object có thể công khai)
- Điều này xác nhận bước đầu tiên đã hoàn tất

## Bước 3: Tạo Bucket Policy

### Sử Dụng AWS Policy Generator

1. Cuộn xuống phần **Bucket policy**
2. Nhấp vào **Policy generator** để khởi chạy AWS Policy Generator
3. Cấu hình policy:
   - **Effect**: Allow (Cho phép)
   - **Principal**: `*` (dấu sao để cho phép tất cả mọi người)
   - **AWS Service**: Amazon S3
   - **Actions**: Chọn `GetObject`
   - **Amazon Resource Name (ARN)**: Nhập ARN bucket của bạn với hậu tố `/*`

### Hiểu Định Dạng ARN

Định dạng ARN cho S3 objects là:
```
arn:aws:s3:::bucket-name/*
```

- ARN của bucket có thể tìm thấy trong thuộc tính bucket
- Thêm `/*` vào cuối để áp dụng policy cho tất cả objects trong bucket
- `/*` đại diện cho tất cả objects trong bucket (sau dấu gạch chéo)

### Policy Mẫu

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::ten-bucket-cua-ban/*"
    }
  ]
}
```

## Bước 4: Áp Dụng Policy

1. Nhấp **Add Statement** (Thêm statement) trong policy generator
2. Nhấp **Generate Policy** (Tạo policy)
3. Sao chép policy JSON đã được tạo
4. Dán vào trình soạn thảo bucket policy
5. Xóa bất kỳ khoảng trắng thừa nếu cần
6. Nhấp **Save changes** (Lưu thay đổi)

## Bước 5: Xác Minh Truy Cập Công Khai

1. Điều hướng đến object của bạn (ví dụ: `coffee.jpg`)
2. Tìm **Object URL**
3. Sao chép và dán URL vào trình duyệt
4. Hình ảnh/tệp bây giờ sẽ có thể truy cập công khai

## Các Cân Nhắc Quan Trọng

### Thực Hành Bảo Mật Tốt Nhất

- **Chỉ công khai bucket khi cần thiết**: Bucket công khai sẽ phơi bày tất cả objects chứa trong đó ra internet
- **Xem xét quyền thường xuyên**: Đảm bảo chỉ các objects dự định mới được công khai
- **Sử dụng bucket policies cẩn thận**: Policy cấu hình sai có thể làm lộ dữ liệu nhạy cảm
- **Xem xét các phương án thay thế**: Sử dụng pre-signed URLs để truy cập tạm thời thay vì công khai toàn bộ bucket

### Điểm Chính Cần Nhớ

- Bucket policies kiểm soát quyền truy cập vào tài nguyên S3
- AWS Policy Generator đơn giản hóa việc tạo policy
- Public bucket policies cho phép bất kỳ ai truy cập objects qua URLs của chúng
- Action `GetObject` là bắt buộc để có quyền đọc objects
- Định dạng ARN phải bao gồm `/*` để áp dụng cho tất cả objects trong bucket

## Tài Nguyên Bổ Sung

- [Tài liệu AWS S3 Bucket Policy](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-policies.html)
- [AWS Policy Generator](https://awspolicygen.s3.amazonaws.com/policygen.html)
- [Ví dụ S3 Bucket Policy](https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-bucket-policies.html)

## Kết Luận

Bạn đã học thành công cách:
- Bật truy cập công khai trên S3 bucket
- Tạo bucket policy bằng AWS Policy Generator
- Áp dụng policy để làm cho objects có thể truy cập công khai
- Xác minh truy cập công khai thông qua object URLs

Hãy nhớ luôn tuân theo các thực hành bảo mật tốt nhất và chỉ bật truy cập công khai khi thực sự cần thiết.




FILE: 42-amazon-s3-static-website-hosting.md


# Lưu Trữ Website Tĩnh trên Amazon S3

## Giới Thiệu

Amazon S3 cung cấp một tính năng mạnh mẽ cho phép bạn lưu trữ các website tĩnh và làm cho chúng có thể truy cập được trên internet. Hướng dẫn này sẽ giới thiệu cho bạn các kiến thức cơ bản về lưu trữ website tĩnh trên S3.

## Tổng Quan về Lưu Trữ Website Tĩnh trên S3

S3 có thể lưu trữ các website tĩnh với các file có thể truy cập được trên internet. Định dạng URL của website phụ thuộc vào AWS region nơi bạn tạo bucket.

### Các Định Dạng URL Website

Tùy thuộc vào AWS region của bạn, URL website tĩnh S3 sẽ theo một trong các mẫu sau:

- **Định dạng 1**: `http://bucket-name.s3-website-region.amazonaws.com`
- **Định dạng 2**: `http://bucket-name.s3-website.region.amazonaws.com`

Sự khác biệt chính giữa các định dạng này là tối thiểu - một cái sử dụng dấu gạch ngang (`-`) trong khi cái kia sử dụng dấu chấm (`.`) trong cấu trúc URL. Mặc dù bạn không cần phải ghi nhớ chính xác các định dạng này, nhưng sẽ rất hữu ích khi biết về chúng.

## Cách Hoạt Động

Đây là quy trình cơ bản để lưu trữ website tĩnh trên S3:

1. **Tạo S3 Bucket**: Bucket của bạn sẽ chứa tất cả các file của website
2. **Upload Nội Dung**: Thêm các file HTML, hình ảnh và các tài nguyên tĩnh khác
3. **Bật Tính Năng Static Website Hosting**: Cấu hình bucket để lưu trữ website
4. **Truy Cập qua URL**: Người dùng có thể truy cập website của bạn thông qua URL website S3

## Quan Trọng: Cấu Hình Truy Cập Công Khai

### Lỗi 403 Forbidden

Để website tĩnh của bạn hoạt động đúng cách, bạn phải bật chế độ đọc công khai (public reads) trên S3 bucket. Nếu không có cấu hình này, người dùng sẽ gặp phải **lỗi 403 Forbidden** khi cố gắng truy cập website của bạn.

### Giải Pháp: Bucket Policies

Để làm cho S3 bucket của bạn có thể truy cập công khai:

1. **Đính Kèm S3 Bucket Policy**: Tạo một policy cho phép truy cập đọc công khai
2. **Cấu Hình Public Access Settings**: Đảm bảo bucket của bạn cho phép đọc công khai

Đây là lý do tại sao việc hiểu về S3 bucket policies là rất quan trọng - chúng kiểm soát ai có thể truy cập nội dung của bạn và như thế nào.

## Những Điểm Chính Cần Nhớ

- S3 có thể lưu trữ các website tĩnh có thể truy cập qua internet
- Định dạng URL website thay đổi theo AWS region
- Quyền truy cập đọc công khai phải được bật để website hoạt động
- Một S3 bucket policy phù hợp là cần thiết để tránh lỗi 403
- Luôn đảm bảo bucket của bạn được cấu hình là public nếu bạn muốn người dùng truy cập website tĩnh của bạn

## Các Bước Tiếp Theo

Bây giờ bạn đã hiểu những kiến thức cơ bản về lưu trữ website tĩnh trên S3, đã đến lúc thực hành các khái niệm này bằng cách tạo và cấu hình website tĩnh được lưu trữ trên S3 của riêng bạn.




FILE: 43-aws-s3-static-website-hosting-tutorial.md


# Hướng Dẫn Lưu Trữ Website Tĩnh Trên AWS S3

## Tổng Quan

Hướng dẫn này sẽ đưa bạn qua quy trình kích hoạt tính năng lưu trữ website tĩnh trên Amazon S3 bucket và làm cho nội dung có thể truy cập công khai.

## Yêu Cầu Trước

- Đã có sẵn một S3 bucket
- Các file cần upload (HTML và file hình ảnh)

## Hướng Dẫn Từng Bước

### 1. Upload File Lên S3 Bucket

Đầu tiên, upload các file cần thiết lên S3 bucket của bạn:
- Upload file `beach.jpg` vào bucket
- Xác nhận rằng bạn đã có hai file trong bucket

### 2. Kích Hoạt Static Website Hosting

1. Điều hướng đến tab **Properties** của bucket
2. Cuộn xuống để tìm phần **Static website hosting**
3. Click vào **Edit**
4. Kích hoạt static website hosting
5. Chỉ định `index.html` làm index document (đây là trang mặc định hoặc trang chủ của website)

**Lưu Ý Quan Trọng:** Sẽ có một cảnh báo cho biết rằng để kích hoạt website endpoint, bạn phải làm cho tất cả nội dung có thể đọc công khai. Điều này nên được cấu hình trong bài học trước bằng cách sử dụng bucket policy.

6. Click **Save** để áp dụng các thay đổi

### 3. Upload File Index

1. Quay lại tab **Objects**
2. Click **Upload**
3. Thêm file `index.html`
4. Click **Upload** sau đó **Close**

### 4. Truy Cập Website Tĩnh

1. Quay lại tab **Properties**
2. Cuộn xuống phần **Static website hosting**
3. Bây giờ bạn sẽ thấy URL **bucket website endpoint**
4. Copy URL này và dán vào trình duyệt của bạn

### 5. Xác Minh Website

Khi bạn truy cập website endpoint, bạn sẽ thấy:
- Nội dung từ `index.html` (ví dụ: "I love coffee. Hello world!")
- Hình ảnh `coffee.jpg` được hiển thị trên trang

### 6. Truy Cập Các File Riêng Lẻ

Bạn có thể truy cập các file riêng lẻ trực tiếp thông qua URL công khai của chúng:
- Click chuột phải vào hình ảnh và chọn "Open image in new tab" để xem URL công khai
- Ví dụ, bạn có thể truy cập `beach.jpg` bằng cách thay đổi tham số URL từ `coffee.jpg` thành `beach.jpg`

## Điểm Chính Cần Nhớ

- S3 static website hosting cho phép bạn lưu trữ website tĩnh trực tiếp từ S3 bucket
- Bucket phải có bucket policy công khai để cho phép quyền đọc công khai
- Bạn cần chỉ định index document (thường là `index.html`)
- Mỗi file trong bucket có thể truy cập được qua URL công khai khi bucket policy cho phép
- Bucket website endpoint cung cấp quyền truy cập vào website tĩnh của bạn

## Tóm Tắt

Bằng cách làm theo các bước này, S3 bucket của bạn giờ đã được kích hoạt thành công cho static website hosting. Nhờ vào S3 bucket policy công khai, tất cả các file đều có thể truy cập được, và website của bạn đã hoạt động và sẵn sàng sử dụng.




FILE: 44-amazon-s3-versioning.md


# Amazon S3 Versioning (Quản lý Phiên bản)

## Giới thiệu về Versioning trong Amazon S3

Versioning là một tính năng mạnh mẽ trong Amazon S3 cho phép bạn giữ nhiều phiên bản khác nhau của một đối tượng trong cùng một bucket. Khả năng này rất quan trọng để quản lý các tệp của bạn một cách an toàn và hiệu quả.

## Cách hoạt động của S3 Versioning

Bạn có thể tạo phiên bản cho các tệp của mình trong Amazon S3, và đây là cài đặt bạn phải bật ở cấp độ bucket. Đây là cách nó hoạt động:

1. **Tải lên lần đầu**: Khi người dùng tải lên một tệp, nó sẽ tạo một phiên bản của tệp đó tại khóa đã chọn.

2. **Tải lên tiếp theo**: Nếu bạn tải lại cùng một khóa (ghi đè lên tệp đó), thay vì thay thế nó, S3 sẽ tạo phiên bản hai, sau đó là phiên bản ba, v.v.

## Tại sao nên sử dụng Versioning?

Việc tạo phiên bản cho các bucket của bạn là một best practice vì một số lý do quan trọng:

### Bảo vệ chống lại việc xóa không mong muốn

Khi bạn xóa một phiên bản tệp, S3 thực sự chỉ thêm một delete marker thay vì xóa vĩnh viễn tệp. Điều này có nghĩa là bạn có thể khôi phục các phiên bản trước đó.

### Khả năng rollback dễ dàng

Nếu bạn cần quay lại trạng thái trước đó, bạn có thể dễ dàng rollback về những gì đã xảy ra cách đây vài ngày hoặc thậm chí vài tuần. Chỉ cần chọn tệp và khôi phục nó về phiên bản trước đó.

## Những lưu ý quan trọng về Versioning

- **Các tệp đã tồn tại trước đó**: Bất kỳ tệp nào chưa được tạo phiên bản trước khi bật versioning sẽ có phiên bản là "null".

- **Tạm dừng Versioning**: Nếu bạn tạm dừng versioning, nó không xóa các phiên bản trước đó, vì vậy đây là một thao tác an toàn. Tất cả các phiên bản hiện có vẫn còn nguyên.

## Best Practices (Thực hành tốt nhất)

- Bật versioning trên các bucket chứa dữ liệu quan trọng
- Sử dụng versioning kết hợp với lifecycle policies để tối ưu hóa chi phí
- Thường xuyên xem xét và quản lý các phiên bản cũ để kiểm soát chi phí lưu trữ
- Cân nhắc sử dụng MFA Delete để bảo vệ bổ sung cho các bucket có versioning

## Kết luận

Amazon S3 versioning cung cấp một lưới an toàn cho dữ liệu của bạn, bảo vệ chống lại việc xóa ngẫu nhiên và cho phép khôi phục dễ dàng các phiên bản tệp trước đó. Đây là một tính năng thiết yếu để duy trì tính toàn vẹn của dữ liệu và đảm bảo cập nhật website an toàn.




FILE: 45-aws-s3-versioning-hands-on.md


# AWS S3 Versioning - Hướng dẫn Thực hành

## Giới thiệu

Trong hướng dẫn này, chúng ta sẽ khám phá tính năng versioning (quản lý phiên bản) của S3 và học cách quản lý các phiên bản khác nhau của objects trong S3 bucket.

## Kích hoạt S3 Versioning

Để bật versioning cho S3 bucket của bạn:

1. Truy cập tab **Properties** của bucket
2. Tìm mục cài đặt **Bucket Versioning**
3. Nhấp **Edit** và chọn **Enable**
4. Lưu các thay đổi

Sau khi được kích hoạt, bất kỳ file nào bạn ghi đè sẽ tạo một phiên bản mới thay vì thay thế hoàn toàn file hiện có.

## Upload và Cập nhật Files

Hãy minh họa versioning với một ví dụ thực tế:

### Upload Lần Đầu

1. Mở website tĩnh của bạn được host trên S3
2. Giả sử file `index.html` hiện tại hiển thị "I love coffee"

### Cập nhật Nội dung

1. Chỉnh sửa file `index.html` local của bạn thành "I really love coffee"
2. Lưu file
3. Upload file đã cập nhật lên S3 bucket
4. Việc upload sẽ tạo một phiên bản mới của file

Khi bạn refresh website, bạn sẽ thấy nội dung đã được cập nhật: "I REALLY love coffee."

## Hiểu về Version IDs

Để xem các version IDs:

1. Truy cập tab **Objects** của bucket
2. Bật toggle **Show versions**

Bạn sẽ nhận thấy:

- **Các file được upload trước khi versioning được bật** có version ID là `null` (ví dụ: `beach.jpg`, `coffee.jpg`)
- **Các file được upload sau khi bật versioning** có các version IDs duy nhất
- File `index.html` giờ hiển thị hai phiên bản:
  - Một với version ID `null` (upload trước khi có versioning)
  - Một với version ID duy nhất (lần upload gần đây)

## Rollback về Phiên bản Trước

Để quay lại phiên bản cũ hơn:

1. Đảm bảo **Show versions** được bật
2. Nhấp vào version ID mới hơn mà bạn muốn xóa
3. Chọn **Delete**
4. Thao tác này thực hiện **permanent delete** (xóa vĩnh viễn) phiên bản cụ thể đó
5. Gõ "permanently delete" để xác nhận
6. Nhấp **Delete objects**

Sau khi xóa phiên bản mới hơn, việc refresh website sẽ hiển thị nội dung trước đó: "I love coffee."

## Delete Markers (Dấu hiệu Xóa)

Khi bạn xóa một file mà không bật show versions:

1. Tắt **Show versions**
2. Chọn một file (ví dụ: `coffee.jpg`)
3. Nhấp **Delete**
4. Gõ "delete" để xác nhận

Điều này không xóa vĩnh viễn object. Thay vào đó, S3 tạo một **delete marker**.

### Hiểu về Delete Markers

- File xuất hiện như đã bị xóa trong chế độ xem thông thường
- Với **Show versions** được bật, bạn có thể thấy delete marker
- Các phiên bản file thực tế vẫn còn trong bucket
- Delete marker đóng vai trò là phiên bản hiện tại, che giấu các phiên bản trước đó

### Tác động của Delete Markers

Nếu bạn refresh webpage, các hình ảnh có delete markers sẽ hiển thị là không khả dụng (lỗi 404 Not Found).

## Khôi phục Objects Đã Xóa

Để khôi phục một file có delete marker:

1. Bật **Show versions**
2. Tìm delete marker trên file của bạn
3. Nhấp vào delete marker
4. Chọn **Delete** để xóa vĩnh viễn delete marker
5. Xác nhận việc xóa

Điều này khôi phục phiên bản trước đó của object. Refresh webpage sẽ hiển thị lại file.

## Best Practices (Phương pháp Tốt nhất)

- **Kiểm soát Phiên bản**: Sử dụng versioning để bảo vệ khỏi việc xóa và ghi đè ngoài ý muốn
- **Khôi phục**: Giữ các phiên bản cho các file quan trọng để dễ dàng rollback
- **Chi phí Lưu trữ**: Nhớ rằng mỗi phiên bản tiêu tốn dung lượng lưu trữ
- **Xóa Vĩnh viễn**: Thận trọng khi xóa vĩnh viễn các phiên bản cụ thể - hành động này không thể hoàn tác

## Kết luận

S3 versioning là một tính năng mạnh mẽ cung cấp:
- Bảo vệ khỏi việc xóa ngoài ý muốn
- Khả năng rollback các thay đổi
- Lịch sử phiên bản hoàn chỉnh của các objects

Hãy thoải mái thử nghiệm với versioning bằng cách upload nhiều phiên bản của các files và quan sát hành vi của delete markers và version rollbacks.




FILE: 46-amazon-s3-replication.md


# Sao Chép Amazon S3 (Amazon S3 Replication)

## Tổng Quan

Amazon S3 Replication cho phép bạn sao chép các đối tượng giữa các bucket S3 một cách tự động. Có hai loại sao chép có sẵn:

- **CRR (Cross-Region Replication - Sao Chép Giữa Các Vùng)**: Sao chép giữa các bucket ở các vùng AWS khác nhau
- **SRR (Same-Region Replication - Sao Chép Trong Cùng Vùng)**: Sao chép giữa các bucket trong cùng một vùng AWS

## Cách Hoạt Động Của S3 Replication

S3 Replication cho phép sao chép bất đồng bộ giữa một bucket S3 nguồn ở một vùng và một bucket S3 đích ở vùng khác (hoặc cùng vùng đối với SRR).

### Điều Kiện Tiên Quyết

Để thiết lập S3 Replication, bạn phải:

1. **Bật Versioning** trên cả bucket nguồn và bucket đích
2. **Cấu hình thiết lập vùng phù hợp**:
   - Đối với CRR: Hai vùng phải khác nhau
   - Đối với SRR: Hai vùng giống nhau
3. **Cấp quyền IAM phù hợp** cho dịch vụ S3 để đọc từ bucket nguồn và ghi vào bucket đích

### Các Tính Năng Chính

- Các bucket có thể nằm trong các tài khoản AWS khác nhau
- Quá trình sao chép diễn ra bất đồng bộ ở chế độ nền
- Yêu cầu quyền IAM phù hợp cho dịch vụ S3

## Các Trường Hợp Sử Dụng

### Cross-Region Replication (CRR - Sao Chép Giữa Các Vùng)

- **Tuân Thủ Quy Định**: Đáp ứng các yêu cầu quy định về lưu trữ dữ liệu tại các vị trí địa lý cụ thể
- **Truy Cập Độ Trễ Thấp**: Cung cấp quyền truy cập nhanh hơn vào dữ liệu bằng cách sao chép nó gần hơn với người dùng cuối ở các vùng khác nhau
- **Sao Chép Giữa Các Tài Khoản**: Sao chép dữ liệu giữa các tài khoản AWS khác nhau cho mục đích tổ chức hoặc bảo mật

### Same-Region Replication (SRR - Sao Chép Trong Cùng Vùng)

- **Tổng Hợp Logs**: Hợp nhất logs từ nhiều bucket S3 vào một bucket duy nhất
- **Sao Chép Trực Tiếp**: Duy trì các bản sao được đồng bộ hóa giữa môi trường production và test
- **Dự Phòng Dữ Liệu**: Tạo các bản sao bổ sung của dữ liệu trong cùng một vùng cho mục đích sao lưu

## Tóm Tắt

S3 Replication là một tính năng mạnh mẽ cho phép sao chép tự động và bất đồng bộ các đối tượng giữa các bucket S3. Cho dù bạn cần sao chép giữa các vùng để tuân thủ quy định và tối ưu hóa độ trễ, hay sao chép trong cùng vùng để tổng hợp logs và môi trường test, S3 Replication đều cung cấp một giải pháp đáng tin cậy cho nhu cầu phân phối dữ liệu của bạn.




FILE: 47-amazon-s3-replication-notes.md


# Amazon S3 Replication - Những Lưu Ý Quan Trọng

## Tổng Quan

Tài liệu này trình bày những lưu ý quan trọng về tính năng Amazon S3 Replication và các hành vi chính của nó.

## Các Điểm Chính

### 1. Chỉ Sao Chép Các Đối Tượng Mới

Sau khi bạn kích hoạt Replication, **chỉ các đối tượng mới sẽ được sao chép**. Các đối tượng đã tồn tại trước khi kích hoạt replication sẽ không được tự động sao chép.

### 2. Sao Chép Các Đối Tượng Đã Tồn Tại

Nếu bạn muốn sao chép các đối tượng đã tồn tại, bạn cần sử dụng tính năng **S3 Batch Replication**. Tính năng này cho phép bạn:
- Sao chép các đối tượng đã tồn tại
- Sao chép các đối tượng đã thất bại trong quá trình replication

### 3. Các Thao Tác Xóa

Đối với các thao tác xóa:
- Bạn **có thể** sao chép các delete markers từ bucket nguồn sang bucket đích (đây là cài đặt tùy chọn)
- Nếu bạn có thao tác xóa với version ID, **chúng sẽ không được sao chép**
- Các thao tác xóa vĩnh viễn không được sao chép để tránh các thao tác xóa độc hại xảy ra từ bucket này sang bucket khác

### 4. Không Có Chuỗi Replication

**Không có chuỗi replication** (no chaining of replications).

**Ví dụ:**
- Nếu bucket một có replication sang bucket hai
- Và bucket hai có replication sang bucket ba
- Thì các đối tượng từ bucket một **không** được sao chép vào bucket ba

Mỗi mối quan hệ replication là độc lập và không lan truyền theo chuỗi.

## Tóm Tắt

S3 Replication là một tính năng mạnh mẽ, nhưng điều quan trọng là phải hiểu những hạn chế và hành vi này để cấu hình chiến lược replication của bạn một cách phù hợp và tránh các kết quả không mong muốn.




FILE: 48-aws-s3-replication-hands-on-tutorial.md


# Hướng Dẫn Thực Hành AWS S3 Replication

## Tổng Quan

Hướng dẫn này trình bày cách thiết lập và cấu hình tính năng sao chép (replication) của Amazon S3, bao gồm cả Cross-Region Replication (CRR) và Same-Region Replication (SRR). Bạn sẽ học cách sao chép các đối tượng giữa các S3 bucket và hiểu được cơ chế hoạt động của delete marker cũng như version replication.

## Yêu Cầu Trước Khi Bắt Đầu

- Tài khoản AWS với quyền phù hợp
- Hiểu biết cơ bản về S3 versioning
- Hai S3 bucket (nguồn và đích)

## Bước 1: Tạo Bucket Nguồn (Origin)

1. Truy cập vào S3 console
2. Tạo bucket mới với các thiết lập sau:
   - **Tên bucket**: `s3-stephane-bucket-origin-v2`
   - **Region**: `eu-west-1` (hoặc region bạn muốn)
   - **Bật versioning**: ✓ Bắt buộc cho replication

> **Quan trọng**: Tính năng replication chỉ hoạt động khi versioning được bật trên cả bucket nguồn và bucket đích.

## Bước 2: Tạo Bucket Đích (Destination)

1. Tạo bucket thứ hai:
   - **Tên bucket**: `s3-stephane-bucket-replica-v2`
   - **Region**: `us-east-1` (cho Cross-Region Replication) hoặc cùng region (cho Same-Region Replication)
   - **Bật versioning**: ✓ Bắt buộc

## Bước 3: Upload File Thử Nghiệm Ban Đầu

1. Truy cập vào bucket nguồn
2. Upload một file thử nghiệm (ví dụ: `beach.jpg`)
3. Lưu ý: File này sẽ **không** được tự động sao chép vì quy tắc replication chưa được cấu hình

## Bước 4: Cấu Hình Quy Tắc Replication

1. Trong bucket nguồn, vào tab **Management**
2. Cuộn xuống phần **Replication rules**
3. Click **Create replication rule**
4. Cấu hình các thiết lập sau:

### Cấu Hình Replication Rule

- **Tên quy tắc**: `DemoReplicationRule`
- **Trạng thái**: Enabled (Đã bật)
- **Source bucket**: Áp dụng cho tất cả objects trong bucket
- **Destination** (Đích):
  - Chọn "Bucket in this account" (Bucket trong tài khoản này)
  - Nhập tên bucket đích: `s3-stephane-bucket-replica-v2`
  - Region sẽ được tự động nhận diện (ví dụ: `us-east-1`)
- **IAM Role**: Tạo role mới (tự động cấu hình)

### Xử Lý Các Object Đã Tồn Tại

Khi được hỏi về việc sao chép các object đã tồn tại:
- **Hành vi mặc định**: Replication chỉ áp dụng cho các object được upload **sau khi** quy tắc được tạo
- **Đối với object đã tồn tại**: Sử dụng S3 Batch Operations để sao chép các object đã upload trước đó
- **Trong hướng dẫn này**: Chọn "No, do not replicate existing objects" (Không sao chép object đã tồn tại)

## Bước 5: Kiểm Tra Replication

### Kiểm Tra 1: Upload Object Mới

1. Upload file mới vào bucket nguồn (ví dụ: `coffee.jpg`)
2. Đợi khoảng 5-10 giây
3. Kiểm tra bucket đích - file sẽ xuất hiện với:
   - Cùng tên file
   - Cùng version ID
   - Metadata giống hệt

### Kiểm Tra 2: Xác Minh Version Replication

1. Trong bucket nguồn, click "Show versions"
2. Ghi nhận version ID (ví dụ: `GBk`)
3. Trong bucket đích, click "Show versions"
4. Xác minh rằng version ID khớp chính xác

### Kiểm Tra 3: Upload Phiên Bản Mới Của File Đã Tồn Tại

1. Upload lại `beach.jpg` vào bucket nguồn
2. Một version mới sẽ được tạo (ví dụ: version ID: `DK2`)
3. Kiểm tra bucket đích để xác nhận version mới được sao chép

## Bước 6: Cấu Hình Delete Marker Replication

### Hiểu Về Delete Marker

Theo mặc định, delete marker **không được sao chép**. Để bật tính năng này:

1. Vào **Management** → **Replication rules**
2. Chỉnh sửa replication rule của bạn
3. Cuộn xuống **Delete marker replication**
4. Bật tùy chọn này
5. Lưu thay đổi

### Kiểm Tra Delete Marker Replication

1. Trong bucket nguồn, xóa một file (ví dụ: `coffee.jpg`)
2. Điều này tạo ra delete marker (không phải xóa vĩnh viễn)
3. Đợi vài giây
4. Kiểm tra bucket đích - delete marker sẽ được sao chép
5. Sử dụng "Show versions" để xác minh object vẫn tồn tại nhưng được đánh dấu là đã xóa

## Các Hành Vi Quan Trọng Của Replication

### Những Gì Được Sao Chép

✅ **Được sao chép**:
- Object mới được upload sau khi replication được bật
- Các version của object
- Metadata
- Delete marker (nếu được bật trong cài đặt replication)

### Những Gì KHÔNG Được Sao Chép

❌ **Không được sao chép**:
- Object đã tồn tại trước khi replication được bật (trừ khi dùng Batch Operations)
- Xóa vĩnh viễn các version cụ thể
- Lifecycle actions
- Object được mã hóa bằng SSE-C

### Hành Vi Xóa Vĩnh Viễn (Permanent Delete)

Khi bạn xóa một **version ID cụ thể** (xóa vĩnh viễn):
- Hành động này **KHÔNG được sao chép** đến bucket đích
- Chỉ có delete marker được sao chép
- Object vẫn tồn tại trong bucket đích

**Ví dụ**:
1. Xóa vĩnh viễn version của `beach.jpg` trong bucket nguồn
2. File vẫn còn trong bucket replica
3. Chỉ có delete marker được sao chép, không phải xóa vĩnh viễn

## Các Loại Replication

### Cross-Region Replication (CRR)
- Sao chép object qua các AWS region khác nhau
- Trường hợp sử dụng: Tuân thủ quy định, truy cập với độ trễ thấp hơn, khôi phục thảm họa

### Same-Region Replication (SRR)
- Sao chép object trong cùng một AWS region
- Trường hợp sử dụng: Tổng hợp log, sao chép trực tiếp giữa tài khoản production và test

## Những Điểm Chính Cần Nhớ

1. **Versioning là bắt buộc** trên cả bucket nguồn và bucket đích
2. **Replication là bất đồng bộ** - mong đợi độ trễ vài giây
3. **Chỉ object mới được sao chép** theo mặc định sau khi bật replication
4. **Delete marker có thể được sao chép** nếu được bật rõ ràng
5. **Xóa vĩnh viễn không bao giờ được sao chép** để duy trì tính toàn vẹn dữ liệu
6. **Version ID được giữ nguyên** trong quá trình replication
7. **IAM role được tự động tạo** để quản lý quyền replication

## Dọn Dẹp

Để tránh chi phí liên tục:

1. Làm trống cả hai bucket (xóa tất cả object và version)
2. Xóa replication rule
3. Xóa cả hai S3 bucket
4. Xóa IAM role được tạo cho replication

## Kết Luận

S3 replication là một tính năng mạnh mẽ cho dự phòng dữ liệu, tuân thủ quy định và khôi phục thảm họa. Hiểu rõ cách hoạt động của delete marker và version replication là rất quan trọng cho các kỳ thi chứng chỉ AWS và triển khai thực tế.

## Các Bước Tiếp Theo

- Khám phá S3 Batch Replication cho các object đã tồn tại
- Tìm hiểu về Replication Time Control (RTC) cho replication có thể dự đoán
- Nghiên cứu S3 lifecycle policies kết hợp với replication
- Xem xét các số liệu và giám sát S3 replication




FILE: 49-amazon-s3-storage-classes-overview.md


# Tổng Quan Các Lớp Lưu Trữ Amazon S3

## Giới Thiệu

Amazon S3 cung cấp nhiều lớp lưu trữ được thiết kế cho các trường hợp sử dụng khác nhau, mỗi lớp có các đặc điểm về tính khả dụng, độ bền và giá cả khác nhau. Hiểu rõ các lớp lưu trữ này là điều cần thiết để tối ưu hóa chi phí và hiệu suất.

## Các Lớp Lưu Trữ Có Sẵn

Amazon S3 cung cấp các lớp lưu trữ sau:

1. **Amazon S3 Standard - Mục Đích Chung**
2. **Amazon S3 - Infrequent Access (IA) - Truy Cập Không Thường Xuyên**
3. **Amazon S3 One Zone - Infrequent Access - Một Vùng Truy Cập Không Thường Xuyên**
4. **Amazon S3 Glacier Instant Retrieval - Truy Xuất Tức Thời**
5. **Amazon S3 Glacier Flexible Retrieval - Truy Xuất Linh Hoạt**
6. **Amazon S3 Glacier Deep Archive - Lưu Trữ Sâu**
7. **Amazon S3 Intelligent-Tiering - Phân Tầng Thông Minh**

### Quản Lý Các Lớp Lưu Trữ

Khi tạo một đối tượng trong Amazon S3, bạn có thể:
- Chọn lớp lưu trữ khi tạo
- Thay đổi lớp lưu trữ thủ công sau khi tạo
- Sử dụng **cấu hình Amazon S3 Lifecycle** để tự động di chuyển đối tượng giữa các lớp lưu trữ

## Khái Niệm Cơ Bản: Độ Bền và Tính Khả Dụng

### Độ Bền (Durability)

**Độ bền** thể hiện tần suất một đối tượng bị mất bởi Amazon S3.

- Amazon S3 có độ bền rất cao: **11 số 9 (99.999999999%)**
- Điều này có nghĩa là trung bình, nếu bạn lưu trữ 10 triệu đối tượng trên Amazon S3, bạn có thể mất một đối tượng duy nhất mỗi 10,000 năm
- **Độ bền giống nhau cho tất cả các lớp lưu trữ** trong Amazon S3

### Tính Khả Dụng (Availability)

**Tính khả dụng** thể hiện mức độ sẵn sàng của dịch vụ.

- Tính khả dụng thay đổi tùy thuộc vào lớp lưu trữ
- Ví dụ, S3 Standard có **tính khả dụng 99.99%**
- Điều này có nghĩa là khoảng 53 phút mỗi năm dịch vụ có thể không khả dụng
- Ứng dụng nên được thiết kế để xử lý các lỗi dịch vụ thỉnh thoảng

## Chi Tiết Các Lớp Lưu Trữ

### 1. Amazon S3 Standard - Mục Đích Chung

**Đặc điểm:**
- **Tính khả dụng:** 99.99%
- **Trường hợp sử dụng:** Dữ liệu được truy cập thường xuyên
- **Hiệu suất:** Độ trễ thấp và thông lượng cao
- **Khả năng phục hồi:** Có thể chịu được hai lỗi cơ sở vật chất đồng thời

**Phù hợp cho:**
- Phân tích dữ liệu lớn (Big data analytics)
- Ứng dụng di động và game
- Phân phối nội dung

### 2. Amazon S3 Standard - Infrequent Access (Standard-IA)

**Đặc điểm:**
- **Tính khả dụng:** 99.9% (thấp hơn một chút so với Standard)
- **Trường hợp sử dụng:** Dữ liệu được truy cập ít thường xuyên nhưng cần truy cập nhanh khi cần
- **Chi phí:** Chi phí lưu trữ thấp hơn S3 Standard, nhưng có phí truy xuất

**Phù hợp cho:**
- Khắc phục thảm họa (Disaster recovery)
- Sao lưu dự phòng (Backups)

### 3. Amazon S3 One Zone - Infrequent Access (One Zone-IA)

**Đặc điểm:**
- **Tính khả dụng:** 99.5%
- **Độ bền:** Độ bền cao chỉ trong một Vùng Khả Dụng (AZ)
- **Rủi ro:** Dữ liệu sẽ bị mất nếu AZ bị phá hủy
- **Chi phí:** Thấp hơn Standard-IA

**Phù hợp cho:**
- Bản sao lưu thứ cấp
- Sao lưu dữ liệu on-premises
- Dữ liệu có thể tái tạo được

## Các Lớp Lưu Trữ Glacier

Amazon Glacier cung cấp lưu trữ đối tượng chi phí thấp dành cho lưu trữ và sao lưu. Tất cả các lớp Glacier có:
- Chi phí lưu trữ cộng với chi phí truy xuất
- Yêu cầu thời gian lưu trữ tối thiểu

### 4. Amazon S3 Glacier Instant Retrieval - Truy Xuất Tức Thời

**Đặc điểm:**
- **Thời gian truy xuất:** Mili giây
- **Thời gian lưu trữ tối thiểu:** 90 ngày
- **Trường hợp sử dụng:** Dữ liệu được truy cập một lần mỗi quý

**Phù hợp cho:**
- Sao lưu cần truy cập ngay lập tức
- Dữ liệu lưu trữ dài hạn với nhu cầu truy xuất tức thời

### 5. Amazon S3 Glacier Flexible Retrieval - Truy Xuất Linh Hoạt

Trước đây được gọi là "Amazon S3 Glacier"

**Các Tùy Chọn Truy Xuất:**
- **Expedited (Nhanh):** 1-5 phút
- **Standard (Tiêu chuẩn):** 3-5 giờ
- **Bulk (Hàng loạt):** 5-12 giờ (miễn phí)

**Đặc điểm:**
- **Thời gian lưu trữ tối thiểu:** 90 ngày
- Thời gian truy xuất linh hoạt dựa trên nhu cầu của bạn

### 6. Amazon S3 Glacier Deep Archive - Lưu Trữ Sâu

**Đặc điểm:**
- **Các Tùy Chọn Truy Xuất:**
  - Standard (Tiêu chuẩn): 12 giờ
  - Bulk (Hàng loạt): 48 giờ
- **Thời gian lưu trữ tối thiểu:** 180 ngày
- **Chi phí:** Tùy chọn lưu trữ có chi phí thấp nhất

**Phù hợp cho:**
- Lưu trữ dài hạn
- Dữ liệu hiếm khi cần truy cập
- Lưu trữ tuân thủ và quy định

## 7. Amazon S3 Intelligent-Tiering - Phân Tầng Thông Minh

Tự động di chuyển đối tượng giữa các tầng truy cập dựa trên mẫu sử dụng.

**Chi phí:**
- Phí giám sát hàng tháng nhỏ
- Phí tự động phân tầng nhỏ
- **Không có phí truy xuất**

**Các Tầng Tự Động:**
1. **Frequent Access Tier (Tầng Truy Cập Thường Xuyên)** - Tầng mặc định (tự động)
2. **Infrequent Access Tier (Tầng Truy Cập Không Thường Xuyên)** - Đối tượng không được truy cập trong 30 ngày (tự động)
3. **Archive Instant Access Tier (Tầng Lưu Trữ Truy Cập Tức Thời)** - Đối tượng không được truy cập trong 90 ngày (tự động)

**Các Tầng Tùy Chọn** (có thể cấu hình):
4. **Archive Access Tier (Tầng Truy Cập Lưu Trữ)** - Có thể cấu hình từ 90 đến 700+ ngày
5. **Deep Archive Access Tier (Tầng Truy Cập Lưu Trữ Sâu)** - Có thể cấu hình từ 180 đến 700+ ngày

**Phù hợp cho:**
- Mẫu truy cập không thể dự đoán
- Tối ưu hóa chi phí tự động mà không cần can thiệp thủ công

## Tổng Kết So Sánh

### Điểm Chính

- **Độ bền:** 11 số 9 (99.999999999%) trên tất cả các lớp lưu trữ
- **Tính khả dụng:** Thay đổi theo lớp lưu trữ - giảm khi có ít vùng hơn
- **Thời gian lưu trữ tối thiểu:** Thay đổi theo lớp (0, 90 hoặc 180 ngày)
- **Giá cả:** Thường giảm với thời gian truy xuất dài hơn và tính khả dụng thấp hơn

### Lưu Ý Quan Trọng

- Bạn không cần ghi nhớ các con số chính xác cho chứng chỉ
- Hiểu mục đích và trường hợp sử dụng của mỗi lớp quan trọng hơn
- Giá thay đổi theo khu vực (ví dụ: us-east-1)
- Xem tài liệu giá cho các yêu cầu cụ thể

## Thực Hành Tốt Nhất

1. **Chọn lớp lưu trữ phù hợp** dựa trên mẫu truy cập
2. **Sử dụng chính sách S3 Lifecycle** để tự động chuyển đổi đối tượng
3. **Xem xét chi phí truy xuất** khi chọn các lớp truy cập không thường xuyên
4. **Sử dụng Intelligent-Tiering** khi mẫu truy cập không thể dự đoán
5. **Lên kế hoạch cho yêu cầu về tính khả dụng** trong thiết kế ứng dụng của bạn

## Kết Luận

Các lớp lưu trữ Amazon S3 cung cấp các tùy chọn linh hoạt để tối ưu hóa chi phí trong khi đáp ứng các yêu cầu về hiệu suất và tính khả dụng. Bằng cách hiểu các đặc điểm của từng lớp lưu trữ, bạn có thể đưa ra quyết định sáng suốt về nơi lưu trữ dữ liệu của mình để tối ưu chi phí.

---

*Để biết giá cả và thông số kỹ thuật mới nhất, vui lòng tham khảo tài liệu chính thức của AWS S3.*




FILE: 5-amazon-aurora-hands-on-tutorial.md


# Hướng Dẫn Thực Hành Amazon Aurora

## Tổng Quan

Hướng dẫn này sẽ giúp bạn tạo và cấu hình cơ sở dữ liệu Amazon Aurora trên AWS. Aurora là dịch vụ cơ sở dữ liệu quan hệ hiệu suất cao, có tính sẵn sàng cao, tương thích với MySQL và PostgreSQL.

> **Lưu ý:** Việc làm theo hướng dẫn thực hành này sẽ phát sinh chi phí AWS. Bạn có thể theo dõi mà không cần thực sự tạo cơ sở dữ liệu để hiểu các tùy chọn có sẵn.

## Tạo Cơ Sở Dữ Liệu Amazon Aurora

### Bước 1: Chọn Phương Thức Tạo Database

Chọn **Standard Create** (Tạo tiêu chuẩn) để có toàn quyền kiểm soát tất cả các tùy chọn cấu hình.

### Bước 2: Chọn Database Engine

Aurora cung cấp hai tùy chọn tương thích:
- **Tương thích MySQL**
- **Tương thích PostgreSQL**

Trong hướng dẫn này, chúng ta sẽ sử dụng Aurora **tương thích MySQL**.

### Bước 3: Chọn Phiên Bản Database

- Sử dụng **bộ chọn phiên bản** để chọn phiên bản Aurora của bạn
- Các bộ lọc có sẵn:
  - Hỗ trợ tính năng global database
  - Hỗ trợ tính năng parallel query
  - Hỗ trợ tính năng Serverless v2
- Phiên bản mặc định hiển thị: **3.04.1** (có thể khác tùy theo AWS cung cấp)

### Bước 4: Chọn Template

Chọn template **Production** để truy cập tất cả các tùy chọn cấu hình.

### Bước 5: Cài Đặt Database

**DB Cluster Identifier:** `database-two` (hoặc tên bạn ưa thích)

**Thông Tin Master:**
- Username: `admin`
- Password: [Nhập mật khẩu bảo mật của bạn]

### Bước 6: Cấu Hình Cluster Storage

Chọn giữa hai tùy chọn lưu trữ:

| Loại Storage | Phù Hợp Cho |
|-------------|-------------|
| **Aurora Standard** | Khối lượng công việc tiết kiệm chi phí với I/O vừa phải |
| **Aurora I/O Optimized** | Các hoạt động đầu vào/đầu ra cao (đọc/ghi chuyên sâu) |

Đối với hầu hết các trường hợp sử dụng, chọn **Aurora Standard**.

### Bước 7: Cấu Hình Instance

**Các Tùy Chọn Instance Class:**
- **Memory Optimized** - Cho khối lượng công việc hiệu suất cao
- **Burstable Classes** - Cho khối lượng công việc biến đổi
- Previous generation classes (tùy chọn)

Cho hướng dẫn này: **db.t3.medium**

**Tùy Chọn Serverless v2:**
Nếu phiên bản Aurora của bạn hỗ trợ Serverless:
- Thay vì chọn loại instance, cấu hình Aurora Capacity Units (ACU)
- Đặt ACU tối thiểu và tối đa cho tự động mở rộng
- Database tự động mở rộng giữa các đơn vị công suất này

### Bước 8: Tính Sẵn Sàng và Độ Bền

**Aurora Replicas:**
- Tạo Aurora replica trong Availability Zone (AZ) khác
- Lợi ích:
  - Tăng cường tính sẵn sàng
  - Cải thiện hiệu suất đọc trên các AZ
  - Chuyển đổi dự phòng tự động nhanh chóng
- Lưu ý: Tùy chọn này làm tăng chi phí nhưng cung cấp đầy đủ khả năng của Aurora

### Bước 9: Cấu Hình Kết Nối

**Compute Resource:** Không kết nối với EC2 instance

**Network Type:** IPv4 (hoặc dual-stack cho hỗ trợ IPv6)

**Cấu Hình VPC:**
- Sử dụng VPC mặc định
- Sử dụng subnet group mặc định

**Public Access:** Bật (cho phép kết nối từ địa chỉ IP công cộng)

**VPC Security Group:**
- Tạo security group mới
- Tên: `demo-database-aurora`
- Cho phép kết nối đến Aurora database

### Bước 10: Cấu Hình Bổ Sung

**Database Port:** 3306 (cổng mặc định của MySQL)

**Các Tính Năng Nâng Cao:**

1. **Local Write Forwarding**
   - Chuyển tiếp ghi từ read replica đến write instance tự động
   - Đơn giản hóa quản lý kết nối

2. **Tùy Chọn Xác Thực Database:**
   - **IAM-based authentication** - Sử dụng IAM roles để truy cập database
   - **Kerberos-based authentication** - Cơ chế xác thực bên ngoài

3. **Enhanced Monitoring:** Có thể tắt cho hướng dẫn này

4. **Tùy Chọn Database:**
   - Tên database ban đầu: `myDB`
   - Lưu giữ backup: 1 ngày
   - Mã hóa: Có sẵn
   - Backtracking: Khả năng tua lại database
   - Log exports: Các tùy chọn logging khác nhau

5. **Deletion Protection:** Bảo vệ database khỏi bị xóa nhầm

### Bước 11: Xem Xét và Tạo

- Xem xét ước tính chi phí hàng tháng
- Nhấp **Create Database**

## Hiểu Về Aurora Cluster Của Bạn

### Các Thành Phần Cluster

Sau khi tạo, Aurora cluster của bạn bao gồm:
- **Regional cluster** với:
  - Một **Writer instance**
  - Một **Reader instance**
- Các instance nằm ở **các Availability Zone khác nhau**

### Connection Endpoints

Aurora cung cấp nhiều loại endpoint:

| Loại Endpoint | Mục Đích | Trường Hợp Sử Dụng |
|--------------|----------|---------------------|
| **Writer Endpoint** | Luôn kết nối đến write instance | Ghi dữ liệu từ ứng dụng |
| **Reader Endpoint** | Luôn kết nối đến read replica | Đọc dữ liệu từ ứng dụng |
| **Instance-specific Endpoints** | Kết nối trực tiếp đến instance cụ thể | Trường hợp sử dụng nâng cao |

> **Thực Hành Tốt Nhất:** Ứng dụng nên sử dụng Writer và Reader endpoints thay vì các endpoint cụ thể của instance.

## Các Tính Năng Nâng Cao

### 1. Thêm Read Replica

- Thêm reader bổ sung vào reader cluster của bạn
- Tăng khả năng mở rộng đọc
- Có thể có tới 15 Aurora replicas

### 2. Cross-Region Read Replicas

- Tạo read replica ở các AWS region khác
- Cải thiện hiệu suất đọc cho các ứng dụng phân tán địa lý
- Cung cấp khả năng phục hồi thảm họa

### 3. Point-in-Time Restore

- Khôi phục database về bất kỳ thời điểm nào trong thời gian lưu giữ backup
- Hữu ích cho các tình huống khôi phục dữ liệu

### 4. Read Replica Auto-Scaling

Cấu hình chính sách tự động mở rộng:

```
Tên Policy: read-replica-scaling-policy
Target Metric: Average CPU Utilization hoặc Connection Count
Target Value: 60%
Min Capacity: 1 replica
Max Capacity: 15 replicas
```

**Cách hoạt động:**
- Giám sát mức sử dụng replica hoặc kết nối
- Tự động thêm replica khi vượt quá ngưỡng
- Thu nhỏ quy mô khi tải giảm
- Có thể xác định thời gian mở rộng cho policy

### 5. Global Database

**Yêu Cầu:**
- Phiên bản Aurora có tính năng global database được bật
- Loại instance đủ lớn cho replikasi toàn cầu

**Khả Năng:**
- Thêm các region database trên nhiều AWS region
- Tạo triển khai Aurora toàn cầu thực sự
- Đọc toàn cầu với độ trễ thấp

**Lưu ý:** Một số loại instance có thể cần được nâng cấp (ví dụ: lên loại instance large) trước khi thêm các region toàn cầu.

## Lợi Ích Chính Của Aurora

- **Hiệu suất tuyệt vời** - Nhanh hơn tới 5 lần so với MySQL tiêu chuẩn
- **Tính sẵn sàng cao** - Chuyển đổi dự phòng tự động trên các AZ
- **Khả năng mở rộng** - Tự động mở rộng với read replicas
- **Khả năng toàn cầu** - Tùy chọn triển khai đa vùng
- **Tùy chọn Serverless** - Tự động mở rộng công suất
- **Giải pháp hoàn chỉnh** - Dịch vụ database được quản lý toàn diện

## Xóa Aurora Database Của Bạn

Để tránh phí liên tục, làm theo các bước sau **theo thứ tự**:

### Bước 1: Xóa Reader Instance
1. Chọn reader instance
2. Chọn **Actions** → **Delete**
3. Gõ `delete me` để xác nhận

### Bước 2: Xóa Writer Instance
1. Chọn writer instance
2. Chọn **Actions** → **Delete**
3. Gõ `delete me` để xác nhận

### Bước 3: Xóa Database Cluster
1. Đợi cả hai instance bị xóa
2. Chọn database cluster
3. Chọn **Actions** → **Delete**
4. Xác nhận xóa

> **Quan Trọng:** Bạn không thể xóa cluster cho đến khi cả reader và writer instance được xóa trước.

## Tóm Tắt

Amazon Aurora là dịch vụ cơ sở dữ liệu quan hệ hàng đầu của AWS, cung cấp:
- Hiệu suất và khả năng mở rộng cao
- Tương thích với MySQL và PostgreSQL
- Replikasi và chuyển đổi dự phòng tự động
- Tự động mở rộng read replica
- Khả năng global database
- Tùy chọn serverless cho khối lượng công việc biến đổi

Điều này làm cho Aurora trở thành lựa chọn tuyệt vời cho các khối lượng công việc production yêu cầu độ tin cậy, hiệu suất và khả năng mở rộng.




FILE: 50-aws-s3-storage-classes-hands-on-tutorial.md


# AWS S3 Storage Classes - Hướng Dẫn Thực Hành

## Tổng Quan
Hướng dẫn này trình bày cách làm việc với các lớp lưu trữ (storage classes) khác nhau của Amazon S3, bao gồm cách thiết lập storage class khi tải lên đối tượng, thay đổi storage class thủ công và tự động hóa chuyển đổi bằng lifecycle rules.

## Tạo S3 Bucket

Đầu tiên, hãy tạo một S3 bucket mới để thực hành:

1. Tạo bucket mới với tên `s3-storage-classes-demos-2022`
2. Chọn bất kỳ region nào bạn muốn
3. Nhấp **Create Bucket**

## Tìm Hiểu Về S3 Storage Classes

Khi tải lên một đối tượng lên S3, bạn có thể chọn từ nhiều storage classes khác nhau. Hãy cùng tìm hiểu từng tùy chọn:

### Các Storage Classes Khả Dụng

#### 1. **S3 Standard**
- Lớp lưu trữ mặc định
- Được thiết kế cho dữ liệu truy cập thường xuyên
- Được lưu trữ trên nhiều Availability Zones (AZs)
- Cung cấp độ trễ thấp và thông lượng cao

#### 2. **S3 Intelligent-Tiering**
- Lý tưởng khi bạn không biết mẫu truy cập dữ liệu của mình
- AWS tự động di chuyển các đối tượng giữa các tiers dựa trên mẫu truy cập
- Bao gồm phí giám sát và tự động phân tiers
- Tối ưu hóa chi phí tự động

#### 3. **S3 Standard-IA (Infrequent Access)**
- Dành cho dữ liệu được truy cập ít thường xuyên
- Vẫn cung cấp độ trễ thấp khi được truy cập
- Chi phí lưu trữ thấp hơn Standard
- Áp dụng thời gian lưu trữ tối thiểu
- Kích thước đối tượng tính phí tối thiểu

#### 4. **S3 One Zone-IA**
- Lưu trữ dữ liệu chỉ trong một Availability Zone duy nhất
- Chi phí thấp hơn Standard-IA
- Phù hợp cho dữ liệu có thể tái tạo nếu bị mất
- **Rủi ro**: Dữ liệu có thể bị mất nếu AZ bị hỏng

#### 5. **S3 Glacier Storage Classes**

**Glacier Instant Retrieval**
- Dành cho dữ liệu lưu trữ cần truy cập ngay lập tức
- Chi phí thấp hơn Standard-IA
- Thời gian truy xuất tính bằng mili giây

**Glacier Flexible Retrieval**
- Dành cho dữ liệu lưu trữ với thời gian truy xuất linh hoạt
- Tùy chọn truy xuất: vài phút đến vài giờ
- Chi phí lưu trữ rất thấp

**Glacier Deep Archive**
- Lớp lưu trữ có chi phí thấp nhất
- Dành cho lưu trữ dài hạn và bảo quản kỹ thuật số
- Thời gian truy xuất: 12-48 giờ

#### 6. **Reduced Redundancy (Đã Ngừng Sử Dụng)**
- Lớp lưu trữ này đã bị ngừng sử dụng
- Không còn được khuyến nghị sử dụng

## Thực Hành: Tải Lên Đối Tượng Với Storage Classes

### Bước 1: Tải Lên Đối Tượng

1. Điều hướng đến bucket của bạn
2. Nhấp **Upload**
3. Nhấp **Add Files** và chọn một tệp (ví dụ: `coffee.JPEG`)
4. Trước khi tải lên, vào **Properties**
5. Trong **Storage Class**, chọn lớp bạn muốn (ví dụ: **Standard-IA**)
6. Nhấp **Upload**

### Bước 2: Xác Minh Storage Class

Sau khi tải lên, bạn có thể xác minh storage class:
- Chọn đối tượng trong bucket của bạn
- Storage class sẽ được hiển thị (ví dụ: `Standard-IA`)

## Thay Đổi Storage Classes Thủ Công

Bạn có thể thay đổi storage class của một đối tượng bất kỳ lúc nào:

1. Chọn đối tượng trong bucket của bạn
2. Vào **Properties**
3. Cuộn xuống **Storage Class**
4. Nhấp **Edit**
5. Chọn storage class mới (ví dụ: **One Zone-IA**)
6. Nhấp **Save Changes**

Đối tượng bây giờ sẽ được lưu trữ trong storage class mới. Bạn có thể lặp lại quy trình này để di chuyển giữa bất kỳ storage classes nào, chẳng hạn như:
- Di chuyển đến **Glacier Instant Retrieval** để lưu trữ
- Di chuyển đến **Intelligent-Tiering** để tối ưu hóa tự động

## Tự Động Hóa Chuyển Đổi Storage Class Với Lifecycle Rules

Thay vì thay đổi storage classes thủ công, bạn có thể tự động hóa quy trình bằng cách sử dụng S3 Lifecycle Rules.

### Tạo Lifecycle Rule

1. Điều hướng đến bucket của bạn
2. Vào tab **Management**
3. Nhấp **Create Lifecycle Rule**

### Cấu Hình Rule

1. **Rule Name**: Nhập tên (ví dụ: `DemoRule`)
2. **Rule Scope**: Chọn áp dụng cho tất cả các đối tượng trong bucket (hoặc chỉ định prefix/tag)
3. Nhấp **Acknowledge** khi được nhắc

### Thiết Lập Transitions

Cấu hình transitions cho phiên bản hiện tại của các đối tượng:

**Ví Dụ Lịch Trình Chuyển Đổi:**
- Sau **30 ngày**: Di chuyển đến **Standard-IA**
- Sau **60 ngày**: Di chuyển đến **Intelligent-Tiering**
- Sau **180 ngày**: Di chuyển đến **Glacier Flexible Retrieval**

Bạn có thể thêm nhiều transitions tùy theo yêu cầu vòng đời dữ liệu của mình.

### Xem Xét và Tạo

1. Xem xét tất cả các transitions đã cấu hình
2. Xác minh timeline chuyển đổi
3. Nhấp **Create Rule**

## Những Điểm Chính Cần Nhớ

- **Nhiều Storage Classes**: S3 cung cấp nhiều storage classes được tối ưu hóa cho các mẫu truy cập và yêu cầu chi phí khác nhau
- **Linh Hoạt**: Bạn có thể thay đổi storage classes thủ công bất kỳ lúc nào
- **Tự Động Hóa**: Lifecycle rules cho phép chuyển đổi tự động dựa trên tuổi của đối tượng
- **Tối Ưu Chi Phí**: Chọn storage class phù hợp có thể giảm đáng kể chi phí lưu trữ
- **Độ Bền Dữ Liệu**: Hầu hết các storage classes (trừ One Zone-IA) lưu trữ dữ liệu trên nhiều AZs để có độ bền cao

## Thực Hành Tốt Nhất

1. **Sử dụng Standard** cho dữ liệu được truy cập thường xuyên
2. **Sử dụng Intelligent-Tiering** khi mẫu truy cập không xác định hoặc thay đổi
3. **Sử dụng Standard-IA hoặc One Zone-IA** cho dữ liệu truy cập không thường xuyên
4. **Sử dụng Glacier classes** cho lưu trữ dài hạn
5. **Triển khai Lifecycle Rules** để tự động tối ưu hóa chi phí
6. **Xem xét thời gian lưu trữ tối thiểu** khi lập kế hoạch chuyển đổi

## Kết Luận

AWS S3 Storage Classes cung cấp các tùy chọn mạnh mẽ để tối ưu hóa chi phí lưu trữ trong khi duy trì mức độ truy cập và độ bền phù hợp cho dữ liệu của bạn. Bằng cách hiểu từng storage class và triển khai lifecycle rules, bạn có thể đảm bảo dữ liệu của mình được lưu trữ một cách hiệu quả về chi phí trong suốt vòng đời của nó.

---

*Hướng dẫn này là một phần của khóa học AWS Storage Services.*




FILE: 51-ec2-instance-metadata-imds.md


# EC2 Instance Metadata (IMDS)

## Tổng Quan

Dịch vụ EC2 Instance Metadata Service (IMDS) là một tính năng mạnh mẽ cho phép các EC2 instance tự tìm hiểu thông tin về chính chúng mà không cần sử dụng IAM Role. Tính năng này không được nhiều nhà phát triển biết đến nhưng là một phần cơ bản trong cách hoạt động của EC2 instance.

## IMDS là gì?

Instance Metadata Service (IMDS) cho phép các EC2 instance truy xuất thông tin về chính chúng bằng cách truy cập một URL endpoint cụ thể:

```
http://169.254.169.254
```

## Thông Tin Có Sẵn

Thông qua metadata service, bạn có thể truy xuất:

- **Tên instance**
- **Địa chỉ IP công khai**
- **Địa chỉ IP riêng tư**
- **Tên IAM Role**
- **Thông tin xác thực bảo mật tạm thời** (nếu có IAM role được gán)
- **User data** (các script khởi chạy)

**Lưu ý:** Mặc dù bạn có thể truy xuất tên IAM Role và thông tin xác thực, bạn không thể truy xuất chính sách IAM được gán cho role thông qua metadata service.

## Metadata và User Data

- **Metadata**: Thông tin về chính EC2 instance
- **User Data**: Các script khởi chạy và dữ liệu cấu hình được sử dụng trong quá trình khởi động instance

Cả hai đều có thể được truy cập thông qua cùng một URL endpoint.

## Các Phiên Bản IMDS

### IMDSv1 (Phiên Bản Cũ)

Phiên bản gốc của Instance Metadata Service:

- **Phương thức truy cập**: Truy cập URL trực tiếp
- **Bảo mật**: Mô hình bảo mật cơ bản
- **Sử dụng**: Các yêu cầu GET đơn giản đến metadata endpoint

```bash
# Ví dụ yêu cầu IMDSv1
curl http://169.254.169.254/latest/meta-data/
```

### IMDSv2 (Được Khuyến Nghị)

Được giới thiệu và bật mặc định từ năm 2023, IMDSv2 cung cấp bảo mật nâng cao:

- **Phương thức truy cập**: Yêu cầu theo phiên làm việc
- **Bảo mật**: Yêu cầu xác thực bằng session token
- **Sử dụng**: Quy trình hai bước

#### Các Bước Truy Cập IMDSv2

**Bước 1: Lấy session token**

Sử dụng yêu cầu PUT để lấy session token:

```bash
TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`
```

**Bước 2: Sử dụng token để truy cập metadata**

Truyền token trong header của yêu cầu:

```bash
curl http://169.254.169.254/latest/meta-data/ \
  -H "X-aws-ec2-metadata-token: $TOKEN"
```

## Cải Tiến Bảo Mật trong IMDSv2

IMDSv2 được AWS giới thiệu để tăng cường bảo mật:

- **Định hướng phiên**: Yêu cầu xác thực dựa trên token
- **Bảo vệ chống tấn công SSRF**: Giảm nguy cơ tấn công Server-Side Request Forgery
- **Token hết hạn**: Token có TTL (Time To Live) có thể cấu hình
- **Chi phí bổ sung**: Yêu cầu quy trình hai bước nhưng cung cấp bảo mật tốt hơn

## Thực Hành Tốt Nhất

1. **Sử dụng IMDSv2**: Luôn ưu tiên IMDSv2 thay vì IMDSv1 để có bảo mật tốt hơn
2. **Quản lý token**: Đặt giá trị TTL phù hợp cho session token
3. **Truy cập an toàn**: Đảm bảo metadata service chỉ có thể truy cập từ bên trong instance
4. **Giám sát sử dụng**: Theo dõi truy cập metadata service để kiểm toán bảo mật

## Tóm Tắt

EC2 Instance Metadata Service là một tính năng quan trọng cho phép các instance tự khám phá cấu hình và thông tin xác thực của chúng. Với việc giới thiệu IMDSv2, AWS đã cải thiện đáng kể tính bảo mật của dịch vụ này trong khi vẫn duy trì chức năng. Hiểu cách sử dụng đúng IMDS là điều cần thiết cho quản lý và bảo mật EC2 instance.




FILE: 52-ec2-instance-metadata-service-hands-on.md


# Dịch Vụ EC2 Instance Metadata (IMDS) - Hướng Dẫn Thực Hành

## Giới Thiệu

Hướng dẫn này trình bày cách sử dụng Dịch vụ EC2 Instance Metadata để truy vấn thông tin instance và lấy thông tin xác thực IAM role từ bên trong một EC2 instance.

## Yêu Cầu Trước

- Tài khoản AWS
- Hiểu biết cơ bản về EC2 instances
- Quen thuộc với các thao tác dòng lệnh

## Tạo EC2 Instance

### Bước 1: Cấu Hình Khởi Chạy Instance

1. Tạo một EC2 instance mới với tên **DemoEC2**
2. Chọn **Amazon Linux 2023 AMI** (phiên bản mới nhất)
3. Di chuyển đến phần **Advanced Details**
4. Tìm cài đặt **Metadata version**

### Bước 2: Hiểu Về Các Phiên Bản Metadata

- **Amazon Linux 2023**: Mặc định là **IMDSv2 only** (chỉ IMDSv2)
- **Amazon Linux 2**: Cho phép chọn giữa **V1 and V2** hoặc **V2 only**

Trong hướng dẫn này, chúng ta sẽ sử dụng Amazon Linux 2023 với IMDSv2.

### Bước 3: Cấu Hình Bảo Mật

1. Tiếp tục **không cần key pair** (tùy chọn)
2. Tạo security group mới:
   - Cho phép **SSH from anywhere** (SSH từ mọi nơi)
3. Để trống **IAM instance profile** ban đầu (chúng ta sẽ thêm sau)

### Bước 4: Khởi Chạy Instance

Khởi chạy instance và kết nối bằng **EC2 Instance Connect**.

## Làm Việc Với Instance Metadata Service

### Hiểu Về IMDSv1 vs IMDSv2

#### Kiểm Tra IMDSv1 (Sẽ Thất Bại Trên Amazon Linux 2023)

```bash
curl http://169.254.169.254/latest/meta-data/
```

**Kết quả**: `401 Unauthorized` (Không được phép)

IMDSv1 bị vô hiệu hóa trên Amazon Linux 2023 vì lý do bảo mật.

### Sử Dụng IMDSv2 (Được Khuyến Nghị)

#### Bước 1: Lấy Session Token

```bash
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
```

Lệnh này:
- Truy vấn endpoint `/latest/api/token`
- Thiết lập thời gian hết hạn token (TTL) trong header
- Lưu token vào biến `TOKEN`

Xác minh token:
```bash
echo $TOKEN
```

#### Bước 2: Truy Vấn Metadata Với Token

```bash
curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/
```

**Kết quả**: Bạn sẽ thấy danh sách các metadata endpoint có sẵn.

## Khám Phá Các Metadata Endpoint

### Hiểu Về Kết Quả Trả Về

- **Có dấu gạch chéo (/)**: Cho biết một thư mục có nhiều dữ liệu bên trong
- **Không có dấu gạch chéo**: Cho biết một giá trị trực tiếp

### Lấy Metadata Cụ Thể

#### Lấy Hostname

```bash
curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/hostname
```

#### Lấy Địa Chỉ IPv4 Nội Bộ

```bash
curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/local-ipv4
```

## Lấy Thông Tin Xác Thực IAM Role

### Thử Nghiệm Ban Đầu (Không Có IAM Role)

Di chuyển đến identity credentials:

```bash
curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/iam/security-credentials/
```

**Kết quả**: `Not found` - Chưa có IAM role nào được gắn kết.

### Gắn Kết IAM Role

1. Trong AWS Console, chọn EC2 instance của bạn
2. Vào **Actions** → **Security** → **Modify IAM role**
3. Chọn bất kỳ IAM role nào (role cụ thể không quan trọng cho demo này)
4. Đợi khoảng 30 giây để thay đổi có hiệu lực

### Lấy Thông Tin Xác Thực

#### Liệt Kê Các Role Có Sẵn

```bash
curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/iam/security-credentials/
```

**Kết quả**: Trả về tên role (ví dụ: `EC2Instance`)

#### Lấy Thông Tin Xác Thực Của Role

```bash
curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/iam/security-credentials/EC2Instance
```

**Kết quả**: Phản hồi JSON chứa:
- `AccessKeyId`: Access key tạm thời
- `SecretAccessKey`: Secret key tạm thời
- `Token`: Session token
- `Expiration`: Thời điểm hết hạn thông tin xác thực (thường là 1 giờ)

### Ví Dụ Phản Hồi

```json
{
  "Code": "Success",
  "LastUpdated": "2024-XX-XXTXX:XX:XXZ",
  "Type": "AWS-HMAC",
  "AccessKeyId": "ASIA...",
  "SecretAccessKey": "...",
  "Token": "...",
  "Expiration": "2024-XX-XXTXX:XX:XXZ"
}
```

## Cách IAM Role Hoạt Động Với EC2

Điều này minh họa cơ chế hoạt động bên dưới:

1. EC2 instance được gán một IAM role
2. AWS tự động cung cấp thông tin xác thực tạm thời qua IMDS
3. AWS CLI và SDK tự động lấy các thông tin xác thực này
4. Thông tin xác thực được xoay vòng trước khi hết hạn

**Quan trọng**: Bạn không cần phải lấy thông tin xác thực này thủ công trong ứng dụng của mình - AWS SDK tự động xử lý việc này.

## Những Điểm Chính

- **IMDSv2** an toàn hơn và bắt buộc trên Amazon Linux 2023
- **Xác thực dựa trên token** ngăn chặn các cuộc tấn công SSRF
- **Thông tin xác thực IAM role** được cung cấp thông qua dịch vụ metadata
- **Xoay vòng thông tin xác thực tự động** đảm bảo bảo mật
- Dịch vụ metadata cho phép EC2 instance tự khám phá cấu hình của chúng

## Dọn Dẹp

Khi hoàn thành hướng dẫn:

1. Di chuyển đến EC2 Console
2. Chọn instance **DemoEC2**
3. **Terminate** (Chấm dứt) instance

## Kết Luận

EC2 Instance Metadata Service là một tính năng mạnh mẽ cho phép các instance truy cập dữ liệu cấu hình và thông tin xác thực IAM một cách an toàn. Mặc dù AWS SDK xử lý hầu hết các thao tác tự động, việc hiểu cơ chế bên dưới rất có giá trị cho việc khắc phục sự cố và các trường hợp sử dụng nâng cao.

---

**Các Bước Tiếp Theo**: Khám phá các dịch vụ AWS khác tích hợp với EC2 metadata service, chẳng hạn như AWS Systems Manager và CloudWatch.




FILE: 53-aws-cli-multiple-accounts-and-profiles.md


# AWS CLI: Quản Lý Nhiều Tài Khoản với Profiles

## Tổng Quan

Khi làm việc với nhiều tài khoản AWS, bạn cần một cách để quản lý các bộ thông tin xác thực và cấu hình khác nhau. AWS CLI cung cấp giải pháp thông qua **profiles**, cho phép bạn tổ chức và chuyển đổi giữa nhiều tài khoản AWS một cách liền mạch.

## Hiểu Về Cấu Hình Mặc Định

Theo mặc định, AWS CLI lưu trữ thông tin xác thực và cấu hình của bạn trong hai tệp:

- **`~/.aws/credentials`**: Chứa AWS access key ID và secret access key
- **`~/.aws/config`**: Chứa cài đặt region và định dạng output

Cả hai tệp đều chứa phần `[default]` được sử dụng khi không chỉ định profile cụ thể.

## Tạo Profiles Bổ Sung

### Sử Dụng Lệnh Configure

Để tạo một profile mới, sử dụng lệnh `aws configure` với cờ `--profile`:

```bash
aws configure --profile my-other-aws-account
```

Bạn sẽ được yêu cầu nhập:
- AWS Access Key ID
- AWS Secret Access Key
- Tên region mặc định (ví dụ: `us-west-2`)
- Định dạng output mặc định (tùy chọn)

### Những Thay Đổi Trong Tệp Cấu Hình

Sau khi tạo profile mới, các tệp của bạn sẽ được cập nhật:

**Tệp credentials:**
```ini
[default]
aws_access_key_id = YOUR_DEFAULT_KEY
aws_secret_access_key = YOUR_DEFAULT_SECRET

[my-other-aws-account]
aws_access_key_id = YOUR_OTHER_KEY
aws_secret_access_key = YOUR_OTHER_SECRET
```

**Tệp config:**
```ini
[default]
region = us-east-1

[profile my-other-aws-account]
region = us-west-2
```

## Sử Dụng Profiles Trong Lệnh

### Profile Mặc Định

Khi bạn chạy lệnh AWS CLI mà không chỉ định profile, profile mặc định sẽ được sử dụng:

```bash
aws s3 ls
```

### Profile Cụ Thể

Để sử dụng một profile cụ thể, thêm cờ `--profile` vào lệnh của bạn:

```bash
aws s3 ls --profile my-other-aws-account
```

Điều này áp dụng cho **mọi lệnh AWS CLI**. Cờ `--profile` có thể được sử dụng với tất cả các dịch vụ và thao tác AWS.

## Thực Hành Tốt Nhất

1. **Sử dụng tên profile mô tả rõ ràng**: Chọn tên xác định rõ tài khoản hoặc môi trường (ví dụ: `production`, `development`, `ten-khach-hang`)

2. **Giữ thông tin xác thực an toàn**: Không bao giờ commit các tệp `~/.aws/credentials` hoặc `~/.aws/config` vào version control

3. **Xác minh profile đang hoạt động**: Luôn kiểm tra kỹ profile bạn đang sử dụng, đặc biệt khi làm việc với các tài khoản production

4. **Tổ chức theo môi trường**: Cân nhắc sử dụng profiles cho các môi trường khác nhau (dev, staging, production)

## Điểm Chính Cần Nhớ

- Profiles cho phép bạn quản lý nhiều tài khoản AWS từ một cài đặt CLI duy nhất
- Sử dụng `aws configure --profile <tên>` để tạo profiles mới
- Sử dụng cờ `--profile <tên>` với bất kỳ lệnh AWS CLI nào để chỉ định tài khoản muốn sử dụng
- Đây là kiến thức thiết yếu cho các developers làm việc với nhiều tài khoản AWS, mặc dù thường không bắt buộc cho các kỳ thi chứng chỉ

## Ứng Dụng Thực Tế

Với vai trò là một developer, bạn sẽ thường xuyên cần:
- Chuyển đổi giữa các tài khoản development và production
- Quản lý tài nguyên trên nhiều tài khoản khách hàng khác nhau
- Làm việc với các AWS regions khác nhau cho cùng một tài khoản

Profiles giúp tất cả các tình huống này trở nên dễ quản lý và giúp ngăn chặn các sai lầm tốn kém do chạy lệnh nhầm tài khoản.




FILE: 54-aws-mfa-cli-sdk-tutorial.md


# Xác Thực Đa Yếu Tố AWS với CLI và SDK

## Tổng Quan

Hướng dẫn này trình bày cách sử dụng Xác thực Đa yếu tố (MFA) với AWS CLI và SDK bằng cách tạo phiên tạm thời sử dụng AWS Security Token Service (STS).

## Khái Niệm Chính

### API STS GetSessionToken

Để sử dụng MFA với CLI hoặc SDK, bạn phải tạo một phiên tạm thời bằng API **STS GetSessionToken**. Đây là lệnh gọi API quan trọng cần nhớ cho mục đích thi cử.

### Các Tham Số Bắt Buộc

Khi gọi `GetSessionToken`, bạn cần cung cấp:
- **Số serial** của thiết bị MFA
- **Mã token** từ thiết bị MFA
- **Thời lượng** hiệu lực của credentials

### Kết Quả Trả Về

API trả về các credentials tạm thời bao gồm:
- Access Key ID
- Secret Access Key
- Session Token
- Thời gian hết hạn

## Hướng Dẫn Từng Bước

### Bước 1: Gán Thiết Bị MFA

1. Truy cập **IAM** trong AWS Console
2. Vào tài khoản người dùng của bạn (ví dụ: "Stephane")
3. Nhấp vào **Security credentials**
4. Nhấp **Assign MFA device**
5. Chọn **Virtual MFA device**
6. Quét mã QR bằng ứng dụng xác thực (ví dụ: Authy, Google Authenticator)
7. Nhập hai mã MFA liên tiếp từ ứng dụng của bạn
8. Nhấp **Assign MFA**
9. **Quan trọng**: Sao chép ARN của thiết bị MFA - bạn sẽ cần nó cho lệnh CLI

### Bước 2: Lấy Session Token Tạm Thời qua CLI

Chạy lệnh sau:

```bash
aws sts get-session-token --serial-number <MFA_DEVICE_ARN> --token-code <MFA_CODE>
```

**Ví dụ kết quả trả về:**
```json
{
  "Credentials": {
    "AccessKeyId": "ASIA...",
    "SecretAccessKey": "...",
    "SessionToken": "...",
    "Expiration": "2024-01-01T12:00:00Z"
  }
}
```

### Bước 3: Cấu Hình AWS Profile với Credentials Tạm Thời

1. Tạo một profile mới cho credentials MFA:
```bash
aws configure --profile mfa
```

2. Nhập **Access Key ID** tạm thời khi được yêu cầu
3. Nhập **Secret Access Key** tạm thời khi được yêu cầu
4. Đặt region mặc định (hoặc nhấn Enter để giữ nguyên)
5. Đặt định dạng output (hoặc nhấn Enter để giữ nguyên)

### Bước 4: Thêm Session Token vào File Credentials

1. Mở file AWS credentials:
   - **Linux/Mac**: `~/.aws/credentials`
   - **Windows**: `%USERPROFILE%\.aws\credentials`

2. Thêm session token vào profile MFA của bạn:
```ini
[mfa]
aws_access_key_id = ASIA...
aws_secret_access_key = ...
aws_session_token = <DÁN_SESSION_TOKEN_DÀI_VÀO_ĐÂY>
```

3. Lưu file

### Bước 5: Sử Dụng Profile MFA

Bây giờ bạn có thể thực hiện các lệnh gọi API sử dụng profile MFA:

```bash
aws s3 ls --profile mfa
```

Lệnh này sẽ sử dụng credentials tạm thời đã được xác thực MFA để liệt kê các S3 buckets.

## Lưu Ý Quan Trọng

- **Credentials tạm thời**: Các credentials này có thời hạn và sẽ hết hạn (thường là sau 1 giờ theo mặc định)
- **Session token**: Session token có thể rất dài - hãy chắc chắn sao chép đầy đủ
- **Bảo mật**: Vì đây là credentials tạm thời nên chúng an toàn hơn credentials dài hạn
- **Mẹo thi**: Nhớ rằng **STS GetSessionToken** là API được sử dụng để tạo session token tạm thời với MFA

## Tóm Tắt

Để sử dụng MFA với AWS CLI/SDK:
1. Gán thiết bị MFA cho IAM user của bạn
2. Gọi `aws sts get-session-token` với số serial thiết bị MFA và mã token
3. Cấu hình AWS profile mới với credentials tạm thời
4. Thêm session token vào file credentials
5. Sử dụng flag `--profile` để thực hiện các lệnh gọi API đã xác thực

Điểm chính cần nhớ là **STS GetSessionToken** tạo ra credentials tạm thời (Access Key, Secret Key và Session Token) có thể được sử dụng cho các lệnh gọi API đã xác thực MFA.




FILE: 55-aws-sdk-overview.md


# Tổng Quan Về AWS SDK

## Giới Thiệu

AWS Software Development Kit (SDK) là một công cụ mạnh mẽ cho phép các nhà phát triển tương tác với các dịch vụ AWS trực tiếp từ mã ứng dụng của họ, mà không cần dựa vào AWS Command Line Interface (CLI).

## AWS SDK Là Gì?

SDK (Software Development Kit - Bộ công cụ phát triển phần mềm) cho phép bạn thực hiện các hành động trên AWS trực tiếp từ mã ứng dụng của bạn. Thay vì sử dụng các lệnh CLI, bạn có thể tương tác với các dịch vụ AWS theo cách lập trình thông qua ngôn ngữ lập trình ưa thích của mình.

## Các Ngôn Ngữ Được Hỗ Trợ

AWS cung cấp các SDK chính thức cho nhiều ngôn ngữ lập trình, bao gồm:

- **Java**
- **.NET**
- **Node.js**
- **PHP**
- **Python** (Boto3)
- **Go**
- **Ruby**
- **C++**

Danh sách các ngôn ngữ được hỗ trợ tiếp tục phát triển theo thời gian khi AWS mở rộng các SDK của mình.

## Mối Liên Hệ Giữa Python SDK và CLI

Một điều thú vị về AWS CLI là nó được xây dựng bằng Python và tận dụng SDK **Boto3**. Khi bạn sử dụng AWS CLI, thực tế bạn đang sử dụng Python SDK ở bên dưới.

## Khi Nào Sử Dụng SDK

SDK được sử dụng khi bạn cần:

- Thực hiện các lệnh gọi API đến các dịch vụ AWS từ mã ứng dụng của bạn
- Tương tác với các dịch vụ như Amazon DynamoDB hoặc Amazon S3 theo cách lập trình
- Xây dựng các ứng dụng cần tự động hóa các hoạt động AWS
- Tích hợp chức năng AWS trực tiếp vào phần mềm của bạn

## Ứng Dụng Thực Tế

Bạn sẽ gặp SDK trong thực tế khi làm việc với AWS Lambda functions, nơi bạn có thể thấy cách SDK hoạt động trong các triển khai mã thực tế. Trải nghiệm thực hành này sẽ minh họa cách sử dụng AWS SDK trong thế giới thực.

## Những Điểm Cần Nhớ

- SDK cho phép tương tác trực tiếp với AWS từ mã ứng dụng
- Có nhiều tùy chọn ngôn ngữ để phù hợp với các môi trường phát triển khác nhau
- AWS CLI được xây dựng trên Python SDK (Boto3)
- Hiểu khi nào sử dụng SDK là quan trọng cho các kỳ thi chứng chỉ AWS
- Kinh nghiệm thực tế với Lambda functions sẽ cung cấp cách sử dụng SDK thực hành

---

*Tổng quan này cung cấp sự hiểu biết cơ bản về AWS SDK và vai trò của chúng trong phát triển ứng dụng đám mây.*




FILE: 56-aws-limits-and-exponential-backoff.md


# Giới hạn AWS và Chiến lược Exponential Backoff

## Tổng quan

AWS có hai loại giới hạn (còn gọi là Quotas - Hạn ngạch) mà các nhà phát triển cần hiểu và quản lý khi làm việc với các dịch vụ AWS.

## Các loại Giới hạn AWS

### 1. Giới hạn Tốc độ API (API Rate Limits)

Giới hạn Tốc độ API xác định số lần bạn có thể gọi một AWS API trong một khoảng thời gian nhất định.

**Ví dụ:**
- **EC2 DescribeInstances API**: 100 lần gọi mỗi giây
- **S3 GetObject API**: 5,500 yêu cầu GET mỗi giây cho mỗi prefix

#### Điều gì xảy ra khi vượt quá Giới hạn Tốc độ?

Khi bạn vượt quá các giới hạn này, bạn sẽ gặp phải:
- **Lỗi Gián đoạn (Intermittent Errors)**: Các yêu cầu của bạn sẽ bị điều tiết (throttled)
- **ThrottlingException**: Mã lỗi cho biết đã vượt quá giới hạn tốc độ

#### Giải pháp cho các vấn đề về Giới hạn Tốc độ

**Đối với Lỗi Gián đoạn:**
- Triển khai **Chiến lược Exponential Backoff** (chi tiết bên dưới)

**Đối với Lỗi Liên tục:**
- Yêu cầu **tăng giới hạn điều tiết API** từ AWS
- Ví dụ: Nếu bạn liên tục cần hơn 100 lần gọi mỗi giây cho DescribeInstances, bạn có thể yêu cầu tăng (ví dụ: lên 300 lần gọi mỗi giây)

### 2. Hạn ngạch Dịch vụ (Service Quotas/Service Limits)

Hạn ngạch Dịch vụ xác định bạn có thể chạy bao nhiêu tài nguyên của một loại cụ thể.

**Ví dụ:**
- **On-Demand Standard Instances**: Tối đa 1,152 vCPU ảo mỗi tài khoản

#### Cách tăng Hạn ngạch Dịch vụ

1. **Phương pháp Thủ công**: Mở ticket hỗ trợ với AWS
2. **Phương pháp Lập trình**: Sử dụng Service Quotas API để yêu cầu tăng tự động

## Chiến lược Exponential Backoff

### Khi nào sử dụng Exponential Backoff

Triển khai Exponential Backoff khi bạn nhận được **ThrottlingException** do quá nhiều lần gọi API.

> **Mẹo Thi**: Các câu hỏi về ThrottlingException thường mong đợi Exponential Backoff là câu trả lời.

### Triển khai SDK

- **AWS SDK**: Cơ chế thử lại với Exponential Backoff **đã được bao gồm** theo mặc định
- **Gọi API Tùy chỉnh**: Nếu bạn tự triển khai các HTTP calls, bạn phải tự triển khai Exponential Backoff

### Nên thử lại Lỗi nào?

Khi triển khai logic thử lại tùy chỉnh:

✅ **NÊN Thử lại:**
- **Lỗi Server 5XX** (500, 503, v.v.)
- **Lỗi Throttling**

❌ **KHÔNG NÊN Thử lại:**
- **Lỗi Client 4XX** (400, 401, 403, v.v.)
- Những lỗi này cho thấy vấn đề với yêu cầu của bạn, và việc thử lại sẽ không thay đổi kết quả

### Cách hoạt động của Exponential Backoff

Chiến lược này bao gồm việc tăng gấp đôi thời gian chờ giữa mỗi lần thử lại:

```
Lần thử 1: Chờ 1 giây
Lần thử 2: Chờ 2 giây (gấp đôi)
Lần thử 3: Chờ 4 giây (gấp đôi)
Lần thử 4: Chờ 8 giây (gấp đôi)
Lần thử 5: Chờ 16 giây (gấp đôi)
```

### Lợi ích của Exponential Backoff

1. **Giảm Tải cho Server**: Càng thử lại nhiều, thời gian chờ càng dài
2. **Phân tán Tải**: Khi nhiều client triển khai chiến lược này đồng thời, tải tổng thể trên server giảm xuống
3. **Tăng Tỷ lệ Thành công**: Cho phép server phục hồi và phục vụ càng nhiều yêu cầu càng tốt

## Những điểm chính cần nhớ

- AWS có hai loại giới hạn: **Giới hạn Tốc độ API** và **Hạn ngạch Dịch vụ**
- Sử dụng **Exponential Backoff** cho lỗi ThrottlingException
- AWS SDK đã bao gồm Exponential Backoff theo mặc định
- Chỉ thử lại **lỗi 5XX**, không thử lại **lỗi 4XX**
- Yêu cầu tăng giới hạn khi bạn liên tục vượt quá hạn ngạch
- Exponential Backoff giúp phân phối tải theo thời gian, giảm áp lực lên server

## Tóm tắt

Hiểu rõ các giới hạn của AWS và triển khai các chiến lược thử lại phù hợp như Exponential Backoff là rất quan trọng để xây dựng các ứng dụng đáng tin cậy và có khả năng mở rộng trên AWS. Các cơ chế này giúp đảm bảo ứng dụng của bạn có thể xử lý throttling một cách ổn định trong khi vẫn duy trì hiệu suất tối ưu.




FILE: 57-aws-credentials-provider-chain.md


# Chuỗi Cung Cấp Thông Tin Xác Thực AWS

## Tổng Quan

Chuỗi Cung Cấp Thông Tin Xác Thực AWS (AWS Credentials Provider Chain) là một khái niệm quan trọng xác định thứ tự mà AWS CLI và SDK tìm kiếm thông tin xác thực. Hiểu rõ chuỗi này rất quan trọng cho việc cấu hình bảo mật AWS đúng cách và khắc phục sự cố.

## Thứ Tự Chuỗi Thông Tin Xác Thực CLI

Khi bạn sử dụng AWS CLI, nó sẽ tìm kiếm thông tin xác thực theo thứ tự ưu tiên sau:

1. **Tùy Chọn Dòng Lệnh** (Ưu tiên cao nhất)
   - Region (vùng)
   - Output format (định dạng đầu ra)
   - Profile (hồ sơ)
   - Access Key ID
   - Secret Access Key
   - Session Token

2. **Biến Môi Trường**
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_SESSION_TOKEN`

3. **File Thông Tin Xác Thực CLI**
   - Được cấu hình qua `aws configure`
   - Nằm tại `~/.aws/credentials`

4. **File Cấu Hình CLI**
   - Nằm tại `~/.aws/config`

5. **Thông Tin Xác Thực Container**
   - Được sử dụng cho ECS tasks

6. **Thông Tin Xác Thực EC2 Instance Profile** (Ưu tiên thấp nhất)
   - IAM role được gán cho EC2 instances

## Thứ Tự Chuỗi Thông Tin Xác Thực SDK

Đối với AWS SDK (ví dụ: Java SDK), thứ tự ưu tiên tương tự:

1. **System Properties** (ví dụ: Java system properties)
2. **Biến Môi Trường**
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
3. **File Profile Thông Tin Xác Thực Mặc Định**
4. **Thông Tin Xác Thực Amazon ECS Container**
5. **Thông Tin Xác Thực EC2 Instance Profile**

## Kịch Bản Phổ Biến: Vấn Đề Ưu Tiên Chuỗi Thông Tin Xác Thực

### Vấn Đề

Xem xét kịch bản này:

1. Bạn triển khai một ứng dụng trên EC2 instance
2. Ứng dụng sử dụng **biến môi trường** với thông tin xác thực IAM user để gọi Amazon S3 API
3. Thông tin xác thực IAM user này có quyền **S3 FullAccess** (truy cập tất cả S3 buckets)
4. Tuân theo best practices, bạn tạo một IAM role với **quyền tối thiểu** (chỉ truy cập một S3 bucket cụ thể)
5. Bạn gán IAM role này cho EC2 instance thông qua instance profile
6. **Vấn đề**: Ứng dụng vẫn có quyền truy cập tất cả S3 buckets!

### Tại Sao Điều Này Xảy Ra?

Chuỗi thông tin xác thực ưu tiên **biến môi trường cao hơn** so với thông tin xác thực EC2 instance profile. Mặc dù bạn đã gán instance profile với quyền hạn chế, nhưng biến môi trường vẫn đang được sử dụng.

### Giải Pháp

**Xóa bỏ (unset) các biến môi trường** trên EC2 instance. Sau khi xóa, chuỗi thông tin xác thực sẽ chuyển sang sử dụng thông tin xác thực EC2 instance profile, có quyền hạn chế đúng cách.

## Best Practices Về Thông Tin Xác Thực

### ❌ Không Bao Giờ Làm Điều Này

- **KHÔNG BAO GIỜ lưu thông tin xác thực trong code**
- Đây là thực hành cực kỳ tệ và là rủi ro bảo mật lớn

### ✅ Best Practices

1. **Kế thừa thông tin xác thực từ chuỗi thông tin xác thực**
2. **Trong AWS**: Sử dụng IAM roles càng nhiều càng tốt
   - EC2 Instance Roles cho EC2 instances
   - ECS Task Roles cho ECS tasks
   - Lambda Execution Roles cho Lambda functions
3. **Bên ngoài AWS**: Sử dụng biến môi trường hoặc named profiles
   - Cấu hình qua AWS CLI: `aws configure`
   - Sử dụng named profiles cho nhiều tài khoản

## Điểm Chính Cần Nhớ

- Chuỗi cung cấp thông tin xác thực tuân theo thứ tự ưu tiên cụ thể
- Biến môi trường có ưu tiên cao hơn instance profiles
- Luôn sử dụng IAM roles khi làm việc trong AWS
- Không bao giờ hardcode thông tin xác thực trong code ứng dụng
- Hiểu rõ chuỗi thông tin xác thực là cần thiết để khắc phục sự cố xác thực

## Mẹo Thi Cử

- Nắm vững thứ tự ưu tiên của chuỗi thông tin xác thực
- Hiểu các câu hỏi kịch bản phổ biến về xung đột thông tin xác thực
- Nhớ rằng biến môi trường ghi đè thông tin xác thực instance profile
- Biết các best practices về quản lý thông tin xác thực trong AWS




FILE: 58-aws-api-request-signing-sigv4.md


# Ký Yêu Cầu API AWS với SigV4

## Tổng Quan

Khi thực hiện các yêu cầu API tới các dịch vụ AWS, bạn cần ký yêu cầu của mình để AWS có thể xác định danh tính và cấp quyền cho bạn. Tài liệu này giải thích cách thức hoạt động của việc ký yêu cầu API AWS và các phương thức khác nhau có sẵn.

## Tại Sao Cần Ký Yêu Cầu API?

Khi bạn gọi AWS HTTP API (API cho tất cả các dịch vụ AWS), bạn phải ký yêu cầu để:
- AWS có thể xác định bạn là ai
- AWS có thể xác minh rằng bạn được ủy quyền thực hiện yêu cầu

### Quy Trình Ký

Để ký một yêu cầu, bạn sử dụng **thông tin xác thực AWS** của mình:
- Access Key (Khóa Truy Cập)
- Secret Key (Khóa Bí Mật)

Bằng cách ký yêu cầu với các thông tin xác thực này, AWS biết danh tính của bạn và có thể xử lý yêu cầu.

## Khi Nào Cần Ký

**Hầu hết các lệnh gọi API đều yêu cầu ký**, với một số ngoại lệ:
- Đọc các đối tượng công khai từ Amazon S3 không yêu cầu ký
- Tất cả các yêu cầu API khác đều phải được ký

## Ký Tự Động

Khi sử dụng các công cụ AWS, việc ký yêu cầu diễn ra tự động:
- **AWS CLI**: Tất cả các yêu cầu được ký mặc định
- **AWS SDK**: Tất cả các yêu cầu được ký tự động

Bạn không cần phải tự triển khai quy trình ký khi sử dụng các công cụ này.

## Signature Version 4 (SigV4)

AWS sử dụng **Signature Version 4 (SigV4)** để ký các yêu cầu API.

### Độ Phức Tạp
- Quy trình SigV4 bao gồm bốn bước
- Chi tiết triển khai khá phức tạp
- Thông thường bạn không cần phải tự triển khai SigV4

### Điều Bạn Cần Biết

Hai cách để truyền chữ ký của bạn đến AWS:

#### 1. Authorization Header

Chữ ký được gửi trong **Authorization header** của yêu cầu HTTP.
- Đây là phương thức mặc định được sử dụng bởi AWS CLI
- Chữ ký được tính toán và đưa vào header của yêu cầu

#### 2. Query String

Chữ ký được đưa trực tiếp vào **URL** dưới dạng tham số query.
- Chữ ký được truyền qua tham số query string
- Sử dụng khóa: `X-Amz-Signature`

## Ví Dụ Thực Tế: URL Amazon S3

Khi truy cập một tệp trong Amazon S3 thông qua trình duyệt, URL bao gồm các tham số SigV4:

### Các Thành Phần URL

Một URL S3 đã ký chứa nhiều tham số:
- **Security Token**: Token xác thực
- **Algorithm**: Chỉ định `AWS4-HMAC-SHA256` (SigV4)
- **Date**: Dấu thời gian của yêu cầu
- **Expires**: Khi URL sẽ hết hạn
- **X-Amz-Credential**: Chứa ID tài khoản và phạm vi thông tin xác thực
- **X-Amz-Signature**: Chữ ký đã được tính toán

### Cấu Trúc Ví Dụ

```
https://bucket-name.s3.region.amazonaws.com/coffee.jpg?
  X-Amz-Security-Token=...
  &X-Amz-Algorithm=AWS4-HMAC-SHA256
  &X-Amz-Date=...
  &X-Amz-Expires=...
  &X-Amz-Credential=...
  &X-Amz-Signature=...
```

URL này được xây dựng bởi trình duyệt web để truy cập các tệp trong Amazon S3 bằng phương thức chữ ký query string.

## Những Điểm Chính Cần Nhớ

1. **SigV4** được sử dụng để ký các yêu cầu tới AWS
2. Chữ ký có thể được truyền qua:
   - HTTP Authorization header
   - Query string với tham số `X-Amz-Signature`
3. AWS CLI và SDK xử lý việc ký tự động
4. Hầu hết các yêu cầu API đều yêu cầu ký (ngoại trừ một số trường hợp đọc đối tượng công khai S3)

## Tài Liệu Tham Khảo

- [Tài Liệu AWS Signature Version 4](https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html)
- [Thông Tin Xác Thực Bảo Mật AWS](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html)




FILE: 59-aws-s3-storage-classes-lifecycle-management.md


# Quản Lý Lifecycle và Storage Classes trên AWS S3

## Tổng Quan

Hướng dẫn này trình bày cách di chuyển objects giữa các storage classes khác nhau trên Amazon S3 bằng cách sử dụng transitions và lifecycle rules để tối ưu hóa chi phí và quản lý dữ liệu.

## Chuyển Đổi Storage Classes

### Các Đường Chuyển Đổi Khả Dụng

Bạn có thể chuyển đổi objects giữa các storage classes theo các đường sau:

- **Standard** → **Standard-IA** → **Intelligent-Tiering** → **One-Zone IA**
- **One-Zone IA** → **Glacier Flexible Retrieval** hoặc **Glacier Deep Archive**

### Thực Hành Tốt Nhất

- Nếu objects sẽ được **truy cập không thường xuyên**, hãy chuyển chúng sang **Standard-IA**
- Để **lưu trữ dài hạn**, hãy chuyển objects sang **Glacier tiers** hoặc **Deep Archive**

## Lifecycle Rules

### Lifecycle Rules là gì?

Lifecycle rules tự động hóa quá trình chuyển đổi hoặc xóa objects, loại bỏ nhu cầu quản lý thủ công.

### Các Loại Actions

#### 1. Transition Actions

Cấu hình objects tự động chuyển sang storage class khác:

- Chuyển sang **Standard-IA** sau 60 ngày tạo
- Chuyển sang **Glacier** để lưu trữ sau 6 tháng

#### 2. Expiration Actions

Cấu hình objects tự động bị xóa sau một khoảng thời gian:

- Xóa access log files sau 365 ngày
- Xóa các phiên bản cũ của files (khi bật versioning)
- Dọn dẹp incomplete multi-part uploads sau 2 tuần

### Cấu Hình Rules

Lifecycle rules có thể được cấu hình dựa trên:

- **Prefix**: Áp dụng cho toàn bộ bucket hoặc các đường dẫn cụ thể
- **Object Tags**: Nhắm mục tiêu các objects được tag cụ thể (ví dụ: department: finance)

## Kịch Bản Thực Tế

### Kịch Bản 1: Quản Lý Ảnh Thumbnail

**Yêu Cầu:**
- Ứng dụng EC2 tạo thumbnails từ ảnh profile được upload
- Thumbnails có thể dễ dàng tạo lại và chỉ cần giữ trong 60 ngày
- Ảnh gốc phải có thể truy xuất ngay lập tức trong 60 ngày
- Sau 60 ngày, người dùng có thể chờ tới 6 giờ để lấy ảnh gốc

**Giải Pháp:**
- **Ảnh gốc**: Sử dụng class **Standard** với lifecycle rule chuyển sang **Glacier** sau 60 ngày
- **Ảnh thumbnail**: Sử dụng **One-Zone IA** (truy cập không thường xuyên, dễ tạo lại) với expiration rule xóa sau 60 ngày
- Sử dụng **prefixes** để phân biệt giữa ảnh gốc và thumbnail

### Kịch Bản 2: Khôi Phục Objects Đã Xóa

**Yêu Cầu:**
- Khôi phục objects đã xóa ngay lập tức trong 30 ngày (hiếm khi xảy ra)
- Khôi phục objects đã xóa trong vòng 48 giờ cho tới 365 ngày

**Giải Pháp:**
- Bật **S3 Versioning** để bảo toàn các phiên bản của object
- Objects đã xóa được ẩn bởi delete marker và có thể khôi phục
- Tạo lifecycle rules để:
  - Chuyển **non-current versions** sang **Standard-IA**
  - Chuyển non-current versions sang **Glacier Deep Archive** để lưu trữ dài hạn

## Amazon S3 Analytics

### Mục Đích

S3 Analytics giúp xác định số ngày tối ưu để chuyển đổi objects giữa các storage classes.

### Tính Năng

- Cung cấp đề xuất cho các class **Standard** và **Standard-IA**
- Không hỗ trợ One-Zone IA hoặc Glacier
- Tạo **CSV report** với các đề xuất và thống kê
- Report được cập nhật **hàng ngày**
- Phân tích dữ liệu ban đầu mất **24-48 giờ** để xuất hiện

### Trường Hợp Sử Dụng

Sử dụng S3 Analytics làm bước đầu tiên để:
- Tạo các lifecycle rules hiệu quả
- Tối ưu hóa các rules hiện có dựa trên mô hình sử dụng thực tế

## Các Điểm Chính Cần Nhớ

- Tự động hóa chuyển đổi storage class bằng lifecycle rules
- Sử dụng storage classes phù hợp dựa trên mô hình truy cập
- Tận dụng versioning cho các kịch bản khôi phục dữ liệu
- Sử dụng S3 Analytics để ra quyết định lifecycle dựa trên dữ liệu
- Cân nhắc sử dụng object prefixes và tags cho việc áp dụng rules chi tiết

## Tóm Tắt

Lifecycle management trên S3 là công cụ mạnh mẽ giúp tối ưu hóa chi phí lưu trữ trong khi vẫn đáp ứng các yêu cầu về khả năng truy cập và tuân thủ. Bằng cách hiểu rõ các storage classes và cách cấu hình lifecycle rules, bạn có thể tự động hóa quản lý dữ liệu một cách hiệu quả.

---

*Tài liệu này dựa trên các thực hành tốt nhất của AWS S3 cho quản lý storage class và tối ưu hóa lifecycle.*




FILE: 6-rds-aurora-security.md


# Bảo Mật RDS và Aurora

## Tổng Quan

Hướng dẫn này bao gồm các tính năng bảo mật và các phương pháp tốt nhất cho cơ sở dữ liệu AWS RDS (Relational Database Service) và Amazon Aurora.

## Mã Hóa Dữ Liệu Lưu Trữ (Encryption at Rest)

Bạn có thể mã hóa dữ liệu lưu trữ trên cơ sở dữ liệu RDS và Aurora, có nghĩa là dữ liệu được mã hóa trên các ổ đĩa.

### Các Điểm Chính:

- **Master và Replicas**: Cả cơ sở dữ liệu master và bất kỳ read replica nào đều được mã hóa bằng AWS KMS (Key Management Service)
- **Cấu Hình Khi Khởi Tạo**: Mã hóa phải được xác định tại thời điểm khởi chạy trong lần khởi chạy đầu tiên của cơ sở dữ liệu
- **Hạn Chế Quan Trọng**: Nếu cơ sở dữ liệu master không được mã hóa, các read replica cũng không thể được mã hóa

### Mã Hóa Cơ Sở Dữ Liệu Chưa Được Mã Hóa

Để mã hóa một cơ sở dữ liệu chưa được mã hóa hiện có:

1. Tạo một snapshot từ cơ sở dữ liệu chưa được mã hóa
2. Khôi phục snapshot đó thành một cơ sở dữ liệu đã được mã hóa

Lưu ý: Bạn phải thực hiện qua quá trình snapshot và restore để kích hoạt mã hóa cho cơ sở dữ liệu hiện có.

## Mã Hóa Trong Quá Trình Truyền Tải (In-Flight Encryption)

Cơ sở dữ liệu RDS và Aurora hỗ trợ mã hóa trong quá trình truyền tải giữa client và cơ sở dữ liệu.

### Cấu Hình:

- Mỗi cơ sở dữ liệu trên RDS và Aurora đều sẵn sàng có mã hóa trong quá trình truyền tải **theo mặc định**
- Client phải sử dụng chứng chỉ gốc TLS từ AWS (được cung cấp trên trang web AWS)

## Xác Thực Cơ Sở Dữ Liệu

RDS và Aurora hỗ trợ nhiều phương thức xác thực:

### 1. Username và Password
Phương pháp xác thực cổ điển sử dụng thông tin đăng nhập username và password.

### 2. Xác Thực IAM Roles
- Bạn có thể sử dụng IAM roles để kết nối đến cơ sở dữ liệu
- Ví dụ: Các EC2 instance có IAM roles có thể xác thực trực tiếp đến cơ sở dữ liệu
- Lợi ích: Loại bỏ nhu cầu quản lý username và password
- Giúp quản lý tất cả bảo mật trong AWS và IAM

## Kiểm Soát Truy Cập Mạng

### Security Groups

Bạn có thể kiểm soát quyền truy cập mạng vào cơ sở dữ liệu bằng security groups:

- Cho phép hoặc chặn các cổng cụ thể
- Cho phép hoặc chặn các địa chỉ IP cụ thể
- Cho phép hoặc chặn các security group cụ thể

### Truy Cập SSH

- RDS và Aurora **không có quyền truy cập SSH** vì chúng là các dịch vụ được quản lý
- Ngoại lệ: Dịch vụ RDS Custom từ AWS có cung cấp quyền truy cập SSH

## Nhật Ký Kiểm Toán (Audit Logs)

### Mục Đích
Audit Logs giúp bạn theo dõi các truy vấn đang được thực hiện trên RDS và Aurora theo thời gian và giám sát các hoạt động cơ sở dữ liệu.

### Cấu Hình:

1. Kích hoạt Audit Logs trên cơ sở dữ liệu RDS hoặc Aurora
2. Lưu ý: Audit logs sẽ bị mất sau một khoảng thời gian

### Lưu Trữ Dài Hạn

Để giữ audit logs trong thời gian dài:

- Gửi chúng đến dịch vụ **CloudWatch Logs** trên AWS
- Điều này đảm bảo logs được lưu giữ và có thể phân tích theo thời gian

## Tóm Tắt

RDS và Aurora cung cấp các tùy chọn bảo mật toàn diện bao gồm:

- ✅ Mã hóa dữ liệu lưu trữ sử dụng KMS
- ✅ Mã hóa trong quá trình truyền tải sử dụng TLS
- ✅ Nhiều phương thức xác thực (username/password và IAM roles)
- ✅ Kiểm soát truy cập mạng qua security groups
- ✅ Ghi nhật ký kiểm toán với tích hợp CloudWatch Logs
- ❌ Không có quyền truy cập SSH (dịch vụ được quản lý)

Các tính năng bảo mật này giúp bạn bảo vệ cơ sở dữ liệu và duy trì tuân thủ các phương pháp tốt nhất về bảo mật.




FILE: 60-aws-s3-lifecycle-rules-tutorial.md


# Hướng Dẫn Quy Tắc Lifecycle AWS S3

## Giới Thiệu

Hướng dẫn này trình bày cách tạo và cấu hình các quy tắc lifecycle cho AWS S3 buckets để tự động quản lý việc chuyển đổi đối tượng giữa các lớp lưu trữ và xử lý hết hạn đối tượng.

## Tạo Quy Tắc Lifecycle

Hãy bắt đầu và tạo một quy tắc lifecycle cho buckets của chúng ta.

1. Điều hướng đến tab **Management** trong S3 bucket của bạn
2. Nhấp **Create a lifecycle rule**
3. Đặt tên cho quy tắc (ví dụ: "demo rule")
4. Áp dụng nó cho tất cả các đối tượng trong bucket và xác nhận

## Năm Hành Động Quy Tắc

Chúng ta có thể thấy có năm hành động quy tắc khác nhau:

1. **Di chuyển các phiên bản hiện tại của đối tượng giữa các lớp lưu trữ**
2. **Di chuyển các phiên bản không hiện tại của đối tượng giữa các lớp**
3. **Hết hạn các phiên bản hiện tại của đối tượng**
4. **Xóa vĩnh viễn các phiên bản không hiện tại của đối tượng**
5. **Xóa các đối tượng đã hết hạn, delete markers, hoặc incomplete multi-part upload**

Hãy xem xét từng cái một.

## Di Chuyển Các Đối Tượng Phiên Bản Hiện Tại Giữa Các Lớp Lưu Trữ

Di chuyển các đối tượng phiên bản hiện tại giữa các lớp lưu trữ có nghĩa là bạn có một bucket có phiên bản, và phiên bản hiện tại là phiên bản mới nhất - phiên bản được hiển thị cho người dùng.

### Ví Dụ Timeline Chuyển Đổi

Bạn có thể cấu hình các chuyển đổi như sau:

- **Sau 30 ngày** → Chuyển sang Standard-IA
- **Sau 60 ngày** → Chuyển sang Intelligent-Tiering
- **Sau 90 ngày** → Chuyển sang Glacier Instant Retrieval
- **Sau 180 ngày** → Chuyển sang Glacier Flexible Retrieval
- **Sau 365 ngày** → Chuyển sang Glacier Deep Archive

Bạn có thể có bao nhiêu chuyển đổi tùy thích.

## Di Chuyển Các Phiên Bản Không Hiện Tại

Chúng ta cũng có thể di chuyển các phiên bản không hiện tại nhanh hơn. Điều này áp dụng cho các đối tượng không phải là hiện tại - các đối tượng đã bị ghi đè bởi một phiên bản mới hơn.

Ví dụ, chúng ta có thể di chuyển các phiên bản không hiện tại vào Glacier Flexible Retrieval sau 90 ngày vì chúng ta biết rằng sau 90 ngày chúng ta sẽ không cần nó để truy xuất. Điều này hoàn hảo và chúng ta có thể tiếp tục, nhưng chúng ta có thể thêm nhiều chuyển đổi hơn.

## Hết Hạn và Xóa Đối Tượng

### Phiên Bản Hiện Tại
Chúng ta muốn cho hết hạn các phiên bản hiện tại của đối tượng sau một khoảng thời gian xác định. Bạn có thể thiết lập nó sau 700 ngày ở phía dưới.

### Phiên Bản Không Hiện Tại
Tương tự đối với các phiên bản không hiện tại - chúng ta muốn xóa vĩnh viễn chúng sau 700 ngày.

## Xem Xét Các Chuyển Đổi

Điều này rất hay vì nó cho bạn thấy một timeline về những gì sẽ xảy ra với phiên bản hiện tại và các phiên bản không hiện tại của đối tượng của bạn.

Nếu chúng ta hài lòng với tất cả những điều này, chúng ta chỉ cần tiếp tục và tạo quy tắc này, và quy tắc này sẽ hoạt động trong nền để thực hiện những gì nó phải làm.

## Kết Luận

Vậy là xong! Bây giờ bạn đã biết cách tự động di chuyển các đối tượng trong AWS giữa các lớp lưu trữ khác nhau.

Tôi hy vọng bạn thích nó và tôi sẽ gặp bạn trong bài giảng tiếp theo.




FILE: 61-amazon-s3-event-notifications.md


# Amazon S3 Event Notifications (Thông báo Sự kiện S3)

## Tổng quan

Amazon S3 Event Notifications cho phép bạn tự động phản ứng với các sự kiện xảy ra trong S3 bucket của bạn. Tính năng này giúp bạn xây dựng kiến trúc hướng sự kiện và tự động hóa quy trình làm việc dựa trên các thao tác với đối tượng S3.

## S3 Events là gì?

S3 events là các hành động xảy ra trong Amazon S3 bucket của bạn, bao gồm:

- **Object Created (Tạo đối tượng)** - Khi một đối tượng mới được tải lên S3
- **Object Removed (Xóa đối tượng)** - Khi một đối tượng bị xóa khỏi S3
- **Object Restored (Khôi phục đối tượng)** - Khi một đối tượng được khôi phục từ lưu trữ lưu trữ
- **Replication Events (Sự kiện sao chép)** - Khi các hoạt động sao chép xảy ra

## Lọc Sự kiện

Bạn có thể lọc các sự kiện dựa trên thuộc tính của đối tượng. Ví dụ:
- Lọc theo phần mở rộng tệp (ví dụ: chỉ các tệp `.jpeg`)
- Lọc theo tiền tố hoặc hậu tố của object key
- Áp dụng các quy tắc lọc tùy chỉnh

## Trường hợp Sử dụng

Một trường hợp sử dụng phổ biến là tự động tạo ảnh thu nhỏ (thumbnail) cho các hình ảnh được tải lên S3:
1. Người dùng tải hình ảnh lên S3
2. Event Notification được kích hoạt
3. Quy trình tự động tạo ảnh thu nhỏ
4. Ảnh thu nhỏ được lưu trữ lại trong S3

## Đích của Event Notification

S3 Event Notifications có thể được gửi đến ba đích chính:

### 1. SNS (Simple Notification Service) Topic
- Xuất bản thông báo đến các subscriber
- Yêu cầu SNS resource access policy

### 2. SQS (Simple Queue Service) Queue
- Xếp hàng các thông điệp để xử lý
- Yêu cầu SQS resource access policy

### 3. Lambda Function
- Thực thi các hàm serverless
- Yêu cầu Lambda resource policy

## Đặc điểm Phân phối

- Các sự kiện thường được phân phối **trong vòng vài giây**
- Trong một số trường hợp, việc phân phối có thể mất một phút hoặc lâu hơn
- Bạn có thể tạo bao nhiêu event notification tùy ý

## Quyền IAM Cần thiết

S3 Event Notifications yêu cầu **resource-based policies** (không phải IAM roles):

### Đối với SNS Topics
Đính kèm **SNS resource access policy** để cho phép S3 bucket gửi thông điệp đến SNS topic.

### Đối với SQS Queues
Đính kèm **SQS resource access policy** để ủy quyền cho dịch vụ S3 gửi dữ liệu vào queue.

### Đối với Lambda Functions
Đính kèm **Lambda resource policy** để đảm bảo Amazon S3 có quyền gọi hàm.

> **Lưu ý:** Các resource access policies này hoạt động tương tự như S3 bucket policies.

## Tích hợp Nâng cao: Amazon EventBridge

Amazon EventBridge cung cấp khả năng nâng cao cho S3 Event Notifications:

### Tính năng Chính

- **Tất cả S3 events** tự động chuyển đến EventBridge
- **Tùy chọn lọc nâng cao** - Lọc theo metadata, kích thước đối tượng và tên
- **Nhiều đích** - Gửi đến hơn 18 dịch vụ AWS đồng thời
- **Các đích bổ sung** bao gồm:
  - AWS Step Functions
  - Amazon Kinesis Data Streams
  - Amazon Kinesis Data Firehose
  - Và nhiều hơn nữa

### Ưu điểm của EventBridge

- **Archive events (Lưu trữ sự kiện)** - Lưu trữ các sự kiện để phân tích lịch sử
- **Replay events (Phát lại sự kiện)** - Xử lý lại các sự kiện khi cần
- **Reliable delivery (Phân phối đáng tin cậy)** - Đảm bảo phân phối nâng cao
- **Rules-based routing (Định tuyến dựa trên quy tắc)** - Thiết lập các quy tắc định tuyến phức tạp

## Tóm tắt

Amazon S3 Event Notifications cho phép bạn phản ứng với các sự kiện trong S3 bucket bằng cách gửi thông báo đến:
- SNS Topics
- SQS Queues
- Lambda Functions
- Amazon EventBridge (cho các tình huống nâng cao)

Tính năng này rất quan trọng để xây dựng các quy trình làm việc tự động, hướng sự kiện trong AWS.




FILE: 62-amazon-s3-event-notifications-hands-on-tutorial.md


# Amazon S3 Event Notifications - Hướng Dẫn Thực Hành

## Tổng Quan

Hướng dẫn này trình bày cách thiết lập và kiểm tra Amazon S3 Event Notifications, cho phép bạn tự động kích hoạt các hành động khi có sự kiện cụ thể xảy ra trong S3 bucket của bạn.

## Yêu Cầu Trước

- Quyền truy cập vào AWS Console
- Quyền tạo S3 bucket và SQS queue
- Hiểu biết cơ bản về các dịch vụ S3 và SQS

## Bước 1: Tạo S3 Bucket

1. Truy cập Amazon S3 trong AWS Console
2. Tạo bucket mới với tên `stephane-v3-events-notifications`
3. Chọn region Ireland
4. Nhấn "Create bucket"

## Bước 2: Cấu Hình Event Notifications

### Hai Tùy Chọn Có Sẵn

Khi thiết lập S3 event notifications, bạn có hai tùy chọn chính:

1. **Tạo Event Notification** - Tích hợp trực tiếp với các dịch vụ AWS cụ thể (Lambda, SNS, SQS)
2. **Bật Amazon EventBridge Integration** - Gửi tất cả sự kiện đến EventBridge để định tuyến và xử lý nâng cao

Trong hướng dẫn này, chúng ta sẽ sử dụng tùy chọn đầu tiên đơn giản hơn.

### Thiết Lập Event Notification

1. Vào bucket vừa tạo
2. Chuyển đến tab **Properties**
3. Cuộn xuống phần **Event notifications**
4. Nhấn **Create event notification**

#### Chi Tiết Cấu Hình

- **Name**: `DemoEventNotification`
- **Prefix**: (để trống)
- **Suffix**: (để trống)

#### Loại Sự Kiện (Event Types)

Chọn **All object create events** - điều này sẽ kích hoạt thông báo mỗi khi có đối tượng được tạo trong bucket.

Các loại sự kiện có sẵn bao gồm:
- Sự kiện tạo đối tượng
- Sự kiện xóa đối tượng
- Sự kiện khôi phục đối tượng
- Và nhiều loại sự kiện cụ thể khác

#### Đích Đến (Destination)

Chọn **SQS queue** làm đích đến (các tùy chọn khác bao gồm Lambda function và SNS topic).

## Bước 3: Tạo SQS Queue

Trước khi cấu hình đích đến, bạn cần tạo một SQS queue:

1. Truy cập Amazon SQS
2. Nhấn **Create queue**
3. Đặt tên: `DemoS3Notification`
4. Nhấn **Create queue**

## Bước 4: Cấu Hình Access Policy

### Vấn Đề

Nếu bạn thử lưu cấu hình event notification ngay lập tức, bạn sẽ nhận được lỗi cho biết không thể xác thực cấu hình đích đến. Đây là vì SQS queue chưa có quyền chấp nhận tin nhắn từ S3.

### Giải Pháp

Bạn cần cập nhật access policy của SQS queue:

1. Vào SQS queue của bạn (`DemoS3Notification`)
2. Nhấn **Edit**
3. Cuộn xuống **Access policy**
4. Nhấn **Policy Generator**

#### Tạo Policy

- **Type**: SQS Queue Policy
- **Effect**: Allow
- **Principal**: * (bất kỳ ai - cho mục đích demo)
- **Actions**: SendMessage
- **ARN**: Sao chép và dán ARN của queue

5. Nhấn **Add Statement**
6. Nhấn **Generate Policy**
7. Sao chép policy đã tạo
8. Dán vào access policy của queue
9. Nhấn **Save**

> **Lưu ý**: Policy sử dụng trong demo này rất dễ dãi (cho phép bất kỳ ai gửi tin nhắn). Trong môi trường production, bạn nên hạn chế quyền này chỉ cho S3 bucket của bạn.

## Bước 5: Hoàn Thành Thiết Lập Event Notification

1. Quay lại cấu hình event notification của S3 bucket
2. Làm mới dropdown SQS queue
3. Chọn `DemoS3Notification`
4. Nhấn **Save changes**

### Sự Kiện Kiểm Tra (Test Event)

Sau khi lưu, Amazon S3 sẽ tự động gửi một sự kiện kiểm tra đến SQS queue để xác minh kết nối.

Bạn có thể xác minh bằng cách:
1. Vào SQS queue của bạn
2. Nhấn **Send and receive messages**
3. Nhấn **Poll for messages**
4. Bạn sẽ thấy một tin nhắn kiểm tra từ S3

## Bước 6: Kiểm Tra Event Notification

Bây giờ hãy kiểm tra event notification với một file thực tế:

1. Truy cập S3 bucket của bạn
2. Nhấn **Upload**
3. Nhấn **Add files**
4. Chọn một file (ví dụ: `coffee.jpeg`)
5. Nhấn **Upload**

### Xác Minh Thông Báo

1. Quay lại SQS queue
2. Nhấn **Send and receive messages**
3. Nhấn **Poll for messages**
4. Bạn sẽ thấy một tin nhắn mới

### Kiểm Tra Tin Nhắn

Tin nhắn sẽ chứa thông tin chi tiết về sự kiện S3:

```json
{
  "eventName": "ObjectCreated:Put",
  "s3": {
    "object": {
      "key": "coffee.jpeg"
    }
  }
}
```

Tin nhắn bao gồm:
- **eventName**: Loại sự kiện (ví dụ: `ObjectCreated:Put`)
- **key**: Tên của file đã được upload (ví dụ: `coffee.jpeg`)
- Metadata bổ sung về sự kiện

## Các Trường Hợp Sử Dụng

S3 Event Notifications rất mạnh mẽ cho việc tự động hóa quy trình làm việc, chẳng hạn như:

- **Xử Lý Hình Ảnh**: Tự động tạo thumbnail khi có ảnh được upload
- **Xử Lý Dữ Liệu**: Kích hoạt Lambda function để xử lý các file đã upload
- **Sao Lưu và Lưu Trữ**: Tự động sao chép file sang vị trí khác
- **Thông Báo**: Cảnh báo nhóm khi có file cụ thể được upload hoặc xóa

## Dọn Dẹp

Sau khi hoàn thành hướng dẫn:
1. Xóa tin nhắn kiểm tra khỏi SQS
2. Tùy chọn xóa file đã upload khỏi S3
3. Nếu không cần, xóa S3 bucket và SQS queue

## Những Điểm Chính Cần Nhớ

- S3 Event Notifications có thể được gửi đến **SQS**, **SNS**, và **Lambda**
- Bạn cũng có thể gửi tất cả sự kiện đến **Amazon EventBridge** để định tuyến và lọc nâng cao
- Cần có access policy phù hợp để S3 có thể gửi tin nhắn đến đích đến của bạn
- Event notification bao gồm thông tin chi tiết về những gì đã xảy ra trong bucket
- Điều này cho phép tự động hóa mạnh mẽ và kiến trúc hướng sự kiện (event-driven)

## Các Bước Tiếp Theo

- Khám phá việc sử dụng Lambda function làm đích đến cho xử lý phức tạp hơn
- Tìm hiểu về Amazon EventBridge để định tuyến sự kiện nâng cao
- Triển khai các trường hợp sử dụng thực tế như tạo thumbnail hình ảnh
- Nghiên cứu các loại sự kiện và tùy chọn lọc khác nhau

---

*Hướng dẫn này trình bày một triển khai cơ bản. Luôn tuân theo các best practice bảo mật của AWS và nguyên tắc quyền tối thiểu (principle of least privilege) khi cấu hình access policy trong môi trường production.*




FILE: 63-amazon-s3-performance-optimization.md


# Tối Ưu Hóa Hiệu Suất Amazon S3

## Hiệu Suất Cơ Bản của S3

Amazon S3 tự động mở rộng để xử lý số lượng yêu cầu rất cao với các đặc tính hiệu suất vượt trội:

### Chỉ Số Hiệu Suất

- **Độ trễ**: 100-200 milliseconds để lấy byte đầu tiên từ S3
- **Giới hạn yêu cầu trên mỗi Prefix**:
  - 3,500 yêu cầu PUT/COPY/POST/DELETE mỗi giây
  - 5,500 yêu cầu GET/HEAD mỗi giây
- **Không giới hạn** số lượng prefix trong bucket của bạn

### Hiểu về Prefix

Prefix là đường dẫn giữa tên bucket và tên object. Dưới đây là một số ví dụ:

| Đường dẫn Object | Prefix |
|-----------------|--------|
| `bucket/folder1/sub1/file` | `/folder1/sub1` |
| `bucket/folder1/sub2/file` | `/folder1/sub2` |
| `bucket/folder2/sub1/file` | `/folder2/sub1` |
| `bucket/folder2/sub2/file` | `/folder2/sub2` |

**Ví dụ**: Nếu bạn phân tán các yêu cầu đọc đều trên bốn prefix khác nhau, bạn có thể đạt được **22,000 yêu cầu mỗi giây** cho các thao tác GET/HEAD.

## Các Kỹ Thuật Tối Ưu Hóa Hiệu Suất S3

### 1. Multi-Part Upload (Tải lên Đa phần)

Multi-part upload cho phép bạn tải lên các file lớn thành nhiều phần song song, tối đa hóa việc sử dụng băng thông.

**Khi nào nên sử dụng**:
- **Khuyến nghị** cho các file trên 100 MB
- **Bắt buộc** cho các file trên 5 GB

**Cách hoạt động**:
1. Chia file lớn thành các phần nhỏ hơn
2. Tải lên từng phần song song lên Amazon S3
3. S3 tự động ghép các phần lại thành file hoàn chỉnh

**Lợi ích**:
- Tải lên song song
- Tốc độ truyền tải nhanh hơn
- Tận dụng băng thông tốt hơn

### 2. S3 Transfer Acceleration (Tăng tốc truyền tải S3)

Transfer Acceleration tăng tốc độ truyền file bằng cách định tuyến dữ liệu qua các edge location của AWS.

**Tính năng chính**:
- Hoạt động cho cả tải lên và tải xuống
- Sử dụng mạng riêng của AWS để truyền tải nhanh hơn
- Tương thích với multi-part upload
- Hơn 200 edge location trên toàn thế giới

**Cách hoạt động**:

```
USA (File) → Edge Location (USA) → [Mạng riêng AWS] → S3 Bucket (Úc)
     ↑                                                        ↑
  Tải lên nhanh                                      Truyền tải nhanh
 (Internet công cộng)                                 (Mạng riêng)
```

**Lợi ích**:
- Giảm thiểu sử dụng internet công cộng
- Tối đa hóa sử dụng mạng riêng AWS
- Nhanh hơn đáng kể cho các truyền tải khoảng cách xa

### 3. S3 Byte-Range Fetches (Lấy dữ liệu theo phạm vi Byte)

Byte-Range Fetches cho phép bạn tải xuống các phạm vi byte cụ thể của file một cách song song.

**Trường hợp sử dụng**:

#### Tăng tốc tải xuống
- Yêu cầu các phạm vi byte khác nhau song song
- Song song hóa các yêu cầu GET để tải xuống nhanh hơn
- Khả năng phục hồi tốt hơn: chỉ thử lại các phạm vi byte bị lỗi

**Ví dụ**:
```
File lớn trong S3
├── Phần 1 (bytes 0-1000) ──┐
├── Phần 2 (bytes 1001-2000) ├──→ Tải xuống song song
└── Phần 3 (bytes 2001-3000) ┘
```

#### Lấy dữ liệu một phần
- Chỉ yêu cầu dữ liệu bạn cần
- Ví dụ: Chỉ lấy phần header của file (50 bytes đầu tiên)
- Thời gian phản hồi nhanh hơn cho các truy vấn metadata

## Tóm tắt

Amazon S3 cung cấp nhiều kỹ thuật tối ưu hóa:

1. **Multi-Part Upload**: Song song hóa việc tải lên cho các file lớn
2. **Transfer Acceleration**: Sử dụng edge location để truyền tải toàn cầu nhanh hơn
3. **Byte-Range Fetches**: Song song hóa tải xuống và lấy dữ liệu một phần

Các kỹ thuật này giúp bạn tối đa hóa hiệu suất S3 cho cả tải lên và tải xuống trong khi vẫn tuân thủ các giới hạn hiệu suất.

---

**Lưu ý**: Hãy chắc chắn bạn hiểu các khái niệm này cho các kỳ thi chứng chỉ AWS.




FILE: 64-aws-s3-object-metadata-and-tags.md


# AWS S3 Object Metadata và Tags

## Tổng quan

Hướng dẫn này trình bày về metadata do người dùng định nghĩa và các thẻ (tags) của đối tượng S3, giải thích mục đích, sự khác biệt và cách tìm kiếm các đối tượng trong S3 buckets.

## Metadata của Đối tượng do Người dùng Định nghĩa

### Metadata của Đối tượng là gì?

Khi bạn tải một đối tượng lên S3, bạn có thể gán metadata cho nó. Metadata về cơ bản là các cặp key-value được đính kèm vào đối tượng của bạn, cung cấp thông tin về chính đối tượng đó.

### Quy ước Đặt tên Metadata

- **Metadata do người dùng định nghĩa** phải có tên bắt đầu bằng `x-amz-meta-`
- AWS cũng tự động tạo metadata riêng của mình

### Ví dụ về Metadata

Đối với một đối tượng S3, bạn có thể thấy:

- `Content-Length`: 7.5 kilobytes (do AWS cung cấp)
- `Content-Type`: html (do AWS cung cấp)
- `x-amz-meta-origin`: paris (do người dùng định nghĩa)

Metadata có thể được truy xuất trong khi lấy đối tượng.

## Tags của Đối tượng S3

### Tags của Đối tượng là gì?

Tags của đối tượng S3 là các cặp key-value cho các đối tượng của bạn trong Amazon S3. Chúng được sử dụng phổ biến hơn metadata cho các mục đích cụ thể.

### Tags so với Metadata

Tags khác với metadata theo nhiều cách quan trọng:

- **Phân quyền chi tiết**: Tags có thể được sử dụng để cấp quyền truy cập vào các đối tượng cụ thể với các tags cụ thể
- **Mục đích phân tích**: Các công cụ như S3 Analytics có thể nhóm kết quả theo tags

### Ví dụ về Tags

Đối với một đối tượng S3, bạn có thể gán:

- `Project`: Blue
- `PHI` (Thông tin Sức khỏe Cá nhân): True

## Hạn chế Quan trọng: Khả năng Tìm kiếm

### Điểm Chính cần Ghi nhớ

⚠️ **Metadata và tags KHÔNG thể tìm kiếm trên Amazon S3**

- Bạn không thể lọc theo metadata
- Bạn không thể lọc theo tags
- Đây không phải là khả năng gốc của S3

## Cách Tìm kiếm Đối tượng S3

### Giải pháp: Chỉ mục Bên ngoài

Nếu bạn cần tìm kiếm S3 buckets của mình dựa trên metadata hoặc tags, bạn phải:

1. **Xây dựng chỉ mục bên ngoài** trong cơ sở dữ liệu (như DynamoDB)
2. **Lưu trữ tất cả metadata và tags** trong chỉ mục có thể tìm kiếm
3. **Thực hiện tìm kiếm** trên cơ sở dữ liệu bên ngoài (DynamoDB)
4. **Trích xuất kết quả** dưới dạng các đối tượng từ Amazon S3

### Mô hình Kiến trúc

```
Đối tượng S3 (với metadata/tags)
    ↓
Chỉ mục Bên ngoài (DynamoDB)
    ↓
Truy vấn Tìm kiếm → DynamoDB
    ↓
Kết quả → Đối tượng S3
```

### Mẹo Thi

Đây là một câu hỏi phổ biến trong kỳ thi và là một mô hình kiến trúc quan trọng cần hiểu cho các chứng chỉ AWS.

## Tóm tắt

- **Metadata**: Các cặp key-value cung cấp thông tin về đối tượng (do người dùng định nghĩa phải bắt đầu bằng `x-amz-meta-`)
- **Tags**: Các cặp key-value được sử dụng cho phân quyền và phân tích
- **Không thể tìm kiếm**: Cả metadata và tags đều không thể tìm kiếm trực tiếp trong S3
- **Giải pháp**: Xây dựng chỉ mục có thể tìm kiếm bên ngoài trong cơ sở dữ liệu như DynamoDB

---

*Tài liệu này dựa trên các phương pháp tốt nhất của AWS S3 và các mô hình kiến trúc phổ biến.*




FILE: 65-amazon-s3-encryption-overview.md


# Tổng Quan về Mã Hóa Object trong Amazon S3

## Giới Thiệu

Mã hóa object trong Amazon S3 cung cấp nhiều phương thức để bảo mật dữ liệu của bạn khi lưu trữ và truyền tải. Hiểu rõ các tùy chọn mã hóa này là rất quan trọng để triển khai các biện pháp bảo mật phù hợp cho S3 buckets của bạn.

## Các Phương Thức Mã Hóa

Bạn có thể mã hóa các object trong S3 buckets bằng một trong bốn phương thức sau:

### 1. Mã Hóa Phía Server (SSE - Server-Side Encryption)

Mã hóa phía server có nhiều loại:

#### SSE-S3 (Mã Hóa Phía Server với Khóa do Amazon S3 Quản Lý)

**Tổng Quan:**
- Mã hóa sử dụng các khóa được xử lý, quản lý và sở hữu bởi AWS
- Bạn không bao giờ có quyền truy cập vào các khóa này
- Object được mã hóa phía server bởi AWS
- Sử dụng thuật toán mã hóa AES-256
- **Được bật mặc định** cho các bucket và object mới

**Cách Hoạt Động:**
1. Người dùng tải lên file với header đúng: `"x-amz-server-side-encryption": "AES256"`
2. Amazon S3 nhận object
3. S3 ghép nối object với khóa thuộc sở hữu của S3
4. Quá trình mã hóa được thực hiện bằng cách kết hợp khóa và object
5. Object đã mã hóa được lưu trữ trong S3 bucket

**Header Bắt Buộc:**
```
x-amz-server-side-encryption: AES256
```

#### SSE-KMS (Mã Hóa Phía Server với Khóa KMS)

**Tổng Quan:**
- Sử dụng AWS Key Management Service (KMS) để quản lý khóa mã hóa
- Cung cấp quyền kiểm soát khóa mã hóa cho người dùng
- Khóa có thể được tạo và quản lý trong KMS
- Việc sử dụng khóa được kiểm toán bằng AWS CloudTrail

**Ưu Điểm:**
- Người dùng có quyền kiểm soát khóa mã hóa
- Khả năng tạo các khóa tùy chỉnh trong KMS
- Theo dõi việc sử dụng khóa thông qua CloudTrail

**Cách Hoạt Động:**
1. Người dùng tải lên object với header KMS, chỉ định khóa KMS cần sử dụng
2. Object xuất hiện trong Amazon S3
3. Khóa KMS được chỉ định từ AWS KMS được sử dụng để mã hóa
4. Object và khóa được kết hợp để tạo file đã mã hóa
5. File đã mã hóa được lưu trữ trong S3 bucket

**Header Bắt Buộc:**
```
x-amz-server-side-encryption: aws:kms
```

**Yêu Cầu Truy Cập:**
Để đọc file được mã hóa bằng SSE-KMS, bạn cần:
- Quyền truy cập vào chính S3 object
- Quyền truy cập vào khóa KMS cơ bản được sử dụng để mã hóa

**Hạn Chế:**
- Các API của KMS (GenerateDataKey cho mã hóa, Decrypt cho giải mã) được tính vào hạn ngạch KMS
- Giới hạn lượt gọi API: 5.000 đến 30.000 yêu cầu mỗi giây (tùy theo vùng)
- Hạn ngạch có thể được tăng thông qua Service Quotas Console
- S3 bucket có lưu lượng cao với mã hóa KMS có thể gặp phải giới hạn throttling

#### SSE-C (Mã Hóa Phía Server với Khóa do Khách Hàng Cung Cấp)

**Tổng Quan:**
- Khóa được quản lý bên ngoài AWS
- Vẫn là mã hóa phía server (khóa được gửi đến AWS)
- Amazon S3 không bao giờ lưu trữ khóa mã hóa
- Khóa bị loại bỏ sau khi sử dụng

**Yêu Cầu:**
- **Phải sử dụng HTTPS** để truyền tải
- Khóa phải được truyền như một phần của HTTP headers cho mọi yêu cầu

**Cách Hoạt Động:**
1. Người dùng tải lên file cùng với khóa mã hóa (được quản lý bên ngoài AWS)
2. Amazon S3 sử dụng khóa do client cung cấp và object để thực hiện mã hóa
3. File đã mã hóa được lưu trữ trong S3 bucket
4. Để đọc file, người dùng phải cung cấp cùng khóa đã được sử dụng để mã hóa

### 2. Mã Hóa Phía Client (Client-Side Encryption)

**Tổng Quan:**
- Mã hóa được thực hiện hoàn toàn ở phía client
- Dữ liệu được mã hóa trước khi gửi đến Amazon S3
- Dữ liệu lấy từ S3 phải được giải mã bởi client
- Client hoàn toàn quản lý khóa và chu trình mã hóa

**Triển Khai:**
- Dễ dàng triển khai hơn khi sử dụng các thư viện client như AWS Client-Side Encryption Library

**Cách Hoạt Động:**
1. Client có một file và một khóa mã hóa (bên ngoài AWS)
2. Client thực hiện mã hóa cục bộ
3. File đã mã hóa được tải lên Amazon S3
4. File vẫn được mã hóa trong S3
5. Client lấy và giải mã file khi cần thiết

## Mã Hóa Trong Quá Trình Truyền Tải (Encryption in Transit)

**Tổng Quan:**
Mã hóa trong quá trình truyền tải, còn được gọi là mã hóa SSL/TLS, bảo vệ dữ liệu trong khi nó được truyền giữa client của bạn và Amazon S3.

**Các Endpoint của S3:**
- **HTTP endpoint** - Không được mã hóa
- **HTTPS endpoint** - Mã hóa trong quá trình truyền tải (được khuyến nghị)

**Thực Hành Tốt Nhất:**
- Luôn sử dụng HTTPS để truyền dữ liệu an toàn
- SSE-C **yêu cầu** giao thức HTTPS
- Hầu hết các client sử dụng HTTPS endpoint theo mặc định

### Bắt Buộc Mã Hóa Trong Quá Trình Truyền Tải

Bạn có thể ép buộc chỉ truy cập qua HTTPS bằng cách sử dụng bucket policy:

**Ví Dụ Bucket Policy:**
```json
{
  "Effect": "Deny",
  "Action": "s3:GetObject",
  "Condition": {
    "aws:SecureTransport": "false"
  }
}
```

**Cách Hoạt Động:**
- `aws:SecureTransport` là `true` khi sử dụng HTTPS
- `aws:SecureTransport` là `false` khi sử dụng HTTP
- Policy từ chối bất kỳ thao tác GetObject nào khi SecureTransport là false
- Người dùng cố gắng sử dụng HTTP sẽ bị chặn
- Người dùng sử dụng HTTPS sẽ được phép truy cập

## Tóm Tắt

Amazon S3 cung cấp các tùy chọn mã hóa toàn diện:

- **SSE-S3**: Mã hóa mặc định với khóa do AWS quản lý (tùy chọn đơn giản nhất)
- **SSE-KMS**: Mã hóa với khóa KMS do khách hàng kiểm soát (kiểm toán và kiểm soát)
- **SSE-C**: Mã hóa với khóa do khách hàng cung cấp (kiểm soát khóa hoàn toàn, khóa không được AWS lưu trữ)
- **Mã Hóa Phía Client**: Kiểm soát hoàn toàn mã hóa và khóa ở phía client
- **Mã Hóa Trong Quá Trình Truyền Tải**: Sử dụng HTTPS để bảo vệ dữ liệu trong quá trình truyền

Chọn phương thức mã hóa phù hợp nhất với yêu cầu bảo mật và tuân thủ của bạn.




FILE: 66-aws-s3-dsse-kms-encryption-overview.md


# Mã Hóa Hai Lớp Phía Máy Chủ Amazon S3 với DSSE-KMS

## Tổng Quan

DSSE-KMS là một tùy chọn mã hóa mới có sẵn trong Amazon S3, được phát hành vào tháng 6 năm 2023. DSSE-KMS là viết tắt của **"mã hóa kép dựa trên KMS"** (Key Management Service).

## DSSE-KMS Là Gì?

Mã hóa hai lớp phía máy chủ Amazon S3 với các khóa được lưu trữ trong AWS Key Management Service (DSSE-KMS) là một tùy chọn mã hóa mới áp dụng **hai lớp mã hóa** cho các đối tượng khi chúng được tải lên S3 bucket.

### Tính Năng Chính

- **Tuân Thủ**: Được thiết kế để đáp ứng National Security Agency CNSSP 15 cho tuân thủ FIPS và hướng dẫn Data-at-Rest Capability Package (DAR CP) Phiên bản 5.0 cho hai lớp mã hóa CNSA
- **Khả Năng Độc Đáo**: Amazon S3 là dịch vụ lưu trữ đối tượng đám mây duy nhất cho phép khách hàng áp dụng hai lớp mã hóa ở cấp độ đối tượng và kiểm soát các khóa dữ liệu được sử dụng cho cả hai lớp
- **Đối Tượng Mục Tiêu**: Giúp khách hàng có quy định cao dễ dàng đáp ứng các tiêu chuẩn bảo mật nghiêm ngặt, chẳng hạn như khách hàng Bộ Quốc phòng Hoa Kỳ (DoD)

## Cách Hoạt Động Của DSSE-KMS

### Triển Khai Mã Hóa

- Mỗi lớp mã hóa sử dụng một **thư viện triển khai mật mã riêng biệt** với các khóa mã hóa dữ liệu riêng lẻ
- Mỗi lớp sử dụng một triển khai khác nhau của thuật toán **Advanced Encryption Standard 256-bit với Galois Counter Mode (AES-GCM)**
- DSSE-KMS giúp bảo vệ dữ liệu nhạy cảm khỏi khả năng thấp về lỗ hổng trong một lớp triển khai mật mã duy nhất

### Quản Lý Khóa

- Sử dụng AWS Key Management Service (AWS KMS) để tạo các khóa dữ liệu
- Cho phép bạn kiểm soát các khóa được quản lý bởi khách hàng bằng cách đặt quyền cho mỗi khóa
- Hỗ trợ chỉ định lịch trình luân chuyển khóa

### Tùy Chọn Cấu Hình

Bạn có thể bật DSSE-KMS theo nhiều cách:
- Chỉ định mã hóa hai lớp phía máy chủ (DSSE) trong yêu cầu PUT hoặc COPY cho một đối tượng
- Cấu hình S3 bucket của bạn để áp dụng DSSE cho tất cả các đối tượng mới theo mặc định
- Thực thi DSSE-KMS bằng cách sử dụng chính sách IAM và bucket

## Các Tùy Chọn Mã Hóa Phía Máy Chủ của Amazon S3

Với bản phát hành này, Amazon S3 hiện cung cấp **bốn tùy chọn** cho mã hóa phía máy chủ:

1. **SSE-S3**: Mã hóa phía máy chủ với các khóa được quản lý bởi Amazon S3
2. **SSE-KMS**: Mã hóa phía máy chủ với AWS KMS
3. **SSE-C**: Mã hóa phía máy chủ với các khóa mã hóa do khách hàng cung cấp
4. **DSSE-KMS**: Mã hóa hai lớp phía máy chủ với các khóa được lưu trữ trong KMS

## Hướng Dẫn Thực Hành

### Bước 1: Tạo S3 Bucket và Bật DSSE-KMS

1. Trong bảng điều khiển Amazon S3, chọn **Buckets** trong ngăn điều hướng
2. Chọn **Create bucket**
3. Chọn một tên duy nhất và có ý nghĩa cho bucket
4. Trong phần **Default encryption**, chọn **DSSE-KMS** làm tùy chọn mã hóa
5. Từ các khóa AWS KMS có sẵn, chọn một khóa phù hợp với yêu cầu của bạn
6. Chọn **Create bucket** để hoàn tất việc tạo

### Bước 2: Tải Lên Đối Tượng vào S3 Bucket Đã Bật DSSE-KMS

1. Trong danh sách Buckets, chọn tên của bucket bạn muốn tải đối tượng lên
2. Trên tab **Objects** cho bucket, chọn **Upload**
3. Trong **Files and folders**, chọn **Add files**
4. Chọn một tệp để tải lên, sau đó chọn **Open**
5. Trong **Server-side encryption**, chọn **Do not specify an encryption key**
6. Chọn **Upload**

**Kết Quả**: Sau khi đối tượng được tải lên S3 bucket, đối tượng đã tải lên sẽ kế thừa cài đặt mã hóa phía máy chủ từ bucket.

### Bước 3: Tải Xuống Đối Tượng Được Mã Hóa DSSE-KMS

1. Chọn đối tượng mà bạn đã tải lên trước đó
2. Chọn **Download** hoặc chọn **Download as** từ menu Object actions
3. Sau khi đối tượng được tải xuống, mở nó cục bộ

**Kết Quả**: Đối tượng được giải mã tự động, không yêu cầu thay đổi ứng dụng khách.

## Lợi Ích

- **Quy Trình Đơn Giản**: Đơn giản hóa quy trình áp dụng hai lớp mã hóa cho dữ liệu của bạn mà không cần đầu tư vào cơ sở hạ tầng cần thiết cho mã hóa phía khách hàng
- **Phân Tích Dữ Liệu**: Bạn có thể truy vấn và phân tích dữ liệu được mã hóa kép của mình với các dịch vụ AWS như Amazon Athena, Amazon SageMaker, và nhiều hơn nữa
- **Tuân Thủ Quy Định**: Giúp đáp ứng các yêu cầu quy định để áp dụng nhiều lớp mã hóa cho dữ liệu của bạn

## Tính Khả Dụng và Giá Cả

- **Tính Khả Dụng**: Có sẵn trong tất cả các AWS Regions
- **Giá Cả**: Để biết thông tin về giá DSSE-KMS, hãy truy cập [trang giá Amazon S3](https://aws.amazon.com/s3/pricing/) (tab Storage) và [trang giá AWS KMS](https://aws.amazon.com/kms/pricing/)

## Bắt Đầu

Bạn có thể bắt đầu với DSSE-KMS thông qua:
- AWS CLI
- AWS Management Console

Để biết thêm thông tin, hãy truy cập [Hướng dẫn Sử dụng Amazon S3](https://docs.aws.amazon.com/s3/).

---

*Tác giả: Irshad*




FILE: 67-aws-s3-encryption-hands-on-tutorial.md


# AWS S3 Encryption - Hướng Dẫn Thực Hành

## Tổng Quan

Hướng dẫn thực hành này sẽ trình bày cách triển khai và quản lý các tùy chọn mã hóa khác nhau cho Amazon S3 bucket. Bạn sẽ học cách cấu hình mã hóa phía máy chủ (server-side encryption) sử dụng SSE-S3, SSE-KMS và DSSE-KMS.

## Yêu Cầu Trước Khi Bắt Đầu

- Quyền truy cập AWS Console
- Hiểu biết cơ bản về Amazon S3
- Các tệp mẫu để tải lên (ví dụ: coffee.jpg, beach.jpg)

## Các Bước Thực Hành

### Bước 1: Tạo S3 Bucket với Mã Hóa Mặc Định

1. **Tạo bucket mới**
   - Tên bucket: `demo-encryption-stephane-v2`
   - Điều hướng qua trình hướng dẫn tạo bucket

2. **Kích hoạt bucket versioning**
   - Cho phép theo dõi các phiên bản khác nhau của đối tượng với các cài đặt mã hóa khác nhau
   - Giữ tùy chọn này được bật

3. **Cấu hình mã hóa mặc định**
   - Trong phần cài đặt "Default encryption"
   - Có ba tùy chọn mã hóa (phải chọn một):
     - **SSE-S3**: Mã hóa phía máy chủ với khóa do Amazon S3 quản lý
     - **SSE-KMS**: Mã hóa phía máy chủ với AWS Key Management Service
     - **DSSE-KMS**: Mã hóa hai lớp phía máy chủ với KMS
   - Chọn **SSE-S3** cho thiết lập ban đầu

4. **Tạo bucket**
   - Nhấp "Create bucket"
   - Bucket hiện đã được tạo với mã hóa mặc định được kích hoạt

### Bước 2: Tải Lên và Xác Minh Mã Hóa

1. **Tải lên một tệp**
   - Nhấp "Add file"
   - Chọn `coffee.jpg`
   - Nhấp "Upload"

2. **Xác minh cài đặt mã hóa**
   - Nhấp vào tệp đã tải lên
   - Cuộn xuống phần "Server-side encryption settings"
   - Xác nhận tệp được mã hóa với **SSE-S3** (khóa do Amazon S3 quản lý)

### Bước 3: Thay Đổi Mã Hóa cho Một Đối Tượng

1. **Chỉnh sửa cài đặt mã hóa**
   - Chọn tệp đã tải lên
   - Nhấp "Edit"
   - Lưu ý: Chỉnh sửa mã hóa phía máy chủ sẽ tạo một phiên bản mới của đối tượng

2. **Ghi đè mã hóa mặc định của bucket**
   - Chọn ghi đè mã hóa mặc định của bucket
   - Chọn loại mã hóa: **SSE-KMS** (hoặc DSSE-KMS)

3. **Về DSSE-KMS**
   - Cung cấp hai lớp mã hóa trên KMS
   - Mã hóa mạnh hơn so với KMS tiêu chuẩn
   - Trong hướng dẫn này, chúng ta sẽ sử dụng **SSE-KMS** tiêu chuẩn

4. **Chỉ định khóa KMS**
   - Tùy chọn 1: Nhập ARN của khóa KMS
   - Tùy chọn 2: Chọn từ các khóa KMS hiện có
   - Chọn khóa **AWS/S3** (khóa KMS mặc định cho dịch vụ S3)
   - Khóa mặc định này không phát sinh chi phí bổ sung
   - Lưu ý: Khóa KMS tùy chỉnh sẽ phát sinh phí hàng tháng

5. **Lưu thay đổi**
   - Nhấp "Save changes"

### Bước 4: Xác Minh Versioning và Mã Hóa Mới

1. **Kiểm tra các phiên bản đối tượng**
   - Điều hướng đến tab "Versions"
   - Bạn sẽ thấy hai phiên bản của tệp

2. **Xác minh mã hóa phiên bản hiện tại**
   - Chọn phiên bản hiện tại
   - Cuộn xuống phần "Server-side encryption"
   - Xác nhận loại mã hóa: **SSE-KMS**
   - Xác minh khóa mã hóa khớp với khóa AWS/S3 KMS mặc định

### Bước 5: Tải Lên với Cài Đặt Mã Hóa Tùy Chỉnh

1. **Tải lên tệp mới**
   - Nhấp "Add file"
   - Chọn `beach.jpg`

2. **Cấu hình mã hóa trong quá trình tải lên**
   - Trong phần "Properties"
   - Tìm "Server-side encryption"
   - Chọn tùy chọn mã hóa:
     - Sử dụng cơ chế mã hóa mặc định, hoặc
     - Ghi đè với SSE-S3, SSE-KMS, hoặc DSSE-KMS

### Bước 6: Sửa Đổi Mã Hóa Mặc Định của Bucket

1. **Truy cập cài đặt mã hóa mặc định**
   - Điều hướng đến cài đặt bucket
   - Cuộn xuống "Default encryption"
   - Nhấp "Edit"

2. **Các tùy chọn mã hóa có sẵn**
   - **SSE-S3**: Khóa do Amazon S3 quản lý
   - **SSE-KMS**: AWS Key Management Service
   - **DSSE-KMS**: Mã hóa hai lớp với KMS

3. **Tùy chọn Bucket Key (cho SSE-KMS/DSSE-KMS)**
   - Có sẵn khi sử dụng mã hóa KMS
   - Giảm chi phí bằng cách tối thiểu hóa các lệnh gọi API đến AWS KMS
   - Được bật theo mặc định
   - Không áp dụng cho SSE-S3

## Tổng Kết Các Tùy Chọn Mã Hóa

### Có Sẵn Trong Console

- **SSE-S3**: Mã hóa phía máy chủ với khóa do Amazon S3 quản lý
- **SSE-KMS**: Mã hóa phía máy chủ với AWS KMS
- **DSSE-KMS**: Mã hóa hai lớp phía máy chủ với AWS KMS

### Không Có Sẵn Trong Console

- **SSE-C**: Mã hóa phía máy chủ với khóa do khách hàng cung cấp
  - Chỉ có thể cấu hình qua AWS CLI
  - Không có sẵn trong AWS Console

- **Client-Side Encryption (Mã hóa phía client)**
  - Dữ liệu được mã hóa ở phía client trước khi tải lên
  - Dữ liệu được giải mã ở phía client sau khi tải xuống
  - Không cần thông báo cho AWS về mã hóa phía client
  - AWS xử lý nó như dữ liệu thông thường

## Những Điểm Chính Cần Ghi Nhớ

1. **Mã hóa mặc định là bắt buộc** - Bạn phải chọn một phương thức mã hóa mặc định cho tất cả các S3 bucket

2. **Ghi đè mã hóa ở cấp độ đối tượng** - Bạn có thể ghi đè mã hóa mặc định của bucket cho từng đối tượng riêng lẻ

3. **Versioning theo dõi các thay đổi mã hóa** - Thay đổi mã hóa của đối tượng sẽ tạo một phiên bản mới

4. **Cân nhắc về chi phí**:
   - Khóa AWS/S3 KMS mặc định là miễn phí
   - Khóa KMS tùy chỉnh phát sinh phí hàng tháng
   - Tùy chọn Bucket Key giảm chi phí API KMS

5. **Giới hạn của Console**:
   - SSE-C yêu cầu AWS CLI
   - Mã hóa phía client được xử lý độc lập

## Kết Luận

Bạn đã học thành công cách cấu hình và quản lý các tùy chọn mã hóa khác nhau trong Amazon S3, bao gồm SSE-S3, SSE-KMS và DSSE-KMS. Hiểu rõ các cơ chế mã hóa này là rất quan trọng để bảo mật dữ liệu của bạn trong AWS.

## Các Bước Tiếp Theo

- Khám phá mã hóa SSE-C sử dụng AWS CLI
- Triển khai mã hóa phía client trong ứng dụng của bạn
- Tìm hiểu về chính sách và quyền của khóa KMS
- Thực hành với các kịch bản mã hóa khác nhau




FILE: 68-aws-s3-default-encryption-vs-bucket-policies.md


# AWS S3: Mã Hóa Mặc Định vs Chính Sách Bucket

## Tổng Quan

Tài liệu này giải thích mối quan hệ giữa mã hóa mặc định của S3 và chính sách bucket, cũng như cách chúng có thể được sử dụng để áp dụng các yêu cầu mã hóa cho các bucket S3 của bạn.

## Mã Hóa Mặc Định

### Hành Vi Mặc Định Hiện Tại

Theo mặc định, tất cả các bucket S3 hiện nay đều có **mã hóa mặc định được kích hoạt với SSE-S3** (Mã hóa phía máy chủ với khóa do Amazon S3 quản lý). Mã hóa này:
- Được áp dụng tự động cho các đối tượng mới
- Được bật mặc định cho tất cả các bucket mới

### Tùy Chỉnh Mã Hóa Mặc Định

Bạn có thể thay đổi cài đặt mã hóa mặc định để sử dụng các phương thức mã hóa khác nhau, chẳng hạn như:
- **SSE-KMS** (Mã hóa phía máy chủ với AWS Key Management Service)
- Các loại mã hóa được hỗ trợ khác

## Chính Sách Bucket Để Áp Dụng Mã Hóa

### Sử Dụng Chính Sách Bucket Để Bắt Buộc Mã Hóa

Chính sách bucket cung cấp một cách để **áp dụng mã hóa** bằng cách từ chối các lệnh gọi API không bao gồm các header mã hóa chính xác. Điều này cho phép bạn bắt buộc các phương thức mã hóa cụ thể cho các đối tượng được tải lên bucket của bạn.

### Ví Dụ Chính Sách Bucket

#### 1. Bắt Buộc Mã Hóa SSE-KMS

Chính sách này từ chối các yêu cầu PUT object không bao gồm header mã hóa AWS KMS:

```json
{
  "Effect": "Deny",
  "Action": "s3:PutObject",
  "Condition": {
    "StringNotEquals": {
      "s3:x-amz-server-side-encryption": "aws:kms"
    }
  }
}
```

#### 2. Bắt Buộc Mã Hóa SSE-C

Chính sách này từ chối các tải lên không bao gồm header thuật toán mã hóa phía khách hàng (SSE-C):

```json
{
  "Effect": "Deny",
  "Action": "s3:PutObject",
  "Condition": {
    "Null": {
      "s3:x-amz-server-side-encryption-customer-algorithm": "true"
    }
  }
}
```

## Thứ Tự Đánh Giá

**Quan trọng:** Chính sách bucket **luôn được đánh giá trước cài đặt mã hóa mặc định**. Điều này có nghĩa là:

1. Nếu chính sách bucket từ chối yêu cầu do thiếu header mã hóa, yêu cầu sẽ bị từ chối
2. Mã hóa mặc định chỉ được áp dụng nếu chính sách bucket cho phép yêu cầu tiếp tục
3. Chính sách bucket có quyền ưu tiên trong việc xác định các yêu cầu mã hóa

## Điểm Chính Cần Ghi Nhớ

- ✅ Mã hóa mặc định được bật theo mặc định với SSE-S3
- ✅ Bạn có thể tùy chỉnh cài đặt mã hóa mặc định (ví dụ: sang SSE-KMS)
- ✅ Chính sách bucket có thể được sử dụng để áp dụng các phương thức mã hóa cụ thể
- ✅ Chính sách bucket được đánh giá **trước** cài đặt mã hóa mặc định
- ✅ Sử dụng chính sách bucket để bắt buộc header mã hóa cho các đối tượng được tải lên

## Thực Hành Tốt Nhất

1. **Kích hoạt mã hóa mặc định** như một biện pháp bảo mật cơ bản
2. **Sử dụng chính sách bucket** khi bạn cần áp dụng các phương thức mã hóa cụ thể
3. **Ghi chép các yêu cầu mã hóa của bạn** cho nhóm và ứng dụng của bạn
4. **Kiểm tra chính sách bucket của bạn** để đảm bảo chúng hoạt động như mong đợi mà không chặn các tải lên hợp lệ




FILE: 69-aws-s3-cors-cross-origin-resource-sharing.md


# AWS S3 CORS (Chia Sẻ Tài Nguyên Giữa Các Nguồn Gốc)

## Tổng Quan

CORS (Cross-Origin Resource Sharing - Chia sẻ tài nguyên giữa các nguồn gốc) là một cơ chế bảo mật dựa trên trình duyệt web, kiểm soát cách thức các tài nguyên có thể được yêu cầu từ các nguồn gốc khác nhau. Hiểu về CORS là điều cần thiết cho việc cấu hình AWS S3, đặc biệt khi lưu trữ các trang web tĩnh.

## Nguồn Gốc (Origin) Là Gì?

Một **nguồn gốc (origin)** bao gồm ba thành phần:
- **Scheme/Giao thức** (ví dụ: HTTPS)
- **Host/Tên miền** (ví dụ: www.example.com)
- **Cổng (Port)** (ví dụ: 443 cho HTTPS)

### Ví dụ:
Đối với `https://www.example.com`:
- Cổng ngầm định: **443** (mặc định của HTTPS)
- Giao thức: **HTTPS**
- Tên miền: **www.example.com**

## Cùng Nguồn Gốc vs Khác Nguồn Gốc

### Cùng Nguồn Gốc
Hai URL có cùng nguồn gốc nếu chúng có:
- Cùng scheme (giao thức)
- Cùng host (máy chủ)
- Cùng port (cổng)

**Ví dụ:** `https://www.example.com/page1` và `https://www.example.com/page2`

### Khác Nguồn Gốc
**Ví dụ:** `www.example.com` và `other.example.com`

## CORS Hoạt Động Như Thế Nào

CORS là một cơ chế bảo mật cho phép hoặc từ chối các yêu cầu đến các nguồn gốc khác khi đang truy cập nguồn gốc chính. Các yêu cầu đến các nguồn gốc khác nhau sẽ không được thực hiện trừ khi nguồn gốc đích cho phép rõ ràng thông qua **CORS headers** (Access-Control-Allow-Origin).

### Luồng Yêu Cầu CORS

1. **Trình Duyệt Web** → **Máy Chủ Web Nguồn Gốc** (`https://www.example.com`)
   - Trình duyệt yêu cầu file index.html

2. **Phản Hồi Index.html**
   - File HTML chỉ ra rằng cần tải thêm các tài nguyên (ví dụ: hình ảnh) từ máy chủ nguồn gốc khác (`www.other.com`)

3. **Yêu Cầu Pre-flight (Trước Chuyến Bay)**
   - Trình duyệt web thực hiện kiểm tra bảo mật bằng cách gửi yêu cầu pre-flight (OPTIONS) đến máy chủ nguồn gốc khác
   - Yêu cầu bao gồm header origin: `Origin: https://www.example.com`

4. **Phản Hồi CORS Headers**
   - Nếu máy chủ nguồn gốc khác được cấu hình cho CORS, nó sẽ phản hồi với các phương thức được cho phép
   - Ví dụ: "Tôi cho phép nguồn gốc example.com thực hiện các phương thức GET, PUT và DELETE"

5. **Yêu Cầu Thực Tế**
   - Nếu trình duyệt hài lòng với CORS headers, nó sẽ tiến hành thực hiện yêu cầu thực tế để lấy các file

## CORS với Amazon S3

Khi một client thực hiện yêu cầu cross-origin đến các S3 bucket của bạn, bạn cần kích hoạt các CORS headers chính xác. Đây là một **câu hỏi phổ biến trong kỳ thi**.

### Cấu Hình Nhanh
Bạn có thể cấu hình CORS để:
- Cho phép một **nguồn gốc cụ thể**
- Cho phép **tất cả các nguồn gốc** bằng cách sử dụng `*` (ký tự đại diện)

### Ví Dụ Tình Huống: Trang Web Tĩnh S3 với Tài Nguyên Cross-Origin

#### Thiết Lập:
- **S3 Bucket Chính:** `my-bucket-html` (lưu trữ index.html)
- **S3 Bucket Tài Nguyên:** `my-bucket-assets` (lưu trữ hình ảnh)
- Cả hai bucket đều bật tính năng lưu trữ trang web tĩnh

#### Luồng Yêu Cầu:

1. **Trình Duyệt** → **S3 Bucket Chính**
   - Yêu cầu: `GET index.html` từ URL trang web tĩnh của `my-bucket-html`

2. **Phản Hồi Index.html**
   - File HTML chứa tham chiếu hình ảnh: `<img src="https://my-bucket-assets.s3-website.../images/coffee.jpg">`

3. **Yêu Cầu Hình Ảnh Cross-Origin**
   - Trình duyệt yêu cầu: `GET images/coffee.jpg`
   - Request headers bao gồm:
     - Host đích: URL của `my-bucket-assets`
     - Origin: URL của `my-bucket-html`

4. **Kiểm Tra CORS**
   - **Không cấu hình CORS:** S3 bucket từ chối yêu cầu
   - **Có cấu hình CORS:** S3 bucket phản hồi với headers thích hợp và cho phép yêu cầu

## Điểm Chính Cần Nhớ

- CORS là một **cơ chế bảo mật của trình duyệt web** kiểm soát các yêu cầu cross-origin
- Các yêu cầu giữa các nguồn gốc khác nhau yêu cầu **sự cho phép rõ ràng** thông qua CORS headers
- Đối với Amazon S3, bạn phải **cấu hình CORS headers** để cho phép các yêu cầu cross-origin
- CORS cho phép hình ảnh, tài nguyên hoặc file được lấy từ một S3 bucket khi yêu cầu xuất phát từ nguồn gốc khác
- Điều này thường được kiểm tra trong các kỳ thi chứng chỉ AWS

## Các Trường Hợp Sử Dụng Phổ Biến

- Lưu trữ trang web tĩnh trên một S3 bucket trong khi phục vụ tài nguyên (hình ảnh, CSS, JavaScript) từ bucket khác
- Gọi API từ ứng dụng web được lưu trữ trên S3 đến tên miền khác
- Phân phối nội dung qua nhiều tên miền hoặc tên miền con

## Mẹo Cho Kỳ Thi

✅ Nhớ rằng CORS phải được cấu hình rõ ràng trên **bucket đích** (bucket được yêu cầu)
✅ Trình duyệt thực thi các chính sách CORS, không phải máy chủ
✅ Các yêu cầu pre-flight sử dụng phương thức HTTP OPTIONS
✅ Các CORS headers phổ biến bao gồm: `Access-Control-Allow-Origin`, `Access-Control-Allow-Methods`, `Access-Control-Allow-Headers`




FILE: 7-amazon-rds-proxy-overview.md


# Tổng Quan về Amazon RDS Proxy

## Giới Thiệu

Amazon RDS Proxy là một dịch vụ proxy cơ sở dữ liệu được quản lý hoàn toàn cho Amazon RDS, giúp ứng dụng mở rộng quy mô hiệu quả bằng cách gom nhóm và chia sẻ các kết nối cơ sở dữ liệu.

## Amazon RDS Proxy là gì?

Mặc dù bạn có thể triển khai cơ sở dữ liệu RDS trong VPC của mình và truy cập trực tiếp, Amazon RDS Proxy cung cấp một lớp bổ sung với nhiều lợi ích:

### Gom Nhóm Kết Nối (Connection Pooling)

Thay vì để mọi ứng dụng kết nối trực tiếp đến instance cơ sở dữ liệu RDS, các ứng dụng sẽ kết nối đến proxy. Proxy sau đó gom nhóm các kết nối này lại thành ít kết nối hơn đến instance cơ sở dữ liệu RDS.

**Lợi ích:**
- Cải thiện hiệu suất cơ sở dữ liệu
- Giảm áp lực lên tài nguyên cơ sở dữ liệu (CPU và RAM)
- Giảm thiểu các kết nối mở và timeout

## Tính Năng Chính

### 1. Hoàn Toàn Serverless và Tự Động Mở Rộng
- Không cần quản lý dung lượng
- Tự động mở rộng quy mô dựa trên nhu cầu
- Tính sẵn sàng cao trên nhiều Availability Zone

### 2. Cải Thiện Thời Gian Failover
- Giảm thời gian failover lên đến **66%**
- Ứng dụng kết nối đến proxy (không bị ảnh hưởng bởi failover)
- Proxy xử lý việc failover giữa các instance chính và dự phòng
- Hoạt động với cả RDS và Aurora

### 3. Hỗ Trợ Cơ Sở Dữ Liệu
RDS Proxy hỗ trợ:
- MySQL
- PostgreSQL
- MariaDB
- Microsoft SQL Server
- Aurora (MySQL và PostgreSQL)

### 4. Không Cần Thay Đổi Code
Chỉ cần thay đổi endpoint kết nối cơ sở dữ liệu từ RDS instance sang RDS Proxy - không cần thay đổi code ứng dụng.

### 5. Ép Buộc Xác Thực IAM
- Ép buộc xác thực IAM cho việc truy cập cơ sở dữ liệu
- Thông tin xác thực có thể được lưu trữ an toàn trong **AWS Secrets Manager**
- Tăng cường bảo mật cho các kết nối cơ sở dữ liệu

### 6. Chỉ Truy Cập Trong VPC
- RDS Proxy không bao giờ có thể truy cập công khai
- Chỉ có thể truy cập từ bên trong VPC của bạn
- Không thể kết nối qua internet (tăng cường bảo mật)

## Trường Hợp Sử Dụng: AWS Lambda Functions

Lambda functions đặc biệt phù hợp để hưởng lợi từ RDS Proxy:

### Vấn Đề
- Lambda functions có thể nhân lên thành hàng trăm hoặc hàng nghìn instance
- Chúng xuất hiện và biến mất rất nhanh
- Mỗi function mở kết nối trực tiếp đến cơ sở dữ liệu tạo ra:
  - Các kết nối mở vẫn còn hoạt động
  - Timeout kết nối
  - Cạn kiệt tài nguyên trên cơ sở dữ liệu

### Giải Pháp
- Lambda functions kết nối đến RDS Proxy thay vì trực tiếp đến cơ sở dữ liệu
- RDS Proxy gom nhóm các kết nối này
- Proxy được thiết kế để xử lý loại tải này
- Kết quả là ít kết nối hơn và được quản lý tốt hơn đến instance cơ sở dữ liệu RDS thực tế

## Điểm Chính Cần Nhớ

1. **Gom Nhóm Kết Nối**: Giảm thiểu và gom nhóm các kết nối đến instance cơ sở dữ liệu RDS
2. **Tối Ưu Failover**: Giảm thời gian failover lên đến 66%
3. **Bảo Mật**: Ép buộc xác thực IAM và lưu trữ thông tin xác thực an toàn trong Secrets Manager
4. **Serverless**: Được quản lý hoàn toàn, tự động mở rộng và tính sẵn sàng cao
5. **Không Thay Đổi Code**: Chỉ cần thay đổi endpoint đơn giản trong ứng dụng
6. **Tích Hợp Lambda**: Hoàn hảo cho các ứng dụng serverless với tải kết nối biến đổi

## Tổng Kết

Amazon RDS Proxy là dịch vụ thiết yếu khi bạn cần:
- Xử lý số lượng lớn kết nối cơ sở dữ liệu một cách hiệu quả
- Cải thiện khả năng phục hồi của ứng dụng trong quá trình failover cơ sở dữ liệu
- Ép buộc xác thực dựa trên IAM cho việc truy cập cơ sở dữ liệu
- Tích hợp Lambda functions hoặc các ứng dụng serverless khác với cơ sở dữ liệu RDS

Dịch vụ này cung cấp khả năng sử dụng tài nguyên tốt hơn, cải thiện tính sẵn sàng và tăng cường bảo mật mà không cần thay đổi code ứng dụng của bạn.




FILE: 70-aws-s3-cors-hands-on-tutorial.md


# AWS S3 CORS (Cross-Origin Resource Sharing) - Hướng Dẫn Thực Hành

## Tổng Quan

Hướng dẫn này trình bày cách cấu hình và kiểm tra Cross-Origin Resource Sharing (CORS) trên các trang web tĩnh Amazon S3. Bạn sẽ học cách kích hoạt các yêu cầu cross-origin giữa hai S3 bucket khác nhau đang lưu trữ các trang web tĩnh.

## CORS là gì?

CORS (Cross-Origin Resource Sharing) là một cơ chế bảo mật cho phép các trang web từ một nguồn gốc (domain) truy cập tài nguyên từ một nguồn gốc khác. Theo mặc định, trình duyệt web chặn các yêu cầu cross-origin vì lý do bảo mật. Các header CORS phải được cấu hình trên server để cho phép các yêu cầu này.

## Yêu Cầu Trước Khi Bắt Đầu

- Tài khoản AWS có quyền truy cập S3
- Các file HTML cơ bản: `index.html` và `extra-page.html`
- Hiểu biết về lưu trữ trang web tĩnh trên S3
- Trình duyệt web có developer tools (Chrome/Firefox)

## Các Bước Thực Hiện

### Bước 1: Chuẩn Bị File HTML

Đầu tiên, sửa đổi file `index.html` để kích hoạt demo CORS:

1. Mở file `index.html`
2. Điều hướng đến dòng 13
3. Xóa các ký tự comment trước thẻ `<div>`
4. Sau thẻ `<script>`, xóa các ký tự đánh dấu comment (`<!--` và `-->`)

Điều này sẽ kích hoạt một script để fetch một trang HTML bổ sung và hiển thị nó trên trang web của bạn.

**Kết Quả Mong Đợi:** Trang web sẽ hiển thị:
- "Hello world I love coffee"
- Một hình ảnh cà phê
- Nội dung được fetch từ `extra-page.html`

### Bước 2: Thiết Lập S3 Bucket Đầu Tiên (Origin Bucket)

1. Điều hướng đến S3 bucket hiện có của bạn
2. Vào tab **Properties**
3. Kích hoạt **Static website hosting**
4. Đặt `index.html` làm index document
5. Upload cả hai file `index.html` và `extra-page.html`
6. Làm cho bucket công khai bằng cách cấu hình bucket policy
7. Truy cập URL endpoint công khai của bucket

**Kiểm Tra:** Tại thời điểm này, yêu cầu fetch hoạt động vì cả hai file đều nằm trong cùng một bucket (cùng nguồn gốc).

### Bước 3: Tạo S3 Bucket Thứ Hai (Nguồn Gốc Khác)

Để demo CORS, tạo một bucket khác trong một region khác:

1. Tạo một bucket mới có tên `demo-other-origin-stephane` (sử dụng tên duy nhất của bạn)
2. Chọn một AWS region khác (ví dụ: Canada)
3. **Bỏ chặn tất cả public access** (chúng ta sẽ làm cho bucket này công khai)
4. Tạo bucket

### Bước 4: Cấu Hình Bucket Thứ Hai Làm Trang Web Tĩnh

1. Vào bucket mới
2. Điều hướng đến tab **Properties**
3. Cuộn xuống **Static website hosting**
4. Kích hoạt static website hosting
5. Đặt `index.html` làm index document (mặc dù chúng ta sẽ không upload nó)

### Bước 5: Làm Cho Bucket Thứ Hai Công Khai

1. Vào tab **Permissions**
2. Chỉnh sửa **Bucket Policy**
3. Thêm policy để làm cho bucket công khai:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::demo-other-origin-stephane/*"
    }
  ]
}
```

4. Thay thế tên bucket trong trường `Resource` bằng ARN của bucket của bạn
5. Lưu thay đổi

### Bước 6: Upload File Lên Bucket Thứ Hai

1. Upload `extra-page.html` lên bucket thứ hai
2. Xác minh file có thể truy cập công khai bằng cách nhấp vào Object URL
3. Bạn sẽ thấy "This extra page has been successfully loaded"

### Bước 7: Cập Nhật Bucket Đầu Tiên

1. Trong bucket đầu tiên, **xóa** file `extra-page.html` (bây giờ chúng ta sẽ fetch nó từ bucket thứ hai)
2. Sửa đổi file `index.html` để fetch từ URL của bucket thứ hai:
   - Sao chép URL trang web tĩnh đầy đủ từ bucket thứ hai (ví dụ: `http://demo-other-origin-stephane.s3-website.ca-central-1.amazonaws.com/extra-page.html`)
   - Cập nhật URL fetch trong `index.html` để trỏ đến đường dẫn đầy đủ này
3. Upload lại file `index.html` đã sửa đổi lên bucket đầu tiên

### Bước 8: Quan Sát Lỗi CORS

1. Mở URL trang web của bucket đầu tiên trong trình duyệt web
2. Mở **Developer Tools** (Chrome: More tools → Developer tools)
3. Vào tab **Console**
4. Làm mới trang

**Lỗi Mong Đợi:**
```
Cross-Origin Request Blocked: The Same Origin Policy disallows reading the remote resource.
CORS header 'Access-Control-Allow-Origin' is missing.
```

Lỗi này xảy ra vì bucket thứ hai chưa được cấu hình CORS, do đó trình duyệt chặn yêu cầu.

### Bước 9: Cấu Hình CORS Trên Bucket Thứ Hai

1. Vào bucket thứ hai
2. Điều hướng đến tab **Permissions**
3. Cuộn xuống **Cross-origin resource sharing (CORS)**
4. Nhấp **Edit**
5. Thêm cấu hình CORS sau:

```json
[
  {
    "AllowedHeaders": ["*"],
    "AllowedMethods": ["GET", "HEAD"],
    "AllowedOrigins": ["http://demo-origin-stephane.s3-website.us-east-1.amazonaws.com"],
    "ExposeHeaders": []
  }
]
```

6. Thay thế URL trong `AllowedOrigins` bằng URL trang web tĩnh của bucket đầu tiên (không có dấu gạch chéo ở cuối)
7. Lưu cấu hình CORS

### Bước 10: Xác Minh CORS Đang Hoạt Động

1. Quay lại trang web của bucket đầu tiên
2. Làm mới trang
3. Nội dung trang bổ sung bây giờ sẽ được tải thành công

**Xác Minh Trong Developer Tools:**
1. Mở tab **Network**
2. Tìm yêu cầu đến `extra-page.html`
3. Nhấp vào nó và xem **Response Headers**
4. Bạn sẽ thấy các header CORS:
   - `Access-Control-Allow-Methods: GET`
   - `Access-Control-Allow-Origin: http://demo-origin-stephane.s3-website.us-east-1.amazonaws.com`

## Các Khái Niệm Chính

### Header CORS

- **Access-Control-Allow-Origin**: Chỉ định nguồn gốc nào có thể truy cập tài nguyên
- **Access-Control-Allow-Methods**: Chỉ định các phương thức HTTP nào được cho phép (GET, POST, v.v.)
- **Access-Control-Allow-Headers**: Chỉ định các header nào có thể được sử dụng trong yêu cầu

### Same-Origin Policy (Chính Sách Cùng Nguồn Gốc)

Theo mặc định, trình duyệt thực thi Same-Origin Policy, ngăn các script từ một nguồn gốc truy cập tài nguyên trên một nguồn gốc khác. CORS cung cấp một cách để nới lỏng hạn chế này một cách an toàn.

### Khi Nào Bạn Cần CORS?

CORS được yêu cầu khi:
- Một ứng dụng web trên một domain cần fetch tài nguyên từ domain khác
- Một API trên một domain cần được truy cập bởi frontend trên một domain khác
- Các tài nguyên tĩnh được lưu trữ trên một domain khác với ứng dụng chính

## Mẹo Thi Chứng Chỉ AWS

- Hiểu CORS là gì ở mức độ cao
- Biết rằng các header CORS phải được cấu hình trên **tài nguyên được truy cập** (không phải nguồn gốc thực hiện yêu cầu)
- Nhớ rằng lỗi CORS xuất hiện trong console của trình duyệt
- Cấu hình CORS trong S3 được thực hiện trong tab Permissions dưới "Cross-origin resource sharing (CORS)"

## Khắc Phục Sự Cố

### Lỗi CORS Vẫn Xuất Hiện

1. Xác minh URL `AllowedOrigins` khớp chính xác (không có dấu gạch chéo ở cuối)
2. Kiểm tra rằng bucket là công khai và object có thể truy cập
3. Xóa cache trình duyệt và làm mới
4. Xác minh cấu hình CORS được lưu đúng cách

### Lỗi 404 Not Found

1. Đảm bảo file tồn tại trong bucket
2. Kiểm tra tên file khớp chính xác (phân biệt chữ hoa chữ thường)
3. Xác minh bucket policy cho phép quyền đọc công khai

## Dọn Dẹp

Để tránh bị tính phí:
1. Xóa tất cả các file đã upload từ cả hai bucket
2. Xóa cả hai S3 bucket
3. Xác minh tất cả tài nguyên đã được loại bỏ

## Kết Luận

Bạn đã cấu hình và kiểm tra thành công CORS trên các trang web tĩnh AWS S3. Điều này minh họa cách các yêu cầu cross-origin hoạt động và cách cấu hình đúng các header CORS để cho phép chúng. Mặc dù điều này có vẻ nâng cao, nhưng việc hiểu CORS rất quan trọng cho kỳ thi chứng chỉ AWS và phát triển ứng dụng web thực tế.

## Tài Nguyên Bổ Sung

- [Tài Liệu AWS S3 CORS](https://docs.aws.amazon.com/AmazonS3/latest/userguide/cors.html)
- [MDN Web Docs - CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [Lưu Trữ Trang Web Tĩnh AWS S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html)




FILE: 71-aws-s3-mfa-delete-overview.md


# Tổng Quan về AWS S3 MFA Delete

## Giới Thiệu

MFA Delete là một tính năng bảo mật trong Amazon S3 cung cấp thêm một lớp bảo vệ cho các thao tác quan trọng trên bucket. MFA là viết tắt của **Multi-Factor Authentication** (Xác thực Đa Yếu Tố), yêu cầu người dùng phải tạo mã code trên thiết bị vật lý hoặc ảo trước khi thực hiện các hành động có tính phá hủy nhất định.

## MFA Delete là gì?

MFA Delete bắt buộc người dùng phải cung cấp mã xác minh từ một thiết bị xác thực trước khi thực thi các thao tác quan trọng trên S3 bucket. Thiết bị xác thực này có thể là:

- Điện thoại di động với ứng dụng xác thực (ví dụ: Google Authenticator)
- Thiết bị phần cứng MFA
- Bất kỳ thiết bị tạo mã token MFA tương thích nào khác

Mã code được tạo ra phải được nhập vào Amazon S3 trước khi hệ thống cho phép thao tác được tiếp tục.

## Khi Nào Cần MFA?

### Các Thao Tác Yêu Cầu MFA:

1. **Xóa vĩnh viễn một phiên bản đối tượng** - Cung cấp bảo vệ chống lại việc xóa vĩnh viễn do nhầm lẫn hoặc ác ý
2. **Tạm ngừng Versioning trên bucket** - Đây là thao tác phá hủy loại bỏ tính năng bảo vệ phiên bản

### Các Thao Tác KHÔNG Yêu Cầu MFA:

1. **Bật Versioning** - Đây là hành động bảo vệ, không phải phá hủy
2. **Liệt kê các phiên bản đã xóa** - Đây là thao tác chỉ đọc

## Điều Kiện Tiên Quyết và Yêu Cầu

Để sử dụng MFA Delete, bạn phải:

1. **Bật Versioning** trên bucket trước - MFA Delete liên quan trực tiếp đến tính năng Versioning
2. **Sử dụng tài khoản root** - Chỉ chủ sở hữu bucket (tài khoản root) mới có thể bật hoặc tắt MFA Delete

## Những Lưu Ý Quan Trọng

- Việc sử dụng tài khoản root không được khuyến khích cho các thao tác thường xuyên, nhưng lại bắt buộc để quản lý cài đặt MFA Delete
- MFA Delete cung cấp thêm một lớp bảo vệ được thiết kế đặc biệt để ngăn chặn việc xóa vĩnh viễn các phiên bản đối tượng
- Cả việc xóa vĩnh viễn đối tượng và tạm ngừng versioning đều được coi là các thao tác phá hủy, đó là lý do tại sao chúng yêu cầu xác thực MFA

## Tóm Tắt

MFA Delete là một tính năng bảo mật thiết yếu bổ sung xác thực đa yếu tố cho các thao tác quan trọng trên S3 bucket. Bằng cách yêu cầu mã xác thực dựa trên thời gian cho các hành động phá hủy như xóa vĩnh viễn đối tượng và tạm ngừng versioning, nó giảm đáng kể nguy cơ mất dữ liệu do nhầm lẫn hoặc truy cập trái phép.




FILE: 72-aws-s3-mfa-delete-tutorial.md


# AWS S3 MFA Delete - Hướng Dẫn Thực Hành

## Tổng Quan

Hướng dẫn này trình bày cách kích hoạt và sử dụng tính năng Multi-Factor Authentication (MFA) Delete cho các bucket Amazon S3. MFA Delete bổ sung thêm một lớp bảo mật bằng cách yêu cầu xác thực MFA trước khi xóa vĩnh viễn các phiên bản đối tượng hoặc vô hiệu hóa versioning trên bucket.

## Yêu Cầu Trước Khi Bắt Đầu

- Quyền truy cập tài khoản AWS Root
- Thiết bị MFA đã được cấu hình cho tài khoản root
- AWS CLI đã được cài đặt và cấu hình
- Kiến thức cơ bản về S3 versioning

## Bước 1: Tạo S3 Bucket với Versioning

1. Truy cập vào giao diện Amazon S3 console
2. Tạo bucket mới với các cài đặt sau:
   - Tên bucket: `demo-stephane-mfa-delete-2020` (hoặc tên bạn chọn)
   - Region: `eu-west-1` (hoặc region bạn muốn)
   - Bật bucket versioning
3. Nhấp **Create bucket**

## Bước 2: Xác Minh Thiết Lập MFA Device

1. Đăng nhập vào AWS console với tài khoản root
2. Điều hướng đến **IAM** → **Security Credentials**
3. Trong phần **Multi-Factor Authentication (MFA)**, xác minh rằng thiết bị MFA ảo đã được cấu hình
4. Sao chép ARN của thiết bị MFA (bạn sẽ cần thông tin này sau)

## Bước 3: Cấu Hình AWS CLI với Root Credentials

> **Cảnh báo**: Không khuyến khích sử dụng thông tin xác thực tài khoản root cho các hoạt động thường xuyên. Chỉ sử dụng cho việc bật MFA Delete.

1. Tạo access keys cho tài khoản root:
   - Vào **IAM** → **Security Credentials**
   - Nhấp **Create access key**
   - Tải xuống và lưu file access key
   
2. Cấu hình AWS CLI với named profile:

```bash
aws configure --profile root-mfa-delete-demo
```

3. Nhập các thông tin khi được yêu cầu:
   - AWS Access Key ID: [Root access key của bạn]
   - AWS Secret Access Key: [Root secret key của bạn]
   - Default region name: `eu-west-1`
   - Default output format: [Nhấn Enter]

4. Kiểm tra profile:

```bash
aws s3 ls --profile root-mfa-delete-demo
```

## Bước 4: Kích Hoạt MFA Delete

Sử dụng AWS CLI để kích hoạt MFA Delete trên bucket:

```bash
aws s3api put-bucket-versioning \
  --bucket demo-stephane-mfa-delete-2020 \
  --versioning-configuration Status=Enabled,MFADelete=Enabled \
  --mfa "arn:aws:iam::ACCOUNT-ID:mfa/root-account-mfa-device MFA-CODE" \
  --profile root-mfa-delete-demo
```

Thay thế:
- `demo-stephane-mfa-delete-2020` bằng tên bucket của bạn
- `arn:aws:iam::ACCOUNT-ID:mfa/root-account-mfa-device` bằng ARN thiết bị MFA của bạn
- `MFA-CODE` bằng mã 6 chữ số hiện tại từ thiết bị MFA

## Bước 5: Xác Minh MFA Delete Đã Được Kích Hoạt

1. Vào bucket S3 trong console
2. Nhấp **Properties** → **Bucket Versioning** → **Edit**
3. Xác minh rằng cả hai đều:
   - Bucket versioning đã **Enabled**
   - MFA Delete đã **Enabled**

## Bước 6: Kiểm Tra Bảo Vệ MFA Delete

### Tải Lên Đối Tượng Thử Nghiệm

1. Tải lên một file thử nghiệm vào bucket (ví dụ: một ảnh JPEG)
2. Việc tải lên hoạt động bình thường

### Kiểm Tra Xóa với Delete Marker

1. Xóa đối tượng đã tải lên từ console
2. Thao tác này tạo delete marker (xóa mềm) - hoạt động không cần MFA

### Kiểm Tra Xóa Vĩnh Viễn (Xóa Version)

1. Điều hướng đến các phiên bản đối tượng
2. Thử xóa vĩnh viễn một phiên bản cụ thể
3. **Kết quả**: Bạn sẽ nhận được thông báo lỗi cho biết MFA Delete đã được kích hoạt
4. Xóa vĩnh viễn yêu cầu sử dụng AWS CLI với xác thực MFA

## Bước 7: Vô Hiệu Hóa MFA Delete

Để vô hiệu hóa MFA Delete, sử dụng lại AWS CLI:

```bash
aws s3api put-bucket-versioning \
  --bucket demo-stephane-mfa-delete-2020 \
  --versioning-configuration Status=Enabled,MFADelete=Disabled \
  --mfa "arn:aws:iam::ACCOUNT-ID:mfa/root-account-mfa-device MFA-CODE" \
  --profile root-mfa-delete-demo
```

Sau khi vô hiệu hóa, bạn có thể xóa vĩnh viễn các phiên bản đối tượng từ console mà không cần MFA.

## Thực Hành Bảo Mật Tốt Nhất

1. **Xóa Root Access Keys**: Sau khi hoàn thành hướng dẫn này, hãy xóa ngay các root access keys bạn đã tạo
   - Vào **IAM** → **Security Credentials**
   - Vô hiệu hóa và xóa các access keys
   
2. **Sử Dụng IAM Users**: Đối với các hoạt động thông thường, luôn sử dụng IAM users với quyền phù hợp thay vì thông tin xác thực root

3. **Bật MFA Delete cho Buckets Quan Trọng**: Cân nhắc bật MFA Delete cho các buckets chứa dữ liệu nhạy cảm hoặc quan trọng

## Lưu Ý Quan Trọng

- MFA Delete chỉ có thể được bật/tắt bằng AWS CLI, không thể thông qua AWS Console
- MFA Delete yêu cầu thông tin xác thực tài khoản root
- Chỉ chủ sở hữu bucket (tài khoản root) mới có thể bật hoặc tắt MFA Delete
- MFA Delete bảo vệ khỏi việc xóa vĩnh viễn các phiên bản đối tượng một cách vô ý
- Xóa mềm (thêm delete markers) không yêu cầu MFA

## Dọn Dẹp

1. Xóa các đối tượng thử nghiệm khỏi bucket
2. Xóa bucket thử nghiệm nếu không còn cần thiết
3. **Quan trọng**: Xóa root access keys từ IAM Security Credentials

## Kết Luận

MFA Delete cung cấp một lớp bảo mật bổ sung cho các S3 buckets của bạn bằng cách yêu cầu xác thực MFA trước khi xóa vĩnh viễn các phiên bản đối tượng. Mặc dù cần quyền truy cập tài khoản root để cấu hình, đây là một tính năng bảo mật có giá trị để bảo vệ dữ liệu quan trọng.

## Script Tham Khảo

Các lệnh được sử dụng trong hướng dẫn này có thể tìm thấy trong: `s3advanced.mfadelete.sh`

---

**Bước Tiếp Theo**: Khám phá các tính năng bảo mật S3 khác như bucket policies, mã hóa và access logging để bảo mật thêm cho các S3 buckets của bạn.




FILE: 73-aws-s3-access-logs.md


# AWS S3 Access Logs (Nhật ký Truy cập S3)

## Tổng quan

S3 Access Logs cung cấp nhật ký kiểm tra đầy đủ về tất cả các yêu cầu được thực hiện đến các S3 bucket của bạn. Tính năng này rất quan trọng cho việc giám sát bảo mật, tuân thủ và hiểu các mẫu truy cập đến tài nguyên S3 của bạn.

## S3 Access Logs là gì?

Cho mục đích kiểm tra, bạn có thể muốn ghi lại tất cả các truy cập được thực hiện vào các S3 bucket của mình. Điều này có nghĩa là bất kỳ yêu cầu nào được thực hiện đến S3 bucket của bạn từ bất kỳ tài khoản nào, dù được ủy quyền hay bị từ chối, đều sẽ được ghi lại dưới dạng file vào một S3 bucket khác.

Dữ liệu được ghi lại sau đó có thể được phân tích bằng các công cụ phân tích dữ liệu như **Amazon Athena**.

## Yêu cầu chính

- **Bucket lưu trữ nhật ký phải ở cùng AWS region** với bucket nguồn
- Bucket lưu trữ nhật ký phải là bucket khác với bucket đang được giám sát

## Cách hoạt động

1. Các yêu cầu được thực hiện đến S3 bucket của bạn
2. Bạn kích hoạt tính năng ghi nhật ký truy cập trên bucket
3. Tất cả các yêu cầu được ghi lại vào bucket lưu trữ nhật ký được chỉ định
4. Nhật ký tuân theo định dạng cụ thể (thông số định dạng chi tiết có sẵn trong tài liệu AWS)

## Cảnh báo quan trọng ⚠️

**Không bao giờ đặt bucket lưu trữ nhật ký giống với bucket bạn đang giám sát.**

Nếu bạn làm điều này, nó sẽ tạo ra một **vòng lặp ghi nhật ký vô hạn**:
- Khi bạn PUT một object vào bucket
- Sự kiện ghi nhật ký tự động tạo ra một mục nhật ký mới
- Mục nhật ký đó lại tạo ra một mục nhật ký khác
- Quá trình này tiếp tục vô hạn
- Bucket của bạn sẽ tăng kích thước theo cấp số nhân
- **Bạn sẽ phải chịu chi phí đáng kể**

### Ví dụ về những gì KHÔNG nên làm:
```
❌ Source Bucket: my-app-bucket
❌ Logging Bucket: my-app-bucket (GIỐNG NHAU - Đừng làm điều này!)
```

### Cấu hình đúng:
```
✅ Source Bucket: my-app-bucket
✅ Logging Bucket: my-app-logs-bucket (Bucket KHÁC NHAU)
```

## Các trường hợp sử dụng

- **Kiểm tra bảo mật**: Theo dõi tất cả các nỗ lực truy cập vào bucket của bạn
- **Yêu cầu tuân thủ**: Duy trì hồ sơ truy cập dữ liệu
- **Phân tích mẫu truy cập**: Hiểu cách S3 bucket của bạn đang được sử dụng
- **Khắc phục sự cố**: Điều tra các lần truy cập trái phép hoặc thất bại
- **Phân tích chi phí**: Xác định các mẫu lưu lượng cao

## Thực hành tốt nhất

1. Luôn sử dụng bucket riêng biệt để lưu trữ nhật ký
2. Thiết lập lifecycle policies trên bucket lưu trữ nhật ký để quản lý thời gian lưu trữ
3. Sử dụng Amazon Athena hoặc các công cụ tương tự để phân tích nhật ký hiệu quả
4. Đảm bảo bucket lưu trữ nhật ký có các kiểm soát truy cập phù hợp
5. Giám sát kích thước bucket lưu trữ nhật ký thường xuyên

## Dịch vụ liên quan

- **Amazon Athena**: Truy vấn và phân tích nhật ký truy cập S3 bằng SQL
- **AWS CloudTrail**: Để ghi nhật ký cấp API của các lệnh gọi dịch vụ AWS
- **Amazon CloudWatch**: Để giám sát và cảnh báo theo thời gian thực

## Tóm tắt

S3 Access Logs là một công cụ mạnh mẽ để duy trì khả năng hiển thị các mẫu truy cập bucket. Bằng cách tuân theo các thực hành tốt nhất và tránh các lỗi phổ biến như vòng lặp ghi nhật ký, bạn có thể giám sát và kiểm tra cơ sở hạ tầng S3 của mình một cách hiệu quả.




FILE: 74-aws-s3-access-logs-hands-on-tutorial.md


# Hướng Dẫn Thực Hành AWS S3 Access Logs

## Tổng Quan

Hướng dẫn này trình bày cách bật và cấu hình S3 Server Access Logging để theo dõi và giám sát quyền truy cập vào các bucket S3 của bạn. Server access logging cung cấp các bản ghi chi tiết về các request được thực hiện đến bucket của bạn, điều này rất quan trọng cho việc kiểm toán bảo mật, phân tích truy cập và khắc phục sự cố.

## Điều Kiện Tiên Quyết

- Tài khoản AWS với quyền S3 phù hợp
- Ít nhất một bucket S3 hiện có để giám sát
- Hiểu biết cơ bản về AWS S3 console

## Hướng Dẫn Từng Bước

### Bước 1: Tạo Bucket Lưu Trữ Logs

Đầu tiên, chúng ta cần tạo một bucket chuyên dụng để lưu trữ các access logs.

1. Điều hướng đến S3 console
2. Nhấp **Create bucket**
3. Nhập tên bucket (ví dụ: `stephane-access-log-v3`)
4. Chọn region ưa thích của bạn
5. Nhấp **Create bucket**

> **Thực Hành Tốt Nhất**: Sử dụng một bucket riêng biệt dành riêng cho logs để giữ dữ liệu có tổ chức và dễ quản lý các chính sách lifecycle hơn.

### Bước 2: Bật Server Access Logging

Bây giờ chúng ta sẽ cấu hình một bucket hiện có để gửi access logs của nó đến logging bucket.

1. Chọn bucket bạn muốn giám sát
2. Vào tab **Properties**
3. Cuộn xuống **Server access logging**
4. Nhấp **Edit**
5. Chọn **Enable**

### Bước 3: Cấu Hình Đích Lưu Trữ Logs

Khi bật server access logging, bạn cần chỉ định nơi các logs sẽ được lưu trữ:

1. **Target bucket**: Chọn logging bucket của bạn (ví dụ: `stephane-access-log-v3`)
2. **Destination region**: Xác minh region (ví dụ: `eu-west-1`)
3. **Bucket prefix** (tùy chọn): Bạn có thể chỉ định prefix như `/logs` để tổ chức các file log, nhưng điều này là tùy chọn
4. **Log object key format**: Chọn từ các định dạng có sẵn:
   - Định dạng mặc định với S3 event time tiêu chuẩn
   - Định dạng thay thế với log file delivery time

Console sẽ hiển thị ví dụ về định dạng log key dựa trên lựa chọn của bạn.

5. Nhấp **Save changes**

> **Lưu Ý**: AWS tự động cập nhật bucket policy trên target logging bucket để cho phép dịch vụ S3 logging ghi các file log.

### Bước 4: Xác Minh Bucket Policy

Sau khi bật logging, điều quan trọng là phải xác minh bucket policy đã được cập nhật chính xác:

1. Điều hướng đến **logging bucket** của bạn
2. Vào tab **Permissions**
3. Cuộn xuống **Bucket policy**
4. Xem lại policy - bây giờ nó sẽ bao gồm quyền cho dịch vụ S3 logging để put objects vào bucket này

### Bước 5: Tạo Hoạt Động

Để kiểm tra chức năng logging, thực hiện một số hoạt động trên bucket được giám sát của bạn:

- Điều hướng qua các objects trong bucket
- Mở files
- Upload files mới (ví dụ: upload một file hình ảnh)
- Bất kỳ thao tác S3 API nào sẽ được ghi log

### Bước 6: Xem Access Logs

Access logs không được gửi ngay lập tức. Thường mất một khoảng thời gian (có thể vài giờ) để logs xuất hiện trong logging bucket của bạn.

1. Điều hướng đến **logging bucket** của bạn
2. Refresh bucket view
3. Bạn sẽ thấy nhiều file log (objects) được tạo tự động
4. Nhấp vào bất kỳ file log nào để xem nội dung của nó

## Hiểu Nội Dung Log

Mỗi file log chứa thông tin chi tiết về các request được thực hiện đến bucket của bạn:

- **API calls**: Các thao tác S3 nào đã được thực hiện
- **Success rate**: Request thành công hay thất bại
- **Requester information**: Ai đã truy cập bucket
- **Bucket details**: Bucket nào đã được truy cập
- **Timestamp**: Khi nào truy cập xảy ra
- **Additional metadata**: Tham số request, mã response, v.v.

> **Lưu Ý**: Các file log có thể khó đọc ở định dạng raw. Hãy xem xét sử dụng AWS Athena hoặc các công cụ phân tích log khác để phân tích và truy vấn dễ dàng hơn.

## Những Điểm Chính

- Server access logging cung cấp audit trails chi tiết cho S3 bucket access
- Luôn sử dụng một bucket riêng để lưu trữ logs
- Log delivery có độ trễ (thường là vài giờ)
- Bucket policies được cấu hình tự động khi bạn bật logging
- Các file log chứa thông tin toàn diện về tất cả các thao tác bucket

## Thực Hành Tốt Nhất

1. **Bật logging cho tất cả production buckets** để bảo mật và tuân thủ
2. **Sử dụng lifecycle policies** trên logging bucket của bạn để lưu trữ hoặc xóa logs cũ
3. **Giám sát chi phí lưu trữ logging bucket** vì logs có thể tích lũy nhanh chóng
4. **Tích hợp với các công cụ phân tích** như AWS Athena để truy vấn log dễ dàng hơn
5. **Bảo mật logging bucket của bạn** với các kiểm soát truy cập phù hợp

## Các Bước Tiếp Theo

- Khám phá tích hợp CloudWatch Logs để giám sát real-time
- Thiết lập phân tích log tự động với AWS Athena
- Cấu hình cảnh báo dựa trên các mẫu truy cập cụ thể
- Xem lại AWS CloudTrail để ghi log ở cấp độ API bổ sung

---

Hướng dẫn này bao gồm các bước thiết yếu để triển khai S3 Server Access Logging. Để biết thêm các cấu hình nâng cao và các trường hợp sử dụng, hãy tham khảo tài liệu AWS S3.




FILE: 75-amazon-s3-pre-signed-urls.md


# Amazon S3 Pre-Signed URLs (URL Đã Ký Trước)

## Tổng Quan

Amazon S3 Pre-Signed URLs là các URL tạm thời cung cấp quyền truy cập an toàn vào các đối tượng S3 riêng tư mà không cần phải công khai chúng. Các URL này có thể được tạo bằng S3 console, AWS CLI hoặc SDK.

## Tính Năng Chính

### Phương Thức Tạo URL
- **S3 Console**: Tạo URL với thời gian hết hạn lên đến 12 giờ
- **AWS CLI/SDK**: Tạo URL với thời gian hết hạn lên đến 168 giờ (7 ngày)

### Kế Thừa Quyền Truy Cập
Khi bạn tạo một pre-signed URL, người dùng nhận được URL đó sẽ kế thừa quyền của người đã tạo ra URL. Điều này áp dụng cho cả thao tác GET (tải xuống) và PUT (tải lên).

## Cách Hoạt Động Của Pre-Signed URLs

1. **Tạo URL**: Với vai trò chủ sở hữu bucket hoặc người dùng được ủy quyền, bạn tạo một pre-signed URL cho một file cụ thể trong S3 bucket riêng tư của mình
2. **Nhúng Thông Tin Xác Thực**: URL mang theo thông tin xác thực của bạn về quyền truy cập file đó
3. **Phân Phối URL**: Bạn gửi URL này cho người dùng mục tiêu cần quyền truy cập tạm thời
4. **Truy Cập File**: Người dùng truy cập file bằng pre-signed URL
5. **Truyền Tải An Toàn**: File được lấy từ S3 bucket trong khi vẫn duy trì tính riêng tư của bucket

## Các Trường Hợp Sử Dụng

Pre-signed URLs thường được sử dụng để cung cấp quyền truy cập tạm thời vào các file cụ thể cho cả việc tải xuống và tải lên:

### Các Tình Huống Tải Xuống
- **Truy Cập Nội Dung Premium**: Chỉ cho phép người dùng đã đăng nhập tải xuống video premium từ S3 bucket của bạn
- **Phân Phối File Động**: Cho phép danh sách người dùng thay đổi liên tục tải xuống file bằng cách tạo URL một cách động
- **Chia Sẻ File Tạm Thời**: Cung cấp quyền truy cập tạm thời vào các file cụ thể mà không ảnh hưởng đến bảo mật bucket

### Các Tình Huống Tải Lên
- **Quyền Tải Lên Tạm Thời**: Cho phép người dùng tạm thời tải file lên một vị trí cụ thể trong S3 bucket của bạn trong khi vẫn giữ bucket ở chế độ riêng tư

## Lợi Ích Về Bảo Mật

- Duy trì tính riêng tư của S3 bucket
- Cung cấp quyền truy cập có giới hạn thời gian
- Không cần phải công khai các file
- Kiểm soát chi tiết quyền truy cập file
- Tự động hết hạn quyền truy cập

## Tóm Tắt

Amazon S3 Pre-Signed URLs là một tính năng mạnh mẽ để cung cấp quyền truy cập an toàn, tạm thời vào các đối tượng S3 riêng tư. Chúng cho phép bạn chia sẻ file mà không làm tổn hại đến tình trạng bảo mật của bucket, khiến chúng trở nên lý tưởng cho các tình huống phân phối và tải lên file có kiểm soát.




FILE: 76-aws-s3-access-points-overview.md


# Tổng Quan về AWS S3 Access Points

## Giới Thiệu

Amazon S3 Access Points đơn giản hóa việc quản lý truy cập dữ liệu cho các tập dữ liệu được chia sẻ trong Amazon S3. Tài liệu này giải thích cách hoạt động của access points và lợi ích của chúng về mặt bảo mật và khả năng mở rộng.

## Thách Thức

Khi làm việc với một S3 bucket chứa lượng lớn dữ liệu thuộc nhiều danh mục khác nhau (ví dụ: dữ liệu tài chính, dữ liệu bán hàng), việc quản lý quyền truy cập cho các người dùng hoặc nhóm khác nhau có thể trở nên phức tạp. Phương pháp truyền thống sử dụng một bucket policy duy nhất có thể trở nên:

- Ngày càng phức tạp khi thêm nhiều người dùng
- Khó quản lý khi dữ liệu tăng trưởng
- Không thể quản lý được theo thời gian với nhiều mẫu truy cập

## Giải Pháp: S3 Access Points

S3 Access Points cung cấp cách thức có khả năng mở rộng để quản lý truy cập đến các tập dữ liệu được chia sẻ bằng cách tạo các điểm truy cập chuyên dụng cho các trường hợp sử dụng khác nhau.

### Kiến Trúc Ví Dụ

Xét một S3 bucket với dữ liệu tài chính và bán hàng:

#### 1. Finance Access Point (Điểm Truy Cập Tài Chính)
- **Mục đích**: Truy cập chuyên dụng đến dữ liệu tài chính
- **Cấu hình**: Policy của access point cấp quyền đọc/ghi cho prefix tài chính
- **Người dùng**: Thành viên nhóm tài chính chỉ có thể truy cập dữ liệu liên quan đến tài chính

#### 2. Sales Access Point (Điểm Truy Cập Bán Hàng)
- **Mục đích**: Truy cập chuyên dụng đến dữ liệu bán hàng
- **Cấu hình**: Policy của access point cấp quyền đọc/ghi cho prefix bán hàng
- **Người dùng**: Thành viên nhóm bán hàng chỉ có thể truy cập dữ liệu liên quan đến bán hàng

#### 3. Analytics Access Point (Điểm Truy Cập Phân Tích)
- **Mục đích**: Quyền truy cập chỉ đọc cho cả dữ liệu tài chính và bán hàng
- **Cấu hình**: Policy của access point cấp quyền chỉ đọc cho cả hai prefix
- **Người dùng**: Nhóm phân tích có thể đọc dữ liệu từ nhiều nguồn mà không có quyền ghi

## Lợi Ích Chính

### 1. Quản Lý Bảo Mật Đơn Giản Hóa
- Các policy bảo mật được phân phối qua các access points thay vì một bucket policy phức tạp duy nhất
- Mỗi access point có policy riêng chuyên dụng
- Bucket policy chính của S3 vẫn giữ đơn giản

### 2. Khả Năng Mở Rộng
- Dễ dàng thêm access points mới khi nhu cầu tổ chức tăng trưởng
- Mỗi access point độc lập và không ảnh hưởng đến các access point khác
- Không cần thường xuyên sửa đổi bucket policy trung tâm

### 3. Mẫu Truy Cập Rõ Ràng
- Mỗi access point định nghĩa một cách cụ thể để truy cập S3 bucket
- Người dùng với quyền IAM phù hợp chỉ có thể truy cập access points được chỉ định của họ
- Quyền truy cập được phân tách logic theo trường hợp sử dụng

## Tính Năng của Access Point

### Tên DNS
- Mỗi access point có tên DNS duy nhất riêng
- Ứng dụng kết nối trực tiếp đến DNS của access point

### Tùy Chọn Kết Nối

#### Internet Origin (Nguồn Internet)
- Access point có thể truy cập qua internet
- Truy cập công khai tiêu chuẩn với xác thực IAM

#### VPC Origin (Nguồn VPC)
- Access point có thể truy cập riêng tư từ bên trong VPC
- Lưu lượng không đi qua internet công cộng

## Cấu Hình VPC Origin

### Kiến Trúc
Khi cấu hình S3 access point với VPC origin cho truy cập riêng tư:

1. **EC2 Instance (hoặc tài nguyên khác)** trong VPC cần truy cập riêng tư đến S3
2. **VPC Endpoint** phải được tạo để kích hoạt kết nối riêng tư
3. **VPC Access Point** cung cấp điểm vào riêng tư đến S3 bucket

### Các Lớp Bảo Mật

#### VPC Endpoint Policy
- Phải cho phép truy cập đến cả target buckets và access points
- Kiểm soát tài nguyên nào trong VPC có thể truy cập access point

#### Access Point Policy
- Định nghĩa quyền cho access point cụ thể
- Tương tự như bucket policy nhưng được giới hạn cho access point

#### S3 Bucket Policy
- Vẫn giữ đơn giản và ủy quyền kiểm soát truy cập chi tiết cho access points
- Mức độ bảo mật cơ bản cho bucket

### Lợi Ích của VPC Origin
- Dữ liệu không bao giờ rời khỏi mạng AWS
- Tăng cường bảo mật cho các workload nhạy cảm
- Giảm chi phí truyền dữ liệu
- Độ trễ thấp hơn cho các ứng dụng dựa trên VPC

## Tóm Tắt

**S3 Access Points** đơn giản hóa quản lý bảo mật cho S3 buckets bằng cách:

- Tạo các access points chuyên dụng, được đặt tên cho các trường hợp sử dụng khác nhau
- Cho phép mỗi access point có policy riêng (tương tự bucket policies)
- Cung cấp tên DNS duy nhất cho mỗi access point
- Hỗ trợ cả internet và VPC origins cho kết nối linh hoạt
- Cho phép quản lý bảo mật ở quy mô lớn mà không cần bucket policies phức tạp

Access points đặc biệt hữu ích cho:
- Các tổ chức lớn với nhiều nhóm truy cập dữ liệu được chia sẻ
- Ứng dụng yêu cầu các mức độ truy cập khác nhau (chỉ đọc vs. đọc-ghi)
- Các kịch bản yêu cầu truy cập S3 riêng tư dựa trên VPC
- Môi trường mà bảo mật và tuân thủ yêu cầu các mẫu truy cập được phân tách

## Thực Hành Tốt Nhất

1. **Sử dụng tên mô tả** cho access points phản ánh mục đích của chúng
2. **Tạo access points riêng biệt** cho các nhóm hoặc ứng dụng khác nhau
3. **Tận dụng VPC origins** cho dữ liệu nhạy cảm cần giữ riêng tư
4. **Giữ bucket policies đơn giản** và ủy quyền các quyền chi tiết cho access points
5. **Ghi chép các mẫu truy cập** cho mỗi access point để duy trì sự rõ ràng

---

*Tài liệu này bao gồm các khái niệm cơ bản về AWS S3 Access Points và vai trò của chúng trong quản lý truy cập an toàn, có khả năng mở rộng đến dữ liệu S3.*




FILE: 77-aws-s3-object-lambda-overview.md


# Tổng Quan AWS S3 Object Lambda

## Giới Thiệu

S3 Object Lambda là một trường hợp sử dụng nâng cao của S3 access points, cho phép bạn chỉnh sửa các đối tượng ngay trước khi chúng được truy xuất bởi ứng dụng gọi. Thay vì nhân bản các bucket để duy trì nhiều phiên bản khác nhau của mỗi đối tượng, S3 Object Lambda cung cấp một giải pháp hiệu quả hơn.

## Cách Hoạt Động của S3 Object Lambda

### Kiến Trúc Cơ Bản

Hệ thống bao gồm nhiều thành phần hoạt động cùng nhau:

1. **S3 Bucket**: Bucket nguồn chứa dữ liệu gốc của bạn
2. **S3 Access Point**: Điểm kết nối đến S3 bucket
3. **Lambda Function**: Mã code chuyển đổi dữ liệu trong quá trình truy xuất
4. **S3 Object Lambda Access Point**: Điểm cuối mà các ứng dụng sử dụng để truy cập dữ liệu đã được chuyển đổi

### Ví Dụ Trường Hợp Sử Dụng: Thương Mại Điện Tử với Nhiều Ứng Dụng

#### Truy Cập Dữ Liệu Gốc
Một ứng dụng thương mại điện tử sở hữu dữ liệu trong S3 bucket và có thể truy cập trực tiếp để đưa vào và lấy ra các đối tượng gốc.

#### Dữ Liệu Đã Biên Tập cho Phân Tích
Ứng dụng phân tích cần truy cập vào các đối tượng đã được biên tập (đã xóa bớt một số dữ liệu). Thay vì tạo một S3 bucket mới:

1. Tạo một S3 access point trên S3 bucket
2. Kết nối nó với một Lambda function để biên tập dữ liệu
3. Tạo một S3 Object Lambda access point trên Lambda function
4. Ứng dụng phân tích truy cập Object Lambda access point này
5. Lambda function truy xuất dữ liệu từ S3 bucket và biên tập nó
6. Ứng dụng phân tích nhận được đối tượng đã biên tập từ cùng một S3 bucket

#### Dữ Liệu Được Làm Giàu cho Marketing
Ứng dụng marketing cần các đối tượng được làm giàu với thông tin bổ sung từ cơ sở dữ liệu khách hàng thân thiết:

1. Tạo một Lambda function khác để làm giàu dữ liệu bằng cách tra cứu từ cơ sở dữ liệu khách hàng thân thiết
2. Tạo một S3 Object Lambda access point khác trên Lambda function này
3. Ứng dụng marketing truy cập access point này để nhận các đối tượng đã được làm giàu

### Lợi Ích Chính

- **Nguồn Dữ Liệu Duy Nhất**: Chỉ cần một S3 bucket
- **Nhiều Góc Nhìn**: Tạo các access point khác nhau và cấu hình Object Lambda để chỉnh sửa dữ liệu theo nhu cầu
- **Chuyển Đổi Tức Thì**: Dữ liệu được chuyển đổi trong quá trình truy xuất, không cần lưu trữ riêng biệt

## Các Trường Hợp Sử Dụng

### 1. Biên Tập Dữ Liệu PII
Xóa bỏ thông tin nhận dạng cá nhân (PII) cho:
- Các ứng dụng phân tích
- Môi trường không phải sản xuất
- Yêu cầu tuân thủ

### 2. Chuyển Đổi Định Dạng Dữ Liệu
Chuyển đổi định dạng dữ liệu tức thì:
- Chuyển đổi XML sang JSON
- Chuyển đổi CSV sang JSON
- Bất kỳ chuyển đổi dữ liệu tùy chỉnh nào

### 3. Xử Lý Hình Ảnh Động
Xử lý hình ảnh dựa trên người dùng yêu cầu:
- Thay đổi kích thước hình ảnh tức thì
- Thêm watermark cụ thể cho người dùng yêu cầu đối tượng
- Áp dụng các chỉnh sửa hình ảnh theo người dùng

### 4. Làm Giàu Dữ Liệu
Nâng cao dữ liệu bằng cách kết hợp với các nguồn khác:
- Thêm thông tin khách hàng từ cơ sở dữ liệu
- Bổ sung metadata từ hệ thống bên ngoài
- Hợp nhất dữ liệu từ nhiều nguồn

## Kết Luận

S3 Object Lambda là một tính năng mạnh mẽ cho phép bạn chuyển đổi dữ liệu S3 theo yêu cầu mà không cần nhân bản lưu trữ hoặc duy trì nhiều phiên bản của các đối tượng. Bằng cách tận dụng các Lambda function và access point, bạn có thể cung cấp các góc nhìn tùy chỉnh về dữ liệu của mình cho các ứng dụng khác nhau một cách hiệu quả.




FILE: 78-aws-cloudfront-overview.md


# Tổng Quan về AWS CloudFront

## Giới Thiệu về CloudFront

CloudFront là dịch vụ **Content Delivery Network (CDN)** được cung cấp bởi AWS. Khi bạn thấy CDN được đề cập trong các kỳ thi hoặc tài liệu AWS, hãy nghĩ ngay đến CloudFront.

## Lợi Ích Chính

### Cải Thiện Hiệu Suất
- **Cải thiện hiệu suất đọc** bằng cách lưu trữ nội dung website tại các edge location khác nhau
- Nội dung được lưu trữ toàn cầu đảm bảo **độ trễ thấp hơn** cho người dùng trên toàn thế giới
- **Nâng cao trải nghiệm người dùng** đáng kể

### Hạ Tầng Toàn Cầu
- Bao gồm **hàng trăm điểm hiện diện** trên toàn cầu
- Bao gồm các **edge location** và **regional edge cache** phân bổ trên toàn thế giới
- Khoảng **216 điểm hiện diện** trên toàn cầu

### Tính Năng Bảo Mật
- Cung cấp **bảo vệ DDoS** thông qua hạ tầng phân tán toàn cầu
- Tích hợp với **AWS Shield** để bảo vệ nâng cao chống lại các mối đe dọa
- Hoạt động với **Web Application Firewall (WAF)** để có thêm các lớp bảo mật

## Cách CloudFront Hoạt Động

### Ví Dụ về Phân Phối Nội Dung
1. Một S3 bucket với website được tạo ở **Úc**
2. Người dùng ở **Mỹ** yêu cầu nội dung từ edge location Mỹ gần nhất
3. CloudFront lấy nội dung từ Úc và lưu trữ tại edge location Mỹ
4. Các người dùng tiếp theo ở Mỹ nhận nội dung trực tiếp từ edge location (không cần lấy từ Úc nữa)
5. Người dùng ở **Trung Quốc** tương tự kết nối đến các điểm hiện diện của Trung Quốc, với nội dung được lưu trữ cục bộ sau lần yêu cầu đầu tiên

## Các Nguồn Gốc (Origins) của CloudFront

CloudFront hỗ trợ nhiều loại nguồn gốc (backend):

### 1. Amazon S3 Bucket
- Được sử dụng để **phân phối và lưu trữ các tệp** tại edge
- Hỗ trợ **tải tệp lên** trực tiếp vào S3 thông qua CloudFront
- Được bảo mật bằng **Origin Access Control (OAC)**
- S3 bucket policy phải được cấu hình để cho phép CloudFront truy cập

### 2. VPC Origin
- Kết nối đến các ứng dụng được lưu trữ trong **mạng AWS riêng tư** của bạn
- Các tài nguyên được hỗ trợ:
  - Private Application Load Balancer
  - Private Network Load Balancer
  - Private EC2 instances

### 3. Custom HTTP Origin
- Bất kỳ backend HTTP công khai nào
- **S3 static website** (bucket phải được kích hoạt làm static website)
- **Public Load Balancer**
- Bất kỳ HTTP server nào khác

## Luồng Yêu Cầu CloudFront

1. **Client gửi HTTP request** đến edge location gần nhất
2. **Edge location kiểm tra bộ nhớ cache cục bộ**
   - Nếu nội dung tồn tại trong cache → Phục vụ trực tiếp từ cache
   - Nếu nội dung không tồn tại → Lấy từ origin
3. **Nội dung được lấy từ origin** được lưu trữ tại edge location
4. **Các yêu cầu tiếp theo** cho cùng nội dung được phục vụ từ cache

### Ví Dụ: S3 làm Origin
- S3 bucket làm origin trong một AWS region cụ thể
- Các edge location trên toàn thế giới (ví dụ: Los Angeles, São Paulo) lưu trữ nội dung
- Yêu cầu đầu tiên kích hoạt việc lấy từ origin qua mạng AWS riêng tư
- Các yêu cầu tiếp theo được phục vụ trực tiếp từ edge location khu vực
- S3 bucket được bảo mật với Origin Access Control và bucket policies

## CloudFront vs S3 Cross-Region Replication

### CloudFront (CDN)
- Sử dụng **Global Edge Network** (~216 điểm hiện diện)
- Các tệp được lưu trữ tại edge location (thường trong ~24 giờ)
- **Tốt nhất cho:** Nội dung tĩnh cần khả năng truy cập toàn cầu
- **Trường hợp sử dụng:** Nội dung không thay đổi thường xuyên và cần phân phối toàn cầu

### S3 Cross-Region Replication
- Phải được **cấu hình cho từng region** (không tự động phủ sóng toàn cầu)
- Các tệp được cập nhật **gần như thời gian thực** (không có caching)
- Sao chép **chỉ đọc**
- **Tốt nhất cho:** Nội dung động yêu cầu độ trễ thấp ở các region cụ thể
- **Trường hợp sử dụng:** Nội dung thay đổi thường xuyên và cần khả năng truy cập ở các region được chọn

## Tóm Tắt Sự Khác Biệt Chính

| Tính Năng | CloudFront | S3 Cross-Region Replication |
|-----------|-----------|----------------------------|
| **Phân Phối** | Toàn cầu (216+ địa điểm) | Yêu cầu thiết lập từng region |
| **Phương Thức Cập Nhật** | Cached (dựa trên TTL) | Gần như thời gian thực |
| **Loại Nội Dung** | Nội dung tĩnh | Nội dung động |
| **Độ Trễ** | Thấp trên toàn cầu | Thấp ở các region được cấu hình |
| **Mục Đích** | Cache và phân phối | Sao chép toàn bộ bucket |

## Kết Luận

CloudFront là giải pháp CDN mạnh mẽ của AWS được thiết kế để:
- Phân phối nội dung toàn cầu với độ trễ thấp
- Cung cấp bảo mật thông qua bảo vệ DDoS
- Tích hợp liền mạch với S3, EC2 và load balancers
- Cải thiện hiệu suất ứng dụng thông qua caching thông minh

Hiểu rõ sự khác biệt giữa CloudFront và S3 Cross-Region Replication là rất quan trọng để thiết kế kiến trúc phù hợp dựa trên nhu cầu phân phối nội dung của bạn.




FILE: 79-aws-cloudfront-s3-hands-on-tutorial.md


# Hướng Dẫn Thực Hành AWS CloudFront với S3

## Tổng Quan

Hướng dẫn này sẽ giúp bạn thiết lập Amazon CloudFront như một Mạng Phân Phối Nội Dung (CDN) để phục vụ các tệp từ một Amazon S3 bucket riêng tư. Bạn sẽ học cách phân phối nội dung toàn cầu mà không cần công khai các đối tượng S3 của mình.

## Yêu Cầu Trước Khi Bắt Đầu

- Tài khoản AWS có quyền truy cập vào dịch vụ S3 và CloudFront
- Hiểu biết cơ bản về S3 buckets và objects
- Các tệp mẫu để tải lên (ví dụ: hình ảnh và tệp HTML)

## Phần 1: Tạo và Cấu Hình S3 Bucket

### Bước 1: Tạo S3 Bucket

1. Truy cập vào bảng điều khiển Amazon S3
2. Nhấp vào **Create Bucket** (Tạo Bucket)
3. Nhập tên bucket (ví dụ: `demo-CloudFront-Stephan-v4`)
4. Cuộn xuống và giữ nguyên tất cả các cài đặt mặc định
5. Nhấp vào **Create Bucket** (Tạo Bucket)

### Bước 2: Tải Tệp Lên Bucket

1. Mở bucket vừa tạo
2. Nhấp vào **Add files** (Thêm tệp)
3. Chọn các tệp để tải lên:
   - `beach.jpg`
   - `coffee.jpg`
   - `index.html`
4. Nhấp vào **Upload** (Tải lên)
5. Đợi quá trình tải lên hoàn tất

### Bước 3: Hiểu Về Cách Truy Cập Đối Tượng S3

Sau khi tải lên, bạn sẽ nhận thấy có hai cách để truy cập các đối tượng:

1. **Object URL (URL Đối Tượng)**: URL trực tiếp đến đối tượng
   - Khi cố gắng truy cập sẽ nhận được lỗi **Access Denied** (Từ Chối Truy Cập) vì các đối tượng không công khai
   
2. **Pre-signed URL (URL Đã Ký Trước)**: URL xác thực tạm thời
   - Nhấp vào **Open** (Mở) trên một đối tượng để tạo pre-signed URL
   - Điều này cho phép truy cập tạm thời vào các đối tượng riêng tư
   - Tuy nhiên, các tài nguyên được tham chiếu (như hình ảnh trong HTML) vẫn có thể không truy cập được nếu chúng không công khai

**Thách Thức**: Chúng ta muốn phục vụ các tệp này mà không cần công khai chúng. Đây là lúc CloudFront phát huy tác dụng.

## Phần 2: Thiết Lập CloudFront Distribution

### Bước 1: Mở Bảng Điều Khiển CloudFront

1. Truy cập vào bảng điều khiển AWS CloudFront
2. Đóng popup thông tin về giá nếu nó xuất hiện

### Bước 2: Chọn Gói CloudFront

CloudFront cung cấp nhiều gói giá khác nhau:

#### Gói Miễn Phí (Được khuyến nghị cho hướng dẫn này)
Bao gồm:
- Số lượng yêu cầu và dung lượng truyền tải dữ liệu đủ mỗi tháng
- Bảo vệ DNS luôn hoạt động
- Chặn lưu lượng theo địa lý
- CDN toàn cầu
- Dịch vụ DNS
- Chứng chỉ TLS miễn phí

#### Gói Doanh Nghiệp
Tính năng bổ sung:
- Edge key-value store
- Bảo vệ DDoS nâng cao
- Cam kết SLA về thời gian hoạt động
- Bảo vệ WordPress
- Hỗ trợ VPC origin (kết nối EC2/ALB riêng tư)

#### Trả Theo Mức Sử Dụng
- Trả tiền dựa trên lưu lượng thực tế
- Chi phí bổ sung cho các tính năng cao cấp

**Đối với hướng dẫn này, hãy chọn Gói Miễn Phí.**

### Bước 3: Tạo Distribution

1. Nhấp vào **Create CloudFront distribution** (Tạo CloudFront distribution)
2. Nhập tên distribution (ví dụ: `demo-new-CloudFront`)
3. Chọn tùy chọn **Single site or app** (Trang web hoặc ứng dụng đơn lẻ)
4. (Tùy chọn) Bạn có thể thêm tên miền tùy chỉnh và cấp phát chứng chỉ TLS
5. Nhấp vào **Next** (Tiếp theo)

### Bước 4: Cấu Hình Origin Settings

1. **Origin Type (Loại Origin)**: Chọn **Amazon S3**
   
   Các tùy chọn có sẵn:
   - Amazon S3
   - Elastic Load Balancer
   - API Gateway
   - Elemental Media Package
   - Các origin tùy chỉnh khác
   - VPC origin (chỉ dành cho gói Doanh nghiệp - cho EC2/ALB riêng tư)

2. **Duyệt và chọn S3 bucket của bạn**: `demo-CloudFront-stephane-v4`

3. **S3 Bucket Access (Quyền Truy Cập S3 Bucket)**: 
   - Bật **Private S3 bucket access** (Quyền truy cập S3 bucket riêng tư)
   - Chọn **Recommended origin settings** (Cài đặt origin được khuyến nghị)
   
4. **Cache Settings (Cài Đặt Bộ Nhớ Đệm)**: 
   - Chọn **Recommended cache settings** (Cài đặt bộ nhớ đệm được khuyến nghị) cho nội dung S3

### Bước 5: Cài Đặt Bảo Mật (Tùy Chọn)

1. **Web Application Firewall (WAF)**: 
   - Không cần thiết cho hướng dẫn này
   - Bảo vệ Layer 7 có sẵn với gói Doanh nghiệp

2. Bỏ qua cấu hình WAF và nhấp vào **Next** (Tiếp theo)

### Bước 6: Xem Lại và Tạo

1. Xem lại tất cả các cài đặt
2. Xác nhận bạn đang ở **Gói Miễn Phí**
3. Nhấp vào **Create distribution** (Tạo distribution)

## Phần 3: Hiểu Về Bucket Policy

### Cấu Hình Tự Động

Sau khi CloudFront distribution được tạo:

1. Quay lại S3 bucket của bạn
2. Vào tab **Permissions** (Quyền hạn)
3. Kiểm tra **Bucket policy** (Chính sách bucket)

Bạn sẽ nhận thấy rằng AWS đã tự động thêm một bucket policy cho phép CloudFront truy cập vào S3 bucket riêng tư của bạn.

**Ví Dụ Bucket Policy**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "cloudfront.amazonaws.com"
      },
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::demo-CloudFront-Stephan-v4/*",
      "Condition": {
        "StringEquals": {
          "AWS:SourceArn": "arn:aws:cloudfront::ACCOUNT-ID:distribution/DISTRIBUTION-ID"
        }
      }
    }
  ]
}
```

Chính sách này đảm bảo rằng chỉ CloudFront distribution của bạn mới có thể truy cập các đối tượng trong bucket trong khi vẫn giữ chúng riêng tư khỏi internet công cộng.

## Phần 4: Kiểm Tra CloudFront Distribution

### Bước 1: Truy Cập CloudFront Domain

1. Trong bảng điều khiển CloudFront, tìm distribution của bạn
2. Sao chép **Domain name** (Tên miền) (ví dụ: `d1234abcd.cloudfront.net`)
3. Mở một tab trình duyệt mới và dán tên miền
4. Nhấn Enter

Ban đầu bạn sẽ thấy lỗi **Access Denied** (Từ Chối Truy Cập) - điều này là bình thường vì bạn chưa chỉ định đường dẫn tệp.

### Bước 2: Truy Cập Các Tệp Riêng Lẻ

Thêm đường dẫn tệp cụ thể vào CloudFront domain:

**Hình Ảnh Coffee**:
```
https://d1234abcd.cloudfront.net/coffee.jpg
```
✅ Hình ảnh tải thành công!

**Hình Ảnh Beach**:
```
https://d1234abcd.cloudfront.net/beach.jpeg
```
✅ Hình ảnh tải thành công!

**Trang HTML**:
```
https://d1234abcd.cloudfront.net/index.html
```
✅ Trang tải với tất cả hình ảnh được tham chiếu!

### Bước 3: Kiểm Tra Hiệu Suất Bộ Nhớ Đệm CDN

1. Truy cập lại hình ảnh beach:
   ```
   https://d1234abcd.cloudfront.net/beach.jpeg
   ```
   
2. Chú ý **tốc độ tải gần như tức thì** - điều này là do hình ảnh hiện đã được lưu trong bộ nhớ đệm tại các vị trí edge của CloudFront

3. Làm mới nhiều lần để trải nghiệm lợi ích về tốc độ

## Các Lợi Ích Chính Được Chứng Minh

### Bảo Mật
- ✅ Các đối tượng S3 vẫn **riêng tư**
- ✅ Quyền truy cập được kiểm soát thông qua CloudFront
- ✅ Không có URL công khai đến các đối tượng S3

### Hiệu Suất
- ✅ **Nội dung được lưu trong bộ nhớ đệm** tại các vị trí edge trên toàn thế giới
- ✅ **Giảm độ trễ** cho người dùng toàn cầu
- ✅ **Thời gian tải nhanh hơn** trong các yêu cầu tiếp theo

### Hiệu Quả Chi Phí
- ✅ Gói miễn phí có sẵn cho mức sử dụng vừa phải
- ✅ Giảm chi phí truyền dữ liệu từ S3
- ✅ Giảm tải lưu lượng từ máy chủ gốc

## Tóm Tắt

Trong hướng dẫn này, bạn đã học được cách:

1. ✅ Tạo S3 bucket và tải tệp lên
2. ✅ Hiểu các phương pháp truy cập đối tượng S3 (Object URL vs Pre-signed URL)
3. ✅ Thiết lập CloudFront distribution với gói Miễn phí
4. ✅ Cấu hình S3 làm CloudFront origin với quyền truy cập riêng tư
5. ✅ Hiểu về các bucket policy được tạo tự động
6. ✅ Kiểm tra phân phối nội dung thông qua CloudFront
7. ✅ Trải nghiệm lợi ích bộ nhớ đệm của CDN

## Các Bước Tiếp Theo

Hãy cân nhắc khám phá:
- Tên miền tùy chỉnh với chứng chỉ SSL/TLS
- CloudFront behaviors và cache policies
- Origin access control (OAC) vs Origin access identity (OAI)
- CloudFront Functions và Lambda@Edge
- Invalidation và quản lý bộ nhớ đệm
- CloudFront security headers và các hạn chế

## Tài Nguyên Bổ Sung

- [Tài Liệu AWS CloudFront](https://docs.aws.amazon.com/cloudfront/)
- [Phương Pháp Hay Nhất Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/best-practices.html)
- [Giá CloudFront](https://aws.amazon.com/cloudfront/pricing/)




FILE: 8-amazon-elasticache-overview.md


# Tổng Quan về Amazon ElastiCache

## Giới Thiệu

Amazon ElastiCache là dịch vụ caching được quản lý giúp bạn triển khai Redis hoặc Memcached một cách dễ dàng. Tương tự như Amazon RDS cung cấp các cơ sở dữ liệu quan hệ được quản lý, ElastiCache cung cấp các công nghệ cache được quản lý.

## Cache là gì?

Cache là **cơ sở dữ liệu trong bộ nhớ (in-memory databases)** với các đặc điểm sau:
- **Hiệu suất cao**
- **Độ trễ thấp**
- Giảm tải cho cơ sở dữ liệu đối với các workload đọc dữ liệu nhiều

### Lợi Ích của ElastiCache

1. **Giảm Tải Cơ Sở Dữ Liệu**: Các truy vấn phổ biến được lưu trong cache, giảm số lần truy vấn trực tiếp vào database
2. **Ứng Dụng Stateless**: Lưu trữ trạng thái ứng dụng trong ElastiCache để làm cho ứng dụng không có trạng thái
3. **Dịch Vụ Được Quản Lý**: AWS xử lý:
   - Bảo trì hệ điều hành
   - Vá lỗi (Patching)
   - Tối ưu hóa
   - Thiết lập và cấu hình
   - Giám sát
   - Khôi phục khi lỗi
   - Sao lưu

### Lưu Ý Quan Trọng

⚠️ **Triển khai yêu cầu thay đổi mã nguồn ứng dụng đáng kể**. Đây không phải là tính năng "bật lên và chạy" đơn giản. Ứng dụng của bạn phải được sửa đổi để truy vấn cache trước hoặc sau khi truy vấn cơ sở dữ liệu.

## Các Kiến Trúc ElastiCache

### 1. Mô Hình Cache-Aside (Lazy Loading)

```
Ứng Dụng → ElastiCache → Cơ Sở Dữ Liệu RDS
```

**Cách hoạt động:**

1. Ứng dụng truy vấn ElastiCache trước
2. **Cache Hit**: Dữ liệu có trong ElastiCache → Trả về dữ liệu ngay lập tức (tiết kiệm một lần truy vấn database)
3. **Cache Miss**: Dữ liệu không có trong cache → Lấy từ cơ sở dữ liệu RDS
4. Ghi dữ liệu đã lấy vào cache cho các truy vấn trong tương lai
5. Giảm tải cho cơ sở dữ liệu RDS

**Lưu Ý Quan Trọng**: Cần có chiến lược invalidation (vô hiệu hóa) cache để đảm bảo chỉ dữ liệu hiện tại được lưu trong cache. Đây là một trong những thách thức chính khi sử dụng công nghệ caching.

### 2. Mô Hình Session Store

**Mục đích**: Làm cho ứng dụng không có trạng thái (stateless)

**Cách hoạt động:**

1. Người dùng đăng nhập vào ứng dụng
2. Ứng dụng ghi dữ liệu session vào ElastiCache
3. Người dùng được chuyển hướng đến instance ứng dụng khác
4. Instance mới lấy dữ liệu session từ ElastiCache
5. Người dùng vẫn đăng nhập mà không cần xác thực lại

Mô hình này cho phép mở rộng theo chiều ngang trong khi vẫn duy trì session người dùng trên nhiều instance ứng dụng.

## So Sánh Redis và Memcached

### Tính Năng của Redis

- ✅ **Multi-Availability Zone** với tự động chuyển đổi dự phòng (auto-failover)
- ✅ **Read Replicas** để mở rộng khả năng đọc và tính sẵn sàng cao
- ✅ **Bền Vững Dữ Liệu** sử dụng AOF (Append-Only File) persistence
- ✅ **Sao Lưu và Khôi Phục**
- ✅ **Cấu Trúc Dữ Liệu Nâng Cao**: Hỗ trợ sets và sorted sets (tuyệt vời cho leaderboards)
- **Kiến Trúc**: Các node Redis sao chép sang các node khác để đảm bảo dự phòng

### Tính Năng của Memcached

- ❌ **Không có High Availability** (phiên bản truyền thống)
- ❌ **Không có Replication** (phiên bản truyền thống)
- ⚠️ **Nguy Cơ Mất Dữ Liệu**: Nếu một node gặp sự cố, dữ liệu cache có thể bị mất
- ✅ **Kiến Trúc Đa Luồng**: Hiệu suất tốt hơn cho một số loại workload
- ⚠️ **Sao Lưu Hạn Chế**: Sao lưu và khôi phục chỉ có trong phiên bản serverless
- **Kiến Trúc**: Nhiều node với sharding/phân vùng dữ liệu

## Điểm Chính Cần Nhớ

- ElastiCache cung cấp dịch vụ Redis và Memcached được quản lý
- Yêu cầu thay đổi mã nguồn ứng dụng để triển khai
- Hai mô hình chính: Cache-Aside và Session Store
- Redis cung cấp nhiều tính năng hơn (HA, replication, persistence)
- Memcached cung cấp kiến trúc sharding đa luồng đơn giản hơn
- Lựa chọn dựa trên trường hợp sử dụng cụ thể và yêu cầu của bạn

## Mẹo Cho Kỳ Thi

Kỳ thi có thể không kiểm tra sâu về so sánh Redis vs Memcached, nhưng hiểu biết về sự khác biệt cơ bản và các trường hợp sử dụng là rất có giá trị cho các tình huống thực tế.




FILE: 80-aws-cloudfront-caching-overview.md


# Tổng Quan về Caching trong AWS CloudFront

## Giới Thiệu

Amazon CloudFront là dịch vụ mạng phân phối nội dung (CDN) lưu trữ nội dung tại các edge location trên toàn thế giới để cải thiện hiệu suất và giảm độ trễ cho người dùng cuối. Hiểu cách hoạt động của CloudFront caching là điều cần thiết để tối ưu hóa hiệu suất và chi phí của ứng dụng.

## Cách Hoạt Động của CloudFront Caching

### Kiến Trúc Cache

- Cache tồn tại ở mỗi CloudFront edge location
- Bạn sẽ có nhiều cache bằng số lượng edge location
- Mỗi object trong cache được xác định bởi một **Cache Key** (Khóa Cache)

### Luồng Xử Lý Request Cache

Khi một request được thực hiện qua CloudFront edge location:

1. Edge location kiểm tra xem object đã được cache chưa
2. Nếu đã cache, kiểm tra xem object đã hết hạn hay chưa dựa trên Time To Live (TTL)
3. Nếu chưa có trong cache hoặc đã hết hạn, request được chuyển tiếp đến origin của bạn
4. Response từ origin được cache tại edge location
5. Các request sau sẽ trả về kết quả đã được cache

### Tối Ưu Hóa Cache

**Mục tiêu**: Tối đa hóa tỷ lệ Cache Hit bằng cách giảm thiểu request đến origin

Điều này có nghĩa là cache càng nhiều nội dung càng tốt tại các edge location của bạn.

### Cache Invalidation (Vô Hiệu Hóa Cache)

Bạn không cần đợi đến khi một item hết hạn dựa trên TTL. Nếu muốn xóa một object khỏi cache ngay lập tức, bạn có thể tạo **cache invalidation**.

## CloudFront Cache Key

### Cache Key là gì?

Cache Key là một **định danh duy nhất** cho mỗi object trong cache.

### Các Thành Phần Cache Key Mặc Định

Theo mặc định, Cache Key bao gồm:
- **Hostname** (tên miền) (ví dụ: `mywebsite.com`)
- **Phần resource của URL** (ví dụ: `/content/stories/example-story.html`)

**Ví dụ:**
```
GET https://mywebsite.com/content/stories/example-story.html
```

Khi xảy ra cache miss:
1. Object được lấy từ origin
2. Object được cache dựa trên hostname và phần resource
3. Các request tiếp theo có cùng hostname và resource sẽ nhận được cache hit

### Cache Key Nâng Cao

Đôi khi nội dung thay đổi dựa trên:
- Tùy chọn người dùng
- Loại thiết bị
- Ngôn ngữ
- Vị trí địa lý

Để đáp ứng điều này, bạn có thể nâng cao Cache Key bằng cách thêm:
- **HTTP headers**
- **Cookies**
- **Query strings** (chuỗi truy vấn)

## CloudFront Cache Policy

**Cache Policy** xác định cách tạo Cache Key bằng cách chỉ định những gì cần bao gồm:

### HTTP Headers
- **None** (Không có): Không bao gồm header nào
- **Whitelist** (Danh sách trắng): Chọn các header cụ thể để bao gồm

### Cookies
- **None**: Không bao gồm cookie nào
- **Whitelist**: Chọn các cookie cụ thể để bao gồm
- **All** (Tất cả): Bao gồm tất cả cookies
- **All-except** (Tất cả ngoại trừ): Bao gồm tất cả trừ các cookie được chỉ định

### Query Strings
- **None**: Không bao gồm query string nào
- **Whitelist**: Chọn các query string cụ thể để bao gồm
- **All-except**: Bao gồm tất cả trừ các query string được chỉ định
- **All**: Bao gồm tất cả query strings

### Kiểm Soát TTL

Trong cache policy, bạn có thể kiểm soát:
- Phạm vi TTL: từ 0 giây đến 1 năm
- Sử dụng các header cụ thể như `Cache-Control` hoặc `Expires`

### Tùy Chọn Policy

- **Tạo custom cache policies** (chính sách cache tùy chỉnh)
- **Sử dụng AWS predefined managed policies** (chính sách được quản lý sẵn bởi AWS)

### Lưu Ý Quan Trọng

**Tất cả HTTP headers, cookies, và query strings được bao gồm trong Cache Key sẽ tự động được chuyển tiếp đến origin request của bạn.**

## Ví Dụ về HTTP Headers

### Kịch Bản: Caching Dựa Trên Ngôn Ngữ

Request với header: `Accept-Language: fr-FR`

#### None Policy
- Không có header nào được cache
- Headers không được chuyển tiếp đến origin
- **Hiệu suất caching tốt nhất** (không có header trong Cache Key)

#### Whitelist Policy
- Chỉ định header nào cần bao gồm (ví dụ: `Accept-Language`)
- Header `Accept-Language` được bao gồm trong Cache Key
- Header được chuyển tiếp đến origin
- Origin có thể phản hồi nội dung bằng ngôn ngữ chính xác

## Ví Dụ về Query Strings

Query strings xuất hiện trong URL sau dấu hỏi chấm.

**Ví dụ:**
```
https://example.com/image/cat.jpg?border=red&size=large
```

### None
- Không có query string nào được sử dụng cho Cache Key
- Không được chuyển tiếp đến origin

### Whitelist
- Chỉ định query string nào cần bao gồm

### Include All-except
- Chỉ định những query string nào cần loại trừ
- Phần còn lại được bao gồm

### All
- Tất cả query strings được bao gồm trong Cache Key
- Tất cả được chuyển tiếp đến origin
- **Hiệu suất caching tệ nhất** (nhiều biến thể)

## Origin Request Policy

### Mục Đích

Đôi khi bạn cần chuyển tiếp thông tin đến origin mà **không nên** là một phần của Cache Key.

### Origin Request Policy là gì?

Origin Request Policy cho phép bạn:
- Bao gồm thêm HTTP headers, cookies, hoặc query strings
- Chuyển tiếp chúng đến origin
- **Không sử dụng chúng trong Cache Key**

### Khả Năng Bổ Sung

Bạn có thể thêm custom HTTP headers hoặc CloudFront HTTP headers vào origin request, ngay cả khi chúng không có trong viewer request.

**Trường hợp sử dụng:**
- Truyền API key
- Truyền secret header

### Tùy Chọn Policy

- **Tạo custom policies** (chính sách tùy chỉnh)
- **Sử dụng AWS predefined managed policies**

## Cache Policy vs Origin Request Policy

### Hiểu Sự Khác Biệt

**Luồng Request:**

1. **Viewer Request** đến với:
   - Query strings
   - Cookies
   - Headers

2. **Cache Policy** xác định những gì cần cache:
   - Ví dụ: Hostname + Resource + Header `Authorization`

3. **Origin Request** có thể cần thông tin bổ sung:
   - User Agent
   - Session ID
   - Referrer query string

4. **Kết quả:**
   - Origin request được bổ sung thêm các tham số
   - Caching chỉ xảy ra dựa trên Cache Policy
   - Các tham số bổ sung từ Origin Request Policy không ảnh hưởng đến caching

### Điểm Chính

**Sự phối hợp** giữa hai policy này cho phép bạn:
- Tối ưu hóa caching (Cache Policy)
- Cung cấp thông tin đầy đủ cho origin (Origin Request Policy)
- Duy trì tỷ lệ cache hit cao trong khi đáp ứng yêu cầu của origin

## Tóm Tắt

- CloudFront caching xảy ra tại các edge location trên toàn thế giới
- Cache Keys xác định các object duy nhất trong cache
- Cache Policies kiểm soát những gì được đưa vào Cache Key
- Origin Request Policies kiểm soát những gì được chuyển tiếp đến origin (mà không ảnh hưởng đến caching)
- Cấu hình đúng giúp tối đa hóa tỷ lệ cache hit và cải thiện hiệu suất
- Hiểu các khái niệm này là điều cần thiết cho các kỳ thi chứng chỉ AWS

## Thực Hành Tốt Nhất

1. **Tối đa hóa tỷ lệ cache hit** bằng cách chọn cẩn thận các thành phần Cache Key
2. **Sử dụng whitelist** thay vì tùy chọn "all" khi có thể
3. **Tách biệt các mối quan tâm về caching** khỏi nhu cầu origin request bằng cách sử dụng cả hai policy
4. **Tận dụng AWS managed policies** khi chúng phù hợp với use case của bạn
5. **Sử dụng cache invalidation** một cách tiết kiệm (phát sinh chi phí)

---

*Tài liệu này dựa trên các khái niệm cơ bản về AWS CloudFront caching và được thiết kế để giúp các developer và solutions architect hiểu và tối ưu hóa hiệu suất CDN.*




FILE: 81-aws-cloudfront-cache-invalidation.md


# Vô Hiệu Hóa Cache CloudFront của AWS

## Tổng Quan

Vô hiệu hóa cache CloudFront là một cơ chế cho phép bạn buộc làm mới nội dung được lưu trong cache tại các edge location trước khi Time To Live (TTL) hết hạn. Điều này đảm bảo người dùng của bạn nhận được nội dung mới nhất từ origin càng sớm càng tốt.

## Vấn Đề

Khi bạn cập nhật nội dung trong backend origin (chẳng hạn như S3 bucket), các edge location của CloudFront sẽ không tự động biết về những thay đổi này. Chúng sẽ tiếp tục phục vụ nội dung đã lưu trong cache cho đến khi TTL hết hạn, điều này có thể dẫn đến việc người dùng nhìn thấy nội dung đã lỗi thời.

## Giải Pháp: Vô Hiệu Hóa Cache

CloudFront cho phép bạn thực hiện vô hiệu hóa cache, buộc làm mới toàn bộ hoặc một phần cache. Điều này loại bỏ nhu cầu phải chờ TTL hết hạn tự nhiên.

### Các Tùy Chọn Vô Hiệu Hóa

Bạn có thể vô hiệu hóa nội dung bằng cách sử dụng đường dẫn file:

- **Vô hiệu hóa tất cả file**: Sử dụng `*` để xóa toàn bộ cache
- **Vô hiệu hóa đường dẫn cụ thể**: Ví dụ, `/images/*` để xóa tất cả hình ảnh
- **Vô hiệu hóa file cụ thể**: Ví dụ, `/index.html` để xóa một file duy nhất

## Cách Hoạt Động

### Ví Dụ Kịch Bản

1. **Trạng Thái Ban Đầu**
   - CloudFront distribution với nhiều edge location
   - Mỗi edge location có cache riêng chứa các file như `index.html` và hình ảnh
   - Origin: S3 bucket
   - TTL: Được thiết lập là 1 ngày

2. **Cập Nhật Nội Dung**
   - Với vai trò quản trị viên, bạn cập nhật các file trong S3 bucket
   - Bạn thêm hoặc thay đổi hình ảnh
   - Bạn sửa đổi file `index.html`
   - Bạn muốn các cập nhật này được phản ánh ngay lập tức cho người dùng

3. **Quá Trình Vô Hiệu Hóa**
   - Vô hiệu hóa `/index.html` để xóa file cụ thể
   - Vô hiệu hóa `/images/*` để xóa tất cả hình ảnh khỏi cache
   - CloudFront thông báo cho các edge location để xóa các file này khỏi cache của chúng

4. **Kết Quả**
   - Khi người dùng yêu cầu `index.html`, CloudFront chuyển tiếp yêu cầu đến một edge location
   - Edge location nhận ra file không còn trong cache của nó nữa
   - Edge location lấy file đã cập nhật từ origin
   - Người dùng nhận được phiên bản mới nhất của nội dung

## Lợi Ích

- **Cập Nhật Tức Thì**: Không cần chờ TTL hết hạn
- **Kiểm Soát Chi Tiết**: Vô hiệu hóa các file cụ thể hoặc toàn bộ thư mục
- **Trải Nghiệm Người Dùng**: Đảm bảo người dùng luôn nhận được nội dung mới nhất

## Thực Hành Tốt Nhất

- Sử dụng đường dẫn cụ thể khi có thể để giảm thiểu phạm vi vô hiệu hóa
- Lập kế hoạch vô hiệu hóa cẩn thận vì chúng có thể phát sinh chi phí
- Cân nhắc các chiến lược phiên bản cho nội dung được cập nhật thường xuyên

## Kết Luận

Vô hiệu hóa cache CloudFront là một công cụ mạnh mẽ để quản lý độ tươi mới của nội dung trong CDN của bạn. Bằng cách hiểu cách vô hiệu hóa nội dung đã lưu trong cache một cách đúng đắn, bạn có thể đảm bảo người dùng của mình luôn nhận được phiên bản mới nhất của các file trong khi vẫn hưởng lợi từ các lợi thế về hiệu suất của CloudFront.




FILE: 82-aws-cloudfront-cache-behaviors.md


# AWS CloudFront Cache Behaviors (Hành Vi Cache)

## Tổng Quan

Cache behaviors trong CloudFront cho phép bạn cấu hình các nguồn gốc (origins) và chiến lược lưu trữ khác nhau cho các mẫu đường dẫn URL khác nhau. Điều này mang lại sự linh hoạt trong việc định tuyến yêu cầu dựa trên loại nội dung hoặc mẫu đường dẫn.

## Hiểu Về Cache Behaviors

Cache behaviors cho phép bạn:
- Định nghĩa các nguồn gốc khác nhau cho các mẫu đường dẫn URL khác nhau
- Định tuyến đến các nhóm nguồn gốc khác nhau dựa trên loại nội dung hoặc đường dẫn
- Triển khai các chiến lược lưu trữ cụ thể cho các loại nội dung khác nhau

### Ví Dụ Định Tuyến Theo Mẫu Đường Dẫn

Bạn có thể cấu hình CloudFront để định tuyến các yêu cầu như sau:
- `/images/*` → Amazon S3
- `/api/*` → Nguồn gốc ứng dụng của bạn
- `/*` → Nguồn gốc mặc định (default cache behavior)

## Cấu Hình Cache Behavior

### Ví Dụ Nhiều Cache Behaviors

Xét một phân phối CloudFront với hai cache behaviors:

1. **Cache Behavior `/api/*`**
   - Định tuyến đến nguồn gốc Application Load Balancer
   - Xử lý các yêu cầu API

2. **Cache Behavior Mặc Định `/*`**
   - Luôn được xử lý cuối cùng
   - Định tuyến đến S3 bucket làm nguồn gốc
   - Hoạt động như phương án dự phòng cho các mẫu không khớp

### Thứ Tự Xử Lý

Khi bạn thêm các cache behaviors bổ sung:
- CloudFront kiểm tra khớp cụ thể nhất trước
- Cache behavior mặc định (`/*`) luôn được xử lý cuối cùng
- Nếu không tìm thấy khớp cụ thể, CloudFront quay về cache behavior mặc định

## Các Trường Hợp Sử Dụng

### Trường Hợp 1: Kiểm Soát Truy Cập Với Signed Cookies

Triển khai xác thực để kiểm soát quyền truy cập vào nội dung S3 bucket:

1. **Cache Behavior Đăng Nhập** (`/login`)
   - Định tuyến đến EC2 instance
   - EC2 instance tạo CloudFront signed cookies
   - Signed cookies được gửi lại cho người dùng

2. **Cache Behavior Mặc Định** (tất cả các URL khác)
   - Yêu cầu signed cookies phải có mặt
   - Cung cấp quyền truy cập vào các tệp trong S3 bucket
   - Chuyển hướng đến `/login` nếu thiếu cookies

Phương pháp này đảm bảo người dùng phải xác thực trước khi truy cập nội dung được bảo vệ.

### Trường Hợp 2: Tối Đa Hóa Tỷ Lệ Cache Hit

Tối ưu hóa caching bằng cách tách riêng nội dung tĩnh và động:

1. **Nội Dung Tĩnh** (Amazon S3)
   - Không có chính sách cache với headers hoặc sessions
   - Tối đa hóa cache hit chỉ dựa trên tài nguyên được yêu cầu
   - Lý tưởng cho hình ảnh, CSS, tệp JavaScript

2. **Nội Dung Động** (REST HTTP Server qua ALB/EC2)
   - Cache dựa trên headers và cookies phù hợp
   - Sử dụng chính sách cache đã định nghĩa cho các phản hồi động
   - Cân bằng giữa caching và nhu cầu cá nhân hóa

## Thực Hành Tốt Nhất

- Cấu hình các cache behaviors cụ thể cho các loại nội dung khác nhau
- Sử dụng cache behavior mặc định làm phương án dự phòng
- Tận dụng signed cookies để kiểm soát truy cập khi cần thiết
- Tách riêng nội dung tĩnh và động để tối ưu hiệu suất cache
- Xem xét thứ tự xử lý khi định nghĩa nhiều cache behaviors

## Tóm Tắt

CloudFront cache behaviors cung cấp khả năng định tuyến và caching mạnh mẽ cho phép bạn tối ưu hóa phân phối nội dung dựa trên nhu cầu cụ thể của ứng dụng. Bằng cách cấu hình cache behaviors đúng cách, bạn có thể cải thiện hiệu suất, triển khai kiểm soát truy cập và tối đa hóa hiệu quả cache.




FILE: 83-aws-cloudfront-cache-behaviors-and-invalidations.md


# AWS CloudFront Cache Behaviors và Invalidations

## Tổng quan

Hướng dẫn này trình bày cách cấu hình cache behaviors trong AWS CloudFront và cách quản lý cache invalidations để đảm bảo nội dung cập nhật được phân phối đúng cách.

## Hiểu về Cache Behaviors

### Default Behavior (Hành vi Mặc định)

CloudFront distributions đi kèm với cache behavior mặc định áp dụng cho toàn bộ nội dung:

- Behavior mặc định sử dụng path pattern wildcard (`*`)
- Path pattern không thể chỉnh sửa đối với behavior mặc định
- Bạn có thể cấu hình cache key và origin request settings

### Cấu hình Cache Policy

Khi tạo cache policy (ví dụ: `DemoCachePolicy`), bạn có thể kiểm soát:

#### Cài đặt Time to Live (TTL)

- **Minimum TTL**: Thời gian tối thiểu các object được lưu trong cache
- **Maximum TTL**: Thời gian tối đa các object được lưu trong cache
- **Default TTL**: Thời gian cache mặc định

#### Cài đặt Cache Key

Bạn có thể chỉ định các thành phần nào được bao gồm trong cache key:

1. **Headers**
   - Chọn từ danh sách headers được định nghĩa sẵn
   - Thêm custom headers nếu cần

2. **Query Strings**
   - Bao gồm tất cả query strings
   - Hoặc chọn các query strings cụ thể từ danh sách

3. **Cookies**
   - Bao gồm tất cả cookies
   - Hoặc chỉ định danh sách các cookies cụ thể

Dữ liệu sẽ được cache dựa trên các cài đặt này cho headers, query strings và cookies.

### Origin Request Policy

Ngoài cache policy, bạn có thể tạo origin request policy (ví dụ: `DemoOriginPolicy`) để truyền thêm dữ liệu tới origin mà không phải là một phần của cache key:

- Headers bổ sung
- Query strings bổ sung
- Cookies bổ sung

Điều này cho phép bạn tăng cường origin request vượt ra ngoài những gì được sử dụng cho caching.

## Tạo Nhiều Cache Behaviors

Bạn có thể tạo nhiều cache behaviors để xử lý các loại nội dung khác nhau:

1. Tạo behavior mới với path pattern cụ thể (ví dụ: `/images/*`)
2. Định tuyến requests tới origin khác (S3 bucket, EC2 instance, v.v.)
3. Áp dụng cache key và origin request policies cụ thể
4. Path patterns cụ thể hơn sẽ được ưu tiên trước

Nhiều cache behaviors cùng tồn tại, với pattern cụ thể nhất được chọn trước.

## Cache Invalidations

### Hiểu về Vấn đề

Khi bạn cập nhật nội dung ở origin (ví dụ: S3 bucket), CloudFront tiếp tục phục vụ phiên bản cached cho đến khi TTL hết hạn. Ví dụ:

- Upload phiên bản mới của `index.html` lên S3
- File được cập nhật trong S3 ngay lập tức
- CloudFront vẫn phục vụ phiên bản cached cũ (ví dụ: trong một ngày)
- Truy cập trực tiếp S3 hiển thị nội dung mới, nhưng CloudFront URL hiển thị nội dung cũ

### Tạo Invalidation

Để buộc CloudFront lấy nội dung mới từ origin:

1. Điều hướng đến tab **Invalidations** trong CloudFront distribution của bạn
2. Tạo invalidation mới
3. Chỉ định các đường dẫn object cần invalidate:
   - Sử dụng `/*` để invalidate tất cả objects
   - Hoặc chỉ định đường dẫn file cụ thể

Khi invalidation hoàn tất, CloudFront sẽ lấy nội dung mới từ origin ở request tiếp theo.

## Ví dụ Thực tế

### Tình huống

1. File ban đầu chứa: "I really love coffee"
2. Cập nhật file thành: "I really love coffee every morning"
3. Upload phiên bản mới lên S3 (không bật versioning, nó sẽ thay thế file cũ)
4. S3 phục vụ nội dung mới ngay lập tức
5. CloudFront vẫn phục vụ phiên bản cũ đã được cache

### Giải pháp

1. Truy cập CloudFront console
2. Điều hướng đến tab Invalidations
3. Tạo invalidation với pattern `/*`
4. Đợi invalidation hoàn tất
5. CloudFront bây giờ phục vụ nội dung đã cập nhật: "I really love coffee every morning"

## Best Practices (Thực hành Tốt nhất)

- Sử dụng giá trị TTL phù hợp dựa trên tần suất cập nhật nội dung
- Cụ thể hóa cache keys để tối ưu cache hit rates
- Sử dụng nhiều cache behaviors cho các loại nội dung khác nhau
- Nhớ rằng invalidations có chi phí - sử dụng chúng một cách hợp lý
- Xem xét chiến lược versioning (ví dụ: tên file có version) để tránh invalidations thường xuyên

## Tóm tắt

CloudFront cache behaviors và policies cung cấp cho bạn khả năng kiểm soát chi tiết về caching và origin requests. Khi bạn cần buộc cập nhật nội dung trước khi TTL hết hạn, cache invalidations cung cấp giải pháp ngay lập tức để làm mới nội dung đã phân phối của bạn.




FILE: 84-aws-cloudfront-vpc-origins.md


# AWS CloudFront VPC Origins

## Tổng quan

Tài liệu này giải thích cách kết nối CloudFront với application load balancer hoặc EC2 instance làm origin, bao gồm cả phương pháp hiện đại sử dụng VPC origins và phương pháp cũ sử dụng mạng công khai.

## Phương pháp hiện đại: VPC Origins

### VPC Origins là gì?

VPC Origins là cách **tốt hơn và mới hơn** để kết nối CloudFront với các ứng dụng backend của bạn. Tính năng này cho phép bạn:

- Phân phối nội dung trực tiếp từ các ứng dụng được lưu trữ trong **private subnet** bên trong VPC của bạn
- Giữ mọi thứ ở chế độ riêng tư mà không cần phơi bày tài nguyên ra internet
- Phân phối traffic đến:
  - Private Application Load Balancers (ALB)
  - Network Load Balancers (NLB)
  - EC2 instances

### Cách hoạt động của VPC Origins

1. Tạo một **CloudFront distribution** với nhiều edge location
2. Người dùng truy cập CloudFront thông qua các edge location này
3. Tạo một **VPC origin** trong CloudFront
4. Kết nối VPC origin với backend của bạn (ALB, NLB, hoặc EC2 instance)
5. CloudFront định tuyến traffic thông qua VPC origin đến private subnet và ứng dụng của bạn

### Lợi ích về bảo mật

Từ góc độ mạng, VPC Origins cung cấp **một trong những thiết lập bảo mật nhất** bởi vì:

- Ứng dụng vẫn được lưu trữ riêng tư và nội bộ
- Bạn kiểm soát chính xác những gì được phơi bày thông qua CloudFront
- Không cần phơi bày ra internet công cộng

## Phương pháp cũ: Public Network (Trước VPC Origins)

### Tổng quan

Trước khi VPC Origins ra đời, bạn phải sử dụng mạng công khai để kết nối CloudFront với origin của mình. Mặc dù vẫn hoạt động, phương pháp này phức tạp hơn và kém bảo mật hơn.

### Phương pháp Public EC2 Instance

**Yêu cầu:**
- EC2 instance phải là **public**
- Lấy danh sách các IP công khai của CloudFront edge location
- Cấu hình security group để chỉ cho phép IP của CloudFront

**Quy trình:**
1. Tìm danh sách tất cả các địa chỉ IP của CloudFront
2. Cập nhật security group của EC2 instance
3. Chỉ cho phép các IP công khai của CloudFront truy cập instance của bạn
4. Instance trở thành public nhưng chỉ giới hạn cho các edge location

### Phương pháp Public Application Load Balancer

**Kiến trúc:**
- ALB phải là **public**
- EC2 instance đằng sau ALB có thể vẫn là **private**
- Mạng riêng tư giữa ALB và EC2 instance được bảo mật bằng security group

**Quy trình:**
1. Đảm bảo ALB có thể truy cập công khai
2. Giữ các EC2 instance trong private subnet
3. Cấu hình security group để cho phép giao tiếp riêng tư giữa ALB và EC2
4. Cập nhật security group của ALB để cho phép tất cả IP công khai của CloudFront

### Nhược điểm của phương pháp cũ

1. **Cấu hình phức tạp:**
   - Phải tìm và duy trì thủ công các IP công khai của CloudFront
   - Cần cập nhật security group

2. **Rủi ro bảo mật:**
   - Nếu ai đó thay đổi security group của ALB hoặc EC2 instance của bạn
   - Tài nguyên của bạn trở thành public với nhiều hơn chỉ CloudFront
   - Tăng bề mặt tấn công

3. **Chi phí bảo trì:**
   - Các dải IP của CloudFront có thể thay đổi
   - Yêu cầu giám sát và cập nhật liên tục

## Khuyến nghị

**Sử dụng VPC Origins** cho tất cả các triển khai mới. Phương pháp hiện đại này cung cấp:
- ✅ Tư thế bảo mật tốt hơn
- ✅ Cấu hình đơn giản hơn
- ✅ Kiến trúc mạng riêng tư
- ✅ Giảm chi phí bảo trì

Phương pháp mạng công khai cũ chỉ nên được xem xét cho các triển khai hiện có chưa được di chuyển.

---

*Hướng dẫn này dựa trên các phương pháp hay nhất và khuyến nghị bảo mật của AWS CloudFront.*




FILE: 85-aws-cloudfront-geo-restriction.md


# AWS CloudFront Geo Restriction (Hạn Chế Địa Lý)

## Tổng Quan

CloudFront geo restriction cho phép bạn kiểm soát ai có thể truy cập distribution của bạn dựa trên vị trí địa lý (quốc gia) mà họ cố gắng truy cập. Tính năng này sử dụng cơ sở dữ liệu geo IP của bên thứ ba để khớp địa chỉ IP của người dùng với quốc gia tương ứng.

## Cách Thức Hoạt Động

Tính năng hạn chế địa lý xác định quốc gia của người dùng bằng cách:
- Khớp địa chỉ IP của người dùng với cơ sở dữ liệu geo IP của bên thứ ba
- Xác định quốc gia liên quan đến địa chỉ IP đó
- Áp dụng các quy tắc cho phép hoặc chặn đã được cấu hình

## Tùy Chọn Cấu Hình

Bạn có thể cấu hình geo restriction theo hai cách:

### 1. Allow List (Danh Sách Cho Phép)
Xác định danh sách các quốc gia được phê duyệt có thể truy cập nội dung của bạn. Chỉ người dùng từ các quốc gia này mới có thể truy cập distribution.

### 2. Block List (Danh Sách Chặn)
Xác định danh sách các quốc gia bị cấm không thể truy cập nội dung của bạn. Người dùng từ các quốc gia này sẽ bị từ chối quyền truy cập vào distribution.

## Trường Hợp Sử Dụng

Trường hợp sử dụng chính cho geo restriction là:
- **Tuân Thủ Luật Bản Quyền**: Kiểm soát quyền truy cập nội dung dựa trên các thỏa thuận cấp phép địa lý và hạn chế bản quyền

## Yêu Cầu Thiết Lập

### Yêu Cầu Gói Dịch Vụ
Để sử dụng chức năng chặn lưu lượng truy cập theo địa lý, bạn cần:
- Gói thanh toán **Pay as You Go** (Trả theo mức sử dụng), hoặc
- Gói CloudFront trả phí

Lưu ý: Gói miễn phí không hỗ trợ tính năng geo restriction.

### Các Bước Cấu Hình

1. Điều hướng đến CloudFront distribution của bạn
2. Vào phần **Security** (Bảo mật)
3. Chọn **CloudFront geographic restrictions** (Hạn chế địa lý CloudFront)
4. Chọn một trong hai:
   - **Allow list**: Chọn các quốc gia được phép
   - **Block list**: Chọn các quốc gia bị chặn
5. Chọn các quốc gia bạn muốn thêm vào danh sách
6. Lưu thay đổi của bạn

## Lưu Ý Quan Trọng

- Hạn chế địa lý chỉ khả dụng trên các gói Pay as You Go hoặc gói trả phí
- Gói miễn phí (manage free plan) không bao gồm chức năng chặn lưu lượng truy cập theo địa lý
- Các thay đổi đối với geo restrictions có thể mất một thời gian để lan truyền
- Tính năng này dựa vào dữ liệu định vị địa lý IP của bên thứ ba, có thể không chính xác 100%

## Thực Hành Tốt Nhất

- Thường xuyên xem xét cài đặt geo restriction của bạn để đảm bảo chúng phù hợp với các thỏa thuận cấp phép nội dung
- Kiểm tra các hạn chế của bạn từ các vị trí khác nhau để xác minh chúng hoạt động như mong đợi
- Lưu ý rằng VPN và proxy có thể ảnh hưởng đến độ chính xác của việc phát hiện địa lý
- Ghi chúng các chính sách geo restriction của bạn cho mục đích tuân thủ và kiểm toán




FILE: 86-aws-cloudfront-signed-urls-and-cookies.md


# AWS CloudFront Signed URLs và Signed Cookies

## Tổng quan

CloudFront Signed URLs và Signed Cookies là các cơ chế để kiểm soát quyền truy cập vào nội dung riêng tư được phân phối qua Amazon CloudFront. Các tính năng này cho phép bạn cung cấp nội dung cao cấp, trả phí hoặc nội dung bị hạn chế cho người dùng trên toàn thế giới trong khi vẫn duy trì bảo mật và kiểm soát truy cập.

## Các trường hợp sử dụng

- Phân phối nội dung cao cấp trả phí toàn cầu
- Kiểm soát ai có quyền truy cập vào các tài nguyên CloudFront cụ thể
- Cung cấp quyền truy cập tạm thời vào các file riêng tư
- Bảo mật phân phối nội dung cho người dùng đã xác thực

## Chính sách Signed URLs và Cookies

Khi tạo signed URL hoặc signed cookie, bạn cần đính kèm một chính sách chỉ định:

### 1. **Thời gian hết hạn**
- Xác định khi nào URL hoặc cookie hết hạn
- Thời gian ngắn cho nội dung tạm thời (ví dụ: phát trực tuyến phim hoặc nhạc - vài phút)
- Thời gian dài cho nội dung người dùng lâu dài (có thể kéo dài nhiều năm)

### 2. **Giới hạn phạm vi IP**
- Chỉ định phạm vi IP nào có thể truy cập dữ liệu
- Được khuyến nghị nếu bạn biết địa chỉ IP mục tiêu của khách hàng
- Thêm một lớp bảo mật bổ sung

### 3. **Trusted Signers (Người ký đáng tin cậy)**
- Xác định tài khoản AWS nào có thể tạo signed URLs
- Kiểm soát ủy quyền ở cấp độ tài khoản

## Signed URLs so với Signed Cookies

### Signed URLs
- **Cấp độ truy cập**: Các file riêng lẻ (một URL cho mỗi file)
- **Trường hợp sử dụng**: Khi bạn cần phân phối quyền truy cập vào các file cụ thể
- **Ví dụ**: 100 file = 100 URL khác nhau

### Signed Cookies
- **Cấp độ truy cập**: Nhiều file (một cookie cho nhiều file)
- **Trường hợp sử dụng**: Khi bạn cần cung cấp quyền truy cập vào nhiều file
- **Ưu điểm**: Cookie có thể được sử dụng lại trên nhiều file

**Khuyến nghị**: Chọn dựa trên yêu cầu cụ thể và trường hợp sử dụng của bạn.

## Cách hoạt động của Signed URLs

### Luồng kiến trúc

1. **Xác thực Client**
   - Client xác thực với ứng dụng của bạn
   - Ứng dụng xác thực thông tin đăng nhập người dùng

2. **Tạo URL**
   - Ứng dụng sử dụng AWS SDK để tạo signed URL từ CloudFront
   - Signed URL được tạo dựa trên chính sách

3. **Phân phối URL**
   - Ứng dụng trả về signed URL cho client

4. **Truy cập nội dung**
   - Client sử dụng signed URL để truy cập nội dung từ CloudFront
   - CloudFront xác thực chữ ký và chính sách
   - Nội dung được phân phối từ edge location gần nhất

### Tích hợp với S3 và OAC

- CloudFront có thể sử dụng Origin Access Control (OAC) để bảo mật tối đa
- Các object trong S3 bucket bị hạn chế chỉ cho phép CloudFront truy cập
- Client không thể truy cập trực tiếp S3 bucket
- Signed URLs cung cấp quyền truy cập được kiểm soát thông qua CloudFront

## CloudFront Signed URLs so với S3 Pre-Signed URLs

### CloudFront Signed URLs

**Mục đích**: Cho phép truy cập vào một đường dẫn bất kể loại origin

**Tính năng**:
- Hoạt động với bất kỳ origin nào (S3, HTTP backend, EC2, v.v.)
- Sử dụng key-pair cấp tài khoản (chỉ root mới có thể quản lý)
- Có thể lọc theo:
  - Địa chỉ IP
  - Đường dẫn
  - Ngày tháng
  - Thời gian hết hạn
- Tận dụng các tính năng caching của CloudFront
- Phân phối edge location toàn cầu

**Kiến trúc**: 
```
Client → CloudFront (với Signed URL) → Origin (S3/EC2/HTTP)
```

### S3 Pre-Signed URLs

**Mục đích**: Truy cập trực tiếp vào các object S3

**Tính năng**:
- Phát hành yêu cầu với quyền của IAM principal đã ký trước URL
- Cấp cùng quyền như thông tin đăng nhập IAM của người ký
- Thời gian tồn tại có giới hạn
- Truy cập trực tiếp vào S3 bucket (bỏ qua CloudFront)

**Kiến trúc**:
```
Client → S3 Bucket (với Pre-Signed URL)
```

## Khi nào sử dụng từng phương pháp

### Sử dụng CloudFront Signed URLs khi:
- Nội dung được phân phối thông qua CloudFront
- S3 bucket bị hạn chế với OAC/OAI
- Bạn cần caching edge location toàn cầu
- Origin có thể là S3, EC2 hoặc bất kỳ HTTP backend nào
- Bạn muốn tận dụng các tính năng của CloudFront

### Sử dụng S3 Pre-Signed URLs khi:
- Người dùng truy cập S3 bucket trực tiếp (không qua CloudFront)
- Không cần phân phối CDN
- Bạn muốn phân phối file trực tiếp từ S3
- Trường hợp sử dụng đơn giản hơn không có yêu cầu caching

## Thực hành tốt nhất

1. **Bảo mật**: Luôn sử dụng HTTPS cho signed URLs
2. **Hết hạn**: Đặt thời gian hết hạn phù hợp dựa trên loại nội dung
3. **Hạn chế IP**: Sử dụng lọc IP khi biết IP của client
4. **Quản lý khóa**: Bảo vệ CloudFront key-pairs (chỉ tài khoản root truy cập)
5. **Giám sát**: Theo dõi việc sử dụng signed URL và các mẫu truy cập

## Tóm tắt

CloudFront Signed URLs và Signed Cookies cung cấp kiểm soát truy cập mạnh mẽ cho phân phối nội dung riêng tư. Bằng cách hiểu sự khác biệt giữa signed URLs và cookies, cũng như khi nào sử dụng CloudFront so với S3 pre-signed URLs, bạn có thể triển khai chiến lược bảo mật và phân phối phù hợp nhất cho ứng dụng của mình.




FILE: 87-aws-cloudfront-signed-urls-key-management.md


# AWS CloudFront Signed URLs - Quản Lý Khóa

## Tổng Quan

Hướng dẫn này giải thích cách tạo và quản lý khóa để ký URL với Amazon CloudFront. Signed URLs cung cấp quyền truy cập an toàn, có giới hạn thời gian vào nội dung CloudFront của bạn.

## Các Loại Signers

CloudFront hỗ trợ hai loại signers để tạo signed URLs:

### 1. Trusted Key Groups (Phương Pháp Được Khuyến Nghị)

**Trusted key group** là phương pháp mới và được khuyến nghị để quản lý signed URLs trên CloudFront.

**Ưu điểm:**
- Tận dụng APIs để tự động tạo và xoay vòng khóa
- Sử dụng IAM cho bảo mật API trong việc quản lý key group
- Có thể được quản lý bởi bất kỳ IAM user nào có đủ quyền (không chỉ root account)
- Khả năng bảo mật và tự động hóa tốt hơn

### 2. CloudFront Key Pairs (Phương Pháp Cũ)

Phương pháp ban đầu sử dụng AWS account với CloudFront key pairs.

**Nhược điểm:**
- Yêu cầu thông tin đăng nhập root account
- Chỉ có thể quản lý qua AWS console
- Không hỗ trợ API để tự động hóa
- Cách tiếp cận kém an toàn hơn
- **Không được khuyến nghị cho các triển khai mới**

## Cách Thức Hoạt Động Của Trusted Key Groups

### Cấu Trúc Khóa

Bạn có thể tạo một hoặc nhiều trusted key groups trong CloudFront distribution của mình. Mỗi triển khai yêu cầu:

1. **Private Key (Khóa Riêng)** - Được sử dụng bởi ứng dụng của bạn (ví dụ: EC2 instances) để ký URLs
2. **Public Key (Khóa Công Khai)** - Được tải lên CloudFront để xác minh chữ ký URL

### Luồng Hoạt Động Của Khóa

```
Private Key → EC2 Instances → Ký URLs
Public Key → CloudFront → Xác Minh Chữ Ký
```

Private key được sử dụng bởi ứng dụng của bạn để tạo signed URLs, trong khi CloudFront sử dụng public key để xác minh tính hợp lệ của các chữ ký.

## Hướng Dẫn Thực Hành: Thiết Lập Trusted Key Groups

### Bước 1: Tạo Cặp Khóa RSA

1. Tạo cặp khóa RSA 2,048-bit sử dụng trình tạo trực tuyến hoặc OpenSSL
2. **Quan trọng:** Kích thước khóa phải chính xác là 2,048 bits
3. Đợi quá trình tạo khóa hoàn tất (khoảng 3 giây)
4. Lưu cả hai khóa:
   - **Private Key**: Giữ an toàn và bí mật - sử dụng bởi ứng dụng của bạn
   - **Public Key**: Sẽ được tải lên CloudFront

> **Lưu Ý Bảo Mật:** Private key nên được lưu trữ an toàn. Public key có thể được tạo lại từ private key nếu cần.

### Bước 2: Tạo Public Key Trong CloudFront

1. Điều hướng đến CloudFront trong AWS Console
2. Vào phần **Key Management**
3. Chọn **Public Keys** từ thanh bên trái
4. Nhấp **Create Public Key**
5. Cung cấp tên (ví dụ: "demo key")
6. Dán public key đã tạo của bạn
7. Nhấp **Create**

**Xử Lý Sự Cố:** Nếu gặp lỗi, hãy xác minh rằng bạn đang sử dụng khóa 2,048-bit. Nếu vấn đề vẫn tiếp diễn, hãy tạo lại cặp khóa 2,048-bit mới.

### Bước 3: Tạo Key Group

1. Trong CloudFront Key Management, chọn **Key Groups**
2. Nhấp **Create Key Group**
3. Cung cấp tên (ví dụ: "demo key group")
4. Thêm tối đa 5 public keys vào nhóm
5. Chọn public key vừa tạo của bạn
6. Nhấp **Create**

### Bước 4: Tham Chiếu Key Group Trong CloudFront Distribution

Key group sẽ được CloudFront tham chiếu để xác thực các signed URLs được tạo bởi ứng dụng của bạn (ví dụ: EC2 instances).

## Phương Pháp Cũ: CloudFront Key Pairs (Không Khuyến Nghị)

### Truy Cập CloudFront Key Pairs

1. Đăng nhập bằng **root account** (bắt buộc)
2. Nhấp vào tên tài khoản của bạn
3. Chọn **My Security Credentials**
4. Tìm phần **CloudFront Key Pair**

### Tạo Key Pair (Phương Pháp Cũ)

1. Chọn tạo key pair mới hoặc tải lên key pair của riêng bạn
2. Nếu tạo mới:
   - Nhấp **Create New Key Pair**
   - Tải xuống file private key
   - Tải xuống file public key
   - Nhấp **Close**

### Quản Lý Key Pairs

- Khóa có thể được đặt thành: Active, Inactive, hoặc Deleted
- Key pairs áp dụng cho tất cả CloudFront distributions
- Private keys phải được phân phối thủ công đến EC2 instances

### Tại Sao Phương Pháp Này Không Được Khuyến Nghị

- **Yêu cầu root account**: Chỉ root account mới có thể quản lý các khóa này
- **Không hỗ trợ API**: Không thể tự động hóa
- **Kém an toàn hơn**: Rủi ro bảo mật cao hơn so với trusted key groups
- **Không tích hợp IAM**: Không thể tận dụng quyền IAM

## Thực Hành Tốt Nhất

1. ✅ **Sử Dụng Trusted Key Groups** - Luôn ưu tiên phương pháp này hơn legacy key pairs
2. ✅ **IAM Users** - Cho phép IAM users với quyền phù hợp quản lý khóa
3. ✅ **Xoay Vòng Khóa** - Sử dụng APIs để tự động hóa việc xoay vòng khóa
4. ✅ **Lưu Trữ An Toàn** - Lưu trữ private keys an toàn (ví dụ: AWS Secrets Manager)
5. ✅ **Khóa 2,048-bit** - Luôn sử dụng khóa RSA 2,048-bit
6. ❌ **Tránh Root Account** - Không sử dụng root account để quản lý khóa

## Lời Khuyên Cho Kỳ Thi

Đối với các kỳ thi chứng chỉ AWS, hãy nhớ:
- **Trusted Key Groups** là phương pháp được khuyến nghị
- Bất kỳ IAM user nào có đủ quyền đều có thể quản lý key groups
- Phương pháp CloudFront Key Pair cũ yêu cầu quyền truy cập root account
- Trusted key groups hỗ trợ tự động hóa dựa trên API
- Private keys ký URLs; public keys xác minh chữ ký

## Tóm Tắt

CloudFront signed URLs cung cấp quyền truy cập an toàn, có kiểm soát vào nội dung của bạn. Phương pháp hiện đại sử dụng trusted key groups mang lại bảo mật, tự động hóa và tích hợp IAM tốt hơn so với phương pháp CloudFront key pair cũ. Luôn ưu tiên trusted key groups cho các triển khai mới.

---

**Điểm Chính Cần Nhớ:**
- Tạo cặp khóa RSA 2,048-bit
- Tải public keys lên CloudFront
- Tạo key groups để tổ chức public keys
- Giữ private keys an toàn trên các máy chủ ứng dụng của bạn
- Sử dụng IAM users thay vì root account để quản lý khóa




FILE: 88-aws-cloudfront-advanced-options.md


# Các Tùy Chọn Nâng Cao của AWS CloudFront

## Tổng quan

Tài liệu này trình bày các tùy chọn cấu hình nâng cao của CloudFront bao gồm định giá, các lớp giá, nhiều nguồn gốc, nhóm nguồn gốc và mã hóa cấp trường.

---

## Định Giá và Lớp Giá của CloudFront

### Hiểu về Định Giá CloudFront

Các edge location của CloudFront được phân bố toàn cầu, và chi phí truyền dữ liệu thay đổi theo khu vực địa lý và vị trí edge location.

#### Ví dụ Định Giá theo Khu Vực

- **Hoa Kỳ, Canada và Mexico**: $0.085/GB cho 10 TB đầu tiên
- **Ấn Độ**: $0.170/GB cho 10 TB đầu tiên (khoảng gấp 2 lần chi phí ở Mỹ)
- **Giảm giá theo Khối lượng**: Giá giảm khi lượng truyền dữ liệu tăng
  - Trên 5 PB được truyền từ Mỹ: $0.020/GB

**Nguyên tắc Chính**: Chi phí truyền dữ liệu tăng từ trái sang phải trên bảng giá, với một số khu vực đắt hơn đáng kể so với các khu vực khác.

### Các Lớp Giá CloudFront

Bạn có thể giảm chi phí bằng cách giới hạn số lượng edge location được sử dụng cho phân phối CloudFront của mình. Ba lớp giá có sẵn:

#### Lớp Giá All (Tất cả)
- **Phủ sóng**: Tất cả các khu vực trên toàn thế giới
- **Hiệu suất**: Hiệu suất tốt nhất
- **Chi phí**: Chi phí cao nhất (bao gồm các khu vực đắt tiền)

#### Lớp Giá 200
- **Phủ sóng**: Hầu hết các khu vực
- **Loại trừ**: Loại trừ các khu vực đắt nhất
- **Chi phí**: Tùy chọn chi phí trung bình

#### Lớp Giá 100
- **Phủ sóng**: Chỉ các khu vực rẻ nhất
- **Khu vực**: Châu Mỹ, Bắc Mỹ và Châu Âu
- **Chi phí**: Tùy chọn chi phí thấp nhất

---

## Nhiều Nguồn Gốc trong CloudFront

### Trường hợp Sử dụng: Định tuyến Dựa trên Nội dung

CloudFront cho phép bạn định tuyến đến các nguồn gốc khác nhau dựa trên loại nội dung hoặc mẫu đường dẫn.

### Ví dụ Cấu hình

Bạn có thể thiết lập các hành vi bộ nhớ cache khác nhau với các mẫu đường dẫn cụ thể:

- **`/images/*`** → S3 bucket cho hình ảnh tĩnh
- **`/api/*`** → Application Load Balancer cho các yêu cầu API
- **`/*`** (mặc định) → S3 bucket cho tất cả nội dung tĩnh khác

Điều này cho phép định tuyến hiệu quả trong đó:
- Các yêu cầu API đi đến Application Load Balancer của bạn
- Nội dung tĩnh được phục vụ từ các S3 bucket

---

## Nhóm Nguồn Gốc (Origin Groups)

### Mục đích

Nhóm nguồn gốc cung cấp tính khả dụng cao và chuyển đổi dự phòng tự động khi nguồn gốc chính bị lỗi.

### Kiến trúc

Một nhóm nguồn gốc bao gồm:
- **Nguồn Gốc Chính**: Lựa chọn đầu tiên để phục vụ yêu cầu
- **Nguồn Gốc Phụ**: Tùy chọn sao lưu để chuyển đổi dự phòng

### Cách Hoạt động

1. CloudFront gửi yêu cầu đến nguồn gốc chính
2. Nếu nguồn gốc chính trả về lỗi, CloudFront tự động thử lại yêu cầu với nguồn gốc phụ
3. Nguồn gốc phụ phản hồi với mã trạng thái thành công

### Ví dụ 1: Các EC2 Instance với Chuyển đổi Dự phòng

- **Nguồn Gốc Chính**: EC2 Instance A
- **Nguồn Gốc Phụ**: EC2 Instance B
- **Lợi ích**: Tính khả dụng cao ở cấp ứng dụng

### Ví dụ 2: S3 Đa Khu vực với Khôi phục Thảm họa

Kiến trúc này cung cấp tính khả dụng cao ở cấp khu vực:

**Thiết lập**:
- **Nguồn Gốc Chính**: S3 bucket ở Khu vực A
- **Nguồn Gốc Phụ**: S3 bucket ở Khu vực B
- **Sao chép**: Sao chép S3 giữa các khu vực

**Quy trình Chuyển đổi Dự phòng**:
1. CloudFront yêu cầu từ S3 bucket chính (Khu vực A)
2. Nếu xảy ra sự cố ở cấp khu vực, yêu cầu thất bại
3. CloudFront tự động yêu cầu từ S3 bucket phụ (Khu vực B)
4. Bucket phụ có dữ liệu được sao chép và phản hồi thành công

**Lợi ích**: Khôi phục thảm họa ở cấp khu vực cho kiến trúc CloudFront và S3

---

## Mã Hóa Cấp Trường (Field-Level Encryption)

### Mục đích

Mã hóa cấp trường bảo vệ thông tin nhạy cảm trong toàn bộ ngăn xếp ứng dụng, thêm một lớp bảo mật bổ sung ngoài mã hóa HTTPS trong quá trình truyền.

### Cách Hoạt động

- Sử dụng **mã hóa bất đối xứng**
- Edge location mã hóa các trường cụ thể bằng **khóa công khai**
- Chỉ các thực thể có **khóa riêng tư** mới có thể giải mã dữ liệu

### Cấu hình

- Chỉ định tối đa **10 trường** để mã hóa (ví dụ: số thẻ tín dụng)
- Cung cấp khóa công khai để mã hóa
- Áp dụng cho các yêu cầu POST được gửi đến CloudFront

### Ví dụ: Bảo vệ Thẻ Tín dụng

**Luồng Kiến trúc**:
1. **Client** → HTTPS → **Edge Location**
2. **Edge Location** → HTTPS → **CloudFront**
3. **CloudFront** → HTTPS → **Application Load Balancer**
4. **Application Load Balancer** → HTTPS → **Web Server**

**Quy trình Mã hóa**:

1. Người dùng gửi thông tin thẻ tín dụng qua HTTPS
2. Edge location mã hóa trường thẻ tín dụng bằng khóa công khai
3. Trường được mã hóa đi qua:
   - CloudFront
   - Application Load Balancer
   - Web Server
4. **Chỉ web server** (có khóa riêng tư) mới có thể giải mã trường

### Lợi ích Bảo mật

- **Bảo vệ end-to-end**: Dữ liệu nhạy cảm được mã hóa tại edge
- **Truy cập giải mã hạn chế**: Chỉ web server mới có thể giải mã
- **Phòng thủ nhiều lớp**: CloudFront và ALB không thể truy cập dữ liệu đã mã hóa
- **Logic ứng dụng tùy chỉnh**: Web server xử lý giải mã với khóa riêng tư

---

## Tóm tắt

Các tùy chọn nâng cao của CloudFront cung cấp:
- **Tối ưu hóa chi phí** thông qua lựa chọn lớp giá
- **Định tuyến linh hoạt** với nhiều nguồn gốc
- **Tính khả dụng cao** sử dụng nhóm nguồn gốc
- **Bảo mật nâng cao** với mã hóa cấp trường

Các tính năng này cho phép bạn xây dựng kiến trúc phân phối nội dung mạnh mẽ, hiệu quả về chi phí và an toàn trên AWS.




FILE: 89-aws-cloudfront-real-time-logs.md


# AWS CloudFront Real-Time Logs (Nhật Ký Thời Gian Thực)

## Tổng Quan

CloudFront Real-Time Logs cho phép bạn nhận tất cả các yêu cầu (requests) được gửi đến CloudFront theo thời gian thực bằng cách chuyển chúng đến Kinesis Data Stream. Tính năng này giúp bạn giám sát, phân tích và thực hiện các hành động dựa trên hiệu suất phân phối nội dung.

## Kiến Trúc

### Luồng Xử Lý Thời Gian Thực

1. **Người dùng** gửi yêu cầu đến **CloudFront**
2. Khi bật real-time logs, tất cả các yêu cầu sẽ được ghi lại vào **Kinesis Data Stream**
3. **Lambda function** có thể xử lý các bản ghi này từ Kinesis Data Stream để xử lý ngay lập tức

### Luồng Xử Lý Gần Thời Gian Thực

Đối với xử lý theo lô gần thời gian thực:

1. **Người dùng** gửi yêu cầu đến **CloudFront**
2. CloudFront gửi logs đến **Kinesis Data Stream** (CloudFront chỉ có thể gửi đến Kinesis Data Stream)
3. **Kinesis Data Firehose** xử lý các bản ghi theo lô (batches)
4. Dữ liệu được chuyển đến các đích như **Amazon S3**, **OpenSearch**, hoặc các đích được hỗ trợ khác

## Tính Năng Chính

### Tỷ Lệ Lấy Mẫu (Sampling Rate)

Bạn có thể cấu hình tỷ lệ lấy mẫu, giúp xác định tỷ lệ phần trăm các yêu cầu được gửi đến Kinesis Data Stream. Điều này đặc biệt hữu ích cho các API hoặc endpoint có lưu lượng truy cập cao, nơi việc ghi lại mọi yêu cầu có thể không cần thiết.

### Tùy Chỉnh Trường và Cache Behaviors

Real-time logs cho phép bạn chỉ định:

- **Những trường nào** sẽ được bao gồm trong logs
- **Cache behaviors hoặc path patterns nào** cần được giám sát

**Ví dụ**: Bạn có thể cấu hình logging chỉ ghi lại các yêu cầu khớp với path pattern `/images/*`, cho phép bạn tập trung vào các loại traffic cụ thể.

## Các Trường Hợp Sử Dụng

- **Giám sát hiệu suất**: Theo dõi các chỉ số phân phối nội dung theo thời gian thực
- **Phân tích bảo mật**: Phát hiện và phản ứng với các mẫu đáng ngờ
- **Phân tích lưu lượng truy cập**: Hiểu hành vi người dùng và các mẫu truy cập
- **Thông tin vận hành**: Đưa ra quyết định dựa trên dữ liệu yêu cầu thực tế

## Lợi Ích

- Khả năng hiển thị dữ liệu yêu cầu CloudFront theo thời gian thực
- Lấy mẫu linh hoạt để kiểm soát khối lượng dữ liệu
- Ghi log có chọn lọc dựa trên cache behaviors
- Tích hợp với các dịch vụ phân tích và xử lý của AWS




FILE: 9-amazon-elasticache-hands-on-tutorial.md


# Hướng Dẫn Thực Hành Amazon ElastiCache

## Giới Thiệu

Trong hướng dẫn thực hành này, chúng ta sẽ thực hành sử dụng Amazon ElastiCache bằng cách tạo và cấu hình một Redis cluster. Hướng dẫn này sẽ đưa bạn qua tất cả các tùy chọn cấu hình có sẵn khi thiết lập ElastiCache.

## Bắt Đầu

Khi bạn bắt đầu tạo ElastiCache cluster, bạn sẽ thấy một số engine được khuyến nghị:

- **Valkey** - Sự thay thế cho Redis (tùy chọn được khuyến nghị)
- **Memcached**
- **Redis OSS**

Trong hướng dẫn này, chúng ta sẽ sử dụng **Redis** vì nó cung cấp các tùy chọn giống như Valkey.

## Tùy Chọn Triển Khai

ElastiCache cung cấp hai tùy chọn triển khai:

1. **Serverless** - Tùy chọn được quản lý hoàn toàn
2. **Node-based cluster** - Kiểm soát nhiều hơn về cấu hình

Chúng ta sẽ chọn **node-based cluster** để hiểu chính xác cách mọi thứ hoạt động.

## Phương Pháp Cấu Hình

Bạn có thể cấu hình cluster của mình theo nhiều cách:

- **Restore from backup** - Sử dụng bản sao lưu hiện có
- **Easy create** - Sử dụng các phương pháp hay nhất được khuyến nghị
  - Cấu hình Production
  - Cấu hình Dev/Test
  - Cấu hình Demo
- **Custom configuration** - Cấu hình thủ công mọi thứ

Trong hướng dẫn này, chúng ta sẽ sử dụng **custom configuration** để xem tất cả các tùy chọn có sẵn.

## Chế Độ Cluster

### Chế Độ Cluster Bị Vô Hiệu Hóa (Cluster Mode Disabled)
- Một shard duy nhất với một primary node
- Lên đến 5 read replica
- Phù hợp cho các triển khai đơn giản hơn

### Chế Độ Cluster Được Kích Hoạt (Cluster Mode Enabled)
- Nhiều shard trên nhiều server
- Tốt hơn cho khả năng mở rộng

Trong hướng dẫn này, chúng ta sẽ sử dụng **cluster mode disabled**.

## Cấu Hình Cơ Bản

### Cài Đặt Cluster
- **Tên Cluster**: DemoCluster
- **Vị trí**: AWS Cloud (cũng có thể chạy on-premises sử dụng AWS Outpost)

### Tùy Chọn Tính Khả Dụng Cao
- **Multi-AZ**: Vô hiệu hóa (để giảm chi phí cho demo này)
  - Cung cấp tính khả dụng cao và failover
  - Hữu ích trong trường hợp primary node lỗi
- **Auto-failover**: Được kích hoạt

### Cấu Hình Engine
- Phiên bản engine (chỉ định theo nhu cầu)
- Cấu hình cổng
- Parameter groups

## Chọn Loại Node

Trong hướng dẫn này, chúng ta sẽ sử dụng **micro instance type**:

- **t2.micro** (Đủ điều kiện Free tier)
- **t3.micro** (Đủ điều kiện Free tier)
- **t4g.micro**

Chúng ta sẽ chọn **t2.micro** để tối ưu hóa chi phí.

## Cấu Hình Replica

- **Số lượng replica**: 0 (để tiết kiệm chi phí)
- Lưu ý: Khi sử dụng Multi-AZ, bạn nên có nhiều replica hơn để có tính khả dụng tốt hơn

## Cấu Hình Mạng

### Subnet Group
- **Tên**: my-first-subnet-group
- Chỉ ra subnet nào mà ElastiCache có thể chạy
- Chọn VPC
- Subnet được chọn tự động (có thể chỉ định thủ công)

### Vị Trí Availability Zone
- Chỉ định replica nào đi đến AZ nào
- Không quan trọng khi không chạy chế độ Multi-AZ

## Cấu Hình Bảo Mật

### Mã Hóa Khi Lưu Trữ (Encryption at Rest)
- Kích hoạt/vô hiệu hóa theo nhu cầu
- Yêu cầu chỉ định key nếu được kích hoạt

### Mã Hóa Khi Truyền Tải (Encryption in Transit)
- Mã hóa dữ liệu giữa client và server
- Kích hoạt tính năng kiểm soát truy cập khi được bật:
  - **Redis AUTH**: Chỉ định password/AUTH token để kết nối
  - **User group access control list**: Tạo user group từ ElastiCache console

Trong hướng dẫn này, chúng ta sẽ **vô hiệu hóa encryption in transit**.

### Security Groups
- Quản lý ứng dụng nào có quyền truy cập mạng vào cluster của bạn

## Cấu Hình Sao Lưu

- Kích hoạt hoặc vô hiệu hóa sao lưu tự động
- Cấu hình thời gian lưu trữ backup theo nhu cầu

## Cấu Hình Bảo Trì

- **Maintenance windows**: Lên lịch cho các bản nâng cấp phiên bản nhỏ
- **Logs**: Cấu hình slow logs hoặc engine logs
  - Có thể được gửi đến CloudWatch Logs

## Gắn Tag

- Thêm tag để tổ chức tài nguyên và theo dõi chi phí

## Tạo Cluster

Sau khi xem xét tất cả các tùy chọn cấu hình:

1. Xem lại tất cả các cài đặt
2. Nhấp **Create** để tạo cache

## Sử Dụng ElastiCache Cluster

Khi ElastiCache database của bạn được tạo:

1. Nhấp vào cluster để xem chi tiết
2. Sử dụng **primary endpoint** cho các thao tác ghi
3. Sử dụng **reader endpoint** cho các thao tác đọc (nếu sử dụng read replica)

## Tính Năng Console

Từ AWS ElastiCache console, bạn có thể xem:

- Chi tiết cluster
- Thông tin nodes
- Metrics
- Logs
- Cài đặt bảo mật mạng

Giao diện console tương tự như RDS, vì ElastiCache chia sẻ nhiều khái niệm với RDS nhưng được thiết kế đặc biệt cho Redis và Memcached.

## Kết Nối Đến Redis

**Lưu ý**: Kết nối đến Redis cache yêu cầu viết mã ứng dụng và nằm ngoài phạm vi của hướng dẫn dựa trên console này. Tuy nhiên, bạn sẽ sử dụng các endpoint được cung cấp trong console để thiết lập kết nối từ ứng dụng của bạn.

## Dọn Dẹp

Để xóa Redis cluster của bạn:

1. Chọn cluster
2. Nhấp **Actions** → **Delete**
3. Chọn có tạo backup cuối cùng hay không (Không cho demo này)
4. Nhập tên cluster để xác nhận
5. Nhấp **Delete**

## Kết Luận:

Hướng dẫn thực hành này đã đề cập đến tất cả các tùy chọn cấu hình thiết yếu để tạo Amazon ElastiCache cluster. Dịch vụ này tương tự như RDS nhưng được tối ưu hóa cho bộ nhớ đệm in-memory với Redis và Memcached engines.

## Những Điểm Chính Cần Nhớ

- ElastiCache hỗ trợ nhiều engine: Valkey, Redis, và Memcached
- Cluster mode có thể bị vô hiệu hóa (single shard) hoặc được kích hoạt (multiple shards)
- Multi-AZ cung cấp tính khả dụng cao nhưng tăng chi phí
- Các tùy chọn mã hóa có sẵn cho cả at rest và in transit
- Security groups và access control lists quản lý quyền truy cập
- Giao diện console tương tự như RDS
- Luôn nhớ xóa tài nguyên khi hoàn thành để tránh chi phí không cần thiết


