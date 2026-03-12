# Mô Hình Circuit Breaker: Kiểm Soát Lưu Lượng Truy Cập Trong Microservices

## Tổng Quan

Mô hình Circuit Breaker là một mô hình khả năng phục hồi quan trọng giúp kiểm soát luồng traffic đến các microservices đang gặp sự cố hoặc vấn đề về hiệu suất. Mô hình này giúp ngăn chặn lỗi lan truyền trong hệ thống phân tán bằng cách giám sát và quản lý lưu lượng truy cập dựa trên tình trạng của các dịch vụ downstream.

## Cách Hoạt Động của Circuit Breaker

Mô hình Circuit Breaker không tự động giám sát tất cả microservices - nó phải được cấu hình rõ ràng cho các dịch vụ cụ thể nơi cần khả năng phục hồi. Sau khi được kích hoạt, nó kiểm soát luồng traffic bằng cách sử dụng ba trạng thái riêng biệt.

## Ba Trạng Thái của Circuit Breaker

### 1. Trạng Thái Closed (Hoạt Động Bình Thường)

- **Trạng thái ban đầu**: Khi ứng dụng khởi động, circuit breaker bắt đầu ở trạng thái closed
- **Hành vi**: Tất cả các request đến đều được phép đi qua microservice
- **So sánh**: Tương tự như mạch điện đóng nơi dòng điện chảy tự do đến các thành phần phía sau
- **Giám sát**: Circuit breaker liên tục giám sát tất cả các request, theo dõi:
  - Tỷ lệ thành công/thất bại của response
  - Các vấn đề về mạng
  - Thời gian phản hồi và độ trễ
  - Tình trạng tổng thể của microservice

### 2. Trạng Thái Open (Chế Độ Lỗi)

**Kích hoạt chuyển đổi**: Circuit breaker chuyển từ closed sang open dựa trên **ngưỡng tỷ lệ lỗi** mà bạn cấu hình. Ví dụ: nếu 50% request thất bại, mạch sẽ mở.

**Hành vi ở trạng thái Open**:
- **Không có request nào** được chuyển tiếp đến microservice đang lỗi
- Các request **thất bại ngay lập tức** với phản hồi lỗi
- Ngăn chặn hiệu ứng gợn sóng và lỗi lan truyền đến các dịch vụ gọi
- Cho microservice đang lỗi thời gian để phục hồi

**Thời gian chờ**: Circuit breaker duy trì ở trạng thái open trong khoảng thời gian đã cấu hình (ví dụ: 90 giây), cho phép microservice có thời gian để:
- Phục hồi từ các lỗi
- Giải quyết các vấn đề về mạng
- Ổn định hiệu suất

### 3. Trạng Thái Half-Open (Kiểm Tra Phục Hồi)

**Chuyển đổi**: Sau khi hết thời gian chờ, circuit breaker chuyển sang trạng thái half-open.

**Hành vi**:
- Cho phép **số lượng request thử nghiệm giới hạn** (ví dụ: 10-20 request) đi qua
- Giám sát tỷ lệ thành công của các request thử nghiệm này
- **Nếu vẫn tiếp tục lỗi** (ví dụ: ≥50% thất bại): Quay lại trạng thái open và chờ lại
- **Nếu request thành công**: Chuyển về trạng thái closed để hoạt động bình thường

**Chu trình phục hồi**: Mô hình tuần hoàn giữa open → half-open → open cho đến khi microservice xử lý thành công các request thử nghiệm, lúc đó nó quay về trạng thái closed.

## Triển Khai với Resilience4j và Spring Boot

Mặc dù mô hình circuit breaker nghe có vẻ phức tạp, nhưng việc triển khai trong microservices Spring Boot cực kỳ đơn giản khi sử dụng thư viện **Resilience4j**.

### Các Tham Số Cấu Hình Chính

- **Failure Rate Threshold**: Phần trăm lỗi kích hoạt trạng thái open (ví dụ: 50%)
- **Wait Duration**: Thời gian duy trì ở trạng thái open trước khi kiểm tra phục hồi (ví dụ: 90 giây)
- **Permitted Calls in Half-Open**: Số lượng request thử nghiệm được phép ở trạng thái half-open (ví dụ: 10-20)
- **Minimum Number of Calls**: Số request tối thiểu cần thiết trước khi tính toán tỷ lệ lỗi

## Lợi Ích

1. **Ngăn chặn lỗi lan truyền**: Dừng việc lỗi lan rộng qua hệ thống
2. **Tự động phục hồi**: Hành vi tự chữa lành thông qua cơ chế kiểm tra half-open
3. **Thất bại nhanh**: Phản hồi lỗi ngay lập tức trong thời gian ngừng hoạt động thay vì để request treo
4. **Bảo vệ tài nguyên**: Ngăn chặn việc áp đảo dịch vụ đang gặp khó khăn với các request bổ sung
5. **Ổn định hệ thống**: Duy trì tình trạng tổng thể của hệ thống bằng cách cô lập các lỗi

## Các Bước Tiếp Theo

Để triển khai mô hình circuit breaker trong microservices của bạn:

1. Thêm dependencies Resilience4j vào dự án Spring Boot của bạn
2. Cấu hình thuộc tính circuit breaker cho các dịch vụ cụ thể
3. Áp dụng annotations circuit breaker cho các phương thức service
4. Kiểm tra hành vi trong các tình huống lỗi khác nhau

## Tài Nguyên Bổ Sung

Để biết thêm thông tin chi tiết, hãy tham khảo [tài liệu chính thức của Resilience4j](https://resilience4j.readme.io/).

---

**Lưu ý**: Đảm bảo bạn hiểu rõ ba trạng thái (closed, open, half-open) và các chuyển đổi giữa chúng trước khi triển khai mô hình này trong hệ thống production. Xem lại hướng dẫn này hoặc tài liệu Resilience4j nếu có bất kỳ khái niệm nào chưa rõ ràng.