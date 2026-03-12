# Mẫu Thiết Kế Circuit Breaker Trong Microservices

## Giới Thiệu

Mẫu thiết kế Circuit Breaker là một pattern quan trọng để xây dựng các microservices có khả năng phục hồi, giúp ngăn chặn các lỗi lan truyền (cascading failures) trong hệ thống phân tán. Pattern này được lấy cảm hứng từ cầu dao điện và cung cấp chức năng bảo vệ tương tự trong kiến trúc phần mềm.

## Hiểu Về Circuit Breaker Trong Hệ Thống Điện

Trước khi đi vào triển khai phần mềm, hãy tìm hiểu khái niệm từ hệ thống điện:

- **Mục đích**: Thiết bị an toàn được thiết kế để bảo vệ mạch điện khỏi dòng điện quá mức hoặc nguy cơ cháy nổ
- **Chức năng**: Tự động ngắt khi phát hiện lỗi như ch短 mạch hoặc quá tải
- **Bảo vệ**: Ngăn chặn hư hỏng cho các thiết bị điện bằng cách dừng dòng điện trong điều kiện nguy hiểm

### Ví Dụ Tình Huống

Khi cầu dao phát hiện chập mạch hoặc quá tải, nó tự động ngắt để bảo vệ các thiết bị (như bóng đèn) khỏi bị hư hỏng. Nếu không có bảo vệ này, dòng điện quá mức sẽ chạy qua và làm hỏng các thiết bị kết nối.

## Mẫu Circuit Breaker Trong Phát Triển Phần Mềm

### Vấn Đề

Trong môi trường phân tán, các lời gọi từ xa đến các dịch vụ và tài nguyên có thể thất bại do nhiều lý do:

- Lỗi tạm thời (transient faults)
- Kết nối mạng chậm
- Vấn đề timeout
- Tài nguyên bị quá tải
- Tình trạng không khả dụng tạm thời

**Quan trọng**: Hầu hết các lỗi này đều tạm thời và thường tự khắc phục sau một khoảng thời gian ngắn.

### Cách Hoạt Động Của Circuit Breaker Pattern

Circuit Breaker pattern giám sát tất cả các lời gọi từ xa đến một dịch vụ cụ thể và thực hiện các hành vi sau:

1. **Giám sát**: Theo dõi tất cả các lời gọi đến các dịch vụ downstream (ví dụ: Cards microservice)
2. **Phát hiện**: Xác định khi một dịch vụ:
   - Mất quá nhiều thời gian để phản hồi
   - Không phản hồi
   - Gặp vấn đề về mạng
3. **Mở Circuit**: Khi phần lớn các lời gọi thất bại, circuit breaker "mở" và:
   - Dừng tất cả các yêu cầu trong tương lai đến dịch vụ bị lỗi
   - Trả về phản hồi lỗi ngay lập tức cho client
   - Ngăn chặn việc chờ đợi và lỗi lan truyền
4. **Thất Bại Nhanh**: Các ứng dụng client (như Accounts microservice và Gateway server) nhận được phản hồi lỗi ngay lập tức thay vì chờ timeout

### Luồng Ví Dụ

```
Gateway Server → Accounts Microservice → Cards Microservice (đang lỗi)
```

Khi Cards microservice bị down hoặc chậm:
- Circuit breaker phát hiện các lỗi
- Mở circuit đến Cards microservice
- Trả về lỗi ngay lập tức cho Accounts microservice
- Ngăn chặn hiệu ứng gợn sóng trên Gateway và các dịch vụ khác
- Các API khác (ví dụ: Accounts + Loans) vẫn hoạt động bình thường

## Cơ Chế Phục Hồi

Circuit breaker không chặn traffic vĩnh viễn:

1. **Thời Gian Phục Hồi**: Cho dịch vụ bị lỗi thời gian để phục hồi (30-90 giây dựa trên cấu hình)
2. **Kiểm Tra Traffic Một Phần**: Định kỳ gửi các yêu cầu giới hạn để kiểm tra xem dịch vụ đã phục hồi chưa
3. **Đóng Circuit**: Nếu traffic một phần thành công, cho phép tất cả các yêu cầu đi qua
4. **Bảo Vệ Liên Tục**: Nếu traffic một phần thất bại, giữ circuit mở thêm thời gian phục hồi

## Các Lợi Ích Chính

### 1. Thất Bại Nhanh
- Yêu cầu thất bại ngay lập tức (trong vòng 1 giây) thay vì chờ timeout (10+ giây)
- Giảm tiêu thụ tài nguyên trên các dịch vụ phụ thuộc
- Cải thiện khả năng đáp ứng tổng thể của hệ thống

### 2. Suy Giảm Tinh Tế (Graceful Degradation)
- Cho phép các cơ chế fallback cho các yêu cầu thất bại
- Cung cấp phản hồi thay thế khi dịch vụ không khả dụng
- Duy trì chức năng một phần trong thời gian gián đoạn

### 3. Phục Hồi Liền Mạch
- Cho các dịch vụ bị lỗi thời gian để phục hồi mà không có traffic đến
- Cho phép các vấn đề tạm thời (vấn đề mạng) tự giải quyết một cách tự nhiên
- Tự động tiếp tục hoạt động bình thường khi dịch vụ phục hồi

## Tóm Tắt

Mẫu Circuit Breaker là thiết yếu để xây dựng kiến trúc microservices có khả năng phục hồi. Bằng cách giám sát các lời gọi dịch vụ, phát hiện lỗi và triển khai quản lý traffic thông minh, nó:

- Ngăn chặn lỗi lan truyền trong mạng lưới microservices
- Cho phép thất bại nhanh và suy giảm tinh tế
- Hỗ trợ phục hồi tự động các dịch vụ bị lỗi tạm thời
- Duy trì sự ổn định tổng thể của hệ thống trong thời gian gián đoạn một phần

Trong các phần tiếp theo, chúng ta sẽ khám phá các chi tiết triển khai thực tế và trình diễn circuit breaker pattern trong môi trường Spring Boot microservices.