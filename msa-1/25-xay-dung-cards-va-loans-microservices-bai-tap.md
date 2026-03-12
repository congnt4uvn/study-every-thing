# Xây Dựng Cards và Loans Microservices - Bài Tập

## Tổng Quan

Sau khi hoàn thành việc phát triển Accounts Microservice với các tiêu chuẩn và thực hành tốt nhất đã được thiết lập, bước tiếp theo là xây dựng các microservices tương tự cho Cards và Loans, tuân theo cùng các mẫu kiến trúc và quy ước.

## Mục Tiêu Bài Tập

Xây dựng hai microservices mới (Cards và Loans) áp dụng tất cả các tiêu chuẩn và thực hành đã học từ việc triển khai Accounts Microservice.

## Hướng Dẫn Triển Khai Từng Bước

### 1. Thiết Lập Dự Án

- Tạo các ứng dụng Spring Boot trống từ [start.spring.io](https://start.spring.io)
- Bao gồm tất cả các dependencies cần thiết
- Tải xuống và giải nén các ứng dụng web Spring Boot

### 2. Triển Khai Các Tính Năng Cốt Lõi

Tuân theo các tiêu chuẩn sau cho cả hai microservices Cards và Loans:

#### Cấu Hình Cơ Sở Dữ Liệu
- Cấu hình cơ sở dữ liệu H2
- Tạo schema cơ sở dữ liệu
- Định nghĩa cấu trúc bảng với các cột phù hợp

#### Tầng Dữ Liệu
- Tạo các lớp entity
- Triển khai JPA repositories
- Thiết lập các mối quan hệ entity phù hợp

#### Tầng Service
- Triển khai mẫu DTO (Data Transfer Object)
- Xây dựng logic nghiệp vụ
- Tạo các thành phần tầng service

#### Tầng API
- Viết các API thực hiện các thao tác CRUD (Create, Read, Update, Delete)
- Triển khai các phương thức HTTP phù hợp
- Tuân theo quy ước RESTful

#### Xử Lý Ngoại Lệ
- Xây dựng logic xử lý ngoại lệ toàn diện
- Tạo các lớp ngoại lệ tùy chỉnh
- Triển khai global exception handlers

#### Tính Năng Bổ Sung
- Triển khai chức năng auditing
- Tài liệu hóa REST APIs sử dụng OpenAPI specification
- Thêm validation phù hợp

## Tài Liệu Tham Khảo

### GitHub Repository

Truy cập mã nguồn tham khảo hoàn chỉnh tại:
```
github.com/easybites/microservices
```

#### Mã Nguồn Có Sẵn
- Section 2 chứa các triển khai hoàn chỉnh:
  - Accounts Microservice
  - Cards Microservice
  - Loans Microservice

### Tham Khảo Database Schema

#### Schema Loans Microservice

**Tên Bảng:** `loans`

**Các Cột:**
- `loan_id` - Khóa chính (tự động tạo)
- `mobile_number` - Số điện thoại khách hàng
- `loan_number` - Mã định danh khoản vay duy nhất
- `loan_type` - Loại khoản vay
- `total_loan` - Tổng số tiền vay
- `amount_paid` - Số tiền đã trả
- `outstanding_amount` - Số tiền còn lại

**Vị Trí:** File `schema.sql` trong thư mục Loans Microservice

### Cấu Hình Port

Cấu hình các port sau trong file `application.yml`:

- **Accounts Microservice:** Port 8080
- **Cards Microservice:** Port 9000
- **Loans Microservice:** Port 8090

## Thực Hành Tốt Nhất

### Quy Ước Đặt Tên
- Tuân theo cùng quy ước đặt tên như Accounts Microservice
- Sử dụng tên lớp nhất quán
- Áp dụng cách đặt tên phương thức thống nhất
- Duy trì tính nhất quán trong tên trường

### Tiêu Chuẩn Mã Nguồn
- Sao chép cấu trúc từ repository tham khảo
- Đảm bảo mã nguồn tương tự cho các sửa đổi trong tương lai
- Duy trì tính nhất quán giữa tất cả các microservices

### Phương Pháp Phát Triển
- Tham khảo GitHub repository khi cần
- Hiểu quy trình và các tiêu chuẩn
- Có thể sao chép mã từ repository
- Tập trung vào việc hiểu chi tiết triển khai

## Tài Nguyên Kiểm Thử

### Postman Collection

Một file JSON Postman collection có sẵn trong GitHub repository:
- Tải xuống collection
- Import vào Postman
- Kiểm thử tất cả các API endpoints

## Các Liên Kết Quan Trọng

Tất cả tài nguyên tham khảo được duy trì trong GitHub repository:

1. **Tài Liệu Spring Boot** - Tài liệu chính thức Spring Boot
2. **Spring Initializr** - [start.spring.io](https://start.spring.io)
3. **DTO Pattern** - Bài viết blog giải thích về pattern
4. **Spring Doc** - Website tài liệu Spring
5. **OpenAPI Specification** - Tiêu chuẩn tài liệu hóa API

## Kết Quả Mong Đợi

Sau khi hoàn thành bài tập này, bạn sẽ:
- Xây dựng hai microservices hoàn chỉnh (Cards và Loans)
- Áp dụng các tiêu chuẩn nhất quán trên nhiều microservices
- Hiểu các mẫu kiến trúc microservice
- Thực hành triển khai ứng dụng Spring Boot cấp doanh nghiệp
- Chuẩn bị cho các chủ đề nâng cao trong các bài giảng sắp tới

## Các Bước Tiếp Theo

Giảng viên sẽ xem xét và giải thích tất cả mã nguồn có trong các microservices này trong các bài giảng tương lai, đảm bảo sự phù hợp giữa triển khai của bạn và kiến trúc tham khảo.

---

**Lưu Ý:** Bài tập này được thiết kế để củng cố việc học thông qua triển khai thực tế. Hãy dành thời gian để hiểu từng thành phần trong khi xây dựng các microservices.