# Demo Hoàn Chỉnh: Giao Tiếp Bất Đồng Bộ Giữa Các Microservices Với RabbitMQ

## Tổng Quan

Hướng dẫn này trình bày việc triển khai hoàn chỉnh giao tiếp bất đồng bộ giữa các microservices Accounts và Message sử dụng RabbitMQ trong kiến trúc microservices Spring Boot.

## Yêu Cầu Trước Khi Bắt Đầu

Trước khi bắt đầu, hãy đảm bảo bạn có:
- RabbitMQ server đang chạy
- Accounts microservice
- Message microservice
- Gateway server application

## Bắt Đầu

### Bước 1: Khởi Động Lại Các Ứng Dụng

Sau khi thực hiện các thay đổi đáng kể đối với Accounts và Message microservices, hãy khởi động lại tất cả các ứng dụng:

1. **Accounts Microservice** - Khởi động lại đầu tiên
2. **Message Microservice** - Khởi động lại sau Accounts
3. **Gateway Server Application** - Khởi động lại cuối cùng (phụ thuộc vào Accounts microservice)

> **Quan trọng**: Luôn khởi động lại các microservices phụ thuộc khi khởi động lại Accounts microservice.

## Xác Minh Cấu Hình RabbitMQ

### Exchanges (Trao Đổi)

Truy cập vào RabbitMQ console và xác minh các exchanges sau:

1. **send-communication** - Exchange chính để gửi thông tin liên lạc
2. **communication-sent** - Exchange để cập nhật trạng thái liên lạc

> **Lưu ý**: Bạn có thể thấy một exchange mồ côi `emailsms-out-zero` nếu trước đó bạn không định nghĩa đích cho output bindings. Exchange này sẽ không xuất hiện trong các RabbitMQ container mới.

### Queues (Hàng Đợi)

Kiểm tra phần queues và streams:

- **communication-sent.accounts** - Hàng đợi được Accounts microservice theo dõi để nhận tin nhắn từ Message microservice

## Kiểm Thử Luồng Bất Đồng Bộ

### Bước 1: Lấy Access Token

Sử dụng Postman để lấy access token mới từ authentication server.

### Bước 2: Tạo Tài Khoản Mới

1. Gửi POST request để tạo tài khoản mới với số điện thoại (ví dụ: kết thúc bằng 687)
2. Phản hồi mong đợi: `201 Account created successfully`
3. Thời gian phản hồi: ~1 giây

### Bước 3: Quan Sát Xử Lý Bất Đồng Bộ

Phản hồi nhanh chỉ ra xử lý bất đồng bộ:
- Tạo tài khoản hoàn thành ngay lập tức
- Giao tiếp với người dùng cuối diễn ra ở chế độ nền
- Message microservice xử lý yêu cầu giao tiếp một cách độc lập

## Các Bước Xác Minh

### Kiểm Tra Trạng Thái Database Ban Đầu

1. Truy cập H2 console tại cổng `8080` (Accounts microservice)
2. Truy vấn bảng `accounts`
3. Quan sát giá trị cột `communication_switch`: `null`

Điều này cho thấy giao tiếp với người dùng cuối chưa hoàn thành.

### Theo Dõi Xử Lý Message

Khi Message microservice hoàn thành giao tiếp:
1. Nó stream một event đến Accounts microservice
2. Event kích hoạt cập nhật bảng accounts

### Xác Minh Trạng Thái Cuối Cùng

1. Chạy lại truy vấn trong H2 console
2. Cột `communication_switch` bây giờ hiển thị: `true`
3. Điều này xác nhận giao tiếp bất đồng bộ thành công

## Lợi Ích Của Kiến Trúc

### Triển Khai Event Streaming

Demo này triển khai thành công event streaming trong mạng lưới microservices EasyBank:

- **Giảm Sự Phụ Thuộc Thời Gian**: Các microservices không bị ràng buộc chặt chẽ về thời gian
- **Cải Thiện Khả Năng Mở Rộng**: Các services có thể xử lý requests độc lập
- **Độ Bền Tốt Hơn**: Lỗi ở một service không chặn các services khác
- **Xử Lý Bất Đồng Bộ**: Các tác vụ chạy lâu không chặn API responses

### Các Phương Pháp Tốt Nhất

1. **Tận Dụng Event Streaming**: Sử dụng khả năng event streaming bất cứ khi nào có thể
2. **Tách Rời Services**: Giảm sự phụ thuộc giữa các microservices
3. **Giám Sát Queues**: Thường xuyên kiểm tra RabbitMQ console để theo dõi tình trạng queue
4. **Kiểm Thử Bất Đồng Bộ**: Xác minh cả phản hồi tức thì và tính nhất quán cuối cùng

## Triển Khai Docker

### Chuẩn Bị

1. Tạo Docker images cụ thể cho triển khai này
2. Push images lên Docker Hub
3. Cập nhật file Docker Compose với các phiên bản image mới

### Kiểm Thử Trong Docker

Sử dụng file Docker Compose đã cập nhật để:
1. Khởi động tất cả các containers
2. Kiểm thử kịch bản hoàn chỉnh từ đầu đến cuối
3. Xác minh giao tiếp bất đồng bộ trong môi trường container

## Tóm Tắt

Triển khai này trình bày:
- ✅ Giao tiếp bất đồng bộ giữa các microservices
- ✅ Tích hợp RabbitMQ với Spring Cloud Stream
- ✅ Event streaming để cập nhật trạng thái
- ✅ Giảm sự phụ thuộc thời gian
- ✅ Triển khai sẵn sàng cho Docker

## Tài Liệu Tham Khảo

Để nhanh chóng ôn lại tất cả các bước đã đề cập, hãy tham khảo các slides và tài liệu đi kèm mô tả quy trình triển khai hoàn chỉnh.

## Các Bước Tiếp Theo

1. Xem xét cấu hình Docker Compose
2. Kiểm thử triển khai trong môi trường Docker
3. Giám sát các chỉ số RabbitMQ và hiệu suất queue
4. Triển khai các mẫu bất đồng bộ bổ sung khi cần thiết

---

**Lưu ý**: Hướng dẫn này là một phần của khóa học toàn diện về kiến trúc microservices bao gồm các mẫu event-driven với Spring Boot và RabbitMQ.