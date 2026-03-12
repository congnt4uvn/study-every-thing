# Mã Hóa Hai Lớp Phía Máy Chủ Amazon S3 với DSSE-KMS

## Tổng Quan

DSSE-KMS là một tùy chọn mã hóa mới có sẵn trong Amazon S3, được phát hành vào tháng 6 năm 2023. DSSE-KMS là viết tắt của **"mã hóa kép dựa trên KMS"** (Key Management Service).

## DSSE-KMS Là Gì?

Mã hóa hai lớp phía máy chủ Amazon S3 với các khóa được lưu trữ trong AWS Key Management Service (DSSE-KMS) là một tùy chọn mã hóa mới áp dụng **hai lớp mã hóa** cho các đối tượng khi chúng được tải lên S3 bucket.

### Tính Năng Chính

- **Tuân Thủ**: Được thiết kế để đáp ứng National Security Agency CNSSP 15 cho tuân thủ FIPS và hướng dẫn Data-at-Rest Capability Package (DAR CP) Phiên bản 5.0 cho hai lớp mã hóa CNSA
- **Khả Năng Độc Đáo**: Amazon S3 là dịch vụ lưu trữ đối tượng đám mây duy nhất cho phép khách hàng áp dụng hai lớp mã hóa ở cấp độ đối tượng và kiểm soát các khóa dữ liệu được sử dụng cho cả hai lớp
- **Đối Tượng Mục Tiêu**: Giúp khách hàng có quy định cao dễ dàng đáp ứng các tiêu chuẩn bảo mật nghiêm ngặt, chẳng hạn như khách hàng Bộ Quốc phòng Hoa Kỳ (DoD)

## Cách Hoạt Động Của DSSE-KMS

### Triển Khai Mã Hóa

- Mỗi lớp mã hóa sử dụng một **thư viện triển khai mật mã riêng biệt** với các khóa mã hóa dữ liệu riêng lẻ
- Mỗi lớp sử dụng một triển khai khác nhau của thuật toán **Advanced Encryption Standard 256-bit với Galois Counter Mode (AES-GCM)**
- DSSE-KMS giúp bảo vệ dữ liệu nhạy cảm khỏi khả năng thấp về lỗ hổng trong một lớp triển khai mật mã duy nhất

### Quản Lý Khóa

- Sử dụng AWS Key Management Service (AWS KMS) để tạo các khóa dữ liệu
- Cho phép bạn kiểm soát các khóa được quản lý bởi khách hàng bằng cách đặt quyền cho mỗi khóa
- Hỗ trợ chỉ định lịch trình luân chuyển khóa

### Tùy Chọn Cấu Hình

Bạn có thể bật DSSE-KMS theo nhiều cách:
- Chỉ định mã hóa hai lớp phía máy chủ (DSSE) trong yêu cầu PUT hoặc COPY cho một đối tượng
- Cấu hình S3 bucket của bạn để áp dụng DSSE cho tất cả các đối tượng mới theo mặc định
- Thực thi DSSE-KMS bằng cách sử dụng chính sách IAM và bucket

## Các Tùy Chọn Mã Hóa Phía Máy Chủ của Amazon S3

Với bản phát hành này, Amazon S3 hiện cung cấp **bốn tùy chọn** cho mã hóa phía máy chủ:

1. **SSE-S3**: Mã hóa phía máy chủ với các khóa được quản lý bởi Amazon S3
2. **SSE-KMS**: Mã hóa phía máy chủ với AWS KMS
3. **SSE-C**: Mã hóa phía máy chủ với các khóa mã hóa do khách hàng cung cấp
4. **DSSE-KMS**: Mã hóa hai lớp phía máy chủ với các khóa được lưu trữ trong KMS

## Hướng Dẫn Thực Hành

### Bước 1: Tạo S3 Bucket và Bật DSSE-KMS

1. Trong bảng điều khiển Amazon S3, chọn **Buckets** trong ngăn điều hướng
2. Chọn **Create bucket**
3. Chọn một tên duy nhất và có ý nghĩa cho bucket
4. Trong phần **Default encryption**, chọn **DSSE-KMS** làm tùy chọn mã hóa
5. Từ các khóa AWS KMS có sẵn, chọn một khóa phù hợp với yêu cầu của bạn
6. Chọn **Create bucket** để hoàn tất việc tạo

### Bước 2: Tải Lên Đối Tượng vào S3 Bucket Đã Bật DSSE-KMS

1. Trong danh sách Buckets, chọn tên của bucket bạn muốn tải đối tượng lên
2. Trên tab **Objects** cho bucket, chọn **Upload**
3. Trong **Files and folders**, chọn **Add files**
4. Chọn một tệp để tải lên, sau đó chọn **Open**
5. Trong **Server-side encryption**, chọn **Do not specify an encryption key**
6. Chọn **Upload**

**Kết Quả**: Sau khi đối tượng được tải lên S3 bucket, đối tượng đã tải lên sẽ kế thừa cài đặt mã hóa phía máy chủ từ bucket.

### Bước 3: Tải Xuống Đối Tượng Được Mã Hóa DSSE-KMS

1. Chọn đối tượng mà bạn đã tải lên trước đó
2. Chọn **Download** hoặc chọn **Download as** từ menu Object actions
3. Sau khi đối tượng được tải xuống, mở nó cục bộ

**Kết Quả**: Đối tượng được giải mã tự động, không yêu cầu thay đổi ứng dụng khách.

## Lợi Ích

- **Quy Trình Đơn Giản**: Đơn giản hóa quy trình áp dụng hai lớp mã hóa cho dữ liệu của bạn mà không cần đầu tư vào cơ sở hạ tầng cần thiết cho mã hóa phía khách hàng
- **Phân Tích Dữ Liệu**: Bạn có thể truy vấn và phân tích dữ liệu được mã hóa kép của mình với các dịch vụ AWS như Amazon Athena, Amazon SageMaker, và nhiều hơn nữa
- **Tuân Thủ Quy Định**: Giúp đáp ứng các yêu cầu quy định để áp dụng nhiều lớp mã hóa cho dữ liệu của bạn

## Tính Khả Dụng và Giá Cả

- **Tính Khả Dụng**: Có sẵn trong tất cả các AWS Regions
- **Giá Cả**: Để biết thông tin về giá DSSE-KMS, hãy truy cập [trang giá Amazon S3](https://aws.amazon.com/s3/pricing/) (tab Storage) và [trang giá AWS KMS](https://aws.amazon.com/kms/pricing/)

## Bắt Đầu

Bạn có thể bắt đầu với DSSE-KMS thông qua:
- AWS CLI
- AWS Management Console

Để biết thêm thông tin, hãy truy cập [Hướng dẫn Sử dụng Amazon S3](https://docs.aws.amazon.com/s3/).

---

*Tác giả: Irshad*