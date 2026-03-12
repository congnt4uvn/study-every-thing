# Tổng Quan về Caching trong AWS CloudFront

## Giới Thiệu

Amazon CloudFront là dịch vụ mạng phân phối nội dung (CDN) lưu trữ nội dung tại các edge location trên toàn thế giới để cải thiện hiệu suất và giảm độ trễ cho người dùng cuối. Hiểu cách hoạt động của CloudFront caching là điều cần thiết để tối ưu hóa hiệu suất và chi phí của ứng dụng.

## Cách Hoạt Động của CloudFront Caching

### Kiến Trúc Cache

- Cache tồn tại ở mỗi CloudFront edge location
- Bạn sẽ có nhiều cache bằng số lượng edge location
- Mỗi object trong cache được xác định bởi một **Cache Key** (Khóa Cache)

### Luồng Xử Lý Request Cache

Khi một request được thực hiện qua CloudFront edge location:

1. Edge location kiểm tra xem object đã được cache chưa
2. Nếu đã cache, kiểm tra xem object đã hết hạn hay chưa dựa trên Time To Live (TTL)
3. Nếu chưa có trong cache hoặc đã hết hạn, request được chuyển tiếp đến origin của bạn
4. Response từ origin được cache tại edge location
5. Các request sau sẽ trả về kết quả đã được cache

### Tối Ưu Hóa Cache

**Mục tiêu**: Tối đa hóa tỷ lệ Cache Hit bằng cách giảm thiểu request đến origin

Điều này có nghĩa là cache càng nhiều nội dung càng tốt tại các edge location của bạn.

### Cache Invalidation (Vô Hiệu Hóa Cache)

Bạn không cần đợi đến khi một item hết hạn dựa trên TTL. Nếu muốn xóa một object khỏi cache ngay lập tức, bạn có thể tạo **cache invalidation**.

## CloudFront Cache Key

### Cache Key là gì?

Cache Key là một **định danh duy nhất** cho mỗi object trong cache.

### Các Thành Phần Cache Key Mặc Định

Theo mặc định, Cache Key bao gồm:
- **Hostname** (tên miền) (ví dụ: `mywebsite.com`)
- **Phần resource của URL** (ví dụ: `/content/stories/example-story.html`)

**Ví dụ:**
```
GET https://mywebsite.com/content/stories/example-story.html
```

Khi xảy ra cache miss:
1. Object được lấy từ origin
2. Object được cache dựa trên hostname và phần resource
3. Các request tiếp theo có cùng hostname và resource sẽ nhận được cache hit

### Cache Key Nâng Cao

Đôi khi nội dung thay đổi dựa trên:
- Tùy chọn người dùng
- Loại thiết bị
- Ngôn ngữ
- Vị trí địa lý

Để đáp ứng điều này, bạn có thể nâng cao Cache Key bằng cách thêm:
- **HTTP headers**
- **Cookies**
- **Query strings** (chuỗi truy vấn)

## CloudFront Cache Policy

**Cache Policy** xác định cách tạo Cache Key bằng cách chỉ định những gì cần bao gồm:

### HTTP Headers
- **None** (Không có): Không bao gồm header nào
- **Whitelist** (Danh sách trắng): Chọn các header cụ thể để bao gồm

### Cookies
- **None**: Không bao gồm cookie nào
- **Whitelist**: Chọn các cookie cụ thể để bao gồm
- **All** (Tất cả): Bao gồm tất cả cookies
- **All-except** (Tất cả ngoại trừ): Bao gồm tất cả trừ các cookie được chỉ định

### Query Strings
- **None**: Không bao gồm query string nào
- **Whitelist**: Chọn các query string cụ thể để bao gồm
- **All-except**: Bao gồm tất cả trừ các query string được chỉ định
- **All**: Bao gồm tất cả query strings

### Kiểm Soát TTL

Trong cache policy, bạn có thể kiểm soát:
- Phạm vi TTL: từ 0 giây đến 1 năm
- Sử dụng các header cụ thể như `Cache-Control` hoặc `Expires`

### Tùy Chọn Policy

- **Tạo custom cache policies** (chính sách cache tùy chỉnh)
- **Sử dụng AWS predefined managed policies** (chính sách được quản lý sẵn bởi AWS)

### Lưu Ý Quan Trọng

**Tất cả HTTP headers, cookies, và query strings được bao gồm trong Cache Key sẽ tự động được chuyển tiếp đến origin request của bạn.**

## Ví Dụ về HTTP Headers

### Kịch Bản: Caching Dựa Trên Ngôn Ngữ

Request với header: `Accept-Language: fr-FR`

#### None Policy
- Không có header nào được cache
- Headers không được chuyển tiếp đến origin
- **Hiệu suất caching tốt nhất** (không có header trong Cache Key)

#### Whitelist Policy
- Chỉ định header nào cần bao gồm (ví dụ: `Accept-Language`)
- Header `Accept-Language` được bao gồm trong Cache Key
- Header được chuyển tiếp đến origin
- Origin có thể phản hồi nội dung bằng ngôn ngữ chính xác

## Ví Dụ về Query Strings

Query strings xuất hiện trong URL sau dấu hỏi chấm.

**Ví dụ:**
```
https://example.com/image/cat.jpg?border=red&size=large
```

### None
- Không có query string nào được sử dụng cho Cache Key
- Không được chuyển tiếp đến origin

### Whitelist
- Chỉ định query string nào cần bao gồm

### Include All-except
- Chỉ định những query string nào cần loại trừ
- Phần còn lại được bao gồm

### All
- Tất cả query strings được bao gồm trong Cache Key
- Tất cả được chuyển tiếp đến origin
- **Hiệu suất caching tệ nhất** (nhiều biến thể)

## Origin Request Policy

### Mục Đích

Đôi khi bạn cần chuyển tiếp thông tin đến origin mà **không nên** là một phần của Cache Key.

### Origin Request Policy là gì?

Origin Request Policy cho phép bạn:
- Bao gồm thêm HTTP headers, cookies, hoặc query strings
- Chuyển tiếp chúng đến origin
- **Không sử dụng chúng trong Cache Key**

### Khả Năng Bổ Sung

Bạn có thể thêm custom HTTP headers hoặc CloudFront HTTP headers vào origin request, ngay cả khi chúng không có trong viewer request.

**Trường hợp sử dụng:**
- Truyền API key
- Truyền secret header

### Tùy Chọn Policy

- **Tạo custom policies** (chính sách tùy chỉnh)
- **Sử dụng AWS predefined managed policies**

## Cache Policy vs Origin Request Policy

### Hiểu Sự Khác Biệt

**Luồng Request:**

1. **Viewer Request** đến với:
   - Query strings
   - Cookies
   - Headers

2. **Cache Policy** xác định những gì cần cache:
   - Ví dụ: Hostname + Resource + Header `Authorization`

3. **Origin Request** có thể cần thông tin bổ sung:
   - User Agent
   - Session ID
   - Referrer query string

4. **Kết quả:**
   - Origin request được bổ sung thêm các tham số
   - Caching chỉ xảy ra dựa trên Cache Policy
   - Các tham số bổ sung từ Origin Request Policy không ảnh hưởng đến caching

### Điểm Chính

**Sự phối hợp** giữa hai policy này cho phép bạn:
- Tối ưu hóa caching (Cache Policy)
- Cung cấp thông tin đầy đủ cho origin (Origin Request Policy)
- Duy trì tỷ lệ cache hit cao trong khi đáp ứng yêu cầu của origin

## Tóm Tắt

- CloudFront caching xảy ra tại các edge location trên toàn thế giới
- Cache Keys xác định các object duy nhất trong cache
- Cache Policies kiểm soát những gì được đưa vào Cache Key
- Origin Request Policies kiểm soát những gì được chuyển tiếp đến origin (mà không ảnh hưởng đến caching)
- Cấu hình đúng giúp tối đa hóa tỷ lệ cache hit và cải thiện hiệu suất
- Hiểu các khái niệm này là điều cần thiết cho các kỳ thi chứng chỉ AWS

## Thực Hành Tốt Nhất

1. **Tối đa hóa tỷ lệ cache hit** bằng cách chọn cẩn thận các thành phần Cache Key
2. **Sử dụng whitelist** thay vì tùy chọn "all" khi có thể
3. **Tách biệt các mối quan tâm về caching** khỏi nhu cầu origin request bằng cách sử dụng cả hai policy
4. **Tận dụng AWS managed policies** khi chúng phù hợp với use case của bạn
5. **Sử dụng cache invalidation** một cách tiết kiệm (phát sinh chi phí)

---

*Tài liệu này dựa trên các khái niệm cơ bản về AWS CloudFront caching và được thiết kế để giúp các developer và solutions architect hiểu và tối ưu hóa hiệu suất CDN.*