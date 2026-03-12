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