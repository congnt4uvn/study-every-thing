# Triển Khai OpenTelemetry Cho Distributed Tracing Trong Microservices

## Tổng Quan

Hướng dẫn này trình bày cách triển khai OpenTelemetry để theo dõi phân tán (distributed tracing) trong các microservices Spring Boot. OpenTelemetry (OTel) là một framework quan sát mã nguồn mở, độc lập với nhà cung cấp, tự động thêm công cụ đo lường vào ứng dụng của bạn để tạo, thu thập và xuất dữ liệu đo lường từ xa bao gồm traces, metrics và logs.

## Yêu Cầu Trước Khi Bắt Đầu

- Ứng dụng microservices Spring Boot
- Docker và Docker Compose
- Maven để quản lý dependencies
- Hiểu biết cơ bản về distributed tracing

## Các Bước Triển Khai

### 1. Dừng Các Container Đang Chạy

Trước khi thực hiện thay đổi, hãy dừng tất cả các container đang chạy:

```bash
docker compose down
```

### 2. Thêm Dependency OpenTelemetry

Điều hướng đến file `pom.xml` trong microservice accounts và thêm dependency OpenTelemetry.

#### Định Nghĩa Phiên Bản OpenTelemetry

Thêm thuộc tính version trong `pom.xml`:

```xml
<properties>
    <otelVersion>1.27.0</otelVersion>
</properties>
```

**Lưu ý:** Luôn kiểm tra repository GitHub để biết phiên bản mới nhất, vì các phiên bản được cập nhật hàng quý.

#### Thêm Dependency OpenTelemetry Java Agent

Thêm dependency sau dependency actuator:

```xml
<dependency>
    <groupId>io.opentelemetry.javaagent</groupId>
    <artifactId>opentelemetry-javaagent</artifactId>
    <version>${otelVersion}</version>
    <scope>runtime</scope>
</dependency>
```

Scope `runtime` đảm bảo rằng thư viện OpenTelemetry chỉ được sử dụng trong thời gian chạy ứng dụng, không phải trong quá trình biên dịch. Dependency này sẽ được đóng gói và có sẵn trong Docker image.

#### Refresh Maven Dependencies

Sau khi thêm dependency, thực hiện Maven refresh để tải xuống các thư viện cần thiết.

### 3. Cấu Hình Logging Pattern

Mở file `application.yml` trong microservice accounts và thêm custom logging pattern.

Thêm cấu hình sau vào phần logging:

```yaml
logging:
  pattern:
    level: "%5p [${spring.application.name:},%X{trace_id:},%X{span_id:}]"
```

#### Giải Thích Pattern

- `%5p`: Dành 5 ký tự cho mức độ nghiêm trọng của log (DEBUG, INFO, WARNING, ERROR)
- `${spring.application.name:}`: Chèn metadata tên ứng dụng
- `%X{trace_id:}`: Chèn trace ID được tạo bởi OpenTelemetry tại runtime
- `%X{span_id:}`: Chèn span ID được tạo bởi OpenTelemetry tại runtime

Pattern này đảm bảo rằng tất cả các câu lệnh log được tạo bởi microservice của bạn đều bao gồm thông tin distributed tracing.

### 4. Cập Nhật Các Controller Class Với Logging

#### CustomerController

Thay thế logging correlation ID hiện tại bằng logging được tăng cường bởi OpenTelemetry:

```java
logger.info("fetchCustomerDetails() method start");
// ... logic nghiệp vụ ...
logger.info("fetchCustomerDetails() method end");
```

#### LoansController

Thêm các câu lệnh logging tương tự:

```java
logger.info("fetchLoanDetails() method start");
// ... logic nghiệp vụ ...
logger.info("fetchLoanDetails() method end");
```

#### CardsController

Thêm logging vào fetch API:

```java
logger.info("fetchCardDetails() method start");
// ... logic nghiệp vụ ...
logger.info("fetchCardDetails() method end");
```

**Quan trọng:** Xóa các câu lệnh logging dựa trên correlation ID cũ, vì OpenTelemetry sẽ tự động chèn trace và span IDs vào tất cả logs dựa trên pattern đã cấu hình.

### 5. Áp Dụng Thay Đổi Cho Tất Cả Microservices

Lặp lại các bước 2-4 cho tất cả các microservices trong kiến trúc của bạn để đảm bảo distributed tracing nhất quán trên toàn bộ hệ thống.

## Hiểu Về Hệ Sinh Thái OpenTelemetry

### Cách Hoạt Động Của OpenTelemetry

OpenTelemetry hoạt động bằng cách gắn bytecode vào ứng dụng microservice của bạn tại runtime. Bytecode này tự động thêm thông tin tracing, thông tin span và các metadata khác vào logs và dữ liệu đo lường từ xa của bạn.

### Grafana Tempo Để Lưu Trữ Trace

Sau khi OpenTelemetry tạo logs với thông tin tracing, chúng ta sử dụng **Grafana Tempo** để lập chỉ mục và lưu trữ dữ liệu tracing:

- **Mục đích**: Tương tự như Loki cho logs và Prometheus cho metrics, Tempo được thiết kế đặc biệt cho traces
- **Lợi ích**: Giải pháp mã nguồn mở, khả năng mở rộng cao và tiết kiệm chi phí
- **Chức năng**: Lưu trữ và phân tích thông tin trace cho các hệ thống phân tán

### Tích Hợp Grafana UI

Grafana cung cấp một giao diện thống nhất kết nối với các nguồn dữ liệu khác nhau:

- **Loki**: Cho log aggregation
- **Prometheus**: Cho metrics
- **Tempo**: Cho distributed tracing

Hệ sinh thái Grafana cung cấp một giao diện chung nơi bạn có thể tìm kiếm logs, thông tin tracing hoặc metrics dựa trên yêu cầu của bạn. Cách tiếp cận thống nhất này khiến việc hiểu Grafana và các thành phần của nó trở nên thiết yếu đối với các nhà phát triển microservices, kỹ sư nền tảng và các thành viên trong nhóm vận hành.

### Lợi Ích Của Visualization

Grafana hiển thị thông tin distributed tracing ở định dạng trực quan dễ hiểu, giúp đơn giản hóa việc:

- Theo dõi các request qua nhiều microservices
- Xác định các nút thắt về hiệu suất
- Debug các vấn đề trong hệ thống phân tán
- Hiểu các phụ thuộc giữa các services

## Các Bước Tiếp Theo

### Tạo Docker Images

Sau khi triển khai các thay đổi OpenTelemetry:

1. Xóa các Docker images hiện có
2. Tạo Docker images mới với tag name **S11**
3. Đảm bảo tất cả các microservices được build với cấu hình OpenTelemetry mới nhất

### Cập Nhật Docker Compose

File Docker Compose cần được cập nhật để:

- Bao gồm cấu hình container Tempo
- Cấu hình tích hợp giữa Tempo và Grafana
- Thiết lập networking phù hợp cho distributed tracing

### Chuẩn Bị Demo

Sau khi Docker images được tạo và Docker Compose được cấu hình, bạn sẽ có thể thấy distributed tracing hoạt động thông qua giao diện Grafana UI.

## Điểm Chính Cần Nhớ

- OpenTelemetry tự động thêm công cụ đo lường vào ứng dụng của bạn cho distributed tracing
- Custom logging patterns đảm bảo trace và span IDs được bao gồm trong tất cả logs
- Hệ sinh thái Grafana (Loki, Prometheus, Tempo) cung cấp khả năng quan sát toàn diện
- Triển khai đúng cách yêu cầu cập nhật trên tất cả các microservices
- Visualization thông qua Grafana làm cho việc debug các hệ thống phân tán trở nên dễ dàng hơn đáng kể

## Best Practices Về Logging

Bạn có thể thêm các câu lệnh log ở bất kỳ lớp nào của ứng dụng:

- **Controller Layer**: Theo dõi các request đến và response đi
- **Service Layer**: Giám sát việc thực thi logic nghiệp vụ
- **DAO Layer**: Theo dõi các tương tác với database

Tất cả logs sẽ tự động bao gồm thông tin distributed tracing dựa trên pattern đã cấu hình, loại bỏ nhu cầu quản lý correlation ID thủ công.

---

**Phiên bản**: S11  
**Cập nhật lần cuối**: Dựa trên OpenTelemetry 1.27.0  
**Lưu ý**: Kiểm tra repository GitHub hàng quý để biết các cập nhật phiên bản và best practices mới nhất.