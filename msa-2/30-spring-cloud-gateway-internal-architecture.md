# Kiến Trúc Nội Bộ của Spring Cloud Gateway

## Tổng Quan

Tài liệu này giải thích kiến trúc nội bộ của Spring Cloud Gateway và cách nó xử lý các request trong môi trường microservices. Spring Cloud Gateway hoạt động như một edge server quản lý routing, filtering và bảo mật cho các ứng dụng microservice.

## Kiến Trúc Luồng Request

### 1. Điểm Nhận Request từ Client

Các client bên ngoài gửi request đến gateway server, bao gồm:
- Ứng dụng di động
- Ứng dụng web
- Các REST API khác

### 2. Gateway Handler Mapping

**Gateway Handler Mapping** là thành phần quan trọng đầu tiên:
- Xác định path được gọi bởi ứng dụng client
- Quyết định microservice nào sẽ nhận request
- Sử dụng cấu hình routing do developer định nghĩa (không dựa trên AI)

Developer phải cấu hình các quy tắc routing chỉ định:
- Mẫu đường dẫn request
- Đích đến là microservice nào

### 3. Predicates (Điều Kiện)

**Predicates** là các thành phần logic boolean thực thi trước khi chuyển tiếp request:
- Định nghĩa các điều kiện phải đáp ứng để chuyển tiếp request
- Trả về true hoặc false dựa trên đánh giá
- Từ chối các request không đáp ứng điều kiện đã định nghĩa
- Tương tự như functional interface predicate trong Java 8

Nếu predicates thất bại, gateway sẽ từ chối request với thông báo lỗi phù hợp.

### 4. Pre-Filters (Bộ Lọc Trước)

**Pre-Filters** thực thi logic nghiệp vụ trước khi chuyển tiếp request đến microservices:
- Xác thực request
- Auditing và logging
- Sửa đổi request
- Kiểm tra bảo mật
- Bất kỳ yêu cầu cross-cutting hoặc yêu cầu phi chức năng nào

Có thể cấu hình nhiều pre-filters dựa trên yêu cầu.

### 5. Xử Lý Microservice

Sau khi đánh giá predicate thành công và thực thi pre-filter:
- Request được chuyển tiếp đến microservice đích (loans, cards, accounts, v.v.)
- Microservice xử lý request
- Response được tạo ra

### 6. Post-Filters (Bộ Lọc Sau)

**Post-Filters** tác động lên response trước khi gửi cho client:
- Sửa đổi response
- Xác thực response
- Logging hoặc auditing bổ sung
- Thu thập số liệu hiệu suất

### 7. Gửi Response

Sau khi thực thi post-filter:
- Response quay về Gateway Handler Mapping
- Gateway Handler Mapping gửi response cho ứng dụng client

## Filters và Predicates Được Định Nghĩa Sẵn

Spring Cloud Gateway cung cấp nhiều filters và predicates tích hợp sẵn cho các tình huống phổ biến.

### Route Predicate Factories

Cấu hình routes dựa trên các tham số khác nhau:
- **Dựa trên Header**: Route dựa trên HTTP headers
- **Dựa trên Cookie**: Route dựa trên giá trị cookie
- **Dựa trên Host**: Route dựa trên mẫu host
- **Dựa trên Method**: Route dựa trên HTTP methods (GET, POST, v.v.)
- **Dựa trên Path**: Route dựa trên đường dẫn URL
- **Dựa trên Query**: Route dựa trên query parameters
- **Dựa trên Remote Address**: Route dựa trên địa chỉ IP client
- **Dựa trên Weight**: Phân phối traffic theo trọng số

### Gateway Filter Factories

Các filters được xây dựng sẵn cho các thao tác phổ biến:
- **AddRequestHeader**: Thêm headers vào requests
- **AddRequestParameter**: Thêm query parameters vào requests
- **AddResponseHeader**: Thêm headers vào responses
- **CircuitBreaker**: Triển khai mẫu circuit breaker
- **CacheRequestBody**: Cache request body để xử lý
- **FallbackHeaders**: Thêm fallback headers
- **JsonToGrpc**: Chuyển đổi JSON requests sang gRPC
- **ModifyRequestBody**: Sửa đổi nội dung request body
- **ModifyResponseBody**: Sửa đổi nội dung response body
- **Retry**: Triển khai logic retry
- **TokenRelay**: Chuyển tiếp security tokens

### Global Filters

Các filters bổ sung có sẵn toàn cục:
- **Gateway Metrics**: Thu thập metrics và dữ liệu monitoring
- **TLS/SSL Handlers**: Thực hiện các thao tác TLS handshake

## Cấu Hình và Triển Khai

Các bài giảng tiếp theo sẽ đề cập:
- Tạo gateway server với Spring Cloud Gateway
- Cấu hình quy tắc routing
- Định nghĩa predicates tùy chỉnh
- Tạo pre-filters và post-filters
- Sử dụng predefined filters hiệu quả

## Tài Nguyên Bổ Sung

Để biết thông tin chi tiết và các tình huống nâng cao, tham khảo [Tài Liệu Chính Thức Spring Cloud Gateway](https://spring.io/projects/spring-cloud-gateway).

## Tóm Tắt

Spring Cloud Gateway cung cấp giải pháp toàn diện cho:
- Routing tập trung trong kiến trúc microservices
- Filtering request và response
- Xử lý request có điều kiện
- Bảo mật và các vấn đề cross-cutting
- Cấu hình dễ dàng với các thành phần định nghĩa sẵn

Kiến trúc đảm bảo tất cả các request đi qua một pipeline được kiểm soát, cho phép xử lý nhất quán các vấn đề chung trên tất cả các microservices.