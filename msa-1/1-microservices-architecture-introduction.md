# Giới Thiệu Về Kiến Trúc Microservices

## Tổng Quan

Tài liệu này cung cấp phần giới thiệu toàn diện về kiến trúc microservices, so sánh với các phương pháp truyền thống như Monolithic và Service-Oriented Architecture (SOA).

## So Sánh Các Mô Hình Kiến Trúc

### 1. Kiến Trúc Monolithic (Nguyên Khối)

#### Kiến Trúc Monolithic Là Gì?

Kiến trúc Monolithic là phương pháp truyền thống trong đó toàn bộ chức năng nghiệp vụ được triển khai như một đơn vị duy nhất. Trong mô hình này:

- Tất cả các thành phần (tầng giao diện, logic nghiệp vụ, tầng truy cập dữ liệu) đều trong một server
- Codebase duy nhất cho toàn bộ ứng dụng
- Database duy nhất hỗ trợ cho tất cả dữ liệu (tài khoản, thẻ, khoản vay, v.v.)

#### Ưu Điểm

1. **Phát Triển và Triển Khai Đơn Giản Hơn**
   - Lý tưởng cho các nhóm và ứng dụng nhỏ
   - Triển khai một lần cho toàn bộ ứng dụng
   - Dễ dàng bắt đầu

2. **Ít Vấn Đề Cross-Cutting Concerns Hơn**
   - Đơn giản hóa bảo mật, kiểm toán và logging
   - Tất cả code ở một nơi

3. **Hiệu Suất Tốt Hơn**
   - Không có độ trễ mạng giữa các thành phần
   - Gọi method trực tiếp thay vì gọi web service

#### Nhược Điểm

1. **Khó Khăn Trong Việc Áp Dụng Công Nghệ Mới**
   - Phải cập nhật toàn bộ codebase
   - Tính linh hoạt hạn chế
   - Các team có thể có sở thích công nghệ xung đột

2. **Thách Thức Trong Bảo Trì**
   - Codebase đơn lẻ ngày càng lớn trở nên khó bảo trì
   - Các thành phần liên kết chặt chẽ
   - Cần kiểm thử nghiêm ngặt cho bất kỳ thay đổi nào

3. **Khả Năng Chịu Lỗi Kém**
   - Vấn đề về khả năng mở rộng
   - Vấn đề về tính sẵn sàng
   - Điểm lỗi đơn lẻ (single point of failure)

4. **Yêu Cầu Triển Khai Toàn Bộ**
   - Bất kỳ thay đổi nhỏ nào cũng yêu cầu triển khai lại toàn bộ ứng dụng
   - Downtime hoàn toàn trong quá trình triển khai
   - Không phù hợp cho ứng dụng 24/7

#### Các Loại Kiến Trúc Monolithic

- Single process monolithic
- Modular monolithic
- Distributed monolithic

Tất cả các dạng đều có những nhược điểm cơ bản giống nhau và hạn chế database đơn lẻ.

### 2. Kiến Trúc SOA (Service-Oriented Architecture)

#### SOA Là Gì?

SOA tách logic UI khỏi logic backend, cho phép tổ chức tốt hơn:

- Tầng giao diện được triển khai trên một server
- Logic nghiệp vụ (tài khoản, thẻ, vay) được triển khai trên server khác
- Giao tiếp qua Enterprise Service Bus (ESB)
- Web services cho phép tương tác giữa các tầng

#### Ưu Điểm

1. **Khả Năng Tái Sử Dụng Services**
   - Services có thể được tái sử dụng trên nhiều ứng dụng

2. **Bảo Trì Tốt Hơn**
   - Codebase riêng biệt cho UI và backend
   - Dễ quản lý các thành phần

3. **Độ Tin Cậy Cao Hơn**
   - Cách ly giữa các tầng

4. **Phát Triển Song Song**
   - Các team có thể làm việc độc lập trên UI và backend

#### Nhược Điểm

1. **Giao Thức Giao Tiếp Phức Tạp**
   - Sử dụng SOAP và định dạng XML
   - Nặng và phức tạp hơn REST

2. **Chi Phí ESB Middleware**
   - Yêu cầu sản phẩm ESB thương mại (ví dụ: Oracle ESB)
   - Chi phí đầu tư cao
   - Thêm thành phần cần bảo trì
   - Độ phức tạp thêm trong giao tiếp

3. **Backend Services Vẫn Liên Kết Chặt**
   - Trong khi UI tách biệt, các backend services vẫn ở cùng nhau

### 3. Kiến Trúc Microservices

#### Microservices Là Gì?

Kiến trúc Microservices bao gồm việc phát triển nhiều services nhỏ được mô hình hóa xung quanh các domain nghiệp vụ:

- Mỗi service tập trung vào một domain nghiệp vụ cụ thể (tài khoản, thẻ, vay)
- Mỗi microservice có database riêng
- Services được triển khai độc lập trên server hoặc container riêng
- Liên kết lỏng lẻo giữa các services

#### Đặc Điểm Chính

1. **Mô Hình Hóa Theo Domain Nghiệp Vụ**
   - Services được tổ chức xung quanh khả năng nghiệp vụ
   - Ranh giới và trách nhiệm rõ ràng

2. **Triển Khai Độc Lập**
   - Mỗi service có lifecycle riêng
   - Không phụ thuộc vào services khác khi triển khai

3. **Đa Dạng Công Nghệ**
   - Mỗi service có thể sử dụng công nghệ khác nhau
   - Tự do chọn tech stack phù hợp cho từng service

4. **Database Riêng Cho Mỗi Service**
   - Mỗi microservice quản lý dữ liệu riêng
   - Có thể chọn SQL hoặc NoSQL dựa trên nhu cầu

#### Ưu Điểm

1. **Phát Triển, Kiểm Thử và Triển Khai Dễ Dàng**
   - Các thành phần liên kết lỏng lẻo
   - Codebase nhỏ, tập trung

2. **Tăng Tính Linh Hoạt (Agility)**
   - Chu kỳ nâng cấp độc lập
   - Thời gian đưa ra thị trường nhanh hơn
   - Tự do áp dụng công nghệ mới cho từng service

3. **Phát Triển Song Song**
   - Các team làm việc độc lập
   - Không có liên kết chặt chẽ giữa các services
   - Lifecycle triển khai riêng

4. **Mở Rộng Ngang và Độc Lập**
   - Chỉ mở rộng những services cần thiết
   - Sử dụng tài nguyên hiệu quả
   - Triển khai bằng Docker container

5. **Linh Hoạt Công Nghệ**
   - Các ngôn ngữ lập trình khác nhau cho mỗi service (Python, Java, Go, v.v.)
   - Database khác nhau cho mỗi service (SQL, NoSQL)
   - Tự do chọn công cụ tốt nhất cho từng domain

#### Nhược Điểm

1. **Độ Phức Tạp**
   - Quản lý nhiều container độc lập
   - Đảm bảo giao tiếp đúng giữa các services
   - Thách thức của hệ thống phân tán

2. **Chi Phí Cơ Sở Hạ Tầng**
   - Nhiều server/container cần giám sát
   - Quản lý cơ sở hạ tầng phức tạp hơn
   - So với 1-2 server trong Monolithic/SOA

3. **Vấn Đề Bảo Mật**
   - Tất cả giao tiếp giữa services qua mạng (REST APIs)
   - Nhiều bề mặt tấn công hơn
   - Quản lý bảo mật phức tạp

#### Khi KHÔNG Nên Dùng Microservices

- Ứng dụng nhỏ
- Công ty nhỏ với nguồn lực hạn chế
- Khi độ phức tạp lớn hơn lợi ích

**Lưu Ý Quan Trọng:** Microservices không phải là giải pháp vạn năng. Đừng cho rằng nó giải quyết mọi vấn đề.

## Điểm Mấu Chốt

Ưu điểm chính của microservices là **khả năng triển khai độc lập**. Khi bạn có thể triển khai services độc lập mà không phụ thuộc vào microservices khác, nhiều lợi ích khác sẽ tự nhiên xuất hiện.

## Ví Dụ: Ứng Dụng EasyBank

### Phương Pháp Monolithic Truyền Thống

```
Server Đơn
├── UI/UX (HTML, CSS, JavaScript)
├── Logic Nghiệp Vụ (Tài khoản, Thẻ, Vay)
└── Database Đơn
```

**Phát triển:** Tất cả teams làm việc trên codebase đơn
**Triển khai:** File WAR/EAR đơn qua Jenkins
**Database:** Một database cho tất cả services

### Phương Pháp SOA

```
Server 1: Ứng Dụng UI
    ↓
Enterprise Service Bus (ESB)
    ↓
Server 2: Backend Services
    ├── Accounts Service
    ├── Cards Service
    └── Loans Service
    
Database Đơn
```

**Phát triển:** Repos riêng cho UI và backend
**Triển khai:** Hai lần triển khai riêng biệt
**Giao tiếp:** Qua ESB middleware

### Phương Pháp Microservices

```
Server 1: Ứng Dụng UI

Server 2: Accounts Microservice → Accounts DB
Server 3: Cards Microservice → Cards DB
Server 4: Loans Microservice → Loans DB
```

**Phát triển:** Repo riêng cho mỗi service (UI, Accounts, Cards, Loans)
**Triển khai:** Triển khai độc lập qua Jenkins/CI-CD cho mỗi service
**Giao tiếp:** Gọi REST API trực tiếp
**Databases:** Database riêng cho mỗi service
**Công nghệ:** Mỗi service có thể dùng ngôn ngữ/framework khác nhau

## So Sánh Chu Kỳ Triển Khai

### Monolithic

- Repository GitHub duy nhất
- Pipeline Jenkins duy nhất
- Triển khai toàn bộ ứng dụng như một đơn vị
- Một lần triển khai = tất cả tính năng/sửa lỗi được phát hành

### SOA

- Hai repository GitHub (UI, Backend)
- Hai pipeline Jenkins
- Triển khai riêng cho UI và Backend
- Giao tiếp qua ESB

### Microservices

- Nhiều repository GitHub (một cho mỗi service)
- Nhiều pipeline Jenkins (một cho mỗi service)
- Triển khai độc lập
- Không có chu kỳ triển khai chung
- Mỗi team service kiểm soát bản phát hành của họ

## Lợi Ích Của Khả Năng Triển Khai Độc Lập

Khi services có thể triển khai độc lập:

1. Các team có thể phát hành tính năng theo tốc độ riêng
2. Thay đổi nhỏ không yêu cầu triển khai toàn hệ thống
3. Giảm rủi ro - lỗi được cách ly
4. Đổi mới và thử nghiệm nhanh hơn
5. Khả năng mở rộng tốt hơn
6. Đa dạng công nghệ trở nên khả thi

## Kết Luận

Các tổ chức ưu tiên microservices vì chúng cho phép:

- **Tính Linh Hoạt:** Phản ứng nhanh với nhu cầu thị trường
- **Tự Do:** Nâng cấp và triển khai độc lập
- **Tốc Độ:** Thời gian đưa ra thị trường nhanh hơn
- **Khả Năng Mở Rộng:** Mở rộng những gì bạn cần, khi bạn cần

Mặc dù microservices mang lại độ phức tạp, nhưng ưu điểm thường vượt trội hơn thách thức đối với các tổ chức đang phát triển cần tính linh hoạt và đổi mới nhanh chóng. Nhiều phương pháp và mô hình tồn tại để vượt qua các thách thức của microservices, sẽ được đề cập trong các chủ đề nâng cao.

---

*Tài liệu này dựa trên phần giới thiệu về kiến trúc microservices sử dụng EasyBank làm ví dụ ứng dụng.*