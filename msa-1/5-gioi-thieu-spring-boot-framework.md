# Giới Thiệu Spring Boot Framework

## Tổng Quan

Trong bài học này, chúng ta sẽ khám phá Spring Boot framework và hiểu tại sao đây là framework tốt nhất để xây dựng microservices dựa trên Java.

## Spring Boot là gì?

Spring Boot là một framework được xây dựng dựa trên Spring framework, cho phép các lập trình viên phát triển và triển khai các ứng dụng web Java, bao gồm cả microservices, một cách rất dễ dàng. Nó cải thiện đáng kể năng suất của lập trình viên và đơn giản hóa công việc của các nhóm phát triển, nền tảng và vận hành.

### Tính Năng Chính

- **JAR Tự Chứa và Có Thể Thực Thi**: Spring Boot cho phép bạn xây dựng các file JAR tự chứa và có thể thực thi thay vì các file WAR hoặc EAR truyền thống
- **Tập Trung Vào Lập Trình Viên**: Là lập trình viên, bạn chỉ cần tập trung vào logic nghiệp vụ trong khi framework xử lý:
  - Khởi động ứng dụng của bạn
  - Đóng gói ứng dụng của bạn
  - Triển khai ứng dụng vào Tomcat server nhúng hoặc web server

## Ưu Điểm Của Spring Boot Framework

### 1. Tính Năng Tích Hợp Sẵn và Tự Động Cấu Hình

Spring Boot cung cấp nhiều tính năng tích hợp sẵn thông qua:
- **Auto Configuration (Tự động cấu hình)**: Tự động cấu hình ứng dụng dựa trên các dependencies
- **Dependency Injection (Tiêm phụ thuộc)**: Quản lý các phụ thuộc component một cách hiệu quả
- **Hỗ Trợ Cloud Platform**: Hỗ trợ native cho nhiều nền tảng đám mây

#### Ví Dụ Về Tự Động Cấu Hình
Khi tạo ứng dụng web với Spring Boot:
- Tự động triển khai lên web server như Tomcat
- Sử dụng cổng mặc định 8080
- Giả định các giá trị mặc định hợp lý
- Cho phép ghi đè các cấu hình mặc định thông qua properties

### 2. Hỗ Trợ Embedded Server

Spring Boot cung cấp các embedded server như:
- Tomcat
- Jetty
- Undertow

**Lợi Ích:**
- Chạy microservices trực tiếp mà không cần cài đặt server riêng
- Không cần bảo trì server thủ công
- Loại bỏ yêu cầu về web server bên ngoài (Tomcat, JBoss, v.v.)

### 3. Tính Năng Production-Ready

Spring Boot hỗ trợ các tính năng production thiết yếu:
- **Metrics (Số liệu)**: Số liệu hiệu suất ứng dụng
- **Health Monitoring (Giám sát sức khỏe)**: Kiểm tra tình trạng ứng dụng
- **External Configurations (Cấu hình bên ngoài)**: Quản lý cấu hình được externalize

#### Spring Boot Actuator
Với dependency Spring Boot Actuator, bạn có thể dễ dàng:
- Expose các metrics của ứng dụng
- Giám sát thông tin health
- Truy cập chi tiết cấu hình

### 4. Phát Triển Nhanh Với Starter Dependencies

**Bootstrap Nhanh**: Nhanh chóng tạo và bắt đầu code các dự án microservice với starter dependencies

**Trước Spring Boot:**
- Cần cấu hình dependency thủ công
- Thiết lập phức tạp cho database, message queues và frameworks
- Quản lý dependency tốn thời gian

**Với Spring Boot Starter Projects:**
- Chỉ cần khai báo các dependencies cần thiết
- Các dependencies được bundle tự động cung cấp
- Ví dụ: MySQL starter bao gồm tất cả dependencies cần thiết để kết nối database

### 5. Ứng Dụng Sẵn Sàng Cho Cloud

Các microservices được xây dựng với Spring Boot sẵn sàng cho cloud và có thể dễ dàng:
- **Containerized (Đóng gói container)**: Đóng gói ứng dụng với Docker
- **Orchestrated (Điều phối)**: Triển khai lên Kubernetes clusters
- **Cloud Deployed (Triển khai cloud)**: Triển khai lên các cloud providers như AWS, GCP, Azure

## So Sánh Cách Tiếp Cận Truyền Thống vs Spring Boot

### Cách Tiếp Cận Truyền Thống (Trước Spring Boot)
```
┌─────────────────────┐
│  Java Runtime (JVM) │
├─────────────────────┤
│  Web Server         │
│  (Tomcat/Jetty)     │
├─────────────────────┤
│  Application        │
│  (định dạng WAR/EAR)│
└─────────────────────┘
```

**Yêu Cầu:**
- Cài đặt Java Runtime Environment (JVM)
- Cài đặt web servers (Tomcat, Jetty, Netty)
- Đóng gói ứng dụng dưới dạng file WAR hoặc EAR
- Triển khai thủ công lên servers

### Cách Tiếp Cận Spring Boot
```
┌─────────────────────┐
│  Java Runtime (JVM) │
├─────────────────────┤
│  Application JAR    │
│  (với embedded      │
│   server)           │
└─────────────────────┘
```

**Lợi Ích:**
- Embedded server được bao gồm trong application JAR
- Không cần cài đặt server riêng
- Không cần bảo trì cấu hình server
- Dễ dàng hơn cho các nhóm platform và operations

## Self-Contained JARs (Fat JARs / Uber JARs)

Các ứng dụng Spring Boot được đóng gói dưới dạng self-contained JARs, còn được gọi là:
- **Fat JARs**
- **Uber JARs**

**Nội Dung:**
- Tất cả dependencies
- Tất cả business logic
- Embedded server

**Ưu Điểm:**
- Mọi thứ được đóng gói cùng nhau
- Triển khai đơn giản
- Giảm độ phức tạp vận hành

## Tóm Tắt

Spring Boot framework cung cấp:
1. Auto-configuration và các tính năng tích hợp sẵn
2. Hỗ trợ embedded server
3. Các tính năng production-ready (metrics, health monitoring)
4. Phát triển nhanh với starter dependencies
5. Ứng dụng sẵn sàng cho cloud

Những ưu điểm này làm cho Spring Boot trở thành lựa chọn tốt nhất để xây dựng microservices dựa trên Java, cải thiện năng suất lập trình viên và đơn giản hóa vận hành.

## Các Bước Tiếp Theo

Trong các bài học tiếp theo, chúng ta sẽ:
- Xây dựng microservices với Spring Boot (demo thực hành)
- Khám phá Spring Boot Actuator
- Đóng gói ứng dụng với Docker
- Triển khai microservices lên Kubernetes clusters

---

*Tài liệu này bao gồm phần giới thiệu về Spring Boot framework cho phát triển microservices.*