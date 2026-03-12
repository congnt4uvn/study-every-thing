# Quản Lý Lifecycle và Storage Classes trên AWS S3

## Tổng Quan

Hướng dẫn này trình bày cách di chuyển objects giữa các storage classes khác nhau trên Amazon S3 bằng cách sử dụng transitions và lifecycle rules để tối ưu hóa chi phí và quản lý dữ liệu.

## Chuyển Đổi Storage Classes

### Các Đường Chuyển Đổi Khả Dụng

Bạn có thể chuyển đổi objects giữa các storage classes theo các đường sau:

- **Standard** → **Standard-IA** → **Intelligent-Tiering** → **One-Zone IA**
- **One-Zone IA** → **Glacier Flexible Retrieval** hoặc **Glacier Deep Archive**

### Thực Hành Tốt Nhất

- Nếu objects sẽ được **truy cập không thường xuyên**, hãy chuyển chúng sang **Standard-IA**
- Để **lưu trữ dài hạn**, hãy chuyển objects sang **Glacier tiers** hoặc **Deep Archive**

## Lifecycle Rules

### Lifecycle Rules là gì?

Lifecycle rules tự động hóa quá trình chuyển đổi hoặc xóa objects, loại bỏ nhu cầu quản lý thủ công.

### Các Loại Actions

#### 1. Transition Actions

Cấu hình objects tự động chuyển sang storage class khác:

- Chuyển sang **Standard-IA** sau 60 ngày tạo
- Chuyển sang **Glacier** để lưu trữ sau 6 tháng

#### 2. Expiration Actions

Cấu hình objects tự động bị xóa sau một khoảng thời gian:

- Xóa access log files sau 365 ngày
- Xóa các phiên bản cũ của files (khi bật versioning)
- Dọn dẹp incomplete multi-part uploads sau 2 tuần

### Cấu Hình Rules

Lifecycle rules có thể được cấu hình dựa trên:

- **Prefix**: Áp dụng cho toàn bộ bucket hoặc các đường dẫn cụ thể
- **Object Tags**: Nhắm mục tiêu các objects được tag cụ thể (ví dụ: department: finance)

## Kịch Bản Thực Tế

### Kịch Bản 1: Quản Lý Ảnh Thumbnail

**Yêu Cầu:**
- Ứng dụng EC2 tạo thumbnails từ ảnh profile được upload
- Thumbnails có thể dễ dàng tạo lại và chỉ cần giữ trong 60 ngày
- Ảnh gốc phải có thể truy xuất ngay lập tức trong 60 ngày
- Sau 60 ngày, người dùng có thể chờ tới 6 giờ để lấy ảnh gốc

**Giải Pháp:**
- **Ảnh gốc**: Sử dụng class **Standard** với lifecycle rule chuyển sang **Glacier** sau 60 ngày
- **Ảnh thumbnail**: Sử dụng **One-Zone IA** (truy cập không thường xuyên, dễ tạo lại) với expiration rule xóa sau 60 ngày
- Sử dụng **prefixes** để phân biệt giữa ảnh gốc và thumbnail

### Kịch Bản 2: Khôi Phục Objects Đã Xóa

**Yêu Cầu:**
- Khôi phục objects đã xóa ngay lập tức trong 30 ngày (hiếm khi xảy ra)
- Khôi phục objects đã xóa trong vòng 48 giờ cho tới 365 ngày

**Giải Pháp:**
- Bật **S3 Versioning** để bảo toàn các phiên bản của object
- Objects đã xóa được ẩn bởi delete marker và có thể khôi phục
- Tạo lifecycle rules để:
  - Chuyển **non-current versions** sang **Standard-IA**
  - Chuyển non-current versions sang **Glacier Deep Archive** để lưu trữ dài hạn

## Amazon S3 Analytics

### Mục Đích

S3 Analytics giúp xác định số ngày tối ưu để chuyển đổi objects giữa các storage classes.

### Tính Năng

- Cung cấp đề xuất cho các class **Standard** và **Standard-IA**
- Không hỗ trợ One-Zone IA hoặc Glacier
- Tạo **CSV report** với các đề xuất và thống kê
- Report được cập nhật **hàng ngày**
- Phân tích dữ liệu ban đầu mất **24-48 giờ** để xuất hiện

### Trường Hợp Sử Dụng

Sử dụng S3 Analytics làm bước đầu tiên để:
- Tạo các lifecycle rules hiệu quả
- Tối ưu hóa các rules hiện có dựa trên mô hình sử dụng thực tế

## Các Điểm Chính Cần Nhớ

- Tự động hóa chuyển đổi storage class bằng lifecycle rules
- Sử dụng storage classes phù hợp dựa trên mô hình truy cập
- Tận dụng versioning cho các kịch bản khôi phục dữ liệu
- Sử dụng S3 Analytics để ra quyết định lifecycle dựa trên dữ liệu
- Cân nhắc sử dụng object prefixes và tags cho việc áp dụng rules chi tiết

## Tóm Tắt

Lifecycle management trên S3 là công cụ mạnh mẽ giúp tối ưu hóa chi phí lưu trữ trong khi vẫn đáp ứng các yêu cầu về khả năng truy cập và tuân thủ. Bằng cách hiểu rõ các storage classes và cách cấu hình lifecycle rules, bạn có thể tự động hóa quản lý dữ liệu một cách hiệu quả.

---

*Tài liệu này dựa trên các thực hành tốt nhất của AWS S3 cho quản lý storage class và tối ưu hóa lifecycle.*