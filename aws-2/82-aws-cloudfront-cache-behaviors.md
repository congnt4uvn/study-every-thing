# AWS CloudFront Cache Behaviors (Hành Vi Cache)

## Tổng Quan

Cache behaviors trong CloudFront cho phép bạn cấu hình các nguồn gốc (origins) và chiến lược lưu trữ khác nhau cho các mẫu đường dẫn URL khác nhau. Điều này mang lại sự linh hoạt trong việc định tuyến yêu cầu dựa trên loại nội dung hoặc mẫu đường dẫn.

## Hiểu Về Cache Behaviors

Cache behaviors cho phép bạn:
- Định nghĩa các nguồn gốc khác nhau cho các mẫu đường dẫn URL khác nhau
- Định tuyến đến các nhóm nguồn gốc khác nhau dựa trên loại nội dung hoặc đường dẫn
- Triển khai các chiến lược lưu trữ cụ thể cho các loại nội dung khác nhau

### Ví Dụ Định Tuyến Theo Mẫu Đường Dẫn

Bạn có thể cấu hình CloudFront để định tuyến các yêu cầu như sau:
- `/images/*` → Amazon S3
- `/api/*` → Nguồn gốc ứng dụng của bạn
- `/*` → Nguồn gốc mặc định (default cache behavior)

## Cấu Hình Cache Behavior

### Ví Dụ Nhiều Cache Behaviors

Xét một phân phối CloudFront với hai cache behaviors:

1. **Cache Behavior `/api/*`**
   - Định tuyến đến nguồn gốc Application Load Balancer
   - Xử lý các yêu cầu API

2. **Cache Behavior Mặc Định `/*`**
   - Luôn được xử lý cuối cùng
   - Định tuyến đến S3 bucket làm nguồn gốc
   - Hoạt động như phương án dự phòng cho các mẫu không khớp

### Thứ Tự Xử Lý

Khi bạn thêm các cache behaviors bổ sung:
- CloudFront kiểm tra khớp cụ thể nhất trước
- Cache behavior mặc định (`/*`) luôn được xử lý cuối cùng
- Nếu không tìm thấy khớp cụ thể, CloudFront quay về cache behavior mặc định

## Các Trường Hợp Sử Dụng

### Trường Hợp 1: Kiểm Soát Truy Cập Với Signed Cookies

Triển khai xác thực để kiểm soát quyền truy cập vào nội dung S3 bucket:

1. **Cache Behavior Đăng Nhập** (`/login`)
   - Định tuyến đến EC2 instance
   - EC2 instance tạo CloudFront signed cookies
   - Signed cookies được gửi lại cho người dùng

2. **Cache Behavior Mặc Định** (tất cả các URL khác)
   - Yêu cầu signed cookies phải có mặt
   - Cung cấp quyền truy cập vào các tệp trong S3 bucket
   - Chuyển hướng đến `/login` nếu thiếu cookies

Phương pháp này đảm bảo người dùng phải xác thực trước khi truy cập nội dung được bảo vệ.

### Trường Hợp 2: Tối Đa Hóa Tỷ Lệ Cache Hit

Tối ưu hóa caching bằng cách tách riêng nội dung tĩnh và động:

1. **Nội Dung Tĩnh** (Amazon S3)
   - Không có chính sách cache với headers hoặc sessions
   - Tối đa hóa cache hit chỉ dựa trên tài nguyên được yêu cầu
   - Lý tưởng cho hình ảnh, CSS, tệp JavaScript

2. **Nội Dung Động** (REST HTTP Server qua ALB/EC2)
   - Cache dựa trên headers và cookies phù hợp
   - Sử dụng chính sách cache đã định nghĩa cho các phản hồi động
   - Cân bằng giữa caching và nhu cầu cá nhân hóa

## Thực Hành Tốt Nhất

- Cấu hình các cache behaviors cụ thể cho các loại nội dung khác nhau
- Sử dụng cache behavior mặc định làm phương án dự phòng
- Tận dụng signed cookies để kiểm soát truy cập khi cần thiết
- Tách riêng nội dung tĩnh và động để tối ưu hiệu suất cache
- Xem xét thứ tự xử lý khi định nghĩa nhiều cache behaviors

## Tóm Tắt

CloudFront cache behaviors cung cấp khả năng định tuyến và caching mạnh mẽ cho phép bạn tối ưu hóa phân phối nội dung dựa trên nhu cầu cụ thể của ứng dụng. Bằng cách cấu hình cache behaviors đúng cách, bạn có thể cải thiện hiệu suất, triển khai kiểm soát truy cập và tối đa hóa hiệu quả cache.