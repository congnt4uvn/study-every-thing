# Cấu Hình Phân Quyền Dựa Trên Role Trong Spring Cloud Gateway

## Tổng Quan

Hướng dẫn này trình bày cách triển khai phân quyền dựa trên role trong Spring Cloud Gateway khi sử dụng OAuth2 với Keycloak làm máy chủ ủy quyền. Chúng ta sẽ vượt qua việc chỉ kiểm tra xác thực đơn giản để thực thi phân quyền dựa trên các role của client.

## Từ Xác Thực Đến Phân Quyền

### Trạng Thái Hiện Tại
Hiện tại, gateway chỉ kiểm tra xem ứng dụng client đã được **xác thực** (authenticated) hay chưa, nhưng không kiểm tra **phân quyền** (authorization) cụ thể (roles hoặc privileges).

### Tại Sao Phân Quyền Quan Trọng
Trong các tình huống thực tế, bạn thường cần xử lý yêu cầu chỉ khi ứng dụng client có các role hoặc quyền cụ thể được gán.

## Triển Khai Kiểm Soát Truy Cập Dựa Trên Role

### Bước 1: Cấu Hình Yêu Cầu Role Trong Gateway

Thay vì sử dụng `.authenticated()`, hãy dùng phương thức `.hasRole()` để chỉ định các role cần thiết:

```java
// Cho các API liên quan đến accounts
.hasRole("ACCOUNTS")

// Cho các API liên quan đến cards
.hasRole("CARDS")

// Cho các API liên quan đến loans
.hasRole("LOANS")
```

Điều này thực thi phân quyền ở cấp độ gateway, đảm bảo chỉ các client có role phù hợp mới có thể truy cập các microservice cụ thể.

## Cấu Hình Roles Trong Keycloak

### Bước 2: Tạo Realm Roles

1. Điều hướng đến **Keycloak Admin Console**
2. Vào **Realm roles**
3. Nhấp **Create role**
4. Tạo roles:
   - Tên role: `ACCOUNTS`
   - Mô tả: "Accounts Role"
   - Nhấp **Save**

**Lưu ý**: Ban đầu chỉ tạo role ACCOUNTS cho mục đích kiểm thử. Các role Cards và Loans sẽ được thêm sau khi kiểm thử negative.

### Bước 3: Gán Roles Cho Service Account

Đối với loại cấp quyền client credentials (machine-to-machine), roles phải được gán trong **Service account roles**, không phải roles thông thường:

1. Vào **Clients** → Chọn client của bạn (ví dụ: `eazybank-callcenter-cc`)
2. Điều hướng đến tab **Service account roles**
3. Nhấp **Assign Role**
4. Chọn role `ACCOUNTS`
5. Nhấp **Assign**

## Hiểu Cấu Trúc JWT Token

### Thông Tin Role Trong Access Token

Sau khi lấy access token mới, kiểm tra nó tại [jwt.io](https://jwt.io). Thông tin role xuất hiện trong payload:

```json
{
  "realm_access": {
    "roles": [
      "ACCOUNTS",
      "default-roles-keycloak",
      "offline_access",
      "uma_authorization"
    ]
  }
}
```

Mảng `realm_access.roles` chứa:
- **Custom roles**: `ACCOUNTS` (role chúng ta cấu hình)
- **Default roles**: Các role chuẩn của Keycloak

## Tạo Custom Role Converter

### Bước 4: Triển Khai KeycloakRoleConverter

Spring Security cần trích xuất thông tin role từ JWT và chuyển đổi sang định dạng `GrantedAuthority`.

Tạo file `KeycloakRoleConverter.java`:

```java
public class KeycloakRoleConverter implements Converter<Jwt, Collection<GrantedAuthority>> {
    
    @Override
    public Collection<GrantedAuthority> convert(Jwt jwt) {
        Map<String, Object> realmAccess = (Map<String, Object>) jwt.getClaims().get("realm_access");
        
        if (realmAccess == null || realmAccess.isEmpty()) {
            return Collections.emptyList();
        }
        
        Collection<String> roles = (Collection<String>) realmAccess.get("roles");
        
        return roles.stream()
            .map(role -> "ROLE_" + role)
            .map(SimpleGrantedAuthority::new)
            .collect(Collectors.toList());
    }
}
```

### Hiểu Logic Chuyển Đổi

1. **Trích xuất Claims**: `jwt.getClaims()` lấy dữ liệu payload
2. **Lấy Realm Access**: Truy cập key `realm_access` chứa một map
3. **Trích xuất Roles**: Lấy mảng `roles` từ map realm_access
4. **Thêm Prefix**: Thêm tiền tố `ROLE_` cho mỗi tên role (yêu cầu của Spring Security)
5. **Chuyển đổi sang GrantedAuthority**: Tạo đối tượng `SimpleGrantedAuthority` cho mỗi role

### Tại Sao Cần Tiền Tố ROLE_?

Khi sử dụng `.hasRole("USER")` trong cấu hình Spring Security, framework tự động chuyển đổi thành `ROLE_USER`. Do đó:
- **Trong Converter**: Thêm tiền tố `ROLE_`
- **Trong Security Config**: Dùng tên role không có tiền tố (framework tự động thêm)

## Tích Hợp Converter Với Cấu Hình Security

### Bước 5: Cấu Hình JWT Authentication Converter

Thêm phương thức để tạo granted authorities extractor:

```java
private Converter<Jwt, Mono<AbstractAuthenticationToken>> grantedAuthoritiesExtractor() {
    JwtAuthenticationConverter jwtAuthenticationConverter = new JwtAuthenticationConverter();
    jwtAuthenticationConverter.setJwtGrantedAuthoritiesConverter(new KeycloakRoleConverter());
    return new ReactiveJwtAuthenticationConverterAdapter(jwtAuthenticationConverter);
}
```

### Bước 6: Cập Nhật Cấu Hình Security

Thay thế cấu hình JWT mặc định:

**Trước:**
```java
.jwt(Customizer.withDefaults())
```

**Sau:**
```java
.jwt(jwtSpec -> jwtSpec
    .jwtAuthenticationConverter(grantedAuthoritiesExtractor()))
```

Điều này thiết lập liên kết giữa `KeycloakRoleConverter` tùy chỉnh của bạn và cấu hình Spring Security.

## Tóm Tắt

Bằng cách triển khai phân quyền dựa trên role, bạn đã nâng cao bảo mật microservices:

1. ✅ Cấu hình yêu cầu role trong gateway
2. ✅ Tạo và gán roles trong Keycloak
3. ✅ Triển khai custom JWT role converter
4. ✅ Tích hợp converter với cấu hình Spring Security

Gateway giờ đây kiểm tra cả **xác thực** (bạn là ai) và **phân quyền** (bạn có thể truy cập gì) trước khi định tuyến yêu cầu đến các microservice.

## Các Bước Tiếp Theo

- Build dự án
- Kiểm thử phân quyền với các role khác nhau
- Triển khai negative testing
- Thêm roles CARDS và LOANS
- Kiểm thử hoàn chỉnh kiểm soát truy cập dựa trên role

---

**Các Chủ Đề Liên Quan:**
- OAuth2 Client Credentials Grant Flow
- Spring Security Authorization
- Keycloak Service Account Roles
- Cấu Trúc JWT Token