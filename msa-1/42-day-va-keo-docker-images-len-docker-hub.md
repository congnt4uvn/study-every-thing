# Đẩy và Kéo Docker Images lên Docker Hub

## Tổng Quan
Trong bài học này, chúng ta sẽ học cách đẩy (push) Docker images từ hệ thống local lên kho lưu trữ từ xa của Docker Hub và cách kéo (pull) chúng về. Điều này rất quan trọng cho việc triển khai microservices lên môi trường production, development hoặc QA.

## Tại Sao Cần Sử Dụng Kho Lưu Trữ Docker Từ Xa?

Docker images chỉ lưu trữ trên hệ thống local của bạn không thể được triển khai lên server production. Giống như cách chúng ta đẩy code lên GitHub, chúng ta cần đẩy Docker images lên các kho lưu trữ từ xa như:

- **Docker Hub** (registry công khai)
- **AWS ECR** (Amazon Elastic Container Registry)
- **GCP Container Registry**
- **Azure Container Registry**
- **GitHub Container Registry**

Trong khóa học này, chúng ta sẽ sử dụng Docker Hub làm kho lưu trữ từ xa.

## Đẩy Docker Images lên Docker Hub

### Cú Pháp Lệnh Push

```bash
docker image push docker.io/<tên-người-dùng>/<tên-image>:<tag>
```

### Ví Dụ: Đẩy Accounts Microservice

```bash
docker image push docker.io/eazybytes/accounts:S4
```

**Phân Tích Lệnh:**
- `docker.io` - Registry của Docker Hub
- `eazybytes` - Tên người dùng Docker Hub
- `accounts` - Tên image
- `S4` - Tên tag

### Đẩy Nhiều Microservices

**Đẩy Loans Microservice:**
```bash
docker image push docker.io/eazybytes/loans:S4
```

**Đẩy Cards Microservice:**
```bash
docker image push docker.io/eazybytes/cards:S4
```

## Xác Thực

### Cách Xác Thực Hoạt Động

Khi bạn thực thi lệnh push, Docker CLI tự động sử dụng thông tin đăng nhập từ Docker Desktop nếu bạn đã đăng nhập. CLI và Docker Desktop làm việc cùng nhau để:

1. Lấy username và password từ Docker Desktop
2. Xác thực với Docker Hub
3. Đẩy image lên kho lưu trữ từ xa

### Lưu Ý Quan Trọng

- **Sử dụng username của riêng bạn:** Không sử dụng username của người khác (như `eazybytes`) trong lệnh push của bạn
- **Yêu cầu đăng nhập:** Nếu bạn chưa đăng nhập vào Docker Desktop, bạn sẽ nhận lỗi "access denied"
- **Tính nhất quán của username:** Sử dụng cùng một username trong `pom.xml` khi tạo Docker images

## Xác Minh Images Đã Được Đẩy Lên

### Phương Pháp 1: Docker Desktop

1. Mở Docker Desktop
2. Nhấp vào phần **Hub**
3. Xem tất cả images trong kho lưu trữ từ xa với:
   - Tên images
   - Tên tags
   - Thời gian đẩy lên
   - Kích thước images

### Phương Pháp 2: Website Docker Hub

1. Đăng nhập vào [hub.docker.com](https://hub.docker.com)
2. Xem các repositories của bạn
3. Kiểm tra chi tiết image bao gồm:
   - Các tags có sẵn
   - Cài đặt hiển thị (public/private)
   - Lệnh pull
   - Lịch sử đẩy lên

## Hiển Thị Image: Public vs Private

### Images Public (Mặc Định)

- Bất kỳ ai cũng có thể pull Docker images của bạn
- Không cần thông tin đăng nhập để tải xuống
- Tương tự như GitHub repositories công khai
- Lý tưởng cho các dự án mã nguồn mở

### Images Private

- Chỉ bạn (và người dùng được ủy quyền) có thể truy cập
- Yêu cầu xác thực để pull
- Gói personal cơ bản cho phép **một kho lưu trữ private**
- Có thể thay đổi trong cài đặt repository

Để thay đổi hiển thị:
1. Vào cài đặt repository
2. Điều hướng đến cài đặt visibility
3. Chuyển đổi giữa public và private

## Kéo Docker Images từ Docker Hub

### Cú Pháp Lệnh Pull

```bash
docker pull <tên-người-dùng>/<tên-image>:<tag>
```

### Ví Dụ: Kéo Cards Microservice

```bash
docker pull eazybytes/cards:S4
```

### Kiểm Tra Quá Trình Pull

1. **Xóa image local:**
   ```bash
   docker images  # Liệt kê các images hiện tại
   # Xóa từ giao diện Docker Desktop hoặc sử dụng:
   docker rmi eazybytes/cards:S4
   ```

2. **Pull từ Docker Hub:**
   ```bash
   docker pull eazybytes/cards:S4
   ```

3. **Xác minh tải xuống:**
   ```bash
   docker images  # Sẽ hiển thị lại cards image
   ```

## Push vs Pull: Sự Khác Biệt Chính

| Lệnh | Hướng | Mục Đích |
|------|-------|----------|
| `docker push` | Local → Từ xa | Tải images lên Docker Hub |
| `docker pull` | Từ xa → Local | Tải images xuống từ Docker Hub |

## Trường Hợp Sử Dụng Docker Hub

### Cộng Tác Nhóm
- Các thành viên trong nhóm có thể pull Docker images
- Không cần rebuild images trên local
- Triển khai nhất quán trong toàn nhóm

### CI/CD Pipelines
- Các công cụ tự động lấy images từ Docker Hub
- Triển khai lên cloud servers (AWS, Azure, GCP)
- Triển khai lên máy ảo
- Quy trình triển khai liên tục

### Các Tình Huống Triển Khai
- Triển khai **Accounts microservice**
- Triển khai **Loans microservice**
- Triển khai **Cards microservice**
- Triển khai đa môi trường (dev, QA, production)

## Thực Hành Tốt Nhất

1. **Quản Lý Username:**
   - Luôn sử dụng Docker Hub username của riêng bạn
   - Đảm bảo tính nhất quán trong `pom.xml` và lệnh push

2. **Chiến Lược Tagging:**
   - Sử dụng các tags có ý nghĩa (ví dụ: `S4`, `v1.0`, `latest`)
   - Duy trì kiểm soát phiên bản thông qua tags

3. **Tổ Chức Image:**
   - Đặt tên image: `<username>/<tên-ứng-dụng>:<tag>`
   - Giữ quy ước đặt tên nhất quán

4. **Bảo Mật:**
   - Sử dụng repositories private cho các ứng dụng nhạy cảm
   - Giữ thông tin đăng nhập an toàn
   - Cập nhật images thường xuyên

## Tóm Tắt

Trong bài học này, chúng ta đã đề cập:
- ✅ Đẩy Docker images lên Docker Hub
- ✅ Xác thực với Docker Hub thông qua Docker Desktop
- ✅ Xác minh images trong Docker Hub (Desktop & Website)
- ✅ Hiển thị image public vs private
- ✅ Kéo Docker images từ Docker Hub
- ✅ Trường hợp sử dụng cho kho lưu trữ Docker từ xa

Docker Hub cho phép cộng tác và triển khai microservices một cách liền mạch trên các môi trường và thành viên nhóm khác nhau.

## Các Bước Tiếp Theo

Trong bài học tiếp theo, chúng ta sẽ khám phá các khái niệm Docker nâng cao hơn cho việc triển khai microservices.

---

**Lưu Ý:** Tất cả các lệnh Docker được sử dụng trong bài học này đều có sẵn trong GitHub repository của khóa học để tham khảo.