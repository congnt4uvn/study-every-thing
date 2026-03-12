# Tổng quan về Amazon ECS

## Giới thiệu

Amazon ECS (Elastic Container Service) là một dịch vụ điều phối container toàn diện trên AWS cho phép bạn khởi chạy và quản lý các Docker container. Hướng dẫn này cung cấp tổng quan về tất cả các khía cạnh khác nhau của Amazon ECS.

## Các kiểu khởi chạy ECS

### Kiểu khởi chạy EC2

Khi bạn khởi chạy Docker container trên AWS bằng ECS, bạn đang khởi chạy một **ECS Task** trên **ECS Cluster**.

**Đặc điểm chính:**
- ECS Cluster được cấu tạo từ các EC2 instance
- Bạn phải **tự cung cấp và duy trì hạ tầng**
- Mỗi EC2 instance phải chạy **ECS Agent**
- ECS Agent đăng ký từng EC2 instance vào dịch vụ Amazon ECS và ECS Cluster được chỉ định

**Cách hoạt động:**
1. Sau khi có hạ tầng, bạn có thể bắt đầu các ECS task
2. AWS tự động khởi động hoặc dừng các container
3. Docker container được đặt trên các EC2 instance theo thời gian
4. Bạn có thể khởi động hoặc dừng ECS task, và chúng sẽ được đặt tự động
5. Docker container được đặt trên các Amazon EC2 instance mà bạn cung cấp trước

### Kiểu khởi chạy Fargate

Kiểu khởi chạy Fargate cung cấp cách tiếp cận **serverless** để chạy container.

**Đặc điểm chính:**
- Bạn **không cung cấp hạ tầng** - không có EC2 instance để quản lý
- Hoàn toàn serverless (mặc dù vẫn có server ở backend)
- Bạn chỉ cần tạo task definition để định nghĩa ECS task
- AWS chạy các ECS task dựa trên yêu cầu về CPU và RAM

**Lợi ích:**
- Không cần biết container đang chạy ở đâu
- Không có EC2 instance được tạo trong tài khoản của bạn
- Để mở rộng, chỉ cần tăng số lượng task
- Không cần quản lý EC2 instance
- **Được khuyến nghị trong các kỳ thi** - Fargate là serverless và dễ quản lý hơn kiểu EC2

## IAM Role cho ECS Task

### EC2 Instance Profile

**Áp dụng cho:** Chỉ kiểu khởi chạy EC2

**Mục đích:** Được sử dụng bởi ECS Agent để:
- Thực hiện API call đến dịch vụ ECS để đăng ký instance
- Gửi log container đến CloudWatch Logs
- Pull Docker image từ ECR (Elastic Container Registry)
- Tham chiếu dữ liệu nhạy cảm trong Secrets Manager hoặc SSM Parameter Store

### ECS Task Role

**Áp dụng cho:** Cả kiểu khởi chạy EC2 và Fargate

**Tính năng chính:**
- Bạn có thể tạo một **role cụ thể cho mỗi task**
- Mỗi role liên kết với các dịch vụ ECS khác nhau
- Được định nghĩa trong task definition của dịch vụ ECS

**Ví dụ:**
- **Task A** với ECS Task A Role: Thực hiện API call đến Amazon S3
- **Task B** với ECS Task B Role: Thực hiện API call đến DynamoDB

**Quan trọng:** Nhớ sự phân biệt giữa EC2 Instance Profile Role và ECS Task Role.

## Tích hợp Load Balancer

ECS task có thể được expose như các endpoint HTTP hoặc HTTPS bằng cách sử dụng load balancer.

### Application Load Balancer (ALB)
- **Được hỗ trợ và khuyến nghị** cho hầu hết các trường hợp sử dụng
- Hoạt động với cả kiểu khởi chạy EC2 và Fargate
- Người dùng kết nối đến ALB, ALB định tuyến traffic đến ECS task

### Network Load Balancer (NLB)
- Chỉ được khuyến nghị cho:
  - Các tình huống throughput rất cao
  - Các trường hợp sử dụng hiệu suất cao
  - Sử dụng với AWS Private Link

### Classic Load Balancer
- **Không được khuyến nghị**
- Không có tính năng nâng cao
- **Không thể liên kết với Fargate**

## Lưu trữ dữ liệu bền vững trên Amazon ECS

### Amazon EFS (Elastic File System)

Để lưu trữ dữ liệu bền vững giữa các ECS task, sử dụng **Data Volume** với Amazon EFS.

**Kiến trúc:**
- Mount hệ thống file Amazon EFS lên ECS task
- Tương thích với cả kiểu khởi chạy **EC2 và Fargate**
- Hệ thống file mạng cho phép mount trực tiếp vào ECS task

**Lợi ích:**
- Các task chạy trong **bất kỳ AZ nào** đều có thể chia sẻ cùng dữ liệu
- Cho phép giao tiếp giữa các task thông qua hệ thống file
- Khả năng lưu trữ chia sẻ đa AZ

### Sự kết hợp hoàn hảo

**Fargate + Amazon EFS** = Giải pháp container serverless lý tưởng

- **Fargate:** Khởi chạy container serverless
- **Amazon EFS:** Hệ thống file serverless
- Cả hai đều là dịch vụ trả tiền theo mức sử dụng
- Không cần quản lý server
- Chỉ cần cung cấp và sử dụng

**Các trường hợp sử dụng:**
- Lưu trữ chia sẻ bền vững đa AZ cho container
- Chia sẻ dữ liệu giữa nhiều ECS task
- Ứng dụng container serverless yêu cầu lưu trữ bền vững

## Tổng kết

Amazon ECS cung cấp điều phối container linh hoạt với hai kiểu khởi chạy:
- **Kiểu khởi chạy EC2:** Kiểm soát hoàn toàn với quản lý hạ tầng thủ công
- **Kiểu khởi chạy Fargate:** Cách tiếp cận serverless, không cần can thiệp (được ưu tiên)

Kết hợp với IAM role phù hợp, tích hợp load balancer, và Amazon EFS cho tính bền vững, ECS cung cấp một giải pháp hoàn chỉnh để chạy các ứng dụng container trên AWS.