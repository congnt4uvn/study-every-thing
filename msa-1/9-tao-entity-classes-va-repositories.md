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