# Các Mô Hình Microservices Hướng Sự Kiện

## Giới Thiệu

Khi xây dựng microservices hướng sự kiện trong môi trường production, có hai mô hình chính được sử dụng rộng rãi trong ngành:

1. **Mô Hình Publisher-Subscriber (Pub/Sub)**
2. **Mô Hình Event Streaming**

Tài liệu này sẽ khám phá cả hai mô hình, sự khác biệt giữa chúng và khi nào nên sử dụng từng phương pháp.

## Mô Hình Publisher-Subscriber (Pub/Sub)

### Tổng Quan

Mô hình Pub/Sub xoay quanh các subscription (đăng ký) trong đó:

- **Producers (Nhà sản xuất)** tạo ra các sự kiện
- Sự kiện được phân phối đến tất cả **subscribers (người đăng ký)** quan tâm để tiêu thụ
- Mỗi subscriber nhận các sự kiện mà họ đã đăng ký

### Đặc Điểm Chính

- Một khi sự kiện được nhận và tiêu thụ bởi consumers, **nó không thể được phát lại**
- Subscribers mới tham gia sau sẽ **không có quyền truy cập vào các sự kiện trong quá khứ**
- Sự kiện được tiêu thụ theo thời gian thực khi chúng xảy ra
- Lý tưởng cho các tình huống không yêu cầu phát lại sự kiện lịch sử

### Triển Khai

Mô hình Pub/Sub thường được triển khai sử dụng **RabbitMQ**, một lựa chọn rất phổ biến cho pattern này.

## Mô Hình Event Streaming

### Tổng Quan

Tương tự như Pub/Sub, mô hình Event Streaming bao gồm producers và consumers, nhưng có sự khác biệt về kiến trúc đáng kể.

### Đặc Điểm Chính

- Sự kiện được **ghi vào log theo cách tuần tự**
- Producers phát hành sự kiện khi chúng xảy ra
- Sự kiện được **lưu trữ theo thứ tự rõ ràng**
- Consumers có thể **đọc từ bất kỳ phần nào của luồng sự kiện**
- **Sự kiện có thể được phát lại**, cho phép clients tham gia bất cứ lúc nào
- Subscribers mới có thể nhận **tất cả các sự kiện trong quá khứ**

### Khả Năng Phát Lại Sự Kiện

Khả năng phát lại sự kiện là điểm khác biệt chính:

- Consumers có tính linh hoạt để đọc dữ liệu lịch sử
- Subscribers có thể tham gia tại bất kỳ thời điểm nào và truy cập các sự kiện trong quá khứ
- Tính năng phát lại có thể được tắt nếu cần

### Triển Khai

**Apache Kafka** là một nền tảng mạnh mẽ được sử dụng rộng rãi cho xử lý event streaming.

## Lựa Chọn Mô Hình Phù Hợp

### Khi Nào Sử Dụng Pub/Sub

- Kịch bản kinh doanh của bạn **không yêu cầu** consumers đọc các sự kiện trong quá khứ
- Tiêu thụ sự kiện theo thời gian thực là đủ
- Yêu cầu kiến trúc đơn giản hơn
- Chi phí lưu trữ thấp hơn

### Khi Nào Sử Dụng Event Streaming

- Consumers cần khả năng **phát lại các sự kiện trong quá khứ**
- Subscribers mới yêu cầu quyền truy cập vào dữ liệu lịch sử
- Cần các pattern event sourcing
- Audit trails và phát lại sự kiện là yêu cầu kinh doanh

### Lưu Ý Quan Trọng

**Không có phương pháp tốt hay xấu** - sự lựa chọn phụ thuộc vào các kịch bản kinh doanh và yêu cầu cụ thể của bạn.

## Kế Hoạch Triển Khai Khóa Học

Khóa học này sẽ đề cập đến cả hai mô hình trong các phần riêng biệt:

### Phần 1: Xây Dựng Event-Driven Microservices với RabbitMQ

Chúng ta sẽ khám phá triển khai mô hình Pub/Sub sử dụng RabbitMQ, bao gồm:
- Cài đặt và cấu hình RabbitMQ
- Triển khai Producer và Consumer
- Các pattern định tuyến message và exchange

### Phần 2: Xây Dựng Event-Driven Microservices với Apache Kafka

Chúng ta sẽ khám phá triển khai mô hình Event Streaming sử dụng Apache Kafka, bao gồm:
- Kiến trúc và các khái niệm Kafka
- Các pattern event streaming
- Consumer groups và phân vùng (partitioning)

## Tóm Tắt

Cả hai mô hình hướng sự kiện đều cung cấp khả năng mạnh mẽ để xây dựng microservices có khả năng mở rộng:

- **Mô Hình Pub/Sub (RabbitMQ)**: Tốt nhất cho phân phối sự kiện theo thời gian thực mà không cần yêu cầu phát lại
- **Mô Hình Event Streaming (Apache Kafka)**: Tốt nhất khi cần phát lại sự kiện và truy cập dữ liệu lịch sử

Chọn mô hình phù hợp nhất với yêu cầu kinh doanh và các ràng buộc kỹ thuật của bạn.

---

**Các Bước Tiếp Theo**: Trong các bài giảng tiếp theo, chúng ta sẽ bắt đầu khám phá mô hình Pub/Sub với chi tiết triển khai RabbitMQ.