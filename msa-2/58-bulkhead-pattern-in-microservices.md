# Mẫu Thiết Kế Bulkhead trong Microservices

## Giới Thiệu

Mẫu thiết kế Bulkhead là một mẫu thiết kế về khả năng phục hồi giúp cải thiện sự cô lập và ổn định của các thành phần hoặc dịch vụ trong kiến trúc microservice. Mẫu thiết kế này được lấy cảm hứng từ các vách ngăn thực tế được sử dụng trong tàu thuyền để ngăn nước tràn vào toàn bộ con tàu nếu một khoang bị thủng.

## Hiểu Về Mẫu Thiết Kế Bulkhead

### Phép So Sánh Với Vách Ngăn Tàu Thuyền

Mẫu thiết kế này lấy tên từ kỹ thuật phân chia khoang được sử dụng trong tàu thuyền. Giống như tàu Titanic có các vách ngăn ngăn chặn việc ngập nước toàn bộ con tàu khi va chạm với tảng băng trôi, mẫu thiết kế Bulkhead trong kiến trúc phần mềm ngăn chặn sự cố ở một thành phần ảnh hưởng đến toàn bộ hệ thống.

### Lợi Ích Chính

Với mẫu thiết kế Bulkhead, bạn có thể:

- **Cô lập sự cố**: Hạn chế tác động của sự cố hoặc tải cao ở một thành phần lan rộng sang các thành phần khác
- **Ngăn chặn cạn kiệt tài nguyên**: Đảm bảo rằng tải cao ở một phần của hệ thống không làm sập toàn bộ hệ thống
- **Cho phép hoạt động độc lập**: Cho phép các thành phần khác tiếp tục hoạt động độc lập ngay cả khi một thành phần đang chịu áp lực
- **Xác định ranh giới tài nguyên**: Phân bổ hoặc chỉ định tài nguyên cho các REST API cụ thể hoặc microservices cụ thể để tránh sử dụng tài nguyên quá mức

## Ví Dụ Thực Tế: Microservice Tài Khoản

### Không Có Mẫu Thiết Kế Bulkhead

Xem xét một microservice Tài khoản với hai REST API:

1. **API myAccount**: Một REST API đơn giản không phụ thuộc vào các microservices khác
2. **API myCustomerDetails**: Một REST API phức tạp phụ thuộc vào các microservices khác như Khoản vay và Thẻ

**Vấn đề**: Không có mẫu thiết kế Bulkhead, API `myCustomerDetails` (có độ phức tạp và thời gian xử lý cao hơn) sẽ tiêu thụ tất cả các luồng và tài nguyên có sẵn trong container Docker. Điều này ảnh hưởng đến hiệu suất của API `myAccount` đơn giản hơn, có thể không nhận đủ luồng hoặc tài nguyên để xử lý các yêu cầu từ khách hàng.

### Với Mẫu Thiết Kế Bulkhead

Bằng cách triển khai mẫu thiết kế Bulkhead:

- Xác định ranh giới rõ ràng cho mỗi REST API
- Chỉ định các luồng và tài nguyên cụ thể từ thread pool cho mỗi API
- API `myAccount` có thể hoạt động hiệu quả bất kể `myCustomerDetails` nhận bao nhiêu yêu cầu
- Mỗi API nhận được số lượng luồng tối thiểu được đảm bảo từ thread pool

## Triển Khai Với Resilience4j

### Lưu Ý Quan Trọng

Hiện tại, Spring Cloud Gateway không hỗ trợ mẫu thiết kế Bulkhead một cách tự nhiên. Bạn chỉ có thể triển khai mẫu thiết kế Bulkhead bằng cách sử dụng thư viện **Resilience4j**.

### Sử Dụng Annotation @Bulkhead

```java
@Bulkhead(name = "myBulkhead", type = Bulkhead.Type.THREADPOOL)
public Response myMethod() {
    // Logic nghiệp vụ của bạn
}
```

### Các Thuộc Tính Cấu Hình

#### Cấu Hình Bulkhead Tiêu Chuẩn

- **maxConcurrentCalls**: Số lượng cuộc gọi đồng thời tối đa mà một bulkhead cụ thể có thể hỗ trợ trên một REST API
- **maxWaitDuration**: Thời gian tối đa để chờ quyền thực thi

#### Cấu Hình Thread Pool Bulkhead

Để kiểm soát chi tiết hơn việc phân bổ luồng:

- **maxThreadPoolSize**: Kích thước tối đa của thread pool
- **coreThreadPoolSize**: Kích thước cốt lõi của thread pool
- **queueCapacity**: Dung lượng của hàng đợi cho các yêu cầu đang chờ

## Kiểm Tra Và Xác Thực

Để xác thực đúng cách việc triển khai mẫu thiết kế Bulkhead, bạn cần:

- Các công cụ kiểm tra hiệu suất thương mại (ví dụ: LoadRunner, JMeter)
- Khả năng giám sát việc sử dụng luồng và phân bổ tài nguyên
- Sự cộng tác với nhóm kiểm tra hiệu suất của bạn

## Tóm Tắt

Mẫu thiết kế Bulkhead rất cần thiết khi bạn cần:

- Xác định ranh giới tài nguyên cho các API trong microservices của bạn
- Ngăn một API độc quyền tài nguyên hệ thống
- Tăng cường khả năng phục hồi và ổn định tổng thể của kiến trúc microservice của bạn

Bằng cách tận dụng mẫu thiết kế này với kiểm tra hiệu suất phù hợp, bạn có thể đảm bảo rằng microservices của bạn duy trì sự ổn định ngay cả trong các điều kiện tải khác nhau.

## Khi Nào Sử Dụng

Cân nhắc triển khai mẫu thiết kế Bulkhead khi:

- Bạn có các API với yêu cầu tài nguyên khác nhau đáng kể
- Một số API phụ thuộc vào nhiều microservices bên ngoài
- Bạn cần đảm bảo mức hiệu suất tối thiểu cho các API quan trọng
- Bạn muốn ngăn chặn các lỗi lan rộng trong hệ thống của bạn