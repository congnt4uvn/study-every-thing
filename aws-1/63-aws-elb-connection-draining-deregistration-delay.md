# AWS ELB Connection Draining / Deregistration Delay

## Tổng quan

Connection Draining là một tính năng quan trọng của AWS Elastic Load Balancers mà bạn cần hiểu cho kỳ thi và ứng dụng thực tế. Tính năng này có tên gọi khác nhau tùy theo loại load balancer:

- **Classic Load Balancer (CLB)**: Được gọi là **Connection Draining**
- **Application Load Balancer (ALB) / Network Load Balancer (NLB)**: Được gọi là **Deregistration Delay**

## Connection Draining là gì?

Connection Draining cho phép các EC2 instance có thời gian để hoàn thành các request đang xử lý hoặc các request đang hoạt động trong khi instance đang được hủy đăng ký hoặc được đánh dấu là không khỏe mạnh. Điều này đảm bảo việc tắt máy một cách êm ái mà không đột ngột ngắt kết nối người dùng đang hoạt động.

### Hành vi chính

- Khi một instance vào chế độ draining, ELB **ngừng gửi request mới** đến instance đó
- Các kết nối hiện có được cho thời gian để hoàn thành dựa trên thời gian draining
- Instance vẫn hoạt động chỉ để hoàn thành các request hiện có

## Cách hoạt động

### Luồng kiến trúc

1. **Ba EC2 Instance** được đăng ký với ELB
2. **Một instance** được đặt vào chế độ draining (đang hủy đăng ký hoặc được đánh dấu không khỏe mạnh)
3. **Người dùng hiện có** đang kết nối với instance đang draining được cho thời gian (thời gian draining) để hoàn thành request
4. **Người dùng mới** kết nối đến ELB được tự động chuyển hướng chỉ đến các instance khỏe mạnh
5. Khi tất cả kết nối hoàn thành, instance draining được hủy đăng ký hoàn toàn

### Sơ đồ minh họa

```
┌─────────────────────────────────────────────┐
│         Elastic Load Balancer (ELB)         │
└─────────────────────────────────────────────┘
              │
              ├───────────────┬───────────────┐
              ▼               ▼               ▼
        ┌──────────┐    ┌──────────┐    ┌──────────┐
        │   EC2    │    │   EC2    │    │   EC2    │
        │ Instance │    │ Instance │    │ Instance │
        │    #1    │    │    #2    │    │    #3    │
        │          │    │          │    │          │
        │ DRAINING │    │  ACTIVE  │    │  ACTIVE  │
        └──────────┘    └──────────┘    └──────────┘
             ▲
             │
    Kết nối hiện có
    hoàn thành êm ái
    
    Kết nối mới → Chuyển hướng đến Instance #2 hoặc #3
```

## Tham số cấu hình

### Cài đặt thời gian Draining

- **Phạm vi**: 1 đến 3,600 giây (1 giây đến 1 giờ)
- **Mặc định**: 300 giây (5 phút)
- **Vô hiệu hóa**: Đặt thành 0 để vô hiệu hóa hoàn toàn connection draining

### Chọn giá trị phù hợp

#### Request ngắn hạn
- **Trường hợp sử dụng**: Request hoàn thành trong vòng chưa đến 1 giây
- **Cài đặt khuyến nghị**: 30 giây
- **Lợi ích**: Instance có thể được drain và đưa offline nhanh chóng
- **Ví dụ**: API call đơn giản, health check, nội dung tĩnh

#### Request dài hạn
- **Trường hợp sử dụng**: Upload, xử lý file, các thao tác chạy lâu
- **Cài đặt khuyến nghị**: Giá trị cao (ví dụ: 1,800-3,600 giây)
- **Đánh đổi**: Instance mất nhiều thời gian hơn để hủy đăng ký hoàn toàn
- **Ví dụ**: Upload file, xử lý video, các thao tác batch

## Thực hành tốt nhất

1. **Khớp với thời gian Request**: Đặt thời gian draining dựa trên thời gian hoàn thành request điển hình của bạn
2. **Cân bằng tính khả dụng**: Xem xét sự đánh đổi giữa tắt máy êm ái và tốc độ thay thế instance
3. **Giám sát Metrics**: Theo dõi số lượng kết nối và thời gian hoàn thành request
4. **Kiểm tra kịch bản**: Xác thực hành vi draining trong các sự kiện triển khai và mở rộng

## Những điểm quan trọng cần lưu ý

- Đặt giá trị thành **zero sẽ vô hiệu hóa draining**, gây ra việc ngắt kết nối ngay lập tức
- **Giá trị thấp** cho phép thay thế instance nhanh hơn nhưng có thể ngắt một số request
- **Giá trị cao** đảm bảo tất cả request hoàn thành nhưng trì hoãn việc loại bỏ instance
- Instance đang draining sẽ **không nhận request mới** từ load balancer

## Các trường hợp sử dụng

- **Sự kiện Auto Scaling**: Chấm dứt instance một cách êm ái trong các thao tác scale-in
- **Thay thế Instance**: Thay thế an toàn các instance không khỏe mạnh mà không làm mất kết nối
- **Cập nhật triển khai**: Đảm bảo triển khai không downtime bằng cách drain trước khi cập nhật
- **Cửa sổ bảo trì**: Chuẩn bị instance cho bảo trì mà không ảnh hưởng đến người dùng

## Tóm tắt

Connection Draining (hoặc Deregistration Delay) là một tính năng quan trọng để duy trì tính khả dụng cao và trải nghiệm người dùng trong các sự kiện vòng đời instance. Bằng cách cấu hình đúng thời gian draining dựa trên mẫu request của ứng dụng, bạn có thể đảm bảo việc tắt máy êm ái và giảm thiểu gián đoạn dịch vụ.

---

**Những điểm chính cần nhớ:**
- Tên gọi khác nhau cho CLB so với ALB/NLB
- Cho phép các request đang xử lý hoàn thành
- Có thể cấu hình từ 1-3,600 giây (mặc định: 300 giây)
- Chọn giá trị dựa trên thời lượng request
- Cần thiết cho triển khai không downtime