# Sử Dụng AWS CLI để Đẩy và Kéo Images vào Amazon ECR

## Tổng Quan

Hướng dẫn này trình bày cách sử dụng AWS CLI và Docker CLI để kéo (pull) và đẩy (push) images vào Amazon Elastic Container Registry (ECR). Bạn sẽ học cách xác thực với ECR, đẩy images từ Docker Hub vào kho ECR riêng tư của mình, và sử dụng các images đó trong ECS tasks.

## Yêu Cầu Trước Khi Bắt Đầu

- Docker đã được cài đặt và đang chạy trên máy tính của bạn
- AWS CLI đã được cấu hình với thông tin xác thực phù hợp
- Quyền IAM để truy cập Amazon ECR

## Xác Thực với Amazon ECR

### Lệnh Đăng Nhập

Để xác thực Docker CLI của bạn với Amazon ECR, bạn cần sử dụng lệnh đăng nhập AWS ECR:

```bash
aws ecr get-login-password | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region>.amazonaws.com
```

**Cách thức hoạt động:**
- Lệnh `aws ecr get-login-password` tạo ra một mật khẩu tạm thời
- Mật khẩu này được truyền vào lệnh `docker login`
- Docker CLI bây giờ đã được xác thực để kết nối với kho lưu trữ riêng tư của bạn trên AWS

Sau khi xác thực thành công, bạn sẽ thấy: `login succeeded`

## Các Lệnh Docker Cơ Bản cho ECR

### Đẩy Image

```bash
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/<image-name>:<tag>
```

### Kéo Image

```bash
docker pull <account-id>.dkr.ecr.<region>.amazonaws.com/<image-name>:<tag>
```

**Lưu ý:** Nếu bạn không thể đẩy hoặc kéo Docker images, hãy kiểm tra xem bạn có quyền IAM phù hợp hay không.

## Demo Thực Hành: Di Chuyển Image từ Docker Hub sang ECR

### Bước 1: Tạo Kho ECR Riêng Tư

1. Điều hướng đến Amazon ECR trong AWS Console
2. Nhấp "Create repository"
3. Chọn "Private repository"
4. Đặt tên cho kho của bạn (ví dụ: `demostephane`)

### Các Tùy Chọn Cấu Hình Kho

- **Tag Immutability**: Ngăn chặn đẩy cùng một tag hai lần
- **Image Scan**: Quét images khi đẩy để tìm các vấn đề bảo mật (đã ngừng sử dụng - nên dùng Amazon Inspector)
- **Registry Level Scan Filters**: Sử dụng Amazon Inspector để quét bảo mật tốt hơn
- **Encryption**: Tùy chọn mã hóa kho ECR của bạn với KMS

### Bước 2: Kiểm Tra Cài Đặt Docker

Kiểm tra xem Docker có đang chạy không:

```bash
docker version
```

### Bước 3: Xác Thực với ECR

Chạy lệnh đăng nhập ECR (lệnh khác nhau cho Mac/Linux và Windows):

**Mac/Linux:**
```bash
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region>.amazonaws.com
```

**Windows:**
Kiểm tra phần "Push commands" trong ECR console để xem lệnh dành cho Windows.

### Bước 4: Kéo Image từ Docker Hub

Kéo image mẫu từ Docker Hub:

```bash
docker pull nginxdemos/hello
```

**Hiểu về Nguồn:**
- Image này đến từ hub.docker.com
- Khi được sử dụng trong ECS task definitions, các EC2 instances sẽ kéo trực tiếp từ Docker Hub
- Chúng ta đang chuyển nó sang ECR để lưu trữ riêng tư

### Bước 5: Gắn Tag cho Image cho ECR

Đổi tên image để khớp với kho ECR của bạn:

```bash
docker tag nginxdemos/hello:latest <account-id>.dkr.ecr.<region>.amazonaws.com/demostephane:latest
```

Điều này tạo một tag mới trỏ đến cùng một image, được định dạng cho kho ECR của bạn.

### Bước 6: Đẩy lên ECR

Đẩy image đã được gắn tag vào kho ECR của bạn:

```bash
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/demostephane:latest
```

Image sẽ được tải lên AWS. Điều này hoạt động vì bạn đã được xác thực với kho ECR của mình. Nếu không có xác thực phù hợp, bạn sẽ nhận được lỗi quyền IAM.

### Bước 7: Xác Minh trong ECR Console

1. Làm mới trang kho ECR của bạn
2. Bạn sẽ thấy image `latest` trong kho `demostephane` của mình
3. Nhấp vào image để xem thông tin chi tiết

## Kho Công Khai vs Kho Riêng Tư

- **Kho Công Khai**: Cho phép bất kỳ ai kéo images của bạn
- **Kho Riêng Tư**: Yêu cầu quyền IAM phù hợp để kéo images

## Sử Dụng ECR Images trong ECS Task Definitions

Sau khi image của bạn có trong ECR, bạn có thể:
1. Tạo hoặc cập nhật ECS task definition
2. Tham chiếu đến image ECR của bạn thay vì Docker Hub
3. ECS sẽ kéo image trực tiếp từ ECR

Điều này cung cấp khả năng kiểm soát, bảo mật tốt hơn và có khả năng kéo nhanh hơn trong mạng AWS.

## Xử Lý Sự Cố

### Không Thể Đẩy hoặc Kéo Images

**Vấn đề:** Lỗi từ chối quyền khi đẩy hoặc kéo images

**Giải pháp:** Xác minh rằng:
- IAM user/role của bạn có các quyền ECR cần thiết
- Bạn đã xác thực thành công bằng lệnh đăng nhập
- Token xác thực của bạn chưa hết hạn (tokens là tạm thời)

### Lệnh Đăng Nhập Thất Bại

**Vấn đề:** Không thể xác thực với ECR

**Giải pháp:** 
- Đảm bảo AWS CLI được cấu hình đúng
- Kiểm tra thông tin xác thực AWS của bạn
- Xác minh quyền IAM của bạn bao gồm quyền truy cập ECR

## Tóm Tắt

Trong hướng dẫn này, bạn đã học cách:
- Xác thực Docker CLI với Amazon ECR
- Tạo kho ECR riêng tư
- Kéo images từ Docker Hub
- Gắn tag và đẩy images vào ECR
- Sử dụng ECR images trong ECS task definitions

Sử dụng Amazon ECR cho container images của bạn cung cấp bảo mật, kiểm soát và tích hợp tốt hơn với các dịch vụ AWS so với việc sử dụng các registry công khai như Docker Hub.