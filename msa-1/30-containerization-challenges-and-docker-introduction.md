# Thách Thức Containerization và Giới Thiệu Docker

## Tổng Quan

Bài giảng này cung cấp giới thiệu toàn diện về containers, Docker và các khái niệm containerization - những công nghệ thiết yếu cho các nhà phát triển microservice làm việc với ứng dụng Java và Spring Boot.

## Container là gì?

**Container** là một môi trường được cách ly lỏng lẻo có thể tồn tại trong:
- Một server
- Một máy ảo (virtual machine)
- Hệ thống local của bạn

Containers cho phép bạn triển khai microservices bằng cách sử dụng **các gói phần mềm** bao gồm:
- Tất cả mã nguồn
- Tất cả các dependencies
- Mọi thứ cần thiết để chạy ứng dụng hoặc microservices một cách nhanh chóng và đáng tin cậy

### Lợi Ích Chính

- **Tính Nhất Quán Môi Trường**: Containers hoạt động giống nhau trên các môi trường computing khác nhau (hệ thống local, VMs trong data center, VMs trên cloud)
- **Không Cần Cài Đặt Thủ Công**: Không cần phải cài đặt dependencies hoặc cấu hình servers thủ công
- **Tính Di Động**: Cùng một container có thể được triển khai trên nhiều môi trường mà không cần sửa đổi

## Container Images

**Container images** (hoặc Docker images) là các gói phần mềm chứa tất cả dependencies và libraries cần thiết.

### So Sánh Image và Container

Hãy nghĩ về mối quan hệ giống như Java classes và objects:
- **Container Image** = Java Class (bộ khung/đại diện)
- **Container** = Java Object (thực thể đang chạy thực tế)

Giống như bạn có thể tạo nhiều objects từ một Java class, bạn có thể tạo nhiều containers từ một container image.

> Docker container là một đại diện đang chạy thực tế của Docker image.

## Software Containerization là gì?

**Software containerization** là một phương pháp ảo hóa hệ điều hành (OS virtualization):
- Triển khai nhiều containers trong một máy đơn lẻ hoặc máy ảo
- Cung cấp môi trường cách ly ảo cho mỗi container
- Làm cho mỗi container cảm thấy như đang chạy trong hệ điều hành riêng của nó

### Containerization vs Ảo Hóa Truyền Thống

| Khía Cạnh | Containerization | Virtual Machines (Hypervisor) |
|-----------|------------------|------------------------------|
| **Mức Độ Ảo Hóa** | Hệ điều hành | Phần cứng |
| **Chia Sẻ Tài Nguyên** | Chia sẻ kernel của host OS | Các OS instances riêng biệt |
| **Cách Ly** | Ảo hóa cấp độ OS | Ảo hóa cấp độ phần cứng |

#### Ảo Hóa Truyền Thống (Hypervisor)
- Ảo hóa các máy
- VMs cảm thấy như đang chạy trên phần cứng vật lý khác nhau
- Mỗi VM có OS instance riêng

#### Containerization
- Ảo hóa hệ điều hành
- Tất cả containers chia sẻ cùng kernel của host operating system
- Mỗi container cảm thấy như có OS riêng biệt

## Docker là gì?

**Docker** là một nền tảng mã nguồn mở:
- Cho phép developers chuyển đổi ứng dụng thành Docker images
- Tự động hóa việc triển khai, mở rộng và quản lý ứng dụng
- Triển khai công nghệ containerization

### Mối Quan Hệ Các Khái Niệm Chính

1. **Software Containerization** = Khái niệm
2. **Docker** = Nền tảng triển khai containerization
3. **Docker Images & Containers** = Được tạo ra từ mã nguồn ứng dụng bằng Docker

## Cách Containerization Hoạt Động

Containers dựa trên ảo hóa hệ điều hành, trong đó nhiều containers:
- Chạy trên cùng một máy vật lý hoặc máy ảo
- Chia sẻ cùng kernel của hệ điều hành
- Khác với VMs truyền thống chạy các OS instances riêng biệt

### Các Tính Năng Linux: Namespaces và Cgroups

Docker containerization dựa vào hai tính năng quan trọng của Linux:

#### 1. Namespaces

**Mục đích**: Cung cấp cách ly (isolation)

Namespaces cho phép tạo môi trường cách ly trong cùng một hệ điều hành. Mỗi container có bộ namespaces riêng chứa:
- Tài nguyên **Process** (tiến trình)
- Tài nguyên **Network** (mạng)
- Tài nguyên **Storage** (lưu trữ)
- Tài nguyên **Communication** (giao tiếp)
- **User** namespaces

**Kết quả**: Các tiến trình trong container chỉ có thể tương tác với tài nguyên trong namespace riêng của chúng, cung cấp sự cách ly với các containers khác.

#### 2. Cgroups (Control Groups)

**Mục đích**: Kiểm soát việc sử dụng tài nguyên

Trong khi namespaces cung cấp cách ly, cgroups kiểm soát lượng tài nguyên mà container có thể sử dụng:
- Phân bổ **CPU**
- Phân bổ **Memory** (bộ nhớ)
- Sử dụng **Disk** (đĩa)
- Băng thông **Network** (mạng)

**Lợi ích**:
- Thực thi giới hạn tài nguyên tại runtime
- Ngăn một container chiếm dụng tài nguyên hệ thống
- Đảm bảo phân bổ công bằng giữa nhiều containers
- Tránh tình huống các containers nhận phân bổ tài nguyên không công bằng

## Docker trên Các Hệ Điều Hành Khác Nhau

### Docker trên Linux
- Cài đặt đơn giản
- Nhận toàn bộ Docker engine trực tiếp trên Linux OS

### Docker trên macOS hoặc Windows
Cài đặt bao gồm hai thành phần:

1. **Docker Client** (CLI)
   - Được cài đặt trên host OS của bạn (Mac hoặc Windows)
   - Cung cấp giao diện người dùng

2. **Docker Server**
   - Được cài đặt trong một máy ảo Linux nhẹ
   - Chạy ẩn phía sau
   - Cung cấp Docker engine thực tế

**Kết quả**: Docker hoạt động nhất quán trên tất cả các hệ điều hành, cung cấp giao diện tương tự bất kể host OS là gì.

### Xác Minh: Lệnh Docker Version

Chạy `docker version` để xem kiến trúc:

```bash
docker version
```

**Ví dụ Output**:
- **Client**: Hiển thị host OS của bạn (ví dụ: Darwin/arm64 cho Mac, Windows cho Windows OS)
- **Server**: Hiển thị Linux (vì nó chạy trong Linux VM nhẹ)

Điều này xác nhận kiến trúc hai thành phần trên các hệ thống không phải Linux.

## Tóm Tắt

Các khái niệm chính đã được đề cập:
- **Container**: Môi trường cách ly lỏng lẻo để triển khai microservices
- **Containerization**: Phương pháp ảo hóa OS để chạy nhiều containers cách ly
- **Docker**: Nền tảng mã nguồn mở triển khai công nghệ containerization
- **Namespaces**: Cung cấp cách ly tài nguyên cho containers
- **Cgroups**: Kiểm soát và quản lý việc sử dụng tài nguyên của containers

## Các Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ khám phá kiến trúc nội bộ của Docker để hiểu cách các thành phần này hoạt động cùng nhau.

---

*Tài liệu này là một phần của khóa học microservices về Spring Boot, Java và các công nghệ containerization.*