# Kubernetes Ingress: Lợi Ích và Quản Lý Lưu Lượng

## Giới Thiệu

Trong bài giảng này, chúng ta sẽ khám phá lý do tại sao các tổ chức nên sử dụng Kubernetes Ingress và hiểu những lợi ích mà nó mang lại cho kiến trúc microservices.

## Lợi Ích của Kubernetes Ingress

### 1. Điểm Truy Cập Duy Nhất

Lợi thế chính đầu tiên của Ingress là nó hoạt động như một **điểm truy cập duy nhất** vào Kubernetes cluster của bạn. Nó đóng vai trò như một edge server thông qua đó bạn có thể cấu hình quyền truy cập cho nhiều microservices trong cluster. Điều này giúp đơn giản hóa việc quản lý quyền truy cập từ bên ngoài vào các microservices của bạn.

> **Lưu ý:** Spring Cloud Gateway cũng cung cấp lợi thế tương tự. Không có cách tiếp cận nào "tốt" hay "xấu" giữa Spring Cloud Gateway và Kubernetes Ingress - nó phụ thuộc vào cấu trúc nhóm và kỹ năng kỹ thuật của tổ chức bạn.

### 2. Chấm Dứt TLS/SSL

Kubernetes Ingress có khả năng **chấm dứt TLS/SSL (TLS/SSL termination)**, điều này rất quan trọng cho bảo mật web.

#### Tại Sao Cần TLS/SSL?

- Tất cả các giao tiếp web sử dụng các giao thức bảo mật như TLS/SSL (bạn thấy HTTPS trên trình duyệt)
- Ngăn chặn việc đánh cắp dữ liệu trong quá trình truyền từ client đến server
- Mã hóa dữ liệu để hacker không thể chặn và đánh cắp thông tin
- Chỉ có servers mới có thể giải mã dữ liệu đã được mã hóa

#### Cân Nhắc Về Hiệu Suất

Tuy nhiên, giao tiếp HTTPS/TLS đi kèm với **chi phí về hiệu suất**. Vì không có hacker nào có thể xâm nhập vào Kubernetes cluster của bạn ngoại trừ thông qua edge server, nên không cần thiết phải duy trì giao tiếp HTTPS bên trong cluster.

**Giải pháp:** Nhiều tổ chức chấm dứt giao tiếp TLS tại lớp Ingress:
- Tại edge server, HTTPS được chuyển đổi thành HTTP
- Khi dữ liệu vào cluster, nó di chuyển qua giao thức HTTP
- Điều này tránh các tác động nghiêm trọng đến hiệu suất trong khi vẫn duy trì bảo mật

### 3. Định Tuyến Dựa Trên Đường Dẫn và Host

Ingress hỗ trợ hai loại định tuyến:

#### Định Tuyến Dựa Trên Đường Dẫn (Path-Based Routing)
```
example.com/app1 → Service 1
example.com/app2 → Service 2
```

#### Định Tuyến Dựa Trên Host (Host-Based Routing)
```
app1.example.com → Service 1
app2.example.com → Service 2
```

Các tổ chức có thể định nghĩa các quy tắc định tuyến dựa trên cấu trúc subdomain và các mẫu truy cập của họ.

### 4. Cân Bằng Tải

Ingress có khả năng **cân bằng tải các yêu cầu** và phân phối lưu lượng truy cập giữa nhiều pods của cùng một service.

**Cách hoạt động:**
1. Ingress chuyển tiếp yêu cầu đến ClusterIP service
2. ClusterIP service phân phối yêu cầu đến các pods có sẵn
3. Lưu lượng được cân bằng giữa các containers được triển khai trong các pods đó

### 5. Annotations Cho Cấu Hình Nâng Cao

Ingress hỗ trợ **annotations** cho phép các khả năng bổ sung:
- Quy tắc viết lại (Rewriting rules)
- Custom headers
- Xác thực và ủy quyền (Authentication và Authorization)
- Các cài đặt nâng cao khác

## Spring Cloud Gateway vs Kubernetes Ingress

### So Sánh Khả Năng

Cả hai giải pháp đều cung cấp các khả năng tương tự:

| Tính Năng | Spring Cloud Gateway | Kubernetes Ingress |
|-----------|---------------------|-------------------|
| Điểm Truy Cập Duy Nhất | ✓ | ✓ |
| Định Tuyến Theo Đường Dẫn | ✓ | ✓ |
| Định Tuyến Theo Host | ✓ | ✓ |
| Cân Bằng Tải | ✓ | ✓ |
| Chấm Dứt TLS/SSL | ✓ | ✓ |
| Xác Thực | ✓ | ✓ |
| Cross-Cutting Concerns | ✓ | ✓ |

### Lựa Chọn Giữa Chúng

Sự lựa chọn phụ thuộc vào:
- Quyết định của kiến trúc sư dự án
- Sở thích của ban lãnh đạo dự án
- Kỹ năng kỹ thuật của nhóm
- Cấu trúc tổ chức

**Quan trọng:** Là các developer, chúng ta nên sẵn sàng làm việc với cả hai cách tiếp cận dựa trên yêu cầu của tổ chức.

## Ingress Controller vs Load Balancer Service

Cả hai đều có thể expose microservices ra thế giới bên ngoài, nhưng chúng khác nhau về khả năng:

### Ingress Controller
- Khả năng định tuyến nâng cao
- Quản lý lưu lượng phức tạp
- Phù hợp cho các microservices quy mô lớn, quan trọng

### Load Balancer Service
- Thiết lập đơn giản hơn
- Chức năng expose cơ bản
- Phù hợp cho:
  - Các tổ chức nhỏ
  - Số lượng microservices hạn chế
  - Các microservices mức độ quan trọng thấp

## Các Loại Lưu Lượng và Thuật Ngữ

### Các Thuật Ngữ Quan Trọng Trong Thảo Luận Về Microservices

#### 1. Ingress Traffic
Lưu lượng **đi vào** một Kubernetes cluster.

#### 2. Egress Traffic
Lưu lượng **đi ra khỏi** một Kubernetes cluster (ngược lại với Ingress traffic).

#### 3. North-South Traffic
Thuật ngữ khác cho Ingress và Egress traffic - lưu lượng đi vào và ra khỏi cluster.

**Lưu ý:** Ingress controllers được thiết kế để xử lý North-South traffic (Ingress/Egress traffic).

### Còn Lưu Lượng Nội Bộ Thì Sao?

**Câu hỏi:** Nếu Ingress xử lý lưu lượng đi vào và ra khỏi cluster, thì lưu lượng giữa các microservices *bên trong* Kubernetes cluster thì sao?

**Trả lời:** Đây là lúc **Service Mesh** phát huy tác dụng.

## Các Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ khám phá chi tiết về Service Mesh và hiểu cách nó quản lý giao tiếp microservice nội bộ trong các Kubernetes clusters.

## Góc Nhìn Của Developer

Là developers, bạn không cần phải học mọi thứ về Kubernetes Ingress - việc thiết lập Ingress thường là trách nhiệm của các quản trị viên Kubernetes. Tuy nhiên, hiểu những khái niệm này đảm bảo bạn đã chuẩn bị sẵn sàng khi:
- Các tổ chức chọn Kubernetes Ingress thay vì Spring Cloud Gateway
- Bạn cần tham gia vào các cuộc thảo luận về kiến trúc
- Bạn được yêu cầu làm việc với các hệ thống dựa trên Ingress

Luôn cập nhật thông tin và sẵn sàng cho mọi tình huống!

---

*Cảm ơn bạn, và hẹn gặp lại trong bài giảng tiếp theo!*