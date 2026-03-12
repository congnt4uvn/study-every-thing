# Tạo Docker Images cho Microservices với Google Jib

## Tổng Quan

Hướng dẫn này trình bày quy trình tạo Docker images cho các microservices Spring Boot sử dụng Google Jib Maven plugin, bao gồm Config Server và Eureka Server, và đẩy chúng lên Docker Hub.

## Yêu Cầu Trước Khi Bắt Đầu

- Docker server đang chạy trên hệ thống local
- Đã cài đặt Maven
- Các dự án microservices (Config Server, Eureka Server, Accounts, Loans, Cards)
- Tài khoản Docker Hub để đẩy images

## Các Bước Thực Hiện

### 1. Thêm Jib Plugin vào Eureka Server

Dự án Eureka Server cần cấu hình Google Jib plugin trong file `pom.xml`.

**Các bước:**
1. Mở file `pom.xml` của bất kỳ microservice nào (ví dụ: Config Server)
2. Sao chép cấu hình Google Jib plugin
3. Thêm vào file `pom.xml` của Eureka Server
4. Cập nhật tag name từ `S6` sang `S8` (Section 8)

> **Lưu ý:** Mặc định, dự án Eureka Server chỉ có cấu hình Spring Boot Maven plugin.

### 2. Cập Nhật Thông Tin Tag Cho Tất Cả Microservices

Cập nhật Docker image tag từ `S6` sang `S8` trong tất cả microservices:

- **Config Server** - Cập nhật tag sang S8
- **Accounts Microservice** - Cập nhật tag từ S6 sang S8
- **Cards Microservice** - Cập nhật tag sang S8
- **Loans Microservice** - Cập nhật tag sang S8

> **Tại sao là S6 chứ không phải S7?** Code được sao chép từ Section 6, không phải Section 7, nên tag ban đầu là S6.

### 3. Build Tất Cả Microservices

1. Thực hiện clean build hoàn toàn cho tất cả microservices
2. Dừng tất cả các instances đang chạy trong IntelliJ IDEA
3. Load tất cả các thay đổi Maven trước khi tiếp tục

### 4. Tạo Docker Images Sử Dụng Jib

Di chuyển đến thư mục của từng microservice trong terminal và thực thi lệnh Maven sau:

```bash
mvn compile jib:dockerBuild
```

#### Thứ Tự Build (Section 8):

1. **Config Server**
   ```bash
   cd config-server
   mvn compile jib:dockerBuild
   ```
   - Lưu ý: Về mặt kỹ thuật không bắt buộc vì không có thay đổi, nhưng vẫn tạo để đồng nhất

2. **Eureka Server**
   ```bash
   cd eureka-server
   mvn compile jib:dockerBuild
   ```

3. **Accounts Microservice**
   ```bash
   cd accounts
   mvn compile jib:dockerBuild
   ```

4. **Loans Microservice**
   ```bash
   cd loans
   mvn compile jib:dockerBuild
   ```

5. **Cards Microservice**
   ```bash
   cd cards
   mvn compile jib:dockerBuild
   ```

> **Lưu ý:** Thứ tự tạo Docker images không quan trọng. Bạn có thể tạo theo bất kỳ trình tự nào.

### 5. Quản Lý Docker Images

#### Dọn Dẹp Images Cũ

1. Mở Docker Dashboard
2. Tìm kiếm các images có tag `S7`
3. Xóa các images không sử dụng để tiết kiệm dung lượng đĩa local
4. Click "Delete Forever" để xóa vĩnh viễn

#### Kiểm Tra Images Mới

Tìm kiếm `S8` trong Docker Dashboard để xem tất cả năm Docker images mới được tạo:
- Config Server (S8)
- Eureka Server (S8)
- Accounts (S8)
- Loans (S8)
- Cards (S8)

### 6. Đẩy Images Lên Docker Hub

Sử dụng cấu trúc lệnh sau để đẩy images lên Docker Hub:

```bash
docker image push docker.io/<docker-username-của-bạn>/<tên-image>:<tag>
```

**Ví dụ:**
```bash
docker image push docker.io/easybytes/configserver:S8
```

Lặp lại quy trình này cho tất cả năm Docker images:
- configserver:S8
- eurekaserver:S8
- accounts:S8
- loans:S8
- cards:S8

### 7. Xác Minh Docker Hub Repository

Sau khi đẩy lên, xác minh trong Docker Hub rằng:
1. Tất cả images đã được upload thành công
2. Mỗi repository chứa nhiều phiên bản (S4, S6, S7, S8, v.v.)
3. Image `eurekaserver` mới đã có mặt

## Tóm Tắt

Bạn đã hoàn thành thành công:
- ✅ Cấu hình Google Jib plugin cho tất cả microservices
- ✅ Cập nhật Docker image tags sang S8
- ✅ Tạo Docker images cho tất cả năm services
- ✅ Dọn dẹp các images S7 cũ
- ✅ Đẩy tất cả images lên Docker Hub

## Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ:
- Cập nhật file Docker Compose
- Khởi động tất cả services với một lệnh Docker Compose duy nhất
- Xác thực service discovery và registration trong môi trường Docker

## Tham Khảo Các Lệnh Chính

| Nhiệm Vụ | Lệnh |
|----------|------|
| Tạo Docker Image | `mvn compile jib:dockerBuild` |
| Đẩy lên Docker Hub | `docker image push docker.io/<username>/<image>:<tag>` |
| Liệt kê Docker Images | `docker images` |

---

**Chủ Đề Liên Quan:**
- Google Jib Maven Plugin
- Spring Boot Microservices
- Quản Lý Docker Image
- Service Discovery với Eureka
- Docker Hub Registry