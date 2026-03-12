

FILE: 1-microservices-architecture-introduction.md


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




FILE: 10-gioi-thieu-dto-pattern.md


# Giới Thiệu DTO Pattern

## Tổng Quan

Trong bài học này, chúng ta sẽ tìm hiểu về **DTO Pattern (Data Transfer Object pattern)**, một design pattern quan trọng để truyền dữ liệu giữa các tầng khác nhau trong ứng dụng Spring Boot microservices.

## Vấn Đề

Sau khi tạo các entity đại diện cho các bảng trong cơ sở dữ liệu và hỗ trợ các thao tác CRUD (tạo, đọc, cập nhật, xóa) cho thông tin tài khoản và khách hàng, chúng ta gặp phải một thách thức:

**Điều gì xảy ra nếu một ứng dụng khách muốn nhận cả dữ liệu tài khoản và khách hàng cùng lúc trong một request duy nhất?**

### Các Cân Nhắc Ban Đầu

- Chúng ta có thể gửi hai đối tượng khác nhau trong một response không? **Không.**
- Chúng ta chỉ có thể gửi một đối tượng duy nhất trong một response.
- Bạn có thể nghĩ: "Hãy tạo thêm một entity hoặc POJO class và nhúng cả trường accounts và customer vào bên trong."

### Tại Sao Cách Tiếp Cận Này Là Sai

**Các entity class liên quan đến tầng cơ sở dữ liệu.** Chúng nên:
- Đại diện rõ ràng và thuần túy cho các bảng cơ sở dữ liệu
- Không bao giờ được sửa đổi để đáp ứng yêu cầu truyền dữ liệu
- Tập trung vào việc đại diện cơ sở dữ liệu

Bạn có thể gặp nhiều tình huống khác nhau khi dữ liệu cần được gửi theo các định dạng hoặc tổ hợp khác nhau. Việc sửa đổi entity class cho mỗi tình huống vi phạm nguyên tắc Single Responsibility.

## DTO Pattern Là Gì?

**DTO** là viết tắt của **Data Transfer Object** (Đối tượng Truyền Dữ liệu).

DTO pattern là một design pattern cho phép bạn truyền dữ liệu giữa các phần khác nhau của ứng dụng, chẳng hạn như:
- Tầng cơ sở dữ liệu (Database layer)
- Tầng trình bày (Presentation layer)
- Tầng dịch vụ (Service layer)

### Cách Hoạt Động

Thay vì gửi trực tiếp các entity class từ cơ sở dữ liệu cho client, chúng ta:

1. **Tạo các DTO class** chứa các trường cụ thể cần thiết cho việc truyền dữ liệu
2. **Viết logic mapper/aggregation** để chuyển đổi dữ liệu từ DB entities sang DTO classes
3. **Gửi DTO classes** đến các ứng dụng client

### Ví Dụ Cấu Trúc

#### Database Entities
```
Customer Entity:
- customerId
- name
- email
- mobileNumber
...

Accounts Entity:
- accountNumber
- customerId
- accountType
- branchAddress
...
```

#### DTO Class
```
CustomerDetails DTO:
- name
- email
- mobileNumber
- accountNumber
- accountType
- branchAddress
...
```

Logic mapper tổng hợp dữ liệu từ cả hai entity `Customer` và `Accounts` thành một DTO class `CustomerDetails` duy nhất.

## Ưu Điểm Của DTO Pattern

### 1. Giảm Lưu Lượng Mạng

**Không có DTO Pattern:**
- Client cần cả dữ liệu customer và accounts
- Phải thực hiện **hai request riêng biệt** (một cho customer, một cho accounts)
- Tốn kém băng thông mạng không cần thiết

**Với DTO Pattern:**
- Client chỉ thực hiện **một request duy nhất**
- Logic mapper kết hợp dữ liệu từ bảng customer và accounts
- Response duy nhất với `CustomerDetails` DTO
- Giảm lưu lượng mạng và cải thiện hiệu suất

### 2. Đóng Gói Logic Serialization

DTO class chỉ đại diện cho dữ liệu mà chúng mang theo mà không có business logic.

**Lợi ích:**
- Vị trí tập trung cho logic serialization
- Hỗ trợ nhiều định dạng (XML, JSON, YAML) dựa trên nhu cầu của client
- Tránh phân tán logic serialization khắp ứng dụng
- Dễ dàng bảo trì khi định dạng serialization thay đổi

### 3. Tách Biệt Các Tầng (Decoupling)

DTO pattern **tách biệt tầng trình bày khỏi tầng truy cập dữ liệu**.

#### Điều Này Có Nghĩa Là Gì?

**Ứng dụng client (presentation layer):**
- Không bao giờ biết về database entities
- Không cần hiểu cấu trúc cơ sở dữ liệu
- Chỉ làm việc với DTO classes

**Thay đổi cơ sở dữ liệu:**
- Thêm cột mới vào DB entities không ảnh hưởng đến clients
- Chỉ cập nhật DTOs nếu clients cần dữ liệu mới
- Thay đổi ở một tầng không lan truyền sang các tầng khác

#### Ví Dụ Kịch Bản

Nếu bạn thêm một cột mới vào cơ sở dữ liệu:
1. DB entity class được cập nhật
2. Nếu clients **không cần** dữ liệu này, **không cập nhật DTO**
3. Clients không bị ảnh hưởng bởi thay đổi cơ sở dữ liệu

Sự tách biệt này đảm bảo khả năng bảo trì và linh hoạt tốt hơn.

## Các Bước Triển Khai Tiếp Theo

Đối với mỗi database entity trong ứng dụng web của chúng ta, chúng ta cần:

1. Tạo DTO class tương ứng
2. Định nghĩa các trường mà clients sẽ nhận được
3. Triển khai logic mapper để chuyển đổi entities sang DTOs
4. Sử dụng DTOs khi phản hồi các REST API/microservice calls

## Tóm Tắt

DTO pattern là cần thiết cho:
- **Truyền dữ liệu** giữa các tầng ứng dụng
- **Giảm lưu lượng mạng** bằng cách kết hợp dữ liệu
- **Đóng gói logic serialization**
- **Tách biệt các tầng** để dễ bảo trì hơn

Bằng cách tuân theo DTO pattern, các microservices Spring Boot của bạn sẽ linh hoạt hơn, dễ bảo trì hơn và hiệu quả hơn.

---

**Bài Học Tiếp Theo:** Chúng ta sẽ triển khai DTO classes và logic mapper trong ứng dụng Spring Boot.




FILE: 11-tao-cac-lop-dto-cho-accounts-microservice.md


# Tạo Các Lớp DTO Cho Accounts Microservice

## Giới Thiệu

Trong bài giảng này, chúng ta sẽ tạo các lớp DTO (Data Transfer Object) đại diện cho mỗi lớp entity trong accounts microservice của chúng ta. Hướng dẫn này bao gồm các khái niệm cơ bản cần thiết cho sinh viên và các lập trình viên junior đang xây dựng REST APIs với Spring Boot.

> **Lưu ý:** Nếu bạn đã quen thuộc với các khái niệm này, hãy xem ở tốc độ cao hơn. Có rất nhiều chủ đề thú vị phía trước khi chúng ta xây dựng các microservices như accounts, cards và loans!

## Hiểu Về DTO Pattern

DTO pattern giúp chúng ta tách biệt các entity database khỏi dữ liệu mà chúng ta truyền giữa các tầng ứng dụng và đến các ứng dụng client. Điều này mang lại nhiều lợi ích:
- Lọc dữ liệu (ẩn các ID nội bộ và thông tin nhạy cảm)
- Tách biệt các mối quan tâm
- Thiết kế API và quản lý phiên bản tốt hơn

## Tạo Package DTO

Đầu tiên, tạo một package mới có tên `dto` trong cấu trúc dự án của bạn. Tất cả các lớp DTO sẽ được đặt trong package này.

## 1. Tạo Lớp AccountsDto

### Định Nghĩa Lớp
```java
@Data
public class AccountsDto {
    private String accountNumber;
    private String accountType;
    private String branchAddress;
}
```

### Các Điểm Chính
- **Quy Ước Đặt Tên**: Luôn kết thúc tên lớp DTO với "Dto" để phân biệt với các lớp entity JPA
- **Lọc Dữ Liệu**: Chúng ta loại bỏ `customerId` khỏi DTO vì đó là định danh database nội bộ mà client không cần
- **Các Trường Bao Gồm**: 
  - `accountNumber` - Số tài khoản
  - `accountType` - Loại tài khoản
  - `branchAddress` - Địa chỉ chi nhánh
- **Annotations JPA**: Loại bỏ tất cả các annotation đặc thù của JPA khỏi DTOs

### Sử Dụng Lombok @Data Annotation

Annotation `@Data` là một tính năng mạnh mẽ của Lombok tự động tạo ra:
- Getters cho tất cả các trường
- Setters cho tất cả các trường
- `RequiredArgsConstructor`
- Phương thức `toString()`
- Phương thức `equals()`
- Phương thức `hashCode()`

> **Lưu Ý Quan Trọng**: Chúng ta không sử dụng `@Data` trên các lớp entity vì việc tạo ra các phương thức `hashCode()` và `equals()` đôi khi có thể gây ra vấn đề với Spring Data JPA.

## 2. Tạo Lớp CustomerDto

### Định Nghĩa Lớp
```java
@Data
public class CustomerDto {
    private String name;
    private String email;
    private String mobileNumber;
}
```

### Các Điểm Chính
- Loại bỏ `customerId` (định danh database nội bộ)
- Chỉ chứa thông tin khách hàng cần thiết cho ứng dụng client:
  - `name` - Tên
  - `email` - Email
  - `mobileNumber` - Số điện thoại di động
- Không có annotation đặc thù của JPA

> **Lưu Ý**: Hiện tại, chúng ta không tạo DTO kết hợp dữ liệu Customer và Accounts. Chúng ta sẽ tạo các DTO như vậy khi cần trong các phần sau.

## 3. Tạo Lớp ResponseDto

Khi client gửi yêu cầu lưu dữ liệu, chúng ta cần gửi lại phản hồi thành công hoặc lỗi. Lớp `ResponseDto` xử lý các phản hồi thành công.

### Định Nghĩa Lớp
```java
@Data
@AllArgsConstructor
public class ResponseDto {
    private String statusCode;
    private String statusMsg;
}
```

### Các Điểm Chính
- **@AllArgsConstructor**: Tạo constructor chấp nhận tất cả các trường làm tham số
  - Annotation `@Data` đơn thuần không tạo constructor với tất cả tham số
  - Chúng ta cần điều này để tạo đối tượng thuận tiện trong tương lai
- **Các Trường**:
  - `statusCode`: Mã trạng thái HTTP (ví dụ: "200" cho thành công, "500" cho lỗi)
  - `statusMsg`: Thông điệp trạng thái có thể đọc được

Điều này cho phép client dễ dàng hiểu liệu các thao tác có thành công hay không.

## 4. Tạo Lớp ErrorResponseDto

Để xử lý lỗi và ngoại lệ trong microservice, chúng ta cần một cấu trúc phản hồi lỗi toàn diện.

### Định Nghĩa Lớp
```java
@Data
@AllArgsConstructor
public class ErrorResponseDto {
    private String apiPath;
    private HttpStatus errorCode;
    private String errorMsg;
    private LocalDateTime errorTime;
}
```

### Các Điểm Chính
- **apiPath**: Endpoint API mà client đã cố gắng gọi
- **errorCode**: Mã trạng thái HTTP (sử dụng enum `HttpStatus`)
- **errorMsg**: Thông điệp lỗi chi tiết
- **errorTime**: Dấu thời gian khi lỗi xảy ra

### Lợi Ích
Bốn trường này cung cấp cho client thông tin đầy đủ để debug:
1. API nào họ đã cố gắng gọi
2. Mã lỗi nào được trả về
3. Thông điệp lỗi nói gì
4. Lỗi xảy ra khi nào

Điều này giúp các developer ở phía client debug các vấn đề bằng cách kiểm tra logs trong hệ thống của họ.

## Tóm Tắt

Chúng ta đã tạo thành công tất cả các lớp DTO cần thiết cho accounts microservice:
1. **AccountsDto** - Đại diện cho thông tin tài khoản
2. **CustomerDto** - Đại diện cho thông tin khách hàng
3. **ResponseDto** - Xử lý phản hồi thành công
4. **ErrorResponseDto** - Xử lý phản hồi lỗi

### Các Bước Tiếp Theo
Mặc dù chúng ta đã tạo các DTO và entity, chúng ta vẫn cần triển khai:
- Logic mapper để chuyển đổi giữa entities và DTOs
- Logic tổng hợp để kết hợp dữ liệu
- Những điều này sẽ được xây dựng khi chúng ta tiến triển qua khóa học

## DTO Pattern - Bối Cảnh Lịch Sử

DTO pattern ban đầu được khuyến nghị bởi **Martin Fowler** trong blog của ông. Ông đã mô tả tại sao chúng ta nên tuân theo Data Transfer Object pattern và cung cấp các ví dụ.

### Kịch Bản Ví Dụ
Xét một database với:
- Bảng `album` (chứa tiêu đề)
- Bảng `artist` (chứa tên)

Nếu client cần cả tiêu đề album và tên nghệ sĩ trong một phản hồi duy nhất:
1. Tạo `AlbumDto` chứa cả thông tin title và artist
2. Sử dụng logic assembler/mapper để ánh xạ dữ liệu entity sang DTO
3. Tùy chọn thêm logic serialization trong lớp DTO

### Đặt Tên Thay Thế
Các tổ chức khác nhau có thể sử dụng tên khác nhau cho DTOs:
- **Value Object (VO)** - Đối tượng giá trị
- **Transfer Object (TO)** - Đối tượng truyền tải

Bất kể quy ước đặt tên nào, nếu một dự án sử dụng các lớp POJO khác nhau (thay vì các POJO entity database) để truyền dữ liệu giữa các tầng ứng dụng, họ đang tuân theo DTO pattern.

## Tài Nguyên Bổ Sung

Để biết thêm thông tin về DTO pattern, tham khảo bài viết blog của Martin Fowler về Data Transfer Objects. URL sẽ có sẵn trong repository GitHub và được đính kèm vào bài giảng này.

---

**Chúc mừng!** Bạn đã tạo thành công các lớp DTO cho Accounts Microservice. Hẹn gặp lại trong bài giảng tiếp theo!




FILE: 12-xay-dung-logic-nghiep-vu-rest-api-va-tang-service.md


# Xây Dựng Logic Nghiệp Vụ REST API và Tầng Service

## Giới Thiệu

Bạn có hào hứng để xây dựng logic nghiệp vụ thực tế không? Trong bài giảng này, chúng ta sẽ xây dựng một REST API hỗ trợ tạo mới tài khoản và thông tin chi tiết khách hàng trong cơ sở dữ liệu H2. Chúng ta sẽ đề cập đến nhiều tiêu chuẩn quan trọng bao gồm:
- Xử lý ngoại lệ
- Logic tầng service
- Tận dụng DTO pattern
- Mapper patterns
- Các best practices cho phát triển REST API

## Thiết Lập REST API Controller

### Thêm Request Mapping Prefix

Trong các dự án thực tế, luôn được khuyến nghị duy trì một đường dẫn API tiền tố chung cho tất cả các REST API trong lớp controller.

```java
@RestController
@RequestMapping(path = "/api", produces = MediaType.APPLICATION_JSON_VALUE)
public class AccountsController {
    // Các phương thức controller
}
```

**Các Điểm Chính:**
- **Path Prefix**: `/api` - Tiền tố chung cho tất cả API trong controller này
- **Versioning**: Một số dự án cũng duy trì số phiên bản như `/api/v1` hoặc `/api/v2`
- **Produces**: Chỉ định định dạng phản hồi là JSON sử dụng `MediaType.APPLICATION_JSON_VALUE`
- Đảm bảo import `MediaType` từ package `org.springframework.http`

### Tạo Phương Thức Create Account

```java
@PostMapping("/create")
public ResponseEntity<ResponseDto> createAccount(@RequestBody CustomerDto customerDto) {
    accountsService.createAccount(customerDto);
    
    return ResponseEntity
            .status(HttpStatus.CREATED)
            .body(new ResponseDto(AccountsConstants.STATUS_201, 
                                  AccountsConstants.MESSAGE_201));
}
```

**Phân Tích Phương Thức:**
- **@PostMapping("/create")**: Ánh xạ đến endpoint `/api/create`
- **@RequestBody**: Ánh xạ request body thành đối tượng `CustomerDto`
- **ResponseEntity<ResponseDto>**: Cho phép gửi status, body và headers trong response
- **HttpStatus.CREATED**: Trả về mã trạng thái 201 cho việc tạo thành công

### Hiểu Về ResponseEntity

`ResponseEntity` là một lớp mạnh mẽ trong Spring Framework cho phép bạn:
- Gửi mã trạng thái HTTP
- Gửi response body
- Gửi custom headers
- Gửi thông tin content type

**Các phương thức có sẵn:**
- `status()` - Đặt mã trạng thái HTTP
- `body()` - Đặt response body
- `header()` - Thêm custom headers
- `contentType()` - Đặt content type

**Tại sao sử dụng ResponseEntity?**
Nếu bạn chỉ trả về `ResponseDto`, chỉ nội dung body được gửi. Với `ResponseEntity`, bạn có toàn quyền kiểm soát:
- Trạng thái HTTP tổng thể
- Response headers
- Response body
- Thông tin metadata

## Tạo Lớp Constants

Đây là tiêu chuẩn được khuyến nghị để duy trì tất cả các giá trị hằng số trong một file riêng biệt.

### Tạo Package Constants và Class

```java
package com.example.accounts.constants;

public class AccountsConstants {
    
    private AccountsConstants() {
        // Constructor private để ngăn khởi tạo
    }
    
    public static final String STATUS_201 = "201";
    public static final String MESSAGE_201 = "Account created successfully";
    public static final String STATUS_200 = "200";
    public static final String MESSAGE_200 = "Request processed successfully";
    public static final String STATUS_500 = "500";
    public static final String MESSAGE_500 = "An error occurred. Please try again or contact support";
}
```

**Best Practices cho Constants:**
1. **Static và Final**: Hằng số nên là `static final` để không thể thay đổi
2. **Đặt Tên Viết Hoa**: Sử dụng chữ cái viết hoa cho tên hằng số (ví dụ: `STATUS_201`)
3. **Dấu Gạch Dưới Phân Cách**: Sử dụng gạch dưới để phân cách từ (ví dụ: `MESSAGE_201`)
4. **Constructor Private**: Ngăn chặn việc khởi tạo lớp constants
5. **Truy Cập Static**: Sử dụng hằng số thông qua tên lớp mà không cần tạo đối tượng

**Tại sao Constructor Private?**
- Ngăn chặn việc tạo đối tượng của lớp constants
- Đảm bảo lớp chỉ được sử dụng để chứa hằng số
- Ngăn chặn "ô nhiễm" với các phương thức hoặc logic nghiệp vụ

## Tạo Tầng Service

### Service Interface

Tạo một service interface để định nghĩa hợp đồng:

```java
package com.example.accounts.service;

/**
 * Service interface cho các thao tác Account
 */
public interface IAccountsService {
    
    /**
     * Tạo một tài khoản mới
     * @param customerDto - Đối tượng CustomerDto chứa thông tin chi tiết khách hàng
     */
    void createAccount(CustomerDto customerDto);
}
```

**Quy Ước Đặt Tên:**
- Thêm tiền tố `I` cho tên interface (ví dụ: `IAccountsService`)
- Điều này chỉ rõ đây là một interface
- Lưu ý: Chúng ta không sử dụng quy ước này cho Repository interfaces vì chúng không có lớp implementation

**JavaDoc Comments:**
- Thêm tài liệu ở cấp độ phương thức
- Mô tả tham số và giá trị trả về
- Giải thích logic phức tạp cho các thành viên team trong tương lai
- Giúp duy trì code tốt hơn

### Service Implementation

```java
package com.example.accounts.service.impl;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class AccountsServiceImpl implements IAccountsService {
    
    private AccountsRepository accountsRepository;
    private CustomerRepository customerRepository;
    
    @Override
    public void createAccount(CustomerDto customerDto) {
        // Triển khai logic nghiệp vụ
    }
}
```

**Các Điểm Chính:**
1. **@Service**: Đánh dấu lớp là một component tầng service
2. **@AllArgsConstructor**: Lombok tạo constructor với tất cả các trường
3. **Constructor Injection**: Spring tự động autowire các dependency khi chỉ có một constructor
4. **Không cần @Autowired**: Với một constructor duy nhất, Spring thực hiện autowiring tự động

**Cách Constructor Injection Hoạt Động:**
- Lombok tạo constructor chấp nhận tất cả các trường
- Spring phát hiện constructor duy nhất
- Tự động inject các repository bean
- Code sạch hơn không cần annotation `@Autowired` tường minh

## Tạo Các Lớp Mapper

Chúng ta cần logic mapper để chuyển đổi giữa các lớp DTO và Entity.

### AccountsMapper

```java
package com.example.accounts.mapper;

public class AccountsMapper {
    
    public static AccountsDto mapToAccountsDto(Accounts accounts, AccountsDto accountsDto) {
        accountsDto.setAccountNumber(accounts.getAccountNumber());
        accountsDto.setAccountType(accounts.getAccountType());
        accountsDto.setBranchAddress(accounts.getBranchAddress());
        return accountsDto;
    }
    
    public static Accounts mapToAccounts(AccountsDto accountsDto, Accounts accounts) {
        accounts.setAccountNumber(accountsDto.getAccountNumber());
        accounts.setAccountType(accountsDto.getAccountType());
        accounts.setBranchAddress(accountsDto.getBranchAddress());
        return accounts;
    }
}
```

### CustomerMapper

```java
package com.example.accounts.mapper;

public class CustomerMapper {
    
    public static CustomerDto mapToCustomerDto(Customer customer, CustomerDto customerDto) {
        customerDto.setName(customer.getName());
        customerDto.setEmail(customer.getEmail());
        customerDto.setMobileNumber(customer.getMobileNumber());
        return customerDto;
    }
    
    public static Customer mapToCustomer(CustomerDto customerDto, Customer customer) {
        customer.setName(customerDto.getName());
        customer.setEmail(customerDto.getEmail());
        customer.setMobileNumber(customerDto.getMobileNumber());
        return customer;
    }
}
```

**Giải Thích Logic Mapper:**
- **Static Methods**: Có thể gọi mà không cần tạo đối tượng mapper
- **Ánh Xạ Hai Chiều**: 
  - `mapToDto`: Entity → DTO
  - `mapToEntity`: DTO → Entity
- **Dựa Trên Setter/Getter**: Sử dụng phương thức getter/setter đơn giản cho việc ánh xạ

## Thư Viện Mapper Thay Thế

### Các Thư Viện Mapper Phổ Biến

Có các thư viện hỗ trợ ánh xạ tự động:

1. **ModelMapper**
2. **MapStruct**

Các thư viện này có thể tự động chuyển đổi giữa DTO và Entity với code tối thiểu.

### Tại Sao Không Sử Dụng Chúng Trong Khóa Học Này?

**Lý do cho việc ánh xạ thủ công:**

1. **Công Nhận Chính Thức**: 
   - Lombok được Spring công nhận chính thức (có sẵn trên start.spring.io)
   - ModelMapper và MapStruct không được liệt kê chính thức

2. **Vấn Đề Bảo Mật**:
   - Các thư viện mã nguồn mở có thể có lỗ hổng bảo mật
   - Có thể cần sự chấp thuận của client/kiến trúc sư
   - Một số website thiếu chứng chỉ chính thức

3. **Kiểm Soát Hoàn Toàn**:
   - Logic serialization tùy chỉnh
   - Che dấu dữ liệu (ví dụ: ẩn một phần số điện thoại)
   - Tính linh hoạt cho các chuyển đổi phức tạp

**Ví Dụ Use Case:**
```java
// Che dấu số điện thoại - chỉ hiển thị 4 số cuối
public static CustomerDto mapToCustomerDto(Customer customer, CustomerDto customerDto) {
    customerDto.setName(customer.getName());
    customerDto.setEmail(customer.getEmail());
    String mobile = customer.getMobileNumber();
    customerDto.setMobileNumber("****" + mobile.substring(mobile.length() - 4));
    return customerDto;
}
```

Tính linh hoạt này có thể không dễ dàng có sẵn với các thư viện mapper tự động.

### Khi Nào Sử Dụng Automated Mappers

Nếu client và project lead của bạn chấp thuận:
- Chúng dễ học
- Chúng dễ sử dụng
- Chúng giảm code boilerplate
- Chúng phù hợp cho các ánh xạ đơn giản

**Tiêu Chí Quyết Định:**
- Chấp thuận của client ✓
- Chấp thuận của project lead ✓
- Không có logic chuyển đổi phức tạp ✓
- Đánh giá bảo mật hoàn tất ✓

## Tóm Tắt

Trong bài giảng này, chúng ta đã đề cập:

1. **Thiết Lập REST API**:
   - Request mapping với path prefix
   - Cấu hình content type phản hồi
   - POST endpoint để tạo tài khoản

2. **Quản Lý Constants**:
   - Tạo lớp constants chuyên dụng
   - Best practices cho đặt tên hằng số
   - Pattern constructor private

3. **Kiến Trúc Tầng Service**:
   - Thiết kế dựa trên interface
   - Triển khai service
   - Dependency injection dựa trên constructor

4. **Mapper Pattern**:
   - Chuyển đổi thủ công DTO ↔ Entity
   - Phương thức mapper static
   - Kiểm soát hoàn toàn việc chuyển đổi dữ liệu

5. **ResponseEntity**:
   - Kiểm soát phản hồi toàn diện
   - Mã trạng thái, headers và body
   - Thiết kế API chuyên nghiệp

## Các Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ tiếp tục triển khai logic nghiệp vụ để tạo tài khoản và khách hàng trong cơ sở dữ liệu. Chúng ta cũng sẽ khám phá xử lý ngoại lệ và validation.

---

**Hãy nghỉ ngơi và hẹn gặp lại trong bài giảng tiếp theo!**




FILE: 13-trien-khai-create-account-api-voi-xu-ly-ngoai-le.md


# Triển Khai Create Account API Với Xử Lý Ngoại Lệ

## Giới Thiệu

Chào mừng trở lại! Trong bài giảng này, chúng ta sẽ hoàn thành việc triển khai logic nghiệp vụ tạo tài khoản, bao gồm:
- Chuyển đổi DTO thành Entity và lưu vào database
- Xử lý ngoại lệ tùy chỉnh
- Global exception handler
- Derived named methods trong Spring Data JPA
- Kiểm thử API với Postman
- Xử lý các trường audit

## Triển Khai Logic Tầng Service

### Bước 1: Chuyển Đổi DTO Thành Entity

Trong `AccountsServiceImpl`, chúng ta cần chuyển đổi `CustomerDto` đầu vào thành entity `Customer`:

```java
@Override
public void createAccount(CustomerDto customerDto) {
    Customer customer = CustomerMapper.mapToCustomer(customerDto, new Customer());
    Customer savedCustomer = customerRepository.save(customer);
    accountsRepository.save(createNewAccount(savedCustomer));
}
```

**Giải Thích:**
1. Sử dụng `CustomerMapper.mapToCustomer()` để chuyển đổi DTO thành Entity
2. Truyền DTO và một đối tượng `Customer()` mới
3. Dữ liệu từ `CustomerDto` được chuyển sang entity `Customer`

### Bước 2: Lưu Customer Vào Database

```java
Customer savedCustomer = customerRepository.save(customer);
```

**Điều Gì Xảy Ra Đằng Sau:**
Spring Data JPA tự động xử lý:
- Tạo câu lệnh SQL
- Mở kết nối database
- Thực thi câu lệnh
- Commit transaction
- Đóng kết nối

**Lưu Ý Quan Trọng:**
- Phương thức `save()` đến từ `JpaRepository` (mà `CustomerRepository` extends)
- Khi lưu, `customerId` được tự động tạo bởi Spring Data JPA
- Lưu kết quả vào `savedCustomer` để truy cập ID được tạo

### Bước 3: Tạo Account Cho Customer

Tạo một phương thức private để tạo account mới:

```java
private Accounts createNewAccount(Customer customer) {
    Accounts newAccount = new Accounts();
    newAccount.setCustomerId(customer.getCustomerId());
    
    long randomAccNumber = 1000000000L + new Random().nextInt(900000000);
    newAccount.setAccountNumber(randomAccNumber);
    newAccount.setAccountType(AccountsConstants.SAVINGS);
    newAccount.setBranchAddress("123 Main Street, New York");
    
    newAccount.setCreatedAt(LocalDateTime.now());
    newAccount.setCreatedBy("Anonymous");
    
    return newAccount;
}
```

**Các Điểm Chính:**
1. **CustomerId**: Liên kết account với customer
2. **Account Number**: Số ngẫu nhiên 10 chữ số do developer tạo
3. **Account Type**: Sử dụng hằng số `SAVINGS` từ `AccountsConstants`
4. **Branch Address**: Địa chỉ mặc định được gán
5. **Audit Fields**: Được điền thủ công bây giờ (sẽ tự động hóa sau)

### Bước 4: Lưu Account Vào Database

```java
accountsRepository.save(createNewAccount(savedCustomer));
```

Điều này thiết lập liên kết giữa customer và account thông qua `customerId`.

## Xử Lý Ngoại Lệ

### Vấn Đề

Chúng ta cần ngăn chặn customer trùng lặp dựa trên số điện thoại:
- Chỉ một customer cho mỗi số điện thoại
- Nhiều customer có thể có cùng email hoặc tên
- Số điện thoại phải là duy nhất

### Tạo Custom Exception

Tạo một lớp exception tùy chỉnh:

```java
package com.example.accounts.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(value = HttpStatus.BAD_REQUEST)
public class CustomerAlreadyExistsException extends RuntimeException {
    
    public CustomerAlreadyExistsException(String message) {
        super(message);
    }
}
```

**Các Điểm Chính:**
1. **Extends RuntimeException**: Bắt buộc cho custom exceptions
2. **Constructor với Message**: Nhận thông điệp exception và truyền cho parent
3. **@ResponseStatus**: Tự động trả về `400 BAD_REQUEST` khi được throw

### Tạo Derived Named Method

Chúng ta cần query theo số điện thoại, nhưng `CustomerRepository` chỉ có phương thức cho `customerId` (primary key).

**Thêm vào CustomerRepository:**

```java
public interface CustomerRepository extends JpaRepository<Customer, Long> {
    
    Optional<Customer> findByMobileNumber(String mobileNumber);
}
```

**Cách Derived Named Methods Hoạt Động:**
- **Quy Ước Đặt Tên**: `findBy` + `TênTrường`
- Spring Data JPA tự động tạo query
- Tên trường phải khớp với trường entity (không phân biệt hoa thường)
- Cho nhiều cột: `findByMobileNumberAndEmail(String mobile, String email)`

**Các Pattern Ví Dụ:**
- `findByMobileNumber` → SELECT * FROM customer WHERE mobile_number = ?
- `findByEmail` → SELECT * FROM customer WHERE email = ?
- `findByNameAndEmail` → SELECT * FROM customer WHERE name = ? AND email = ?

### Validate Trước Khi Lưu

Thêm logic validation trong `AccountsServiceImpl`:

```java
@Override
public void createAccount(CustomerDto customerDto) {
    // Validate nếu customer đã tồn tại
    Optional<Customer> optionalCustomer = customerRepository
            .findByMobileNumber(customerDto.getMobileNumber());
    
    if(optionalCustomer.isPresent()) {
        throw new CustomerAlreadyExistsException(
            "Customer already registered with given mobile number: " 
            + customerDto.getMobileNumber()
        );
    }
    
    // Tạo customer và account
    Customer customer = CustomerMapper.mapToCustomer(customerDto, new Customer());
    customer.setCreatedAt(LocalDateTime.now());
    customer.setCreatedBy("Anonymous");
    
    Customer savedCustomer = customerRepository.save(customer);
    accountsRepository.save(createNewAccount(savedCustomer));
}
```

**Luồng Logic:**
1. Query database theo số điện thoại
2. Nếu customer tồn tại (`isPresent()` trả về true), throw exception
3. Nếu không, tiến hành tạo account

## Global Exception Handler

### Vấn Đề Với Xử Lý Exception Cục Bộ

Nếu chúng ta xử lý exception trong mỗi phương thức controller:
- Code trùng lặp qua nhiều controller
- Khó bảo trì
- Phản hồi lỗi không nhất quán

### Giải Pháp: Global Exception Handler

Tạo một exception handler tập trung:

```java
package com.example.accounts.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.context.request.WebRequest;

import java.time.LocalDateTime;

@ControllerAdvice
public class GlobalExceptionHandler {
    
    @ExceptionHandler(CustomerAlreadyExistsException.class)
    public ResponseEntity<ErrorResponseDto> handleCustomerAlreadyExistsException(
            CustomerAlreadyExistsException exception,
            WebRequest webRequest) {
        
        ErrorResponseDto errorResponseDto = new ErrorResponseDto(
            webRequest.getDescription(false),
            HttpStatus.BAD_REQUEST,
            exception.getMessage(),
            LocalDateTime.now()
        );
        
        return new ResponseEntity<>(errorResponseDto, HttpStatus.BAD_REQUEST);
    }
}
```

**Các Thành Phần Chính:**

1. **@ControllerAdvice**: Báo cho Spring lớp này xử lý exception toàn cục cho tất cả controller

2. **@ExceptionHandler**: Chỉ định exception nào phương thức này xử lý
   - Tham số: `CustomerAlreadyExistsException.class`
   - Phương thức được gọi khi exception này được throw

3. **Tham Số WebRequest**: 
   - `getDescription(false)` → Chỉ trả về đường dẫn API
   - `getDescription(true)` → Trả về đường dẫn API + IP client + chi tiết khác

4. **Tạo ErrorResponseDto**:
   - **apiPath**: Endpoint mà client cố gắng gọi
   - **errorCode**: `HttpStatus.BAD_REQUEST` (400)
   - **errorMsg**: Thông điệp exception
   - **errorTime**: Timestamp hiện tại

5. **Return**: `ResponseEntity` với chi tiết lỗi và HTTP status

### Lợi Ích Của Global Exception Handler

- ✅ Xử lý exception tập trung
- ✅ Phản hồi lỗi nhất quán
- ✅ Dễ dàng thêm exception handler mới
- ✅ Không trùng lặp code
- ✅ Định tuyến exception tự động

## Cập Nhật Controller

### Autowiring Service

Sử dụng constructor-based dependency injection:

```java
@RestController
@RequestMapping(path = "/api", produces = MediaType.APPLICATION_JSON_VALUE)
@AllArgsConstructor
public class AccountsController {
    
    private IAccountsService accountsService;
    
    @PostMapping("/create")
    public ResponseEntity<ResponseDto> createAccount(@RequestBody CustomerDto customerDto) {
        accountsService.createAccount(customerDto);
        
        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(new ResponseDto(AccountsConstants.STATUS_201, 
                                      AccountsConstants.MESSAGE_201));
    }
}
```

**Tại Sao Constructor Injection?**
- ✅ Cách tiếp cận được khuyến nghị hơn field injection
- ✅ Với `@AllArgsConstructor`, Lombok tạo constructor
- ✅ Constructor duy nhất → Không cần annotation `@Autowired`
- ✅ Spring tự động thực hiện dependency injection

**Luồng Exception:**
1. Nếu không có exception → Trả về phản hồi thành công (201)
2. Nếu exception xảy ra → Không bao giờ đến controller
3. Exception được bắt bởi `GlobalExceptionHandler`
4. Phản hồi lỗi được gửi đến client

## Kiểm Thử Với Postman

### Thiết Lập Postman

1. **Tải Postman**: Tải công cụ từ website chính thức
2. **Import Collection**: 
   - Tải collection JSON từ GitHub repo
   - File → Import → Thả file JSON
   - Tất cả request được tải tự động

### Request Tạo Account

**Endpoint:** `POST http://localhost:8080/api/create`

**Request Body:**
```json
{
    "name": "Madan Reddy",
    "email": "madan@example.com",
    "mobileNumber": "1234567890"
}
```

**Lưu Ý Quan Trọng:**
- Tên trường JSON phải khớp với các trường `CustomerDto`: `name`, `email`, `mobileNumber`
- Spring Boot sử dụng thư viện Jackson để chuyển đổi JSON ↔ POJO
- Chuyển đổi xảy ra tự động

### Request Đầu Tiên - Phản Hồi Thành Công

**Response:**
```json
{
    "statusCode": "201",
    "statusMsg": "Account created successfully"
}
```

**HTTP Status:** `201 CREATED`

### Request Thứ Hai - Số Điện Thoại Trùng Lặp

**Response:**
```json
{
    "apiPath": "uri=/api/create",
    "errorCode": "BAD_REQUEST",
    "errorMsg": "Customer already registered with given mobile number: 1234567890",
    "errorTime": "2026-03-09T10:30:45"
}
```

**HTTP Status:** `400 BAD_REQUEST`

## Sửa Lỗi Audit Fields

### Lỗi Ban Đầu

Lần thử đầu tiên thất bại vì `createdAt` và `createdBy` là null (vi phạm ràng buộc not-null).

### Giải Pháp - Điền Thủ Công

Thêm audit fields trước khi lưu:

```java
// Cho Customer
customer.setCreatedAt(LocalDateTime.now());
customer.setCreatedBy("Anonymous");

// Cho Account
newAccount.setCreatedAt(LocalDateTime.now());
newAccount.setCreatedBy("Anonymous");
```

**Lưu Ý:** Chúng ta sẽ tự động hóa điều này sử dụng Spring Data JPA auditing trong các bài giảng sau.

## Xác Minh Dữ Liệu Trong H2 Console

### Truy Cập H2 Console

1. Điều hướng đến: `http://localhost:8080/h2-console`
2. Kết nối đến database
3. Chạy queries để xác minh dữ liệu

### Query Bảng Customer

```sql
SELECT * FROM customer;
```

**Kết Quả:**
- Chi tiết customer được insert thành công
- `customerId` được tự động tạo

### Query Bảng Accounts

```sql
SELECT * FROM accounts;
```

**Kết Quả:**
- Số tài khoản ngẫu nhiên 10 chữ số được tạo
- `customerId` liên kết đến bảng customer
- Loại tài khoản và địa chỉ chi nhánh được điền

## Xử Lý Vấn Đề Dev Tools Restart

### Vấn Đề: Hot Swap Thất Bại

Khi thực hiện nhiều thay đổi, Spring DevTools có thể thất bại trong việc hot reload:
```
Hot swap failed
```

### Giải Pháp

1. **Dừng server thủ công**
2. **Clean và rebuild**: `mvn clean install`
3. **Khởi động lại server**

Điều này đảm bảo tất cả thay đổi được tải đúng cách.

## Tóm Tắt

Trong bài giảng toàn diện này, chúng ta đã triển khai:

### ✅ Triển Khai Tầng Service
- Chuyển đổi DTO thành Entity sử dụng mappers
- Lưu customer vào database
- Tạo và lưu account với số tài khoản ngẫu nhiên
- Liên kết account với customer qua `customerId`

### ✅ Xử Lý Custom Exception
- Tạo `CustomerAlreadyExistsException`
- Extends `RuntimeException`
- Sử dụng annotation `@ResponseStatus`

### ✅ Derived Named Methods
- `findByMobileNumber()` trong repository
- Tự động tạo query bởi Spring Data JPA
- Validation trước khi lưu

### ✅ Global Exception Handler
- Xử lý exception tập trung với `@ControllerAdvice`
- `@ExceptionHandler` cho exception cụ thể
- Phản hồi lỗi nhất quán

### ✅ Triển Khai Controller
- Constructor-based dependency injection
- `@AllArgsConstructor` cho constructor tự động
- Sử dụng `ResponseEntity` đúng cách

### ✅ Kiểm Thử
- Thiết lập và sử dụng Postman
- Validation kịch bản thành công
- Validation kịch bản exception
- Xác minh database qua H2 console

## Các Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ triển khai:
- **Read API** (lấy thông tin chi tiết account)
- **Update API** (sửa đổi account/customer)
- **Delete API** (xóa account)

Điều này sẽ hoàn thành các thao tác CRUD đầy đủ cho Accounts Microservice!

---

**Bạn có hào hứng không? Hãy tiếp tục xây dựng trong bài giảng tiếp theo!**




FILE: 14-trien-khai-fetch-account-api.md


# Triển Khai Fetch Account API

## Tổng Quan
Trong phần này, chúng ta sẽ tạo một REST API để truy xuất thông tin tài khoản và khách hàng từ cơ sở dữ liệu bằng cách nhận số điện thoại làm đầu vào. API sẽ trả về thông tin đầy đủ về khách hàng và tài khoản ngân hàng dựa trên số điện thoại được cung cấp.

## Bước 1: Tạo Phương Thức Controller

Đầu tiên, thêm một phương thức mới trong lớp `AccountsController`:

```java
@GetMapping("/fetch")
public ResponseEntity<CustomerDto> fetchAccountDetails(@RequestParam String mobileNumber) {
    CustomerDto customerDto = iAccountService.fetchAccount(mobileNumber);
    return ResponseEntity.status(HttpStatus.OK).body(customerDto);
}
```

**Các Điểm Chính:**
- Phương thức trả về `CustomerDto` được bọc trong `ResponseEntity`
- Sử dụng `@RequestParam` để nhận số điện thoại dưới dạng tham số truy vấn
- Ánh xạ đến endpoint `/api/fetch`
- Sử dụng annotation `@GetMapping` cho các thao tác đọc dữ liệu

## Bước 2: Định Nghĩa Phương Thức Service Interface

Thêm phương thức trừu tượng trong `IAccountService`:

```java
CustomerDto fetchAccount(String mobileNumber);
```

## Bước 3: Tạo ResourceNotFoundException

Tạo một lớp exception tùy chỉnh mới trong package exception:

```java
@ResponseStatus(value = HttpStatus.NOT_FOUND)
public class ResourceNotFoundException extends RuntimeException {
    
    public ResourceNotFoundException(String resourceName, String fieldName, String fieldValue) {
        super(String.format("%s not found with the given input data %s : '%s'", 
            resourceName, fieldName, fieldValue));
    }
}
```

**Chi Tiết Exception:**
- Trả về trạng thái `404 NOT_FOUND`
- Nhận ba tham số: tên resource, tên trường, và giá trị trường
- Cung cấp thông báo lỗi chi tiết cho client

## Bước 4: Thêm Phương Thức Global Exception Handler

Thêm xử lý exception trong `GlobalExceptionHandler`:

```java
@ExceptionHandler(ResourceNotFoundException.class)
public ResponseEntity<ErrorResponseDto> handleResourceNotFoundException(
        ResourceNotFoundException exception,
        WebRequest webRequest) {
    
    ErrorResponseDto errorResponseDto = new ErrorResponseDto(
        webRequest.getDescription(false),
        HttpStatus.NOT_FOUND,
        exception.getMessage(),
        LocalDateTime.now()
    );
    
    return new ResponseEntity<>(errorResponseDto, HttpStatus.NOT_FOUND);
}
```

## Bước 5: Triển Khai Logic Service

Triển khai phương thức `fetchAccount()` trong `AccountsServiceImpl`:

```java
@Override
public CustomerDto fetchAccount(String mobileNumber) {
    // Lấy thông tin khách hàng
    Customer customer = customerRepository.findByMobileNumber(mobileNumber)
        .orElseThrow(() -> new ResourceNotFoundException(
            "Customer", "mobileNumber", mobileNumber));
    
    // Lấy thông tin tài khoản
    Accounts accounts = accountsRepository.findByCustomerId(customer.getCustomerId())
        .orElseThrow(() -> new ResourceNotFoundException(
            "Account", "customerId", customer.getCustomerId().toString()));
    
    // Chuyển đổi sang DTOs
    CustomerDto customerDto = CustomerMapper.mapToCustomerDto(customer, new CustomerDto());
    customerDto.setAccountsDto(AccountsMapper.mapToAccountsDto(accounts, new AccountsDto()));
    
    return customerDto;
}
```

## Bước 6: Thêm Phương Thức Repository

Tạo phương thức mới trong `AccountsRepository`:

```java
Optional<Accounts> findByCustomerId(Long customerId);
```

Phương thức này truy vấn tài khoản theo customer ID, tận dụng khả năng tự động tạo query của Spring Data JPA.

## Bước 7: Cải Tiến CustomerDto

Thêm trường `AccountsDto` lồng nhau vào `CustomerDto` để trả về thông tin kết hợp:

```java
@Data
public class CustomerDto {
    private String name;
    private String email;
    private String mobileNumber;
    private AccountsDto accountsDto;  // Trường mới
}
```

**Các Tùy Chọn Thiết Kế:**
- **Tùy chọn 1:** Thêm trường `AccountsDto` trong `CustomerDto` (được khuyến nghị cho ứng dụng nhỏ)
- **Tùy chọn 2:** Tạo lớp DTO tổng hợp riêng biệt (tốt hơn cho ứng dụng phức tạp với nhiều trường)

## Kiểm Thử API

### Yêu Cầu Thành Công
**Endpoint:** `GET http://localhost:8080/api/fetch?mobileNumber=1234567890`

**Phản hồi:**
```json
{
    "name": "John Doe",
    "email": "john@example.com",
    "mobileNumber": "1234567890",
    "accountsDto": {
        "accountNumber": 123456789,
        "accountType": "Savings",
        "branchAddress": "123 Main Street"
    }
}
```

### Trường Hợp Lỗi
**Endpoint:** `GET http://localhost:8080/api/fetch?mobileNumber=9999999999`

**Phản hồi (404 NOT FOUND):**
```json
{
    "apiPath": "/api/fetch",
    "errorCode": "NOT_FOUND",
    "errorMessage": "Customer not found with the given input data mobileNumber : '9999999999'",
    "errorTime": "2024-03-09T10:30:45"
}
```

## Các Lưu Ý Quan Trọng

1. **Mất Dữ Liệu H2 Database:** Dữ liệu bị mất khi server khởi động lại (vấn đề tạm thời cho đến khi chuyển sang MySQL)
2. **Tham Số Truy Vấn:** Đảm bảo tên `@RequestParam` khớp với tên tham số
3. **Xử Lý Exception:** Luôn xác minh các exception handler được cấu hình đúng
4. **Kiểm Thử:** Unit testing và debugging rất quan trọng để phát hiện các lỗi nhỏ

## Các Điểm Chính Cần Nhớ

- Sử dụng `@GetMapping` cho các thao tác đọc dữ liệu
- `@RequestParam` nhận các tham số truy vấn
- Exception tùy chỉnh cung cấp thông tin lỗi chi tiết
- DTO pattern ngăn chặn việc lộ thông tin entity nhạy cảm
- Phương thức Repository có thể được tự động tạo bởi Spring Data JPA
- DTO lồng nhau cho phép trả về phản hồi tổng hợp

## Các Bước Tiếp Theo

Trong phần tiếp theo, chúng ta sẽ triển khai các thao tác cập nhật và xóa để hoàn thiện chức năng CRUD cho accounts microservice.




FILE: 15-trien-khai-update-account-api.md


# Triển Khai Update Account API

## Tổng Quan

Trong bài học này, chúng ta sẽ xây dựng REST API cho phép ứng dụng khách cập nhật thông tin tài khoản trong Accounts Microservice. API này bổ sung cho các API tạo và lấy thông tin tài khoản đã có.

## Yêu Cầu

### Các Trường Có Thể Cập Nhật
- Tên khách hàng
- Địa chỉ email
- Số điện thoại
- Loại tài khoản
- Địa chỉ chi nhánh

### Quy Tắc Nghiệp Vụ: Số Tài Khoản Không Thể Thay Đổi
**Quan trọng**: Sau khi số tài khoản được tạo, nó **không thể được cập nhật** bởi người dùng cuối. Số tài khoản đóng vai trò là định danh chính và phải luôn không đổi.

## Các Bước Triển Khai

### 1. Tầng Service - Interface IAccountService

Đầu tiên, tạo một phương thức trừu tượng trong interface `IAccountService`:

```java
boolean updateAccount(CustomerDto customerDto);
```

**Chi Tiết Phương Thức:**
- **Kiểu Trả Về**: `boolean` - cho biết thao tác cập nhật có thành công hay không
- **Tham Số**: `CustomerDto` - chứa dữ liệu đã cập nhật từ ứng dụng khách

### 2. Triển Khai Service - Class AccountService

Override phương thức `updateAccount` trong class `AccountService`:

#### Logic Triển Khai

1. **Khởi Tạo Cờ Kết Quả**
   ```java
   boolean isUpdated = false;
   ```

2. **Trích Xuất Thông Tin Tài Khoản**
   - Lấy `AccountsDto` từ `CustomerDto`
   - Trích xuất số tài khoản từ DTO

3. **Lấy Tài Khoản Hiện Có**
   - Sử dụng số tài khoản làm tiêu chí tìm kiếm (vì nó là primary key)
   - Dùng phương thức `findById()` từ Spring Data JPA
   - Annotation `@Id` đánh dấu số tài khoản là primary key
   - Nếu không tìm thấy bản ghi, ném ra `ResourceNotFoundException`

4. **Cập Nhật Dữ Liệu Tài Khoản**
   - Ánh xạ dữ liệu từ DTO sang Accounts entity bằng `mapper()`
   - Gọi phương thức `save()` trên `AccountsRepository`
   - Tài khoản đã cập nhật được trả về và lưu trữ

5. **Lấy và Cập Nhật Khách Hàng**
   - Trích xuất `customerId` từ đối tượng Accounts đã cập nhật
   - Sử dụng `findById()` với `CustomerRepository`
   - Nếu không có bản ghi khách hàng, ném ra `ResourceNotFoundException`
   - Ánh xạ dữ liệu cập nhật từ DTO sang Customer entity
   - Gọi phương thức `save()` trên `CustomerRepository`

6. **Trả Về Trạng Thái Thành Công**
   - Đặt `isUpdated = true`
   - Trả về giá trị boolean cho tầng controller

#### Hiểu Về Phương Thức save() Của Spring Data JPA

Phương thức `save()` rất thông minh:
- **Nếu không có giá trị primary key**: Thực hiện thao tác **INSERT**
- **Nếu có giá trị primary key**: Thực hiện thao tác **UPDATE**

### 3. Tầng Controller - AccountsController

Tạo một phương thức mới để xử lý các yêu cầu cập nhật:

```java
@PutMapping("/update")
public ResponseEntity<ResponseDto> updateAccountDetails(@RequestBody CustomerDto customerDto) {
    boolean isUpdated = iAccountService.updateAccount(customerDto);
    
    if (isUpdated) {
        return ResponseEntity
            .status(HttpStatus.OK)
            .body(new ResponseDto(StatusCode.STATUS_200, "Yêu cầu đã được xử lý thành công"));
    } else {
        return ResponseEntity
            .status(HttpStatus.INTERNAL_SERVER_ERROR)
            .body(new ResponseDto(StatusCode.STATUS_500, 
                "Đã xảy ra lỗi. Vui lòng thử lại hoặc liên hệ đội phát triển"));
    }
}
```

**Chi Tiết Endpoint:**
- **Phương Thức HTTP**: PUT
- **Đường Dẫn**: `/api/update`
- **Request Body**: `CustomerDto` với thông tin đã cập nhật
- **Phản Hồi Thành Công**: 200 OK - "Yêu cầu đã được xử lý thành công"
- **Phản Hồi Lỗi**: 500 Internal Server Error

## Kiểm Thử

### Test Case Tích Cực

1. **Tạo tài khoản** bằng create API
2. **Lấy tài khoản** bằng get API với số điện thoại
3. **Cập nhật tài khoản** bằng cách sửa đổi dữ liệu phản hồi:
   - Thay đổi tên (ví dụ: "Madan Reddy" → "Madan Mohan")
   - Thay đổi email (ví dụ: "tutor@eazybytes.com" → "madan@eazybytes.com")
   - Thay đổi số điện thoại
   - Thay đổi loại tài khoản (ví dụ: "Savings" → "Current")
   - Thay đổi địa chỉ chi nhánh
4. **Gửi yêu cầu PUT** đến `/api/update`
5. **Xác minh**: Lấy lại tài khoản với số điện thoại mới
6. **Kết quả**: Tất cả các trường đã cập nhật phải phản ánh giá trị mới

### Test Case Tiêu Cực

1. **Cung cấp một số tài khoản không tồn tại** trong yêu cầu
2. **Gửi yêu cầu PUT**
3. **Kết Quả Mong Đợi**: Phản hồi lỗi với thông báo "Không tìm thấy tài khoản với số tài khoản: [giá trị]"

## Vấn Đề Đã Biết: Các Trường Auditing

### Lỗi Hiện Tại
Khi cập nhật bản ghi, các trường `updatedAt` và `updatedBy` **không được tự động cập nhật**. Điều này là do chúng ta không điền thủ công các giá trị này khi lưu bản ghi vào cơ sở dữ liệu.

### Giải Pháp (Sắp Tới)
Lỗi này sẽ được khắc phục trong các bài học sắp tới bằng cách triển khai **các thay đổi liên quan đến auditing**. Spring Data JPA framework sẽ tự động xử lý:
- `createdAt`
- `createdBy`
- `updatedAt`
- `updatedBy`

Hiện tại, chúng ta có thể chấp nhận lỗi nhỏ này tạm thời.

## Những Điểm Chính Cần Nhớ

1. **Tính Bất Biến Của Số Tài Khoản**: Số tài khoản không thể thay đổi sau khi được tạo, đảm bảo tính toàn vẹn dữ liệu
2. **Sử Dụng Primary Key**: Việc dùng `findById()` tận dụng primary key để truy vấn cơ sở dữ liệu hiệu quả
3. **Phương Thức save() Thông Minh**: Tự động xác định thực hiện insert hay update dựa trên sự hiện diện của primary key
4. **Xử Lý Lỗi Đúng Cách**: Ném `ResourceNotFoundException` cho các bản ghi bị thiếu
5. **Kiến Trúc Phân Lớp**: Tách biệt các mối quan tâm giữa tầng service và controller

## Tiếp Theo Là Gì?

Trong bài học tiếp theo, chúng ta sẽ triển khai **Delete Account API** để hoàn thành các thao tác CRUD cho Accounts Microservice.

---

**Lưu ý**: Các ví dụ code đầy đủ có thể tìm thấy trong kho lưu trữ GitHub được đề cập trong bài học.




FILE: 16-trien-khai-delete-account-api.md


# Triển Khai Delete Account API

## Tổng Quan
Trong phần này, chúng ta sẽ tạo một REST API trong accounts microservice để xóa thông tin khách hàng và tài khoản hiện có dựa trên số điện thoại di động.

## Thiết Kế API
API xóa sẽ:
- Nhận số điện thoại di động làm tham số đầu vào
- Tải thông tin customer entity từ cơ sở dữ liệu bằng số điện thoại
- Trích xuất customerId từ customer entity
- Xóa các bản ghi từ cả hai bảng accounts và customer sử dụng customerId

## Các Bước Triển Khai

### 1. Tạo Phương Thức Trong Service Interface
Đầu tiên, tạo một phương thức mới trong interface `IAccountService`:

```java
boolean deleteAccount(String mobileNumber);
```

Phương thức này:
- Trả về giá trị boolean cho biết thao tác xóa có thành công hay không
- Nhận số điện thoại di động làm tham số đầu vào

### 2. Triển Khai Phương Thức Service
Trong class `AccountService`, triển khai phương thức `deleteAccount()`:

```java
@Override
public boolean deleteAccount(String mobileNumber) {
    Customer customer = customerRepository.findByMobileNumber(mobileNumber)
        .orElseThrow(() -> new ResourceNotFoundException("Customer", "mobileNumber", mobileNumber));
    
    accountsRepository.deleteByCustomerId(customer.getCustomerId());
    customerRepository.deleteById(customer.getCustomerId());
    
    return true;
}
```

**Chi Tiết Triển Khai:**
1. Lấy thông tin customer sử dụng `findByMobileNumber()` từ `CustomerRepository`
2. Nếu không tồn tại bản ghi, throw `ResourceNotFoundException`
3. Lấy customerId từ customer entity
4. Xóa bản ghi account sử dụng `deleteByCustomerId()`
5. Xóa bản ghi customer sử dụng `deleteById()`

### 3. Tạo Phương Thức Delete Tùy Chỉnh Trong Repository
Thêm phương thức delete tùy chỉnh trong `AccountsRepository`:

```java
@Transactional
@Modifying
void deleteByCustomerId(Long customerId);
```

**Các Annotation Quan Trọng:**
- `@Transactional`: Đảm bảo query chạy trong một transaction
- `@Modifying`: Thông báo cho Spring Data JPA rằng phương thức này sẽ thay đổi dữ liệu

**Tại Sao Cần Các Annotation Này:**
- Các phương thức tùy chỉnh update hoặc delete dữ liệu cần các annotation này
- `@Transactional` đảm bảo rằng nếu có lỗi xảy ra khi runtime, mọi thay đổi một phần sẽ được rollback
- Các phương thức framework như `deleteById()` đã có các annotation này tích hợp sẵn
- Các phương thức tùy chỉnh cần annotation rõ ràng để thông báo cho framework về việc sửa đổi dữ liệu

**Tại Sao Không Sử Dụng `deleteById()` Cho Accounts?**
- `deleteById()` yêu cầu primary key (account number trong trường hợp này)
- Để sử dụng `deleteById()`, chúng ta cần thực hiện một query bổ sung để lấy account number
- Sử dụng `deleteByCustomerId()` hiệu quả hơn vì chúng ta đã có customerId

### 4. Tạo Phương Thức Controller
Thêm endpoint delete trong controller class:

```java
@DeleteMapping("/delete")
public ResponseEntity<ResponseDto> deleteAccountDetails(@RequestParam String mobileNumber) {
    boolean isDeleted = iAccountService.deleteAccount(mobileNumber);
    
    if (isDeleted) {
        return ResponseEntity
            .status(HttpStatus.OK)
            .body(new ResponseDto(StatusConstants.STATUS_200, StatusConstants.MESSAGE_200));
    } else {
        return ResponseEntity
            .status(HttpStatus.INTERNAL_SERVER_ERROR)
            .body(new ResponseDto(StatusConstants.STATUS_500, StatusConstants.MESSAGE_500));
    }
}
```

**Chi Tiết Controller:**
- Sử dụng annotation `@DeleteMapping` cho phương thức HTTP DELETE
- Đường dẫn API: `/api/delete`
- Nhận số điện thoại di động làm query parameter
- Trả về:
  - Status 200 với thông báo thành công nếu xóa thành công
  - Status 500 với thông báo lỗi nếu xóa thất bại

## Kiểm Thử API

### Kịch Bản 1: Xóa Thành Công
1. Tạo một tài khoản mới với số điện thoại
2. Xác minh tài khoản tồn tại bằng GET API
3. Gọi DELETE API: `/api/delete?mobileNumber={mobileNumber}`
4. Nhận phản hồi thành công (Status 200)
5. Xác minh việc xóa bằng cách gọi GET API - sẽ trả về 404 Not Found

### Kịch Bản 2: Xóa Bản Ghi Không Tồn Tại
1. Gọi DELETE API với số điện thoại không tồn tại
2. Sẽ nhận lỗi 404 Not Found
3. Đây là hành vi mong đợi vì không có dữ liệu để xóa

## Các Khái Niệm Chính

### Phương Thức Delete Tùy Chỉnh Trong Spring Data JPA
- Mẫu tên phương thức: `deleteBy{TênTrường}`
- Spring Data JPA tự động tạo delete query
- Tương tự như `findBy` cho SELECT query, `deleteBy` chỉ định DELETE query

### Quản Lý Transaction
- Tất cả các thao tác xóa nên chạy trong một transaction
- Nếu có lỗi xảy ra, transaction sẽ được rollback
- Ngăn chặn việc xóa dữ liệu một phần (ví dụ: xóa account nhưng không xóa customer)

### Tính Toàn Vẹn Dữ Liệu
- Cả bản ghi customer và account đều được xóa cùng nhau
- Sử dụng customerId đảm bảo tính toàn vẹn tham chiếu
- Transaction đảm bảo thao tác nguyên tử

## Tóm Tắt
Chúng ta đã triển khai thành công thao tác DELETE, hoàn thành tất cả bốn thao tác CRUD:
- **C**reate - Create account API
- **R**ead - Fetch account API
- **U**pdate - Update account API
- **D**elete - Delete account API

## Các Bước Tiếp Theo
Các chủ đề quan trọng sau sẽ được đề cập tiếp theo:
1. Xử lý RuntimeException đúng cách
2. Audit các cột metadata với Spring Data JPA
3. Tài liệu hóa REST APIs

## Lưu Ý
Khi khởi động lại ứng dụng với H2 database, tất cả dữ liệu sẽ bị mất. Đây là tạm thời trong quá trình phát triển. Sau này, khi chuyển sang MySQL database, dữ liệu sẽ được duy trì lâu dài.




FILE: 17-xu-ly-ngoai-le-runtime-voi-global-exception-handler.md


# Xử Lý Ngoại Lệ Runtime với Global Exception Handler

## Tổng Quan

Trong bài giảng này, chúng ta sẽ học cách xử lý các ngoại lệ runtime trong các REST API của Accounts microservice bằng cách sử dụng phương pháp global exception handler. Điều này đảm bảo các phản hồi lỗi thích hợp được gửi đến ứng dụng client khi xảy ra lỗi không mong đợi.

## Tình Trạng Hiện Tại

Accounts microservice của chúng ta hiện có bốn REST API hỗ trợ các thao tác CRUD. `GlobalExceptionHandler` hiện tại chỉ xử lý hai ngoại lệ nghiệp vụ:
- `ResourceNotFoundException`
- `CustomerAlreadyExistException`

Đây là các ngoại lệ do người dùng định nghĩa, nhưng chúng ta cần xử lý các ngoại lệ runtime có thể xảy ra bất cứ lúc nào và ở bất kỳ vị trí nào trong ứng dụng.

## Triển Khai Xử Lý Ngoại Lệ Toàn Cục

### Bước 1: Thêm Exception Handler Tổng Quát

Để xử lý tất cả các ngoại lệ runtime, chúng ta cần thêm một phương thức exception handler mới trong lớp `GlobalExceptionHandler`:

```java
@ExceptionHandler(Exception.class)
public ResponseEntity<ErrorResponseDto> handleGlobalException(
    Exception exception,
    WebRequest webRequest
) {
    ErrorResponseDto errorResponseDto = new ErrorResponseDto(
        webRequest.getDescription(false),
        HttpStatus.INTERNAL_SERVER_ERROR,
        exception.getMessage(),
        LocalDateTime.now()
    );
    
    return new ResponseEntity<>(errorResponseDto, HttpStatus.INTERNAL_SERVER_ERROR);
}
```

### Cách Hoạt Động

1. **Phân Cấp Ngoại Lệ**: Lớp `Exception` trong Java đại diện cho tất cả các loại ngoại lệ (checked và unchecked)
2. **Xử Lý Ưu Tiên**: Spring Boot framework tìm kiếm các phương thức handler khớp chính xác với ngoại lệ trước
3. **Cơ Chế Dự Phòng**: Nếu không có handler cụ thể nào tồn tại, exception handler tổng quát sẽ được gọi

### Cấu Trúc Phản Hồi

Phản hồi lỗi bao gồm:
- **API Path**: Endpoint được gọi
- **HTTP Status**: `INTERNAL_SERVER_ERROR` (500)
- **Error Message**: Thông báo ngoại lệ thực tế từ Spring Boot
- **Timestamp**: Ngày và giờ hiện tại

## Cơ Hội Cải Tiến

Trong các ứng dụng thực tế, bạn có thể cải tiến phương thức này để:
- Kích hoạt thông báo email cho đội ngũ vận hành
- Ghi log vào bảng cơ sở dữ liệu để theo dõi ngoại lệ
- Tạo báo cáo để phân tích
- Triển khai logic nghiệp vụ tùy chỉnh dựa trên yêu cầu

## Kiểm Thử Global Exception Handler

### Tạo Kịch Bản Kiểm Thử

Để kiểm thử xử lý ngoại lệ runtime, chúng ta có thể cố ý tạo ra `NullPointerException`:

1. Xóa annotation `@AllArgsConstructor` khỏi `AccountsController`
2. Điều này chỉ để lại constructor mặc định
3. Không có constructor, autowiring sẽ không xảy ra
4. Trường `IAccountService` vẫn là null
5. Bất kỳ thao tác API nào cũng sẽ ném ra `NullPointerException`

### Các Bước Kiểm Thử

1. Thực hiện các thay đổi và rebuild ứng dụng
2. Kiểm thử bất kỳ endpoint API nào (ví dụ: Create Account API)
3. Gửi request đến endpoint

### Phản Hồi Mong Đợi

```json
{
    "apiPath": "/api/create",
    "errorCode": "INTERNAL_SERVER_ERROR",
    "errorMessage": "Cannot invoke method because object is null",
    "timestamp": "2024-03-09T10:30:00"
}
```

Mã trạng thái HTTP sẽ là **500 Internal Server Error**.

## Các Khái Niệm Chính

### Annotation @ControllerAdvice

Annotation này cho phép xử lý ngoại lệ toàn cục trên tất cả các controller trong ứng dụng.

### Annotation @ExceptionHandler

Annotation này đánh dấu một phương thức là exception handler cho các loại ngoại lệ cụ thể.

### Mẫu Triển Khai

Sự kết hợp của `@ControllerAdvice` và `@ExceptionHandler` cho phép bạn:
1. Tập trung hóa logic xử lý ngoại lệ
2. Xử lý ngoại lệ toàn cục trên tất cả các controller
3. Cung cấp phản hồi lỗi nhất quán
4. Tách biệt xử lý lỗi khỏi logic nghiệp vụ

## Câu Hỏi Phỏng Vấn

**Hỏi: Làm thế nào để triển khai logic ngoại lệ toàn cục trong ứng dụng Spring Boot?**

**Đáp:** Sử dụng sự kết hợp của các annotation `@ControllerAdvice` và `@ExceptionHandler`:
- Tạo một lớp được đánh dấu với `@ControllerAdvice`
- Định nghĩa các phương thức được đánh dấu với `@ExceptionHandler`
- Chỉ định (các) loại ngoại lệ cần xử lý
- Triển khai logic phản hồi lỗi trong phương thức

## Tóm Tắt

- Xử lý ngoại lệ toàn cục đảm bảo tất cả các ngoại lệ runtime được xử lý đúng cách
- Handler `Exception.class` hoạt động như bộ bắt lỗi cho tất cả các ngoại lệ chưa được xử lý
- Spring Boot ưu tiên các exception handler cụ thể hơn handler tổng quát
- Phương pháp này cung cấp phản hồi lỗi nhất quán cho ứng dụng client
- Kiến thức thiết yếu cho việc phát triển REST API với Spring Boot

## Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ tiếp tục xây dựng kiến trúc microservices với các tính năng và thực hành tốt nhất bổ sung.

---

**Lưu ý**: Xử lý ngoại lệ đúng cách là rất quan trọng đối với các ứng dụng production và thể hiện thực hành phát triển Spring Boot chuyên nghiệp.




FILE: 18-validation-du-lieu-dau-vao-trong-rest-apis.md


# Validation Dữ Liệu Đầu Vào Trong REST APIs

## Tổng Quan

Khi xây dựng microservices và REST APIs, việc thực hiện validation trên dữ liệu đầu vào nhận từ các ứng dụng client là rất quan trọng. Bài học này đề cập đến việc triển khai input validation trong ứng dụng Spring Boot microservices để đảm bảo tính toàn vẹn dữ liệu và ngăn chặn các truy vấn cơ sở dữ liệu không cần thiết với dữ liệu không hợp lệ.

## Tại Sao Input Validation Quan Trọng

### Các Trường Hợp Validation Phổ Biến

- **Số Điện Thoại**: Người dùng có thể gửi 5 hoặc 9 chữ số thay vì 10 chữ số yêu cầu
- **Định Dạng Email**: Người dùng có thể không tuân theo định dạng email đúng (thiếu ký tự @, tên miền, v.v.)
- **Độ Dài Tên**: Người dùng có thể gửi tên quá ngắn (2-3 ký tự)
- **Trường Rỗng**: Người dùng có thể gửi giá trị rỗng hoặc null cho các trường bắt buộc

### Lợi Ích Của Input Validation

1. **Ngăn Chặn Truy Vấn Database Không Hợp Lệ**: Từ chối dữ liệu không hợp lệ trước khi nó đến tầng database
2. **Cải Thiện Hiệu Suất**: Tránh các thao tác database không cần thiết
3. **Trải Nghiệm Người Dùng Tốt Hơn**: Cung cấp thông báo lỗi rõ ràng cho clients
4. **Tính Toàn Vẹn Dữ Liệu**: Đảm bảo dữ liệu đáp ứng yêu cầu nghiệp vụ

## Các Bước Triển Khai

### Bước 1: Thêm Dependency Validation

Đảm bảo dependency sau có trong `pom.xml`:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-validation</artifactId>
</dependency>
```

Dependency này cung cấp tất cả các annotation và thư viện validation cần thiết.

### Bước 2: Thêm Validation Annotations Vào DTOs

#### Validations Cho CustomerDto

```java
public class CustomerDto {
    
    @NotEmpty(message = "Name cannot be null or empty")
    @Size(min = 5, max = 30, message = "The length of the customer name should be between 5 and 30")
    private String name;
    
    @NotEmpty(message = "Email address cannot be null or empty")
    @Email(message = "Email address should be a valid value")
    private String email;
    
    @Pattern(regexp = "(^$|[0-9]{10})", message = "Mobile number must be 10 digits")
    private String mobileNumber;
}
```

#### Validations Cho AccountsDto

```java
public class AccountsDto {
    
    @NotEmpty(message = "Account number cannot be null or empty")
    @Pattern(regexp = "(^$|[0-9]{10})", message = "Account number must be 10 digits")
    private Long accountNumber;
    
    @NotEmpty(message = "Account type cannot be null or empty")
    private String accountType;
    
    @NotEmpty(message = "Branch address cannot be null or empty")
    private String branchAddress;
}
```

### Bước 3: Các Annotation Validation Phổ Biến

Package `jakarta.validation.constraints` cung cấp nhiều annotation validation khác nhau:

- **@NotEmpty**: Trường không được null hoặc rỗng
- **@NotNull**: Trường không được null
- **@NotBlank**: Trường không được để trống (khoảng trắng)
- **@Size**: Chỉ định độ dài min và max
- **@Email**: Validate định dạng email
- **@Pattern**: Validate theo mẫu regex
- **@Digits**: Chỉ chấp nhận giá trị số
- **@Min / @Max**: Validate phạm vi số
- **@Future / @Past**: Validate ngày tháng
- **@Positive / @Negative**: Validate dấu của số

### Bước 4: Kích Hoạt Validation Trong Controller

Thêm các annotation validation vào controller:

```java
@RestController
@RequestMapping("/api")
@Validated
@AllArgsConstructor
public class AccountsController {
    
    @PostMapping("/create")
    public ResponseEntity<ResponseDto> createAccount(
        @Valid @RequestBody CustomerDto customerDto) {
        // Implementation
    }
    
    @PutMapping("/update")
    public ResponseEntity<ResponseDto> updateAccountDetails(
        @Valid @RequestBody CustomerDto customerDto) {
        // Implementation
    }
    
    @GetMapping("/fetch")
    public ResponseEntity<CustomerDto> fetchAccountDetails(
        @RequestParam 
        @Pattern(regexp = "(^$|[0-9]{10})", message = "Mobile number must be 10 digits")
        String mobileNumber) {
        // Implementation
    }
    
    @DeleteMapping("/delete")
    public ResponseEntity<ResponseDto> deleteAccountDetails(
        @RequestParam 
        @Pattern(regexp = "(^$|[0-9]{10})", message = "Mobile number must be 10 digits")
        String mobileNumber) {
        // Implementation
    }
}
```

**Các Annotation Chính:**
- **@Validated**: Kích hoạt validation trên controller class
- **@Valid**: Kích hoạt validation trên request body
- **@Pattern**: Validate request parameters theo regex

### Bước 5: Xử Lý Validation Exceptions

Tạo global exception handler để xử lý các lỗi validation:

```java
@ControllerAdvice
public class GlobalExceptionHandler extends ResponseEntityExceptionHandler {
    
    @Override
    protected ResponseEntity<Object> handleMethodArgumentNotValid(
            MethodArgumentNotValidException exception,
            HttpHeaders headers,
            HttpStatusCode status,
            WebRequest request) {
        
        Map<String, String> validationErrors = new HashMap<>();
        
        List<ObjectError> validationErrorList = exception.getBindingResult().getAllErrors();
        
        validationErrorList.forEach((error) -> {
            String fieldName = ((FieldError) error).getField();
            String validationMsg = error.getDefaultMessage();
            validationErrors.put(fieldName, validationMsg);
        });
        
        return new ResponseEntity<>(validationErrors, HttpStatus.BAD_REQUEST);
    }
}
```

**Chi Tiết Triển Khai:**
1. Kế thừa class `ResponseEntityExceptionHandler`
2. Override phương thức `handleMethodArgumentNotValid()`
3. Trích xuất tất cả lỗi validation từ exception
4. Tạo map các tên trường và thông báo lỗi
5. Trả về các lỗi dưới dạng response với status `BAD_REQUEST`

## Kiểm Thử Validation

### Ví Dụ 1: Request Create Không Hợp Lệ

**Request:**
```json
{
    "name": "A",
    "email": "invalid-email",
    "mobileNumber": "123456789"
}
```

**Response (400 Bad Request):**
```json
{
    "name": "The length of the customer name should be between 5 and 30",
    "email": "Email address should be a valid value",
    "mobileNumber": "Mobile number must be 10 digits"
}
```

### Ví Dụ 2: Request Create Hợp Lệ

**Request:**
```json
{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "mobileNumber": "1234567890"
}
```

**Response (200 OK):**
```json
{
    "statusCode": "201",
    "statusMsg": "Account created successfully"
}
```

### Ví Dụ 3: Query Parameter Không Hợp Lệ

**Request:**
```
GET /api/fetch?mobileNumber=12345
```

**Response (400 Bad Request):**
```json
{
    "mobileNumber": "Mobile number must be 10 digits"
}
```

## Best Practices

1. **Luôn validate dữ liệu đầu vào** ở tầng API trước khi xử lý
2. **Cung cấp thông báo lỗi rõ ràng** giúp clients hiểu vấn đề gì đã xảy ra
3. **Sử dụng annotation validation phù hợp** dựa trên yêu cầu nghiệp vụ
4. **Validate cả request body và query parameters** một cách nhất quán
5. **Không validate response DTOs** (như ResponseDto, ErrorResponseDto) vì chúng chỉ dùng để gửi dữ liệu cho clients
6. **Giữ các quy tắc validation đồng bộ** giữa các operations khác nhau (create, update, v.v.)
7. **Xem xét các validation đặc thù nghiệp vụ** ngoài các kiểm tra định dạng chuẩn

## Tóm Tắt

Input validation là một khía cạnh quan trọng trong việc xây dựng REST APIs mạnh mẽ. Bằng cách sử dụng validation framework của Spring Boot:

- Chúng ta đảm bảo chất lượng dữ liệu trước khi nó đến business logic
- Chúng ta cung cấp thông báo lỗi có ý nghĩa cho các ứng dụng client
- Chúng ta ngăn chặn các thao tác database không cần thiết
- Chúng ta tuân theo các best practices trong phát triển API

Validation framework rất linh hoạt và có thể được mở rộng dựa trên yêu cầu nghiệp vụ cụ thể.

---

**Bước Tiếp Theo**: Tiếp tục nâng cao microservices của bạn với các tính năng và best practices bổ sung.




FILE: 19-tai-lieu-hoa-rest-apis-voi-openapi-specification.md


# Tài Liệu Hóa REST APIs với OpenAPI Specification

## Tại Sao Cần Tài Liệu Hóa REST APIs?

Khi xây dựng microservices và REST APIs, việc tài liệu hóa trở nên cực kỳ quan trọng khi:
- Cung cấp APIs cho các bên ngoài hoặc các team khác trong tổ chức
- Làm việc với team UI hoặc team phát triển ứng dụng mobile
- Hợp tác với team testing cần hiểu về hành vi của API

Không có tài liệu phù hợp, bạn sẽ phải trả lời liên tục các câu hỏi về:
- Định dạng request
- Định dạng response
- Các quy tắc validation

Thay vì phải tổ chức nhiều cuộc họp để giải thích về APIs, việc tài liệu hóa chúng theo tiêu chuẩn công nghiệp sẽ tiết kiệm thời gian và công sức.

## OpenAPI Specification

OpenAPI là một tiêu chuẩn cộng đồng mã nguồn mở cung cấp phương thức chuẩn hóa để định nghĩa các HTTP APIs như REST APIs. Nó cho phép người tiêu dùng:
- Nhanh chóng khám phá cách một API hoạt động
- Cấu hình cơ sở hạ tầng
- Tự động sinh client code và server code
- Tạo các test cases tự động

## Bắt Đầu với SpringDoc OpenAPI

Việc tài liệu hóa trở nên đơn giản với thư viện **SpringDoc OpenAPI** có sẵn tại [springdoc.org](https://springdoc.org).

### Thêm Dependency

Thêm Maven dependency sau vào file `pom.xml` của bạn:

```xml
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>${springdoc.version}</version>
</dependency>
```

**Lưu Ý Quan Trọng Về Phiên Bản:**
- Cho Spring Boot 3.x trở lên: Sử dụng phiên bản springdoc-openapi mới nhất
- Cho Spring Boot 2.x hoặc 1.x: Sử dụng springdoc-openapi v1.7.0

### Các Bước Triển Khai

1. Thêm dependency vào file `pom.xml`
2. Load các thay đổi Maven để tải dependency
3. Build và khởi động lại ứng dụng
4. Truy cập Swagger UI tại: `http://localhost:8080/swagger-ui/index.html`

## Tính Năng Của Tài Liệu Tự Động

Sau khi cấu hình, SpringDoc OpenAPI tự động quét các REST APIs và tạo tài liệu bao gồm:

### Các API Endpoints
- Tất cả các đường dẫn REST API từ controllers
- Các thao tác HTTP được hỗ trợ (GET, POST, PUT, DELETE)

### Thông Tin Request
- Các tham số request (path variables, query params)
- Định dạng và cấu trúc request body
- Các trường bắt buộc và tùy chọn
- Quy tắc validation (min/max length, patterns, v.v.)

### Thông Tin Response
- Mã status code
- Cấu trúc response body
- Định dạng thành công và lỗi

### Tài Liệu Schema
Tất cả các DTO objects (Data Transfer Objects) được tài liệu hóa với:
- Tên và kiểu dữ liệu của các trường
- Ràng buộc validation từ các annotations
- Cấu trúc đối tượng lồng nhau

## Ví Dụ: Tài Liệu AccountsController

Tài liệu được tạo ra sẽ hiển thị:

**Update Account API (PUT)**
- Chấp nhận: JSON body với cấu trúc CustomerDto
- Các trường bắt buộc: name, email, mobile number
- Validation: Định dạng email, pattern số điện thoại
- Response: Status code 200 với statusCode và statusMessage

**Create Account API (POST)**
- Chấp nhận: Schema CustomerDto
- Response: Status code và status message

**Fetch Account API (GET)**
- Chấp nhận: Query parameter (mobile number) - bắt buộc
- Response: CustomerDto với đầy đủ thông tin customer và account

**Delete Account API (DELETE)**
- Chấp nhận: Query parameter (mobile number)
- Response: Status code và status message

## Lợi Ích

1. **Tự Kiểm Thử**: Developers có thể test APIs trực tiếp từ Swagger UI
2. **Giao Tiếp Rõ Ràng**: Loại bỏ việc giải thích lặp đi lặp lại
3. **Tài Liệu Chuyên Nghiệp**: Định dạng theo tiêu chuẩn công nghiệp
4. **Dễ Dàng Tích Hợp**: Yêu cầu thiết lập tối thiểu
5. **Cập Nhật Tự Động**: Tài liệu cập nhật khi code thay đổi

## Thực Hành Tốt Nhất

- Luôn thêm SpringDoc OpenAPI dependency vào microservices của bạn
- Tài liệu hóa trước khi deploy lên production
- Tránh việc phải giải thích APIs thủ công cho từng người tiêu dùng
- Sử dụng đây là baseline; nâng cao thêm với các annotations tùy chỉnh cho output chuyên nghiệp hơn

## Bước Tiếp Theo

Mặc dù tài liệu cơ bản đã hoạt động tốt, bạn có thể nâng cao thêm bằng cách:
- Thêm mô tả và ví dụ tùy chỉnh
- Sử dụng các annotations của SpringDoc để làm rõ hơn
- Cung cấp giá trị mẫu cho các DTOs
- Làm cho tài liệu chuyên nghiệp và sẵn sàng cho production hơn

Thiết lập cơ bản này cung cấp tài liệu xuất sắc với nỗ lực tối thiểu, giúp REST APIs của bạn dễ dàng sử dụng và kiểm thử.




FILE: 2-architecture-patterns-comparison.md


# So Sánh Các Mô Hình Kiến Trúc: Monolithic vs SOA vs Microservices

## Tổng Quan

Tài liệu này cung cấp so sánh chi tiết về ba mô hình kiến trúc chính: Monolithic, Service-Oriented Architecture (SOA), và Microservices. Hiểu rõ những khác biệt này là rất quan trọng để đưa ra quyết định kiến trúc đúng đắn.

## Đặc Điểm Kiến Trúc

### Kiến Trúc Monolithic

**Đặc Điểm Chính:**
- Toàn bộ codebase được triển khai trong một server duy nhất
- Database hỗ trợ duy nhất
- Các thành phần liên kết chặt chẽ
- Tất cả logic nghiệp vụ ở một nơi

**Biểu Diễn Trực Quan:**
```
┌─────────────────────────────┐
│   Server Đơn                │
│  ┌─────────────────────┐   │
│  │ UI + Logic Nghiệp Vụ│   │
│  │ (Liên Kết Chặt)     │   │
│  └─────────────────────┘   │
└─────────────────────────────┘
          ↓
   Database Đơn
```

### Kiến Trúc SOA (Service-Oriented Architecture)

**Đặc Điểm Chính:**
- Tách biệt logic UI và backend
- Yêu cầu thành phần middleware (ESB)
- Phức tạp để bảo trì
- Chi phí đầu tư cao
- Database hỗ trợ duy nhất
- **Services hạt thô (coarse-grained)**

**Biểu Diễn Trực Quan:**
```
┌──────────────┐
│  UI Server   │
└──────────────┘
       ↓
┌──────────────┐
│     ESB      │ (Middleware)
└──────────────┘
       ↓
┌──────────────┐
│Backend Server│
│  (Tài khoản, │
│  Thẻ, Vay)   │
└──────────────┘
       ↓
Database Đơn
```

### Kiến Trúc Microservices

**Đặc Điểm Chính:**
- Logic backend được tách theo domain nghiệp vụ
- Mỗi microservice được triển khai trên server/container riêng
- Mỗi microservice có database riêng
- Công nghệ database có thể khác nhau cho mỗi service (RDBMS, NoSQL, Redis, v.v.)
- **Services hạt mịn (fine-grained)**
- Linh hoạt hoàn toàn dựa trên yêu cầu nghiệp vụ

**Biểu Diễn Trực Quan:**
```
┌──────────────┐
│  UI Server   │
└──────────────┘
       ↓ (REST APIs)
┌─────────────────────────────────────┐
│  ┌──────────┐  ┌──────────┐        │
│  │ Tài khoản│  │   Thẻ    │  ...   │
│  │    MS    │  │   MS     │        │
│  └──────────┘  └──────────┘        │
│       ↓             ↓               │
│  ┌────────┐   ┌────────┐          │
│  │Acct DB │   │Card DB │          │
│  │(SQL)   │   │(NoSQL) │          │
│  └────────┘   └────────┘          │
└─────────────────────────────────────┘
```

## So Sánh Độ Chi Tiết (Granularity)

| Kiến Trúc | Độ Chi Tiết | Tính Linh Hoạt |
|-----------|-------------|----------------|
| **Monolithic** | Đơn Vị Đơn | Thấp - Mọi thứ cùng nhau |
| **SOA** | Hạt Thô | Trung Bình - UI/Backend tách biệt |
| **Microservices** | Hạt Mịn | Cao - Tách theo domain nghiệp vụ |

### Tại Sao Độ Chi Tiết Quan Trọng

- **Monolithic**: Không tách biệt, mọi thứ đóng gói cùng nhau
- **SOA**: Có tách biệt nhưng linh hoạt hạn chế (không có nhiều database, codebase backend chung)
- **Microservices**: Tách biệt hoàn toàn theo domain nghiệp vụ với lifecycle độc lập

## So Sánh Từng Tính Năng

### 1. Phát Triển Song Song

| Kiến Trúc | Đánh Giá | Mô Tả |
|-----------|----------|-------|
| **Monolithic** | 😢 Kém | Developers khóc - không thể phát triển song song |
| **SOA** | 😐 Trung Bình | Có một số linh hoạt giữa teams UI và backend |
| **Microservices** | 😊 Xuất Sắc | Tự do hoàn toàn cho các teams khác nhau - **CHIẾN THẮNG** |

**Ưu Điểm Microservices:**
- Các teams khác nhau làm việc độc lập
- Lifecycle phát triển riêng biệt
- Lifecycle triển khai riêng biệt
- Chu kỳ nâng cấp riêng biệt

### 2. Tính Linh Hoạt (Agility)

| Kiến Trúc | Đánh Giá | Mô Tả |
|-----------|----------|-------|
| **Monolithic** | 😢 Kém | Không linh hoạt - khó áp dụng framework/ngôn ngữ mới |
| **SOA** | 😐 Trung Bình | Có thể làm ở mức độ nào đó |
| **Microservices** | 😊 Xuất Sắc | Linh hoạt cao - teams làm việc độc lập - **CHIẾN THẮNG** |

**Ưu Điểm Microservices:**
- Dễ nâng cấp với framework mới
- Dễ áp dụng ngôn ngữ mới
- Quyết định độc lập của team
- Cần nỗ lực tối thiểu cho thay đổi

### 3. Khả Năng Mở Rộng (Scalability)

| Kiến Trúc | Đánh Giá | Mô Tả |
|-----------|----------|-------|
| **Monolithic** | 😢 Kém | Rất khó để mở rộng |
| **SOA** | 😐 Trung Bình | Thách thức - độ phức tạp của ESB |
| **Microservices** | 😊 Xuất Sắc | Cực kỳ dễ và tự động - **CHIẾN THẮNG** |

#### Chi Tiết Khả Năng Mở Rộng

**Thách Thức của Monolithic:**
- Tất cả code trong một server lớn
- Cần thêm một server lớn nữa để mở rộng
- Thiết lập load balancing thủ công
- Quy trình rất thách thức

**Thách Thức của SOA:**
- Logic backend trong một server lớn
- Phải mở rộng cả thành phần ESB
- Độ phức tạp bổ sung

**Ưu Điểm Microservices:**
- Mở rộng cực kỳ dễ dàng
- Tự động hóa với Docker và Kubernetes
- Mở rộng từng service riêng lẻ khi cần
- Không cần mở rộng toàn bộ ứng dụng

### 4. Khả Năng Sử Dụng (Usability)

| Kiến Trúc | Đánh Giá | Mô Tả |
|-----------|----------|-------|
| **Monolithic** | 😢 Kém | Khó triển khai tính năng mới |
| **SOA** | 😐 Trung Bình | Cải thiện một số so với monolithic |
| **Microservices** | 😊 Xuất Sắc | Triển khai nâng cấp trong vài ngày/giây - **CHIẾN THẮNG** |

**Kịch Bản Ví Dụ:**

*Team Tài khoản muốn triển khai tính năng để tăng khả năng sử dụng:*

**Cách Tiếp Cận Monolithic/SOA:**
- Phải phối hợp với tất cả các teams
- Quy trình phê duyệt dài
- Yêu cầu triển khai đầy đủ
- Mất vài tuần/tháng

**Cách Tiếp Cận Microservices:**
- Chỉ thảo luận nội bộ team
- Phê duyệt của khách hàng
- Triển khai trong vài giây với Docker/Kubernetes
- Không cần phối hợp với teams khác

### 5. Độ Phức Tạp & Chi Phí Vận Hành

| Kiến Trúc | Đánh Giá | Mô Tả |
|-----------|----------|-------|
| **Monolithic** | 😊 Đơn Giản | Chỉ một server để quản lý - **CHIẾN THẮNG** |
| **SOA** | 😐 Trung Bình | Ba thành phần (UI, Backend, ESB) |
| **Microservices** | 😢 Phức Tạp | Hàng trăm/ngàn services |

#### Chi Tiết Vận Hành

**Ưu Điểm Monolithic:**
- Một server để giám sát
- Vận hành đơn giản
- Dễ đảm bảo server chạy tốt

**Độ Phức Tạp SOA:**
- Ba thành phần để quản lý
- UI server
- Backend server
- ESB component

**Thách Thức Microservices:**
- Một số tổ chức triển khai hàng ngàn microservices
- Hàng trăm server khác nhau
- Chi phí vận hành cao
- Quản lý hàng ngày phức tạp

**Lưu Ý:** Nhiều sản phẩm và framework tồn tại trong hệ sinh thái microservices để vượt qua những thách thức này (sẽ đề cập trong các chủ đề nâng cao).

### 6. Vấn Đề Bảo Mật & Hiệu Suất

| Kiến Trúc | Đánh Giá | Mô Tả |
|-----------|----------|-------|
| **Monolithic** | 😊 Tốt Nhất | Vấn đề bảo mật tối thiểu, hiệu suất tốt nhất - **CHIẾN THẮNG** |
| **SOA** | 😐 Trung Bình | Một số vấn đề bảo mật/hiệu suất |
| **Microservices** | 😢 Thách Thức | Nhiều vấn đề bảo mật hơn, độ trễ mạng |

#### Chi Tiết Bảo Mật & Hiệu Suất

**Ưu Điểm Monolithic:**
- Gọi method trong cùng server
- Không có độ trễ mạng
- Ít vấn đề bảo mật hơn
- Hiệu suất tốt nhất

**Thách Thức Microservices:**
- Giao tiếp qua mạng (REST APIs)
- Độ trễ mạng giữa các services
- Nhiều API calls cần bảo mật
- Chi phí hiệu suất do network calls

**Trước vs. Hiện Tại:**
- **Trước:** Method calls trong cùng server (nhanh)
- **Hiện Tại:** REST API calls qua mạng (chậm hơn nhưng linh hoạt hơn)

## Ma Trận So Sánh Hoàn Chỉnh

| Tính Năng | Monolithic | SOA | Microservices |
|-----------|-----------|-----|---------------|
| **Phát Triển Song Song** | ❌ Kém | 🟡 Trung Bình | ✅ Xuất Sắc |
| **Tính Linh Hoạt** | ❌ Kém | 🟡 Trung Bình | ✅ Xuất Sắc |
| **Khả Năng Mở Rộng** | ❌ Kém | 🟡 Trung Bình | ✅ Xuất Sắc |
| **Khả Năng Sử Dụng** | ❌ Kém | 🟡 Trung Bình | ✅ Xuất Sắc |
| **Độ Phức Tạp** | ✅ Đơn Giản | 🟡 Trung Bình | ❌ Phức Tạp |
| **Bảo Mật & Hiệu Suất** | ✅ Xuất Sắc | 🟡 Trung Bình | ❌ Thách Thức |

## Khung Quyết Định: Khi Nào Sử Dụng Từng Kiến Trúc

### Chọn Monolithic Khi:

✅ Ứng dụng web nhỏ
✅ Tổ chức nhỏ
✅ Quy mô team hạn chế
✅ Cần triển khai không thường xuyên
✅ Ưu tiên sự đơn giản
✅ Ngân sách hạn chế cho cơ sở hạ tầng

### Chọn SOA Khi:

🟡 **Lưu Ý:** SOA hiếm khi được sử dụng ngày nay. Hầu hết các thảo luận tập trung vào Monolithic vs. Microservices.

### Chọn Microservices Khi:

✅ Ứng dụng lớn
✅ Tổ chức lớn
✅ Yêu cầu triển khai thường xuyên
✅ Cần nâng cấp thường xuyên
✅ Cần tính linh hoạt và nhanh nhẹn
✅ Nhiều teams độc lập
✅ Yêu cầu mở rộng khác nhau theo service
✅ Sẵn sàng xử lý độ phức tạp vận hành

## Những Điểm Cần Nhớ

### Các Điểm Quan Trọng

1. **Microservices KHÔNG phải là giải pháp vạn năng** - Nó không giải quyết mọi vấn đề cho mọi ứng dụng

2. **Ngữ Cảnh Quan Trọng** - Chọn kiến trúc dựa trên:
   - Quy mô ứng dụng
   - Quy mô tổ chức
   - Tần suất triển khai
   - Cấu trúc team
   - Nhu cầu mở rộng

3. **Có Đánh Đổi** - Mỗi kiến trúc đều có ưu và nhược điểm

4. **Xu Hướng Hiện Đại** - Thảo luận hiện tại chủ yếu là Monolithic vs. Microservices (SOA đã lỗi thời)

### Chuẩn Bị Phỏng Vấn

**Câu Hỏi Phỏng Vấn Phổ Biến:**

1. *"Sự khác biệt giữa Monolithic và Microservices là gì?"*
   - Tập trung vào triển khai, khả năng mở rộng, tính linh hoạt, và độ phức tạp

2. *"Khi nào nên sử dụng Microservices so với Monolithic?"*
   - Sử dụng khung quyết định ở trên
   - Xem xét quy mô ứng dụng, quy mô tổ chức, và tần suất triển khai

3. *"Những thách thức của Microservices là gì?"*
   - Độ phức tạp, chi phí vận hành, vấn đề bảo mật, độ trễ mạng

4. *"Những lợi ích của Microservices là gì?"*
   - Phát triển song song, tính linh hoạt, khả năng mở rộng, khả năng sử dụng, triển khai độc lập

## Kết Luận

Lựa chọn giữa Monolithic, SOA, và Microservices phụ thuộc vào ngữ cảnh cụ thể của bạn:

- **Bắt đầu với Monolithic** nếu bạn nhỏ và đơn giản
- **Chuyển sang Microservices** khi bạn cần tính linh hoạt, khả năng mở rộng, và triển khai thường xuyên
- **Tránh SOA** trong các dự án mới (mô hình cũ)

Nhớ rằng: Hiểu sâu về các mô hình này sẽ giúp bạn đưa ra quyết định kiến trúc tốt hơn và xuất sắc trong các cuộc phỏng vấn kỹ thuật.

---

*Chia sẻ kiến thức này với người khác để giúp họ hiểu rõ hơn về các mô hình kiến trúc!*




FILE: 20-nang-cao-tai-lieu-openapi-voi-metadata.md


# Nâng Cao Tài Liệu OpenAPI Với Metadata

## Tổng Quan

Trong bài học này, chúng ta sẽ học cách nâng cao tài liệu REST API bằng cách thêm thông tin metadata toàn diện sử dụng các annotation OpenAPI trong Spring Boot. Chúng ta sẽ cải thiện phần đầu của tài liệu Swagger UI để bao gồm tiêu đề, mô tả, thông tin liên hệ, chi tiết giấy phép và các liên kết tài liệu bên ngoài.

## Vấn Đề

Hiện tại, phần đầu của tài liệu REST API thiếu các thông tin quan trọng:
- Mục đích của các REST API
- Tóm tắt và mô tả
- Thông tin liên hệ
- Thông tin giấy phép

Điều này khiến người sử dụng API khó hiểu về ngữ cảnh và hướng dẫn sử dụng API của chúng ta.

## Giải Pháp: Sử Dụng Các Annotation OpenAPI

### Bước 1: Định Vị Class Chính Spring Boot

Điều hướng đến class chính Spring Boot của bạn - trong ví dụ này là `AccountsApplication`. Đây là nơi chúng ta sẽ thêm các annotation metadata OpenAPI.

### Bước 2: Thêm Annotation @OpenApiDefinition

Thêm annotation `@OpenApiDefinition` vào class chính của bạn để cung cấp các chi tiết định nghĩa với OpenAPI.

```java
@OpenApiDefinition(
    info = @Info(
        title = "Accounts Microservice REST API Documentation",
        description = "EasyBank Accounts Microservice REST API Documentation",
        version = "v1",
        contact = @Contact(
            name = "Tên của bạn",
            email = "email.cua.ban@example.com",
            url = "https://www.eazybytes.com"
        ),
        license = @License(
            name = "Apache 2.0",
            url = "https://www.eazybytes.com"
        )
    ),
    externalDocs = @ExternalDocumentation(
        description = "EasyBank Accounts Microservice REST API Documentation",
        url = "https://www.eazybytes.com/swagger-ui.html"
    )
)
@SpringBootApplication
public class AccountsApplication {
    // Mã nguồn ứng dụng
}
```

## Giải Thích Các Tham Số Annotation

### Annotation @Info

Annotation `@Info` chấp nhận các tham số sau:

1. **title**: Tóm tắt ngắn gọn về các REST API của bạn
   - Ví dụ: "Accounts Microservice REST API Documentation"

2. **description**: Mô tả chi tiết về các REST API của bạn
   - Ví dụ: "EasyBank Accounts Microservice REST API Documentation"

3. **version**: Phiên bản của API
   - Ví dụ: "v1", "v2", "v3" dựa trên yêu cầu của bạn

4. **contact**: Thông tin liên hệ để được hỗ trợ

5. **license**: Chi tiết giấy phép cho API của bạn

### Annotation @Contact

Annotation `@Contact` bao gồm:
- **name**: Tên của người hoặc nhóm để liên hệ
- **email**: Email liên hệ (có thể là email cá nhân hoặc nhóm)
- **url**: URL trang web để liên hệ

### Annotation @License

Annotation `@License` chỉ định:
- **name**: Tên giấy phép (ví dụ: "Apache 2.0")
- **url**: URL nơi mọi người có thể đọc thêm về chi tiết giấy phép

### Annotation @ExternalDocumentation

Cung cấp các tài nguyên tài liệu bổ sung:
- **description**: Mô tả về tài liệu bên ngoài
- **url**: URL nơi mọi người có thể truy cập tài liệu chi tiết

## Các Tùy Chọn Cấu Hình Bổ Sung

Đặc tả OpenAPI hỗ trợ nhiều tùy chọn cấu hình nâng cao khác:

- **Chi tiết bảo mật**: Định nghĩa các schema xác thực và phân quyền
- **Chi tiết máy chủ**: Chỉ định các URL nơi REST API được lưu trữ
- **Tags**: Tổ chức các API thành các nhóm logic
- **Extensions**: Thêm các thuộc tính tùy chỉnh

Để có phạm vi bao quát toàn diện về đặc tả OpenAPI và hệ sinh thái Swagger, hãy cân nhắc các khóa đào tạo chuyên biệt.

## Kiểm Tra Các Thay Đổi

1. Lưu các thay đổi vào class chính của bạn
2. Build ứng dụng
3. Refresh trang Swagger UI HTML
4. Xác minh rằng phần đầu bây giờ hiển thị:
   - Tiêu đề và mô tả
   - Chi tiết liên hệ (email, website)
   - Thông tin giấy phép
   - Các liên kết tài liệu bên ngoài

## Lưu Ý Quan Trọng: Best Practices Về Cấu Trúc Package

### Cách Tiếp Cận Được Khuyến Nghị

Class chính Spring Boot của bạn nên ở trong package gốc, với tất cả các package khác là sub-package:

```
com.eazybytes.accounts (Class chính: AccountsApplication)
├── controller
├── service
├── repository
└── entity
```

Đây là **cách tiếp cận được khuyến nghị nhất** vì Spring Boot tự động quét tất cả các sub-package.

### Cách Tiếp Cận Thay Thế (Không Được Khuyến Nghị)

Nếu bạn tạo các package bên ngoài cấu trúc package chính, bạn **phải** chỉ định rõ ràng các vị trí component sử dụng các annotation này:

```java
@ComponentScan(basePackages = {
    "com.eazybytes.controller",
    "com.eazybytes.service"
})
@EnableJpaRepositories(basePackages = "com.eazybytes.repository")
@EntityScan(basePackages = "com.eazybytes.entity")
@SpringBootApplication
public class AccountsApplication {
    // Mã nguồn ứng dụng
}
```

**Quan trọng**: Nếu không có các annotation này, Spring Boot sẽ không phát hiện các component của bạn, và ứng dụng sẽ không hoạt động chính xác.

## Các Bước Tiếp Theo

Trong bài học tiếp theo, chúng ta sẽ nâng cao tài liệu ở cấp độ controller bằng cách:
- Loại bỏ thông tin kỹ thuật như tên class
- Ẩn chi tiết hostname
- Cung cấp dữ liệu ví dụ cho các request và response API
- Làm cho tài liệu thân thiện hơn với người dùng

## Những Điểm Chính

1. Sử dụng `@OpenApiDefinition` để thêm metadata toàn diện vào tài liệu API của bạn
2. Bao gồm thông tin title, description, version, contact và license
3. Cung cấp các liên kết tài liệu bên ngoài cho các tài nguyên bổ sung
4. Tuân theo các best practices về cấu trúc package Spring Boot
5. Luôn duy trì các sub-package dưới package ứng dụng chính
6. Tài liệu được nâng cao cải thiện khả năng sử dụng API và trải nghiệm developer

## Kết Luận

Bằng cách thêm metadata phù hợp vào tài liệu OpenAPI của bạn, bạn làm cho người sử dụng API dễ dàng hiểu mục đích, thông tin liên hệ và giấy phép của các REST API của bạn. Cách tiếp cận tài liệu chuyên nghiệp này là điều cần thiết cho các microservice sẵn sàng cho production.




FILE: 21-nang-cao-tai-lieu-rest-api-voi-swagger-annotations.md


# Nâng Cao Tài Liệu REST API với Swagger Annotations

## Tổng Quan
Hướng dẫn này trình bày cách nâng cao tài liệu REST API sử dụng các annotation OpenAPI/Swagger trong ứng dụng Spring Boot. Chúng ta sẽ cải thiện tài liệu cho AccountsController bằng cách thêm mô tả chi tiết, tóm tắt và thông tin phản hồi.

## Tình Trạng Hiện Tại
Tài liệu REST API hiện tại hiển thị:
- Tên kỹ thuật `AccountsController` không có thông tin mô tả
- Không có mô tả cho các API trong controller
- Thông tin hạn chế về các hoạt động API và phản hồi

## Nâng Cao Tài Liệu Cấp Controller

### Sử Dụng Annotation @Tag
Để cung cấp thông tin về tất cả các API trong một controller class, sử dụng annotation `@Tag`:

```java
@Tag(
    name = "CRUD REST APIs cho Accounts trong EasyBank",
    description = "CRUD REST APIs trong EasyBank để tạo, cập nhật, lấy và xóa thông tin tài khoản"
)
@RestController
public class AccountsController {
    // ... các phương thức controller
}
```

**Điểm Chính:**
- Annotation `@Tag` thuộc package Swagger/OpenAPI SpringDoc
- `name` cung cấp tóm tắt cho tất cả các API trong controller
- `description` đưa ra thông tin chi tiết về mục đích của controller

**Kết Quả:** Thay vì chỉ thấy "AccountsController", khách hàng sẽ thấy mô tả chuyên nghiệp giải thích rằng phần này chứa bốn REST API để xử lý các thao tác tạo, cập nhật, lấy và xóa.

## Nâng Cao Tài Liệu Cấp API Operation

### Sử Dụng Annotation @Operation

Đối với các API operation riêng lẻ, sử dụng annotation `@Operation`:

```java
@Operation(
    summary = "Create Account REST API",
    description = "REST API để tạo Customer và Account mới trong EasyBank"
)
@PostMapping("/create")
public ResponseEntity<ResponseDto> createAccount(@RequestBody AccountDto accountDto) {
    // ... implementation
}
```

**Điểm Chính:**
- `summary` cung cấp tiêu đề ngắn gọn cho API
- `description` đưa ra thông tin chi tiết về chức năng của API

## Tùy Chỉnh Tài Liệu Response

### Sử Dụng Annotation @ApiResponse

Theo mặc định, tài liệu hiển thị phản hồi 200 OK. Để tùy chỉnh:

```java
@Operation(
    summary = "Create Account REST API",
    description = "REST API để tạo Customer và Account mới trong EasyBank"
)
@ApiResponse(
    responseCode = "201",
    description = "HttpStatus.CREATED"
)
@PostMapping("/create")
public ResponseEntity<ResponseDto> createAccount(@RequestBody AccountDto accountDto) {
    // ... implementation
}
```

**Điểm Chính:**
- `@ApiResponse` ghi đè phản hồi 200 mặc định
- `responseCode` chỉ định mã trạng thái HTTP thực tế được trả về
- `description` giải thích ý nghĩa của mã trạng thái

## Xử Lý Nhiều Mã Response

### Sử Dụng Annotation @ApiResponses

Đối với các operation trả về nhiều phản hồi có thể:

```java
@Operation(
    summary = "Update Account Details REST API",
    description = "REST API để cập nhật thông tin Customer và Account dựa trên số tài khoản"
)
@ApiResponses({
    @ApiResponse(
        responseCode = "200",
        description = "HttpStatus.OK"
    ),
    @ApiResponse(
        responseCode = "500",
        description = "HttpStatus.INTERNAL_SERVER_ERROR"
    )
})
@PutMapping("/update")
public ResponseEntity<ResponseDto> updateAccount(@RequestBody AccountDto accountDto) {
    // ... implementation
}
```

**Điểm Chính:**
- Sử dụng `@ApiResponses` (số nhiều) để định nghĩa nhiều phản hồi
- Mỗi `@ApiResponse` được phân cách bằng dấu phẩy
- Điều này cung cấp thông tin trước cho khách hàng và nhà phát triển về các phản hồi có thể xảy ra

## Ví Dụ: Tài Liệu API Hoàn Chỉnh

### Fetch Account API
```java
@Operation(
    summary = "Fetch Account Details REST API",
    description = "REST API để lấy thông tin Customer và Account dựa trên số tài khoản"
)
@ApiResponse(
    responseCode = "200",
    description = "HttpStatus.OK"
)
@GetMapping("/fetch")
public ResponseEntity<AccountDto> fetchAccount(@RequestParam String accountNumber) {
    // ... implementation
}
```

### Delete Account API
```java
@Operation(
    summary = "Delete Account REST API",
    description = "REST API để xóa Customer và Account dựa trên số tài khoản"
)
@ApiResponses({
    @ApiResponse(
        responseCode = "200",
        description = "HttpStatus.OK"
    ),
    @ApiResponse(
        responseCode = "500",
        description = "HttpStatus.INTERNAL_SERVER_ERROR"
    )
})
@DeleteMapping("/delete")
public ResponseEntity<ResponseDto> deleteAccount(@RequestParam String accountNumber) {
    // ... implementation
}
```

## Lợi Ích

Sau khi triển khai các cải tiến này:
1. **Tài Liệu Chuyên Nghiệp**: Khách hàng thấy thông tin rõ ràng, mô tả thay vì tên kỹ thuật
2. **Hiểu Rõ Hơn**: Nhà phát triển và tester biết chính xác chức năng của từng API
3. **Rõ Ràng Về Response**: Chỉ dẫn rõ ràng về các mã trạng thái HTTP có thể và ý nghĩa của chúng
4. **Cải Thiện Trải Nghiệm Developer**: Giúp việc tích hợp với các API dễ dàng hơn

## Response Schema

Tài liệu hiện nay hiển thị:
- Mã trạng thái HTTP chính xác (201, 200, 500, v.v.)
- Định dạng phản hồi (application/json)
- Cấu trúc schema (status code và status message)

## Các Bước Tiếp Theo

Cải tiến tiếp theo sẽ tập trung vào:
- Cải thiện tài liệu schema object
- Thêm dữ liệu mẫu vào schema objects
- Thay thế tên kỹ thuật bằng tên mô tả hơn
- Cung cấp giá trị mẫu để rõ ràng hơn

## Tóm Tắt

Bằng cách sử dụng các annotation `@Tag`, `@Operation`, `@ApiResponse`, và `@ApiResponses`, bạn có thể nâng cao đáng kể tài liệu REST API của mình. Điều này làm cho các API của bạn chuyên nghiệp hơn, dễ hiểu hơn và đơn giản hơn để tích hợp cho các ứng dụng khách và nhóm phát triển.




FILE: 22-nang-cao-tai-lieu-schema-voi-schema-annotations.md


# Nâng Cao Tài Liệu Schema với @Schema Annotations

## Tổng Quan

Trong hướng dẫn này, chúng ta sẽ học cách nâng cao tài liệu OpenAPI cho các đối tượng schema bằng cách sử dụng annotation `@Schema` trong microservices Spring Boot. Điều này cho phép chúng ta cung cấp tên thân thiện với nghiệp vụ, mô tả và các giá trị ví dụ cho các DTO và trường của chúng.

## Tại Sao Cần Nâng Cao Tài Liệu Schema?

- **Tên Thân Thiện với Nghiệp Vụ**: Thay thế tên class kỹ thuật bằng các thuật ngữ nghiệp vụ dễ hiểu hơn
- **Mô Tả Rõ Ràng**: Giải thích ý nghĩa của mỗi schema và trường
- **Giá Trị Ví Dụ**: Cung cấp dữ liệu mẫu giúp người dùng API hiểu định dạng mong đợi
- **Tài Liệu Chuyên Nghiệp**: Tạo tài liệu API toàn diện, dễ hiểu

## Nâng Cao CustomerDto

### Tài Liệu Cấp Class

Thêm annotation `@Schema` ở cấp class để cung cấp thông tin tổng quan:

```java
@Schema(
    name = "Customer",
    description = "Schema để lưu thông tin khách hàng và tài khoản"
)
public class CustomerDto {
    // các trường...
}
```

### Tài Liệu Cấp Trường

Thêm annotation `@Schema` cho từng trường:

```java
@Schema(
    description = "Tên của khách hàng",
    example = "Nguyễn Văn A"
)
private String name;

@Schema(
    description = "Địa chỉ email của khách hàng",
    example = "nguyenvana@example.com"
)
private String email;

@Schema(
    description = "Số điện thoại di động của khách hàng",
    example = "+84901234567"
)
private String mobileNumber;

@Schema(
    description = "Chi tiết tài khoản của khách hàng"
)
private AccountsDto accounts;
```

## Nâng Cao AccountsDto

### Cấu Hình Cấp Class

```java
@Schema(
    name = "Accounts",
    description = "Schema để lưu thông tin tài khoản"
)
public class AccountsDto {
    // các trường...
}
```

### Annotations Cấp Trường

```java
@Schema(
    description = "Số tài khoản của Easy Bank"
)
private Long accountNumber;

@Schema(
    description = "Loại tài khoản của Easy Bank",
    example = "Tiết kiệm"
)
private String accountType;

@Schema(
    description = "Địa chỉ chi nhánh của Easy Bank",
    example = "123 Hà Nội"
)
private String branchAddress;
```

**Lưu ý**: Tham số `example` là tùy chọn. Sử dụng nó ở những nơi mang lại giá trị cho người dùng API.

## Nâng Cao ResponseDto

### Phản Hồi Thành Công Chuẩn

```java
@Schema(
    name = "Response",
    description = "Schema để lưu thông tin phản hồi thành công"
)
public class ResponseDto {
    
    @Schema(
        description = "Mã trạng thái trong phản hồi",
        example = "200"
    )
    private String statusCode;
    
    @Schema(
        description = "Thông báo trạng thái trong phản hồi",
        example = "Yêu cầu được xử lý thành công"
    )
    private String statusMessage;
}
```

## Nâng Cao ErrorResponseDto

### Schema Phản Hồi Lỗi

```java
@Schema(
    name = "ErrorResponse",
    description = "Schema để lưu thông tin phản hồi lỗi"
)
public class ErrorResponseDto {
    
    @Schema(
        description = "Đường dẫn API được gọi bởi client"
    )
    private String apiPath;
    
    @Schema(
        description = "Mã lỗi đại diện cho lỗi đã xảy ra"
    )
    private String errorCode;
    
    @Schema(
        description = "Thông báo lỗi đại diện cho lỗi đã xảy ra"
    )
    private String errorMessage;
    
    @Schema(
        description = "Thời gian xảy ra lỗi"
    )
    private LocalDateTime errorTime;
}
```

**Lưu ý**: Có thể bỏ qua các giá trị ví dụ cho phản hồi lỗi vì chúng thay đổi theo từng tình huống.

## Tài Liệu Hóa Phản Hồi Lỗi trong Các API Operation

### Vấn Đề

`ErrorResponseDto` sẽ không tự động xuất hiện trong Swagger UI vì OpenAPI không thể quét logic `GlobalExceptionHandler`.

### Giải Pháp

Thêm schema phản hồi lỗi vào các API operation bằng cách sử dụng `@ApiResponse`:

```java
@ApiResponse(
    responseCode = "500",
    description = "Lỗi Máy Chủ Nội Bộ",
    content = @Content(
        schema = @Schema(implementation = ErrorResponseDto.class)
    )
)
```

### Ví Dụ Hoàn Chỉnh

```java
@Operation(
    summary = "REST API Cập Nhật Tài Khoản",
    description = "REST API để cập nhật chi tiết tài khoản"
)
@ApiResponse(
    responseCode = "200",
    description = "HTTP Status OK"
)
@ApiResponse(
    responseCode = "500",
    description = "Lỗi Máy Chủ Nội Bộ",
    content = @Content(
        schema = @Schema(implementation = ErrorResponseDto.class)
    )
)
@PutMapping("/update")
public ResponseEntity<ResponseDto> updateAccount(@RequestBody AccountsDto accountsDto) {
    // triển khai
}
```

## Xác Minh Tài Liệu

### Các Bước Xác Minh

1. **Lưu tất cả thay đổi** trong các class DTO
2. **Build dự án** để tạo lại OpenAPI specifications
3. **Truy cập Swagger UI** (thường tại `http://localhost:8080/swagger-ui.html`)
4. **Kiểm tra các mục sau**:
   - Các đối tượng schema có tên thân thiện với nghiệp vụ
   - Mỗi trường có thông tin mô tả
   - Các giá trị ví dụ xuất hiện trong tài liệu
   - Các schema phản hồi lỗi hiển thị được

### Những Gì Bạn Nên Thấy

- **Phần Schemas**: Tất cả DTO được liệt kê với tên tùy chỉnh (Customer, Accounts, Response, ErrorResponse)
- **Mô Tả Trường**: Mỗi trường hiển thị mục đích và giá trị ví dụ
- **API Operations**: Request/response body ví dụ được điền đầy đủ
- **Phản Hồi Lỗi**: Phản hồi lỗi 500 hiển thị cấu trúc schema ErrorResponse

## Thực Hành Tốt Nhất

1. **Sử Dụng Tên Thân Thiện với Nghiệp Vụ**: Đặt tên schema dễ hiểu cho các bên liên quan phi kỹ thuật
2. **Cung Cấp Mô Tả Rõ Ràng**: Giải thích mục đích của mỗi schema và trường
3. **Bao Gồm Các Ví Dụ Liên Quan**: Thêm giá trị ví dụ ở những nơi giúp làm rõ định dạng mong đợi
4. **Tài Liệu Hóa Phản Hồi Lỗi**: Định nghĩa rõ ràng các schema lỗi trong API operations
5. **Giữ Ví Dụ Thực Tế**: Sử dụng các ví dụ đại diện cho trường hợp sử dụng thực tế
6. **Nhất Quán**: Tuân theo cùng một mẫu tài liệu trên tất cả các DTO

## Lợi Ích

- **Tài Liệu Chuyên Nghiệp**: Tạo tài liệu API toàn diện, dễ hiểu
- **Trải Nghiệm Developer Tốt Hơn**: Người dùng API có thể nhanh chóng hiểu cách sử dụng API
- **Giảm Chi Phí Hỗ Trợ**: Tài liệu rõ ràng giảm thiểu câu hỏi và vấn đề tích hợp
- **Tuân Thủ Tiêu Chuẩn**: Tuân theo các thực hành tốt nhất của OpenAPI Specification

## Tóm Tắt

Bằng cách sử dụng annotation `@Schema` ở cả cấp class và cấp trường, chúng ta có thể nâng cao đáng kể tài liệu REST API. Điều này bao gồm:

- Tên thân thiện với nghiệp vụ tùy chỉnh cho các đối tượng schema
- Thông tin mô tả cho từng trường
- Giá trị ví dụ để hướng dẫn người dùng API
- Tài liệu hóa đúng các phản hồi lỗi

Những cải tiến này làm cho các API microservices của bạn chuyên nghiệp hơn và dễ sử dụng hơn.




FILE: 23-cai-thien-ma-trang-thai-http-cho-phan-hoi-loi.md


# Cải Thiện Mã Trạng Thái HTTP Cho Phản Hồi Lỗi

## Tổng Quan
Trong bài giảng này, chúng ta sẽ giải quyết vấn đề sử dụng cùng một mã trạng thái HTTP (500) cho các tình huống lỗi khác nhau trong REST APIs. Chúng ta sẽ triển khai các mã trạng thái phù hợp hơn để cung cấp sự rõ ràng tốt hơn cho các client sử dụng API.

## Vấn Đề
Trước đây, chúng ta đã sử dụng mã trạng thái HTTP 500 (Internal Server Error) trong nhiều tình huống:
- Xử lý RuntimeException trong GlobalExceptionHandler
- Các thao tác cập nhật thất bại
- Các thao tác xóa thất bại

Cách tiếp cận này tạo ra sự nhầm lẫn cho các client API vì họ không thể phân biệt giữa các loại lỗi khác nhau.

## Giải Pháp

### 1. Giới Thiệu Mã Trạng Thái HTTP 417
Chúng ta đã giới thiệu mã trạng thái HTTP 417 (Expectation Failed) cho các thao tác thất bại trong quá trình thực thi:

**Thao Tác Update (Cập Nhật):**
```java
// Bên trong controller class
if (!isUpdated) {
    return ResponseEntity
        .status(HttpStatus.EXPECTATION_FAILED)
        .body(new ResponseDto(STATUS_417, MESSAGE_417_UPDATE));
}
```

**Thao Tác Delete (Xóa):**
```java
if (!isDeleted) {
    return ResponseEntity
        .status(HttpStatus.EXPECTATION_FAILED)
        .body(new ResponseDto(STATUS_417, MESSAGE_417_DELETE));
}
```

### 2. Cập Nhật Constants (Hằng Số)
Tạo các hằng số mới cho status 417:
- `STATUS_417 = "417"`
- `MESSAGE_417_UPDATE = "Update operation failed. Please try again or contact dev team"`
- `MESSAGE_417_DELETE = "Delete operation failed. Please try again or contact dev team"`

Các hằng số cũ STATUS_500 và MESSAGE_500 đã được comment nhưng vẫn giữ lại để tham khảo.

### 3. Tài Liệu Phản Hồi API

Mỗi API giờ đây có các mã phản hồi được tài liệu hóa đầy đủ:

**Thao Tác Create và Fetch:**
- 200/201: Phản hồi thành công
- 500: RuntimeException với schema ErrorResponseDto

**Thao Tác Update:**
- 204: Thành công (No Content)
- 417: Expectation Failed (thao tác thất bại)
- 500: RuntimeException với schema ErrorResponseDto

**Thao Tác Delete:**
- 204: Thành công (No Content)
- 417: Expectation Failed (thao tác thất bại)
- 500: RuntimeException với schema ErrorResponseDto

### 4. Loại Bỏ Các Ví Dụ Gây Nhầm Lẫn

Chúng ta đã loại bỏ các giá trị example được hardcode từ ResponseDto:
```java
// Trước đây
@Schema(example = "200")
private String statusCode;

@Schema(example = "Request processed successfully")
private String statusMessage;

// Sau khi thay đổi
private String statusCode;
private String statusMessage;
```

Điều này ngăn chặn sự nhầm lẫn khi tài liệu OpenAPI hiển thị mã trạng thái 200 ngay cả đối với phản hồi 417 hoặc 500.

## Lợi Ích

1. **Phân Biệt Lỗi Rõ Ràng**: Các client giờ đây có thể phân biệt giữa:
   - Runtime exceptions (500)
   - Các lỗi thao tác dự kiến (417)
   - Các thao tác thành công (200/204)

2. **Tài Liệu API Tốt Hơn**: Tài liệu OpenAPI/Swagger giờ đây hiển thị rõ ràng tất cả các mã phản hồi có thể có cho mỗi endpoint

3. **Trải Nghiệm Client Được Cải Thiện**: Người sử dụng API có thể triển khai xử lý lỗi thông minh hơn dựa trên các mã trạng thái cụ thể

## Tóm Tắt

Bằng cách giới thiệu mã trạng thái HTTP 417 cho các lỗi thao tác và duy trì 500 cho runtime exceptions, chúng ta đã tạo ra một hợp đồng rõ ràng hơn giữa REST API của chúng ta và các client. Mỗi endpoint API giờ đây có các mã phản hồi được tài liệu hóa tốt, đại diện chính xác cho các tình huống khác nhau.

Schema ErrorResponseDto giờ đây được hiển thị đúng cách trong phần schemas của OpenAPI, và tất cả các định dạng phản hồi đều hiển thị rõ ràng trong tài liệu.

## Điểm Chính Cần Nhớ
- Sử dụng mã trạng thái HTTP phù hợp cho các tình huống lỗi khác nhau
- HTTP 417 phù hợp cho các lỗi expectation/operation failures
- HTTP 500 nên được dành riêng cho các runtime exceptions không mong đợi
- Loại bỏ các giá trị example có thể tạo ra nhầm lẫn trong tài liệu API
- Tài liệu hóa tất cả các mã phản hồi có thể có cho mỗi endpoint API




FILE: 24-tong-ket-cac-annotation-spring-boot-cho-rest-services.md


# Tổng Kết Các Annotation Spring Boot Cho REST Services

## Tổng Quan

Tài liệu này cung cấp bản tóm tắt toàn diện về các annotation và class thiết yếu của Spring Boot được sử dụng để xây dựng REST APIs trong kiến trúc microservices. Những annotation và component này là nền tảng khi phát triển REST services với Spring Boot.

## Các Annotation và Class Quan Trọng

### 1. @RestController

**Mục đích**: Đánh dấu một class là REST API controller.

**Cách sử dụng**:
- Đặt annotation này lên đầu class để expose các Java method dưới dạng REST APIs
- Hoạt động kết hợp với các HTTP mapping annotation như `@GetMapping`, `@PostMapping`
- Thông báo cho Spring Boot framework expose tất cả các Java method dưới dạng REST endpoints

**Ví dụ Tình huống**:
```java
@RestController
public class AccountsController {
    // Các REST API method
}
```

**Lưu ý**: `@RestController` là sự kết hợp của `@Controller` + `@ResponseBody`

---

### 2. @Controller vs @RestController

**@Controller**:
- Sử dụng khi bạn cần cả REST APIs và Spring MVC methods trong cùng một class
- Yêu cầu annotation `@ResponseBody` trên từng method riêng lẻ cần trả về JSON

**@RestController**:
- Sử dụng khi tất cả các method trong class là REST endpoints
- Tự động áp dụng `@ResponseBody` cho tất cả các method
- Được ưa chuộng cho các controller REST API thuần túy

---

### 3. @ResponseBody

**Mục đích**: Chỉ định rằng giá trị trả về của method nên được gắn vào response body của web.

**Cách sử dụng**:
- Sử dụng với annotation `@Controller`
- Thông báo cho Spring Boot trả về response ở định dạng JSON thay vì Spring MVC style (HTML/UI format)
- Không cần thiết khi sử dụng `@RestController` (đã được bao gồm sẵn)

**Khi nào sử dụng**:
- Khi sử dụng `@Controller` và cần các method cụ thể trả về JSON
- Controller hỗn hợp với cả REST và MVC methods

---

### 4. ResponseEntity

**Loại**: Class (không phải annotation)

**Mục đích**: Đại diện cho toàn bộ HTTP response bao gồm headers, status và body.

**Tính năng**:
- Cho phép gửi thông tin response đầy đủ (headers, status code, body)
- Sử dụng generics để chỉ định kiểu đối tượng trong response body
- Cung cấp toàn quyền kiểm soát HTTP response

**Ví dụ**:
```java
public ResponseEntity<CustomerDTO> getCustomer() {
    return ResponseEntity.ok(customerDTO);
}
```

**Lợi ích**:
- Kiểm soát hoàn toàn HTTP response
- Có thể đặt custom headers và status codes
- Response body an toàn về kiểu dữ liệu

---

### 5. @ControllerAdvice

**Mục đích**: Kích hoạt xử lý exception toàn cục trên tất cả các controller.

**Cách sử dụng**:
- Đặt trên một class để biến nó thành global exception handler
- Hoạt động với annotation `@ExceptionHandler`
- Chặn các exception được throw bởi bất kỳ controller nào

**Cách hoạt động**:
1. Tạo một class được annotate với `@ControllerAdvice`
2. Định nghĩa các method được annotate với `@ExceptionHandler`
3. Gắn mỗi method với các loại exception cụ thể
4. Khi exception đó xảy ra trong bất kỳ controller nào, handler method sẽ được thực thi

**Ví dụ Tình huống**:
```java
@ControllerAdvice
public class GlobalExceptionHandler {
    
    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleResourceNotFound(ResourceNotFoundException ex) {
        // Xử lý exception
    }
}
```

---

### 6. @RestControllerAdvice

**Mục đích**: Phiên bản chuyên biệt của `@ControllerAdvice` cho REST APIs.

**Cấu thành**: `@ControllerAdvice` + `@ResponseBody`

**Mối quan hệ**: Tương tự như mối quan hệ giữa `@Controller` và `@RestController`

**Khi nào sử dụng**:
- Khi bạn muốn các exception handler method trả về output JSON một cách nghiêm ngặt
- Cho các ứng dụng REST API thuần túy

**Lưu ý**: Cả `@ControllerAdvice` và `@RestControllerAdvice` đều hoạt động hiệu quả cho REST services. Ví dụ trong Accounts Microservice sử dụng `@ControllerAdvice` thành công.

---

### 7. RequestEntity

**Loại**: Class (tương tự ResponseEntity)

**Mục đích**: Đại diện cho một HTTP request bao gồm headers và body.

**Tình huống sử dụng**:
- Khi bạn cần nhận cả request body và request headers như một method parameter duy nhất
- Cung cấp quyền truy cập vào thông tin request đầy đủ

**Khi không cần thiết**:
- Khi bạn chỉ cần request body (sử dụng `@RequestBody` thay thế)
- Khi bạn chỉ cần các header cụ thể (sử dụng `@RequestHeader` thay thế)

**Ví dụ**:
```java
public ResponseEntity<String> processRequest(RequestEntity<CustomerDTO> requestEntity) {
    // Trích xuất headers và body từ requestEntity
    HttpHeaders headers = requestEntity.getHeaders();
    CustomerDTO body = requestEntity.getBody();
    // Thực thi logic nghiệp vụ
}
```

---

### 8. @RequestHeader

**Mục đích**: Gắn một method parameter với một request header.

**Cách sử dụng**:
- Trích xuất các giá trị header cụ thể từ HTTP request
- Truyền giá trị header như method parameter

**Ví dụ**:
```java
@GetMapping("/customer")
public ResponseEntity<CustomerDTO> getCustomer(
    @RequestHeader("Authorization") String authToken) {
    // Sử dụng authToken trong logic nghiệp vụ
}
```

---

### 9. @RequestBody

**Mục đích**: Gắn HTTP request body với một method parameter.

**Cách sử dụng**:
- Nhận toàn bộ request body dưới dạng một đối tượng Java
- Tự động deserialize JSON thành đối tượng Java

**Ví dụ**:
```java
@PostMapping("/account")
public ResponseEntity<String> createAccount(
    @RequestBody AccountDTO accountDTO) {
    // Sử dụng accountDTO trong logic nghiệp vụ
}
```

---

## Quy Trình Phát Triển REST API Hoàn Chỉnh

Khi xây dựng REST APIs với Spring Boot, hãy tuân theo trình tự này:

1. **Tạo Controller Class**
   - Annotate với `@RestController`

2. **Định nghĩa Java Methods**
   - Thêm HTTP mapping annotations (`@GetMapping`, `@PostMapping`, `@PutMapping`, `@DeleteMapping`)

3. **Xử lý Request Input**
   - Sử dụng `@RequestBody` cho request body
   - Sử dụng `@RequestHeader` cho các header cụ thể
   - Sử dụng `RequestEntity` cho request hoàn chỉnh (headers + body)

4. **Trả về Response**
   - Sử dụng `ResponseEntity` để kiểm soát hoàn toàn response

5. **Triển khai Global Exception Handling**
   - Tạo một class với `@ControllerAdvice` hoặc `@RestControllerAdvice`
   - Định nghĩa các method với `@ExceptionHandler` cho các loại exception khác nhau

---

## Mẹo Phỏng Vấn

Khi được hỏi "Làm thế nào để xây dựng REST APIs với Spring Boot?", hãy giải thích quy trình như một câu chuyện:

1. Bắt đầu bằng cách tạo một class và annotate nó với `@RestController`
2. Tạo các Java method và annotate chúng với HTTP mappings (`@GetMapping`, `@PostMapping`, v.v.)
3. Sử dụng `@RequestBody`, `@RequestHeader`, hoặc `RequestEntity` để nhận input
4. Triển khai logic nghiệp vụ trong các method
5. Trả về response sử dụng `ResponseEntity`
6. Định nghĩa global exception handling sử dụng `@ControllerAdvice` và `@ExceptionHandler`

Cách giải thích tuần tự này thể hiện sự hiểu biết hoàn chỉnh về quy trình phát triển REST API.

---

## Bảng Tóm Tắt

| Annotation/Class | Loại | Mục đích |
|-----------------|------|---------|
| `@RestController` | Annotation | Đánh dấu class là REST controller |
| `@Controller` | Annotation | Đánh dấu class là controller (REST + MVC) |
| `@ResponseBody` | Annotation | Trả về JSON response từ method |
| `ResponseEntity` | Class | Kiểm soát HTTP response hoàn chỉnh |
| `@ControllerAdvice` | Annotation | Xử lý exception toàn cục |
| `@RestControllerAdvice` | Annotation | Xử lý exception toàn cục cho REST |
| `RequestEntity` | Class | Đại diện HTTP request hoàn chỉnh |
| `@RequestHeader` | Annotation | Gắn request header với parameter |
| `@RequestBody` | Annotation | Gắn request body với parameter |

---

## Best Practices (Thực Hành Tốt Nhất)

1. **Sử dụng `@RestController`** cho các controller REST API thuần túy
2. **Sử dụng `ResponseEntity`** để xử lý response linh hoạt
3. **Triển khai global exception handling** với `@ControllerAdvice`
4. **Chọn annotation input phù hợp** dựa trên nhu cầu của bạn:
   - `@RequestBody` cho nội dung body
   - `@RequestHeader` cho các header cụ thể
   - `RequestEntity` khi bạn cần cả hai
5. **Giữ các annotation này sẵn sàng** cho phỏng vấn và phát triển

---

## Kết Luận

Những annotation và class này tạo thành nền tảng cho việc phát triển REST service với Spring Boot. Hiểu rõ mục đích, mối quan hệ và các tình huống sử dụng thích hợp của chúng là điều cần thiết để xây dựng microservices mạnh mẽ. Hãy giữ tài liệu tham khảo này sẵn sàng cho cả việc phát triển và chuẩn bị phỏng vấn.

---

**Khóa học**: Microservices với Spring Boot  
**Module**: Phát triển REST API  
**Chủ đề**: Tổng kết các Annotation Spring Boot




FILE: 25-xay-dung-cards-va-loans-microservices-bai-tap.md


# Xây Dựng Cards và Loans Microservices - Bài Tập

## Tổng Quan

Sau khi hoàn thành việc phát triển Accounts Microservice với các tiêu chuẩn và thực hành tốt nhất đã được thiết lập, bước tiếp theo là xây dựng các microservices tương tự cho Cards và Loans, tuân theo cùng các mẫu kiến trúc và quy ước.

## Mục Tiêu Bài Tập

Xây dựng hai microservices mới (Cards và Loans) áp dụng tất cả các tiêu chuẩn và thực hành đã học từ việc triển khai Accounts Microservice.

## Hướng Dẫn Triển Khai Từng Bước

### 1. Thiết Lập Dự Án

- Tạo các ứng dụng Spring Boot trống từ [start.spring.io](https://start.spring.io)
- Bao gồm tất cả các dependencies cần thiết
- Tải xuống và giải nén các ứng dụng web Spring Boot

### 2. Triển Khai Các Tính Năng Cốt Lõi

Tuân theo các tiêu chuẩn sau cho cả hai microservices Cards và Loans:

#### Cấu Hình Cơ Sở Dữ Liệu
- Cấu hình cơ sở dữ liệu H2
- Tạo schema cơ sở dữ liệu
- Định nghĩa cấu trúc bảng với các cột phù hợp

#### Tầng Dữ Liệu
- Tạo các lớp entity
- Triển khai JPA repositories
- Thiết lập các mối quan hệ entity phù hợp

#### Tầng Service
- Triển khai mẫu DTO (Data Transfer Object)
- Xây dựng logic nghiệp vụ
- Tạo các thành phần tầng service

#### Tầng API
- Viết các API thực hiện các thao tác CRUD (Create, Read, Update, Delete)
- Triển khai các phương thức HTTP phù hợp
- Tuân theo quy ước RESTful

#### Xử Lý Ngoại Lệ
- Xây dựng logic xử lý ngoại lệ toàn diện
- Tạo các lớp ngoại lệ tùy chỉnh
- Triển khai global exception handlers

#### Tính Năng Bổ Sung
- Triển khai chức năng auditing
- Tài liệu hóa REST APIs sử dụng OpenAPI specification
- Thêm validation phù hợp

## Tài Liệu Tham Khảo

### GitHub Repository

Truy cập mã nguồn tham khảo hoàn chỉnh tại:
```
github.com/easybites/microservices
```

#### Mã Nguồn Có Sẵn
- Section 2 chứa các triển khai hoàn chỉnh:
  - Accounts Microservice
  - Cards Microservice
  - Loans Microservice

### Tham Khảo Database Schema

#### Schema Loans Microservice

**Tên Bảng:** `loans`

**Các Cột:**
- `loan_id` - Khóa chính (tự động tạo)
- `mobile_number` - Số điện thoại khách hàng
- `loan_number` - Mã định danh khoản vay duy nhất
- `loan_type` - Loại khoản vay
- `total_loan` - Tổng số tiền vay
- `amount_paid` - Số tiền đã trả
- `outstanding_amount` - Số tiền còn lại

**Vị Trí:** File `schema.sql` trong thư mục Loans Microservice

### Cấu Hình Port

Cấu hình các port sau trong file `application.yml`:

- **Accounts Microservice:** Port 8080
- **Cards Microservice:** Port 9000
- **Loans Microservice:** Port 8090

## Thực Hành Tốt Nhất

### Quy Ước Đặt Tên
- Tuân theo cùng quy ước đặt tên như Accounts Microservice
- Sử dụng tên lớp nhất quán
- Áp dụng cách đặt tên phương thức thống nhất
- Duy trì tính nhất quán trong tên trường

### Tiêu Chuẩn Mã Nguồn
- Sao chép cấu trúc từ repository tham khảo
- Đảm bảo mã nguồn tương tự cho các sửa đổi trong tương lai
- Duy trì tính nhất quán giữa tất cả các microservices

### Phương Pháp Phát Triển
- Tham khảo GitHub repository khi cần
- Hiểu quy trình và các tiêu chuẩn
- Có thể sao chép mã từ repository
- Tập trung vào việc hiểu chi tiết triển khai

## Tài Nguyên Kiểm Thử

### Postman Collection

Một file JSON Postman collection có sẵn trong GitHub repository:
- Tải xuống collection
- Import vào Postman
- Kiểm thử tất cả các API endpoints

## Các Liên Kết Quan Trọng

Tất cả tài nguyên tham khảo được duy trì trong GitHub repository:

1. **Tài Liệu Spring Boot** - Tài liệu chính thức Spring Boot
2. **Spring Initializr** - [start.spring.io](https://start.spring.io)
3. **DTO Pattern** - Bài viết blog giải thích về pattern
4. **Spring Doc** - Website tài liệu Spring
5. **OpenAPI Specification** - Tiêu chuẩn tài liệu hóa API

## Kết Quả Mong Đợi

Sau khi hoàn thành bài tập này, bạn sẽ:
- Xây dựng hai microservices hoàn chỉnh (Cards và Loans)
- Áp dụng các tiêu chuẩn nhất quán trên nhiều microservices
- Hiểu các mẫu kiến trúc microservice
- Thực hành triển khai ứng dụng Spring Boot cấp doanh nghiệp
- Chuẩn bị cho các chủ đề nâng cao trong các bài giảng sắp tới

## Các Bước Tiếp Theo

Giảng viên sẽ xem xét và giải thích tất cả mã nguồn có trong các microservices này trong các bài giảng tương lai, đảm bảo sự phù hợp giữa triển khai của bạn và kiến trúc tham khảo.

---

**Lưu Ý:** Bài tập này được thiết kế để củng cố việc học thông qua triển khai thực tế. Hãy dành thời gian để hiểu từng thành phần trong khi xây dựng các microservices.




FILE: 26-xay-dung-loans-microservice-tong-quan.md


# Xây Dựng Loans Microservice - Tổng Quan

## Giới Thiệu

Phần này trình bày cách triển khai microservice Loans (Quản lý Khoản vay), tuân theo cùng các mẫu kiến trúc và tiêu chuẩn mã hóa như microservice Accounts. Microservice này sẽ xử lý các thao tác về khoản vay bao gồm tạo, đọc, cập nhật và xóa (CRUD).

## Cấu Hình Dự Án

### Các Dependency Maven (pom.xml)

Loans microservice sử dụng các dependency chính sau:

- **Spring Boot Actuator** - Để giám sát và quản lý
- **Spring Data JPA** - Cho các thao tác cơ sở dữ liệu
- **Spring Boot Starter Validation** - Để xác thực đầu vào
- **Spring Boot Starter Web** - Để phát triển REST API
- **Spring Boot DevTools** - Tiện ích phát triển
- **H2 Database** - Cơ sở dữ liệu trong bộ nhớ
- **Lombok** - Giảm code boilerplate
- **SpringDoc OpenAPI** - Để tài liệu hóa API
- **Spring Boot Starter Test** - Để kiểm thử

**Chi Tiết Dự Án:**
- Group ID: `com.easybytes`
- Artifact ID: `loans`
- Phiên Bản Java: 17
- Cổng: **8090** (quan trọng để duy trì xuyên suốt khóa học)

### Cấu Hình Application (application.yaml)

```yaml
server:
  port: 8090

spring:
  datasource:
    url: jdbc:h2:mem:loansdb
    driver-class-name: org.h2.Driver
    username: sa
    password: ''
  h2:
    console:
      enabled: true
  jpa:
    database-platform: org.hibernate.dialect.H2Dialect
    hibernate:
      ddl-auto: update
    show-sql: true
```

**Quan Trọng:** Luôn sử dụng cổng 8090 cho Loans microservice để tránh các vấn đề cấu hình với Docker và Kubernetes ở các phần sau.

## Cấu Trúc Cơ Sở Dữ Liệu

### Cấu Trúc Bảng Loans

Loans microservice sử dụng một bảng duy nhất tên là `loans`:

| Tên Cột | Kiểu Dữ Liệu | Mô Tả |
|---------|--------------|-------|
| loan_id | Primary Key | Định danh duy nhất tự động sinh |
| mobile_number | String | Số điện thoại khách hàng (liên kết với Accounts microservice) |
| loan_number | String | Mã số khoản vay được sinh ra |
| loan_type | String | Loại khoản vay (ví dụ: Vay mua nhà, Vay mua xe) |
| total_loan | Decimal | Tổng số tiền vay |
| amount_paid | Decimal | Số tiền đã trả |
| outstanding_amount | Decimal | Số tiền còn lại phải trả |
| created_at | Timestamp | Thời điểm tạo bản ghi |
| created_by | String | Người tạo bản ghi |
| updated_at | Timestamp | Thời điểm cập nhật cuối |
| updated_by | String | Người cập nhật cuối cùng |

**Lưu Ý Thiết Kế:** Loans microservice không có bảng customer riêng. Nó sử dụng số điện thoại để liên kết với khách hàng đã tạo trong Accounts microservice.

## Các Lớp Entity

### Base Entity

Chứa các trường audit chung:
- `created_at` - Thời điểm tạo
- `created_by` - Thông tin người tạo
- `updated_at` - Thời điểm sửa đổi cuối
- `updated_by` - Thông tin người sửa đổi cuối

### Loans Entity

```java
@Entity
public class Loans extends BaseEntity {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long loanId;
    
    private String mobileNumber;
    private String loanNumber;
    private String loanType;
    private Integer totalLoan;
    private Integer amountPaid;
    private Integer outstandingAmount;
}
```

**Điểm Chính:**
- Kế thừa `BaseEntity` để có các trường audit
- Việc sinh khóa chính được ủy thác cho Spring Data JPA
- Tên trường khớp với tên cột (không cần annotation `@Column`)
- Loan ID không được expose trong DTOs (chi tiết kỹ thuật, không phải thông tin nghiệp vụ)

## Data Transfer Objects (DTOs)

### Loans DTO

Chỉ chứa các trường liên quan đến nghiệp vụ:
- `mobileNumber` - Số điện thoại khách hàng
- `loanNumber` - Định danh khoản vay
- `loanType` - Loại khoản vay
- `totalLoan` - Tổng số tiền vay
- `amountPaid` - Số tiền đã trả
- `outstandingAmount` - Số dư còn lại

**Lợi Ích Của DTO Pattern:**
- Tách biệt biểu diễn nội bộ với API bên ngoài
- Ẩn các chi tiết kỹ thuật (như khóa chính)
- Cho phép validation và annotation tài liệu hóa

### Các Annotation Validation

- `@NotEmpty` - Đảm bảo trường không rỗng
- `@Pattern` - Xác thực theo mẫu regex
- `@Positive` - Chỉ chấp nhận số dương (không cho phép số 0)
- `@PositiveOrZero` - Chấp nhận số 0 và số dương

### Các Annotation OpenAPI

- `@Schema` - Thêm mô tả và metadata vào tài liệu API

## Tầng Repository

### Loans Repository

```java
public interface LoansRepository extends JpaRepository<Loans, Long> {
    Optional<Loans> findByMobileNumber(String mobileNumber);
    Optional<Loans> findByLoanNumber(String loanNumber);
}
```

**Các Phương Thức Tùy Chỉnh:**
- `findByMobileNumber` - Lấy khoản vay theo số điện thoại khách hàng
- `findByLoanNumber` - Lấy khoản vay theo mã số khoản vay

Các phương thức này cần thiết vì khóa chính là `loanId`, nhưng các thao tác nghiệp vụ sử dụng số điện thoại và số khoản vay.

## Tầng Controller

### Loans Controller

**Cấu Hình Cơ Bản:**
- `@RestController` - Đánh dấu là REST controller
- `@RequestMapping("/api")` - Đường dẫn cơ sở cho tất cả API
- Trả về response dạng JSON
- Inject `ILoanService` cho logic nghiệp vụ

### Các API Endpoints

1. **Tạo Khoản Vay** - `POST /api/create`
   - Nhận số điện thoại làm query parameter
   - Tạo bản ghi khoản vay mới
   - Trả về 201 (Created) khi thành công

2. **Lấy Chi Tiết Khoản Vay** - `GET /api/fetch`
   - Nhận số điện thoại làm query parameter
   - Trả về chi tiết khoản vay
   - Trả về 200 (OK) với dữ liệu khoản vay

3. **Cập Nhật Chi Tiết Khoản Vay** - `PUT /api/update`
   - Nhận Loans DTO trong request body
   - Cập nhật thông tin khoản vay
   - Trả về 200 (OK) khi thành công
   - Trả về 417 (Expectation Failed) khi thất bại

4. **Xóa Chi Tiết Khoản Vay** - `DELETE /api/delete`
   - Nhận số điện thoại làm query parameter
   - Xóa bản ghi khoản vay
   - Trả về 200 (OK) khi thành công

**Tài Liệu OpenAPI:**
Tất cả endpoints bao gồm:
- `@Operation` - Tóm tắt và mô tả operation
- `@ApiResponse` - Mã response và mô tả

## Tầng Service

### Interface ILoanService

Định nghĩa bốn phương thức trừu tượng:
- `createLoan(String mobileNumber)`
- `fetchLoan(String mobileNumber)`
- `updateLoan(LoansDto loansDto)`
- `deleteLoan(String mobileNumber)`

### Triển Khai Loan Service

#### Logic Tạo Khoản Vay

```java
public void createLoan(String mobileNumber) {
    // Kiểm tra khoản vay đã tồn tại chưa
    Optional<Loans> optionalLoans = loansRepository.findByMobileNumber(mobileNumber);
    if(optionalLoans.isPresent()) {
        throw new LoanAlreadyExistsException("Loan already exists");
    }
    
    // Tạo khoản vay mới
    loansRepository.save(createNewLoan(mobileNumber));
}
```

**Giá Trị Mặc Định Khoản Vay Mới:**
- Mã Số Khoản Vay: Số ngẫu nhiên 12 chữ số
- Loại Khoản Vay: Vay mua nhà (mặc định)
- Tổng Khoản Vay: 100,000 (sử dụng dấu gạch dưới để dễ đọc: `100_000`)
- Số Tiền Đã Trả: 0
- Số Tiền Còn Lại: 100,000

**Lưu Ý Tính Năng Java:** Dấu gạch dưới trong các giá trị số (được giới thiệu trong Java 7/8) cải thiện khả năng đọc. JVM loại bỏ chúng trong quá trình biên dịch.

#### Logic Lấy Khoản Vay

```java
public LoansDto fetchLoan(String mobileNumber) {
    Loans loans = loansRepository.findByMobileNumber(mobileNumber)
        .orElseThrow(() -> new ResourceNotFoundException("Loan", "mobileNumber", mobileNumber));
    
    return LoansMapper.mapToLoansDto(loans, new LoansDto());
}
```

- Lấy khoản vay theo số điện thoại
- Ném `ResourceNotFoundException` nếu không tìm thấy
- Chuyển đổi entity sang DTO bằng mapper

#### Logic Cập Nhật Khoản Vay

```java
public boolean updateLoan(LoansDto loansDto) {
    Loans loans = loansRepository.findByLoanNumber(loansDto.getLoanNumber())
        .orElseThrow(() -> new ResourceNotFoundException("Loan", "loanNumber", loansDto.getLoanNumber()));
    
    LoansMapper.mapToLoans(loansDto, loans);
    loansRepository.save(loans);
    return true;
}
```

- Lấy theo mã số khoản vay (định danh bất biến)
- Map các giá trị DTO vào entity
- Phương thức Save thực hiện UPDATE (không phải INSERT) khi bản ghi đã tồn tại
- Trả về true khi thành công

#### Logic Xóa Khoản Vay

```java
public boolean deleteLoan(String mobileNumber) {
    Loans loans = loansRepository.findByMobileNumber(mobileNumber)
        .orElseThrow(() -> new ResourceNotFoundException("Loan", "mobileNumber", mobileNumber));
    
    loansRepository.deleteById(loans.getLoanId());
    return true;
}
```

- Lấy khoản vay theo số điện thoại
- Xóa theo khóa chính (loanId)
- Trả về true khi thành công

## Xử Lý Exception

### Các Exception Tùy Chỉnh

- **LoanAlreadyExistsException** - Ném khi cố gắng tạo khoản vay trùng lặp
- **ResourceNotFoundException** - Ném khi không tìm thấy khoản vay

### Global Exception Handler

Xử lý:
- Lỗi validation đầu vào
- Runtime exceptions
- Custom business exceptions

Trả về error response phù hợp với:
- Thông báo lỗi
- Mã trạng thái
- Timestamp
- Đường dẫn API

## Kiểm Thử Với Postman

### Các Kịch Bản Test

**1. Tạo Khoản Vay**
```
POST http://localhost:8090/api/create?mobileNumber=1234567890
Response: 201 - Tạo khoản vay thành công
```

**2. Lấy Khoản Vay**
```
GET http://localhost:8090/api/fetch?mobileNumber=1234567890
Response: 200 - Trả về chi tiết khoản vay
```

**3. Cập Nhật Khoản Vay**
```
PUT http://localhost:8090/api/update
Body: {
  "mobileNumber": "1234567890",
  "loanNumber": "123456789012",
  "loanType": "Vehicle Loan",
  "totalLoan": 100000,
  "amountPaid": 10000,
  "outstandingAmount": 90000
}
Response: 200 - Cập nhật khoản vay thành công
```

**4. Xóa Khoản Vay**
```
DELETE http://localhost:8090/api/delete?mobileNumber=1234567890
Response: 200 - Xóa khoản vay thành công
```

### Các Test Case Tiêu Cực

**Lỗi Validation:**
- Số tiền âm → Lỗi validation
- Định dạng số điện thoại không hợp lệ → Lỗi validation
- Mã khoản vay > 12 chữ số → Lỗi validation

**Lỗi Nghiệp Vụ:**
- Số điện thoại không tồn tại → ResourceNotFoundException
- Tạo khoản vay trùng lặp → LoanAlreadyExistsException

## Ghi Chú Quan Trọng

1. **Tính Nhất Quán Số Điện Thoại:** Sử dụng cùng một số điện thoại xuyên suốt các microservices Accounts, Loans và Cards để kiểm thử tích hợp ở các phần sau.

2. **Số Cổng:** Luôn sử dụng cổng 8090 cho Loans microservice để tránh vấn đề với cấu hình Docker và Kubernetes.

3. **Chiến Lược Lặp Lại:** Khóa học lặp lại mỗi khái niệm ba lần trên ba microservices (Accounts, Loans, Cards) để củng cố kiến thức và xây dựng trí nhớ cơ bắp.

4. **Tiêu Chuẩn Code:** Tuân theo cùng các tiêu chuẩn và mẫu code trên tất cả microservices để đảm bảo tính nhất quán.

## Bước Tiếp Theo

Bài giảng tiếp theo sẽ đề cập đến Cards microservice, tuân theo các mẫu và tiêu chuẩn tương tự. Bạn có thể bỏ qua nếu đã nắm vững các khái niệm, hoặc xem lại để củng cố.

## Tóm Tắt

Loans microservice minh họa:
- Cấu trúc dự án Spring Boot tiêu chuẩn
- Phát triển REST API với các HTTP method phù hợp
- JPA entities và repositories với các truy vấn tùy chỉnh
- DTO pattern cho thiết kế API
- Input validation và xử lý exception
- Tài liệu OpenAPI
- Triển khai logic nghiệp vụ trong tầng service
- Các thao tác CRUD với xử lý lỗi phù hợp

Tất cả các mẫu và thực hành sẽ được lặp lại trong Cards microservice để củng cố kiến thức.




FILE: 27-xay-dung-cards-microservice-tong-quan.md


# Xây Dựng Cards Microservice - Tổng Quan

## Giới Thiệu

Phần này trình bày cách triển khai microservice Cards (Quản lý Thẻ), microservice thứ ba và cuối cùng trong bộ ba dịch vụ nghiệp vụ cốt lõi của chúng ta (Accounts, Loans và Cards). Vì các mẫu thiết kế và tiêu chuẩn đã được giải thích hai lần trước đó, phần này sẽ là một hướng dẫn nhanh tập trung vào các chi tiết triển khai chính.

## Cấu Hình Dự Án

### Các Maven Dependencies (pom.xml)

**Chi Tiết Dự Án:**
- Group ID: `com.easybytes`
- Artifact ID: `cards`
- Name: `cards`
- Phiên Bản Java: 17

**Các Dependency Chính:**
- Spring Boot Actuator
- Spring Data JPA
- Spring Boot Starter Validation
- Spring Boot Starter Web
- Spring Boot DevTools
- H2 Database
- Lombok
- SpringDoc OpenAPI
- Spring Boot Starter Test

### Cấu Hình Application (application.yaml)

```yaml
server:
  port: 9000

spring:
  datasource:
    url: jdbc:h2:mem:cardsdb
    driver-class-name: org.h2.Driver
    username: sa
    password: ''
  h2:
    console:
      enabled: true
  jpa:
    database-platform: org.hibernate.dialect.H2Dialect
    hibernate:
      ddl-auto: update
    show-sql: true
```

### Tóm Tắt Phân Bổ Số Cổng

| Microservice | Số Cổng |
|-------------|---------|
| Accounts | 8080 |
| Loans | 8090 |
| Cards | 9000 |

**Quan Trọng:** Luôn sử dụng cổng 9000 cho Cards microservice xuyên suốt khóa học để đảm bảo tính nhất quán với cấu hình Docker và Kubernetes.

## Cấu Trúc Cơ Sở Dữ Liệu

### Cấu Trúc Bảng Cards

Cards microservice sử dụng một bảng duy nhất có tên `cards`:

| Tên Cột | Kiểu Dữ Liệu | Mô Tả |
|---------|--------------|-------|
| card_id | Primary Key | Định danh duy nhất tự động sinh |
| mobile_number | String | Số điện thoại khách hàng (liên kết với Accounts microservice) |
| card_number | String | Số thẻ được sinh ra (12 chữ số) |
| card_type | String | Loại thẻ (ví dụ: Thẻ tín dụng, Thẻ ghi nợ) |
| total_limit | Decimal | Tổng hạn mức tín dụng/ghi nợ |
| amount_used | Decimal | Số tiền đã sử dụng/chi tiêu |
| available_amount | Decimal | Số tiền còn lại có thể sử dụng |
| created_at | Timestamp | Thời điểm tạo bản ghi |
| created_by | String | Người tạo bản ghi |
| updated_at | Timestamp | Thời điểm cập nhật cuối |
| updated_by | String | Người cập nhật cuối cùng |

**Triết Lý Thiết Kế:**
- Giữ microservices đơn giản để tập trung vào tiêu chuẩn và khái niệm
- Tránh logic nghiệp vụ phức tạp thay đổi theo từng dự án
- Tập trung vào các mẫu kiến trúc và thực hành tốt nhất
- Sử dụng số điện thoại nhất quán trên tất cả microservices để tích hợp

## Các Lớp Entity

### Base Entity

Chứa các trường audit:
- `created_at`
- `created_by`
- `updated_at`
- `updated_by`

### Cards Entity

```java
@Entity
public class Cards extends BaseEntity {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long cardId;
    
    private String mobileNumber;
    private String cardNumber;
    private String cardType;
    private Integer totalLimit;
    private Integer amountUsed;
    private Integer availableAmount;
}
```

**Tính Năng Chính:**
- Tự động sinh khóa chính được xử lý bởi Spring Data JPA
- Kế thừa `BaseEntity` cho audit trail
- Tên trường khớp với tên cột (không cần `@Column`)

## Data Transfer Objects (DTOs)

### Cards DTO

```java
public class CardsDto {
    @Schema(description = "Số điện thoại khách hàng")
    @NotEmpty(message = "Số điện thoại không được để trống")
    @Pattern(regexp = "^[0-9]{10}$", message = "Số điện thoại phải có 10 chữ số")
    private String mobileNumber;
    
    @Schema(description = "Số thẻ")
    @NotEmpty(message = "Số thẻ không được để trống")
    @Pattern(regexp = "^[0-9]{12}$", message = "Số thẻ phải có 12 chữ số")
    private String cardNumber;
    
    @Schema(description = "Loại thẻ")
    @NotEmpty(message = "Loại thẻ không được để trống")
    private String cardType;
    
    @Schema(description = "Tổng hạn mức")
    @Positive(message = "Tổng hạn mức phải là số dương")
    private Integer totalLimit;
    
    @Schema(description = "Số tiền đã sử dụng")
    @PositiveOrZero(message = "Số tiền đã sử dụng phải là số dương hoặc 0")
    private Integer amountUsed;
    
    @Schema(description = "Số tiền còn lại")
    @PositiveOrZero(message = "Số tiền còn lại phải là số dương hoặc 0")
    private Integer availableAmount;
}
```

**Lợi Ích Của DTO:**
- Triển khai DTO pattern để tách biệt biểu diễn nội bộ và bên ngoài
- Bao gồm các annotation validation
- Tài liệu OpenAPI schema
- Các giá trị ví dụ cho tài liệu API tốt hơn

### Error Response DTO

Cấu trúc error response chuẩn cho xử lý lỗi nhất quán.

## Tầng Repository

### Cards Repository

```java
public interface CardsRepository extends JpaRepository<Cards, Long> {
    Optional<Cards> findByMobileNumber(String mobileNumber);
    Optional<Cards> findByCardNumber(String cardNumber);
}
```

**Các Phương Thức Tùy Chỉnh:**
- `findByMobileNumber` - Lấy thẻ theo số điện thoại khách hàng
- `findByCardNumber` - Lấy thẻ theo số thẻ

Cần thiết vì khóa chính là `cardId`, nhưng các thao tác nghiệp vụ sử dụng số điện thoại và số thẻ.

## Tầng Controller

### Cards Controller

**Cấu Hình:**
- `@RestController` - Đánh dấu là REST controller
- `@RequestMapping("/api")` - Đường dẫn cơ sở cho tất cả endpoints
- Trả về response dạng JSON
- Auto-wire `ICardService`

### Các API Endpoints

#### 1. Tạo Thẻ
```
POST /api/create?mobileNumber={mobileNumber}
Response: 201 Created
```
- Nhận số điện thoại làm query parameter
- Tạo thẻ mới cho khách hàng
- Trả về 201 khi thành công

#### 2. Lấy Chi Tiết Thẻ
```
GET /api/fetch?mobileNumber={mobileNumber}
Response: 200 OK
```
- Lấy chi tiết thẻ theo số điện thoại
- Trả về thông tin thẻ dạng JSON

#### 3. Cập Nhật Chi Tiết Thẻ
```
PUT /api/update
Body: CardsDto
Response: 200 OK hoặc 417 Expectation Failed
```
- Nhận Cards DTO trong request body
- Cập nhật thông tin thẻ
- Trả về 200 khi thành công, 417 khi thất bại

#### 4. Xóa Chi Tiết Thẻ
```
DELETE /api/delete?mobileNumber={mobileNumber}
Response: 200 OK hoặc 417 Expectation Failed
```
- Xóa thẻ theo số điện thoại
- Trả về 200 khi thành công, 417 khi thất bại

## Tầng Service

### Interface ICardService

Định nghĩa bốn phương thức trừu tượng:
- `createCard(String mobileNumber)`
- `fetchCard(String mobileNumber)`
- `updateCard(CardsDto cardsDto)`
- `deleteCard(String mobileNumber)`

### Triển Khai Card Service

#### Logic Tạo Thẻ

```java
public void createCard(String mobileNumber) {
    // Kiểm tra thẻ đã tồn tại chưa
    Optional<Cards> optionalCards = cardsRepository.findByMobileNumber(mobileNumber);
    if(optionalCards.isPresent()) {
        throw new CardAlreadyExistsException("Thẻ đã tồn tại với số điện thoại này");
    }
    
    // Tạo và lưu thẻ mới
    cardsRepository.save(createNewCard(mobileNumber));
}

private Cards createNewCard(String mobileNumber) {
    Cards newCard = new Cards();
    long randomCardNumber = 100000000000L + new Random().nextInt(900000000);
    newCard.setCardNumber(Long.toString(randomCardNumber));
    newCard.setMobileNumber(mobileNumber);
    newCard.setCardType("Credit Card");
    newCard.setTotalLimit(100_000); // Sử dụng underscore để dễ đọc
    newCard.setAmountUsed(0);
    newCard.setAvailableAmount(100_000);
    return newCard;
}
```

**Giá Trị Mặc Định Cho Thẻ Mới:**
- **Số Thẻ:** Số ngẫu nhiên 12 chữ số
- **Loại Thẻ:** Thẻ tín dụng (mặc định)
- **Tổng Hạn Mức:** 100,000 (100K)
- **Số Tiền Đã Sử Dụng:** 0
- **Số Tiền Còn Lại:** 100,000

**Lưu Ý:** Dấu gạch dưới trong các giá trị số (ví dụ: `100_000`) cải thiện khả năng đọc. Được giới thiệu trong Java 7/8, chúng bị loại bỏ trong quá trình biên dịch.

#### Logic Lấy Thẻ

```java
public CardsDto fetchCard(String mobileNumber) {
    Cards cards = cardsRepository.findByMobileNumber(mobileNumber)
        .orElseThrow(() -> new ResourceNotFoundException("Card", "mobileNumber", mobileNumber));
    
    return CardMapper.mapToCardsDto(cards, new CardsDto());
}
```

- Lấy thẻ theo số điện thoại
- Ném `ResourceNotFoundException` nếu không tìm thấy
- Chuyển đổi entity sang DTO bằng mapper

#### Logic Cập Nhật Thẻ

```java
public boolean updateCard(CardsDto cardsDto) {
    Cards cards = cardsRepository.findByCardNumber(cardsDto.getCardNumber())
        .orElseThrow(() -> new ResourceNotFoundException("Card", "cardNumber", cardsDto.getCardNumber()));
    
    CardMapper.mapToCards(cardsDto, cards);
    cardsRepository.save(cards);
    return true;
}
```

- Lấy theo số thẻ (định danh bất biến)
- Map DTO sang entity
- Phương thức Save thực hiện UPDATE (khóa chính đã tồn tại)
- Trả về true khi thành công

#### Logic Xóa Thẻ

```java
public boolean deleteCard(String mobileNumber) {
    Cards cards = cardsRepository.findByMobileNumber(mobileNumber)
        .orElseThrow(() -> new ResourceNotFoundException("Card", "mobileNumber", mobileNumber));
    
    cardsRepository.deleteById(cards.getCardId());
    return true;
}
```

- Lấy thẻ theo số điện thoại
- Xóa theo khóa chính (cardId)
- Phương án thay thế: Phương thức tùy chỉnh `deleteByMobileNumber` (được sử dụng trong Accounts microservice)
- Trả về true khi thành công

## Xử Lý Exception

### Các Exception Tùy Chỉnh

- **CardAlreadyExistsException** - Ném khi cố gắng tạo thẻ trùng lặp
- **ResourceNotFoundException** - Ném khi không tìm thấy thẻ

### Global Exception Handler

Xử lý:
- Lỗi validation đầu vào
- Runtime exceptions
- Business exceptions

Trả về error responses nhất quán với:
- Thông báo lỗi
- Mã trạng thái HTTP
- Timestamp
- Đường dẫn API

## Các Component Bổ Sung

### Card Mapper

Lớp tiện ích với các phương thức static:
- `mapToCardsDto(Cards cards, CardsDto cardsDto)` - Entity sang DTO
- `mapToCards(CardsDto cardsDto, Cards cards)` - DTO sang Entity

### Constants File

Chứa các hằng số ứng dụng.

### Audit Aware Implementation

Xử lý việc điền các trường audit cho `created_by` và `updated_by`.

## Kiểm Thử Với Postman

### Khởi Động Application

1. Chạy lớp main `CardsApplication` ở chế độ debug
2. Application khởi động trên cổng 9000
3. Xác minh logs khởi động xác nhận cổng 9000

### Các Kịch Bản Test

#### 1. Tạo Thẻ

```
POST http://localhost:9000/api/create?mobileNumber=1234567890
Response: 201 - Tạo thẻ thành công
```

#### 2. Lấy Chi Tiết Thẻ

```
GET http://localhost:9000/api/fetch?mobileNumber=1234567890

Response:
{
  "mobileNumber": "1234567890",
  "cardNumber": "123456789012",
  "cardType": "Credit Card",
  "totalLimit": 100000,
  "amountUsed": 0,
  "availableAmount": 100000
}
```

#### 3. Cập Nhật Chi Tiết Thẻ

```
PUT http://localhost:9000/api/update

Body:
{
  "mobileNumber": "1234567890",
  "cardNumber": "123456789012",
  "cardType": "Debit Card",
  "totalLimit": 100000,
  "amountUsed": 10000,
  "availableAmount": 90000
}

Response: 200 - Cập nhật thẻ thành công
```

**Sau Khi Cập Nhật - Lấy Lại:**
- Loại Thẻ: Đã đổi thành "Debit Card"
- Số Tiền Đã Sử Dụng: 10,000
- Số Tiền Còn Lại: 90,000

#### 4. Xóa Chi Tiết Thẻ

```
DELETE http://localhost:9000/api/delete?mobileNumber=1234567890
Response: 200 - Xóa thẻ thành công
```

**Xác Minh:**
- Cố gắng lấy sau khi xóa trả về 404 Not Found

### Các Test Case Tiêu Cực

#### Lỗi Validation

**Test Đầu Vào Không Hợp Lệ:**
```json
{
  "mobileNumber": "1234567890",
  "cardNumber": "1234567890123", // 13 chữ số - không hợp lệ
  "cardType": "Debit Card",
  "totalLimit": -100000,          // số âm - không hợp lệ
  "amountUsed": -10000,           // số âm - không hợp lệ
  "availableAmount": -90000       // số âm - không hợp lệ
}
```

**Kết Quả:** Trả về nhiều lỗi validation

#### Validation Số Điện Thoại

**Số điện thoại 9 chữ số:**
```
GET http://localhost:9000/api/fetch?mobileNumber=123456789
Response: 400 - Lỗi validation
```

#### Resource Not Found

**Số điện thoại không tồn tại:**
```
GET http://localhost:9000/api/fetch?mobileNumber=9999999999
Response: 404 - Không tìm thấy thẻ với dữ liệu đầu vào
```

## Tài Liệu Swagger UI

### Truy Cập Swagger UI

```
URL: http://localhost:9000/swagger-ui/index.html
```

**Tài Liệu Có Sẵn:**
- Bốn API endpoints (Create, Fetch, Update, Delete)
- Cards schema với mô tả trường
- Error Response schema
- Cấu trúc Response DTO
- Chức năng try-it-out để test

### Tài Liệu Schema

Tất cả DTOs bao gồm:
- Mô tả trường
- Quy tắc validation
- Giá trị ví dụ
- Kiểu dữ liệu

## Những Lưu Ý Quan Trọng

### 1. Thiết Lập Microservices Hoàn Chỉnh

Cả ba microservices (Accounts, Loans, Cards) đã hoàn thiện với:
- ✅ Cấu trúc dự án chuẩn
- ✅ Triển khai logic nghiệp vụ
- ✅ Xử lý exception
- ✅ Input validation
- ✅ Tài liệu OpenAPI
- ✅ Tích hợp H2 database
- ✅ Các thao tác CRUD

### 2. Khuyến Nghị Học Tập

**Dành Thời Gian:**
- Dành 4-8 giờ hoặc cả ngày để hiểu code
- Xem xét từng dòng code trong các microservices này
- Thiết lập tất cả microservices trong IDE local của bạn
- Test tất cả APIs bằng Postman collection được cung cấp
- Xác minh mọi thứ hoạt động với H2 database

### 3. Nền Tảng Cho Các Khái Niệm Tương Lai

Ba microservices này là **bước đệm** cho tất cả các khái niệm trong tương lai của khóa học:
- Docker containerization
- Kubernetes deployment
- Service discovery
- API Gateway
- Circuit breakers
- Distributed tracing
- Và nhiều hơn nữa...

### 4. Lợi Ích Của Chiến Lược Lặp Lại

Bằng cách triển khai ba microservices tương tự:
- Mỗi khái niệm được thực hành ba lần
- Các mẫu trở thành trí nhớ cơ bắp
- Tiêu chuẩn được củng cố
- Tự tin tăng lên với sự lặp lại
- Học tập tiềm thức xảy ra

### 5. Tính Nhất Quán Số Điện Thoại

**Quan Trọng:** Sử dụng cùng một số điện thoại trên cả ba microservices cho:
- Kiểm thử tích hợp
- Lấy response kết hợp
- Các thao tác xuyên service
- Demo Spring Cloud trong tương lai

## Triết Lý Thiết Kế

### Tập Trung Vào Sự Đơn Giản

Các microservices được cố ý giữ đơn giản để:
- **Tập Trung Vào Tiêu Chuẩn** - Học các mẫu kiến trúc
- **Tập Trung Vào Khái Niệm** - Hiểu công nghệ microservices
- **Tập Trung Vào Phương Pháp** - Thành thạo các thực hành phát triển
- **Tránh Phức Tạp** - Logic nghiệp vụ thay đổi theo dự án
- **Tối Đa Hóa Học Tập** - Các mẫu chung có lợi cho tất cả developers

### Không Phải Về Logic Nghiệp Vụ

Logic nghiệp vụ là:
- Khác nhau cho mỗi dự án
- Không áp dụng được phổ quát
- Tốn thời gian để triển khai
- Không phải mục tiêu học tập chính

Thay vào đó, tập trung vào:
- Các mẫu kiến trúc
- Tiêu chuẩn code
- Thực hành tốt nhất
- Khả năng của framework
- Kỹ thuật tích hợp

## Tóm Tắt

Cards microservice hoàn thiện bộ ba của chúng ta, minh họa:

1. **Kiến Trúc Nhất Quán** trên cả ba services
2. **Các Mẫu Chuẩn** - Tầng Repository, Service, Controller
3. **DTO Pattern** - Tách biệt mối quan tâm
4. **Validation** - Input validation với annotations
5. **Exception Handling** - Global error handling
6. **Documentation** - Tích hợp OpenAPI/Swagger
7. **Database Integration** - H2 với Spring Data JPA
8. **RESTful APIs** - Các phương thức HTTP và mã trạng thái phù hợp

### Thành Tựu Chính

✅ Ba microservices hoạt động đầy đủ  
✅ Tiêu chuẩn code nhất quán  
✅ Xử lý exception toàn diện  
✅ Input validation trên tất cả endpoints  
✅ Tài liệu API với Swagger  
✅ Sẵn sàng cho Docker/Kubernetes  
✅ Nền tảng cho các khái niệm nâng cao  

## Bước Tiếp Theo

1. **Nghỉ ngơi xứng đáng** - Bạn đã làm tốt lắm!
2. **Xem lại code** - Đảm bảo hiểu hoàn toàn
3. **Test kỹ lưỡng** - Xác thực tất cả kịch bản
4. **Chuẩn bị cho phần tiếp theo** - Các khái niệm microservices nâng cao đang chờ đợi

Hành trình tiếp tục ở phần tiếp theo, nơi các microservices này sẽ được nâng cao với các tính năng cấp doanh nghiệp!

---

**Chúc mừng bạn đã hoàn thành các microservices nền tảng! 🎉**




FILE: 28-kich-thuoc-hop-ly-va-ranh-gioi-microservices.md


# Kích Thước Hợp Lý và Ranh Giới Microservices

## Giới Thiệu

Sau khi xây dựng ba microservices khác nhau (Accounts, Loans và Cards) với REST APIs, chúng ta đối mặt với một thách thức quan trọng khác trong kiến trúc microservices: **Thách thức 2 - Làm thế nào để xác định kích thước hợp lý và ranh giới dịch vụ của Microservices**.

## Phép So Sánh với Kích Cỡ Áo

### Hiểu về Tầm Quan Trọng của Kích Thước

Giống như việc chọn kích cỡ áo phù hợp là rất quan trọng để thoải mái và đẹp mắt, việc xác định kích thước hợp lý cho microservices cũng cần thiết cho một kiến trúc thành công:

- **Small (S)** → Quá nhỏ đối với một số người
- **Medium (M)** → Vừa vặn tiêu chuẩn
- **Large (L)** → Thoải mái cho người có vóc dáng lớn hơn
- **Extra Large (XL)** → Phù hợp với kích cỡ lớn hơn
- **Double Extra Large (XXL)** → Kích cỡ tối đa

### Vấn Đề với Kích Thước Không Phù Hợp

**Mặc Sai Kích Cỡ:**
- Người mặc M nhưng mặc XXL: xấu hổ, rộng thùng thình, không thoải mái
- Người mặc XL nhưng mặc S: chật, hạn chế, không thể di chuyển đúng cách

**Tương tự, trong Agile/Scrum:**
- User stories được định kích thước bằng cách sử dụng kích cỡ áo dựa trên độ phức tạp
- Nguyên tắc tương tự áp dụng cho microservices

## Thách Thức 2: Xác Định Kích Thước Hợp Lý cho Microservices

### Kích Thước Hợp Lý là Gì?

Kích thước hợp lý là khía cạnh thách thức nhất khi xây dựng một hệ thống microservice thành công. Nó bao gồm:

1. **Không Quá Lớn**: Microservices không nên quá lớn đến mức bạn mất đi các lợi ích của kiến trúc microservices
2. **Không Quá Nhỏ**: Microservices không nên quá nhỏ đến mức thiếu logic nghiệp vụ đầy đủ
3. **Cân Bằng**: Tìm điểm tối ưu giảm thiểu chi phí vận hành trong khi tối đa hóa lợi ích

### Tại Sao Kích Thước Hợp Lý Quan Trọng?

**Vấn Đề với Kích Thước Không Hợp Lý:**

**Quá Nhiều Microservices Nhỏ:**
- Tăng chi phí vận hành
- Kết nối phức tạp
- Quản lý giao tiếp khó khăn
- Nhiều hạ tầng cần bảo trì hơn

**Quá Ít Microservices Lớn:**
- Mất lợi ích của microservices
- Giảm tính linh hoạt
- Khó scale độc lập
- Triển khai phức tạp hơn

### Các Bên Liên Quan Chịu Trách Nhiệm

- Kiến trúc sư (Architects)
- Lập trình viên (Developers)
- Trưởng nhóm kỹ thuật (Technical Leads)
- Quản lý (Managers)

## Hai Phương Pháp Phổ Biến để Xác Định Kích Thước Hợp Lý

### 1. Định Kích Thước Theo Lĩnh Vực (Domain-Driven Sizing - DDS)

#### Tổng Quan

Xác định kích thước và ranh giới cho microservices phù hợp chặt chẽ với các lĩnh vực nghiệp vụ và khả năng kinh doanh.

#### Ví Dụ: Ứng Dụng EasyBank

**Các Lĩnh Vực (Phòng ban/Mảng kinh doanh):**
- Tài khoản (Accounts)
- Thẻ (Cards)
- Vay (Loans)
- (Các lĩnh vực khác...)

**Cách Hoạt Động:**

Xây dựng microservices dựa trên các lĩnh vực nghiệp vụ này. Ví dụ:
- Accounts Microservice
- Cards Microservice
- Loans Microservice

#### Khi Nào Không Nên Sử Dụng Nghiêm Ngặt

**Tránh định kích thước nghiêm ngặt theo lĩnh vực khi:**
- Một lĩnh vực rất lớn
- Một lĩnh vực duy nhất xử lý nhiều sản phẩm
- Hàng trăm lập trình viên làm việc trên một lĩnh vực
- Các hoạt động kinh doanh phức tạp trong một lĩnh vực

#### Quy Trình

**Bước 1: Thu Thập Kiến Thức Lĩnh Vực**
- Trò chuyện với các chuyên gia lĩnh vực
- Tham vấn các lãnh đạo kinh doanh
- Liên quan các chuyên gia kỹ thuật
- Gặp gỡ khách hàng, phân tích viên kinh doanh và chủ sản phẩm
- Phỏng vấn nhân viên có kinh nghiệm (những người làm việc hàng thập kỷ)

**Bước 2: Thu Thập Thông Tin (3-6 tháng)**
- Các hoạt động được xử lý bởi mỗi lĩnh vực
- Quy mô nhóm
- Các ứng dụng hiện có
- Quy trình kinh doanh
- Hoạt động hàng ngày

**Bước 3: Các Phiên Brainstorming**
- Liên quan tất cả các bên liên quan:
  - Người kinh doanh
  - Người kỹ thuật
  - Khách hàng
  - Chủ sản phẩm
  - Chuyên gia lĩnh vực

**Bước 4: Xác Định Kích Thước Hợp Lý**
- Dựa trên thông tin đã thu thập
- Sự đồng thuận giữa các bên liên quan
- Phương pháp lặp lại

#### Tinh Chỉnh Liên Tục

Các tổ chức thường:
1. Bắt đầu với các giả định và kích thước ban đầu
2. Bắt đầu phát triển và triển khai
3. Theo dõi chi phí vận hành
4. Xem xét lại và tinh chỉnh kích thước khi cần
5. Hoặc **tách** các microservices lớn hoặc **gộp** các microservices nhỏ lại với nhau

#### Ưu Điểm
- Hiểu biết sâu về lĩnh vực
- Quyết định có thông tin đầy đủ
- Phù hợp với khả năng kinh doanh

#### Nhược Điểm
- **Tốn thời gian** (tối thiểu 3-6 tháng)
- Yêu cầu chuyên gia có kiến thức sâu về kinh doanh và lĩnh vực
- Cần phối hợp nhiều bên liên quan

---

### 2. Định Kích Thước Theo Event-Storming (Event-Storming Sizing - ESS)

#### Tổng Quan

Một người điều phối tiến hành các phiên tương tác với các bên liên quan sử dụng giấy note dính để xác định các sự kiện, lệnh và phản ứng.

#### Người Tham Gia

- Chủ sản phẩm (Product owners)
- Lập trình viên (Developers)
- Kiểm thử viên (Testers)
- Khách hàng (Clients)
- Chủ doanh nghiệp (Business owners)
- Lãnh đạo kinh doanh (Business leaders)

#### Quy Trình

**Bước 1: Xác Định Sự Kiện**

Mỗi người tham gia sử dụng giấy note dính để viết các sự kiện có thể xảy ra trong kinh doanh.

**Ví Dụ Sự Kiện trong Ngân Hàng:**
- Khách hàng hoàn tất thanh toán
- Khách hàng tìm kiếm sản phẩm
- Tài khoản được tạo
- Đơn xin vay được gửi

**Bước 2: Xác Định Lệnh (Commands)**

Lệnh là các quy trình khởi tạo sự kiện.

**Ví Dụ:**
- **Sự kiện**: Thanh toán hoàn tất
- **Lệnh**: Khách hàng nhấp nút "Thanh toán"

**Bước 3: Xác Định Phản Ứng (Reactions)**

Phản ứng là kết quả của các sự kiện.

**Ví Dụ:**
- **Sự kiện**: Thanh toán hoàn tất
- **Phản ứng**: Số tiền được khấu trừ từ tài khoản

**Lưu ý**: Một phản ứng đôi khi có thể đóng vai trò là lệnh cho sự kiện tiếp theo.

**Bước 4: Phân Loại Theo Lĩnh Vực**

Nhóm các sự kiện, lệnh và phản ứng theo lĩnh vực:
- **Lĩnh vực Cards**: Tất cả sự kiện, lệnh, phản ứng liên quan đến thẻ
- **Lĩnh vực Loans**: Tất cả sự kiện, lệnh, phản ứng liên quan đến vay
- **Lĩnh vực Accounts**: Tất cả sự kiện, lệnh, phản ứng liên quan đến tài khoản

#### Ưu Điểm

✅ **Nhanh**: Hoàn thành trong 5-6 cuộc họp trong một tháng
✅ **Không cần chuyên gia**: Bất kỳ ai sử dụng hoặc kiểm thử sản phẩm đều có thể tham gia
✅ **Tương tác và hấp dẫn**: Các phiên vui vẻ với nhiều bên liên quan
✅ **Toàn diện**: Thu thập nhiều thông tin nhanh chóng
✅ **Hiệu quả**: Hiệu quả hơn so với Định kích thước theo Lĩnh vực
✅ **Đơn giản**: Quy trình và kết quả rõ ràng

#### Các Bước Triển Khai (từ Blog Lucidchart)

**Bước 1**: Mời đúng người
- Khách hàng
- Lập trình viên
- Kiểm thử viên
- Quản lý
- Kiến trúc sư
- Lãnh đạo kinh doanh

**Bước 2**: Cung cấp không gian mô hình hóa không giới hạn
- Sử dụng giấy note dính hoặc công cụ số (ví dụ: Lucidchart)
- Cho các bên liên quan tự do đề cập đến bất kỳ số lượng sự kiện nào
- Cho phép trùng lặp (người điều phối sẽ loại bỏ chúng sau)

**Bước 3**: Xác định lệnh cho mỗi sự kiện lĩnh vực

**Bước 4**: Xác định phản ứng
- Xem xét phản ứng dây chuyền
- Phản ứng có thể kích hoạt sự kiện mới

**Bước 5**: Phân loại theo lĩnh vực
- Lĩnh vực kinh doanh
- Tạo sản phẩm
- Bán hàng
- Kiểm thử
- Các lĩnh vực tổ chức khác

**Bước 6**: Sử dụng các sự kiện đã phân loại làm đầu vào cho việc định kích thước microservice

#### Tài Nguyên

**Blog Lucidchart**: Chứa hướng dẫn chi tiết về việc điều phối các phiên event-storming
- Hữu ích cho lập trình viên để hiểu quy trình
- Hữu ích cho chuẩn bị phỏng vấn
- Tài liệu tham khảo cho triển khai thực tế
- Mất khoảng 10 phút để đọc

## So Sánh: Định Kích Thước Theo Lĩnh Vực vs Event-Storming

| Khía Cạnh | Định Kích Thước Theo Lĩnh Vực | Định Kích Thước Event-Storming |
|-----------|-------------------------------|-------------------------------|
| **Thời Gian Yêu Cầu** | 3-6 tháng | 1 tháng (5-6 cuộc họp) |
| **Chuyên Môn Cần Thiết** | Cao (cần chuyên gia lĩnh vực) | Thấp (ai cũng có thể tham gia) |
| **Tốc Độ** | Chậm | Nhanh |
| **Sự Tham Gia** | Hạn chế bên liên quan | Tất cả bên liên quan |
| **Hiệu Quả** | Phụ thuộc vào chuyên gia | Rất hiệu quả |
| **Quy Trình** | Tuần tự, chính thức | Tương tác, vui vẻ |
| **Tính Linh Hoạt** | Ít linh hoạt hơn | Linh hoạt hơn |

## Những Điểm Chính Cần Nhớ

1. **Kích thước hợp lý là quan trọng**: Đây là nền tảng của kiến trúc microservices thành công
2. **Cân bằng là chìa khóa**: Tránh các cực đoan (quá lớn hoặc quá nhỏ)
3. **Quy trình liên tục**: Kích thước nên được xem xét lại và tinh chỉnh theo thời gian
4. **Sự tham gia của các bên liên quan**: Bao gồm các quan điểm đa dạng cho quyết định tốt hơn
5. **Chọn phương pháp phù hợp**: Chọn Định kích thước theo Lĩnh vực hoặc Event-Storming dựa trên nhu cầu tổ chức của bạn
6. **Chi phí vận hành quan trọng**: Xem xét chi phí bảo trì và giao tiếp

## Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ áp dụng các nguyên tắc kích thước hợp lý này vào ví dụ EasyBank để thấy triển khai thực tế và làm rõ hơn các khái niệm.

## Tài Liệu Tham Khảo

- Blog Lucidchart về Event Storming
- Tài liệu GitHub README (sẽ được cập nhật với các liên kết)
- Ví dụ ứng dụng EasyBank

---

*Tài liệu này là một phần của khóa học Microservices với Spring Boot.*




FILE: 28-right-sizing-microservices-va-ranh-gioi-dich-vu.md


# Right-Sizing Microservices và Ranh Giới Dịch Vụ

## Giới Thiệu

Trong bài học này, chúng ta sẽ khám phá cách định kích thước phù hợp cho microservices và xác định ranh giới dịch vụ thích hợp thông qua ví dụ thực tế về ứng dụng ngân hàng. Chúng ta sẽ phân tích ba phương pháp khác nhau được đề xuất bởi các nhóm khác nhau và xác định chiến lược sizing nào hiệu quả nhất.

## Tình Huống

Một ứng dụng ngân hàng cần di chuyển hoặc được xây dựng dựa trên kiến trúc microservices. CEO/CTO thành lập ba nhóm khác nhau để phân tích và đề xuất chiến lược sizing microservices của riêng họ.

Các nhóm đã sử dụng các phương pháp như:
- Domain-Driven Sizing (Định kích thước theo miền nghiệp vụ)
- Event-Driven Sizing (Định kích thước theo sự kiện)

## Các Đề Xuất Của Các Nhóm

### Phương Án Nhóm 1: 2 Microservices

**Cấu trúc:**
1. **Accounts Microservice** - Kết hợp:
   - Chức năng Tài khoản Tiết kiệm
   - Chức năng Tài khoản Giao dịch

2. **Cards & Loans Microservice** - Kết hợp:
   - Quản lý Thẻ
   - Quản lý Khoản vay

**Phân tích:**
- ❌ **Không được khuyến nghị** - Tạo ra sự liên kết chặt chẽ
- Thẻ và Khoản vay được gộp chung
- Tài khoản Tiết kiệm và Tài khoản Giao dịch được gộp chung
- Các cải tiến trong tương lai của một nhóm (ví dụ: Thẻ) sẽ ảnh hưởng đến nhóm khác (ví dụ: Khoản vay)
- Thiếu tính linh hoạt cho sự phát triển độc lập

### Phương Án Nhóm 2: 4 Microservices ✅

**Cấu trúc:**
1. **Saving Account Microservice** (Microservice Tài khoản Tiết kiệm)
2. **Trading Account Microservice** (Microservice Tài khoản Giao dịch)
3. **Cards Microservice** (Microservice Thẻ)
4. **Loans Microservice** (Microservice Khoản vay)

**Phân tích:**
- ✅ **Hợp lý nhất và được Khuyến nghị**
- Mỗi miền nghiệp vụ là một microservice độc lập
- Cung cấp sự liên kết lỏng lẻo giữa các dịch vụ
- Mang lại tính linh hoạt cho các nhóm khác nhau có chu trình cải tiến riêng
- Các nhóm có thể chọn ngôn ngữ lập trình và cơ sở dữ liệu riêng
- Lựa chọn an toàn hơn cho yêu cầu hiện tại

### Phương Án Nhóm 3: 7+ Microservices

**Cấu trúc:**
1. **Saving Account Microservice** (Microservice Tài khoản Tiết kiệm)
2. **Trading Account Microservice** (Microservice Tài khoản Giao dịch)
3. **Debit Card Microservice** (Microservice Thẻ Ghi nợ)
4. **Credit Card Microservice** (Microservice Thẻ Tín dụng)
5. **Home Loan Microservice** (Microservice Vay mua Nhà)
6. **Vehicle Loan Microservice** (Microservice Vay mua Xe)
7. **Personal Loan Microservice** (Microservice Vay Cá nhân)

**Phân tích:**
- ⚠️ **Quá Chi tiết** - Chỉ hợp lý khi có sự khác biệt về chức năng đáng kể
- Chỉ có ý nghĩa nếu có sự khác biệt chức năng lớn giữa:
  - Thẻ ghi nợ vs. Thẻ tín dụng
  - Vay mua nhà vs. Vay mua xe vs. Vay cá nhân
- Nếu chức năng tương tự, điều này tạo ra:
  - Quá nhiều microservices
  - Chi phí vận hành cao
  - Độ phức tạp không cần thiết

## Tiêu Chí Quyết Định

Khi chọn kích thước microservices, hãy xem xét:

1. **Phân tách Miền Nghiệp vụ**: Mỗi microservice nên đại diện cho một miền nghiệp vụ riêng biệt
2. **Liên kết Lỏng lẻo**: Các dịch vụ nên độc lập và liên kết lỏng lẻo
3. **Tính Tự chủ của Nhóm**: Các nhóm khác nhau nên có khả năng cải tiến dịch vụ của họ một cách độc lập
4. **Chi phí Vận hành**: Tránh tạo quá nhiều dịch vụ làm tăng độ phức tạp quản lý
5. **Sự Khác biệt về Chức năng**: Chỉ tách dịch vụ khi có sự khác biệt đáng kể về logic nghiệp vụ

## Phương Án Chiến Thắng

**Phương án của Nhóm 2 được lựa chọn** vì:

- Hiện tại không có logic nghiệp vụ riêng biệt để phân biệt giữa:
  - Thẻ ghi nợ vs. Thẻ tín dụng
  - Vay mua nhà vs. Vay mua xe vs. Vay cá nhân
- Những khác biệt nhỏ có thể được xử lý thông qua:
  - Các cột trong cơ sở dữ liệu
  - Cấu hình
  - Các phương pháp khác cho những khác biệt logic nghiệp vụ nhỏ
- Cung cấp sự cân bằng tốt giữa tách biệt các mối quan tâm và sự đơn giản trong vận hành

## Những Điểm Chính Cần Nhớ

1. **Không có Sizing Hoàn hảo ngay từ Ngày Đầu**: Không có kích thước "đúng" phổ quát cho microservices ban đầu
2. **Phát triển Liên tục**: Các tổ chức nên liên tục đánh giá và định kích thước lại microservices của họ
3. **Quá trình Học hỏi**: Các công ty học hỏi từ việc triển khai microservices và điều chỉnh ranh giới cho phù hợp
4. **Linh hoạt cho Tương lai**: Nếu có vấn đề phát sinh (ví dụ: Cards microservice trở nên quá phức tạp), bạn có thể tách nó sau thành Debit Card và Credit Card microservices
5. **Sự Tham gia của Các Bên liên quan**: Các thay đổi sizing lớn nên được thảo luận với tất cả các bên liên quan
6. **Tránh Over-Engineering**: Đừng tạo microservices riêng biệt cho những khác biệt logic nghiệp vụ nhỏ

## Thực Hành Tốt Nhất

- Bắt đầu với phương pháp sizing an toàn, vừa phải
- Giám sát độ phức tạp của dịch vụ và tính tự chủ của nhóm
- Sẵn sàng tách hoặc hợp nhất các dịch vụ dựa trên kinh nghiệm thực tế
- Cân bằng giữa quá ít (liên kết chặt chẽ) và quá nhiều (chi phí vận hành) microservices
- Xem xét khả năng tách biệt cơ sở dữ liệu
- Đánh giá yêu cầu về chu trình cải tiến của nhóm

## Kết Luận

Right-sizing microservices là một quá trình lặp đi lặp lại. Bắt đầu với một phương pháp hợp lý cung cấp sự liên kết lỏng lẻo và tính tự chủ của nhóm, sau đó điều chỉnh dựa trên kinh nghiệm và yêu cầu thực tế. Mục tiêu không phải là đạt được sizing hoàn hảo ngay từ ngày đầu tiên, mà là tạo ra một kiến trúc linh hoạt có thể phát triển cùng với nhu cầu của tổ chức bạn.




FILE: 29-strangler-fig-pattern-cho-viec-migrate-microservices.md


# Strangler Fig Pattern cho việc Migration Microservices

## Tổng quan

Khi migration một ứng dụng legacy hoặc monolithic sang kiến trúc microservices hiện đại, **Strangler Fig Pattern** là một design pattern đã được chứng minh mà các tổ chức có thể tuân theo. Pattern này cho phép tiếp cận migration dần dần với rủi ro thấp.

## Strangler Fig Pattern là gì?

Strangler Fig Pattern là một software migration pattern được sử dụng để dần dần thay thế hoặc tái cấu trúc một legacy system bằng một system mới. Đặc điểm chính là legacy application được thay thế bằng cách tiếp cận hiện đại **từng phần một**, mà không làm gián đoạn chức năng hiện có.

### Nguồn gốc của tên gọi

Pattern này lấy tên từ cách thức cây sung dây (strangler fig plant) phát triển quanh một cây hiện có, từ từ thay thế nó cho đến khi cây gốc không còn cần thiết nữa. Cây sung dây:
1. Bắt đầu như một cây nhỏ mọc bên cạnh cây gốc
2. Dần dần phát triển quanh cây chính
3. Cuối cùng thay thế hoàn toàn cây gốc

Cùng một chiến lược này được áp dụng khi các tổ chức migrate các legacy application của họ sang microservices.

## Khi nào sử dụng Pattern này

Strangler Fig Pattern được khuyến nghị mạnh mẽ trong các trường hợp sau:

1. **Hệ thống Legacy lớn hoặc phức tạp**: Khi hiện đại hóa một legacy system lớn hoặc phức tạp (không khuyến nghị cho các hệ thống nhỏ)
2. **Tránh rủi ro Big Bang Migration**: Khi bạn muốn tránh các rủi ro liên quan đến việc viết lại hệ thống hoàn toàn hoặc "Big Bang" migration (đột ngột migrate mọi thứ trong một ngày)
3. **Tính liên tục hoạt động**: Khi legacy system cần duy trì hoạt động trong quá trình chuyển đổi sang hệ thống mới

## Ví dụ Migration: Ứng dụng Ngân hàng

Hãy xem xét một ví dụ thực tế về migration ứng dụng ngân hàng:

### Trạng thái ban đầu
- **Ứng dụng Monolithic** chứa toàn bộ chức năng:
  - Cards (Thẻ)
  - Accounts (Tài khoản)
  - Loans (Khoản vay)

### Các giai đoạn Migration

#### Giai đoạn 1: Accounts Microservice
- Development team tạo **Accounts microservice**
- Chức năng còn lại (Cards và Loans) vẫn ở trong monolithic app
- Team xác thực rằng Accounts microservice hoạt động đúng trong production

#### Giai đoạn 2: Cards Microservice
- Sau khi hài lòng với việc triển khai Accounts microservice
- Team migrate chức năng **Cards** sang microservice
- Monolithic app bây giờ chỉ chứa chức năng Loans

#### Giai đoạn 3: Loans Microservice
- Sau khi Cards migration thành công
- Team migrate chức năng **Loans**
- Monolithic app được thay thế hoàn toàn

#### Trạng thái cuối cùng
- Không còn monolithic app
- Tất cả chức năng tồn tại như các microservices độc lập

## Lợi ích chính

### 1. Rủi ro tối thiểu
- Migrate chỉ một component tại một thời điểm giảm rủi ro
- Các vấn đề dễ dàng được xử lý khi chúng xảy ra
- Bài học từ lần migration đầu tiên giúp ích cho các lần migration tiếp theo

### 2. Migration từng bước
- Tránh các thách thức của Big Bang migration
- Khả năng rollback dễ dàng
- Xử lý tốt hơn các bất ngờ và vấn đề
- Development team có cơ hội học hỏi từ sai lầm

### 3. Testing và Validation hiệu quả
- Cả monolithic và microservices cùng tồn tại trong quá trình migration
- Traffic có thể được route giữa legacy và hệ thống mới
- Kết quả có thể được so sánh giữa hai component
- Phân phối traffic linh hoạt (ví dụ: chia 50-50%)
- 100% traffic có thể được chuyển hướng về monolithic nếu có vấn đề
- Legacy code vẫn ở trạng thái "chết" nhưng sẵn có nếu cần

## Bốn giai đoạn của Migration

### 1. Identification (Xác định)
- Xác định cần bao nhiêu microservices
- Thực hiện right-sizing của microservices sử dụng phương pháp Domain-Driven Design (DDD)
- Chia nhỏ monolithic application thành các domain riêng biệt

### 2. Transformation (Chuyển đổi)
- Chuyển đổi các component từ legacy sang microservices
- Viết lại các service sử dụng công nghệ mới hơn
- Phát triển và test các microservices riêng lẻ

### 3. Coexistence (Cùng tồn tại)
- Cả monolithic và microservices tồn tại đồng thời
- Giới thiệu **Strangler Facade** để xử lý routing traffic
- Thường được triển khai bằng cách sử dụng **API Gateway**
- Dần dần chuyển traffic từ legacy sang microservices

### 4. Elimination (Loại bỏ)
- Loại bỏ hoàn toàn legacy application
- Tất cả traffic chảy đến microservices/ứng dụng hiện đại
- Legacy system được thay thế hoàn toàn

## Chuẩn bị phỏng vấn

Pattern này thường được hỏi trong các cuộc phỏng vấn. Khi được hỏi: **"Bạn đang migrate legacy của mình sang ứng dụng dựa trên microservice như thế nào?"**

**Trả lời**: Giải thích Strangler Fig Pattern, bao gồm:
- Phương pháp migration dần dần, từng phần một
- Bốn giai đoạn: Identification, Transformation, Coexistence, và Elimination
- Lợi ích của rủi ro tối thiểu và migration từng bước
- Sử dụng API Gateway để routing traffic trong giai đoạn coexistence
- Ví dụ về việc migrate các component từng cái một

## Tóm tắt

Strangler Fig Pattern là phương pháp được khuyến nghị để migrate các legacy system phức tạp sang kiến trúc microservices. Nó cung cấp một con đường an toàn, từng bước cho phép các tổ chức:
- Giảm thiểu rủi ro migration
- Duy trì tính liên tục hoạt động
- Học hỏi và thích ứng trong quá trình
- Test kỹ lưỡng trước khi cam kết hoàn toàn
- Rollback nếu cần thiết

Bằng cách tuân theo pattern này, các development team có thể hiện đại hóa thành công ứng dụng của họ trong khi tránh được các cạm bẫy của Big Bang migrations.




FILE: 3-microservices-definition.md


# Định nghĩa và Tổng quan về Microservices

## Giới thiệu

Trong bài giảng này, chúng ta sẽ khám phá định nghĩa chính thức về microservices, cung cấp cho bạn một giải thích rõ ràng và súc tích mà bạn có thể sử dụng khi giao tiếp với cả các bên liên quan kỹ thuật và phi kỹ thuật.

## Định nghĩa Chính thức

Định nghĩa về microservices, được đưa ra bởi **James Lewis và Martin Fowler** trong bài viết blog có ảnh hưởng của họ, phát biểu rằng:

> **Microservices là một cách tiếp cận để phát triển một ứng dụng đơn lẻ như một bộ các dịch vụ nhỏ.**

### Các Đặc điểm Chính

1. **Bộ các Dịch vụ Nhỏ**
   - Một ứng dụng đơn lẻ được chia nhỏ thành nhiều dịch vụ nhỏ, tập trung
   - Ví dụ: Ứng dụng web EasyBank có thể được phát triển thành các dịch vụ riêng biệt:
     - Dịch vụ Tài khoản (Accounts)
     - Dịch vụ Vay vốn (Loans)
     - Dịch vụ Thẻ (Cards)

2. **Các Tiến trình Độc lập**
   - Mỗi dịch vụ chạy trong tiến trình riêng của nó
   - Các dịch vụ được cách ly và tự chứa

3. **Giao tiếp Nhẹ**
   - Các dịch vụ giao tiếp bằng cách sử dụng các cơ chế nhẹ
   - Các giao thức phổ biến bao gồm REST APIs
   - Cho phép giao tiếp liền mạch giữa các dịch vụ

4. **Thiết kế Hướng Nghiệp vụ**
   - Microservices được xây dựng xung quanh các khả năng nghiệp vụ
   - Mỗi dịch vụ đại diện cho một lĩnh vực nghiệp vụ cụ thể
   - Phù hợp với cấu trúc tổ chức và chức năng kinh doanh

5. **Triển khai Độc lập**
   - Các dịch vụ có thể được triển khai độc lập
   - Máy móc triển khai tự động hoàn toàn
   - Không cần triển khai lại toàn bộ ứng dụng cho các thay đổi trong một dịch vụ

## Tự động hóa và CI/CD

Một trong những lợi thế quan trọng nhất của microservices là khả năng tự động hóa toàn bộ quy trình triển khai:

- **Tự động Build**: Ngay khi một lập trình viên commit code vào kho lưu trữ của microservice, quá trình build được kích hoạt tự động
- **Tích hợp Liên tục**: Các bản build tự động được triển khai đến môi trường phát triển và UAT
- **Triển khai Liên tục**: Triển khai production cũng có thể được tự động hóa bằng cách sử dụng khái niệm CI/CD
- **Hiệu quả**: Giảm can thiệp thủ công và tăng tốc chu kỳ phát hành

## Tóm tắt Lợi ích

Kiến trúc Microservices mang lại nhiều lợi thế:

- **Khả năng Mở rộng**: Các dịch vụ riêng lẻ có thể được mở rộng độc lập
- **Linh hoạt**: Ngăn xếp công nghệ có thể thay đổi cho từng dịch vụ
- **Khả năng Phục hồi**: Lỗi trong một dịch vụ không làm sập toàn bộ ứng dụng
- **Phát triển Nhanh hơn**: Các nhóm có thể làm việc trên các dịch vụ khác nhau đồng thời
- **Bảo trì Dễ dàng**: Codebase nhỏ hơn dễ hiểu và bảo trì hơn

## Tham khảo Nhanh

Khi được hỏi "Microservices là gì?" bạn có thể sử dụng định nghĩa súc tích này:

*"Microservices là một cách tiếp cận để phát triển ứng dụng như một bộ các dịch vụ nhỏ, độc lập chạy trong các tiến trình riêng của chúng, giao tiếp qua các cơ chế nhẹ, được xây dựng xung quanh các khả năng nghiệp vụ và có thể được triển khai độc lập thông qua các quy trình triển khai tự động."*

## Kết luận

Định nghĩa này cung cấp một nền tảng vững chắc để hiểu kiến trúc microservices. Cho dù bạn đang giải thích khái niệm này cho người dùng nghiệp vụ, khách hàng hay các thành viên nhóm kỹ thuật, định nghĩa chính thức này bao gồm tất cả các khía cạnh thiết yếu của microservices.

---

**Bối cảnh Khóa học**: Bài giảng này là một phần của khóa học toàn diện về kiến trúc microservices sử dụng Java và Spring Boot, nơi chúng ta sẽ đi sâu hơn vào các chi tiết triển khai và các phương pháp hay nhất.




FILE: 30-containerization-challenges-and-docker-introduction.md


# Thách Thức Containerization và Giới Thiệu Docker

## Tổng Quan

Bài giảng này cung cấp giới thiệu toàn diện về containers, Docker và các khái niệm containerization - những công nghệ thiết yếu cho các nhà phát triển microservice làm việc với ứng dụng Java và Spring Boot.

## Container là gì?

**Container** là một môi trường được cách ly lỏng lẻo có thể tồn tại trong:
- Một server
- Một máy ảo (virtual machine)
- Hệ thống local của bạn

Containers cho phép bạn triển khai microservices bằng cách sử dụng **các gói phần mềm** bao gồm:
- Tất cả mã nguồn
- Tất cả các dependencies
- Mọi thứ cần thiết để chạy ứng dụng hoặc microservices một cách nhanh chóng và đáng tin cậy

### Lợi Ích Chính

- **Tính Nhất Quán Môi Trường**: Containers hoạt động giống nhau trên các môi trường computing khác nhau (hệ thống local, VMs trong data center, VMs trên cloud)
- **Không Cần Cài Đặt Thủ Công**: Không cần phải cài đặt dependencies hoặc cấu hình servers thủ công
- **Tính Di Động**: Cùng một container có thể được triển khai trên nhiều môi trường mà không cần sửa đổi

## Container Images

**Container images** (hoặc Docker images) là các gói phần mềm chứa tất cả dependencies và libraries cần thiết.

### So Sánh Image và Container

Hãy nghĩ về mối quan hệ giống như Java classes và objects:
- **Container Image** = Java Class (bộ khung/đại diện)
- **Container** = Java Object (thực thể đang chạy thực tế)

Giống như bạn có thể tạo nhiều objects từ một Java class, bạn có thể tạo nhiều containers từ một container image.

> Docker container là một đại diện đang chạy thực tế của Docker image.

## Software Containerization là gì?

**Software containerization** là một phương pháp ảo hóa hệ điều hành (OS virtualization):
- Triển khai nhiều containers trong một máy đơn lẻ hoặc máy ảo
- Cung cấp môi trường cách ly ảo cho mỗi container
- Làm cho mỗi container cảm thấy như đang chạy trong hệ điều hành riêng của nó

### Containerization vs Ảo Hóa Truyền Thống

| Khía Cạnh | Containerization | Virtual Machines (Hypervisor) |
|-----------|------------------|------------------------------|
| **Mức Độ Ảo Hóa** | Hệ điều hành | Phần cứng |
| **Chia Sẻ Tài Nguyên** | Chia sẻ kernel của host OS | Các OS instances riêng biệt |
| **Cách Ly** | Ảo hóa cấp độ OS | Ảo hóa cấp độ phần cứng |

#### Ảo Hóa Truyền Thống (Hypervisor)
- Ảo hóa các máy
- VMs cảm thấy như đang chạy trên phần cứng vật lý khác nhau
- Mỗi VM có OS instance riêng

#### Containerization
- Ảo hóa hệ điều hành
- Tất cả containers chia sẻ cùng kernel của host operating system
- Mỗi container cảm thấy như có OS riêng biệt

## Docker là gì?

**Docker** là một nền tảng mã nguồn mở:
- Cho phép developers chuyển đổi ứng dụng thành Docker images
- Tự động hóa việc triển khai, mở rộng và quản lý ứng dụng
- Triển khai công nghệ containerization

### Mối Quan Hệ Các Khái Niệm Chính

1. **Software Containerization** = Khái niệm
2. **Docker** = Nền tảng triển khai containerization
3. **Docker Images & Containers** = Được tạo ra từ mã nguồn ứng dụng bằng Docker

## Cách Containerization Hoạt Động

Containers dựa trên ảo hóa hệ điều hành, trong đó nhiều containers:
- Chạy trên cùng một máy vật lý hoặc máy ảo
- Chia sẻ cùng kernel của hệ điều hành
- Khác với VMs truyền thống chạy các OS instances riêng biệt

### Các Tính Năng Linux: Namespaces và Cgroups

Docker containerization dựa vào hai tính năng quan trọng của Linux:

#### 1. Namespaces

**Mục đích**: Cung cấp cách ly (isolation)

Namespaces cho phép tạo môi trường cách ly trong cùng một hệ điều hành. Mỗi container có bộ namespaces riêng chứa:
- Tài nguyên **Process** (tiến trình)
- Tài nguyên **Network** (mạng)
- Tài nguyên **Storage** (lưu trữ)
- Tài nguyên **Communication** (giao tiếp)
- **User** namespaces

**Kết quả**: Các tiến trình trong container chỉ có thể tương tác với tài nguyên trong namespace riêng của chúng, cung cấp sự cách ly với các containers khác.

#### 2. Cgroups (Control Groups)

**Mục đích**: Kiểm soát việc sử dụng tài nguyên

Trong khi namespaces cung cấp cách ly, cgroups kiểm soát lượng tài nguyên mà container có thể sử dụng:
- Phân bổ **CPU**
- Phân bổ **Memory** (bộ nhớ)
- Sử dụng **Disk** (đĩa)
- Băng thông **Network** (mạng)

**Lợi ích**:
- Thực thi giới hạn tài nguyên tại runtime
- Ngăn một container chiếm dụng tài nguyên hệ thống
- Đảm bảo phân bổ công bằng giữa nhiều containers
- Tránh tình huống các containers nhận phân bổ tài nguyên không công bằng

## Docker trên Các Hệ Điều Hành Khác Nhau

### Docker trên Linux
- Cài đặt đơn giản
- Nhận toàn bộ Docker engine trực tiếp trên Linux OS

### Docker trên macOS hoặc Windows
Cài đặt bao gồm hai thành phần:

1. **Docker Client** (CLI)
   - Được cài đặt trên host OS của bạn (Mac hoặc Windows)
   - Cung cấp giao diện người dùng

2. **Docker Server**
   - Được cài đặt trong một máy ảo Linux nhẹ
   - Chạy ẩn phía sau
   - Cung cấp Docker engine thực tế

**Kết quả**: Docker hoạt động nhất quán trên tất cả các hệ điều hành, cung cấp giao diện tương tự bất kể host OS là gì.

### Xác Minh: Lệnh Docker Version

Chạy `docker version` để xem kiến trúc:

```bash
docker version
```

**Ví dụ Output**:
- **Client**: Hiển thị host OS của bạn (ví dụ: Darwin/arm64 cho Mac, Windows cho Windows OS)
- **Server**: Hiển thị Linux (vì nó chạy trong Linux VM nhẹ)

Điều này xác nhận kiến trúc hai thành phần trên các hệ thống không phải Linux.

## Tóm Tắt

Các khái niệm chính đã được đề cập:
- **Container**: Môi trường cách ly lỏng lẻo để triển khai microservices
- **Containerization**: Phương pháp ảo hóa OS để chạy nhiều containers cách ly
- **Docker**: Nền tảng mã nguồn mở triển khai công nghệ containerization
- **Namespaces**: Cung cấp cách ly tài nguyên cho containers
- **Cgroups**: Kiểm soát và quản lý việc sử dụng tài nguyên của containers

## Các Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ khám phá kiến trúc nội bộ của Docker để hiểu cách các thành phần này hoạt động cùng nhau.

---

*Tài liệu này là một phần của khóa học microservices về Spring Boot, Java và các công nghệ containerization.*




FILE: 30-thach-thuc-containerization-va-gioi-thieu-docker.md


# Thách Thức Containerization và Giới Thiệu Docker

## Tổng Quan

Trong kiến trúc microservices, với trách nhiệm lớn đến sức mạnh lớn. Khi bạn đón nhận các thách thức của việc triển khai microservices và xử lý chúng theo các thực tiễn tốt nhất trong ngành, bạn sẽ mở khóa toàn bộ tiềm năng và lợi ích của microservices.

Phần này giới thiệu một thách thức quan trọng: **Làm thế nào để xử lý việc triển khai, tính di động và khả năng mở rộng của microservices**.

## Ba Thách Thức Chính

### 1. Thách Thức Triển Khai

**Câu hỏi:** Làm thế nào để triển khai hàng trăm microservices nhỏ với nỗ lực và chi phí tối thiểu?

- Với ứng dụng nguyên khối (monolithic), bạn chỉ có một file JAR, WAR, hoặc EAR duy nhất để triển khai lên web server hoặc application server
- Với kiến trúc microservices, các tổ chức có thể có hàng trăm microservices
- **Vấn đề:** Chúng ta có cần 100 servers và máy ảo khác nhau để triển khai chúng không? (Tất nhiên là không - đó không phải là giải pháp khả thi)

### 2. Thách Thức Tính Di Động

**Câu hỏi:** Làm thế nào để di chuyển hàng trăm microservices qua các môi trường với nỗ lực, cấu hình và chi phí tối thiểu?

#### Hành Trình Qua Các Môi Trường

Ứng dụng phải di chuyển qua nhiều môi trường:

1. Máy của developer
2. GitHub repository (hoặc hệ thống quản lý phiên bản khác)
3. Môi trường Development
4. Môi trường UAT/SIT/QA (sau khi build ổn định)
5. Môi trường Production replica (sau khi hoàn thành testing)
6. Môi trường Production (sau khi testing pre-production)

#### Các Vấn Đề Về Tính Di Động

- Với ứng dụng monolithic: Một ứng dụng, một server - dễ dàng cấu hình và di chuyển
- Với microservices: Ai quản lý tính di động cho hàng trăm services?
- **Các mối quan tâm:**
  - Yêu cầu phiên bản JDK cụ thể
  - Cấu hình web server cụ thể
  - Cấu trúc thư mục cụ thể
  - Cấu hình database cụ thể
  - Ai thực hiện tất cả công việc thủ công này cho hàng trăm microservices?

### 3. Thách Thức Khả Năng Mở Rộng

**Câu hỏi:** Làm thế nào để mở rộng các microservices cụ thể theo thời gian thực dựa trên nhu cầu traffic?

- Ứng dụng Monolithic: Mở rộng đơn giản - chỉ cần thêm một server replica
- Microservices: Câu chuyện khác
  - Cần mở rộng từng microservices riêng lẻ dựa trên nhu cầu
  - Phải scale up trong lúc traffic cao
  - Phải scale down khi nhu cầu giảm
  - Tất cả phải xảy ra với:
    - Nỗ lực tối thiểu
    - Chi phí tối thiểu
    - Không can thiệp thủ công

## Giải Pháp: Containerization

### Tại Sao Containerization?

Để vượt qua những thách thức này, chúng ta phải **containerize tất cả các microservices**.

### Containerization Là Gì?

Containerization chuyển đổi một dự án Maven thông thường thành một container. Các containers này:

- Có kích thước rất nhỏ
- Cung cấp môi trường tự cô lập cho ứng dụng
- Bao gồm tất cả các dependencies cần thiết

### Lợi Ích

- Đóng gói phiên bản Java, Tomcat, cấu hình database, cấu trúc thư mục - tất cả bên trong một container
- Triển khai cùng một container trên bất kỳ môi trường hoặc cloud nào mà không cần thay đổi
- Tối ưu hóa tài nguyên
- Môi trường cô lập cho mỗi microservice

## Docker: Nền Tảng Containerization

### Docker Là Gì?

Docker là một **nền tảng mã nguồn mở** cung cấp khả năng đóng gói và chạy ứng dụng trong một môi trường cô lập lỏng lẻo gọi là **container**.

### Docker Hoạt Động Như Thế Nào

1. Bắt đầu với một ứng dụng Maven
2. Chuyển đổi nó thành Docker image bằng Docker
3. Chạy image đó như một container bên trong bất kỳ máy ảo hoặc môi trường cloud nào

## Phép So Sánh Container

### Nguồn Cảm Hứng Từ Ngành Vận Tải Biển

Hãy nghĩ về một con tàu chở hàng vận chuyển hàng hóa giữa các quốc gia bằng containers.

**Tại sao sử dụng containers?**
- Tối ưu hóa không gian
- Cung cấp môi trường riêng biệt, cô lập cho từng loại hàng hóa
- Ví dụ: Một container có làm lạnh cho táo, một container khác không cần làm mát cho hàng điện tử

### Áp Dụng Cho Microservices

Giống như tàu biển tối ưu hóa tài nguyên với containers, chúng ta triển khai microservices như containers:

**Các Yêu Cầu Khác Nhau:**
- Một microservice có thể dùng Java 17
- Một microservice khác có thể dùng Java 21
- Databases, frameworks và ngôn ngữ khác nhau

**Vấn Đề Với Cách Tiếp Cận Truyền Thống:**
- Quản lý tất cả microservices trên một VM hoặc jumbo server duy nhất cực kỳ khó khăn
- Tài nguyên không được sử dụng tối ưu

**Giải Pháp Container:**
- Triển khai 10 microservices khác nhau với 10 yêu cầu khác nhau trên một VM duy nhất
- Mỗi container có môi trường cô lập riêng
- Tối ưu hóa việc sử dụng tài nguyên

## Điểm Chính Cần Nhớ

Khi nghĩ về Docker và containers, hãy nhớ đến phép so sánh với ngành vận tải biển. Giống như ngành vận tải biển hưởng lợi từ containers, chúng ta áp dụng cùng khái niệm cho microservices với Docker.

## Các Bước Tiếp Theo

Trong các bài giảng tiếp theo, chúng ta sẽ khám phá:
- Giới thiệu chi tiết về Docker
- Cách containerize ứng dụng
- Các thách thức cụ thể mà Docker giải quyết
- Ví dụ triển khai thực tế

---

**Ghi nhớ:** Đừng nản lòng trước các thách thức. Bằng cách đối mặt với những thách thức này và triển khai các giải pháp phù hợp, bạn sẽ tạo ra một ứng dụng microservices hoàn hảo mà tổ chức của bạn có thể tận dụng đầy đủ các lợi ích.




FILE: 31-containers-vs-virtual-machines.md


# Container so với Máy ảo trong Triển khai Microservices

## Giới thiệu

Trong bài giảng này, chúng ta sẽ làm rõ sự khác biệt cơ bản giữa container và máy ảo truyền thống, đồng thời hiểu tại sao container là lựa chọn ưu tiên cho việc triển khai microservices.

## Triển khai Server Truyền thống (Trước thời đại Cloud)

### Cài đặt Server Vật lý
- Các tổ chức mua phần cứng riêng
- Cài đặt hệ điều hành trên phần cứng vật lý
- Server kết nối với mạng công cộng
- Code được triển khai sử dụng web server hoặc application server
- Địa chỉ IP công khai được gán cho server
- Ánh xạ DNS cho truy cập tên miền

## Máy ảo trong Cloud Computing

### Máy ảo là gì?
- Server ảo được cung cấp bởi các nhà cung cấp cloud (AWS, Azure, GCP)
- Không thể nhìn thấy vật lý - chỉ có thể truy cập qua internet
- Được tạo từ phần cứng vật lý trong data center

### Cách tạo Máy ảo

**Cơ sở hạ tầng vật lý:**
- Phần cứng/server vật lý ở tầng dưới cùng
- Nhà cung cấp cloud sử dụng công nghệ **Hypervisor**
- Một server vật lý được chia thành nhiều VM (VM1, VM2, VM3)

**Phân phối tài nguyên:**
- Tài nguyên vật lý (RAM, ổ cứng) được phân phối ảo
- Ví dụ: Server 64GB RAM, 4TB ổ cứng chia sẻ cho nhiều VM
- Mỗi VM có thể có hệ điều hành khác nhau:
  - VM1: Windows OS
  - VM2: Linux OS
  - VM3: Mac OS

### Triển khai Microservices với Máy ảo

**Quy trình cài đặt:**
1. Tạo máy ảo với guest OS
2. Cài đặt thủ công các binary và thư viện cần thiết (JDK, web server, Maven)
3. Triển khai microservice
4. Truy cập qua địa chỉ IP công khai

**Ví dụ kịch bản:**
- AccountService → VM1
- LoanService → VM2
- CardService → VM3

## Vấn đề với Máy ảo cho Microservices

### 1. **Vấn đề về Khả năng mở rộng**
- 100 microservices = 100 VM? Không khả thi!
- Chi phí cloud cao
- Lãng phí tài nguyên (VM 16GB RAM cho microservice nhỏ)

### 2. **Xung đột phụ thuộc**
Khi triển khai nhiều service trong một VM:
- AccountService cần Java 8
- LoanService cần Java 17
- CardService cần Python
- **Kết quả:** Các phụ thuộc không tương thích trong cùng môi trường

### 3. **Rủi ro về tính sẵn sàng**
- Khởi động lại VM ảnh hưởng tất cả các service
- Không có rủi ro downtime chấp nhận được

### 4. **Mở rộng chậm**
Mở rộng từ 1 lên 3 instance yêu cầu:
- Tạo VM mới
- Cài đặt guest OS
- Cài đặt binary và thư viện
- **Tổng thời gian:** ~15 phút
- Đến lúc đó, traffic có thể đã bình thường
- Thu nhỏ quy mô cũng mất 5-10 phút

## Container: Giải pháp

### Kiến trúc Container

**Các tầng cơ sở hạ tầng:**
1. **Phần cứng vật lý** (server)
2. **Hệ điều hành chủ** (Windows/Linux/Mac)
3. **Container Engine** (Docker)
4. **Containers** (AccountService, LoanService, CardService)

### Ưu điểm chính của Container

#### 1. **Nhẹ**
- Không cần hệ điều hành guest riêng
- Chia sẻ hệ điều hành chủ
- Thao tác nhanh (giây, không phải phút):
  - Tạo container
  - Xóa container
  - Khởi động lại container

#### 2. **Môi trường cô lập**
Nhiều container trên cùng server, mỗi container có:
- Container1: Java 8
- Container2: Java 17
- Container3: Python
- Mạng ảo cô lập
- Các container không biết về môi trường của nhau

#### 3. **Tự chứa**
- Tất cả phụ thuộc được đóng gói cùng nhau
- JDK + thư viện Spring Boot được bao gồm
- Không cần cài đặt thủ công

#### 4. **Tính di động**
- Đưa container đóng gói đến bất kỳ môi trường nào
- Chuyển đổi thành container đang chạy với một lệnh duy nhất
- Không cần:
  - Cài đặt Java
  - Download thư viện Spring Boot
  - Cấu hình thủ công

#### 5. **Cô lập tài nguyên**
Mỗi container có riêng:
- Mạng
- Tài nguyên
- Bộ nhớ
- Lưu trữ
- Cô lập trừ khi được cho phép rõ ràng

#### 6. **Triển khai dễ dàng**
- Các thành phần nhẹ
- Khởi động lại/tạo/xóa nhanh chóng
- Downtime tối thiểu

## Máy ảo so với Container: Tóm tắt

| Khía cạnh | Máy ảo | Container |
|-----------|--------|-----------|
| **Guest OS** | Bắt buộc | Không bắt buộc (chia sẻ host OS) |
| **Kích thước** | Nặng (GBs) | Nhẹ (MBs) |
| **Thời gian khởi động** | Phút | Giây |
| **Phân phối tài nguyên** | Hypervisor | Container Engine (Docker) |
| **Cô lập** | Cô lập toàn bộ OS | Cô lập cấp độ process |
| **Tính di động** | Phức tạp | Đơn giản (đóng gói) |
| **Khả năng mở rộng** | Chậm (15 phút) | Nhanh (giây) |
| **Triển khai** | Cần cài đặt thủ công | Một lệnh duy nhất |

## Kết luận

**Điểm chính:** Khi triển khai microservices, nói KHÔNG với máy ảo và nói CÓ với container!

Container giải quyết các thách thức chính của triển khai dựa trên VM:
- ✅ Nhẹ và nhanh
- ✅ Môi trường cô lập
- ✅ Dễ dàng di chuyển
- ✅ Mở rộng nhanh chóng
- ✅ Lãng phí tài nguyên tối thiểu

Trong các bài giảng tiếp theo, chúng ta sẽ thấy những lợi ích này trong thực tế khi chúng ta chuyển đổi microservices của mình thành Docker container.

---

**Bước tiếp theo:** Chuyển đổi microservices thành Docker container và trải nghiệm trực tiếp các ưu điểm.




FILE: 32-kien-truc-va-cac-thanh-phan-docker.md


# Kiến Trúc và Các Thành Phần Docker

## Tổng Quan

Bài giảng này giải thích các thành phần quan trọng có sẵn trong Docker và kiến trúc nội bộ của nó. Hiểu về kiến trúc Docker là rất quan trọng để container hóa các microservices được xây dựng bằng Spring Boot và Java.

## Các Thành Phần Docker

### 1. Docker Client

Docker client là giao diện chính để tương tác với Docker. Khi bạn cài đặt Docker trên bất kỳ hệ thống nào, bạn sẽ nhận được cả Docker client và Docker server.

Docker client được sử dụng để đưa ra các chỉ thị cho Docker server về cách container hóa ứng dụng.

#### Các Thành Phần của Docker Client:

**Docker CLI (Command Line Interface)**
- Cách tiếp cận phổ biến nhất để đưa ra lệnh cho Docker server
- Cho phép bạn đưa ra lệnh trực tiếp từ terminal hoặc command line
- Tương tự như GitHub CLI hoặc các công cụ CLI khác được cung cấp bởi nhiều sản phẩm
- Đây là cách tiếp cận chúng ta sẽ sử dụng trong khóa học này

**Docker Remote API**
- Một cách thay thế để đưa ra lệnh cho Docker server bằng cách sử dụng APIs
- Có thể được sử dụng để thực thi các lệnh như chạy một Docker container từ Docker image
- Cung cấp quyền truy cập theo chương trình vào chức năng Docker

### 2. Docker Server (Docker Host)

Docker server, còn được gọi là Docker host, là thành phần cốt lõi thực hiện công việc thực tế.

**Lưu Ý Quan Trọng:**
- Cả Docker client và Docker server đều được cài đặt trên cùng một hệ thống (máy local của bạn)
- Đừng nhầm lẫn với việc cài đặt trên server từ xa

#### Docker Daemon

Docker server chạy một tiến trình Docker daemon mà:
- Chạy liên tục trong nền
- Chấp nhận các lệnh từ client (CLI)
- Xử lý các chỉ thị để tạo Docker images và containers

#### Docker Images

Docker image là một đại diện được đóng gói của ứng dụng của bạn bao gồm:
- Tất cả các dependencies cần thiết
- Cài đặt cấu hình
- Phiên bản Java và runtime
- Mã nguồn ứng dụng

Khi bạn cung cấp các chỉ thị cho Docker server (dependencies, phiên bản Java, cấu hình), nó sẽ chuyển đổi ứng dụng Spring Boot, ứng dụng Maven hoặc microservice của bạn thành một Docker image.

#### Docker Containers

Containers là các instance đang chạy của Docker images:
- Không thể tạo được nếu không có Docker image
- Đại diện cho ứng dụng web hoặc microservice của bạn ở trạng thái đang chạy
- Khi container đang chạy, bạn có thể truy cập các REST APIs và logic nghiệp vụ microservice thông qua endpoint URL bằng cách sử dụng đúng số port và đường dẫn API

**Lưu Trữ:**
Tất cả images và containers được lưu trữ bên trong Docker server của bạn.

### 3. Docker Registry

Docker Registry là một hệ thống repository để lưu trữ và phân phối Docker images.

#### Docker Hub

Docker Hub là registry chính thức được cung cấp bởi Docker:
- Lưu trữ tất cả Docker images của bạn
- Làm cho images có sẵn để sử dụng công khai
- Bảo vệ images bằng xác thực cho quyền truy cập riêng tư
- Tương tự như cách GitHub lưu trữ mã nguồn

#### Private Registries

Nhiều nhà cung cấp đám mây và nền tảng cung cấp private registries:
- **GitHub** - GitHub Container Registry
- **AWS** - Amazon Elastic Container Registry (ECR)
- **GCP** - Google Container Registry
- **Azure** - Azure Container Registry

**Trường Hợp Sử Dụng:**
Nếu tổ chức của bạn sử dụng rộng rãi AWS, việc đẩy Docker images lên private registry của AWS (ECR) là hợp lý, từ đó tất cả các triển khai microservice sẽ diễn ra.

**Trong Khóa Học Này:**
Chúng ta sẽ sử dụng Docker Hub để lưu trữ tất cả Docker images.

## Quy Trình Làm Việc Docker

Đây là quy trình điển hình khi làm việc với Docker:

### Bước 1: Đưa Ra Chỉ Thị
Đưa ra chỉ thị cho Docker server bằng cách sử dụng Docker client (CLI), chẳng hạn như "chạy một container từ một Docker image."

### Bước 2: Xác Thực Image
Docker server xác thực xem Docker image có sẵn trong hệ thống local của bạn hay không.

### Bước 3: Truy Xuất Image
Nếu image không có sẵn locally, Docker sẽ lấy nó từ một repository từ xa như Docker Hub.

### Bước 4: Tạo Container
Khi Docker image đã được kéo về hệ thống local của bạn, một container được tạo bởi Docker server bằng cách sử dụng image đó.

### Bước 5: Ứng Dụng Sẵn Sàng
Khi container đang chạy, ứng dụng của bạn đã sẵn sàng để sử dụng.

## Ví Dụ Thực Tế: MySQL với Docker

**Cách Tiếp Cận Truyền Thống:**
1. Truy cập website MySQL
2. Tải xuống gói cài đặt MySQL
3. Cài đặt trên hệ thống của bạn
4. Cấu hình cơ sở dữ liệu

Đây là một quá trình rườm rà và dài dòng.

**Cách Tiếp Cận Docker:**
1. Kéo MySQL image từ Docker Hub
2. Chạy một container từ MySQL image
3. MySQL server hiện đang chạy trên hệ thống của bạn

Điều này đơn giản hóa đáng kể quá trình thiết lập.

## Quy Trình Triển Khai

Sau khi bạn đã phát triển và kiểm tra microservice của mình locally:

1. **Tạo** một Docker image cho microservice của bạn
2. **Kiểm tra** image bằng cách tạo và chạy một container
3. **Xác minh** rằng mọi thứ hoạt động chính xác
4. **Đẩy** Docker image lên một repository từ xa (Docker Hub)
5. **Triển khai** từ repository đến môi trường dev, staging hoặc production

Quy trình này tương tự như cách bạn lưu trữ mã Java trong repositories GitHub - Docker images được lưu trữ trong Docker registries cho mục đích triển khai.

## Tóm Tắt

Kiến trúc Docker bao gồm ba thành phần chính:

1. **Docker Client** - Giao diện để đưa ra lệnh (CLI hoặc Remote API)
2. **Docker Server** - Công cụ cốt lõi tạo và quản lý images và containers
3. **Docker Registry** - Hệ thống repository để lưu trữ và phân phối images

Hiểu kiến trúc này là điều cần thiết cho:
- Container hóa các Spring Boot microservices
- Quản lý triển khai ứng dụng
- Đơn giản hóa môi trường phát triển và production
- Đảm bảo tính nhất quán trên các môi trường khác nhau

## Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ đề cập đến cách cài đặt Docker trên hệ thống local của bạn và bắt đầu tạo Docker images cho các microservices của bạn.

---

**Điểm Chính Cần Nhớ:**
- Docker Client cung cấp giao diện CLI và API cho các lệnh
- Docker Server (Docker Host) quản lý images và containers thông qua Docker daemon
- Docker Registry (Docker Hub hoặc private registries) lưu trữ và phân phối images
- Containers là các instance đang chạy của images
- Docker đơn giản hóa triển khai và tính nhất quán của môi trường




FILE: 33-cai-dat-docker-desktop.md


# Cài Đặt Docker Desktop

## Tổng Quan

Bài giảng này cung cấp hướng dẫn từng bước để cài đặt Docker Desktop trên hệ thống local của bạn. Việc cài đặt Docker là điều cần thiết để thực hành các khái niệm microservice và container hóa ứng dụng Spring Boot.

## Yêu Cầu Hệ Thống

Trước khi cài đặt Docker, hãy đảm bảo hệ thống của bạn đáp ứng các yêu cầu sau:

- **RAM tối thiểu:** 4 GB RAM hệ thống
- **Bộ xử lý:** Bộ xử lý 64-bit
- **Hệ điều hành được hỗ trợ:**
  - Apple macOS
  - Microsoft Windows
  - Linux

## Các Bước Cài Đặt

### Bước 1: Truy Cập Website Docker

Truy cập [docker.com](https://docker.com) trên trình duyệt web của bạn.

### Bước 2: Tải Docker Desktop

1. Trên trang chủ, bạn sẽ thấy tùy chọn "Download Docker Desktop"
2. Website tự động phát hiện hệ điều hành của bạn (Mac, Windows hoặc Linux)
3. Chọn phiên bản phù hợp cho hệ điều hành của bạn
4. Nhấp vào "Download Docker Desktop"

### Bước 3: Cài Đặt Docker

1. Sau khi tải xuống hoàn tất, tìm file cài đặt
2. Nhấp đúp vào file cài đặt
3. Làm theo trình hướng dẫn cài đặt (nhấp Next → Next → Next)
4. Hoàn tất quá trình cài đặt

### Bước 4: Xác Minh Cài Đặt

Quá trình cài đặt rất đơn giản và sẽ hoàn tất mà không gặp vấn đề gì. Nếu bạn cần thêm trợ giúp, hãy tham khảo tài liệu chính thức.

## Tài Liệu và Hỗ Trợ Docker

Nếu bạn gặp bất kỳ thách thức nào trong quá trình cài đặt:

### Tài Liệu Chính Thức

1. Nhấp vào "Get Started" trên website Docker
2. Chọn "Learn how to install Docker"
3. Điều hướng đến [website tài liệu Docker](https://docs.docker.com)
4. Chọn hệ điều hành của bạn:
   - Install Docker Desktop on Mac
   - Install Docker Desktop on Windows
   - Install Docker Desktop on Linux

### Tài Nguyên Khắc Phục Sự Cố

Nếu bạn gặp vấn đề cài đặt, có nhiều nguồn tài nguyên có sẵn:

1. **Docker Troubleshooting Guide:** Kiểm tra tài liệu khắc phục sự cố chính thức cho các vấn đề phổ biến
2. **Stack Overflow:** Tìm kiếm các vấn đề cài đặt Docker trên Stack Overflow
3. **Docker Community:** Truy cập trợ giúp từ diễn đàn cộng đồng Docker
4. **Course Q&A:** Đăng câu hỏi trong phần Q&A của Udemy

**Quan trọng:** Đừng nản lòng - quá trình cài đặt được thiết kế để đơn giản và dễ dàng!

## Tạo Tài Khoản Docker Hub

### Bước 1: Đăng Ký

1. Sau khi cài đặt Docker Desktop, nhấp vào nút "Sign In"
2. Bạn sẽ được chuyển hướng đến [hub.docker.com](https://hub.docker.com)
3. Tạo tài khoản mới nếu bạn chưa có
4. Chọn tên người dùng và mật khẩu
5. **Không cần thẻ tín dụng** cho gói miễn phí

### Bước 2: Ghi Nhớ Tên Người Dùng

Tên người dùng Docker Hub của bạn rất quan trọng - bạn sẽ cần nó trong các bài giảng sắp tới. Ví dụ:
- Tên người dùng: `eazybytes`

### Bước 3: Chọn Gói

Docker Hub cung cấp nhiều gói:

#### Gói Personal (Miễn phí - $0)
- **Repositories công khai không giới hạn**
- Hoàn hảo cho khóa học này
- Lý tưởng cho việc học và các dự án cá nhân
- Không cần thanh toán

#### Gói Trả Phí
- **Gói Pro, Team và Business** có sẵn
- Bắt buộc cho repositories riêng tư
- Được sử dụng trong môi trường production
- Các tổ chức thường cung cấp những gói này cho các dự án thực tế

**Cho khóa học này:** Gói Personal (miễn phí) là đủ. Tất cả Docker images sẽ được lưu trữ trong repositories công khai.

## Tính Năng Docker Hub

### Official Images

Docker Hub lưu trữ các images chính thức từ các sản phẩm và nền tảng lớn:
- **Python:** Images runtime Python chính thức
- **MySQL:** Hơn 1 tỷ lượt tải xuống
- **PostgreSQL:** Image cơ sở dữ liệu phổ biến
- **Ubuntu:** Images Ubuntu Linux chính thức
- Và nhiều hơn nữa...

### Tìm Kiếm Images

**Ví dụ: Tìm MySQL Image**

1. Tìm kiếm "MySQL" trong Docker Hub
2. Tìm thẻ "Docker Official Image"
3. Lưu ý số lượt tải xuống (ví dụ: 1 tỷ+ lượt tải xuống)
4. Sử dụng lệnh được cung cấp để pull image:
   ```bash
   docker pull mysql
   ```

### Sử Dụng Docker Hub

Docker Hub phục vụ hai mục đích chính:

1. **Lưu Trữ Images Của Bạn:** Tải lên Docker images của riêng bạn (công khai hoặc riêng tư)
2. **Lấy Images Khác:** Tải xuống và sử dụng images chính thức từ các sản phẩm, cơ sở dữ liệu, servers và ngôn ngữ lập trình

## Ứng Dụng Docker Desktop

### Truy Cập Docker Desktop

Sau khi cài đặt và đăng nhập:

1. Nhấp vào biểu tượng Docker trong khay hệ thống (Windows/Linux) hoặc thanh menu (Mac)
2. Nhấp vào "Dashboard" để mở ứng dụng Docker Desktop

### Tính Năng Docker Dashboard

Docker Desktop dashboard cung cấp quyền truy cập vào:

- **Images:** Xem tất cả Docker images local
- **Containers:** Quản lý containers đang chạy và đã dừng
- **Volumes:** Quản lý Docker volumes
- **Settings:** Cấu hình các tùy chọn Docker

### Đăng Nhập

Nếu bạn chưa đăng nhập:

1. Nhấp vào nút ở góc trên bên phải của Docker Desktop
2. Nhập thông tin đăng nhập Docker Hub của bạn (tên người dùng và mật khẩu)
3. Docker local của bạn sẽ kết nối với repository Docker Hub của bạn

Kết nối này cho phép bạn:
- Đẩy images lên Docker Hub
- Kéo private images từ repositories của bạn
- Đồng bộ hóa môi trường Docker local và remote của bạn

## Xác Minh Cài Đặt

### Sử Dụng Terminal/Command Line

Bạn có thể xác nhận cài đặt Docker thành công bằng cách chạy lệnh trong terminal của bạn.

#### Kiểm Tra Phiên Bản Docker

Chạy lệnh sau:
```bash
docker version
```

**Kết quả mong đợi:**
- **Thông tin Client:**
  - Chi tiết phiên bản
  - Hệ điều hành (ví dụ: Darwin cho Mac, Windows, Linux)
  
- **Thông tin Server:**
  - Chi tiết phiên bản
  - Hệ điều hành (thường là Linux)

### Hiểu Về Kiến Trúc

**Lưu ý quan trọng:** Bất kể hệ điều hành host của bạn (Mac, Windows), Docker nội bộ tạo một máy ảo Linux nhỏ và nhẹ nơi Docker server chạy.

**Ví dụ:**
- **Host OS:** macOS (Darwin)
- **Docker Server OS:** Linux (chạy trong một VM nhẹ)

Kiến trúc này đảm bảo hành vi nhất quán trên tất cả các nền tảng.

## Thực Hành Tốt Nhất

### Trước Khi Tiếp Tục

1. ✅ **Cài đặt Docker Desktop** trên hệ thống local của bạn
2. ✅ **Tạo tài khoản Docker Hub** với tên người dùng dễ nhớ
3. ✅ **Đăng nhập vào Docker Desktop** với thông tin đăng nhập của bạn
4. ✅ **Xác minh cài đặt** bằng lệnh `docker version`
5. ✅ **Làm quen với** Docker Dashboard

### Lời Nhắc Quan Trọng

- **Thực hành là Cần thiết:** Nếu không cài đặt Docker, bạn không thể thực hành các khái niệm microservice được đề cập trong các bài giảng sắp tới
- **Gói Miễn Phí Là Đủ:** Gói Personal (miễn phí) cung cấp mọi thứ cần thiết cho khóa học này
- **Hỗ Trợ Cộng Đồng:** Trợ giúp rộng rãi có sẵn từ cộng đồng Docker nếu bạn gặp vấn đề
- **Tài Liệu:** Tài liệu Docker chính thức cung cấp hướng dẫn cài đặt chi tiết cho tất cả các nền tảng

## Vấn Đề Phổ Biến và Giải Pháp

### Cài Đặt Thất Bại

1. Kiểm tra yêu cầu hệ thống (4GB RAM, bộ xử lý 64-bit)
2. Đảm bảo bạn có quyền administrator/root
3. Kiểm tra phần mềm xung đột
4. Tham khảo hướng dẫn khắc phục sự cố

### Không Thể Đăng Nhập Docker Hub

1. Xác minh tên người dùng và mật khẩu của bạn
2. Kiểm tra kết nối internet
3. Thử đặt lại mật khẩu trên hub.docker.com

### Lệnh Docker Version Không Tìm Thấy

1. Khởi động lại terminal/command prompt của bạn
2. Kiểm tra xem Docker Desktop có đang chạy không
3. Cài đặt lại Docker nếu cần thiết

## Bước Tiếp Theo

Với Docker được cài đặt thành công:

1. Bạn sẽ học các lệnh và thao tác Docker
2. Bạn sẽ tạo Docker images cho Spring Boot microservices
3. Bạn sẽ chạy containers từ Docker images
4. Bạn sẽ đẩy images lên Docker Hub
5. Bạn sẽ triển khai các microservices được container hóa

## Tóm Tắt

Các điểm chính được đề cập trong bài giảng này:

- Cài đặt Docker Desktop rất đơn giản và có tài liệu đầy đủ
- Docker Hub cung cấp gói Personal miễn phí cho repositories công khai
- Docker Desktop dashboard quản lý images, containers và volumes
- Docker nội bộ sử dụng Linux cho server, bất kể host OS
- Images chính thức từ các sản phẩm lớn có sẵn trên Docker Hub
- Hỗ trợ cộng đồng rất rộng rãi để khắc phục sự cố

**Cài đặt Docker của bạn giờ đây sẽ hoàn tất và được xác minh!**

## Tham Khảo Nhanh

### URLs Quan Trọng
- Website Docker: [docker.com](https://docker.com)
- Docker Hub: [hub.docker.com](https://hub.docker.com)
- Tài liệu Docker: [docs.docker.com](https://docs.docker.com)

### Lệnh Chính
```bash
# Kiểm tra phiên bản Docker
docker version

# Pull một image từ Docker Hub
docker pull <image-name>

# Xem images local
docker images

# Xem containers đang chạy
docker ps
```

---

**Sẵn Sàng Để Thực Hành:** Với Docker được cài đặt và xác minh, bạn hiện đã sẵn sàng để khám phá việc container hóa microservices và tìm hiểu các lệnh Docker trong các bài giảng sắp tới!




FILE: 34-tong-quan-cac-phuong-phap-tao-docker-image.md


# Các Phương Pháp Tạo Docker Image cho Microservices

## Tổng Quan

Việc chuyển đổi các microservices thành Docker images giúp chúng trở nên nhẹ hơn và phù hợp để vượt qua các thách thức liên quan đến triển khai, tính di động và khả năng mở rộng. Khi tạo Docker image từ một ứng dụng web hoặc ứng dụng Spring Boot, có ba phương pháp thường được sử dụng trong ngành.

Phần này sẽ khám phá cả ba phương pháp, và đến cuối phần, chúng ta sẽ chọn một phương pháp để tiếp tục sử dụng trong suốt phần còn lại của khóa học.

## Ba Phương Pháp Phổ Biến

### 1. Phương Pháp Dockerfile

**Phương pháp Dockerfile** là phương pháp cơ bản và truyền thống nhất để tạo Docker images.

**Cách hoạt động:**
- Viết một tập hợp các chỉ thị trong Dockerfile
- Docker server tạo Docker image dựa trên các chỉ thị này
- Yêu cầu học cú pháp Docker và các best practices

**Ứng dụng trong khóa học:**
- Chúng ta sẽ sử dụng phương pháp này để tạo Docker image cho **Accounts Microservice**

**Đặc điểm:**
- Phương pháp cơ bản nhất
- Có đường cong học tập đối với cú pháp Docker
- Cung cấp khả năng kiểm soát chi tiết quá trình tạo image

---

### 2. Phương Pháp Buildpacks

**Buildpacks** đơn giản hóa quá trình containerization bằng cách loại bỏ việc phải viết Docker files thủ công.

**Cách hoạt động:**
- Tạo Docker image bằng một lệnh Maven duy nhất
- Maven sử dụng khái niệm Buildpacks ở hậu trường
- Không cần cung cấp chỉ thị thủ công cho Docker server

**Bối cảnh:**
- Dự án được khởi xướng và phát triển bởi Heroku và Pivotal
- Dựa trên các best practices học được qua nhiều năm
- Đơn giản hóa việc containerization ứng dụng web

**Ứng dụng trong khóa học:**
- Chúng ta sẽ sử dụng phương pháp này để tạo Docker image cho **Loans Microservice**

**Ưu điểm:**
- Không cần viết Dockerfiles cấp thấp
- Quá trình tạo image tự động
- Xây dựng dựa trên các best practices của ngành

---

### 3. Phương Pháp Google Jib

**Google Jib** là một công cụ Java được phát triển bởi Google và sau đó được mã nguồn mở.

**Cách hoạt động:**
- Sử dụng lệnh Maven plugin để tạo Docker images
- Hoạt động với bất kỳ ứng dụng Java nào
- Không cần viết Dockerfiles cấp thấp

**Ứng dụng trong khóa học:**
- Chúng ta sẽ sử dụng phương pháp này để tạo Docker image cho **Cards Microservice**

**Ưu điểm:**
- Dễ dàng tạo Docker image cho ứng dụng Java
- Không yêu cầu Dockerfile
- Tích hợp liền mạch với quy trình build Maven

---

## Sơ Đồ Ánh Xạ Microservice-Phương Pháp

| Microservice | Phương Pháp Tạo Docker Image |
|--------------|------------------------------|
| Accounts     | Dockerfile                   |
| Loans        | Buildpacks                   |
| Cards        | Google Jib                   |

**Lưu ý:** Ba microservices (Accounts, Loans và Cards) được phát triển như một phần của ứng dụng ngân hàng (Bank Application). Việc ánh xạ mỗi phương pháp với một microservice hoàn toàn trùng hợp nhưng thuận tiện cho việc trình diễn cả ba phương pháp.

## Tiếp Theo Là Gì

Mỗi phương pháp có những ưu điểm và nhược điểm riêng, sẽ được thảo luận chi tiết khi chúng ta khám phá từng phương pháp. Đến cuối phần này, chúng ta sẽ chọn một phương pháp để tuân theo trong suốt phần còn lại của khóa học.

---

## Tóm Tắt

- **Ba phương pháp chính** tồn tại để tạo Docker images từ ứng dụng Spring Boot
- **Dockerfile**: Phương pháp truyền thống, thủ công với khả năng kiểm soát chi tiết
- **Buildpacks**: Phương pháp tự động sử dụng Maven, không cần Dockerfile
- **Google Jib**: Công cụ tối ưu hóa cho Java với tích hợp Maven plugin
- Chúng ta sẽ khám phá cả ba phương pháp trước khi chọn một cho phần còn lại của khóa học




FILE: 35-tao-dockerfile-cho-accounts-microservice.md


# Tạo Dockerfile cho Accounts Microservice

## Tổng quan
Trong bài học này, chúng ta sẽ viết Dockerfile cho Accounts Microservice để cho phép đóng gói ứng dụng bằng Docker.

## Điều kiện tiên quyết
Trước khi tạo Dockerfile:
1. Dừng instance đang chạy của Accounts Microservice bằng cách nhấn `Ctrl + C`
2. Đảm bảo Docker đang chạy trên hệ thống của bạn
   - **Mac**: Biểu tượng Docker xuất hiện ở thanh menu trên cùng
   - **Windows**: Biểu tượng Docker xuất hiện ở góc dưới bên phải
3. Xác minh Docker đang chạy bằng cách mở Docker Dashboard
   - Click vào biểu tượng Docker và chọn "Dashboard"
   - Bạn sẽ thấy containers và images (có thể trống nếu đây là lần đầu tiên)

## Tạo Dockerfile

### Bước 1: Tạo file Dockerfile
1. Nhấp chuột phải vào thư mục Accounts Microservice của bạn
2. Chọn "New File"
3. Đặt tên chính xác là `Dockerfile` (không có phần mở rộng như .txt, .xml, hoặc .yml)
4. Docker sẽ tìm kiếm đúng tên file này

### Bước 2: Viết các lệnh trong Dockerfile

#### Base Image (FROM)
```dockerfile
# Bắt đầu với base image chứa Java runtime
FROM openjdk:17-jdk-slim
```

**Giải thích:**
- Lệnh `FROM` cho Docker biết rằng image của chúng ta phụ thuộc vào một base image khác
- Chúng ta sử dụng `openjdk:17-jdk-slim` làm base image
- Định dạng: `tênImage:tênTag`
  - Tên image: `openjdk`
  - Tag: `17-jdk-slim` (tương đương với phiên bản Java)

**Tìm Docker Images:**
- Truy cập [Docker Hub](https://hub.docker.com/)
- Tìm kiếm "openjdk"
- Click vào Docker image chính thức
- Duyệt các tags có sẵn trong phần "Tags"
- Ví dụ:
  - `22-slim-bullseye` cho Java 22
  - `17-jdk-slim` cho Java 17

#### Thông tin Maintainer
```dockerfile
# Thông tin về người duy trì image
MAINTAINER easybytes.com
```

**Giải thích:**
- Từ khóa `MAINTAINER` chỉ định người duy trì Docker image
- Cần có khoảng trắng giữa `MAINTAINER` và thông tin người duy trì

#### Sao chép Application JAR
```dockerfile
# Thêm file jar của ứng dụng vào image
COPY target/accounts-0.0.1-SNAPSHOT.jar accounts-0.0.1-SNAPSHOT.jar
```

**Giải thích:**
- Lệnh `COPY` sao chép files từ máy local của bạn vào Docker image
- Cú pháp: `COPY <nguồn> <đích>`
- Nguồn: `target/accounts-0.0.1-SNAPSHOT.jar` (đường dẫn tương đối so với vị trí Dockerfile)
- Đích: `accounts-0.0.1-SNAPSHOT.jar` (thư mục root của Docker image)
- File JAR chứa tất cả business code và các thư viện Spring Boot

#### Lệnh Entry Point
```dockerfile
# Thực thi ứng dụng
ENTRYPOINT ["java", "-jar", "accounts-0.0.1-SNAPSHOT.jar"]
```

**Giải thích:**
- Lệnh `ENTRYPOINT` định nghĩa những gì sẽ được thực thi khi container khởi động
- Các lệnh được cung cấp dưới dạng chuỗi ngăn cách bằng dấu phẩy trong dấu ngoặc vuông
- Mỗi phần của lệnh nằm trong dấu ngoặc kép do có khoảng trắng
- Tương đương với việc chạy: `java -jar accounts-0.0.1-SNAPSHOT.jar`
- Không cần tiền tố `target/` vì JAR nằm ở thư mục root của Docker image

## Dockerfile hoàn chỉnh

```dockerfile
# Bắt đầu với base image chứa Java runtime
FROM openjdk:17-jdk-slim

# Thông tin về người duy trì image
MAINTAINER easybytes.com

# Thêm file jar của ứng dụng vào image
COPY target/accounts-0.0.1-SNAPSHOT.jar accounts-0.0.1-SNAPSHOT.jar

# Thực thi ứng dụng
ENTRYPOINT ["java", "-jar", "accounts-0.0.1-SNAPSHOT.jar"]
```

## Các phụ thuộc của Docker Image

Khi tạo Docker image, nó đóng gói tất cả các phụ thuộc:
1. **Phụ thuộc cơ bản**: OpenJDK (Java Runtime Environment)
2. **Phụ thuộc ứng dụng**: accounts-0.0.1-SNAPSHOT.jar
   - Chứa tất cả business logic
   - Bao gồm các thư viện Spring Boot
   - Được đóng gói từ máy local của bạn

## Bước tiếp theo

Trong bài học tiếp theo, chúng ta sẽ sử dụng Dockerfile này để tạo Docker image cho Accounts Microservice.

## Những điểm chính cần nhớ

- Dockerfile phải được đặt tên chính xác là `Dockerfile` không có phần mở rộng
- `FROM` import một base image (Java runtime trong trường hợp này)
- `MAINTAINER` ghi lại thông tin người duy trì image
- `COPY` chuyển các artifacts của ứng dụng vào image
- `ENTRYPOINT` định nghĩa lệnh khởi động container
- Docker images đóng gói tất cả các phụ thuộc trong một định dạng di động

---

**Tác giả:** easybytes.com




FILE: 36-xay-dung-docker-images-cho-accounts-microservice.md


# Xây Dựng Docker Images cho Accounts Microservice

## Tổng Quan

Hướng dẫn này trình bày cách xây dựng Docker image cho accounts microservice sử dụng Dockerfile. Chúng ta sẽ tìm hiểu quy trình tạo Docker image và kiểm tra nội dung của nó.

## Yêu Cầu Trước Khi Bắt Đầu

Trước khi xây dựng Docker images, hãy đảm bảo:
- Docker đã được cài đặt trên hệ thống local
- Docker server đang chạy
- Bạn đã có tài khoản Docker Hub

## Bước 1: Xác Minh Cài Đặt Docker

Đầu tiên, xác minh Docker đã được cài đặt và chạy đúng cách bằng cách thực thi lệnh version:

```bash
docker version
```

Lệnh này hiển thị cả phiên bản client và server của Docker đang chạy trên hệ thống, xác nhận rằng Docker đã được thiết lập đúng cách.

## Bước 2: Xây Dựng Docker Image

### Cấu Trúc Lệnh Docker Build

Lệnh cơ bản để xây dựng Docker image là:

```bash
docker build . -t <docker-username>/<image-name>:<tag>
```

### Các Thành Phần Lệnh:

- `docker build .` - Xây dựng image từ Dockerfile trong thư mục hiện tại
- `-t` - Flag để chỉ định tag/tên cho image
- `<docker-username>` - Tên người dùng Docker Hub của bạn
- `<image-name>` - Tên microservice của bạn (ví dụ: accounts)
- `<tag>` - Phiên bản hoặc tên tag (ví dụ: s4)

### Ví Dụ Lệnh:

```bash
docker build . -t eazybytes/accounts:s4
```

### Lưu Ý Quan Trọng:

1. **Vị Trí Dockerfile**: Nếu Dockerfile nằm trong thư mục hiện tại, sử dụng `.` (dấu chấm). Nếu không, cung cấp đường dẫn đầy đủ đến vị trí Dockerfile.

2. **Tên Người Dùng Docker**: Luôn bao gồm tên người dùng Docker Hub của bạn như một tiền tố. Điều này rất quan trọng để push images lên Docker Hub sau này.

3. **Quy Ước Đặt Tên**: Tuân theo định dạng: `username/service-name:version`
   - Ví dụ: `eazybytes/accounts:s4`
   - Trong đó `eazybytes` là tên người dùng Docker Hub
   - `accounts` là tên microservice
   - `s4` chỉ section 4 hoặc phiên bản 4

## Bước 3: Hiểu Quy Trình Build

Khi bạn thực thi lệnh build, Docker server:

1. **Tải Base Image**: Đầu tiên, nó tải base image (ví dụ: `openjdk:17-slim`) từ repository từ xa (docker.io library)

2. **Thực Hiện Các Chỉ Thị**: Sau đó thực thi tuần tự từng instruction trong Dockerfile

3. **Tạo Các Layers**: Mỗi instruction tạo một layer mới trong Docker image

### Ví Dụ Output Khi Build:

Quá trình Docker build sẽ hiển thị:
- Tải base image (openjdk17-slim)
- Sao chép accounts JAR file từ thư mục target local
- Tạo image cuối cùng với tên `docker.io/eazybytes/accounts:s4`

## Bước 4: Liệt Kê Docker Images

Sau khi build, xác minh image đã được tạo:

```bash
docker images
```

Lệnh này liệt kê tất cả Docker images trên hệ thống local. Tìm kiếm image vừa tạo:

**Ví Dụ Output:**
```
REPOSITORY            TAG    IMAGE ID       CREATED          SIZE
eazybytes/accounts    s4     abc123def456   1 minute ago     456MB
```

## Bước 5: Kiểm Tra Docker Image

Để xem thông tin chi tiết về Docker image:

```bash
docker inspect <image-id>
```

**Mẹo**: Bạn không cần gõ toàn bộ image ID. Chỉ cần sử dụng 3-4 ký tự đầu tiên.

Ví dụ:
```bash
docker inspect abc1
```

### Thông Tin Quan Trọng Từ Lệnh Inspect:

1. **Author/Maintainer**: Hiển thị ai đã tạo image (ví dụ: eazybytes.com)

2. **JAVA_HOME**: Tự động được set thành OpenJDK 17 dựa trên base image

3. **Entry Point**: Lệnh chạy khi container khởi động (ví dụ: `java -jar accounts.jar`)

4. **Operating System**: Linux (Docker sử dụng Linux namespaces và control groups)

5. **Layers**: Tất cả các layers tạo nên image của bạn

## Bước 6: Xem Image Trong Docker Desktop

Bạn cũng có thể khám phá image sử dụng giao diện Docker Desktop:

1. Mở Docker Desktop
2. Click vào phần "Images"
3. Tìm image của bạn (ví dụ: `accounts:s4`)
4. Click vào tên image để xem tất cả layers

Biểu diễn trực quan này hiển thị tất cả các layers có sẵn trong Docker image, xác nhận việc tạo thành công.

## Hiểu Kiến Trúc Docker

### Các Thành Phần Docker:

- **Docker CLI (Client)**: Giao diện dòng lệnh nơi bạn chạy các lệnh Docker
- **Docker Server (Daemon)**: Dịch vụ backend xử lý các lệnh Docker và quản lý images/containers
- **Docker Hub**: Repository từ xa để lưu trữ và chia sẻ Docker images

### Lưu Ý Quan Trọng:

Tất cả các lệnh Docker yêu cầu Docker server phải đang chạy. Nếu server không chạy, các lệnh như `docker build`, `docker images`, hoặc bất kỳ lệnh Docker nào khác sẽ không hoạt động.

## Các Bước Tiếp Theo

Bây giờ Docker image đã được tạo thành công, bạn đã sẵn sàng để:
1. Chuyển đổi Docker image thành Docker container
2. Test microservice đã được containerize
3. Push image lên Docker Hub để chia sẻ

## Tóm Tắt

Trong hướng dẫn này, bạn đã học:
- Cách xác minh cài đặt Docker
- Xây dựng Docker images sử dụng lệnh `docker build`
- Quy ước đặt tên đúng cho Docker images
- Liệt kê và kiểm tra Docker images
- Hiểu quy trình build và kiến trúc Docker
- Sử dụng Docker Desktop để xem chi tiết image

## Best Practices (Thực Hành Tốt Nhất)

1. Luôn bao gồm tên người dùng Docker Hub trong tên image
2. Sử dụng tags/versions có ý nghĩa cho images
3. Đảm bảo Docker server đang chạy trước khi thực thi lệnh
4. Thực hành các lệnh này nhiều lần để xây dựng sự quen thuộc
5. Giữ Dockerfile trong thư mục root của dự án microservice

---

**Lưu Ý**: Khi bạn thực hành các lệnh Docker này nhiều lần, chúng sẽ trở nên quen thuộc. Chi tiết bổ sung về các lệnh Docker sẽ được đề cập trong các bài giảng sắp tới.




FILE: 37-chay-docker-containers-tu-docker-images.md


# Chạy Docker Containers từ Docker Images

## Tổng Quan

Hướng dẫn này trình bày cách chạy Docker containers từ Docker images, quản lý vòng đời container, hiểu về port mapping, và tận dụng Docker để giải quyết các thách thức về triển khai, tính di động và khả năng mở rộng trong microservices.

## Tương Tự Lệnh Docker Run

Lệnh `docker run` tương tự như toán tử `new` trong Java:
- Giống như toán tử `new` tạo nhiều instances/objects của một class
- Lệnh `docker run` tạo nhiều containers từ một Docker image

## Chạy Container Đầu Tiên

### Lệnh Docker Run Cơ Bản

```bash
docker run -p 8080:8080 eazybytes/accounts:s4
```

### Các Thành Phần Lệnh:

- `docker run` - Lệnh để tạo và khởi động container
- `-p 8080:8080` - Port mapping (host:container)
- `eazybytes/accounts:s4` - Tên Docker image

### Hiểu Output:

Khi bạn thực thi lệnh này:
- Docker container khởi động thành công
- Accounts microservice khởi động ở port 8080
- Các log khởi động Spring Boot xuất hiện trong terminal
- Container chạy ở **attached mode** (chế độ foreground)

### Test Container:

Bạn có thể validate container đang chạy bằng các công cụ như Postman:
1. Gửi request đến `http://localhost:8080/api/create`
2. Bạn sẽ nhận được response thành công
3. Điều này xác nhận microservice đang chạy đúng

## Hiểu Về Port Mapping

### Tại Sao Cần Port Mapping

Mặc định, Docker containers khởi động trong **mạng cô lập** riêng của chúng. Các dịch vụ chạy bên trong containers không thể được truy cập từ mạng bên ngoài (như hệ thống local của bạn) nếu không có port mapping rõ ràng.

### Cú Pháp Port Mapping

```bash
docker run -p <host-port>:<container-port> <image-name>
```

### Phân Tích Port Mapping:

- **Port Đầu Tiên (Host Port)**: `8080` - Port được expose ra thế giới bên ngoài (hệ thống local của bạn)
- **Port Thứ Hai (Container Port)**: `8080` - Port nơi container chạy bên trong Docker network

**Ví Dụ**: `-p 8081:8080`
- Container chạy ở port 8080 bên trong Docker network
- Được expose ra hệ thống bên ngoài ở port 8081
- Các request bên ngoài phải sử dụng port 8081 để truy cập service

### Biểu Diễn Trực Quan:

```
Mạng Bên Ngoài (Hệ Thống Local)
         ↓ (Port 8081)
    Port Mapping
         ↓
Docker Network (Cô Lập)
         ↓ (Port 8080)
    Accounts Container
```

## Chạy Containers Ở Detached Mode

### Vấn Đề Với Attached Mode

Khi chạy ở attached mode (mặc định):
- Terminal bị block bởi các log của container
- Không thể chạy các lệnh khác
- Không tiện lợi cho developers

### Giải Pháp: Detached Mode

Sử dụng flag `-d` để chạy containers ở background:

```bash
docker run -d -p 8080:8080 eazybytes/accounts:s4
```

### Lợi Ích Của Detached Mode:

- Container chạy ở background
- Terminal vẫn sẵn sàng cho các lệnh khác
- Trả về container ID ngay lập tức
- Không hiển thị logs trong terminal (truy cập chúng riêng)

**Ví Dụ Output:**
```
abc123def456789... (container ID)
```

## Quản Lý Docker Containers

### Liệt Kê Các Container Đang Chạy

```bash
docker ps
```

**Output Mẫu:**
```
CONTAINER ID   IMAGE                    COMMAND                  CREATED          STATUS          PORTS                    NAMES
abc123def456   eazybytes/accounts:s4   "java -jar accounts…"   23 seconds ago   Up 22 seconds   0.0.0.0:8080->8080/tcp  random_name
```

**Thông Tin Hiển Thị:**
- Container ID
- Tên image
- Lệnh được sử dụng để chạy
- Thời gian tạo
- Port mapping
- Tên container (được tạo ngẫu nhiên)

### Liệt Kê Tất Cả Containers (Bao Gồm Đã Dừng)

```bash
docker ps -a
```

Lệnh này hiển thị tất cả containers bất kể trạng thái của chúng (running hoặc stopped).

### Khởi Động Container Đã Tồn Tại

```bash
docker start <container-id>
```

**Lưu Ý**: Bạn có thể chỉ sử dụng 3-4 ký tự đầu tiên của container ID:

```bash
docker start abc1
```

### Dừng Container Đang Chạy

```bash
docker stop <container-id>
```

**Ví Dụ:**
```bash
docker stop abc1
```

### Dừng Từ Docker Desktop

1. Mở Docker Desktop
2. Vào phần Containers
3. Tìm container đang chạy của bạn
4. Click nút "Stop"

## Sử Dụng Docker Desktop

### Xem Containers

Docker Desktop cung cấp GUI để quản lý containers:

1. **Tab Containers**: Xem tất cả containers
2. **Tùy Chọn Filter**: Hiển thị chỉ containers đang chạy
3. **Chi Tiết Container**: Click vào bất kỳ container nào để xem:
   - **Logs**: Logs khởi động Spring Boot và logs ứng dụng
   - **Inspect**: Cấu hình container (JAVA_VERSION, JAVA_HOME, ports)
   - **Files**: Duyệt filesystem của container
   - **Stats**: Sử dụng CPU, memory, tiêu thụ tài nguyên
   - **Terminal**: Truy cập giao diện command-line của container

### Container Logs

Xem logs trong Docker Desktop:
- Tất cả logs khởi động Spring Boot
- Logs gọi REST API
- Cập nhật logs real-time

### Container Inspection

Xem cấu hình chi tiết:
- `JAVA_VERSION`: Phiên bản JDK đang sử dụng
- `JAVA_HOME`: Đường dẫn đến JDK (ví dụ: `/usr/local/openjdk`)
- Cấu hình port
- Biến môi trường

### Container Files

Duyệt filesystem của container:
- Xác minh vị trí file JAR (ví dụ: thư mục root)
- Kiểm tra đường dẫn cài đặt JDK (`/usr/local/openjdk`)
- Kiểm tra tất cả files được bao gồm trong image

### Container Terminal

Truy cập terminal của container đang chạy:
```bash
pwd  # Kiểm tra thư mục hiện tại (thường là root /)
```

Điều này cho phép bạn thực thi các lệnh trực tiếp bên trong container đang chạy.

### Container Statistics

Giám sát việc sử dụng tài nguyên:
- **CPU Usage**: Phần trăm CPU được sử dụng
- **Memory Usage**: Tiêu thụ RAM
- **Network I/O**: Tốc độ truyền dữ liệu
- **Disk I/O**: Các hoạt động đọc/ghi

## Chạy Nhiều Containers

### Tạo Nhiều Instances

Bạn có thể tạo bất kỳ số lượng containers nào từ cùng một Docker image:

**Container Đầu Tiên:**
```bash
docker run -d -p 8080:8080 eazybytes/accounts:s4
```

**Container Thứ Hai:**
```bash
docker run -d -p 8081:8080 eazybytes/accounts:s4
```

### Lưu Ý Quan Trọng Với Nhiều Containers:

1. **Host Ports Phải Là Duy Nhất**: Bạn không thể sử dụng lại cùng một host port (8080, 8081 phải khác nhau)
2. **Container Ports Có Thể Giống Nhau**: Containers chạy trong mạng cô lập, nên các internal ports có thể giống nhau
3. **Mỗi Container Là Độc Lập**: Các instances riêng biệt với tài nguyên riêng

### Port Mapping Cho Nhiều Containers:

```
Container 1: -p 8080:8080
  - Hệ thống host: port 8080
  - Container: port 8080

Container 2: -p 8081:8080
  - Hệ thống host: port 8081
  - Container: port 8080
```

### Tại Sao Host Ports Phải Khác Nhau?

- Hệ thống local của bạn chia sẻ một mạng
- Port 8080 chỉ có thể được sử dụng một lần trên host
- Containers có mạng cô lập, nên chúng có thể sử dụng cùng internal port

### Xác Minh

Kiểm tra cả hai containers đang chạy:
```bash
docker ps
```

**Output:**
```
CONTAINER ID   IMAGE                    PORTS                    NAMES
abc123def456   eazybytes/accounts:s4   0.0.0.0:8080->8080/tcp  container1
def456abc789   eazybytes/accounts:s4   0.0.0.0:8081->8080/tcp  container2
```

### Test Nhiều Containers

Test từng container bằng Postman:
- Container 1: `http://localhost:8080/api/create`
- Container 2: `http://localhost:8081/api/create`

Cả hai đều phải response thành công với dữ liệu độc lập.

## Xóa Containers

### Sử Dụng Docker Desktop

1. Mở Docker Desktop
2. Vào phần Containers
3. Chọn các containers bạn muốn xóa
4. Click nút "Delete"

### Sử Dụng Terminal

```bash
docker rm <container-id>
```

**Lưu Ý**: Bạn phải dừng container trước khi xóa nó.

## Lợi Ích Của Docker Cho Microservices

### 1. Khả Năng Mở Rộng (Scalability)

**Dễ Dàng Mở Rộng Theo Chiều Ngang:**
- Tạo nhiều instances với một lệnh duy nhất
- Scale từ 1 đến N instances ngay lập tức
- Không cần thiết lập phức tạp

**Ví Dụ:**
```bash
docker run -d -p 8080:8080 eazybytes/accounts:s4
docker run -d -p 8081:8080 eazybytes/accounts:s4
docker run -d -p 8082:8080 eazybytes/accounts:s4
```

### 2. Tính Di Động (Portability)

**Chạy Bất Cứ Nơi Nào Docker Được Cài Đặt:**
- Cùng một Docker image hoạt động trên bất kỳ hệ thống nào
- Không cần cài đặt JDK, Spring Boot, hoặc Maven riêng
- Tất cả dependencies được bao gồm trong image
- Hành vi nhất quán trên các môi trường

**Người Dùng Chỉ Cần:**
- Docker được cài đặt
- Docker image
- Một lệnh: `docker run`

### 3. Đơn Giản Hóa Triển Khai (Deployment)

**Triển Khai Nhất Quán Trên Các Môi Trường:**
- Hệ thống local
- Virtual machines
- Cloud servers (AWS, Azure, GCP)
- Data centers on-premises

**Cùng Lệnh Ở Mọi Nơi:**
```bash
docker run -d -p 8080:8080 eazybytes/accounts:s4
```

**Không Cần Cấu Hình Theo Môi Trường:**
- Cùng Docker image
- Cùng lệnh
- Hành vi dự đoán được

## Tóm Tắt Workflow Hoàn Chỉnh

### Các Bước Chạy Spring Boot Application Trong Docker

**Bước 1: Build Application**
```bash
mvn clean install
```
- Chạy từ vị trí có file `pom.xml`
- Tạo fat JAR trong thư mục `target`

**Bước 2: Tạo Dockerfile**

Định nghĩa instructions để build Docker image với:
- Base image (ví dụ: OpenJDK)
- Copy file JAR
- Lệnh entry point

**Bước 3: Build Docker Image**
```bash
docker build . -t eazybytes/accounts:s4
```
- Cung cấp đường dẫn Dockerfile
- Tag với tên và phiên bản phù hợp

**Bước 4: Chạy Docker Container**
```bash
docker run -d -p 8080:8080 eazybytes/accounts:s4
```
- Chỉ định port mapping
- Cung cấp tên image
- Container khởi động và chạy application

## Những Điểm Chính Cần Nhớ

1. **Lệnh Docker Run**: Tạo containers từ images (tương tự toán tử `new` trong Java)
2. **Port Mapping**: Cần thiết để truy cập containers từ mạng bên ngoài
3. **Detached Mode**: Sử dụng flag `-d` để chạy containers ở background
4. **Nhiều Containers**: Tạo không giới hạn instances từ một image
5. **Quản Lý Container**: Sử dụng lệnh `docker ps`, `docker start`, `docker stop`
6. **Docker Desktop**: Cung cấp GUI để quản lý container dễ dàng
7. **Lợi Ích**: Giải quyết các thách thức về deployment, portability và scalability

## Best Practices (Thực Hành Tốt Nhất)

1. Luôn chạy containers ở detached mode (`-d`) cho development
2. Sử dụng host ports duy nhất khi chạy nhiều containers
3. Giám sát containers bằng statistics của Docker Desktop
4. Dọn dẹp các stopped containers thường xuyên
5. Sử dụng port mappings có ý nghĩa để dễ nhận diện
6. Test containers kỹ lưỡng sau khi tạo

## Tham Chiếu Các Lệnh Thường Dùng

```bash
# Chạy container (detached mode)
docker run -d -p 8080:8080 eazybytes/accounts:s4

# Liệt kê running containers
docker ps

# Liệt kê tất cả containers
docker ps -a

# Khởi động container
docker start <container-id>

# Dừng container
docker stop <container-id>

# Xóa container
docker rm <container-id>

# Xem container logs
docker logs <container-id>

# Truy cập container terminal
docker exec -it <container-id> /bin/bash
```

---

**Lưu Ý**: Thực hành các lệnh này nhiều lần để xây dựng sự quen thuộc. Khi bạn làm việc với Docker nhiều hơn, các thao tác này sẽ trở nên trực quan và hiệu quả.




FILE: 38-nhuoc-diem-cua-dockerfile-va-cac-giai-phap-thay-the.md


# Nhược Điểm Của Dockerfile Approach và Các Giải Pháp Thay Thế

## Tổng Quan

Mặc dù Dockerfile cung cấp một cách để containerize Spring Boot microservices, nó đi kèm với một số nhược điểm đáng kể khiến việc sử dụng trở nên thách thức cho các đội phát triển. Bài giảng này khám phá những hạn chế này và giới thiệu các giải pháp thay thế tốt hơn: **Buildpacks** và **Google Jib**.

## Best Practices Dọn Dẹp Container

Trước khi đi vào các nhược điểm, điều quan trọng là duy trì môi trường Docker sạch sẽ.

### Tại Sao Cần Dọn Dẹp Containers?

- **Sử Dụng Memory**: Containers đang chạy tiêu thụ RAM
- **Sử Dụng Storage**: Containers đã dừng vẫn chiếm dung lượng đĩa
- **Hiệu Suất Hệ Thống**: Quá nhiều containers có thể gây treo hệ thống
- **Quan Trọng Cho Hệ Thống Cấu Hình Thấp**: Thiết yếu nếu bạn có RAM hoặc storage hạn chế

### Cách Dọn Dẹp Containers

**Sử Dụng Docker Desktop:**
1. Mở Docker Desktop
2. Vào phần Containers
3. Dừng running containers bằng cách click nút "Stop"
4. Xóa unused containers bằng cách click nút "Delete"

**Sử Dụng Terminal:**
```bash
# Kiểm tra running containers
docker ps

# Dừng một container
docker stop <container-id>

# Xóa một container
docker rm <container-id>

# Xóa tất cả stopped containers
docker container prune
```

**Best Practice**: Thường xuyên dọn dẹp unused containers. Bạn luôn có thể tạo lại chúng bằng lệnh `docker run` khi cần.

## Nhược Điểm Của Dockerfile Approach

### 1. Đường Cong Học Tập Dốc

#### Thách Thức:

Viết Dockerfiles hiệu quả yêu cầu chuyên môn về các khái niệm Docker:
- Docker instructions và keywords
- Tối ưu hóa layer
- Lựa chọn base image
- Cấu hình entry point
- Copy commands và quản lý file

#### Tại Sao Đây Là Vấn Đề:

- **Không Thân Thiện Với Developers**: Developers tập trung vào application code, không phải DevOps
- **Tốn Thời Gian**: Học Docker sâu mất nhiều thời gian đáng kể
- **Yêu Cầu Chuyên Môn**: Dockerfiles đơn giản hoạt động cho demos, nhưng dự án thực cần kiến thức nâng cao
- **Trách Nhiệm Sai**: Developers không nên cần phải là chuyên gia Docker

**Ví Dụ**: Dockerfile đơn giản mà chúng ta đã tạo hoạt động cho các kịch bản cơ bản, nhưng ứng dụng lớn yêu cầu cấu hình Docker phức tạp hơn nhiều.

### 2. Độ Phức Tạp Của Best Practices

#### Yêu Cầu:

Để tạo Docker images production-ready, bạn phải tuân theo nhiều best practices:

**Tối Ưu Hóa Kích Thước Image:**
- Giữ images nhỏ nhất có thể
- Xóa các files và dependencies không cần thiết
- Sử dụng multi-stage builds
- Chọn minimal base images

**Tối Ưu Hóa Hiệu Suất:**
- Triển khai các chiến lược layer caching
- Sử dụng các kỹ thuật nén
- Tối ưu hóa thứ tự build
- Giảm thiểu số lượng layer

**Tiêu Chuẩn Bảo Mật:**
- Scan các lỗ hổng bảo mật
- Sử dụng trusted base images
- Tránh chạy dưới quyền root user
- Giữ dependencies được cập nhật
- Triển khai security scanning

#### Vấn Đề:

- **Yêu Cầu Chuyên Môn**: Triển khai tất cả best practices cần kiến thức Docker sâu
- **Đầu Tư Thời Gian**: Nỗ lực đáng kể để học và triển khai đúng cách
- **Cập Nhật Liên Tục**: Best practices phát triển; theo kịp là thách thức
- **Dễ Sai**: Dễ bỏ lỡ các bước bảo mật hoặc tối ưu hóa quan trọng

### 3. Cơn Ác Mộng Bảo Trì

#### Thách Thức:

Trong kiến trúc microservices với nhiều services:

**Kịch Bản:**
- Accounts microservice → Cần một Dockerfile
- Loans microservice → Cần một Dockerfile
- Cards microservice → Cần một Dockerfile
- Payment microservice → Cần một Dockerfile
- ... và tiếp tục

**Với 100 Microservices:**
- 100 Dockerfiles khác nhau cần bảo trì
- Mỗi cái cần updates khi best practices thay đổi
- Mỗi cái cần security patches
- Mỗi cái cần tối ưu hóa

#### Vấn Đề:

- **Trùng Lặp**: Các Dockerfiles tương tự trên các services với biến thể nhỏ
- **Độ Phức Tạp Versioning**: Quản lý các phiên bản khác nhau của Dockerfiles
- **Vấn Đề Nhất Quán**: Khó đảm bảo tất cả Dockerfiles tuân theo cùng tiêu chuẩn
- **Overhead Cập Nhật**: Thay đổi một best practice có nghĩa là cập nhật 100 files
- **Lỗi Con Người**: Nhiều files = nhiều cơ hội mắc lỗi hơn

### 4. Quản Lý Low-Level Instructions

#### Vấn Đề:

Dockerfiles yêu cầu chỉ định thủ công:
- Mọi file cần copy
- Phiên bản base image chính xác
- Cài đặt dependency thủ công
- Custom build arguments
- Biến môi trường
- Port exposures
- Volume mounts

#### Tại Sao Đây Là Vấn Đề:

- **Tẻ Nhạt**: Viết low-level instructions cho mọi microservice
- **Boilerplate**: Nhiều code lặp lại
- **Dễ Vỡ**: Lỗi nhỏ có thể phá vỡ build
- **Không Trừu Tượng**: Developers phải xử lý các chi tiết infrastructure

## Nhu Cầu Cho Các Giải Pháp Tốt Hơn

### Những Gì Developers Thực Sự Muốn:

1. **Tự Động Tạo Image**: Docker images được tạo mà không cần viết Dockerfiles
2. **Best Practices Tích Hợp**: Tối ưu hóa và bảo mật được xử lý tự động
3. **Không Cần Chuyên Môn Docker**: Không cần học Docker sâu
4. **Khả Năng Bảo Trì**: Dễ dàng cập nhật và bảo trì trên nhiều services
5. **Nhất Quán**: Cùng tiêu chuẩn được áp dụng tự động cho tất cả services

### Giải Pháp: Các Phương Pháp Hiện Đại

Hai giải pháp mạnh mẽ đã xuất hiện để giải quyết những thách thức này:

## Giới Thiệu Các Phương Pháp Thay Thế

### 1. Buildpacks

**Buildpacks Là Gì?**

Buildpacks cung cấp một abstraction cấp cao hơn để tạo Docker images tự động.

**Tính Năng Chính:**
- Tự động phát hiện loại application
- Áp dụng best practices tự động
- Không cần Dockerfile
- Tạo image được tối ưu hóa
- Security scanning tích hợp sẵn
- Được duy trì bởi các cloud platforms

**Lợi Ích:**
- ✅ Không cần chuyên môn Docker
- ✅ Tối ưu hóa tự động
- ✅ Bảo mật tích hợp sẵn
- ✅ Dễ sử dụng
- ✅ Tiêu chuẩn ngành (được sử dụng bởi Cloud Foundry, Heroku, Google Cloud)

### 2. Google Jib

**Google Jib Là Gì?**

Google Jib là công cụ build Docker images được tối ưu hóa cho Java applications mà không cần Docker daemon hoặc Dockerfile.

**Tính Năng Chính:**
- Build trực tiếp từ Maven/Gradle
- Không cần Dockerfile
- Không cần cài Docker
- Builds nhanh với incremental
- Layering được tối ưu hóa
- Builds có thể tái tạo

**Lợi Ích:**
- ✅ Plugin Maven/Gradle đơn giản
- ✅ Builds nhanh với caching
- ✅ Không cần kiến thức Docker
- ✅ Hoàn hảo cho Java applications
- ✅ Được duy trì bởi Google

## So Sánh: Dockerfile vs Phương Pháp Hiện Đại

| Khía Cạnh | Dockerfile | Buildpacks | Google Jib |
|-----------|-----------|------------|------------|
| **Độ Phức Tạp** | Cao | Thấp | Thấp |
| **Đường Cong Học Tập** | Dốc | Tối thiểu | Tối thiểu |
| **Bảo Trì** | Thủ công | Tự động | Tự động |
| **Best Practices** | Thủ công | Tích hợp | Tích hợp |
| **Bảo Mật** | Thủ công | Tích hợp | Tích hợp |
| **Tối Ưu Hóa** | Thủ công | Tự động | Tự động |
| **Chuyên Môn Docker** | Cần thiết | Không cần | Không cần |
| **Cần Dockerfile** | Có | Không | Không |
| **Tối Ưu Cho Java** | Không | Một phần | Có |

## Quyết Định: Tiến Về Phía Trước

### Tại Sao Chúng Ta Không Sử Dụng Dockerfiles

Dựa trên các nhược điểm đã thảo luận:

1. **Quá Phức Tạp**: Yêu cầu kiến thức Docker rộng
2. **Tốn Thời Gian**: Overhead học tập và triển khai
3. **Gánh Nặng Bảo Trì**: Quản lý nhiều Dockerfiles là không thực tế
4. **Dễ Sai**: Quy trình thủ công dẫn đến lỗi
5. **Không Tập Trung Vào Developer**: Developers nên tập trung vào code, không phải Docker

### Phương Pháp Của Chúng Ta Tiếp Theo

Chúng ta sẽ khám phá cả hai giải pháp hiện đại:

1. **Buildpacks** - Giải pháp universal, cloud-native
2. **Google Jib** - Tối ưu hóa cho Java, nhanh và đơn giản

**Mục Tiêu**: Đánh giá cả hai phương pháp và chọn phương pháp tốt nhất cho kiến trúc microservices của chúng ta.

## Tiếp Theo Là Gì?

### Lộ Trình Học Tập:

1. **Khám Phá Buildpacks**
   - Học cách Buildpacks hoạt động
   - Tạo Docker images sử dụng Buildpacks
   - Xem nó dễ dàng như thế nào so với Dockerfiles

2. **Khám Phá Google Jib**
   - Học cách Jib tích hợp với Maven
   - Tạo Docker images sử dụng Jib
   - So sánh với phương pháp Buildpacks

3. **Đưa Ra Lựa Chọn**
   - Đánh giá ưu và nhược điểm của mỗi cái
   - Chọn giải pháp tốt nhất cho nhu cầu của chúng ta
   - Triển khai trên tất cả microservices

## Những Điểm Chính Cần Nhớ

1. **Dockerfiles Có Hạn Chế**: 
   - Đường cong học tập dốc
   - Best practices phức tạp
   - Cơn ác mộng bảo trì
   - Quản lý low-level instructions

2. **Tồn Tại Các Giải Pháp Tốt Hơn**:
   - Buildpacks: Cloud-native, tự động, best practices tích hợp
   - Google Jib: Tối ưu cho Java, nhanh, không cần Docker

3. **Tập Trung Vào Development**:
   - Developers nên tập trung vào application code
   - Các vấn đề infrastructure nên được tự động hóa
   - Công cụ nên đơn giản hóa, không làm phức tạp

4. **Công Cụ Hiện Đại Tốt Hơn**:
   - Tối ưu hóa tự động
   - Bảo mật tích hợp
   - Bảo trì dễ dàng
   - Không cần chuyên môn Docker

## Tóm Tắt

Mặc dù Dockerfiles cung cấp cách để containerize applications, chúng đưa ra những thách thức đáng kể:
- Yêu cầu học tập phức tạp
- Triển khai best practice thủ công
- Khó bảo trì ở quy mô lớn
- Tốn thời gian cho developers

Các giải pháp hiện đại như **Buildpacks** và **Google Jib** giải quyết các vấn đề này bằng cách:
- Tự động hóa việc tạo image
- Áp dụng best practices tự động
- Không yêu cầu chuyên môn Docker
- Làm cho bảo trì đơn giản

Trong các bài giảng sắp tới, chúng ta sẽ khám phá chi tiết cả hai giải pháp và chọn giải pháp tốt nhất cho kiến trúc microservices của chúng ta.

---

**Quan Trọng**: Chúng ta sẽ không còn sử dụng phương pháp Dockerfile trong khóa học này do các hạn chế của nó. Tập trung học Buildpacks và Google Jib thay thế—chúng đại diện cho cách hiện đại, thân thiện với developer để containerize microservices.




FILE: 39-xay-dung-docker-images-voi-buildpacks.md


# Xây Dựng Docker Images Với Buildpacks

## Tổng Quan

Buildpacks cung cấp một phương pháp hiện đại, thân thiện với developer để tạo Docker images mà không cần viết Dockerfiles. Hướng dẫn này trình bày cách sử dụng Buildpacks với Spring Boot Maven plugin để tự động tạo Docker images production-ready.

## Buildpacks Là Gì?

### Định Nghĩa

**Buildpacks** chuyển đổi source code của ứng dụng thành Docker images có thể chạy trên bất kỳ nền tảng cloud nào—mà không cần các instructions Dockerfile ở mức thấp.

### Khả Năng Chính

- **Tạo Image Tự Động**: Tạo Docker images với một lệnh Maven duy nhất
- **Không Cần Dockerfile**: Loại bỏ nhu cầu về các Docker instructions thủ công
- **Phân Tích Source Code**: Tự động quét code và dependencies
- **Best Practices Tích Hợp**: Tuân theo các tiêu chuẩn Docker về bảo mật, caching và nén

## Lịch Sử và Phát Triển

### Nguồn Gốc

- **Ban Đầu Phát Triển**: Bởi Heroku
- **Tiến Hóa**: Pivotal và Heroku hợp tác tạo ra **Cloud Native Buildpacks**
- **Mục Đích**: Đơn giản hóa việc tạo Docker image đồng thời đảm bảo chất lượng production-grade

### Tại Sao Buildpacks Tồn Tại

Buildpacks được tạo ra để giải quyết độ phức tạp mà developers gặp phải khi:
- Học các khái niệm Docker sâu sắc
- Triển khai security best practices
- Tối ưu hóa kích thước và hiệu suất image
- Duy trì nhiều Dockerfiles

Thay vì yêu cầu developers trở thành chuyên gia Docker, Buildpacks tận dụng **nhiều năm kinh nghiệm** từ Heroku và Pivotal để tự động áp dụng best practices.

## Hệ Sinh Thái Buildpacks

### Tổng Quan Framework

Buildpacks là một **framework/ecosystem/concept** cung cấp:
- Tự động phát hiện loại ứng dụng
- Tối ưu hóa theo ngôn ngữ cụ thể
- Tạo image production-ready

### Paketo Buildpacks

**Paketo Buildpacks** là implementation được sử dụng cho các ứng dụng Java.

**Các Ngôn Ngữ Được Hỗ Trợ:**
- ☕ Java
- 🐹 Go
- 🏔️ GraalVM
- 🐍 Python
- 💎 Ruby
- 🐘 PHP
- 🟢 Node.js

Nếu microservice hoặc web application của bạn được viết bằng bất kỳ ngôn ngữ nào trong số này, bạn có thể sử dụng Buildpacks một cách an toàn.

### Bên Trong

Khi bạn sử dụng Buildpacks với Spring Boot:
- Spring Boot Maven plugin tận dụng Buildpacks
- Buildpacks sử dụng Paketo Buildpacks implementation
- Paketo xử lý việc tạo Docker image thực tế

## Yêu Cầu Trước Khi Bắt Đầu

Trước khi sử dụng Buildpacks, đảm bảo:
- ✅ Docker đã được cài đặt và đang chạy
- ✅ Docker server đang hoạt động (Buildpacks giao tiếp với Docker server)
- ✅ Maven đã được cài đặt
- ✅ Spring Boot project đã được thiết lập

## Thiết Lập Buildpacks Trong Spring Boot

### Bước 1: Cấu Hình pom.xml

Mở file `pom.xml` của bạn và cấu hình như sau:

#### Chỉ Định Loại Packaging

Thêm cấu hình packaging sau version:

```xml
<version>0.0.1-SNAPSHOT</version>
<packaging>jar</packaging>
```

#### Cấu Hình Spring Boot Maven Plugin

Thêm hoặc xác minh cấu hình Spring Boot Maven plugin:

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-maven-plugin</artifactId>
            <configuration>
                <image>
                    <name>eazybytes/${project.artifactId}:s4</name>
                </image>
            </configuration>
        </plugin>
    </plugins>
</build>
```

#### Phân Tích Cấu Hình Image Name

```xml
<image>
    <name>eazybytes/${project.artifactId}:s4</name>
</image>
```

**Các Thành Phần:**
- `eazybytes` - Tên người dùng Docker Hub của bạn (thay bằng của bạn)
- `${project.artifactId}` - Đọc động artifact ID từ pom.xml
- `s4` - Tên tag/version (section 4)

**Kết Quả Ví Dụ**: `eazybytes/loans:s4`

#### Sử Dụng Artifact ID Động

Thay vì hardcode tên microservice:

```xml
<!-- ❌ Hardcoded -->
<name>eazybytes/loans:s4</name>

<!-- ✅ Dynamic (được khuyến nghị) -->
<name>eazybytes/${project.artifactId}:s4</name>
```

Điều này tự động sử dụng artifact ID được định nghĩa ở đầu pom.xml:

```xml
<artifactId>loans</artifactId>
```

### Bước 2: Xác Minh Java Version

Đảm bảo Java version được chỉ định trong pom.xml:

```xml
<properties>
    <java.version>17</java.version>
</properties>
```

Buildpacks sẽ phát hiện điều này và sử dụng phiên bản JDK phù hợp.

## Xây Dựng Docker Image Với Buildpacks

### Lệnh Maven

Điều hướng đến thư mục project của bạn (nơi có pom.xml) và chạy:

```bash
mvn spring-boot:build-image
```

### Lệnh Này Làm Gì

1. **Gọi Spring Boot Maven Plugin**: Thực thi build-image goal
2. **Tận Dụng Buildpacks**: Sử dụng Buildpacks framework bên trong
3. **Phân Tích Application**: Quét source code và dependencies
4. **Tải Base Images**: Lấy Paketo Buildpacks base images (chỉ lần đầu tiên)
5. **Tạo Docker Image**: Tạo image được tối ưu hóa, production-ready

### Thực Thi Lần Đầu Tiên

**Thời Gian Dự Kiến**: ~5 phút

**Những Gì Xảy Ra:**
- Tải Paketo Buildpacks libraries và images
- Tải base images (ví dụ: Java runtime)
- Cache images locally cho việc sử dụng trong tương lai

**Ví Dụ Output:**
```
[INFO] Building image 'docker.io/eazybytes/loans:s4'
[INFO] 
[INFO]  > Pulling builder image 'docker.io/paketobuildpacks/builder:base' 100%
[INFO]  > Pulled builder image 'paketobuildpacks/builder@sha256:...'
[INFO]  > Pulling run image 'docker.io/paketobuildpacks/run:base-cnb' 100%
[INFO]  > Pulled run image 'paketobuildpacks/run@sha256:...'
[INFO]  > Executing lifecycle version v0.14.2
[INFO]  > Using build cache volume 'pack-cache-...'
```

### Chi Tiết Quy Trình Build

Trong quá trình build, Buildpacks:

1. **Phát Hiện Java Version**: Đọc từ pom.xml properties
2. **Quét Dependencies**: Phân tích tất cả dependencies trong pom.xml
3. **Tải JDK**: Lấy JDK phù hợp (ví dụ: JDK 17)
4. **Tạo Layers**: Tổ chức application trong các layers được tối ưu hóa
5. **Áp Dụng Best Practices**: Triển khai caching, compression, security
6. **Tạo Image**: Tạo Docker image cuối cùng

**Chỉ Báo Tiến Trình:**
```
[INFO] Downloading buildpacks... 36%
[INFO] Analyzing dependencies... 41%
[INFO] Building application layers... 67%
[INFO] Creating image... 89%
[INFO] Successfully built image 'eazybytes/loans:s4'
```

### Các Builds Tiếp Theo

**Thời Gian**: Nhanh hơn nhiều (vài giây đến 1-2 phút)

**Tại Sao?**
- Base images đã được cache
- Chỉ các layers thay đổi được rebuild
- Tối ưu hóa incremental build

## Xác Minh Docker Image

### Liệt Kê Docker Images

```bash
docker images
```

**Output Dự Kiến:**
```
REPOSITORY           TAG    IMAGE ID       CREATED          SIZE
eazybytes/loans      s4     abc123def456   2 minutes ago    311MB
eazybytes/accounts   s4     def456abc789   1 hour ago       456MB
paketobuildpacks/... base   ...            ...              1.31GB
```

### So Sánh Kích Thước Image

**Phương Pháp Dockerfile (Accounts)**: 456 MB
**Phương Pháp Buildpacks (Loans)**: 311 MB

**Giảm**: ~145 MB (nhỏ hơn 32%)

### Tại Sao Buildpacks Images Nhỏ Hơn

Buildpacks tự động:
- ✅ Xóa các files không cần thiết
- ✅ Tối ưu hóa tổ chức layer
- ✅ Triển khai compression
- ✅ Sử dụng minimal base images
- ✅ Áp dụng chiến lược caching
- ✅ Tuân theo Docker best practices

Mà không cần là chuyên gia Docker, bạn nhận được tất cả các tối ưu hóa này tự động!

### Paketo Buildpacks Image

Bạn cũng sẽ thấy một Paketo image lớn (1.31 GB):
- **Mục Đích**: Công cụ build-time để tạo images
- **Không Để Deploy**: Chỉ generated microservice image được deploy
- **Tải Một Lần**: Được cache locally cho tất cả builds tương lai

## Chạy Docker Container

### Tạo và Khởi Động Container

Chạy Docker image dưới dạng container:

```bash
docker run -d -p 8090:8090 eazybytes/loans:s4
```

**Phân Tích Lệnh:**
- `docker run` - Tạo và khởi động container
- `-d` - Detached mode (chạy ở background)
- `-p 8090:8090` - Port mapping (host:container)
- `eazybytes/loans:s4` - Tên Docker image

**Output:**
```
abc123def456789... (container ID)
```

### Bỏ Qua Build Warnings

Bạn có thể thấy warnings trong quá trình container khởi động:
```
WARNING: The requested image's platform (linux/amd64) does not match...
```

**Hành Động**: Các warnings này thường an toàn để bỏ qua.

## Xác Minh và Test

### Sử Dụng Docker Desktop

**Xem Images:**
1. Mở Docker Desktop
2. Vào tab "Images"
3. Tìm `eazybytes/loans` image

**Xem Containers:**
1. Vào tab "Containers"
2. Xem running `loans` container
3. Click tên container để xem logs

**Container Logs:**
```
  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =|_||___/=/_/_/_/
 :: Spring Boot ::               (v3.x.x)

...
Tomcat started on port(s): 8090 (http)
Started LoansApplication in 3.456 seconds
```

### Test Với Postman

**Create Loan API:**

**Endpoint:** `POST http://localhost:8090/api/create`

**Request Body:**
```json
{
    "mobileNumber": "1234567890"
}
```

**Response Dự Kiến:**
```json
{
    "statusCode": "201",
    "statusMsg": "Loan created successfully"
}
```

**Thành Công**: Xác nhận container đang chạy đúng và microservice hoạt động.

## Tóm Tắt Workflow Hoàn Chỉnh

### Các Bước Xây Dựng Docker Image Với Buildpacks

**Bước 1: Cấu Hình pom.xml**
```xml
<packaging>jar</packaging>

<build>
    <plugins>
        <plugin>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-maven-plugin</artifactId>
            <configuration>
                <image>
                    <name>eazybytes/${project.artifactId}:s4</name>
                </image>
            </configuration>
        </plugin>
    </plugins>
</build>
```

**Bước 2: Build Docker Image**
```bash
mvn spring-boot:build-image
```

**Bước 3: Chạy Dưới Dạng Container**
```bash
docker run -d -p 8090:8090 eazybytes/loans:s4
```

### Các Điểm Chính

1. **Spring Boot Maven Plugin**: Đi kèm mặc định với Spring Boot applications
2. **Image Name**: Được cấu hình trong pom.xml dưới plugin configuration
3. **Không Có Dockerfile**: Buildpacks xử lý mọi thứ tự động
4. **Production Standards**: Security, caching, compression được áp dụng tự động

## So Sánh Buildpacks vs Dockerfile

| Khía Cạnh | Dockerfile | Buildpacks |
|-----------|-----------|-----------|
| **Độ Phức Tạp** | Cao | Thấp |
| **Kiến Thức Docker** | Cần thiết | Không cần |
| **Cấu Hình** | Dockerfile | pom.xml |
| **Lệnh** | docker build | mvn spring-boot:build-image |
| **Tối Ưu Hóa** | Thủ công | Tự động |
| **Bảo Mật** | Thủ công | Tích hợp |
| **Kích Thước Image** | Lớn hơn (456 MB) | Nhỏ hơn (311 MB) |
| **Bảo Trì** | Mỗi microservice | Cấu hình plugin |
| **Best Practices** | Phải triển khai | Tự động áp dụng |

## Ưu Điểm Của Buildpacks

### 1. Thân Thiện Với Developer
- Không cần chuyên môn Docker
- Lệnh Maven đơn giản
- Công cụ Spring Boot quen thuộc

### 2. Tối Ưu Hóa Tự Động
- Kích thước image nhỏ hơn
- Layer caching
- Compression
- Tối ưu hóa hiệu suất

### 3. Bảo Mật Tích Hợp
- Vulnerability scanning
- Security patches
- Trusted base images
- Cập nhật thường xuyên từ Paketo

### 4. Production Standards
- Industry best practices
- Cloud-native ready
- Nhất quán trên các applications

### 5. Bảo Trì Thấp
- Không có Dockerfile để bảo trì
- Cập nhật qua Maven plugin
- Cấu hình tập trung

### 6. Hỗ Trợ Đa Ngôn Ngữ
- Java, Go, Python, Ruby, PHP, Node.js
- Phương pháp nhất quán trên các ngôn ngữ
- Cùng workflow cho các stacks khác nhau

## Những Điểm Chính Cần Nhớ

1. **Buildpacks Là Gì**: Framework chuyển đổi source code thành Docker images tự động
2. **Không Cần Dockerfile**: Một lệnh Maven tạo images production-ready
3. **Best Practices Tự Động**: Security, optimization, caching được xử lý tự động
4. **Tốt Hơn Dockerfile**: Images nhỏ hơn, bảo trì dễ hơn, không cần chuyên môn Docker
5. **Tích Hợp Spring Boot**: Hoạt động liền mạch với Spring Boot Maven plugin
6. **Production Ready**: Được sử dụng bởi Heroku, Pivotal và các cloud platforms lớn

## Best Practices

1. **Luôn chỉ định Docker username** trong cấu hình image
2. **Sử dụng dynamic artifact ID** thay vì hardcoding tên
3. **Giữ Docker running** trước khi thực thi lệnh build-image
4. **Dọn dẹp containers** thường xuyên để giải phóng tài nguyên
5. **Sử dụng tagging nhất quán** trên các microservices
6. **Tận dụng caching** bằng cách không thay đổi pom.xml không cần thiết

## Tham Chiếu Các Lệnh Thường Dùng

```bash
# Build Docker image với Buildpacks
mvn spring-boot:build-image

# Liệt kê Docker images
docker images

# Chạy container
docker run -d -p 8090:8090 eazybytes/loans:s4

# Kiểm tra running containers
docker ps

# Xem container logs
docker logs <container-id>

# Dừng container
docker stop <container-id>
```

## Xử Lý Sự Cố

### Vấn Đề: Build thất bại với "Cannot connect to Docker"
**Giải Pháp**: Đảm bảo Docker Desktop đang chạy

### Vấn Đề: Build lần đầu rất chậm
**Dự Kiến**: Tải lần đầu mất hơn 5 phút; các builds tiếp theo nhanh

### Vấn Đề: Port đã được sử dụng
**Giải Pháp**: Thay đổi host port trong lệnh docker run: `-p 8091:8090`

## Các Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ khám phá phương pháp thứ ba: **Google Jib**, một giải pháp hiện đại khác để xây dựng Docker images mà không cần Dockerfiles.

---

**Tóm Tắt**: Buildpacks cung cấp một giải pháp thay thế vượt trội cho Dockerfiles bằng cách tự động tạo Docker images production-ready với best practices, security và optimization tích hợp—tất cả mà không cần chuyên môn Docker.




FILE: 4-xay-dung-microservices-voi-spring-boot.md


# Xây Dựng Microservices với Spring Boot

## Giới Thiệu

Trong các bài giảng trước, chúng ta đã thảo luận về microservices là gì và chúng khác biệt như thế nào so với kiến trúc nguyên khối (monolithic) và SOA. Giờ đây khi đã hiểu được các ưu điểm của microservices, câu hỏi tiếp theo là: **Làm thế nào chúng ta có thể xây dựng microservices trong bất kỳ dự án nào?**

Cuối cùng thì, các nhà phát triển cần phải xây dựng các microservices này bằng cách sử dụng các ngôn ngữ backend như Java.

## Thách Thức

Trong suốt khóa học này, chúng ta sẽ trình bày nhiều thách thức gặp phải khi xây dựng microservices. Đối với mỗi thách thức, chúng ta sẽ:
1. Giới thiệu thách thức
2. Trình bày giải pháp hoặc tiêu chuẩn tốt nhất để vượt qua nó

### Thách Thức #1: Làm Thế Nào Để Xây Dựng Microservices Một Cách Hiệu Quả

Trong các ứng dụng web truyền thống, chẳng hạn như ứng dụng nguyên khối:
- Chúng ta phát triển tất cả code bằng các lớp và phương thức Java
- Đóng gói thành file WAR hoặc EAR
- Triển khai vào web server như Tomcat hoặc các application servers khác

**Quy trình này cực kỳ tốn thời gian:**
1. Phát triển ứng dụng web
2. Đóng gói ứng dụng
3. Triển khai vào web server

### Tại Sao Các Phương Pháp Truyền Thống Không Phù Hợp Với Microservices

Trong các dự án thực tế tại các tổ chức lớn, họ có thể xây dựng **hàng trăm hoặc thậm chí hàng nghìn microservices**. Việc xây dựng, đóng gói và triển khai tất cả các microservices này bằng phương pháp truyền thống là:
- Cực kỳ thách thức
- Thực tế là không thể thực hiện được

## Giải Pháp: Spring Boot Framework

**Spring Boot Framework** là giải pháp tốt nhất để vượt qua những thách thức này.

### Spring Boot Là Gì?

Spring Boot giúp chúng ta xây dựng microservices một cách hiệu quả bằng cách giải quyết các thách thức về triển khai và đóng gói đã đề cập ở trên. Trong suốt khóa học này, chúng ta sẽ sử dụng Spring Boot framework để xây dựng microservices.

## Kiến Thức Tiên Quyết

### Kiến Thức Yêu Cầu

Nếu bạn mới làm quen với Spring Framework và chưa nắm vững các khái niệm cơ bản như:
- Bean là gì?
- Autowiring là gì?

**Khuyến nghị:** Hãy tham gia một khóa học tập trung vào Spring Framework trước. Nắm vững các kiến thức cơ bản trước khi tiếp tục với microservices.

### Các Chủ Đề Spring Framework Cần Thành Thạo

- Kiến thức nền tảng về Spring Framework
- Spring Boot
- Xây dựng REST services
- Spring AOP
- Spring MVC
- Spring Security
- Spring Data JPA

### Lưu Ý Quan Trọng

Nếu bạn đã nắm vững các kiến thức cơ bản về Spring Framework và Spring Boot, bạn có thể tiếp tục với khóa học này. Điều quan trọng là phải có nền tảng vững chắc về các kiến thức cơ bản của Spring Framework trước khi xây dựng microservices.

## Các Bước Tiếp Theo

Từ bài giảng tiếp theo, chúng ta sẽ bước vào thế giới của Spring Boot và bắt đầu xây dựng microservices!

---

*Hết Bài Giảng*




FILE: 40-xay-dung-docker-images-voi-google-jib.md


# Xây Dựng Docker Images với Google Jib

## Giới Thiệu

Trong bài học này, chúng ta sẽ khám phá **Google Jib** như một phương pháp tạo Docker images cho các microservices Java. Jib là một công cụ chuyên biệt được thiết kế dành riêng cho việc containerize các ứng dụng Java.

## Google Jib Là Gì?

Google Jib là một công cụ mã nguồn mở để xây dựng các Docker images và OCI images được tối ưu hóa cho các ứng dụng Java mà không cần viết Dockerfile hoặc cài đặt Docker cục bộ.

**Repository chính thức:** https://github.com/GoogleContainerTools/jib

### Đặc Điểm Chính

- **Chuyên dụng cho Java**: Chỉ hoạt động với các ứng dụng Java
- **Không Cần Dockerfile**: Tạo images production-ready mà không cần viết cấu hình Docker
- **Docker Tùy Chọn**: Có thể build images mà không cần cài Docker cục bộ
- **Thời Gian Build Nhanh**: Nhanh hơn đáng kể so với Buildpacks (~11 giây so với thời gian dài hơn nhiều)

## Jib vs Buildpacks

| Tính Năng | Jib | Buildpacks |
|-----------|-----|------------|
| Hỗ Trợ Ngôn Ngữ | Chỉ Java | Python, Ruby, Node.js, Java và nhiều hơn |
| Tốc Độ Build | Nhanh (~11 giây) | Chậm hơn |
| Yêu Cầu Docker | Tùy chọn | Bắt buộc cho local builds |
| Trường Hợp Sử Dụng | Microservices Java | Dự án đa ngôn ngữ |

## Thiết Lập Jib Cho Dự Án Maven

### Bước 1: Cấu Hình Plugin trong pom.xml

Thêm Jib Maven plugin vào `pom.xml`:

```xml
<build>
    <plugins>
        <plugin>
            <groupId>com.google.cloud.tools</groupId>
            <artifactId>jib-maven-plugin</artifactId>
            <version>3.3.2</version>
            <configuration>
                <to>
                    <image>docker.io/ten-nguoi-dung/${project.artifactId}:s4</image>
                </to>
            </configuration>
        </plugin>
    </plugins>
</build>
```

### Bước 2: Cấu Hình Loại Packaging

Đảm bảo `pom.xml` của bạn có loại packaging được đặt là JAR:

```xml
<packaging>jar</packaging>
```

### Bước 3: Build Docker Image

Chạy lệnh Maven sau để tạo Docker image:

```bash
mvn compile jib:dockerBuild
```

Lệnh này sẽ:
- Quét cấu hình `pom.xml` của bạn
- Tạo Docker image production-ready
- Lưu trữ trong Docker registry cục bộ

## Ví Dụ Xây Dựng Cards Microservice

### Chi Tiết Cấu Hình

Cho ví dụ cards microservice:

```xml
<configuration>
    <to>
        <image>eazybytes/cards:s4</image>
    </to>
</configuration>
```

- **Tên Người Dùng Docker**: eazybytes
- **Project Artifact ID**: cards (lấy từ pom.xml)
- **Tag**: s4

### Quy Trình Build và Run

1. **Build image:**
   ```bash
   mvn compile jib:dockerBuild
   ```

2. **Xác minh image:**
   ```bash
   docker images
   ```
   
   Kết quả: Kích thước image khoảng 322 MB

3. **Chạy container:**
   ```bash
   docker run -d -p 9000:9000 eazybytes/cards:s4
   ```

4. **Xác minh container đang chạy:**
   ```bash
   docker ps
   ```

## Kích Thước và Chất Lượng Image

- **Kích thước**: ~322 MB (tương tự Buildpacks)
- **Chất lượng**: Production-ready, tuân theo các best practices về:
  - Tối ưu hóa hiệu suất
  - Tiêu chuẩn bảo mật
  - Layer caching
  - Nén dữ liệu

## Hiểu Về Tính Năng "Ngày Tạo"

Bạn có thể nhận thấy rằng các images được tạo bởi Jib hiển thị ngày tạo như "43 năm trước" hoặc "53 năm trước". Đây **không phải là lỗi**, mà là một tính năng có chủ đích:

### Tại Sao Lại Dùng Ngày Cũ?

- Sử dụng ngày bắt đầu cố định (thường từ những năm 1970)
- Đảm bảo builds có thể tái tạo
- Cho phép Docker nhận biết các images giống nhau
- Tối ưu hóa quá trình tái tạo image
- Nếu bạn rebuild mà không có thay đổi, hash của image vẫn giống hệt

Cách tiếp cận này cho phép caching và so sánh Docker images tốt hơn.

## Tính Năng Nâng Cao: Build Mà Không Cần Docker

Một trong những tính năng mạnh mẽ nhất của Jib là khả năng tạo Docker images **mà không cần cài Docker cục bộ**.

### Sử Dụng Lệnh Build

```bash
mvn compile jib:build
```

Lệnh này sẽ:
1. Build Docker image từ ứng dụng của bạn
2. Push trực tiếp lên registry từ xa (Docker Hub, GCR, ECR, v.v.)
3. Bỏ qua Docker cục bộ hoàn toàn

### Cấu Hình Remote Registries

#### Docker Hub
```xml
<image>docker.io/ten-nguoi-dung/ung-dung:tag</image>
```

#### Google Container Registry (GCR)
```xml
<image>gcr.io/du-an-gcp/ung-dung:tag</image>
```

#### Amazon Elastic Container Registry (ECR)
```xml
<image>tai-khoan.dkr.ecr.region.amazonaws.com/ung-dung:tag</image>
```

### Xác Thực

Khi push lên remote registries, bạn cần cấu hình thông tin đăng nhập:
- Docker Hub: Thông tin đăng nhập Docker
- GCR: Thông tin đăng nhập Google Cloud
- ECR: Thông tin đăng nhập AWS

Tham khảo tài liệu Jib để biết cấu hình xác thực cụ thể.

## Trường Hợp Sử Dụng Remote Building

Tính năng này đặc biệt có giá trị cho:

1. **CI/CD Pipelines**: Build images trong Jenkins, GitHub Actions, hoặc các công cụ CI/CD khác
2. **Build Servers Nhẹ**: Không cần cài Docker daemon nặng nề
3. **Quy Trình Làm Việc của Developer**: Developers push code, CI/CD xử lý containerization
4. **Bảo Mật**: Tránh chạy Docker daemon với quyền cao

## Tóm Tắt Từng Bước

### Bước 1: Cấu Hình Plugin
Thêm Jib Maven plugin vào `pom.xml` với cấu hình tên image dưới tag `<configuration>`.

### Bước 2: Build Image
Chạy lệnh:
```bash
mvn compile jib:dockerBuild
```

Lệnh này tạo Docker image trong hệ thống cục bộ sử dụng Docker server.

### Bước 3: Chạy Container
Thực thi container với:
```bash
docker run -d -p [host-port]:[container-port] [ten-image]:[tag]
```

Ứng dụng của bạn giờ đã sẵn sàng nhận requests dưới dạng Docker container.

## Ưu Điểm Chính

✅ **Images Production-Ready**: Tuân theo tất cả tiêu chuẩn production (hiệu suất, bảo mật, caching, nén)

✅ **Không Cần Viết Dockerfile**: Developers không cần kiến thức Docker chuyên sâu

✅ **Docker Tùy Chọn**: Có thể build mà không cần cài Docker cục bộ

✅ **Build Nhanh**: Nhanh hơn đáng kể so với các phương pháp khác

✅ **Phân Lớp Tối Ưu**: Tách layer thông minh để caching tốt hơn

✅ **Được Google Hỗ Trợ**: Được Google duy trì, đã được kiểm chứng trong môi trường production

## Kết Luận

Google Jib cung cấp một giải pháp xuất sắc để containerize các microservices Java với cấu hình tối thiểu và hiệu quả tối đa. Khả năng tạo Docker images production-ready mà không cần viết Dockerfile hoặc thậm chí không cần cài Docker cục bộ khiến nó trở thành lựa chọn hấp dẫn cho các dự án Java.

Trong bài học tiếp theo, chúng ta sẽ so sánh cả ba phương pháp (Dockerfile, Buildpacks và Jib) và chọn phương pháp tốt nhất cho phần còn lại của khóa học.

---

## Tài Liệu Tham Khảo Nhanh

| Tác Vụ | Lệnh |
|--------|------|
| Build với Docker cục bộ | `mvn compile jib:dockerBuild` |
| Build và push lên registry | `mvn compile jib:build` |
| Chạy container | `docker run -d -p [port]:[port] [image]:[tag]` |
| Liệt kê images | `docker images` |
| Liệt kê containers đang chạy | `docker ps` |




FILE: 41-so-sanh-cac-phuong-phap-tao-docker-image.md


# So Sánh Các Phương Pháp Tạo Docker Image

## Tổng Quan

Trong bài giảng này, chúng ta so sánh ba phương pháp phổ biến nhất để tạo Docker image cho microservices: Dockerfile, Buildpacks và Google Jib. Chúng ta sẽ xem xét ưu điểm, nhược điểm của từng phương pháp và giúp bạn chọn phương pháp phù hợp cho dự án của mình.

## Ba Phương Pháp Chính

Chúng ta đã khám phá ba phương pháp chính để tạo Docker image:
1. **Dockerfile**
2. **Buildpacks**
3. **Google Jib**

## Phương Pháp Nào Tốt Hơn?

**Không có phương pháp nào "tốt hơn" một cách tuyệt đối.** Mỗi phương pháp đều có ưu và nhược điểm riêng. Bạn cần lựa chọn dựa trên tình huống và yêu cầu cụ thể của mình.

## Phương Pháp Dockerfile

### Nhược Điểm
- Yêu cầu chuyên môn để viết Dockerfile đúng cách
- Phải tuân theo các tiêu chuẩn production và best practices một cách thủ công
- Cần được bảo trì cho tất cả các microservices
- Đường cong học tập cao hơn cho các developer

### Ưu Điểm
- **Tính linh hoạt tối đa** cho các yêu cầu tùy chỉnh
- Có thể đạt được bất kỳ cấu hình tùy chỉnh nào khi tạo Docker image
- Kiểm soát hoàn toàn quá trình tạo image

### Khi Nào Nên Sử Dụng
- Khi bạn có các yêu cầu tùy chỉnh cụ thể
- Khi bạn cần kiểm soát chi tiết quá trình tạo image
- Khi các giải pháp tiêu chuẩn không đáp ứng nhu cầu của bạn

### Tại Sao Không Sử Dụng Trong Khóa Học Này
Là các developer, chúng ta không muốn gánh vác việc học tất cả các khái niệm về Docker file và tuân theo các best practices một cách thủ công. Thay vào đó, chúng ta có thể dựa vào các nền tảng mã nguồn mở như Buildpacks và Google Jib.

## Buildpacks vs Jib: So Sánh Tính Năng

### Phân Tích Bảng So Sánh

Website của Buildpacks cung cấp bảng so sánh chi tiết trong tab "Features". Dưới đây là những điểm nổi bật:

#### Ưu Điểm Của Buildpacks
- ✅ **Advanced Caching**: Buildpacks cung cấp caching thông minh
- ✅ **Bill of Materials (SBOM)**: Buildpacks có, Jib không có
- ✅ **Modular và Pluggable**: Buildpacks cung cấp tính linh hoạt
- ✅ **Hỗ Trợ Đa Ngôn Ngữ**: Hỗ trợ nhiều ngôn ngữ lập trình (Java, Python, Node.js, v.v.)
- ✅ **Hỗ Trợ Đa Tiến Trình**: Có thể xử lý nhiều processes
- ✅ **Minimal App Image**: Tạo image được tối ưu hóa mặc định
- ✅ **Tính Linh Hoạt**: Có thể sử dụng cho nhiều công nghệ khác nhau

#### Đặc Điểm Của Jib
- ✅ **Minimal App Image**: Tạo image được tối ưu hóa mặc định
- ✅ **Tối Ưu Cho Java**: Được tối ưu hóa cao cho ứng dụng Java
- ❌ **Chỉ Java**: Giới hạn ở các microservices dựa trên Java
- ❌ **Không Có Advanced Caching**: Không cung cấp cùng mức độ caching như Buildpacks
- ❌ **Không Có SBOM**: Không tạo bill of materials

#### Đặc Điểm Của Dockerfile
- ✅ **Hỗ Trợ Đa Ngôn Ngữ**: Có thể hỗ trợ bất kỳ ngôn ngữ nào
- ✅ **Tính Linh Hoạt Tối Đa**: Kiểm soát hoàn toàn việc tạo image
- ⚠️ **Minimal App Image**: Có thể đạt được nhưng cần điều kiện và cấu hình thủ công

## Tại Sao Buildpacks Thường Được Ưa Chuộng

Nhiều developer chọn Buildpacks vì:
- Hỗ trợ nhiều ngôn ngữ lập trình
- Làm việc với kiến trúc microservice đa dạng
- Một phương pháp cho tất cả microservices bất kể ngôn ngữ
- Tránh phải duy trì nhiều phương pháp build khác nhau

## Tại Sao Chúng Ta Sử Dụng Jib Trong Khóa Học Này

Mặc dù Buildpacks là "người chiến thắng rõ ràng" trong bảng so sánh, chúng ta sử dụng **Google Jib** cho khóa học này. Dưới đây là ba lý do chính:

### Lý Do 1: Hiệu Năng và Tiết Kiệm Tài Nguyên
- **Thời Gian Build Nhanh Hơn**: Jib tạo Docker image nhanh hơn nhiều so với Buildpacks
- **Sử Dụng Bộ Nhớ Thấp Hơn**: Chiếm ít RAM và storage hơn trên hệ thống local
- **Tốt Hơn Cho Phần Cứng Hạn Chế**: Nhiều sinh viên chỉ có laptop với 8GB hoặc 16GB RAM
- **Thân Thiện Với Phát Triển Local**: Buildpacks có thể rất chậm và yêu cầu nhiều storage và RAM

### Lý Do 2: Tập Trung Vào Một Ngôn Ngữ
- Các microservices của chúng ta **chỉ dựa trên Java**
- Không có ý định phát triển microservices bằng các ngôn ngữ khác
- Không cần hỗ trợ đa ngôn ngữ cho khóa học này
- Jib hoàn toàn phù hợp cho microservices Java

> **Lưu ý**: Trong các dự án thực tế với microservices đa ngôn ngữ, Buildpacks là phương pháp được khuyến nghị.

### Lý Do 3: Vấn Đề Tương Thích Với Mac OS
- Buildpacks có các vấn đề đã biết trên hệ điều hành Mac
- Các lỗi chính thức đã được ghi nhận với team Buildpacks
- Các bản sửa lỗi có thể mất nhiều tháng hoặc thậm chí nhiều năm để ổn định trên Mac
- Nhiều sinh viên sử dụng hệ điều hành Mac
- Buildpacks hoạt động trên Mac nhưng có thể rất chậm
- Một số sinh viên có thể gặp khó khăn khi tạo Docker image với Buildpacks

**Xác Thực Jib**: Đã được xác thực hoạt động hoàn hảo trên:
- ✅ Windows
- ✅ Mac
- ✅ Linux

## Khuyến Nghị Cho Các Tình Huống Khác Nhau

### Cho Khóa Học Này
**Sử Dụng Jib** vì:
- Môi trường phát triển local
- Chỉ sử dụng microservices Java
- Cần tốc độ và hiệu quả
- Tài nguyên phần cứng hạn chế (laptop 8-16GB RAM)
- Yêu cầu tương thích đa nền tảng

### Cho Ứng Dụng Production
**Khuyến nghị: Buildpacks** (nhưng Jib cũng hoạt động tốt)

Ưu điểm của Buildpacks trong production:
- Server mạnh xử lý yêu cầu tài nguyên dễ dàng
- Khả năng caching nâng cao
- Bill of materials cho việc theo dõi bảo mật
- Hỗ trợ đa ngôn ngữ cho tính linh hoạt trong tương lai
- Hỗ trợ hệ sinh thái tốt hơn

**Jib Trong Production**: Cũng hoàn toàn khả thi cho microservices Java

### Cho Dự Án Đa Ngôn Ngữ
**Sử Dụng Buildpacks** vì:
- Một phương pháp cho tất cả microservices
- Không cần duy trì các hệ thống build khác nhau
- Quy trình build nhất quán trong tổ chức

### Cho Dự Án Chỉ Java Với Yêu Cầu Tùy Chỉnh
Cân nhắc **Dockerfile** khi:
- Các giải pháp tiêu chuẩn không đáp ứng nhu cầu
- Bạn cần kiểm soát chi tiết
- Team có chuyên môn về Docker

## Những Điểm Chính Cần Nhớ

1. **Không Có Phương Pháp Xấu Hay Tốt**: Tất cả các phương pháp đều hợp lệ và có điểm mạnh riêng
2. **Ngữ Cảnh Quan Trọng**: Chọn dựa trên yêu cầu và ràng buộc của dự án
3. **Có Sự Đánh Đổi**: Cân bằng giữa tính linh hoạt, dễ sử dụng và tính năng
4. **Local vs Production**: Các môi trường khác nhau có thể hưởng lợi từ các phương pháp khác nhau
5. **Kỹ Năng Team**: Xem xét chuyên môn của team và đường cong học tập

## Ma Trận Quyết Định

| Tiêu Chí | Dockerfile | Buildpacks | Jib |
|----------|-----------|-----------|-----|
| Tính Linh Hoạt | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Dễ Sử Dụng | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Tốc Độ (Local) | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Đa Ngôn Ngữ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ (chỉ Java) |
| Sử Dụng Tài Nguyên | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Tính Năng Nâng Cao | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Tương Thích Mac | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## Kết Luận

Trong suốt khóa học này, chúng ta sẽ tiếp tục sử dụng **Google Jib** làm phương pháp chính để tạo Docker image. Quyết định này dựa trên các cân nhắc thực tế cho môi trường học tập, nhưng hãy nhớ rằng trong các dự án thực tế của bạn, bạn nên đánh giá tất cả các lựa chọn và chọn cái phù hợp nhất với tình huống cụ thể của mình.

Bảng so sánh do Buildpacks cung cấp cho thấy nhiều ưu điểm, và trong môi trường production với tài nguyên đầy đủ, Buildpacks thường là lựa chọn được ưa chuộng. Tuy nhiên, cho mục đích học tập của chúng ta với microservices Java trên máy phát triển local, Jib cung cấp sự cân bằng tối ưu giữa tốc độ, đơn giản và độ tin cậy.

**Ghi nhớ**: Chọn cái gì phù hợp dựa trên dự án và tình huống của bạn. Cả ba phương pháp đều sẵn sàng cho production và được sử dụng rộng rãi trong ngành.




FILE: 42-day-va-keo-docker-images-len-docker-hub.md


# Đẩy và Kéo Docker Images lên Docker Hub

## Tổng Quan
Trong bài học này, chúng ta sẽ học cách đẩy (push) Docker images từ hệ thống local lên kho lưu trữ từ xa của Docker Hub và cách kéo (pull) chúng về. Điều này rất quan trọng cho việc triển khai microservices lên môi trường production, development hoặc QA.

## Tại Sao Cần Sử Dụng Kho Lưu Trữ Docker Từ Xa?

Docker images chỉ lưu trữ trên hệ thống local của bạn không thể được triển khai lên server production. Giống như cách chúng ta đẩy code lên GitHub, chúng ta cần đẩy Docker images lên các kho lưu trữ từ xa như:

- **Docker Hub** (registry công khai)
- **AWS ECR** (Amazon Elastic Container Registry)
- **GCP Container Registry**
- **Azure Container Registry**
- **GitHub Container Registry**

Trong khóa học này, chúng ta sẽ sử dụng Docker Hub làm kho lưu trữ từ xa.

## Đẩy Docker Images lên Docker Hub

### Cú Pháp Lệnh Push

```bash
docker image push docker.io/<tên-người-dùng>/<tên-image>:<tag>
```

### Ví Dụ: Đẩy Accounts Microservice

```bash
docker image push docker.io/eazybytes/accounts:S4
```

**Phân Tích Lệnh:**
- `docker.io` - Registry của Docker Hub
- `eazybytes` - Tên người dùng Docker Hub
- `accounts` - Tên image
- `S4` - Tên tag

### Đẩy Nhiều Microservices

**Đẩy Loans Microservice:**
```bash
docker image push docker.io/eazybytes/loans:S4
```

**Đẩy Cards Microservice:**
```bash
docker image push docker.io/eazybytes/cards:S4
```

## Xác Thực

### Cách Xác Thực Hoạt Động

Khi bạn thực thi lệnh push, Docker CLI tự động sử dụng thông tin đăng nhập từ Docker Desktop nếu bạn đã đăng nhập. CLI và Docker Desktop làm việc cùng nhau để:

1. Lấy username và password từ Docker Desktop
2. Xác thực với Docker Hub
3. Đẩy image lên kho lưu trữ từ xa

### Lưu Ý Quan Trọng

- **Sử dụng username của riêng bạn:** Không sử dụng username của người khác (như `eazybytes`) trong lệnh push của bạn
- **Yêu cầu đăng nhập:** Nếu bạn chưa đăng nhập vào Docker Desktop, bạn sẽ nhận lỗi "access denied"
- **Tính nhất quán của username:** Sử dụng cùng một username trong `pom.xml` khi tạo Docker images

## Xác Minh Images Đã Được Đẩy Lên

### Phương Pháp 1: Docker Desktop

1. Mở Docker Desktop
2. Nhấp vào phần **Hub**
3. Xem tất cả images trong kho lưu trữ từ xa với:
   - Tên images
   - Tên tags
   - Thời gian đẩy lên
   - Kích thước images

### Phương Pháp 2: Website Docker Hub

1. Đăng nhập vào [hub.docker.com](https://hub.docker.com)
2. Xem các repositories của bạn
3. Kiểm tra chi tiết image bao gồm:
   - Các tags có sẵn
   - Cài đặt hiển thị (public/private)
   - Lệnh pull
   - Lịch sử đẩy lên

## Hiển Thị Image: Public vs Private

### Images Public (Mặc Định)

- Bất kỳ ai cũng có thể pull Docker images của bạn
- Không cần thông tin đăng nhập để tải xuống
- Tương tự như GitHub repositories công khai
- Lý tưởng cho các dự án mã nguồn mở

### Images Private

- Chỉ bạn (và người dùng được ủy quyền) có thể truy cập
- Yêu cầu xác thực để pull
- Gói personal cơ bản cho phép **một kho lưu trữ private**
- Có thể thay đổi trong cài đặt repository

Để thay đổi hiển thị:
1. Vào cài đặt repository
2. Điều hướng đến cài đặt visibility
3. Chuyển đổi giữa public và private

## Kéo Docker Images từ Docker Hub

### Cú Pháp Lệnh Pull

```bash
docker pull <tên-người-dùng>/<tên-image>:<tag>
```

### Ví Dụ: Kéo Cards Microservice

```bash
docker pull eazybytes/cards:S4
```

### Kiểm Tra Quá Trình Pull

1. **Xóa image local:**
   ```bash
   docker images  # Liệt kê các images hiện tại
   # Xóa từ giao diện Docker Desktop hoặc sử dụng:
   docker rmi eazybytes/cards:S4
   ```

2. **Pull từ Docker Hub:**
   ```bash
   docker pull eazybytes/cards:S4
   ```

3. **Xác minh tải xuống:**
   ```bash
   docker images  # Sẽ hiển thị lại cards image
   ```

## Push vs Pull: Sự Khác Biệt Chính

| Lệnh | Hướng | Mục Đích |
|------|-------|----------|
| `docker push` | Local → Từ xa | Tải images lên Docker Hub |
| `docker pull` | Từ xa → Local | Tải images xuống từ Docker Hub |

## Trường Hợp Sử Dụng Docker Hub

### Cộng Tác Nhóm
- Các thành viên trong nhóm có thể pull Docker images
- Không cần rebuild images trên local
- Triển khai nhất quán trong toàn nhóm

### CI/CD Pipelines
- Các công cụ tự động lấy images từ Docker Hub
- Triển khai lên cloud servers (AWS, Azure, GCP)
- Triển khai lên máy ảo
- Quy trình triển khai liên tục

### Các Tình Huống Triển Khai
- Triển khai **Accounts microservice**
- Triển khai **Loans microservice**
- Triển khai **Cards microservice**
- Triển khai đa môi trường (dev, QA, production)

## Thực Hành Tốt Nhất

1. **Quản Lý Username:**
   - Luôn sử dụng Docker Hub username của riêng bạn
   - Đảm bảo tính nhất quán trong `pom.xml` và lệnh push

2. **Chiến Lược Tagging:**
   - Sử dụng các tags có ý nghĩa (ví dụ: `S4`, `v1.0`, `latest`)
   - Duy trì kiểm soát phiên bản thông qua tags

3. **Tổ Chức Image:**
   - Đặt tên image: `<username>/<tên-ứng-dụng>:<tag>`
   - Giữ quy ước đặt tên nhất quán

4. **Bảo Mật:**
   - Sử dụng repositories private cho các ứng dụng nhạy cảm
   - Giữ thông tin đăng nhập an toàn
   - Cập nhật images thường xuyên

## Tóm Tắt

Trong bài học này, chúng ta đã đề cập:
- ✅ Đẩy Docker images lên Docker Hub
- ✅ Xác thực với Docker Hub thông qua Docker Desktop
- ✅ Xác minh images trong Docker Hub (Desktop & Website)
- ✅ Hiển thị image public vs private
- ✅ Kéo Docker images từ Docker Hub
- ✅ Trường hợp sử dụng cho kho lưu trữ Docker từ xa

Docker Hub cho phép cộng tác và triển khai microservices một cách liền mạch trên các môi trường và thành viên nhóm khác nhau.

## Các Bước Tiếp Theo

Trong bài học tiếp theo, chúng ta sẽ khám phá các khái niệm Docker nâng cao hơn cho việc triển khai microservices.

---

**Lưu Ý:** Tất cả các lệnh Docker được sử dụng trong bài học này đều có sẵn trong GitHub repository của khóa học để tham khảo.




FILE: 43-gioi-thieu-docker-compose-va-cau-hinh.md


# Giới Thiệu Docker Compose và Cấu Hình

## Tổng Quan
Trong bài học này, chúng ta sẽ khám phá Docker Compose, một công cụ mạnh mẽ giải quyết thách thức quản lý nhiều microservices. Chúng ta sẽ học cách định nghĩa và cấu hình tất cả microservices trong một file YAML duy nhất và khởi động chúng chỉ bằng một lệnh.

## Vấn Đề: Quản Lý Nhiều Microservices

### Thách Thức Hiện Tại

Với ba microservices của chúng ta (Accounts, Loans và Cards), chúng ta đối mặt với nhiều vấn đề:

- **Tạo Container Thủ Công:** Phải chạy lệnh `docker run` riêng biệt cho mỗi microservice
- **Nhiều Instances:** Khởi động nhiều instances yêu cầu chạy lệnh nhiều lần
- **Tốn Thời Gian:** Quản lý 100 microservices sẽ yêu cầu 100 lệnh riêng biệt
- **Dễ Sai Sót:** Thực thi thủ công tăng khả năng mắc lỗi
- **Không Mở Rộng Được:** Cách tiếp cận này không khả thi cho môi trường production

### Ví Dụ Cách Tiếp Cận Thủ Công

```bash
docker run -p 8080:8080 eazybytes/accounts:S4
docker run -p 8090:8090 eazybytes/loans:S4
docker run -p 9000:9000 eazybytes/cards:S4
```

## Giải Pháp: Docker Compose

### Docker Compose Là Gì?

**Docker Compose** là công cụ để định nghĩa và chạy ứng dụng Docker đa container. Với Compose, bạn có thể:

- ✅ Sử dụng file YAML để cấu hình tất cả các services của ứng dụng
- ✅ Tạo và khởi động tất cả services chỉ bằng một lệnh
- ✅ Quản lý services trên các môi trường khác nhau (production, staging, development, testing)
- ✅ Làm việc liền mạch với CI/CD pipelines

### Lợi Ích Chính

1. **Khởi động, dừng và rebuild services** dễ dàng
2. **Xem trạng thái của các services đang chạy** ở một nơi
3. **Stream log output** từ tất cả services
4. **Chạy các lệnh một lần** trên các services
5. **Đơn giản hóa việc điều phối microservices**

## Cài Đặt Docker Compose

### Xác Minh

Docker Compose được cài đặt tự động với Docker Desktop. Xác minh cài đặt:

```bash
docker compose version
```

**Ví Dụ Output:**
```
Docker Compose version v2.x.x
```

### Cài Đặt Thủ Công

Nếu Docker Compose chưa được cài đặt, truy cập [trang cài đặt Docker Compose chính thức](https://docs.docker.com/compose/install/) và làm theo hướng dẫn cho hệ điều hành của bạn.

## Tạo Cấu Hình Docker Compose

### Bước 1: Tạo File docker-compose.yml

Tạo file có tên `docker-compose.yml` trong thư mục dự án của bạn (ví dụ: trong project accounts microservice):

```yaml
# Vị trí file: /accounts/docker-compose.yml
```

**Lưu Ý:** Extension `.yml` là bắt buộc vì cấu hình ở định dạng YAML.

### Bước 2: Định Nghĩa Services

#### Cấu Trúc Cơ Bản

```yaml
services:
  accounts:
    image: "eazybytes/accounts:S4"
    container_name: accounts-ms
    ports:
      - "8080:8080"
    deploy:
      resources:
        limits:
          memory: 700m
    networks:
      - eazybank
```

### Cấu Hình docker-compose.yml Đầy Đủ

```yaml
services:
  accounts:
    image: "eazybytes/accounts:S4"
    container_name: accounts-ms
    ports:
      - "8080:8080"
    deploy:
      resources:
        limits:
          memory: 700m
    networks:
      - eazybank

  loans:
    image: "eazybytes/loans:S4"
    container_name: loans-ms
    ports:
      - "8090:8090"
    deploy:
      resources:
        limits:
          memory: 700m
    networks:
      - eazybank

  cards:
    image: "eazybytes/cards:S4"
    container_name: cards-ms
    ports:
      - "9000:9000"
    deploy:
      resources:
        limits:
          memory: 700m
    networks:
      - eazybank

networks:
  eazybank:
    driver: bridge
```

## Phân Tích Cấu Hình

### 1. Phần Services

Phần tử gốc chứa tất cả các định nghĩa service:

```yaml
services:
  # Tất cả microservices được định nghĩa ở đây
```

### 2. Các Phần Tử Cấu Hình Service

#### Image
Chỉ định Docker image sử dụng:
```yaml
image: "eazybytes/accounts:S4"
```

#### Container Name
Gán tên có ý nghĩa cho container:
```yaml
container_name: accounts-ms
```

**Tại Sao Quan Trọng?**
- Không có điều này, Docker gán tên ngẫu nhiên (ví dụ: "angry_cannon")
- Giúp nhận diện container dễ dàng hơn
- Cải thiện quản lý và debug

#### Port Mapping
Ánh xạ cổng container sang cổng host:
```yaml
ports:
  - "8080:8080"  # host:container
```

**Định Dạng:** `"<cổng-host>:<cổng-container>"`

Nhiều ánh xạ cổng (nếu cần):
```yaml
ports:
  - "8080:8080"
  - "8081:8081"
```

#### Giới Hạn Memory
Hạn chế phân bổ memory tối đa:
```yaml
deploy:
  resources:
    limits:
      memory: 700m
```

**Lợi Ích:**
- Ngăn một service tiêu thụ toàn bộ memory hệ thống
- Đảm bảo phân phối tài nguyên công bằng
- Quan trọng cho hệ thống có RAM hạn chế (ví dụ: 16GB)

#### Networks
Gắn thẻ services vào một mạng chung:
```yaml
networks:
  - eazybank
```

**Mục Đích:**
- Cho phép giao tiếp giữa các services
- Không có điều này, services chạy trong mạng cô lập
- Bắt buộc cho microservices cần giao tiếp với nhau

### 3. Phần Networks

Định nghĩa mạng tùy chỉnh ở cấp độ gốc:

```yaml
networks:
  eazybank:
    driver: bridge
```

**Cấu Hình Mạng:**
- **Tên:** `eazybank` (có thể là bất kỳ tên nào)
- **Driver:** `bridge` - tạo mạng bridge cho giao tiếp service

## Quy Tắc Cú Pháp YAML

### Thụt Lề
YAML dựa vào thụt lề chính xác (sử dụng khoảng trắng, không phải tab):

```yaml
services:           # Cấp độ gốc (không thụt lề)
  accounts:         # 2 khoảng trắng
    image: "..."    # 4 khoảng trắng
    ports:          # 4 khoảng trắng
      - "8080:8080" # 6 khoảng trắng (mục danh sách với dấu gạch ngang)
```

### Danh Sách
Sử dụng dấu gạch ngang (-) cho các mục danh sách:

```yaml
ports:
  - "8080:8080"
  - "8081:8081"

networks:
  - eazybank
```

### Cặp Key-Value
Sử dụng dấu hai chấm (:) theo sau bởi khoảng trắng:

```yaml
image: "eazybytes/accounts:S4"
container_name: accounts-ms
```

## Cấu Trúc Phân Cấp Cấu Hình

```
services (gốc)
├── accounts (tên service)
│   ├── image
│   ├── container_name
│   ├── ports
│   ├── deploy
│   │   └── resources
│   │       └── limits
│   │           └── memory
│   └── networks
├── loans (tên service)
│   └── ... (cùng cấu trúc)
└── cards (tên service)
    └── ... (cùng cấu trúc)

networks (gốc)
└── eazybank
    └── driver
```

## Tại Sao Cấu Hình Mạng Quan Trọng

### Không Có Cấu Hình Mạng
- Mỗi service chạy trong mạng cô lập riêng
- Không thể giao tiếp giữa các services
- Services không thể khám phá lẫn nhau

### Có Cấu Hình Mạng
- Tất cả services chia sẻ cùng mạng (`eazybank`)
- Bridge driver cho phép giao tiếp
- Services có thể giao tiếp sử dụng tên container làm hostname
- Hỗ trợ các phụ thuộc service trong tương lai

## Thực Hành Tốt Nhất

### 1. Vị Trí File
- Đặt `docker-compose.yml` ở vị trí trung tâm
- Check vào version control (GitHub)
- Giữ cùng với các microservices liên quan

### 2. Đặt Tên Container
- Sử dụng tên mô tả với hậu tố: `-ms` (microservice)
- Ví dụ: `accounts-ms`, `loans-ms`, `cards-ms`
- Tránh tên ngẫu nhiên do Docker tạo

### 3. Giới Hạn Tài Nguyên
- Luôn đặt giới hạn memory trong production
- Ngăn cạn kiệt tài nguyên
- Điều chỉnh dựa trên yêu cầu service

### 4. Chiến Lược Mạng
- Sử dụng mạng tùy chỉnh cho các services liên quan
- Sử dụng bridge driver cho cấu hình đơn giản
- Lập kế hoạch cho nhu cầu giao tiếp service trong tương lai

### 5. Image Tags
- Sử dụng tags cụ thể (ví dụ: `S4`) thay vì `latest`
- Đảm bảo tính nhất quán phiên bản
- Tạo điều kiện cho rollbacks

## Hỗ Trợ IDE

### IntelliJ IDEA
- Plugin YAML cung cấp syntax highlighting
- Hỗ trợ tự động thụt lề
- Xác thực cấu trúc YAML

### VS Code
- Extension Docker cung cấp IntelliJ
- Extension YAML cho hỗ trợ cú pháp
- Hỗ trợ ngôn ngữ Docker Compose

## Chuẩn Bị Cho Triển Khai

### Trạng Thái Hiện Tại
✅ File Docker Compose đã tạo  
✅ Ba microservices đã được cấu hình  
✅ Thiết lập mạng hoàn tất  
✅ Giới hạn memory đã định nghĩa  
✅ Ánh xạ cổng đã thiết lập  

### Các Bước Tiếp Theo
Trong bài học tiếp theo, chúng ta sẽ học cách:
- Khởi động tất cả microservices với một lệnh duy nhất
- Xác minh trạng thái service
- Quản lý các container đang chạy
- Xem logs từ tất cả services

## Tóm Tắt

Trong bài học này, chúng ta đã đề cập:
- ✅ Thách thức quản lý nhiều microservices thủ công
- ✅ Giới thiệu Docker Compose và lợi ích của nó
- ✅ Cài đặt và xác minh Docker Compose
- ✅ Tạo file cấu hình `docker-compose.yml`
- ✅ Cấu hình services (image, ports, memory, networks)
- ✅ Thiết lập mạng tùy chỉnh cho giao tiếp giữa các services
- ✅ Cú pháp YAML và quy tắc thụt lề
- ✅ Thực hành tốt nhất cho cấu hình Docker Compose

Docker Compose đơn giản hóa quản lý microservices bằng cách thay thế nhiều lệnh thủ công bằng một file cấu hình khai báo duy nhất.

---

**Bài Học Tiếp Theo:** Khởi động tất cả microservices với một lệnh Docker Compose duy nhất.




FILE: 44-khoi-dong-microservices-voi-docker-compose.md


# Khởi Động Microservices với Docker Compose

## Tổng Quan

Trong bài học này, chúng ta sẽ tìm hiểu cách khởi động tất cả các microservices bằng lệnh Docker Compose. Docker Compose cho phép chúng ta quản lý nhiều container với một lệnh duy nhất, giúp làm việc với kiến trúc microservices dễ dàng hơn.

## Yêu Cầu Trước Khi Bắt Đầu

- Đã cài đặt Docker Desktop
- File cấu hình Docker Compose YAML đã được thiết lập
- Các microservices (accounts, loans, cards) sẵn sàng để chạy

## Lỗi Thường Gặp: Chạy Docker Compose Từ Thư Mục Sai

Khi thực hiện lệnh Docker Compose, bạn phải ở trong thư mục chứa file `docker-compose.yaml`.

### Ví Dụ Về Lỗi

Nếu bạn đang ở trong thư mục cards microservice mà không có file Docker Compose và chạy:

```bash
docker compose up
```

Bạn sẽ nhận được lỗi:
```
no configuration file provided, not found
```

### Giải Pháp

Di chuyển đến thư mục chứa file `docker-compose.yaml` (ví dụ: thư mục accounts):

```bash
cd accounts
ls  # Xác nhận file docker-compose.yaml có mặt
```

## Khởi Động Microservices với Docker Compose

### Lệnh Cơ Bản

```bash
docker compose up
```

Lệnh này khởi động tất cả các container được định nghĩa trong file Docker Compose YAML. Tuy nhiên, lệnh này sẽ giữ terminal của bạn bận với các log.

### Chế Độ Detached (Khuyến Nghị)

Để khởi động containers ở chế độ nền:

```bash
docker compose up -d
```

Cờ `-d` chạy containers ở chế độ detached, giải phóng terminal của bạn.

### Kiểm Tra Containers Đang Chạy

Kiểm tra các containers đang chạy bằng:

```bash
docker ps
```

Kết quả mong đợi hiển thị:
- Ba microservices đang chạy
- Các cổng: 8080, 8090, 9000
- Tên containers như đã cấu hình

### Xem Trong Docker Desktop

Trong Docker Desktop:
1. Điều hướng đến **Containers**
2. Bạn sẽ thấy một thư mục cha (được đặt tên theo thư mục nơi bạn chạy lệnh)
3. Dưới thư mục này, cả ba microservices xuất hiện:
   - Loans microservice
   - Cards microservice
   - Accounts microservice

**Lưu ý**: Có thể có lỗi hiển thị nơi "accounts-ms" hiển thị chỉ là "ms" trong Docker Desktop, nhưng CLI hiển thị tên đúng.

## Kiểm Tra Các Microservices

Sau khi khởi động containers, kiểm tra từng microservice:

### Tạo Account
- Cổng: 8080
- Gửi request → Phản hồi thành công ✓

### Tạo Loan
- Cổng: 8090
- Gửi request → Phản hồi thành công ✓

### Tạo Card
- Cổng: 9000
- Gửi request → Phản hồi thành công ✓

## Dừng Microservices với Docker Compose

### Dừng và Xóa Containers (Khuyến Nghị)

```bash
docker compose down
```

Lệnh này:
- Dừng tất cả containers
- Xóa tất cả containers
- Dọn dẹp tài nguyên

**Lưu ý**: Cờ `-d` không áp dụng cho `docker compose down`.

### Dừng Mà Không Xóa

```bash
docker compose stop
```

Lệnh này chỉ dừng containers mà không xóa chúng. Tuy nhiên, nên sử dụng `docker compose down` để dọn dẹp tài nguyên.

### Xác Nhận

Kiểm tra Docker Desktop sau khi chạy `docker compose down`:
- Tất cả containers đã được xóa
- Không còn containers nào trong danh sách

## Tóm Tắt Các Lệnh Docker Compose Chính

| Lệnh | Mục Đích |
|---------|---------|
| `docker compose up` | Khởi động tất cả containers (chế độ foreground) |
| `docker compose up -d` | Khởi động tất cả containers (chế độ nền/detached) |
| `docker compose down` | Dừng và xóa tất cả containers |
| `docker compose stop` | Dừng containers mà không xóa |
| `docker ps` | Liệt kê các containers đang chạy |

## Mạng (Networking)

Một mạng Docker có tên `easybank` đã được tạo trong cấu hình Docker Compose. Mạng này cho phép:
- Giao tiếp giữa các containers
- Phát hiện dịch vụ (Service discovery)
- Cách ly mạng

Chúng ta sẽ khám phá chi tiết về giao tiếp mạng giữa các containers trong các phần tiếp theo sử dụng mạng bridge driver.

## Thực Hành Tốt Nhất

### Cấu Trúc File YAML

1. **Thụt Lề Rất Quan Trọng**: Mỗi khoảng trắng đều có ý nghĩa trong file YAML
2. **Xác Thực Cú Pháp**: Đảm bảo cấu trúc đúng trước khi chạy
3. **Kiểm Soát Phiên Bản**: Lưu docker-compose.yaml trong kho GitHub của bạn
4. **Tính Nhất Quán**: Tuân theo cấu trúc đã thiết lập cho tất cả các dịch vụ

### Lưu Ý Quan Trọng

⚠️ **Luôn chạy lệnh Docker Compose từ thư mục chứa file `docker-compose.yaml`**

⚠️ **Chú ý đến thụt lề YAML** - khoảng cách không đúng sẽ gây lỗi

⚠️ **Sử dụng `docker compose down`** thay vì `stop` để dọn dẹp tài nguyên đúng cách

## Ưu Điểm Của Docker Compose

- **Quản Lý Bằng Một Lệnh**: Khởi động/dừng nhiều microservices cùng lúc
- **Cấu Hình Nhất Quán**: Tất cả dịch vụ được định nghĩa trong một file
- **Dễ Dàng Sao Chép**: Chia sẻ cấu hình giữa các nhóm
- **Quản Lý Mạng**: Tự động tạo và cấu hình mạng
- **Ánh Xạ Cổng**: Cấu hình cổng tập trung

## Các Bước Tiếp Theo

Trong các bài học tiếp theo, chúng ta sẽ đi sâu hơn vào:
- Mạng container và giao tiếp giữa các dịch vụ
- Cấu hình Docker Compose nâng cao
- Phụ thuộc dịch vụ và thứ tự khởi động
- Cấu hình theo môi trường cụ thể

## Kết Luận

Docker Compose đơn giản hóa việc quản lý microservices bằng cách cho phép bạn:
- Khởi động nhiều dịch vụ với `docker compose up -d`
- Dừng và dọn dẹp với `docker compose down`
- Quản lý các ứng dụng đa container phức tạp một cách hiệu quả

Hãy chắc chắn rằng bạn hiểu cấu trúc và cú pháp của file Docker Compose YAML, vì nó là nền tảng để làm việc với các microservices được container hóa.

---

**Cảm ơn bạn, và hẹn gặp lại trong bài học tiếp theo!**




FILE: 45-docker-compose-commands-start-stop-up-down.md


# Các Lệnh Docker Compose: Start, Stop, Up và Down

## Tổng Quan

Trong bài giảng này, chúng ta sẽ khám phá các lệnh Docker Compose khác nhau và hiểu khi nào nên sử dụng từng lệnh. Chúng ta sẽ tìm hiểu sự khác biệt chính giữa `docker compose up`, `docker compose down`, `docker compose start` và `docker compose stop`.

## Các Lệnh Docker Compose

### Docker Compose Up

Lệnh `docker compose up` được sử dụng để **tạo và khởi động container từ đầu**.

```bash
docker compose up
```

- Tạo các container mới dựa trên cấu hình docker-compose.yml của bạn
- Nếu container chưa tồn tại, nó sẽ tạo chúng
- Nếu container đã tồn tại với cùng tên, nó sẽ sử dụng các container có sẵn đó
- Sử dụng cờ `-d` để chạy ở chế độ detached (chạy nền)

```bash
docker compose up -d
```

### Docker Compose Down

Lệnh `docker compose down` được sử dụng để **dừng và xóa container**.

```bash
docker compose down
```

- Dừng tất cả các container đang chạy
- Xóa hoàn toàn các container
- Giải phóng tài nguyên hệ thống

### Docker Compose Stop

Lệnh `docker compose stop` được sử dụng để **dừng container mà không xóa chúng**.

```bash
docker compose stop
```

- Dừng tất cả các container đang chạy được khởi động bằng docker compose
- Các container vẫn còn trong hệ thống (không bị xóa)
- Hữu ích khi bạn muốn tạm dừng dịch vụ của mình
- Nếu không có container nào đang chạy, lệnh này không có tác dụng gì

### Docker Compose Start

Lệnh `docker compose start` được sử dụng để **khởi động các container đã dừng có sẵn**.

```bash
docker compose start
```

- Tìm kiếm các container có sẵn và khởi động chúng
- KHÔNG tạo container mới
- Chỉ hoạt động nếu container đã tồn tại
- Nếu không có container nào tồn tại, lệnh sẽ thất bại

## Sự Khác Biệt Chính

### `docker compose up` vs `docker compose start`

- **`docker compose up`**: Tạo container từ đầu nếu chúng chưa tồn tại, hoặc sử dụng container có sẵn nếu đã có
- **`docker compose start`**: Chỉ khởi động các container đã dừng có sẵn; thất bại nếu không có container nào tồn tại

### `docker compose down` vs `docker compose stop`

- **`docker compose down`**: Dừng VÀ xóa hoàn toàn các container
- **`docker compose stop`**: Chỉ dừng container; giữ chúng để sử dụng sau

## Ví Dụ Thực Tế

Đây là quy trình làm việc điển hình:

1. **Thiết lập ban đầu**: Tạo và khởi động container
   ```bash
   docker compose up -d
   ```

2. **Tạm dừng**: Dừng container mà không xóa chúng
   ```bash
   docker compose stop
   ```

3. **Tiếp tục làm việc**: Khởi động lại các container đã dừng
   ```bash
   docker compose start
   ```

4. **Dọn dẹp**: Dừng và xóa tất cả container
   ```bash
   docker compose down
   ```

## Thực Hành Tốt Nhất

- **Sử dụng `docker compose up` và `docker compose down`** cho hầu hết các hoạt động hàng ngày
- Luôn xóa container khi bạn không cần chúng để giải phóng không gian hệ thống
- Chỉ sử dụng `docker compose stop` và `docker compose start` khi bạn cần bảo toàn trạng thái container tạm thời

## Các Dịch Vụ Ví Dụ

Trong phần demo, chúng ta làm việc với ba microservice:
- **accounts-ms** (Microservice Tài khoản)
- **loans-ms** (Microservice Khoản vay)
- **cards-ms** (Microservice Thẻ)

## Kiểm Tra

Bạn có thể kiểm tra trạng thái container của mình bằng cách:
- Giao diện Docker Desktop
- Dòng lệnh với `docker ps` (cho container đang chạy)
- Dòng lệnh với `docker ps -a` (cho tất cả container, bao gồm cả đã dừng)

## Tóm Tắt

Hiểu được sự khác biệt giữa các lệnh Docker Compose này là rất quan trọng cho việc quản lý container hiệu quả:

- `docker compose up`: Tạo và khởi động (từ đầu hoặc từ container có sẵn)
- `docker compose down`: Dừng và xóa
- `docker compose start`: Khởi động các container đã dừng có sẵn
- `docker compose stop`: Dừng mà không xóa

Chọn lệnh phù hợp dựa trên việc bạn muốn bảo toàn hay xóa container của mình.




FILE: 46-docker-extensions-and-logs-explorer.md


# Docker Extensions và Logs Explorer

## Giới thiệu về Docker Extensions

Docker Desktop cung cấp một hệ sinh thái mở rộng phong phú có thể nâng cao đáng kể quy trình phát triển của bạn. Những extensions này được thiết kế để giải quyết các vấn đề phổ biến và thêm các tính năng hữu ích vào môi trường Docker Desktop.

## Truy cập Docker Extensions

Để truy cập các Docker extensions:
1. Mở Docker Desktop
2. Điều hướng đến tùy chọn **Add Extensions** (Thêm Extensions)
3. Duyệt qua hàng nghìn extensions có sẵn dựa trên yêu cầu của bạn

## Khi nào nên sử dụng Docker Extensions

Docker extensions đặc biệt hữu ích khi bạn:
- Gặp phải vấn đề với Docker containers, images, hoặc Docker Desktop
- Có các tác vụ lặp đi lặp lại tốn nhiều thời gian
- Cần chức năng bổ sung không có sẵn trong Docker Desktop mặc định

**Khuyến nghị**: Luôn tìm kiếm các extensions phù hợp khi gặp khó khăn. Nhiều nhà phát triển có thể đã gặp các vấn đề tương tự và tạo ra các extensions để giải quyết chúng.

## Extension Logs Explorer

### Tổng quan

**Logs Explorer** là một extension Docker chính thức được xuất bản bởi Docker Inc., cung cấp chế độ xem tập trung các logs từ tất cả containers của bạn.

### Các bước cài đặt

1. Trong Docker Desktop, tìm kiếm "log" trong thị trường extensions
2. Chọn **Logs Explorer**
3. Nhấp vào nút **Install** (Cài đặt)
4. Extension sẽ được cài đặt và có sẵn trong phần Extensions

### Tính năng chính

#### Xem Log tập trung
- Xem logs từ tất cả các containers đang chạy và đã dừng ở một nơi
- Loại bỏ nhu cầu điều hướng đến từng container riêng lẻ

#### Logs được mã hóa màu
Khi chạy nhiều microservices (ví dụ: thông qua `docker compose up`), mỗi service có màu riêng:
- **Accounts microservice**: Màu xanh dương (Blue)
- **Loans microservice**: Màu đỏ (Red)
- **Cards microservice**: Màu xanh lá (Green)

Mã hóa màu này giúp dễ dàng phân biệt giữa các services khác nhau chỉ trong một cái nhìn.

#### Tùy chọn lọc

1. **Lọc theo container cụ thể**: Chọn một container cụ thể để chỉ xem logs của nó
2. **Lọc theo trạng thái container**: Chuyển đổi giữa:
   - Containers đang chạy
   - Containers đã dừng
3. **Lọc theo loại log**: Lọc theo:
   - Standard output (stdout)
   - Standard error (stderr)

#### Chức năng tìm kiếm
- Tính năng tìm kiếm tích hợp để tìm các mục log cụ thể
- Giúp nhanh chóng xác định thông tin liên quan trong các file log lớn

## Ví dụ thực tế

Khi chạy kiến trúc microservices với Docker Compose:

```bash
docker compose up
```

Điều hướng đến Docker Desktop → Extensions → Logs Explorer để:
- Xem tất cả logs của microservices trong một chế độ xem
- Xác định service nào tạo ra các mục log cụ thể bằng màu sắc
- Lọc logs theo tên service
- Tìm kiếm các lỗi hoặc thông điệp cụ thể

## Lợi ích của việc sử dụng Docker Extensions

1. **Tiết kiệm thời gian**: Tự động hóa các tác vụ lặp đi lặp lại và hợp lý hóa quy trình làm việc
2. **Tăng năng suất**: Truy cập các công cụ bổ sung mà không cần rời khỏi Docker Desktop
3. **Giải quyết vấn đề**: Tận dụng các giải pháp của cộng đồng cho các vấn đề phổ biến
4. **Cải thiện giám sát**: Khả năng hiển thị tốt hơn vào hoạt động của container

## Thực hành tốt nhất

- Cài đặt Logs Explorer ngay lập tức để cải thiện trải nghiệm debugging
- Thường xuyên kiểm tra các extensions mới giải quyết các điểm khó khăn của bạn
- Khám phá các extensions chính thức trước để có độ tin cậy và hỗ trợ
- Đọc mô tả và đánh giá của extension trước khi cài đặt

## Kết luận

Docker extensions, đặc biệt là Logs Explorer, có thể cải thiện đáng kể trải nghiệm phát triển của bạn bằng cách:
- Đơn giản hóa quản lý log trên nhiều containers
- Cung cấp khả năng hiển thị tốt hơn vào hoạt động của microservices
- Giảm thời gian điều hướng giữa các containers khác nhau

**Khuyến nghị mạnh mẽ**: Cài đặt extension Logs Explorer trên hệ thống của bạn để hợp lý hóa quy trình Docker và quá trình debugging.

## Tài nguyên bổ sung

- Docker Extensions Marketplace: Có sẵn trong Docker Desktop
- Tài liệu Docker Extensions chính thức
- Extensions đóng góp bởi cộng đồng cho các trường hợp sử dụng chuyên biệt

---

**Các bước tiếp theo**: Trong bài giảng tiếp theo, chúng ta sẽ khám phá các tính năng Docker bổ sung và các thực hành tốt nhất cho phát triển microservices.




FILE: 47-docker-commands-reference.md


# Các Lệnh Docker Cơ Bản Sử Dụng Hàng Ngày

## Tổng Quan

Hướng dẫn này bao gồm các lệnh Docker quan trọng nhất mà bạn sẽ sử dụng hàng ngày khi làm việc với microservices. Các lệnh này cũng thường được hỏi trong các buổi phỏng vấn kỹ thuật.

## Các Lệnh Quản Lý Image

### 1. Liệt Kê Docker Images

```bash
docker images
```

Liệt kê tất cả các Docker images có trong Docker server cục bộ của bạn.

### 2. Kiểm Tra Chi Tiết Docker Image

```bash
docker image inspect <image_id>
```

Hiển thị thông tin chi tiết về một image cụ thể. Bạn có thể sử dụng 3-4 ký tự đầu tiên của image ID thay vì ID đầy đủ.

**Lưu ý:** Docker đủ thông minh để phát hiện toàn bộ image ID hoặc container ID dựa trên giá trị ngắn được cung cấp.

### 3. Xóa Docker Image

```bash
docker image rm <image_id>
```

Xóa một hoặc nhiều Docker images. Bạn có thể chỉ định nhiều image IDs cách nhau bởi dấu cách.

**Lệnh thay thế:**
```bash
docker rmi <image_id>
```

### 4. Build Docker Image

```bash
docker build -t <image_name> .
```

Tạo Docker image dựa trên Dockerfile. Cờ `-t` chỉ định tag (tên image).

**Quan trọng:** Đảm bảo Dockerfile có trong cùng vị trí mà bạn chạy lệnh này.

### 5. Push Docker Image

```bash
docker image push <image_name>
```

Đẩy Docker image từ hệ thống cục bộ lên repository từ xa (ví dụ: Docker Hub).

### 6. Pull Docker Image

```bash
docker image pull <image_name>
```

Kéo Docker image từ repository từ xa về hệ thống cục bộ.

### 7. Xóa Images Không Sử Dụng

```bash
docker image prune
```

Xóa tất cả images không được sử dụng. Một image được coi là không sử dụng nếu không có container nào liên kết (đang chạy hoặc đã dừng).

### 8. Xem Lịch Sử Image

```bash
docker history <image_name>
```

Hiển thị tất cả các lớp trung gian và các lệnh được thực thi trong quá trình build image. Hữu ích cho việc debug các vấn đề build image.

## Các Lệnh Quản Lý Container

### 9. Chạy Container

```bash
docker run -p <host_port>:<container_port> <image_name>
```

Khởi động Docker container dựa trên một image với ánh xạ port.

### 10. Liệt Kê Containers Đang Chạy

```bash
docker ps
```

Hiển thị tất cả containers đang chạy.

### 11. Liệt Kê Tất Cả Containers

```bash
docker ps -a
```

Hiển thị tất cả containers, bao gồm cả đang chạy và đã dừng.

### 12. Khởi Động Container

```bash
docker container start <container_id>
```

Khởi động một container đã dừng trước đó. Bạn có thể chỉ định nhiều container IDs cách nhau bởi dấu cách.

### 13. Dừng Container

```bash
docker container stop <container_id>
```

Dừng container đang chạy một cách nhẹ nhàng. Docker server cho container khoảng 5 giây để đóng các tài nguyên (kết nối database, file systems, v.v.) trước khi dừng.

### 14. Kill Container

```bash
docker container kill <container_id>
```

Kill một hoặc nhiều containers đang chạy ngay lập tức mà không đợi graceful shutdown.

**Sự khác biệt giữa Stop và Kill:**
- **Stop:** Cho container ~5 giây để đóng các tài nguyên
- **Kill:** Kết thúc container ngay lập tức

### 15. Tạm Dừng Container

```bash
docker container pause <container_id>
```

Tạm dừng container tạm thời để nó ngừng nhận traffic.

### 16. Tiếp Tục Container

```bash
docker container unpause <container_id>
```

Tiếp tục container đã tạm dừng để nó bắt đầu nhận requests trở lại.

### 17. Khởi Động Lại Container

```bash
docker container restart <container_id>
```

Khởi động lại một hoặc nhiều containers.

### 18. Kiểm Tra Chi Tiết Container

```bash
docker container inspect <container_id>
```

Hiển thị thông tin chi tiết về một container.

### 19. Xem Logs Container

```bash
docker container logs <container_id>
```

Lấy tất cả logs của một container.

**Mẹo:** Sử dụng Docker Desktop thuận tiện hơn để xem logs theo thời gian thực.

### 20. Theo Dõi Logs Container

```bash
docker container logs -f <container_id>
```

Liên tục theo dõi đầu ra logs của container trong terminal. Cờ `-f` yêu cầu Docker theo dõi đầu ra logs liên tục.

### 21. Xem Thống Kê Container

```bash
docker container stats
```

Hiển thị thống kê container bao gồm CPU utilization, memory usage, và I/O usage.

### 22. Thực Thi Lệnh Trong Container Đang Chạy

```bash
docker exec -it <container_id> sh
```

Mở shell bên trong container đang chạy, cho phép bạn thực thi các lệnh trong môi trường của container.

### 23. Xóa Container

```bash
docker rm <container_id>
```

Xóa một hoặc nhiều containers. Bạn có thể chỉ định nhiều container IDs cách nhau bởi dấu cách.

### 24. Xóa Tất Cả Containers Đã Dừng

```bash
docker container prune
```

Xóa tất cả containers đã dừng bằng một lệnh duy nhất. Bạn không cần chỉ định container IDs.

## Các Lệnh Bảo Trì Hệ Thống

### 25. Dọn Dẹp Toàn Hệ Thống

```bash
docker system prune
```

Xóa tất cả:
- Containers đã dừng
- Images không sử dụng
- Networks không sử dụng
- Volumes không sử dụng
- Build cache

### 26. Đăng Nhập Docker Hub

```bash
docker login -u <username>
```

Đăng nhập vào Docker Hub từ CLI. Bạn sẽ được nhắc nhập mật khẩu.

**Lưu ý:** Nếu bạn đang sử dụng Docker Desktop, bạn có thể đăng nhập qua trình duyệt, và CLI của bạn sẽ tự động kết nối với tài khoản Docker Hub.

### 27. Đăng Xuất Docker Hub

```bash
docker logout
```

Đăng xuất khỏi tài khoản Docker Hub Container Registry.

## Các Lệnh Docker Compose

### 28. Khởi Động Services Với Docker Compose

```bash
docker compose up
```

Tạo và khởi động containers dựa trên file Docker Compose.

### 29. Dừng và Xóa Services

```bash
docker compose down
```

Dừng và xóa containers được định nghĩa trong file Docker Compose.

### 30. Dừng Services (Không Xóa)

```bash
docker compose stop
```

Dừng containers mà không xóa chúng.

### 31. Khởi Động Services Đã Tồn Tại

```bash
docker compose start
```

Khởi động containers đã được tạo trước đó (không tạo containers từ đầu).

## Các Thực Hành Tốt Nhất

1. **Sử Dụng Docker Desktop:** Cách thuận tiện nhất để tương tác với Docker images và containers, vì nó cung cấp giao diện người dùng thân thiện.

2. **IDs Ngắn:** Bạn có thể sử dụng 3-4 ký tự đầu tiên của bất kỳ ID nào (image hoặc container) thay vì ID đầy đủ.

3. **Graceful Shutdown:** Ưu tiên `docker container stop` hơn `docker container kill` để cho phép dọn dẹp tài nguyên đúng cách.

4. **Dọn Dẹp Định Kỳ:** Sử dụng các lệnh prune thường xuyên để giải phóng không gian đĩa.

5. **Giám Sát Logs:** Sử dụng Docker Desktop để xem logs theo thời gian thực trong quá trình phát triển.

## Tóm Tắt

Các lệnh Docker này rất cần thiết cho công việc phát triển microservices hàng ngày và thường được đề cập trong các buổi phỏng vấn kỹ thuật. Hãy giữ tài liệu tham khảo này trong tầm tay, và cũng kiểm tra trang GitHub repository để có thêm tài nguyên.

Nhớ rằng: Chọn cách tiếp cận phù hợp nhất với bạn—lệnh CLI hoặc giao diện Docker Desktop UI!




FILE: 48-cloud-native-applications-definition.md


# Ứng Dụng Cloud Native - Định Nghĩa

## Tổng Quan

Bài giảng này giới thiệu các khái niệm cơ bản về ứng dụng cloud native, bao gồm định nghĩa, đặc điểm và mối quan hệ với kiến trúc microservices. Hiểu những khái niệm này là rất quan trọng đối với bất kỳ developer microservice nào, vì chúng tạo nền tảng cho việc xây dựng các ứng dụng hiện đại, có khả năng mở rộng.

## Các Chủ Đề Được Đề Cập

- Định nghĩa về Ứng dụng Cloud Native
- Đặc điểm của Ứng dụng Cloud Native
- Giới thiệu về Phương pháp luận 12 Factor và 15 Factor
- Mối quan hệ giữa Ứng dụng Cloud Native và Microservices

## Ứng Dụng Cloud Native Là Gì?

### Định Nghĩa Đơn Giản (Phi Kỹ Thuật)

Ứng dụng Cloud Native là các ứng dụng phần mềm được thiết kế và phát triển đặc biệt để tận dụng các nguyên tắc điện toán đám mây và khai thác tối đa các công nghệ và dịch vụ cloud native.

Những ứng dụng này:
- Được xây dựng và tối ưu hóa để chạy trong bất kỳ môi trường cloud nào
- Được thiết kế để tận dụng các lợi thế của cloud như:
  - **Khả năng mở rộng (Scalability)** - khả năng phát triển theo nhu cầu
  - **Tính đàn hồi (Elasticity)** - khả năng tự động giảm hoặc tăng tài nguyên
  - **Tính linh hoạt (Flexibility)** - khả năng thích nghi với các yêu cầu thay đổi

> **Nói một cách đơn giản**: Ứng dụng cloud native được xây dựng cho môi trường cloud để các tổ chức có thể tận dụng hoàn toàn các dịch vụ và công nghệ của nhà cung cấp cloud.

### Định Nghĩa Chính Thức (Kỹ Thuật)

Theo **Cloud Native Computing Foundation (CNCF)**:

> *"Các công nghệ cloud native trao quyền cho các tổ chức xây dựng và chạy các ứng dụng có khả năng mở rộng trong các môi trường động hiện đại như public cloud, private cloud và hybrid cloud."*

## Các Công Nghệ Chính Trong Ứng Dụng Cloud Native

Ứng dụng cloud native tận dụng một số công nghệ chính:

1. **Containers** - Đóng gói ứng dụng nhẹ, dễ di chuyển
2. **Service Meshes** - Lớp cơ sở hạ tầng cho giao tiếp giữa các service
3. **Microservices** - Phong cách kiến trúc với các service kết nối lỏng lẻo
4. **Immutable Infrastructure** - Cơ sở hạ tầng được thay thế thay vì sửa đổi
5. **Declarative APIs** - APIs mô tả trạng thái mong muốn của hệ thống

## Tính Linh Hoạt Của Môi Trường Cloud

Ứng dụng cloud native có thể chạy trên bất kỳ loại môi trường cloud nào:

- **Public Cloud** (AWS, Azure, GCP)
- **Private Cloud** (Trung tâm dữ liệu tại chỗ)
- **Hybrid Cloud** (Kết hợp public và private)

Tính linh hoạt này ngăn chặn việc **bị khóa với nhà cung cấp** (vendor lock-in) cụ thể nào.

## Lợi Ích Của Ứng Dụng Cloud Native

### 1. Hệ Thống Có Khả Năng Phục Hồi (Resilient)
- Có thể chịu đựng các lỗi
- Khả năng tự phục hồi
- Tính khả dụng cao

### 2. Hệ Thống Dễ Quản Lý (Manageable)
- Dễ dàng triển khai và cập nhật
- Đơn giản để giám sát và bảo trì
- Hoạt động tự động

### 3. Hệ Thống Có Thể Quan Sát (Observable)
- Khả năng hiển thị hoàn toàn về hành vi ứng dụng
- Giám sát và ghi log thời gian thực
- Số liệu và truy vết toàn diện

### 4. Kiến Trúc Kết Nối Lỏng Lẻo (Loosely Coupled)
- Các service độc lập có thể phát triển riêng biệt
- Dễ dàng kiểm tra từng thành phần
- Giảm sự phụ thuộc giữa các thành phần

## Lợi Ích Trong Phát Triển

Với các công nghệ cloud native và tự động hóa mạnh mẽ, các tổ chức đạt được:

- **Triển Khai Thường Xuyên** - Phát hành thay đổi nhanh chóng và an toàn
- **Thay Đổi Có Thể Dự Đoán** - Quy trình triển khai nhất quán
- **Giảm Thiểu Công Việc Thủ Công** - Giảm công việc thủ công thông qua tự động hóa
- **Thay Đổi Tác Động Cao** - Khả năng đổi mới nhanh chóng
- **Giảm Lỗi** - Kiểm tra và cô lập tốt hơn ngăn chặn các vấn đề hồi quy

## Khả Năng Cải Tiến Nhanh Chóng

Ứng dụng cloud native cho phép các developer:
- Thực hiện các thay đổi nhỏ mà không ảnh hưởng đến toàn bộ hệ thống
- Phát triển các cải tiến mới một cách nhanh chóng
- Triển khai cập nhật với rủi ro tối thiểu
- Kiểm tra các thay đổi một cách độc lập

Điều này có thể thực hiện được nhờ tính chất kết nối lỏng lẻo của kiến trúc.

## Điểm Chính Cần Nhớ

Khi giải thích về ứng dụng cloud native:

- **Đối với đối tượng phi kỹ thuật**: Sử dụng định nghĩa đơn giản tập trung vào tối ưu hóa cloud và các lợi thế
- **Đối với đối tượng kỹ thuật**: Tham khảo định nghĩa chính thức của CNCF và đề cập đến các công nghệ cụ thể

## Nội Dung Tiếp Theo

Trong các bài giảng tiếp theo, chúng ta sẽ khám phá:
- Ứng dụng cloud native liên quan đến microservices như thế nào
- Phương pháp luận 12 Factor và 15 Factor
- Các phương pháp hay nhất để xây dựng ứng dụng cloud native
- Triển khai thực tế với Spring Boot

---

## Tóm Tắt

Ứng dụng cloud native đại diện cho một cách tiếp cận hiện đại trong việc xây dựng phần mềm, tận dụng tối đa khả năng của điện toán đám mây. Bằng cách sử dụng các công nghệ như containers, microservices và declarative APIs, những ứng dụng này đạt được khả năng phục hồi, khả năng quản lý và khả năng quan sát trong khi vẫn duy trì tính linh hoạt trên các môi trường cloud khác nhau. Hiểu những nguyên tắc này là rất quan trọng để phát triển các hệ thống dựa trên microservices thành công.




FILE: 49-dac-diem-ung-dung-cloud-native.md


# Ứng Dụng Cloud Native - Các Đặc Điểm Chính

## Giới Thiệu

Trong bài giảng này, chúng ta sẽ tìm hiểu về các đặc điểm quan trọng của ứng dụng cloud-native. Khi bạn nhìn thấy những đặc điểm này trong bất kỳ ứng dụng nào, bạn có thể dễ dàng xác định chúng là ứng dụng cloud-native.

## Các Đặc Điểm Chính

### 1. Kiến Trúc Microservices

Đặc điểm chính đầu tiên của ứng dụng cloud-native là **microservices**.

- Xây dựng ứng dụng dựa trên microservice có tính **liên kết lỏng lẻo** và **kích thước nhỏ gọn**
- Cung cấp tính linh hoạt để phát triển chúng **song song**
- Cho phép **triển khai và mở rộng độc lập**
- Đây là lợi thế chính của ứng dụng cloud-native
- Ứng dụng cloud-native là một chủ đề rộng hơn, và microservices là một trong những tính năng quan trọng của nó

### 2. Containerization (Đóng Gói Container)

Sau khi xây dựng microservices và tách biệt logic nghiệp vụ, bạn sẽ đóng gói ứng dụng của mình với sự trợ giúp của **Docker** hoặc phần mềm containerization khác.

**Lợi Ích của Container:**
- Ứng dụng được đóng gói và triển khai bằng Docker containers
- Cung cấp **môi trường nhẹ và nhất quán** để chạy ứng dụng
- Làm cho ứng dụng **có tính di động cao** trên các nền tảng và hạ tầng đám mây khác nhau
- Code hoạt động tương tự bất kể môi trường đám mây nào (hệ thống local, AWS, GCP, Azure)
- Tất cả các nền tảng đám mây sẽ hoạt động theo cách rất tương tự

**So Sánh với Ứng Dụng Monolithic:**
- Ứng dụng monolithic không cung cấp sự linh hoạt như vậy
- Đòi hỏi nỗ lực đáng kể để mang lại tính nhất quán trên tất cả các nền tảng đám mây

### 3. Khả Năng Mở Rộng và Đàn Hồi

Ứng dụng cloud-native cung cấp khả năng mở rộng và đàn hồi tuyệt vời.

- Ứng dụng được xây dựng trên microservices và containers có thể dễ dàng **mở rộng theo chiều ngang**
- Có thể xử lý bất kỳ loại lưu lượng truy cập nào đến ứng dụng của bạn
- Việc thêm nhiều instances của dịch vụ cực kỳ dễ dàng
- Có thể đạt được tự động với các nền tảng điều phối container như **Kubernetes**
- Có thể tự động mở rộng ứng dụng microservice với Kubernetes

### 4. Thực Hành DevOps

Ứng dụng cloud-native tuân theo các thực hành DevOps bằng cách áp dụng các nguyên tắc DevOps.

**Lợi Ích:**
- Thúc đẩy **văn hóa hợp tác** giữa các nhóm phát triển và vận hành
- Không có sự đổ lỗi giữa các nhà phát triển và nhóm vận hành
- Tích hợp **continuous integration (CI)**
- Hỗ trợ **continuous delivery (CD)**
- Kích hoạt **quy trình triển khai tự động**
- Tối ưu hóa quy trình phát triển và triển khai phần mềm
- Cung cấp sự linh hoạt hoàn toàn cho tổ chức để lựa chọn:
  - Chỉ Continuous Integration
  - Continuous Delivery
  - Continuous Deployment

### 5. Khả Năng Phục Hồi và Chịu Lỗi

Các ứng dụng được phát triển với các nguyên tắc cloud-native có tính phục hồi và chịu lỗi cao.

**Tính Năng Chính:**
- Có thể chịu đựng mọi loại lỗi
- Sử dụng các kỹ thuật như:
  - Kiến trúc phân tán
  - Cân bằng tải (Load balancing)
  - Khôi phục lỗi tự động
- Đảm bảo **tính sẵn sàng cao** và **khả năng chịu lỗi**

**Ví Dụ Thực Tế:**
- Triển khai một microservice ở nhiều vị trí
- Nếu một vị trí bị ngừng hoạt động (mất điện hoặc sự cố internet), microservice vẫn tiếp tục hoạt động từ các vị trí khác
- Các nền tảng như Kubernetes có thể tự động:
  - Tắt các instances microservice không hoạt động
  - Khởi động các instances mới tự động
- Đảm bảo khôi phục lỗi tự động và khả năng chịu lỗi

### 6. Tận Dụng Các Dịch Vụ Cloud-Native

Ứng dụng cloud-native tận dụng các dịch vụ cloud-native ở mức độ lớn.

**Ưu Điểm:**
- Được phát triển để **tận dụng môi trường đám mây** một cách rộng rãi
- Tổ chức không phải tập trung vào hạ tầng
- Tất cả các dịch vụ được **giám sát và duy trì** bởi nhà cung cấp nền tảng đám mây
- Các nhà phát triển và tổ chức có thể tập trung nhiều hơn vào:
  - Logic ứng dụng
  - Cải thiện logic nghiệp vụ
- Ít tập trung hơn vào các thành phần hạ tầng

## Kết Luận

Đây là tất cả các đặc điểm quan trọng của ứng dụng cloud-native. Trong suốt khóa học này, chúng ta sẽ khám phá tất cả các đặc điểm này trong các phần khác nhau.

Khi bạn thấy một ứng dụng tuân theo tất cả các đặc điểm này, bạn có thể tự tin khẳng định đó là một ứng dụng cloud-native.

---

*Ghi chú: Tài liệu này là một phần của khóa học toàn diện về microservices với Spring Boot và ứng dụng cloud-native.*




FILE: 5-gioi-thieu-spring-boot-framework.md


# Giới Thiệu Spring Boot Framework

## Tổng Quan

Trong bài học này, chúng ta sẽ khám phá Spring Boot framework và hiểu tại sao đây là framework tốt nhất để xây dựng microservices dựa trên Java.

## Spring Boot là gì?

Spring Boot là một framework được xây dựng dựa trên Spring framework, cho phép các lập trình viên phát triển và triển khai các ứng dụng web Java, bao gồm cả microservices, một cách rất dễ dàng. Nó cải thiện đáng kể năng suất của lập trình viên và đơn giản hóa công việc của các nhóm phát triển, nền tảng và vận hành.

### Tính Năng Chính

- **JAR Tự Chứa và Có Thể Thực Thi**: Spring Boot cho phép bạn xây dựng các file JAR tự chứa và có thể thực thi thay vì các file WAR hoặc EAR truyền thống
- **Tập Trung Vào Lập Trình Viên**: Là lập trình viên, bạn chỉ cần tập trung vào logic nghiệp vụ trong khi framework xử lý:
  - Khởi động ứng dụng của bạn
  - Đóng gói ứng dụng của bạn
  - Triển khai ứng dụng vào Tomcat server nhúng hoặc web server

## Ưu Điểm Của Spring Boot Framework

### 1. Tính Năng Tích Hợp Sẵn và Tự Động Cấu Hình

Spring Boot cung cấp nhiều tính năng tích hợp sẵn thông qua:
- **Auto Configuration (Tự động cấu hình)**: Tự động cấu hình ứng dụng dựa trên các dependencies
- **Dependency Injection (Tiêm phụ thuộc)**: Quản lý các phụ thuộc component một cách hiệu quả
- **Hỗ Trợ Cloud Platform**: Hỗ trợ native cho nhiều nền tảng đám mây

#### Ví Dụ Về Tự Động Cấu Hình
Khi tạo ứng dụng web với Spring Boot:
- Tự động triển khai lên web server như Tomcat
- Sử dụng cổng mặc định 8080
- Giả định các giá trị mặc định hợp lý
- Cho phép ghi đè các cấu hình mặc định thông qua properties

### 2. Hỗ Trợ Embedded Server

Spring Boot cung cấp các embedded server như:
- Tomcat
- Jetty
- Undertow

**Lợi Ích:**
- Chạy microservices trực tiếp mà không cần cài đặt server riêng
- Không cần bảo trì server thủ công
- Loại bỏ yêu cầu về web server bên ngoài (Tomcat, JBoss, v.v.)

### 3. Tính Năng Production-Ready

Spring Boot hỗ trợ các tính năng production thiết yếu:
- **Metrics (Số liệu)**: Số liệu hiệu suất ứng dụng
- **Health Monitoring (Giám sát sức khỏe)**: Kiểm tra tình trạng ứng dụng
- **External Configurations (Cấu hình bên ngoài)**: Quản lý cấu hình được externalize

#### Spring Boot Actuator
Với dependency Spring Boot Actuator, bạn có thể dễ dàng:
- Expose các metrics của ứng dụng
- Giám sát thông tin health
- Truy cập chi tiết cấu hình

### 4. Phát Triển Nhanh Với Starter Dependencies

**Bootstrap Nhanh**: Nhanh chóng tạo và bắt đầu code các dự án microservice với starter dependencies

**Trước Spring Boot:**
- Cần cấu hình dependency thủ công
- Thiết lập phức tạp cho database, message queues và frameworks
- Quản lý dependency tốn thời gian

**Với Spring Boot Starter Projects:**
- Chỉ cần khai báo các dependencies cần thiết
- Các dependencies được bundle tự động cung cấp
- Ví dụ: MySQL starter bao gồm tất cả dependencies cần thiết để kết nối database

### 5. Ứng Dụng Sẵn Sàng Cho Cloud

Các microservices được xây dựng với Spring Boot sẵn sàng cho cloud và có thể dễ dàng:
- **Containerized (Đóng gói container)**: Đóng gói ứng dụng với Docker
- **Orchestrated (Điều phối)**: Triển khai lên Kubernetes clusters
- **Cloud Deployed (Triển khai cloud)**: Triển khai lên các cloud providers như AWS, GCP, Azure

## So Sánh Cách Tiếp Cận Truyền Thống vs Spring Boot

### Cách Tiếp Cận Truyền Thống (Trước Spring Boot)
```
┌─────────────────────┐
│  Java Runtime (JVM) │
├─────────────────────┤
│  Web Server         │
│  (Tomcat/Jetty)     │
├─────────────────────┤
│  Application        │
│  (định dạng WAR/EAR)│
└─────────────────────┘
```

**Yêu Cầu:**
- Cài đặt Java Runtime Environment (JVM)
- Cài đặt web servers (Tomcat, Jetty, Netty)
- Đóng gói ứng dụng dưới dạng file WAR hoặc EAR
- Triển khai thủ công lên servers

### Cách Tiếp Cận Spring Boot
```
┌─────────────────────┐
│  Java Runtime (JVM) │
├─────────────────────┤
│  Application JAR    │
│  (với embedded      │
│   server)           │
└─────────────────────┘
```

**Lợi Ích:**
- Embedded server được bao gồm trong application JAR
- Không cần cài đặt server riêng
- Không cần bảo trì cấu hình server
- Dễ dàng hơn cho các nhóm platform và operations

## Self-Contained JARs (Fat JARs / Uber JARs)

Các ứng dụng Spring Boot được đóng gói dưới dạng self-contained JARs, còn được gọi là:
- **Fat JARs**
- **Uber JARs**

**Nội Dung:**
- Tất cả dependencies
- Tất cả business logic
- Embedded server

**Ưu Điểm:**
- Mọi thứ được đóng gói cùng nhau
- Triển khai đơn giản
- Giảm độ phức tạp vận hành

## Tóm Tắt

Spring Boot framework cung cấp:
1. Auto-configuration và các tính năng tích hợp sẵn
2. Hỗ trợ embedded server
3. Các tính năng production-ready (metrics, health monitoring)
4. Phát triển nhanh với starter dependencies
5. Ứng dụng sẵn sàng cho cloud

Những ưu điểm này làm cho Spring Boot trở thành lựa chọn tốt nhất để xây dựng microservices dựa trên Java, cải thiện năng suất lập trình viên và đơn giản hóa vận hành.

## Các Bước Tiếp Theo

Trong các bài học tiếp theo, chúng ta sẽ:
- Xây dựng microservices với Spring Boot (demo thực hành)
- Khám phá Spring Boot Actuator
- Đóng gói ứng dụng với Docker
- Triển khai microservices lên Kubernetes clusters

---

*Tài liệu này bao gồm phần giới thiệu về Spring Boot framework cho phát triển microservices.*




FILE: 50-so-sanh-ung-dung-cloud-native-va-truyen-thong.md


# Ứng Dụng Cloud Native So Với Ứng Dụng Truyền Thống

## Giới Thiệu

Trong bài giảng này, chúng ta sẽ khám phá những khác biệt chính giữa ứng dụng cloud-native và ứng dụng doanh nghiệp truyền thống. Hiểu được những khác biệt này sẽ giúp bạn đánh giá cao những lợi thế của việc áp dụng kiến trúc cloud-native.

## Những Khác Biệt Chính

### 1. Hành Vi Có Thể Dự Đoán vs Không Thể Dự Đoán

**Ứng Dụng Cloud Native:**
- Có **hành vi có thể dự đoán**
- Dễ dàng theo dõi các vấn đề và ngoại lệ
- Logic nghiệp vụ được liên kết lỏng lẻo và tách biệt thành nhiều microservices
- Có thể dễ dàng dự đoán nơi xảy ra ngoại lệ

**Ứng Dụng Truyền Thống:**
- Có **hành vi không thể dự đoán**
- Khó theo dõi các vấn đề
- Tất cả logic nghiệp vụ được gom lại với nhau trong cấu trúc nguyên khối (monolithic)
- Nhà phát triển cần bỏ ra nhiều nỗ lực để debug tất cả các dòng code
- Không thể dễ dàng xác định nơi xảy ra ngoại lệ

**Ví Dụ:**
Trong môi trường microservice, nếu có vấn đề, bạn có thể nhanh chóng xác định microservice nào đang gây ra sự cố. Trong ứng dụng monolithic, bạn phải debug toàn bộ codebase để tìm nguồn gốc của vấn đề.

### 2. Tính Độc Lập Với Hệ Điều Hành

**Ứng Dụng Cloud Native:**
- **Không phụ thuộc vào OS**
- Trừu tượng hóa hệ điều hành
- Hoạt động nhất quán trên các hệ điều hành khác nhau
- Áp dụng Docker containers và Docker images
- Containers trừu tượng hóa lớp OS

**Ứng Dụng Doanh Nghiệp Truyền Thống:**
- **Phụ thuộc vào hệ điều hành**
- Yêu cầu cấu hình OS cụ thể
- Ít tính di động hơn trên các môi trường khác nhau

### 3. Kích Thước và Dung Lượng

**Ứng Dụng Cloud Native:**
- **Kích thước phù hợp** với dung lượng thích hợp
- Hoạt động theo **cách độc lập**
- Mỗi microservice có kích thước tối ưu riêng
- Các dịch vụ có thể mở rộng độc lập

**Ứng Dụng Truyền Thống:**
- Có **dung lượng quá khổ**
- Tất cả logic nghiệp vụ tồn tại trong một ứng dụng hoặc codebase duy nhất
- Các thành phần **phụ thuộc lẫn nhau**
- Không thể mở rộng từng thành phần riêng biệt

### 4. Phương Pháp Phát Triển và Triển Khai

**Ứng Dụng Cloud Native:**
- Hỗ trợ **continuous delivery** với các nguyên tắc DevOps
- Áp dụng **tự động hóa**
- Hỗ trợ phong cách làm việc **Agile**
- Cho phép lặp lại và triển khai nhanh chóng
- Thúc đẩy sự hợp tác giữa các nhóm phát triển và vận hành

**Ứng Dụng Doanh Nghiệp Truyền Thống:**
- Tuân theo phương pháp phát triển **waterfall (thác nước)**
- Không hỗ trợ phong cách làm việc Agile
- Quy trình triển khai thủ công
- Chu kỳ phát hành dài hơn

### 5. Khôi Phục và Khả Năng Mở Rộng

**Ứng Dụng Cloud Native:**
- Hỗ trợ **khôi phục nhanh chóng**
- Cho phép **mở rộng tự động**
- Kubernetes có thể tự động:
  - Tạo instances mới nếu một instance bị lỗi
  - Khôi phục tự động từ các lỗi
  - Mở rộng ứng dụng dựa trên lưu lượng truy cập đến
- Khả năng tự phục hồi (self-healing)

**Ứng Dụng Truyền Thống:**
- Không sử dụng Docker containers
- Không thể dựa vào các nền tảng như Kubernetes
- **Khôi phục cực kỳ chậm**
- Không có phong cách khôi phục tự động
- Không có khả năng mở rộng tự động
- Yêu cầu can thiệp thủ công để mở rộng

## Kết Luận

Từ những khác biệt này, rõ ràng là **ứng dụng cloud-native là người chiến thắng rõ ràng** so với các ứng dụng doanh nghiệp truyền thống.

Ứng dụng cloud-native cung cấp:
- ✅ Khả năng dự đoán tốt hơn
- ✅ Độc lập với hệ điều hành
- ✅ Kiến trúc có kích thước phù hợp
- ✅ Hỗ trợ continuous delivery
- ✅ Khôi phục và mở rộng tự động

### Bước Tiếp Theo

Bây giờ bạn đã hiểu về những lợi thế của ứng dụng cloud-native, bạn có thể tự hỏi:

> **"Có nguyên tắc hoặc hướng dẫn nào mà chúng ta cần tuân theo khi xây dựng các ứng dụng cloud-native này để có được tất cả những lợi thế này không?"**

**Câu trả lời:** Có! Có những hướng dẫn và nguyên tắc tuyệt vời mà chúng ta có thể tuân theo khi xây dựng các ứng dụng cloud-native hoặc microservices. Những nguyên tắc này sẽ được trình bày trong bài giảng tiếp theo.

---

*Ghi chú: Tài liệu này là một phần của khóa học toàn diện về microservices với Spring Boot và ứng dụng cloud-native.*




FILE: 51-12-15-factor-methodology-gioi-thieu.md


# Giới Thiệu về Phương Pháp Luận 12/15-Factor

## Tổng Quan

Bài giảng này cung cấp phần giới thiệu về các nguyên tắc phát triển và tiêu chuẩn cần thiết để xây dựng ứng dụng cloud-native và microservices sử dụng Spring Boot và Java.

## Câu Hỏi Chính

**Làm thế nào để thành công trong việc xây dựng các ứng dụng cloud-native hoặc microservices tốt hơn?**

Câu trả lời nằm ở việc tuân theo các nguyên tắc hướng dẫn và tiêu chuẩn đã được thiết lập.

## Phương Pháp Luận 12-Factor

### Lịch Sử và Nguồn Gốc

- **Năm Giới Thiệu**: 2012
- **Tạo bởi**: Đội ngũ kỹ sư tại Heroku Cloud Platform
- **Mục đích**: 12 nguyên tắc phát triển nhằm hướng dẫn các nhà phát triển trong việc thiết kế và phát triển ứng dụng cloud-native
- **Nền tảng**: Dựa trên kinh nghiệm chuyên môn sâu rộng của đội ngũ Heroku qua nhiều năm xây dựng ứng dụng cloud-native

### Lợi Ích Khi Tuân Theo Phương Pháp Luận 12-Factor

Khi bạn tuân theo phương pháp luận 12-Factor, ứng dụng của bạn sẽ có những lợi thế sau:

1. **Sẵn Sàng Cho Cloud Platform**: Triển khai liền mạch bất kể nền tảng cloud nào bạn chọn
2. **Khả Năng Mở Rộng và Đàn Hồi**: Hỗ trợ sẵn có ở cốt lõi của ứng dụng cloud-native
3. **Tính Di Động Của Hệ Thống**: Ứng dụng có thể chạy trên các hệ thống và môi trường khác nhau mà không gặp vấn đề
4. **Triển Khai Liên Tục**: Hỗ trợ triển khai liên tục và tính linh hoạt

### Tham Khảo

- **Website**: [12factor.net](https://12factor.net)
- **Nội dung**: Mô tả chi tiết về tất cả 12 factors và phương pháp luận

## Phương Pháp Luận 15-Factor

### Sự Phát Triển và Cải Tiến

- **Tác giả**: Kevin Hoffman
- **Sách**: "Beyond the Twelve-Factor App" (Vượt Ra Ngoài Ứng Dụng 12-Factor)
- **Cải tiến**: Thêm 3 nguyên tắc nữa vào 12 factors ban đầu
- **Trạng thái hiện tại**: Phương pháp luận mới nhất và được cập nhật nhất (tính đến nay)

### Tại Sao Cần Cập Nhật?

Ứng dụng 12-Factor ban đầu là một điểm khởi đầu tuyệt vời, nhưng khi công nghệ phát triển từng ngày, một số lĩnh vực cần được xem xét lại để phù hợp với các thực tiễn tốt nhất hiện tại. Phương pháp luận 15-Factor đảm bảo rằng các ứng dụng không chỉ hoạt động trên cloud mà còn **phát triển mạnh mẽ**.

### Mô Tả Sách

> "Năm 2012, người tiên phong cloud Heroku đã phát triển ứng dụng 12 Factor, một tập hợp các quy tắc và hướng dẫn giúp các tổ chức xây dựng ứng dụng cloud-native. Đó là một điểm khởi đầu tuyệt vời, nhưng khi công nghệ thay đổi từng ngày, một số lĩnh vực cần được xem xét lại để phù hợp với các thực tiễn tốt nhất hiện tại. Cuốn sách thực tế này mở rộng các hướng dẫn ban đầu để giúp bạn xây dựng các ứng dụng không chỉ hoạt động trên cloud mà còn phát triển thịnh vượng."

## Tầm Quan Trọng Đối Với Các Nhà Phát Triển

### Tại Sao Các Phương Pháp Luận Này Quan Trọng

1. **Tuân Thủ Tiêu Chuẩn**: Nếu không tuân theo các tiêu chuẩn này, ứng dụng không thể thực sự được gọi là "cloud-native"
2. **Phòng Ngừa Vấn Đề**: Tuân theo các hướng dẫn này giúp tránh các vấn đề phổ biến
3. **Thực Tiễn Tốt Nhất**: Được xây dựng dựa trên kinh nghiệm phát triển rộng rãi với ứng dụng cloud-native
4. **Chuẩn Bị Phỏng Vấn**: Chủ đề phổ biến trong các cuộc phỏng vấn tập trung vào microservices

### Tính Liên Quan Trong Phỏng Vấn

Nếu bạn tham dự một cuộc phỏng vấn tập trung vào microservices, chắc chắn sẽ có câu hỏi về:
- Phương pháp luận 12-Factor
- Phương pháp luận 15-Factor

**Hiểu rõ từng phương pháp luận là rất quan trọng cho sự thành công của bạn.**

## Tiếp Theo Là Gì?

Trong các bài giảng sắp tới, chúng ta sẽ:
- Đi sâu vào từng phương pháp luận trong 15 factors
- Học về chúng theo định dạng dễ hiểu
- Hiểu các ứng dụng và triển khai thực tế

## Tóm Tắt

- **Phương Pháp Luận 12-Factor**: Tập hợp nguyên tắc ban đầu từ Heroku (2012)
- **Phương Pháp Luận 15-Factor**: Phiên bản nâng cao bởi Kevin Hoffman (thực tiễn tốt nhất hiện tại)
- Cả hai đều cung cấp các hướng dẫn thiết yếu để xây dựng ứng dụng cloud-native thành công
- Kiến thức quan trọng cho phát triển microservices và phỏng vấn

---

**Lưu ý**: Mỗi phương pháp luận sẽ được giải thích chi tiết trong các bài giảng tiếp theo, giúp dễ dàng hiểu và áp dụng trong các tình huống thực tế.




FILE: 52-15-factor-methodology-nam-nguyen-tac-dau-tien.md


# Phương Pháp Luận 15-Factor: Năm Nguyên Tắc Đầu Tiên

## Tổng Quan

Tài liệu này bao gồm năm nguyên tắc đầu tiên của phương pháp luận 15-factor để xây dựng microservices cloud-native với Spring Boot. Những hướng dẫn này giúp đảm bảo rằng các microservices có khả năng mở rộng, dễ bảo trì và tuân theo các thực tiễn tốt nhất trong ngành.

---

## 1. Một Codebase Cho Một Ứng Dụng

### Nguyên Tắc
Phải có sự tương ứng một-một giữa một ứng dụng và codebase của nó. Mỗi ứng dụng hoặc microservice nên có codebase riêng biệt.

### Các Điểm Chính
- **Repository Riêng Biệt**: Mỗi microservice nên có repository GitHub riêng hoặc codebase riêng trong hệ thống quản lý phiên bản
- **Quản Lý Code Chung**: Code chung cho nhiều microservices nên được:
  - Quản lý riêng như một thư viện, HOẶC
  - Triển khai như một dịch vụ độc lập (backing service)
- **Build Một Lần**: Bất kể bạn triển khai vào bao nhiêu môi trường, chỉ build và đóng gói codebase một lần duy nhất
- **Không Build Riêng Cho Từng Môi Trường**: Không build lại codebase cho mỗi môi trường (dev, QA, production)

### Lợi Ích
- Tổ chức code tốt hơn và linh hoạt hơn
- Cấu trúc code sạch hơn
- Dễ dàng theo dõi và kiểm soát phiên bản
- Triển khai artifact đơn lẻ trên tất cả môi trường

### Hình Dung
```
Codebase Đơn → Build Một Lần → Triển khai đến:
  ├── Development (Phát triển)
  ├── Testing (Kiểm thử)
  └── Production (Sản xuất)
```

### Thực Hành Tốt Nhất
- Cấu hình theo môi trường (chi tiết database, v.v.) nên được lưu trữ bên ngoài codebase
- Cấu hình được inject từ bên ngoài trong quá trình triển khai
- Cùng một Docker image/artifact được triển khai đến tất cả môi trường

---

## 2. API First (API Là Ưu Tiên)

### Nguyên Tắc
Luôn áp dụng tư duy "API First" khi thiết kế và phát triển ứng dụng cloud-native.

### Các Điểm Chính
- **Thiết Kế Với APIs**: Ngay từ đầu, thiết kế logic nghiệp vụ để được expose thông qua REST APIs
- **Giao Tiếp Microservices**: Mọi thứ trong microservices được phát triển dưới dạng REST APIs
- **Hợp Tác Nhóm**: Các nhóm khác nhau có thể làm việc độc lập trên các APIs khác nhau

### Lợi Ích
1. **Tính Linh Hoạt**: Logic nghiệp vụ có thể được gọi bởi các APIs hoặc microservices khác như backing services
2. **Tích Hợp Có Thể Kiểm Thử**: Viết các bài test tích hợp trong deployment pipeline trước khi triển khai
3. **Sửa Đổi Độc Lập**: Sửa đổi triển khai API bên trong mà không ảnh hưởng đến các ứng dụng phụ thuộc
4. **Phát Triển Song Song**: Nhiều nhóm có thể làm việc đồng thời trên các APIs khác nhau

### Thực Hành Tốt Nhất
Nghĩ "API First" xuyên suốt toàn bộ vòng đời phát triển, từ thiết kế đến triển khai.

---

## 3. Quản Lý Dependency (Phụ Thuộc)

### Nguyên Tắc
Khai báo rõ ràng tất cả các dependency của ứng dụng trong một file manifest duy nhất và đảm bảo chúng có thể truy cập được thông qua dependency manager.

### Các Điểm Chính
- **File Manifest**: Sử dụng `pom.xml` (Maven) hoặc `build.gradle` (Gradle) cho ứng dụng Java
- **Repository Trung Tâm**: Dependencies được tải về từ repository trung tâm (Maven Central)
- **Artifact Đơn Lẻ**: Tất cả dependency libraries được đóng gói thành một artifact duy nhất trong quá trình build

### Cách Hoạt Động

1. **Developer**: Định nghĩa dependencies trong `pom.xml`
2. **Build Tool (Maven/Gradle)**: Đọc file manifest
3. **Kiểm Tra Local**: Kiểm tra xem dependencies có tồn tại trong repository local không
4. **Tải Về**: Nếu không có ở local, tải về từ Maven Central Repository
5. **Lưu Trữ Local**: Lưu các JARs đã tải về trong repository local
6. **Đóng Gói**: Trong quá trình build, tất cả dependencies được đóng gói thành:
   - Một fat JAR duy nhất (Spring Boot), HOẶC
   - Một Docker image

### Lợi Ích
- Quản lý dependency rõ ràng và có kiểm soát
- Không cần tải dependency thủ công
- Build nhất quán trên các môi trường
- Đơn giản hóa quản lý microservices

### Anti-Pattern (Mẫu Không Nên Làm)
❌ **Không Nên**: Tải dependency thủ công và thêm vào classpath (cách làm cũ)
- Trở nên cực kỳ phức tạp với hàng trăm microservices
- Dễ gây lỗi và tốn thời gian

---

## 4. Design, Build, Release, Run (Thiết Kế, Build, Release, Chạy)

### Nguyên Tắc
Codebase của bạn phải tiến triển từ thiết kế đến production bằng cách tuân theo các giai đoạn riêng biệt và tách biệt.

### Bốn Giai Đoạn

#### 1. Giai Đoạn Design (Thiết Kế)
- Xác định các công nghệ, dependencies và công cụ cần thiết
- Bao gồm phát triển và unit testing
- Định nghĩa tất cả yêu cầu kỹ thuật cho microservice

#### 2. Giai Đoạn Build
- Biên dịch và đóng gói codebase với các dependencies
- Tạo một **artifact bất biến** (immutable)
- Gán một số định danh duy nhất (phiên bản: 1.0, 2.0, 3.0, v.v.)
- **Không sửa đổi thủ công** artifact đã đóng gói

#### 3. Giai Đoạn Release
- Kết hợp build artifact với các cấu hình triển khai theo môi trường
- Ví dụ: thông tin database, cấu trúc thư mục, thuộc tính server
- Tạo một release component bất biến
- Gán định danh duy nhất (ví dụ: phiên bản 6.1.5 hoặc timestamp)
- Lưu trữ trong repository trung tâm để dễ dàng rollback

#### 4. Giai Đoạn Run (Chạy)
- Triển khai và chạy ứng dụng trong môi trường được chỉ định
- Sử dụng release artifact cụ thể
- **Không sửa đổi code trong runtime**

### Các Quy Tắc Chính
- ✅ **Duy trì sự tách biệt nghiêm ngặt** giữa các giai đoạn
- ✅ **Artifacts bất biến** - không thay đổi sau khi build
- ✅ **Khả năng tái tạo** - cùng artifact = cùng hành vi
- ❌ **Không sửa đổi runtime** để tránh không khớp

### Lợi Ích
- Dễ dàng rollback về phiên bản trước
- Hành vi nhất quán trên các môi trường
- Deployment pipeline rõ ràng
- Builds có thể tái tạo

---

## 5. Configuration, Credentials và Code (Cấu Hình, Thông Tin Xác Thực và Code)

### Nguyên Tắc
Cấu hình nên được lưu trữ riêng biệt với code và không bao giờ nhúng trong codebase.

### Configuration Là Gì?
Configuration bao gồm các yếu tố thay đổi giữa các lần triển khai:
- Thuộc tính database
- Thuộc tính hệ thống message
- Thông tin xác thực API của bên thứ ba
- Feature flags
- Bất kỳ cài đặt theo môi trường nào

### Các Điểm Chính
- **Lưu Trữ Riêng Biệt**: Duy trì cấu hình trong một codebase riêng
- **Không Có Dữ Liệu Nhạy Cảm Trong Code**: Không bao giờ expose thông tin nhạy cảm trong code repository
- **Runtime Injection**: Inject cấu hình vào thời điểm triển khai dựa trên môi trường
- **Sửa Đổi Độc Lập**: Thay đổi cấu hình mà không cần rebuild ứng dụng

### Các Loại Configuration
1. **Cấu Hình Mặc Định**: Có thể được đóng gói trong ứng dụng
2. **Cấu Hình Theo Môi Trường**: Phải được externalize
   - Cài đặt Development
   - Cài đặt QA
   - Cài đặt Production

### Ví Dụ Configuration
- Username và password database
- Connection strings
- API keys và credentials
- Service endpoints
- Feature flags theo môi trường

### Cách Hoạt Động
```
Codebase Đơn → Build Một Lần → Docker Image
                                    ↓
Triển khai đến Môi trường + Inject Cấu hình Runtime:
  ├── Development (cấu hình dev)
  ├── Testing (cấu hình QA)
  └── Production (cấu hình prod)
```

### Giải Pháp Spring Boot
**Spring Cloud Config Server**: Một project riêng trong hệ sinh thái Spring giúp triển khai hướng dẫn này trong microservices.

### Lợi Ích
- Docker image đơn lẻ cho tất cả môi trường
- Không cần rebuild khi thay đổi môi trường
- Xử lý dữ liệu nhạy cảm an toàn
- Đơn giản hóa quản lý hàng trăm microservices
- Dễ dàng cập nhật cấu hình mà không cần redeploy

### Thực Hành Tốt Nhất
- Lưu trữ cấu hình trong một configuration server tập trung
- Sử dụng các tiêu chuẩn externalization cho dữ liệu nhạy cảm
- Không bao giờ commit thông tin xác thực nhạy cảm vào version control

---

## Tóm Tắt

Năm nguyên tắc đầu tiên này của phương pháp luận 15-factor cung cấp nền tảng vững chắc để xây dựng microservices cloud-native:

1. **Một Codebase** - Một repository cho mỗi microservice
2. **API First** - Thiết kế mọi thứ như APIs
3. **Quản Lý Dependency** - Sử dụng Maven/Gradle để kiểm soát dependency rõ ràng
4. **Design, Build, Release, Run** - Tuân theo các giai đoạn riêng biệt, bất biến
5. **Quản Lý Configuration** - Externalize các cấu hình theo môi trường

Bằng cách tuân theo các hướng dẫn này, bạn đảm bảo rằng microservices của bạn:
- ✅ Có khả năng mở rộng
- ✅ Dễ bảo trì
- ✅ Có thể tái tạo
- ✅ Dễ dàng triển khai trên nhiều môi trường
- ✅ An toàn

---

## Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ thảo luận về các nguyên tắc còn lại của phương pháp luận 15-factor để hoàn thiện hiểu biết của chúng ta về các thực tiễn tốt nhất cho microservices cloud-native.




FILE: 53-15-factor-methodology-nguyen-tac-sau-den-muoi.md


# Phương Pháp Luận 15-Factor: Nguyên Tắc Sáu Đến Mười

## Tổng Quan

Tài liệu này bao gồm các nguyên tắc từ 6 đến 10 của phương pháp luận 15-factor để xây dựng microservices cloud-native với Spring Boot. Những hướng dẫn này tập trung vào các khía cạnh vận hành bao gồm logging, disposability, backing services, environment parity và administrative processes.

---

## 6. Logs (Nhật Ký)

### Thách Thức
Trong các ứng dụng monolithic truyền thống, logs được ghi vào các file tại các vị trí cụ thể trên server. Khi có vấn đề xảy ra, developers phải truy cập thủ công vào các file log này để điều tra. Tuy nhiên, cách tiếp cận này không hiệu quả với kiến trúc microservices khi bạn có thể có hàng trăm services chạy trên nhiều servers.

### Nguyên Tắc
Việc định tuyến và lưu trữ log **không phải** là mối quan tâm của ứng dụng. Ứng dụng không nên ghi logs vào các thư mục hoặc vị trí cụ thể.

### Cách Hoạt Động
1. **Standard Output**: Ứng dụng chỉ đơn giản chuyển hướng logs ra standard output (stdout)
2. **Sequential Events**: Logs được xử lý như các sự kiện tuần tự theo thời gian
3. **External Tool**: Một công cụ log aggregator xử lý việc lưu trữ và rotation logs
4. **Centralized Access**: Log aggregator thu thập, tập hợp và cung cấp quyền truy cập vào tất cả logs để debugging

### Kiến Trúc
```
Accounts Microservice  ──┐
                         ├──> Standard Output ──> Log Aggregator Tool
Loans Microservice     ──┤                         (Lưu Trữ Tập Trung)
                         │                                  │
Cards Microservice     ──┘                                  ↓
                                                    UI Đơn Để Tìm Kiếm
```

### Lợi Ích
- ✅ Quản lý log tập trung cho tất cả microservices
- ✅ Dễ dàng tìm kiếm và debug từ một giao diện duy nhất
- ✅ Không cần truy cập từng server riêng lẻ
- ✅ Đơn giản hóa log rotation và retention policies
- ✅ Tương quan sự kiện tốt hơn giữa các services

### Triển Khai
- Ứng dụng sử dụng các logging framework chuẩn
- Logs được in ra standard output
- Các công cụ log aggregator bên ngoài (ví dụ: ELK Stack, Splunk, CloudWatch) thu thập và index logs
- Operations và development teams truy cập logs thông qua dashboard thống nhất

### Nội Dung Khóa Học
Khóa học này bao gồm một phần riêng biệt trình bày cách triển khai log aggregation, đưa logs từ tất cả microservices vào một công cụ tập trung với UI duy nhất để tìm kiếm và phân tích.

---

## 7. Disposability (Khả Năng Hủy Bỏ)

### Cách Tiếp Cận Truyền Thống vs. Cloud-Native

**Ứng Dụng Monolithic Truyền Thống:**
- Ưu tiên hàng đầu: Giữ ứng dụng luôn chạy
- Không có chỗ cho việc terminate hoặc stop
- Yêu cầu giám sát thủ công

**Ứng Dụng Cloud-Native:**
- Ứng dụng được coi là **ephemeral** (tạm thời)
- Nhiều instances chạy trên các môi trường
- Thay thế và scaling tự động

### Nguyên Tắc
Ứng dụng nên được thiết kế cho **disposability** - chúng có thể được start hoặc stop khi cần thiết mà không gây ra vấn đề.

### Khả Năng Chính

#### 1. Phục Hồi Tự Động
- Các instances không phản hồi có thể bị terminate và thay thế tự động
- Các nền tảng như Kubernetes xử lý điều này mà không cần can thiệp thủ công

#### 2. Auto-Scaling
- Trong thời gian tải cao, các instances bổ sung được spin up tự động
- Khi tải giảm, các instances được shutdown để tiết kiệm tài nguyên

#### 3. Fast Startup (Khởi Động Nhanh)
- Khởi động nhanh cho phép hệ thống linh hoạt
- Đảm bảo tính vững chắc và khả năng phục hồi
- Quan trọng để xử lý workloads động

#### 4. Graceful Shutdown (Tắt Máy Nhẹ Nhàng)
Khi shutdown, ứng dụng phải:
- ✅ Ngừng chấp nhận requests mới
- ✅ Xử lý thành công tất cả requests đang thực hiện
- ✅ Hoàn thành các operations đang chờ
- ✅ Trả jobs về worker queues (đối với worker processes)
- ✅ Thoát sạch sẽ

### Công Nghệ Hỗ Trợ

**Spring Boot + Docker:**
- Tạo và hủy microservices trong vòng **vài giây**

**Virtual Machines Truyền Thống:**
- Mất 10-15 phút để start/stop
- Không phù hợp cho dynamic scaling

### Tích Hợp Kubernetes
Khi sử dụng Docker containers với Kubernetes orchestrator:
- Tự động đáp ứng yêu cầu disposability
- Health checks và restart policies tự động
- Scaling và load balancing liền mạch
- Rolling updates không downtime

### Thực Hành Tốt Nhất
- Thiết kế cho stateless operations khi có thể
- Sử dụng external storage cho state (databases, caches)
- Implement health check endpoints
- Xử lý SIGTERM signals cho graceful shutdown
- Giữ startup time tối thiểu

### Nội Dung Khóa Học
Khóa học này sử dụng Docker ngay từ đầu và giới thiệu Kubernetes vào cuối khóa, chạy tất cả microservices trong Kubernetes cluster để đạt được true disposability.

---

## 8. Backing Services (Dịch Vụ Hỗ Trợ)

### Định Nghĩa
Backing services là các tài nguyên bên ngoài mà microservices của bạn phụ thuộc vào:
- Databases (MySQL, PostgreSQL, MongoDB)
- SMTP servers
- FTP servers
- Caching systems (Redis, Memcached)
- Message brokers (RabbitMQ, Kafka)
- Third-party APIs

### Nguyên Tắc
Xử lý backing services như **attached resources** có thể được sửa đổi hoặc thay thế mà không cần thay đổi code ứng dụng.

### Resource Binding
Kết nối với backing services được thực hiện thông qua **resource binding**, cung cấp:
- URL/endpoint
- Username
- Password
- Các tham số kết nối khác

Những thông tin này nên được cung cấp thông qua **externalized configurations**, không hardcode trong ứng dụng.

### Ví Dụ: Chuyển Đổi Database

Trong suốt vòng đời phát triển phần mềm, các databases khác nhau thường được sử dụng:
- **Development**: Local database hoặc H2
- **Testing**: QA database
- **Production**: Production database

Bằng cách xử lý databases như attached resources, bạn có thể chuyển đổi giữa chúng chỉ bằng cách thay đổi cấu hình:

```
Cùng Docker Image + Cấu Hình Khác Nhau:
├── Development  → Local Database (chỉ đổi config)
├── Testing      → QA Database (chỉ đổi config)
└── Production   → Production Database (chỉ đổi config)
```

### Không Cần Rebuild
- ❌ **Không Nên**: Rebuild Docker image cho mỗi môi trường
- ✅ **Nên**: Sử dụng cùng Docker image với các cấu hình bên ngoài khác nhau

### Chuyển Đổi Backing Services
```
Application
    ├── Local Database (development)
    ├── AWS RDS (testing)
    └── Azure SQL (production)
    
Chỉ thay đổi cấu hình - không thay đổi code!
```

### Lợi Ích
- ✅ Linh hoạt môi trường
- ✅ Dễ dàng thay thế dịch vụ
- ✅ Đơn giản hóa disaster recovery
- ✅ Độc lập với vendor
- ✅ Testing với các providers khác nhau

### Triển Khai
- Sử dụng Spring profiles cho các cấu hình theo môi trường
- Externalize tất cả connection details
- Sử dụng environment variables hoặc configuration servers
- Không bao giờ hardcode credentials hoặc URLs

---

## 9. Environment Parity (Sự Tương Đồng Môi Trường)

### Nguyên Tắc
Giảm thiểu sự khác biệt giữa các môi trường khác nhau và tránh các shortcuts tốn kém. Làm cho tất cả môi trường (development, testing, production) giống nhau nhất có thể.

### Tại Sao Quan Trọng
Khi môi trường trông giống nhau:
- ✅ Ứng dụng hoạt động nhất quán
- ✅ Ít bugs theo môi trường hơn
- ✅ Dễ debugging và troubleshooting hơn
- ✅ Giảm vấn đề "works on my machine"

### Ba Khoảng Cách Cần Giải Quyết

#### 1. Time Gap (Khoảng Cách Thời Gian)
**Vấn Đề**: Thời gian dài giữa code development và production deployment

**Giải Pháp**:
- Áp dụng CI/CD pipelines
- Implement continuous deployment
- Tự động hóa toàn bộ quy trình deployment
- Giảm thời gian từ development đến production

**Lợi Ích**:
- Feedback loops nhanh hơn
- Môi trường được đồng bộ hóa
- Debugging dễ dàng hơn

#### 2. People Gap (Khoảng Cách Con Người)
**Vấn Đề**: Developers xây dựng ứng dụng, nhưng operations teams deploy riêng biệt

**Giải Pháp**:
- Áp dụng **văn hóa DevOps**
- Thúc đẩy sự hợp tác giữa developers và operators
- Tuân theo triết lý: **"You build it, you run it"**

**Lợi Ích**:
- Phối hợp tốt hơn
- Trách nhiệm được chia sẻ
- Ít vấn đề handoff hơn
- Giải quyết vấn đề nhanh hơn

#### 3. Tools Gap (Khoảng Cách Công Cụ)
**Vấn Đề**: Các công cụ và backing services khác nhau giữa các môi trường

**Ví Dụ Thực Hành Xấu**:
```
❌ Development:  H2 Database
❌ Production:   PostgreSQL
```

**Tại Sao Thất Bại**:
- Code được tối ưu hóa cho H2 có thể không hoạt động với PostgreSQL
- Các SQL dialects khác nhau gây ra vấn đề
- Đặc điểm hiệu suất khác nhau
- Bugs chỉ xuất hiện ở production

**Giải Pháp**:
```
✅ Development:  PostgreSQL 14.5
✅ Testing:      PostgreSQL 14.5
✅ Production:   PostgreSQL 14.5
```

### Thực Hành Tốt Nhất
- Sử dụng cùng backing services trên tất cả môi trường
- Duy trì cùng phiên bản của tools và services
- Sử dụng containers để đảm bảo tính nhất quán
- Tự động hóa provisioning môi trường
- Document cấu hình môi trường
- Đồng bộ môi trường thường xuyên

### Lợi Ích
- ✅ Hành vi nhất quán giữa các môi trường
- ✅ Ít bất ngờ ở production hơn
- ✅ Debugging dễ dàng hơn
- ✅ Giảm bugs liên quan đến môi trường
- ✅ Chu kỳ deployment nhanh hơn

---

## 10. Administrative Processes (Quy Trình Quản Trị)

### Định Nghĩa
Administrative processes là các tác vụ quản lý cần thiết để hỗ trợ ứng dụng:
- Database migrations
- Batch jobs để dọn dẹp dữ liệu
- Cập nhật và chuyển đổi dữ liệu
- One-time scripts
- Maintenance tasks

### Nguyên Tắc
Administrative và management tasks nên được xử lý như **isolated processes**, tách biệt với application processes.

### Yêu Cầu Chính

#### 1. Version Control
- Code cho administrative tasks phải được version controlled
- Theo dõi thay đổi giống như application code
- Duy trì lịch sử của migrations và scripts

#### 2. Packaging
- Đóng gói administrative tasks cùng với ứng dụng
- Deploy chúng vào cùng môi trường
- Đảm bảo chúng có sẵn khi cần

#### 3. Execution Environment
- Chạy trong cùng môi trường với ứng dụng
- Sử dụng cùng runtime và dependencies
- Truy cập cùng backing services

### Anti-Pattern Phổ Biến
❌ **Không Bỏ Qua Ở Môi Trường Thấp Hơn**

Developers đôi khi bỏ qua việc chạy administrative tasks ở dev/QA để tiết kiệm thời gian:
- Bỏ qua database migrations
- Không chạy batch jobs
- Bỏ qua maintenance tasks
- Deploy trực tiếp vào production

**Kết Quả**: Thất bại bất ngờ ở production!

### Thực Hành Tốt Nhất

#### Tùy Chọn 1: Independent Microservices (Được Khuyến Nghị)
```
Business Logic Microservice  ──> Chạy liên tục
                                 Phục vụ clients

Administrative Microservice  ──> Chạy một lần
                                 Hủy bỏ khi xong
```

**Lợi Ích**:
- ✅ Tách biệt concerns rõ ràng
- ✅ Có thể hủy bỏ sau khi thực thi
- ✅ Không làm phình to ứng dụng chính
- ✅ Scaling và monitoring độc lập

**Tại Sao Hiệu Quả**:
- Tránh mang logic administrative không cần thiết trong microservice
- Main service chạy liên tục không bị overhead
- Administrative tasks thực thi khi cần và terminate

#### Tùy Chọn 2: Designated Endpoints
Administrative tasks có thể được tích hợp trực tiếp vào ứng dụng:
- Kích hoạt bằng cách gọi các endpoints cụ thể
- Vẫn được tách biệt logic
- Có thể disable ở production

**Lưu Ý**: Mặc dù khả thi, deploy như independent microservices được ưu tiên hơn.

### Ví Dụ

**Database Migration**:
```
Migration Service:
  1. Chạy schema updates
  2. Migrate data
  3. Validate migration
  4. Exit/terminate
```

**Data Cleanup Batch Job**:
```
Cleanup Service:
  1. Xác định records cũ
  2. Archive/delete data
  3. Log results
  4. Exit/terminate
```

### Lợi Ích
- ✅ Kiến trúc sạch
- ✅ Hiệu quả tài nguyên
- ✅ Testing tốt hơn
- ✅ Hành vi nhất quán trên các môi trường
- ✅ Version control đúng đắn
- ✅ Rollback dễ dàng hơn

---

## Tóm Tắt

Các nguyên tắc 6-10 của phương pháp luận 15-factor tập trung vào sự xuất sắc trong vận hành:

### 6. Logs
- Định tuyến logs ra standard output
- Sử dụng external log aggregators
- Tìm kiếm và debug tập trung

### 7. Disposability
- Thiết kế cho fast startup và graceful shutdown
- Cho phép automatic scaling
- Sử dụng Docker + Kubernetes cho ephemeral instances

### 8. Backing Services
- Xử lý external dependencies như attached resources
- Chuyển đổi services qua cấu hình
- Không cần thay đổi code

### 9. Environment Parity
- Giảm thiểu sự khác biệt giữa các môi trường
- Giải quyết time, people và tools gaps
- Sử dụng cùng backing services ở mọi nơi

### 10. Administrative Processes
- Xử lý như isolated, independent processes
- Version control và package với ứng dụng
- Deploy như separate microservices khi có thể

---

## Implementation Stack

Các nguyên tắc này được triển khai trong suốt khóa học bằng cách sử dụng:
- **Spring Boot**: Fast startup và framework support
- **Docker**: Container-based deployment
- **Kubernetes**: Orchestration và auto-scaling
- **Log Aggregators**: Centralized logging solutions
- **Spring Cloud Config**: Externalized configuration
- **CI/CD Pipelines**: Automated deployment

---

## Bước Tiếp Theo

Chúng ta đã đề cập đến 10 trong số 15 nguyên tắc. Trong bài giảng tiếp theo, chúng ta sẽ thảo luận về năm hướng dẫn cuối cùng để hoàn thiện hiểu biết của chúng ta về phương pháp luận 15-factor cho cloud-native microservices.

---

**Key Takeaway**: Những nguyên tắc vận hành này đảm bảo microservices của bạn sẵn sàng cho production, có khả năng mở rộng và dễ bảo trì trong môi trường cloud.




FILE: 54-15-factor-methodology-principles-eleven-to-fifteen.md


# Phương Pháp Luận 15-Factor: Các Nguyên Tắc 11-15 Cho Ứng Dụng Cloud-Native

## Tổng Quan
Bài giảng này thảo luận về năm nguyên tắc cuối cùng của phương pháp luận 15-factor để xây dựng ứng dụng cloud-native và microservices với Spring Boot.

---

## Nguyên Tắc 11: Port Binding (Ràng Buộc Cổng)

### Định Nghĩa
Tất cả các ứng dụng cloud-native phải **độc lập** và expose các dịch vụ của chúng thông qua port binding.

### Các Khái Niệm Chính

#### Ứng Dụng Độc Lập (Self-Contained)
- Ứng dụng **không nên phụ thuộc vào server bên ngoài** trong môi trường thực thi
- Cách tiếp cận truyền thống: Ứng dụng web Java chạy trong các container server bên ngoài (Tomcat, Jetty, Undertow)
- Cách tiếp cận cloud-native: Ứng dụng quản lý server như **embedded dependencies**

#### Triển Khai Với Spring Boot
- Sử dụng **embedded servers** trong ứng dụng
- Mỗi ứng dụng map với server riêng của nó
- Loại bỏ nhu cầu triển khai Tomcat server bên ngoài

#### Thực Hành Tốt Nhất
- ❌ **Không nên**: Triển khai nhiều ứng dụng trong một server
- ✅ **Nên**: Triển khai mỗi ứng dụng trong một server độc lập
- Expose các dịch vụ ra thế giới bên ngoài thông qua **port binding**

#### Tích Hợp Docker
Khi chạy Docker containers:
```bash
docker run -p [host-port]:[container-port]
```
- Sử dụng port forwarding/mapping để expose microservices
- Cho phép microservices hoạt động như backing services cho các ứng dụng khác

### Lợi Ích
- Thực hành phổ biến trong hệ thống cloud-native
- Tạo điều kiện giao tiếp giữa các microservices
- Loại bỏ việc quản lý server thủ công trên các triển khai

---

## Nguyên Tắc 12: Stateless Processes (Quy Trình Không Trạng Thái)

### Định Nghĩa
Thiết kế ứng dụng như **quy trình không trạng thái** với **kiến trúc không chia sẻ** để đạt được khả năng mở rộng cao.

### Tại Sao Stateless?

#### Yêu Cầu Về Khả Năng Mở Rộng
- Ứng dụng cloud-native cần scale động
- Nhiều instances của cùng một microservice chạy đồng thời
- Ví dụ: Accounts microservice scale bằng cách tạo nhiều instances trong thời gian traffic cao

#### Nguyên Tắc Chính
**Tất cả các instances phải stateless và không chia sẻ gì với nhau**

### Vấn Đề Với Ứng Dụng Có Trạng Thái
- Khi instances giữ dữ liệu, việc tắt chúng gây ra **mất dữ liệu**
- Logic nghiệp vụ bị ảnh hưởng
- Không thể scale đáng tin cậy

### Giải Pháp: Data Stores Bên Ngoài

#### Backing Services Để Quản Lý Trạng Thái
Khi cần lưu trữ dữ liệu, sử dụng:
- **Databases** cho dữ liệu persistent
- **Redis cache** cho thông tin caching
- Các data stores khác cho nhu cầu cụ thể

#### Lợi Ích
- Không mất dữ liệu khi instances tắt
- Instances mới có thể đọc từ data store
- Duy trì kiến trúc stateless thực sự

### Không Nên Lưu Gì Trong Instances
- ❌ Thông tin session người dùng
- ❌ Dữ liệu caching
- ❌ Bất kỳ trạng thái tạm thời nào

### Thực Hành Tốt Nhất
> Luôn lưu trữ thông tin trong các hệ thống lưu trữ bên ngoài, làm cho instances của bạn trở thành ứng dụng stateless thực sự.

---

## Nguyên Tắc 13: Concurrency (Xử Lý Đồng Thời)

### Định Nghĩa
Ứng dụng nên hỗ trợ **xử lý đồng thời** để xử lý nhiều người dùng cùng lúc và đạt được khả năng mở rộng thực sự.

### Khả Năng Mở Rộng Vượt Ra Ngoài Stateless
Mặc dù stateless quan trọng, khả năng mở rộng cũng yêu cầu:
- Khả năng phục vụ **số lượng lớn người dùng**
- Khả năng **xử lý đồng thời**
- Xử lý request song song

### Quản Lý Processes

#### Horizontal Scaling (Mở Rộng Ngang)
- Nhiều instances microservice nên xử lý requests **song song**
- Không tuần tự, từng cái một
- Nhiều traffic hơn = cần nhiều processes hơn

#### Vertical vs Horizontal Scalability

**Vertical Scalability (Mở Rộng Dọc)** (❌ Không Khuyến Nghị)
- Tăng RAM và CPU cho một máy duy nhất
- Giới hạn bởi khả năng phần cứng tối đa
- Không thể scale vô hạn

**Horizontal Scalability (Mở Rộng Ngang)** (✅ Khuyến Nghị)
- Tạo nhiều virtual machines với cùng cấu hình
- Triển khai containers/processes trên các máy
- **Không có giới hạn thực tế** cho việc scaling
- Ví dụ: Nhiều VMs với 2GB RAM, 2 CPU mỗi cái

### Java/JVM Concurrency
- Quản lý concurrency được tích hợp sẵn
- Sử dụng **thread pools** với nhiều threads
- Xử lý concurrent requests tự động

### Các Loại Process

#### Web Processes
- Xử lý HTTP requests
- Phục vụ traffic người dùng

#### Worker Processes
- Thực thi scheduled background jobs
- Xử lý các tác vụ bất đồng bộ

### Điểm Chính
> Không có khả năng concurrency trong ngôn ngữ lập trình và kiến trúc của bạn, ứng dụng cloud-native không thể scale hiệu quả.

---

## Nguyên Tắc 14: Telemetry (Đo Xa)

### Định Nghĩa
Ứng dụng cloud-native phải cung cấp **khả năng quan sát toàn diện** thông qua dữ liệu telemetry để giám sát và quản lý từ xa.

### Thách Thức

#### Monolithic vs Cloud-Native
- **Monolithic**: Giám sát 1-2 ứng dụng/servers (dễ dàng)
- **Cloud-Native**: Giám sát hàng trăm containers, services và servers (phức tạp)

### Observability Như Một Đặc Tính Cơ Bản
Truy cập dữ liệu chính xác và toàn diện từ mỗi component hệ thống tại **một vị trí tập trung duy nhất**.

### Các Loại Dữ Liệu Telemetry

1. **Logs** - Thông tin chi tiết để troubleshooting
2. **Metrics** - Đo lường hiệu suất
3. **Traces** - Theo dõi luồng request
4. **Health Status** - Đánh giá sức khỏe hệ thống
5. **Events** - Ghi lại các sự kiện quan trọng

### So Sánh Với Space Probe
Kevin Hoffman so sánh ứng dụng cloud-native với **tàu thăm dò vũ trụ**:
- NASA/ISRO giám sát tàu thăm dò từ xa bằng telemetry
- Nguyên tắc tương tự áp dụng cho ứng dụng cloud-native
- Giám sát và kiểm soát từ xa yêu cầu dữ liệu telemetry

### Chiến Lược Triển Khai
- Ứng dụng phải **cung cấp thông tin telemetry** cho một component tập trung
- Giám sát và kiểm soát hành vi từ vị trí trung tâm này
- Cho phép ra quyết định dựa trên thông tin

### Nội Dung Khóa Học
> Triển khai telemetry chi tiết sẽ được đề cập trong các phần sắp tới của khóa học này.

---

## Nguyên Tắc 15: Authentication & Authorization (Xác Thực & Phân Quyền)

### Định Nghĩa
Triển khai **bảo mật zero-trust** với authentication và authorization phù hợp cho tất cả các giao tiếp trong hệ thống.

### Bảo Mật Như Một Khía Cạnh Quan Trọng
Bảo mật thường không nhận được sự nhấn mạnh xứng đáng trong các hệ thống phần mềm.

### Cách Tiếp Cận Zero-Trust
Mọi giao tiếp và tương tác phải tuân theo các tiêu chuẩn bảo mật:
- Trong hệ thống
- Trong mạng lưới microservices
- Trong các hệ thống cloud-native

### Các Lớp Bảo Mật

#### Trách Nhiệm Của Operations Team
- Giao thức HTTPS
- Chứng chỉ SSL
- Bảo vệ Firewall
- Bảo mật hạ tầng

#### Trách Nhiệm Của Development Team
- **Authentication**
- **Authorization**

### Authentication vs Authorization

#### Authentication (Xác Thực)
- **Theo dõi và xác định** ai đang truy cập ứng dụng
- Thường sử dụng username và password
- Xác minh danh tính người dùng

#### Authorization (Phân Quyền)
- Xảy ra **sau authentication**
- Đánh giá quyền của người dùng
- Xác định người dùng có đủ đặc quyền cho các hành động cụ thể không
- Kiểm soát truy cập tài nguyên

### Triển Khai Trong Khóa Học Này
Một phần riêng sẽ tập trung vào:
- Triển khai bảo mật trong microservices
- Tiêu chuẩn **OAuth 2.1**
- Giao thức **OpenID Connect**
- Thực thi bảo mật thực tế

---

## Tổng Kết

### Tất Cả 15 Nguyên Tắc Của Phương Pháp Luận Factor Đã Được Đề Cập
Các nguyên tắc và hướng dẫn này là thiết yếu để xây dựng ứng dụng cloud-native và microservices thực sự.

### Lưu Ý Quan Trọng

#### Cho Phát Triển
- ✅ Tuân theo tất cả 15 nguyên tắc khi xây dựng microservices
- ✅ Ứng dụng không thể được gọi là "microservices" hoặc "cloud-native" nếu không tuân theo các nguyên tắc này

#### Cho Phỏng Vấn
- Chủ đề phỏng vấn phổ biến
- Tham khảo các nguyên tắc và slides này
- Ôn tập phương pháp luận 15-factor trước khi phỏng vấn

### Các Phần Sắp Tới
Khóa học này sẽ triển khai tất cả các nguyên tắc này một cách thực tế trong khi xây dựng microservices với Spring Boot.

---

## Tài Nguyên
- Slides khóa học được cung cấp để tham khảo
- Các phần sắp tới: triển khai chi tiết
- Phần bảo mật: OAuth 2.1 và OpenID Connect
- Phần telemetry: giám sát và quan sát

---

**Cảm ơn bạn và hẹn gặp lại trong phần tiếp theo!**




FILE: 55-configuration-management-in-microservices.md


# Quản Lý Cấu Hình Trong Microservices

## Giới Thiệu

Quản lý cấu hình là một trong những thách thức quan trọng khi xây dựng microservices hoặc ứng dụng cloud-native. Phần này khám phá các thách thức, giải pháp có sẵn và các phương pháp tốt nhất để quản lý cấu hình trong kiến trúc microservices.

## Các Thách Thức Chính

### 1. Tách Biệt Cấu Hình Khỏi Logic Nghiệp Vụ

**Câu hỏi:** Làm thế nào để tách biệt các cấu hình hoặc thuộc tính khỏi logic nghiệp vụ trong microservices?

**Tại sao điều này quan trọng:**
- Không tách biệt thì không thể tái sử dụng cùng một Docker image cho nhiều môi trường
- Gộp logic nghiệp vụ và cấu hình lại với nhau đòi hỏi phải tạo Docker image riêng cho mỗi môi trường
- Phương pháp này không được khuyến nghị và trở nên khó quản lý với nhiều môi trường

**Phương pháp tốt nhất:** Sử dụng cùng một Docker image cho tất cả môi trường, bao gồm cả production, bằng cách đưa cấu hình ra bên ngoài.

### 2. Tiêm Cấu Hình Tại Runtime

**Câu hỏi:** Làm thế nào để tiêm các cấu hình hoặc thuộc tính tại runtime trong quá trình khởi động microservice?

**Các điểm cần xem xét:**
- Các thuộc tính nhạy cảm như thông tin xác thực không thể được hardcode trong cấu hình hoặc logic nghiệp vụ
- Cấu hình phải được tiêm vào microservices trong quá trình khởi động service
- Bảo mật và tính linh hoạt là tối quan trọng

### 3. Kho Lưu Trữ Cấu Hình Tập Trung

**Câu hỏi:** Làm thế nào để duy trì các cấu hình trong kho lưu trữ tập trung với quản lý phiên bản?

**Vấn đề:**
- Ứng dụng monolithic thường chỉ có 1-2 ứng dụng, giúp việc quản lý cấu hình thủ công khả thi
- Với hàng trăm microservices, quản lý cấu hình thủ công trở nên cực kỳ phức tạp
- Kiểm soát phiên bản và khả năng kiểm tra là thiết yếu

**Giải pháp:** Duy trì tất cả thuộc tính trong kho lưu trữ tập trung với hỗ trợ quản lý phiên bản phù hợp.

## Các Giải Pháp Có Sẵn

Hệ sinh thái Spring Boot cung cấp nhiều giải pháp cho quản lý cấu hình:

### 1. Cấu Hình Spring Boot Cơ Bản
- Cấu hình Spring Boot với các thuộc tính liên quan
- Sử dụng Spring Profiles cho các cấu hình theo môi trường cụ thể
- **Cấp độ:** Giải pháp cơ bản

### 2. Cấu Hình Bên Ngoài
- Áp dụng cấu hình bên ngoài cho ứng dụng Spring Boot
- Cấu hình được lưu trữ bên ngoài ứng dụng
- **Cấp độ:** Giải pháp trung gian

### 3. Spring Cloud Config Server
- Triển khai một configuration server riêng biệt
- Sử dụng dự án Spring Cloud Config Server
- **Cấp độ:** Giải pháp nâng cao và được khuyến nghị

## Phương Pháp Truyền Thống vs. Microservices

### Cấu Hình Ứng Dụng Truyền Thống

**Đặc điểm:**
- Source code và file cấu hình được đóng gói cùng nhau
- Cần rebuild cho mỗi môi trường với các cấu hình khác nhau
- Không đảm bảo hành vi nhất quán giữa các môi trường
- Logic nghiệp vụ có thể khác nhau giữa các môi trường

**Hạn chế:**
- Hoạt động cho ứng dụng monolithic với một ứng dụng
- Không mở rộng được cho kiến trúc microservices
- Nhiều lần build tạo ra sự phức tạp và không nhất quán

### Cấu Hình Microservices (Phương Pháp 15-Factor)

**Nguyên tắc:** Tất cả các cấu hình thay đổi giữa các lần deployment phải được cung cấp bên ngoài build component.

**Ví dụ về Cấu Hình Bên Ngoài:**
- Thông tin xác thực
- URL của các service
- Resource handles
- Cài đặt theo môi trường cụ thể

**Lợi ích:**
- Các artifact của ứng dụng vẫn bất biến trên tất cả môi trường
- Sử dụng một Docker image duy nhất trên tất cả môi trường
- Cấu hình được tiêm từ các vị trí bên ngoài tại runtime

## Quy Trình Được Khuyến Nghị

### Quy Trình Build và Deployment

```
1. Source Code (GitHub Repository)
   ↓
2. Biên dịch & Đóng gói (Build chung)
   ↓
3. Tạo Docker Image (Artifact bất biến)
   ↓
4. Tiêm Cấu Hình tại Runtime
   ↓
5. Triển khai đến Môi trường Đích
```

### Deployment Theo Môi Trường Cụ Thể

**Môi Trường Development:**
- Sử dụng cùng Docker image
- Tiêm cấu hình development tại runtime
- Triển khai đến hạ tầng development

**Môi Trường QA:**
- Sử dụng cùng Docker image
- Tiêm cấu hình QA tại runtime
- Triển khai đến hạ tầng QA

**Môi Trường Production:**
- Sử dụng cùng Docker image
- Tiêm cấu hình production tại runtime
- Triển khai đến hạ tầng production

## Những Điểm Chính Cần Ghi Nhớ

1. **Tách biệt là Quan trọng:** Luôn tách cấu hình khỏi logic nghiệp vụ
2. **Tính Bất Biến:** Build một lần, deploy mọi nơi với cùng một artifact
3. **Tiêm từ Bên Ngoài:** Tiêm cấu hình tại runtime dựa trên môi trường đích
4. **Quản Lý Tập Trung:** Sử dụng kho lưu trữ tập trung cho tất cả cấu hình
5. **Kiểm Soát Phiên Bản:** Duy trì versioning cho tất cả thay đổi cấu hình
6. **Bảo Mật:** Xử lý dữ liệu nhạy cảm thông qua runtime injection, không bao giờ hardcode

## Các Bước Tiếp Theo

Phần này sẽ đề cập:
- Trình diễn chi tiết về tất cả các phương pháp cấu hình
- Ưu điểm và nhược điểm của từng phương pháp
- Các phương pháp hay nhất và khuyến nghị
- Thay đổi code thực tế trong các microservices accounts, loans và cards

## Kết Luận

Quản lý cấu hình là thiết yếu để xây dựng microservices có khả năng mở rộng và dễ bảo trì. Bằng cách tuân theo phương pháp 15-factor và đưa cấu hình ra bên ngoài, chúng ta đảm bảo tính nhất quán, bảo mật và hiệu quả hoạt động trên tất cả các môi trường.

---

**Ghi chú:** Tài liệu này là một phần của khóa học microservices toàn diện sử dụng Spring Boot, bao gồm các triển khai thực tế và các thách thức trong thực tế.




FILE: 56-configuration-management-in-spring-boot-microservices.md


# Quản Lý Cấu Hình trong Spring Boot Microservices

## Giới Thiệu

Trong bài giảng này, chúng ta sẽ khám phá các nguyên tắc cơ bản về quản lý cấu hình trong các ứng dụng Spring Boot, đặc biệt trong bối cảnh kiến trúc microservices. Vì hầu hết các nhà phát triển và tổ chức trong hệ sinh thái Java sử dụng Spring Boot để phát triển microservices, việc hiểu về quản lý cấu hình là rất quan trọng để xây dựng các ứng dụng có khả năng mở rộng và dễ bảo trì.

## Thách Thức về Cấu Hình

### Vấn Đề Cốt Lõi

Thách thức chính mà chúng ta gặp phải là **tách biệt các thuộc tính cho microservices** sao cho cùng một artifact code bất biến có thể được sử dụng trên các môi trường khác nhau (phát triển, QA, production) mà không cần xây dựng lại ứng dụng.

### Mục Tiêu

- Tách biệt cấu hình khỏi mã nguồn
- Tách biệt cấu hình ra bên ngoài để hỗ trợ nhiều môi trường
- Cho phép thay đổi cấu hình mà không cần triển khai lại code

## Tách Biệt Cấu Hình trong Spring Boot

Spring Boot cung cấp hỗ trợ mạnh mẽ cho việc tách biệt cấu hình, cho phép bạn làm việc với cùng một mã ứng dụng trên các môi trường khác nhau mà không cần xây dựng lại.

### Các Phương Pháp Nguồn Cấu Hình

Spring Boot hỗ trợ nhiều phương pháp để cung cấp cấu hình:

1. **Tệp Thuộc Tính**: `application.properties` hoặc `application.yml`
2. **Biến Môi Trường**: Các biến môi trường cấp hệ điều hành
3. **Tham Số Dòng Lệnh**: Các tham số được truyền trong thời gian chạy khi khởi động ứng dụng
4. **Java System Properties**: Các thuộc tính hệ thống JVM
5. **JNDI Attributes**: Các thuộc tính Java Naming and Directory Interface
6. **Servlet Config Init Parameters**: Các tham số khởi tạo Servlet

## Thứ Tự Ưu Tiên Cấu Hình

Khi cùng một thuộc tính được định nghĩa ở nhiều vị trí, Spring Boot tuân theo thứ tự ưu tiên cụ thể (từ thấp đến cao):

1. **Tệp Application Properties/YAML** (Ưu tiên thấp nhất)
2. **Biến Môi Trường Hệ Điều Hành**
3. **Java System Properties**
4. **JNDI Attributes**
5. **Servlet Config Init Parameters**
6. **Tham Số Dòng Lệnh** (Ưu tiên cao nhất)

> **Quan Trọng**: Các giá trị ưu tiên thấp hơn sẽ bị ghi đè bởi các giá trị ưu tiên cao hơn. Tham số dòng lệnh có ưu tiên cao nhất và sẽ ghi đè tất cả các cấu hình khác.

## Hành Vi Cấu Hình Mặc Định

Theo mặc định, Spring Boot tìm kiếm cấu hình trong:
- `application.properties`
- `application.yml` (hoặc `application.yaml`)

Các tệp này được đặt trong vị trí classpath và thường được sử dụng trong các microservices như accounts, loans và cards.

### Hạn Chế của Phương Pháp Mặc Định

Mặc dù tiện lợi, việc lưu trữ tất cả cấu hình trong các tệp thuộc tính trong mã nguồn có những hạn chế:
- Cấu hình được đóng gói cùng với mã nguồn
- Khó thay đổi cấu hình mà không thay đổi code
- Không phù hợp cho các giá trị cụ thể theo môi trường (thông tin đăng nhập database, URLs, v.v.)

## Đọc Thuộc Tính trong Spring Boot

Spring Boot cung cấp ba phương pháp phổ biến để đọc thuộc tính trong logic nghiệp vụ của bạn:

### 1. Annotation @Value

Annotation `@Value` cho phép bạn inject các giá trị thuộc tính riêng lẻ vào các trường Java.

**Cách hoạt động:**
```java
@Value("${property.key.name}")
private String propertyValue;
```

- Định nghĩa một trường Java trong logic nghiệp vụ của bạn
- Đánh dấu nó với `@Value` và chỉ định key thuộc tính
- Spring Boot tự động điền giá trị vào trường trong quá trình khởi động ứng dụng
- Giá trị được giải quyết từ tất cả các nguồn đã cấu hình, tôn trọng thứ tự ưu tiên

**Trường Hợp Sử Dụng**: Đọc các thuộc tính riêng lẻ khi bạn chỉ có một vài giá trị cấu hình.

### 2. Environment Interface

Interface `Environment` cung cấp quyền truy cập vào các thuộc tính từ môi trường runtime của ứng dụng, đặc biệt hữu ích cho các biến môi trường.

**Cách hoạt động:**
```java
@Autowired
private Environment environment;

public void someMethod() {
    String value = environment.getProperty("property.name");
}
```

- Autowire interface `Environment` vào class của bạn
- Sử dụng phương thức `getProperty()` để lấy giá trị thuộc tính
- Truyền tên thuộc tính biến môi trường làm tham số

**Trường Hợp Sử Dụng**: Truy cập các biến môi trường hệ điều hành và thông tin nhạy cảm được cấu hình bởi quản trị viên máy chủ.

### 3. Annotation @ConfigurationProperties (Được Khuyến Nghị)

Đây là phương pháp được khuyến nghị nhất khi xử lý nhiều thuộc tính liên quan.

**Ưu Điểm:**
- Tránh hardcode các key thuộc tính
- Xử lý nhiều thuộc tính một cách hiệu quả
- Cung cấp binding cấu hình an toàn về kiểu dữ liệu
- Tổ chức và bảo trì tốt hơn

**Cách hoạt động:**
```java
@ConfigurationProperties(prefix = "myapp")
public class MyConfig {
    private String property1;
    private int property2;
    
    // Getters và setters
}
```

**Tệp cấu hình:**
```yaml
myapp:
  property1: value1
  property2: 123
```

**Các Điểm Chính:**
- Định nghĩa các thuộc tính với prefix chung trong tệp thuộc tính của bạn
- Tạo một class Java được đánh dấu với `@ConfigurationProperties`
- Chỉ định giá trị prefix trong annotation
- Định nghĩa các trường khớp với tên và kiểu thuộc tính
- Bao gồm getters và setters cho tất cả các trường
- Spring Boot tự động bind các giá trị thuộc tính vào các trường trong quá trình khởi động

**Trường Hợp Sử Dụng**: Quản lý nhiều thuộc tính cấu hình liên quan với tổ chức tốt hơn và an toàn về kiểu dữ liệu.

## So Sánh Các Phương Pháp

| Phương Pháp | Tốt Nhất Cho | Nhược Điểm |
|-------------|--------------|------------|
| @Value | Ít thuộc tính riêng lẻ | Keys bị hardcode, một thuộc tính một lúc |
| Environment | Biến môi trường, dữ liệu nhạy cảm | Truy xuất thủ công, keys bị hardcode |
| @ConfigurationProperties | Nhiều thuộc tính liên quan | Yêu cầu thiết lập class bổ sung |

## Thực Hành Tốt Nhất

1. **Sử dụng @ConfigurationProperties** cho các nhóm thuộc tính liên quan
2. **Tách biệt dữ liệu nhạy cảm** bằng cách sử dụng biến môi trường
3. **Ghi nhớ thứ tự ưu tiên** khi ghi đè thuộc tính
4. **Tài liệu hóa các thuộc tính** của bạn để team hiểu rõ
5. **Sử dụng phương pháp phù hợp** dựa trên số lượng thuộc tính

## Bước Tiếp Theo

Trong các bài giảng sắp tới, chúng ta sẽ:
- Triển khai cả ba phương pháp trong microservices của chúng ta
- Khám phá các demo thực tế của từng phương pháp
- Thảo luận về nhược điểm của các phương pháp cấu hình Spring Boot cơ bản
- Tìm hiểu về quản lý cấu hình nâng cao với Spring Cloud Config Server

## Tóm Tắt

Spring Boot cung cấp quản lý cấu hình linh hoạt thông qua nhiều phương pháp tách biệt. Hiểu thứ tự ưu tiên và chọn phương pháp phù hợp để đọc thuộc tính là điều cần thiết để xây dựng microservices có thể bảo trì. Trong khi các phương pháp cơ bản hoạt động tốt cho các tình huống đơn giản, các ứng dụng doanh nghiệp hưởng lợi từ các giải pháp nâng cao như Spring Cloud Config Server để quản lý cấu hình tập trung.




FILE: 57-reading-properties-with-value-annotation.md


# Đọc Thuộc Tính với Annotation @Value trong Spring Boot

## Tổng Quan

Bài giảng này trình bày cách đọc các thuộc tính từ file cấu hình trong microservices Spring Boot bằng cách sử dụng annotation `@Value`. Chúng ta sẽ cập nhật các microservices để định nghĩa thuộc tính trong `application.yml` và đọc chúng trong code Java.

## Thiết Lập Dự Án

### Tạo Cấu Trúc Dự Án

1. Tạo cấu trúc thư mục mới:
   - `section6/v1-springboot/` - Chứa phiên bản 1 của microservices sử dụng các phương pháp cơ bản của Spring Boot
   - Sao chép các microservices từ section 4: accounts, cards, và loans

2. Mở dự án trong IntelliJ IDEA:
   - Nhấp vào nút **Open**
   - Điều hướng đến vị trí workspace: `microservices/section6/v1-springboot`
   - Chọn thư mục cha và nhấp **Open**
   - Nhấp **Load** để phát hiện tất cả các dự án Maven

## Chuyển Sang Google Jib để Tạo Docker Images

Vì chúng ta đã quyết định sử dụng Google Jib để tạo Docker images, cần cập nhật tất cả microservices:

### Microservice Cards (Đã Sử Dụng Jib)

1. Mở `pom.xml`
2. Điều hướng đến cấu hình Google Jib Maven plugin
3. Đổi tên image thành `s6` (cho section 6)
4. Load các thay đổi Maven
5. Sao chép chi tiết plugin

### Microservice Accounts

1. Xóa `Dockerfile` (không còn cần thiết)
2. Mở `pom.xml`
3. Xóa Spring Boot Maven plugin
4. Thay thế bằng Google Jib Maven plugin
5. Load các thay đổi Maven

### Microservice Loans

1. Mở `pom.xml`
2. Tìm Spring Boot Maven plugin
3. Thay thế bằng Google Jib Maven plugin
4. Load các thay đổi Maven

> **Lưu ý**: `project.artifactId` sẽ tự động tạo tên Docker image khác nhau cho mỗi microservice.

## Định Nghĩa Thuộc Tính trong application.yml

Trong microservice **accounts**, mở `application.yml` và thêm:

```yaml
build:
  version: 1.0
```

Điều này tạo một thuộc tính với key `build.version` và giá trị `1.0`.

## Đọc Thuộc Tính với Annotation @Value

### Bước 1: Tạo Field trong Controller

Trong `AccountsController.java`, thêm một field để chứa giá trị thuộc tính:

```java
@Value("${build.version}")
private String buildVersion;
```

**Giải Thích Cú Pháp**:
- Sử dụng annotation `@Value`
- Tuân theo cú pháp Spring Expression Language (SpEL): `"${property.key}"`
- Property key: `build.version`

### Bước 2: Tạo REST API Endpoint

Thêm một phương thức mới để xuất thông tin build version:

```java
@GetMapping("/build-info")
@Operation(
    summary = "Lấy Thông Tin Build",
    description = "Lấy thông tin build được triển khai vào accounts microservice"
)
@ApiResponses({
    @ApiResponse(
        responseCode = "200",
        description = "HTTP Status OK"
    ),
    @ApiResponse(
        responseCode = "500",
        description = "HTTP Status Internal Server Error",
        content = @Content(
            schema = @Schema(implementation = ErrorResponseDto.class)
        )
    )
})
public ResponseEntity<String> getBuildInfo() {
    return ResponseEntity
            .status(HttpStatus.OK)
            .body(buildVersion);
}
```

## Sửa Lỗi Constructor Autowiring

### Vấn Đề

Khi sử dụng `@AllArgsConstructor`, Lombok tạo constructor với TẤT CẢ các fields, bao gồm `buildVersion`. Spring cố gắng tìm một bean kiểu `String`, nhưng không tồn tại.

### Giải Pháp

1. Xóa annotation `@AllArgsConstructor`
2. Tạo constructor tùy chỉnh cho dependency injection:

```java
private final IAccountService iAccountService;

@Value("${build.version}")
private String buildVersion;

public AccountsController(IAccountService iAccountService) {
    this.iAccountService = iAccountService;
}
```

**Best Practices**:
- Sử dụng từ khóa `final` cho các dependencies được inject
- Annotation `@Autowired` là tùy chọn khi chỉ có một constructor
- Đây là phương pháp được khuyến nghị nhất cho constructor-based dependency injection

## Kiểm Thử API

1. Khởi động accounts microservice ở chế độ debug
2. Ứng dụng khởi động tại cổng 8080
3. Kiểm thử bằng Postman:
   - **Method**: GET
   - **URL**: `http://localhost:8080/api/build-info`
   - **Response**: `1.0`

> **Mẹo**: Import Postman collection từ GitHub repository để truy cập tất cả các API requests đã được cấu hình sẵn.

## Hạn Chế của Phương Pháp @Value Annotation

### Khi Nào Nên Sử Dụng

- **Được Khuyến Nghị**: Chỉ cho 1-2 thuộc tính
- Nhu cầu inject thuộc tính đơn giản

### Nhược Điểm

1. **Không Mở Rộng Được**: Tạo 100 fields cho 100 thuộc tính là không khả thi
2. **Tên Thuộc Tính Hardcoded**: Property keys được hardcode trong annotations
3. **Vấn Đề Bảo Trì**: Khó quản lý trong microservices lớn với nhiều thuộc tính
4. **Không Type Safe**: Giới hạn validation và chuyển đổi kiểu

### Giải Pháp Tốt Hơn

Cho nhiều thuộc tính hoặc cấu hình phức tạp, sử dụng:
- Annotation `@ConfigurationProperties` (sẽ đề cập trong bài giảng tiếp theo)
- Cung cấp cấu hình type-safe binding
- Nhóm các thuộc tính liên quan lại với nhau
- Hỗ trợ validation

## Tóm Tắt

- Thuộc tính có thể được định nghĩa trong `application.yml` hoặc `application.properties`
- Sử dụng `@Value("${property.key}")` để inject giá trị thuộc tính
- Constructor-based dependency injection là phương pháp được khuyến nghị
- Phương pháp này hoạt động tốt cho các tình huống đơn giản với ít thuộc tính
- Cho cấu hình phức tạp, sử dụng `@ConfigurationProperties` thay thế

## Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ khám phá phương pháp thứ hai sử dụng `@ConfigurationProperties` để quản lý thuộc tính mạnh mẽ hơn trong microservices.




FILE: 58-reading-environment-properties-with-environment-interface.md


# Đọc Thuộc Tính Môi Trường với Environment Interface

## Tổng Quan

Bài giảng này trình bày cách thức thứ hai để đọc các thuộc tính trong microservices Spring Boot sử dụng interface `Environment`. Phương pháp này đặc biệt hữu ích cho việc truy cập các biến môi trường được định nghĩa trong môi trường triển khai.

## Tại Sao Sử Dụng Biến Môi Trường?

### Vấn Đề Bảo Mật

- **Thông Tin Nhạy Cảm**: Mật khẩu và dữ liệu nhạy cảm khác không nên được lưu trong file `application.yaml`
- **Bảo Mật Cấu Hình**: Biến môi trường ngăn chặn việc lộ thông tin nhạy cảm
- **Kiểm Soát Truy Cập**: Chỉ quản trị viên máy chủ mới có quyền truy cập vào biến môi trường production
- **Thực Hành Tốt Nhất**: Luôn định nghĩa các chi tiết cấu hình nhạy cảm dưới dạng biến môi trường

## Các Bước Triển Khai

### 1. Autowire Environment Interface

Thêm interface Environment vào controller của bạn:

```java
import org.springframework.core.env.Environment;
import org.springframework.beans.factory.annotation.Autowired;

@Autowired
private Environment environment;
```

**Quan Trọng**: Đảm bảo bạn import đúng Environment interface:
- ✅ Đúng: `org.springframework.core.env.Environment` (Spring Core Framework)
- ❌ Sai: Environment interface của Hibernate

### 2. Tạo REST API để Đọc Thuộc Tính Môi Trường

Ví dụ: Đọc Phiên Bản Java từ JAVA_HOME

```java
@GetMapping("/java-version")
@Operation(
    summary = "Lấy Phiên Bản Java",
    description = "Lấy thông tin phiên bản Java được cài đặt trong accounts microservice"
)
public ResponseEntity<String> getJavaVersion() {
    String javaHome = environment.getProperty("JAVA_HOME");
    return ResponseEntity.ok(javaHome);
}
```

### 3. Kiểm Tra API

**Endpoint**: `/api/java-version`  
**Phương Thức**: `GET`  
**Phản Hồi**: Trả về giá trị của biến môi trường JAVA_HOME

Ví dụ phản hồi:
```
C:\Users\YourUser\.sdkman\candidates\java\current
```

## Ví Dụ Bổ Sung

### Đọc Đường Dẫn Cài Đặt Maven

```java
String mavenHome = environment.getProperty("MAVEN_HOME");
```

**Ví Dụ Phản Hồi**: 
```
C:\apache-maven-3.8.6
```

Điều này cho thấy rõ ràng phiên bản Maven (3.8.6) được cài đặt trên hệ thống.

## Quy Trình Kiểm Tra

1. **Build Ứng Dụng**: Biên dịch dự án sau khi thực hiện thay đổi
2. **Khởi Động Lại Ứng Dụng**: Khởi động lại ở chế độ debug để kiểm tra
3. **Kiểm Tra với Postman**: Gửi yêu cầu GET đến `/api/java-version`
4. **Xác Minh Phản Hồi**: Kiểm tra rằng giá trị biến môi trường được trả về

## Ưu Điểm

- ✅ Truy cập vào các biến môi trường hệ thống
- ✅ Xử lý an toàn thông tin nhạy cảm
- ✅ Triển khai đơn giản với phương thức `getProperty()`

## Nhược Điểm

- ❌ Chỉ có thể đọc một thuộc tính tại một thời điểm
- ❌ Yêu cầu hardcode tên khóa thuộc tính trong mã Java
- ❌ Không được khuyến nghị cho việc đọc nhiều thuộc tính
- ❌ Không mở rộng tốt cho các ứng dụng có nhiều biến môi trường

## Khi Nào Sử Dụng Phương Pháp Này

**Phù Hợp Cho**:
- Đọc 1-2 thuộc tính môi trường
- Truy cập nhanh các biến cấp hệ thống
- Nhu cầu cấu hình đơn giản

**Không Khuyến Nghị Cho**:
- Ứng dụng có nhiều thuộc tính môi trường
- Quản lý cấu hình phức tạp
- Đọc thuộc tính quy mô lớn (sử dụng các phương pháp nâng cao thay thế)

## Điểm Chính Cần Nhớ

1. Interface `Environment` cung cấp truy cập trực tiếp vào các biến môi trường hệ thống
2. Luôn sử dụng Environment interface của Spring Core Framework, không phải của Hibernate
3. Phương pháp này lý tưởng cho việc đọc thuộc tính quy mô nhỏ
4. Đối với nhu cầu phức tạp hơn, hãy xem xét các phương pháp cấu hình nâng cao
5. Biến môi trường tăng cường bảo mật bằng cách giữ dữ liệu nhạy cảm ra khỏi file cấu hình

## Các Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ khám phá **Phương Pháp Thứ Ba** để đọc thuộc tính, giải quyết một số hạn chế của phương pháp này và cung cấp các giải pháp mở rộng hơn cho quản lý cấu hình.

---

**Lưu Ý**: Trong môi trường production, các bản cài đặt Java thường hiển thị đường dẫn thư mục đầy đủ bao gồm tên phiên bản, giúp dễ dàng xác định phiên bản Java chính xác đang được sử dụng.




FILE: 59-configuration-properties-approach.md


# Đọc Nhiều Configuration Properties với @ConfigurationProperties

## Tổng Quan

Bài giảng này trình bày cách tiếp cận thứ ba để đọc các thuộc tính cấu hình trong Spring Boot microservices sử dụng annotation `@ConfigurationProperties`. Cách tiếp cận này cho phép đọc nhiều thuộc tính cùng lúc bằng một POJO class duy nhất, khắc phục các hạn chế của annotation `@Value` và interface `Environment`.

## Hạn Chế của Các Cách Tiếp Cận Trước

Hai cách tiếp cận đầu tiên (annotation `@Value` và interface `Environment`) có một số hạn chế:

1. **Hardcode tên khóa thuộc tính** trong code Java
2. **Chỉ đọc được một thuộc tính tại một thời điểm**
3. **Trùng lặp code** khi cần sử dụng cùng các thuộc tính ở nhiều controller class
4. **Khó bảo trì** khi xử lý nhiều thuộc tính

## Cách Tiếp Cận @ConfigurationProperties

### Bước 1: Định Nghĩa Properties với Prefix Chung

Trong file `application.yml`, định nghĩa các thuộc tính với prefix chung:

```yaml
accounts:
  message: "Chào mừng đến với Accounts Microservice"
  contactDetails:
    name: "Nguyễn Văn A"
    email: "nguyenvana@example.com"
  onCallSupport:
    - "123-456-7890"
    - "098-765-4321"
```

**Các Điểm Quan Trọng:**
- Tất cả thuộc tính chia sẻ prefix chung (`accounts`)
- Thuộc tính có thể là string đơn giản, map, hoặc list
- Hỗ trợ các thuộc tính lồng nhau

### Bước 2: Tạo POJO Class

Tạo DTO class để đại diện cho các thuộc tính cấu hình. Bạn có thể sử dụng POJO class truyền thống hoặc Java Record (giới thiệu trong Java 17).

#### Sử Dụng Java Record (Khuyến Nghị)

```java
public record AccountsContactInfoDto(
    String message,
    Map<String, String> contactDetails,
    List<String> onCallSupport
) {}
```

**Lợi Ích của Java Record:**
- Hoạt động như một data carrier bất biến
- Tự động tạo constructor, getter, `equals()`, `hashCode()`, và `toString()`
- Không có phương thức setter (các field là final)
- Code sạch hơn và ngắn gọn hơn

### Bước 3: Đánh Dấu với @ConfigurationProperties

Thêm annotation `@ConfigurationProperties` vào DTO class:

```java
@ConfigurationProperties(prefix = "accounts")
public record AccountsContactInfoDto(
    String message,
    Map<String, String> contactDetails,
    List<String> onCallSupport
) {}
```

**Quan Trọng:** Giá trị prefix phải khớp với prefix được định nghĩa trong `application.yml`.

### Bước 4: Kích Hoạt Configuration Properties

Trong Spring Boot main class, kích hoạt configuration properties:

```java
@SpringBootApplication
@EnableConfigurationProperties(AccountsContactInfoDto.class)
public class AccountsApplication {
    public static void main(String[] args) {
        SpringApplication.run(AccountsApplication.class, args);
    }
}
```

### Bước 5: Sử Dụng Configuration trong Controller

Inject và sử dụng configuration DTO trong controller:

```java
@RestController
@RequestMapping("/api")
public class AccountsController {
    
    @Autowired
    private AccountsContactInfoDto accountsContactInfoDto;
    
    @GetMapping("/contact-info")
    @Operation(
        summary = "Lấy Thông Tin Liên Hệ",
        description = "Thông tin liên hệ có thể được sử dụng trong trường hợp có vấn đề"
    )
    public AccountsContactInfoDto getContactInfo() {
        return accountsContactInfoDto;
    }
}
```

## Cách Hoạt Động

1. Trong quá trình khởi động ứng dụng, Spring Boot đọc tất cả các thuộc tính với prefix `accounts`
2. Spring tạo bean của `AccountsContactInfoDto` và ánh xạ các giá trị thuộc tính vào các field
3. Bean có sẵn để dependency injection trong toàn bộ ứng dụng
4. Tên field trong DTO class phải khớp với tên thuộc tính trong `application.yml`
5. Kiểu dữ liệu phải tương thích (String, Map<String, String>, List<String>, v.v.)

## Kiểm Thử API

Sau khi triển khai, bạn có thể kiểm thử API bằng Postman hoặc bất kỳ HTTP client nào:

**Request:**
```
GET http://localhost:8080/api/contact-info
```

**Response:**
```json
{
  "message": "Chào mừng đến với Accounts Microservice",
  "contactDetails": {
    "name": "Nguyễn Văn A",
    "email": "nguyenvana@example.com"
  },
  "onCallSupport": [
    "123-456-7890",
    "098-765-4321"
  ]
}
```

## Ưu Điểm của @ConfigurationProperties

1. **Cấu hình type-safe** - Xác thực kiểu thuộc tính tại thời điểm compile
2. **Single source of truth** - Một DTO class cho tất cả các thuộc tính liên quan
3. **Không hardcode** - Tên thuộc tính không được hardcode trong business logic
4. **Tái sử dụng** - Inject cùng một DTO ở bất kỳ đâu trong ứng dụng
5. **Khả năng mở rộng** - Dễ dàng xử lý hàng trăm thuộc tính
6. **Được khuyến nghị bởi Spring Team** - Best practice chính thức

## So Sánh với Các Cách Tiếp Cận Khác

| Cách Tiếp Cận | Thuộc Tính Đơn | Nhiều Thuộc Tính | Type Safety | Tái Sử Dụng | Khuyến Nghị |
|---------------|----------------|------------------|-------------|-------------|-------------|
| @Value | ✓ | ✗ | ✗ | ✗ | ✗ |
| Environment | ✓ | ✗ | ✗ | Hạn chế | Chỉ cho biến môi trường |
| @ConfigurationProperties | ✓ | ✓ | ✓ | ✓ | ✓ |

## Best Practices

1. **Sử dụng prefix có ý nghĩa** phản ánh tên microservice hoặc tính năng của bạn
2. **Khớp chính xác tên field** với tên thuộc tính trong file cấu hình
3. **Sử dụng kiểu dữ liệu phù hợp** (String, Map, List) dựa trên cấu trúc thuộc tính
4. **Cân nhắc sử dụng Java Records** cho các configuration DTO bất biến
5. **Sử dụng @ConfigurationProperties cho application properties**, Environment interface cho biến môi trường

## Các Bước Tiếp Theo

Cách tiếp cận này hoạt động tốt cho một môi trường duy nhất, nhưng nếu bạn cần các giá trị thuộc tính khác nhau cho các môi trường khác nhau (dev, QA, production) thì sao?

Trong bài giảng tiếp theo, chúng ta sẽ khám phá các tính năng nâng cao của Spring Boot để quản lý cấu hình đặc thù cho từng môi trường bằng cách sử dụng **Spring Profiles**.

## Tóm Tắt

- `@ConfigurationProperties` là cách tiếp cận trưởng thành và được khuyến nghị nhất để đọc các thuộc tính cấu hình
- Nó loại bỏ việc trùng lặp code và hardcode tên thuộc tính
- Java Records cung cấp cách clean để tạo các configuration DTO bất biến
- Các thuộc tính được tự động ánh xạ vào các POJO field trong quá trình khởi động ứng dụng
- Cách tiếp cận này mở rộng tốt cho các ứng dụng có nhiều thuộc tính cấu hình




FILE: 6-kien-thuc-co-ban-ve-rest-services.md


# Kiến Thức Cơ Bản Về REST Services

## Giới Thiệu

Khi xây dựng microservices với Spring Boot framework, chúng ta cần xây dựng REST services. Cuối cùng, một microservice là một dịch vụ expose business logic của nó cho các API khác hoặc ứng dụng UI bên ngoài thông qua REST API.

## REST Service Là Gì?

REST services hoạt động dựa trên giao thức HTTP so với các web services dựa trên SOAP. REST services rất nhẹ vì chúng có thể hoạt động với định dạng dữ liệu nhẹ là JSON. Đó là lý do tại sao REST là phương pháp phổ biến nhất để thiết lập giao tiếp giữa hai ứng dụng web.

### Đặc Điểm Chính

- **Nhẹ**: Sử dụng định dạng dữ liệu JSON
- **Dựa trên HTTP**: Hoạt động trên giao thức HTTP
- **Được Sử Dụng Rộng Rãi**: Phương pháp phổ biến nhất cho giao tiếp giữa các ứng dụng

## Các Mô Hình Giao Tiếp

### Giao Tiếp Đồng Bộ (Synchronous Communication)

Sử dụng REST services, chúng ta có thể thiết lập giao tiếp đồng bộ giữa nhiều API, services hoặc ứng dụng web.

**Giao tiếp đồng bộ** có nghĩa là khi một request đến từ ứng dụng bên ngoài đến microservice, ứng dụng bên ngoài sẽ đợi response trước khi tiếp tục request tiếp theo.

> **Lưu ý**: Giao tiếp đồng bộ không phải là tùy chọn duy nhất để xây dựng microservices. Microservices bất đồng bộ có thể được xây dựng bằng message queues và Kafka.

## Các Kịch Bản Sử Dụng REST Service

Khi chúng ta xây dựng services với REST APIs, ứng dụng web của chúng ta expose các endpoints mà ứng dụng client có thể gọi bằng cách gửi requests.

### Các Kịch Bản Phổ Biến:

1. **UI đến Backend Server**: Ứng dụng frontend giao tiếp với backend servers thông qua REST API
2. **Service đến Service**: Các backend servers hoặc microservices khác nhau giao tiếp với nhau qua REST API
3. **Frameworks Web Hiện Đại**: Các UI frameworks như Angular và React fetch hoặc lưu trữ dữ liệu trong backend databases thông qua REST services

## HTTP Methods và CRUD Operations

REST APIs hỗ trợ các thao tác CRUD (Create, Read, Update, Delete) trong hệ thống lưu trữ. Khi xây dựng APIs expose các thao tác này, bạn phải tuân theo các tiêu chuẩn của HTTP methods.

### Tiêu Chuẩn HTTP Methods

| Thao Tác | HTTP Method | Mô Tả |
|----------|-------------|-------|
| **Create** | POST | Sử dụng khi lưu hoặc tạo dữ liệu |
| **Read** | GET | Sử dụng khi đọc dữ liệu từ hệ thống lưu trữ và gửi cho client |
| **Update** | PUT | Sử dụng khi cập nhật toàn bộ record hoặc dữ liệu chính |
| **Update** | PATCH | Sử dụng khi cập nhật cột cụ thể hoặc một phần thông tin nhỏ |
| **Delete** | DELETE | Sử dụng khi client muốn xóa dữ liệu |

### Thực Hành Tốt Nhất

- **POST**: Để tạo dữ liệu mới
- **GET**: Cho các thao tác chỉ đọc
- **PUT**: Để cập nhật toàn bộ records
- **PATCH**: Cho cập nhật một phần
- **DELETE**: Cho các thao tác xóa

## Tiêu Chuẩn Phát Triển REST API

Khi xây dựng REST services và microservices, hãy tuân theo các tiêu chuẩn thiết yếu sau:

### 1. Xác Thực Đầu Vào (Input Validation)

**Tại sao quan trọng**: 
- Ứng dụng UI có HTML forms và input elements để validation
- REST APIs có thể được gọi bởi bất kỳ ứng dụng nào (backend, mobile, v.v.)
- Bạn không thể dựa vào validations xảy ra trong hệ thống bên ngoài

**Khuyến nghị**: Luôn thực hiện xác thực đầu vào đúng cách trên REST APIs của bạn và xử lý requests tương ứng.

### 2. Xử Lý Ngoại Lệ (Exception Handling)

**Tại sao quan trọng**:
- Clients cần hiểu những vấn đề xảy ra với APIs của bạn
- Không có thông báo lỗi phù hợp, clients không thể xác định dữ liệu nào sai hoặc tại sao thao tác thất bại
- Ngăn chặn sự can thiệp và giải thích thủ công

**Khuyến nghị**: 
- Xử lý đúng cả runtime exceptions và business exceptions
- Luôn gửi responses có ý nghĩa cho clients
- Bao phủ tất cả các kịch bản với exception handling

### 3. Tài Liệu API (API Documentation)

**Tại sao quan trọng**:
- Microservices có thể có hàng trăm hoặc hàng nghìn REST services
- Clients bên ngoài cần biết:
  - Định dạng request
  - Quy tắc validation
  - Định dạng response
  - Các thao tác được hỗ trợ

**Khuyến nghị**:
- Tài liệu hóa REST services sử dụng các tiêu chuẩn như:
  - **OpenAPI Specification**
  - **Swagger**
- Giúp onboarding clients mới dễ dàng hơn nhiều
- Giảm nhu cầu về các phiên chuyển giao kiến thức thủ công

### Lợi Ích Của Tài Liệu Hóa Đúng Cách

Khi bạn tài liệu hóa REST services tốt với các tiêu chuẩn này:
- Cuộc sống của bạn trở nên dễ dàng hơn khi quản lý số lượng lớn APIs
- Clients có thể tự phục vụ mà không cần hỗ trợ liên tục
- Giảm độ phức tạp khi onboarding các consumers mới
- Loại bỏ các giải thích qua email hoặc phiên KT phức tạp

## Tóm Tắt

Để xây dựng REST services sẵn sàng cho production với Spring Boot framework:

1. ✅ Tuân theo tiêu chuẩn HTTP methods cho các thao tác CRUD
2. ✅ Triển khai xác thực đầu vào đúng cách
3. ✅ Xử lý exceptions một cách có ý nghĩa
4. ✅ Tài liệu hóa services sử dụng OpenAPI/Swagger

Các tiêu chuẩn này đảm bảo bạn ở vị trí tốt để xây dựng services sẵn sàng cho production cho các dự án thực tế.




FILE: 60-spring-boot-profiles-configuration.md


# Spring Boot Profiles cho Cấu Hình Theo Môi Trường

## Tổng Quan

Spring Boot profiles cung cấp một cơ chế mạnh mẽ để quản lý các cấu hình theo từng môi trường cụ thể trong các ứng dụng microservices. Tính năng này cho phép bạn duy trì các giá trị thuộc tính khác nhau cho các môi trường khác nhau mà không cần xây dựng lại ứng dụng.

## Thách Thức

Khi triển khai microservices trên nhiều môi trường (development, QA, production), việc sử dụng cùng một giá trị thuộc tính cho tất cả các môi trường tạo ra những thách thức đáng kể:

- Thông tin xác thực cơ sở dữ liệu phải khác nhau giữa các môi trường
- Cài đặt cấu hình cần các giá trị cụ thể cho từng môi trường
- Yêu cầu bảo mật thay đổi theo môi trường
- Phân bổ tài nguyên khác nhau dựa trên nhu cầu môi trường

## Spring Boot Profiles Là Gì?

Spring Boot profiles là công cụ để nhóm các cấu hình và thuộc tính dựa trên môi trường mục tiêu. Chúng cho phép bạn:

- Tạo các bộ file cấu hình khác nhau
- Kích hoạt cấu hình cụ thể dựa trên môi trường hiện tại
- Chạy cùng một mã nguồn với các thuộc tính riêng cho từng môi trường
- Kiểm soát việc tạo bean dựa trên profile đang hoạt động

## Lợi Ích Của Việc Sử Dụng Profiles

1. **Tính Linh Hoạt Theo Môi Trường**: Các giá trị cấu hình khác nhau cho các môi trường khác nhau
2. **Mã Nguồn Duy Nhất**: Cùng một mã nguồn chạy trong tất cả các môi trường với các cấu hình khác nhau
3. **Kiểm Soát Bean**: Tạo bean có điều kiện dựa trên profile đang hoạt động
4. **Không Cần Xây Dựng Lại**: Kích hoạt các profile khác nhau mà không cần xây dựng lại ứng dụng

## Profile Mặc Định

Theo mặc định, Spring Boot kích hoạt **profile mặc định**. Tất cả các thuộc tính được định nghĩa trong:
- `application.properties`
- `application.yml`

Các file này thuộc về profile mặc định và luôn được kích hoạt trừ khi bị ghi đè.

## Tạo Profiles Tùy Chỉnh

Để tạo các profile theo môi trường cụ thể, hãy tuân theo quy ước đặt tên sau:

### Đối Với File Properties:
```
application-{tên-profile}.properties
```

### Đối Với File YAML:
```
application-{tên-profile}.yml
```

### Ví Dụ:
- `application-prod.yml` - Profile production
- `application-qa.yml` - Profile QA
- `application-dev.yml` - Profile development

## Kích Hoạt Profiles

### Sử Dụng Thuộc Tính Cấu Hình

Đặt profile hoạt động bằng thuộc tính `spring.profiles.active`:

```yaml
spring:
  profiles:
    active: prod
```

### Kích Hoạt Nhiều Profiles

Bạn có thể kích hoạt nhiều profile cùng lúc bằng các giá trị phân cách bằng dấu phẩy:

```yaml
spring:
  profiles:
    active: prod,monitoring,security
```

### Kích Hoạt Từ Dòng Lệnh

Kích hoạt profile khi khởi động ứng dụng:

```bash
java -jar application.jar --spring.profiles.active=prod
```

### Biến Môi Trường

Đặt qua biến môi trường:

```bash
export SPRING_PROFILES_ACTIVE=prod
```

## Ví Dụ Cấu Trúc Profile

Với ba profile được cấu hình, cấu trúc ứng dụng của bạn sẽ là:

```
src/main/resources/
├── application.yml (profile mặc định)
├── application-dev.yml (profile development)
├── application-qa.yml (profile QA)
└── application-prod.yml (profile production)
```

## Thực Hành Tốt Nhất

### 1. Không Xây Dựng Lại Cho Các Môi Trường Khác Nhau

Một khi ứng dụng của bạn đã được xây dựng và đóng gói, nó **không nên được sửa đổi**. Điều này đặc biệt quan trọng trong kiến trúc microservices, nơi việc xây dựng lại cho từng môi trường là:
- Phức tạp và rườm rà
- Tốn thời gian
- Dễ xảy ra lỗi
- Không có khả năng mở rộng

### 2. Xử Lý Thông Tin Nhạy Cảm Cẩn Thận

Đối với thông tin nhạy cảm không thể lưu trữ trong file cấu hình:
- Cung cấp thuộc tính từ bên ngoài trong quá trình khởi động ứng dụng
- Sử dụng biến môi trường
- Tận dụng hệ thống quản lý bí mật (HashiCorp Vault, AWS Secrets Manager, v.v.)
- Xem xét Spring Cloud Config Server

### 3. Tổ Chức Profile

- **Profile Mặc Định**: Cài đặt phát triển cục bộ
- **Profile Dev**: Môi trường phát triển
- **Profile QA**: Môi trường kiểm thử
- **Profile Prod**: Môi trường sản xuất

### 4. Thứ Tự Ưu Tiên Thuộc Tính

Spring Boot tuân theo thứ tự cụ thể khi tải thuộc tính:
1. Thuộc tính theo profile cụ thể (`application-{profile}.yml`)
2. Thuộc tính profile mặc định (`application.yml`)
3. Nguồn cấu hình bên ngoài

## Cân Nhắc Cho Microservices

Trong kiến trúc microservices, profiles trở nên quan trọng hơn:

- **Khả Năng Mở Rộng**: Quản lý hàng chục hoặc hàng trăm dịch vụ
- **Tính Nhất Quán**: Đảm bảo tất cả các dịch vụ tuân theo cùng một chiến lược profile
- **Triển Khai**: Kích hoạt profile chính xác trong quá trình điều phối
- **Quản Lý Cấu Hình**: Cấu hình tập trung khi có thể

## Kiểm Soát Việc Tạo Bean

Bạn có thể tạo bean có điều kiện dựa trên profile đang hoạt động bằng annotation `@Profile`:

```java
@Configuration
public class DatabaseConfig {
    
    @Bean
    @Profile("dev")
    public DataSource devDataSource() {
        // Cấu hình cơ sở dữ liệu development
    }
    
    @Bean
    @Profile("prod")
    public DataSource prodDataSource() {
        // Cấu hình cơ sở dữ liệu production
    }
}
```

## Tùy Chọn Cấu Hình Bên Ngoài

Khi thuộc tính không thể được duy trì trong file cấu hình, hãy xem xét:

1. **Tham số dòng lệnh**
2. **Biến môi trường**
3. **File cấu hình bên ngoài**
4. **Spring Cloud Config Server**
5. **Công cụ quản lý bí mật**
6. **Kubernetes ConfigMaps và Secrets**

## Tóm Tắt

Spring Boot profiles cung cấp:
- Quản lý cấu hình theo môi trường cụ thể
- Tính linh hoạt mà không cần thay đổi mã nguồn
- Một artifact xây dựng duy nhất cho tất cả các môi trường
- Tạo bean có kiểm soát
- Quy trình triển khai đơn giản hóa

Cách tiếp cận này đảm bảo microservices của bạn có thể được triển khai trên các môi trường khác nhau một cách hiệu quả trong khi vẫn duy trì tính nhất quán và bảo mật.

## Các Bước Tiếp Theo

Trong các phần sắp tới, chúng ta sẽ thực hiện:
- Tạo profile QA và production cho accounts microservice
- Cấu hình thuộc tính theo môi trường cụ thể
- Kích hoạt profile trong các kịch bản triển khai khác nhau
- Quản lý thông tin xác thực nhạy cảm từ bên ngoài

---

**Ghi Nhớ**: Xây dựng một lần, triển khai mọi nơi với các cấu hình khác nhau bằng cách sử dụng Spring Boot profiles!




FILE: 61-implementing-spring-boot-profiles-in-microservices.md


# Triển Khai Spring Boot Profiles trong Microservices

## Giới Thiệu

Hướng dẫn này minh họa cách triển khai thực tế Spring Boot profiles trong accounts microservice. Cách tiếp cận tương tự có thể áp dụng cho các microservices khác như loans và cards.

## Tạo File Cấu Hình Theo Profile

### Bước 1: Tạo File YAML Theo Profile

Tạo hai file YAML bổ sung trong thư mục `resources` cùng với file `application.yml` hiện có:

1. **Profile QA**: `application-qa.yml`
2. **Profile Production**: `application-prod.yml`

Cấu trúc thư mục resources của bạn sẽ như sau:

```
src/main/resources/
├── application.yml (profile mặc định)
├── application-qa.yml (profile QA)
└── application-prod.yml (profile production)
```

## Xác Định Thuộc Tính Theo Môi Trường

### Thuộc Tính KHÔNG Nên Thay Đổi

Một số thuộc tính nên giữ nguyên trong tất cả các môi trường:

- **Cổng Server**: Giữ số cổng nhất quán giữa các môi trường
- **Cấu Hình Database**: Cài đặt cơ sở dữ liệu H2 (trong ví dụ này)
- **Cấu Hình Tĩnh**: Các giá trị không thay đổi theo môi trường

### Thuộc Tính NÊN Thay Đổi

Xác định các thuộc tính cần giá trị khác nhau cho mỗi môi trường:

- **Build Version**: Theo dõi các phiên bản khác nhau trong mỗi môi trường
- **Thông Điệp Ứng Dụng**: Thông điệp cụ thể cho từng môi trường
- **Chi Tiết Liên Hệ**: Thông tin liên hệ hỗ trợ khác nhau cho mỗi môi trường
- **Cài Đặt Riêng**: API endpoints, timeouts, v.v.

## Cấu Hình Profile Mặc Định

### application.yml (Profile Mặc Định)

```yaml
# Profile mặc định cho phát triển cục bộ
build:
  version: "3.0"

accounts:
  message: "Chào mừng đến EasyBank Accounts - APIs Phát Triển Cục Bộ"
  contactDetails:
    name: "John Doe - Lập Trình Viên"
    email: "john.doe@easybank.com"
  onCallSupport:
    - "(555) 123-4567"
    - "(555) 123-4568"
```

## Cấu Hình Profile QA

### application-qa.yml

```yaml
spring:
  config:
    activate:
      on-profile: "qa"

build:
  version: "2.0"

accounts:
  message: "Chào mừng đến EasyBank Accounts - APIs QA"
  contactDetails:
    name: "Jane Smith - Trưởng Nhóm QA"
    email: "jane.smith@easybank.com"
  onCallSupport:
    - "(555) 234-5678"
    - "(555) 234-5679"
```

### Các Phần Tử Cấu Hình Chính

Thuộc tính `spring.config.activate.on-profile` cho Spring Boot biết khi nào kích hoạt file này:

```yaml
spring:
  config:
    activate:
      on-profile: "qa"
```

Điều này có nghĩa là: "Kích hoạt file này khi profile QA được kích hoạt."

## Cấu Hình Profile Production

### application-prod.yml

```yaml
spring:
  config:
    activate:
      on-profile: "prod"

build:
  version: "1.0"

accounts:
  message: "Chào mừng đến EasyBank Accounts - APIs Production"
  contactDetails:
    name: "Sarah Johnson - Chủ Sở Hữu Sản Phẩm"
    email: "sarah.johnson@easybank.com"
  onCallSupport:
    - "(555) 345-6789"
    - "(555) 345-6790"
```

## Import File Profile

### Cập Nhật application.yml

Thêm cấu hình import để cho Spring Boot biết về các file profile của bạn:

```yaml
spring:
  config:
    import:
      - application-qa.yml
      - application-prod.yml
```

Ví dụ hoàn chỉnh:

```yaml
spring:
  config:
    import:
      - application-qa.yml
      - application-prod.yml
  profiles:
    active: qa  # Kích hoạt profile QA

server:
  port: 8080

build:
  version: "3.0"

accounts:
  message: "Chào mừng đến EasyBank Accounts - APIs Phát Triển Cục Bộ"
  contactDetails:
    name: "John Doe - Lập Trình Viên"
    email: "john.doe@easybank.com"
  onCallSupport:
    - "(555) 123-4567"
    - "(555) 123-4568"
```

## Kích Hoạt Profiles

### Phương Pháp 1: Trong application.yml

Thêm thuộc tính `spring.profiles.active`:

```yaml
spring:
  profiles:
    active: qa
```

### Phương Pháp 2: Dòng Lệnh (Được Khuyên Dùng Cho Production)

Kích hoạt profile từ bên ngoài mà không sửa đổi code:

```bash
java -jar accounts-service.jar --spring.profiles.active=prod
```

### Phương Pháp 3: Biến Môi Trường

```bash
export SPRING_PROFILES_ACTIVE=prod
java -jar accounts-service.jar
```

### Phương Pháp 4: Biến Môi Trường Docker

```bash
docker run -e SPRING_PROFILES_ACTIVE=prod accounts-service:latest
```

## Kiểm Tra Kích Hoạt Profile

### Bước 1: Kiểm Tra Profile Mặc Định

1. Không kích hoạt profile nào (hoặc comment dòng `spring.profiles.active`)
2. Build và khởi động lại ứng dụng
3. Kiểm tra các endpoint:

**Endpoint Build Info:**
```json
GET /actuator/build-info
Response: { "version": "3.0" }
```

**Endpoint Contact Info:**
```json
GET /contact-info
Response: {
  "message": "Chào mừng đến EasyBank Accounts - APIs Phát Triển Cục Bộ",
  "contactDetails": {
    "name": "John Doe - Lập Trình Viên",
    "email": "john.doe@easybank.com"
  },
  "onCallSupport": ["(555) 123-4567", "(555) 123-4568"]
}
```

### Bước 2: Kiểm Tra Profile QA

1. Đặt `spring.profiles.active: qa` trong `application.yml`
2. Build và khởi động lại ứng dụng
3. Kiểm tra các endpoint:

**Endpoint Build Info:**
```json
GET /actuator/build-info
Response: { "version": "2.0" }
```

**Endpoint Contact Info:**
```json
GET /contact-info
Response: {
  "message": "Chào mừng đến EasyBank Accounts - APIs QA",
  "contactDetails": {
    "name": "Jane Smith - Trưởng Nhóm QA",
    "email": "jane.smith@easybank.com"
  },
  "onCallSupport": ["(555) 234-5678", "(555) 234-5679"]
}
```

### Bước 3: Kiểm Tra Profile Production

1. Đặt `spring.profiles.active: prod` trong `application.yml`
2. Build và khởi động lại ứng dụng
3. Xác minh các giá trị cụ thể cho production được trả về

## Cách Hoạt Động Của Profile Override

Khi một profile được kích hoạt, Spring Boot tuân theo thứ tự ưu tiên này:

1. **Thuộc Tính Profile Đang Hoạt Động** (ví dụ: `application-qa.yml`) - **Ưu Tiên Cao Nhất**
2. **Thuộc Tính Profile Mặc Định** (ví dụ: `application.yml`) - **Ưu Tiên Thấp Hơn**

Nếu cùng một key thuộc tính tồn tại trong cả hai file:
- Giá trị từ profile đang hoạt động **ghi đè** giá trị mặc định
- Các thuộc tính chỉ có trong profile mặc định vẫn khả dụng
- Các thuộc tính chỉ có trong profile đang hoạt động được thêm vào

### Ví Dụ:

**application.yml:**
```yaml
build:
  version: "3.0"
server:
  port: 8080
```

**application-qa.yml:**
```yaml
build:
  version: "2.0"
```

**Kết quả khi profile QA được kích hoạt:**
```yaml
build:
  version: "2.0"  # Bị ghi đè bởi profile QA
server:
  port: 8080      # Kế thừa từ profile mặc định
```

## Thực Hành Tốt Nhất Cho Quản Lý Profile

### 1. Giữ Code Không Thay Đổi (Immutable)

**Vấn Đề**: Thay đổi `spring.profiles.active` trong `application.yml` yêu cầu rebuild Docker image cho mỗi môi trường.

**Giải Pháp**: Sử dụng các phương pháp cấu hình bên ngoài (dòng lệnh, biến môi trường) để kích hoạt profile.

### 2. Quy Ước Đặt Tên

- Sử dụng chữ thường cho tên profile: `qa`, `prod`, `dev`
- Nhất quán giữa tất cả các microservices
- Khớp tên profile trong tên file và thuộc tính kích hoạt

### 3. Tổ Chức Thuộc Tính

```yaml
# Nhóm các thuộc tính liên quan
build:
  version: "1.0"

accounts:
  message: "..."
  contactDetails:
    name: "..."
    email: "..."
  onCallSupport:
    - "..."
```

### 4. Không Nhân Bản Thuộc Tính Tĩnh

Chỉ bao gồm các thuộc tính thay đổi giữa các môi trường trong các file theo profile cụ thể.

### 5. Chiến Lược Version

Xem xét chiến lược version có ý nghĩa cho deployment của bạn:
- **Dev**: Version cao nhất (tính năng mới nhất)
- **QA**: Version trung gian (đang kiểm thử)
- **Prod**: Version ổn định (đã phát hành)

## Tùy Chọn Cấu Hình Bên Ngoài

Để triển khai thực sự không thay đổi, sử dụng cấu hình bên ngoài:

### 1. Tham Số Dòng Lệnh
```bash
java -jar app.jar --spring.profiles.active=prod --accounts.message="Thông điệp tùy chỉnh"
```

### 2. Biến Môi Trường
```bash
SPRING_PROFILES_ACTIVE=prod
ACCOUNTS_MESSAGE="Thông điệp tùy chỉnh"
```

### 3. ConfigMaps (Kubernetes)
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: accounts-config
data:
  spring.profiles.active: "prod"
```

### 4. Spring Cloud Config Server
Quản lý cấu hình tập trung cho tất cả các microservices.

## Bài Tập

Áp dụng cùng cách triển khai profile cho:
- **Loans Microservice**
- **Cards Microservice**

Tạo các profile sau cho mỗi dịch vụ:
- `application-qa.yml`
- `application-prod.yml`

Đảm bảo mỗi dịch vụ có các thông tin riêng cho từng môi trường:
- Build versions
- Thông điệp chào mừng
- Chi tiết liên hệ
- Thông tin hỗ trợ

## Tóm Tắt

Triển khai này minh họa:
- ✅ Tạo nhiều file profile
- ✅ Cấu hình thuộc tính theo profile cụ thể
- ✅ Kích hoạt profile theo nhiều cách khác nhau
- ✅ Kiểm tra hành vi của profile
- ✅ Hiểu cơ chế ghi đè thuộc tính
- ✅ Thực hành tốt nhất cho triển khai production

## Các Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ khám phá:
- **Phương pháp cấu hình thuộc tính bên ngoài**
- **Kích hoạt profile động**
- **Tránh thay đổi code khi chuyển môi trường**
- **Chiến lược profile cho Docker và Kubernetes**

---

**Ghi Nhớ**: Xây dựng một lần, triển khai mọi nơi bằng cách sử dụng kích hoạt profile từ bên ngoài!




FILE: 62-externalizing-spring-boot-configuration.md


# Cấu Hình Bên Ngoài Cho Spring Boot

## Thách Thức Với Profile Được Hardcode

### Vấn Đề Hiện Tại

Khi kích hoạt profile bằng cách hardcode giá trị trong `application.yml`:

```yaml
spring:
  profiles:
    active: qa
```

**Nhược Điểm:**
- Yêu cầu rebuild Docker image cho mỗi môi trường
- Yêu cầu tạo lại package ứng dụng web
- Vi phạm **phương pháp 12-Factor App**
- Code không immutable giữa các môi trường
- Tăng độ phức tạp và thời gian triển khai

### Giải Pháp

Spring Boot cung cấp nhiều cách để **externalize cấu hình** và kích hoạt profile từ nguồn bên ngoài mà không cần sửa đổi code.

## Các Phương Pháp Cấu Hình Bên Ngoài

Spring Boot hỗ trợ nhiều phương pháp để externalize cấu hình, mỗi phương pháp có mức độ ưu tiên khác nhau.

### Thứ Tự Ưu Tiên Cấu Hình (Cao Xuống Thấp)

1. **Command Line Arguments** - Ưu Tiên Cao Nhất
2. **JVM System Properties** - Ưu Tiên Trung Bình
3. **Environment Variables** - Ưu Tiên Tiêu Chuẩn
4. **Profile-Specific Properties** (`application-{profile}.yml`)
5. **Default Properties** (`application.yml`) - Ưu Tiên Thấp Nhất

## 1. Command Line Arguments (Tham Số Dòng Lệnh)

### Tổng Quan

Command line arguments cung cấp **ưu tiên cao nhất** cho cấu hình. Spring Boot tự động chuyển đổi command line arguments thành các cặp key-value và thêm chúng vào environment object.

### Đặc Điểm

- **Ưu tiên cao nhất** - Ghi đè tất cả các nguồn cấu hình khác
- **Hiệu lực ngay lập tức** - Không cần thay đổi code
- **Linh hoạt** - Truyền bất kỳ thuộc tính nào một cách động
- **Minh bạch** - Dễ dàng xem giá trị nào đang được sử dụng

### Cú Pháp

```bash
java -jar application.jar --property.key=value
```

### Ví Dụ Cơ Bản

#### Ghi Đè Build Version

```bash
java -jar accounts-service.jar --build.version=4.0
```

#### Kích Hoạt Profile

```bash
java -jar accounts-service.jar --spring.profiles.active=prod
```

#### Nhiều Thuộc Tính

Phân tách nhiều thuộc tính bằng khoảng trắng:

```bash
java -jar accounts-service.jar \
  --spring.profiles.active=prod \
  --build.version=1.0 \
  --server.port=8081
```

### Ví Dụ Nâng Cao

#### Giá Trị Thuộc Tính Phức Tạp

```bash
java -jar accounts-service.jar \
  --spring.profiles.active=prod \
  --accounts.message="Chào mừng đến APIs Production" \
  --accounts.contactDetails.name="Đội Hỗ Trợ Production"
```

#### Ghi Đè Cấu Hình Database

```bash
java -jar accounts-service.jar \
  --spring.profiles.active=prod \
  --spring.datasource.url=jdbc:mysql://prod-db:3306/accounts \
  --spring.datasource.username=prod_user
```

### Quy Tắc Quan Trọng

1. **Tiền tố**: Luôn sử dụng `--` trước property key
2. **Khoảng cách**: Phân tách nhiều arguments bằng khoảng trắng
3. **Dấu ngoặc kép**: Sử dụng dấu ngoặc kép cho giá trị có khoảng trắng
4. **Định dạng**: `--property.key=value` (không có khoảng trắng xung quanh `=`)

## 2. JVM System Properties (Thuộc Tính Hệ Thống JVM)

### Tổng Quan

JVM system properties cung cấp cấu hình ở cấp độ Java Virtual Machine. Chúng có **ưu tiên thấp hơn command line arguments** nhưng **cao hơn property files**.

### Đặc Điểm

- **Ưu tiên trung bình** - Giữa command line và property files
- **Cấp độ JVM** - Đặt trước khi ứng dụng khởi động
- **Java tiêu chuẩn** - Hoạt động với bất kỳ ứng dụng Java nào

### Cú Pháp

```bash
java -Dproperty.key=value -jar application.jar
```

### Sự Khác Biệt Chính So Với Command Line Arguments

| Tính Năng | Command Line Args | JVM System Properties |
|---------|------------------|----------------------|
| Tiền tố | `--` | `-D` |
| Ưu tiên | Cao nhất | Trung bình |
| Cú pháp | `--key=value` | `-Dkey=value` |
| Vị trí | Sau tên JAR | Trước `-jar` |

### Ví Dụ

#### Kích Hoạt Profile Với JVM Property

```bash
java -Dspring.profiles.active=prod -jar accounts-service.jar
```

#### Nhiều JVM Properties

```bash
java -Dspring.profiles.active=prod \
     -Dbuild.version=1.0 \
     -Dserver.port=8081 \
     -jar accounts-service.jar
```

#### Kết Hợp: JVM Properties và Command Line Arguments

```bash
java -Dspring.profiles.active=qa \
     -jar accounts-service.jar \
     --build.version=2.0
```

**Kết quả**: Profile sẽ là `qa` (từ JVM property), nhưng build version sẽ là `2.0` (command line có ưu tiên cao hơn).

### Khi Cùng Thuộc Tính Được Định Nghĩa Ở Cả Hai

Nếu cùng một thuộc tính được định nghĩa ở cả hai nơi:

```bash
java -Dspring.profiles.active=qa \
     -jar accounts-service.jar \
     --spring.profiles.active=prod
```

**Kết quả**: Profile `prod` sẽ được kích hoạt (command line arguments thắng do có ưu tiên cao hơn).

### Truy Cập JVM Properties Trong Java Code

```java
String profileValue = System.getProperty("spring.profiles.active");
```

## 3. Environment Variables (Biến Môi Trường)

### Tổng Quan

Environment variables được **hỗ trợ phổ biến** trên tất cả các nền tảng và ngôn ngữ lập trình, khiến chúng trở nên lý tưởng cho các ứng dụng containerized và cloud-native.

### Đặc Điểm

- **Hỗ trợ phổ biến** - Hoạt động trên tất cả các ngôn ngữ và nền tảng
- **Thân thiện với Container** - Hoàn hảo cho Docker và Kubernetes
- **Bền vững** - Có thể được đặt ở cấp độ OS
- **Không phụ thuộc ngôn ngữ** - Không đặc biệt cho Java hoặc Spring Boot

### Ưu Điểm

1. **Độc Lập Nền Tảng**: Hoạt động bất kể ngôn ngữ lập trình
2. **Container Native**: Phương pháp tiêu chuẩn trong Docker/Kubernetes
3. **Sẵn Sàng Cloud**: Được hỗ trợ bởi tất cả các nền tảng cloud
4. **Tương Thích Serverless**: Hoạt động với AWS Lambda, Azure Functions, v.v.
5. **Bảo Mật**: Có thể được inject một cách an toàn mà không cần hardcode

### Quy Tắc Đặt Tên

Spring Boot yêu cầu quy ước đặt tên cụ thể cho environment variables:

1. **Chuyển sang CHỮ HOA**: Tất cả các chữ cái phải viết hoa
2. **Thay dấu chấm (.) bằng gạch dưới (_)**
3. **Thay dấu gạch ngang (-) bằng gạch dưới (_)**

### Ví Dụ Chuyển Đổi

| Thuộc tính trong application.yml | Environment Variable |
|----------------------------|---------------------|
| `spring.profiles.active` | `SPRING_PROFILES_ACTIVE` |
| `build.version` | `BUILD_VERSION` |
| `server.port` | `SERVER_PORT` |
| `spring.datasource.url` | `SPRING_DATASOURCE_URL` |
| `accounts.contact-details.name` | `ACCOUNTS_CONTACT_DETAILS_NAME` |

## Đặt Environment Variables

### Windows (PowerShell)

#### Tạm Thời (Phiên Hiện Tại)

```powershell
$env:SPRING_PROFILES_ACTIVE="prod"
$env:BUILD_VERSION="1.0"
java -jar accounts-service.jar
```

#### Vĩnh Viễn (Cấp Độ Hệ Thống)

```powershell
[System.Environment]::SetEnvironmentVariable("SPRING_PROFILES_ACTIVE", "prod", "User")
```

### Windows (Command Prompt)

#### Tạm Thời

```cmd
set SPRING_PROFILES_ACTIVE=prod
set BUILD_VERSION=1.0
java -jar accounts-service.jar
```

#### Thực Thi Inline

```cmd
set SPRING_PROFILES_ACTIVE=prod && java -jar accounts-service.jar
```

### Linux / macOS

#### Tạm Thời (Phiên Hiện Tại)

```bash
export SPRING_PROFILES_ACTIVE=prod
export BUILD_VERSION=1.0
java -jar accounts-service.jar
```

#### Thực Thi Inline (Lệnh Đơn)

```bash
SPRING_PROFILES_ACTIVE=prod BUILD_VERSION=1.0 java -jar accounts-service.jar
```

#### Vĩnh Viễn (User Profile)

Thêm vào `~/.bashrc` hoặc `~/.bash_profile`:

```bash
export SPRING_PROFILES_ACTIVE=prod
export BUILD_VERSION=1.0
```

Sau đó tải lại:
```bash
source ~/.bashrc
```

## Sử Dụng Docker và Container

### Lệnh Docker Run

```bash
docker run -e SPRING_PROFILES_ACTIVE=prod \
           -e BUILD_VERSION=1.0 \
           -e SERVER_PORT=8080 \
           accounts-service:latest
```

### Docker Compose

```yaml
version: '3.8'
services:
  accounts:
    image: accounts-service:latest
    environment:
      - SPRING_PROFILES_ACTIVE=prod
      - BUILD_VERSION=1.0
      - SERVER_PORT=8080
      - SPRING_DATASOURCE_URL=jdbc:mysql://db:3306/accounts
```

### Dockerfile (Build-time)

```dockerfile
FROM openjdk:17-jdk-slim
COPY target/accounts-service.jar app.jar

# Đặt environment variables
ENV SPRING_PROFILES_ACTIVE=prod
ENV BUILD_VERSION=1.0

ENTRYPOINT ["java", "-jar", "/app.jar"]
```

## Cấu Hình Kubernetes

### Deployment Với Environment Variables

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: accounts-service
spec:
  template:
    spec:
      containers:
      - name: accounts
        image: accounts-service:latest
        env:
        - name: SPRING_PROFILES_ACTIVE
          value: "prod"
        - name: BUILD_VERSION
          value: "1.0"
```

### Sử Dụng ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: accounts-config
data:
  SPRING_PROFILES_ACTIVE: "prod"
  BUILD_VERSION: "1.0"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: accounts-service
spec:
  template:
    spec:
      containers:
      - name: accounts
        image: accounts-service:latest
        envFrom:
        - configMapRef:
            name: accounts-config
```

### Sử Dụng Secrets (Dữ Liệu Nhạy Cảm)

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: accounts-secrets
type: Opaque
stringData:
  SPRING_DATASOURCE_USERNAME: "prod_user"
  SPRING_DATASOURCE_PASSWORD: "secure_password"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: accounts-service
spec:
  template:
    spec:
      containers:
      - name: accounts
        image: accounts-service:latest
        envFrom:
        - secretRef:
            name: accounts-secrets
```

## Truy Cập Environment Variables Trong Java

### Sử Dụng System.getenv()

```java
public class ConfigExample {
    public static void main(String[] args) {
        String profile = System.getenv("SPRING_PROFILES_ACTIVE");
        String version = System.getenv("BUILD_VERSION");
        
        System.out.println("Active Profile: " + profile);
        System.out.println("Build Version: " + version);
    }
}
```

### Sử Dụng @Value Annotation Của Spring

```java
@Component
public class AppConfig {
    
    @Value("${spring.profiles.active:default}")
    private String activeProfile;
    
    @Value("${build.version}")
    private String buildVersion;
    
    public void printConfig() {
        System.out.println("Profile: " + activeProfile);
        System.out.println("Version: " + buildVersion);
    }
}
```

### Sử Dụng Spring Environment

```java
@Component
public class ConfigService {
    
    @Autowired
    private Environment env;
    
    public void displayConfig() {
        String profile = env.getProperty("spring.profiles.active");
        String version = env.getProperty("build.version");
        
        System.out.println("Active Profile: " + profile);
        System.out.println("Build Version: " + version);
    }
}
```

## Ví Dụ Về Thứ Tự Ưu Tiên Hoàn Chỉnh

Cho các nguồn cấu hình sau:

**application.yml:**
```yaml
build:
  version: "3.0"
```

**application-prod.yml:**
```yaml
build:
  version: "1.0"
```

**Environment Variable:**
```bash
BUILD_VERSION=2.0
```

**JVM System Property:**
```bash
-Dbuild.version=2.5
```

**Command Line Argument:**
```bash
--build.version=4.0
```

**Kết quả**: `build.version = "4.0"` (Command line có ưu tiên cao nhất)

## Thực Hành Tốt Nhất

### 1. Chọn Phương Pháp Phù Hợp

- **Phát triển**: Sử dụng `application.yml` hoặc cấu hình IDE
- **Testing/QA**: Sử dụng environment variables hoặc command line
- **Production**: Sử dụng environment variables (Docker/Kubernetes)
- **Nền tảng Cloud**: Sử dụng dịch vụ cấu hình đặc thù của nền tảng

### 2. Cân Nhắc Bảo Mật

- **Không bao giờ hardcode** thông tin xác thực nhạy cảm trong property files
- **Sử dụng environment variables** cho secrets
- **Sử dụng công cụ quản lý secrets** (Vault, AWS Secrets Manager)
- **Kubernetes Secrets** cho triển khai container

### 3. Tài Liệu

- Ghi chép phương pháp cấu hình được sử dụng trong mỗi môi trường
- Duy trì hướng dẫn cấu hình cho đội vận hành
- Liệt kê tất cả các environment variables cần thiết

### 4. Kiểm Thử

- Kiểm tra cấu hình trong mỗi môi trường trước khi triển khai
- Xác minh thứ tự ưu tiên hoạt động như mong đợi
- Kiểm tra cấu hình bên ngoài ghi đè đúng cách

## Tóm Tắt

### So Sánh Các Phương Pháp Cấu Hình

| Phương Pháp | Ưu Tiên | Trường Hợp Sử Dụng | Nền Tảng |
|--------|-----------|----------|----------|
| Command Line | Cao nhất | Kiểm tra nhanh, ghi đè | Bất kỳ |
| JVM Properties | Cao | Cấu hình đặc thù JVM | Chỉ Java |
| Environment Variables | Trung bình | Containers, cloud, production | Phổ biến |
| Profile Files | Thấp | Mặc định theo môi trường | Spring Boot |
| Default Properties | Thấp nhất | Mặc định ứng dụng | Spring Boot |

### Điểm Chính Cần Nhớ

✅ **Externalize tất cả cấu hình theo môi trường**
✅ **Không bao giờ rebuild artifacts cho các môi trường khác nhau**
✅ **Sử dụng environment variables cho triển khai production**
✅ **Command line arguments có ưu tiên cao nhất**
✅ **Tuân theo phương pháp 12-Factor App cho ứng dụng cloud-native**

## Các Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ:
- **Minh họa** tất cả các phương pháp externalization này
- **Kích hoạt profiles** bằng các phương pháp khác nhau
- **Kiểm tra thứ tự ưu tiên** với các ví dụ thực tế
- **Triển khai** microservices với cấu hình bên ngoài

---

**Ghi Nhớ**: Xây dựng một lần, cấu hình mọi nơi - chìa khóa cho triển khai immutable!




FILE: 63-spring-boot-profiles-externalized-configuration.md


# Spring Boot Profiles và Cấu Hình Bên Ngoài (Externalized Configuration)

## Tổng Quan

Hướng dẫn này trình bày cách kích hoạt Spring Boot profiles sử dụng các phương pháp cấu hình bên ngoài. Những kỹ thuật này cho phép bạn triển khai cùng một Docker image trên nhiều môi trường khác nhau mà không cần build lại, giúp microservices của bạn trở nên bất biến (immutable).

## Các Phương Pháp Cấu Hình Bên Ngoài

Spring Boot hỗ trợ ba phương pháp chính cho cấu hình bên ngoài (theo thứ tự ưu tiên):

1. **Command Line Arguments - Tham số dòng lệnh** (Ưu tiên cao nhất)
2. **JVM System Variables - Biến hệ thống JVM**
3. **Environment Variables - Biến môi trường**

## Demo: Kích Hoạt Profiles Sử Dụng IDE

### Yêu Cầu Tiên Quyết

- Ứng dụng Spring Boot với class chính `AccountsApplication`
- IDE (IntelliJ IDEA hoặc tương tự)
- File `application.yml` với nhiều profiles (QA, Prod)

## Phương Pháp 1: Command Line Arguments (Tham Số Dòng Lệnh)

### Các Bước:

1. Nhấp chuột phải vào class `AccountsApplication`
2. Chọn **Modify Run Configuration**
3. Trong trường **Program Arguments**, thêm:
   ```
   --spring.profiles.active=prod --build.version=1.1
   ```

### Cú Pháp:
- Sử dụng tiền tố **double hyphens** (`--`)
- Định dạng: `--property.name=value`

### Ví Dụ:
```
--spring.profiles.active=prod --build.version=1.1
```

### Kiểm Tra:

- **Contact Info API**: Trả về dữ liệu từ prod profile (production APIs, thông tin product owner)
- **Build Info API**: Trả về `1.1` (giá trị được ghi đè, không phải `1.0` mặc định từ prod profile)

## Phương Pháp 2: JVM System Variables (Biến Hệ Thống JVM)

### Các Bước:

1. Nhấp chuột phải vào `AccountsApplication`
2. Chọn **Modify Run Configuration**
3. Xóa command line arguments
4. Click **Modify Options** → **Add VM Options**
5. Trong trường **VM Options**, thêm:
   ```
   -Dspring.profiles.active=prod -Dbuild.version=1.3
   ```

### Cú Pháp:
- Sử dụng tiền tố `-D` cho mỗi property
- Định dạng: `-Dproperty.name=value`

### Ví Dụ:
```
-Dspring.profiles.active=prod -Dbuild.version=1.3
```

### Kiểm Tra:

- **Contact Info API**: Trả về dữ liệu từ prod profile
- **Build Info API**: Trả về `1.3`

## Phương Pháp 3: Environment Variables (Biến Môi Trường)

### Các Bước:

1. Nhấp chuột phải vào `AccountsApplication`
2. Chọn **Modify Run Configuration**
3. Xóa VM arguments
4. Trong trường **Environment Variables**, thêm:
   ```
   SPRING_PROFILES_ACTIVE=prod;BUILD_VERSION=1.8
   ```

### Quy Tắc Cú Pháp:
- **Không cần tiền tố**
- **Chỉ sử dụng chữ IN HOA**
- Thay dấu chấm (`.`) bằng dấu gạch dưới (`_`)
- Phân cách nhiều biến bằng dấu chấm phẩy (`;`)

### Ví Dụ:
```
SPRING_PROFILES_ACTIVE=prod;BUILD_VERSION=1.8
```

### Kiểm Tra:

- **Contact Info API**: Trả về dữ liệu từ prod profile
- **Build Info API**: Trả về `1.8`

## Kiểm Tra Thứ Tự Ưu Tiên Cấu Hình

### Kịch Bản: Cấu Hình Cả Ba Phương Pháp

Cấu hình cả ba phương pháp với các giá trị khác nhau:

```
Command Line Args:     --build.version=1.3
VM Options:           -Dbuild.version=1.1
Environment Variables: BUILD_VERSION=1.8
```

### Kết Quả:

1. **Với cả ba phương pháp được cấu hình**: Kết quả là `1.3` (Command line arguments thắng)
2. **Không có command line args**: Kết quả là `1.1` (JVM system variables thắng)
3. **Không có command line args và VM options**: Kết quả là `1.8` (Environment variables thắng)
4. **Không có cấu hình bên ngoài nào**: Kết quả là `1.0` (Mặc định từ prod profile)

## Thứ Tự Ưu Tiên (Từ Cao Đến Thấp)

1. ✅ **Command Line Arguments** (`--property=value`)
2. ✅ **JVM System Variables** (`-Dproperty=value`)
3. ✅ **Environment Variables** (`PROPERTY=value`)
4. ✅ **Profile-Specific Properties** (application-{profile}.yml)
5. ✅ **Default Properties** (application.yml)

## Lợi Ích

- **Microservices Bất Biến**: Triển khai cùng một Docker image trên nhiều môi trường
- **Không Cần Build Lại**: Thay đổi cấu hình mà không cần build lại Docker images
- **Cấu Hình Theo Môi Trường**: Dễ dàng chuyển đổi giữa dev, QA và prod
- **Linh Hoạt Ghi Đè**: Ghi đè bất kỳ property nào tại runtime

## Hạn Chế

Mặc dù phương pháp này hoạt động cho các trường hợp cơ bản, nhưng nó có một số nhược điểm:

- Không phù hợp cho kiến trúc microservices phức tạp
- Khả năng mở rộng hạn chế khi quản lý nhiều microservices
- Thay đổi cấu hình yêu cầu khởi động lại ứng dụng
- Không có quản lý cấu hình tập trung
- Khó theo dõi các thay đổi cấu hình

## Bước Tiếp Theo

Áp dụng cấu hình tương tự cho:
- **Loans Microservice**
- **Cards Microservice**

Trong các bài giảng tiếp theo, chúng ta sẽ khám phá các phương pháp quản lý cấu hình nâng cao hơn để giải quyết những hạn chế này.

## Những Điểm Chính Cần Nhớ

✅ Spring Boot profiles cho phép cấu hình theo môi trường cụ thể  
✅ Cấu hình bên ngoài cho phép ghi đè properties tại runtime  
✅ Command line arguments có độ ưu tiên cao nhất  
✅ Phương pháp này hoạt động cho các trường hợp cơ bản nhưng có hạn chế  
✅ Cần các giải pháp quản lý cấu hình nâng cao cho môi trường production  

## Chủ Đề Liên Quan

- Spring Boot Profiles
- Triển Khai Docker Image
- Quản Lý Cấu Hình trong Microservices
- Cấu Hình CI/CD Pipeline




FILE: 64-spring-boot-profiles-assignment-cards-loans.md


# Bài Tập Spring Boot Profiles - Cards và Loans Microservices

## Tổng Quan

Bài giảng này cung cấp một bài tập để thực hành triển khai Spring Boot profiles và quản lý cấu hình trong các microservices Cards và Loans, tương tự như những gì đã được thực hiện trong Accounts microservice.

## Tình Trạng Hiện Tại

Tính đến thời điểm này, chúng ta đã:
- Cập nhật accounts microservice với các khái niệm về Spring Boot profiles
- Giới thiệu nhiều thuộc tính bên trong file `application.yml`
- Đọc các thuộc tính đó thông qua ba REST APIs khác nhau bên trong accounts microservice

## Hướng Dẫn Bài Tập

### Nhiệm Vụ Của Bạn

Bạn cần thực hiện các thay đổi tương tự bên trong **Cards** và **Loans** microservices. Bài tập này được thiết kế để dễ dàng và cung cấp thực hành thực tế.

### Tài Liệu Tham Khảo

Nếu bạn có câu hỏi về tên thuộc tính hoặc giá trị thuộc tính cần sử dụng, vui lòng tham khảo code trong GitHub repository:

**Repository:** `eazybytes/microservice`

**Đường dẫn:** Section 6 → thư mục `v1-springboot`

Bên trong thư mục này, bạn sẽ tìm thấy ba microservices:
- **Accounts** (đã hoàn thành)
- **Cards** (bài tập)
- **Loans** (bài tập)

### Hướng Dẫn Cấu Hình

Đối với Cards và Loans microservices:
- Sử dụng **cấu trúc thuộc tính giống** như Accounts microservice
- Cung cấp **giá trị khác nhau** cho:
  - Số điện thoại
  - Chi tiết liên hệ
  - Thông điệp

Bạn có thể tìm tất cả chi tiết thuộc tính cần thiết bằng cách:
1. Truy cập vào GitHub repository
2. Xem file `application.yml` cho mỗi microservice

## Tại Sao Bài Tập Này Quan Trọng

### Lợi Ích Của Việc Hoàn Thành Bài Tập

1. **Thực Hành Thực Tế**: Bài tập này cung cấp kinh nghiệm thực tế với các khái niệm
2. **Củng Cố Kiến Thức**: Triển khai thay đổi trên nhiều microservices giúp củng cố việc học
3. **Trí Nhớ Tiềm Thức**: Thực hành lặp đi lặp lại giúp nhúng các khái niệm này vào trí nhớ tiềm thức của bạn
4. **Sẵn Sàng Cho Phỏng Vấn**: Với đủ thực hành, bạn sẽ có thể trả lời các câu hỏi liên quan một cách tự tin, ngay cả khi được hỏi bất ngờ

### Phương Pháp Học Tập

- Khóa học giải thích các khái niệm sử dụng một microservice (Accounts)
- Bạn thực hành bằng cách triển khai các thay đổi tương tự trong hai microservices khác (Cards và Loans)
- Phương pháp này mang lại thực hành đáng kể và hiểu biết sâu sắc

## Nhận Trợ Giúp

### Nếu Bạn Gặp Vấn Đề

- **Đừng nản lòng** nếu bạn đối mặt với thử thách
- Bài giảng tiếp theo sẽ đề cập nhanh đến các thay đổi code cho Cards và Loans microservices
- Bạn luôn có thể tham khảo code trong GitHub repository để được hướng dẫn

### GitHub Repository

Tất cả các triển khai hoàn chỉnh đều có sẵn trong GitHub repository để tham khảo nếu cần.

## Các Bước Tiếp Theo

1. Mở Cards microservice
2. Triển khai Spring Boot profiles và các thuộc tính cấu hình
3. Tạo REST APIs để đọc các thuộc tính
4. Lặp lại cho Loans microservice
5. Kiểm tra các triển khai của bạn

## Kết Luận

Bài tập này là một cơ hội tuyệt vời để thực hành và củng cố hiểu biết của bạn về:
- Spring Boot profiles
- Quản lý cấu hình
- Externalization thuộc tính
- Phát triển REST API

Chúc bạn may mắn với bài tập! Bài giảng tiếp theo sẽ xem xét giải pháp hoàn chỉnh.




FILE: 65-implementing-spring-boot-profiles-cards-loans-solution.md


# Triển Khai Spring Boot Profiles trong Cards và Loans Microservices - Hướng Dẫn Giải Pháp

## Giới Thiệu

Bài giảng này cung cấp hướng dẫn đầy đủ về việc triển khai Spring Boot profiles và quản lý cấu hình trong Cards và Loans microservices, bao gồm tất cả các thay đổi code cần thiết để hoàn thành bài tập.

## Triển Khai Thay Đổi trong Loans Microservice

### Bước 1: Cập Nhật LoansController

Điều hướng đến class `LoansController` và thực hiện các thay đổi sau:

#### Dependency Injection và Autowiring

```java
@Autowired
private Environment environment;

@Autowired
private LoansContactInfoDto loansContactInfoDto;

@Value("${build.version}")
private String buildVersion;
```

#### Constructor Injection

```java
public LoansController(ILoanService loanService) {
    this.loanService = loanService;
}
```

#### Tạo Ba REST APIs

**1. Build Info API**

Trả về phiên bản build hiện tại:

```java
@GetMapping("/build-info")
@Operation(
    summary = "Get Build Info",
    description = "Get build version information"
)
@ApiResponses({
    @ApiResponse(
        responseCode = "200",
        description = "HTTP Status OK"
    )
})
public ResponseEntity<String> getBuildInfo() {
    return ResponseEntity.ok(buildVersion);
}
```

**2. Java Version API**

Đọc biến môi trường JAVA_HOME:

```java
@GetMapping("/java-version")
@Operation(
    summary = "Get Java Version",
    description = "Get Java version details"
)
@ApiResponses({
    @ApiResponse(
        responseCode = "200",
        description = "HTTP Status OK"
    )
})
public ResponseEntity<String> getJavaVersion() {
    return ResponseEntity.ok(environment.getProperty("JAVA_HOME"));
}
```

**3. Contact Info API**

Trả về tất cả các thuộc tính cấu hình:

```java
@GetMapping("/contact-info")
@Operation(
    summary = "Get Contact Info",
    description = "Get contact information"
)
@ApiResponses({
    @ApiResponse(
        responseCode = "200",
        description = "HTTP Status OK"
    )
})
public ResponseEntity<LoansContactInfoDto> getContactInfo() {
    return ResponseEntity.ok(loansContactInfoDto);
}
```

### Bước 2: Tạo LoansContactInfoDto

Tạo một record class với prefix `loans`:

```java
@ConfigurationProperties(prefix = "loans")
public record LoansContactInfoDto(
    String message,
    Map<String, String> contactDetails,
    List<String> onCallSupport
) {}
```

**Điểm Quan Trọng:**
- Sử dụng prefix `loans` để khớp với các thuộc tính trong application.yml
- Định nghĩa như một record class
- Chứa các trường: message, contactDetails, onCallSupport
- Kiểu dữ liệu khớp với các thuộc tính được định nghĩa trong application.yml

### Bước 3: Kích Hoạt Configuration Properties

Trong class `LoansApplication`:

```java
@EnableConfigurationProperties(value = {LoansContactInfoDto.class})
@SpringBootApplication
public class LoansApplication {
    public static void main(String[] args) {
        SpringApplication.run(LoansApplication.class, args);
    }
}
```

### Bước 4: Tạo Các File Cấu Hình

#### application.yml

```yaml
spring:
  profiles:
    active: qa
  config:
    import:
      - application_qa.yml
      - application_prod.yml

build:
  version: "1.0"

loans:
  message: "Chào mừng đến với Loans Microservice"
  contactDetails:
    name: "John Doe"
    email: "john.doe@example.com"
  onCallSupport:
    - "555-1234"
    - "555-5678"
```

#### application_qa.yml

```yaml
spring:
  config:
    activate:
      on-profile: qa

build:
  version: "2.0"

loans:
  message: "Chào mừng đến với Loans Microservice - Môi Trường QA"
  contactDetails:
    name: "QA Support Team"
    email: "qa@example.com"
  onCallSupport:
    - "555-QA-01"
    - "555-QA-02"
```

#### application_prod.yml

```yaml
spring:
  config:
    activate:
      on-profile: prod

build:
  version: "1.0"

loans:
  message: "Chào mừng đến với Loans Microservice - Production"
  contactDetails:
    name: "Production Support"
    email: "prod@example.com"
  onCallSupport:
    - "555-PROD-24/7"
```

### Bước 5: Kiểm Tra Loans Microservice

#### Kiểm Tra với QA Profile (Mặc Định)

1. Khởi động ứng dụng ở chế độ debug
2. Profile QA được kích hoạt mặc định trong application.yml

**Kiểm Tra Build Info API:**
```
GET http://localhost:8090/build-info
Response: "2.0"
```

**Kiểm Tra Java Version API:**
```
GET http://localhost:8090/java-version
Response: <Đường dẫn JAVA_HOME từ hệ thống local>
```

**Kiểm Tra Contact Info API:**
```
GET http://localhost:8090/contact-info
Response: Thuộc tính từ QA profile
```

#### Kiểm Tra với Production Profile

**Kích hoạt sử dụng Command Line Arguments:**

1. Dừng server
2. Click phải vào LoansApplication
3. Chọn "Modify Run Configuration"
4. Thêm program arguments: `--spring.profiles.active=prod`
5. Apply và khởi động ứng dụng

**Xác Nhận:**
- Contact Info API trả về thuộc tính production
- Build Info API trả về "1.0"

## Triển Khai Thay Đổi trong Cards Microservice

### Bước 1: Cập Nhật CardsController

Triển khai theo mẫu tương tự như Loans:

#### Autowiring và Dependency Injection

```java
@Autowired
private Environment environment;

@Autowired
private CardsContactInfoDto cardsContactInfoDto;

@Value("${build.version}")
private String buildVersion;
```

#### Tạo Ba REST APIs

1. **Build Info API** - Trả về phiên bản build
2. **Java Version API** - Trả về biến môi trường JAVA_HOME
3. **Contact Info API** - Trả về tất cả thuộc tính cấu hình từ CardsContactInfoDto

### Bước 2: Tạo CardsContactInfoDto

```java
@ConfigurationProperties(prefix = "cards")
public record CardsContactInfoDto(
    String message,
    Map<String, String> contactDetails,
    List<String> onCallSupport
) {}
```

**Quan Trọng:** Sử dụng prefix `cards` để khớp với các thuộc tính trong application.yml.

### Bước 3: Kích Hoạt Configuration Properties

Trong class `CardsApplication`:

```java
@EnableConfigurationProperties(value = {CardsContactInfoDto.class})
@SpringBootApplication
public class CardsApplication {
    public static void main(String[] args) {
        SpringApplication.run(CardsApplication.class, args);
    }
}
```

### Bước 4: Tạo Các File Cấu Hình

Tạo các file sau:
- `application.yml`
- `application_qa.yml`
- `application_prod.yml`

Sử dụng prefix `cards` cho tất cả các thuộc tính thay vì `loans`.

### Bước 5: Kiểm Tra Cards Microservice

#### Kiểm Tra với QA Profile

Khởi động ứng dụng ở chế độ debug. Mặc định, profile QA được kích hoạt.

**Kiểm Tra Build Info API:**
```
GET http://localhost:9000/build-info
Response: "2.0"
```

**Kiểm Tra Java Version API:**
```
GET http://localhost:9000/java-version
Response: <Đường dẫn JAVA_HOME>
```

**Kiểm Tra Contact Info API:**
```
GET http://localhost:9000/contact-info
Response: Thuộc tính từ QA profile
```

#### Kiểm Tra với Production Profile

1. Dừng server
2. Click phải vào CardsApplication
3. Chọn "Modify Run Configuration"
4. Thêm: `--spring.profiles.active=prod`
5. Apply và khởi động ứng dụng

**Xác Nhận:**
- Contact Info API trả về thuộc tính production
- Build Info API trả về "1.0"

## Những Điều Cần Lưu Ý Quan Trọng

### Khoảng Cách trong File YAML

**Quan Trọng:** Khoảng cách trong file YAML cực kỳ quan trọng.

❌ **Sai:**
```yaml
spring:
  config:
    profiles:  # Khoảng cách thừa - Vị trí sai!
      active: qa
```

✅ **Đúng:**
```yaml
spring:
  profiles:
    active: qa
```

**Cảnh Báo:** Ngay cả một khoảng cách thừa cũng có thể phá vỡ việc kích hoạt profile bằng cách đặt thuộc tính dưới phần tử cha sai.

### Tóm Tắt Ba Microservices

Tất cả các thay đổi đã được hoàn thành cho:
- ✅ Accounts Microservice
- ✅ Cards Microservice
- ✅ Loans Microservice

### Tài Nguyên Tham Khảo

Nếu bạn có bất kỳ câu hỏi nào, hãy tham khảo GitHub repository để xem các ví dụ triển khai đầy đủ.

## Hạn Chế của Phương Pháp Này

### Triển Khai Hiện Tại

Đây là **phương pháp cơ bản nhất** cho quản lý cấu hình trong microservices.

### Nhược Điểm

Mặc dù phương pháp này hoạt động, nó có **những nhược điểm nghiêm trọng** đối với các tổ chức xây dựng hàng trăm microservices:

1. Cấu hình phân tán trên nhiều microservices
2. Khó quản lý ở quy mô lớn
3. Không có quản lý cấu hình tập trung
4. Khó cập nhật cấu hình mà không cần triển khai lại
5. Hạn chế tính linh hoạt cho các thay đổi cấu hình động

### Tiếp Theo Là Gì

Bài giảng tiếp theo sẽ khám phá chi tiết các nhược điểm này và giới thiệu các phương pháp tốt hơn để quản lý cấu hình trong kiến trúc microservice quy mô lớn.

## Những Điểm Chính

1. Spring Boot profiles cho phép cấu hình theo môi trường
2. `@ConfigurationProperties` cung cấp ràng buộc cấu hình an toàn kiểu
3. Thuộc tính có thể được đọc bằng `@Value`, `Environment`, và DTOs
4. Kích hoạt profile có thể thực hiện qua application.yml hoặc command-line arguments
5. Khoảng cách trong YAML rất quan trọng để cấu hình đúng
6. Phương pháp cơ bản này cần cải thiện cho ứng dụng cấp doanh nghiệp

## Các Bước Tiếp Theo

Tiếp tục bài giảng tiếp theo để hiểu:
- Nhược điểm của phương pháp cấu hình hiện tại
- Các giải pháp thay thế tốt hơn cho kiến trúc microservice quy mô lớn
- Giải pháp quản lý cấu hình tập trung




FILE: 66-han-che-cau-hinh-spring-boot-va-giai-phap.md


# Hạn Chế Cấu Hình Spring Boot và Giải Pháp

## Tổng Quan

Tài liệu này thảo luận về các hạn chế và nhược điểm khi externalize (đưa ra ngoài) cấu hình chỉ sử dụng Spring Boot framework, và giới thiệu Spring Cloud Config Server như một giải pháp nâng cao để vượt qua những thách thức này.

## Hạn Chế của Quản Lý Cấu Hình Spring Boot

### 1. Quản Lý Cấu Hình Thủ Công

**Vấn Đề:**
- Externalize cấu hình thông qua CLI arguments, JVM properties và environment variables đòi hỏi thiết lập thủ công
- Việc inject cấu hình phải được thực hiện thủ công trong quá trình khởi động ứng dụng
- Thường liên quan đến việc thực thi các lệnh riêng biệt hoặc thiết lập ứng dụng thủ công
- Phụ thuộc nhiều vào CI/CD pipelines (GitHub Actions, Jenkins, v.v.)

**Tác Động:**
- Dẫn đến các lỗi tiềm ẩn trong quá trình triển khai
- Yêu cầu sự can thiệp của con người để thiết lập cấu hình
- Quản lý cấu hình trên tất cả các instance microservice trở nên khó khăn
- Nguy cơ sai sót cấu hình ngay cả khi có tự động hóa

### 2. Thiếu Kiểm Soát Phiên Bản và Audit

**Vấn Đề:**
- Với hàng trăm microservices, bạn sẽ có hàng nghìn thuộc tính cấu hình
- Các thuộc tính cấu hình phát triển và thay đổi hàng ngày
- Spring Boot profiles lưu trữ tất cả cấu hình trong source code
- Bất kỳ ai có quyền truy cập vào source code hoặc Docker images đều có thể xem tất cả cấu hình

**Tính Năng Cần Thiết:**
- Phiên bản hóa cấu hình dựa trên releases
- Chức năng audit:
  - Ai đã truy cập dữ liệu cấu hình
  - Client nào đã truy cập dữ liệu cấu hình
- Repository tập trung với version control
- Theo dõi các revisions và thay đổi

**Hạn Chế Hiện Tại:**
Spring Boot profiles đơn thuần không thể cung cấp những lợi thế này, khiến đây trở thành một hạn chế đáng kể.

### 3. Vấn Đề Bảo Mật

**Nhiều Vấn Đề Bảo Mật:**

#### a) Thiếu Kiểm Soát Truy Cập Chi Tiết
- Environment variables hiển thị cho tất cả quản trị viên server
- Thông tin đăng nhập database được lưu trữ dưới dạng environment variables bị lộ cho server admins
- Không có cơ chế kiểm soát truy cập chi tiết

#### b) Mật Khẩu Dạng Plain Text
- Mật khẩu database và dữ liệu nhạy cảm phải được lưu trữ ở dạng plain text
- Áp dụng cho tất cả các phương pháp: CLI, JVM properties, environment variables và Spring Boot profiles
- Không hỗ trợ mã hóa/giải mã
- Không thể lưu trữ secrets một cách bảo mật trong ứng dụng

#### c) Lộ Cấu Hình
- Cấu hình trong Spring Boot profiles được nhúng trong source code
- Bất kỳ ai có quyền truy cập code đều có thể xem tất cả cấu hình
- Không khôn ngoan khi để lộ tất cả cấu hình cho mọi người

### 4. Thách Thức Về Khả Năng Mở Rộng

**Kịch Bản:**
- 3 microservices (accounts, loans, cards)
- 3 instances mỗi microservice = 9 containers tổng cộng
- Mở rộng lên 100 microservices × 5 instances = 500 instances

**Vấn Đề:**
- Cung cấp cấu hình externalized cho hàng trăm instances cực kỳ khó khăn
- Các tác vụ thủ công phải được lặp lại cho từng microservice instance
- Phương pháp hiện tại không hoạt động cho nhiều microservice instances
- Quản lý cấu hình trở nên không thể quản lý được ở quy mô lớn

### 5. Không Cập Nhật Cấu Hình Tại Runtime

**Vấn Đề:**
- Bất kỳ thay đổi giá trị property nào đều yêu cầu restart ứng dụng
- Không thể thay đổi properties trong khi microservices đang chạy
- Phải restart tất cả containers/microservices để áp dụng thay đổi cấu hình

**Hành Vi Mong Muốn:**
- Microservices nên tự động đọc các giá trị property mới nhất
- Không cần restart cho việc cập nhật cấu hình
- Khả năng làm mới cấu hình động

## Kết Luận

Với tất cả những hạn chế này, chỉ riêng Spring Boot là không đủ để quản lý cấu hình trong các ứng dụng microservices.

### Khi Nào Chỉ Sử Dụng Spring Boot:

1. **Dự Án Nhỏ:** Số lượng properties rất hạn chế với các ứng dụng mức độ nghiêm trọng thấp
2. **Thiếu Kiến Thức:** Các team không biết về các tùy chọn quản lý cấu hình nâng cao

## Giải Pháp: Spring Cloud Config Server

Để vượt qua tất cả những thách thức này, giải pháp được đề xuất là **Spring Cloud Config Server**, cung cấp:

- Quản lý cấu hình tập trung
- Version control và auditing
- Tính năng bảo mật nâng cao
- Hỗ trợ mã hóa/giải mã
- Cập nhật cấu hình động không cần restart
- Quản lý cấu hình có thể mở rộng cho hàng trăm microservices

## Các Bước Tiếp Theo

Các bài giảng tiếp theo sẽ đề cập đến việc triển khai và sử dụng Spring Cloud Config Server để giải quyết tất cả các hạn chế đã thảo luận ở trên.

---

**Ghi Chú Khóa Học:** Nội dung này là một phần của khóa học microservices toàn diện tập trung vào các công nghệ Spring Boot và Spring Cloud.




FILE: 67-spring-cloud-config-introduction.md


# Giới Thiệu Spring Cloud Config

## Tổng Quan

Trong các bài giảng trước, chúng ta đã thảo luận về cách quản lý cấu hình trong microservices chỉ với Spring Boot. Tuy nhiên, cách tiếp cận này có nhiều hạn chế và nhược điểm. Bài giảng này giới thiệu một phương pháp tốt hơn, được khuyến nghị cho các tổ chức đang xây dựng hàng trăm microservices: **Spring Cloud Config**.

## Spring Cloud Config là gì?

Spring Cloud Config là một dự án trong hệ sinh thái Spring được thiết kế để xử lý cấu hình trong các hệ thống cloud-native như microservices. Nó cung cấp một máy chủ cấu hình tập trung, hỗ trợ cả phía server và client cho các cấu hình được externalized trong các hệ thống phân tán.

## Khái Niệm Cốt Lõi

Cách tiếp cận này bao gồm việc xây dựng một ứng dụng riêng biệt hoạt động như một **máy chủ cấu hình tập trung** (centralized configuration server). Máy chủ này:

- Hoạt động như nơi trung tâm để quản lý tất cả các thuộc tính và cấu hình bên ngoài
- Hỗ trợ tất cả microservices trên mọi môi trường
- Cho phép các microservices đăng ký như các clients
- Cung cấp hỗ trợ phía server và client cho cấu hình externalized

## Hai Yếu Tố Cốt Lõi

Máy chủ config tập trung xoay quanh hai yếu tố cơ bản:

### 1. Lưu Trữ Cấu Hình Tập Trung

Bạn có thể tự do lưu trữ tất cả các cấu hình hoặc property files ở bất kỳ vị trí nào:

- **GitHub repository**
- **File system** (hệ thống tệp)
- **Database** (cơ sở dữ liệu)
- **Classpath**
- Nhiều tùy chọn khác được hỗ trợ bởi Spring Cloud Config Server

Chọn một vị trí mà bạn muốn lưu trữ tất cả các cấu hình và properties một cách an toàn.

### 2. Configuration Server (Máy Chủ Cấu Hình)

Sau khi bạn lưu trữ tất cả các properties hoặc cấu hình:

- Máy chủ cấu hình giám sát dữ liệu cấu hình trong kho dữ liệu
- Tạo điều kiện quản lý và phân phối đến nhiều ứng dụng (microservices)
- Tải tất cả các cấu hình bằng cách kết nối với repository tập trung của bạn
- Giữ các properties của tất cả microservices và môi trường

## Cách Hoạt Động

Quy trình làm việc tuân theo các bước sau:

1. **Lưu trữ cấu hình** trong một repository tập trung (database, GitHub repo, file system, hoặc classpath)

2. **Tạo một configuration server** với Spring Cloud Config kết nối đến repository tập trung của bạn

3. **Microservices kết nối như config clients** trong quá trình khởi động để tải cấu hình của chúng

### Luồng Ví Dụ

```
Microservices (Loans, Accounts, Cards)
         ↓
    Kết nối khi Khởi động
         ↓
Máy Chủ Cấu Hình Tập Trung
         ↓
Repository Tập Trung (GitHub/Database/FileSystem)
```

Tất cả các microservices (như loans, accounts, và cards) kết nối với máy chủ cấu hình tập trung trong quá trình khởi động. Theo cách này:

- Các properties và cấu hình được ủy thác cho một vị trí bên ngoài
- Microservices đọc các properties này trong quá trình khởi động dựa trên profile được kích hoạt
- Tất cả các hạn chế của Spring Boot đơn thuần đều được khắc phục

## Lợi Ích

- **Quản lý tập trung**: Nguồn chân lý duy nhất cho tất cả cấu hình
- **Cấu hình theo môi trường**: Hỗ trợ nhiều môi trường
- **Cập nhật động**: Cấu hình có thể được cập nhật mà không cần triển khai lại
- **Kiểm soát phiên bản**: Khi sử dụng Git, cấu hình được quản lý phiên bản
- **Bảo mật**: Bảo mật tập trung cho các cấu hình nhạy cảm
- **Khả năng mở rộng**: Hỗ trợ hàng trăm microservices

## Hệ Sinh Thái Spring Cloud

Spring Cloud Config là một phần của dự án **Spring Cloud** lớn hơn, cung cấp nhiều framework cho các nhà phát triển để nhanh chóng xây dựng các mẫu phổ biến trong microservices và ứng dụng cloud-native.

### Các Dự Án Spring Cloud Phổ Biến

- **Spring Cloud Config**: Quản lý cấu hình
- **Service Registration and Discovery**: Service registry
- **Routing and Tracing**: API gateway và định tuyến request
- **Load Balancing**: Cân bằng tải phía client
- **Spring Cloud Security**: Các mẫu bảo mật
- **Distributed Tracing**: Theo dõi request qua các services
- **Messaging**: Giao tiếp theo hướng sự kiện

## Điểm Chính Cần Nhớ

- Spring Cloud Config cung cấp phương pháp tập trung cho quản lý cấu hình
- Nó hỗ trợ nhiều backend storage cho các tệp cấu hình
- Microservices hoạt động như config clients, tải cấu hình khi khởi động
- Spring Cloud khác với Spring Boot - nó được xây dựng trên Spring Boot
- Nhiều dự án Spring Cloud sẽ được sử dụng trong suốt quá trình phát triển microservices

## Tài Nguyên

- Trang web chính thức: [spring.io](https://spring.io)
- Điều hướng đến: Projects → Spring Cloud → Spring Cloud Config
- Tài liệu chính thức cung cấp thông tin chi tiết về tất cả các tùy chọn được hỗ trợ

## Các Bước Tiếp Theo

Trong các bài giảng tiếp theo, chúng ta sẽ bắt đầu triển khai Spring Cloud Config trong các ứng dụng microservices của mình. Các khái niệm sẽ trở nên rõ ràng hơn thông qua việc thực hành.

---

**Lưu ý**: Đây là phần giới thiệu về Spring Cloud Config. Hãy tập trung vào việc hiểu các khái niệm cốt lõi về quản lý cấu hình tập trung và cách microservices tương tác với config server.




FILE: 68-tao-spring-cloud-config-server.md


# Tạo Spring Cloud Config Server

## Tổng Quan
Hướng dẫn này trình bày cách tạo một Config Server riêng biệt sử dụng Spring Cloud Config để quản lý cấu hình tập trung trong kiến trúc microservices.

## Thiết Lập Cấu Trúc Dự Án

### Trạng Thái Hiện Tại
- Vị trí: `section6/v1-springboot`
- Chứa ba microservices:
  - Accounts (Tài khoản)
  - Cards (Thẻ)
  - Loans (Khoản vay)
- Quản lý cấu hình: Chỉ sử dụng Spring Boot

### Chuyển Sang Spring Cloud Config
Thay vì chỉnh sửa thư mục v1-springboot hiện tại, chúng ta sẽ tạo phiên bản mới:

1. **Sao chép thư mục** `v1-springboot`
2. **Đổi tên thành** `v2-spring-cloud-config`
3. Cách này giữ lại tham chiếu cho cả hai phương pháp:
   - v1: Cấu hình Spring Boot
   - v2: Spring Cloud Config

### Dọn Dẹp
- Xóa thư mục `.idea` (thư mục workspace của IntelliJ)
- Thư mục này thuộc về workspace trước đó

## Tạo Dự Án Config Server

### Sử Dụng Spring Initializr

Truy cập [start.spring.io](https://start.spring.io) và cấu hình:

#### Metadata Dự Án
- **Loại Dự Án:** Maven
- **Ngôn Ngữ:** Java
- **Phiên Bản Spring Boot:** 3.1.2 (hoặc phiên bản ổn định mới nhất)
- **Group:** `com.eazybytes`
- **Artifact ID:** `configserver`
- **Tên:** `configserver`
- **Mô Tả:** `Config Server for EazyBank Microservices`
- **Packaging:** JAR

> **Lưu Ý:** Luôn sử dụng phiên bản Spring Boot ổn định mới nhất. Repository GitHub sẽ được cập nhật hàng quý.

#### Dependencies (Thư Viện Phụ Thuộc)
Thêm các dependencies sau:

1. **Config Server**
   - Mục đích: Quản lý cấu hình tập trung qua Git, SVN, hoặc HashiCorp Vault
   - Sử dụng để xây dựng configuration server

2. **Spring Boot Actuator**
   - Mục đích: Giám sát và quản lý ứng dụng
   - Tính năng: Kiểm tra health, metrics, quản lý session

### Hiểu Về Versioning Spring Cloud

Khi bạn xem `pom.xml`:
- **Phiên Bản Spring Boot:** 3.1.2
- **Phiên Bản Spring Cloud:** 2022.0.3

#### Tại Sao Số Phiên Bản Khác Nhau?
- Spring Boot và Spring Cloud là các dự án riêng biệt trong hệ sinh thái Spring
- Mỗi dự án có số phiên bản độc lập
- `start.spring.io` tự động ánh xạ các phiên bản tương thích

#### Tham Chiếu Ánh Xạ Phiên Bản
Truy cập [trang web Spring Cloud](https://spring.io/projects/spring-cloud) để xem release train:

| Phiên Bản Spring Boot | Phiên Bản Spring Cloud |
|----------------------|------------------------|
| 3.0.x - 3.1.x       | 2022.0.3              |
| Phiên bản cũ hơn     | Xem tài liệu          |

#### Sự Thật Thú Vị: Tên Phiên Bản Spring Cloud
Các phiên bản Spring Cloud được đặt tên theo các ga tàu điện ngầm London:
- Dalston
- Edgware
- Finchley
- Greenwich
- Hoxton
- Ilford
- Jubilee
- Kilburn

Chú ý thứ tự theo bảng chữ cái: D, E, F, G, H, I, J, K!

## Thiết Lập Config Server

### 1. Giải Nén và Import Dự Án

1. **Generate** dự án từ Spring Initializr
2. **Giải nén** file `configserver.zip` đã tải xuống
3. **Sao chép** vào thư mục `v2-spring-cloud-config`
4. **Mở** trong IntelliJ IDEA

### 2. Cấu Hình Main Application Class

Mở `ConfigServerApplication.java` và thêm annotation:

```java
@EnableConfigServer
@SpringBootApplication
public class ConfigServerApplication {
    public static void main(String[] args) {
        SpringApplication.run(ConfigServerApplication.class, args);
    }
}
```

Annotation `@EnableConfigServer` kích hoạt chức năng Config Server.

### 3. Cấu Hình Application Properties

1. **Đổi tên** `application.properties` thành `application.yml`
2. **Cấu hình** cổng server:

```yaml
server:
  port: 8071
```

> **Quan Trọng:** Sử dụng cổng 8071 nhất quán trong suốt khóa học để tránh các vấn đề cấu hình.

## Tùy Chọn Lưu Trữ Cấu Hình

Config Server cần một vị trí tập trung để đọc cấu hình. Có nhiều tùy chọn khả dụng:

### 1. Classpath
Lưu trữ cấu hình trong classpath của Config Server.

### 2. File System (Hệ Thống File)
Lưu trữ cấu hình trong bất kỳ thư mục nào trên server hoặc hệ thống local của bạn.

### 3. Git Repository (Phổ Biến Nhất)
Lưu trữ cấu hình trong repository GitHub.

### Các Tùy Chọn Khác
- Database (Cơ sở dữ liệu)
- AWS S3
- HashiCorp Vault

## Các Bước Tiếp Theo

Trong các bài giảng tiếp theo, chúng ta sẽ khám phá ba phương pháp:
1. Cấu hình dựa trên Classpath
2. Cấu hình dựa trên File System
3. Cấu hình dựa trên GitHub

## Cấu Trúc Dự Án Sau Khi Thiết Lập

```
v2-spring-cloud-config/
├── accounts/
├── cards/
├── loans/
└── configserver/
```

Tất cả bốn dự án Maven nên được load trong IntelliJ workspace của bạn.

## Tóm Tắt

- Đã tạo một dự án Config Server riêng biệt sử dụng Spring Cloud Config
- Đã cấu hình server chạy trên cổng 8071
- Đã chuẩn bị cho quản lý cấu hình tập trung
- Duy trì khả năng tương thích ngược với v1 (chỉ Spring Boot)

## Các Annotation Chính
- `@EnableConfigServer` - Kích hoạt chức năng Spring Cloud Config Server

## Các Dependencies Chính
- `spring-cloud-config-server` - Triển khai Config Server
- `spring-boot-starter-actuator` - Giám sát và quản lý ứng dụng

---

*Đây là một phần của khóa học EazyBank Microservices về Spring Cloud Config.*




FILE: 69-luu-tru-cau-hinh-microservices-trong-config-server.md


# Lưu Trữ Cấu Hình Microservices Trong Config Server

## Tổng Quan
Bài học này trình bày cách lưu trữ tất cả cấu hình của microservices bên trong classpath của Spring Cloud Config Server và làm cho chúng có thể truy cập được bởi các microservices riêng lẻ.

## Thiết Lập Tên Ứng Dụng Cho Config Server

Đầu tiên, cấu hình tên ứng dụng cho Config Server trong file `application.yml`:

```yaml
spring:
  application:
    name: configserver
```

**Quan trọng:** Tất cả các ứng dụng Spring Boot nên có tên được gán thông qua thuộc tính `spring.application.name`. Điều này rất cần thiết để Spring Cloud Config Server hoạt động đúng cách.

## Tạo Cấu Trúc Thư Mục Cấu Hình

1. Tạo thư mục `config` bên trong thư mục `resources`
2. Thư mục này sẽ lưu trữ tất cả cấu hình liên quan đến microservices

## Quy Ước Đặt Tên Cho File Cấu Hình

### Thách Thức
Nếu nhiều microservices sử dụng cùng tên file (ví dụ: `application.yml`, `application-prod.yml`), sẽ tạo ra sự nhầm lẫn cho Config Server.

### Giải Pháp
Đặt tên file cấu hình sử dụng tên microservice/ứng dụng làm tiền tố:

- `accounts.yml` - Profile mặc định cho microservice accounts
- `accounts-prod.yml` - Profile production cho microservice accounts
- `accounts-qa.yml` - Profile QA cho microservice accounts

**Quan trọng:** Sử dụng dấu gạch ngang (`-`) không phải dấu gạch dưới (`_`) làm ký tự phân cách.

## Thiết Lập File Cấu Hình

### File Cho Microservice Accounts

Tạo ba file cấu hình trong thư mục `config`:

1. **accounts.yml** - Chứa thuộc tính profile mặc định
2. **accounts-prod.yml** - Chứa thuộc tính profile production  
3. **accounts-qa.yml** - Chứa thuộc tính profile QA

### Hướng Dẫn Về Nội Dung

Mỗi file nên chứa:
- Thông tin phiên bản build
- Thông điệp đặc thù cho microservice
- Chi tiết liên hệ
- Thông tin hỗ trợ on-call

**Loại bỏ khỏi các file này:**
- Cấu hình `server.port`
- Thuộc tính kết nối cơ sở dữ liệu (ví dụ: cài đặt H2)
- Câu lệnh `spring.config.import`

Các thuộc tính này được quản lý bởi các microservices riêng lẻ, không được externalize.

### Microservices Cards và Loans

Theo cùng mẫu, tạo:
- `cards.yml`, `cards-prod.yml`, `cards-qa.yml`
- `loans.yml`, `loans-prod.yml`, `loans-qa.yml`

## Cấu Hình Spring Cloud Config Server

Cập nhật file `application.yml` của Config Server:

```yaml
spring:
  application:
    name: configserver
  profiles:
    active: native
  cloud:
    config:
      server:
        native:
          search-locations: classpath:/config
```

### Giải Thích Cấu Hình

- **`spring.profiles.active: native`** - Kích hoạt profile native, bắt buộc khi sử dụng classpath để lưu trữ cấu hình
- **`spring.cloud.config.server.native.search-locations`** - Chỉ định vị trí lưu trữ cấu hình (`classpath:/config`)

## Build và Khởi Động Config Server

1. Bật annotation processing (cần thiết cho Lombok)
2. Build ứng dụng
3. Khởi động ở chế độ debug
4. Server sẽ khởi động trên cổng 8071

## Xác Thực Configuration Server

### Các API Endpoint

Config Server cung cấp các đường dẫn GET API để lấy cấu hình:

```
http://localhost:8071/{application}/{profile}
```

### Ví Dụ

- `http://localhost:8071/accounts/prod` - Profile production cho accounts
- `http://localhost:8071/accounts/qa` - Profile QA cho accounts
- `http://localhost:8071/accounts/default` - Profile mặc định cho accounts
- `http://localhost:8071/loans/prod` - Profile production cho loans
- `http://localhost:8071/cards/qa` - Profile QA cho cards

### Hành Vi Mong Đợi

Khi truy cập một profile cụ thể:
- Các thuộc tính từ profile được yêu cầu sẽ được tải
- Các thuộc tính từ profile mặc định cũng được tải
- Trong quá trình khởi động microservice, các thuộc tính của profile cụ thể sẽ ghi đè giá trị mặc định

### Định Dạng Response

API trả về JSON chứa:
- Thuộc tính của profile cụ thể
- Thuộc tính của profile mặc định
- Metadata cấu hình

**Mẹo:** Cài đặt extension Chrome "JSON View" để xem response JSON được định dạng đẹp.

## Các Vấn Đề Thường Gặp

### Đặt Tên File Không Đúng
**Vấn đề:** Sử dụng dấu gạch dưới (`_`) thay vì dấu gạch ngang (`-`) trong tên file (ví dụ: `accounts_prod.yml`)

**Giải pháp:** Sử dụng dấu gạch ngang: `accounts-prod.yml`

Đây là quy ước đặt tên quan trọng - thậm chí một lỗi ký tự đơn cũng có thể gây ra lỗi tải cấu hình.

## Tóm Tắt

Đã hoàn thành thành công:
1. ✅ Tạo Config Server với tên ứng dụng
2. ✅ Thiết lập cấu trúc thư mục cấu hình
3. ✅ Tạo file cấu hình cho microservices accounts, cards, và loans
4. ✅ Cấu hình native profile cho lưu trữ classpath
5. ✅ Khởi động và xác thực Config Server
6. ✅ Xác minh tất cả profiles tải đúng thông qua các API endpoint

## Các Bước Tiếp Theo

Bài học tiếp theo sẽ đề cập đến việc thiết lập kết nối giữa các microservices riêng lẻ và Spring Cloud Config Server, cho phép các microservices lấy cấu hình của chúng trong quá trình khởi động dựa trên profile đang hoạt động.




FILE: 7-tao-rest-api-voi-spring-boot.md


# Tạo REST API trong Spring Boot

## Tổng quan
Hướng dẫn này minh họa cách tạo một REST API cơ bản trong ứng dụng Spring Boot trả về phản hồi "Hello World". Chúng ta sẽ tìm hiểu các khái niệm và bước cần thiết để xây dựng và chạy endpoint REST đầu tiên.

## Yêu cầu trước
- Đã tạo ứng dụng web Spring Boot cơ bản
- IntelliJ IDEA hoặc IDE tương tự
- Hiểu biết về các khái niệm cơ bản của Spring Boot

## Bước 1: Tạo Package Controller
Đầu tiên, tạo cấu trúc package mới để tổ chức các REST controller:
```
com.eazybytes.accounts.controller
```

## Bước 2: Tạo Class Accounts Controller
Bên trong package controller, tạo một class mới có tên `AccountsController`. Class này sẽ chứa tất cả các REST API liên quan đến microservice accounts.

```java
package com.eazybytes.accounts.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AccountsController {
    
    @GetMapping("/say-hello")
    public String sayHello() {
        return "Hello World";
    }
}
```

## Hiểu về các Annotation

### @RestController
- Đặt annotation này ở trên class của bạn
- Hướng dẫn Spring Boot framework rằng class này sẽ chứa các phương thức REST API
- Yêu cầu Spring Boot expose các phương thức có annotation HTTP ra bên ngoài dưới dạng REST API

### @GetMapping
- Chỉ ra rằng phương thức hỗ trợ HTTP GET request
- Được sử dụng khi API chỉ trả về dữ liệu cho client
- Yêu cầu tham số path để chỉ định URL endpoint

**Cú pháp:**
```java
@GetMapping("/say-hello")
```

## Bước 3: Build và Chạy Ứng dụng

1. **Bật Annotation Processing**
   - Khi build lần đầu tiên, IDE sẽ nhắc bạn bật annotation processing
   - Điều này cần thiết để hỗ trợ thư viện Lombok
   - Hãy bật nó để tiếp tục

2. **Build Project**
   - Thực hiện build trong IDE của bạn
   - Đảm bảo tất cả dependencies đã được resolve

3. **Khởi động Ứng dụng**
   - Điều hướng đến class chính Spring Boot (ví dụ: `AccountsApplication`)
   - Chạy ứng dụng ở chế độ debug
   - Ứng dụng sẽ khởi động mặc định trên cổng 8080

## Điều gì xảy ra Đằng sau

Khi ứng dụng khởi động, Spring Boot tự động:
- Nhận diện H2 database trong dependencies và hoàn tất auto-configuration cho H2 console
- Cấu hình Spring Boot Actuator dựa trên dependencies trong `pom.xml`
- Deploy ứng dụng web lên embedded Tomcat server tại cổng 8080
- Thiết lập các cấu hình mặc định mà không cần setup thủ công

**Lợi ích chính:**
- Không cần chỉ định số port
- Không cần cấu hình thiết lập server
- Không cần cung cấp chi tiết kết nối database
- Spring Boot giả định các giá trị mặc định hợp lý

## Bước 4: Kiểm tra API

1. Mở trình duyệt web
2. Truy cập: `http://localhost:8080/say-hello`
3. Bạn sẽ thấy phản hồi: **"Hello World"**

**Lưu ý:** Gọi URL từ trình duyệt tự động sử dụng HTTP GET method, phù hợp với annotation `@GetMapping` của chúng ta.

## Spring Boot DevTools - Tính năng Hot Reload

Spring Boot bao gồm các công cụ năng suất như DevTools giúp cải thiện hiệu quả làm việc của developer thông qua chức năng tự động restart.

### Cách hoạt động:
1. Thực hiện thay đổi code (ví dụ: đổi "Hello World" thành "Hi World")
2. Lưu các thay đổi
3. Build project
4. Spring Boot tự động restart ứng dụng

**Hiệu suất:**
- Khởi động ban đầu: ~6.834 giây
- Restart sau thay đổi: ~8 milliseconds
- Chỉ các class thay đổi được reload (ví dụ: `AccountsController`)

### So sánh với Cách tiếp cận Truyền thống
Trong các ứng dụng monolithic không dùng Spring Boot:
- Cần restart thủ công cho mỗi thay đổi
- Thời gian restart dài hơn đáng kể
- Giảm năng suất developer hàng ngày

## Cấu hình Theme cho IntelliJ IDEA

### Cài đặt Theme
1. Mở **IntelliJ IDEA**
2. Vào **Preferences/Settings**
3. Điều hướng đến **Plugins**
4. Click vào **Marketplace**
5. Tìm kiếm các theme:
   - **Dark Purple Theme** của JetBrains
   - **One Dark Theme** của Mark Skelton
6. Click **Install** cho theme bạn thích
7. Restart IDE nếu được nhắc

### Áp dụng Theme
1. Vào **Preferences/Settings**
2. Tìm kiếm "theme"
3. Điều hướng đến **Appearance & Behavior** → **Appearance**
4. Chọn theme ưa thích từ dropdown

## Bật Lombok Annotation Processing

Để sử dụng các annotation Lombok trong khóa học:

1. Mở **Preferences/Settings**
2. Tìm kiếm "annotation"
3. Điều hướng đến **Build, Execution, Deployment** → **Compiler** → **Annotation Processors**
4. Chọn **Enable annotation processing**
5. Click **Apply** và **OK**

**Quan trọng:** Không có thiết lập này, các annotation Lombok sẽ không hoạt động đúng.

## Những điểm chính cần nhớ

1. **@RestController** đánh dấu một class là REST API controller
2. **@GetMapping** định nghĩa các HTTP GET endpoint với path cụ thể
3. Spring Boot xử lý auto-configuration dựa trên dependencies
4. DevTools cho phép phát triển nhanh với hot reload
5. Các request từ trình duyệt sử dụng GET method mặc định
6. Cần cấu hình tối thiểu để tạo một microservice hoạt động

## Tóm tắt

Spring Boot framework làm cho việc xây dựng microservices trở nên cực kỳ dễ dàng. Với kiến thức về các bước cơ bản này, bạn có thể tạo template hoặc skeleton microservice trong vòng 1-2 phút, sau đó cập nhật nó với logic nghiệp vụ của riêng bạn. Auto-configuration và các công cụ năng suất giảm đáng kể thời gian và công sức phát triển.

## Bước tiếp theo
Trong các bài giảng sắp tới, chúng ta sẽ khám phá:
- Ghi đè các cấu hình mặc định của Spring Boot
- Các mẫu REST API nâng cao
- Tích hợp database
- Các annotation Lombok bổ sung




FILE: 70-integrating-microservices-with-spring-cloud-config-server.md


# Tích Hợp Microservices với Spring Cloud Config Server

## Tổng Quan

Hướng dẫn này trình bày cách kết nối một microservice (accounts) với Spring Cloud Config Server để quản lý cấu hình tập trung. Bằng cách chuyển các thuộc tính cấu hình sang một kho lưu trữ tập trung, bạn có thể quản lý nhiều môi trường (dev, qa, prod) hiệu quả hơn.

## Yêu Cầu Trước

- Microservice accounts đã được tạo
- Spring Cloud Config Server đã được thiết lập và đang chạy
- Các file cấu hình đã được lưu trữ trong Config Server (accounts.yml, accounts-prod.yml, accounts-qa.yml)

## Bước 1: Dọn Dẹp Các File Cấu Hình Local

Đầu tiên, xóa các file cấu hình theo profile không cần thiết khỏi microservice accounts:

1. Xóa các file `application-prod.yml` và `application-qa.yml`
2. Mở file `application.yml` và xóa:
   - Các câu lệnh config import
   - Cài đặt kích hoạt profile
   - Các thuộc tính build version

Chỉ giữ lại các thuộc tính thiết yếu như:
- Cổng server
- Cấu hình Spring Data JPA/database

## Bước 2: Cấu Hình Tên Application

Thêm tên application vào `application.yml`. Tên này phải khớp với tên các file cấu hình trong Config Server:

```yaml
spring:
  application:
    name: accounts  # Phải khớp với tiền tố file cấu hình (accounts.yml, accounts-prod.yml, v.v.)
  profiles:
    active: prod    # Kích hoạt profile mặc định
```

**Quan trọng**: Config Server sử dụng tên application này để xác định file cấu hình nào sẽ được cung cấp cho microservice này.

## Bước 3: Thêm Dependency Spring Cloud Config Client

Thêm dependency Spring Cloud Config Client vào `pom.xml`:

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-config</artifactId>
</dependency>
```

## Bước 4: Cấu Hình Phiên Bản Spring Cloud

Vì đây là dependency Spring Cloud đầu tiên trong microservice accounts, hãy thêm thuộc tính phiên bản Spring Cloud và quản lý dependency:

```xml
<properties>
    <java.version>17</java.version>
    <spring-cloud.version>2023.0.0</spring-cloud.version>
</properties>

<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-dependencies</artifactId>
            <version>${spring-cloud.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

Sau khi thêm các thay đổi này, tải lại các dependency Maven.

## Bước 5: Cấu Hình Kết Nối Config Server

Thêm URL Config Server vào `application.yml`:

```yaml
spring:
  config:
    import: "optional:configserver:http://localhost:8071"
```

**Các Điểm Chính**:
- Tiền tố `configserver:` - Cho biết kết nối đến Config Server
- Tiền tố `optional:` - Cho phép microservice khởi động ngay cả khi Config Server không khả dụng (sẽ hiển thị cảnh báo nhưng không thất bại)
- Cổng `8071` - Cổng mà Config Server đang chạy
- Xóa `optional:` nếu cấu hình là quan trọng và microservice không nên khởi động nếu thiếu nó

## Bước 6: Khởi Động và Kiểm Tra Microservice

1. Khởi động microservice accounts
2. Kiểm tra console logs để xác minh kết nối Config Server
3. Tìm các thông báo kích hoạt profile (ví dụ: "activated profile: prod")

### Kiểm Tra với Postman

Kiểm tra các endpoint sau để xác minh cấu hình được tải đúng:

**Contact Info API** (kiểm tra thuộc tính theo profile):
```
GET http://localhost:8080/api/contact-info
```
Kết quả mong đợi cho profile prod:
```json
{
    "message": "Properties from prod",
    "contactDetails": {
        "name": "Product Owner",
        "email": "call support"
    }
}
```

**Build Info API** (kiểm tra thuộc tính version):
```
GET http://localhost:8080/api/build-info
```
Kết quả mong đợi cho profile prod:
```json
{
    "version": "1.0"
}
```

## Bước 7: Ghi Đè Profile bằng Cấu Hình Bên Ngoài

Bạn có thể ghi đè profile mặc định bằng cách sử dụng tham số dòng lệnh:

1. Nhấp chuột phải vào ứng dụng accounts
2. Chọn "Modify Run Configurations"
3. Thêm vào Program Arguments:
```
--spring.profiles.active=qa
```
4. Apply và khởi động lại microservice

### Kiểm Tra Profile QA

Sau khi khởi động lại với profile QA:

**Build Info API**:
```
GET http://localhost:8080/api/build-info
```
Kết quả mong đợi:
```json
{
    "version": "2.0"
}
```

**Contact Info API**:
```
GET http://localhost:8080/api/contact-info
```
Kết quả mong đợi (thuộc tính profile QA):
```json
{
    "message": "Properties from qa",
    "contactDetails": {
        "name": "QA Team",
        "email": "qa support"
    }
}
```

## Cách Hoạt Động

1. **Khởi động**: Khi microservice accounts khởi động, nó đọc `spring.application.name` và `spring.profiles.active`
2. **Kết nối**: Nó kết nối đến Config Server tại URL đã chỉ định
3. **Yêu cầu**: Nó yêu cầu cấu hình theo mẫu: `{application-name}-{profile}.yml`
4. **Phản hồi**: Config Server trả về các file cấu hình phù hợp
5. **Tải**: Microservice tải các thuộc tính này và sử dụng chúng trong runtime

## Lợi Ích của Phương Pháp Này

- **Cấu Hình Tập Trung**: Tất cả thuộc tính theo môi trường ở một nơi
- **Cập Nhật Dễ Dàng**: Thay đổi cấu hình mà không cần rebuild microservices
- **Linh Hoạt Môi Trường**: Chuyển đổi giữa các môi trường bằng cấu hình bên ngoài
- **Quản Lý Phiên Bản**: Cấu hình có thể được quản lý phiên bản trong Git
- **Bảo Mật**: Các thuộc tính nhạy cảm có thể được mã hóa trong Config Server

## Bước Tiếp Theo

Áp dụng cùng một tích hợp cho các microservices khác (cards, loans):
1. Thêm các dependency tương tự
2. Cấu hình tên application
3. Thiết lập kết nối Config Server
4. Kiểm tra REST APIs để xác minh việc tải cấu hình

## Khắc Phục Sự Cố

**Vấn đề**: Microservice không khởi động được khi Config Server bị down
- **Giải pháp**: Thêm tiền tố `optional:` vào config import URL

**Vấn đề**: Thuộc tính profile sai đang được tải
- **Giải pháp**: Xác minh `spring.application.name` khớp chính xác với tên file Config Server

**Vấn đề**: Thuộc tính không cập nhật
- **Giải pháp**: Đảm bảo Config Server đang chạy và có thể truy cập được tại URL đã chỉ định

## Tóm Tắt

Bạn đã thành công:
- ✅ Dọn dẹp các file cấu hình local
- ✅ Cấu hình tên application và profile mặc định
- ✅ Thêm dependency Spring Cloud Config Client
- ✅ Kết nối microservice với Config Server
- ✅ Kiểm tra việc tải thuộc tính theo profile
- ✅ Trình bày ghi đè profile từ bên ngoài

Microservice accounts bây giờ tải tất cả cấu hình của nó từ Config Server tập trung, giúp quản lý dễ dàng hơn trên nhiều môi trường.




FILE: 71-integrating-cards-and-loans-microservices-with-config-server.md


# Tích Hợp Microservices Cards và Loans với Config Server

## Tổng Quan

Hướng dẫn này trình bày quy trình từng bước để tích hợp các microservices Cards và Loans với Spring Cloud Config Server. Quy trình giống hệt nhau cho cả hai microservices và tuân theo cùng một mẫu đã sử dụng cho microservice Accounts.

## Yêu Cầu Trước

- Các microservices Cards và Loans đã được tạo
- Spring Cloud Config Server đang chạy trên cổng 8071
- Các file cấu hình đã được chuẩn bị trong Config Server:
  - `loans.yml`, `loans-prod.yml`, `loans-qa.yml`
  - `cards.yml`, `cards-prod.yml`, `cards-qa.yml`

## Phần 1: Tích Hợp Microservice Loans

### Bước 1: Dọn Dẹp Các File Cấu Hình

Điều hướng đến microservice Loans và thực hiện dọn dẹp sau:

1. Vào thư mục `resources`
2. Xóa các file YAML theo profile:
   - `application-prod.yml`
   - `application-qa.yml`
3. Mở `application.yml` và xóa tất cả các thuộc tính đã định nghĩa trước đó

### Bước 2: Cấu Hình application.yml cho Loans

Thay thế nội dung trong `application.yml` bằng cấu hình sau:

```yaml
spring:
  application:
    name: loans  # Phải khớp với tên file Config Server (loans.yml, loans-prod.yml, v.v.)
  profiles:
    active: prod  # Kích hoạt profile mặc định
  config:
    import: "optional:configserver:http://localhost:8071"
```

**Lưu Ý Quan Trọng**:
- `spring.application.name` phải là **loans** để khớp với tên file cấu hình trong Config Server
- Profile mặc định được đặt là `prod`
- Tiền tố `optional:` cho phép microservice khởi động ngay cả khi Config Server không khả dụng

### Bước 3: Cập Nhật pom.xml cho Loans

Thêm các cấu hình sau vào `pom.xml`:

#### Thêm Thuộc Tính Phiên Bản Spring Cloud

```xml
<properties>
    <java.version>17</java.version>
    <spring-cloud.version>2022.0.3</spring-cloud.version>
</properties>
```

#### Thêm Dependency Spring Cloud Config

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-config</artifactId>
</dependency>
```

#### Thêm Dependency Management

Thêm phần này trước phần `<build>` với các plugins:

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-dependencies</artifactId>
            <version>${spring-cloud.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

**Quan Trọng**: Các cấu hình này rất cần thiết để tích hợp giữa Spring Cloud và Spring Boot hoạt động đúng cách.

### Bước 4: Rebuild và Khởi Động Microservice Loans

1. Rebuild ứng dụng để tải xuống các dependencies
2. Khởi động microservice Loans trên cổng **8090**
3. Xác minh logs khởi động hiển thị kết nối đến Config Server

### Bước 5: Kiểm Tra Tích Hợp Microservice Loans

Sử dụng Postman để kiểm tra các endpoint sau:

#### Build Info API

```
GET http://localhost:8090/api/build-info
```

**Kết Quả Mong Đợi** (từ profile prod):
```json
{
    "version": "1.0"
}
```

#### Contact Info API

```
GET http://localhost:8090/api/contact-info
```

**Kết Quả Mong Đợi** (từ profile prod):
```json
{
    "message": "Properties from prod profile",
    "contactDetails": {
        "name": "Product Owner",
        "email": "call support"
    }
}
```

✅ **Thành Công**: Nếu bạn nhận được các phản hồi này, microservice Loans đã được tích hợp thành công với Config Server!

---

## Phần 2: Tích Hợp Microservice Cards

Quy trình cho microservice Cards giống hệt với Loans. Làm theo các bước tương tự với các giá trị khác nhau.

### Bước 1: Dọn Dẹp Các File Cấu Hình

Điều hướng đến microservice Cards:

1. Vào thư mục `resources`
2. Xóa các file YAML theo profile:
   - `application-prod.yml`
   - `application-qa.yml`
3. Mở `application.yml` và xóa các thuộc tính không cần thiết

### Bước 2: Cấu Hình application.yml cho Cards

Cập nhật `application.yml` với cấu hình sau:

```yaml
spring:
  application:
    name: cards  # Phải khớp với tên file Config Server (cards.yml, cards-prod.yml, v.v.)
  profiles:
    active: prod  # Kích hoạt profile mặc định
  config:
    import: "optional:configserver:http://localhost:8071"
```

**Quan Trọng**: `spring.application.name` phải là **cards** để khớp với tên file cấu hình trong Config Server.

### Bước 3: Cập Nhật pom.xml cho Cards

Thêm các cấu hình tương tự vào `pom.xml` của microservice Cards:

#### Thêm Thuộc Tính Phiên Bản Spring Cloud

```xml
<properties>
    <java.version>17</java.version>
    <spring-cloud.version>2022.0.3</spring-cloud.version>
</properties>
```

#### Thêm Dependency Spring Cloud Config

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-config</artifactId>
</dependency>
```

#### Thêm Dependency Management

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-dependencies</artifactId>
            <version>${spring-cloud.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

### Bước 4: Rebuild và Khởi Động Microservice Cards

1. **Quan Trọng**: Rebuild microservice Cards sau khi thực hiện tất cả các thay đổi
2. Khởi động microservice Cards trên cổng **9000**
3. Xác minh microservice đang ở trạng thái running

### Bước 5: Kiểm Tra Tích Hợp Microservice Cards

Sử dụng Postman để kiểm tra các endpoint sau:

#### Build Info API

```
GET http://localhost:9000/api/build-info
```

**Kết Quả Mong Đợi** (từ profile prod):
```json
{
    "version": "1.2"
}
```

#### Contact Info API

```
GET http://localhost:9000/api/contact-info
```

**Kết Quả Mong Đợi** (từ profile prod):
```json
{
    "message": "Properties from prod profile",
    "contactDetails": {
        "name": "Product Owner",
        "email": "call support"
    }
}
```

✅ **Thành Công**: Microservice Cards bây giờ đã được tích hợp thành công với Config Server!

---

## Tóm Tắt

### Những Gì Chúng Ta Đã Hoàn Thành

Cả ba microservices (Accounts, Loans, Cards) giờ đã được tích hợp với Spring Cloud Config Server:

| Microservice | Cổng | Tên Application | Trạng Thái |
|-------------|------|------------------|--------|
| Accounts    | 8080 | accounts         | ✅ Đã Tích Hợp |
| Loans       | 8090 | loans            | ✅ Đã Tích Hợp |
| Cards       | 9000 | cards            | ✅ Đã Tích Hợp |

### Lợi Ích Chính

- **Quản Lý Tập Trung**: Tất cả thuộc tính microservice giờ được quản lý bởi Spring Cloud Config Server
- **Khả Năng Mở Rộng**: Quy trình tương tự hoạt động cho dù bạn có 3 hay 100 microservices
- **Tính Nhất Quán**: Tất cả microservices tuân theo cùng một mẫu cấu hình

### Tóm Tắt Thay Đổi Cấu Hình

Cho mỗi microservice, chúng ta đã:

1. ✅ Xóa các file YAML theo profile
2. ✅ Cập nhật `application.yml` với:
   - Tên application
   - Profile mặc định
   - Kết nối Config Server
3. ✅ Cập nhật `pom.xml` với:
   - Phiên bản Spring Cloud
   - Dependency Config Client
   - Dependency management
4. ✅ Rebuild và khởi động lại microservice
5. ✅ Kiểm tra REST APIs để xác minh tích hợp

### Hạn Chế Kiến Trúc Hiện Tại

⚠️ **Lưu Ý Quan Trọng**: Hiện tại, tất cả cấu hình được lưu trữ bên trong **classpath** của chính Config Server.

**Vấn Đề Tiềm Ẩn**:
- Bất kỳ ai có quyền truy cập vào code Config Server đều có thể xem tất cả các thuộc tính
- Không lý tưởng cho môi trường production
- Vấn đề bảo mật với dữ liệu nhạy cảm

### Bước Tiếp Theo

Trong phần tiếp theo, chúng ta sẽ giải quyết hạn chế này bằng cách:
- Chuyển cấu hình sang một **vị trí file system bên ngoài**
- Tách riêng cấu hình khỏi code Spring Cloud Config Server
- Cải thiện bảo mật và kiểm soát truy cập

## Danh Sách Kiểm Tra Khắc Phục Sự Cố

Nếu tích hợp không hoạt động, hãy xác minh:

- [ ] Tên application khớp chính xác với tên file Config Server
- [ ] Config Server đang chạy trên cổng 8071
- [ ] Phiên bản Spring Cloud được định nghĩa đúng cách
- [ ] Phần dependency management đã được thêm
- [ ] Ứng dụng đã được rebuild sau khi thay đổi pom.xml
- [ ] Cổng đúng được sử dụng cho mỗi microservice
- [ ] Tên profile khớp với các profile có sẵn trong Config Server

## Thực Hành Tốt Nhất

1. **Đặt Tên Nhất Quán**: Sử dụng tên application nhất quán trên các file Config Server và microservices
2. **Quản Lý Phiên Bản**: Giữ các phiên bản Spring Cloud đồng bộ trên tất cả microservices
3. **Luôn Rebuild**: Luôn rebuild sau khi thay đổi dependencies
4. **Kiểm Tra Kỹ Lưỡng**: Kiểm tra tất cả REST APIs sau khi tích hợp
5. **Xác Minh Logs**: Kiểm tra logs khởi động cho các thông báo kết nối Config Server

---

**Chúc Mừng!** Bạn đã tích hợp thành công tất cả các microservices với Spring Cloud Config Server. Quản lý cấu hình tập trung giờ đã được thiết lập và sẵn sàng cho các cải tiến tiếp theo.




FILE: 72-storing-config-server-configurations-in-file-system.md


# Lưu Trữ Cấu Hình Spring Cloud Config Server Trong File System

## Tổng Quan

Hướng dẫn này giải thích cách chuyển các file cấu hình từ classpath sang vị trí file system trong Spring Cloud Config Server. Phương pháp này cung cấp bảo mật và kiểm soát truy cập tốt hơn cho môi trường production.

## Tại Sao Sử Dụng Phương Pháp File System?

### Ưu Điểm

1. **Bảo Mật Tăng Cường**: Các file cấu hình được lưu trữ tại vị trí server nơi microservice được triển khai
2. **Kiểm Soát Truy Cập**: Quản trị viên server có thể thực thi các hạn chế bảo mật trên thư mục
3. **Truy Cập Hạn Chế**: Chỉ ứng dụng Config Server mới có thể truy cập các file cấu hình
4. **Sẵn Sàng Production**: Ngăn chặn truy cập trái phép vào dữ liệu cấu hình nhạy cảm

### Trường Hợp Sử Dụng

- Môi trường production yêu cầu bảo mật nghiêm ngặt
- Tổ chức có đội ngũ quản trị server chuyên dụng
- Dự án xử lý dữ liệu cấu hình nhạy cảm
- Yêu cầu tuân thủ cho quản lý cấu hình

## Yêu Cầu Trước

- Spring Cloud Config Server đã được thiết lập
- Các file cấu hình hiện tại trong classpath (thư mục resources/config)
- Vị trí file system đã được chuẩn bị để lưu trữ cấu hình

## Bước 1: Sao Chép Các File Cấu Hình Vào File System

### Xác Định Các File Cấu Hình

Từ project Config Server của bạn, xác định tất cả các file cấu hình trong:
```
src/main/resources/config/
├── accounts.yml
├── accounts-prod.yml
├── accounts-qa.yml
├── loans.yml
├── loans-prod.yml
├── loans-qa.yml
├── cards.yml
├── cards-prod.yml
└── cards-qa.yml
```

### Tạo Thư Mục File System

Chọn một vị trí trên server/hệ thống local của bạn để lưu trữ cấu hình.

**Ví Dụ Vị Trí**:

**macOS/Linux**:
```
/Users/eazybytes/documents/config
```

**Windows**:
```
C:\config
```
hoặc
```
D:\config
```

### Sao Chép Files

Sao chép tất cả các file cấu hình từ classpath đến vị trí file system bạn đã chọn.

**Xác Minh**: Điều hướng đến thư mục và đảm bảo tất cả các file có mặt:
```
users/
└── eazybytes/
    └── documents/
        └── config/
            ├── accounts.yml
            ├── accounts-prod.yml
            ├── accounts-qa.yml
            ├── loans.yml
            ├── loans-prod.yml
            ├── loans-qa.yml
            ├── cards.yml
            ├── cards-prod.yml
            └── cards-qa.yml
```

## Bước 2: Cập Nhật Cấu Hình Config Server

### Chỉnh Sửa application.yml

Mở `application.yml` trong project Config Server của bạn và cập nhật vị trí tìm kiếm.

#### Cấu Hình Hiện Tại (Classpath)

```yaml
spring:
  profiles:
    active: native
  cloud:
    config:
      server:
        native:
          search-locations: classpath:/config
```

#### Cấu Hình Mới (File System)

**Cho macOS/Linux**:
```yaml
spring:
  profiles:
    active: native  # Phải giữ 'native' cho phương pháp file system
  cloud:
    config:
      server:
        native:
          # search-locations: classpath:/config  # Comment vị trí cũ
          search-locations: file:///Users/eazybytes/documents/config
```

**Cho Windows (ổ C:)**:
```yaml
spring:
  profiles:
    active: native
  cloud:
    config:
      server:
        native:
          search-locations: file:///C:/config
```

**Cho Windows (ổ D:)**:
```yaml
spring:
  profiles:
    active: native
  cloud:
    config:
      server:
        native:
          search-locations: file:///D:/config
```

### Quy Tắc Cú Pháp Quan Trọng

1. **Tiền tố**: Sử dụng `file:` thay vì `classpath:`
2. **Dấu gạch chéo sau file:**: Sử dụng **ba dấu gạch chéo** (`///`) sau `file:`
3. **Dấu phân cách đường dẫn**: Sử dụng **hai dấu gạch chéo** (`//`) giữa các tên thư mục
4. **Profile**: Phải giữ `active: native` (không thay đổi điều này)
5. **Dấu gạch chéo**: Luôn sử dụng dấu gạch chéo (`/`), ngay cả trên Windows

### Ví Dụ Phân Tích Đường Dẫn

**Đường Dẫn macOS/Linux**:
```
file:///Users/eazybytes/documents/config
│    │   │                          │
│    │   └─ cấu trúc thư mục        └─ thư mục cấu hình
│    └─────── ba dấu gạch chéo
└────────────── tiền tố file
```

**Đường Dẫn Windows**:
```
file:///C:/config
│    │   │  │
│    │   │  └─ thư mục cấu hình
│    │   └──── ký tự ổ đĩa
│    └──────── ba dấu gạch chéo
└───────────── tiền tố file
```

## Bước 3: Rebuild và Khởi Động Lại Services

### Build Config Server

```bash
# Điều hướng đến thư mục config server
cd configserver

# Build project
mvn clean install
```

### Khởi Động Lại Theo Đúng Thứ Tự

**Quan Trọng**: Luôn khởi động Config Server trước khi khởi động các microservices khác.

1. **Dừng tất cả các services đang chạy**:
   - Microservice Accounts
   - Microservice Loans
   - Microservice Cards
   - Config Server

2. **Khởi động Config Server**:
   ```bash
   # Khởi động Config Server trên cổng 8071
   java -jar configserver.jar
   ```
   Đợi khởi động thành công.

3. **Khởi động microservices**:
   ```bash
   # Khởi động Accounts (cổng 8080)
   java -jar accounts.jar
   
   # Khởi động Loans (cổng 8090)
   java -jar loans.jar
   
   # Khởi động Cards (cổng 9000)
   java -jar cards.jar
   ```

## Bước 4: Xác Minh Việc Tải Cấu Hình

### Kiểm Tra Endpoints Config Server

Sử dụng trình duyệt hoặc Postman để xác minh Config Server có thể đọc từ file system.

#### Kiểm Tra Loans Prod Profile

```
GET http://localhost:8071/loans/prod
```

**Kết Quả Mong Đợi**:
```json
{
  "name": "loans",
  "profiles": ["prod"],
  "label": null,
  "version": null,
  "state": null,
  "propertySources": [
    {
      "name": "file:///Users/eazybytes/documents/config/loans-prod.yml",
      "source": {
        "build": {
          "version": "1.0"
        },
        "accounts": {
          "message": "Properties from prod profile",
          "contactDetails": {
            "name": "Product Owner",
            "email": "call support"
          }
        }
      }
    }
  ]
}
```

**Xác Minh Chính**: Xem thuộc tính `name` dưới `propertySources`. Nó phải hiển thị **đường dẫn file system**, không phải `classpath`.

#### Kiểm Tra Cards Profile

```
GET http://localhost:8071/cards/prod
```

**Mong Đợi**: Phản hồi phải hiển thị đường dẫn `file:///...` cho biết vị trí file system.

#### Kiểm Tra Accounts Profile

```
GET http://localhost:8071/accounts/prod
```

**Mong Đợi**: Xác nhận đường dẫn file system tương tự.

### Kiểm Tra Tích Hợp Microservice

Xác minh rằng các microservices tải thành công cấu hình từ Config Server.

#### Kiểm Tra Cards Contact Info

```
GET http://localhost:9000/api/contact-info
```

**Kết Quả Mong Đợi** (thuộc tính profile prod):
```json
{
  "message": "Properties from prod profile",
  "contactDetails": {
    "name": "Product Owner",
    "email": "call support"
  }
}
```

Điều này xác nhận:
- ✅ Config Server đọc từ file system
- ✅ Microservice Cards kết nối với Config Server
- ✅ Profile prod được kích hoạt theo mặc định
- ✅ Thuộc tính được tải đúng

#### Kiểm Tra Ngẫu Nhiên

Bạn có thể kiểm tra ngẫu nhiên các microservices khác:

```
GET http://localhost:8080/api/contact-info  # Accounts
GET http://localhost:8090/api/contact-info  # Loans
```

Tất cả phải trả về thuộc tính profile prod.

## Tóm Tắt Cấu Hình

### Những Gì Đã Thay Đổi

| Khía Cạnh | Trước (Classpath) | Sau (File System) |
|--------|-------------------|---------------------|
| Vị trí | `src/main/resources/config/` | `/Users/eazybytes/documents/config/` |
| Truy cập | Bất kỳ ai có quyền truy cập code | Bị hạn chế bởi admin server |
| Cú pháp | `classpath:/config` | `file:///Users/eazybytes/documents/config` |
| Profile | `native` | `native` (không thay đổi) |
| Bảo mật | Thấp | Cao |

### Những Gì Không Thay Đổi

- ✅ Profile phải vẫn là `native`
- ✅ Tên file cấu hình không thay đổi
- ✅ Cấu hình microservice không thay đổi
- ✅ REST API endpoints không thay đổi
- ✅ Cơ chế kích hoạt profile không thay đổi

## Ví Dụ Đường Dẫn Theo Hệ Điều Hành

### macOS

```yaml
search-locations: file:///Users/username/documents/config
search-locations: file:///opt/config
search-locations: file:///var/config
```

### Linux

```yaml
search-locations: file:///home/username/config
search-locations: file:///opt/config
search-locations: file:///etc/config
```

### Windows

```yaml
search-locations: file:///C:/config
search-locations: file:///D:/project/config
search-locations: file:///C:/Users/username/documents/config
```

## Thực Hành Bảo Mật Tốt Nhất

### Quyền Thư Mục

**Linux/macOS**:
```bash
# Đặt quyền hạn chế
chmod 700 /Users/eazybytes/documents/config

# Chỉ user config server có thể đọc
chown configserver:configserver /Users/eazybytes/documents/config
```

**Windows**:
- Nhấp chuột phải vào thư mục → Properties → Security
- Xóa tất cả users trừ tài khoản service Config Server
- Cấp quyền chỉ đọc cho Config Server

### Quyền File

```bash
# Đặt các file cấu hình ở chế độ chỉ đọc
chmod 400 /Users/eazybytes/documents/config/*.yml
```

### Mã Hóa

Đối với các thuộc tính nhạy cảm, xem xét:
- Mã hóa Spring Cloud Config
- Quản lý secret bên ngoài (Vault, AWS Secrets Manager)
- Biến môi trường cho credentials

## Khắc Phục Sự Cố

### Config Server Không Tìm Thấy Files

**Triệu Chứng**: Config Server khởi động nhưng trả về cấu hình rỗng

**Giải Pháp**:
1. Xác minh đường dẫn file là chính xác (kiểm tra ký tự ổ đĩa, tên thư mục)
2. Đảm bảo ba dấu gạch chéo sau `file:`
3. Kiểm tra quyền thư mục
4. Xác minh files tồn tại tại vị trí đã chỉ định
5. Sử dụng đường dẫn tuyệt đối, không phải đường dẫn tương đối

### Định Dạng Đường Dẫn Sai

**Lỗi Phổ Biến**:

❌ `file:/Users/...` (chỉ một dấu gạch chéo)  
✅ `file:///Users/...` (ba dấu gạch chéo)

❌ `file:///C:\config` (dấu gạch chéo ngược trên Windows)  
✅ `file:///C:/config` (dấu gạch chéo xuôi)

❌ `file:///Users\eazybytes\...` (dấu gạch chéo hỗn hợp)  
✅ `file:///Users/eazybytes/...` (tất cả dấu gạch chéo xuôi)

### Microservices Không Thể Kết Nối

**Triệu Chứng**: Microservices không khởi động được hoặc không thể tải thuộc tính

**Giải Pháp**:
1. Đảm bảo Config Server khởi động thành công trước
2. Xác minh Config Server có thể truy cập tại `http://localhost:8071`
3. Kiểm tra logs microservice cho lỗi kết nối
4. Kiểm tra endpoints Config Server trực tiếp trong trình duyệt

### Lỗi Permission Denied

**Triệu Chứng**: Logs Config Server hiển thị "Access Denied" hoặc "Permission Denied"

**Giải Pháp**:
1. Kiểm tra quyền thư mục (cần quyền đọc)
2. Xác minh user process Config Server có quyền truy cập
3. Trên Windows, kiểm tra file không bị khóa bởi process khác

## Lợi Ích Đạt Được

Bằng cách chuyển sang phương pháp file system:

- ✅ **Bảo Mật Tốt Hơn**: Cấu hình được tách riêng khỏi code ứng dụng
- ✅ **Kiểm Soát Truy Cập**: Admin server có thể hạn chế truy cập thư mục
- ✅ **Linh Hoạt Triển Khai**: Cấu hình tách riêng khỏi artifacts triển khai
- ✅ **Quản Lý Phiên Bản**: Vẫn có thể sử dụng Git cho việc versioning cấu hình
- ✅ **Sẵn Sàng Production**: Đáp ứng yêu cầu bảo mật doanh nghiệp
- ✅ **Cập Nhật Dễ Dàng**: Cập nhật cấu hình mà không cần redeploy Config Server

## Bước Tiếp Theo

Xem xét các cải tiến sau:

1. **Git Backend**: Lưu trữ cấu hình trong repository Git thay vì file system
2. **Mã Hóa**: Mã hóa các thuộc tính nhạy cảm bằng mã hóa Spring Cloud Config
3. **Nhiều Vị Trí**: Cấu hình nhiều vị trí tìm kiếm cho tính dự phòng
4. **Refresh Scope**: Triển khai làm mới thuộc tính động mà không cần khởi động lại
5. **Giám Sát**: Thêm giám sát cho các thay đổi cấu hình

## Tóm Tắt

Bạn đã thành công:

- ✅ Sao chép các file cấu hình từ classpath sang file system
- ✅ Cập nhật Config Server để sử dụng vị trí file system
- ✅ Thay đổi `search-locations` từ `classpath:` sang `file:`
- ✅ Duy trì yêu cầu profile `native`
- ✅ Xác minh Config Server tải từ file system
- ✅ Kiểm tra tích hợp microservice
- ✅ Tăng cường bảo mật với phương pháp file system

**Điểm Chính**: Thay đổi duy nhất cần thiết là cập nhật thuộc tính `search-locations` trong Config Server. Tất cả microservices tiếp tục hoạt động mà không cần bất kỳ sửa đổi nào, đồng thời đạt được bảo mật cải thiện thông qua lưu trữ file system.




FILE: 73-config-server-github-integration.md


# Lưu Trữ Thuộc Tính Cấu Hình trong GitHub Repository

## Tổng Quan

Hướng dẫn này giải thích cách cấu hình Spring Cloud Config Server để lưu trữ và tải các thuộc tính cấu hình từ kho lưu trữ GitHub. Đây là phương pháp được khuyến nghị nhất do các ưu điểm về bảo mật, quản lý phiên bản và khả năng kiểm tra.

## Ưu Điểm của Phương Pháp GitHub

- **Bảo mật**: Bảo vệ kho lưu trữ GitHub của bạn để kiểm soát quyền truy cập
- **Quản lý phiên bản**: Theo dõi các thay đổi theo thời gian với lịch sử Git
- **Kiểm tra**: Xem lại các cấu hình lịch sử từ nhiều tháng hoặc năm trước
- **Tốt hơn các giải pháp thay thế**: Phương pháp file system và classpath không hỗ trợ quản lý phiên bản

## Thiết Lập GitHub Repository

### Cấu Trúc Repository

Tạo một kho lưu trữ GitHub (ví dụ: `eazybytes-config`) với cấu trúc sau:

```
eazybytes-config/
├── accounts.yml
├── cards.yml
├── loans.yml
├── eureka-server.yml
└── gateway-server.yml
```

### Repository Công Khai vs Riêng Tư

- **Phát triển/Học tập**: Repository công khai có thể chấp nhận được
- **Môi trường Production**: Luôn sử dụng repository riêng tư với xác thực

## Cấu Hình Config Server

### Bước 1: Cập Nhật Application Profile

Trong `application.yml` của Config Server, thay đổi profile hoạt động từ `native` sang `git`:

```yaml
spring:
  profiles:
    active: git
```

### Bước 2: Cấu Hình Thuộc Tính Git

Comment cấu hình native và thêm cấu hình Git:

```yaml
spring:
  cloud:
    config:
      server:
        # native:
        #   search-locations: "classpath:/config"
        git:
          uri: https://github.com/your-username/eazybytes-config.git
          default-label: main
          timeout: 5
          clone-on-start: true
          force-pull: true
```

## Giải Thích Các Thuộc Tính Cấu Hình

### uri
- **Mô tả**: URL kho lưu trữ GitHub
- **Định dạng**: HTTPS URL của repository của bạn
- **Ví dụ**: `https://github.com/your-username/eazybytes-config.git`

### default-label
- **Mô tả**: Tên nhánh mặc định để sử dụng
- **Giá trị**: `main` (hoặc `master` tùy thuộc vào repository của bạn)
- **Mục đích**: Chỉ định nhánh nào để đọc cấu hình

### timeout
- **Mô tả**: Thời gian chờ tối đa cho kết nối GitHub
- **Giá trị**: `5` (giây)
- **Mục đích**: Fail nhanh nếu không thể kết nối đến kho lưu trữ GitHub
- **Lợi ích**: Cảnh báo ngoại lệ ngay lập tức cho nhóm vận hành/phát triển

### clone-on-start
- **Mô tả**: Clone repository trong quá trình khởi động
- **Giá trị**: `true`
- **Mục đích**: Đảm bảo cấu hình có sẵn ngay lập tức
- **Quan trọng**: Không có thuộc tính này, việc clone xảy ra khi có request đầu tiên, có thể gây ra vấn đề khởi động

### force-pull
- **Mô tả**: Ghi đè các thay đổi cục bộ khi khởi động lại
- **Giá trị**: `true`
- **Mục đích**: Luôn đồng bộ với remote repository (vị trí chính)
- **Lợi ích**: Ngăn chặn các thay đổi cục bộ ảnh hưởng đến cấu hình

## Kiểm Tra Cấu Hình

### 1. Xác Minh Config Server

Khởi động Config Server và xác minh nó đang sử dụng Git profile bằng cách kiểm tra console logs.

### 2. Kiểm Tra Truy Xuất Cấu Hình

Truy cập endpoint của Config Server:

```
http://localhost:8071/accounts/prod
```

Bạn sẽ thấy:
- Các thuộc tính cấu hình từ kho lưu trữ GitHub
- Liên kết URL GitHub trong response

### 3. Kiểm Tra Tích Hợp Microservices

Khởi động các microservices theo thứ tự:
1. Config Server
2. Accounts Microservice
3. Loans Microservice
4. Cards Microservice

Kiểm tra endpoint contact-info của từng microservice để xác minh chúng đang đọc cấu hình từ Config Server.

## Xác Thực cho Repository Riêng Tư

### Xác Thực Username/Password

Thêm vào `application.yml`:

```yaml
spring:
  cloud:
    config:
      server:
        git:
          uri: https://github.com/your-username/private-repo.git
          username: your-username
          password: your-password
```

### Xác Thực SSH

Để tăng cường bảo mật, sử dụng SSH keys thay vì username/password. Cấu hình:
- Host key
- Host key algorithm
- Private key

Tham khảo tài liệu chính thức của Spring Cloud Config để biết chi tiết thiết lập SSH.

## Các Tùy Chọn Backend Thay Thế

Spring Cloud Config Server hỗ trợ nhiều tùy chọn backend khác nhau:

### Các Backend Được Hỗ Trợ
- **Git Backend**: GitHub, GitLab, Bitbucket
- **AWS CodeCommit**: Kho lưu trữ Git được quản lý bởi AWS
- **Google Cloud Source**: Kho lưu trữ Git của Google Cloud
- **File System Backend**: Hệ thống tệp cục bộ (không khuyến nghị cho production)
- **Vault Backend**: Tích hợp HashiCorp Vault
- **CredHub Server**: Cloud Foundry CredHub
- **AWS Secrets Manager**: Quản lý bí mật của AWS
- **AWS Parameter Store**: AWS Systems Manager Parameter Store
- **JDBC Backend**: Lưu trữ cấu hình dựa trên cơ sở dữ liệu

## Thực Hành Tốt Nhất

1. **Luôn sử dụng repository riêng tư trong môi trường production**
2. **Bật `clone-on-start` để phát hiện sớm vấn đề cấu hình**
3. **Đặt giá trị timeout phù hợp cho hành vi fail-fast**
4. **Sử dụng `force-pull` để ngăn chặn vấn đề thay đổi cục bộ**
5. **Ghi chép các thay đổi cấu hình trong Git commit messages**
6. **Sử dụng chiến lược nhánh cho các môi trường khác nhau**

## Khắc Phục Sự Cố

### Config Server không khởi động được
- Xác minh URL kho lưu trữ GitHub là chính xác
- Kiểm tra kết nối mạng đến GitHub
- Xác minh default-label khớp với tên nhánh của bạn

### Microservices không thể đọc cấu hình
- Đảm bảo Config Server được khởi động trước
- Xác minh microservices được cấu hình với URL Config Server chính xác
- Kiểm tra logs của Config Server để tìm lỗi kết nối

## Đọc Thêm

Để biết các cấu hình nâng cao và tính năng bổ sung, tham khảo:
- [Tài Liệu Chính Thức Spring Cloud Config](https://spring.io/projects/spring-cloud-config)
- Tài liệu tham khảo Spring Cloud Config Server
- Hướng dẫn xác thực và cấu hình SSH

## Kết Luận

Sử dụng GitHub làm backend cho Spring Cloud Config Server cung cấp một phương pháp mạnh mẽ, có khả năng mở rộng và dễ bảo trì để quản lý cấu hình microservices. Khả năng quản lý phiên bản và kiểm tra làm cho nó trở thành lựa chọn được khuyến nghị cho môi trường production.

## Những Điểm Chính Cần Nhớ

- GitHub backend là phương pháp được khuyến nghị nhất
- Cấu hình đúng đảm bảo hành vi fail-fast
- Xác thực rất quan trọng cho repository riêng tư
- Tài liệu chính thức là nguồn tài nguyên tốt nhất cho các tình huống nâng cao
- Kiến thức và hiểu biết quan trọng hơn số năm kinh nghiệm




FILE: 74-refreshing-microservices-configuration-dynamically.md


# Làm mới cấu hình Microservices một cách động

Hiện tại, bên trong mạng lưới microservices của chúng ta, chúng ta có ba microservices khác nhau và có một config server, và chúng ta có thể đọc các thuộc tính từ config server trong quá trình khởi động các ứng dụng microservices.

Vậy là mọi thứ đang hoạt động hoàn hảo và bạn có thể nghĩ rằng đây là kết thúc của spring cloud config server và chúng ta có thể không gặp phải bất kỳ thách thức nào khác về mặt quản lý cấu hình.

Nhưng trong bài giảng này, tôi muốn giới thiệu một vấn đề mới mà chúng ta có thể gặp phải bên trong môi trường microservices về mặt quản lý cấu hình.

Hãy nghĩ như bạn đã thiết lập config server và tất cả các microservices của bạn đã khởi động bằng cách kết nối với config server, chúng đã tải các thuộc tính một cách hoàn hảo.

Đột nhiên bạn muốn thay đổi một thuộc tính cụ thể bên trong config server của bạn và bạn muốn điều tương tự được phản ánh ngay lập tức mà không cần khởi động lại các microservices của bạn.

Ở đây bạn có thể có một câu hỏi, vấn đề gì xảy ra nếu tôi khởi động lại microservices của mình. Bên trong microservice, đó không phải là một microservice mà có hàng trăm microservices và sẽ có nhiều instance cho mỗi microservice.

Vì vậy, việc khởi động lại các instances của microservices của bạn lại là một tác vụ thủ công mà ai đó phải đảm nhiệm.

Bất cứ khi nào bạn đưa một số tác vụ thủ công vào bên trong microservice, thì nó sẽ làm cho thiết lập microservices của bạn trở nên rất phức tạp.

Đó là lý do tại sao chúng ta nên tìm kiếm một tùy chọn để làm mới các thuộc tính mà không cần khởi động lại các instances microservices.

Ví dụ, hãy nghĩ như bạn có một feature flag mà bạn đã cấu hình bên trong config server. Vì vậy, dựa trên một feature flag như một cờ boolean, bạn muốn kiểm soát hành vi của logic nghiệp vụ microservice của bạn.

Khi cờ bị vô hiệu hóa, bạn muốn thực thi một đoạn mã khác.

Những cờ này bạn muốn thay đổi bất cứ lúc nào bên trong config server và bạn muốn điều tương tự được phản ánh ngay lập tức bên trong các microservices riêng lẻ của bạn mà không cần khởi động lại.

Vì vậy, đây là kịch bản phổ biến nhất mà các dự án sẽ cố gắng đạt được bên trong mạng lưới microservices của họ.

Đó là lý do tại sao trong bài giảng này, hãy cùng tập trung vào cách làm mới các cấu hình hoặc thuộc tính bên trong microservices mà không cần khởi động lại các instances.

## Bước 1: Thêm Spring Boot Actuator Dependency

Đầu tiên, chúng ta cần đảm bảo tất cả các microservices riêng lẻ của chúng ta đều có dependency spring boot actuator được định nghĩa bên trong pom.xml.

Vì vậy, nếu bạn có thể vào pom.xml của cards microservice và tìm kiếm actuator, bạn có thể thấy có spring boot starter actuator đã được thêm vào, điều tương tự chúng ta đã thêm từ lâu bên trong loans và accounts microservice.

Vì vậy, chúng ta đã có dependency actuator bên trong các instances microservices của chúng ta.

## Bước 2: Chuyển đổi Record Classes thành Normal Classes

Bước tiếp theo, chúng ta cần đi đến các lớp Dto nơi chúng ta đang cố gắng giữ tất cả các chi tiết thuộc tính của chúng ta.

Vì vậy, ở đây chúng ta có bên trong accounts microservice, có một record class với tên AccountsContactInfo chứa tất cả các thuộc tính mà microservice của tôi sẽ đọc trong quá trình khởi động từ config server.

Với thiết lập này, chúng ta có một vấn đề bất cứ khi nào chúng ta sử dụng một record class, điều đó có nghĩa là một khi đối tượng của AccountContactInfoDto này được tạo trong quá trình khởi động, chúng ta không thể thay đổi các giá trị thuộc tính tại runtime bằng cách gọi phương thức setter.

Bất cứ khi nào bạn sử dụng record class, tất cả các trường của bạn sẽ là final. Một khi đối tượng được tạo với sự trợ giúp của constructor, thì không có cách nào để thay đổi các giá trị bên trong các trường.

Đó là lý do tại sao chúng ta cần chuyển đổi AccountsContactInfo này thành một class bình thường thay vì record class.

Vì vậy, hãy để tôi loại bỏ record và đề cập đến class. Sau đó, chúng ta cần loại bỏ các cú pháp này như chúng ta không cần đề cập đến các trường bên trong các dấu ngoặc này.

Vì vậy, tôi đang loại bỏ điều đó, bây giờ bên trong class của tôi, tôi sẽ định nghĩa tất cả các trường.

Trường đầu tiên là `private String message`. Một khi tôi đã định nghĩa điều này, tôi sẽ đề cập đến dấu chấm phẩy, sau đó tôi sẽ đề cập `private Map contactDetails`, tôi sẽ đề cập đến dấu chấm phẩy ở cuối và tương tự tôi sẽ đề cập private trước trường List, đó là `onCallSupport`.

Vì vậy, bây giờ chúng ta có ba trường khác nhau bên trong class của chúng ta. Bước tiếp theo, chúng ta cần đề cập annotation `@Getter` và annotation `@Setter`.

Vì vậy, đây là các annotations từ Lombok sử dụng các annotations này. Chỉ framework spring boot của tôi mới có thể lấy các trường và đặt các trường tại runtime.

### Áp dụng cho LoansContactInfoDto

Hãy để tôi thực hiện các thay đổi tương tự bên trong LoansContactInfoDto.

Vì vậy, hãy để tôi tìm kiếm LoansContactInfoDto. Ở đây tôi sẽ loại bỏ record này và thay đổi thành class. Sau đó, tôi sẽ loại bỏ tất cả các trường này và loại bỏ các dấu ngoặc này.

Sau đó, tôi sẽ lấy các trường này từ AccountsInfoDto vì chúng ta sẽ duy trì cùng một bộ trường ở đây, điều này cũng sẽ hoạt động đúng mà không có bất kỳ vấn đề nào khi trao đổi như bạn biết, tôi cần đề cập annotation `@Getter` tiếp theo là annotation `@Setter`.

### Áp dụng cho CardsContactInfoDto

Vì vậy, hãy để tôi làm điều tương tự cho CardsContactInfoDto.

Vì vậy, trước tiên tôi sẽ đề cập đến các annotations Lombok, sau đó tôi sẽ thay đổi record này thành class, tiếp theo tôi sẽ loại bỏ tất cả các trường này cùng với các dấu ngoặc và tôi sẽ lấy tên trường từ các class khác mà chúng ta có.

Và tôi sẽ đề cập điều tương tự trong CardsContactInfoDto.

Vì vậy, chúng ta đã thực hiện những thay đổi liên quan đến Dto này trong tất cả các microservices. Vì vậy, điều này sẽ cho phép các microservices của chúng ta thay đổi các giá trị thuộc tính tại runtime.

## Bước 3: Cấu hình Actuator Endpoints

Sau khi thực hiện những thay đổi này, tôi cần vào application.yml của Accounts Microservice.

Bên trong application.yml này, chúng ta cần bật các đường dẫn API actuator. Theo mặc định, actuator sẽ không expose tất cả các đường dẫn API liên quan đến quản lý.

Đó là lý do tại sao chúng ta cần bật chúng một cách cụ thể bằng cách giới thiệu một thuộc tính ở đây.

Vì vậy, thuộc tính mà tôi muốn đề cập ở đây là `management` vì chúng ta muốn bật các API liên quan đến quản lý.

Vì vậy, chúng ta cần đề cập `management` này ở vị trí gốc. Và tại management này, tôi cần đề cập `endpoints`, trong endpoints này chúng ta cần đề cập `web`, sau web này chúng ta cần đề cập `exposure`.

Sau exposure, chúng ta cần đề cập `include`. Một khi chúng ta định nghĩa phần tử include này bên trong thuộc tính của bạn, chúng ta cần bật actuator endpoint sẽ cho phép làm mới các thuộc tính tại runtime.

Ở đây thay vì chỉ đề cập refresh API, thay vào đó chúng ta có thể đề cập giá trị asterisk (*). Với giá trị asterisk này, tôi đang nói với spring boot actuator của mình để bật và expose tất cả các management endpoint được hỗ trợ bởi spring boot actuator.

Và bên trong các endpoints này, chúng ta cũng sẽ có endpoint liên quan đến refresh.

```yaml
management:
  endpoints:
    web:
      exposure:
        include: "*"
```

### Áp dụng cho Cards và Loans Microservices

Bây giờ chúng ta cần thực hiện bộ thay đổi tương tự bên trong loans và cards microservice.

Vì vậy, hãy để tôi vào application.yml của cards microservice. Trong cards microservice này, chúng ta cần mở application.yml. Bên trong application.yml, tôi sẽ giới thiệu cùng một thuộc tính.

Hãy để tôi làm điều tương tự cho loans microservice. Bên trong application.yml, tôi sẽ đề cập cùng một thuộc tính.

## Demo: Thay đổi thuộc tính tại Runtime

Với điều này, chúng ta đã thực hiện tất cả các thay đổi liên quan bên trong microservices của chúng ta. Bước tiếp theo, hãy cùng thử khởi động tất cả các microservices của chúng ta, sau đó chúng ta có thể thử thay đổi một thuộc tính runtime bên trong GitHub repo và xem liệu theo mặc định nó có phản ánh bên trong các microservices riêng lẻ của chúng ta không.

Vì vậy, đầu tiên hãy để tôi thực hiện build. Một khi build hoàn thành, tôi sẽ dừng tất cả các ứng dụng của mình. Sau khi tất cả các ứng dụng của tôi dừng lại, đầu tiên tôi sẽ khởi động ứng dụng config server của mình.

Một khi config server của tôi khởi động thành công, tôi sẽ khởi động AccountsApplication, tiếp theo là CardsApplication. Sau CardsApplication, tôi cũng sẽ khởi động LoansApplication.

Bây giờ tất cả các instances microservices và config servers của tôi đã khởi động thành công.

### Thay đổi Properties trong GitHub Repo

Bước tiếp theo, tôi sẽ thử thay đổi các giá trị thuộc tính bên trong GitHub repo.

Hiện tại bạn có thể thấy đối với accounts-prod.yml, chúng ta có message nói rằng: "hello, welcome to EazyBank accounts related prod APIs". Ở đây trong message này, tôi sẽ thay thế "prod" này bằng "production", nhưng trước khi tôi thử thay thế, trước tiên hãy để tôi chỉ cho bạn ngay bây giờ accounts microservice hoặc microservice khác của chúng ta sẽ có message với giá trị prod.

Vì vậy, ở đây tôi đang thử gọi API contact-info cho accounts microservice. Bạn có thể thấy có prod APIs ở đây.

Tương tự, nếu tôi vào cards và gọi contact-info này, ở đây chúng ta cũng đang nhận được prod APIs và điều tương tự tôi có thể xác nhận cho loans.

Vì vậy, đối với loans, tôi cũng chỉ đang thử gọi contact-info này sẽ có prod APIs này bên trong message.

Bây giờ hãy để tôi vào GitHub repo, ở đây tôi sẽ nhấp vào nút edit này và thay thế prod này bằng production.

Vì vậy, tôi sẽ làm điều tương tự cho các microservices khác. Trước đó, hãy để tôi commit file này trực tiếp vào GitHub repo.

Một khi tôi hoàn thành với file accounts này, tôi sẽ mở file liên quan đến cards. Vì vậy, cards-prod là file mà chúng ta cần thay đổi ở đây.

Vì vậy, hãy để tôi nhấp vào nút edit này và thay thế prod này bằng production. Commit các thay đổi vào GitHub repo, sau đó tôi sẽ mở loans-prod.yml.

Và ở đây tôi cũng sẽ nhấp vào nút edit này, thay thế prod này bằng production và commit các thay đổi vào GitHub repo.

### Kiểm tra Config Server

Bây giờ trước tiên tôi sẽ cho thấy hành vi của config server. Ở đây tôi đang thử gọi API account/prod có sẵn bên trong config server.

Bạn có thể thấy config server của tôi có giá trị thuộc tính mới nhất là production. Điều này xác nhận bất cứ khi nào một microservice instance đang cố gắng gọi đường dẫn API này trong quá trình khởi động, config server của tôi sẽ không dựa vào cache cục bộ.

Nó luôn luôn sẽ kiểm tra với bản sao chính có sẵn bên trong GitHub repo và nó sẽ trả về cùng các giá trị mới nhất cho accounts microservice.

Điều tương tự tôi có thể xác nhận cho loans. Đối với loans, chúng ta cũng có production này, tương tự cho cards chúng ta có thể xác nhận. Vì vậy, đối với cards, nó cũng hoạt động tốt.

Điều này có nghĩa là không có vấn đề gì trong việc làm mới các thuộc tính trên config server.

### Vấn đề với Microservices

Bây giờ vấn đề duy nhất là các microservices của chúng ta phải có khả năng đọc các giá trị mới nhất này và chúng ta đã biết rằng microservices sẽ chỉ kết nối với config server trong quá trình khởi động của ứng dụng.

Bây giờ, để phản ánh các thuộc tính mới nhất này, chúng ta cần khởi động lại các instances microservices và chúng ta đang cố gắng tránh quy trình đó vì chúng ta cần tránh khởi động lại các ứng dụng microservices của chúng ta vì nó sẽ ảnh hưởng đến lưu lượng truy cập và vì nó liên quan đến quy trình thủ công.

### Giải pháp: Actuator Refresh API

Vậy làm thế nào để vượt qua thách thức này?

Như tôi đã nói, actuator sẽ expose một API với tên refresh. Nếu bạn vào accounts actuator như `localhost:8080/actuator` đối với actuator này, bạn sẽ có rất nhiều API được expose.

Và ở đây chỉ cần tìm kiếm refresh. Vì vậy, đây là đường dẫn. Nếu tôi thử gọi điều này, nó nói rằng method not allowed vì từ trình duyệt, luôn luôn phương thức http get sẽ được gọi.

Nhưng refresh API này chỉ hỗ trợ phương thức post. Đó là lý do tại sao chúng ta cần vào postman để gọi refresh API này.

Trước đó, hãy để tôi gọi tất cả contact info một lần nữa bên trong microservices của tôi để đảm bảo các thuộc tính chưa được phản ánh hiện tại bên trong microservices.

Vì vậy, đối với loans, bạn có thể thấy cùng một prod cũ vẫn ở đó. Tương tự đối với accounts, cùng một cái cũ vẫn ở đó. Và bây giờ đối với cards, tôi đang thử gọi cho điều này, cũng có cùng một giá trị prod cũ ở đây.

### Gọi Refresh Endpoint

Bước tiếp theo, chúng ta cần gọi URL actuator refresh. Đối với điều tương tự bên trong thư mục accounts, bạn có thể thấy có một request với tên refresh config.

Vì vậy, hãy để tôi nhấp vào điều này. Bạn có thể thấy đây là URL mà chúng ta cần gọi vì chúng ta đang cố gắng làm mới config của accounts microservice, chúng ta cần sử dụng URL endpoint của accounts microservice instance như `localhost:8080/actuator/refresh`.

Theo mặc định, URL này không bao giờ được expose bên trong microservices của bạn. Vì chúng ta đã đề cập đến cấu hình này bên trong tất cả các microservices, tất cả các management endpoints đang được expose.

Nếu bạn chỉ muốn expose refresh, bạn cần đề cập refresh ở đây, nhưng tôi muốn sử dụng Asterisk vì trong các phần sắp tới, chúng ta cần bật nhiều management endpoints khác.

Tôi hy vọng bạn hiểu rõ. Bây giờ tôi đang thử gọi API này. Không cần gửi bất kỳ dữ liệu request nào bên trong body. Nó có thể để trống, nhưng vui lòng đảm bảo phương thức Http là post.

Tôi đang thử nhấp vào nút send. Bạn sẽ nhận được phản hồi từ refresh API của bạn nói rằng thuộc tính accounts.message đã được thay đổi và điều tương tự hiện tại đang được làm mới đằng sau hậu trường.

Ngoài accounts.message, chúng ta cũng nhận được thêm một thuộc tính nữa là config.client.version. Vì vậy, bạn sẽ luôn nhận được thuộc tính này bất cứ khi nào bạn thay đổi điều gì đó trên GitHub repo vì bất cứ khi nào có thay đổi xảy ra, config server của bạn sẽ thay đổi số version đằng sau hậu trường và điều tương tự nó đang cố gắng gửi đến các ứng dụng config client như accounts microservice.

Chúng ta chỉ cần lo lắng về message này vì đây là message sẽ ảnh hưởng đến logic nghiệp vụ của chúng ta.

### Xác nhận Thay đổi

Vì vậy, bây giờ chúng ta đã làm mới nó. Tôi sẽ vào contact-info của accounts microservice. Vì vậy, đây là contact info của accounts microservice. Tôi đã không khởi động lại accounts microservice của mình.

Bạn đã sẵn sàng để xem điều kỳ diệu chưa? Hiện tại bạn có thể thấy giá trị ở đây là prod. Ngay khi tôi nhấp vào nút send, nó được thay đổi thành production API.

Điều đó có nghĩa là chúng ta có thể thay đổi giá trị thuộc tính runtime mà không cần khởi động lại accounts microservice của chúng ta.

### Áp dụng cho Loans và Cards

Bây giờ hoạt động tương tự tôi phải làm cho loans và cards.

Bây giờ nếu bạn vào và kiểm tra loans microservice, bạn có thể thấy nó vẫn đang tham chiếu đến prod vì chúng ta chưa gọi refresh API có sẵn đối với loans microservice.

Vì vậy, đối với điều tương tự, hãy vào thư mục loans và nhấp vào refresh config này, sau đó bạn có thể nhấp vào nút send. Bạn sẽ nhận được message nói rằng loans.message đã được thay đổi đằng sau hậu trường.

Bây giờ nếu bạn vào contact-info và thử gọi lần này, bạn sẽ nhận được production APIs.

Hãy để tôi làm điều tương tự cho cards. Đối với điều tương tự, trước tiên, tôi cần gọi refresh config này có mặt trong cards.

Một khi tôi nhận được phản hồi này, tôi có thể vào contact-info của cards và ở đây tôi đang thử nhấp vào nút send này. Bạn có thể thấy tôi đang nhận được production làm output.

## Tóm tắt các bước

Tôi hy vọng bạn đã hiểu rõ cách chúng ta có thể làm mới các giá trị thuộc tính runtime của chúng ta với sự trợ giúp của actuator refresh endpoint.

Hãy cùng thử xem lại các bước mà chúng ta đã làm theo một cách rất nhanh chóng ở đây. Tôi đã đề cập đến tất cả các bước mà chúng ta đã làm theo bên trong slide này để nó sẽ đóng vai trò là tài liệu tham khảo cho bạn.

### Các bước cần tuân theo:

1. **Thêm Spring Boot Actuator Dependency** vào pom.xml
2. **Cấu hình Actuator** để expose refresh endpoint bằng cách thêm thuộc tính:
   ```yaml
   management.endpoints.web.exposure.include=refresh
   ```
   Hoặc bạn cũng có thể đề cập giá trị asterisk (*)
3. **Gọi Actuator Refresh Endpoint** bất cứ khi nào bạn muốn làm mới các thuộc tính của bạn bên trong accounts microservices hoặc bất kỳ microservices nào khác mà không cần khởi động lại, bạn chỉ cần gọi đường dẫn actuator, đó là `actuator/refresh` đối với microservices instance của bạn

### Quy trình làm mới cấu hình:

Vì vậy, hãy cùng thử hình dung điều này. Bạn có thể thấy ở đây trong bước đầu tiên, chúng ta sẽ push dữ liệu cấu hình mới vào config repo, sau đó chúng ta sẽ gọi `actuator/refresh` bằng phương thức Http post.

Vì vậy, tôi đang cố gắng đưa ra demo bằng cách sử dụng account microservice ở đây. Vì vậy, bây giờ account microservice của tôi đằng sau hậu trường sẽ yêu cầu configuration server cung cấp các giá trị thuộc tính đã được thay đổi so với phiên bản trước.

Vì vậy, config server của tôi sẽ đi và cố gắng pull tất cả các thay đổi mới nhất từ GitHub repo trong bước bốn và điều tương tự nó sẽ cố gắng gửi lại cho accounts microservice bằng cách tuân theo bước năm và bước sáu.

Và cuối cùng, vì account microservice của tôi sẽ nhận được các chi tiết thuộc tính đã được thay đổi, nó sẽ đọc chúng từ config server bên trong bước bảy bằng cách reload tất cả các cấu hình mới vào microservices mà không cần khởi động lại ứng dụng.

## Hạn chế của phương pháp này

Vì vậy, điều này là siêu, siêu hoàn hảo. Nhưng có một nhược điểm nghiêm trọng mà chúng ta có bên trong phương pháp này.

Nhược điểm là hãy nghĩ như bạn có 100 microservices và mỗi trong số chúng có năm instances khác nhau, điều đó có nghĩa là sẽ có tổng cộng 500 instances microservices đang chạy bên trong production của bạn.

Và vì lý do nào đó, bạn đang cố gắng thay đổi thuộc tính trong tất cả các microservices. Sau đó, bạn cần gọi refresh endpoint đối với tất cả 500 instances đang chạy bên trong production của bạn.

Và việc thực hiện điều này thủ công sẽ là một quy trình cực kỳ, cực kỳ cồng kềnh.

Một số operations team hoặc một số platform team sẽ cố gắng tự động hóa quy trình này bằng cách viết một số scripts bên trong CI/CD pipelines hoặc họ sẽ cố gắng viết Jenkins jobs hoặc CI/CD jobs, sẽ gọi tất cả các microservices instances refresh endpoints.

Nhưng vẫn vậy, nó có thể không phải là một giải pháp thuận tiện cho nhiều dự án.

## Kết luận

Đó là lý do tại sao hãy cùng khám phá điều này thêm nữa và cố gắng xác định liệu có bất kỳ tùy chọn tốt hơn nào mà chúng ta có để làm mới các thuộc tính một cách động mà không cần gọi refresh endpoint này cho từng instance microservice hay không.

Tôi hy vọng bạn đã hiểu rõ. Cảm ơn bạn và tôi sẽ gặp bạn trong bài giảng tiếp theo. Tạm biệt.




FILE: 75-refreshing-microservices-configuration-without-restart.md


# Làm Mới Cấu Hình Microservices Không Cần Khởi Động Lại

## Tổng Quan

Hướng dẫn này trình bày cách làm mới các thuộc tính cấu hình động trong microservices Spring Boot mà không cần khởi động lại các instance, sử dụng Spring Boot Actuator và Spring Cloud Config Server.

## Vấn Đề

Trong kiến trúc microservices với Spring Cloud Config Server, các thuộc tính được tải trong quá trình khởi động ứng dụng. Tuy nhiên, khi bạn cần thay đổi cấu hình tại runtime:

- **Thách Thức Khởi Động Lại Thủ Công**: Với hàng trăm microservices và nhiều instance cho mỗi service (ví dụ: 100 microservices × 5 instances = 500 instances), việc khởi động lại tất cả các instance thủ công rất khó khăn
- **Ảnh Hưởng Downtime**: Việc khởi động lại ảnh hưởng đến traffic production
- **Use Case Phổ Biến**: Feature flags cần được bật/tắt động để kiểm soát hành vi business logic

## Giải Pháp: Spring Boot Actuator Refresh Endpoint

### Điều Kiện Tiên Quyết

1. **Spring Boot Actuator Dependency** - Đã được thêm vào microservices:
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

### Bước 1: Sửa Đổi Các Lớp DTO

**Vấn Đề với Record Classes**: Các record class trong Java có các trường final không thể sửa đổi sau khi đối tượng được tạo.

**Giải Pháp**: Chuyển đổi record classes thành các class thông thường với getters/setters.

#### Trước (Record Class):
```java
public record AccountsContactInfoDto(
    String message,
    Map<String, String> contactDetails,
    List<String> onCallSupport
) {}
```

#### Sau (Regular Class):
```java
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class AccountsContactInfoDto {
    private String message;
    private Map<String, String> contactDetails;
    private List<String> onCallSupport;
}
```

Áp dụng các thay đổi tương tự cho:
- `LoansContactInfoDto`
- `CardsContactInfoDto`

### Bước 2: Kích Hoạt Actuator Endpoints

Thêm cấu hình vào `application.yml` trong tất cả microservices (accounts, loans, cards):

```yaml
management:
  endpoints:
    web:
      exposure:
        include: "*"
```

**Lưu ý**: Sử dụng `"*"` để expose tất cả management endpoints. Đối với production, nên chỉ expose `refresh`:
```yaml
management:
  endpoints:
    web:
      exposure:
        include: refresh
```

### Bước 3: Kiểm Tra Configuration Refresh

#### 1. Khởi Động Tất Cả Các Ứng Dụng
- Khởi động Config Server
- Khởi động Accounts Microservice
- Khởi động Cards Microservice
- Khởi động Loans Microservice

#### 2. Xác Minh Cấu Hình Ban Đầu
Kiểm tra contact-info endpoint cho mỗi microservice:
- `GET http://localhost:8080/contact-info` (Accounts)
- `GET http://localhost:8090/contact-info` (Cards)
- `GET http://localhost:8100/contact-info` (Loans)

Thông báo ban đầu: `"Hello, welcome to EazyBank accounts related prod APIs"`

#### 3. Cập Nhật Cấu Hình trong GitHub Repository

Sửa đổi các file thuộc tính trong config repository:
- `accounts-prod.yml`
- `cards-prod.yml`
- `loans-prod.yml`

Thay đổi: `prod APIs` → `production APIs`

#### 4. Xác Minh Config Server Có Giá Trị Mới Nhất
```
GET http://localhost:8888/accounts/prod
GET http://localhost:8888/cards/prod
GET http://localhost:8888/loans/prod
```

Config Server luôn lấy từ GitHub (không có cache cục bộ), nên nó hiển thị giá trị đã cập nhật ngay lập tức.

#### 5. Microservices Vẫn Hiển Thị Giá Trị Cũ
Nếu không refresh, microservices vẫn giữ giá trị cấu hình từ lúc khởi động.

#### 6. Gọi Actuator Refresh Endpoint

**Quan Trọng**: Sử dụng phương thức HTTP POST (không phải GET)

```
POST http://localhost:8080/actuator/refresh
```

**Response**:
```json
[
    "accounts.message",
    "config.client.version"
]
```

Response cho biết các thuộc tính nào đã được làm mới.

#### 7. Xác Minh Cấu Hình Đã Cập Nhật
```
GET http://localhost:8080/contact-info
```

Thông báo bây giờ hiển thị: `"Hello, welcome to EazyBank accounts related production APIs"`

**Thành Công!** Cấu hình đã được cập nhật mà không cần khởi động lại.

#### 8. Lặp Lại Cho Các Microservices Khác
```
POST http://localhost:8090/actuator/refresh  (Cards)
POST http://localhost:8100/actuator/refresh  (Loans)
```

## Quy Trình Configuration Refresh

```
┌─────────────────────────────────────────────────────────────┐
│ Bước 1: Push cấu hình mới vào Config Repository (GitHub)   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Bước 2: Gọi POST /actuator/refresh trên microservice       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Bước 3: Microservice yêu cầu các thuộc tính đã cập nhật    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Bước 4: Config Server pull phiên bản mới nhất từ GitHub    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Bước 5-6: Config Server trả về các thuộc tính đã thay đổi  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Bước 7: Microservice reload cấu hình (không restart!)      │
└─────────────────────────────────────────────────────────────┘
```

## Tóm Tắt Các Bước

1. ✅ Thêm Spring Boot Actuator dependency vào `pom.xml`
2. ✅ Kích hoạt refresh endpoint trong `application.yml`:
   ```yaml
   management.endpoints.web.exposure.include: refresh
   ```
3. ✅ Chuyển đổi các DTO record classes thành regular classes với `@Getter` và `@Setter`
4. ✅ Cập nhật cấu hình trong Config Repository
5. ✅ Gọi `POST /actuator/refresh` trên mỗi microservice instance

## Thách Thức Còn Lại

**Vấn Đề Khả Năng Mở Rộng**: Với 500+ microservice instances, việc gọi refresh endpoint thủ công trên mỗi instance là không thực tế.

### Các Giải Pháp Tạm Thời Hiện Tại
- **CI/CD Scripts**: Tự động hóa việc gọi refresh endpoint qua pipelines
- **Jenkins Jobs**: Lên lịch các jobs để gọi refresh trên tất cả instances

### Cần Giải Pháp Tốt Hơn
Các giải pháp tạm thời này có thể không thuận tiện cho tất cả các dự án. Cần một giải pháp tốt hơn để broadcast các thay đổi cấu hình đến tất cả các microservice instances cùng lúc.

**Chủ Đề Tiếp Theo**: Khám phá các giải pháp thay thế tốt hơn cho việc làm mới cấu hình động ở quy mô lớn (sẽ được đề cập trong các bài giảng tiếp theo).

## Những Điểm Chính

- ✅ Spring Boot Actuator cung cấp `/actuator/refresh` endpoint để cập nhật cấu hình runtime
- ✅ Không cần khởi động lại ứng dụng
- ✅ Config Server luôn lấy phiên bản mới nhất từ repository
- ✅ Microservices cần trigger refresh rõ ràng
- ⚠️ Gọi thủ công không mở rộng tốt cho các triển khai lớn
- 🔍 Cần các giải pháp broadcasting tốt hơn cho môi trường production

## Công Nghệ Sử Dụng

- Spring Boot
- Spring Cloud Config Server
- Spring Boot Actuator
- Lombok
- GitHub (Config Repository)

## Các Microservices Liên Quan

- **Accounts Microservice** (Port 8080)
- **Cards Microservice** (Port 8090)
- **Loans Microservice** (Port 8100)
- **Config Server** (Port 8888)




FILE: 76-spring-cloud-bus-configuration-refresh.md


# Làm mới cấu hình Microservices với Spring Cloud Bus

## Tổng quan

Hướng dẫn này giải thích cách sử dụng Spring Cloud Bus để làm mới cấu hình trên nhiều instance microservice mà không cần can thiệp thủ công trên từng instance. Phương pháp này loại bỏ nhu cầu phải gọi API refresh riêng lẻ cho từng instance microservice.

## Vấn đề

Khi sử dụng Spring Cloud Config Server, việc làm mới cấu hình lúc runtime yêu cầu phải gọi API refresh cho **từng instance microservice một cách riêng biệt**. Trong môi trường production với hàng trăm instance, điều này trở nên không khả thi và tốn thời gian.

## Giải pháp: Spring Cloud Bus

**Spring Cloud Bus** kết nối tất cả các node của hệ thống phân tán với một message broker nhẹ. Nó có thể phát sóng các thay đổi trạng thái (như thay đổi cấu hình) hoặc lệnh quản lý đến tất cả các instance được kết nối.

### Lợi ích chính

- **Chỉ gọi API một lần**: Gọi API bus-refresh chỉ một lần trên bất kỳ instance nào
- **Tự động lan truyền**: Thay đổi tự động lan truyền đến tất cả instance kết nối với message broker
- **Khả năng mở rộng**: Hoạt động với 500+ instance mà không tăng thêm chi phí
- **Hỗ trợ nhiều broker**: RabbitMQ, Kafka, v.v.

## Kiến trúc

Spring Cloud Bus sử dụng message broker (RabbitMQ hoặc Kafka) để kết nối tất cả các instance microservice. Khi bạn gọi endpoint bus-refresh trên một instance, message broker sẽ truyền thông tin thay đổi cấu hình đến tất cả các node đã đăng ký.

## Các bước triển khai

### Bước 1: Cài đặt RabbitMQ

Sử dụng Docker để nhanh chóng cài đặt RabbitMQ:

```bash
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
```

Lệnh này khởi động RabbitMQ với:
- **Core component** (port 5672): Xử lý chức năng message queue
- **Management UI** (port 15672): Cung cấp giao diện web để quản lý RabbitMQ

### Bước 2: Thêm Dependencies

Thêm dependency Spring Cloud Bus AMQP vào `pom.xml` của **tất cả microservices** và **Config Server**:

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-bus-amqp</artifactId>
</dependency>
```

Dependency này bao gồm:
- Spring Cloud Bus
- Tích hợp RabbitMQ (AMQP)

### Bước 3: Kích hoạt Actuator Endpoints

Đảm bảo dependency actuator có mặt trong tất cả microservices:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

Trong `application.yml` của mỗi microservice, expose endpoint bus-refresh:

```yaml
management:
  endpoints:
    web:
      exposure:
        include: "*"  # Expose tất cả actuator endpoints bao gồm bus-refresh
```

Bạn có thể chỉ định cụ thể chỉ expose `bus-refresh` nếu muốn:

```yaml
management:
  endpoints:
    web:
      exposure:
        include: "bus-refresh"
```

### Bước 4: Cấu hình kết nối RabbitMQ

Thêm thông tin kết nối RabbitMQ vào `application.yml` của **tất cả microservices** và **Config Server**:

```yaml
spring:
  rabbitmq:
    host: localhost
    port: 5672
    username: guest
    password: guest
```

**Lưu ý**: Đây là các giá trị mặc định. Nếu RabbitMQ đang chạy với cấu hình mặc định, Spring Boot sẽ tự động kết nối ngay cả khi không chỉ định rõ ràng các thuộc tính này. Tuy nhiên, đối với các thiết lập tùy chỉnh, hãy đảm bảo cung cấp giá trị chính xác.

### Bước 5: Build và khởi động lại Services

1. Dừng tất cả các instance microservice đang chạy
2. Thực hiện Maven clean build để tải xuống dependencies mới:
   ```bash
   mvn clean install
   ```
3. Khởi động Config Server trước
4. Khởi động tất cả microservices khác (Accounts, Loans, Cards, v.v.)

## Kiểm tra làm mới cấu hình

### Bước 1: Xác minh cấu hình ban đầu

Kiểm tra endpoint contact-info cho mỗi microservice để xác minh giá trị cấu hình hiện tại:

```http
GET http://localhost:8080/api/contact-info
```

Ví dụ response:
```json
{
  "message": "production APIs"
}
```

### Bước 2: Cập nhật cấu hình trong GitHub

Sửa đổi các file cấu hình trong GitHub repository (ví dụ: `accounts-prod.yml`, `loans-prod.yml`, `cards-prod.yml`):

```yaml
# Thay đổi từ
message: "production APIs"

# Thành
message: "prod APIs"
```

Commit và push thay đổi lên GitHub.

### Bước 3: Xác minh Config Server có giá trị mới nhất

Kiểm tra Config Server có thể đọc các giá trị đã cập nhật:

```http
GET http://localhost:8888/accounts/prod
```

Config Server nên trả về cấu hình đã cập nhật ngay lập tức mà không cần khởi động lại.

### Bước 4: Gọi Bus Refresh API

Gọi endpoint bus-refresh trên **bất kỳ một microservice nào** (ví dụ: Accounts):

```http
POST http://localhost:8080/actuator/bus-refresh
```

Response mong đợi: `204 No Content` (xử lý thành công không trả về nội dung)

### Bước 5: Xác minh tất cả Microservices đã làm mới

Kiểm tra endpoint contact-info trên **tất cả microservices** (Accounts, Loans, Cards):

```http
GET http://localhost:8080/api/contact-info  # Accounts
GET http://localhost:8090/api/contact-info  # Loans
GET http://localhost:9000/api/contact-info  # Cards
```

**Tất cả microservices nên trả về cấu hình đã cập nhật** mà không cần:
- Khởi động lại bất kỳ instance nào
- Gọi refresh/bus-refresh trên từng instance riêng lẻ

## Cách hoạt động: Luồng hoàn chỉnh

1. **Push thay đổi**: Developer push thay đổi cấu hình lên GitHub repository
2. **Gọi Bus Refresh**: Người vận hành gọi `actuator/bus-refresh` trên bất kỳ instance microservice nào
3. **Sự kiện thay đổi Config**: Microservice kích hoạt sự kiện thay đổi cấu hình đến message broker
4. **Phát sóng đến tất cả Nodes**: Message broker phát sóng sự kiện đến tất cả instance microservice đã đăng ký
5. **Tải lại cấu hình**: Mỗi microservice kết nối với Config Server và tải lại properties mà không khởi động lại

```
┌──────────────┐
│   GitHub     │
│  Repository  │
└──────┬───────┘
       │ 1. Push thay đổi
       ▼
┌──────────────────┐
│  Config Server   │◄────────────────┐
└──────┬───────────┘                 │
       │                             │
       │ 3. Kích hoạt sự kiện        │ 5. Tải lại Config
       ▼                             │
┌──────────────────┐                 │
│  RabbitMQ Broker │                 │
└──────┬───────────┘                 │
       │ 4. Phát sóng                │
       ├─────────────────────────────┤
       │                             │
   ┌───▼────┐  ┌────────┐  ┌────────▼┐
   │Accounts│  │ Loans  │  │  Cards  │
   │  (1)   │  │        │  │         │
   └────────┘  └────────┘  └─────────┘
   2. POST /actuator/bus-refresh
```

## Tóm tắt các thay đổi cần thiết

| Bước | Thành phần | Hành động |
|------|-----------|--------|
| 1 | Tất cả Microservices | Thêm dependency actuator |
| 2 | Tất cả Microservices | Kích hoạt endpoint bus-refresh trong `application.yml` |
| 3 | Tất cả Microservices + Config Server | Thêm dependency `spring-cloud-starter-bus-amqp` |
| 4 | Hệ thống Local | Cài đặt RabbitMQ (khuyến nghị dùng Docker) |
| 5 | Tất cả Microservices + Config Server | Cấu hình thông tin kết nối RabbitMQ |

## Ưu điểm

✅ **Chỉ gọi một lần**: Làm mới tất cả instance với một lần gọi API  
✅ **Không cần khởi động lại**: Cập nhật cấu hình mà không có downtime  
✅ **Khả năng mở rộng**: Hoạt động với hàng trăm hoặc hàng nghìn instance  
✅ **Kiểm soát tập trung**: Quản lý cấu hình từ một nơi

## Cân nhắc

### Trách nhiệm bổ sung

Sử dụng Spring Cloud Bus yêu cầu:
- **Cài đặt message broker**: RabbitMQ hoặc Kafka phải được cài đặt và bảo trì
- **Độ tin cậy mạng**: Kết nối message broker phải ổn định
- **Giám sát**: Đảm bảo tất cả instance được đăng ký đúng cách với broker

### Khi nào nên sử dụng phương pháp này

**Phù hợp cho:**
- Môi trường có nhiều instance microservice (10+)
- Thay đổi cấu hình không thường xuyên
- Tổ chức có cơ sở hạ tầng hỗ trợ message brokers

**Có thể không cần thiết cho:**
- Triển khai nhỏ (2-3 instance)
- Cấu hình tĩnh hiếm khi thay đổi
- Dự án không có cơ sở hạ tầng message broker

## Nhược điểm: Vẫn cần kích hoạt thủ công

Ngay cả với Spring Cloud Bus, ai đó vẫn phải gọi API bus-refresh ít nhất một lần. Properties sẽ không tự động làm mới nếu không có lệnh gọi này.

Điều này có thể là:
- **Thủ công**: Nhóm vận hành gọi API khi cần thiết
- **Tự động hóa**: Pipeline CI/CD kích hoạt bus-refresh sau deployment
- **Script**: Script tùy chỉnh giám sát thay đổi và kích hoạt refresh

Đối với các tổ chức thay đổi properties thường xuyên (hàng ngày hoặc nhiều hơn), việc kích hoạt thủ công này vẫn có thể gây phiền toái. Phương pháp tiếp theo sẽ liên quan đến làm mới cấu hình tự động bằng webhooks hoặc các cơ chế khác.

## Kết luận

Spring Cloud Bus cung cấp giải pháp mạnh mẽ để làm mới cấu hình trên nhiều instance microservice. Bằng cách chấp nhận trách nhiệm bổ sung duy trì message broker, bạn có được khả năng cập nhật cấu hình hiệu quả trên toàn bộ hệ sinh thái microservices của mình.

Phương pháp này đạt được sự cân bằng giữa tính đơn giản trong vận hành và khả năng mở rộng, làm cho nó lý tưởng cho hầu hết các môi trường production với yêu cầu thay đổi cấu hình vừa phải.




FILE: 77-lam-moi-cau-hinh-dong-voi-spring-cloud-bus.md


# Spring Cloud Bus để Làm Mới Cấu Hình Động

## Tổng Quan

Hướng dẫn này trình bày cách sử dụng Spring Cloud Bus để làm mới cấu hình trên nhiều instance microservice mà không cần khởi động lại chúng. Bằng cách triển khai Spring Cloud Bus với message broker như RabbitMQ, bạn có thể tránh việc phải gọi API refresh trên từng instance microservice riêng lẻ.

## Vấn Đề

Khi sử dụng Spring Cloud Config Server, chúng ta gặp phải thách thức:
- Phải gọi API refresh cho **từng instance microservice** một cách riêng biệt
- Nếu bạn có 500 instance trong môi trường production, bạn cần gọi endpoint refresh 500 lần
- Điều này trở nên không thể quản lý được khi hệ thống của bạn mở rộng quy mô

## Giải Pháp: Spring Cloud Bus

Spring Cloud Bus kết nối tất cả các node của hệ thống phân tán với một message broker nhẹ. Nó có thể phát sóng các thay đổi trạng thái (như thay đổi cấu hình) hoặc hướng dẫn quản lý đến tất cả các microservice được kết nối.

### Lợi Ích Chính

- **Chỉ Một Lần Gọi API**: Chỉ cần gọi bus refresh API một lần trên bất kỳ instance nào
- **Tự Động Lan Truyền**: Các thay đổi được tự động truyền đạt đến tất cả các instance khác
- **Khả Năng Mở Rộng**: Hoạt động hiệu quả cho dù bạn có 5 hay 500 instance

## Các Bước Triển Khai

### Bước 1: Thiết Lập RabbitMQ

RabbitMQ đóng vai trò là message broker kết nối tất cả các microservice.

**Sử Dụng Docker (Khuyến Nghị)**:
```bash
docker run -d --hostname rabbitmq --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
```

Lệnh này:
- Cài đặt component quản lý RabbitMQ (UI)
- Cài đặt component core RabbitMQ (chức năng message queue)
- Mở port 5672 cho message broker
- Mở port 15672 cho giao diện quản lý

### Bước 2: Thêm Dependencies

Thêm dependency Spring Cloud Bus AMQP vào tất cả microservice (accounts, cards, loans) **và** config server.

**pom.xml**:
```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-bus-amqp</artifactId>
</dependency>
```

Dependency này bao gồm cả:
- Spring Cloud Starter Bus
- Tích hợp RabbitMQ (AMQP)

### Bước 3: Kích Hoạt Actuator Endpoints

Đảm bảo endpoint bus refresh được expose trong tất cả microservice.

**application.yml**:
```yaml
management:
  endpoints:
    web:
      exposure:
        include: "*"
```

Sử dụng `"*"` để expose tất cả actuator endpoints bao gồm:
- `/actuator/refresh`
- `/actuator/bus-refresh`

### Bước 4: Cấu Hình Kết Nối RabbitMQ

Thêm thông tin kết nối RabbitMQ trong `application.yml` của tất cả microservice.

**application.yml**:
```yaml
spring:
  rabbitmq:
    host: localhost
    port: 5672
    username: guest
    password: guest
```

**Lưu ý**: Đây là các giá trị mặc định. Spring Boot sẽ tự động kết nối sử dụng các giá trị mặc định này ngay cả khi không được cấu hình rõ ràng. Tuy nhiên, khuyến nghị nên chỉ định chúng để rõ ràng và trong trường hợp sử dụng các giá trị khác trong môi trường của bạn.

### Bước 5: Build và Khởi Động Services

1. **Clean build** tất cả microservice để tải xuống các dependency mới:
   ```bash
   mvn clean install
   ```

2. **Khởi động services** theo thứ tự:
   - Config Server
   - Accounts Microservice
   - Loans Microservice
   - Cards Microservice

## Cách Hoạt Động

### Luồng Kiến Trúc

1. **Thiết Lập Ban Đầu**: Tất cả microservice và config server đăng ký làm client với RabbitMQ message broker

2. **Thay Đổi Cấu Hình**: Push các thay đổi cấu hình mới lên GitHub repository

3. **Kích Hoạt Refresh**: Gọi `/actuator/bus-refresh` trên **bất kỳ một** instance microservice

4. **Phát Sóng Sự Kiện**: Config server kích hoạt một config change event đến message broker

5. **Lan Truyền**: Message broker truyền đạt thay đổi đến tất cả các instance microservice đã đăng ký

6. **Tải Lại**: Tất cả instance kết nối với config server và tải lại properties mà không cần khởi động lại

### Ví Dụ Quy Trình

**Trước khi refresh**:
- Tất cả microservice hiển thị: `"This is production"`

**Thay đổi cấu hình**:
- Cập nhật GitHub: Đổi "production" thành "prod"
- Config server có thể đọc ngay các giá trị mới

**Gọi bus refresh**:
```http
POST http://localhost:8080/actuator/bus-refresh
```

**Kết quả**:
- Response: `204 No Content` (thành công)
- Tất cả microservice bây giờ hiển thị: `"This is prod"` mà không cần khởi động lại

## Kiểm Tra Triển Khai

1. **Xác minh giá trị ban đầu** bằng cách gọi endpoint `/contact-info` trên tất cả microservice

2. **Thay đổi giá trị property** trong GitHub repository (ví dụ: trong `accounts-prod.yml`, `cards-prod.yml`, `loans-prod.yml`)

3. **Gọi bus refresh** trên bất kỳ instance nào:
   ```http
   POST http://localhost:8080/actuator/bus-refresh
   ```

4. **Xác minh thay đổi** bằng cách gọi `/contact-info` trên tất cả microservice - tất cả phải phản ánh giá trị mới

## Tóm Tắt Các Yêu Cầu

| Bước | Hành Động | Áp Dụng Cho |
|------|-----------|-------------|
| 1 | Thêm dependency Actuator | Tất cả microservice |
| 2 | Kích hoạt endpoint bus refresh | Tất cả microservice |
| 3 | Thêm dependency Spring Cloud Bus AMQP | Tất cả microservice + Config Server |
| 4 | Thiết lập và khởi động RabbitMQ | Hệ thống local/Production |
| 5 | Cấu hình thông tin kết nối RabbitMQ | Tất cả microservice (tùy chọn nếu dùng mặc định) |

## Ưu Điểm

✅ **Khả Năng Mở Rộng**: Làm mới hàng trăm instance chỉ với một lần gọi API  
✅ **Hiệu Quả**: Không cần khởi động lại microservice  
✅ **Tự Động Hóa**: Các thay đổi lan truyền tự động qua message broker  
✅ **Linh Hoạt**: Hoạt động với RabbitMQ hoặc Apache Kafka

## Hạn Chế

⚠️ **Trách Nhiệm Bổ Sung**: Phải duy trì và giám sát hạ tầng message broker  
⚠️ **Kích Hoạt Thủ Công**: Vẫn phải có ai đó gọi endpoint bus refresh ít nhất một lần  
⚠️ **Phụ Thuộc**: Tất cả instance phải được kết nối với cùng một message broker  

## Khi Nào Nên Sử Dụng Phương Pháp Này

**Phù hợp khi**:
- Thay đổi cấu hình không thường xuyên (không hàng ngày)
- Bạn có nhiều instance microservice (100+)
- Việc refresh thủ công hoặc qua CI/CD là chấp nhận được

**Cân nhắc giải pháp khác nếu**:
- Thay đổi cấu hình xảy ra rất thường xuyên
- Bạn cần làm mới hoàn toàn tự động không cần can thiệp thủ công
- Bạn muốn tránh chi phí vận hành của việc quản lý message broker

## Bước Tiếp Theo

Để đạt được việc làm mới cấu hình hoàn toàn tự động mà không cần can thiệp thủ công, hãy xem xét:
- Sử dụng Spring Cloud Config Monitor với webhooks
- Triển khai GitHub webhooks để tự động kích hoạt bus refresh
- Khám phá các mẫu quản lý cấu hình thay thế

## Tài Nguyên Bổ Sung

- [Tài Liệu Spring Cloud Bus](https://spring.io/projects/spring-cloud-bus)
- [Tài Liệu RabbitMQ](https://www.rabbitmq.com/documentation.html)
- [Tài Liệu Spring Cloud Config](https://spring.io/projects/spring-cloud-config)




FILE: 78-automating-configuration-refresh-with-github-webhooks.md


# Tự Động Làm Mới Cấu Hình với GitHub Webhooks và Spring Cloud Config Monitor

## Tổng Quan

Hướng dẫn này trình bày cách tự động làm mới các thuộc tính cấu hình trong microservices mà không cần can thiệp thủ công, sử dụng GitHub webhooks kết hợp với Spring Cloud Bus và Spring Cloud Config Monitor.

## Vấn Đề Đặt Ra

Trước đây, chúng ta có thể làm mới thuộc tính tại runtime bằng cách gọi:
- API `/bus-refresh` trên bất kỳ instance nào
- API `/refresh` trên tất cả các microservice instances

Tuy nhiên, cả hai phương pháp đều yêu cầu **gọi thủ công**. Chúng ta cần một giải pháp tự động làm mới thuộc tính khi có thay đổi được push lên configuration repository.

## Kiến Trúc Giải Pháp

Phương pháp tự động được xây dựng dựa trên Spring Cloud Bus và bổ sung:
- **Spring Cloud Config Monitor** - Mở endpoint `/monitor`
- **GitHub Webhooks** - Tự động kích hoạt làm mới khi có thay đổi cấu hình

### Cách Hoạt Động

1. Một thay đổi được push lên GitHub configuration repository
2. GitHub webhook gửi POST request đến endpoint `/monitor` trên Config Server
3. Config Server tự động kích hoạt sự kiện refresh qua Spring Cloud Bus và RabbitMQ
4. Tất cả microservices nhận thông báo refresh và cập nhật cấu hình

## Các Bước Triển Khai

### Bước 1: Thêm Dependency Config Monitor

Thêm dependency Spring Cloud Config Monitor **chỉ vào Config Server** trong `pom.xml`:

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-config-monitor</artifactId>
</dependency>
```

Dependency này mở endpoint REST API `/monitor` (không phải actuator endpoint).

### Bước 2: Cấu Hình Config Server

Cập nhật `application.yaml` của Config Server:

```yaml
management:
  endpoints:
    web:
      exposure:
        include: "*"

spring:
  rabbitmq:
    host: localhost
    port: 5672
    username: guest
    password: guest
```

**Tại sao phải mở tất cả management endpoints?**
Config Server cần tự động gọi API `bus-refresh` ở hậu trường.

### Bước 3: Thiết Lập RabbitMQ

Đảm bảo RabbitMQ đang chạy với cấu hình mặc định:
- Host: localhost
- Port: 5672
- Username: guest
- Password: guest

### Bước 4: Cấu Hình GitHub Webhook

#### Truy Cập Cài Đặt Webhook
1. Điều hướng đến GitHub configuration repository của bạn
2. Vào **Settings** → **Webhooks**
3. Click **Add webhook**

#### Thách Thức Cấu Hình Webhook

**Vấn đề:** GitHub không thể truy cập `http://localhost:8071/monitor` vì:
- Đây là URL cục bộ không có IP công khai
- GitHub servers không thể phân giải localhost

**Giải pháp:** Sử dụng dịch vụ relay webhook như [hookdeck.com](https://hookdeck.com)

### Bước 5: Thiết Lập Hookdeck để Test Cục Bộ

#### Cài Đặt Hookdeck CLI

Cho macOS:
```bash
brew install hookdeck
```

#### Đăng Nhập vào Hookdeck
```bash
hookdeck login
```

#### Tạo Connection
```bash
hookdeck listen 8071
```

Khi được nhắc:
- **Path:** `/monitor`
- **Connection label:** `localhost`

Lệnh này tạo một webhook URL công khai chuyển hướng đến Config Server cục bộ của bạn.

#### Cấu Hình GitHub Webhook

1. Copy URL webhook Hookdeck đã tạo
2. Trong cài đặt webhook GitHub:
   - **Payload URL:** `https://<hookdeck-url>/monitor`
   - **Content type:** `application/json`
   - **Events:** Chọn "Just the push event"
3. Click **Add webhook**

## Kiểm Tra Thiết Lập

### Bước 1: Khởi Động Tất Cả Services

Khởi động services theo thứ tự:
1. RabbitMQ (qua Docker)
2. Config Server (port 8071)
3. Accounts microservice
4. Loans microservice
5. Cards microservice

### Bước 2: Xác Minh Cấu Hình Hiện Tại

Test Config Server endpoint:
```
GET http://localhost:8071/cards/prod
```

Test microservice endpoint:
```
GET http://localhost:9000/contact-info
```

Cả hai phải trả về giá trị thuộc tính hiện tại (ví dụ: `prod`).

### Bước 3: Thực Hiện Thay Đổi Cấu Hình

1. Chỉnh sửa file cấu hình trong GitHub (ví dụ: `cards-prod.yaml`)
2. Thay đổi giá trị thuộc tính (ví dụ: từ `prod` thành `webhook`)
3. Commit thay đổi

### Bước 4: Quan Sát Làm Mới Tự Động

**Điều gì xảy ra:**
1. GitHub kích hoạt webhook
2. Hookdeck chuyển tiếp request đến `localhost:8071/monitor`
3. Config Server logs hiển thị POST request với response 200
4. Config Server tự động kích hoạt `/bus-refresh`
5. Tất cả microservices nhận thông báo refresh

### Bước 5: Xác Minh Cấu Hình Đã Cập Nhật

Test lại microservice endpoint:
```
GET http://localhost:9000/contact-info
```

Response phải phản ánh giá trị thuộc tính mới (ví dụ: `webhook`) **mà không cần can thiệp thủ công**.

## Chi Tiết Webhook

### Thông Tin Webhook Payload

Khi xem webhook delivery trong GitHub Settings:
- **Delivery Status:** Success/Failure
- **Request Headers:** Content-Type, User-Agent, v.v.
- **Request Body:** Bao gồm chi tiết commit, files đã sửa đổi, commit message
- **Response:** Status code và response body

### Ví Dụ Dữ Liệu Webhook Event
```json
{
  "commits": [{
    "id": "commit-id",
    "message": "update cards-prod.yaml",
    "modified": ["cards-prod.yaml"]
  }]
}
```

## Sơ Đồ Kiến Trúc Hoàn Chỉnh

```
┌─────────────┐         ┌──────────────┐         ┌───────────────┐
│   GitHub    │ webhook │   Hookdeck   │ forward │ Config Server │
│ Repository  ├────────►│   (relay)    ├────────►│  /monitor     │
└─────────────┘         └──────────────┘         └───────┬───────┘
                                                          │
                                                          │ /bus-refresh
                                                          ▼
                                                  ┌───────────────┐
                                                  │   RabbitMQ    │
                                                  │   (AMQP Bus)  │
                                                  └───────┬───────┘
                                                          │
                        ┌─────────────────────────────────┼─────────────────┐
                        │                                 │                 │
                        ▼                                 ▼                 ▼
                ┌───────────────┐               ┌────────────┐     ┌──────────┐
                │   Accounts    │               │   Loans    │     │  Cards   │
                │ Microservice  │               │Microservice│     │Microservice
                └───────────────┘               └────────────┘     └──────────┘
```

## Tóm Tắt Các Bước Cấu Hình

1. **Thêm Actuator dependency** vào tất cả microservices và Config Server
2. **Bật endpoint bus-refresh** qua thuộc tính management
3. **Thêm Spring Cloud Bus AMQP dependency** vào tất cả ứng dụng
4. **Thêm Spring Cloud Config Monitor dependency** chỉ vào Config Server (mở `/monitor`)
5. **Khởi động RabbitMQ** sử dụng lệnh Docker
6. **Tạo GitHub webhook** gửi POST requests đến `/monitor` khi có push events

## Khác Biệt Chính So Với Phương Pháp Thủ Công

| Khía Cạnh | Phương Pháp Thủ Công | Phương Pháp Tự Động |
|-----------|---------------------|---------------------|
| Kích hoạt | Gọi API thủ công đến `/bus-refresh` hoặc `/refresh` | Tự động khi Git push |
| Can thiệp thủ công | Yêu cầu | Không yêu cầu |
| Thành phần bổ sung | Spring Cloud Bus + RabbitMQ | Spring Cloud Bus + RabbitMQ + Config Monitor + Webhook |
| Sẵn sàng production | Hạn chế | Cao |

## Xem Xét Production

### Trong Môi Trường Production

- Đội ngũ vận hành cấu hình **IP công khai hoặc domain name** thay vì localhost
- Không cần dịch vụ relay như Hookdeck
- Webhook trực tiếp từ GitHub đến endpoint công khai của Config Server

### Lợi Ích

- **Cập nhật cấu hình không downtime**
- **Lan truyền ngay lập tức** đến tất cả microservice instances
- **Không cần can thiệp thủ công**
- **Audit trail** qua GitHub commits và webhook delivery logs

## Các Bước Tiếp Theo

Sau khi thành thạo quản lý cấu hình:
1. **Dockerize microservices** - Chuyển ứng dụng thành Docker images
2. **Docker Compose deployment** - Điều phối tất cả services
3. **Production deployment** - Triển khai lên môi trường cloud

## Xử Lý Sự Cố

### Webhook Không Kích Hoạt
- Xác minh webhook delivery status trong GitHub Settings
- Kiểm tra console Hookdeck để xem relay logs
- Đảm bảo Config Server đang chạy trên port đúng

### Thuộc Tính Không Làm Mới
- Xác minh endpoint `/bus-refresh` đã được bật
- Kiểm tra kết nối RabbitMQ trong tất cả services
- Đảm bảo annotation `@RefreshScope` trên các configuration beans
- Xem lại logs của Config Server và microservices

### Vấn Đề Kết Nối RabbitMQ
- Xác minh RabbitMQ đang chạy: `docker ps`
- Kiểm tra thuộc tính connection trong tất cả services
- Đảm bảo firewall cho phép port 5672

## Kết Luận

Phương pháp tự động này loại bỏ các bước làm mới cấu hình thủ công, khiến kiến trúc microservices của bạn thực sự sẵn sàng cho production. Bằng cách kết hợp Spring Cloud Bus, Config Monitor và GitHub webhooks, bạn đạt được:

- **Tự động hóa** - Không cần gọi API thủ công
- **Độ tin cậy** - Cấu hình nhất quán trên tất cả instances
- **Khả năng kiểm toán** - Git commits đóng vai trò change logs
- **Khả năng mở rộng** - Hoạt động với số lượng microservice instances bất kỳ

Càng chịu trách nhiệm nhiều (chạy RabbitMQ, cấu hình webhooks), kiến trúc microservices của bạn càng mang lại nhiều quyền lực và tính linh hoạt.




FILE: 79-docker-compose-configuration-for-microservices.md


# Cấu Hình Docker Compose cho Microservices Spring Boot với Config Server

## Tổng Quan

Hướng dẫn này trình bày cách cấu hình Docker Compose cho nhiều microservices Spring Boot với Config Server tập trung, hỗ trợ nhiều môi trường (default, QA và production).

## Yêu Cầu Tiên Quyết

- Các microservices đang hoạt động: Accounts, Loans và Cards
- Config Server đã được triển khai
- Hiểu biết về Docker và Docker Compose
- Kiến thức về Spring Cloud Config

## Cấu Trúc Dự Án

Cấu hình Docker Compose được tổ chức theo môi trường:

```
v2-spring-cloud-config/
└── docker-compose/
    ├── default/
    │   └── docker-compose.yml
    ├── qa/
    │   └── docker-compose.yml
    └── prod/
        └── docker-compose.yml
```

## Cấu Hình Docker Compose

### Cấu Hình Các Services

File Docker Compose bao gồm bốn services:
1. **Config Server** - Quản lý cấu hình tập trung
2. **Accounts Microservice** - Dịch vụ tài khoản
3. **Loans Microservice** - Dịch vụ cho vay
4. **Cards Microservice** - Dịch vụ thẻ

### Config Server Service

```yaml
configserver:
  image: eazybytes/configserver:s6
  container_name: configserver-ms
  ports:
    - "8071:8071"
  deploy:
    resources:
      limits:
        memory: 700m
  networks:
    - eazybank
```

### Ví Dụ Cấu Hình Microservice (Accounts)

```yaml
accounts:
  image: eazybytes/accounts:s6
  container_name: accounts-ms
  ports:
    - "8080:8080"
  environment:
    SPRING_CONFIG_IMPORT: configserver:http://configserver:8071/
    SPRING_PROFILES_ACTIVE: default
    SPRING_APPLICATION_NAME: accounts
  deploy:
    resources:
      limits:
        memory: 700m
  networks:
    - eazybank
```

## Các Khái Niệm Cấu Hình Quan Trọng

### 1. Biến Môi Trường (Environment Variables)

Biến môi trường được sử dụng để ghi đè các thuộc tính ứng dụng trong môi trường Docker:

- **SPRING_CONFIG_IMPORT**: Chỉ định kết nối đến Config Server
  - Định dạng: `configserver:http://configserver:8071/`
  - Xóa tiền tố `optional:` trong môi trường production
  - Sử dụng tên service thay vì `localhost`

- **SPRING_PROFILES_ACTIVE**: Định nghĩa Spring profile đang active
  - Giá trị: `default`, `qa`, hoặc `prod`
  - Phải khớp với vị trí file Docker Compose

- **SPRING_APPLICATION_NAME**: Định danh ứng dụng
  - Phải khớp với tiền tố file cấu hình trong Config Server
  - Bắt buộc do bug trong Spring Cloud Config Server (workaround)

### 2. Tên Service vs Localhost

**Quan trọng**: Trong môi trường Docker, các microservices không thể sử dụng `localhost` để giao tiếp với nhau.

- ❌ **Sai**: `http://localhost:8071`
- ✅ **Đúng**: `http://configserver:8071`

Mỗi Docker container chạy trong mạng cô lập riêng. Khi sử dụng `localhost`, container cố gắng kết nối với chính nó, không phải với các container khác.

### 3. Cấu Hình Network

Tất cả services phải ở trên cùng một Docker network để giao tiếp:

```yaml
networks:
  - eazybank
```

Điều này cho phép các services tham chiếu lẫn nhau bằng tên service (ví dụ: `configserver`, `accounts`).

### 4. Giới Hạn Bộ Nhớ

Giới hạn tài nguyên ngăn containers tiêu thụ quá nhiều bộ nhớ:

```yaml
deploy:
  resources:
    limits:
      memory: 700m
```

## Quản Lý Phụ Thuộc Services

### Thách Thức

Docker Compose khởi động containers theo thứ tự nhưng không đợi services sẵn sàng hoàn toàn. Điều này tạo ra vấn đề:

1. Config Server container khởi động
2. Microservices khởi động ngay lập tức (không đợi)
3. Microservices thất bại vì Config Server chưa sẵn sàng nhận request

### Giải Pháp

Để đảm bảo thứ tự khởi động và sẵn sàng đúng, chúng ta cần:

1. Triển khai các probe **liveness** và **readiness** trong Config Server
2. Thêm cấu hình phụ thuộc trong Docker Compose cho microservices
3. Đợi Config Server khỏe mạnh trước khi khởi động các services phụ thuộc

Các khái niệm này (liveness và readiness) sẽ được đề cập trong bài học tiếp theo.

## Cấu Hình Theo Môi Trường

### Môi Trường Default

- Vị trí: `docker-compose/default/`
- Profile: `default`
- Sử dụng cho: Phát triển và test local

### Môi Trường QA

- Vị trí: `docker-compose/qa/`
- Profile: `qa`
- Sử dụng cho: Kiểm thử đảm bảo chất lượng

### Môi Trường Production

- Vị trí: `docker-compose/prod/`
- Profile: `prod`
- Sử dụng cho: Triển khai production

## Các Bước Migration

1. **Tạo cấu trúc thư mục**
   ```
   docker-compose/
   ├── default/
   ├── qa/
   └── prod/
   ```

2. **Copy file Docker Compose hiện có** vào thư mục `default/`

3. **Cập nhật image tags** từ `s4` sang `s6` (hoặc section hiện tại)

4. **Thêm Config Server service** vào Docker Compose

5. **Thêm biến môi trường** cho tất cả microservices

6. **Cấu hình phụ thuộc services** (bước tiếp theo)

## Best Practices (Thực Hành Tốt Nhất)

1. **Xóa tiền tố `optional:`** trong Config Server imports cho production
2. **Sử dụng tên services** thay vì `localhost` trong môi trường Docker
3. **Tách file Docker Compose** cho các môi trường khác nhau
4. **Đặt giới hạn bộ nhớ** cho tất cả containers
5. **Sử dụng cùng network** cho tất cả services liên quan
6. **Đánh version Docker images** với tags có ý nghĩa (ví dụ: `s6`)

## Các Vấn Đề Thường Gặp và Giải Pháp

### Vấn Đề 1: Microservice Không Thể Kết Nối Config Server

**Triệu chứng**: Lỗi connection refused hoặc timeout

**Giải pháp**: 
- Kiểm tra tên service đúng (`configserver` không phải `localhost`)
- Xác minh tất cả services trên cùng network
- Đảm bảo port mapping của Config Server đúng (8071:8071)

### Vấn Đề 2: Load Sai Configuration Profile

**Triệu chứng**: Ứng dụng sử dụng properties sai

**Giải pháp**:
- Xác minh biến môi trường `SPRING_PROFILES_ACTIVE`
- Kiểm tra vị trí file Docker Compose khớp với môi trường mong muốn
- Xác nhận Config Server có files đúng theo profile

### Vấn Đề 3: Config Server Chưa Sẵn Sàng

**Triệu chứng**: Microservices thất bại khi khởi động với lỗi connection

**Giải pháp**:
- Triển khai health checks và readiness probes
- Thêm phụ thuộc services trong Docker Compose
- Sử dụng `depends_on` với điều kiện health

## Các Bước Tiếp Theo

1. Hiểu các khái niệm **liveness** và **readiness**
2. Triển khai health checks trong Config Server
3. Thêm cấu hình phụ thuộc trong Docker Compose
4. Test trình tự khởi động với `docker-compose up`
5. Triển khai lên Kubernetes cluster

## Tóm Tắt

Cấu hình này cho phép:
- ✅ Hỗ trợ đa môi trường (default, QA, prod)
- ✅ Quản lý cấu hình tập trung
- ✅ Giao tiếp giữa các container
- ✅ Quản lý tài nguyên với giới hạn bộ nhớ
- ✅ Kiến trúc microservices có thể mở rộng

Bước tiếp theo là triển khai health checks và phụ thuộc services phù hợp để đảm bảo thứ tự khởi động đáng tin cậy.




FILE: 8-cau-hinh-h2-database-va-yaml-properties.md


# Cấu Hình H2 Database và YAML Properties trong Spring Boot

## Tổng Quan

Bài học này đề cập đến việc thiết lập cấu hình H2 database và sử dụng định dạng YAML cho các thuộc tính ứng dụng Spring Boot. Chúng ta sẽ học cách cấu hình database, kích hoạt H2 console và tạo database schema tự động trong quá trình khởi động ứng dụng.

## Yêu Cầu Tiên Quyết

- Đã hoàn thành tạo REST API từ bài học trước
- Dự án Spring Boot có dependency H2 database
- Hiểu biết cơ bản về khái niệm database

## Tại Sao Sử Dụng Định Dạng YAML?

### Properties Truyền Thống vs YAML

**Định dạng .properties truyền thống:**
```properties
server.port=8080
spring.datasource.url=jdbc:h2:mem:testdb
spring.datasource.driver-class-name=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=
```

**Định dạng YAML (.yml):**
```yaml
server:
  port: 8080

spring:
  datasource:
    url: jdbc:h2:mem:testdb
    driver-class-name: org.h2.Driver
    username: sa
    password: ''
```

### Ưu Điểm Của Định Dạng YAML

1. **Trực quan và dễ đọc** - Dễ hiểu cấu trúc
2. **Không lặp lại** - Các key không bị lặp lại không cần thiết
3. **Tiêu chuẩn công nghiệp** - Được sử dụng trong Docker, Kubernetes, AWS, GCP, Azure
4. **Hướng tới tương lai** - Spring Boot có khả năng chuyển sang định dạng YAML
5. **Tổ chức tốt hơn** - Cấu trúc phân cấp làm cho cấu hình rõ ràng hơn

## Cấu Hình Application Properties

### Bước 1: Đổi Tên File Properties

1. Điều hướng đến thư mục `src/main/resources`
2. Đổi tên `application.properties` thành `application.yml`
3. Cài đặt plugin YAML trong IDE của bạn để hỗ trợ cú pháp tốt hơn

### Bước 2: Cấu Hình Server Properties

```yaml
server:
  port: 8080
```

- Đặt port server ứng dụng là 8080 (port mặc định)
- Thực hành tốt là khai báo rõ ràng port
- Các microservices khác nhau sẽ cần số port khác nhau

### Bước 3: Cấu Hình H2 Database

```yaml
spring:
  datasource:
    url: jdbc:h2:mem:testdb
    driver-class-name: org.h2.Driver
    username: sa
    password: ''
```

**Chi Tiết Cấu Hình:**
- **url**: Chuỗi kết nối cho H2 in-memory database
- **driver-class-name**: H2 JDBC driver
- **username**: Username mặc định là "sa"
- **password**: Password trống (mặc định)

### Bước 4: Kích Hoạt H2 Console

```yaml
spring:
  h2:
    console:
      enabled: true
```

Điều này kích hoạt H2 web console có thể truy cập tại `http://localhost:8080/h2-console`

### Bước 5: Cấu Hình JPA Properties

```yaml
spring:
  jpa:
    database-platform: org.hibernate.dialect.H2Dialect
    hibernate:
      ddl-auto: update
    show-sql: true
```

**Giải Thích Cấu Hình JPA:**

- **database-platform**: Chỉ định H2 dialect cho Hibernate
- **ddl-auto: update**: Tự động tạo bảng trong quá trình khởi động nếu chúng chưa tồn tại
- **show-sql: true**: In tất cả các truy vấn SQL ra console để debug

## Quy Tắc Cú Pháp YAML

### Các Quy Tắc Quan Trọng Cần Tuân Theo:

1. **Indentation quan trọng** - Sử dụng khoảng cách nhất quán (thường là 2 spaces)
2. **Dấu hai chấm theo sau là khoảng trắng** - Luôn thêm khoảng trắng sau dấu hai chấm
3. **Cấu trúc phân cấp** - Sử dụng indentation để hiển thị mối quan hệ cha-con
4. **Không dùng tabs** - Sử dụng spaces cho indentation, không phải tabs

### Ví Dụ Cấu Trúc:

```yaml
parent:
  child1: value1
  child2:
    grandchild: value2
```

## Tạo Database Schema

### Bước 1: Tạo File schema.sql

Tạo một file có tên `schema.sql` trong thư mục `src/main/resources`.

### Bước 2: Định Nghĩa Cấu Trúc Bảng

**Bảng Customer:**
```sql
CREATE TABLE IF NOT EXISTS customer (
  customer_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL,
  mobile_number VARCHAR(20) NOT NULL,
  created_at DATE NOT NULL,
  created_by VARCHAR(20) NOT NULL,
  updated_at DATE DEFAULT NULL,
  updated_by VARCHAR(20) DEFAULT NULL
);
```

**Bảng Accounts:**
```sql
CREATE TABLE IF NOT EXISTS accounts (
  customer_id INT NOT NULL,
  account_number BIGINT AUTO_INCREMENT PRIMARY KEY,
  account_type VARCHAR(100) NOT NULL,
  branch_address VARCHAR(200) NOT NULL,
  created_at DATE NOT NULL,
  created_by VARCHAR(20) NOT NULL,
  updated_at DATE DEFAULT NULL,
  updated_by VARCHAR(20) DEFAULT NULL,
  FOREIGN KEY (customer_id) REFERENCES customer(customer_id) ON DELETE CASCADE
);
```

### Tiêu Chuẩn Các Cột Metadata

Mỗi bảng bao gồm bốn cột metadata này:
- **created_at**: Timestamp khi bản ghi được tạo
- **created_by**: Người dùng đã tạo bản ghi
- **updated_at**: Timestamp khi bản ghi được cập nhật lần cuối
- **updated_by**: Người dùng đã cập nhật lần cuối

Các cột này giúp theo dõi nguồn gốc dữ liệu và là thực hành tiêu chuẩn trong các dự án thực tế.

## Truy Cập H2 Console

### Bước 1: Khởi Động Ứng Dụng

Với Spring Boot DevTools, ứng dụng sẽ tự động khởi động lại khi phát hiện thay đổi.

### Bước 2: Truy Cập Console

Mở trình duyệt của bạn và điều hướng đến:
```
http://localhost:8080/h2-console
```

### Bước 3: Đăng Nhập

- **JDBC URL**: `jdbc:h2:mem:testdb`
- **Username**: `sa`
- **Password**: (để trống)
- Nhấp vào "Connect"

### Bước 4: Xác Minh Các Bảng

Bạn sẽ thấy hai bảng được tạo:
- **CUSTOMER** - với các cột: customer_id, name, email, mobile_number, created_at, created_by, updated_at, updated_by
- **ACCOUNTS** - với các cột: customer_id, account_number, account_type, branch_address, created_at, created_by, updated_at, updated_by

## Hiểu Về H2 In-Memory Database

### Các Đặc Điểm Chính:

1. **Lưu trữ tạm thời** - Dữ liệu chỉ được lưu trong bộ nhớ
2. **Mất dữ liệu khi tắt** - Tất cả dữ liệu và bảng bị xóa khi server dừng
3. **Hiệu suất nhanh** - Các thao tác trong bộ nhớ rất nhanh
4. **Tự động tạo lại** - Bảng được tạo lại khi khởi động bằng schema.sql
5. **Hoàn hảo cho phát triển** - Lý tưởng cho mục đích kiểm thử và phát triển

### Tại Sao Sử Dụng schema.sql?

Vì H2 là in-memory:
- Bảng biến mất khi ứng dụng dừng
- Tạo bảng thủ công mỗi lần rất tẻ nhạt
- `schema.sql` tự động hóa việc tạo bảng trong quá trình khởi động
- Spring Boot thực thi các script này tự động

## Ví Dụ application.yml Hoàn Chỉnh

```yaml
server:
  port: 8080

spring:
  datasource:
    url: jdbc:h2:mem:testdb
    driver-class-name: org.h2.Driver
    username: sa
    password: ''
  h2:
    console:
      enabled: true
  jpa:
    database-platform: org.hibernate.dialect.H2Dialect
    hibernate:
      ddl-auto: update
    show-sql: true
```

## Điểm Chính Cần Nhớ

1. **YAML được ưa chuộng** hơn file properties để dễ đọc và cấu trúc tốt hơn
2. **Indentation rất quan trọng** trong YAML - duy trì khoảng cách nhất quán
3. **H2 console** cung cấp truy cập dễ dàng để xem nội dung database
4. **schema.sql** tự động hóa việc tạo bảng trong quá trình khởi động
5. **Các cột metadata** (created_at, created_by, updated_at, updated_by) là thực hành tiêu chuẩn
6. **show-sql: true** giúp debug bằng cách hiển thị các truy vấn được thực thi
7. **In-memory databases** hoàn hảo cho phát triển nhưng dữ liệu không bền vững

## Các Bước Tiếp Theo

Trong bài học tiếp theo, chúng ta sẽ xây dựng code sử dụng Spring Data JPA để tương tác với H2 database và các bảng. Điều này sẽ cho phép chúng ta thực hiện các thao tác CRUD (Create, Read, Update, Delete) trên dữ liệu.

## Thực Hành Tốt Nhất

1. Luôn khai báo rõ ràng server port trong cấu hình
2. Sử dụng định dạng YAML để dễ bảo trì hơn
3. Kích hoạt H2 console trong quá trình phát triển để debug dễ dàng
4. Bao gồm các cột metadata trong tất cả các bảng
5. Sử dụng `show-sql: true` trong quá trình phát triển để hiểu việc thực thi truy vấn
6. Giữ cấu trúc bảng đơn giản để tập trung vào khái niệm microservices
7. Sử dụng `CREATE TABLE IF NOT EXISTS` để tránh lỗi khi khởi động lại

## Các Vấn Đề Thường Gặp và Giải Pháp

### Vấn đề: YAML không được nhận dạng
**Giải pháp**: Cài đặt plugin YAML trong IDE của bạn

### Vấn đề: Lỗi indentation
**Giải pháp**: Sử dụng spaces thay vì tabs, duy trì indentation 2-space nhất quán

### Vấn đề: Không truy cập được H2 console
**Giải pháp**: Đảm bảo `spring.h2.console.enabled: true` được đặt trong application.yml

### Vấn đề: Bảng không được tạo
**Giải pháp**: Xác minh schema.sql nằm trong thư mục `src/main/resources` và kiểm tra lỗi cú pháp SQL

## Tóm Tắt

Bài học này đề cập đến cấu hình cần thiết cho H2 database trong ứng dụng microservices Spring Boot. Chúng ta đã học về ưu điểm của định dạng YAML, cách cấu hình thuộc tính ứng dụng, tạo database schemas tự động và truy cập H2 console để quản lý database. Những bước nền tảng này chuẩn bị cho chúng ta để triển khai Spring Data JPA trong bài học tiếp theo.




FILE: 80-liveness-and-readiness-probes-in-microservices.md


# Liveness và Readiness Probes trong Microservices

## Giới thiệu

Trong các ứng dụng microservices và cloud-native, các container được triển khai và quản lý bởi các nền tảng điều phối như Kubernetes và Docker. Các nền tảng này cần hiểu được liệu các container đang chạy có khỏe mạnh và hoạt động bình thường hay không. Đây là lúc **liveness** và **readiness probes** phát huy tác dụng.

## Liveness là gì?

**Liveness** là một cơ chế gửi tín hiệu từ container hoặc ứng dụng để chỉ ra liệu container có đang chạy bình thường hay gặp vấn đề về sức khỏe.

### Cách hoạt động của Liveness

- **Nếu container còn sống**: Không cần hành động gì; trạng thái hiện tại là tốt
- **Nếu container chết**: Nền tảng điều phối (Kubernetes, Docker, v.v.) sẽ cố gắng phục hồi ứng dụng bằng cách:
  - Khởi động lại container
  - Tạo container mới nếu khởi động lại thất bại

### Đặc điểm chính

Liveness trả lời một câu hỏi **đúng hoặc sai** đơn giản: **"Container này còn sống không?"**

- **Đúng**: Không cần hành động
- **Sai**: Cần hành động khắc phục (khởi động lại hoặc tạo mới)

### Ví dụ thực tế

Hãy nghĩ về một võ sĩ quyền anh đang ngồi và chờ đợi trận đấu bắt đầu. Điều này xác nhận võ sĩ còn sống và sắp bắt đầu trận đấu, nhưng không nhất thiết có nghĩa là họ đã sẵn sàng để đối mặt với đối thủ - họ có thể vẫn đang khởi động hoặc nhận hướng dẫn từ huấn luyện viên.

## Readiness là gì?

**Readiness** là một probe được sử dụng để xác định liệu container hoặc ứng dụng có sẵn sàng bắt đầu nhận lưu lượng mạng từ client hay không.

### Hiểu về Readiness

Trong quá trình khởi động, một container có thể:
- **Còn sống** (liveness probe trả về kết quả tích cực)
- Nhưng **chưa sẵn sàng** để chấp nhận lưu lượng vì nó đang:
  - Thực hiện công việc nền
  - Khởi động để chấp nhận yêu cầu
  - Thực hiện khởi tạo cơ sở dữ liệu

### Đặc điểm chính

Readiness trả lời câu hỏi: **"Container này có sẵn sàng nhận lưu lượng mạng không?"**

- **Đúng**: Container có thể chấp nhận yêu cầu
- **Sai**: Container cần thêm thời gian để chuẩn bị

### Tại sao Readiness quan trọng

Các nền tảng như Kubernetes đảm bảo cả liveness và readiness đều trả về kết quả tích cực trước khi định tuyến lưu lượng client đến container. Điều này ngăn chặn các tình huống:
- Kiểm tra liveness thành công
- Nhưng ứng dụng chưa hoàn toàn khởi động
- Dẫn đến các yêu cầu thất bại

### Ví dụ thực tế

Khi một võ sĩ quyền anh sẵn sàng chiến đấu, họ đứng dậy từ tư thế ngồi và di chuyển ra giữa võ đài. Điều này cho thấy họ vừa còn sống VÀ sẵn sàng tiếp tục trận đấu.

## Sự khác biệt giữa Liveness và Readiness

| Khía cạnh | Liveness | Readiness |
|-----------|----------|-----------|
| **Mục đích** | Kiểm tra container có sống không | Kiểm tra container có thể chấp nhận lưu lượng không |
| **Hành động khi thất bại** | Khởi động lại/tạo lại container | Không định tuyến lưu lượng đến container |
| **Kịch bản khởi động** | Có thể tích cực ngay lập tức | Thường mất nhiều thời gian hơn khi khởi động |
| **Trường hợp sử dụng** | Phát hiện ứng dụng bị crash | Phát hiện ứng dụng vẫn đang khởi tạo |

## Triển khai trong Spring Boot

Spring Boot cung cấp các actuator endpoints để hiển thị thông tin liveness và readiness.

### Các Endpoint có sẵn

- **Sức khỏe tổng thể**: `/actuator/health`
- **Chỉ liveness**: `/actuator/health/liveness`
- **Chỉ readiness**: `/actuator/health/readiness`

### Các bước cấu hình

#### 1. Thêm Actuator Dependency

Đảm bảo Spring Boot Actuator dependency có trong `pom.xml`:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

#### 2. Cấu hình application.yml

Thêm cấu hình sau để kích hoạt và hiển thị các health endpoints:

```yaml
management:
  health:
    readiness-state:
      enabled: true
    liveness-state:
      enabled: true
  endpoint:
    health:
      probes:
        enabled: true
```

### Cách hoạt động đằng sau

Spring Boot sử dụng các health indicators để cung cấp thông tin liveness và readiness:

- **LivenessStateHealthIndicator**: Cung cấp trạng thái liveness
- **ReadinessStateHealthIndicator**: Cung cấp trạng thái readiness

Các indicator này hiển thị thông tin sức khỏe thông qua các actuator endpoint URLs.

## Trường hợp thực tế: Ví dụ Config Server

Khi khởi động các microservices có phụ thuộc, bạn cần đảm bảo config server đã hoàn toàn khởi động và chấp nhận lưu lượng trước khi khởi động các dịch vụ phụ thuộc (accounts, loans, cards microservices).

### Kiểm tra triển khai

1. **Khởi động config server** (đảm bảo RabbitMQ đang chạy nếu cần)

2. **Kiểm tra sức khỏe tổng thể**:
   ```
   http://localhost:8071/actuator/health
   ```
   Kết quả: `{"status": "UP"}`

3. **Kiểm tra liveness**:
   ```
   http://localhost:8071/actuator/health/liveness
   ```
   Kết quả: `{"status": "UP"}`

4. **Kiểm tra readiness**:
   ```
   http://localhost:8071/actuator/health/readiness
   ```
   Kết quả: `{"status": "UP"}`

### Ý nghĩa của Status

- **UP**: Container/ứng dụng khỏe mạnh và sẵn sàng
- **DOWN**: Container/ứng dụng có vấn đề hoặc chưa sẵn sàng

## Thực hành tốt nhất

1. **Luôn triển khai cả hai probes** khi dịch vụ của bạn có các thành phần phụ thuộc
2. **Cấu hình timeout phù hợp** cho readiness trong quá trình khởi động
3. **Sử dụng liveness probes cẩn thận** - kiểm tra quá tích cực có thể gây ra vòng lặp khởi động lại
4. **Kiểm tra probes ở local** trước khi triển khai lên Kubernetes/môi trường cloud
5. **Giám sát các lỗi probe** để phát hiện sớm các vấn đề ứng dụng

## Tích hợp với Docker Compose

Trong các cấu hình tương lai, bạn có thể sử dụng các health endpoints này trong Docker Compose để xác định phụ thuộc dịch vụ và thứ tự khởi động, đảm bảo các dịch vụ phụ thuộc chỉ khởi động khi các dịch vụ bắt buộc đã sẵn sàng.

## Kết luận

Liveness và readiness probes là các khái niệm thiết yếu trong kiến trúc microservices, cho phép các nền tảng điều phối:
- Phát hiện và phục hồi từ các lỗi
- Quản lý vòng đời container hiệu quả
- Đảm bảo lưu lượng chỉ được định tuyến đến các container khỏe mạnh, sẵn sàng
- Hỗ trợ các hoạt động mở rộng với sự tự tin

Bằng cách triển khai các probes này trong các microservices Spring Boot của bạn, bạn tạo ra các ứng dụng có khả năng phục hồi tốt hơn và sẵn sàng cho production.




FILE: 81-docker-compose-health-checks-and-dependencies.md


# Kiểm Tra Sức Khỏe và Phụ Thuộc Dịch Vụ trong Docker Compose

## Tổng Quan

Hướng dẫn này giải thích cách cấu hình kiểm tra sức khỏe (health checks) và phụ thuộc dịch vụ trong Docker Compose cho kiến trúc microservices sử dụng Spring Boot, Config Server và RabbitMQ.

## Mục Lục

1. [Cấu Hình Health Checks cho Config Server](#cấu-hình-health-checks-cho-config-server)
2. [Thiết Lập Phụ Thuộc Dịch Vụ](#thiết-lập-phụ-thuộc-dịch-vụ)
3. [Thêm Dịch Vụ RabbitMQ](#thêm-dịch-vụ-rabbitmq)
4. [Tối Ưu Cấu Hình Docker Compose](#tối-ưu-cấu-hình-docker-compose)

## Cấu Hình Health Checks cho Config Server

### Tại Sao Cần Health Checks?

Health checks cho phép Docker Compose xác định xem một dịch vụ đã khởi động thành công và sẵn sàng nhận yêu cầu hay chưa. Không có health checks, Docker Compose chỉ biết khi nào dịch vụ bắt đầu khởi động, chứ không biết khi nào nó hoạt động đầy đủ.

### Thêm Cấu Hình Health Check

Trong dịch vụ `config-server` của file `docker-compose.yml`, thêm phần `healthcheck` sau cấu hình `ports`:

```yaml
config-server:
  ports:
    - "8071:8071"
  healthcheck:
    test: "curl --fail --silent localhost:8071/actuator/health/readiness | grep UP || exit 1"
    interval: 10s
    timeout: 5s
    retries: 10
    start_period: 10s
```

### Giải Thích Các Tham Số Health Check

- **test**: Lệnh kiểm tra sức khỏe dịch vụ. Sử dụng `curl` để gọi endpoint readiness của actuator và tìm kiếm trạng thái "UP" bằng `grep`
- **interval**: Thời gian giữa các lần thử health check (10 giây)
- **timeout**: Thời gian tối đa chờ phản hồi cho mỗi lần kiểm tra (5 giây)
- **retries**: Số lần thử lại trước khi coi dịch vụ không khỏe mạnh (10 lần)
- **start_period**: Thời gian trễ ban đầu trước khi bắt đầu health checks (10 giây)

## Thiết Lập Phụ Thuộc Dịch Vụ

### Cấu Hình depends_on với Điều Kiện Sức Khỏe

Để microservice `accounts` đợi Config Server hoàn toàn khỏe mạnh, thêm cấu hình sau:

```yaml
accounts:
  ports:
    - "8080:8080"
  depends_on:
    config-server:
      condition: service_healthy
```

### Các Tùy Chọn Điều Kiện Có Sẵn

- **service_started**: Chỉ đợi cho đến khi dịch vụ khởi động (không kiểm tra sức khỏe)
- **service_healthy**: Đợi cho đến khi health check thành công (được khuyến nghị)
- **service_completed_successfully**: Đợi dịch vụ hoàn thành thành công (phiên bản Docker mới hơn)

### Tại Sao Nên Dùng service_healthy

Sử dụng `condition: service_healthy` đảm bảo các dịch vụ phụ thuộc chỉ khởi động sau khi health check của Config Server thành công, tránh lỗi kết nối và lỗi khởi động.

### Áp Dụng Phụ Thuộc Cho Các Microservices Khác

Áp dụng cấu hình tương tự cho microservices `loans` và `cards`:

```yaml
loans:
  ports:
    - "8090:8090"
  depends_on:
    config-server:
      condition: service_healthy

cards:
  ports:
    - "9000:9000"
  depends_on:
    config-server:
      condition: service_healthy
```

## Thêm Dịch Vụ RabbitMQ

### Tại Sao Cần RabbitMQ?

RabbitMQ được yêu cầu cho Spring Cloud Bus, cho phép cập nhật cấu hình động trên các microservices mà không cần khởi động lại.

### Cấu Hình Dịch Vụ RabbitMQ

```yaml
rabbit:
  image: rabbitmq:3-management
  hostname: rabbitmq
  ports:
    - "5672:5672"
    - "15672:15672"
  healthcheck:
    test: rabbitmq-diagnostics -q ping
    interval: 10s
    timeout: 5s
    retries: 10
    start_period: 10s
  networks:
    - easybank
```

### Hiểu Về Các Cổng RabbitMQ

- **5672**: Cổng nhắn tin RabbitMQ cốt lõi
- **15672**: Cổng giao diện quản lý

RabbitMQ có hai thành phần yêu cầu các cổng riêng biệt:
1. Chức năng nhắn tin cốt lõi
2. Giao diện quản lý

### Health Check RabbitMQ

Health check sử dụng lệnh `rabbitmq-diagnostics -q ping`, đây là phương pháp chính thức được khuyến nghị trong tài liệu RabbitMQ.

### Thêm Phụ Thuộc RabbitMQ vào Config Server

```yaml
config-server:
  # ... các cấu hình khác
  depends_on:
    rabbit:
      condition: service_healthy
```

## Trình Tự Khởi Động Dịch Vụ

Với các cấu hình này, thứ tự khởi động là:

1. **RabbitMQ** khởi động trước và đợi health check thành công
2. **Config Server** khởi động sau khi RabbitMQ khỏe mạnh
3. **Accounts, Loans và Cards** microservices khởi động song song sau khi Config Server khỏe mạnh

### Phụ Thuộc Bắc Cầu

Các microservices accounts, loans và cards không cần phụ thuộc trực tiếp vào RabbitMQ vì:
- Chúng đã phụ thuộc vào Config Server
- Config Server phụ thuộc vào RabbitMQ
- Docker Compose tự động xử lý phụ thuộc bắc cầu

Tuy nhiên, bạn có thể thêm phụ thuộc RabbitMQ một cách rõ ràng nếu muốn mà không gây vấn đề gì.

## Tối Ưu Cấu Hình Docker Compose

### Vấn Đề: Cấu Hình Lặp Lại

File docker-compose.yml hiện tại chứa các cấu hình trùng lặp trên các dịch vụ:
- Hướng dẫn deploy lặp lại cho nhiều dịch vụ
- Cấu hình network lặp lại cho mỗi dịch vụ

### Giải Pháp: File Cấu Hình Chung

Chuyển các cấu hình lặp lại vào file chung và import chúng. Cách tiếp cận này:
- Loại bỏ sự trùng lặp
- Làm cho việc cập nhật dễ dàng hơn (thay đổi một lần, áp dụng mọi nơi)
- Cải thiện khả năng bảo trì

### Quan Trọng: Cấu Hình Network cho RabbitMQ

**Rất quan trọng**: Đừng quên thêm cấu hình network vào dịch vụ RabbitMQ:

```yaml
rabbit:
  # ... các cấu hình khác
  networks:
    - easybank
```

Không có cấu hình này, RabbitMQ sẽ khởi động trong một mạng cô lập, ngăn chặn giao tiếp với các microservices khác.

### Định Nghĩa Network

Ở cuối file docker-compose.yml, định nghĩa mạng chia sẻ:

```yaml
networks:
  easybank:
    driver: bridge
```

Tất cả các dịch vụ nên tham chiếu mạng này để đảm bảo chúng có thể giao tiếp với nhau.

## Tóm Tắt

Cấu hình này đảm bảo:
- ✅ Các dịch vụ khởi động theo đúng thứ tự
- ✅ Health checks xác thực sự sẵn sàng của dịch vụ
- ✅ Phụ thuộc ngăn chặn khởi động dịch vụ sớm
- ✅ Tất cả dịch vụ có thể giao tiếp trên cùng một mạng
- ✅ Cấu hình có thể bảo trì và mở rộng

## Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ tối ưu file docker-compose.yml bằng cách:
- Trích xuất các cấu hình chung
- Tạo các template cấu hình có thể tái sử dụng
- Giảm thêm sự trùng lặp




FILE: 82-toi-uu-hoa-docker-compose-voi-cau-hinh-chung.md


# Tối Ưu Hóa Docker Compose Với Cấu Hình Chung

## Tổng Quan

Trong bài học này, chúng ta sẽ học cách tối ưu hóa file `docker-compose.yml` bằng cách loại bỏ nội dung lặp lại và tạo các template cấu hình có thể tái sử dụng thông qua file `common-config.yml` riêng biệt.

## Tạo File Cấu Hình Chung

### Bước 1: Tạo common-config.yml

Tạo một file mới có tên `common-config.yml` trong cùng thư mục với file `docker-compose.yml`:

```yaml
services:
  network-deploy-service:
    networks:
      - eazybank
```

### Bước 2: Định Nghĩa Các Service Cấu Hình Cơ Bản

#### Network Deploy Service

Service này chứa cấu hình liên quan đến network mà tất cả các service cần:

```yaml
services:
  network-deploy-service:
    networks:
      - eazybank
```

#### Microservice Base Config

Service này kế thừa network service và thêm các cấu hình chung cho microservices:

```yaml
  microservice-base-config:
    extends:
      service: network-deploy-service
    deploy:
      resources:
        limits:
          memory: 700m
```

**Lưu ý:** Biến môi trường `SPRING_PROFILES_ACTIVE` ban đầu được xem xét ở đây nhưng đã được chuyển sang service tiếp theo để giữ cấu hình RabbitMQ riêng biệt.

#### Microservice ConfigServer Config

Service này dành cho các microservices phụ thuộc vào config server:

```yaml
  microservice-configserver-config:
    extends:
      service: microservice-base-config
    depends_on:
      configserver:
        condition: service_healthy
    environment:
      SPRING_PROFILES_ACTIVE: default
      SPRING_CONFIG_IMPORT: configserver:http://configserver:8071/
```

## Phân Cấp Cấu Hình Service

### Cấu Trúc Cấu Hình Ba Tầng

1. **network-deploy-service**: Cấu hình network cơ bản
2. **microservice-base-config**: Kế thừa network service + thêm cấu hình deployment
3. **microservice-configserver-config**: Kế thừa base config + thêm phụ thuộc config server

### Tại Sao Phải Tách Riêng Các Service?

- **RabbitMQ** chỉ cần cấu hình network (sử dụng `network-deploy-service`)
- **Config Server** cần cấu hình network + deployment (sử dụng `microservice-base-config`)
- **Microservices nghiệp vụ** (accounts, loans, cards) cần tất cả cấu hình bao gồm phụ thuộc config server (sử dụng `microservice-configserver-config`)

## Cập Nhật docker-compose.yml

### RabbitMQ Service

Thay thế cấu hình network bằng:

```yaml
rabbitmq:
  image: rabbitmq:3.13-management
  hostname: rabbitmq
  ports:
    - "5672:5672"
    - "15672:15672"
  healthcheck:
    test: rabbitmq-diagnostics check_port_connectivity
    interval: 10s
    timeout: 5s
    retries: 10
    start_period: 5s
  extends:
    file: common-config.yml
    service: network-deploy-service
```

### Config Server

```yaml
configserver:
  image: "eazybytes/configserver:s6"
  container_name: configserver-ms
  ports:
    - "8071:8071"
  healthcheck:
    test: "curl --fail --silent localhost:8071/actuator/health/readiness | grep UP || exit 1"
    interval: 10s
    timeout: 5s
    retries: 10
    start_period: 10s
  extends:
    file: common-config.yml
    service: microservice-base-config
```

### Microservices Nghiệp Vụ (Accounts, Loans, Cards)

Với mỗi microservice, xóa bỏ:
- Phần `depends_on`
- Phần `deploy`
- Phần `networks`
- Biến môi trường `SPRING_CONFIG_IMPORT`
- Biến môi trường `SPRING_PROFILES_ACTIVE`

Thay thế bằng:

```yaml
accounts:
  image: "eazybytes/accounts:s6"
  container_name: accounts-ms
  ports:
    - "8080:8080"
  environment:
    SPRING_APPLICATION_NAME: "accounts"
  extends:
    file: common-config.yml
    service: microservice-configserver-config
```

## Lợi Ích Của Phương Pháp Này

1. **Nguồn Chân Lý Duy Nhất**: Tên network, giới hạn bộ nhớ và cấu hình chung ở một nơi
2. **Bảo Trì Dễ Dàng Hơn**: Thay đổi cấu hình một lần, áp dụng cho tất cả services
3. **Cải Thiện Khả Năng Đọc**: File `docker-compose.yml` ngắn gọn và sạch hơn
4. **Tổ Chức Tốt Hơn**: Tách biệt các mối quan tâm giữa cấu hình chung và cấu hình đặc thù của service
5. **Giảm Trùng Lặp**: Không còn các khối cấu hình lặp lại

## Những Điểm Chính Cần Nhớ

- Các cấu hình chung được trích xuất vào `common-config.yml`
- Các service kế thừa cấu hình cơ bản bằng từ khóa `extends`
- Phân cấp cấu hình cho phép các mẫu tái sử dụng linh hoạt
- RabbitMQ, Config Server và microservices nghiệp vụ mỗi cái kế thừa các base service phù hợp
- Các thay đổi tương lai đối với cấu hình chung chỉ cần thực hiện ở một nơi

## Bước Tiếp Theo

Trong bài học tiếp theo, chúng ta sẽ tạo các Docker image để kiểm tra các thay đổi docker-compose này.




FILE: 83-xay-dung-va-day-docker-images-cho-microservices.md


# Xây Dựng và Đẩy Docker Images cho Microservices

## Tổng Quan

Hướng dẫn này bao gồm việc tạo Docker images cho tất cả các microservices bao gồm config server, và đẩy chúng lên Docker Hub. Chúng ta sẽ sử dụng Google Jib để xây dựng Docker images một cách hiệu quả cho các microservices: accounts, cards, loans và config server.

## Yêu Cầu Trước Khi Bắt Đầu

- Đã cài đặt Maven
- Đã cài đặt và chạy Docker Desktop
- Có tài khoản Docker Hub
- Dự án Spring Boot microservices (accounts, cards, loans, config server)

## Tại Sao Cần Tạo Lại Docker Images?

Chúng ta cần tạo lại Docker images cho các microservices accounts, loans và cards vì đã có nhiều thay đổi quan trọng liên quan đến quản lý cấu hình trong Spring Cloud Config.

## Cấu Trúc Dự Án

```
section-6/v2-spring-cloud-config/
├── accounts/
├── cards/
├── config-server/
└── loans/
```

## Xây Dựng Docker Images với Google Jib

### Bước 1: Xây Dựng Image cho Accounts Microservice

Điều hướng đến thư mục accounts microservice (nơi có file `pom.xml`) và chạy lệnh:

```bash
mvn compile jib:dockerBuild
```

**Lưu ý:** Chữ 'B' trong `dockerBuild` phải viết hoa.

Lệnh này sẽ:
- Tạo một Docker image mới cho accounts microservice
- Gắn thẻ (tag) là `S6`
- Hoàn thành trong khoảng 8 giây

**Tại sao dùng Jib?** Jib rất nhanh và vô cùng tiện lợi cho các hệ thống local, đó là lý do tại sao nó được sử dụng trong suốt khóa học này.

### Bước 2: Xây Dựng Image cho Cards Microservice

Điều hướng đến thư mục cards microservice và chạy cùng lệnh:

```bash
mvn compile jib:dockerBuild
```

Lệnh này tạo Docker image có tên `cards` với thẻ `S6`, hoàn thành trong khoảng 10 giây.

### Bước 3: Xây Dựng Image cho Loans Microservice

Điều hướng đến thư mục loans microservice và thực thi:

```bash
mvn compile jib:dockerBuild
```

### Bước 4: Cấu Hình Jib Plugin cho Config Server

**Quan trọng:** Lệnh tương tự sẽ không hoạt động cho config server ban đầu vì chúng ta chưa thêm thông tin plugin Jib vào file `pom.xml` của nó.

#### Thêm Jib Plugin vào Config Server

1. Mở file `pom.xml` của config server
2. Sao chép cấu hình Jib plugin từ file `pom.xml` của bất kỳ microservice nào khác
3. Thêm nó sau phần Spring Boot Maven plugin

**Ví Dụ Cấu Hình Plugin:**

```xml
<plugin>
    <groupId>com.google.cloud.tools</groupId>
    <artifactId>jib-maven-plugin</artifactId>
    <configuration>
        <to>
            <image>eazybytes/${project.artifactId}:S6</image>
        </to>
    </configuration>
</plugin>
```

Cấu hình bao gồm:
- Tên image: `eazybytes/config-server`
- Thẻ (tag): `S6`

4. Tải lại các thay đổi Maven
5. Điều hướng đến thư mục config server trong terminal
6. Chạy lệnh build:

```bash
mvn compile jib:dockerBuild
```

## Xác Minh Docker Images

### Sử Dụng Docker CLI

```bash
docker images
```

### Sử Dụng Docker Desktop Dashboard

1. Mở Docker Desktop
2. Điều hướng đến tab Images
3. Bạn sẽ thấy bốn images mới với thẻ `S6`:
   - accounts:S6
   - cards:S6
   - loans:S6
   - config-server:S6

## Dọn Dẹp Các Images Cũ

Để tiết kiệm dung lượng lưu trữ, xóa các Docker images không cần thiết từ các phần trước (ví dụ: images S4):

1. Mở Docker Desktop Dashboard
2. Điều hướng đến Images
3. Xóa các images không sử dụng:
   - Images buildpacks cũ
   - Images có thẻ Section 4 (S4) cho loans, cards, accounts
   - Các images không sử dụng khác

**Giữ lại các images sau:**
- RabbitMQ
- MySQL
- Keycloak (để test)
- Các images S6 mới nhất

### Dọn Dẹp Containers Không Sử Dụng

Kiểm tra các containers không sử dụng và xóa chúng. Ví dụ, nếu RabbitMQ container đang chạy, bạn có thể xóa nó vì Docker Compose sẽ tự động tạo lại khi cần.

## Đẩy Images Lên Docker Hub

### Yêu Cầu Trước Khi Đẩy

- Đảm bảo bạn đã đăng nhập vào Docker Desktop
- Docker phải đang chạy

### Định Dạng Lệnh Push

```bash
docker image push docker.io/<tên-docker-username>/<tên-image>:<thẻ>
```

### Quy Trình Đẩy Từng Bước

#### 1. Đẩy Accounts Image

```bash
docker image push docker.io/eazybytes/accounts:S6
```

**Lưu ý:** Image phải tồn tại trong hệ thống local của bạn thì lệnh push mới hoạt động.

Sau vài giây, Docker image của accounts sẽ được đẩy thành công lên Docker Hub.

#### 2. Đẩy Loans Image

```bash
docker image push docker.io/eazybytes/loans:S6
```

#### 3. Đẩy Cards Image

```bash
docker image push docker.io/eazybytes/cards:S6
```

#### 4. Đẩy Config Server Image

```bash
docker image push docker.io/eazybytes/config-server:S6
```

## Xác Minh Images Trên Docker Hub

1. Truy cập [Docker Hub](https://hub.docker.com/)
2. Đăng nhập vào tài khoản của bạn
3. Làm mới trang
4. Bạn sẽ thấy các repositories với images mới:
   - config-server
   - cards
   - loans
   - accounts

### Kiểm Tra Các Thẻ Image

Nhấp vào bất kỳ repository nào (ví dụ: accounts) để xem các thẻ có sẵn:
- **Thẻ S4:** Docker image từ Section 4
- **Thẻ S6:** Docker image mới nhất từ Section 6

**Lưu ý:** Config server sẽ chỉ có thẻ S6 vì không có image S4 nào được đẩy lên trước đó.

## Lợi Ích Của Việc Đẩy Lên Docker Hub

- **Lưu Trữ Từ Xa:** Images được lưu trữ trong repository từ xa
- **Truy Cập Dễ Dàng:** Bất kỳ ai cũng có thể pull và sử dụng các images này
- **Tính Công Khai:** Images được công khai để chia sẻ
- **Tích Hợp Docker Compose:** Khi chạy Docker Compose mà không có images local, nó sẽ tự động pull từ repository từ xa

## Tóm Tắt

Trong hướng dẫn này, chúng ta đã:
1. ✅ Tạo Docker images cho tất cả các microservices (accounts, cards, loans, config server) sử dụng Google Jib
2. ✅ Cấu hình Jib plugin trong file `pom.xml` của config server
3. ✅ Dọn dẹp các Docker images và containers cũ không sử dụng
4. ✅ Đẩy thành công tất cả Docker images lên Docker Hub với thẻ S6
5. ✅ Xác minh các images đã có sẵn trên Docker Hub

## Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ kiểm tra file Docker Compose với profile mặc định và xác minh rằng tất cả các thay đổi cấu hình đều hoạt động chính xác.

## Tham Khảo Các Lệnh Chính

| Hành Động | Lệnh |
|-----------|------|
| Xây dựng Docker image với Jib | `mvn compile jib:dockerBuild` |
| Liệt kê Docker images | `docker images` |
| Đẩy image lên Docker Hub | `docker image push docker.io/<username>/<image>:<tag>` |
| Xóa Docker image | `docker image rm <image-id>` |

---

**Khóa Học:** Microservices với Spring Boot  
**Phần:** 6 - Docker và Quản Lý Cấu Hình  
**Thời Gian:** Hoàn thành trong khoảng 30-40 phút




FILE: 84-docker-compose-configuration-and-rabbitmq-integration.md


# Cấu Hình Docker Compose và Tích Hợp RabbitMQ cho Microservices

## Tổng Quan

Hướng dẫn này trình bày cách cấu hình và chạy microservices sử dụng Docker Compose, bao gồm thiết lập RabbitMQ để làm mới cấu hình động mà không cần khởi động lại containers.

## Yêu Cầu Trước

- Docker Desktop đã được cài đặt và đang chạy
- Không có containers nào đang chạy (môi trường sạch)
- Git repository chứa các file cấu hình
- Postman để test API

## Thiết Lập Ban Đầu

### Bước 1: Di Chuyển đến Thư Mục Docker Compose

```bash
cd docker-compose/default
```

### Bước 2: Khởi Động Containers với Docker Compose

```bash
docker compose up -d
```

Lệnh này khởi động tất cả containers ở chế độ detached. Thứ tự khởi động:
1. RabbitMQ service
2. Config Server
3. Các microservices Accounts, Cards và Loans

### Bước 3: Kiểm Tra Containers Đang Chạy

```bash
docker ps
```

Bạn sẽ thấy:
- **RabbitMQ**: Trạng thái hiển thị "healthy" (đã cấu hình health check)
- **Config Server**: Trạng thái hiển thị "healthy" (đã cấu hình health check)
- **Accounts, Cards, Loans**: Mới khởi động (chưa cấu hình health check)

## Kiểm Tra Profile Mặc Định

### Endpoint Build Info

```
GET http://localhost:8080/api/build-info
```

Kết quả mong đợi: Version 3.0 (profile mặc định)

### Endpoint Java Version

```
GET http://localhost:8080/api/java-version
```

Kết quả mong đợi: Đường dẫn JAVA_HOME bên trong container

### Endpoint Contact Info

```
GET http://localhost:8080/api/contact-info
```

Kết quả mong đợi: Các thuộc tính từ profile mặc định

## Cấu Hình Làm Mới Động với Webhooks

### Bước 1: Thiết Lập Hookdeck

1. Truy cập [Hookdeck](https://hookdeck.com)
2. Click vào "test webhook post"
3. Click "add destination" để tạo session mới

### Bước 2: Cài Đặt và Đăng Nhập Hookdeck CLI

```bash
# Nếu có session trước, logout trước
hookdeck logout

# Đăng nhập vào session mới
hookdeck login
```

### Bước 3: Khởi Động Webhook Listener

```bash
hookdeck listen 8071 /monitor localhost
```

Lệnh này tạo một webhook URL để tích hợp với GitHub.

### Bước 4: Cấu Hình GitHub Webhook

1. Điều hướng đến GitHub repository của bạn (ví dụ: `eazybytes-config`)
2. Vào **Settings** → **Webhooks**
3. Chỉnh sửa webhook có sẵn hoặc tạo mới
4. Cập nhật **Payload URL** với webhook URL từ Hookdeck
5. Click **Update webhook**

## Khắc Phục Sự Cố Kết Nối RabbitMQ

### Vấn Đề

Khi test làm mới cấu hình, bạn có thể gặp lỗi 500. Kiểm tra logs của Config Server cho thấy:

```
Attempting to connect to RabbitMQ at localhost:5672
```

Điều này thất bại vì RabbitMQ không chạy trên `localhost` mà trong một container riêng biệt.

### Giải Pháp: Cập Nhật Cấu Hình Docker Compose

Trong file `docker-compose.yml`, thêm chi tiết kết nối RabbitMQ vào cấu hình microservice chung:

```yaml
microservice-base-config:
  deploy:
    environment:
      SPRING_RABBITMQ_HOST: rabbit  # Tên service, không phải localhost
```

Cấu hình này áp dụng cho:
- Config Server
- Microservice Accounts
- Microservice Cards
- Microservice Loans

### Tại Sao Cách Này Hoạt Động

- Tất cả containers chạy trong cùng một Docker network
- Các services có thể kết nối bằng tên service (ví dụ: `rabbit`)
- Port mặc định (5672), username và password không thay đổi

## Khởi Động Lại Containers với Cấu Hình Đã Cập Nhật

### Bước 1: Dừng và Xóa Containers Hiện Tại

```bash
docker compose down
```

### Bước 2: Khởi Động Containers với Cấu Hình Mới

```bash
docker compose up -d
```

### Bước 3: Kiểm Tra Kết Nối Config Server

Kiểm tra logs của Config Server:

```
Attempting to connect to RabbitMQ at rabbit:5672
Successfully created new connection
```

### Bước 4: Kiểm Tra Trạng Thái Health

```
GET http://localhost:8080/actuator/health
```

Kết quả mong đợi: `"status": "UP"`

```
GET http://localhost:8080/actuator/health/readiness
```

Kết quả mong đợi: `"status": "UP"`

## Kiểm Tra Làm Mới Cấu Hình Động

### Bước 1: Cập Nhật Cấu Hình trên GitHub

1. Điều hướng đến `accounts.yml` trong GitHub repository
2. Chỉnh sửa file (ví dụ: thay đổi `local` thành `docker`)
3. Commit thay đổi

### Bước 2: Xác Minh Webhook Đã Kích Hoạt

Kiểm tra terminal Hookdeck - bạn sẽ thấy mã trạng thái 200 cho biết webhook đã được gửi thành công.

### Bước 3: Kiểm Tra Cập Nhật Cấu Hình

```
GET http://localhost:8080/api/contact-info
```

Kết quả phải phản ánh thuộc tính đã được cập nhật **mà không cần khởi động lại containers**.

### Bước 4: Hoàn Tác Thay Đổi (Tùy Chọn)

1. Chỉnh sửa `accounts.yml` lại (đổi `docker` về `local`)
2. Commit thay đổi
3. Xác minh mã trạng thái 200 trong terminal Hookdeck
4. Test endpoint lại để xác nhận thuộc tính đã được hoàn tác

## Các Khái Niệm Chính

### Độ Ưu Tiên của Biến Môi Trường

Biến môi trường có độ ưu tiên cao nhất trong hệ thống phân cấp cấu hình Spring Boot, ghi đè các giá trị trong `application.yml` và `commonconfig.yml`.

### Health Checks

- **Health endpoint**: Hiển thị trạng thái tổng thể của ứng dụng, bao gồm các phụ thuộc tùy chọn (RabbitMQ)
- **Readiness endpoint**: Hiển thị nếu ứng dụng sẵn sàng chấp nhận traffic (loại trừ các phụ thuộc tùy chọn)

### Service Discovery trong Docker Networks

Các containers trong cùng Docker network có thể giao tiếp bằng tên service được định nghĩa trong `docker-compose.yml`.

## Cấu Trúc File Cấu Hình

- **docker-compose.yml**: Cấu hình điều phối containers
- **application.yml**: Các thuộc tính đặc thù cho ứng dụng
- **commonconfig.yml**: Cấu hình chung cho tất cả microservices
- **accounts.yml**: Các thuộc tính của microservice Accounts

## Các Bước Tiếp Theo

- Thiết lập Docker Compose cho profile **prod**
- Thiết lập Docker Compose cho profile **qa**
- Xác thực tất cả profiles hoạt động đúng
- Cấu hình health checks cho Accounts, Cards và Loans microservices

## Tóm Tắt

Thiết lập này trình bày:
- Khởi động nhiều microservices với Docker Compose
- Cấu hình RabbitMQ cho quản lý cấu hình phân tán
- Triển khai làm mới cấu hình động qua GitHub webhooks
- Khắc phục sự cố kết nối mạng của containers
- Kiểm tra thay đổi cấu hình mà không cần khởi động lại containers

Thiết lập Docker Compose với tích hợp RabbitMQ cho phép cập nhật cấu hình liền mạch trên tất cả microservices trong profile mặc định.




FILE: 85-cau-hinh-docker-compose-da-moi-truong.md


# Cấu Hình Docker Compose Đa Môi Trường Cho Microservices

## Tổng Quan

Hướng dẫn này trình bày cách cấu hình và triển khai các microservices Spring Boot trên nhiều môi trường khác nhau (default, QA và production) sử dụng Docker Compose với các profile theo từng môi trường.

## Yêu Cầu Trước

- Đã cài đặt Docker Desktop
- Dự án Spring Boot microservices
- Các file cấu hình Docker Compose
- Repository Git cho quản lý cấu hình (eazybytes-config)

## Kiến Trúc

Thiết lập bao gồm các container sau:
- **RabbitMQ** - Message broker
- **Config Server** - Spring Cloud Config Server
- **Accounts Microservice** - Dịch vụ tài khoản
- **Loans Microservice** - Dịch vụ khoản vay
- **Cards Microservice** - Dịch vụ thẻ

## Tạo File Docker Compose Theo Môi Trường

### Bước 1: Dừng Các Container Đang Chạy

Trước khi tạo file Docker Compose mới, hãy dừng tất cả các container đang chạy:

```bash
docker compose down
```

Lệnh này sẽ dừng và xóa tất cả các container trong hệ thống của bạn.

### Bước 2: Tạo Cấu Hình Theo Profile

Quy trình rất đơn giản:

1. Sao chép hai file từ thư mục `default`
2. Dán chúng vào thư mục `prod`
3. Dán chúng vào thư mục `qa`

### Bước 3: Chỉnh Sửa Biến Môi Trường

Chỉ cần thay đổi duy nhất trong file `commonconfig.yml`:

**Cho môi trường Production:**
```yaml
spring:
  profiles:
    active: prod
```

**Cho môi trường QA:**
```yaml
spring:
  profiles:
    active: qa
```

## Lợi Ích Chính

### 1. Docker Image Bất Biến (Immutable)
- Sử dụng cùng một Docker image trên tất cả các môi trường
- Kiểm soát hành vi thông qua biến môi trường
- Duy trì tính nhất quán trong triển khai

### 2. Cấu Hình Theo Từng Môi Trường
- Tùy chỉnh tài nguyên cho từng môi trường
- Ví dụ: Tăng cấp phát bộ nhớ trong production
  ```yaml
  # commonconfig.yml - Production
  memory: 1024mb  # Thay vì 700mb trong default
  ```

### 3. Tích Hợp Spring Boot
- Tận dụng Spring profiles để quản lý cấu hình
- Tích hợp liền mạch với Docker containers
- Quản lý cấu hình bên ngoài

## Kiểm Tra Cấu Hình

### Khởi Động Container Với Profile Production

1. Di chuyển đến thư mục production:
   ```bash
   cd prod
   ```

2. Khởi động tất cả containers:
   ```bash
   docker compose up
   ```

3. Các container sau sẽ được khởi động:
   - RabbitMQ
   - Config Server
   - Loans Microservice
   - Cards Microservice
   - Accounts Microservice

### Xác Minh Trạng Thái Container

Kiểm tra trạng thái container trong Docker Desktop:
1. Mở Docker Desktop
2. Chọn profile `prod`
3. Xác minh từng container:
   - ✓ RabbitMQ - Khởi động thành công
   - ✓ Config Server - Khởi động thành công
   - ✓ Loans Microservice - Khởi động thành công
   - ✓ Cards Microservice - Khởi động thành công
   - ✓ Accounts Microservice - Khởi động thành công

## Kiểm Tra Thay Đổi Cấu Hình

### Kiểm Tra Cập Nhật Cấu Hình Động

1. **Chỉnh Sửa Cấu Hình:**
   - Truy cập repository `eazybytes-config`
   - Chỉnh sửa file `cards-prod.yml`
   - Thay đổi thuộc tính message:
     ```yaml
     message: "Docker APIs"
     ```
   - Commit thay đổi lên GitHub

2. **Kiểm Tra Thay Đổi:**
   - Sử dụng Postman để gọi API `contact-info` của Cards microservice
   - Kết quả trả về sẽ hiển thị: `"Docker APIs"`

3. **Hoàn Tác Thay Đổi:**
   - Chỉnh sửa `cards-prod.yml` một lần nữa
   - Đổi lại thành:
     ```yaml
     message: "Prod APIs"
     ```
   - Commit thay đổi lên GitHub

4. **Xác Minh Việc Hoàn Tác:**
   - Gọi API lại trong Postman
   - Kết quả trả về sẽ hiển thị: `"Prod APIs"`
   - Lưu ý: Có thể có độ trễ 5-10 giây để refresh thuộc tính

## Thực Hành Tốt Nhất

### 1. Quản Lý Cấu Hình
- Giữ cấu hình theo môi trường trong các file riêng biệt
- Sử dụng kiểm soát phiên bản (Git) cho repository cấu hình
- Triển khai theo dõi thay đổi phù hợp

### 2. Phương Pháp Học
- Hoàn thành khóa học theo tốc độ của riêng bạn
- Mục tiêu một phần mỗi ngày hoặc mỗi tuần
- Tránh cố gắng hoàn thành mọi thứ trong một lần
- Nghỉ ngơi để tiếp thu kiến thức

### 3. Phân Bổ Tài Nguyên
- Điều chỉnh tài nguyên container dựa trên nhu cầu môi trường
- Production thường yêu cầu nhiều bộ nhớ và CPU hơn
- Giám sát và tối ưu hóa dựa trên việc sử dụng thực tế

## Xử Lý Sự Cố

### Độ Trễ Refresh Cấu Hình
- Thay đổi cấu hình có thể mất 5-10 giây để lan truyền
- Đợi một chút trước khi kiểm tra sau khi commit thay đổi

### Vấn Đề Khởi Động Container
- Đảm bảo tất cả các port cần thiết đều khả dụng
- Kiểm tra Docker Desktop để xem log chi tiết của container
- Xác minh kết nối mạng giữa các container

## Tổng Kết

Thiết lập Docker Compose đa môi trường này cung cấp:
- ✓ Triển khai Docker image đơn lẻ trên tất cả các môi trường
- ✓ Quản lý cấu hình theo từng môi trường
- ✓ Tích hợp liền mạch với Spring Boot profiles
- ✓ Cập nhật cấu hình động mà không cần triển khai lại
- ✓ Linh hoạt tùy chỉnh tài nguyên theo từng môi trường

## Tài Nguyên và Hỗ Trợ

### Nhận Trợ Giúp
- **Website:** [eazybytes.com](https://eazybytes.com)
- **Email:** tutor@eazybytes.com
- **LinkedIn:** Theo dõi eazybytes để cập nhật thường xuyên
- **Udemy:** Gửi tin nhắn thông qua nền tảng khóa học

### Phản Hồi
Phản hồi của bạn rất có giá trị! Vui lòng:
- Cung cấp đánh giá khóa học
- Chia sẻ những gì bạn thích hoặc không thích
- Kết nối trên LinkedIn để phản hồi cá nhân
- Liên hệ qua email cho các câu hỏi cụ thể

---

**Bước Tiếp Theo:** Nghỉ ngơi và tiếp tục với phần tiếp theo khi sẵn sàng. Hãy nhớ, học tập đều đặn hiệu quả hơn việc học dồn!




FILE: 9-tao-entity-classes-va-repositories.md


# Tạo Entity Classes và Repository Interfaces với Spring Data JPA

## Tổng Quan

Bài giảng này trình bày cách tạo các lớp entity JPA và các interface repository để tương tác với các bảng cơ sở dữ liệu trong ứng dụng microservices Spring Boot. Chúng ta sẽ học cách ánh xạ các lớp Java vào các bảng cơ sở dữ liệu và tận dụng framework Spring Data JPA cho các thao tác CRUD.

## Yêu Cầu Trước

- Cơ sở dữ liệu H2 được cấu hình với các bảng `accounts` và `customer`
- Đã thêm dependency Spring Data JPA vào `pom.xml`
- Hiểu biết cơ bản về cơ sở dữ liệu và Java

## Cấu Trúc Bảng

Chúng ta đang làm việc với hai bảng cơ sở dữ liệu:
- **customer**: Lưu trữ thông tin khách hàng
- **accounts**: Lưu trữ chi tiết tài khoản ngân hàng

Cả hai bảng đều bao gồm bốn cột metadata:
- `created_at`: Thời gian tạo bản ghi
- `created_by`: Người dùng đã tạo bản ghi
- `updated_at`: Thời gian cập nhật bản ghi lần cuối
- `updated_by`: Người dùng đã cập nhật lần cuối

## Tạo Lớp Base Entity

### Bước 1: Tạo Package Entity

Tạo package mới: `com.easybytes.accounts.entity`

Package này sẽ chứa tất cả các lớp entity đại diện cho các bảng cơ sở dữ liệu.

### Bước 2: Tạo Lớp BaseEntity

Do tất cả các bảng đều có chung các cột metadata, chúng ta sẽ tạo một lớp cha để tránh trùng lặp code.

```java
package com.easybytes.accounts.entity;

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;
import javax.persistence.*;
import java.time.LocalDateTime;

@MappedSuperclass
@Getter
@Setter
@ToString
public class BaseEntity {
    
    @Column(updatable = false)
    private LocalDateTime createdAt;
    
    @Column(updatable = false)
    private String createdBy;
    
    @Column(insertable = false)
    private LocalDateTime updatedAt;
    
    @Column(insertable = false)
    private String updatedBy;
}
```

### Giải Thích Các Annotation Chính

#### Các Annotation Lombok
- **@Getter**: Tự động tạo các phương thức getter cho tất cả các trường
- **@Setter**: Tự động tạo các phương thức setter cho tất cả các trường
- **@ToString**: Tạo phương thức `toString()` cho lớp

#### Các Annotation JPA
- **@MappedSuperclass**: Chỉ ra rằng lớp này sẽ đóng vai trò là lớp cha cho các lớp entity
- **@Column**: Cấu hình ánh xạ cột và hành vi
  - `updatable = false`: Ngăn cập nhật cột khi cập nhật bản ghi (cho các trường creation)
  - `insertable = false`: Ngăn chèn cột khi tạo bản ghi (cho các trường update)

### Quy Ước Đặt Tên

Tên trường tuân theo quy ước camelCase, mà Spring Data JPA tự động ánh xạ sang các cột cơ sở dữ liệu snake_case:
- `createdAt` → `created_at`
- `createdBy` → `created_by`
- `updatedAt` → `updated_at`
- `updatedBy` → `updated_by`

## Tạo Entity Customer

### Bước 1: Tạo Lớp Customer

```java
package com.easybytes.accounts.entity;

import lombok.*;
import javax.persistence.*;

@Entity
@Getter
@Setter
@ToString
@AllArgsConstructor
@NoArgsConstructor
public class Customer extends BaseEntity {
    
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO, generator = "native")
    @GenericGenerator(name = "native", strategy = "native")
    private Long customerId;
    
    private String name;
    
    private String email;
    
    @Column(name = "mobile_number")
    private String mobileNumber;
}
```

### Giải Thích Các Annotation Chính

#### Các Annotation Entity
- **@Entity**: Đánh dấu lớp này là entity JPA đại diện cho một bảng cơ sở dữ liệu
- **@Table**: (Tùy chọn) Chỉ định rõ tên bảng nếu khác với tên lớp

#### Các Annotation Primary Key
- **@Id**: Chỉ định trường này là khóa chính
- **@GeneratedValue**: Cấu hình tự động tạo khóa chính
  - `strategy = GenerationType.AUTO`: Chiến lược tự động tạo
  - `generator = "native"`: Tham chiếu đến generator được định nghĩa bên dưới
- **@GenericGenerator**: Định nghĩa một generator tùy chỉnh
  - `strategy = "native"`: Sử dụng cơ chế tạo sequence native của cơ sở dữ liệu (tùy thuộc database)

#### Các Annotation Lombok
- **@AllArgsConstructor**: Tạo constructor với tất cả các trường làm tham số
- **@NoArgsConstructor**: Tạo constructor không tham số

### Ánh Xạ Trường

Annotation `@Column` là tùy chọn khi tên trường khớp với tên cột (bỏ qua phân biệt chữ hoa/thường và dấu gạch dưới). Sử dụng ở đây để làm rõ:

```java
@Column(name = "mobile_number")
private String mobileNumber;
```

## Tạo Entity Accounts

### Bước 1: Tạo Lớp Accounts

```java
package com.easybytes.accounts.entity;

import lombok.*;
import javax.persistence.*;

@Entity
@Getter
@Setter
@ToString
@AllArgsConstructor
@NoArgsConstructor
public class Accounts extends BaseEntity {
    
    @Column(name = "customer_id")
    private Long customerId;
    
    @Id
    @Column(name = "account_number")
    private Long accountNumber;
    
    @Column(name = "account_type")
    private String accountType;
    
    @Column(name = "branch_address")
    private String branchAddress;
}
```

### Các Điểm Khác Biệt Quan Trọng

1. **Không Có Tự Động Tạo Khóa Chính**: Không giống như entity `Customer`, `accountNumber` không sử dụng `@GeneratedValue`
2. **Tạo Account Number Thủ Công**: Số tài khoản sẽ được tạo theo logic lập trình trong tầng service
3. **Lý Do Logic Nghiệp Vụ**: Số tài khoản ngân hàng thường là số có 10 chữ số, không phải ID tuần tự (1, 2, 3...)

### Quan Hệ Khóa Ngoại

Trường `customerId` thiết lập mối liên kết giữa các bảng `accounts` và `customer`, nhưng nó không phải là khóa chính của bảng này.

## Tạo Các Interface Repository

### Bước 1: Tạo Package Repository

Tạo package mới: `com.easybytes.accounts.repository`

### Bước 2: Tạo Interface CustomerRepository

```java
package com.easybytes.accounts.repository;

import com.easybytes.accounts.entity.Customer;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface CustomerRepository extends JpaRepository<Customer, Long> {
}
```

### Bước 3: Tạo Interface AccountsRepository

```java
package com.easybytes.accounts.repository;

import com.easybytes.accounts.entity.Accounts;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface AccountsRepository extends JpaRepository<Accounts, Long> {
}
```

## Hiểu Về JpaRepository

### Các Khái Niệm Chính

1. **Annotation @Repository**: Đánh dấu interface là repository của Spring Data, cho phép Spring tạo bean implementation tại runtime

2. **Interface JpaRepository**: Cung cấp các phương thức có sẵn cho các thao tác CRUD
   - Tham số generic: `JpaRepository<Entity, PrimaryKeyType>`
   - `Customer`: Lớp entity
   - `Long`: Kiểu dữ liệu của khóa chính

3. **Tự Động Tạo Phương Thức**: Spring Data JPA tạo code implementation tại runtime

### Các Phương Thức Có Sẵn

Không cần viết bất kỳ SQL nào, bạn đã có quyền truy cập vào các phương thức như:

#### Thao Tác Tạo/Cập Nhật
- `save(entity)`: Chèn hoặc cập nhật một bản ghi
- `saveAll(entities)`: Chèn/cập nhật hàng loạt

#### Thao Tác Đọc
- `findById(id)`: Tìm bản ghi theo khóa chính
- `findAll()`: Lấy tất cả các bản ghi
- `findAllById(ids)`: Tìm nhiều bản ghi theo ID
- `count()`: Đếm tổng số bản ghi
- `existsById(id)`: Kiểm tra xem bản ghi có tồn tại không

#### Thao Tác Xóa
- `deleteById(id)`: Xóa theo khóa chính
- `delete(entity)`: Xóa entity cụ thể
- `deleteAll()`: Xóa tất cả bản ghi

### Phân Cấp Repository

`JpaRepository` kế thừa:
- `PagingAndSortingRepository`: Cung cấp khả năng phân trang và sắp xếp
- `QueryByExampleExecutor`: Cho phép truy vấn theo mẫu

## Các Phương Pháp Hay Nhất

### 1. Sử Dụng Các Annotation Lombok
- Giảm code boilerplate
- Giữ các lớp ngắn gọn và dễ đọc
- Các phương thức được tạo xuất hiện trong bytecode, không phải source code

### 2. Tuân Thủ Quy Ước Đặt Tên
- Khớp tên trường với tên cột (camelCase sang snake_case)
- Sử dụng tên entity và repository mô tả rõ ràng

### 3. Tạo Lớp Base Cho Các Trường Chung
- Giảm trùng lặp code
- Đảm bảo tính nhất quán giữa các entity
- Dễ dàng bảo trì hơn

### 4. Sử Dụng Annotation @Column Một Cách Chiến Lược
- Bắt buộc khi tên không khớp
- Hữu ích cho mục đích tài liệu hóa
- Cấu hình hành vi cột (updatable, insertable)

### 5. Xem Xét Chiến Lược Khóa Chính
- Sử dụng tự động tạo cho ID nội bộ
- Sử dụng tạo thủ công cho các định danh có ý nghĩa nghiệp vụ
- Chọn chiến lược generator phù hợp cho cơ sở dữ liệu của bạn

## Tổng Kết

Trong bài giảng này, chúng ta đã hoàn thành:

1. ✅ Tạo lớp `BaseEntity` với các trường metadata chung
2. ✅ Triển khai entity `Customer` với khóa chính tự động tạo
3. ✅ Triển khai entity `Accounts` với khóa chính tạo thủ công
4. ✅ Tạo các interface repository kế thừa `JpaRepository`
5. ✅ Hiểu về các annotation Spring Data JPA và mục đích của chúng
6. ✅ Học về các thao tác CRUD có sẵn thông qua repositories

## Các Bước Tiếp Theo

Trong các bài giảng sắp tới, chúng ta sẽ:
- Triển khai các REST API endpoint để sử dụng các repository này
- Thực hiện demo các thao tác CRUD
- Thêm logic nghiệp vụ trong tầng service
- Xử lý tạo số tài khoản
- Kiểm thử luồng hoàn chỉnh từ API đến cơ sở dữ liệu

## Tài Liệu Tham Khảo Thêm

- [Tài liệu Spring Data JPA](https://spring.io/projects/spring-data-jpa)
- [Tài liệu Lombok](https://projectlombok.org/)
- [Đặc tả JPA](https://jakarta.ee/specifications/persistence/)

---

**Lưu ý**: Để hiểu sâu hơn về framework Spring Data JPA, hãy tham khảo một khóa học Spring toàn diện bao gồm các mẫu repository, phương thức truy vấn và các tính năng JPA nâng cao.


