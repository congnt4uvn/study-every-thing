# Giao Tiếp Bất Đồng Bộ với Mô Hình Pub/Sub trong Microservices

## Tổng Quan

Tài liệu này giải thích cách triển khai giao tiếp bất đồng bộ sử dụng mô hình Publish/Subscribe (Pub/Sub) trong kiến trúc microservices với Spring Boot và RabbitMQ.

## Kiến Trúc Hiện Tại

Hệ sinh thái microservices của chúng ta hiện bao gồm:
- **Accounts Microservice** - Xử lý các thao tác CRUD trên tài khoản
- **Cards Microservice** - Quản lý các thao tác thẻ
- **Loans Microservice** - Quản lý các thao tác khoản vay

Các microservices này hiện đang sử dụng **giao tiếp đồng bộ** cho các thao tác nghiệp vụ quan trọng yêu cầu phản hồi ngay lập tức cho người dùng cuối.

## Tại Sao Cần Giao Tiếp Bất Đồng Bộ?

Trong khi giao tiếp đồng bộ là cần thiết cho các thao tác quan trọng, một số tình huống được hưởng lợi từ xử lý bất đồng bộ:
- Gửi thông báo (SMS/Email)
- Các tác vụ xử lý nền
- Tách rời các dịch vụ phụ thuộc
- Cải thiện khả năng phục hồi của hệ thống

## Kịch Bản: Tạo Tài Khoản với Thông Báo Bất Đồng Bộ

### Vấn Đề

Khi tạo tài khoản mới, hai thao tác xảy ra:
1. **Quan trọng**: Tạo tài khoản và lưu vào cơ sở dữ liệu (yêu cầu phản hồi ngay lập tức)
2. **Không quan trọng**: Gửi thông báo cho người dùng (có thể xử lý bất đồng bộ)

Chúng ta không muốn Accounts microservice phải xử lý tất cả logic giao tiếp trực tiếp.

### Giải Pháp: Pub/Sub với RabbitMQ

Chúng ta sẽ triển khai một **Message Microservice** mới chuyên xử lý các giao tiếp, sử dụng RabbitMQ làm event broker.

## Luồng Triển Khai

### Bước 1-2: Tạo Tài Khoản (Đồng Bộ)
```
Người dùng → Accounts Microservice → Cơ sở dữ liệu
```
- Người dùng gửi yêu cầu tạo tài khoản mới
- Accounts microservice tạo tài khoản trong cơ sở dữ liệu
- Phản hồi ngay lập tức được gửi cho người dùng: "Tài khoản đã được tạo thành công"

### Bước 3: Phát Hành Event (Bắt Đầu Bất Đồng Bộ)
```
Accounts Microservice → Event Broker (RabbitMQ) → Queue
```
- Accounts microservice phát hành một event đến event broker
- Event chứa thông tin chi tiết về việc tạo tài khoản
- Event được đặt vào một queue

### Bước 4: Tiêu Thụ Event
```
Queue → Message Microservice → Người dùng (SMS/Email)
```
- Message microservice liên tục giám sát queue
- Khi phát hiện event, nó đọc chi tiết event
- Gửi thông báo SMS/Email cho người dùng

### Bước 5-6: Luồng Xác Nhận (Bất Đồng Bộ Ngược)
```
Message Microservice → Event Broker → Queue Khác
```
- Sau khi xử lý, Message microservice phát hành một event xác nhận
- Event được đặt vào queue mà Accounts microservice đang giám sát

### Bước 7: Cập Nhật Trạng Thái
```
Queue → Accounts Microservice → Cập Nhật Cơ sở dữ liệu
```
- Accounts microservice nhận thông báo
- Cập nhật cột cơ sở dữ liệu: "Giao tiếp đã được gửi cho khách hàng"

## Lợi Ích Chính

### 1. **Ghép Nối Lỏng Lẻo**
- Các microservices không biết về nhau trực tiếp
- Chúng chỉ tương tác với event broker
- Dễ dàng thêm subscribers mới mà không cần sửa đổi publishers

### 2. **Khả Năng Phục Hồi**
- Nếu Message microservice chậm hoặc ngừng hoạt động, Accounts microservice không bị ảnh hưởng
- Các event được xếp hàng cho đến khi consumers sẵn sàng
- Không có lỗi dây chuyền

### 3. **Tách Biệt Các Mối Quan Tâm**
- Accounts microservice tập trung vào quản lý tài khoản
- Message microservice tập trung vào giao tiếp
- Trách nhiệm đơn lẻ rõ ràng

### 4. **Khả Năng Mở Rộng**
- Có thể mở rộng Message microservice độc lập dựa trên tải thông báo
- Nhiều instances có thể tiêu thụ từ cùng một queue

## Ngăn Xếp Công Nghệ

- **Event Broker**: RabbitMQ (Mô hình Pub/Sub)
- **Framework**: Spring Boot
- **Pattern**: Kiến trúc Hướng Sự Kiện
- **Mô Hình Giao Tiếp**: Tin nhắn bất đồng bộ

## Các Thành Phần Kiến Trúc

### Accounts Microservice
- Phát hành các event tạo tài khoản
- Đăng ký nhận các event xác nhận giao tiếp
- Cập nhật trạng thái tài khoản trong cơ sở dữ liệu

### Message Microservice (Mới)
- Đăng ký nhận các event tạo tài khoản
- Gửi thông báo SMS/Email
- Phát hành các event xác nhận giao tiếp

### Event Broker (RabbitMQ)
- Quản lý các message queues
- Định tuyến events giữa publishers và subscribers
- Đảm bảo giao hàng tin nhắn đáng tin cậy

## Những Cân Nhắc Quan Trọng

1. **Khi Nào Sử Dụng Giao Tiếp Đồng Bộ**
   - Các thao tác nghiệp vụ quan trọng yêu cầu phản hồi ngay lập tức
   - Các thao tác mà tính nhất quán là bắt buộc
   - Các thao tác hướng người dùng cần phản hồi tức thì

2. **Khi Nào Sử Dụng Giao Tiếp Bất Đồng Bộ**
   - Các tác vụ nền không quan trọng
   - Thông báo và cảnh báo
   - Các quy trình chạy lâu
   - Đồng bộ hóa dữ liệu giữa các dịch vụ

## Các Bước Tiếp Theo

Trong các bài giảng sắp tới, chúng ta sẽ đề cập:
- Thiết lập RabbitMQ làm event broker
- Cấu hình queues và exchanges
- Triển khai publishers trong Accounts microservice
- Triển khai subscribers trong Message microservice
- Xử lý lỗi và cơ chế thử lại
- Giám sát và khả năng quan sát

## Kết Luận

Bằng cách triển khai mô hình Pub/Sub với RabbitMQ, chúng ta đạt được một kiến trúc microservices có khả năng phục hồi, mở rộng và bảo trì tốt hơn. Mẫu giao tiếp bất đồng bộ cho phép chúng ta tách rời các dịch vụ trong khi vẫn duy trì độ tin cậy của hệ thống.