# Xác Thực và Triển Khai Helm Charts cho Microservices

## Tổng Quan

Hướng dẫn này trình bày cách xác thực Helm charts trước khi triển khai bằng lệnh `helm template`, khắc phục các lỗi thường gặp và chuẩn bị triển khai microservices lên Kubernetes cluster.

## Yêu Cầu Tiên Quyết

- Đã cài đặt và cấu hình Helm
- Các Helm charts tùy chỉnh cho microservices EasyBank
- Quyền truy cập Terminal vào thư mục dự án

## Xác Thực Helm Charts với helm template

### Mục Đích

Trước khi cài đặt Helm charts vào Kubernetes cluster, việc xác thực các file manifest Kubernetes sẽ được tạo ra là rất quan trọng. Lệnh `helm template` cho phép bạn xem trước các file này mà không thực sự triển khai chúng.

### Sử Dụng Lệnh helm template

1. **Di chuyển đến thư mục Helm chart**
   ```bash
   cd dev-env
   ```

2. **Chạy lệnh template**
   ```bash
   helm template .
   ```
   
   Dấu chấm (`.`) cho Helm biết rằng template nằm trong thư mục hiện tại.

### Kết Quả Mong Đợi

Lệnh này tạo ra tất cả các file manifest Kubernetes mà Helm sẽ tạo, bao gồm:
- Cấu hình Deployment
- Định nghĩa Service
- ConfigMaps
- Biến môi trường

## Khắc Phục Các Lỗi Thường Gặp

### Lỗi Cấu Hình Service Port

**Vấn đề:** Lỗi trong file template `common.service` nằm trong chart `easybank-common`.

**Triệu chứng:** Tên biến cho port chứa ký tự đặc biệt: `value.special_character.port`

**Giải pháp:**
1. Di chuyển đến templates của chart:
   ```
   easybank-common/templates/service.yaml
   ```

2. Sửa biến port từ:
   ```yaml
   port: {{ .Values.special_character.port }}
   ```
   
   Thành:
   ```yaml
   port: {{ .Values.service.port }}
   ```

## Biên Dịch Lại Helm Charts Sau Khi Thay Đổi

Khi bạn thay đổi common chart (`easybank-common`), tất cả các charts phụ thuộc phải được biên dịch lại.

### Biên Dịch Lại Charts của Từng Microservice

Di chuyển đến thư mục Helm chart của mỗi microservice và chạy:

```bash
cd easybank-services/accounts
helm dependency build
```

Lặp lại quy trình này cho tất cả các microservices phụ thuộc vào `easybank-common`.

### Biên Dịch Lại Environment Charts

Sau khi cập nhật microservice charts, biên dịch lại các charts theo môi trường:

**Môi Trường Development:**
```bash
cd environments/dev-env
helm dependency build
```

**Môi Trường QA:**
```bash
cd environments/qa-env
helm dependency build
```

**Môi Trường Production:**
```bash
cd environments/prod-env
helm dependency build
```

## Xác Thực Manifests Được Tạo Ra

### Ví dụ: Message Microservice

Sau khi chạy `helm template`, bạn có thể xem xét deployment được tạo:

```yaml
metadata:
  name: message-deployment
spec:
  replicas: 1
  # Các biến môi trường và cấu hình khác
```

### Xác Thực Theo Môi Trường

Các môi trường khác nhau sẽ tạo ra tên tài nguyên khác nhau:

**Môi Trường Production:**
```bash
cd prod-env
helm template .
```
Kết quả bao gồm: `easybank-prod-configmap`

**Môi Trường Development:**
```bash
cd dev-env
helm template .
```
Kết quả bao gồm: `easybank-dev-configmap`

## Yêu Cầu Trước Khi Triển Khai

Trước khi triển khai microservices lên Kubernetes, đảm bảo các thành phần sau đã được thiết lập:

### Các Thành Phần Hạ Tầng Cần Thiết

1. **Keycloak** - Quản lý định danh và truy cập
2. **Apache Kafka** - Nền tảng streaming sự kiện
3. **Grafana** - Giám sát và quan sát

### Sử Dụng Helm Charts Có Sẵn

Bạn không cần tạo Helm charts thủ công cho các thành phần này. Chúng được sử dụng rộng rãi trong ngành, và các cộng đồng mã nguồn mở đã xây dựng Helm charts cho:
- Kafka
- Keycloak
- Grafana

Các charts này có thể được cài đặt trực tiếp từ các Helm repositories.

## Các Bước Tiếp Theo

1. Thiết lập các thành phần hạ tầng (Keycloak, Kafka, Grafana) sử dụng Helm charts có sẵn
2. Triển khai môi trường bạn chọn (dev, qa, hoặc prod) bằng cách cài đặt environment Helm chart tương ứng
3. Xác minh tất cả microservices đang chạy chính xác
4. Giám sát việc triển khai sử dụng Grafana dashboards

## Thực Hành Tốt

- Luôn xác thực Helm charts bằng `helm template` trước khi cài đặt
- Biên dịch lại tất cả charts phụ thuộc sau khi sửa đổi common charts
- Kiểm tra triển khai trong môi trường development trước khi đưa lên QA và production
- Giữ các cấu hình theo môi trường riêng biệt
- Sử dụng version control cho tất cả thay đổi Helm chart

## Tóm Tắt

Lệnh `helm template` là công cụ xác thực quan trọng cho phép bạn xem trước các file manifest Kubernetes trước khi triển khai. Bằng cách phát hiện lỗi sớm và xác thực cấu hình trên các môi trường khác nhau, bạn có thể đảm bảo việc triển khai kiến trúc microservices của mình diễn ra suôn sẻ.