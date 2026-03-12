# Quản Lý Dependencies với BOM trong Spring Boot Microservices

## Tổng Quan

Hướng dẫn này trình bày cách hợp lý hóa quản lý dependencies trên nhiều microservices bằng cách sử dụng phương pháp Bill of Materials (BOM). Bằng cách tập trung kiểm soát phiên bản trong file BOM cha, bạn có thể quản lý dependencies hiệu quả hơn và duy trì tính nhất quán trên tất cả các microservices.

## BOM (Bill of Materials) là gì?

Bill of Materials (BOM) là một loại file POM đặc biệt giúp tập trung quản lý phiên bản dependencies. Thay vì định nghĩa phiên bản trong từng microservice riêng lẻ, bạn định nghĩa chúng một lần trong file BOM cha, giúp bạn kiểm soát tập trung tất cả các phiên bản dependencies.

## Lợi Ích của Việc Sử Dụng BOM

- **Kiểm Soát Phiên Bản Tập Trung**: Quản lý tất cả phiên bản dependencies tại một vị trí duy nhất
- **Tính Nhất Quán**: Đảm bảo tất cả microservices sử dụng các phiên bản tương thích
- **Cập Nhật Dễ Dàng**: Thay đổi phiên bản một lần trong file BOM thay vì cập nhật từng microservice
- **Giảm Trùng Lặp**: Loại bỏ các số phiên bản hardcode trên các microservices
- **Bảo Trì Đơn Giản**: Hợp lý hóa quy trình phát triển và triển khai

## Các Bước Triển Khai

### 1. Tạo Dự Án BOM

Đầu tiên, tạo một dự án BOM chuyên dụng (ví dụ: `eazy-bom`) với file `pom.xml` định nghĩa tất cả các dependencies chung và phiên bản của chúng.

**Các yếu tố chính trong pom.xml của BOM:**
- Định nghĩa properties cho tất cả phiên bản dependencies
- Sử dụng `<dependencyManagement>` để import Spring Boot và Spring Cloud BOMs
- Thiết lập cấu hình chung như phiên bản Java, image tags và phiên bản plugins

### 2. Cấu Hình Microservices Sử Dụng BOM

**Bước 1: Cập Nhật Khai Báo Parent**

Thay thế Spring Boot parent chuẩn bằng BOM parent của bạn:

```xml
<parent>
    <groupId>com.example</groupId>
    <artifactId>eazy-bom</artifactId>
    <version>1.0.0</version>
    <relativePath>../eazy-bom/pom.xml</relativePath>
</parent>
```

**Quan trọng**: `<relativePath>` phải trỏ đến vị trí pom.xml của BOM tương đối với microservice.

**Bước 2: Xóa Phần Properties**

Xóa phần properties khỏi pom.xml của microservice, vì chúng đã được định nghĩa trong BOM cha.

**Bước 3: Cập Nhật Dependencies**

Đối với dependencies, tuân theo các quy tắc sau:

- **Spring Boot dependencies**: Không cần phiên bản (kế thừa từ BOM)
  ```xml
  <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-actuator</artifactId>
  </dependency>
  ```

- **Third-party dependencies**: Tham chiếu các properties phiên bản từ BOM
  ```xml
  <dependency>
      <groupId>io.opentelemetry</groupId>
      <artifactId>opentelemetry-api</artifactId>
      <version>${otel.version}</version>
  </dependency>
  ```

**Bước 4: Cập Nhật Build Plugins**

Tham chiếu phiên bản plugins từ properties của BOM:

```xml
<plugin>
    <groupId>com.google.cloud.tools</groupId>
    <artifactId>jib-maven-plugin</artifactId>
    <version>${jib.version}</version>
    <configuration>
        <to>
            <image>username/microservice-name:${image.tag}</image>
        </to>
    </configuration>
</plugin>
```

**Bước 5: Xóa Dependency Management Trùng Lặp**

Xóa phần `<dependencyManagement>` khỏi microservices vì nó đã có trong BOM.

## Ví Dụ: Migration Accounts Microservice

### Trước (với Spring Boot Parent):
```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.3.3</version>
</parent>

<properties>
    <java.version>17</java.version>
    <spring-cloud.version>2023.0.0</spring-cloud.version>
    <!-- ... nhiều properties khác ... -->
</properties>
```

### Sau (với BOM Parent):
```xml
<parent>
    <groupId>com.example</groupId>
    <artifactId>eazy-bom</artifactId>
    <version>1.0.0</version>
    <relativePath>../eazy-bom/pom.xml</relativePath>
</parent>

<!-- Không cần phần properties -->
```

## Các Properties Thường Được Quản Lý trong BOM

BOM thường quản lý các properties sau:

- **spring-boot.version**: Phiên bản Spring Boot framework
- **spring-cloud.version**: Phiên bản Spring Cloud
- **java.version**: Phiên bản ngôn ngữ Java
- **maven.compiler.source**: Phiên bản source của Maven compiler
- **maven.compiler.target**: Phiên bản target của Maven compiler
- **otel.version**: Phiên bản OpenTelemetry
- **micrometer.version**: Phiên bản Micrometer metrics
- **h2.version**: Phiên bản H2 database
- **lombok.version**: Phiên bản Lombok
- **spring-doc.version**: Phiên bản SpringDoc OpenAPI
- **jib.version**: Phiên bản Google Jib plugin
- **image.tag**: Docker image tag cho tất cả microservices

## Hiểu về Spring Boot BOM Import

Khi bạn import Spring Boot dependencies trong BOM của mình:

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-dependencies</artifactId>
            <version>${spring-boot.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

Điều này **không** tự động thêm tất cả Spring Boot dependencies vào microservices của bạn. Thay vào đó:

1. BOM import các phiên bản Spring Boot dependency
2. Mỗi microservice khai báo các dependencies cụ thể mà nó cần
3. Các phiên bản được kế thừa từ BOM
4. Chỉ các dependencies được khai báo mới được tải xuống

Cách tiếp cận này cho bạn quyền kiểm soát dependencies nào mà mỗi microservice sử dụng trong khi vẫn duy trì tính nhất quán về phiên bản.

## Kiểm Tra Cấu Hình BOM

### 1. Reload Maven Projects
Sau khi thực hiện thay đổi, reload tất cả Maven projects trong IDE để đảm bảo không có lỗi biên dịch.

### 2. Test một Microservice
Khởi động một microservice đơn giản (ví dụ: Config Server) để xác minh nó chạy đúng với cấu hình BOM.

### 3. Test Thay Đổi Phiên Bản
Để xác minh BOM đang hoạt động:
1. Thay đổi một phiên bản trong BOM (ví dụ: Spring Boot version từ 3.3.3 sang 3.3.2)
2. Xóa thư mục `target` trong microservice
3. Reload Maven projects
4. Khởi động microservice và kiểm tra nó sử dụng phiên bản mới

**Lưu ý**: Nếu thay đổi không được áp dụng, hãy thử:
- Reload Maven projects nhiều lần
- Xóa Maven cache
- Khởi động lại IDE

## Best Practices (Thực Hành Tốt Nhất)

### 1. Chiến Lược Kiểm Soát Phiên Bản
- **Spring Boot/Cloud**: Quản lý trong BOM, không cần phiên bản trong microservices
- **Third-party libraries**: Định nghĩa properties phiên bản trong BOM, tham chiếu trong microservices
- Điều này cho bạn quyền kiểm soát rõ ràng đối với phiên bản third-party dependencies

### 2. Cấu Hình Relative Path
Luôn chỉ định `<relativePath>` trong khai báo parent, đặc biệt cho CI/CD pipelines:
```xml
<relativePath>../eazy-bom/pom.xml</relativePath>
```

### 3. Quản Lý Image Tag
Sử dụng property image tag chung (ví dụ: `image.tag`) để duy trì versioning nhất quán trên tất cả Docker images của microservices.

### 4. Migration Từng Bước
Migrate từng microservice một để kiểm tra cấu hình BOM trước khi áp dụng cho tất cả microservices.

## Xử Lý Sự Cố

### IDE Không Nhận Diện BOM
- Đảm bảo relative path đúng
- Reload Maven projects
- Khởi động lại IDE

### Xung Đột Phiên Bản
- Kiểm tra tất cả microservices tham chiếu cùng phiên bản BOM
- Xác minh không có phiên bản hardcode ghi đè cài đặt BOM

### Vấn Đề Maven Cache
- Chạy `mvn clean install` trong dự án BOM trước
- Xóa local Maven repository cache nếu cần
- Sử dụng chức năng "Reload All Maven Projects" của IDE

## Kết Luận

Triển khai cấu trúc BOM cho kiến trúc microservices của bạn mang lại:

- **Kiểm soát tập trung** đối với tất cả phiên bản dependencies
- **Bảo trì đơn giản** khi cập nhật phiên bản
- **Tính nhất quán** trên tất cả microservices
- **Giảm lỗi** do không khớp phiên bản
- **Hợp lý hóa** quy trình phát triển

Bằng cách tuân theo phương pháp này, bạn có thể quản lý dependencies hiệu quả trên toàn bộ hệ sinh thái microservices của mình từ một vị trí duy nhất.

---

*Hướng dẫn này dựa trên Spring Boot 3.x và Spring Cloud 2023.x. Điều chỉnh cấu hình theo phiên bản và yêu cầu cụ thể của bạn.*