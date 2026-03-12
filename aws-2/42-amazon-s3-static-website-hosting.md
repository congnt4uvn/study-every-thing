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