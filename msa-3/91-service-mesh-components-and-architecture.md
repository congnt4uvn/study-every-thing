# Các Thành Phần và Kiến Trúc của Service Mesh

## Giới Thiệu

Trong bài giảng này, chúng ta sẽ tìm hiểu các thành phần quan trọng của service mesh, những thành phần chịu trách nhiệm xử lý các yêu cầu phi nghiệp vụ trong kiến trúc microservices.

## Các Thành Phần Cốt Lõi của Service Mesh

Các triển khai service mesh thường bao gồm hai thành phần quan trọng:

### 1. Data Plane (Tầng Dữ Liệu)

**Data plane** chịu trách nhiệm định tuyến lưu lượng giữa các microservices.

**Đặc điểm chính:**
- Xử lý tất cả lưu lượng truy cập đến các container của bạn
- Sử dụng proxy để quản lý giao tiếp
- Mỗi instance microservice đi kèm với một proxy sidecar container nhẹ
- Các proxy chặn mỗi request và response đến container microservice thực tế
- Data plane là tầng mà service mesh triển khai tất cả các sidecar container

### 2. Control Plane (Tầng Điều Khiển)

**Control plane** chịu trách nhiệm cấu hình, quản lý và giám sát tất cả các proxy.

**Tính năng chính:**
- Tạo các sidecar container trong data plane mỗi khi có pod hoặc container mới được tạo
- Bao gồm các thành phần quan trọng như:
  - Control-plane API
  - Service discovery (Khám phá dịch vụ)
  - Configuration management (Quản lý cấu hình)

## Các Triển Khai Service Mesh Phổ Biến

Service mesh là một khái niệm hoặc đặc tả. Để triển khai nó trong các deployment microservice, chúng ta sử dụng một trong các implementation có sẵn:

- **Istio** (phổ biến nhất)
- **Linkerd** (phổ biến nhất)
- **Consul**
- **Kong**
- **AWS App Mesh**
- **Azure Service Mesh**

Việc lựa chọn service mesh phụ thuộc vào yêu cầu cụ thể của tổ chức và ngân sách.

## Service Mesh trong Kubernetes

### Tổng Quan Kiến Trúc

Khi sử dụng một triển khai service mesh như Istio trong Kubernetes cluster:

1. **Kubernetes Cluster** chứa các pod với các microservices (ví dụ: accounts, loans, và cards microservices)
2. **Main Containers** chạy logic nghiệp vụ cốt lõi
3. **Sidecar Proxies** được tự động tạo bởi Istio control plane cho mỗi pod
4. Trong Istio, các sidecar proxy này được gọi là **Envoy proxies**

### Luồng Lưu Lượng

```
Request Từ Bên Ngoài → Sidecar Container (Envoy Proxy) → Main Container
```

**Cách hoạt động:**
- Lưu lượng không bao giờ đi trực tiếp đến pod thực tế
- Lưu lượng trước tiên đi đến sidecar container (Envoy proxy)
- Envoy proxy thực thi logic liên quan đến:
  - Giám sát bảo mật
  - Thu thập metrics
  - Các yêu cầu phi nghiệp vụ khác
- Cuối cùng, request được chuyển tiếp đến container thực tế

Mô hình này áp dụng cho tất cả các microservices (accounts, loans, cards, v.v.).

### Tầng Data Plane

Tầng mà tất cả các Envoy proxy (sidecar container) được triển khai được gọi là **Istio data plane**. Lý do là vì chúng chịu trách nhiệm quản lý tất cả lưu lượng đến các microservices của bạn.

## Tài Nguyên Học Tập

Để biết thêm chi tiết về service mesh, hãy truy cập các trang web triển khai như:
- **Istio**: [https://istio.io](https://istio.io)
  - Tuyên bố đơn giản hóa observability, traffic management, security và policy
  - Cung cấp tài liệu mở rộng về khả năng và triển khai

## Tại Sao Developer Nên Biết Về Service Mesh

Mặc dù service mesh là một kỹ năng kỹ thuật riêng biệt và các developer không cần phải là chuyên gia, nhưng việc hiểu các khái niệm này rất quan trọng:

### Lợi Ích Cho Developer:
- Giúp các cuộc thảo luận về chủ đề microservices nâng cao dễ dàng hơn
- Chuẩn bị cho các câu hỏi phỏng vấn về môi trường production
- Giúp hiểu kiến trúc tổng thể của microservices hiện đại

### Những Gì Bạn Nên Biết:
- Service mesh là gì?
- Khả năng của nó là gì?
- Nó phù hợp như thế nào trong hệ sinh thái microservices

### Các Khái Niệm Nâng Cao Cần Biết:
- Ingress
- Service mesh
- Sidecar containers

## Bảo Mật Với Service Mesh

### Mutual TLS (mTLS)

Service mesh có thể bảo mật giao tiếp service-to-service nội bộ trong cluster bằng cách sử dụng **Mutual TLS (mTLS)**.

**Tại sao điều này quan trọng:**
- Bạn có thể bảo mật edge server với OAuth2 và Spring Security
- Nhưng còn các microservices nội bộ trong Kubernetes cluster của bạn thì sao?
- **Câu trả lời là mTLS**

Đây là một khái niệm quan trọng có thể xuất hiện trong các cuộc phỏng vấn khi thảo luận về kiến trúc bảo mật microservices.

## Kết Luận

Service mesh cung cấp một cách mạnh mẽ để xử lý các cross-cutting concerns trong kiến trúc microservices mà không thêm độ phức tạp vào logic nghiệp vụ của bạn. Hiểu các thành phần của nó (data plane và control plane) và các tính năng bảo mật (như mTLS) là điều cần thiết cho các developer microservices hiện đại.

---

*Bài giảng này cung cấp nền tảng để hiểu kiến trúc service mesh. Bài giảng tiếp theo sẽ đi sâu hơn vào mTLS và bảo mật giao tiếp microservices nội bộ.*