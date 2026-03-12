# Tích Hợp Loki với Tempo Sử Dụng Derived Fields trong Grafana

## Tổng Quan

Hướng dẫn này trình bày cách tạo điều hướng liền mạch giữa log Loki và distributed tracing Tempo trong Grafana sử dụng derived fields. Tích hợp này cho phép các nhà phát triển truy cập trực tiếp thông tin trace từ các câu lệnh log mà không cần tra cứu trace ID thủ công.

## Vấn Đề Đặt Ra

Với cấu hình cơ bản, trace ID và span ID hiển thị trong log Loki. Tuy nhiên, để xem thông tin tracing chi tiết trong Tempo, các nhà phát triển phải:
1. Sao chép trace ID từ log
2. Điều hướng đến Tempo
3. Tìm kiếm trace ID theo cách thủ công

Quy trình làm việc này không hiệu quả và làm gián đoạn quá trình gỡ lỗi.

## Giải Pháp: Derived Fields

Derived fields trong Loki cho phép tự động trích xuất dữ liệu từ log message và liên kết với các data source khác của Grafana như Tempo.

## Các Bước Cấu Hình

### Phương Pháp 1: Cấu Hình Qua Giao Diện

1. **Điều Hướng đến Loki Data Source**
   - Vào Connections → Data Sources
   - Chọn Loki data source

2. **Thêm Derived Field**
   - Trong phần "Derived fields", nhấp "Add"
   - Cấu hình các thông tin sau:
     - **Field Name**: `trace_id`
     - **Regex Pattern**: Tạo pattern để khớp với định dạng log của bạn
     - **Internal Link**: Chọn Tempo làm data source đích
     - **Query**: `${__value.raw}` (truyền giá trị đã trích xuất cho Tempo)

3. **Kiểm Tra Pattern**
   - Sử dụng tính năng debug log message
   - Dán một mẫu log entry từ microservice của bạn
   - Xác minh rằng trace ID được trích xuất chính xác

4. **Lưu Cấu Hình**
   - Nhấp "Save and Test"

5. **Xác Minh Tích Hợp**
   - Vào Explore
   - Truy vấn logs: `{container="accounts-microservice"}`
   - Nhấp vào bất kỳ log entry nào có thông tin trace
   - Một link "Tempo" sẽ xuất hiện bên cạnh trường trace ID
   - Nhấp vào link sẽ mở thông tin tracing đầy đủ

### Phương Pháp 2: File Cấu Hình (Được Khuyến Nghị)

Để cấu hình tồn tại qua các lần khởi động lại Grafana, định nghĩa derived fields trong file `datasource.yml`:

```yaml
datasources:
  - name: Loki
    type: loki
    jsonData:
      derivedFields:
        - datasourceUid: tempo
          matcherRegex: "trace_id=(\\w+)"
          name: trace_id
          url: "$${__value.raw}"
```

**Lưu Ý Quan Trọng:**
- Tham chiếu đến Tempo data source UID (thường là `tempo`)
- Sử dụng dấu gạch chéo ngược kép (`\\`) trong regex pattern để escape trong YAML
- Sử dụng ký hiệu đô la kép (`$$`) cho tham chiếu biến trong YAML

## Lợi Ích

1. **Cải Thiện Trải Nghiệm Nhà Phát Triển**: Điều hướng trực tiếp từ logs đến traces
2. **Gỡ Lỗi Nhanh Hơn**: Không cần sao chép trace ID thủ công
3. **Tích Hợp Liền Mạch**: Hoạt động tự động cho tất cả log entries
4. **Cấu Hình Bền Vững**: Cấu hình dựa trên file tồn tại qua các lần khởi động lại Grafana

## Ví Dụ Use Case

Khi điều tra các vấn đề trong accounts microservice:
1. Truy vấn logs trong Grafana Explore
2. Tìm log entry liên quan
3. Nhấp vào link Tempo bên cạnh trace ID
4. Xem distributed trace đầy đủ với tất cả các tương tác service

## Chi Tiết Kỹ Thuật

- **Data Sources**: Loki (logs) và Tempo (traces)
- **Pattern Matching**: Regular expressions trích xuất trace ID từ log messages
- **Phương Thức Tích Hợp**: Liên kết nội bộ giữa các Grafana data sources
- **Query Parameter**: `${__value.raw}` truyền trace ID đã trích xuất

## Kết Luận

Derived fields cung cấp một cách mạnh mẽ để kết nối các data source observability khác nhau trong Grafana. Bằng cách liên kết Loki logs với Tempo traces, các nhà phát triển có thể điều hướng liền mạch giữa log messages và thông tin distributed tracing, cải thiện đáng kể trải nghiệm gỡ lỗi và khắc phục sự cố trong kiến trúc microservices.

## Chủ Đề Liên Quan

- Distributed Tracing với OpenTelemetry
- Cấu Hình Grafana Tempo
- Loki Log Aggregation
- Microservices Observability
- Tích Hợp Spring Boot với Grafana Stack