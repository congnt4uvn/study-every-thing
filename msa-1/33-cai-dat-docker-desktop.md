# Cài Đặt Docker Desktop

## Tổng Quan

Bài giảng này cung cấp hướng dẫn từng bước để cài đặt Docker Desktop trên hệ thống local của bạn. Việc cài đặt Docker là điều cần thiết để thực hành các khái niệm microservice và container hóa ứng dụng Spring Boot.

## Yêu Cầu Hệ Thống

Trước khi cài đặt Docker, hãy đảm bảo hệ thống của bạn đáp ứng các yêu cầu sau:

- **RAM tối thiểu:** 4 GB RAM hệ thống
- **Bộ xử lý:** Bộ xử lý 64-bit
- **Hệ điều hành được hỗ trợ:**
  - Apple macOS
  - Microsoft Windows
  - Linux

## Các Bước Cài Đặt

### Bước 1: Truy Cập Website Docker

Truy cập [docker.com](https://docker.com) trên trình duyệt web của bạn.

### Bước 2: Tải Docker Desktop

1. Trên trang chủ, bạn sẽ thấy tùy chọn "Download Docker Desktop"
2. Website tự động phát hiện hệ điều hành của bạn (Mac, Windows hoặc Linux)
3. Chọn phiên bản phù hợp cho hệ điều hành của bạn
4. Nhấp vào "Download Docker Desktop"

### Bước 3: Cài Đặt Docker

1. Sau khi tải xuống hoàn tất, tìm file cài đặt
2. Nhấp đúp vào file cài đặt
3. Làm theo trình hướng dẫn cài đặt (nhấp Next → Next → Next)
4. Hoàn tất quá trình cài đặt

### Bước 4: Xác Minh Cài Đặt

Quá trình cài đặt rất đơn giản và sẽ hoàn tất mà không gặp vấn đề gì. Nếu bạn cần thêm trợ giúp, hãy tham khảo tài liệu chính thức.

## Tài Liệu và Hỗ Trợ Docker

Nếu bạn gặp bất kỳ thách thức nào trong quá trình cài đặt:

### Tài Liệu Chính Thức

1. Nhấp vào "Get Started" trên website Docker
2. Chọn "Learn how to install Docker"
3. Điều hướng đến [website tài liệu Docker](https://docs.docker.com)
4. Chọn hệ điều hành của bạn:
   - Install Docker Desktop on Mac
   - Install Docker Desktop on Windows
   - Install Docker Desktop on Linux

### Tài Nguyên Khắc Phục Sự Cố

Nếu bạn gặp vấn đề cài đặt, có nhiều nguồn tài nguyên có sẵn:

1. **Docker Troubleshooting Guide:** Kiểm tra tài liệu khắc phục sự cố chính thức cho các vấn đề phổ biến
2. **Stack Overflow:** Tìm kiếm các vấn đề cài đặt Docker trên Stack Overflow
3. **Docker Community:** Truy cập trợ giúp từ diễn đàn cộng đồng Docker
4. **Course Q&A:** Đăng câu hỏi trong phần Q&A của Udemy

**Quan trọng:** Đừng nản lòng - quá trình cài đặt được thiết kế để đơn giản và dễ dàng!

## Tạo Tài Khoản Docker Hub

### Bước 1: Đăng Ký

1. Sau khi cài đặt Docker Desktop, nhấp vào nút "Sign In"
2. Bạn sẽ được chuyển hướng đến [hub.docker.com](https://hub.docker.com)
3. Tạo tài khoản mới nếu bạn chưa có
4. Chọn tên người dùng và mật khẩu
5. **Không cần thẻ tín dụng** cho gói miễn phí

### Bước 2: Ghi Nhớ Tên Người Dùng

Tên người dùng Docker Hub của bạn rất quan trọng - bạn sẽ cần nó trong các bài giảng sắp tới. Ví dụ:
- Tên người dùng: `eazybytes`

### Bước 3: Chọn Gói

Docker Hub cung cấp nhiều gói:

#### Gói Personal (Miễn phí - $0)
- **Repositories công khai không giới hạn**
- Hoàn hảo cho khóa học này
- Lý tưởng cho việc học và các dự án cá nhân
- Không cần thanh toán

#### Gói Trả Phí
- **Gói Pro, Team và Business** có sẵn
- Bắt buộc cho repositories riêng tư
- Được sử dụng trong môi trường production
- Các tổ chức thường cung cấp những gói này cho các dự án thực tế

**Cho khóa học này:** Gói Personal (miễn phí) là đủ. Tất cả Docker images sẽ được lưu trữ trong repositories công khai.

## Tính Năng Docker Hub

### Official Images

Docker Hub lưu trữ các images chính thức từ các sản phẩm và nền tảng lớn:
- **Python:** Images runtime Python chính thức
- **MySQL:** Hơn 1 tỷ lượt tải xuống
- **PostgreSQL:** Image cơ sở dữ liệu phổ biến
- **Ubuntu:** Images Ubuntu Linux chính thức
- Và nhiều hơn nữa...

### Tìm Kiếm Images

**Ví dụ: Tìm MySQL Image**

1. Tìm kiếm "MySQL" trong Docker Hub
2. Tìm thẻ "Docker Official Image"
3. Lưu ý số lượt tải xuống (ví dụ: 1 tỷ+ lượt tải xuống)
4. Sử dụng lệnh được cung cấp để pull image:
   ```bash
   docker pull mysql
   ```

### Sử Dụng Docker Hub

Docker Hub phục vụ hai mục đích chính:

1. **Lưu Trữ Images Của Bạn:** Tải lên Docker images của riêng bạn (công khai hoặc riêng tư)
2. **Lấy Images Khác:** Tải xuống và sử dụng images chính thức từ các sản phẩm, cơ sở dữ liệu, servers và ngôn ngữ lập trình

## Ứng Dụng Docker Desktop

### Truy Cập Docker Desktop

Sau khi cài đặt và đăng nhập:

1. Nhấp vào biểu tượng Docker trong khay hệ thống (Windows/Linux) hoặc thanh menu (Mac)
2. Nhấp vào "Dashboard" để mở ứng dụng Docker Desktop

### Tính Năng Docker Dashboard

Docker Desktop dashboard cung cấp quyền truy cập vào:

- **Images:** Xem tất cả Docker images local
- **Containers:** Quản lý containers đang chạy và đã dừng
- **Volumes:** Quản lý Docker volumes
- **Settings:** Cấu hình các tùy chọn Docker

### Đăng Nhập

Nếu bạn chưa đăng nhập:

1. Nhấp vào nút ở góc trên bên phải của Docker Desktop
2. Nhập thông tin đăng nhập Docker Hub của bạn (tên người dùng và mật khẩu)
3. Docker local của bạn sẽ kết nối với repository Docker Hub của bạn

Kết nối này cho phép bạn:
- Đẩy images lên Docker Hub
- Kéo private images từ repositories của bạn
- Đồng bộ hóa môi trường Docker local và remote của bạn

## Xác Minh Cài Đặt

### Sử Dụng Terminal/Command Line

Bạn có thể xác nhận cài đặt Docker thành công bằng cách chạy lệnh trong terminal của bạn.

#### Kiểm Tra Phiên Bản Docker

Chạy lệnh sau:
```bash
docker version
```

**Kết quả mong đợi:**
- **Thông tin Client:**
  - Chi tiết phiên bản
  - Hệ điều hành (ví dụ: Darwin cho Mac, Windows, Linux)
  
- **Thông tin Server:**
  - Chi tiết phiên bản
  - Hệ điều hành (thường là Linux)

### Hiểu Về Kiến Trúc

**Lưu ý quan trọng:** Bất kể hệ điều hành host của bạn (Mac, Windows), Docker nội bộ tạo một máy ảo Linux nhỏ và nhẹ nơi Docker server chạy.

**Ví dụ:**
- **Host OS:** macOS (Darwin)
- **Docker Server OS:** Linux (chạy trong một VM nhẹ)

Kiến trúc này đảm bảo hành vi nhất quán trên tất cả các nền tảng.

## Thực Hành Tốt Nhất

### Trước Khi Tiếp Tục

1. ✅ **Cài đặt Docker Desktop** trên hệ thống local của bạn
2. ✅ **Tạo tài khoản Docker Hub** với tên người dùng dễ nhớ
3. ✅ **Đăng nhập vào Docker Desktop** với thông tin đăng nhập của bạn
4. ✅ **Xác minh cài đặt** bằng lệnh `docker version`
5. ✅ **Làm quen với** Docker Dashboard

### Lời Nhắc Quan Trọng

- **Thực hành là Cần thiết:** Nếu không cài đặt Docker, bạn không thể thực hành các khái niệm microservice được đề cập trong các bài giảng sắp tới
- **Gói Miễn Phí Là Đủ:** Gói Personal (miễn phí) cung cấp mọi thứ cần thiết cho khóa học này
- **Hỗ Trợ Cộng Đồng:** Trợ giúp rộng rãi có sẵn từ cộng đồng Docker nếu bạn gặp vấn đề
- **Tài Liệu:** Tài liệu Docker chính thức cung cấp hướng dẫn cài đặt chi tiết cho tất cả các nền tảng

## Vấn Đề Phổ Biến và Giải Pháp

### Cài Đặt Thất Bại

1. Kiểm tra yêu cầu hệ thống (4GB RAM, bộ xử lý 64-bit)
2. Đảm bảo bạn có quyền administrator/root
3. Kiểm tra phần mềm xung đột
4. Tham khảo hướng dẫn khắc phục sự cố

### Không Thể Đăng Nhập Docker Hub

1. Xác minh tên người dùng và mật khẩu của bạn
2. Kiểm tra kết nối internet
3. Thử đặt lại mật khẩu trên hub.docker.com

### Lệnh Docker Version Không Tìm Thấy

1. Khởi động lại terminal/command prompt của bạn
2. Kiểm tra xem Docker Desktop có đang chạy không
3. Cài đặt lại Docker nếu cần thiết

## Bước Tiếp Theo

Với Docker được cài đặt thành công:

1. Bạn sẽ học các lệnh và thao tác Docker
2. Bạn sẽ tạo Docker images cho Spring Boot microservices
3. Bạn sẽ chạy containers từ Docker images
4. Bạn sẽ đẩy images lên Docker Hub
5. Bạn sẽ triển khai các microservices được container hóa

## Tóm Tắt

Các điểm chính được đề cập trong bài giảng này:

- Cài đặt Docker Desktop rất đơn giản và có tài liệu đầy đủ
- Docker Hub cung cấp gói Personal miễn phí cho repositories công khai
- Docker Desktop dashboard quản lý images, containers và volumes
- Docker nội bộ sử dụng Linux cho server, bất kể host OS
- Images chính thức từ các sản phẩm lớn có sẵn trên Docker Hub
- Hỗ trợ cộng đồng rất rộng rãi để khắc phục sự cố

**Cài đặt Docker của bạn giờ đây sẽ hoàn tất và được xác minh!**

## Tham Khảo Nhanh

### URLs Quan Trọng
- Website Docker: [docker.com](https://docker.com)
- Docker Hub: [hub.docker.com](https://hub.docker.com)
- Tài liệu Docker: [docs.docker.com](https://docs.docker.com)

### Lệnh Chính
```bash
# Kiểm tra phiên bản Docker
docker version

# Pull một image từ Docker Hub
docker pull <image-name>

# Xem images local
docker images

# Xem containers đang chạy
docker ps
```

---

**Sẵn Sàng Để Thực Hành:** Với Docker được cài đặt và xác minh, bạn hiện đã sẵn sàng để khám phá việc container hóa microservices và tìm hiểu các lệnh Docker trong các bài giảng sắp tới!