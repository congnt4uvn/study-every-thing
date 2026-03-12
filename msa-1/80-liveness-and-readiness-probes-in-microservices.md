# Liveness và Readiness Probes trong Microservices

## Giới thiệu

Trong các ứng dụng microservices và cloud-native, các container được triển khai và quản lý bởi các nền tảng điều phối như Kubernetes và Docker. Các nền tảng này cần hiểu được liệu các container đang chạy có khỏe mạnh và hoạt động bình thường hay không. Đây là lúc **liveness** và **readiness probes** phát huy tác dụng.

## Liveness là gì?

**Liveness** là một cơ chế gửi tín hiệu từ container hoặc ứng dụng để chỉ ra liệu container có đang chạy bình thường hay gặp vấn đề về sức khỏe.

### Cách hoạt động của Liveness

- **Nếu container còn sống**: Không cần hành động gì; trạng thái hiện tại là tốt
- **Nếu container chết**: Nền tảng điều phối (Kubernetes, Docker, v.v.) sẽ cố gắng phục hồi ứng dụng bằng cách:
  - Khởi động lại container
  - Tạo container mới nếu khởi động lại thất bại

### Đặc điểm chính

Liveness trả lời một câu hỏi **đúng hoặc sai** đơn giản: **"Container này còn sống không?"**

- **Đúng**: Không cần hành động
- **Sai**: Cần hành động khắc phục (khởi động lại hoặc tạo mới)

### Ví dụ thực tế

Hãy nghĩ về một võ sĩ quyền anh đang ngồi và chờ đợi trận đấu bắt đầu. Điều này xác nhận võ sĩ còn sống và sắp bắt đầu trận đấu, nhưng không nhất thiết có nghĩa là họ đã sẵn sàng để đối mặt với đối thủ - họ có thể vẫn đang khởi động hoặc nhận hướng dẫn từ huấn luyện viên.

## Readiness là gì?

**Readiness** là một probe được sử dụng để xác định liệu container hoặc ứng dụng có sẵn sàng bắt đầu nhận lưu lượng mạng từ client hay không.

### Hiểu về Readiness

Trong quá trình khởi động, một container có thể:
- **Còn sống** (liveness probe trả về kết quả tích cực)
- Nhưng **chưa sẵn sàng** để chấp nhận lưu lượng vì nó đang:
  - Thực hiện công việc nền
  - Khởi động để chấp nhận yêu cầu
  - Thực hiện khởi tạo cơ sở dữ liệu

### Đặc điểm chính

Readiness trả lời câu hỏi: **"Container này có sẵn sàng nhận lưu lượng mạng không?"**

- **Đúng**: Container có thể chấp nhận yêu cầu
- **Sai**: Container cần thêm thời gian để chuẩn bị

### Tại sao Readiness quan trọng

Các nền tảng như Kubernetes đảm bảo cả liveness và readiness đều trả về kết quả tích cực trước khi định tuyến lưu lượng client đến container. Điều này ngăn chặn các tình huống:
- Kiểm tra liveness thành công
- Nhưng ứng dụng chưa hoàn toàn khởi động
- Dẫn đến các yêu cầu thất bại

### Ví dụ thực tế

Khi một võ sĩ quyền anh sẵn sàng chiến đấu, họ đứng dậy từ tư thế ngồi và di chuyển ra giữa võ đài. Điều này cho thấy họ vừa còn sống VÀ sẵn sàng tiếp tục trận đấu.

## Sự khác biệt giữa Liveness và Readiness

| Khía cạnh | Liveness | Readiness |
|-----------|----------|-----------|
| **Mục đích** | Kiểm tra container có sống không | Kiểm tra container có thể chấp nhận lưu lượng không |
| **Hành động khi thất bại** | Khởi động lại/tạo lại container | Không định tuyến lưu lượng đến container |
| **Kịch bản khởi động** | Có thể tích cực ngay lập tức | Thường mất nhiều thời gian hơn khi khởi động |
| **Trường hợp sử dụng** | Phát hiện ứng dụng bị crash | Phát hiện ứng dụng vẫn đang khởi tạo |

## Triển khai trong Spring Boot

Spring Boot cung cấp các actuator endpoints để hiển thị thông tin liveness và readiness.

### Các Endpoint có sẵn

- **Sức khỏe tổng thể**: `/actuator/health`
- **Chỉ liveness**: `/actuator/health/liveness`
- **Chỉ readiness**: `/actuator/health/readiness`

### Các bước cấu hình

#### 1. Thêm Actuator Dependency

Đảm bảo Spring Boot Actuator dependency có trong `pom.xml`:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

#### 2. Cấu hình application.yml

Thêm cấu hình sau để kích hoạt và hiển thị các health endpoints:

```yaml
management:
  health:
    readiness-state:
      enabled: true
    liveness-state:
      enabled: true
  endpoint:
    health:
      probes:
        enabled: true
```

### Cách hoạt động đằng sau

Spring Boot sử dụng các health indicators để cung cấp thông tin liveness và readiness:

- **LivenessStateHealthIndicator**: Cung cấp trạng thái liveness
- **ReadinessStateHealthIndicator**: Cung cấp trạng thái readiness

Các indicator này hiển thị thông tin sức khỏe thông qua các actuator endpoint URLs.

## Trường hợp thực tế: Ví dụ Config Server

Khi khởi động các microservices có phụ thuộc, bạn cần đảm bảo config server đã hoàn toàn khởi động và chấp nhận lưu lượng trước khi khởi động các dịch vụ phụ thuộc (accounts, loans, cards microservices).

### Kiểm tra triển khai

1. **Khởi động config server** (đảm bảo RabbitMQ đang chạy nếu cần)

2. **Kiểm tra sức khỏe tổng thể**:
   ```
   http://localhost:8071/actuator/health
   ```
   Kết quả: `{"status": "UP"}`

3. **Kiểm tra liveness**:
   ```
   http://localhost:8071/actuator/health/liveness
   ```
   Kết quả: `{"status": "UP"}`

4. **Kiểm tra readiness**:
   ```
   http://localhost:8071/actuator/health/readiness
   ```
   Kết quả: `{"status": "UP"}`

### Ý nghĩa của Status

- **UP**: Container/ứng dụng khỏe mạnh và sẵn sàng
- **DOWN**: Container/ứng dụng có vấn đề hoặc chưa sẵn sàng

## Thực hành tốt nhất

1. **Luôn triển khai cả hai probes** khi dịch vụ của bạn có các thành phần phụ thuộc
2. **Cấu hình timeout phù hợp** cho readiness trong quá trình khởi động
3. **Sử dụng liveness probes cẩn thận** - kiểm tra quá tích cực có thể gây ra vòng lặp khởi động lại
4. **Kiểm tra probes ở local** trước khi triển khai lên Kubernetes/môi trường cloud
5. **Giám sát các lỗi probe** để phát hiện sớm các vấn đề ứng dụng

## Tích hợp với Docker Compose

Trong các cấu hình tương lai, bạn có thể sử dụng các health endpoints này trong Docker Compose để xác định phụ thuộc dịch vụ và thứ tự khởi động, đảm bảo các dịch vụ phụ thuộc chỉ khởi động khi các dịch vụ bắt buộc đã sẵn sàng.

## Kết luận

Liveness và readiness probes là các khái niệm thiết yếu trong kiến trúc microservices, cho phép các nền tảng điều phối:
- Phát hiện và phục hồi từ các lỗi
- Quản lý vòng đời container hiệu quả
- Đảm bảo lưu lượng chỉ được định tuyến đến các container khỏe mạnh, sẵn sàng
- Hỗ trợ các hoạt động mở rộng với sự tự tin

Bằng cách triển khai các probes này trong các microservices Spring Boot của bạn, bạn tạo ra các ứng dụng có khả năng phục hồi tốt hơn và sẵn sàng cho production.