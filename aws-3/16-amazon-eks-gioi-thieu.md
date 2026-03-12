# Amazon EKS - Giới Thiệu

## Amazon EKS là gì?

Amazon EKS là viết tắt của **Amazon Elastic Kubernetes Service**. Đây là dịch vụ được quản lý cho phép bạn khởi chạy và quản lý các Kubernetes cluster trên AWS.

## Kubernetes là gì?

Kubernetes là một **hệ thống mã nguồn mở** dùng để tự động triển khai, mở rộng và quản lý các ứng dụng được đóng gói trong container (thường là Docker).

### Sự khác biệt chính so với ECS

- **ECS** không phải là mã nguồn mở và chỉ dành riêng cho AWS
- **Kubernetes** là mã nguồn mở và được sử dụng bởi nhiều nhà cung cấp đám mây khác nhau, mang lại sự chuẩn hóa
- Cả hai dịch vụ đều có mục tiêu tương tự là chạy container, nhưng với API rất khác nhau
- Kubernetes **độc lập với đám mây** và có thể được sử dụng trên bất kỳ đám mây nào (Azure, Google Cloud, v.v.)

## Chế độ khởi chạy EKS

Amazon EKS hỗ trợ hai chế độ khởi chạy:

1. **Chế độ EC2**: Triển khai worker nodes dưới dạng EC2 instances
2. **Chế độ Fargate**: Triển khai serverless containers trong EKS cluster

## Trường hợp sử dụng Amazon EKS

Sử dụng Amazon EKS khi công ty bạn:
- Đang sử dụng Kubernetes tại chỗ (on-premises)
- Đang sử dụng Kubernetes trên đám mây khác
- Muốn sử dụng Kubernetes API
- Muốn AWS quản lý Kubernetes cluster
- Cần di chuyển container giữa các đám mây một cách dễ dàng

## Kiến trúc EKS

Một triển khai EKS điển hình bao gồm:

- **VPC** với 3 Availability Zones
- **Public và private subnets** trong mỗi AZ
- **EKS Worker Nodes** (EC2 instances)
- **EKS Pods** chạy trên mỗi node (tương tự như ECS tasks)
- **Auto Scaling Group** để quản lý các nodes
- **Load Balancers** (private hoặc public) để expose EKS/Kubernetes services

## Các loại EKS Node

### 1. Managed Node Groups (Nhóm Node được Quản lý)
- AWS tạo và quản lý nodes (EC2 instances) cho bạn
- Nodes là một phần của Auto Scaling group được quản lý bởi dịch vụ EKS
- Hỗ trợ **On-Demand** và **Spot Instances**

### 2. Self-Managed Nodes (Nodes tự quản lý)
- Tùy chỉnh và kiểm soát nhiều hơn
- Bạn tự tạo các nodes
- Bạn đăng ký chúng vào EKS cluster
- Bạn quản lý các nodes của mình như một phần của ASG
- Có thể sử dụng **Amazon EKS Optimized AMI** có sẵn hoặc tự build AMI của riêng bạn
- Hỗ trợ **On-Demand** và **Spot Instances**

### 3. AWS Fargate
- Không cần bảo trì
- Không có nodes để quản lý
- Chỉ cần chạy containers trên Amazon EKS

## Data Volumes trong Amazon EKS

Bạn có thể gắn data volumes vào Amazon EKS cluster bằng cách:
- Chỉ định **StorageClass manifest** trên EKS cluster của bạn
- Tận dụng driver tuân thủ **Container Storage Interface (CSI)**

### Các loại Storage được hỗ trợ

- **Amazon EBS**
- **Amazon EFS** (loại storage duy nhất hoạt động với Fargate)
- **Amazon FSx for Lustre**
- **Amazon FSx for NetApp ONTAP**

## Điểm quan trọng cho kỳ thi

- EKS = Kubernetes được quản lý trên AWS
- Kubernetes độc lập với đám mây và là mã nguồn mở
- Hỗ trợ chế độ khởi chạy EC2 và Fargate
- Sử dụng EKS cho triển khai Kubernetes đa đám mây hoặc hybrid
- Tích hợp storage thông qua CSI driver
- EFS là tùy chọn storage duy nhất tương thích với Fargate