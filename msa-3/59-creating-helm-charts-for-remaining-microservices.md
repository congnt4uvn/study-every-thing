# Tạo Helm Charts cho các Microservices còn lại

## Tổng quan

Trong hướng dẫn này, chúng ta sẽ tạo Helm charts cho tất cả các microservices còn lại trong ứng dụng Spring Boot. Sau khi đã tạo Helm chart cho Accounts microservice, chúng ta sẽ sao chép và tùy chỉnh nó cho Cards, Config Server, Eureka Server, Gateway Server, Loans và Message microservices.

## Tạo Helm Charts bằng cách Sao chép

Thay vì tạo từng Helm chart từ đầu, chúng ta có thể tận dụng Helm chart của Accounts hiện có:

1. **Sao chép Helm chart của Accounts** vào cùng thư mục
2. **Đổi tên** nó thành microservice đích (ví dụ: "cards")
3. **Tùy chỉnh** các file cấu hình

### Quy trình từng bước

#### 1. Chỉnh sửa Chart.yaml

Mở file `Chart.yaml` và cập nhật tên:

```yaml
name: cards  # Đổi từ 'accounts'
```

Không cần thay đổi gì khác trong file này.

#### 2. Hiểu về Cấu trúc Thư mục

- **templates/**: Chứa các templates chung - không cần thay đổi
- **charts/**: Chứa các dependencies đã biên dịch (EasyBank Common) - không cần thay đổi
- **Chart.lock**: Được tạo bởi Helm trong quá trình biên dịch
- **values.yaml**: Cần tùy chỉnh cho từng microservice

> **Lưu ý**: Nếu gặp vấn đề khi biên dịch, bạn có thể xóa `Chart.lock` và biên dịch lại.

#### 3. Tùy chỉnh values.yaml

Cập nhật file `values.yaml` với các giá trị cụ thể cho từng microservice:

```yaml
deploymentName: cards-deployment
serviceName: cards-service
appLabel: cards
appName: cards
replicaCount: 1
image:
  name: easybytes/cards
  tag: latest
containerPort: 9000
port: 9000
targetPort: 9000
serviceType: ClusterIP
```

## Cấu hình cho từng Microservice

### Cards Microservice

**Cấu hình chính:**
- Container Port: `9000`
- Service Type: `ClusterIP`
- Kafka Enabled: `false` (Cards không kết nối với Kafka)

### Config Server

**Cấu hình values.yaml:**

```yaml
deploymentName: configserver-deployment
serviceName: configserver-service
appLabel: configserver
appName: configserver
image:
  name: easybytes/configserver
containerPort: 8071
serviceType: ClusterIP
```

**Các giá trị Boolean:**
- `profileEnabled: false` - Config server tải properties của tất cả profiles
- `configEnabled: false` - Config server không cần URL config của chính nó
- `eurekaEnabled: false`
- `resourceServerEnabled: false`
- `otelEnabled: true`
- `kafkaEnabled: false`

> **Tại sao profile bị vô hiệu hóa**: Config server quản lý properties cho tất cả profiles. Các microservices riêng lẻ cần thuộc tính profile để lấy cấu hình cụ thể từ Spring Cloud Config Server.

### Eureka Server

**Cấu hình chính:**
- Container Port: `8070`

**Các giá trị Boolean:**
- `appNameEnabled: true`
- `profileEnabled: false`
- `configEnabled: true`
- `eurekaEnabled: false`
- `resourceServerEnabled: false`
- `otelEnabled: true`
- `kafkaEnabled: false`

### Gateway Server

**Cấu hình chính:**
- Service Type: `LoadBalancer` (được expose ra ngoài cho các client)

**Các giá trị Boolean:**
- `resourceServerEnabled: true` - Gateway hoạt động như OAuth2 resource server

> **Quan trọng**: Gateway là microservice duy nhất được cấu hình làm resource server trong kiến trúc này.

### Loans Microservice

**Cấu hình chính:**
- Container Port: `8090`
- Image: `easybytes/loans`

Cấu hình tương tự như Cards và Accounts microservices, với số port và tên image là điểm khác biệt chính.

### Message Microservice

**Cấu hình chính:**
- Container Port: `9010`
- Được xây dựng với Spring Cloud Functions và Spring Cloud Stream

**Các giá trị Boolean:**
- `profileEnabled: false`
- `configEnabled: false`
- `eurekaEnabled: false`
- `otelEnabled: false`
- `kafkaEnabled: true` - Message microservice sử dụng Kafka

## Biên dịch lại Helm Charts

### Khi nào cần Biên dịch lại

Bạn không cần biên dịch lại nếu:
- Các dependent charts đã có sẵn ở dạng nén
- Bạn đang sử dụng cùng một EasyBank Common Helm chart

### Cách Biên dịch lại

Nếu cần, chạy lệnh sau trong thư mục Helm chart của microservice:

```bash
helm dependency build
```

Lệnh này sẽ:
- Xóa các charts cũ
- Thay thế bằng các phiên bản mới được biên dịch

**Lưu ý**: Cùng một EasyBank Common Helm chart đã nén từ Accounts microservice sẽ được sử dụng cho tất cả các microservices.

## Helm Chart theo Môi trường

### Thách thức

Việc cài đặt từng Helm chart theo cách thủ công (accounts, cards, config server, v.v.) rất tẻ nhạt và dễ xảy ra lỗi.

### Giải pháp

Tạo một **Helm chart theo môi trường** để:
1. Định nghĩa tất cả các giá trị liên quan đến ConfigMap
2. Khai báo dependencies trên tất cả các Helm charts của microservices
3. Cho phép triển khai bằng một lệnh duy nhất

Cách tiếp cận này sẽ làm cho hệ sinh thái Helm dễ quản lý hơn nhiều sau khi thiết lập ban đầu.

## Điểm chính cần nhớ

- **Thiết lập một lần**: Tạo Helm charts là hoạt động một lần giúp đơn giản hóa các lần triển khai sau
- **Tái sử dụng**: Templates và dependency charts có thể được tái sử dụng cho các microservices
- **Tùy chỉnh**: Chỉ có `values.yaml` cần sửa đổi cho từng microservice
- **Tự động hóa**: Helm charts theo môi trường cho phép triển khai bằng một lệnh
- **Nhất quán**: Sử dụng một common Helm chart đảm bảo tính nhất quán giữa tất cả microservices

## Các bước tiếp theo

Trong bài giảng tiếp theo, chúng ta sẽ khám phá:
- Tạo Helm charts theo môi trường
- Liên kết tất cả các Helm charts của microservices lại với nhau
- Demo quy trình triển khai hoàn chỉnh

---

**Lưu ý**: Thiết lập ban đầu đòi hỏi công sức thủ công, nhưng một khi đã cấu hình xong, hệ sinh thái Helm sẽ đơn giản hóa đáng kể việc triển khai và quản lý microservices.