# Xây Dựng Docker Images với Google Jib

## Giới Thiệu

Trong bài học này, chúng ta sẽ khám phá **Google Jib** như một phương pháp tạo Docker images cho các microservices Java. Jib là một công cụ chuyên biệt được thiết kế dành riêng cho việc containerize các ứng dụng Java.

## Google Jib Là Gì?

Google Jib là một công cụ mã nguồn mở để xây dựng các Docker images và OCI images được tối ưu hóa cho các ứng dụng Java mà không cần viết Dockerfile hoặc cài đặt Docker cục bộ.

**Repository chính thức:** https://github.com/GoogleContainerTools/jib

### Đặc Điểm Chính

- **Chuyên dụng cho Java**: Chỉ hoạt động với các ứng dụng Java
- **Không Cần Dockerfile**: Tạo images production-ready mà không cần viết cấu hình Docker
- **Docker Tùy Chọn**: Có thể build images mà không cần cài Docker cục bộ
- **Thời Gian Build Nhanh**: Nhanh hơn đáng kể so với Buildpacks (~11 giây so với thời gian dài hơn nhiều)

## Jib vs Buildpacks

| Tính Năng | Jib | Buildpacks |
|-----------|-----|------------|
| Hỗ Trợ Ngôn Ngữ | Chỉ Java | Python, Ruby, Node.js, Java và nhiều hơn |
| Tốc Độ Build | Nhanh (~11 giây) | Chậm hơn |
| Yêu Cầu Docker | Tùy chọn | Bắt buộc cho local builds |
| Trường Hợp Sử Dụng | Microservices Java | Dự án đa ngôn ngữ |

## Thiết Lập Jib Cho Dự Án Maven

### Bước 1: Cấu Hình Plugin trong pom.xml

Thêm Jib Maven plugin vào `pom.xml`:

```xml
<build>
    <plugins>
        <plugin>
            <groupId>com.google.cloud.tools</groupId>
            <artifactId>jib-maven-plugin</artifactId>
            <version>3.3.2</version>
            <configuration>
                <to>
                    <image>docker.io/ten-nguoi-dung/${project.artifactId}:s4</image>
                </to>
            </configuration>
        </plugin>
    </plugins>
</build>
```

### Bước 2: Cấu Hình Loại Packaging

Đảm bảo `pom.xml` của bạn có loại packaging được đặt là JAR:

```xml
<packaging>jar</packaging>
```

### Bước 3: Build Docker Image

Chạy lệnh Maven sau để tạo Docker image:

```bash
mvn compile jib:dockerBuild
```

Lệnh này sẽ:
- Quét cấu hình `pom.xml` của bạn
- Tạo Docker image production-ready
- Lưu trữ trong Docker registry cục bộ

## Ví Dụ Xây Dựng Cards Microservice

### Chi Tiết Cấu Hình

Cho ví dụ cards microservice:

```xml
<configuration>
    <to>
        <image>eazybytes/cards:s4</image>
    </to>
</configuration>
```

- **Tên Người Dùng Docker**: eazybytes
- **Project Artifact ID**: cards (lấy từ pom.xml)
- **Tag**: s4

### Quy Trình Build và Run

1. **Build image:**
   ```bash
   mvn compile jib:dockerBuild
   ```

2. **Xác minh image:**
   ```bash
   docker images
   ```
   
   Kết quả: Kích thước image khoảng 322 MB

3. **Chạy container:**
   ```bash
   docker run -d -p 9000:9000 eazybytes/cards:s4
   ```

4. **Xác minh container đang chạy:**
   ```bash
   docker ps
   ```

## Kích Thước và Chất Lượng Image

- **Kích thước**: ~322 MB (tương tự Buildpacks)
- **Chất lượng**: Production-ready, tuân theo các best practices về:
  - Tối ưu hóa hiệu suất
  - Tiêu chuẩn bảo mật
  - Layer caching
  - Nén dữ liệu

## Hiểu Về Tính Năng "Ngày Tạo"

Bạn có thể nhận thấy rằng các images được tạo bởi Jib hiển thị ngày tạo như "43 năm trước" hoặc "53 năm trước". Đây **không phải là lỗi**, mà là một tính năng có chủ đích:

### Tại Sao Lại Dùng Ngày Cũ?

- Sử dụng ngày bắt đầu cố định (thường từ những năm 1970)
- Đảm bảo builds có thể tái tạo
- Cho phép Docker nhận biết các images giống nhau
- Tối ưu hóa quá trình tái tạo image
- Nếu bạn rebuild mà không có thay đổi, hash của image vẫn giống hệt

Cách tiếp cận này cho phép caching và so sánh Docker images tốt hơn.

## Tính Năng Nâng Cao: Build Mà Không Cần Docker

Một trong những tính năng mạnh mẽ nhất của Jib là khả năng tạo Docker images **mà không cần cài Docker cục bộ**.

### Sử Dụng Lệnh Build

```bash
mvn compile jib:build
```

Lệnh này sẽ:
1. Build Docker image từ ứng dụng của bạn
2. Push trực tiếp lên registry từ xa (Docker Hub, GCR, ECR, v.v.)
3. Bỏ qua Docker cục bộ hoàn toàn

### Cấu Hình Remote Registries

#### Docker Hub
```xml
<image>docker.io/ten-nguoi-dung/ung-dung:tag</image>
```

#### Google Container Registry (GCR)
```xml
<image>gcr.io/du-an-gcp/ung-dung:tag</image>
```

#### Amazon Elastic Container Registry (ECR)
```xml
<image>tai-khoan.dkr.ecr.region.amazonaws.com/ung-dung:tag</image>
```

### Xác Thực

Khi push lên remote registries, bạn cần cấu hình thông tin đăng nhập:
- Docker Hub: Thông tin đăng nhập Docker
- GCR: Thông tin đăng nhập Google Cloud
- ECR: Thông tin đăng nhập AWS

Tham khảo tài liệu Jib để biết cấu hình xác thực cụ thể.

## Trường Hợp Sử Dụng Remote Building

Tính năng này đặc biệt có giá trị cho:

1. **CI/CD Pipelines**: Build images trong Jenkins, GitHub Actions, hoặc các công cụ CI/CD khác
2. **Build Servers Nhẹ**: Không cần cài Docker daemon nặng nề
3. **Quy Trình Làm Việc của Developer**: Developers push code, CI/CD xử lý containerization
4. **Bảo Mật**: Tránh chạy Docker daemon với quyền cao

## Tóm Tắt Từng Bước

### Bước 1: Cấu Hình Plugin
Thêm Jib Maven plugin vào `pom.xml` với cấu hình tên image dưới tag `<configuration>`.

### Bước 2: Build Image
Chạy lệnh:
```bash
mvn compile jib:dockerBuild
```

Lệnh này tạo Docker image trong hệ thống cục bộ sử dụng Docker server.

### Bước 3: Chạy Container
Thực thi container với:
```bash
docker run -d -p [host-port]:[container-port] [ten-image]:[tag]
```

Ứng dụng của bạn giờ đã sẵn sàng nhận requests dưới dạng Docker container.

## Ưu Điểm Chính

✅ **Images Production-Ready**: Tuân theo tất cả tiêu chuẩn production (hiệu suất, bảo mật, caching, nén)

✅ **Không Cần Viết Dockerfile**: Developers không cần kiến thức Docker chuyên sâu

✅ **Docker Tùy Chọn**: Có thể build mà không cần cài Docker cục bộ

✅ **Build Nhanh**: Nhanh hơn đáng kể so với các phương pháp khác

✅ **Phân Lớp Tối Ưu**: Tách layer thông minh để caching tốt hơn

✅ **Được Google Hỗ Trợ**: Được Google duy trì, đã được kiểm chứng trong môi trường production

## Kết Luận

Google Jib cung cấp một giải pháp xuất sắc để containerize các microservices Java với cấu hình tối thiểu và hiệu quả tối đa. Khả năng tạo Docker images production-ready mà không cần viết Dockerfile hoặc thậm chí không cần cài Docker cục bộ khiến nó trở thành lựa chọn hấp dẫn cho các dự án Java.

Trong bài học tiếp theo, chúng ta sẽ so sánh cả ba phương pháp (Dockerfile, Buildpacks và Jib) và chọn phương pháp tốt nhất cho phần còn lại của khóa học.

---

## Tài Liệu Tham Khảo Nhanh

| Tác Vụ | Lệnh |
|--------|------|
| Build với Docker cục bộ | `mvn compile jib:dockerBuild` |
| Build và push lên registry | `mvn compile jib:build` |
| Chạy container | `docker run -d -p [port]:[port] [image]:[tag]` |
| Liệt kê images | `docker images` |
| Liệt kê containers đang chạy | `docker ps` |