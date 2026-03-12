# Triển Khai Logic Nghiệp Vụ với Spring Cloud Functions

## Tổng Quan

Hướng dẫn này trình bày cách định nghĩa logic nghiệp vụ sử dụng Spring Cloud Functions trong kiến trúc microservices. Chúng ta sẽ tạo một class `MessageFunctions` xử lý thông báo email và SMS sử dụng các khái niệm lập trình hàm (functional programming).

## Yêu Cầu Tiên Quyết

- Hiểu về Lambda Expressions trong Java 8
- Quen thuộc với Functional Interfaces
- Kiến thức cơ bản về Spring Cloud Functions
- Hiểu về các mẫu giao tiếp bất đồng bộ (asynchronous communication)

## Tạo Class MessageFunctions

### Thiết Lập Logger

Đầu tiên, tạo một class có tên `MessageFunctions` với biến logger để theo dõi việc thực thi function:

```java
public class MessageFunctions {
    private static final Logger log = LoggerFactory.getLogger(MessageFunctions.class);
    
    // Các functions cho logic nghiệp vụ sẽ được định nghĩa tại đây
}
```

## Hiểu Về Function Interface

Interface `Function` từ Java Core Library (`java.util.function`) chấp nhận hai tham số kiểu:
- **T**: Kiểu đầu vào (Input)
- **R**: Kiểu trả về (Output)

Interface này được đánh dấu với annotation `@FunctionalInterface`, nghĩa là nó yêu cầu một lambda expression chấp nhận đầu vào và trả về đầu ra.

## Triển Khai Email Function

### Định Nghĩa Function

Tạo một email function xử lý thông điệp tài khoản:

```java
@Bean
public Function<AccountsMessageDto, AccountsMessageDto> email() {
    return accountsMessageDto -> {
        log.info("Sending email with the details: {}", accountsMessageDto);
        return accountsMessageDto;
    };
}
```

### Các Điểm Chính:
- **Đầu vào**: `AccountsMessageDto` - Nhận thông điệp từ accounts microservice thông qua message broker
- **Đầu ra**: `AccountsMessageDto` - Trả về cùng một object để thực hiện function composition
- **Annotation @Bean**: Đảm bảo Spring Cloud Functions giám sát function này
- **Logic Nghiệp Vụ**: Ghi log thao tác gửi email (việc triển khai gửi email thực tế được bỏ qua để tập trung vào các khái niệm Spring Cloud)

## Triển Khai SMS Function

### Định Nghĩa Function

Tạo một SMS function cũng xử lý thông điệp tài khoản:

```java
@Bean
public Function<AccountsMessageDto, Long> sms() {
    return accountsMessageDto -> {
        log.info("Sending SMS with the details: {}", accountsMessageDto);
        return accountsMessageDto.accountNumber();
    };
}
```

### Các Điểm Chính:
- **Đầu vào**: `AccountsMessageDto` - Nhận dữ liệu từ email function đã được kết hợp
- **Đầu ra**: `Long` - Trả về số tài khoản để thông báo cho accounts microservice
- **Getters của Record Class**: Vì `AccountsMessageDto` là một record class, các phương thức getter không có tiền tố "get". Sử dụng `accountNumber()` trực tiếp thay vì `getAccountNumber()`

## Chiến Lược Function Composition

### Tại Sao Kết Hợp Các Functions?

Kiến trúc triển khai function composition để tạo một pipeline xử lý logic:

1. **Accounts Microservice** → Gửi thông điệp đến message broker
2. **Message Broker** → Gọi function `email`
3. **Email Function** → Xử lý và chuyển tiếp đến function `sms`
4. **SMS Function** → Gửi xác nhận trở lại accounts microservice

### Luồng Dữ Liệu:

```
AccountsMessageDto → [Email Function] → AccountsMessageDto → [SMS Function] → Long (accountNumber)
```

### Tại Sao Trả Về AccountsMessageDto Từ Email Function?

Email function trả về cùng object `AccountsMessageDto` vì:
- SMS function cần tất cả thông tin từ thông điệp gốc
- Function composition yêu cầu các kiểu output/input khớp nhau giữa các functions được kết nối
- Điều này cho phép luồng dữ liệu mượt mà qua pipeline xử lý

### Tại Sao Trả Về Long Từ SMS Function?

SMS function trả về số tài khoản vì:
- Nó báo hiệu việc hoàn thành quy trình thông báo
- Accounts microservice có thể sử dụng điều này để cập nhật database
- Một cột mới có thể theo dõi xem việc giao tiếp đã được gửi thành công hay chưa
- Cho phép xác nhận bất đồng bộ về việc gửi thông điệp

## Các Functional Interfaces Khác

Spring Cloud Functions hỗ trợ thêm các functional interfaces từ `java.util.function`:

### Supplier Interface

```java
@FunctionalInterface
public interface Supplier<T> {
    T get();
}
```

**Trường Hợp Sử Dụng**: Khi bạn cần tạo output mà không cần chấp nhận bất kỳ input nào

### Consumer Interface

```java
@FunctionalInterface
public interface Consumer<T> {
    void accept(T t);
}
```

**Trường Hợp Sử Dụng**: Khi bạn cần chấp nhận input mà không trả về bất kỳ output nào

## Tóm Tắt

Trong triển khai này, chúng ta đã tạo:
1. **Email Function**: Chấp nhận `AccountsMessageDto`, ghi log chi tiết email, trả về `AccountsMessageDto`
2. **SMS Function**: Chấp nhận `AccountsMessageDto`, ghi log chi tiết SMS, trả về `Long` (số tài khoản)
3. **Function Composition**: Email và SMS functions hoạt động như một đơn vị logic duy nhất
4. **Giao Tiếp Bất Đồng Bộ**: Các functions giao tiếp qua message broker cho kiến trúc tách rời

## Các Bước Tiếp Theo

- Kiểm thử các functions với message broker (RabbitMQ)
- Cấu hình Spring Cloud Stream bindings
- Triển khai function composition trong application properties
- Thêm cột database để theo dõi trạng thái giao tiếp

## Những Điểm Chính Cần Nhớ

- Spring Cloud Functions tận dụng các functional interfaces của Java 8
- Các functions có thể được kết hợp để tạo các pipeline xử lý phức tạp
- Annotation `@Bean` là bắt buộc để Spring Cloud Functions giám sát các functions của bạn
- Function composition yêu cầu xem xét cẩn thận các kiểu input/output
- Các functional interfaces khác nhau (Function, Supplier, Consumer) phục vụ các trường hợp sử dụng khác nhau

---

**Lưu Ý**: Triển khai này tập trung vào các khái niệm Spring Cloud Functions. Logic gửi email/SMS thực tế nên được triển khai dựa trên yêu cầu cụ thể và các nhà cung cấp dịch vụ của bạn.