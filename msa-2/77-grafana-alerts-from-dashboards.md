# Tạo Cảnh Báo từ Dashboard Grafana

## Tổng Quan

Hướng dẫn này trình bày một phương pháp thay thế để tạo cảnh báo trong Grafana bằng cách kích hoạt chúng trực tiếp từ dashboard, thay vì định nghĩa chúng riêng lẻ trong các quy tắc cảnh báo. Phương pháp này cung cấp quy trình làm việc tích hợp hơn cho việc giám sát microservices.

## Yêu Cầu Tiên Quyết

- Grafana instance với Prometheus làm nguồn dữ liệu
- Các microservices expose metrics thông qua Micrometer và Actuator
- Prometheus được cấu hình để scrape metrics từ microservices
- Môi trường Docker để triển khai microservices

## Tạo Cảnh Báo Dựa Trên Dashboard

### Bước 1: Tạo Dashboard Mới

1. Điều hướng đến phần dashboards của Grafana
2. Nhấp vào **New Dashboard**
3. Đặt tên cho dashboard (ví dụ: "AlertsDemo")
4. Lưu dashboard

### Bước 2: Thêm Panel Visualization

1. Nhấp vào **Add Visualization**
2. Chọn **Time Series** làm loại visualization
3. Chọn **Prometheus** làm nguồn dữ liệu

### Bước 3: Cấu Hình Query Metric

Để giám sát microservice Cards:

```
Metric: up
Label: job
Value: cards
```

Query này kiểm tra xem microservice Cards có đang chạy (giá trị 1) hay đã dừng (giá trị 0).

### Bước 4: Cấu Hình Cảnh Báo

1. Nhấp vào tab **Alert** trong panel editor
2. Cung cấp tiêu đề mô tả cho panel (ví dụ: "cards up")
3. Nhấp **Apply** để lưu panel
4. Nhấp **Edit** và điều hướng đến phần **Alert**
5. Nhấp **Create Alert Rule**
6. Lưu dashboard khi được yêu cầu

### Bước 5: Định Nghĩa Điều Kiện Cảnh Báo

Cấu hình các tham số cảnh báo sau:

**Hàm Reduce:**
- Function: `Last`

**Ngưỡng (Threshold):**
- Điều kiện: `Is below`
- Giá trị: `1`

**Tổ Chức:**
- Folder: Tạo folder mới "cards"
- Group: Tạo group mới "cards"

**Chu Kỳ Đánh Giá:**
- Khoảng đánh giá: `10s`
- Thời gian chờ: `30s`

### Bước 6: Thêm Chú Thích Cảnh Báo

Thêm các chú thích mô tả để tài liệu hóa cảnh báo tốt hơn:

1. **Summary**: "Cards microservice is down"
2. **Description**: "Please do something"

Dashboard UID và Panel ID được tự động điền.

### Bước 7: Lưu Quy Tắc Cảnh Báo

Nhấp **Save rule and exit** để hoàn tất cấu hình cảnh báo.

## Kiểm Tra Cảnh Báo

### Xem Trạng Thái Bình Thường

1. Điều hướng đến dashboard
2. Đặt khoảng thời gian thành 5 phút gần nhất
3. Quan sát biểu tượng trái tim màu xanh lá cho biết trạng thái healthy
4. Giá trị metric nên là `1` (service đang chạy)

### Kích Hoạt Cảnh Báo

1. Dừng microservice Cards trong Docker Desktop:
   - Chọn cards microservice
   - Nhấp Stop

2. Quan sát các thay đổi trạng thái cảnh báo:
   - **Pending**: Biểu tượng trái tim chuyển sang màu vàng/cam
   - **Firing**: Biểu tượng trái tim chuyển sang màu đỏ (sau ~30s)
   - Đường màu vàng xuất hiện trên panel tại điểm kích hoạt cảnh báo

3. Kiểm tra thông báo webhook cho các tin nhắn cảnh báo

### Giải Quyết Cảnh Báo

1. Khởi động microservice Cards trong Docker Desktop
2. Đợi khoảng 20 giây để service khởi động
3. Quan sát trạng thái cảnh báo trở về OK (biểu tượng trái tim màu xanh lá)
4. Giá trị metric trở về `1`

## Kiến Trúc Giám Sát Microservices

### Tổng Quan Các Thành Phần

```
Microservices (với Micrometer & Actuator)
    ↓ (expose metrics)
Prometheus
    ↓ (scrape metrics)
Prometheus UI (visualization cơ bản)
    ↓ (nguồn dữ liệu)
Grafana (dashboards & alerts nâng cao)
    ↓ (thông báo)
Webhook/Kênh Thông Báo
```

### Các Thành Phần Chính

1. **Microservices**: Expose metrics thông qua Micrometer và Spring Boot Actuator
2. **Prometheus**: Scrape và lưu trữ dữ liệu metrics từ microservices
3. **Grafana**: Cung cấp khả năng visualization nâng cao, dashboards và alerting
4. **Kênh Thông Báo**: Webhook hoặc các kênh khác để gửi cảnh báo

## Best Practices (Thực Hành Tốt Nhất)

### Cho Developers

- Hiểu kiến trúc microservices từ đầu đến cuối
- Biết kiến thức cơ bản về Grafana để giám sát và khắc phục sự cố
- Có khả năng cấu hình các cảnh báo và dashboards cơ bản
- Cung cấp hướng dẫn cho các team platform và operations

### Cho Platform Teams

- Tuân theo các cấu hình được khuyến nghị cho môi trường production
- Thiết lập các khoảng đánh giá phù hợp dựa trên mức độ quan trọng của service
- Cấu hình nhiều kênh thông báo để đảm bảo dự phòng
- Tài liệu hóa các quy trình phản hồi cảnh báo

## Những Điểm Chính

1. **Cảnh báo dựa trên dashboard** cung cấp phương pháp giám sát tích hợp
2. **Trạng thái cảnh báo** chuyển qua: OK → Pending → Firing → OK
3. **Chỉ báo trực quan** (biểu tượng trái tim và đường có màu) cung cấp cái nhìn tổng quan nhanh về trạng thái
4. **Chú thích** giúp tài liệu hóa cảnh báo cho sự cộng tác của team
5. **Stack giám sát hoàn chỉnh** (Micrometer + Prometheus + Grafana) cho phép khả năng quan sát toàn diện

## Kết Luận

Hiểu được pipeline giám sát metrics hoàn chỉnh từ microservices đến Grafana là điều cần thiết cho việc phát triển microservice hiện đại. Kiến thức này giúp developers:

- Vượt qua các cuộc phỏng vấn liên quan đến microservices
- Trở thành thành viên có giá trị trong team với kiến thức từ đầu đến cuối
- Cung cấp hướng dẫn kỹ thuật cho các team operations
- Demo các khả năng giám sát một cách hiệu quả

Khả năng tạo, cấu hình và quản lý cảnh báo từ dashboards Grafana là một kỹ năng quan trọng để duy trì các kiến trúc microservice đáng tin cậy.