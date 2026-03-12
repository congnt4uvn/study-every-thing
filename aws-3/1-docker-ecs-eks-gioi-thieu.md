# Giới thiệu về Docker, ECS và EKS trên AWS

## Tổng quan

Chào mừng đến với phần này về containers, nơi chúng ta sẽ thảo luận về Docker, Amazon ECS (Elastic Container Service), và Amazon EKS (Elastic Kubernetes Service).

## Docker là gì?

Docker là một nền tảng phát triển phần mềm được thiết kế để triển khai ứng dụng sử dụng công nghệ container. Các đặc điểm chính bao gồm:

- **Container hóa**: Ứng dụng được đóng gói thành các container chuẩn hóa
- **Tính di động**: Container có thể chạy trên bất kỳ hệ điều hành nào
- **Tính nhất quán**: Ứng dụng chạy giống nhau bất kể môi trường nào
- **Không có vấn đề tương thích**: Loại bỏ các vấn đề đặc thù từng máy
- **Hành vi có thể dự đoán**: Giảm công việc bảo trì
- **Triển khai dễ dàng**: Đơn giản hóa quá trình bảo trì và triển khai
- **Độc lập công nghệ**: Hoạt động với bất kỳ ngôn ngữ lập trình, hệ điều hành hoặc công nghệ nào

### Các trường hợp sử dụng Docker

- **Kiến trúc microservice**: Lý tưởng để xây dựng hệ thống phân tán
- **Lift and shift**: Di chuyển ứng dụng từ on-premises lên cloud
- **Workload container**: Bất kỳ tình huống nào yêu cầu ứng dụng container hóa

## Docker hoạt động như thế nào trên hệ điều hành

Docker chạy trên các server (chẳng hạn như EC2 instances) với Docker agent được cài đặt. Từ đó, bạn có thể khởi động nhiều Docker container:

- **Ứng dụng Java** trong Docker container
- **Ứng dụng Node.js** trong Docker container
- **Cơ sở dữ liệu** (ví dụ: MySQL) trong Docker container
- Nhiều phiên bản của cùng một ứng dụng

Từ góc độ server, tất cả những thứ này đều là Docker container được quản lý bởi Docker agent.

## Lưu trữ Docker Image - Docker Repository

### Docker Hub
- Repository công khai
- Chứa base image cho nhiều công nghệ và hệ điều hành (Ubuntu, MySQL, v.v.)
- Registry Docker phổ biến nhất

### Amazon ECR (Elastic Container Registry)
- **Repository riêng tư**: Cho các image độc quyền của bạn
- **Amazon ECR Public Gallery**: Tùy chọn repository công khai trên AWS

## Docker so với Máy ảo (Virtual Machines)

Docker là một công nghệ ảo hóa, nhưng khác với VM truyền thống:

### Kiến trúc Máy ảo
```
Cơ sở hạ tầng
└── Hệ điều hành máy chủ
    └── Hypervisor
        └── Guest OS + Ứng dụng
```

- Ví dụ: EC2 instances chạy như VM trên hypervisor
- Cách ly hoàn toàn giữa các VM
- Không chia sẻ tài nguyên
- Riêng biệt cho từng khách hàng

### Kiến trúc Docker Container
```
Cơ sở hạ tầng
└── Hệ điều hành máy chủ (ví dụ: EC2 instance)
    └── Docker Daemon
        └── Nhiều container nhẹ
```

- **Chia sẻ tài nguyên**: Container chia sẻ tài nguyên với máy chủ
- **Cùng tồn tại**: Nhiều container trên một server duy nhất
- **Networking**: Container có thể chia sẻ mạng
- **Chia sẻ dữ liệu**: Container có thể chia sẻ dữ liệu
- **Hiệu quả**: Chạy nhiều container hơn trên mỗi server
- **Đánh đổi bảo mật**: Ít cách ly hơn VM, nhưng hiệu quả hơn

## Bắt đầu với Docker

Quy trình làm việc với Docker bao gồm:

1. **Viết Dockerfile**: Định nghĩa cách container của bạn sẽ được xây dựng
2. **Build Docker Image**: 
   - Bắt đầu với base Docker image
   - Thêm các file của bạn
   - Build image
3. **Push lên Repository**: 
   - Tải lên (push) Docker Hub (công khai) hoặc Amazon ECR (riêng tư)
4. **Pull từ Repository**: Tải xuống image khi cần
5. **Run Docker Image**: Khi chạy, nó trở thành Docker container thực thi code của bạn

## Quản lý Docker Container trên AWS

### Amazon ECS (Elastic Container Service)
- Nền tảng riêng của Amazon để quản lý Docker
- Dịch vụ điều phối container gốc của AWS

### Amazon EKS (Elastic Kubernetes Service)
- Dịch vụ Kubernetes được quản lý bởi Amazon
- Điều phối container mã nguồn mở
- Giải pháp tiêu chuẩn ngành

### AWS Fargate
- Nền tảng container serverless của Amazon
- Hoạt động với cả ECS và EKS
- Không cần quản lý server

### Amazon ECR (Elastic Container Registry)
- Lưu trữ container image
- Tích hợp liền mạch với ECS và EKS

## Tóm tắt

Phần này đã đề cập:
- Docker là gì và lợi ích của nó
- Cách Docker hoạt động trên AWS
- Docker so với Máy ảo
- Quy trình làm việc và repository của Docker
- Các dịch vụ quản lý container của AWS (ECS, EKS, Fargate, ECR)

Tiếp theo, chúng ta sẽ tìm hiểu sâu về Amazon ECS và khám phá chi tiết các dịch vụ này.