# Phương Pháp Luận 15-Factor: Các Nguyên Tắc 11-15 Cho Ứng Dụng Cloud-Native

## Tổng Quan
Bài giảng này thảo luận về năm nguyên tắc cuối cùng của phương pháp luận 15-factor để xây dựng ứng dụng cloud-native và microservices với Spring Boot.

---

## Nguyên Tắc 11: Port Binding (Ràng Buộc Cổng)

### Định Nghĩa
Tất cả các ứng dụng cloud-native phải **độc lập** và expose các dịch vụ của chúng thông qua port binding.

### Các Khái Niệm Chính

#### Ứng Dụng Độc Lập (Self-Contained)
- Ứng dụng **không nên phụ thuộc vào server bên ngoài** trong môi trường thực thi
- Cách tiếp cận truyền thống: Ứng dụng web Java chạy trong các container server bên ngoài (Tomcat, Jetty, Undertow)
- Cách tiếp cận cloud-native: Ứng dụng quản lý server như **embedded dependencies**

#### Triển Khai Với Spring Boot
- Sử dụng **embedded servers** trong ứng dụng
- Mỗi ứng dụng map với server riêng của nó
- Loại bỏ nhu cầu triển khai Tomcat server bên ngoài

#### Thực Hành Tốt Nhất
- ❌ **Không nên**: Triển khai nhiều ứng dụng trong một server
- ✅ **Nên**: Triển khai mỗi ứng dụng trong một server độc lập
- Expose các dịch vụ ra thế giới bên ngoài thông qua **port binding**

#### Tích Hợp Docker
Khi chạy Docker containers:
```bash
docker run -p [host-port]:[container-port]
```
- Sử dụng port forwarding/mapping để expose microservices
- Cho phép microservices hoạt động như backing services cho các ứng dụng khác

### Lợi Ích
- Thực hành phổ biến trong hệ thống cloud-native
- Tạo điều kiện giao tiếp giữa các microservices
- Loại bỏ việc quản lý server thủ công trên các triển khai

---

## Nguyên Tắc 12: Stateless Processes (Quy Trình Không Trạng Thái)

### Định Nghĩa
Thiết kế ứng dụng như **quy trình không trạng thái** với **kiến trúc không chia sẻ** để đạt được khả năng mở rộng cao.

### Tại Sao Stateless?

#### Yêu Cầu Về Khả Năng Mở Rộng
- Ứng dụng cloud-native cần scale động
- Nhiều instances của cùng một microservice chạy đồng thời
- Ví dụ: Accounts microservice scale bằng cách tạo nhiều instances trong thời gian traffic cao

#### Nguyên Tắc Chính
**Tất cả các instances phải stateless và không chia sẻ gì với nhau**

### Vấn Đề Với Ứng Dụng Có Trạng Thái
- Khi instances giữ dữ liệu, việc tắt chúng gây ra **mất dữ liệu**
- Logic nghiệp vụ bị ảnh hưởng
- Không thể scale đáng tin cậy

### Giải Pháp: Data Stores Bên Ngoài

#### Backing Services Để Quản Lý Trạng Thái
Khi cần lưu trữ dữ liệu, sử dụng:
- **Databases** cho dữ liệu persistent
- **Redis cache** cho thông tin caching
- Các data stores khác cho nhu cầu cụ thể

#### Lợi Ích
- Không mất dữ liệu khi instances tắt
- Instances mới có thể đọc từ data store
- Duy trì kiến trúc stateless thực sự

### Không Nên Lưu Gì Trong Instances
- ❌ Thông tin session người dùng
- ❌ Dữ liệu caching
- ❌ Bất kỳ trạng thái tạm thời nào

### Thực Hành Tốt Nhất
> Luôn lưu trữ thông tin trong các hệ thống lưu trữ bên ngoài, làm cho instances của bạn trở thành ứng dụng stateless thực sự.

---

## Nguyên Tắc 13: Concurrency (Xử Lý Đồng Thời)

### Định Nghĩa
Ứng dụng nên hỗ trợ **xử lý đồng thời** để xử lý nhiều người dùng cùng lúc và đạt được khả năng mở rộng thực sự.

### Khả Năng Mở Rộng Vượt Ra Ngoài Stateless
Mặc dù stateless quan trọng, khả năng mở rộng cũng yêu cầu:
- Khả năng phục vụ **số lượng lớn người dùng**
- Khả năng **xử lý đồng thời**
- Xử lý request song song

### Quản Lý Processes

#### Horizontal Scaling (Mở Rộng Ngang)
- Nhiều instances microservice nên xử lý requests **song song**
- Không tuần tự, từng cái một
- Nhiều traffic hơn = cần nhiều processes hơn

#### Vertical vs Horizontal Scalability

**Vertical Scalability (Mở Rộng Dọc)** (❌ Không Khuyến Nghị)
- Tăng RAM và CPU cho một máy duy nhất
- Giới hạn bởi khả năng phần cứng tối đa
- Không thể scale vô hạn

**Horizontal Scalability (Mở Rộng Ngang)** (✅ Khuyến Nghị)
- Tạo nhiều virtual machines với cùng cấu hình
- Triển khai containers/processes trên các máy
- **Không có giới hạn thực tế** cho việc scaling
- Ví dụ: Nhiều VMs với 2GB RAM, 2 CPU mỗi cái

### Java/JVM Concurrency
- Quản lý concurrency được tích hợp sẵn
- Sử dụng **thread pools** với nhiều threads
- Xử lý concurrent requests tự động

### Các Loại Process

#### Web Processes
- Xử lý HTTP requests
- Phục vụ traffic người dùng

#### Worker Processes
- Thực thi scheduled background jobs
- Xử lý các tác vụ bất đồng bộ

### Điểm Chính
> Không có khả năng concurrency trong ngôn ngữ lập trình và kiến trúc của bạn, ứng dụng cloud-native không thể scale hiệu quả.

---

## Nguyên Tắc 14: Telemetry (Đo Xa)

### Định Nghĩa
Ứng dụng cloud-native phải cung cấp **khả năng quan sát toàn diện** thông qua dữ liệu telemetry để giám sát và quản lý từ xa.

### Thách Thức

#### Monolithic vs Cloud-Native
- **Monolithic**: Giám sát 1-2 ứng dụng/servers (dễ dàng)
- **Cloud-Native**: Giám sát hàng trăm containers, services và servers (phức tạp)

### Observability Như Một Đặc Tính Cơ Bản
Truy cập dữ liệu chính xác và toàn diện từ mỗi component hệ thống tại **một vị trí tập trung duy nhất**.

### Các Loại Dữ Liệu Telemetry

1. **Logs** - Thông tin chi tiết để troubleshooting
2. **Metrics** - Đo lường hiệu suất
3. **Traces** - Theo dõi luồng request
4. **Health Status** - Đánh giá sức khỏe hệ thống
5. **Events** - Ghi lại các sự kiện quan trọng

### So Sánh Với Space Probe
Kevin Hoffman so sánh ứng dụng cloud-native với **tàu thăm dò vũ trụ**:
- NASA/ISRO giám sát tàu thăm dò từ xa bằng telemetry
- Nguyên tắc tương tự áp dụng cho ứng dụng cloud-native
- Giám sát và kiểm soát từ xa yêu cầu dữ liệu telemetry

### Chiến Lược Triển Khai
- Ứng dụng phải **cung cấp thông tin telemetry** cho một component tập trung
- Giám sát và kiểm soát hành vi từ vị trí trung tâm này
- Cho phép ra quyết định dựa trên thông tin

### Nội Dung Khóa Học
> Triển khai telemetry chi tiết sẽ được đề cập trong các phần sắp tới của khóa học này.

---

## Nguyên Tắc 15: Authentication & Authorization (Xác Thực & Phân Quyền)

### Định Nghĩa
Triển khai **bảo mật zero-trust** với authentication và authorization phù hợp cho tất cả các giao tiếp trong hệ thống.

### Bảo Mật Như Một Khía Cạnh Quan Trọng
Bảo mật thường không nhận được sự nhấn mạnh xứng đáng trong các hệ thống phần mềm.

### Cách Tiếp Cận Zero-Trust
Mọi giao tiếp và tương tác phải tuân theo các tiêu chuẩn bảo mật:
- Trong hệ thống
- Trong mạng lưới microservices
- Trong các hệ thống cloud-native

### Các Lớp Bảo Mật

#### Trách Nhiệm Của Operations Team
- Giao thức HTTPS
- Chứng chỉ SSL
- Bảo vệ Firewall
- Bảo mật hạ tầng

#### Trách Nhiệm Của Development Team
- **Authentication**
- **Authorization**

### Authentication vs Authorization

#### Authentication (Xác Thực)
- **Theo dõi và xác định** ai đang truy cập ứng dụng
- Thường sử dụng username và password
- Xác minh danh tính người dùng

#### Authorization (Phân Quyền)
- Xảy ra **sau authentication**
- Đánh giá quyền của người dùng
- Xác định người dùng có đủ đặc quyền cho các hành động cụ thể không
- Kiểm soát truy cập tài nguyên

### Triển Khai Trong Khóa Học Này
Một phần riêng sẽ tập trung vào:
- Triển khai bảo mật trong microservices
- Tiêu chuẩn **OAuth 2.1**
- Giao thức **OpenID Connect**
- Thực thi bảo mật thực tế

---

## Tổng Kết

### Tất Cả 15 Nguyên Tắc Của Phương Pháp Luận Factor Đã Được Đề Cập
Các nguyên tắc và hướng dẫn này là thiết yếu để xây dựng ứng dụng cloud-native và microservices thực sự.

### Lưu Ý Quan Trọng

#### Cho Phát Triển
- ✅ Tuân theo tất cả 15 nguyên tắc khi xây dựng microservices
- ✅ Ứng dụng không thể được gọi là "microservices" hoặc "cloud-native" nếu không tuân theo các nguyên tắc này

#### Cho Phỏng Vấn
- Chủ đề phỏng vấn phổ biến
- Tham khảo các nguyên tắc và slides này
- Ôn tập phương pháp luận 15-factor trước khi phỏng vấn

### Các Phần Sắp Tới
Khóa học này sẽ triển khai tất cả các nguyên tắc này một cách thực tế trong khi xây dựng microservices với Spring Boot.

---

## Tài Nguyên
- Slides khóa học được cung cấp để tham khảo
- Các phần sắp tới: triển khai chi tiết
- Phần bảo mật: OAuth 2.1 và OpenID Connect
- Phần telemetry: giám sát và quan sát

---

**Cảm ơn bạn và hẹn gặp lại trong phần tiếp theo!**