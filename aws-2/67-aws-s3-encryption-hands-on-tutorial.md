# AWS S3 Encryption - Hướng Dẫn Thực Hành

## Tổng Quan

Hướng dẫn thực hành này sẽ trình bày cách triển khai và quản lý các tùy chọn mã hóa khác nhau cho Amazon S3 bucket. Bạn sẽ học cách cấu hình mã hóa phía máy chủ (server-side encryption) sử dụng SSE-S3, SSE-KMS và DSSE-KMS.

## Yêu Cầu Trước Khi Bắt Đầu

- Quyền truy cập AWS Console
- Hiểu biết cơ bản về Amazon S3
- Các tệp mẫu để tải lên (ví dụ: coffee.jpg, beach.jpg)

## Các Bước Thực Hành

### Bước 1: Tạo S3 Bucket với Mã Hóa Mặc Định

1. **Tạo bucket mới**
   - Tên bucket: `demo-encryption-stephane-v2`
   - Điều hướng qua trình hướng dẫn tạo bucket

2. **Kích hoạt bucket versioning**
   - Cho phép theo dõi các phiên bản khác nhau của đối tượng với các cài đặt mã hóa khác nhau
   - Giữ tùy chọn này được bật

3. **Cấu hình mã hóa mặc định**
   - Trong phần cài đặt "Default encryption"
   - Có ba tùy chọn mã hóa (phải chọn một):
     - **SSE-S3**: Mã hóa phía máy chủ với khóa do Amazon S3 quản lý
     - **SSE-KMS**: Mã hóa phía máy chủ với AWS Key Management Service
     - **DSSE-KMS**: Mã hóa hai lớp phía máy chủ với KMS
   - Chọn **SSE-S3** cho thiết lập ban đầu

4. **Tạo bucket**
   - Nhấp "Create bucket"
   - Bucket hiện đã được tạo với mã hóa mặc định được kích hoạt

### Bước 2: Tải Lên và Xác Minh Mã Hóa

1. **Tải lên một tệp**
   - Nhấp "Add file"
   - Chọn `coffee.jpg`
   - Nhấp "Upload"

2. **Xác minh cài đặt mã hóa**
   - Nhấp vào tệp đã tải lên
   - Cuộn xuống phần "Server-side encryption settings"
   - Xác nhận tệp được mã hóa với **SSE-S3** (khóa do Amazon S3 quản lý)

### Bước 3: Thay Đổi Mã Hóa cho Một Đối Tượng

1. **Chỉnh sửa cài đặt mã hóa**
   - Chọn tệp đã tải lên
   - Nhấp "Edit"
   - Lưu ý: Chỉnh sửa mã hóa phía máy chủ sẽ tạo một phiên bản mới của đối tượng

2. **Ghi đè mã hóa mặc định của bucket**
   - Chọn ghi đè mã hóa mặc định của bucket
   - Chọn loại mã hóa: **SSE-KMS** (hoặc DSSE-KMS)

3. **Về DSSE-KMS**
   - Cung cấp hai lớp mã hóa trên KMS
   - Mã hóa mạnh hơn so với KMS tiêu chuẩn
   - Trong hướng dẫn này, chúng ta sẽ sử dụng **SSE-KMS** tiêu chuẩn

4. **Chỉ định khóa KMS**
   - Tùy chọn 1: Nhập ARN của khóa KMS
   - Tùy chọn 2: Chọn từ các khóa KMS hiện có
   - Chọn khóa **AWS/S3** (khóa KMS mặc định cho dịch vụ S3)
   - Khóa mặc định này không phát sinh chi phí bổ sung
   - Lưu ý: Khóa KMS tùy chỉnh sẽ phát sinh phí hàng tháng

5. **Lưu thay đổi**
   - Nhấp "Save changes"

### Bước 4: Xác Minh Versioning và Mã Hóa Mới

1. **Kiểm tra các phiên bản đối tượng**
   - Điều hướng đến tab "Versions"
   - Bạn sẽ thấy hai phiên bản của tệp

2. **Xác minh mã hóa phiên bản hiện tại**
   - Chọn phiên bản hiện tại
   - Cuộn xuống phần "Server-side encryption"
   - Xác nhận loại mã hóa: **SSE-KMS**
   - Xác minh khóa mã hóa khớp với khóa AWS/S3 KMS mặc định

### Bước 5: Tải Lên với Cài Đặt Mã Hóa Tùy Chỉnh

1. **Tải lên tệp mới**
   - Nhấp "Add file"
   - Chọn `beach.jpg`

2. **Cấu hình mã hóa trong quá trình tải lên**
   - Trong phần "Properties"
   - Tìm "Server-side encryption"
   - Chọn tùy chọn mã hóa:
     - Sử dụng cơ chế mã hóa mặc định, hoặc
     - Ghi đè với SSE-S3, SSE-KMS, hoặc DSSE-KMS

### Bước 6: Sửa Đổi Mã Hóa Mặc Định của Bucket

1. **Truy cập cài đặt mã hóa mặc định**
   - Điều hướng đến cài đặt bucket
   - Cuộn xuống "Default encryption"
   - Nhấp "Edit"

2. **Các tùy chọn mã hóa có sẵn**
   - **SSE-S3**: Khóa do Amazon S3 quản lý
   - **SSE-KMS**: AWS Key Management Service
   - **DSSE-KMS**: Mã hóa hai lớp với KMS

3. **Tùy chọn Bucket Key (cho SSE-KMS/DSSE-KMS)**
   - Có sẵn khi sử dụng mã hóa KMS
   - Giảm chi phí bằng cách tối thiểu hóa các lệnh gọi API đến AWS KMS
   - Được bật theo mặc định
   - Không áp dụng cho SSE-S3

## Tổng Kết Các Tùy Chọn Mã Hóa

### Có Sẵn Trong Console

- **SSE-S3**: Mã hóa phía máy chủ với khóa do Amazon S3 quản lý
- **SSE-KMS**: Mã hóa phía máy chủ với AWS KMS
- **DSSE-KMS**: Mã hóa hai lớp phía máy chủ với AWS KMS

### Không Có Sẵn Trong Console

- **SSE-C**: Mã hóa phía máy chủ với khóa do khách hàng cung cấp
  - Chỉ có thể cấu hình qua AWS CLI
  - Không có sẵn trong AWS Console

- **Client-Side Encryption (Mã hóa phía client)**
  - Dữ liệu được mã hóa ở phía client trước khi tải lên
  - Dữ liệu được giải mã ở phía client sau khi tải xuống
  - Không cần thông báo cho AWS về mã hóa phía client
  - AWS xử lý nó như dữ liệu thông thường

## Những Điểm Chính Cần Ghi Nhớ

1. **Mã hóa mặc định là bắt buộc** - Bạn phải chọn một phương thức mã hóa mặc định cho tất cả các S3 bucket

2. **Ghi đè mã hóa ở cấp độ đối tượng** - Bạn có thể ghi đè mã hóa mặc định của bucket cho từng đối tượng riêng lẻ

3. **Versioning theo dõi các thay đổi mã hóa** - Thay đổi mã hóa của đối tượng sẽ tạo một phiên bản mới

4. **Cân nhắc về chi phí**:
   - Khóa AWS/S3 KMS mặc định là miễn phí
   - Khóa KMS tùy chỉnh phát sinh phí hàng tháng
   - Tùy chọn Bucket Key giảm chi phí API KMS

5. **Giới hạn của Console**:
   - SSE-C yêu cầu AWS CLI
   - Mã hóa phía client được xử lý độc lập

## Kết Luận

Bạn đã học thành công cách cấu hình và quản lý các tùy chọn mã hóa khác nhau trong Amazon S3, bao gồm SSE-S3, SSE-KMS và DSSE-KMS. Hiểu rõ các cơ chế mã hóa này là rất quan trọng để bảo mật dữ liệu của bạn trong AWS.

## Các Bước Tiếp Theo

- Khám phá mã hóa SSE-C sử dụng AWS CLI
- Triển khai mã hóa phía client trong ứng dụng của bạn
- Tìm hiểu về chính sách và quyền của khóa KMS
- Thực hành với các kịch bản mã hóa khác nhau