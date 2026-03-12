# Khả Năng Phục Hồi của Microservices và Mô Hình Circuit Breaker

## Tổng Quan

Tài liệu này thảo luận về khả năng chịu lỗi và các mô hình phục hồi trong kiến trúc microservices, tập trung vào mô hình Circuit Breaker để xử lý các lỗi lan truyền.

## Giới Thiệu về Khả Năng Phục Hồi trong Microservices

Khả năng phục hồi là yếu tố quan trọng trong kiến trúc microservices để đảm bảo rằng sự cố của một dịch vụ không tạo ra hiệu ứng gợn sóng trên toàn bộ hệ thống. Hiểu về khả năng chịu lỗi giúp chúng ta xây dựng các microservices mạnh mẽ có thể xử lý các thách thức vận hành hàng ngày.

## Kịch Bản Điển Hình của Microservice

### Các Thành Phần Kiến Trúc

Trong một mạng lưới microservices điển hình, chúng ta có:

- **Edge Server / API Gateway**: Nhận lưu lượng truy cập từ bên ngoài từ các client
- **Accounts Microservice**: Xử lý thông tin tài khoản và khách hàng
- **Loans Microservice**: Quản lý thông tin khoản vay
- **Cards Microservice**: Xử lý dữ liệu liên quan đến thẻ

### Luồng API fetchCustomerDetails

Hệ thống cung cấp một REST API tại đường dẫn `fetchCustomerDetails` trong accounts microservice. Khi được gọi, API này trả về thông tin khách hàng đầy đủ bao gồm:

- Chi tiết khách hàng
- Thông tin tài khoản
- Chi tiết khoản vay
- Thông tin thẻ

#### Luồng Yêu Cầu

1. **Yêu Cầu từ Client**: Client bên ngoài gửi yêu cầu đến API Gateway
2. **Chuyển Tiếp từ Gateway**: Edge server chuyển tiếp yêu cầu đến accounts microservice
3. **Điều Phối Dịch Vụ**: Accounts microservice:
   - Có quyền truy cập trực tiếp vào dữ liệu tài khoản và khách hàng
   - Gọi loans microservice để lấy chi tiết khoản vay
   - Gọi cards microservice để lấy chi tiết thẻ
4. **Tổng Hợp Phản Hồi**: Accounts microservice tổng hợp tất cả các phản hồi
5. **Trả Về Phản Hồi**: Thông tin đầy đủ được gửi lại qua edge server đến client

## Vấn Đề: Lỗi Lan Truyền

### Mô Tả Kịch Bản

Xem xét tình huống một microservice trong luồng gặp sự cố:

- **Cards microservice** gặp vấn đề
- Có thể đang xử lý quá nhiều yêu cầu
- Phản hồi rất chậm hoặc không phản hồi

### Phân Tích Tác Động

#### Kịch Bản Bình Thường
- Thời gian phản hồi mong đợi: **< 1 giây**
- Luồng dữ liệu mượt mà qua tất cả các dịch vụ

#### Kịch Bản Có Vấn Đề
- Thời gian phản hồi của Cards microservice: **> 10 giây** hoặc không có phản hồi
- Một thread trong accounts microservice chờ đợi phản hồi từ cards
- Tài nguyên hệ thống (bộ nhớ, CPU) bị phân bổ và bị khóa

### Hiệu Ứng Gợn Sóng

Khi cards microservice có vấn đề về hiệu suất, nó gây ra lỗi lan truyền:

1. **Tác Động đến Accounts Microservice**
   - Một yêu cầu chờ đợi hơn 10 giây
   - Nhiều yêu cầu tích tụ, mỗi yêu cầu đều chờ đợi
   - Các thread và tài nguyên bị tiêu thụ
   - Hiệu suất tổng thể giảm sút

2. **Tác Động đến Edge Server**
   - Accounts microservice phản hồi chậm
   - Các thread của Edge server chờ lâu hơn
   - Tiêu thụ tài nguyên tăng lên
   - Sự suy giảm hiệu suất lan rộng

3. **Tác Động Toàn Hệ Thống**
   - Tất cả lưu lượng truy cập qua edge server bị ảnh hưởng
   - Không chỉ `fetchCustomerDetails`, mà cả các API khác
   - Một microservice bị lỗi ảnh hưởng đến toàn bộ mạng lưới

## Giải Pháp: Mô Hình Circuit Breaker

Để xử lý các tình huống này và ngăn chặn lỗi lan truyền, chúng ta có thể triển khai **mô hình Circuit Breaker** - một mô hình phục hồi quan trọng trong kiến trúc microservices.

### Lợi Ích Chính

- Ngăn chặn hiệu ứng gợn sóng trong toàn bộ mạng lưới microservice
- Bảo vệ tài nguyên khỏi bị cạn kiệt
- Duy trì sự ổn định của hệ thống trong khi có lỗi cục bộ
- Cho phép giảm cấp dịch vụ một cách uyển chuyển

### Cách Hoạt Động

Mô hình Circuit Breaker sẽ được đề cập chi tiết trong các bài giảng tiếp theo, tập trung vào:

- Các trạng thái của circuit breaker (Closed, Open, Half-Open)
- Cấu hình ngưỡng lỗi
- Cài đặt timeout
- Cơ chế dự phòng (fallback)
- Chiến lược phục hồi

## Kết Luận

Hiểu về khả năng chịu lỗi và triển khai các mô hình phục hồi như Circuit Breaker là điều cần thiết để xây dựng microservices mạnh mẽ. Một lỗi dịch vụ đơn lẻ không nên làm suy yếu toàn bộ hệ thống. Bằng cách triển khai các mô hình phục hồi phù hợp, chúng ta có thể:

- Cô lập lỗi
- Ngăn chặn cạn kiệt tài nguyên
- Duy trì tính khả dụng của hệ thống
- Cung cấp trải nghiệm người dùng tốt hơn

## Các Bước Tiếp Theo

Trong các bài giảng tiếp theo, chúng ta sẽ khám phá:

- Triển khai chi tiết mô hình Circuit Breaker
- Cấu hình và các phương pháp hay nhất
- Tích hợp với Spring Boot và Resilience4j
- Giám sát và khả năng quan sát

---

*Tài liệu này là một phần của loạt bài toàn diện về kiến trúc microservices bao gồm service discovery, API gateways và các mô hình phục hồi.*