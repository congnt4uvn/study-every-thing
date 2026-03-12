# Demo Distributed Tracing với Grafana và Tempo

## Tổng quan

Hướng dẫn này trình bày cách triển khai distributed tracing trong các microservices Spring Boot sử dụng Grafana, Loki, Prometheus và Tempo. Chúng ta sẽ khám phá cách theo dõi các request qua nhiều microservices và phân tích các điểm nghẽn hiệu suất.

## Yêu cầu trước

- Các microservices Spring Boot (accounts, cards, loans, gateway)
- Thiết lập Grafana với các nguồn dữ liệu:
  - Loki (cho logs)
  - Prometheus (cho metrics)
  - Tempo (cho distributed tracing)

## Xem Logs với Loki

### Truy cập Logs

1. Điều hướng đến Grafana và chọn **Loki** làm nguồn dữ liệu
2. Truy vấn logs cho microservice accounts
3. Kiểm tra các mục log với thông tin tracing

### Cấu trúc mẫu Log

Mẫu logging tuân theo cấu trúc sau:

```
[MỨC ĐỘ] [TÊN_ỨNG_DỤNG, TRACE_ID, SPAN_ID]
```

**Các thành phần:**
- **Mức độ (Severity)**: 5 ký tự đầu tiên chỉ mức độ log (DEBUG, INFO, WARN)
- **Tên ứng dụng**: Tên microservice (ví dụ: accounts)
- **Trace ID**: Định danh chung cho tất cả microservices trong một request
- **Span ID**: Định danh duy nhất cho mỗi lần gọi service/method

### Ví dụ câu lệnh Log

```
INFO [accounts, 1a2b3c4d5e6f7g8h, 9i0j1k2l3m4n] fetchCustomerDetails() method end
```

## Tracing qua các Microservices

### Tìm kiếm Logs liên quan

1. Trích xuất **Trace ID** từ log của bất kỳ microservice nào
2. Tìm kiếm cùng Trace ID trong các microservices khác (cards, loans, gateway)
3. Mỗi microservice sẽ có cùng Trace ID nhưng khác Span ID

**Điểm quan trọng**: Trace ID không đổi trên tất cả microservices, trong khi Span ID thay đổi cho mỗi service hoặc method được gọi.

### Các trường hợp sử dụng

- Theo dõi các method được thực thi qua các services
- Debug các tình huống ngoại lệ với các câu lệnh log có liên quan
- Hiểu luồng request hoàn chỉnh qua các microservices của bạn

## Trực quan hóa Traces với Tempo

### Truy cập Tempo

1. Trong Grafana, chọn **Tempo** làm nguồn dữ liệu
2. Tìm kiếm sử dụng Trace ID từ bất kỳ microservice nào
3. Chạy truy vấn để xem trực quan hóa trace

### Hiểu về Trực quan hóa Trace

Giao diện Tempo cung cấp biểu đồ waterfall đẹp mắt hiển thị:

#### Luồng Request

```
Gateway Server
  └─> API fetchCustomerDetails (Accounts)
      ├─> CustomerController.fetchCustomerDetails
      │   └─> Repository Layer (lấy dữ liệu account)
      ├─> Microservice Loans
      │   └─> Lấy thông tin khoản vay
      └─> Microservice Cards
          └─> Lấy thông tin thẻ
```

### Tính năng chính

1. **Khả năng hiển thị cấp method**: Xem tất cả các method được gọi và thời gian thực thi
2. **Phân tích hiệu suất**: Xác định method hoặc service nào tiêu tốn nhiều thời gian nhất
3. **Thời gian tổng hợp**: Các service cha hiển thị thời gian tích lũy bao gồm cả các lời gọi service con
4. **Thời gian riêng lẻ**: Mỗi service hiển thị thời gian thực thi của chính nó

### Phân tích điểm nghẽn hiệu suất

- **Thời gian cấp cao nhất**: Hiển thị thời gian tổng hợp cho tất cả các lời gọi downstream
- **Thời gian cấp thấp hơn**: Hiển thị thời gian thực thi của từng service/method riêng lẻ
- Dễ dàng xác định các service hoặc method chậm gây ra trзадержки

### Lợi ích khi Debug

- Theo dõi hành trình request qua toàn bộ mạng microservice
- Xác định chính xác nơi request thất bại hoặc bị kẹt
- Hiểu đặc điểm hiệu suất của từng service

## So sánh với các công cụ khác

### Zipkin

**Khả năng:**
- Trực quan hóa distributed tracing
- Tương tự Tempo để xem thông tin trace

**Hạn chế:**
- Chỉ cung cấp thông tin tracing
- Không có chế độ xem logs tích hợp
- Sản phẩm riêng biệt không có dashboard thống nhất

### Jaeger (của Red Hat)

**Khả năng:**
- Xác định distributed tracing
- Tốt cho trực quan hóa trace

**Hạn chế:**
- Không có thông tin logs tích hợp
- Thiếu dashboard observability thống nhất

### Ưu điểm của Tempo

**Tại sao Tempo là lựa chọn tốt nhất:**

1. **Tích hợp Grafana**: Hoạt động liền mạch trong hệ sinh thái Grafana
2. **Dashboard thống nhất**: Truy cập logs, metrics và traces ở một nơi
3. **Observability hoàn chỉnh**: Kết hợp:
   - **Loki** cho logs
   - **Prometheus** cho metrics
   - **Tempo** cho traces
4. **Ba trụ cột của Observability**: Logs, metrics và traces tất cả trong một sản phẩm

## Ba trụ cột của Observability

1. **Logs**: Thông tin chi tiết về sự kiện (Loki)
2. **Metrics**: Đo lường hiệu suất (Prometheus)
3. **Traces**: Theo dõi luồng request (Tempo)

## Các phương pháp hay nhất

1. **Sử dụng Trace IDs nhất quán** trên tất cả microservices
2. **Thêm các câu lệnh log có ý nghĩa** tại các điểm thực thi quan trọng
3. **Giám sát thời gian tổng hợp và riêng lẻ** để xác định điểm nghẽn
4. **Tận dụng giao diện thống nhất của Grafana** cho observability toàn diện
5. **Triển khai các mẫu logging phù hợp** với mức độ nghiêm trọng, tên ứng dụng và thông tin trace

## Tóm tắt

Distributed tracing với Grafana Tempo cung cấp các khả năng mạnh mẽ để:
- Hiểu luồng request qua các microservices
- Xác định điểm nghẽn hiệu suất
- Debug các hệ thống phân tán phức tạp
- Đạt được observability hoàn chỉnh với logs, metrics và traces

Sự tích hợp của Tempo, Loki và Prometheus trong Grafana cung cấp giải pháp toàn diện cho observability và monitoring của microservices.

---

**Các bước tiếp theo**: Khám phá các tính năng nâng cao của Grafana và thiết lập cảnh báo tùy chỉnh dựa trên các metrics từ trace.