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