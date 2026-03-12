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