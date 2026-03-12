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