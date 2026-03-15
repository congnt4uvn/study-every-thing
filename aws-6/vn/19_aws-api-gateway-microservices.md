# AWS API Gateway - Kiến Trúc Microservice

## Tổng Quan

API Gateway cung cấp một giao diện duy nhất cho tất cả các microservices trong tổ chức của bạn, cho phép bạn sử dụng các API endpoints với nhiều tài nguyên backend khác nhau trong khi ẩn đi sự phức tạp từ phía clients.

## Các Thành Phần Kiến Trúc Chính

### 1. API Gateway Làm Giao Diện Trung Tâm

API Gateway hoạt động như một điểm vào thống nhất, định tuyến các requests đến các backend services khác nhau:

- **URL duy nhất** cho tất cả các services
- **Nhiều đường dẫn định tuyến** đến các backends khác nhau
- **Tích hợp client đơn giản hóa**

### 2. Tích Hợp Backend Services

API Gateway có thể định tuyến đến nhiều AWS services khác nhau:

#### Ví Dụ Về Routes:
- **`/service1`** → Elastic Load Balancer (ELB) → ECS Cluster (microservices)
- **`/docs`** → S3 Bucket (tài liệu và nội dung học tập)
- **`/service2`** → ELB → EC2 Auto Scaling Group

### 3. Quản Lý Domain với Route 53

Route 53 tích hợp với API Gateway để cung cấp:

- **Tên miền tùy chỉnh** thay vì DNS mặc định của API Gateway
- **Hỗ trợ đa khách hàng (multi-tenant)**:
  - `customer1.example.com` cho Khách hàng 1
  - `customer2.example.com` cho Khách hàng 2
- **Quản lý chứng chỉ SSL** cho từng domain

### 4. Tính Năng Của API Gateway

#### Chuyển Đổi Dữ Liệu
- Áp dụng các quy tắc forwarding
- Chuyển đổi dữ liệu đến trước khi gửi đến backends
- Sửa đổi cấu trúc request/response

#### Bảo Mật
- Áp dụng chứng chỉ SSL/TLS cho từng domain
- Xác thực và phân quyền
- Quản lý API key

## Lợi Ích

1. **Giao Diện Thống Nhất**: Điểm vào duy nhất cho tất cả microservices
2. **Ẩn Sự Phức Tạp**: Clients không cần biết chi tiết backend
3. **Định Tuyến Linh Hoạt**: Dễ dàng thêm/sửa đổi service endpoints
4. **Chuyển Đổi Dữ Liệu**: Sửa đổi dữ liệu tại tầng gateway
5. **Quản Lý Bảo Mật**: SSL và xác thực tập trung

## Tóm Tắt Mô Hình Kiến Trúc

```
Yêu Cầu Từ Client
    ↓
Route 53 (Domain Tùy Chỉnh)
    ↓
API Gateway (Định Tuyến, Chuyển Đổi, SSL)
    ↓
    ├─ /service1 → ELB → ECS Cluster
    ├─ /docs → S3 Bucket
    └─ /service2 → ELB → EC2 Auto Scaling
```

## Các Trường Hợp Sử Dụng

- Kiến trúc microservices với nhiều backend services
- Ứng dụng đa khách hàng (multi-tenant) với domains riêng biệt
- Phiên bản API và tích hợp legacy services
- Quản lý và giám sát API tập trung

---

**Lưu Ý**: Mô hình kiến trúc này lý tưởng khi bạn muốn hợp nhất các microservices và cung cấp một URL thống nhất ra bên ngoài trong khi ẩn đi tất cả sự phức tạp về định tuyến, chuyển đổi dữ liệu và quản lý chứng chỉ SSL tại tầng API Gateway.
