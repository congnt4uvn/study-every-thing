# Chạy Docker Containers từ Docker Images

## Tổng Quan

Hướng dẫn này trình bày cách chạy Docker containers từ Docker images, quản lý vòng đời container, hiểu về port mapping, và tận dụng Docker để giải quyết các thách thức về triển khai, tính di động và khả năng mở rộng trong microservices.

## Tương Tự Lệnh Docker Run

Lệnh `docker run` tương tự như toán tử `new` trong Java:
- Giống như toán tử `new` tạo nhiều instances/objects của một class
- Lệnh `docker run` tạo nhiều containers từ một Docker image

## Chạy Container Đầu Tiên

### Lệnh Docker Run Cơ Bản

```bash
docker run -p 8080:8080 eazybytes/accounts:s4
```

### Các Thành Phần Lệnh:

- `docker run` - Lệnh để tạo và khởi động container
- `-p 8080:8080` - Port mapping (host:container)
- `eazybytes/accounts:s4` - Tên Docker image

### Hiểu Output:

Khi bạn thực thi lệnh này:
- Docker container khởi động thành công
- Accounts microservice khởi động ở port 8080
- Các log khởi động Spring Boot xuất hiện trong terminal
- Container chạy ở **attached mode** (chế độ foreground)

### Test Container:

Bạn có thể validate container đang chạy bằng các công cụ như Postman:
1. Gửi request đến `http://localhost:8080/api/create`
2. Bạn sẽ nhận được response thành công
3. Điều này xác nhận microservice đang chạy đúng

## Hiểu Về Port Mapping

### Tại Sao Cần Port Mapping

Mặc định, Docker containers khởi động trong **mạng cô lập** riêng của chúng. Các dịch vụ chạy bên trong containers không thể được truy cập từ mạng bên ngoài (như hệ thống local của bạn) nếu không có port mapping rõ ràng.

### Cú Pháp Port Mapping

```bash
docker run -p <host-port>:<container-port> <image-name>
```

### Phân Tích Port Mapping:

- **Port Đầu Tiên (Host Port)**: `8080` - Port được expose ra thế giới bên ngoài (hệ thống local của bạn)
- **Port Thứ Hai (Container Port)**: `8080` - Port nơi container chạy bên trong Docker network

**Ví Dụ**: `-p 8081:8080`
- Container chạy ở port 8080 bên trong Docker network
- Được expose ra hệ thống bên ngoài ở port 8081
- Các request bên ngoài phải sử dụng port 8081 để truy cập service

### Biểu Diễn Trực Quan:

```
Mạng Bên Ngoài (Hệ Thống Local)
         ↓ (Port 8081)
    Port Mapping
         ↓
Docker Network (Cô Lập)
         ↓ (Port 8080)
    Accounts Container
```

## Chạy Containers Ở Detached Mode

### Vấn Đề Với Attached Mode

Khi chạy ở attached mode (mặc định):
- Terminal bị block bởi các log của container
- Không thể chạy các lệnh khác
- Không tiện lợi cho developers

### Giải Pháp: Detached Mode

Sử dụng flag `-d` để chạy containers ở background:

```bash
docker run -d -p 8080:8080 eazybytes/accounts:s4
```

### Lợi Ích Của Detached Mode:

- Container chạy ở background
- Terminal vẫn sẵn sàng cho các lệnh khác
- Trả về container ID ngay lập tức
- Không hiển thị logs trong terminal (truy cập chúng riêng)

**Ví Dụ Output:**
```
abc123def456789... (container ID)
```

## Quản Lý Docker Containers

### Liệt Kê Các Container Đang Chạy

```bash
docker ps
```

**Output Mẫu:**
```
CONTAINER ID   IMAGE                    COMMAND                  CREATED          STATUS          PORTS                    NAMES
abc123def456   eazybytes/accounts:s4   "java -jar accounts…"   23 seconds ago   Up 22 seconds   0.0.0.0:8080->8080/tcp  random_name
```

**Thông Tin Hiển Thị:**
- Container ID
- Tên image
- Lệnh được sử dụng để chạy
- Thời gian tạo
- Port mapping
- Tên container (được tạo ngẫu nhiên)

### Liệt Kê Tất Cả Containers (Bao Gồm Đã Dừng)

```bash
docker ps -a
```

Lệnh này hiển thị tất cả containers bất kể trạng thái của chúng (running hoặc stopped).

### Khởi Động Container Đã Tồn Tại

```bash
docker start <container-id>
```

**Lưu Ý**: Bạn có thể chỉ sử dụng 3-4 ký tự đầu tiên của container ID:

```bash
docker start abc1
```

### Dừng Container Đang Chạy

```bash
docker stop <container-id>
```

**Ví Dụ:**
```bash
docker stop abc1
```

### Dừng Từ Docker Desktop

1. Mở Docker Desktop
2. Vào phần Containers
3. Tìm container đang chạy của bạn
4. Click nút "Stop"

## Sử Dụng Docker Desktop

### Xem Containers

Docker Desktop cung cấp GUI để quản lý containers:

1. **Tab Containers**: Xem tất cả containers
2. **Tùy Chọn Filter**: Hiển thị chỉ containers đang chạy
3. **Chi Tiết Container**: Click vào bất kỳ container nào để xem:
   - **Logs**: Logs khởi động Spring Boot và logs ứng dụng
   - **Inspect**: Cấu hình container (JAVA_VERSION, JAVA_HOME, ports)
   - **Files**: Duyệt filesystem của container
   - **Stats**: Sử dụng CPU, memory, tiêu thụ tài nguyên
   - **Terminal**: Truy cập giao diện command-line của container

### Container Logs

Xem logs trong Docker Desktop:
- Tất cả logs khởi động Spring Boot
- Logs gọi REST API
- Cập nhật logs real-time

### Container Inspection

Xem cấu hình chi tiết:
- `JAVA_VERSION`: Phiên bản JDK đang sử dụng
- `JAVA_HOME`: Đường dẫn đến JDK (ví dụ: `/usr/local/openjdk`)
- Cấu hình port
- Biến môi trường

### Container Files

Duyệt filesystem của container:
- Xác minh vị trí file JAR (ví dụ: thư mục root)
- Kiểm tra đường dẫn cài đặt JDK (`/usr/local/openjdk`)
- Kiểm tra tất cả files được bao gồm trong image

### Container Terminal

Truy cập terminal của container đang chạy:
```bash
pwd  # Kiểm tra thư mục hiện tại (thường là root /)
```

Điều này cho phép bạn thực thi các lệnh trực tiếp bên trong container đang chạy.

### Container Statistics

Giám sát việc sử dụng tài nguyên:
- **CPU Usage**: Phần trăm CPU được sử dụng
- **Memory Usage**: Tiêu thụ RAM
- **Network I/O**: Tốc độ truyền dữ liệu
- **Disk I/O**: Các hoạt động đọc/ghi

## Chạy Nhiều Containers

### Tạo Nhiều Instances

Bạn có thể tạo bất kỳ số lượng containers nào từ cùng một Docker image:

**Container Đầu Tiên:**
```bash
docker run -d -p 8080:8080 eazybytes/accounts:s4
```

**Container Thứ Hai:**
```bash
docker run -d -p 8081:8080 eazybytes/accounts:s4
```

### Lưu Ý Quan Trọng Với Nhiều Containers:

1. **Host Ports Phải Là Duy Nhất**: Bạn không thể sử dụng lại cùng một host port (8080, 8081 phải khác nhau)
2. **Container Ports Có Thể Giống Nhau**: Containers chạy trong mạng cô lập, nên các internal ports có thể giống nhau
3. **Mỗi Container Là Độc Lập**: Các instances riêng biệt với tài nguyên riêng

### Port Mapping Cho Nhiều Containers:

```
Container 1: -p 8080:8080
  - Hệ thống host: port 8080
  - Container: port 8080

Container 2: -p 8081:8080
  - Hệ thống host: port 8081
  - Container: port 8080
```

### Tại Sao Host Ports Phải Khác Nhau?

- Hệ thống local của bạn chia sẻ một mạng
- Port 8080 chỉ có thể được sử dụng một lần trên host
- Containers có mạng cô lập, nên chúng có thể sử dụng cùng internal port

### Xác Minh

Kiểm tra cả hai containers đang chạy:
```bash
docker ps
```

**Output:**
```
CONTAINER ID   IMAGE                    PORTS                    NAMES
abc123def456   eazybytes/accounts:s4   0.0.0.0:8080->8080/tcp  container1
def456abc789   eazybytes/accounts:s4   0.0.0.0:8081->8080/tcp  container2
```

### Test Nhiều Containers

Test từng container bằng Postman:
- Container 1: `http://localhost:8080/api/create`
- Container 2: `http://localhost:8081/api/create`

Cả hai đều phải response thành công với dữ liệu độc lập.

## Xóa Containers

### Sử Dụng Docker Desktop

1. Mở Docker Desktop
2. Vào phần Containers
3. Chọn các containers bạn muốn xóa
4. Click nút "Delete"

### Sử Dụng Terminal

```bash
docker rm <container-id>
```

**Lưu Ý**: Bạn phải dừng container trước khi xóa nó.

## Lợi Ích Của Docker Cho Microservices

### 1. Khả Năng Mở Rộng (Scalability)

**Dễ Dàng Mở Rộng Theo Chiều Ngang:**
- Tạo nhiều instances với một lệnh duy nhất
- Scale từ 1 đến N instances ngay lập tức
- Không cần thiết lập phức tạp

**Ví Dụ:**
```bash
docker run -d -p 8080:8080 eazybytes/accounts:s4
docker run -d -p 8081:8080 eazybytes/accounts:s4
docker run -d -p 8082:8080 eazybytes/accounts:s4
```

### 2. Tính Di Động (Portability)

**Chạy Bất Cứ Nơi Nào Docker Được Cài Đặt:**
- Cùng một Docker image hoạt động trên bất kỳ hệ thống nào
- Không cần cài đặt JDK, Spring Boot, hoặc Maven riêng
- Tất cả dependencies được bao gồm trong image
- Hành vi nhất quán trên các môi trường

**Người Dùng Chỉ Cần:**
- Docker được cài đặt
- Docker image
- Một lệnh: `docker run`

### 3. Đơn Giản Hóa Triển Khai (Deployment)

**Triển Khai Nhất Quán Trên Các Môi Trường:**
- Hệ thống local
- Virtual machines
- Cloud servers (AWS, Azure, GCP)
- Data centers on-premises

**Cùng Lệnh Ở Mọi Nơi:**
```bash
docker run -d -p 8080:8080 eazybytes/accounts:s4
```

**Không Cần Cấu Hình Theo Môi Trường:**
- Cùng Docker image
- Cùng lệnh
- Hành vi dự đoán được

## Tóm Tắt Workflow Hoàn Chỉnh

### Các Bước Chạy Spring Boot Application Trong Docker

**Bước 1: Build Application**
```bash
mvn clean install
```
- Chạy từ vị trí có file `pom.xml`
- Tạo fat JAR trong thư mục `target`

**Bước 2: Tạo Dockerfile**

Định nghĩa instructions để build Docker image với:
- Base image (ví dụ: OpenJDK)
- Copy file JAR
- Lệnh entry point

**Bước 3: Build Docker Image**
```bash
docker build . -t eazybytes/accounts:s4
```
- Cung cấp đường dẫn Dockerfile
- Tag với tên và phiên bản phù hợp

**Bước 4: Chạy Docker Container**
```bash
docker run -d -p 8080:8080 eazybytes/accounts:s4
```
- Chỉ định port mapping
- Cung cấp tên image
- Container khởi động và chạy application

## Những Điểm Chính Cần Nhớ

1. **Lệnh Docker Run**: Tạo containers từ images (tương tự toán tử `new` trong Java)
2. **Port Mapping**: Cần thiết để truy cập containers từ mạng bên ngoài
3. **Detached Mode**: Sử dụng flag `-d` để chạy containers ở background
4. **Nhiều Containers**: Tạo không giới hạn instances từ một image
5. **Quản Lý Container**: Sử dụng lệnh `docker ps`, `docker start`, `docker stop`
6. **Docker Desktop**: Cung cấp GUI để quản lý container dễ dàng
7. **Lợi Ích**: Giải quyết các thách thức về deployment, portability và scalability

## Best Practices (Thực Hành Tốt Nhất)

1. Luôn chạy containers ở detached mode (`-d`) cho development
2. Sử dụng host ports duy nhất khi chạy nhiều containers
3. Giám sát containers bằng statistics của Docker Desktop
4. Dọn dẹp các stopped containers thường xuyên
5. Sử dụng port mappings có ý nghĩa để dễ nhận diện
6. Test containers kỹ lưỡng sau khi tạo

## Tham Chiếu Các Lệnh Thường Dùng

```bash
# Chạy container (detached mode)
docker run -d -p 8080:8080 eazybytes/accounts:s4

# Liệt kê running containers
docker ps

# Liệt kê tất cả containers
docker ps -a

# Khởi động container
docker start <container-id>

# Dừng container
docker stop <container-id>

# Xóa container
docker rm <container-id>

# Xem container logs
docker logs <container-id>

# Truy cập container terminal
docker exec -it <container-id> /bin/bash
```

---

**Lưu Ý**: Thực hành các lệnh này nhiều lần để xây dựng sự quen thuộc. Khi bạn làm việc với Docker nhiều hơn, các thao tác này sẽ trở nên trực quan và hiệu quả.