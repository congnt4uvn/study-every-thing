# Tại Sao Chúng Ta Cần Edge Server (API Gateway) Trong Kiến Trúc Microservices

## Giới Thiệu

Tài liệu này giải thích sự cần thiết của việc có một edge server (API Gateway) riêng biệt trong kiến trúc microservices và những thách thức khi không có nó.

## Thách Thức Khi Không Có Edge Server

### Giao Tiếp Trực Tiếp Từ Client Đến Microservice

Trong kiến trúc microservices không có edge server:
- Các microservices riêng lẻ (accounts, loans, cards) được triển khai trên các server/container riêng biệt
- Các client bên ngoài giao tiếp trực tiếp với từng microservice tương ứng
- Trong các dự án thực tế với hơn 100 microservices, điều này tạo ra nhiều thách thức nghiêm trọng

### Các Vấn Đề Chính

1. **Thiếu Tính Nhất Quán**: Việc triển khai các cross-cutting concerns (bảo mật, kiểm toán, logging, routing) đòi hỏi phải lặp lại logic trên tất cả các microservices
2. **Không Nhất Quán Giữa Các Developer**: Các developer khác nhau có thể tuân theo các tiêu chuẩn khác nhau khi triển khai cùng một concerns
3. **Không Có Kiểm Soát Tập Trung**: Khó khăn trong việc áp dụng các thực hành bảo mật, kiểm toán và logging thống nhất

### Tại Sao Thư Viện Chung Không Giải Quyết Được Vấn Đề

Mặc dù việc xây dựng các cross-cutting concerns vào một thư viện chung có vẻ hợp lý, nhưng nó có những nhược điểm:

- **Khớp Nối Chặt Chẽ**: Tạo ra sự phụ thuộc giữa thư viện chung và tất cả các microservices
- **Bảo Trì Khó Khăn**: Các thay đổi về bảo mật, kiểm toán hoặc logging đòi hỏi:
  - Kiểm thử hồi quy toàn diện
  - Phân tích tác động trên tất cả các microservices
  - Không khả thi với số lượng lớn microservices

## Giải Pháp Edge Server

### Tổng Quan Kiến Trúc

```
Ứng dụng Client → Edge Server/API Gateway → Microservices
                                             ├─ Accounts
                                             ├─ Loans
                                             └─ Cards
```

### Cách Hoạt Động

1. Edge server nằm giữa các ứng dụng client và microservices
2. Nhận tất cả các request từ bên ngoài
3. Thực thi logic của các cross-cutting concerns
4. Xác thực các request
5. Chỉ chuyển tiếp đến microservice thực tế sau khi xác thực

## Khả Năng Của API Gateway

### Các Chức Năng Cốt Lõi

1. **Cross-Cutting Concerns**
   - Bảo mật (xác thực & phân quyền)
   - Logging
   - Kiểm toán
   - Định tuyến

2. **Khả Năng Chịu Lỗi & Độ Bền**
   - Ngăn chặn lỗi lan truyền (cascading failures)
   - Làm cho các dịch vụ downstream có khả năng chịu lỗi
   - Triển khai circuit breaker
   - Xử lý ngoại lệ

3. **Quản Lý Lưu Lượng**
   - Retry và timeout cho các lệnh gọi dịch vụ nội bộ
   - Chính sách quota dựa trên gói đăng ký của client (standard, premium, advanced)
   - Giới hạn tốc độ (rate limiting)

### Quy Trình Xử Lý Request

API Gateway xử lý các request qua nhiều giai đoạn:

1. **Giai Đoạn Xác Thực**
   - Xác thực request
   - Blacklist/whitelist địa chỉ IP
   - Kiểm tra danh sách include/exclude

2. **Giai Đoạn Bảo Mật**
   - Xác thực (Authentication)
   - Phân quyền (Authorization)

3. **Kiểm Soát Lưu Lượng**
   - Giới hạn tốc độ (Rate limiting)
   - Áp dụng quota

4. **Định Tuyến & Chuyển Đổi**
   - Định tuyến động
   - Service discovery
   - Chỉnh sửa request/response
   - Chuyển đổi giao thức (ví dụ: HTTPS → HTTP)

5. **Giám Sát & Logging**
   - Tích hợp với công cụ giám sát (Grafana)
   - Logging tập trung
   - Theo dõi lỗi qua dashboard

6. **Caching** (Tùy chọn)
   - Tích hợp Redis cache
   - Logic nghiệp vụ dựa trên cache

## API Gateway vs Eureka Server

### Tại Sao Không Dùng Eureka Cho Mọi Thứ?

**Mục Đích Của Eureka Server**: Tập trung nghiêm ngặt vào service discovery và service registry

**Mục Đích Của API Gateway**: Xử lý các yêu cầu phi chức năng và cross-cutting concerns

### Lợi Ích Của Việc Tách Biệt

- **Linh Hoạt**: Tổ chức có thể chọn component nào để sử dụng
- **Tách Biệt Mối Quan Tâm**: Các component khác nhau xử lý các vấn đề khác nhau
- **Triển Khai Tùy Chọn**: Chức năng Gateway có thể được bỏ qua nếu không cần

## Triển Khai Với Spring Cloud

Việc xây dựng API Gateway có thể có vẻ phức tạp, nhưng các framework Spring Boot và Spring Cloud đơn giản hóa đáng kể việc triển khai.

### Điểm Chính

- Dễ dàng triển khai với Spring Cloud
- Các pattern và practices được tài liệu hóa tốt
- Giải pháp sẵn sàng cho doanh nghiệp
- Kiến trúc có khả năng mở rộng

## Tóm Tắt Ưu Điểm

✅ **Tính Nhất Quán**: Triển khai tập trung các cross-cutting concerns  
✅ **Khả Năng Bảo Trì**: Điểm duy nhất cho cập nhật và thay đổi  
✅ **Linh Hoạt**: Dễ dàng thay đổi chính sách mà không ảnh hưởng đến microservices  
✅ **Bảo Mật**: Xác thực và phân quyền tập trung  
✅ **Độ Bền**: Circuit breakers và khả năng chịu lỗi  
✅ **Giám Sát**: Logging và metrics thống nhất  
✅ **Kiểm Soát Lưu Lượng**: Quản lý rate limiting và quota  
✅ **Linh Hoạt Giao Thức**: Khả năng chuyển đổi giao thức  

## Kết Luận

Edge Server/API Gateway là thiết yếu cho:
- Quản lý giao tiếp bên ngoài trong microservices
- Triển khai các cross-cutting concerns một cách nhất quán
- Đảm bảo khả năng chịu lỗi và độ bền
- Cung cấp tính linh hoạt và khả năng bảo trì

Trong các phần tiếp theo, chúng ta sẽ khám phá cách Spring Cloud giúp triển khai các khả năng này trong kiến trúc microservices của chúng ta.

---

**Lưu ý**: Tất cả các chức năng có thể được kích hoạt hoặc vô hiệu hóa dựa trên yêu cầu nghiệp vụ. Các khả năng được đề cập là phổ biến nhưng không đầy đủ.