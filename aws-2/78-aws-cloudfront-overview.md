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