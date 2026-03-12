# Thách Thức Về Service Discovery và Traditional Load Balancer Trong Microservices

## Giới Thiệu

Trong bài giảng này, chúng ta sẽ khám phá các thách thức và nhược điểm khi sử dụng phương pháp truyền thống của kiến trúc nguyên khối (monolithic) cho việc giao tiếp nội bộ trong môi trường microservices, đặc biệt khi các khái niệm service discovery và service registration không được sử dụng.

## Phương Pháp Giao Tiếp Truyền Thống

### Yêu Cầu Cơ Bản

Trong một mạng web, khi một service hoặc ứng dụng cần giao tiếp với service khác, nó cần các thông tin định vị thiết yếu như:
- **Địa chỉ IP**
- **Tên DNS** (Domain Name - Tên miền)

### Kịch Bản Đơn Giản: Giao Tiếp Giữa Hai Microservices

Hãy xem xét một kịch bản trong đó hai microservices, **Accounts** và **Loans**, cần giao tiếp với nhau:

#### Thuật Ngữ
- **Upstream Service**: Service phụ thuộc (ví dụ: Accounts microservice)
- **Downstream Service**: Service được phụ thuộc vào (ví dụ: Loans microservice)
- **Backing Service**: Một service mà service khác phải dựa vào để gửi phản hồi thành công

#### Cấu Hình Ví Dụ
- **Accounts Microservice**: Được triển khai như upstream service
- **Loans Microservice**: Được triển khai tại IP `127.54.37.23` như downstream service

### Phương Pháp Giao Tiếp

Accounts microservice có thể giao tiếp với Loans microservice bằng hai cách:

1. **Hardcode địa chỉ IP**: Nhúng trực tiếp địa chỉ IP vào code
2. **DNS/Hostname**: Sử dụng tên miền được ánh xạ tới địa chỉ IP

Phương pháp truyền thống này không sử dụng service discovery hay load balancing - chỉ đơn giản là giao tiếp trực tiếp qua hostname, DNS hoặc địa chỉ IP.

## Thách Thức Với Triển Khai Đơn Instance

### Khi Nào Hoạt Động Tốt

Phương pháp truyền thống hoạt động tốt khi:
- Chỉ có **một instance** của Loans microservice đang chạy
- Việc quản lý ánh xạ tên DNS sang địa chỉ IP là đơn giản
- Môi trường tương đối tĩnh

### Lợi Ích Của DNS

Sử dụng tên DNS thay vì hardcode địa chỉ IP mang lại:
- **Tính linh hoạt**: Thay đổi địa chỉ IP chỉ cần cập nhật ánh xạ DNS
- **Không cần thay đổi code**: Code của Accounts microservice không cần thay đổi khi IP thay đổi
- **Quản lý tập trung**: Đội ngũ platform/operations xử lý việc ánh xạ

## Vấn Đề Trong Môi Trường Cloud

### Thách Thức Với Nhiều Instances

Trong môi trường cloud với nhiều instances, phương pháp truyền thống thất bại vì:

1. **Nhiều địa chỉ IP**: Mỗi instance có địa chỉ IP riêng
2. **Quản lý DNS phức tạp**: Phải duy trì ánh xạ giữa DNS và nhiều địa chỉ IP
3. **Hạn chế của Round Robin**: Mặc dù các thuật toán như Round Robin có thể phân phối traffic, việc quản lý DNS records trở nên phức tạp

### Tại Sao Hoạt Động Tốt Cho Ứng Dụng Nguyên Khối

Phương pháp dựa trên DNS truyền thống phù hợp với ứng dụng monolithic/SOA vì:
- Số lượng services hạn chế
- Triển khai tĩnh trên máy vật lý hoặc VMs chạy lâu dài
- Địa chỉ IP không đổi trừ khi thay đổi thủ công

### Tại Sao Thất Bại Với Microservices

Môi trường microservices đối mặt với những thách thức đặc biệt:

#### 1. Thay Đổi Nhanh Chóng
- Containers được triển khai và hủy bỏ thường xuyên
- Auto-scaling đưa instances mới vào và loại bỏ chúng dựa trên traffic
- Instances lỗi được thay thế bằng instances mới có địa chỉ IP khác

#### 2. Bản Chất Tạm Thời (Ephemeral)
- **Ephemeral** nghĩa là có tuổi thọ ngắn và có thể bị hủy bất cứ lúc nào
- Containers có tuổi thọ ngắn hơn so với triển khai truyền thống
- Không thể duy trì DNS records chính xác với địa chỉ IP liên tục thay đổi

#### 3. Scale Động
- Scale up trong thời gian traffic cao
- Scale down trong thời gian traffic thấp
- Tự động thay thế instances không phản hồi

## Kiến Trúc Traditional Load Balancer

### Thiết Lập Điển Hình

```
Ứng Dụng Client
        ↓
    Tên DNS (services.easybank.com)
        ↓
Primary Load Balancer
        ↓
    Bảng Định Tuyến
        ↓
Microservices (Accounts, Cards, Loans)
        ↓
Secondary Load Balancer (Dự phòng)
```

### Cách Hoạt Động

1. **Yêu cầu từ Client**: Ứng dụng gọi microservices qua tên DNS
2. **Primary Load Balancer**: Xử lý các yêu cầu đến
3. **Bảng định tuyến**: Chứa ánh xạ địa chỉ IP được cấu hình thủ công
4. **Chuyển tiếp yêu cầu**: Định tuyến traffic đến microservices phù hợp
5. **Secondary Load Balancer**: Giám sát primary và thay thế nếu nó lỗi

## Nhược Điểm Của Traditional Load Balancers

### 1. Khả Năng Scale Ngang Hạn Chế và Chi Phí License

- **Cấu hình thủ công**: Địa chỉ IP phải được biết trước và cấu hình
- **Bảng định tuyến tĩnh**: Yêu cầu duy trì thủ công các địa chỉ IP
- **Không scale động**: Không thể thực hiện scale-up và scale-down động hiệu quả
- **Chi phí license**: Các nhà cung cấp cloud tính phí cho traditional load balancers
- **Tác động ngân sách**: Cần phân bổ ngân sách bổ sung

### 2. Single Point of Failure (Điểm Lỗi Duy Nhất)

- **Dự phòng hạn chế**: Ngay cả với primary và secondary load balancers, cả hai có thể lỗi
- **Khó cluster hóa**: Không thể scale load balancers dễ dàng trong môi trường cluster
- **Điểm nghẽn traffic**: Tất cả yêu cầu đến được tập trung tại một vị trí
- **Rủi ro gián đoạn hoàn toàn**: Lỗi load balancers ảnh hưởng toàn bộ hệ thống

### 3. Quản Lý Cấu Hình IP Thủ Công

- **Nhiệm vụ bất khả thi**: Cập nhật cấu hình IP thủ công là không thực tế cho microservices
- **Thay đổi liên tục**: Vòng đời container yêu cầu cập nhật thường xuyên
- **Lỗi con người**: Quy trình thủ công dễ mắc sai lầm
- **Chi phí vận hành**: Đầu tư thời gian và tài nguyên đáng kể

### 4. Phức Tạp và Không Tương Thích Với Container

- **Bản chất phức tạp**: Traditional load balancers yêu cầu bảo trì phức tạp
- **Quản lý thủ công**: Không thể tự động hóa dễ dàng
- **Không thân thiện với container**: Không tương thích với Docker containers
- **Môi trường động**: Containers có thể được tạo hoặc hủy bất cứ lúc nào

## Vấn Đề Chính: Duy Trì Bảng Định Tuyến Thủ Công

Thách thức lớn nhất với traditional load balancers trong microservices là yêu cầu **duy trì thủ công bảng định tuyến**. Điều này không thực tế vì:

- Containers và microservices có tính **ephemeral** (tạm thời)
- Instances liên tục được tạo và hủy
- Địa chỉ IP thay đổi động
- Không có thời gian cho can thiệp thủ công

## Tóm Tắt

Các phương pháp load balancing truyền thống và giao tiếp service dựa trên DNS:

✅ **Hoạt động tốt cho**:
- Ứng dụng monolithic
- Ứng dụng SOA
- Triển khai tĩnh
- Số lượng services nhỏ

❌ **Thất bại với**:
- Ứng dụng cloud-native
- Kiến trúc microservices
- Môi trường container động
- Các kịch bản auto-scaling

Vấn đề cốt lõi là các phương pháp truyền thống yêu cầu cấu hình tĩnh, được quản lý thủ công, không tương thích với bản chất động và tạm thời của cloud-native microservices.

## Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ khám phá các giải pháp để vượt qua những thách thức này cho các ứng dụng cloud-native và microservices, bao gồm:
- Các pattern Service Discovery
- Cơ chế Service Registration
- Phương pháp load balancing hiện đại
- Giải pháp thân thiện với container

---

**Ghi chú**: Nội dung này dựa trên bài giảng kỹ thuật về kiến trúc microservices sử dụng Java Spring Boot framework.