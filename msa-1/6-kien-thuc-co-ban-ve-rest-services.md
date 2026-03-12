# Kiến Thức Cơ Bản Về REST Services

## Giới Thiệu

Khi xây dựng microservices với Spring Boot framework, chúng ta cần xây dựng REST services. Cuối cùng, một microservice là một dịch vụ expose business logic của nó cho các API khác hoặc ứng dụng UI bên ngoài thông qua REST API.

## REST Service Là Gì?

REST services hoạt động dựa trên giao thức HTTP so với các web services dựa trên SOAP. REST services rất nhẹ vì chúng có thể hoạt động với định dạng dữ liệu nhẹ là JSON. Đó là lý do tại sao REST là phương pháp phổ biến nhất để thiết lập giao tiếp giữa hai ứng dụng web.

### Đặc Điểm Chính

- **Nhẹ**: Sử dụng định dạng dữ liệu JSON
- **Dựa trên HTTP**: Hoạt động trên giao thức HTTP
- **Được Sử Dụng Rộng Rãi**: Phương pháp phổ biến nhất cho giao tiếp giữa các ứng dụng

## Các Mô Hình Giao Tiếp

### Giao Tiếp Đồng Bộ (Synchronous Communication)

Sử dụng REST services, chúng ta có thể thiết lập giao tiếp đồng bộ giữa nhiều API, services hoặc ứng dụng web.

**Giao tiếp đồng bộ** có nghĩa là khi một request đến từ ứng dụng bên ngoài đến microservice, ứng dụng bên ngoài sẽ đợi response trước khi tiếp tục request tiếp theo.

> **Lưu ý**: Giao tiếp đồng bộ không phải là tùy chọn duy nhất để xây dựng microservices. Microservices bất đồng bộ có thể được xây dựng bằng message queues và Kafka.

## Các Kịch Bản Sử Dụng REST Service

Khi chúng ta xây dựng services với REST APIs, ứng dụng web của chúng ta expose các endpoints mà ứng dụng client có thể gọi bằng cách gửi requests.

### Các Kịch Bản Phổ Biến:

1. **UI đến Backend Server**: Ứng dụng frontend giao tiếp với backend servers thông qua REST API
2. **Service đến Service**: Các backend servers hoặc microservices khác nhau giao tiếp với nhau qua REST API
3. **Frameworks Web Hiện Đại**: Các UI frameworks như Angular và React fetch hoặc lưu trữ dữ liệu trong backend databases thông qua REST services

## HTTP Methods và CRUD Operations

REST APIs hỗ trợ các thao tác CRUD (Create, Read, Update, Delete) trong hệ thống lưu trữ. Khi xây dựng APIs expose các thao tác này, bạn phải tuân theo các tiêu chuẩn của HTTP methods.

### Tiêu Chuẩn HTTP Methods

| Thao Tác | HTTP Method | Mô Tả |
|----------|-------------|-------|
| **Create** | POST | Sử dụng khi lưu hoặc tạo dữ liệu |
| **Read** | GET | Sử dụng khi đọc dữ liệu từ hệ thống lưu trữ và gửi cho client |
| **Update** | PUT | Sử dụng khi cập nhật toàn bộ record hoặc dữ liệu chính |
| **Update** | PATCH | Sử dụng khi cập nhật cột cụ thể hoặc một phần thông tin nhỏ |
| **Delete** | DELETE | Sử dụng khi client muốn xóa dữ liệu |

### Thực Hành Tốt Nhất

- **POST**: Để tạo dữ liệu mới
- **GET**: Cho các thao tác chỉ đọc
- **PUT**: Để cập nhật toàn bộ records
- **PATCH**: Cho cập nhật một phần
- **DELETE**: Cho các thao tác xóa

## Tiêu Chuẩn Phát Triển REST API

Khi xây dựng REST services và microservices, hãy tuân theo các tiêu chuẩn thiết yếu sau:

### 1. Xác Thực Đầu Vào (Input Validation)

**Tại sao quan trọng**: 
- Ứng dụng UI có HTML forms và input elements để validation
- REST APIs có thể được gọi bởi bất kỳ ứng dụng nào (backend, mobile, v.v.)
- Bạn không thể dựa vào validations xảy ra trong hệ thống bên ngoài

**Khuyến nghị**: Luôn thực hiện xác thực đầu vào đúng cách trên REST APIs của bạn và xử lý requests tương ứng.

### 2. Xử Lý Ngoại Lệ (Exception Handling)

**Tại sao quan trọng**:
- Clients cần hiểu những vấn đề xảy ra với APIs của bạn
- Không có thông báo lỗi phù hợp, clients không thể xác định dữ liệu nào sai hoặc tại sao thao tác thất bại
- Ngăn chặn sự can thiệp và giải thích thủ công

**Khuyến nghị**: 
- Xử lý đúng cả runtime exceptions và business exceptions
- Luôn gửi responses có ý nghĩa cho clients
- Bao phủ tất cả các kịch bản với exception handling

### 3. Tài Liệu API (API Documentation)

**Tại sao quan trọng**:
- Microservices có thể có hàng trăm hoặc hàng nghìn REST services
- Clients bên ngoài cần biết:
  - Định dạng request
  - Quy tắc validation
  - Định dạng response
  - Các thao tác được hỗ trợ

**Khuyến nghị**:
- Tài liệu hóa REST services sử dụng các tiêu chuẩn như:
  - **OpenAPI Specification**
  - **Swagger**
- Giúp onboarding clients mới dễ dàng hơn nhiều
- Giảm nhu cầu về các phiên chuyển giao kiến thức thủ công

### Lợi Ích Của Tài Liệu Hóa Đúng Cách

Khi bạn tài liệu hóa REST services tốt với các tiêu chuẩn này:
- Cuộc sống của bạn trở nên dễ dàng hơn khi quản lý số lượng lớn APIs
- Clients có thể tự phục vụ mà không cần hỗ trợ liên tục
- Giảm độ phức tạp khi onboarding các consumers mới
- Loại bỏ các giải thích qua email hoặc phiên KT phức tạp

## Tóm Tắt

Để xây dựng REST services sẵn sàng cho production với Spring Boot framework:

1. ✅ Tuân theo tiêu chuẩn HTTP methods cho các thao tác CRUD
2. ✅ Triển khai xác thực đầu vào đúng cách
3. ✅ Xử lý exceptions một cách có ý nghĩa
4. ✅ Tài liệu hóa services sử dụng OpenAPI/Swagger

Các tiêu chuẩn này đảm bảo bạn ở vị trí tốt để xây dựng services sẵn sàng cho production cho các dự án thực tế.