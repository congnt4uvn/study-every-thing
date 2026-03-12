# Truyền Sự Kiện từ Message Microservice sang Accounts Microservice

## Tổng Quan

Hướng dẫn này trình bày cách triển khai truyền sự kiện hai chiều giữa các microservices sử dụng Spring Cloud Stream và Spring Cloud Functions. Cụ thể, chúng ta sẽ cấu hình Message microservice để gửi sự kiện đến Accounts microservice.

## Tình Trạng Triển Khai Hiện Tại

Trước đây, chúng ta đã triển khai truyền sự kiện theo một chiều:
- Sự kiện chảy từ Accounts microservice → Message microservice (bước 1-4)

Bây giờ chúng ta cần hoàn thành luồng hai chiều:
- Sự kiện chảy từ Message microservice → Accounts microservice

## Các Bước Cấu Hình

### 1. Cấu Hình Output Binding trong Message Microservice

Trong file `application.yml` của Message microservice, thêm output binding tương tự input binding hiện có:

```yaml
spring:
  cloud:
    stream:
      bindings:
        emailsms-in-0:
          destination: send-communication.message
        emailsms-out-0:
          destination: communication-sent
```

**Các Điểm Chính:**
- Định dạng tên output binding: `{tên-function}-out-0`
- Tiền tố tên function: `emailsms` (khớp với định nghĩa Spring Cloud Function)
- Destination: `communication-sent` (hoạt động như tên exchange trong RabbitMQ)
- Hậu tố `-out-0` chỉ ra output binding với chỉ số bắt đầu từ 0

### 2. Hiểu Về Ưu Điểm Của Spring Cloud Functions

**Không Cần Gửi Message Thủ Công!**

Không giống như Accounts microservice nơi chúng ta sử dụng `StreamBridge`:
```java
streamBridge.send("outputBinding", message);
```

Với Spring Cloud Functions, framework tự động:
- Phát hiện kiểu trả về của function
- Gửi giá trị trả về như một message đến exchange đã cấu hình
- Sử dụng cấu trúc kết hợp function để xác định output binding

Function `sms` trả về `Long` (số tài khoản), được tự động gửi đến exchange `communication-sent`.

## 3. Tạo Consumer Function trong Accounts Microservice

### Bước 3.1: Tạo Package Functions và Class

Tạo package mới: `com.eazybytes.accounts.functions`

Tạo file `AccountsFunctions.java`:

```java
package com.eazybytes.accounts.functions;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import java.util.function.Consumer;

@Configuration
public class AccountsFunctions {
    
    private static final Logger log = LoggerFactory.getLogger(AccountsFunctions.class);
    
    @Bean
    public Consumer<Long> updateCommunication(IAccountService accountService) {
        return accountNumber -> {
            log.info("Đang cập nhật trạng thái giao tiếp cho số tài khoản: {}", accountNumber);
            accountService.updateCommunicationStatus(accountNumber);
        };
    }
}
```

**Tại Sao Sử Dụng Consumer Interface?**
- **Consumer**: Nhận đầu vào, không trả về gì (trường hợp của chúng ta)
- **Supplier**: Không có đầu vào, trả về đầu ra
- **Function**: Nhận đầu vào, trả về đầu ra

### Bước 3.2: Thêm Cột Database

Cập nhật file `schema.sql`:

```sql
CREATE TABLE accounts (
    -- các cột hiện có...
    branch_address VARCHAR(200) NOT NULL,
    communication_switch BOOLEAN,
    -- các cột khác...
);
```

### Bước 3.3: Cập Nhật Entity Class

Thêm vào entity `Accounts`:

```java
@Column(name = "communication_switch")
private Boolean communicationSwitch;
```

### Bước 3.4: Thêm Phương Thức Service

Trong interface `IAccountService`:

```java
Boolean updateCommunicationStatus(Long accountNumber);
```

Trong `AccountServiceImpl`:

```java
@Override
public Boolean updateCommunicationStatus(Long accountNumber) {
    boolean isUpdated = false;
    if (accountNumber != null) {
        Accounts accounts = accountsRepository.findById(accountNumber)
            .orElseThrow(() -> new ResourceNotFoundException("Account", "AccountNumber", accountNumber.toString()));
        accounts.setCommunicationSwitch(true);
        accountsRepository.save(accounts);
        isUpdated = true;
    }
    return isUpdated;
}
```

### Bước 3.5: Cấu Hình Application Properties

Trong file `application.yml` của Accounts microservice:

```yaml
spring:
  cloud:
    function:
      definition: updateCommunication
    stream:
      bindings:
        updateCommunication-in-0:
          destination: communication-sent
          group: accounts
```

**Các Lưu Ý Quan Trọng:**
- Định nghĩa function: `updateCommunication` (khớp với tên bean function)
- Đối với nhiều functions độc lập, phân tách bằng dấu chấm phẩy: `function1;function2`
- Định dạng input binding: `{tên-function}-in-0`
- Tên group ngăn việc tạo hậu tố ngẫu nhiên cho queue

## Kiến Trúc Luồng Message

```
Message Microservice
    ↓ (trả về Long accountNumber từ function sms)
    ↓
RabbitMQ Exchange: communication-sent
    ↓
RabbitMQ Queue: communication-sent.accounts
    ↓
Accounts Microservice (function updateCommunication)
    ↓
Cập nhật communication_switch = true trong database
```

## Các Khái Niệm Chính

### Ưu Điểm Của Spring Cloud Function

1. **Xử Lý Message Tự Động**: Giá trị trả về được tự động gửi đến các destination đã cấu hình
2. **Code Sạch**: Không cần sử dụng StreamBridge thủ công
3. **Dễ Dàng Di Chuyển**: Chuyển đổi liền mạch giữa các nền tảng messaging
4. **Hỗ Trợ Kết Hợp**: Nhiều functions có thể được liên kết bằng ký hiệu pipe

### Quy Ước Đặt Tên Queue

Định dạng: `{destination}.{group}`

Ví dụ: `communication-sent.accounts`

- **Destination**: Từ cấu hình output binding
- **Group**: Ngăn hậu tố ngẫu nhiên, đảm bảo tên queue nhất quán

### Dependency Injection trong Phương Thức @Bean

```java
@Bean
public Consumer<Long> updateCommunication(IAccountService accountService) {
    // accountService được tự động inject - không cần @Autowired
}
```

Spring tự động inject các tham số trong phương thức `@Bean` khi runtime.

## Kiểm Thử

Trong bài giảng tiếp theo, chúng ta sẽ trình diễn:
1. Khởi động cả hai microservices
2. Kích hoạt sự kiện từ Accounts → Message
3. Message microservice xử lý và gửi phản hồi
4. Accounts microservice nhận phản hồi
5. Xác minh cập nhật database

## Tóm Tắt

- Triển khai truyền sự kiện hai chiều giữa các microservices
- Sử dụng Spring Cloud Functions để loại bỏ code boilerplate
- Cấu hình bindings phù hợp trong cả hai microservices
- Tạo Consumer function để xử lý messages đến
- Thêm cột database để theo dõi trạng thái giao tiếp
- Tận dụng việc tạo binding tự động của Spring Cloud Stream

## Thực Hành Tốt Nhất

1. Luôn sử dụng Spring Cloud Functions để có code sạch hơn và dễ bảo trì hơn
2. Khớp tên destination giữa output và input bindings
3. Sử dụng tên group để kiểm soát việc đặt tên queue
4. Chọn functional interface phù hợp (Consumer/Supplier/Function)
5. Để Spring xử lý dependency injection trong phương thức @Bean

## Lợi Ích Của Cách Tiếp Cận Này

- **Giảm Code Boilerplate**: Không cần viết code gửi message thủ công
- **Tính Linh Hoạt Cao**: Dễ dàng chuyển đổi giữa các hệ thống messaging (RabbitMQ, Kafka, etc.)
- **Dễ Bảo Trì**: Code rõ ràng, dễ hiểu và dễ mở rộng
- **Tích Hợp Tốt**: Tích hợp tự nhiên với Spring ecosystem

## Kết Luận

Việc triển khai truyền sự kiện hai chiều giữa microservices sử dụng Spring Cloud Stream và Spring Cloud Functions mang lại nhiều lợi ích về hiệu suất, khả năng bảo trì và tính linh hoạt. Cách tiếp cận này giúp giảm đáng kể lượng code cần viết và duy trì, đồng thời cung cấp một giải pháp mạnh mẽ cho kiến trúc event-driven microservices.