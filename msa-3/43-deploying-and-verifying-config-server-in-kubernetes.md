# Triển Khai và Xác Minh Config Server trong Kubernetes - Hướng Dẫn Hoàn Chỉnh

## Tổng Quan

Hướng dẫn toàn diện này trình bày quy trình đầy đủ để triển khai microservice Config Server Spring Boot vào Kubernetes cluster cục bộ bằng cách sử dụng các file manifest Kubernetes. Chúng ta sẽ đề cập đến việc triển khai, xác minh qua nhiều phương pháp và kiểm tra kỹ lưỡng dịch vụ đang chạy.

## Yêu Cầu Tiên Quyết

- Kubernetes cluster cục bộ (ví dụ: Docker Desktop với Kubernetes đã bật)
- Công cụ kubectl CLI đã cài đặt và cấu hình
- Microservice Config Server với file manifest Kubernetes (`config-server.yaml`)
- Kubernetes Dashboard (tùy chọn, để xác minh trực quan)

## Phần 1: Xác Minh Trạng Thái Ban Đầu của Cluster

Trước khi triển khai Config Server, điều quan trọng là xác minh trạng thái hiện tại của Kubernetes cluster để đảm bảo namespace mặc định đang trống và sẵn sàng cho việc triển khai.

### Kiểm Tra Các Deployment Hiện Có

Chạy lệnh sau để liệt kê tất cả các deployment:

```bash
kubectl get deployments
```

**Kết Quả Mong Đợi:** "No resources found in default namespace"

Điều này xác nhận rằng hiện tại không có deployment nào trong namespace mặc định.

### Kiểm Tra Các Service Hiện Có

Kiểm tra các service hiện đang chạy trong cluster của bạn:

```bash
kubectl get services
```

**Kết Quả Mong Đợi:** Bạn chỉ nên thấy một service mặc định liên quan đến chính Kubernetes cluster. Không có service nào liên quan đến microservice.

### Kiểm Tra Replica Sets

Xác minh rằng không có replica set nào tồn tại:

```bash
kubectl get replicaset
```

**Kết Quả Mong Đợi:** "No resources found in default namespace"

### Xác Minh qua Kubernetes Dashboard

Bạn cũng có thể xác minh trạng thái trống bằng Kubernetes Dashboard:

1. Mở Kubernetes Dashboard của bạn
2. Đảm bảo bạn đã chọn namespace **default** từ menu dropdown
3. Nhấp vào **Deployments** - sẽ hiển thị "Nothing to display"
4. Kiểm tra **Pods** - sẽ hiển thị "Nothing to display"
5. Kiểm tra **Replica Sets** - sẽ hiển thị "Nothing to display"
6. Kiểm tra **Services** - chỉ nên hiển thị một service liên quan đến Kubernetes

Điều này xác nhận rằng namespace mặc định của bạn đã sạch và sẵn sàng cho việc triển khai.

## Phần 2: Triển Khai Config Server lên Kubernetes

### Bước 1: Điều Hướng đến Vị Trí File Manifest

Trước khi chạy lệnh triển khai, đảm bảo bạn đang ở trong thư mục chính xác nơi file manifest `config-server.yaml` của bạn được lưu trữ.

```bash
# Xác minh thư mục hiện tại
pwd

# Liệt kê các file để xác nhận config-server.yaml tồn tại
ls
```

### Bước 2: Áp Dụng Kubernetes Manifest

Thực thi lệnh sau để triển khai Config Server:

```bash
kubectl apply -f config-server.yaml
```

**Kết Quả Mong Đợi:**
```
deployment.apps/config-server-deployment created
service/config-server created
```

Output này xác nhận rằng cả deployment và service đã được tạo thành công.

**Lưu Ý:** Tất cả các lệnh Kubernetes được sử dụng trong hướng dẫn này sẽ được ghi lại trong kho GitHub để tham khảo trong tương lai.

## Phần 3: Xác Minh Việc Triển Khai

Sau khi áp dụng file manifest, xác minh rằng Config Server đã được triển khai thành công bằng nhiều phương pháp.

### Phương Pháp 1: Xác Minh Deployments

Kiểm tra trạng thái deployment:

```bash
kubectl get deployments
```

**Kết Quả Mong Đợi:**
```
NAME                        READY   UP-TO-DATE   AVAILABLE   AGE
config-server-deployment    1/1     1            1           30s
```

**Ý Nghĩa:**
- **NAME**: Tên deployment là `config-server-deployment`
- **READY**: Hiển thị `1/1`, nghĩa là trạng thái mong muốn là 1 replica và trạng thái thực tế cũng là 1
- Container đang ở trạng thái khỏe mạnh không có vấn đề gì

### Phương Pháp 2: Xác Minh Services

Kiểm tra cấu hình service:

```bash
kubectl get services
```

**Kết Quả Mong Đợi:**
```
NAME            TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
kubernetes      ClusterIP      10.96.0.1       <none>        443/TCP          5d
config-server   LoadBalancer   10.96.157.23    localhost     8071:30153/TCP   1m
```

**Thông Tin Chính:**
- **Tên Service**: `config-server`
- **Loại Service**: `LoadBalancer`
- **Cluster IP**: Địa chỉ IP nội bộ (ví dụ: 10.96.157.23) - chỉ truy cập được trong cluster
- **External IP**: `localhost` (vì đây là môi trường cục bộ)
- **Ánh Xạ Port**: 
  - Port bên ngoài: `8071` (truy cập được từ bên ngoài cluster)
  - NodePort: `30153` (tự động gán bởi Kubernetes)

**Lưu Ý Quan Trọng:**
- Cluster IP chỉ có ý nghĩa trong Kubernetes cluster
- Trong môi trường cục bộ, External IP hiển thị là `localhost`
- Trong môi trường cloud (AWS, Azure, GCP), bạn sẽ nhận được địa chỉ IP công khai thực tế
- Config Server được expose tại `localhost:8071`
- Port `30153` là NodePort tự động gán bởi Kubernetes (sẽ được giải thích trong các bài giảng sau về các loại service)

### Phương Pháp 3: Xác Minh Replica Sets

Kiểm tra trạng thái replica set:

```bash
kubectl get replicaset
```

**Kết Quả Mong Đợi:**
```
NAME                                  DESIRED   CURRENT   READY   AGE
config-server-deployment-7f8d9b5c4d   1         1         1       2m
```

**Ý Nghĩa:**
- **Desired**: 1 replica nên đang chạy
- **Current**: 1 replica hiện đang chạy
- **Ready**: 1 replica đã sẵn sàng phục vụ traffic

**Quan Trọng:** Nếu số lượng current là 0, Kubernetes sẽ tự động phát hiện điều này và tạo container mới để thay thế container bị lỗi. Đây là một phần của khả năng tự phục hồi (self-healing) của Kubernetes.

### Phương Pháp 4: Xác Minh Pods

Kiểm tra trạng thái pod:

```bash
kubectl get pods
```

**Kết Quả Mong Đợi:**
```
NAME                                        READY   STATUS    RESTARTS   AGE
config-server-deployment-7f8d9b5c4d-x9k2m   1/1     Running   0          3m
```

**Thông Tin Chính:**
- **Tên Pod**: Được tạo tự động với tên deployment làm tiền tố
- **Status**: `Running` - container đang chạy thành công
- **Ready**: `1/1` - tất cả container trong pod đã sẵn sàng

## Phần 4: Xác Minh Qua Kubernetes Dashboard

Kubernetes Dashboard cung cấp cách trực quan để xác minh và giám sát việc triển khai của bạn.

### Truy Cập Dashboard

Đảm bảo bạn đã cài đặt và có thể truy cập Kubernetes Dashboard. Chọn namespace **default**.

### 1. Kiểm Tra Services

Điều hướng đến phần **Services**:

- **Tên Service**: `config-server`
- **Loại**: `LoadBalancer`
- **External Endpoint**: `localhost:8071`

Điều này cho thấy service của bạn được expose đúng cách và có thể truy cập được.

### 2. Kiểm Tra Deployments

Điều hướng đến phần **Deployments**:

- **Deployment**: `config-server-deployment`
- Nhấp vào deployment để xem thông tin chi tiết:
  - Chi tiết pod
  - Container image được sử dụng
  - Nhãn được gán
  - Chi tiết cấu hình

### 3. Kiểm Tra Pods

Điều hướng đến phần **Pods** và nhấp vào pod config-server của bạn:

- Xem thông tin pod toàn diện
- Kiểm tra trạng thái và sức khỏe của pod
- **Tính Năng Quan Trọng**: Nhấp vào tùy chọn **"Logs"** để xem logs

### Xem Logs của Pod

Tính năng logs trong Kubernetes Dashboard rất quan trọng cho việc debug:

1. Nhấp vào pod config-server
2. Nhấp nút **"Logs"**
3. Xem tất cả logs ứng dụng Spring Boot
4. Sử dụng logs để debug bất kỳ vấn đề nào với container của bạn

Đây là nơi chính để kiểm tra khi khắc phục sự cố với container.

### 4. Kiểm Tra Replica Sets

Điều hướng đến phần **Replica Sets**:

- Xem replica set cho config-server-deployment
- Xem trạng thái running so với desired
- Kiểm tra pods nào đang chạy container
- Giám sát sức khỏe và trạng thái của pod

## Phần 5: Kiểm Tra Config Server

Sau khi triển khai, hãy kiểm tra kỹ lưỡng Config Server bằng cách truy cập các endpoint cấu hình của nó.

### Kiểm Tra 1: Cấu Hình Accounts Microservice (Production Profile)

Truy cập cấu hình accounts service cho production profile:

```
URL: http://localhost:8071/accounts/prod
```

**Kết Quả Mong Đợi:** 
- Trả về các thuộc tính cấu hình cho accounts microservice
- Bao gồm các thuộc tính từ cả production profile và default profile
- Các thuộc tính được merge và trả về ở định dạng JSON

### Kiểm Tra 2: Cấu Hình Loans Microservice

Truy cập cấu hình loans service:

```
URL: http://localhost:8071/loans/default
```

**Kết Quả Mong Đợi:**
- Trả về các thuộc tính cấu hình cho loans microservice
- Hiển thị các thuộc tính từ default profile

### Kiểm Tra 3: Cấu Hình Eureka Server

Truy cập cấu hình Eureka Server:

```
URL: http://localhost:8071/eureka/default
```

**Kết Quả Mong Đợi:**
- Trả về các thuộc tính cấu hình Eureka Server
- Tất cả thuộc tính đến từ default profile

**Lưu Ý Quan Trọng:** Eureka Server không có các thuộc tính riêng cho profile. Tất cả thuộc tính Eureka đều có sẵn trong default profile, đó là lý do tại sao chúng ta truy cập nó với `/default`.

### Xác Nhận Kiểm Tra Thành Công

Nếu cả ba endpoint đều trả về các thuộc tính cấu hình như mong đợi, điều này xác nhận rằng:
- Config Server đã được triển khai thành công lên Kubernetes cluster
- Service có thể truy cập được tại `localhost:8071`
- Việc lấy cấu hình đang hoạt động chính xác
- Tất cả microservices sẽ có thể lấy cấu hình của chúng

## Phần 6: Hiểu về Các Loại Service trong Kubernetes

Config Server được expose bằng loại service **LoadBalancer**. Hãy hiểu điều này có nghĩa là gì:

### Các Thành Phần Service

1. **ClusterIP**: 
   - Địa chỉ IP nội bộ trong cluster
   - Chỉ truy cập được từ bên trong Kubernetes cluster
   - Mọi service đều nhận một ClusterIP mặc định

2. **NodePort**: 
   - Port `30153` trong ví dụ của chúng ta
   - Tự động gán bởi Kubernetes
   - Cho phép truy cập service qua IP của bất kỳ node nào
   - Phạm vi port: 30000-32767

3. **LoadBalancer**: 
   - Cung cấp truy cập bên ngoài đến service
   - Trong môi trường cục bộ: Sử dụng `localhost`
   - Trong môi trường cloud: Cung cấp load balancer thực với IP công khai
   - Expose service tại port `8071`

### Môi Trường Cục Bộ vs Cloud

**Môi Trường Cục Bộ:**
- External IP: `localhost`
- Phù hợp cho phát triển và kiểm thử
- Không cần load balancing thực sự

**Môi Trường Cloud (AWS, Azure, GCP):**
- External IP: Địa chỉ IP công khai thực (ví dụ: 52.123.45.67)
- Cung cấp load balancer của nhà cung cấp cloud
- Phân phối traffic tự động
- Tính khả dụng cao và khả năng mở rộng

## Phần 7: Hướng Dẫn Khắc Phục Sự Cố

### Xem Logs Sử Dụng kubectl

Nếu bạn gặp vấn đề, hãy kiểm tra logs của pod:

```bash
# Lấy tên pod trước
kubectl get pods

# Xem logs (thay thế <pod-name> bằng tên pod thực tế)
kubectl logs <pod-name>

# Theo dõi logs theo thời gian thực
kubectl logs -f <pod-name>

# Xem logs từ instance container trước đó (nếu container restart)
kubectl logs <pod-name> --previous
```

### Xem Logs Sử Dụng Kubernetes Dashboard

1. Điều hướng đến **Pods**
2. Nhấp vào pod config-server
3. Nhấp nút **"Logs"**
4. Xem logs ứng dụng Spring Boot
5. Sử dụng tính năng tìm kiếm và lọc để tìm lỗi cụ thể

### Các Vấn Đề Thường Gặp và Giải Pháp

#### Vấn Đề 1: Pod Không Khởi Động

**Triệu Chứng:** Trạng thái pod hiển thị `Error`, `CrashLoopBackOff`, hoặc `ImagePullBackOff`

**Giải Pháp:**
- Kiểm tra logs để tìm lỗi ứng dụng
- Xác minh Docker image tồn tại và có thể truy cập được
- Kiểm tra image pull secrets nếu sử dụng private registry
- Xác minh giới hạn tài nguyên không quá hạn chế

#### Vấn Đề 2: Service Không Truy Cập Được

**Triệu Chứng:** Không thể truy cập service tại `localhost:8071`

**Giải Pháp:**
- Xác minh loại service là LoadBalancer
- Kiểm tra cấu hình port trong file manifest
- Đảm bảo pod đang ở trạng thái `Running`
- Xác minh không có xung đột port trên máy cục bộ của bạn

#### Vấn Đề 3: Connection Refused

**Triệu Chứng:** Endpoint service trả về "connection refused"

**Giải Pháp:**
- Đảm bảo container port khớp với target port của service
- Xác minh ứng dụng đang lắng nghe trên port chính xác (8071)
- Kiểm tra xem ứng dụng đã khởi động thành công trong logs chưa
- Xác minh các quy tắc firewall không chặn port

#### Vấn Đề 4: Cấu Hình Không Load

**Triệu Chứng:** Các endpoint trả về lỗi hoặc phản hồi trống

**Giải Pháp:**
- Xác minh Config Server được kết nối với configuration repository
- Kiểm tra thông tin xác thực và quyền truy cập Git repository
- Đảm bảo các file cấu hình tồn tại trong repository
- Xem lại logs Config Server để tìm lỗi kết nối

### Kubernetes Self-Healing (Tự Phục Hồi)

Hãy nhớ rằng Kubernetes có khả năng tự phục hồi:

- Nếu container bị crash, Kubernetes tự động restart nó
- Nếu desired replicas không khớp với current replicas, Kubernetes tạo hoặc xóa pods
- Health checks đảm bảo chỉ pods khỏe mạnh nhận traffic
- Các node bị lỗi kích hoạt việc lên lịch lại pod sang các node khỏe mạnh

## Phần 8: Tóm Tắt Triển Khai

### Những Gì Chúng Ta Đã Triển Khai

✅ **Config Server Deployment:**
- 1 replica (pod) chạy Config Server container
- Chính sách restart tự động
- Phân bổ và giới hạn tài nguyên
- Cấu hình health check

✅ **Config Server Service:**
- Loại: LoadBalancer
- Truy cập bên ngoài qua `localhost:8071`
- ClusterIP nội bộ cho giao tiếp trong cluster
- NodePort `30153` cho truy cập cấp node

### Lợi Ích Chính

1. **Quản Lý Cấu Hình Tập Trung**: Tất cả microservices có thể lấy cấu hình từ một vị trí trung tâm
2. **Tự Phục Hồi**: Kubernetes tự động phục hồi từ lỗi
3. **Khả Năng Mở Rộng**: Dễ dàng mở rộng bằng cách điều chỉnh số lượng replica
4. **Service Discovery**: Các service khác có thể khám phá Config Server qua Kubernetes DNS
5. **Load Balancing**: Load balancing tích hợp sẵn cho traffic bên ngoài

### Danh Sách Kiểm Tra Xác Minh Triển Khai

Trước khi tiến hành triển khai các microservices khác, hãy đảm bảo:

- [ ] Deployment hiển thị `1/1` ready
- [ ] Service có loại LoadBalancer và external endpoint
- [ ] Trạng thái pod là `Running`
- [ ] Replica set hiển thị desired = current = 1
- [ ] Tất cả test endpoints trả về cấu hình như mong đợi
- [ ] Logs hiển thị Spring Boot khởi động thành công
- [ ] Không có lỗi trong Kubernetes Dashboard

## Tài Nguyên Bổ Sung

### Tham Chiếu Lệnh

Tất cả các lệnh được sử dụng trong hướng dẫn này:

```bash
# Lệnh xác minh
kubectl get deployments
kubectl get services
kubectl get replicaset
kubectl get pods

# Lệnh triển khai
kubectl apply -f config-server.yaml

# Lệnh logging
kubectl logs <pod-name>
kubectl logs -f <pod-name>

# Mô tả tài nguyên để biết thông tin chi tiết
kubectl describe deployment config-server-deployment
kubectl describe service config-server
kubectl describe pod <pod-name>
```

### Liên Kết Tài Liệu

- Các file manifest đầy đủ có sẵn trong kho GitHub
- Tất cả lệnh được ghi lại để tham khảo trong tương lai
- Ví dụ cấu hình cho các profile khác nhau
- Hướng dẫn khắc phục sự cố với các kịch bản thường gặp

## Kết Luận

Chúc mừng! Bạn đã thành công:

1. ✅ Xác minh trạng thái ban đầu của Kubernetes cluster
2. ✅ Triển khai Config Server lên Kubernetes bằng file manifest
3. ✅ Xác minh triển khai qua nhiều phương pháp (kubectl và Dashboard)
4. ✅ Kiểm tra tất cả các endpoint cấu hình thành công
5. ✅ Hiểu về các loại service và networking trong Kubernetes

Config Server của bạn hiện đang chạy trong Kubernetes và sẵn sàng phục vụ cấu hình cho các microservices khác. Đây là bước đầu tiên quan trọng trong việc xây dựng kiến trúc microservices trên Kubernetes.

## Các Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ khám phá:
- Triển khai các microservices bổ sung (Accounts, Loans, Cards)
- Cấu hình giao tiếp giữa các service
- Thiết lập service discovery với Eureka
- Triển khai API Gateway trong Kubernetes
- Quản lý cấu hình theo môi trường cụ thể

Cảm ơn và hẹn gặp lại bạn trong bài giảng tiếp theo!