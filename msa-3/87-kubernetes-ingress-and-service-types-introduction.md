# Kubernetes Ingress và Các Loại Service Nâng Cao

## Giới Thiệu

Phần này tập trung vào các khái niệm DevOps nâng cao thường được áp dụng trong môi trường microservices production thực tế. Mặc dù các lập trình viên không cần phải học chi tiết các khái niệm này, nhưng việc hiểu ở mức độ tổng quan sẽ mang lại lợi thế đáng kể trong các buổi phỏng vấn về microservices và công việc hàng ngày.

## Tại Sao Cần Học Các Khái Niệm DevOps Nâng Cao?

Khi tham gia phỏng vấn về microservices, ứng viên thường trả lời câu hỏi từ góc độ lập trình viên. Tuy nhiên, nếu bạn có thể cung cấp thêm những hiểu biết về các thực tiễn trong môi trường production sử dụng các khái niệm DevOps khác nhau, bạn chắc chắn sẽ gây ấn tượng với người phỏng vấn nhờ kiến thức rộng hơn của mình.

## Tổng Quan Về Các Loại Service Trong Kubernetes

Chúng ta đã học cách expose microservices bằng cách sử dụng các đối tượng Service trong Kubernetes. Tài liệu chính thức của Kubernetes mô tả nhiều loại service:

### Các Loại Service Phổ Biến
- **ClusterIP**: Giao tiếp nội bộ trong cluster (mặc định)
- **NodePort**: Expose service trên IP của mỗi Node tại một cổng tĩnh
- **LoadBalancer**: Expose service ra bên ngoài sử dụng load balancer của cloud provider

### Loại Service ExternalName

Ngoài ba loại service phổ biến, Kubernetes còn cung cấp loại service **ExternalName**.

#### Trường Hợp Sử Dụng ExternalName
ExternalName được sử dụng khi bạn muốn ánh xạ service của mình đến một tên DNS hoặc tên miền mà tổ chức của bạn sở hữu. Loại service này cung cấp tính linh hoạt cho các quản trị viên Kubernetes để ánh xạ các service đến các tên miền cụ thể.

#### Lợi Ích
- Các ứng dụng client có thể đơn giản chỉ cần forward request đến tên miền được cung cấp
- Loại service ExternalName xử lý việc chuyển tiếp request đến pod hoặc container tương ứng trong Kubernetes cluster
- Cung cấp sự trừu tượng hóa giữa DNS bên ngoài và định tuyến service nội bộ

## Giới Thiệu Về Kubernetes Ingress

### Ingress Là Gì?

Ingress là một cách khác để expose microservices ra ngoài Kubernetes cluster. Tuy nhiên, điều quan trọng cần hiểu là:

- **Ingress KHÔNG phải là một loại service**
- Ingress là một khái niệm và đối tượng riêng biệt trong Kubernetes
- Nó xuất hiện như một chủ đề riêng trong tài liệu chính thức của Kubernetes (không nằm trong các loại Service)

### Ingress vs LoadBalancer Service

Cả Ingress và LoadBalancer service type đều có thể expose microservices ra ngoài Kubernetes cluster, nhưng chúng phục vụ các mục đích khác nhau và có những đặc điểm riêng biệt:

| Khía Cạnh | LoadBalancer Service | Ingress |
|-----------|---------------------|---------|
| Loại | Loại service | Đối tượng Kubernetes riêng biệt |
| Mục đích | Expose một service duy nhất | Có thể expose nhiều service |
| Định tuyến | Đơn giản dựa trên port | Quy tắc định tuyến nâng cao (path, host-based) |
| Trường hợp sử dụng | Expose service riêng lẻ | Định tuyến cấp ứng dụng |

### Sự Khác Biệt Chính

Sự khác biệt chính là trong khi LoadBalancer là một loại service, Ingress là một khái niệm Kubernetes độc lập cung cấp khả năng định tuyến phức tạp hơn để expose nhiều service thông qua một điểm vào duy nhất.

## Các Bước Tiếp Theo

Trong các bài giảng tiếp theo, chúng ta sẽ đi sâu vào:
- Các khái niệm và kiến trúc Ingress chi tiết
- Cách cấu hình các tài nguyên Ingress
- Các ví dụ thực tế về việc sử dụng Ingress
- Best practices cho môi trường production

## Tóm Tắt

- Kiến thức DevOps nâng cao mang lại lợi thế trong phỏng vấn và công việc thực tế
- Kubernetes cung cấp nhiều loại service: ClusterIP, NodePort, LoadBalancer và ExternalName
- Loại service ExternalName ánh xạ các service đến tên miền của tổ chức
- Ingress là một khái niệm riêng biệt với các loại Service
- Ingress cung cấp khả năng định tuyến nâng cao để expose microservices

---

*Tài liệu này đề cập đến phần giới thiệu về Kubernetes Ingress và các loại service nâng cao như một phần của loạt bài về microservices DevOps.*