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