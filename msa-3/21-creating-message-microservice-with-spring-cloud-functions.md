# Tạo Message Microservice với Spring Cloud Functions

## Tổng quan
Hướng dẫn này sẽ giúp bạn tạo một message microservice sử dụng Spring Cloud Functions. Microservice này sẽ xử lý chức năng nhắn tin cho ứng dụng EazyBank, cho phép giao tiếp qua email và SMS.

## Yêu cầu tiên quyết
- Java 17
- Maven
- Spring Boot 3.1.2 (hoặc phiên bản ổn định mới nhất)
- IntelliJ IDEA

## Bước 1: Tạo khung dự án

### Sử dụng Spring Initializr
1. Truy cập vào [start.spring.io](https://start.spring.io)
2. Cấu hình dự án với các thiết lập sau:
   - **Project**: Maven
   - **Language**: Java
   - **Spring Boot Version**: 3.1.2 (hoặc phiên bản ổn định hiện tại)
   
### Metadata dự án
- **Group**: `com.easybytes`
- **Artifact**: `message`
- **Name**: `message`
- **Description**: Microservice hỗ trợ messaging trong EazyBank
- **Package Name**: `com.easybytes.message` (tự động điền)
- **Packaging**: JAR
- **Java Version**: 17

## Bước 2: Thêm Dependencies

### Spring Cloud Function Dependency
Tìm kiếm "function" trong phần dependencies và thêm **Spring Cloud Function**.

**Spring Cloud Function là gì?**
- Hỗ trợ triển khai business logic thông qua functions
- Hỗ trợ mô hình lập trình thống nhất trên các nhà cung cấp serverless
- Khả năng chạy độc lập (standalone), local hoặc trên PaaS
- Triết lý viết một lần, triển khai mọi nơi

### Dependencies được bao gồm
Khi bạn click "Explore", bạn sẽ thấy:
- `spring-boot-starter`
- `spring-cloud-function-context` (dependency quan trọng)
- Các dependencies cho testing

### Tải xuống dự án
Click nút "Download" để tải xuống Maven project có tên "message".

## Bước 3: Thiết lập Workspace

### Tổ chức cấu trúc dự án
1. Tạo một thư mục mới cho phần phát triển Section 13
2. Sao chép thư mục Section 12 (chứa code phần trước)
3. Đổi tên thành `section13`
4. Xóa thư mục `.idea`
5. Giải nén và dán dự án message đã tải xuống vào section13

### Mở trong IntelliJ IDEA
1. Click nút **Open**
2. Điều hướng đến: `storage/workspaces/microservices/section13`
3. Click **Open**
4. Load tất cả các Maven projects

## Bước 4: Tạo DTO Package và Record Class

### Tạo DTO Package
Điều hướng đến thư mục source của messages microservice và tạo:
```
com.eazybytes.message.dto
```

Package này sẽ chứa các class để nhận messages từ message broker.

### Tạo AccountsMessageDto Record

**Tại sao sử dụng Record?**
Java records cung cấp:
- Tự động tạo getter
- Các trường bất biến (final mặc định)
- Cú pháp ngắn gọn
- Đảm bảo an toàn luồng (thread-safe) cho data carriers

**Định nghĩa Record:**
Tạo record `AccountsMessageDto` với các trường sau:
- `accountNumber` - Số tài khoản khách hàng
- `name` - Tên khách hàng
- `email` - Địa chỉ email (để gửi email)
- `mobileNumber` - Số điện thoại (để gửi SMS)

**Luồng dữ liệu:**
Accounts microservice gửi messages đến message broker theo định dạng DTO này, message service sẽ nhận và xử lý.

**Best Practice:**
Thêm Javadoc comments để giải quyết warnings và tài liệu hóa code đúng cách.

## Bước 5: Tạo Functions Package

### Tạo Functions Package
Tạo một package mới trong `com.eazybytes.message`:
```
com.eazybytes.message.functions
```

Package này sẽ chứa tất cả các functions cần thiết cho business logic.

### Tạo MessageFunctions Class
1. Tạo một class mới: `MessageFunctions`
2. Thêm annotation `@Configuration` lên trên class
3. Class này sẽ xử lý tất cả các thao tác messaging đến người dùng cuối

## Bước 6: Triển khai Business Logic

Trong bài giảng tiếp theo, chúng ta sẽ tiếp tục triển khai business logic sử dụng Spring Cloud Functions.

## Các khái niệm chính

### Lợi ích của Spring Cloud Function
- **Sẵn sàng Serverless**: Triển khai lên AWS Lambda, Azure Functions, Google Cloud Functions
- **Độc lập nền tảng**: Cùng một đoạn code hoạt động trên nhiều cloud providers khác nhau
- **Chạy độc lập**: Có thể chạy như một ứng dụng Spring Boot thông thường
- **Triển khai linh hoạt**: Phát triển local, PaaS, hoặc serverless

### Mục đích của Message Microservice
- Xử lý giao tiếp với khách hàng
- Gửi thông báo qua email
- Gửi thông báo qua SMS
- Xử lý messages từ accounts microservice thông qua message broker

## Tóm tắt
Trong hướng dẫn này, chúng ta đã:
1. Tạo dự án Spring Boot với Spring Cloud Function dependency
2. Thiết lập workspace và cấu trúc dự án
3. Tạo DTO record class để nhận messages
4. Chuẩn bị functions package cho việc triển khai business logic

## Các bước tiếp theo
- Triển khai business logic dựa trên functions
- Cấu hình tích hợp message broker
- Thiết lập khả năng gửi email và SMS
- Kiểm thử message microservice

---

**Lưu ý**: Đây là phần thiết lập nền tảng. Việc triển khai thực tế các messaging functions sẽ được đề cập trong các bài giảng tiếp theo.