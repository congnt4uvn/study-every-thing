# AWS CloudFront Edge Functions - Tài Liệu Học Tập

## Tổng Quan

Tài liệu này đề cập đến **Tùy Chỉnh Tại Edge** trong AWS, tập trung vào CloudFront Edge Functions.

## Tùy Chỉnh Tại Edge Là Gì?

Tùy chỉnh tại Edge nghĩa là thực thi logic tại các vị trí Edge của CloudFront trước khi yêu cầu đến ứng dụng chính của bạn. Cách tiếp cận này giảm thiểu độ trễ bằng cách chạy code gần người dùng trên toàn cầu.

## Edge Functions

**Edge Functions** là những đoạn code mà bạn viết và gắn vào CloudFront distributions. Chúng cho phép bạn tùy chỉnh phân phối nội dung và thêm logic mà không cần quản lý server.

### Các Loại Edge Functions

AWS CloudFront cung cấp hai loại Edge Functions:

1. **CloudFront Functions**
2. **Lambda@Edge**

Cả hai đều:
- **Serverless** - Không cần quản lý server
- **Triển khai toàn cầu** - Chạy tại các vị trí Edge trên toàn thế giới
- **Trả theo sử dụng** - Chỉ trả tiền cho những gì bạn sử dụng

## Các Trường Hợp Sử Dụng

Edge Functions cho phép nhiều tùy chỉnh khác nhau cho ứng dụng hiện đại:

### Bảo Mật & Quyền Riêng Tư
- Tăng cường bảo mật website và quyền riêng tư
- Giảm thiểu bot tại Edge
- Xác thực và phân quyền người dùng

### Hiệu Suất & Tối Ưu Hóa
- Ứng dụng web động tại Edge
- Chuyển đổi hình ảnh thời gian thực
- Định tuyến thông minh giữa các origins và data centers

### Trải Nghiệm Người Dùng
- Tối ưu hóa công cụ tìm kiếm (SEO)
- Kiểm thử A/B
- Ưu tiên người dùng
- Theo dõi và phân tích người dùng

### Phân Phối Nội Dung
- Tùy chỉnh nội dung CDN từ CloudFront

## CloudFront Functions Hoạt Động Như Thế Nào

### Luồng Yêu Cầu

1. **Viewer Request**: Client gửi yêu cầu đến CloudFront
2. **Origin Request**: CloudFront chuyển tiếp yêu cầu đến origin server
3. Edge Functions có thể chặn và sửa đổi yêu cầu tại nhiều điểm khác nhau trong luồng này

## Lợi Ích Chính

- ✅ Không cần quản lý server
- ✅ Triển khai toàn cầu
- ✅ Độ trễ tối thiểu
- ✅ Hiệu quả về chi phí (trả theo sử dụng)
- ✅ Kiến trúc serverless hoàn toàn

## Mẹo Học Tập

- Hiểu sự khác biệt giữa CloudFront Functions và Lambda@Edge
- Biết khi nào sử dụng Edge Functions so với regional functions
- Thực hành xác định các trường hợp sử dụng phù hợp cho tùy chỉnh Edge
- Học luồng request/response trong CloudFront

## Khái Niệm Quan Trọng Cần Nhớ

- Edge Functions chạy **gần người dùng** để giảm thiểu độ trễ
- Chúng được gắn vào **CloudFront distributions**
- Hai loại: **CloudFront Functions** và **Lambda@Edge**
- Nhiều trường hợp sử dụng từ bảo mật đến tối ưu hóa
