# Cấu Hình Bên Ngoài Cho Spring Boot

## Thách Thức Với Profile Được Hardcode

### Vấn Đề Hiện Tại

Khi kích hoạt profile bằng cách hardcode giá trị trong `application.yml`:

```yaml
spring:
  profiles:
    active: qa
```

**Nhược Điểm:**
- Yêu cầu rebuild Docker image cho mỗi môi trường
- Yêu cầu tạo lại package ứng dụng web
- Vi phạm **phương pháp 12-Factor App**
- Code không immutable giữa các môi trường
- Tăng độ phức tạp và thời gian triển khai

### Giải Pháp

Spring Boot cung cấp nhiều cách để **externalize cấu hình** và kích hoạt profile từ nguồn bên ngoài mà không cần sửa đổi code.

## Các Phương Pháp Cấu Hình Bên Ngoài

Spring Boot hỗ trợ nhiều phương pháp để externalize cấu hình, mỗi phương pháp có mức độ ưu tiên khác nhau.

### Thứ Tự Ưu Tiên Cấu Hình (Cao Xuống Thấp)

1. **Command Line Arguments** - Ưu Tiên Cao Nhất
2. **JVM System Properties** - Ưu Tiên Trung Bình
3. **Environment Variables** - Ưu Tiên Tiêu Chuẩn
4. **Profile-Specific Properties** (`application-{profile}.yml`)
5. **Default Properties** (`application.yml`) - Ưu Tiên Thấp Nhất

## 1. Command Line Arguments (Tham Số Dòng Lệnh)

### Tổng Quan

Command line arguments cung cấp **ưu tiên cao nhất** cho cấu hình. Spring Boot tự động chuyển đổi command line arguments thành các cặp key-value và thêm chúng vào environment object.

### Đặc Điểm

- **Ưu tiên cao nhất** - Ghi đè tất cả các nguồn cấu hình khác
- **Hiệu lực ngay lập tức** - Không cần thay đổi code
- **Linh hoạt** - Truyền bất kỳ thuộc tính nào một cách động
- **Minh bạch** - Dễ dàng xem giá trị nào đang được sử dụng

### Cú Pháp

```bash
java -jar application.jar --property.key=value
```

### Ví Dụ Cơ Bản

#### Ghi Đè Build Version

```bash
java -jar accounts-service.jar --build.version=4.0
```

#### Kích Hoạt Profile

```bash
java -jar accounts-service.jar --spring.profiles.active=prod
```

#### Nhiều Thuộc Tính

Phân tách nhiều thuộc tính bằng khoảng trắng:

```bash
java -jar accounts-service.jar \
  --spring.profiles.active=prod \
  --build.version=1.0 \
  --server.port=8081
```

### Ví Dụ Nâng Cao

#### Giá Trị Thuộc Tính Phức Tạp

```bash
java -jar accounts-service.jar \
  --spring.profiles.active=prod \
  --accounts.message="Chào mừng đến APIs Production" \
  --accounts.contactDetails.name="Đội Hỗ Trợ Production"
```

#### Ghi Đè Cấu Hình Database

```bash
java -jar accounts-service.jar \
  --spring.profiles.active=prod \
  --spring.datasource.url=jdbc:mysql://prod-db:3306/accounts \
  --spring.datasource.username=prod_user
```

### Quy Tắc Quan Trọng

1. **Tiền tố**: Luôn sử dụng `--` trước property key
2. **Khoảng cách**: Phân tách nhiều arguments bằng khoảng trắng
3. **Dấu ngoặc kép**: Sử dụng dấu ngoặc kép cho giá trị có khoảng trắng
4. **Định dạng**: `--property.key=value` (không có khoảng trắng xung quanh `=`)

## 2. JVM System Properties (Thuộc Tính Hệ Thống JVM)

### Tổng Quan

JVM system properties cung cấp cấu hình ở cấp độ Java Virtual Machine. Chúng có **ưu tiên thấp hơn command line arguments** nhưng **cao hơn property files**.

### Đặc Điểm

- **Ưu tiên trung bình** - Giữa command line và property files
- **Cấp độ JVM** - Đặt trước khi ứng dụng khởi động
- **Java tiêu chuẩn** - Hoạt động với bất kỳ ứng dụng Java nào

### Cú Pháp

```bash
java -Dproperty.key=value -jar application.jar
```

### Sự Khác Biệt Chính So Với Command Line Arguments

| Tính Năng | Command Line Args | JVM System Properties |
|---------|------------------|----------------------|
| Tiền tố | `--` | `-D` |
| Ưu tiên | Cao nhất | Trung bình |
| Cú pháp | `--key=value` | `-Dkey=value` |
| Vị trí | Sau tên JAR | Trước `-jar` |

### Ví Dụ

#### Kích Hoạt Profile Với JVM Property

```bash
java -Dspring.profiles.active=prod -jar accounts-service.jar
```

#### Nhiều JVM Properties

```bash
java -Dspring.profiles.active=prod \
     -Dbuild.version=1.0 \
     -Dserver.port=8081 \
     -jar accounts-service.jar
```

#### Kết Hợp: JVM Properties và Command Line Arguments

```bash
java -Dspring.profiles.active=qa \
     -jar accounts-service.jar \
     --build.version=2.0
```

**Kết quả**: Profile sẽ là `qa` (từ JVM property), nhưng build version sẽ là `2.0` (command line có ưu tiên cao hơn).

### Khi Cùng Thuộc Tính Được Định Nghĩa Ở Cả Hai

Nếu cùng một thuộc tính được định nghĩa ở cả hai nơi:

```bash
java -Dspring.profiles.active=qa \
     -jar accounts-service.jar \
     --spring.profiles.active=prod
```

**Kết quả**: Profile `prod` sẽ được kích hoạt (command line arguments thắng do có ưu tiên cao hơn).

### Truy Cập JVM Properties Trong Java Code

```java
String profileValue = System.getProperty("spring.profiles.active");
```

## 3. Environment Variables (Biến Môi Trường)

### Tổng Quan

Environment variables được **hỗ trợ phổ biến** trên tất cả các nền tảng và ngôn ngữ lập trình, khiến chúng trở nên lý tưởng cho các ứng dụng containerized và cloud-native.

### Đặc Điểm

- **Hỗ trợ phổ biến** - Hoạt động trên tất cả các ngôn ngữ và nền tảng
- **Thân thiện với Container** - Hoàn hảo cho Docker và Kubernetes
- **Bền vững** - Có thể được đặt ở cấp độ OS
- **Không phụ thuộc ngôn ngữ** - Không đặc biệt cho Java hoặc Spring Boot

### Ưu Điểm

1. **Độc Lập Nền Tảng**: Hoạt động bất kể ngôn ngữ lập trình
2. **Container Native**: Phương pháp tiêu chuẩn trong Docker/Kubernetes
3. **Sẵn Sàng Cloud**: Được hỗ trợ bởi tất cả các nền tảng cloud
4. **Tương Thích Serverless**: Hoạt động với AWS Lambda, Azure Functions, v.v.
5. **Bảo Mật**: Có thể được inject một cách an toàn mà không cần hardcode

### Quy Tắc Đặt Tên

Spring Boot yêu cầu quy ước đặt tên cụ thể cho environment variables:

1. **Chuyển sang CHỮ HOA**: Tất cả các chữ cái phải viết hoa
2. **Thay dấu chấm (.) bằng gạch dưới (_)**
3. **Thay dấu gạch ngang (-) bằng gạch dưới (_)**

### Ví Dụ Chuyển Đổi

| Thuộc tính trong application.yml | Environment Variable |
|----------------------------|---------------------|
| `spring.profiles.active` | `SPRING_PROFILES_ACTIVE` |
| `build.version` | `BUILD_VERSION` |
| `server.port` | `SERVER_PORT` |
| `spring.datasource.url` | `SPRING_DATASOURCE_URL` |
| `accounts.contact-details.name` | `ACCOUNTS_CONTACT_DETAILS_NAME` |

## Đặt Environment Variables

### Windows (PowerShell)

#### Tạm Thời (Phiên Hiện Tại)

```powershell
$env:SPRING_PROFILES_ACTIVE="prod"
$env:BUILD_VERSION="1.0"
java -jar accounts-service.jar
```

#### Vĩnh Viễn (Cấp Độ Hệ Thống)

```powershell
[System.Environment]::SetEnvironmentVariable("SPRING_PROFILES_ACTIVE", "prod", "User")
```

### Windows (Command Prompt)

#### Tạm Thời

```cmd
set SPRING_PROFILES_ACTIVE=prod
set BUILD_VERSION=1.0
java -jar accounts-service.jar
```

#### Thực Thi Inline

```cmd
set SPRING_PROFILES_ACTIVE=prod && java -jar accounts-service.jar
```

### Linux / macOS

#### Tạm Thời (Phiên Hiện Tại)

```bash
export SPRING_PROFILES_ACTIVE=prod
export BUILD_VERSION=1.0
java -jar accounts-service.jar
```

#### Thực Thi Inline (Lệnh Đơn)

```bash
SPRING_PROFILES_ACTIVE=prod BUILD_VERSION=1.0 java -jar accounts-service.jar
```

#### Vĩnh Viễn (User Profile)

Thêm vào `~/.bashrc` hoặc `~/.bash_profile`:

```bash
export SPRING_PROFILES_ACTIVE=prod
export BUILD_VERSION=1.0
```

Sau đó tải lại:
```bash
source ~/.bashrc
```

## Sử Dụng Docker và Container

### Lệnh Docker Run

```bash
docker run -e SPRING_PROFILES_ACTIVE=prod \
           -e BUILD_VERSION=1.0 \
           -e SERVER_PORT=8080 \
           accounts-service:latest
```

### Docker Compose

```yaml
version: '3.8'
services:
  accounts:
    image: accounts-service:latest
    environment:
      - SPRING_PROFILES_ACTIVE=prod
      - BUILD_VERSION=1.0
      - SERVER_PORT=8080
      - SPRING_DATASOURCE_URL=jdbc:mysql://db:3306/accounts
```

### Dockerfile (Build-time)

```dockerfile
FROM openjdk:17-jdk-slim
COPY target/accounts-service.jar app.jar

# Đặt environment variables
ENV SPRING_PROFILES_ACTIVE=prod
ENV BUILD_VERSION=1.0

ENTRYPOINT ["java", "-jar", "/app.jar"]
```

## Cấu Hình Kubernetes

### Deployment Với Environment Variables

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: accounts-service
spec:
  template:
    spec:
      containers:
      - name: accounts
        image: accounts-service:latest
        env:
        - name: SPRING_PROFILES_ACTIVE
          value: "prod"
        - name: BUILD_VERSION
          value: "1.0"
```

### Sử Dụng ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: accounts-config
data:
  SPRING_PROFILES_ACTIVE: "prod"
  BUILD_VERSION: "1.0"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: accounts-service
spec:
  template:
    spec:
      containers:
      - name: accounts
        image: accounts-service:latest
        envFrom:
        - configMapRef:
            name: accounts-config
```

### Sử Dụng Secrets (Dữ Liệu Nhạy Cảm)

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: accounts-secrets
type: Opaque
stringData:
  SPRING_DATASOURCE_USERNAME: "prod_user"
  SPRING_DATASOURCE_PASSWORD: "secure_password"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: accounts-service
spec:
  template:
    spec:
      containers:
      - name: accounts
        image: accounts-service:latest
        envFrom:
        - secretRef:
            name: accounts-secrets
```

## Truy Cập Environment Variables Trong Java

### Sử Dụng System.getenv()

```java
public class ConfigExample {
    public static void main(String[] args) {
        String profile = System.getenv("SPRING_PROFILES_ACTIVE");
        String version = System.getenv("BUILD_VERSION");
        
        System.out.println("Active Profile: " + profile);
        System.out.println("Build Version: " + version);
    }
}
```

### Sử Dụng @Value Annotation Của Spring

```java
@Component
public class AppConfig {
    
    @Value("${spring.profiles.active:default}")
    private String activeProfile;
    
    @Value("${build.version}")
    private String buildVersion;
    
    public void printConfig() {
        System.out.println("Profile: " + activeProfile);
        System.out.println("Version: " + buildVersion);
    }
}
```

### Sử Dụng Spring Environment

```java
@Component
public class ConfigService {
    
    @Autowired
    private Environment env;
    
    public void displayConfig() {
        String profile = env.getProperty("spring.profiles.active");
        String version = env.getProperty("build.version");
        
        System.out.println("Active Profile: " + profile);
        System.out.println("Build Version: " + version);
    }
}
```

## Ví Dụ Về Thứ Tự Ưu Tiên Hoàn Chỉnh

Cho các nguồn cấu hình sau:

**application.yml:**
```yaml
build:
  version: "3.0"
```

**application-prod.yml:**
```yaml
build:
  version: "1.0"
```

**Environment Variable:**
```bash
BUILD_VERSION=2.0
```

**JVM System Property:**
```bash
-Dbuild.version=2.5
```

**Command Line Argument:**
```bash
--build.version=4.0
```

**Kết quả**: `build.version = "4.0"` (Command line có ưu tiên cao nhất)

## Thực Hành Tốt Nhất

### 1. Chọn Phương Pháp Phù Hợp

- **Phát triển**: Sử dụng `application.yml` hoặc cấu hình IDE
- **Testing/QA**: Sử dụng environment variables hoặc command line
- **Production**: Sử dụng environment variables (Docker/Kubernetes)
- **Nền tảng Cloud**: Sử dụng dịch vụ cấu hình đặc thù của nền tảng

### 2. Cân Nhắc Bảo Mật

- **Không bao giờ hardcode** thông tin xác thực nhạy cảm trong property files
- **Sử dụng environment variables** cho secrets
- **Sử dụng công cụ quản lý secrets** (Vault, AWS Secrets Manager)
- **Kubernetes Secrets** cho triển khai container

### 3. Tài Liệu

- Ghi chép phương pháp cấu hình được sử dụng trong mỗi môi trường
- Duy trì hướng dẫn cấu hình cho đội vận hành
- Liệt kê tất cả các environment variables cần thiết

### 4. Kiểm Thử

- Kiểm tra cấu hình trong mỗi môi trường trước khi triển khai
- Xác minh thứ tự ưu tiên hoạt động như mong đợi
- Kiểm tra cấu hình bên ngoài ghi đè đúng cách

## Tóm Tắt

### So Sánh Các Phương Pháp Cấu Hình

| Phương Pháp | Ưu Tiên | Trường Hợp Sử Dụng | Nền Tảng |
|--------|-----------|----------|----------|
| Command Line | Cao nhất | Kiểm tra nhanh, ghi đè | Bất kỳ |
| JVM Properties | Cao | Cấu hình đặc thù JVM | Chỉ Java |
| Environment Variables | Trung bình | Containers, cloud, production | Phổ biến |
| Profile Files | Thấp | Mặc định theo môi trường | Spring Boot |
| Default Properties | Thấp nhất | Mặc định ứng dụng | Spring Boot |

### Điểm Chính Cần Nhớ

✅ **Externalize tất cả cấu hình theo môi trường**
✅ **Không bao giờ rebuild artifacts cho các môi trường khác nhau**
✅ **Sử dụng environment variables cho triển khai production**
✅ **Command line arguments có ưu tiên cao nhất**
✅ **Tuân theo phương pháp 12-Factor App cho ứng dụng cloud-native**

## Các Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ:
- **Minh họa** tất cả các phương pháp externalization này
- **Kích hoạt profiles** bằng các phương pháp khác nhau
- **Kiểm tra thứ tự ưu tiên** với các ví dụ thực tế
- **Triển khai** microservices với cấu hình bên ngoài

---

**Ghi Nhớ**: Xây dựng một lần, cấu hình mọi nơi - chìa khóa cho triển khai immutable!