# Triển Khai OpenFeign Client Để Giao Tiếp Giữa Các Microservice

## Tổng Quan

Hướng dẫn này trình bày cách triển khai OpenFeign client trong kiến trúc microservices sử dụng Spring Boot để cho phép giao tiếp nội bộ giữa các microservice thông qua Eureka Server để khám phá dịch vụ.

## Kịch Bản

Chúng ta sẽ xây dựng một REST API mới trong **microservice accounts** với các chức năng:
- Thu thập thông tin liên quan đến tài khoản
- Lấy thông tin khoản vay từ microservice loans
- Lấy thông tin thẻ từ microservice cards
- Tổng hợp tất cả các phản hồi dựa trên số điện thoại di động
- Trả về dữ liệu khách hàng đầy đủ cho client

Microservice accounts cần giao tiếp nội bộ với các microservice cards và loans để lấy dữ liệu mà nó không có.

## Yêu Cầu Trước

- Eureka Server đang chạy
- Các microservice Accounts, Loans và Cards đã đăng ký với Eureka
- Cấu trúc dự án Maven

## Các Bước Triển Khai

### 1. Thêm Dependency OpenFeign

Truy cập [start.spring.io](https://start.spring.io) và thực hiện:
1. Chọn Maven làm công cụ build
2. Nhấp vào "Add dependency"
3. Tìm kiếm "OpenFeign"
4. Chọn dự án starter OpenFeign
5. Nhấp "Explore" và sao chép chi tiết dependency

Thêm dependency vào file `pom.xml` của microservice accounts (sau dependency Netflix Eureka Client):

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-openfeign</artifactId>
</dependency>
```

Nhấp "Load Maven changes" để tải xuống các thư viện OpenFeign.

### 2. Kích Hoạt Feign Clients

Mở class Spring Boot chính (`AccountsApplication`) và thêm annotation `@EnableFeignClients`:

```java
@EnableFeignClients
@SpringBootApplication
public class AccountsApplication {
    // code hiện có
}
```

Annotation này kích hoạt chức năng Feign client, cho phép microservice accounts kết nối với các microservice khác.

### 3. So Sánh OpenFeign Với Cách Tiếp Cận Truyền Thống

**Cách Tiếp Cận Truyền Thống (REST Template/Web Client):**
- Yêu cầu viết code triển khai
- Xử lý thủ công URL, số cổng, dữ liệu request
- Logic xử lý exception tùy chỉnh

**Cách Tiếp Cận OpenFeign:**
- Chỉ cần code khai báo (tương tự Spring Data JPA)
- Không cần code triển khai
- Chỉ định nghĩa interface với các phương thức trừu tượng
- Framework tự động tạo implementation khi chạy

### 4. Tạo Các DTO

Sao chép các DTO cần thiết từ các microservice cards và loans:

**Từ Microservice Cards:**
- Sao chép class `CardsDto` vào package `com.eazybytes.accounts.dto`

**Từ Microservice Loans:**
- Sao chép class `LoansDto` vào package `com.eazybytes.accounts.dto`

### 5. Tạo Interface CardsFeignClient

Tạo package mới: `com.eazybytes.accounts.service.client`

Tạo interface `CardsFeignClient`:

```java
package com.eazybytes.accounts.service.client;

import com.eazybytes.accounts.dto.CardsDto;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

@FeignClient(value = "cards")
public interface CardsFeignClient {
    
    @GetMapping(value = "/api/fetch", consumes = "application/json")
    CardsDto fetchCardDetails(@RequestParam String mobileNumber);
}
```

**Các Điểm Quan Trọng:**
- `@FeignClient(value = "cards")` - Sử dụng tên logic mà microservice cards đăng ký với Eureka Server
- Signature của phương thức phải khớp với REST API thực tế trong CardsController
- Không cần code triển khai - chỉ khai báo phương thức trừu tượng
- Bao gồm đường dẫn REST API đầy đủ (ví dụ: `/api/fetch`)

### 6. Tạo Interface LoansFeignClient

Tạo interface `LoansFeignClient` trong cùng package:

```java
package com.eazybytes.accounts.service.client;

import com.eazybytes.accounts.dto.LoansDto;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

@FeignClient(value = "loans")
public interface LoansFeignClient {
    
    @GetMapping(value = "/api/fetch", consumes = "application/json")
    LoansDto fetchLoanDetails(@RequestParam String mobileNumber);
}
```

**Các Điểm Quan Trọng:**
- `@FeignClient(value = "loans")` - Sử dụng tên logic cho microservice loans
- Signature của phương thức khớp với fetch API trong LoansController
- Kiểu trả về là `LoansDto`
- Tham số request là `mobileNumber`

## Cách Hoạt Động

### Quy Trình Khám Phá Dịch Vụ

1. **Đăng Ký**: Các microservice cards và loans đăng ký với Eureka Server sử dụng tên logic ("cards" và "loans")

2. **Khám Phá**: Khi chạy, Feign client kết nối với Eureka Server và lấy chi tiết instance cho tên logic được chỉ định

3. **Lưu Cache**: Chi tiết instance được lưu cache trong 30 giây (thời gian mặc định)

4. **Cân Bằng Tải**: Trong khoảng thời gian cache 30 giây, Feign client sử dụng chi tiết IP đã lưu mà không kết nối lại với Eureka Server

5. **Gọi API**: Feign client gọi API đích với các tham số request được chỉ định

### Bên Trong Hoạt Động

OpenFeign tự động xử lý:
- Tạo code triển khai khi chạy
- Kết nối với Eureka Server để khám phá dịch vụ
- Phân giải địa chỉ IP của instance
- Serialization request/response
- Xử lý lỗi

## Yêu Cầu Cho Interface Feign Client

Khi tạo các interface Feign client, đảm bảo:

1. **Khớp Signature Phương Thức**: Tham số đầu vào, kiểu trả về và phương thức HTTP phải khớp với REST API thực tế
2. **Tên Logic**: Sử dụng cùng tên mà microservice đích dùng để đăng ký với Eureka
3. **Đường Dẫn Đầy Đủ**: Bao gồm toàn bộ đường dẫn REST API (cấp controller + cấp phương thức)
4. **Annotations**: Đánh dấu đúng với `@FeignClient`, `@GetMapping`/`@PostMapping`, v.v.
5. **Không Có Implementation**: Chỉ code khai báo - không có logic nghiệp vụ

## Lợi Ích Của OpenFeign

- **Phong Cách Khai Báo**: Tương tự Spring Data JPA - định nghĩa interface, không phải implementation
- **Giao Tiếp Đơn Giản**: Không cần quản lý REST template hoặc web client
- **Cân Bằng Tải Tích Hợp**: Cân bằng tải phía client thông qua tích hợp Eureka
- **Khám Phá Dịch Vụ Tự Động**: Tích hợp liền mạch với Eureka Server
- **Ít Code Boilerplate**: Code tối thiểu so với cách tiếp cận truyền thống

## Các Bước Tiếp Theo

Trong giai đoạn tiếp theo, bạn sẽ:
- Triển khai REST API mới trong microservice accounts
- Sử dụng Feign client để lấy dữ liệu từ các microservice cards và loans
- Tổng hợp các phản hồi và trả về thông tin khách hàng đầy đủ

## Tóm Tắt

OpenFeign cung cấp cách tiếp cận khai báo cho giao tiếp microservice, loại bỏ nhu cầu triển khai REST client thủ công. Bằng cách định nghĩa các interface với annotation và signature phương thức phù hợp, framework tự động tạo tất cả code triển khai cần thiết khi chạy, tích hợp liền mạch với Eureka Server để khám phá dịch vụ và cân bằng tải phía client.