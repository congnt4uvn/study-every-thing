# Cấu Trúc và Quản Lý Helm Chart

## Tổng Quan

Hướng dẫn này giải thích cấu trúc chuẩn của Helm chart và trình bày cách quản lý các bản cài đặt Helm trong Kubernetes, sử dụng WordPress làm ví dụ trước khi chuyển sang triển khai microservices.

## Cấu Trúc Helm Chart

Bất kỳ Helm chart nào cũng tuân theo một cấu trúc được định nghĩa trước, dù bạn tự tạo hay sử dụng chart của bên thứ ba.

### Cấu Trúc Thư Mục

```
wordpress/                    # Thư mục cha (tên chart)
├── Chart.yaml               # Metadata của chart
├── values.yaml              # Cấu hình giá trị động
├── charts/                  # Các chart phụ thuộc
└── templates/               # Template manifest Kubernetes
```

### Các Thành Phần Chính

#### 1. Chart.yaml
File này chứa thông tin metadata về Helm chart:
- Phiên bản chart
- Phiên bản API
- Phiên bản ứng dụng
- Các phụ thuộc vào chart khác
- Mô tả
- Thông tin người duy trì
- Repository nguồn

**Ví dụ từ WordPress chart:**
```yaml
apiVersion: v2
appVersion: "6.3.1"
dependencies:
  - name: memcached
  - name: mariadb
  - name: common
description: "WordPress là nền tảng blog và quản lý nội dung phổ biến nhất thế giới"
version: 17.1.4
```

#### 2. values.yaml
Chứa tất cả các giá trị động sẽ được inject vào các file template tại runtime. Đây là các cặp key-value để cấu hình:
- Chi tiết Docker image
- Giới hạn tài nguyên
- Cấu hình service
- Cài đặt theo môi trường cụ thể

Tất cả các giá trị được định nghĩa ở đây sẽ được Helm chart sử dụng tại runtime để chuẩn bị các file manifest Kubernetes dựa trên các template.

#### 3. Thư Mục charts/
Chứa các Helm chart khác mà chart hiện tại phụ thuộc vào. Mỗi phụ thuộc tự nó là một Helm chart hoàn chỉnh với cấu trúc riêng.

**Ví dụ:** WordPress chart phụ thuộc vào:
- `common` - Tiện ích chung
- `mariadb` - Cơ sở dữ liệu
- `memcached` - Lớp caching

#### 4. Thư Mục templates/
Chứa các file template manifest Kubernetes:
- `deployment.yaml` - Cấu hình Deployment
- `service.yaml` - Định nghĩa Service
- `configmap.yaml` - Template ConfigMap
- `secret.yaml` - Template Secret
- Và nhiều hơn nữa...

Các template này tuân theo cú pháp manifest Kubernetes chuẩn nhưng bao gồm việc inject giá trị động từ `values.yaml`.

**Ví dụ cấu trúc deployment.yaml:**
- Sử dụng cú pháp deployment Kubernetes chuẩn
- Inject các giá trị runtime từ `values.yaml`
- Hỗ trợ tất cả các file template, không chỉ deployment

### Các File Bổ Sung
- `.helmignore` - File cần bỏ qua (do Helm quản lý)
- `Chart.lock` - File khóa phụ thuộc (do Helm quản lý)
- `values.schema.json` - Schema xác thực values (tùy chọn)

## Quản Lý Helm Release

### Liệt Kê Các Release Đã Cài Đặt

```bash
helm ls
```

**Kết quả bao gồm:**
- Tên release
- Namespace
- Số revision
- Trạng thái (deployed, failed, v.v.)
- Tên và phiên bản chart
- Phiên bản ứng dụng

**Ví dụ kết quả:**
```
NAME         NAMESPACE   REVISION   STATUS     CHART              APP VERSION
happy-panda  default     1          deployed   wordpress-17.1.4   6.3.1
```

**Lưu ý:** Phiên bản chart (17.1.4) đề cập đến chính Helm chart, trong khi phiên bản app (6.3.1) đề cập đến ứng dụng WordPress được triển khai.

### Gỡ Cài Đặt Release

```bash
helm uninstall <tên-release>
```

**Ví dụ:**
```bash
helm uninstall happy-panda
```

Lệnh đơn giản này sẽ xóa:
- Tất cả deployment
- Tất cả pod
- Tất cả replica set
- Tất cả service
- Tất cả config map
- Tất cả secret
- Tất cả tài nguyên khác được tạo bởi chart

### Xác Minh

Sau khi gỡ cài đặt, xác minh thông qua Kubernetes dashboard:
- Không có workload nào được hiển thị
- Không có deployment
- Không có pod
- Không có replica set
- Service đã bị xóa
- Config map đã bị xóa
- Secret đã bị xóa

## Tạo Helm Chart Tùy Chỉnh Cho Microservices

### Tại Sao Cần Tạo Chart Tùy Chỉnh?

Các Helm chart của bên thứ ba như WordPress sẵn có, nhưng đối với microservices tùy chỉnh:
- Không có chart được xây dựng sẵn
- Yêu cầu kinh doanh là duy nhất
- Cần các file manifest Kubernetes tùy chỉnh

### Lợi Ích của Helm Chart Tùy Chỉnh

1. **Triển Khai Bằng Lệnh Đơn** - Triển khai tất cả microservices với một lệnh
2. **Quản Lý Môi Trường** - Duy trì các file `values.yaml` riêng cho các môi trường khác nhau
3. **Kiểm Soát Phiên Bản** - Theo dõi phiên bản chart cùng với code
4. **Tái Sử Dụng** - Sử dụng cùng cấu trúc chart cho nhiều triển khai

### Các Bước Tiếp Theo

Cho Eazy Bytes Microservices:
1. Tạo cấu trúc Helm chart tùy chỉnh
2. Định nghĩa các template phù hợp cho tất cả microservices
3. Cấu hình `values.yaml` cho các môi trường khác nhau
4. Triển khai sử dụng lệnh Helm

## Tóm Tắt

Helm chart cung cấp một cách mạnh mẽ để quản lý triển khai Kubernetes:
- **Cấu trúc chuẩn hóa** làm cho chart dễ dự đoán và bảo trì
- **Inject giá trị động** cho phép cấu hình theo môi trường cụ thể
- **Lệnh đơn giản** để cài đặt và gỡ cài đặt
- **Quản lý phụ thuộc** xử lý các stack ứng dụng phức tạp

Sức mạnh của Helm nằm ở khả năng quản lý toàn bộ stack ứng dụng bằng các lệnh đơn giản, làm cho nó lý tưởng cho kiến trúc microservices.

---

*Hướng dẫn này là một phần của loạt bài về triển khai microservices với Kubernetes và Helm.*