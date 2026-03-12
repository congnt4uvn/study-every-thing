# Metrics và Giám Sát trong Microservices: Giới Thiệu về Prometheus và Grafana

## Tổng Quan

Hướng dẫn này giới thiệu trụ cột thứ hai của khả năng quan sát và giám sát trong kiến trúc microservices: **Metrics (Số liệu)**. Trong khi logging giúp chúng ta hiểu các sự kiện cụ thể, metrics cung cấp thông tin chi tiết toàn diện về tình trạng và hiệu suất của ứng dụng.

## Tại Sao Metrics Quan Trọng

### Hạn Chế Của Việc Chỉ Sử Dụng Logs

Event logs giúp chúng ta hiểu điều gì đã xảy ra trong các tình huống hoặc phương thức cụ thể, nhưng chúng có những hạn chế:
- Không thể cung cấp trạng thái sức khỏe tổng thể của microservices
- Không đưa ra thông tin chi tiết về hiệu suất theo thời gian thực
- Thiếu các chế độ xem tổng hợp trên nhiều instances

### Metrics Cung Cấp Gì

Metrics cung cấp các phép đo số về hiệu suất ứng dụng, bao gồm:
- Mức sử dụng CPU
- Mức sử dụng bộ nhớ
- Mức sử dụng heap dump
- Số lượng threads
- Connection pools
- Tỷ lệ lỗi
- Và nhiều chỉ số hiệu suất khác

## Các Thành Phần Của Kiến Trúc Giám Sát

### 1. Spring Boot Actuator

**Vai trò**: Tạo metrics ở mức microservice

- Expose (công khai) metrics cho mỗi microservice instance
- Truy cập qua endpoint `/actuator/metrics`
- Cung cấp các metrics ứng dụng toàn diện ngay từ đầu
- Phải được thêm vào dưới dạng dependency cho tất cả microservices

**Thách thức**: Kiểm tra thủ công các actuator endpoints cho nhiều instances rất tốn thời gian và không thực tế ở quy mô lớn (hãy tưởng tượng 100 microservices với nhiều instances mỗi cái).

### 2. Micrometer

**Vai trò**: Chuyển đổi định dạng metrics và trừu tượng hóa vendor

Micrometer đóng vai trò như một facade quan sát ứng dụng trung lập với vendor, tương tự như SLF4J đối với logging.

#### Tính Năng Chính:
- Chuyển đổi metrics từ Spring Boot Actuator từ định dạng JSON sang các định dạng cụ thể cho từng hệ thống giám sát
- Cung cấp giao diện trung lập với vendor để thu thập metrics
- Hỗ trợ nhiều hệ thống giám sát thông qua các dependencies khác nhau

#### Các Vendor Được Hỗ Trợ:
- Prometheus
- App Optics
- Azure Monitor
- CloudWatch
- Datadog
- Dynatrace
- Elastic
- Graphite
- OpenTelemetry
- Và nhiều hơn nữa

#### Tương Tự Với SLF4J:
Giống như SLF4J (Simple Logging Framework for Java) trừu tượng hóa các logging frameworks (Java Util Logging, Log4j, Logback), Micrometer trừu tượng hóa việc thu thập metrics cho các hệ thống giám sát khác nhau.

**Triển Khai**: Chỉ cần thêm dependency Micrometer dành riêng cho vendor (ví dụ: micrometer-prometheus), và nó sẽ xử lý mọi độ phức tạp ở phía sau.

### 3. Prometheus

**Vai trò**: Tổng hợp và lưu trữ metrics

- Giải pháp giám sát mã nguồn mở
- Định kỳ scrape (thu thập) metrics từ các microservice containers
- Tổng hợp metrics từ tất cả các instances vào một vị trí duy nhất
- Tương tự như Loki (tổng hợp logs), nhưng dành cho metrics
- Cung cấp UI để giám sát và trực quan hóa cơ bản

#### Khả Năng Chính:
- Thu thập metrics từ các microservices riêng lẻ
- Lưu trữ metrics được hợp nhất ở một vị trí
- Xây dựng các dashboards và đồ thị cơ bản
- Cho phép giám sát tập trung

### 4. Grafana

**Vai trò**: Trực quan hóa nâng cao và cảnh báo

#### Tại Sao Cần Grafana Khi Đã Có Prometheus?

Mặc dù Prometheus cung cấp giám sát cơ bản, nhưng nó có những hạn chế:
- Không thể xây dựng các dashboards phức tạp, có thể tùy chỉnh
- Khả năng cảnh báo và thông báo hạn chế

#### Ưu Điểm Của Grafana:
- Tạo các dashboards tinh vi, tương tác
- Cung cấp hệ thống cảnh báo và thông báo nâng cao
- Tích hợp liền mạch với Prometheus (tương tự như tích hợp Loki)
- Cung cấp công cụ trực quan hóa cấp chuyên nghiệp

## Quy Trình Giám Sát

1. **Tạo Metrics**: Spring Boot Actuator expose metrics ở định dạng JSON
2. **Chuyển Đổi Định Dạng**: Micrometer chuyển đổi metrics sang định dạng tương thích với Prometheus
3. **Tổng Hợp**: Prometheus định kỳ scrape và hợp nhất metrics từ tất cả các instances
4. **Trực Quan Hóa**: Grafana truy vấn Prometheus để xây dựng dashboards và thiết lập cảnh báo

## Chiến Lược Triển Khai

Giải pháp giám sát hoàn chỉnh bao gồm:

1. Thêm Spring Boot Actuator dependency vào tất cả microservices
2. Thêm Micrometer Prometheus dependency để chuyển đổi định dạng
3. Cấu hình Prometheus để scrape các metrics endpoints
4. Tích hợp Prometheus với Grafana
5. Xây dựng các custom dashboards trong Grafana
6. Thiết lập cảnh báo và thông báo khi vượt ngưỡng

## Lợi Ích Của Giám Sát Dựa Trên Metrics

- **Giám Sát Sức Khỏe Theo Thời Gian Thực**: Đội ngũ vận hành có thể liên tục giám sát tình trạng microservices
- **Theo Dõi Hiệu Suất**: Xác định các điểm nghẽn và suy giảm hiệu suất
- **Cảnh Báo Chủ Động**: Nhận thông báo trước khi các vấn đề trở nên nghiêm trọng
- **Khả Năng Mở Rộng**: Giám sát hàng trăm microservices và instances một cách hiệu quả
- **Phân Tích Lịch Sử**: Theo dõi xu hướng hiệu suất theo thời gian
- **Lập Kế Hoạch Năng Lực**: Đưa ra quyết định sáng suốt về phân bổ tài nguyên

## Các Bước Tiếp Theo

Trong các bài giảng tiếp theo, chúng ta sẽ triển khai từng bước các thành phần này và chứng minh cách chúng hoạt động cùng nhau để cung cấp giám sát toàn diện cho các ứng dụng microservices.

---

**Tóm Tắt**: Metrics là yếu tố thiết yếu để giám sát tình trạng và hiệu suất của microservices. Sự kết hợp của Spring Boot Actuator, Micrometer, Prometheus và Grafana cung cấp một giải pháp giám sát mạnh mẽ, có khả năng mở rộng, cho phép các đội ngũ vận hành duy trì các kiến trúc microservices hoạt động tốt và hiệu suất cao.