# Tạo Helm Chart cho Microservice Accounts

## Tổng quan

Hướng dẫn này trình bày cách tạo Helm chart cho microservice accounts bằng cách tận dụng Helm chart `easybank-common`, nơi chứa tất cả các file template Kubernetes manifest cần thiết.

## Yêu cầu trước

- Helm chart `easybank-common` với các template đã được định nghĩa sẵn
- Hiểu biết cơ bản về Helm charts và Kubernetes
- Microservice accounts đã sẵn sàng để triển khai

## Bước 1: Tạo cấu trúc dự án

Đầu tiên, tạo một thư mục mới có tên `easybank-services` để tổ chức tất cả các Helm chart của microservices:

```bash
mkdir easybank-services
cd easybank-services
```

## Bước 2: Tạo Helm Chart

Tạo một Helm chart mới cho microservice accounts:

```bash
helm create accounts
```

Lệnh này tạo một thư mục có tên `accounts` với cấu trúc Helm chart mặc định.

## Bước 3: Dọn dẹp các file mặc định

Xóa các file template mặc định và xóa nội dung của `values.yaml`, vì chúng ta sẽ định nghĩa riêng:

1. Xóa tất cả các file trong thư mục `templates/`
2. Xóa nội dung của file `values.yaml`

## Bước 4: Cấu hình Chart.yaml

Mở file `chart.yaml` và cập nhật với cấu hình sau:

```yaml
apiVersion: v2
name: accounts
description: Helm chart cho accounts microservice
version: 1.0.0
appVersion: "1.0.0"

dependencies:
  - name: easybank-common
    version: 0.1.0
    repository: file://../../easybank-common
```

### Các điểm chính:

- **name**: Tên của chart (accounts)
- **version**: Cập nhật lên 1.0.0
- **dependencies**: Định nghĩa phụ thuộc vào chart `easybank-common`
- **repository**: Sử dụng giao thức `file://` với đường dẫn tương đối (`../../`) để tham chiếu đến common chart cục bộ

Ký hiệu `../../` điều hướng lên hai thư mục từ vị trí hiện tại để tìm chart `easybank-common`.

## Bước 5: Thêm các file Template

Tạo hai file template trong thư mục `templates/`:

### deployment.yaml

```yaml
{{ include "common.deployment" . }}
```

### service.yaml

```yaml
{{ include "common.service" . }}
```

Các template này tham chiếu đến các template chung được định nghĩa trong chart `easybank-common`:
- `common.deployment` - Template cho Kubernetes Deployment
- `common.service` - Template cho Kubernetes Service

Cách tiếp cận này cho phép tái sử dụng cấu hình chung trên nhiều microservices.

## Bước 6: Cấu hình values.yaml

Điền vào `values.yaml` với cấu hình sau:

```yaml
deploymentName: accounts-deployment
serviceName: accounts-service
appLabel: accounts
appName: accounts
replicaCount: 1

image:
  repository: eazybank/accounts
  tag: s14

containerPort: 8080

service:
  type: ClusterIP
  port: 8080
  targetPort: 8080

# Các cờ biến môi trường
appNameEnabled: true
profileEnabled: true
configEnabled: true
eurekaEnabled: true
resourceServerEnabled: false
otelEnabled: true
kafkaEnabled: true
```

### Chi tiết cấu hình:

#### Cài đặt cơ bản
- **deploymentName**: Tên cho Kubernetes Deployment
- **serviceName**: Tên cho Kubernetes Service
- **appLabel**: Label được sử dụng để xác định ứng dụng
- **appName**: Tên ứng dụng (được sử dụng làm `spring.application.name`)
- **replicaCount**: Số lượng pod replica

#### Cấu hình Image
- **image.repository**: Repository của Docker image
- **image.tag**: Tag của image (s14 đề cập đến section 14 với implementation Kafka)

#### Cấu hình Port
- **containerPort**: Port mà container lắng nghe (8080)
- **service.type**: ClusterIP (chỉ truy cập nội bộ, không expose ra bên ngoài)
- **service.port**: Port của Service
- **service.targetPort**: Port đích trên pod

#### Các cờ biến môi trường

Các cờ boolean này kiểm soát biến môi trường nào được inject:

- **appNameEnabled**: Inject biến môi trường `SPRING_APPLICATION_NAME`
- **profileEnabled**: Kích hoạt cấu hình Spring profiles
- **configEnabled**: Kích hoạt kết nối đến Config Server
- **eurekaEnabled**: Kích hoạt service discovery của Eureka
- **resourceServerEnabled**: Đặt thành `false` vì chỉ Gateway đóng vai trò là OAuth2 resource server
- **otelEnabled**: Kích hoạt OpenTelemetry cho logging đến Grafana và distributed tracing đến Grafana Tempo
- **kafkaEnabled**: Kích hoạt kết nối Kafka cho giao tiếp event-driven với message microservice

## Bước 7: Build Helm Dependencies

Biên dịch Helm chart và tải về các dependencies:

```bash
cd accounts
helm dependency build
```

Lệnh này thực hiện:
1. Biên dịch Helm chart accounts
2. Tải về và đóng gói các chart phụ thuộc (easybank-common)
3. Đặt dependency đã nén vào thư mục `charts/`

Sau khi thực thi, bạn sẽ thấy một file nén như `easybank-common-0.1.0.tgz` trong thư mục `charts/`.

## Các lưu ý quan trọng

### Tại sao cần các file Template

Mặc dù các template đã được định nghĩa trong `easybank-common`, chúng ta vẫn cần các file template trong chart accounts. Các file này hoạt động như các tham chiếu để include các template chung:

```yaml
{{ include "common.deployment" . }}
```

Cú pháp này import template từ dependency chart.

### Service Type: ClusterIP

Service type được đặt thành ClusterIP vì:
- Microservice accounts không nên được expose ra bên ngoài
- Chỉ Gateway server cần truy cập từ bên ngoài
- Các microservice nội bộ giao tiếp trong cluster

### Helm Dependency Build

Lệnh `helm dependency build` phải được chạy cho bất kỳ chart nào có dependencies. Chart `easybank-common` không yêu cầu lệnh này vì nó không có dependencies.

## Xác minh

Sau khi build, xác minh cấu trúc:

```
accounts/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── deployment.yaml
│   └── service.yaml
└── charts/
    └── easybank-common-0.1.0.tgz
```

## Các bước tiếp theo

Lặp lại quy trình này cho tất cả các microservices còn lại trong kiến trúc của bạn, tùy chỉnh `values.yaml` cho các yêu cầu cụ thể của từng service.

## Tóm tắt

Bạn đã tạo thành công một Helm chart cho microservice accounts với:
- Tận dụng các template được chia sẻ từ easybank-common
- Định nghĩa các cấu hình cụ thể cho service
- Duy trì dependencies đúng cách
- Sẵn sàng để triển khai Kubernetes

Mẫu này có thể được nhân rộng cho tất cả các microservices trong hệ thống, đảm bảo tính nhất quán và khả năng tái sử dụng trong toàn bộ cơ sở hạ tầng triển khai của bạn.