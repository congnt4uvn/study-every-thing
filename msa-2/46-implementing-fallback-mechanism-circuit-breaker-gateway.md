# Triển Khai Cơ Chế Fallback Cho Circuit Breaker Pattern Trong Gateway Server

## Tổng Quan

Hướng dẫn này giải thích cách triển khai cơ chế fallback cho circuit breaker pattern bên trong Spring Cloud Gateway server. Cơ chế fallback cung cấp xử lý lỗi mượt mà thay vì ném các runtime exception đến các ứng dụng client.

## Vấn Đề

Hiện tại, khi circuit breaker được kích hoạt trong Gateway server mà không có cơ chế fallback, nó sẽ ném các runtime exception như:
- Lỗi service không khả dụng
- Lỗi gateway timeout
- Thông báo upstream service không khả dụng

Trong các ứng dụng kinh doanh thực tế, việc ném RuntimeException trực tiếp đến các ứng dụng client hoặc UI không phải là cách tiếp cận hợp lệ. Chúng ta cần một cơ chế fallback phù hợp để cung cấp các phản hồi có ý nghĩa.

## Các Bước Triển Khai

### Bước 1: Tạo Fallback Controller

1. Tạo package mới `controller` bên trong ứng dụng Gateway server
2. Tạo class `FallbackController` với annotation `@RestController`
3. Triển khai REST API endpoint cho phản hồi fallback

```java
@RestController
public class FallbackController {
    
    @RequestMapping("/contactsupport")
    public Mono<String> contactSupport() {
        return Mono.just("Đã xảy ra lỗi. Vui lòng thử lại sau hoặc liên hệ đội ngũ hỗ trợ.");
    }
}
```

**Lưu Ý Quan Trọng:**
- Vì Spring Cloud Gateway được xây dựng trên Spring Reactive, cần wrap String trả về với `Mono`
- Sử dụng `Mono.just()` để trả về thông báo phản hồi
- Tùy chỉnh logic fallback dựa trên yêu cầu nghiệp vụ (ví dụ: kích hoạt email, trả về phản hồi mặc định)

### Bước 2: Cấu Hình Fallback URI Trong Circuit Breaker

Thêm cấu hình fallback URI vào circuit breaker pattern trong ứng dụng Gateway server:

```java
.setFallbackUri("forward:/contactsupport")
```

Cấu hình này cho circuit breaker pattern biết cần chuyển tiếp request đến endpoint `/contactsupport` bất cứ khi nào có exception xảy ra.

### Bước 3: Build Và Test

1. Lưu các thay đổi và build ứng dụng
2. Test với Postman hoặc bất kỳ REST client nào

## Các Kịch Bản Kiểm Thử

### Luồng Request Thành Công
- Gửi request đến service
- Xác minh phản hồi thành công từ microservice thực tế
- Cơ chế fallback **không được gọi**
- Trạng thái circuit breaker hiển thị là **CLOSED**

### Mô Phỏng Phản Hồi Chậm
1. Đặt breakpoint trong accounts controller để mô phỏng phản hồi chậm
2. Gửi request - nó sẽ dừng tại breakpoint
3. Thay vì nhận "gateway timeout" hoặc "upstream service unavailable", client nhận được:
   ```
   Đã xảy ra lỗi. Vui lòng thử lại sau hoặc liên hệ đội ngũ hỗ trợ.
   ```
4. Các ứng dụng client không bao giờ biết điều gì đang xảy ra đằng sau
5. Giải phóng breakpoint - các request thành công tiếp theo sẽ bỏ qua fallback

## Tóm Tắt Các Bước Triển Khai

### 1. Thêm Maven Dependency
Thêm dependency Circuit Breaker vào `pom.xml` của Gateway Server

### 2. Cấu Hình Circuit Breaker Filter
Gọi circuit breaker filter nội bộ và định nghĩa:
- Tên circuit breaker
- Fallback URI

### 3. Cấu Hình Properties Trong application.yml
Thiết lập các thuộc tính circuit breaker sau:
- `slidingWindowSize` - Số lượng cuộc gọi cần theo dõi
- `permittedNumberOfCallsInHalfOpenState` - Số cuộc gọi được phép ở trạng thái half-open
- `failureRateThreshold` - Ngưỡng phần trăm để mở circuit
- `waitDurationInOpenState` - Thời gian chờ trước khi chuyển sang trạng thái half-open

## Lợi Ích

- **Xử Lý Lỗi Mượt Mà**: Ứng dụng client nhận được thông báo lỗi có ý nghĩa
- **Trải Nghiệm Người Dùng Tốt Hơn**: Không có runtime exception khó hiểu được hiển thị cho người dùng cuối
- **Tính Linh Hoạt**: Dễ dàng tùy chỉnh logic fallback dựa trên yêu cầu nghiệp vụ
- **Tính Minh Bạch**: Các vấn đề backend được ẩn khỏi ứng dụng client

## Các Bước Tiếp Theo

Chủ đề tiếp theo sẽ đề cập đến việc triển khai circuit breaker pattern bên trong các microservice riêng lẻ, chẳng hạn như accounts microservice, thay vì chỉ ở cấp độ gateway.

## Những Điểm Chính

- Cơ chế fallback là thiết yếu cho việc triển khai circuit breaker sẵn sàng cho production
- Spring Cloud Gateway sử dụng lập trình reactive (Mono/Flux)
- Fallback REST API chỉ thực thi khi có exception xảy ra
- Cấu hình circuit breaker là khai báo và dễ bảo trì