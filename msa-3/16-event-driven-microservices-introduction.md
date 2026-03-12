# Xây Dựng Microservices Hướng Sự Kiện (Event-Driven)

## Giới Thiệu

Phần này giới thiệu **Thử thách #10: Xây dựng Microservices hướng sự kiện**. Chúng ta sẽ khám phá microservices hướng sự kiện là gì, tại sao chúng quan trọng, và cách triển khai chúng trong kiến trúc microservices của bạn.

## Hiểu Về Temporal Coupling (Khớp Nối Thời Gian)

### Loose Coupling vs Temporal Coupling

**Loose Coupling (Khớp nối lỏng lẻo)** là nguyên tắc thiết kế trong đó chúng ta xây dựng logic nghiệp vụ ứng dụng trong các microservices riêng biệt để chúng có thể:
- Phát triển độc lập
- Triển khai độc lập
- Mở rộng độc lập

Ví dụ, trong khóa học chúng ta đã tách:
- Logic tài khoản → Accounts microservice
- Logic thẻ → Cards microservice
- Logic vay → Loans microservice

**Temporal Coupling (Khớp nối thời gian)** xảy ra khi một service gọi đến service khác và mong đợi nhận phản hồi ngay lập tức trước khi tiếp tục xử lý.

### Ví Dụ Về Temporal Coupling

Xét hai microservices:
- **Microservice1** (người gọi) phụ thuộc vào **Microservice2** (người được gọi)
- Khi Microservice1 gọi đến Microservice2, nó liên tục chờ đợi phản hồi
- Bất kỳ hành vi chậm trễ nào của Microservice2 đều ảnh hưởng trực tiếp đến hiệu suất của Microservice1

**Điểm chính:** Temporal coupling xảy ra với giao tiếp đồng bộ (synchronous communication), đặc biệt khi sử dụng REST APIs.

## Tránh Temporal Coupling

### Giải Pháp: Giao Tiếp Bất Đồng Bộ

Để tránh temporal coupling, chúng ta nên sử dụng **giao tiếp bất đồng bộ (asynchronous communication)** bất cứ khi nào có thể trong mạng lưới microservices. Giao tiếp đồng bộ không phải lúc nào cũng cần thiết - nhiều tình huống thực tế có thể được thực hiện hiệu quả với các mẫu bất đồng bộ.

## Các Cách Tiếp Cận Giao Tiếp Đồng Bộ

### 1. Phương Pháp Imperative (Mệnh Lệnh)
- Một thread chuyên dụng được gán cho giao tiếp
- Thread bị **chặn (blocked)** trong khi chờ phản hồi
- Thread ở trạng thái idle cho đến khi Microservice2 phản hồi
- Sử dụng thread kém hiệu quả

### 2. Phương Pháp Reactive (Phản Ứng)
- Một thread khởi tạo cuộc gọi đến Microservice2
- Thread quay lại thread pool sau khi gọi
- Thread xử lý request tiếp theo có sẵn
- Thread chỉ được gán khi phản hồi đến
- Sử dụng thread hiệu quả hơn

**Quan trọng:** Cả hai phương pháp vẫn sử dụng giao tiếp đồng bộ - Microservice1 không thể tiếp tục logic nghiệp vụ tiếp theo cho đến khi nhận được phản hồi từ Microservice2.

## Khi Nào Sử Dụng Giao Tiếp Đồng Bộ

Giao tiếp đồng bộ phù hợp cho **các tình huống nghiệp vụ quan trọng** yêu cầu phản hồi ngay lập tức cho người dùng cuối.

### Ví Dụ: Ứng Dụng Ngân Hàng
- Người dùng nhấp vào nút để kiểm tra số dư tài khoản hiện tại
- Người dùng mong đợi nhìn thấy phản hồi ngay lập tức trên màn hình
- Giao tiếp đồng bộ là cần thiết trong trường hợp này

## Microservices Hướng Sự Kiện

### Sự Kiện (Event) Là Gì?

**Sự kiện (Event)** là một sự cố xảy ra bên trong microservices của bạn, biểu thị:
- Sự chuyển đổi trạng thái
- Một cập nhật trong hệ thống

Khi một sự kiện xảy ra, các bên liên quan phải được thông báo.

### Ví Dụ Thực Tế: Ứng Dụng Thương Mại Điện Tử

Xét quy trình xử lý đơn hàng của Amazon:

1. **Order Microservice**: Khi người dùng hoàn tất thanh toán, đơn hàng được xác nhận
2. **Sự kiện được kích hoạt**: Order microservice tạo ra một sự kiện/thông báo
3. **Delivery Microservice**: Nhận thông báo
4. **Lợi ích chính**: Order microservice không chờ đợi quá trình giao hàng hoàn thành

**Đây là giao tiếp bất đồng bộ:**
- Order microservice gửi thông báo
- Công việc của nó đã hoàn thành
- Không chờ đợi phản hồi từ delivery microservice

## Xây Dựng Microservices Hướng Sự Kiện

Để triển khai microservices hướng sự kiện, bạn cần:

### Các Thành Phần Kiến Trúc
1. **Event-Driven Architecture**: Mẫu thiết kế để tạo và tiêu thụ sự kiện
2. **Asynchronous Communication**: Truyền thông điệp không chặn
3. **Event Brokers**: Phần mềm trung gian để phân phối sự kiện

### Hệ Sinh Thái Spring Cloud

Tận dụng các dự án Spring Cloud sau:
- **Spring Cloud Function**: Để xây dựng các event handler
- **Spring Cloud Stream**: Để xây dựng microservices hướng sự kiện

## Tóm Tắt

Microservices hướng sự kiện mang lại:
- ✅ Giảm temporal coupling
- ✅ Khả năng mở rộng tốt hơn
- ✅ Cải thiện khả năng phục hồi của hệ thống
- ✅ Sử dụng tài nguyên hiệu quả hơn

Trong các bài giảng tiếp theo, chúng ta sẽ khám phá chi tiết thế giới của microservices hướng sự kiện!

---

**Bước Tiếp Theo:** Tìm hiểu cách triển khai kiến trúc hướng sự kiện sử dụng Spring Cloud Function và Spring Cloud Stream.