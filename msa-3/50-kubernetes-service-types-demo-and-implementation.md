# Demo và Triển Khai Các Loại Dịch Vụ Kubernetes

## Tổng Quan

Hướng dẫn này trình bày ba loại dịch vụ Kubernetes chính (LoadBalancer, ClusterIP và NodePort) và cách chúng hoạt động khi expose microservices trong Kubernetes cluster.

## Hiểu Về Triển Khai Dịch Vụ Hiện Tại

### Kiểm Tra Các Dịch Vụ Đã Triển Khai

Để xem tất cả các dịch vụ trong Kubernetes cluster, chạy lệnh:

```bash
kubectl get services
```

Lệnh này hiển thị:
- Tên dịch vụ
- Loại dịch vụ
- IP bên ngoài (nếu có)
- Cổng và node port

### Loại Dịch Vụ: LoadBalancer

Microservice accounts ban đầu được triển khai với loại LoadBalancer:

**Đặc điểm:**
- **External IP**: `localhost` (trong cluster local) hoặc public IP (trong môi trường cloud)
- **Port**: 8080
- **NodePort**: Được tạo ngẫu nhiên (ví dụ: 30175)

**Luồng Request:**
1. Request từ bên ngoài → LoadBalancer (External IP)
2. LoadBalancer → NodePort
3. NodePort → ClusterIP
4. ClusterIP → Container microservice

**Kiểm Tra LoadBalancer:**
```
http://localhost:8080/api/contact-info
```

### Những Cân Nhắc Quan Trọng Với LoadBalancer

**Tại Sao Nên Tránh LoadBalancer Trong Production:**

1. **Vấn Đề Bảo Mật**: Microservices không nên được truy cập trực tiếp từ client bên ngoài. Traffic nên đi qua edge server/API gateway.

2. **Chi Phí**: Trong môi trường cloud:
   - Địa chỉ IP công khai không miễn phí
   - Mỗi LoadBalancer cần một public IP riêng
   - 100 microservices = 100 public IP = hóa đơn cloud đáng kể

## Triển Khai Loại Dịch Vụ ClusterIP

### Cấu Hình

Chỉnh sửa file Kubernetes manifest cho microservice accounts:

```yaml
type: ClusterIP
```

**Lưu ý**: "IP" phải viết hoa.

### Áp Dụng Cấu Hình

```bash
kubectl apply -f accounts-microservice.yaml
kubectl get services
```

### Hoạt Động Của ClusterIP

**Đặc điểm:**
- **External IP**: Không có
- **Cluster IP**: Chỉ có IP nội bộ
- **Port**: 8080
- **Khả năng truy cập**: Chỉ từ bên trong Kubernetes cluster

**Kết quả**: Các request từ trình duyệt bên ngoài tới API sẽ thất bại với lỗi "site cannot be reached", vì traffic từ bên ngoài cluster bị chặn.

**Giao Tiếp Nội Bộ**: Các ứng dụng khác trong cluster có thể giao tiếp sử dụng:
- Tên dịch vụ: `accounts`
- Địa chỉ Cluster IP
- Port: 8080

## Triển Khai Loại Dịch Vụ NodePort

### Cấu Hình

Chỉnh sửa file Kubernetes manifest:

```yaml
type: NodePort
```

Không cần chỉ định giá trị NodePort cụ thể; Kubernetes sẽ tạo ngẫu nhiên.

### Áp Dụng Cấu Hình

```bash
kubectl apply -f accounts-microservice.yaml
kubectl get services
```

### Hoạt Động Của NodePort

**Ví dụ Output:**
- **Service Type**: NodePort
- **NodePort**: 31182 (được tạo ngẫu nhiên)

**Truy Cập Microservice:**

❌ **Thất bại** - Sử dụng service port:
```
http://localhost:8080/api/contact-info
```

✅ **Thành công** - Sử dụng NodePort:
```
http://localhost:31182/api/contact-info
```

### Hạn Chế Của NodePort

- Cần sử dụng NodePort cụ thể để truy cập từ bên ngoài
- Nếu microservice được triển khai vào worker node khác, địa chỉ IP sẽ thay đổi
- Có thể gây vấn đề về khả năng truy cập trong production

## Thực Hành Tốt Nhất và Khuyến Nghị

### Lựa Chọn Loại Dịch Vụ

| Loại Dịch Vụ | Trường Hợp Sử Dụng | Khả Năng Truy Cập |
|--------------|-------------------|-------------------|
| **ClusterIP** | Microservices nội bộ | Chỉ trong cluster |
| **NodePort** | Phát triển/kiểm thử | Bên ngoài qua NodePort |
| **LoadBalancer** | Dịch vụ công khai | Bên ngoài qua public IP |

### Khuyến Nghị Cho Production

1. **Gateway Server**: Chỉ sử dụng LoadBalancer cho API Gateway/Edge Server
2. **Microservices Nội Bộ**: Sử dụng ClusterIP cho tất cả microservices khác
3. **Bảo Mật**: Định tuyến tất cả traffic bên ngoài qua gateway server
4. **Tối Ưu Chi Phí**: Giảm thiểu việc sử dụng LoadBalancer để giảm chi phí cloud

### Chiến Lược Triển Khai Tương Lai

Trong các phần tiếp theo về Kafka, Grafana và các thành phần khác:
- Thay đổi tất cả microservices sang loại **ClusterIP**
- **Ngoại lệ**: Giữ Gateway Server là **LoadBalancer**
- Điều này đảm bảo bảo mật và quản lý chi phí hợp lý

## Khôi Phục Thay Đổi

Cho mục đích học tập trong giai đoạn triển khai Kubernetes ban đầu, microservice accounts vẫn giữ là LoadBalancer:

```yaml
type: LoadBalancer
```

Điều này giúp dễ hiểu và kiểm thử hơn khi bạn làm việc qua các khái niệm triển khai Kubernetes.

## Tóm Tắt

- **LoadBalancer**: Expose dịch vụ ra bên ngoài với public IP (tốn kém, sử dụng hạn chế)
- **ClusterIP**: Chỉ truy cập nội bộ (được khuyến nghị cho hầu hết microservices)
- **NodePort**: Truy cập bên ngoài qua node port (phù hợp cho phát triển)

Hiểu các loại dịch vụ này rất quan trọng cho kiến trúc microservice Kubernetes và chiến lược triển khai phù hợp.

---

**Bước Tiếp Theo**: Trong các bài giảng tiếp theo, chúng ta sẽ khám phá việc bảo mật microservices và triển khai các mẫu gateway phù hợp với các loại dịch vụ Kubernetes.