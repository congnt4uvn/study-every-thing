# Cấu Hình Gateway Server Như OAuth2 Resource Server

## Tổng Quan

Hướng dẫn này trình bày cách chuyển đổi Spring Cloud Gateway server thành OAuth2 resource server, cho phép nó xác thực JWT access token được cấp bởi Keycloak authorization server.

## Yêu Cầu Trước

- Keycloak authorization server đã được thiết lập và đang chạy
- Thông tin client credentials đã được cấu hình trong auth server
- Ứng dụng Spring Cloud Gateway (từ Section 11)

## Các Bước Thực Hiện

### 1. Thiết Lập Dự Án

Tạo folder section mới bằng cách sao chép implementation trước đó:

```bash
# Sao chép Section 11 sang Section 12
# Xóa các file ẩn (.idea, etc.)
```

Mở project trong IntelliJ IDEA và bật annotation processing khi được nhắc.

### 2. Thêm Maven Dependencies

Thêm ba dependencies liên quan đến security vào file `pom.xml` của Gateway server:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
</dependency>

<dependency>
    <groupId>org.springframework.security</groupId>
    <artifactId>spring-security-oauth2-resource-server</artifactId>
</dependency>

<dependency>
    <groupId>org.springframework.security</groupId>
    <artifactId>spring-security-oauth2-jose</artifactId>
</dependency>
```

**Mục Đích Của Các Dependencies:**
- `spring-boot-starter-security`: Thêm Spring Security framework
- `spring-security-oauth2-resource-server`: Chuyển đổi gateway thành OAuth2 resource server
- `spring-security-oauth2-jose`: Cung cấp hỗ trợ xử lý JWT token

Tải lại Maven changes để download tất cả các thư viện cần thiết.

### 3. Tạo Cấu Hình Security

Tạo package mới: `com.eazybytes.gatewayserver.config`

Tạo class mới `SecurityConfig.java`:

```java
package com.eazybytes.gatewayserver.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.reactive.EnableWebFluxSecurity;
import org.springframework.security.config.web.server.ServerHttpSecurity;
import org.springframework.security.web.server.SecurityWebFilterChain;

@Configuration
@EnableWebFluxSecurity
public class SecurityConfig {

    @Bean
    public SecurityWebFilterChain springSecurityFilterChain(ServerHttpSecurity serverHttpSecurity) {
        serverHttpSecurity
            .authorizeExchange(exchanges -> exchanges
                .pathMatchers(HttpMethod.GET).permitAll()
                .pathMatchers("/easybank/accounts/**").authenticated()
                .pathMatchers("/easybank/cards/**").authenticated()
                .pathMatchers("/easybank/loans/**").authenticated()
            )
            .oauth2ResourceServer(oAuth2ResourceServerSpec -> 
                oAuth2ResourceServerSpec.jwt(Customizer.withDefaults())
            )
            .csrf(csrfSpec -> csrfSpec.disable());
        
        return serverHttpSecurity.build();
    }
}
```

**Các Điểm Chính:**

- **@Configuration**: Báo cho Spring tạo các bean từ class này trong quá trình khởi động
- **@EnableWebFluxSecurity**: Bắt buộc cho Spring Cloud Gateway (reactive framework). Sử dụng `@EnableWebSecurity` cho ứng dụng Spring Boot web thông thường
- **authorizeExchange()**: Cấu hình các quy tắc phân quyền request
- **pathMatchers()**: Định nghĩa các quy tắc security cho các API path cụ thể
- **permitAll()**: Cho phép truy cập không cần xác thực (cho các phương thức GET)
- **authenticated()**: Yêu cầu xác thực cho các path được chỉ định
- **oauth2ResourceServer()**: Chuyển đổi gateway thành OAuth2 resource server
- **jwt()**: Kích hoạt xác thực JWT token với cài đặt mặc định
- **csrf().disable()**: Vô hiệu hóa bảo vệ CSRF (không cần thiết khi không có browser tham gia)

### 4. Cấu Hình Resource Server Properties

Thêm cấu hình sau vào file `application.yml`:

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          jwk-set-uri: http://localhost:7080/realms/master/protocol/openid-connect/certs
```

**Mục Đích:**
- Resource server tải xuống public certificate từ Keycloak trong quá trình khởi động
- Public certificate này được sử dụng để xác thực JWT access token
- Resource server có thể xác minh xem token có được Keycloak cấp hợp lệ hay không
- Public certificate chỉ có thể xác thực token nhưng không thể tạo token mới (chỉ private certificate của Keycloak mới có thể tạo token)

## Giải Thích Các Quy Tắc Security

Cấu hình triển khai mô hình security như sau:

1. **Tất cả GET requests**: Được phép không cần xác thực (truy cập chỉ đọc)
2. **POST/PUT/DELETE requests** đến `/easybank/accounts/**`, `/easybank/cards/**`, `/easybank/loans/**`: Yêu cầu xác thực

**Độ Ưu Tiên**: Các cấu hình được đánh giá từ trên xuống dưới, do đó GET request có độ ưu tiên đầu tiên và luôn được cho phép, ngay cả trên các path yêu cầu xác thực.

## Cách Hoạt Động Của Token Validation

1. Client gửi access token trong request đến Gateway
2. Gateway (resource server) xác thực token sử dụng public certificate từ Keycloak
3. Nếu hợp lệ, request được xử lý; nếu không hợp lệ, request bị từ chối
4. Public certificate được tải xuống lúc khởi động từ endpoint `jwk-set-uri`

## Tóm Tắt

Ba thay đổi chính đã được thực hiện:
1. Thêm ba Maven dependencies cho OAuth2 và hỗ trợ JWT
2. Tạo class `SecurityConfig` với các quy tắc security
3. Cấu hình `jwk-set-uri` trong `application.yml` để xác thực token

Gateway server hiện hoạt động như OAuth2 resource server trong luồng client credentials grant flow.

## Các Bước Tiếp Theo

- Build project
- Test cấu hình security
- Xác minh token validation hoạt động như mong đợi

## Tài Nguyên Bổ Sung

- Để biết thêm chi tiết về bảo vệ CSRF, tham khảo tài liệu Spring Security
- Cân nhắc tham gia khóa học Spring Security toàn diện để hiểu sâu hơn