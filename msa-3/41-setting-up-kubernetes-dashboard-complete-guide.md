# Hướng Dẫn Cài Đặt Kubernetes Dashboard - Đầy Đủ Chi Tiết

## Giới Thiệu

Cho đến nay, chúng ta đã tương tác với Kubernetes cluster chủ yếu thông qua các lệnh kubectl từ terminal cục bộ. Tuy nhiên, có một cách tiếp cận mạnh mẽ khác: sử dụng Admin UI để tương tác với Kubernetes cluster và giám sát trạng thái tổng thể của nó.

Việc có quyền truy cập vào UI cho Kubernetes cluster của bạn sẽ làm cho việc quản lý cluster trở nên dễ dàng hơn rất nhiều. Trong hướng dẫn này, chúng ta sẽ đi qua toàn bộ quy trình thiết lập Kubernetes Dashboard - giao diện quản trị của Kubernetes.

## Tìm Hiểu Về Kubernetes Dashboard

Kubernetes Dashboard là giao diện người dùng dựa trên web cho phép bạn:
- Xem trạng thái tổng thể của Kubernetes cluster
- Quản lý và triển khai ứng dụng
- Giám sát tài nguyên và khối lượng công việc
- Khắc phục sự cố các ứng dụng container

**Lưu Ý Quan Trọng:** Dashboard UI không được triển khai mặc định trong bất kỳ Kubernetes cluster nào, vì vậy chúng ta cần thực hiện các bước cài đặt cụ thể.

## Yêu Cầu Trước Khi Bắt Đầu

Trước khi bắt đầu, hãy đảm bảo bạn có:
- Docker Desktop được cài đặt với phiên bản mới nhất
- Kubernetes cluster cục bộ đang chạy
- Truy cập vào terminal với kubectl đã được cấu hình

## Cài Đặt Helm Package Manager

### Helm Là Gì?

Helm là trình quản lý gói (package manager) cho Kubernetes, tương tự như npm hoạt động trong hệ sinh thái JavaScript. Chúng ta sẽ sử dụng Helm để cài đặt Kubernetes Dashboard.

### Các Bước Cài Đặt Theo Hệ Điều Hành

#### Người Dùng macOS

Nếu bạn đã cài đặt Homebrew (package manager được khuyến nghị cho macOS):

```bash
brew install helm
```

#### Người Dùng Windows

1. Đầu tiên, cài đặt Chocolatey package manager bằng cách truy cập trang web chính thức
2. Làm theo hướng dẫn cài đặt trên trang web Chocolatey
3. Sau khi Chocolatey được cài đặt, chạy lệnh:

```powershell
choco install kubernetes-helm
```

### Xác Minh Cài Đặt Helm

Sau khi cài đặt, xác minh rằng Helm đã được cài đặt đúng cách:

```bash
helm version
```

Bạn sẽ thấy đầu ra hiển thị phiên bản hiện tại của Helm được cài đặt trên hệ thống của bạn.

## Cài Đặt Kubernetes Dashboard

### Bước 1: Thêm Helm Repository

Thực thi lệnh sau để thêm Kubernetes Dashboard Helm repository:

```bash
helm repo add kubernetes-dashboard https://kubernetes.github.io/dashboard/
```

### Bước 2: Cài Đặt Dashboard

Chạy lệnh cài đặt:

```bash
helm upgrade --install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard --create-namespace --namespace kubernetes-dashboard
```

Quá trình cài đặt sẽ mất 2-3 phút. Sau khi hoàn thành, bạn sẽ thấy thông báo xác nhận.

**Lưu Ý:** Nếu gặp cảnh báo hoặc lỗi, hãy đảm bảo bạn có Docker Desktop mới nhất và Kubernetes cluster cục bộ đang chạy.

### Bước 3: Truy Cập Dashboard

Để expose dashboard nhằm truy cập cục bộ, chạy lệnh:

```bash
kubectl -n kubernetes-dashboard port-forward svc/kubernetes-dashboard-kong-proxy 8443:443
```

**Quan Trọng:** Giữ cửa sổ terminal này mở. Việc đóng nó hoặc thực thi các lệnh khác sẽ dừng port forwarding, khiến dashboard không thể truy cập được.

### Bước 4: Mở Dashboard Trong Trình Duyệt

Truy cập dashboard tại: `https://localhost:8443`

Bạn có thể thấy cảnh báo chứng chỉ vì cluster tạo chứng chỉ tự ký (self-signed certificate). Đối với thử nghiệm cục bộ, điều này có thể chấp nhận được:
1. Nhấp vào "Show details" (Hiển thị chi tiết) hoặc "Advanced" (Nâng cao)
2. Nhấp vào "Visit this website" (Truy cập trang web này) hoặc "Proceed" (Tiếp tục)

Bây giờ bạn sẽ thấy trang đăng nhập Kubernetes Dashboard yêu cầu token.

## Lưu Ý Về Số Cổng

**Quan Trọng:** Trong các phiên bản hoặc phương pháp cài đặt khác nhau, dashboard có thể khả dụng trên các cổng khác nhau:
- Phương pháp hiện tại dựa trên Helm: Cổng **8443**
- Phương pháp cũ/không còn dùng: Cổng **8001**

Đừng lo lắng về sự khác biệt về số cổng trong các hướng dẫn hoặc video khác nhau.

## Tạo Admin User Và Xác Thực

### Bước 1: Tạo Service Account

Service Account là thông tin xác thực cho một người dùng cụ thể trong Kubernetes.

Tạo file có tên `dashboard-admin-user.yaml`:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kubernetes-dashboard
```

Áp dụng cấu hình:

```bash
kubectl apply -f dashboard-admin-user.yaml
```

### Bước 2: Tạo Cluster Role Binding

Để cấp quyền admin cho service account, tạo file có tên `dashboard-role-binding.yaml`:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kubernetes-dashboard
```

Áp dụng cấu hình:

```bash
kubectl apply -f dashboard-role-binding.yaml
```

**Hiểu Về Cấu Hình:**
- **apiVersion**: Chỉ định phiên bản API cho RBAC (rbac.authorization.k8s.io/v1)
- **kind**: ClusterRoleBinding liên kết cluster role với một subject
- **roleRef**: Tham chiếu đến cluster-admin role (role được định nghĩa trước có quyền truy cập đầy đủ cluster)
- **subjects**: Chỉ định ServiceAccount để liên kết role

### Tùy Chọn Xác Thực 1: Token Tạm Thời

Tạo token tạm thời:

```bash
kubectl -n kubernetes-dashboard create token admin-user
```

Lệnh này tạo token ngắn hạn sẽ hết hạn nếu không được sử dụng.

### Tùy Chọn Xác Thực 2: Token Dài Hạn (Được Khuyến Nghị)

Để có token vĩnh viễn, tạo tài nguyên Secret.

Tạo file có tên `secret.yaml`:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: admin-user
  namespace: kubernetes-dashboard
  annotations:
    kubernetes.io/service-account.name: "admin-user"
type: kubernetes.io/service-account-token
```

Áp dụng cấu hình:

```bash
kubectl apply -f secret.yaml
```

Lấy token:

```bash
kubectl get secret admin-user -n kubernetes-dashboard -o jsonpath={".data.token"} | base64 -d
```

**Quan Trọng:** Khi sao chép token, đừng bao gồm bất kỳ ký tự theo sau nào như `%`.

Lưu token này một cách an toàn - bạn có thể sử dụng nó nhiều lần để truy cập dashboard mà không cần tạo token mới mỗi lần.

## Truy Cập Dashboard

1. Dán token của bạn vào trang đăng nhập dashboard
2. Chọn tùy chọn "Token"
3. Nhấp "Sign In" (Đăng nhập)

Bây giờ bạn đã có quyền truy cập đầy đủ vào Kubernetes Dashboard!

## Hiểu Về Các Khái Niệm Kubernetes

### Namespaces

Namespaces là các khu vực bị cô lập trong Kubernetes cluster, tương tự như có môi trường dev, QA và production. Chúng giúp tổ chức và phân tách tài nguyên.

Namespace `kubernetes-dashboard` chứa tất cả các tài nguyên liên quan đến chính dashboard UI.

### Service Accounts

Service Accounts là thông tin xác thực cho các process chạy trong pods hoặc cho người dùng truy cập cluster. Chúng xác định danh tính và quyền hạn.

### Cluster Roles Và Bindings

- **ClusterRole**: Định nghĩa quyền hạn (những hành động nào có thể được thực hiện)
- **ClusterRoleBinding**: Gán roles cho users hoặc service accounts
- **cluster-admin**: Role được định nghĩa trước với quyền truy cập quản trị đầy đủ vào cluster

### Secrets

Secrets lưu trữ thông tin nhạy cảm như mật khẩu, tokens và keys một cách an toàn trong Kubernetes.

## Khám Phá Dashboard

Sau khi đăng nhập, bạn có thể khám phá:

### Điều Hướng

1. **Namespace Selector**: Chuyển đổi giữa các namespaces khác nhau (mặc định là "default")
2. **Workloads**: Xem Deployments, Pods, ReplicaSets, v.v.
3. **Service Accounts**: Trong namespace kubernetes-dashboard, bạn sẽ thấy tài khoản admin-user
4. **Cluster Role Bindings**: Xem các phân công role và quyền hạn

### Ví Dụ: Xem Các Thành Phần Dashboard

Điều hướng đến namespace `kubernetes-dashboard` để thấy:
- **Deployments**: Các instance đang chạy của ứng dụng dashboard
- **Pods**: Các instance riêng lẻ chạy mã dashboard
- **ReplicaSets**: Đảm bảo số lượng bản sao pod mong muốn

Các thành phần này tồn tại vì chính dashboard UI chạy như một ứng dụng trong Kubernetes.

### Hiểu Về Quyền Hạn

Để xem quyền hạn của admin-user:
1. Đi đến **Service Accounts** trong namespace kubernetes-dashboard
2. Nhấp vào **admin-user**
3. Điều hướng đến **Cluster Role Bindings**
4. Nhấp vào binding **admin-user**
5. Xem chi tiết role **cluster-admin**

Role cluster-admin hiển thị:
- **Resources**: `*` (tất cả tài nguyên)
- **Verbs**: `*` (tất cả hành động)
- **API Groups**: `*` (tất cả nhóm API)

Điều này có nghĩa là người dùng có quyền truy cập super-user với đầy đủ quyền hạn trên toàn bộ cluster.

## Thực Hành Tốt Nhất

1. **Bảo Mật**: Trong môi trường production, tránh sử dụng role cluster-admin. Tạo các role cụ thể với quyền hạn giới hạn dựa trên nguyên tắc quyền tối thiểu (principle of least privilege).

2. **Quản Lý Token**: Lưu trữ token dài hạn của bạn một cách an toàn. Đừng chia sẻ nó hoặc commit nó vào version control.

3. **Truy Cập Dashboard**: Trong production, sử dụng các cơ chế xác thực phù hợp và hạn chế truy cập dashboard thông qua network policies.

4. **Cập Nhật Thường Xuyên**: Thường xuyên cập nhật Helm, kubectl và Kubernetes Dashboard để có các bản vá bảo mật và tính năng mới.

## Khắc Phục Sự Cố

### Không Thể Truy Cập Dashboard
- Đảm bảo lệnh port-forward đang chạy
- Kiểm tra xem Kubernetes cluster của bạn có đang chạy không
- Xác minh Docker Desktop đã được cập nhật

### Lỗi Token Không Hợp Lệ
- Đảm bảo bạn đã sao chép toàn bộ token mà không có ký tự theo sau
- Xác minh token chưa hết hạn (nếu sử dụng token ngắn hạn)
- Xác nhận secret đã được tạo thành công

### Bị Từ Chối Quyền
- Xác minh ClusterRoleBinding đã được áp dụng đúng cách
- Kiểm tra xem service account có tồn tại trong namespace đúng không

## Tóm Tắt

Bạn đã thiết lập thành công Kubernetes Dashboard với:
1. ✅ Helm package manager đã được cài đặt
2. ✅ Kubernetes Dashboard đã được triển khai
3. ✅ Admin service account được tạo với quyền cluster-admin
4. ✅ Token xác thực dài hạn đã được tạo
5. ✅ Truy cập đầy đủ vào Kubernetes Dashboard UI

Dashboard cung cấp một cách trực quan để quản lý và giám sát Kubernetes cluster của bạn, bổ sung cho giao diện dòng lệnh kubectl.

## Các Bước Tiếp Theo

- Khám phá các tính năng và views khác nhau của dashboard
- Tìm hiểu chi tiết hơn về Helm
- Thực hành triển khai ứng dụng thông qua dashboard
- Nghiên cứu Kubernetes RBAC (Role-Based Access Control) cho bảo mật production

---

**Tài Liệu Tham Khảo:**
- [Tài Liệu Kubernetes Dashboard Chính Thức](https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/)
- [Trang Web Helm Chính Thức](https://helm.sh)
- Tài Liệu Kubernetes RBAC

Cảm ơn bạn đã theo dõi hướng dẫn này! Chúc bạn học Kubernetes vui vẻ!