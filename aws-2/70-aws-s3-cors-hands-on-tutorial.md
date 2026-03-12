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