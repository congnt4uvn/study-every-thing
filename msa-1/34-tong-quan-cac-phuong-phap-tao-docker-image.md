# Các Phương Pháp Tạo Docker Image cho Microservices

## Tổng Quan

Việc chuyển đổi các microservices thành Docker images giúp chúng trở nên nhẹ hơn và phù hợp để vượt qua các thách thức liên quan đến triển khai, tính di động và khả năng mở rộng. Khi tạo Docker image từ một ứng dụng web hoặc ứng dụng Spring Boot, có ba phương pháp thường được sử dụng trong ngành.

Phần này sẽ khám phá cả ba phương pháp, và đến cuối phần, chúng ta sẽ chọn một phương pháp để tiếp tục sử dụng trong suốt phần còn lại của khóa học.

## Ba Phương Pháp Phổ Biến

### 1. Phương Pháp Dockerfile

**Phương pháp Dockerfile** là phương pháp cơ bản và truyền thống nhất để tạo Docker images.

**Cách hoạt động:**
- Viết một tập hợp các chỉ thị trong Dockerfile
- Docker server tạo Docker image dựa trên các chỉ thị này
- Yêu cầu học cú pháp Docker và các best practices

**Ứng dụng trong khóa học:**
- Chúng ta sẽ sử dụng phương pháp này để tạo Docker image cho **Accounts Microservice**

**Đặc điểm:**
- Phương pháp cơ bản nhất
- Có đường cong học tập đối với cú pháp Docker
- Cung cấp khả năng kiểm soát chi tiết quá trình tạo image

---

### 2. Phương Pháp Buildpacks

**Buildpacks** đơn giản hóa quá trình containerization bằng cách loại bỏ việc phải viết Docker files thủ công.

**Cách hoạt động:**
- Tạo Docker image bằng một lệnh Maven duy nhất
- Maven sử dụng khái niệm Buildpacks ở hậu trường
- Không cần cung cấp chỉ thị thủ công cho Docker server

**Bối cảnh:**
- Dự án được khởi xướng và phát triển bởi Heroku và Pivotal
- Dựa trên các best practices học được qua nhiều năm
- Đơn giản hóa việc containerization ứng dụng web

**Ứng dụng trong khóa học:**
- Chúng ta sẽ sử dụng phương pháp này để tạo Docker image cho **Loans Microservice**

**Ưu điểm:**
- Không cần viết Dockerfiles cấp thấp
- Quá trình tạo image tự động
- Xây dựng dựa trên các best practices của ngành

---

### 3. Phương Pháp Google Jib

**Google Jib** là một công cụ Java được phát triển bởi Google và sau đó được mã nguồn mở.

**Cách hoạt động:**
- Sử dụng lệnh Maven plugin để tạo Docker images
- Hoạt động với bất kỳ ứng dụng Java nào
- Không cần viết Dockerfiles cấp thấp

**Ứng dụng trong khóa học:**
- Chúng ta sẽ sử dụng phương pháp này để tạo Docker image cho **Cards Microservice**

**Ưu điểm:**
- Dễ dàng tạo Docker image cho ứng dụng Java
- Không yêu cầu Dockerfile
- Tích hợp liền mạch với quy trình build Maven

---

## Sơ Đồ Ánh Xạ Microservice-Phương Pháp

| Microservice | Phương Pháp Tạo Docker Image |
|--------------|------------------------------|
| Accounts     | Dockerfile                   |
| Loans        | Buildpacks                   |
| Cards        | Google Jib                   |

**Lưu ý:** Ba microservices (Accounts, Loans và Cards) được phát triển như một phần của ứng dụng ngân hàng (Bank Application). Việc ánh xạ mỗi phương pháp với một microservice hoàn toàn trùng hợp nhưng thuận tiện cho việc trình diễn cả ba phương pháp.

## Tiếp Theo Là Gì

Mỗi phương pháp có những ưu điểm và nhược điểm riêng, sẽ được thảo luận chi tiết khi chúng ta khám phá từng phương pháp. Đến cuối phần này, chúng ta sẽ chọn một phương pháp để tuân theo trong suốt phần còn lại của khóa học.

---

## Tóm Tắt

- **Ba phương pháp chính** tồn tại để tạo Docker images từ ứng dụng Spring Boot
- **Dockerfile**: Phương pháp truyền thống, thủ công với khả năng kiểm soát chi tiết
- **Buildpacks**: Phương pháp tự động sử dụng Maven, không cần Dockerfile
- **Google Jib**: Công cụ tối ưu hóa cho Java với tích hợp Maven plugin
- Chúng ta sẽ khám phá cả ba phương pháp trước khi chọn một cho phần còn lại của khóa học