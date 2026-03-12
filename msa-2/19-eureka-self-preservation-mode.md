# Chế Độ Tự Bảo Vệ Của Eureka (Self-Preservation Mode)

## Tổng Quan

Tài liệu này giải thích về chế độ tự bảo vệ trong Eureka Server, tại sao nó tồn tại, và cách nó hoạt động để duy trì tính ổn định trong mạng lưới microservice.

## Hiểu Thông Báo Cảnh Báo

Khi bạn thấy thông báo cảnh báo trên bảng điều khiển Eureka, điều này thường do một khái niệm gọi là **chế độ tự bảo vệ**. Cảnh báo này xuất hiện khi Eureka Server kích hoạt cơ chế bảo vệ này.

## Chế Độ Tự Bảo Vệ Là Gì?

Chế độ tự bảo vệ là một tính năng an toàn trong Eureka Server giúp ngăn chặn việc loại bỏ sớm các instance dịch vụ khỏi registry trong trường hợp có vấn đề về mạng hoặc lỗi tạm thời.

### Hoạt Động Bình Thường

Trong một mạng lưới microservice hoạt động bình thường:
- Eureka Server mong đợi nhận heartbeat từ các instance microservice đã đăng ký
- Nếu không nhận được heartbeat trong một khoảng thời gian nhất định, Eureka cho rằng instance đó không phản hồi, bị crash hoặc không khỏe mạnh
- Hành vi mặc định là xóa instance không phản hồi khỏi service registry
- Điều này giúp duy trì cái nhìn cập nhật về tất cả các instance dịch vụ khỏe mạnh đã đăng ký

### Vấn Đề: Lỗi Mạng

Các vấn đề về mạng có thể xảy ra trong thực tế - các website có thể tạm thời không khả dụng trong vài giây hoặc vài phút trước khi có thể truy cập trở lại. Các lỗi mạng tương tự có thể xảy ra trong mạng lưới microservice:

- Độ trễ hệ thống tạm thời hoặc lỗi mạng có thể khiến Eureka Server bỏ lỡ các heartbeat
- Điều này dẫn đến việc hết hạn sai hoặc loại bỏ nhầm các instance dịch vụ khỏe mạnh
- Việc loại bỏ không cần thiết gây ra sự không ổn định và gián đoạn trong mạng lưới microservice

**Ví Dụ Kịch Bản:**
- Lỗi mạng xảy ra trong 5 phút
- Eureka Server không nhận được bất kỳ heartbeat nào trong thời gian này
- Nếu Eureka loại bỏ tất cả các instance, registry sẽ trở nên trống rỗng
- Các dịch vụ client cố gắng khám phá microservice sẽ gặp ngoại lệ
- Service discovery và client-side load balancing thất bại

## Cách Chế Độ Tự Bảo Vệ Hoạt Động

### Kích Hoạt

Eureka Server chuyển sang chế độ tự bảo vệ khi nhận ra rằng phần lớn các instance microservice không gửi heartbeat. Thay vì ngay lập tức loại bỏ tất cả các instance dịch vụ:

1. Eureka chuyển sang chế độ tự bảo vệ
2. Ngay cả khi không nhận được tín hiệu heartbeat, nó không loại bỏ chi tiết dịch vụ khỏi registry
3. Điều này ngăn chặn việc loại bỏ tất cả các instance do độ trễ mạng tạm thời hoặc lỗi

### Trong Chế Độ Tự Bảo Vệ

- Eureka Server tiếp tục cung cấp các instance đã đăng ký cho các ứng dụng client
- Nó duy trì chế độ này ngay cả khi nghi ngờ một số instance không còn khả dụng
- Giả định rằng lỗi mạng có thể chỉ tồn tại giữa Eureka Server và các instance
- Điều này duy trì tính ổn định và khả dụng của service registry
- Client vẫn có thể khám phá và tương tác với các instance khả dụng

### Hủy Kích Hoạt

Chế độ tự bảo vệ tiếp tục cho đến khi:
- Đạt được ngưỡng cụ thể của các instance khỏe mạnh, HOẶC
- Các dịch vụ down được đưa trở lại online, HOẶC
- Lỗi mạng được giải quyết

## Ví Dụ Trực Quan

### Trạng Thái Ban Đầu (Trước Khi Có Vấn Đề Mạng)
- 5 instance của loans microservice được đăng ký
- Tất cả các instance gửi heartbeat mỗi 30 giây
- Eureka hiển thị tất cả 5 instance đều UP

### Vấn Đề Mạng Xảy Ra
- Vấn đề mạng giữa Eureka và các instance microservice
- Instance 4 và Instance 5 ngừng gửi heartbeat
- Eureka không loại bỏ chúng ngay lập tức
- Eureka cho 3 cơ hội (chờ tổng cộng 90 giây)
- Nếu không nhận được heartbeat sau 90 giây, Instance 4 và 5 bị loại bỏ
- Registry bây giờ chỉ hiển thị instance 1, 2, và 3

### Chế Độ Tự Bảo Vệ Được Kích Hoạt
- Eureka nhận ra 15% tổng số instance đã hết hạn (ngưỡng mặc định là 85%)
- Chuyển sang chế độ tự bảo vệ
- Bây giờ nếu Instance 3 cũng ngừng gửi heartbeat, nó sẽ không bị loại bỏ
- Instance 3 vẫn còn trong registry mặc dù thiếu heartbeat

## Các Thuộc Tính Cấu Hình

### 1. Khoảng Thời Gian Gia Hạn Lease
```yaml
eureka.instance.lease-renewal-interval-in-seconds: 30
```
- Mặc định: 30 giây
- Xác định tần suất Eureka Server mong đợi nhận tín hiệu heartbeat từ các client microservice

### 2. Thời Lượng Hết Hạn Lease
```yaml
eureka.instance.lease-expiration-duration-in-seconds: 90
```
- Mặc định: 90 giây
- Thời gian tối đa Eureka chờ để nhận một heartbeat
- Nếu không có heartbeat trong vòng 90 giây, instance có thể bị loại bỏ

### 3. Bộ Đếm Thời Gian Khoảng Loại Bỏ
```yaml
eureka.server.eviction-interval-timer-in-ms: 60000
```
- Mặc định: 60,000 mili giây (60 giây)
- Tần suất chạy của bộ lập lịch loại bỏ
- Bộ lập lịch kiểm tra xem chế độ tự bảo vệ có được kích hoạt không
- Nếu không kích hoạt: thực hiện quá trình loại bỏ
- Nếu kích hoạt: bỏ qua loại bỏ

### 4. Ngưỡng Phần Trăm Gia Hạn
```yaml
eureka.server.renewal-percent-threshold: 0.85
```
- Mặc định: 0.85 (85%)
- Được sử dụng để tính toán phần trăm mong đợi của heartbeat mỗi phút
- Nếu Eureka nhận được ít hơn 85% heartbeat mong đợi, nó chuyển sang chế độ tự bảo vệ

### 5. Khoảng Cập Nhật Ngưỡng Gia Hạn
```yaml
eureka.server.renewal-threshold-update-interval-ms: 900000
```
- Mặc định: 900,000 mili giây (15 phút)
- Bộ lập lịch chạy mỗi 15 phút để tính toán tổng số heartbeat mong đợi
- Giúp Eureka thích ứng với thay đổi về số lượng instance đã đăng ký
- Dựa trên tổng số heartbeat, tính toán giá trị ngưỡng để kích hoạt chế độ tự bảo vệ

### 6. Bật Tự Bảo Vệ
```yaml
eureka.server.enable-self-preservation: true
```
- Mặc định: true
- Đặt thành false để vô hiệu hóa vĩnh viễn chế độ tự bảo vệ
- **Cảnh báo:** Vô hiệu hóa tính năng này có thể dẫn đến vấn đề ổn định trong lỗi mạng

## Hiểu Cảnh Báo Trên Dashboard

Khi chế độ tự bảo vệ hoạt động, bạn sẽ thấy cảnh báo này:

> **KHẨN CẤP! EUREKA CÓ THỂ ĐANG SAI KHI TUYÊN BỐ CÁC INSTANCE ĐANG HOẠT ĐỘNG KHI CHÚNG KHÔNG. GIA HẠN ÍT HƠN NGƯỠNG VÀ DO ĐÓ CÁC INSTANCE KHÔNG BỊ HẾT HẠN CHỈ ĐỂ AN TOÀN.**

**Dịch nghĩa:**
- Chi tiết instance được hiển thị có thể không chính xác
- Heartbeat (gia hạn) ít hơn ngưỡng mong đợi
- Các instance không bị hết hạn như một biện pháp an toàn
- Đây là cơ chế bảo vệ, không phải lỗi

## Thực Hành Tốt Nhất

### Đừng Hoảng Sợ
Khi bạn thấy cảnh báo tự bảo vệ:
- Đây là cơ chế bảo vệ bình thường
- Khi vấn đề mạng được giải quyết, cảnh báo sẽ tự động biến mất
- Các instance microservice sẽ tiếp tục gửi tín hiệu heartbeat
- Eureka sẽ thoát khỏi chế độ tự bảo vệ

### Khi Nào Nên Vô Hiệu Hóa Tự Bảo Vệ
Cân nhắc vô hiệu hóa chế độ tự bảo vệ chỉ khi:
- Mạng của bạn cực kỳ ổn định
- Bạn có cơ chế thay thế để xử lý lỗi mạng
- Bạn hiểu rủi ro của việc có một service registry trống

**Rủi Ro Khi Vô Hiệu Hóa:**
- Tất cả chi tiết dịch vụ có thể bị xóa trong lỗi mạng
- Service registry trở nên trống rỗng
- Dẫn đến vấn đề ổn định trong mạng lưới microservice
- Không ai có thể cứu mạng lưới microservice của bạn khỏi các lỗi dây chuyền

## Tóm Tắt

- **Mục đích:** Eureka Server không hoảng sợ khi không nhận được heartbeat từ phần lớn các instance
- **Hành vi:** Giữ bình tĩnh và chuyển sang chế độ tự bảo vệ (như thiền định)
- **Trong Chế Độ:** Không loại bỏ các instance khỏi service registry
- **Trường Hợp Sử Dụng:** Tính năng cứu cánh khi lỗi mạng phổ biến
- **Kết Quả:** Giúp xử lý các cảnh báo dương tính giả và duy trì tính khả dụng của dịch vụ

## Kết Luận

Chế độ tự bảo vệ là một tính năng quan trọng để duy trì tính ổn định của microservice. Nó ngăn chặn các lỗi thảm khốc do vấn đề mạng tạm thời bằng cách giữ nguyên service registry. Hiểu được cơ chế này giúp các nhà phát triển và vận hành đưa ra quyết định có cơ sở về kiến trúc microservice của họ và tránh hoảng sợ không cần thiết khi thấy thông báo cảnh báo.