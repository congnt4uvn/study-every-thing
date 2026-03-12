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