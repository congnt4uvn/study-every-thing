# Thách Thức Containerization và Giới Thiệu Docker

## Tổng Quan

Trong kiến trúc microservices, với trách nhiệm lớn đến sức mạnh lớn. Khi bạn đón nhận các thách thức của việc triển khai microservices và xử lý chúng theo các thực tiễn tốt nhất trong ngành, bạn sẽ mở khóa toàn bộ tiềm năng và lợi ích của microservices.

Phần này giới thiệu một thách thức quan trọng: **Làm thế nào để xử lý việc triển khai, tính di động và khả năng mở rộng của microservices**.

## Ba Thách Thức Chính

### 1. Thách Thức Triển Khai

**Câu hỏi:** Làm thế nào để triển khai hàng trăm microservices nhỏ với nỗ lực và chi phí tối thiểu?

- Với ứng dụng nguyên khối (monolithic), bạn chỉ có một file JAR, WAR, hoặc EAR duy nhất để triển khai lên web server hoặc application server
- Với kiến trúc microservices, các tổ chức có thể có hàng trăm microservices
- **Vấn đề:** Chúng ta có cần 100 servers và máy ảo khác nhau để triển khai chúng không? (Tất nhiên là không - đó không phải là giải pháp khả thi)

### 2. Thách Thức Tính Di Động

**Câu hỏi:** Làm thế nào để di chuyển hàng trăm microservices qua các môi trường với nỗ lực, cấu hình và chi phí tối thiểu?

#### Hành Trình Qua Các Môi Trường

Ứng dụng phải di chuyển qua nhiều môi trường:

1. Máy của developer
2. GitHub repository (hoặc hệ thống quản lý phiên bản khác)
3. Môi trường Development
4. Môi trường UAT/SIT/QA (sau khi build ổn định)
5. Môi trường Production replica (sau khi hoàn thành testing)
6. Môi trường Production (sau khi testing pre-production)

#### Các Vấn Đề Về Tính Di Động

- Với ứng dụng monolithic: Một ứng dụng, một server - dễ dàng cấu hình và di chuyển
- Với microservices: Ai quản lý tính di động cho hàng trăm services?
- **Các mối quan tâm:**
  - Yêu cầu phiên bản JDK cụ thể
  - Cấu hình web server cụ thể
  - Cấu trúc thư mục cụ thể
  - Cấu hình database cụ thể
  - Ai thực hiện tất cả công việc thủ công này cho hàng trăm microservices?

### 3. Thách Thức Khả Năng Mở Rộng

**Câu hỏi:** Làm thế nào để mở rộng các microservices cụ thể theo thời gian thực dựa trên nhu cầu traffic?

- Ứng dụng Monolithic: Mở rộng đơn giản - chỉ cần thêm một server replica
- Microservices: Câu chuyện khác
  - Cần mở rộng từng microservices riêng lẻ dựa trên nhu cầu
  - Phải scale up trong lúc traffic cao
  - Phải scale down khi nhu cầu giảm
  - Tất cả phải xảy ra với:
    - Nỗ lực tối thiểu
    - Chi phí tối thiểu
    - Không can thiệp thủ công

## Giải Pháp: Containerization

### Tại Sao Containerization?

Để vượt qua những thách thức này, chúng ta phải **containerize tất cả các microservices**.

### Containerization Là Gì?

Containerization chuyển đổi một dự án Maven thông thường thành một container. Các containers này:

- Có kích thước rất nhỏ
- Cung cấp môi trường tự cô lập cho ứng dụng
- Bao gồm tất cả các dependencies cần thiết

### Lợi Ích

- Đóng gói phiên bản Java, Tomcat, cấu hình database, cấu trúc thư mục - tất cả bên trong một container
- Triển khai cùng một container trên bất kỳ môi trường hoặc cloud nào mà không cần thay đổi
- Tối ưu hóa tài nguyên
- Môi trường cô lập cho mỗi microservice

## Docker: Nền Tảng Containerization

### Docker Là Gì?

Docker là một **nền tảng mã nguồn mở** cung cấp khả năng đóng gói và chạy ứng dụng trong một môi trường cô lập lỏng lẻo gọi là **container**.

### Docker Hoạt Động Như Thế Nào

1. Bắt đầu với một ứng dụng Maven
2. Chuyển đổi nó thành Docker image bằng Docker
3. Chạy image đó như một container bên trong bất kỳ máy ảo hoặc môi trường cloud nào

## Phép So Sánh Container

### Nguồn Cảm Hứng Từ Ngành Vận Tải Biển

Hãy nghĩ về một con tàu chở hàng vận chuyển hàng hóa giữa các quốc gia bằng containers.

**Tại sao sử dụng containers?**
- Tối ưu hóa không gian
- Cung cấp môi trường riêng biệt, cô lập cho từng loại hàng hóa
- Ví dụ: Một container có làm lạnh cho táo, một container khác không cần làm mát cho hàng điện tử

### Áp Dụng Cho Microservices

Giống như tàu biển tối ưu hóa tài nguyên với containers, chúng ta triển khai microservices như containers:

**Các Yêu Cầu Khác Nhau:**
- Một microservice có thể dùng Java 17
- Một microservice khác có thể dùng Java 21
- Databases, frameworks và ngôn ngữ khác nhau

**Vấn Đề Với Cách Tiếp Cận Truyền Thống:**
- Quản lý tất cả microservices trên một VM hoặc jumbo server duy nhất cực kỳ khó khăn
- Tài nguyên không được sử dụng tối ưu

**Giải Pháp Container:**
- Triển khai 10 microservices khác nhau với 10 yêu cầu khác nhau trên một VM duy nhất
- Mỗi container có môi trường cô lập riêng
- Tối ưu hóa việc sử dụng tài nguyên

## Điểm Chính Cần Nhớ

Khi nghĩ về Docker và containers, hãy nhớ đến phép so sánh với ngành vận tải biển. Giống như ngành vận tải biển hưởng lợi từ containers, chúng ta áp dụng cùng khái niệm cho microservices với Docker.

## Các Bước Tiếp Theo

Trong các bài giảng tiếp theo, chúng ta sẽ khám phá:
- Giới thiệu chi tiết về Docker
- Cách containerize ứng dụng
- Các thách thức cụ thể mà Docker giải quyết
- Ví dụ triển khai thực tế

---

**Ghi nhớ:** Đừng nản lòng trước các thách thức. Bằng cách đối mặt với những thách thức này và triển khai các giải pháp phù hợp, bạn sẽ tạo ra một ứng dụng microservices hoàn hảo mà tổ chức của bạn có thể tận dụng đầy đủ các lợi ích.