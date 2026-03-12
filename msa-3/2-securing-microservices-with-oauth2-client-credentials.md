# Bảo Mật Microservices với OAuth2 Client Credentials Grant Flow

## Tổng Quan

Hướng dẫn này giải thích cách bảo mật kiến trúc microservices Spring Boot sử dụng OAuth2 Client Credentials Grant Type Flow. Chúng ta sẽ tập trung vào việc bảo vệ Gateway Server (Edge Server) - điểm vào của mạng lưới microservices.

## Các Thành Phần Kiến Trúc

### 1. Ứng Dụng Client
- Dịch vụ bên ngoài, API, hoặc backend server
- Cố gắng kết nối với mạng lưới microservices
- Phải đăng ký với authorization server

### 2. Authorization Server (Keycloak)
- Quản lý xác thực và phân quyền
- Phát hành access token cho các client đã đăng ký
- Xác thực access token

### 3. Gateway Server (Resource Server)
- Hoạt động như edge server cho microservices
- Xác thực access token trước khi chuyển tiếp yêu cầu
- Định tuyến yêu cầu đến các microservices nội bộ

### 4. Microservices Nội Bộ
- Các microservices: Accounts, Loans, và Cards
- Được bảo vệ phía sau firewall/Docker network
- Không thể truy cập trực tiếp từ bên ngoài

## Luồng OAuth2 Client Credentials

### Quy Trình Từng Bước

#### Bước 1: Client Yêu Cầu Access Token
```
Client → Auth Server
- Gửi: Client ID và Client Secret
- Nhận: Access Token (và ID Token nếu hỗ trợ OpenID)
```

Ứng dụng client phải:
- Đăng ký với Keycloak
- Được phê duyệt bởi quản trị viên Keycloak
- Nhận thông tin xác thực hợp lệ (Client ID và Client Secret)

#### Bước 2: Client Gọi Gateway Kèm Access Token
```
Client → Gateway Server
- Gửi: Yêu cầu API + Access Token
```

#### Bước 3: Gateway Xác Thực Access Token
```
Gateway → Auth Server
- Gửi: Access Token để xác thực
- Nhận: Xác nhận hợp lệ
```

Gateway Server:
- Nhận access token từ client
- Xác thực với authorization server
- Đảm bảo chỉ những client đã xác thực mới được tiếp tục

#### Bước 4: Chuyển Tiếp Yêu Cầu
```
Gateway → Internal Microservices
- Chuyển tiếp yêu cầu đã xác thực đến microservices Accounts/Loans/Cards
```

#### Bước 5: Trả Về Kết Quả
```
Internal Microservices → Gateway → Client
- Kết quả chảy ngược qua gateway về client
```

## Quyết Định Thiết Kế Bảo Mật

### Tại Sao Chỉ Bảo Mật Gateway?

**Câu hỏi**: Tại sao không biến các microservices riêng lẻ (Accounts, Loans, Cards) thành resource servers?

**Trả lời**: 

1. **Cô Lập Mạng**: Các microservices nội bộ được triển khai phía sau:
   - Firewalls
   - Docker networks
   - Kubernetes clusters
   
   Điều này ngăn chặn truy cập trực tiếp từ bên ngoài.

2. **Ảnh Hưởng Hiệu Suất**: Biến tất cả microservices thành resource servers sẽ:
   - Yêu cầu xác thực access token cho mọi request
   - Bao gồm cả giao tiếp nội bộ giữa các microservices
   - Gây ra overhead hiệu suất không cần thiết
   - Tăng độ phức tạp của hệ thống

3. **Kiến Trúc Đơn Giản Hóa**: 
   - Chỉ Gateway cần xác thực token
   - Giao tiếp nội bộ vẫn hiệu quả
   - Phân tách trách nhiệm tốt hơn

### Bảo Mật Mạng

Các client bên ngoài **không thể** gọi trực tiếp các microservices nội bộ vì:
- Microservices được triển khai trong mạng cô lập (Docker/Kubernetes)
- Chỉ Gateway Server tồn tại trong cùng mạng
- Client không có lựa chọn nào khác ngoài định tuyến qua Gateway

### Bảo Mật Microservices Nội Bộ

Mặc dù các microservices nội bộ không phải là OAuth2 resource servers, chúng vẫn nên được bảo mật bằng:
- Service mesh security (ví dụ: Istio)
- mTLS (Mutual TLS)
- Network policies
- Các phương pháp tiêu chuẩn công nghiệp khác (được đề cập khi triển khai Kubernetes)

## Khi Nào Sử Dụng Client Credentials Grant Type

Grant type này phù hợp khi:
- ✅ Hai ứng dụng backend/APIs giao tiếp với nhau
- ✅ Không có người dùng cuối tham gia
- ✅ Không có ứng dụng frontend tham gia
- ✅ Giao tiếp máy-với-máy (machine-to-machine)
- ✅ Xác thực dịch vụ-với-dịch vụ (service-to-service)

KHÔNG phù hợp khi:
- ❌ Người dùng cuối cần xác thực
- ❌ Ứng dụng trình duyệt tham gia
- ❌ Cần sự đồng ý của người dùng

## Các Bước Triển Khai

Các chủ đề sau sẽ được đề cập trong các bài giảng tiếp theo:

1. **Thiết Lập Keycloak làm Authorization Server**
   - Cài đặt và cấu hình
   - Thiết lập Realm và client

2. **Cấu Hình Spring Cloud Gateway làm Resource Server**
   - Thêm dependencies OAuth2
   - Cấu hình bảo mật
   - Thiết lập xác thực token

3. **Đăng Ký Ứng Dụng Client trong Keycloak**
   - Tạo client credentials
   - Cấu hình quyền và scope

4. **Kiểm Thử OAuth2 Flow**
   - Lấy access tokens
   - Thực hiện các yêu cầu đã xác thực
   - Xử lý hết hạn token

## Tóm Tắt

- Gateway Server hoạt động như điểm vào duy nhất và resource server
- Các ứng dụng client phải lấy access token từ Keycloak
- Access token được xác thực trước khi yêu cầu đến microservices nội bộ
- Các microservices nội bộ được bảo vệ bởi cô lập mạng
- Phương pháp này cân bằng giữa bảo mật, hiệu suất và sự đơn giản

## Những Điểm Chính Cần Nhớ

1. **Client Credentials Grant Type** hoàn hảo cho giao tiếp API-to-API
2. **Bảo mật cấp Gateway** cung cấp xác thực tập trung
3. **Cô lập mạng** bảo vệ các microservices nội bộ
4. **Tối ưu hiệu suất** bằng cách tránh xác thực token dư thừa
5. **Best practices công nghiệp** cho bảo mật microservices

---

*Bài Giảng Tiếp Theo: Thiết Lập Keycloak Authorization Server*