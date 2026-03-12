# AWS CloudFront Cache Behaviors và Invalidations

## Tổng quan

Hướng dẫn này trình bày cách cấu hình cache behaviors trong AWS CloudFront và cách quản lý cache invalidations để đảm bảo nội dung cập nhật được phân phối đúng cách.

## Hiểu về Cache Behaviors

### Default Behavior (Hành vi Mặc định)

CloudFront distributions đi kèm với cache behavior mặc định áp dụng cho toàn bộ nội dung:

- Behavior mặc định sử dụng path pattern wildcard (`*`)
- Path pattern không thể chỉnh sửa đối với behavior mặc định
- Bạn có thể cấu hình cache key và origin request settings

### Cấu hình Cache Policy

Khi tạo cache policy (ví dụ: `DemoCachePolicy`), bạn có thể kiểm soát:

#### Cài đặt Time to Live (TTL)

- **Minimum TTL**: Thời gian tối thiểu các object được lưu trong cache
- **Maximum TTL**: Thời gian tối đa các object được lưu trong cache
- **Default TTL**: Thời gian cache mặc định

#### Cài đặt Cache Key

Bạn có thể chỉ định các thành phần nào được bao gồm trong cache key:

1. **Headers**
   - Chọn từ danh sách headers được định nghĩa sẵn
   - Thêm custom headers nếu cần

2. **Query Strings**
   - Bao gồm tất cả query strings
   - Hoặc chọn các query strings cụ thể từ danh sách

3. **Cookies**
   - Bao gồm tất cả cookies
   - Hoặc chỉ định danh sách các cookies cụ thể

Dữ liệu sẽ được cache dựa trên các cài đặt này cho headers, query strings và cookies.

### Origin Request Policy

Ngoài cache policy, bạn có thể tạo origin request policy (ví dụ: `DemoOriginPolicy`) để truyền thêm dữ liệu tới origin mà không phải là một phần của cache key:

- Headers bổ sung
- Query strings bổ sung
- Cookies bổ sung

Điều này cho phép bạn tăng cường origin request vượt ra ngoài những gì được sử dụng cho caching.

## Tạo Nhiều Cache Behaviors

Bạn có thể tạo nhiều cache behaviors để xử lý các loại nội dung khác nhau:

1. Tạo behavior mới với path pattern cụ thể (ví dụ: `/images/*`)
2. Định tuyến requests tới origin khác (S3 bucket, EC2 instance, v.v.)
3. Áp dụng cache key và origin request policies cụ thể
4. Path patterns cụ thể hơn sẽ được ưu tiên trước

Nhiều cache behaviors cùng tồn tại, với pattern cụ thể nhất được chọn trước.

## Cache Invalidations

### Hiểu về Vấn đề

Khi bạn cập nhật nội dung ở origin (ví dụ: S3 bucket), CloudFront tiếp tục phục vụ phiên bản cached cho đến khi TTL hết hạn. Ví dụ:

- Upload phiên bản mới của `index.html` lên S3
- File được cập nhật trong S3 ngay lập tức
- CloudFront vẫn phục vụ phiên bản cached cũ (ví dụ: trong một ngày)
- Truy cập trực tiếp S3 hiển thị nội dung mới, nhưng CloudFront URL hiển thị nội dung cũ

### Tạo Invalidation

Để buộc CloudFront lấy nội dung mới từ origin:

1. Điều hướng đến tab **Invalidations** trong CloudFront distribution của bạn
2. Tạo invalidation mới
3. Chỉ định các đường dẫn object cần invalidate:
   - Sử dụng `/*` để invalidate tất cả objects
   - Hoặc chỉ định đường dẫn file cụ thể

Khi invalidation hoàn tất, CloudFront sẽ lấy nội dung mới từ origin ở request tiếp theo.

## Ví dụ Thực tế

### Tình huống

1. File ban đầu chứa: "I really love coffee"
2. Cập nhật file thành: "I really love coffee every morning"
3. Upload phiên bản mới lên S3 (không bật versioning, nó sẽ thay thế file cũ)
4. S3 phục vụ nội dung mới ngay lập tức
5. CloudFront vẫn phục vụ phiên bản cũ đã được cache

### Giải pháp

1. Truy cập CloudFront console
2. Điều hướng đến tab Invalidations
3. Tạo invalidation với pattern `/*`
4. Đợi invalidation hoàn tất
5. CloudFront bây giờ phục vụ nội dung đã cập nhật: "I really love coffee every morning"

## Best Practices (Thực hành Tốt nhất)

- Sử dụng giá trị TTL phù hợp dựa trên tần suất cập nhật nội dung
- Cụ thể hóa cache keys để tối ưu cache hit rates
- Sử dụng nhiều cache behaviors cho các loại nội dung khác nhau
- Nhớ rằng invalidations có chi phí - sử dụng chúng một cách hợp lý
- Xem xét chiến lược versioning (ví dụ: tên file có version) để tránh invalidations thường xuyên

## Tóm tắt

CloudFront cache behaviors và policies cung cấp cho bạn khả năng kiểm soát chi tiết về caching và origin requests. Khi bạn cần buộc cập nhật nội dung trước khi TTL hết hạn, cache invalidations cung cấp giải pháp ngay lập tức để làm mới nội dung đã phân phối của bạn.