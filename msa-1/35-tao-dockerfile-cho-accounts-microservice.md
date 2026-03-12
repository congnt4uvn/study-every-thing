# Tạo Dockerfile cho Accounts Microservice

## Tổng quan
Trong bài học này, chúng ta sẽ viết Dockerfile cho Accounts Microservice để cho phép đóng gói ứng dụng bằng Docker.

## Điều kiện tiên quyết
Trước khi tạo Dockerfile:
1. Dừng instance đang chạy của Accounts Microservice bằng cách nhấn `Ctrl + C`
2. Đảm bảo Docker đang chạy trên hệ thống của bạn
   - **Mac**: Biểu tượng Docker xuất hiện ở thanh menu trên cùng
   - **Windows**: Biểu tượng Docker xuất hiện ở góc dưới bên phải
3. Xác minh Docker đang chạy bằng cách mở Docker Dashboard
   - Click vào biểu tượng Docker và chọn "Dashboard"
   - Bạn sẽ thấy containers và images (có thể trống nếu đây là lần đầu tiên)

## Tạo Dockerfile

### Bước 1: Tạo file Dockerfile
1. Nhấp chuột phải vào thư mục Accounts Microservice của bạn
2. Chọn "New File"
3. Đặt tên chính xác là `Dockerfile` (không có phần mở rộng như .txt, .xml, hoặc .yml)
4. Docker sẽ tìm kiếm đúng tên file này

### Bước 2: Viết các lệnh trong Dockerfile

#### Base Image (FROM)
```dockerfile
# Bắt đầu với base image chứa Java runtime
FROM openjdk:17-jdk-slim
```

**Giải thích:**
- Lệnh `FROM` cho Docker biết rằng image của chúng ta phụ thuộc vào một base image khác
- Chúng ta sử dụng `openjdk:17-jdk-slim` làm base image
- Định dạng: `tênImage:tênTag`
  - Tên image: `openjdk`
  - Tag: `17-jdk-slim` (tương đương với phiên bản Java)

**Tìm Docker Images:**
- Truy cập [Docker Hub](https://hub.docker.com/)
- Tìm kiếm "openjdk"
- Click vào Docker image chính thức
- Duyệt các tags có sẵn trong phần "Tags"
- Ví dụ:
  - `22-slim-bullseye` cho Java 22
  - `17-jdk-slim` cho Java 17

#### Thông tin Maintainer
```dockerfile
# Thông tin về người duy trì image
MAINTAINER easybytes.com
```

**Giải thích:**
- Từ khóa `MAINTAINER` chỉ định người duy trì Docker image
- Cần có khoảng trắng giữa `MAINTAINER` và thông tin người duy trì

#### Sao chép Application JAR
```dockerfile
# Thêm file jar của ứng dụng vào image
COPY target/accounts-0.0.1-SNAPSHOT.jar accounts-0.0.1-SNAPSHOT.jar
```

**Giải thích:**
- Lệnh `COPY` sao chép files từ máy local của bạn vào Docker image
- Cú pháp: `COPY <nguồn> <đích>`
- Nguồn: `target/accounts-0.0.1-SNAPSHOT.jar` (đường dẫn tương đối so với vị trí Dockerfile)
- Đích: `accounts-0.0.1-SNAPSHOT.jar` (thư mục root của Docker image)
- File JAR chứa tất cả business code và các thư viện Spring Boot

#### Lệnh Entry Point
```dockerfile
# Thực thi ứng dụng
ENTRYPOINT ["java", "-jar", "accounts-0.0.1-SNAPSHOT.jar"]
```

**Giải thích:**
- Lệnh `ENTRYPOINT` định nghĩa những gì sẽ được thực thi khi container khởi động
- Các lệnh được cung cấp dưới dạng chuỗi ngăn cách bằng dấu phẩy trong dấu ngoặc vuông
- Mỗi phần của lệnh nằm trong dấu ngoặc kép do có khoảng trắng
- Tương đương với việc chạy: `java -jar accounts-0.0.1-SNAPSHOT.jar`
- Không cần tiền tố `target/` vì JAR nằm ở thư mục root của Docker image

## Dockerfile hoàn chỉnh

```dockerfile
# Bắt đầu với base image chứa Java runtime
FROM openjdk:17-jdk-slim

# Thông tin về người duy trì image
MAINTAINER easybytes.com

# Thêm file jar của ứng dụng vào image
COPY target/accounts-0.0.1-SNAPSHOT.jar accounts-0.0.1-SNAPSHOT.jar

# Thực thi ứng dụng
ENTRYPOINT ["java", "-jar", "accounts-0.0.1-SNAPSHOT.jar"]
```

## Các phụ thuộc của Docker Image

Khi tạo Docker image, nó đóng gói tất cả các phụ thuộc:
1. **Phụ thuộc cơ bản**: OpenJDK (Java Runtime Environment)
2. **Phụ thuộc ứng dụng**: accounts-0.0.1-SNAPSHOT.jar
   - Chứa tất cả business logic
   - Bao gồm các thư viện Spring Boot
   - Được đóng gói từ máy local của bạn

## Bước tiếp theo

Trong bài học tiếp theo, chúng ta sẽ sử dụng Dockerfile này để tạo Docker image cho Accounts Microservice.

## Những điểm chính cần nhớ

- Dockerfile phải được đặt tên chính xác là `Dockerfile` không có phần mở rộng
- `FROM` import một base image (Java runtime trong trường hợp này)
- `MAINTAINER` ghi lại thông tin người duy trì image
- `COPY` chuyển các artifacts của ứng dụng vào image
- `ENTRYPOINT` định nghĩa lệnh khởi động container
- Docker images đóng gói tất cả các phụ thuộc trong một định dạng di động

---

**Tác giả:** easybytes.com