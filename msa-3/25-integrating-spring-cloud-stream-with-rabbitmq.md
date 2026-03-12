# Tích hợp Spring Cloud Stream với RabbitMQ trong Microservices

## Tổng quan

Hướng dẫn này trình bày cách tích hợp Spring Cloud Stream với RabbitMQ để kích hoạt giao tiếp theo mô hình sự kiện giữa các microservices. Chúng ta sẽ cấu hình hai microservices:
- **Message Microservice**: Nhận và xử lý tin nhắn từ RabbitMQ
- **Accounts Microservice**: Gửi tin nhắn đến RabbitMQ khi tài khoản mới được tạo

## Yêu cầu

- Microservices Spring Boot
- RabbitMQ message broker
- Hiểu biết cơ bản về kiến trúc hướng sự kiện

## Bước 1: Cấu hình Message Microservice

### 1.1 Cập nhật Dependencies

Đầu tiên, dừng message microservice đang chạy và cập nhật file `pom.xml`.

**Xóa dependency cũ:**
```xml
<!-- Xóa spring-cloud-function-context -->
```

**Thêm Spring Cloud Stream dependencies:**
```xml
<dependencies>
    <!-- Dependency chính của Spring Cloud Stream -->
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-stream</artifactId>
    </dependency>
    
    <!-- RabbitMQ binder cho Spring Cloud Stream -->
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-stream-binder-rabbit</artifactId>
    </dependency>
    
    <!-- Dependencies cho testing -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>
    
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-stream-test-binder</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
```

**Lưu ý:** Spring Cloud Stream đã bao gồm các dependencies của Spring Cloud Function, nên chúng ta không cần thêm riêng.

### 1.2 Thêm Google Jib Plugin

Thêm Google Jib plugin để tạo Docker images:

```xml
<build>
    <plugins>
        <plugin>
            <groupId>com.google.cloud.tools</groupId>
            <artifactId>jib-maven-plugin</artifactId>
            <configuration>
                <to>
                    <image>eazybytes/${project.artifactId}:S13</image>
                </to>
            </configuration>
        </plugin>
    </plugins>
</build>
```

### 1.3 Cấu hình application.yml

Thêm các thuộc tính sau vào `application.yml`:

```yaml
spring:
  cloud:
    function:
      definition: emailsms
    stream:
      bindings:
        emailsms-in-0:
          destination: send-communication
          group: ${spring.application.name}
  rabbitmq:
    host: localhost
    port: 5672
    username: guest
    password: guest
    connection-timeout: 10s
```

**Giải thích cấu hình:**

- **Tên Binding (`emailsms-in-0`)**: Quy ước đặt tên mặc định của Spring Cloud Stream
  - `emailsms`: Tên function
  - `in`: Input binding (đầu vào)
  - `0`: Chỉ số bắt đầu
  
- **Destination**: Tên queue trong RabbitMQ (`send-communication`)
  - Input bindings kết nối với **queues**
  - Function sẽ tiêu thụ tin nhắn từ queue này

- **Group**: Sử dụng tên application để tránh tên queue được tạo ngẫu nhiên

- **RabbitMQ Connection**: Chi tiết kết nối chuẩn cho RabbitMQ local

## Bước 2: Cấu hình Accounts Microservice

### 2.1 Cập nhật Dependencies

Mở `pom.xml` trong accounts microservice và thêm:

```xml
<dependencies>
    <!-- Spring Cloud Stream -->
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-stream</artifactId>
    </dependency>
    
    <!-- RabbitMQ Binder -->
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-stream-binder-rabbit</artifactId>
    </dependency>
</dependencies>
```

Cập nhật tag Docker image trong cấu hình Jib plugin:
```xml
<image>eazybytes/${project.artifactId}:S13</image>
```

### 2.2 Tạo AccountsMessageDto Record Class

Tạo record class mới trong package `dto`:

```java
package com.eazybank.accounts.dto;

public record AccountsMessageDto(
    Long accountNumber,
    String name,
    String email,
    String mobileNumber
) {}
```

### 2.3 Cấu hình application.yml

Thêm các thuộc tính sau:

```yaml
spring:
  cloud:
    stream:
      bindings:
        sendCommunication-out-0:
          destination: send-communication
  rabbitmq:
    host: localhost
    port: 5672
    username: guest
    password: guest
    connection-timeout: 10s
```

**Giải thích cấu hình:**

- **Tên Binding (`sendCommunication-out-0`)**: 
  - `sendCommunication`: Tên binding tùy chỉnh
  - `out`: Output binding (đầu ra)
  - `0`: Chỉ số

- **Destination**: Tên exchange trong RabbitMQ (`send-communication`)
  - Output bindings kết nối với **exchanges**
  - Tin nhắn gửi đến binding này sẽ được publish lên exchange

### 2.4 Triển khai Logic Gửi Tin nhắn

Cập nhật class `AccountServiceImpl`:

```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.cloud.stream.function.StreamBridge;
import lombok.AllArgsConstructor;

@Service
@AllArgsConstructor
public class AccountServiceImpl implements IAccountService {
    
    private static final Logger log = LoggerFactory.getLogger(AccountServiceImpl.class);
    
    private AccountRepository accountRepository;
    private CustomerRepository customerRepository;
    private StreamBridge streamBridge;
    
    @Override
    public void createAccount(CustomerDto customerDto) {
        Customer customer = CustomerMapper.mapToCustomer(customerDto, new Customer());
        Customer savedCustomer = customerRepository.save(customer);
        
        Account account = createNewAccount(savedCustomer);
        Account savedAccount = accountRepository.save(account);
        
        // Gửi tin nhắn thông báo
        sendCommunication(savedAccount, savedCustomer);
    }
    
    private void sendCommunication(Account account, Customer customer) {
        AccountsMessageDto accountsMessageDto = new AccountsMessageDto(
            account.getAccountNumber(),
            customer.getName(),
            customer.getEmail(),
            customer.getMobileNumber()
        );
        
        log.info("Đang gửi yêu cầu thông báo cho chi tiết: {}", accountsMessageDto);
        
        boolean result = streamBridge.send("sendCommunication-out-0", accountsMessageDto);
        
        log.info("Yêu cầu thông báo có được xử lý thành công không?: {}", result);
    }
}
```

**Chi tiết triển khai:**

1. **StreamBridge**: Bean được inject từ Spring Cloud Stream để gửi tin nhắn
2. **Phương thức send()**: 
   - Tham số đầu: Tên output binding (`sendCommunication-out-0`)
   - Tham số thứ hai: Object tin nhắn (`AccountsMessageDto`)
3. **Giá trị trả về**: Boolean cho biết tin nhắn có được gửi thành công đến RabbitMQ
4. **Logging**: Theo dõi quá trình gửi tin nhắn để debug

## Kiến trúc Luồng Tin nhắn

```
Accounts Microservice
    |
    | (tạo tài khoản)
    v
Phương thức sendCommunication()
    |
    | (StreamBridge.send())
    v
RabbitMQ Exchange (send-communication)
    |
    | (định tuyến tin nhắn)
    v
RabbitMQ Queue (send-communication)
    |
    | (tiêu thụ tin nhắn)
    v
Message Microservice (hàm emailsms)
```

## Khái niệm chính

### Input vs Output Bindings

- **Input Bindings** (`-in-`): 
  - Tiêu thụ tin nhắn từ **queues**
  - Sử dụng trong message microservice
  - Kết nối functions với nguồn tin nhắn

- **Output Bindings** (`-out-`): 
  - Publish tin nhắn lên **exchanges**
  - Sử dụng trong accounts microservice
  - Gửi tin nhắn đến RabbitMQ

### Ánh xạ Destination

- **Queue Destination**: Sử dụng với input bindings (consumers)
- **Exchange Destination**: Sử dụng với output bindings (producers)

### Thuộc tính Group

- Đảm bảo đặt tên queue nhất quán
- Ngăn RabbitMQ thêm giá trị ngẫu nhiên vào tên queue
- Sử dụng tên application để tổ chức

## Kiểm thử Tích hợp

1. **Khởi động RabbitMQ**: Đảm bảo RabbitMQ đang chạy trên `localhost:5672`
2. **Khởi động Message Microservice**: Sẽ tạo queue và bắt đầu tiêu thụ
3. **Khởi động Accounts Microservice**: Sẵn sàng gửi tin nhắn
4. **Tạo Tài khoản Mới**: Kích hoạt tạo tài khoản qua REST API
5. **Xác minh**: Kiểm tra console RabbitMQ để theo dõi luồng tin nhắn và logs để xử lý

## Tổng kết

Chúng ta đã tích hợp thành công Spring Cloud Stream với RabbitMQ trong microservices:

- ✅ Đã thêm Spring Cloud Stream và RabbitMQ binder dependencies
- ✅ Đã cấu hình input bindings trong message microservice (consumer)
- ✅ Đã cấu hình output bindings trong accounts microservice (producer)
- ✅ Đã triển khai logic gửi tin nhắn với StreamBridge
- ✅ Đã thiết lập thuộc tính kết nối RabbitMQ
- ✅ Đã tạo giao tiếp hướng sự kiện giữa các microservices

Các microservices hiện đã sẵn sàng cho giao tiếp hướng sự kiện thông qua RabbitMQ!