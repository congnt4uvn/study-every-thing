# Kiến Trúc và Các Thành Phần Docker

## Tổng Quan

Bài giảng này giải thích các thành phần quan trọng có sẵn trong Docker và kiến trúc nội bộ của nó. Hiểu về kiến trúc Docker là rất quan trọng để container hóa các microservices được xây dựng bằng Spring Boot và Java.

## Các Thành Phần Docker

### 1. Docker Client

Docker client là giao diện chính để tương tác với Docker. Khi bạn cài đặt Docker trên bất kỳ hệ thống nào, bạn sẽ nhận được cả Docker client và Docker server.

Docker client được sử dụng để đưa ra các chỉ thị cho Docker server về cách container hóa ứng dụng.

#### Các Thành Phần của Docker Client:

**Docker CLI (Command Line Interface)**
- Cách tiếp cận phổ biến nhất để đưa ra lệnh cho Docker server
- Cho phép bạn đưa ra lệnh trực tiếp từ terminal hoặc command line
- Tương tự như GitHub CLI hoặc các công cụ CLI khác được cung cấp bởi nhiều sản phẩm
- Đây là cách tiếp cận chúng ta sẽ sử dụng trong khóa học này

**Docker Remote API**
- Một cách thay thế để đưa ra lệnh cho Docker server bằng cách sử dụng APIs
- Có thể được sử dụng để thực thi các lệnh như chạy một Docker container từ Docker image
- Cung cấp quyền truy cập theo chương trình vào chức năng Docker

### 2. Docker Server (Docker Host)

Docker server, còn được gọi là Docker host, là thành phần cốt lõi thực hiện công việc thực tế.

**Lưu Ý Quan Trọng:**
- Cả Docker client và Docker server đều được cài đặt trên cùng một hệ thống (máy local của bạn)
- Đừng nhầm lẫn với việc cài đặt trên server từ xa

#### Docker Daemon

Docker server chạy một tiến trình Docker daemon mà:
- Chạy liên tục trong nền
- Chấp nhận các lệnh từ client (CLI)
- Xử lý các chỉ thị để tạo Docker images và containers

#### Docker Images

Docker image là một đại diện được đóng gói của ứng dụng của bạn bao gồm:
- Tất cả các dependencies cần thiết
- Cài đặt cấu hình
- Phiên bản Java và runtime
- Mã nguồn ứng dụng

Khi bạn cung cấp các chỉ thị cho Docker server (dependencies, phiên bản Java, cấu hình), nó sẽ chuyển đổi ứng dụng Spring Boot, ứng dụng Maven hoặc microservice của bạn thành một Docker image.

#### Docker Containers

Containers là các instance đang chạy của Docker images:
- Không thể tạo được nếu không có Docker image
- Đại diện cho ứng dụng web hoặc microservice của bạn ở trạng thái đang chạy
- Khi container đang chạy, bạn có thể truy cập các REST APIs và logic nghiệp vụ microservice thông qua endpoint URL bằng cách sử dụng đúng số port và đường dẫn API

**Lưu Trữ:**
Tất cả images và containers được lưu trữ bên trong Docker server của bạn.

### 3. Docker Registry

Docker Registry là một hệ thống repository để lưu trữ và phân phối Docker images.

#### Docker Hub

Docker Hub là registry chính thức được cung cấp bởi Docker:
- Lưu trữ tất cả Docker images của bạn
- Làm cho images có sẵn để sử dụng công khai
- Bảo vệ images bằng xác thực cho quyền truy cập riêng tư
- Tương tự như cách GitHub lưu trữ mã nguồn

#### Private Registries

Nhiều nhà cung cấp đám mây và nền tảng cung cấp private registries:
- **GitHub** - GitHub Container Registry
- **AWS** - Amazon Elastic Container Registry (ECR)
- **GCP** - Google Container Registry
- **Azure** - Azure Container Registry

**Trường Hợp Sử Dụng:**
Nếu tổ chức của bạn sử dụng rộng rãi AWS, việc đẩy Docker images lên private registry của AWS (ECR) là hợp lý, từ đó tất cả các triển khai microservice sẽ diễn ra.

**Trong Khóa Học Này:**
Chúng ta sẽ sử dụng Docker Hub để lưu trữ tất cả Docker images.

## Quy Trình Làm Việc Docker

Đây là quy trình điển hình khi làm việc với Docker:

### Bước 1: Đưa Ra Chỉ Thị
Đưa ra chỉ thị cho Docker server bằng cách sử dụng Docker client (CLI), chẳng hạn như "chạy một container từ một Docker image."

### Bước 2: Xác Thực Image
Docker server xác thực xem Docker image có sẵn trong hệ thống local của bạn hay không.

### Bước 3: Truy Xuất Image
Nếu image không có sẵn locally, Docker sẽ lấy nó từ một repository từ xa như Docker Hub.

### Bước 4: Tạo Container
Khi Docker image đã được kéo về hệ thống local của bạn, một container được tạo bởi Docker server bằng cách sử dụng image đó.

### Bước 5: Ứng Dụng Sẵn Sàng
Khi container đang chạy, ứng dụng của bạn đã sẵn sàng để sử dụng.

## Ví Dụ Thực Tế: MySQL với Docker

**Cách Tiếp Cận Truyền Thống:**
1. Truy cập website MySQL
2. Tải xuống gói cài đặt MySQL
3. Cài đặt trên hệ thống của bạn
4. Cấu hình cơ sở dữ liệu

Đây là một quá trình rườm rà và dài dòng.

**Cách Tiếp Cận Docker:**
1. Kéo MySQL image từ Docker Hub
2. Chạy một container từ MySQL image
3. MySQL server hiện đang chạy trên hệ thống của bạn

Điều này đơn giản hóa đáng kể quá trình thiết lập.

## Quy Trình Triển Khai

Sau khi bạn đã phát triển và kiểm tra microservice của mình locally:

1. **Tạo** một Docker image cho microservice của bạn
2. **Kiểm tra** image bằng cách tạo và chạy một container
3. **Xác minh** rằng mọi thứ hoạt động chính xác
4. **Đẩy** Docker image lên một repository từ xa (Docker Hub)
5. **Triển khai** từ repository đến môi trường dev, staging hoặc production

Quy trình này tương tự như cách bạn lưu trữ mã Java trong repositories GitHub - Docker images được lưu trữ trong Docker registries cho mục đích triển khai.

## Tóm Tắt

Kiến trúc Docker bao gồm ba thành phần chính:

1. **Docker Client** - Giao diện để đưa ra lệnh (CLI hoặc Remote API)
2. **Docker Server** - Công cụ cốt lõi tạo và quản lý images và containers
3. **Docker Registry** - Hệ thống repository để lưu trữ và phân phối images

Hiểu kiến trúc này là điều cần thiết cho:
- Container hóa các Spring Boot microservices
- Quản lý triển khai ứng dụng
- Đơn giản hóa môi trường phát triển và production
- Đảm bảo tính nhất quán trên các môi trường khác nhau

## Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ đề cập đến cách cài đặt Docker trên hệ thống local của bạn và bắt đầu tạo Docker images cho các microservices của bạn.

---

**Điểm Chính Cần Nhớ:**
- Docker Client cung cấp giao diện CLI và API cho các lệnh
- Docker Server (Docker Host) quản lý images và containers thông qua Docker daemon
- Docker Registry (Docker Hub hoặc private registries) lưu trữ và phân phối images
- Containers là các instance đang chạy của images
- Docker đơn giản hóa triển khai và tính nhất quán của môi trường