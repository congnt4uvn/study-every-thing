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