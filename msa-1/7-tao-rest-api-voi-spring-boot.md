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