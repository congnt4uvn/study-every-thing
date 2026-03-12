# Tạo Amazon ECS Cluster Đầu Tiên

## Tổng Quan

Hướng dẫn này sẽ giúp bạn từng bước tạo Amazon ECS (Elastic Container Service) cluster đầu tiên và hiểu về các tùy chọn capacity provider khác nhau.

## Tạo ECS Cluster

### Bước 1: Điều Hướng Đến ECS Clusters

1. Trong AWS Console, nhấp vào **Clusters** ở menu bên trái
2. Nhấp vào **Create cluster**

### Bước 2: Cấu Hình Cluster

**Tên Cluster**: Chọn bất kỳ tên nào bạn muốn (ví dụ: `DemoCluster`)

### Bước 3: Lựa Chọn Infrastructure

Trong phần Infrastructure, bạn cần chọn cách để có được capacity. AWS cung cấp một số tùy chọn:

#### Tùy Chọn 1: Fargate Only (Serverless)
- Phương pháp hoàn toàn serverless
- Bạn không cần quan tâm đến servers
- AWS cung cấp và quản lý infrastructure cho bạn

#### Tùy Chọn 2: Fargate and Managed Instances
- Kết hợp Fargate với EC2 instances do AWS quản lý
- AWS quản lý các EC2 instances ở phía sau
- Bạn cần tạo một instance profile

#### Tùy Chọn 3: Fargate and Self-managed Instances (Cũ)
- Phương pháp cũ, bạn tự quản lý EC2 instances
- Yêu cầu tạo auto-scaling group
- Bạn phải chọn loại AMI và loại EC2 instance
- AWS đang chuyển dần khỏi tùy chọn này

## Thiết Lập Managed Instances

### Tạo Các IAM Roles Cần Thiết

#### Instance Profile Role

1. Nhấp vào **Create new instance profile**
2. Chọn **EC2 Role for ECS Managed Instances**
3. Nhấp **Next**
4. Đặt tên là `ecsInstanceRole`
5. Nhấp **Create role**

#### Infrastructure Role

1. Tạo một infrastructure role mới
2. Chọn **Infrastructure for ECS Managed Instances**
3. Nhấp **Next** và tạo role

### Lựa Chọn Instance

Bạn có hai tùy chọn để chọn instance:

#### ECS Default (Khuyến Nghị Cho Production)
- AWS chọn instances dựa trên task definition và service requirements
- Tự động tối ưu hóa cho workload của bạn

#### Custom Configuration
- Tự chỉ định yêu cầu vCPU và memory (min/max)
- Có thể bắt buộc các loại instance cụ thể (ví dụ: chỉ `t3.micro`)
- Ví dụ: Đặt **Allowed instance type** thành `t3.micro` để giới hạn chỉ loại instance đó

### Cấu Hình Self-managed Instances

Để demo, bạn cũng có thể sử dụng self-managed instances:

- Tạo một **auto-scaling group** mới (on-demand)
- Loại instance: `t3.micro`
- Sử dụng default role cho EC2 instance role
- Capacity tối đa: 2 instances
- Không cần SSH access
- Kích thước root EBS volume: 30 GB
- Để network settings mặc định
- Nhấp **Create**

## Hiểu Về Auto Scaling Groups

Sau khi tạo cluster, một Auto Scaling Group được tự động tạo:

- Tên: `Infra-ECS-Cluster`
- Capacity ban đầu: 0
- Min capacity: 0
- Max capacity: 5
- Trải rộng trên 3 Availability Zones (AZs)

Điều này đảm bảo các ECS tasks của bạn sẽ được khởi chạy trên nhiều AZs để đạt tính sẵn sàng cao.

## Khám Phá ECS Cluster

### Bảng Điều Khiển Cluster

Khi cluster được tạo, bạn có thể khám phá nó:

- **Services**: Hiển thị số lượng services đang chạy (ban đầu là 0)
- **Tasks**: Hiển thị số lượng tasks đang chạy (ban đầu là 0)
- **Infrastructure**: Phần quan trọng nhất

### Capacity Providers

ECS cluster của bạn có ba capacity providers:

1. **FARGATE**
   - Khởi chạy Fargate tasks trên ECS cluster
   - Serverless compute cho containers

2. **FARGATE_SPOT**
   - Khởi chạy Fargate tasks ở chế độ Spot
   - Tương tự như EC2 Spot instances
   - Tiết kiệm chi phí cho các workloads chịu lỗi được

3. **ASG Provider**
   - Khởi chạy EC2 instances thông qua Auto Scaling Group
   - Managed scaling
   - Kích thước ban đầu: 0

### Khởi Chạy Container Instances

Để xem cách container instances hoạt động:

1. Vào **Details** trong ASG
2. Chỉnh sửa desired capacity thành 1
3. Một EC2 instance sẽ được tạo và đăng ký vào `DemoCluster`
4. Instance xuất hiện trong **Container instances**

### Chi Tiết Container Instance

Khi instance đang chạy và đã đăng ký:

- Loại instance: `t2.micro` (hoặc loại bạn đã chọn)
- Trạng thái: Running
- Tasks đang chạy: 0
- CPU khả dụng: 1024
- Memory khả dụng: 982 MB

Điều này cho thấy capacity có sẵn để khởi chạy tasks. Bạn có thể khởi chạy tasks trên instance này cho đến khi capacity cạn kiệt.

## Tùy Chọn Triển Khai Task

Khi tạo một ECS task, bạn có thể chọn khởi chạy nó trên:

- **Fargate capacity provider** (serverless)
- **Fargate Spot capacity provider** (tối ưu chi phí)
- **Container instances** từ Auto Scaling Group

## Tóm Tắt

Bây giờ bạn đã có một ECS cluster hoàn chỉnh với:

- ✅ Ba capacity providers (Fargate, Fargate Spot, ASG)
- ✅ Container instances sẵn sàng chạy tasks
- ✅ Auto Scaling Group để quản lý EC2 capacity

Bạn đã sẵn sàng để chạy ECS service đầu tiên!

## Các Bước Tiếp Theo

Trong bài học tiếp theo, chúng ta sẽ tìm hiểu cách triển khai và chạy service đầu tiên trên ECS cluster này.