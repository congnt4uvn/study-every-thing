# Triển khai Micrometer và Prometheus trong Microservices

## Tổng quan

Hướng dẫn này sẽ trình bày cách triển khai Micrometer và Prometheus để giám sát các microservices. Việc tích hợp này cho phép bạn xuất các metrics của actuator ở định dạng mà Prometheus có thể hiểu được, từ đó giúp giám sát hiệu quả kiến trúc microservices của bạn.

## Yêu cầu trước khi bắt đầu

- Các microservices Spring Boot (Accounts, Loans, Cards)
- Config Server
- Eureka Server
- Gateway Server
- Công cụ build Maven

## Các bước triển khai

### Bước 1: Thêm dependency Micrometer

Thêm dependency Micrometer Prometheus registry vào file `pom.xml` của mỗi microservice, ngay sau dependency actuator:

```xml
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-registry-prometheus</artifactId>
</dependency>
```

**Những điểm quan trọng:**
- Dependency này yêu cầu Micrometer xuất các metrics của actuator ở định dạng Prometheus
- Nếu tổ chức của bạn sử dụng hệ thống giám sát khác, chỉ cần thay đổi `artifactId`
- Thêm dependency này vào tất cả các microservices: Accounts, Loans, Cards, Eureka Server, Config Server và Gateway Server

### Bước 2: Cấu hình thuộc tính ứng dụng

Thêm thuộc tính sau vào file `application.yml` của mỗi microservice trong phần `management`:

```yaml
management:
  metrics:
    tags:
      application: ${spring.application.name}
```

**Mục đích:**
- Thuộc tính này nhóm tất cả metrics của mỗi microservice dưới tên ứng dụng của nó
- Giúp xác định metrics nào thuộc về microservice nào
- Giá trị được gán động từ thuộc tính `spring.application.name`

### Bước 3: Build và khởi động các services

1. **Clean Build**: Thực hiện clean Maven build cho tất cả các microservices

2. **Khởi động các services theo thứ tự**:
   - Khởi động **Config Server** đầu tiên
   - Khởi động **Eureka Server** thứ hai
   - Khởi động các microservices **Accounts**, **Loans** và **Cards** (có thể khởi động song song)
   - Khởi động **Gateway Server** cuối cùng

### Bước 4: Kiểm tra các endpoints metrics

#### Endpoint Actuator Metrics

Truy cập endpoint metrics tổng quát của bất kỳ microservice nào:

```
http://localhost:8080/actuator/metrics
```

Endpoint này hiển thị tất cả các metrics có sẵn được xuất bởi actuator.

#### Chi tiết metrics cụ thể

Để xem chi tiết của một metric cụ thể:

```
http://localhost:8080/actuator/metrics/system.cpu.usage
http://localhost:8080/actuator/metrics/process.uptime
```

**Ví dụ Response:**
- CPU usage: Hiển thị mức sử dụng CPU hiện tại (ví dụ: 0.0)
- Process uptime: Hiển thị service đã chạy được bao lâu (ví dụ: 172 giây)

#### Endpoint Prometheus

Endpoint quan trọng cho việc tích hợp Prometheus:

```
http://localhost:8080/actuator/prometheus
```

Endpoint này xuất tất cả metrics ở định dạng Prometheus, mà Prometheus sẽ thu thập (scrape) theo các khoảng thời gian đều đặn (ví dụ: mỗi 5, 10 hoặc 60 giây tùy theo cấu hình).

### Cổng của các Microservices

| Service | Cổng |
|---------|------|
| Accounts | 8080 |
| Loans | 8090 |
| Cards | 9000 |
| Eureka Server | 8070 |
| Config Server | 8071 |
| Gateway Server | 8072 |

### Danh sách kiểm tra

Kiểm tra endpoint Prometheus cho tất cả các services:

- ✓ Accounts: `http://localhost:8080/actuator/prometheus`
- ✓ Loans: `http://localhost:8090/actuator/prometheus`
- ✓ Cards: `http://localhost:9000/actuator/prometheus`
- ✓ Eureka Server: `http://localhost:8070/actuator/prometheus`
- ✓ Config Server: `http://localhost:8071/actuator/prometheus`
- ✓ Gateway Server: `http://localhost:8072/actuator/prometheus`

## Lợi ích chính

1. **Ít thay đổi code**: Chỉ cần thêm dependency và cấu hình
2. **Metrics chuẩn hóa**: Tất cả metrics được xuất ở định dạng tương thích với Prometheus
3. **Giám sát dễ dàng**: Prometheus tự động thu thập metrics từ tất cả các microservices
4. **Linh hoạt**: Có thể chuyển sang các hệ thống giám sát khác bằng cách thay đổi artifact ID
5. **Khả năng quan sát tập trung**: Tất cả metrics của microservices có sẵn trong một hệ thống giám sát

## Cách hoạt động

1. **Micrometer** đóng vai trò như một facade để thu thập metrics
2. **Prometheus registry** định dạng metrics theo chuẩn tương thích với Prometheus
3. **Prometheus server** định kỳ thu thập (scrape) endpoint `/actuator/prometheus`
4. Metrics được gắn thẻ với tên ứng dụng để dễ dàng nhận diện
5. Tất cả metrics có sẵn để truy vấn và trực quan hóa

## Tóm tắt

Bằng cách thêm dependency Micrometer Prometheus và cấu hình các thuộc tính ứng dụng, tất cả các microservices giờ đây đã xuất các metrics của actuator ở định dạng mà Prometheus có thể hiểu được. Điều này cho phép giám sát toàn diện và khả năng quan sát trên toàn bộ kiến trúc microservices của bạn mà không cần thay đổi nhiều logic nghiệp vụ hoặc code Java.