# Các Loại Service trong Kubernetes cho Microservices

## Tổng Quan

Khi triển khai microservices lên Kubernetes, việc hiểu rõ các loại service là vô cùng quan trọng để expose ứng dụng một cách đúng đắn. Hướng dẫn này đề cập đến ba loại service chính trong Kubernetes: ClusterIP, NodePort và LoadBalancer, kèm theo các ví dụ thực tế cho Spring Boot microservices.

## Vấn Đề Khi Expose Tất Cả Services

Ban đầu, bạn có thể triển khai tất cả microservices với service type là LoadBalancer, expose chúng ra thế giới bên ngoài:
- Loans microservice
- Cards microservice
- Gateway server
- Eureka server
- Keycloak
- Config server

**Tuy nhiên, đây KHÔNG phải là cách tiếp cận đúng!**

Chỉ có **Gateway server** nên được expose ra bên ngoài vì nó đóng vai trò là edge server. Tất cả các client communications nên được định tuyến qua gateway, không phải trực tiếp đến từng microservice riêng lẻ.

## Ba Loại Service Chính

### 1. ClusterIP Service

**Service type mặc định** - Được sử dụng cho giao tiếp nội bộ trong Kubernetes cluster.

#### Đặc điểm:
- Tạo một địa chỉ IP nội bộ cho giao tiếp trong cluster
- **KHÔNG thể truy cập** từ bên ngoài cluster
- Service type mặc định nếu không chỉ định
- Tốt nhất cho việc bảo mật microservices khỏi traffic bên ngoài

#### Use Case:
Hoàn hảo cho các backend microservices (accounts, loans, cards) chỉ nên giao tiếp nội bộ.

#### Cấu Hình Ví Dụ:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: accounts
spec:
  type: ClusterIP
  ports:
    - port: 80
      targetPort: 8080
  selector:
    app: accounts
```

#### Cách Hoạt Động:

1. **Container Port**: Microservice chạy trên port 8080 bên trong pod
2. **Service Port**: Được expose cho các services khác tại port 80 thông qua ClusterIP
3. **Phương Thức Truy Cập**: Các services khác sử dụng:
   - Địa chỉ ClusterIP
   - Tên service (ví dụ: `http://accounts:80`)

#### Load Balancing:
Kubernetes tự động cân bằng tải các requests giữa nhiều pod replicas. Nếu bạn có 2 replicas trên các worker nodes khác nhau, Kubernetes phân phối traffic một cách thông minh mà client không cần biết vị trí của pods.

**Ví Dụ Setup:**
- Worker Node 1: Accounts pod (port 8080)
- Worker Node 2: Accounts pod (port 8080)
- ClusterIP Service: Expose cả hai tại port 80

Các services khác chỉ cần gọi `http://accounts:80` và Kubernetes sẽ xử lý routing!

---

### 2. NodePort Service

Expose service trên IP của mỗi worker node tại một port cố định.

#### Đặc điểm:
- Tự động gán một port trong khoảng: **30000-32767**
- Có thể truy cập từ bên ngoài cluster
- Yêu cầu biết địa chỉ IP của worker nodes
- Được xây dựng trên ClusterIP

#### Cấu Hình Ví Dụ:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: accounts
spec:
  type: NodePort
  ports:
    - port: 80
      targetPort: 8080
      nodePort: 32593  # Tùy chọn - tự động tạo nếu không chỉ định
  selector:
    app: accounts
```

#### Luồng Traffic:

1. Client bên ngoài gửi request đến: `http://<worker-node-ip>:32593`
2. Request đến NodePort (32593)
3. Chuyển tiếp đến ClusterIP service (port 80)
4. Cân bằng tải đến pod phù hợp (port 8080)

#### Nhược Điểm:

❌ **Vấn Đề IP Động**: Nếu worker node bị lỗi và được thay thế, địa chỉ IP của nó sẽ thay đổi
❌ **Phụ Thuộc Client**: Clients bên ngoài phải theo dõi và cập nhật địa chỉ IP của worker nodes
❌ **Không Sẵn Sàng Production**: Khó quản lý trong môi trường production

---

### 3. LoadBalancer Service

Cung cấp một external load balancer với địa chỉ IP public tĩnh.

#### Đặc điểm:
- Tạo một external load balancer (được cung cấp bởi cloud provider)
- Gán một **địa chỉ IP public tĩnh**
- Được xây dựng trên NodePort và ClusterIP
- Sẵn sàng production cho external traffic

#### Cấu Hình Ví Dụ:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: gateway
spec:
  type: LoadBalancer
  ports:
    - port: 80
      targetPort: 8080
  selector:
    app: gateway
```

#### Luồng Traffic:

1. Client bên ngoài gửi request đến: `http://<public-ip-or-domain>`
2. Load Balancer nhận traffic (IP public tĩnh)
3. Chuyển tiếp đến NodePort của worker node phù hợp
4. NodePort chuyển tiếp đến ClusterIP service
5. Cân bằng tải đến pod container phù hợp

#### Ưu Điểm:

✅ **IP Public Tĩnh**: Không bao giờ thay đổi trừ khi admin thay đổi thủ công
✅ **Ánh Xạ DNS**: Có thể ánh xạ tới tên miền (ví dụ: `api.mycompany.com`)
✅ **Đơn Giản Cho Client**: Clients sử dụng một endpoint duy nhất bất kể cluster thay đổi
✅ **Tự Động Theo Dõi**: Load balancer tự động theo dõi thay đổi của worker nodes
✅ **Mở Rộng Động**: Xử lý việc scaling replicas tự động (2 → 3 replicas)

---

## Best Practices cho Microservices

### Chiến Lược Service Type Được Khuyến Nghị:

| Microservice | Service Type | Lý Do |
|-------------|-------------|-------|
| Gateway Server | LoadBalancer | Điểm vào cho tất cả external traffic |
| Eureka Server | ClusterIP | Chỉ service discovery nội bộ |
| Config Server | ClusterIP | Quản lý cấu hình nội bộ |
| Accounts Service | ClusterIP | Backend service - không cần truy cập bên ngoài |
| Loans Service | ClusterIP | Backend service - không cần truy cập bên ngoài |
| Cards Service | ClusterIP | Backend service - không cần truy cập bên ngoài |
| Keycloak | LoadBalancer (tùy chọn) | Có thể cần truy cập bên ngoài cho OAuth flows |

### Lợi Ích Bảo Mật:

Sử dụng ClusterIP cho backend services mang lại:
- Bảo vệ khỏi truy cập bên ngoài không được ủy quyền
- Ngăn chặn việc expose trực tiếp microservices
- Thực thi gateway pattern (điểm vào duy nhất)
- Giảm bề mặt tấn công

---

## Tóm Tắt

Hiểu rõ các loại service trong Kubernetes là **thiết yếu** cho các nhà phát triển microservice:

- **ClusterIP**: Giao tiếp nội bộ, lựa chọn mặc định cho backend services
- **NodePort**: Truy cập bên ngoài qua node IP, phù hợp cho testing/development
- **LoadBalancer**: Sẵn sàng production cho truy cập bên ngoài với IP tĩnh

**Điểm Chính**: Chỉ expose Gateway server của bạn với LoadBalancer. Giữ tất cả các microservices khác ở chế độ internal bằng ClusterIP để có bảo mật và kiến trúc tốt hơn.

---

## Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ xem một demo thực tế về cấu hình các loại service này trong một deployment Spring Boot microservices thực tế.

**Chúc Bạn Học Tốt!** 🚀