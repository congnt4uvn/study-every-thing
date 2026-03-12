# Quản Lý Thư Viện Dùng Chung với Maven Multi-Modules trong Microservices

## Tổng Quan

Hướng dẫn này trình bày cách tạo và quản lý các thư viện dùng chung trong kiến trúc microservices bằng cách sử dụng dự án Maven multi-module. Thay vì nhân bản code trên nhiều microservices, chúng ta sẽ sử dụng phương pháp Bill of Materials (BOM) với các submodule để chia sẻ code chung một cách hiệu quả.

## Tạo Cấu Trúc Multi-Module

### Bước 1: Tạo Submodule Common

1. Click chuột phải vào dự án `eazy-bom` và chọn **New Module**
2. Cấu hình module với các thiết lập sau:
   - **Tên Module**: `common` (có thể tùy chỉnh theo yêu cầu)
   - **Ngôn Ngữ**: Java
   - **Loại**: Maven
   - **Group**: `com.eazybytes`
   - **Artifact**: `common`
   - **JDK**: 21
   - **Phiên Bản Java**: 21
   - **Packaging**: jar

3. Thêm các dependency cần thiết:
   - Spring Web
   - Lombok

4. Click **Create** để tạo submodule trong `eazy-bom`

### Bước 2: Cấu Hình Parent POM

Trong file `eazy-bom/pom.xml`, thêm phần modules sau phần properties:

```xml
<modules>
    <module>common</module>
</modules>
```

Định nghĩa thuộc tính version cho module common:

```xml
<properties>
    <common-jib.version>1.0.0</common-jib.version>
</properties>
```

### Bước 3: Cấu Hình POM của Common Submodule

Trong file `common/pom.xml`, thực hiện các thay đổi sau:

1. Thay thế Spring Boot parent bằng tham chiếu đến eazy-bom parent
2. Cập nhật version để sử dụng thuộc tính:
   ```xml
   <version>${common-jib.version}</version>
   ```

3. Cập nhật phần mô tả:
   ```xml
   <description>Common project cho eazybank microservices</description>
   ```

4. Thêm dependency SpringDoc cho các annotation OpenAPI:
   ```xml
   <dependency>
       <groupId>org.springdoc</groupId>
       <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
   </dependency>
   ```

5. Cấu hình Lombok để sử dụng version từ parent POM

6. Xóa cấu hình build (đã có trong parent POM)

7. Xóa dependency Spring Boot Starter Test (đã có trong parent POM)

8. Xóa tất cả chi tiết properties vì chúng được kế thừa từ parent

## Di Chuyển Code Dùng Chung vào Common Module

### Bước 1: Chuẩn Bị Cấu Trúc Common Module

1. Xóa file `CommonApplication.java` (chúng ta không muốn submodule có thể thực thi)
2. Tạo package mới: `dto`

### Bước 2: Di Chuyển ErrorResponseDto

1. Copy `ErrorResponseDto` từ bất kỳ microservice nào
2. Paste vào module `common` trong package `dto`
3. Xóa `ErrorResponseDto` khỏi tất cả các microservices:
   - Accounts microservice
   - Cards microservice
   - Loans microservice

## Thêm Common Dependency vào Các Microservices

Mỗi microservice cần thư viện common phải thêm nó như một dependency trong `pom.xml`:

```xml
<dependency>
    <groupId>com.eazybytes</groupId>
    <artifactId>common</artifactId>
    <version>${common-jib.version}</version>
</dependency>
```

Thêm dependency này vào:
- Accounts microservice
- Loans microservice
- Cards microservice

Sau khi thêm dependency, load lại các thay đổi Maven trong mỗi microservice.

## Khắc Phục Lỗi Biên Dịch

Nếu bạn gặp lỗi biên dịch sau khi di chuyển code dùng chung:

1. Cập nhật các câu lệnh import trong các class sử dụng `ErrorResponseDto`:
   - `GlobalExceptionHandler`
   - Controllers (Accounts, Loans, Cards)

2. Mở các file bị ảnh hưởng và save lại để kích hoạt tự động giải quyết

3. Rebuild dự án để xác minh tất cả lỗi đã được giải quyết

## Publish Common Module

Để publish module common vào local Maven repository:

```bash
cd common
mvn clean install
```

Lệnh này sẽ:
- Build module common
- Publish JAR vào local Maven repository
- Làm cho nó có sẵn cho việc tạo Docker image và các build khác

JAR sẽ có sẵn trong local Maven repository (thường là `~/.m2/repository` hoặc `%USERPROFILE%\.m2\repository`).

## Tạo Docker Images

Sau khi build thành công module common, bạn có thể tạo Docker images cho các microservices:

```bash
cd accounts
mvn compile jib:dockerBuild
```

Quá trình tạo image sẽ lấy JAR của module common từ local Maven repository.

## Best Practices

1. **Nhiều Submodules**: Bạn có thể tạo nhiều submodule dưới `eazy-bom` cho các mục đích khác nhau:
   - Security
   - Logging
   - Auditing
   - Common utilities

2. **Tránh Single Jumbo Modules**: Đừng tạo một Maven module lớn duy nhất. Chia chức năng thành các module tập trung, có mục đích cụ thể.

3. **Cẩn Thận**: Mặc dù phương pháp này giảm việc nhân bản code, hãy cẩn thận để không tạo ra:
   - Thách thức về deployment
   - Sự liên kết chặt chẽ giữa các microservices
   - Shared state hoặc dependencies vi phạm nguyên tắc microservices

4. **Quản Lý Version**: Sử dụng properties trong parent POM để quản lý version một cách nhất quán trên tất cả các module

## Lợi Ích

- **Tái Sử Dụng Code**: Viết một lần, sử dụng trên nhiều microservices
- **Tính Nhất Quán**: Các model và utilities dùng chung đảm bảo hành vi nhất quán
- **Khả Năng Bảo Trì**: Cập nhật code dùng chung ở một nơi
- **Type Safety**: Kiểm tra tại thời điểm biên dịch trên các microservices

## Tóm Tắt

Phương pháp này cho phép bạn tạo các thư viện dùng chung cho microservices của mình trong khi vẫn duy trì lợi ích của việc triển khai độc lập và khả năng mở rộng. Bằng cách sử dụng Maven multi-modules và BOM files, bạn có thể quản lý dependencies hiệu quả và giảm việc nhân bản code mà không tạo ra sự liên kết chặt chẽ.

Hãy luôn cân nhắc sự đánh đổi giữa việc tái sử dụng code và tính độc lập của microservices khi quyết định những gì cần chia sẻ giữa các services.