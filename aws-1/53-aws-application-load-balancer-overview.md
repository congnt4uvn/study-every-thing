# Tổng Quan về AWS Application Load Balancer (ALB)

## Lưu Ý: Về Classic Load Balancer (CLB)

Classic Load Balancer đã bị ngừng hỗ trợ tại AWS và sẽ sớm không còn khả dụng trong AWS Console. Kỳ thi cũng đã loại bỏ mọi tham chiếu đến nó, do đó nó sẽ không được đề cập sâu trong khóa học này hay các bài thực hành.

## Giới Thiệu về Application Load Balancer

Application Load Balancer (ALB) là loại load balancer thứ hai có sẵn trong AWS. Đây là một **load balancer chỉ hoạt động ở Layer 7 (HTTP)**, được thiết kế đặc biệt cho lưu lượng HTTP.

### Các Tính Năng Chính

- **Định Tuyến Đa Ứng Dụng**: Định tuyến lưu lượng đến nhiều ứng dụng HTTP trên nhiều máy
- **Target Groups (Nhóm Đích)**: Tổ chức các máy thành các nhóm logic gọi là target groups
- **Hỗ Trợ Container**: Cân bằng tải cho nhiều ứng dụng trên cùng một EC2 instance sử dụng container và ECS
- **Hỗ Trợ HTTP/2 và WebSocket**: Hỗ trợ đầy đủ các giao thức HTTP hiện đại
- **Chuyển Hướng Tự Động**: Có thể chuyển hướng lưu lượng từ HTTP sang HTTPS tại tầng load balancer

## Khả Năng Định Tuyến

ALB hỗ trợ định tuyến thông minh dựa trên nhiều tiêu chí khác nhau:

### 1. Định Tuyến Theo Đường Dẫn (Path-Based)
Định tuyến dựa trên đường dẫn URL:
- `example.com/users` → Target Group 1
- `example.com/posts` → Target Group 2

### 2. Định Tuyến Theo Hostname
Định tuyến dựa trên tên miền:
- `one.example.com` → Target Group 1
- `other.example.com` → Target Group 2

### 3. Định Tuyến Theo Query String và Header
Định tuyến dựa trên tham số truy vấn:
- `example.com/reserves?id=123&order=false` → Target Group cụ thể

## Trường Hợp Sử Dụng

ALB lý tưởng cho:
- **Kiến trúc microservices**
- **Ứng dụng dựa trên container** (Docker, ECS)
- **Tính năng ánh xạ cổng** để chuyển hướng cổng động trên các EC2 instance chạy ECS

### So Sánh với Classic Load Balancer

- **Classic Load Balancer**: Cần một load balancer cho mỗi ứng dụng
- **Application Load Balancer**: Một ALB có thể xử lý nhiều ứng dụng cùng lúc

## Ví Dụ Kiến Trúc: Microservices

```
External Application Load Balancer (Công khai)
    ↓
    ├── Target Group 1: route /user
    │   └── EC2 Instances (Ứng dụng User)
    │
    └── Target Group 2: route /search
        └── EC2 Instances (Ứng dụng Search)
```

Cả hai microservices hoạt động độc lập nhưng đều có thể truy cập thông qua cùng một ALB, ALB sẽ định tuyến các yêu cầu một cách thông minh dựa trên đường dẫn URL.

## Target Groups (Nhóm Đích)

Target groups có thể bao gồm:

1. **EC2 Instances** - Được quản lý bởi Auto Scaling Groups
2. **ECS Tasks** - Cho các ứng dụng container hóa
3. **Lambda Functions** - Nền tảng của serverless trong AWS
4. **Địa Chỉ IP** - Phải là địa chỉ IP private

ALB có thể định tuyến đến nhiều target groups, và các health check được thực hiện ở cấp độ target group.

## Ví Dụ Định Tuyến Nâng Cao: Kiến Trúc Hybrid

```
Application Load Balancer
    ↓
    ├── Target Group 1: ?Platform=Mobile
    │   └── EC2 Instances (AWS Cloud)
    │
    └── Target Group 2: ?Platform=Desktop
        └── Private Servers (On-Premises)
```

Trong ví dụ này:
- Lưu lượng mobile được định tuyến sử dụng query string `?Platform=Mobile` đến các EC2 instance trên cloud
- Lưu lượng desktop được định tuyến sử dụng query string `?Platform=Desktop` đến các máy chủ tại chỗ (được đăng ký bằng IP private)

## Những Điều Cần Lưu Ý

### Fixed Hostname (Tên Miền Cố Định)
- ALB cung cấp một hostname cố định (tương tự Classic Load Balancer)

### Bảo Toàn IP Của Client
Các application server không nhìn thấy trực tiếp IP của client. Thay vào đó, ALB sử dụng các header đặc biệt:

- **X-Forwarded-For**: Chứa địa chỉ IP thực của client
- **X-Forwarded-Port**: Chứa cổng của client
- **X-Forwarded-Proto**: Chứa giao thức được sử dụng (HTTP/HTTPS)

### Quy Trình Connection Termination

```
Client (12.34.56.78)
    ↓ [Connection Termination]
Load Balancer (Private IP)
    ↓
EC2 Instance
```

1. Client kết nối đến load balancer với IP công khai của họ (ví dụ: 12.34.56.78)
2. Load balancer ngắt kết nối (terminate connection)
3. Load balancer tạo kết nối mới đến EC2 instance sử dụng IP private của nó
4. EC2 instance đọc IP gốc của client từ header `X-Forwarded-For`

## Tóm Tắt

Application Load Balancer là một load balancer Layer 7 mạnh mẽ, xuất sắc trong việc định tuyến lưu lượng HTTP trong các kiến trúc phân tán hiện đại. Khả năng định tuyến nâng cao, hỗ trợ nhiều loại target khác nhau, và tích hợp liền mạch với các dịch vụ container và serverless khiến nó trở thành lựa chọn ưu tiên cho các ứng dụng microservices và cloud-native.