# Kiến Trúc và Thành Phần Kubernetes: Hướng Dẫn Chi Tiết

## Giới Thiệu

Trước khi triển khai các microservices vào Kubernetes cluster, điều quan trọng là phải hiểu cấu trúc bên trong của Kubernetes và các thành phần chịu tr책nhiệm cho việc triển khai tự động, rollout, scaling và các lợi ích khác mà Kubernetes cung cấp.

## Hiểu Về Kubernetes Cluster

Khi nói về Kubernetes, chúng ta đang đề cập đến một **cluster** - tập hợp các máy chủ hoặc máy ảo làm việc cùng nhau để cung cấp kết quả mong muốn cho người dùng cuối. Bên trong Kubernetes cluster, nhiều máy chủ hoặc máy ảo làm việc cùng nhau để đảm bảo các microservices hoạt động tốt mà không gặp sự cố.

### Tại Sao Chọn Kubernetes Thay Vì Docker Compose?

Bạn có thể thắc mắc: "Tại sao phải sử dụng thiết lập Kubernetes cluster phức tạp? Không thể triển khai microservices chỉ với Docker Compose sao?"

Mặc dù Docker Compose hữu ích, nhưng nó có những hạn chế đáng kể:

- **Giới Hạn Máy Chủ Đơn**: Docker Compose triển khai tất cả containers trên một máy chủ duy nhất
- **Vấn Đề Khả Năng Mở Rộng**: Ứng dụng production có thể có hàng trăm microservices không thể đặt hết trên một máy chủ
- **Không Có Tự Động Hóa**: Docker và Docker Compose thiếu khả năng triển khai tự động, rollout và scaling
- **Công Việc Thủ Công**: Chỉ sử dụng containers và Docker trong môi trường production đòi hỏi nhiều công việc thủ công

Kubernetes giải quyết các vấn đề này bằng cách cung cấp **môi trường phân tán đa máy chủ** nơi các microservices có thể được triển khai trên nhiều máy chủ (nodes) khác nhau trong cluster, với khả năng điều phối container tích hợp sẵn.

> **Hiểu Biết Quan Trọng**: Containers không giải quyết mọi vấn đề. Không có điều phối, việc quản lý containers trong môi trường production có thể trở nên quá tải.

## Kiến Trúc Kubernetes Cluster

Một Kubernetes cluster bao gồm hai loại nodes:

1. **Master Node (Control Plane)**: Chịu trách nhiệm kiểm soát và duy trì toàn bộ Kubernetes cluster
2. **Worker Nodes**: Chịu trách nhiệm xử lý traffic và chạy các microservices thực tế

## Các Thành Phần Của Master Node

Master Node (còn gọi là Control Plane) chứa một số thành phần quan trọng:

### 1. Kube API Server

**Kube API Server** là thành phần quản lý trung tâm:

- Cung cấp APIs để tương tác với Kubernetes cluster
- Tạo điều kiện giao tiếp giữa master nodes và worker nodes
- Nhận hướng dẫn từ các nguồn bên ngoài

**Các Cách Tương Tác Với Kubernetes Cluster:**
- **Admin UI**: Giao diện dashboard của Kubernetes
- **kubectl CLI**: Giao diện dòng lệnh để thực thi các lệnh Kubernetes

Người dùng cung cấp hướng dẫn cho Kubernetes thông qua cấu hình YAML, chỉ định các chi tiết như:
- Microservice nào cần triển khai
- Số lượng replicas cần thiết
- Docker image cần sử dụng

### 2. Scheduler

Thành phần **Scheduler**:

- Nhận yêu cầu từ Kube API Server
- Xác định worker node phù hợp nhất cho việc triển khai
- Thực hiện tính toán để xác định node tốt nhất dựa trên:
  - Băng thông khả dụng
  - Khối lượng công việc hiện tại
  - Tài nguyên khả dụng

**Quy Trình Ví Dụ:**
1. Người dùng chỉ thị: "Triển khai accounts microservice"
2. Kube API Server chuyển hướng dẫn đến Scheduler
3. Scheduler xác định worker node tối ưu
4. Scheduler gửi hướng dẫn triển khai về Kube API Server
5. Kube API Server giao tiếp với worker node được chọn

### 3. Controller Manager

**Controller Manager**:

- Liên tục theo dõi containers và worker nodes trong cluster
- Giám sát trạng thái sức khỏe của tất cả các thành phần
- Đảm bảo **trạng thái thực tế** khớp với **trạng thái mong muốn**
- Tự động thay thế các containers hoặc worker nodes có vấn đề

**Quản Lý Trạng Thái Mong Muốn:**
- Người dùng chỉ định: "Luôn chạy 3 instances của accounts microservice"
- Controller Manager thực hiện kiểm tra sức khỏe thường xuyên
- Nếu một instance bị lỗi, Controller Manager sẽ:
  - Chấm dứt container có vấn đề
  - Khởi chạy container mới để duy trì 3 instances khỏe mạnh

### 4. etcd

**etcd** đóng vai trò là bộ não của Kubernetes cluster:

- Hoạt động như cơ sở dữ liệu key-value phân tán
- Lưu trữ tất cả thông tin của Kubernetes cluster
- Duy trì dữ liệu cấu hình và trạng thái

**Ví Dụ Sử Dụng:**
- Controller Manager truy vấn etcd để hiểu số lượng replicas mong muốn
- Kube API Server ghi hướng dẫn của người dùng vào etcd
- Scheduler và các thành phần khác tham chiếu etcd trong các hoạt động

## Các Thành Phần Của Worker Node

Worker nodes chứa các thành phần chạy các workloads thực tế:

### 1. Kubelet

**Kubelet** là agent chạy trên tất cả worker nodes:

- Đóng vai trò cầu nối giao tiếp giữa master và worker nodes
- Nhận hướng dẫn triển khai từ master node thông qua Kube API Server
- Thực thi lệnh để triển khai và quản lý containers

**Ví Dụ:**
- Master node chỉ thị: "Triển khai accounts microservice với 3 replicas"
- Kubelet nhận và thực thi các hướng dẫn này

### 2. Container Runtime

**Container Runtime**:

- Cung cấp môi trường để chạy containers
- Thường là Docker, nhưng có thể là các container runtimes khác
- Phải được cài đặt trên tất cả worker nodes để cluster hoạt động

### 3. Pod

**Pod** là đơn vị triển khai nhỏ nhất trong Kubernetes:

- Được tạo bên trong worker nodes
- Chứa một hoặc nhiều containers
- Cung cấp sự cô lập giữa các microservices khác nhau

**Đặc Điểm Chính:**
- Worker nodes là các máy chủ/VMs lớn, nhưng containers không triển khai trực tiếp vào chúng
- Kubernetes tạo pods bên trong worker nodes
- Containers chạy bên trong pods

**Mô Hình Sử Dụng Pod:**

**Một Container Trên Mỗi Pod (Phổ Biến Nhất):**
- Mỗi microservice (accounts, cards, loans) chạy trong pod riêng
- Một container ứng dụng chính trên mỗi pod

**Nhiều Containers Trên Mỗi Pod (Sidecar Pattern):**
- Container ứng dụng chính + containers hỗ trợ/tiện ích
- Containers hỗ trợ giúp đỡ hoạt động của container chính
- Tất cả containers trong pod chia sẻ cùng một vòng đời

> **Quan Trọng**: Một pod thường chỉ chứa một container ứng dụng chính. Nhiều containers trong một pod được sử dụng cho các dịch vụ hỗ trợ (sidecar pattern).

### 4. Kube Proxy

**Kube Proxy** xử lý mạng:

- Cho phép containers giao tiếp với thế giới bên ngoài
- Tạo điều kiện giao tiếp giữa các containers trong cluster
- Có thể hạn chế giao tiếp chỉ trong nội bộ cluster

## Quy Trình Kubernetes Hoàn Chỉnh

Đây là cách tất cả các thành phần làm việc cùng nhau:

1. **Đầu Vào Người Dùng**: Hướng dẫn được cung cấp qua kubectl CLI hoặc Admin UI
2. **Kube API Server**: Nhận và xử lý hướng dẫn
3. **etcd**: Lưu trữ cấu hình và trạng thái mong muốn
4. **Scheduler**: Xác định worker node tối ưu cho triển khai
5. **Worker Node**: Kubelet nhận hướng dẫn triển khai
6. **Container Runtime**: Tạo và chạy containers bên trong pods
7. **Kube Proxy**: Xử lý mạng và phơi bày dịch vụ
8. **Controller Manager**: Liên tục giám sát và duy trì trạng thái mong muốn

## Khả Năng Mở Rộng và Tính Khả Dụng Cao

- **Nhiều Master Nodes**: Các cluster lớn yêu cầu nhiều master nodes
- **Nhiều Worker Nodes**: Có thể thêm bất kỳ số lượng worker nodes nào
- **Phân Phối Tải**: Tương tự như quản lý dự án (tỷ lệ 1 quản lý : 10 nhà phát triển)
- **Khả Năng Chịu Lỗi**: Cơ chế chuyển đổi dự phòng và phục hồi tự động

> **Lưu Ý**: Một master node đơn không thể xử lý số lượng worker nodes không giới hạn. Mở rộng master nodes của bạn tỷ lệ thuận với worker nodes.

## Tóm Tắt

Kubernetes cung cấp nền tảng điều phối container mạnh mẽ thông qua kiến trúc được thiết kế tốt:

- **Master Node (Control Plane)**: Quản lý cluster với Kube API Server, Scheduler, Controller Manager và etcd
- **Worker Nodes**: Chạy các workloads thực tế với Kubelet, Container Runtime, Pods và Kube Proxy
- **Tự Động Hóa**: Khả năng triển khai tự động, scaling và tự phục hồi
- **Khả Năng Mở Rộng**: Kiến trúc phân tán hỗ trợ hàng trăm microservices

Hiểu các thành phần này là rất quan trọng trước khi triển khai microservices vào Kubernetes cluster. Khi bạn làm việc thực hành với triển khai Kubernetes, các khái niệm này sẽ trở nên rõ ràng và thực tế hơn.

## Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ:
- Tạo một Kubernetes cluster
- Triển khai microservices vào cluster
- Xem các khái niệm kiến trúc này trong thực tế

Đảm bảo xem lại các thành phần này và mối quan hệ của chúng trước khi tiếp tục để đảm bảo sự rõ ràng.

---

*Hướng dẫn này bao gồm kiến trúc cơ bản của Kubernetes để triển khai các Java Spring Boot microservices trong môi trường production.*