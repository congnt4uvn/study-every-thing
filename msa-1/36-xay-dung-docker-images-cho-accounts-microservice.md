# Xây Dựng Docker Images cho Accounts Microservice

## Tổng Quan

Hướng dẫn này trình bày cách xây dựng Docker image cho accounts microservice sử dụng Dockerfile. Chúng ta sẽ tìm hiểu quy trình tạo Docker image và kiểm tra nội dung của nó.

## Yêu Cầu Trước Khi Bắt Đầu

Trước khi xây dựng Docker images, hãy đảm bảo:
- Docker đã được cài đặt trên hệ thống local
- Docker server đang chạy
- Bạn đã có tài khoản Docker Hub

## Bước 1: Xác Minh Cài Đặt Docker

Đầu tiên, xác minh Docker đã được cài đặt và chạy đúng cách bằng cách thực thi lệnh version:

```bash
docker version
```

Lệnh này hiển thị cả phiên bản client và server của Docker đang chạy trên hệ thống, xác nhận rằng Docker đã được thiết lập đúng cách.

## Bước 2: Xây Dựng Docker Image

### Cấu Trúc Lệnh Docker Build

Lệnh cơ bản để xây dựng Docker image là:

```bash
docker build . -t <docker-username>/<image-name>:<tag>
```

### Các Thành Phần Lệnh:

- `docker build .` - Xây dựng image từ Dockerfile trong thư mục hiện tại
- `-t` - Flag để chỉ định tag/tên cho image
- `<docker-username>` - Tên người dùng Docker Hub của bạn
- `<image-name>` - Tên microservice của bạn (ví dụ: accounts)
- `<tag>` - Phiên bản hoặc tên tag (ví dụ: s4)

### Ví Dụ Lệnh:

```bash
docker build . -t eazybytes/accounts:s4
```

### Lưu Ý Quan Trọng:

1. **Vị Trí Dockerfile**: Nếu Dockerfile nằm trong thư mục hiện tại, sử dụng `.` (dấu chấm). Nếu không, cung cấp đường dẫn đầy đủ đến vị trí Dockerfile.

2. **Tên Người Dùng Docker**: Luôn bao gồm tên người dùng Docker Hub của bạn như một tiền tố. Điều này rất quan trọng để push images lên Docker Hub sau này.

3. **Quy Ước Đặt Tên**: Tuân theo định dạng: `username/service-name:version`
   - Ví dụ: `eazybytes/accounts:s4`
   - Trong đó `eazybytes` là tên người dùng Docker Hub
   - `accounts` là tên microservice
   - `s4` chỉ section 4 hoặc phiên bản 4

## Bước 3: Hiểu Quy Trình Build

Khi bạn thực thi lệnh build, Docker server:

1. **Tải Base Image**: Đầu tiên, nó tải base image (ví dụ: `openjdk:17-slim`) từ repository từ xa (docker.io library)

2. **Thực Hiện Các Chỉ Thị**: Sau đó thực thi tuần tự từng instruction trong Dockerfile

3. **Tạo Các Layers**: Mỗi instruction tạo một layer mới trong Docker image

### Ví Dụ Output Khi Build:

Quá trình Docker build sẽ hiển thị:
- Tải base image (openjdk17-slim)
- Sao chép accounts JAR file từ thư mục target local
- Tạo image cuối cùng với tên `docker.io/eazybytes/accounts:s4`

## Bước 4: Liệt Kê Docker Images

Sau khi build, xác minh image đã được tạo:

```bash
docker images
```

Lệnh này liệt kê tất cả Docker images trên hệ thống local. Tìm kiếm image vừa tạo:

**Ví Dụ Output:**
```
REPOSITORY            TAG    IMAGE ID       CREATED          SIZE
eazybytes/accounts    s4     abc123def456   1 minute ago     456MB
```

## Bước 5: Kiểm Tra Docker Image

Để xem thông tin chi tiết về Docker image:

```bash
docker inspect <image-id>
```

**Mẹo**: Bạn không cần gõ toàn bộ image ID. Chỉ cần sử dụng 3-4 ký tự đầu tiên.

Ví dụ:
```bash
docker inspect abc1
```

### Thông Tin Quan Trọng Từ Lệnh Inspect:

1. **Author/Maintainer**: Hiển thị ai đã tạo image (ví dụ: eazybytes.com)

2. **JAVA_HOME**: Tự động được set thành OpenJDK 17 dựa trên base image

3. **Entry Point**: Lệnh chạy khi container khởi động (ví dụ: `java -jar accounts.jar`)

4. **Operating System**: Linux (Docker sử dụng Linux namespaces và control groups)

5. **Layers**: Tất cả các layers tạo nên image của bạn

## Bước 6: Xem Image Trong Docker Desktop

Bạn cũng có thể khám phá image sử dụng giao diện Docker Desktop:

1. Mở Docker Desktop
2. Click vào phần "Images"
3. Tìm image của bạn (ví dụ: `accounts:s4`)
4. Click vào tên image để xem tất cả layers

Biểu diễn trực quan này hiển thị tất cả các layers có sẵn trong Docker image, xác nhận việc tạo thành công.

## Hiểu Kiến Trúc Docker

### Các Thành Phần Docker:

- **Docker CLI (Client)**: Giao diện dòng lệnh nơi bạn chạy các lệnh Docker
- **Docker Server (Daemon)**: Dịch vụ backend xử lý các lệnh Docker và quản lý images/containers
- **Docker Hub**: Repository từ xa để lưu trữ và chia sẻ Docker images

### Lưu Ý Quan Trọng:

Tất cả các lệnh Docker yêu cầu Docker server phải đang chạy. Nếu server không chạy, các lệnh như `docker build`, `docker images`, hoặc bất kỳ lệnh Docker nào khác sẽ không hoạt động.

## Các Bước Tiếp Theo

Bây giờ Docker image đã được tạo thành công, bạn đã sẵn sàng để:
1. Chuyển đổi Docker image thành Docker container
2. Test microservice đã được containerize
3. Push image lên Docker Hub để chia sẻ

## Tóm Tắt

Trong hướng dẫn này, bạn đã học:
- Cách xác minh cài đặt Docker
- Xây dựng Docker images sử dụng lệnh `docker build`
- Quy ước đặt tên đúng cho Docker images
- Liệt kê và kiểm tra Docker images
- Hiểu quy trình build và kiến trúc Docker
- Sử dụng Docker Desktop để xem chi tiết image

## Best Practices (Thực Hành Tốt Nhất)

1. Luôn bao gồm tên người dùng Docker Hub trong tên image
2. Sử dụng tags/versions có ý nghĩa cho images
3. Đảm bảo Docker server đang chạy trước khi thực thi lệnh
4. Thực hành các lệnh này nhiều lần để xây dựng sự quen thuộc
5. Giữ Dockerfile trong thư mục root của dự án microservice

---

**Lưu Ý**: Khi bạn thực hành các lệnh Docker này nhiều lần, chúng sẽ trở nên quen thuộc. Chi tiết bổ sung về các lệnh Docker sẽ được đề cập trong các bài giảng sắp tới.