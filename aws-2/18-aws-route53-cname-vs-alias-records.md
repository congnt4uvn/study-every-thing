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