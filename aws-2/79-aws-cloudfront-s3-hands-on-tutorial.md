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